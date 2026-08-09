"""lib29fe — mg-29fe's INDEPENDENT instrument for the audit of mg-28ff.

Written from the DEFINITIONS in `docs/OneThird-C3-PrefixCapture-mg-76b2.md` (Lemma 2.1,
Lemma 3.1, §4) and from `Op-Form`, NOT from `code/l2_conditionality_28ff/lib28ff.py`,
which was deliberately not opened until this file produced its numbers (PREDICTIONS E5).

DEFINITIONS USED (all re-derived here from the corpus, none copied):

  * Population: posets `P` on `{0,..,n-1}` for which the IDENTITY is a linear extension
    ("naturally labelled").  Counted here, not assumed.
  * `pos(i)`  — position of element `i` in a uniform random linear extension `sigma`.
  * `(S_P)_{ij} = Pr[pos(j) = i]`; doubly stochastic.  `a_ij = (S_ij + S_ji)/2` for `i != j`.
  * `E(f) = <f,(I-S)f> = sum_{i<j} a_ij (f_i - f_j)^2`.
  * `d_i = 1 - (S_P)_ii = Pr[pos(i) != i]`,  `Delta_P = max_i d_i`.
  * `leak(A) = E|A \\ sigma(A)| = <1_A,(I-S)1_A>`;  for `A_k = {0..k-1}`,
    `leak(A_k) = E #{i < k : pos(i) >= k}`.
  * `Phi_P(A) = leak(A) / min(|A|, n-|A|)`;  `Phi*_pref = min_k Phi_P(A_k)`.
  * `1 - lambda_std = min_{f perp 1} E(f)/||f||^2`.
  * `mu_pref     = min{ E(g)/||g||^2 : g perp 1, g nondecreasing along e }`.

EXACTNESS.  Every decision-path quantity is a `Fraction`.  The PSD test is BRUTE-FORCE
PRINCIPAL MINORS (`M >= 0` iff every elementary symmetric function of its eigenvalues,
i.e. every principal-minor sum `e_k`, is `>= 0`).  This is deliberately NOT
Faddeev-LeVerrier: mg-28ff's E3 records a sign error in exactly that routine, and an
auditor reusing the same algorithm inherits the same failure mode.  Floats appear only in
the SEARCH for cone minimisers, never on a verdict path.
"""

from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache

# ----------------------------------------------------------------- posets

def transitive_closed(n, rel):
    """rel: frozenset of (i,j) with i<j.  True iff transitively closed."""
    for (i, j) in rel:
        for (k, l) in rel:
            if j == k and (i, l) not in rel:
                return False
    return True


def all_natural_posets(n):
    """Every poset on [n] whose identity permutation is a linear extension.

    A relation set on the pairs i<j is a poset iff it is transitively closed
    (irreflexivity and antisymmetry are automatic because every pair points upward).
    """
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(pairs)
    out = []
    for mask in range(1 << m):
        rel = frozenset(pairs[b] for b in range(m) if mask >> b & 1)
        if transitive_closed(n, rel):
            out.append(rel)
    return out


def natural_posets_sample(n, k, seed=12345):
    """A DETERMINISTIC sample of `k` naturally labelled posets on [n].

    Fixed LCG, no `random` module.  Rejection-samples transitively closed relation sets.
    EVERY figure derived from this is a SAMPLE and is labelled as such at its use site.
    """
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(pairs)
    state = seed
    seen, out = set(), []
    tries = 0
    while len(out) < k and tries < 4000000:
        tries += 1
        state = (1103515245 * state + 12345) % (1 << 31)
        mask = state % (1 << m)
        rel = frozenset(pairs[b] for b in range(m) if mask >> b & 1)
        if rel in seen or not transitive_closed(n, rel):
            continue
        seen.add(rel)
        out.append(rel)
    return out


def linear_extensions(n, rel):
    """All linear extensions, each as a tuple `perm` with perm[t] = element at position t."""
    below = [0] * n            # bitmask of elements that must precede i
    for (i, j) in rel:
        below[j] |= 1 << i
    res = []
    order = []

    def rec(placed):
        if placed == (1 << n) - 1:
            res.append(tuple(order))
            return
        for i in range(n):
            if placed >> i & 1:
                continue
            if below[i] & ~placed:
                continue
            order.append(i)
            rec(placed | 1 << i)
            order.pop()

    rec(0)
    return res


def is_decomposable(n, rel):
    """P is an ordinal sum at k iff every element < k is below every element >= k."""
    for k in range(1, n):
        if all((i, j) in rel for i in range(k) for j in range(k, n)):
            return True
    return False


# ----------------------------------------------------------------- statistics

class Poset:
    """Everything the audit needs about one poset, in exact rationals."""

    def __init__(self, n, rel):
        self.n, self.rel = n, rel
        les = linear_extensions(n, rel)
        self.N = len(les)
        N = self.N

        # counts[i][j] = # of linear extensions with pos(j) = i
        counts = [[0] * n for _ in range(n)]
        leak_ct = [0] * n           # leak_ct[k] = sum over LEs of #{i<k : pos(i)>=k}
        dfoot = 0                   # sum over LEs of sum_i |i - pos(i)|
        for perm in les:
            pos = [0] * n
            for t, el in enumerate(perm):
                pos[el] = t
            for j in range(n):
                counts[pos[j]][j] += 1
                dfoot += abs(j - pos[j])
            for k in range(1, n):
                leak_ct[k] += sum(1 for i in range(k) if pos[i] >= k)

        self.S = [[F(counts[i][j], N) for j in range(n)] for i in range(n)]
        self.a = [[(self.S[i][j] + self.S[j][i]) / 2 if i != j else F(0)
                   for j in range(n)] for i in range(n)]
        self.d = [F(1) - self.S[i][i] for i in range(n)]
        self.Delta = max(self.d)
        self.leak = [F(leak_ct[k], N) for k in range(n)]      # leak[0] unused
        self.EDF = F(dfoot, N)
        self.decomposable = is_decomposable(n, rel)

    # ---- energy / matrices

    def L(self):
        """I - S, symmetrised: L[i][i] = d_i, L[i][j] = -a_ij."""
        n = self.n
        return [[self.d[i] if i == j else -self.a[i][j] for j in range(n)]
                for i in range(n)]

    def energy(self, f):
        n = self.n
        return sum(self.a[i][j] * (f[i] - f[j]) ** 2
                   for i in range(n) for j in range(i + 1, n))

    def rayleigh(self, f):
        """R(f) for f perp 1 (caller centres it)."""
        n = self.n
        mean = sum(f, F(0)) / n
        g = [x - mean for x in f]
        nrm = sum(x * x for x in g)
        if nrm == 0:
            return None
        return self.energy(g) / nrm

    # ---- conductance

    def Phi(self, k):
        return self.leak[k] / min(k, self.n - k)

    def Phi_star_pref(self):
        return min(self.Phi(k) for k in range(1, self.n))

    def Phi_star_all(self):
        """min over ALL cuts (used only for the R2 control)."""
        n = self.n
        best = None
        for size in range(1, n):
            for A in combinations(range(n), size):
                Aset = set(A)
                ind = [F(1) if i in Aset else F(0) for i in range(n)]
                lk = quad(self.L(), ind)
                v = lk / min(size, n - size)
                if best is None or v < best:
                    best = v
        return best


def quad(M, f):
    n = len(f)
    return sum(f[i] * M[i][j] * f[j] for i in range(n) for j in range(n))


# ----------------------------------------------------------------- exact PSD

def det_frac(M):
    """Exact determinant by fraction-free-ish Gaussian elimination on Fractions."""
    n = len(M)
    A = [row[:] for row in M]
    det = F(1)
    for c in range(n):
        piv = None
        for r in range(c, n):
            if A[r][c] != 0:
                piv = r
                break
        if piv is None:
            return F(0)
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            det = -det
        det *= A[c][c]
        inv = F(1) / A[c][c]
        for r in range(c + 1, n):
            if A[r][c] == 0:
                continue
            fac = A[r][c] * inv
            for cc in range(c, n):
                A[r][cc] -= fac * A[c][cc]
    return det


def is_psd(M):
    """EXACT.  M symmetric rational is PSD iff every principal-minor sum e_k >= 0.

    e_k = sum over |T|=k of det(M_T) is the k-th elementary symmetric function of the
    eigenvalues; det(xI+M) = sum_k e_k x^{n-k}, and a monic polynomial with all
    coefficients >= 0 has no positive real root, so no eigenvalue can be negative.
    Brute force over all 2^n principal submatrices: n <= 7 here, so this is cheap AND
    it shares no algorithm with the parent's Faddeev-LeVerrier (whose sign convention
    is where mg-28ff's E3 fired).
    """
    n = len(M)
    for k in range(1, n + 1):
        e = F(0)
        for T in combinations(range(n), k):
            e += det_frac([[M[i][j] for j in T] for i in T])
        if e < 0:
            return False
    return True


def is_psd_fast(M):
    """EXACT PSD test by symmetric Gaussian elimination (O(n^3)).

    For a SYMMETRIC matrix: M >= 0 iff at every step the pivot is >= 0, and whenever a
    pivot is 0 the whole remaining row/column is 0.  Used on the hot path; arm A3j of
    the selftest asserts it agrees with `is_psd` (brute-force principal minors) on every
    matrix the sweep actually tests, so the fast path cannot drift from the slow one.
    """
    n = len(M)
    A = [row[:] for row in M]
    for c in range(n):
        if A[c][c] < 0:
            return False
        if A[c][c] == 0:
            for r in range(c, n):
                if A[c][r] != 0 or A[r][c] != 0:
                    return False
            continue
        inv = F(1) / A[c][c]
        for r in range(c + 1, n):
            if A[r][c] == 0:
                continue
            fac = A[r][c] * inv
            for cc in range(c, n):
                A[r][cc] -= fac * A[c][cc]
    return True


def gap_at_least(P, t, fast=True):
    """EXACT: is 1 - lambda_std >= t?   <=>  (I-S) - t(I - J/n) PSD."""
    n = P.n
    L = P.L()
    M = [[L[i][j] - t * ((F(1) if i == j else F(0)) - F(1, n)) for j in range(n)]
         for i in range(n)]
    return is_psd_fast(M) if fast else is_psd(M)


def bracket_gap(P, iters=30, fast=True):
    """EXACT rational bracket [lo, hi] for 1 - lambda_std.  No float anywhere.

    Bisection is on DYADIC rationals so denominators stay small; `iters` steps give a
    bracket of width 2^-iters.  Every claim built on this states which end it uses and
    in which direction that end is conservative.
    """
    lo, hi = F(0), F(2)
    if not gap_at_least(P, F(1, 10 ** 9), fast):
        return F(0), F(1, 10 ** 9)          # decomposable / zero gap
    for _ in range(iters):
        mid = (lo + hi) / 2
        if gap_at_least(P, mid, fast):
            lo = mid
        else:
            hi = mid
    return lo, hi


# ----------------------------------------------------------------- monotone cone

def psi_basis(n):
    """psi_k(i) = k/n - [i<k], k = 1..n-1.  Spans 1^perp; nonneg combos = monotone cone."""
    return [[F(k, n) - (F(1) if i < k else F(0)) for i in range(n)] for k in range(1, n)]


def cone_QN(P):
    """Q = psi^T (I-S) psi  and  N = psi^T psi, both EXACT, from the DEFINITIONS."""
    n = P.n
    psi = psi_basis(n)
    L = P.L()
    m = n - 1
    Q = [[sum(psi[k][i] * L[i][j] * psi[l][j] for i in range(n) for j in range(n))
          for l in range(m)] for k in range(m)]
    N = [[sum(psi[k][i] * psi[l][i] for i in range(n)) for l in range(m)]
         for k in range(m)]
    return Q, N


def cone_QN_closedform(P):
    """mg-28ff's claimed closed forms, recomputed here so the CHECK is independent."""
    n = P.n
    m = n - 1
    Q = [[sum(P.a[i][j]
              for i in range(min(k + 1, l + 1))
              for j in range(max(k + 1, l + 1), n))
          for l in range(m)] for k in range(m)]
    N = [[F(min(k + 1, l + 1)) - F((k + 1) * (l + 1), n) for l in range(m)]
         for k in range(m)]
    return Q, N


def mu_pref_float(P):
    """Cone minimum of the Rayleigh quotient.  FLOAT SEARCH — a measurement.

    Enumerates the faces of the cone (supports) and takes the smallest generalized
    eigenpair on each; the cone minimum is attained at a face where the restricted
    minimiser is nonnegative.  Returns (value, rational vector g) with g re-verified
    exactly by the caller.
    """
    import numpy as np
    n = P.n
    Q, N = cone_QN(P)
    m = n - 1
    Qf = np.array([[float(x) for x in row] for row in Q])
    Nf = np.array([[float(x) for x in row] for row in N])
    psi = psi_basis(n)
    best, bestc = None, None
    for r in range(1, m + 1):
        for T in combinations(range(m), r):
            idx = list(T)
            A = Qf[np.ix_(idx, idx)]
            B = Nf[np.ix_(idx, idx)]
            try:
                Bi = np.linalg.inv(B)
                w, V = np.linalg.eig(Bi @ A)
            except np.linalg.LinAlgError:
                continue
            order = np.argsort(w.real)
            for oi in order:
                if abs(w[oi].imag) > 1e-9:
                    continue
                v = V[:, oi].real
                if v.max() < -v.min():
                    v = -v
                if v.min() < -1e-9:
                    continue
                val = float(w[oi].real)
                if best is None or val < best - 1e-15:
                    c = [0.0] * m
                    for p, i in enumerate(idx):
                        c[i] = max(v[p], 0.0)
                    best, bestc = val, c
                break
    if bestc is None:
        return None, None
    g = [sum(F(round(bestc[k] * 10 ** 6), 10 ** 6) * psi[k][i] for k in range(m))
         for i in range(n)]
    return best, g


def monotone(g):
    return all(g[i] <= g[i + 1] for i in range(len(g) - 1))


# ----------------------------------------------------------------- exact cone minimum

def mat_inv(M):
    """Exact inverse of a rational matrix, or None if singular."""
    n = len(M)
    A = [row[:] + [F(1) if i == j else F(0) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        piv = None
        for r in range(c, n):
            if A[r][c] != 0:
                piv = r
                break
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        inv = F(1) / A[c][c]
        A[c] = [x * inv for x in A[c]]
        for r in range(n):
            if r == c or A[r][c] == 0:
                continue
            fac = A[r][c]
            A[r] = [A[r][k] - fac * A[c][k] for k in range(2 * n)]
    return [row[n:] for row in A]


def min_on_simplex(M):
    """EXACT  min { c^T M c : c >= 0, sum c = 1 }  for small symmetric rational M.

    The minimiser has some support T, and on the relative interior of that face the
    KKT/stationarity condition is `M_T c_T = mu * 1`, giving value `mu = 1/(1^T M_T^-1 1)`
    and `c_T = M_T^-1 1 / (1^T M_T^-1 1)`.  Enumerating every support T covers the
    boundary too, so the minimum over all FEASIBLE (c_T >= 0) candidates is the global
    minimum.  Singular faces are skipped: their minimum is attained on a sub-face, which
    is itself enumerated.  Vertices (|T| = 1) are always feasible, so the candidate set
    is never empty.
    """
    m = len(M)
    best = None
    for r in range(1, m + 1):
        for T in combinations(range(m), r):
            MT = [[M[i][j] for j in T] for i in T]
            Mi = mat_inv(MT)
            if Mi is None:
                continue
            s = sum(sum(row) for row in Mi)
            if s == 0:
                continue
            mu = F(1) / s
            c = [sum(row) * mu for row in Mi]
            if any(x < 0 for x in c):
                continue
            if best is None or mu < best:
                best = mu
    return best


def is_copositive(M):
    """EXACT: M symmetric rational is copositive iff min over the simplex is >= 0."""
    v = min_on_simplex(M)
    return v is not None and v >= 0


def mu_pref_at_least(P, t, QN=None):
    """EXACT: is mu_pref >= t?   <=>  Q - tN copositive over the monotone cone."""
    Q, N = QN if QN else cone_QN(P)
    m = len(Q)
    return is_copositive([[Q[i][j] - t * N[i][j] for j in range(m)] for i in range(m)])


def bracket_mu_pref(P, iters=30):
    """EXACT rational bracket [lo, hi] for mu_pref.  No float on any decision path.

    This is STRICTLY STRONGER than mg-28ff, which computes mu_pref by a float support
    enumeration plus a float generalized eigenproblem and labels the extremal direction
    a MEASUREMENT (§6, §10).  Here both directions are exact.
    """
    QN = cone_QN(P)
    lo, hi = F(0), F(2)
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mu_pref_at_least(P, mid, QN):
            lo = mid
        else:
            hi = mid
    return lo, hi
