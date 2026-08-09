"""lib28ff — the instrument for mg-28ff (ATTACK THE L2 CONDITIONALITY, branch C).

Written from scratch for this ticket.  It shares NO code with `lib76b2`, `libA94`,
`lib_d3c7`, `lib3969` or `core.py`.  The reason is not hygiene theatre: this ticket's job
is to decide whether `mg-76b2`'s theorem survives without its hypothesis, and an instrument
that inherits `mg-76b2`'s library cannot find a defect that lives in that library.

DESIGN COMMITMENTS  (PREDICTIONS.md E3)
---------------------------------------
* **No float ever decides a verdict.**  Every published inequality is settled in exact
  `Fraction` arithmetic.  The one genuinely spectral comparison, `r <= 1 - lambda_std`, is
  decided WITHOUT computing `lambda_std`: it is equivalent to positive semidefiniteness of
  `(I - S_P) - r*(I - J/n)`, and PSD of a rational symmetric matrix is decided exactly by
  the signs of its characteristic polynomial's coefficients (`psd_exact`).
* Floats appear only in `jacobi` / `cone_min`, whose job is to FIND candidate vectors.
  Every candidate is then rationalised and re-verified exactly before it is believed.
* Every count names its population at the print site.

THE OBJECTS  (all from the source's own definitions, restated here)
------------------------------------------------------------------
`P` is a poset on `{0..n-1}` whose identity permutation is the distinguished linear
extension `e`.  `T[x][a] = Pr[x occupies position a]` under a uniform random linear
extension; `S_P = (T + T^T)/2`; `a_ij = (S_P)_ij` for `i != j` are the weights of a graph
whose combinatorial Laplacian is exactly `I - S_P` (the diagonal works out because `T` is
doubly stochastic).  `lambda_std` is the top eigenvalue of `S_P` on `H = 1^perp`, so
`1 - lambda_std` is the algebraic connectivity of that graph.
`Phi_P(A) = E|A \\ sigma(A)| / min(|A|, n-|A|)`, and `E|A \\ sigma(A)| = w(A, A^c)`.
"""

from fractions import Fraction as F
from itertools import combinations, permutations
import math

# --------------------------------------------------------------------- posets


class Poset:
    """Poset on {0..n-1} for which the identity is a linear extension (= `e`)."""

    def __init__(self, n, rel, name=""):
        self.n = n
        self.name = name
        rel = set(rel)
        changed = True
        while changed:                                    # transitive closure
            changed = False
            for (a, b) in list(rel):
                for (c, d) in list(rel):
                    if b == c and (a, d) not in rel:
                        rel.add((a, d))
                        changed = True
        for (x, y) in rel:
            assert x < y, f"{name}: identity is not a linear extension ({x},{y})"
        self.rel = frozenset(rel)
        self._c = {}

    def __repr__(self):
        return f"Poset(n={self.n}, {self.name or sorted(self.rel)})"

    # ---- linear extensions -------------------------------------------------

    def les(self):
        if "les" not in self._c:
            r = self.rel
            self._c["les"] = [p for p in permutations(range(self.n))
                              if all(p.index(x) < p.index(y) for (x, y) in r)]
        return self._c["les"]

    def positions(self):
        """For each linear extension p, the vector pos with pos[x] = position of x."""
        if "pos" not in self._c:
            out = []
            for p in self.les():
                q = [0] * self.n
                for a, x in enumerate(p):
                    q[x] = a
                out.append(tuple(q))
            self._c["pos"] = out
        return self._c["pos"]

    # ---- transport ---------------------------------------------------------

    def T(self):
        if "T" not in self._c:
            n, ps = self.n, self.positions()
            N = len(ps)
            Mx = [[0] * n for _ in range(n)]
            for q in ps:
                for x in range(n):
                    Mx[x][q[x]] += 1
            self._c["T"] = [[F(Mx[x][a], N) for a in range(n)] for x in range(n)]
        return self._c["T"]

    def S(self):
        """S_P = (T + T^T)/2, exact."""
        if "S" not in self._c:
            T, n = self.T(), self.n
            self._c["S"] = [[(T[i][j] + T[j][i]) / 2 for j in range(n)] for i in range(n)]
        return self._c["S"]

    def a(self, i, j):
        return self.S()[i][j]

    def delta_max(self):
        """Delta_P = max_i d_i = max_i (1 - (S_P)_ii).  <= 1 always."""
        if "dmax" not in self._c:
            S = self.S()
            self._c["dmax"] = max(F(1) - S[i][i] for i in range(self.n))
        return self._c["dmax"]

    def laplacian(self):
        """I - S_P, exact.  Its diagonal is d_i and its off-diagonal is -a_ij."""
        if "L" not in self._c:
            S, n = self.S(), self.n
            self._c["L"] = [[(F(1) if i == j else F(0)) - S[i][j] for j in range(n)]
                            for i in range(n)]
        return self._c["L"]

    # ---- energies, leaks, conductance --------------------------------------

    def energy(self, f):
        """<f,(I-S_P)f> = sum_{i<j} a_ij (f_i - f_j)^2, exact."""
        S, n = self.S(), self.n
        tot = F(0)
        for i in range(n):
            for j in range(i + 1, n):
                if S[i][j]:
                    tot += S[i][j] * (f[i] - f[j]) ** 2
        return tot

    def leak(self, A):
        """E|A \\ sigma(A)| with sigma(A) = {p[i] : i in A}.

        Computed from the DEFINITION over linear extensions, never from the matrix, so
        that `energy(1_A) == leak(A)` is a real cross-check and not a tautology.
        """
        A = frozenset(A)
        key = ("leak", A)
        if key not in self._c:
            tot = 0
            for p in self.les():
                img = {p[i] for i in A}
                tot += len(A) - len(A & img)
            self._c[key] = F(tot, len(self.les()))
        return self._c[key]

    def phi(self, A):
        A = frozenset(A)
        a = len(A)
        assert 0 < a < self.n
        return self.leak(A) / min(a, self.n - a)

    def phi_star_prefix(self):
        """min over prefixes A_k = {0..k-1}, 1 <= k <= n-1.  Exact.  (= min over suffixes,
        because Phi is a function of the cut: leak(A) = leak(A^c).)"""
        if "psp" not in self._c:
            best, arg = None, None
            for k in range(1, self.n):
                v = self.phi(range(k))
                if best is None or v < best:
                    best, arg = v, k
            self._c["psp"] = (best, arg)
        return self._c["psp"]

    def phi_star(self):
        """min over ALL cuts.  Exact, brute force."""
        if "ps" not in self._c:
            best, arg = None, None
            for m in range(1, self.n):
                for A in combinations(range(self.n), m):
                    v = self.phi(A)
                    if best is None or v < best:
                        best, arg = v, A
            self._c["ps"] = (best, frozenset(arg))
        return self._c["ps"]

    def leak_min_at_size(self, m):
        """min leak over ALL sets of size m, with an argmin.  Exact."""
        best, arg = None, None
        for A in combinations(range(self.n), m):
            v = self.leak(A)
            if best is None or v < best:
                best, arg = v, A
        return best, frozenset(arg)

    # ---- footrule ----------------------------------------------------------

    def E_footrule(self):
        """E[ sum_i |i - pos(i)| ] over a uniform random linear extension.  Exact."""
        if "DF" not in self._c:
            ps = self.positions()
            tot = sum(sum(abs(i - q[i]) for i in range(self.n)) for q in ps)
            self._c["DF"] = F(tot, len(ps))
        return self._c["DF"]

    def E_sq_displacement(self):
        """E[ sum_i (i - pos(i))^2 ].  Exact.  (Spearman rho's numerator.)"""
        if "D2" not in self._c:
            ps = self.positions()
            tot = sum(sum((i - q[i]) ** 2 for i in range(self.n)) for q in ps)
            self._c["D2"] = F(tot, len(ps))
        return self._c["D2"]

    # ---- ordinal-sum structure ---------------------------------------------

    def cut_points(self):
        return [k for k in range(1, self.n)
                if all((x, y) in self.rel for x in range(k) for y in range(k, self.n))]

    def is_primitive(self):
        """Ordinal-sum-indecomposable with respect to e.  Equivalently (checked in the
        selftest) the weighted graph a_ij is connected, equivalently 1-lambda_std > 0."""
        return not self.cut_points()

    def is_chain(self):
        return len(self.les()) == 1


# ------------------------------------------------------------ the psi basis

def psi(n, k):
    """psi_k(i) = k/n - 1[i<k].  Centred prefix indicator (times -1), so that the
    monotone cone in 1^perp is exactly {sum_k c_k psi_k : c >= 0}."""
    return [F(k, n) - (1 if i < k else 0) for i in range(n)]


def pencil(P):
    """(Q, N) with Q_kl = <psi_k,(I-S_P)psi_l> and N_kl = <psi_k,psi_l>, exact.

    Closed forms, derived on paper and asserted against the definition in the selftest:
        Q_kl = sum of a_ij over i < min(k,l) and j >= max(k,l)      (so Q_kk = leak(A_k))
        N_kl = min(k,l) - k*l/n
    """
    n = P.n
    S = P.S()
    Q = [[F(0)] * (n - 1) for _ in range(n - 1)]
    for ki in range(n - 1):
        k = ki + 1
        for li in range(n - 1):
            l = li + 1
            lo, hi = min(k, l), max(k, l)
            tot = F(0)
            for i in range(lo):
                for j in range(hi, n):
                    tot += S[i][j]
            Q[ki][li] = tot
    N = [[F(min(ki + 1, li + 1)) - F((ki + 1) * (li + 1), n) for li in range(n - 1)]
         for ki in range(n - 1)]
    return Q, N


def from_coeffs(n, c):
    """The vector sum_k c_k psi_k in R^n."""
    f = [F(0)] * n
    for ki, ck in enumerate(c):
        if ck:
            pk = psi(n, ki + 1)
            for i in range(n):
                f[i] += ck * pk[i]
    return f


def is_monotone(f, strict=False):
    for i in range(len(f) - 1):
        if f[i] > f[i + 1] or (strict and f[i] >= f[i + 1]):
            return False
    return True


def rayleigh(P, f):
    """<f,(I-S_P)f>/||f||^2 for f perp 1.  Exact.  Asserts f is centred."""
    s = sum(f)
    assert s == 0, f"rayleigh: f is not centred (sum = {s})"
    nn = sum(x * x for x in f)
    assert nn != 0, "rayleigh: f = 0"
    return P.energy(f) / nn


# ------------------------------------------------- exact positive semidefinite

def charpoly_coeffs(A):
    """Faddeev-LeVerrier.  Returns [e_1, ..., e_m], the elementary symmetric functions of
    the eigenvalues (equivalently, e_k = sum of the k x k principal minors).  Exact.

    The recurrence produces `c_k` with det(xI - A) = x^m - c_1 x^{m-1} - ... - c_m, while
    det(xI - A) = sum_k (-1)^k e_k x^{m-k}.  Matching coefficients gives
    e_k = (-1)^(k+1) c_k, and dropping that sign is exactly the defect arm A6 caught.
    """
    m = len(A)
    M = [[F(0)] * m for _ in range(m)]
    for i in range(m):
        M[i][i] = F(1)
    es = []
    for k in range(1, m + 1):
        AM = [[sum(A[i][t] * M[t][j] for t in range(m)) for j in range(m)]
              for i in range(m)]
        c = sum(AM[i][i] for i in range(m)) / k
        es.append(c if k % 2 == 1 else -c)
        M = [[AM[i][j] - (c if i == j else F(0)) for j in range(m)] for i in range(m)]
    return es


def psd_exact(A):
    """Is the SYMMETRIC rational matrix A positive semidefinite?  EXACT.

    A symmetric real matrix has all eigenvalues >= 0 iff every elementary symmetric
    function e_k of its eigenvalues is >= 0.  (=>) is immediate; (<=) because
    det(-tI - A) = (-1)^m * sum_k e_k t^{m-k} with e_0 = 1, which is nonzero for every
    t > 0, so there is no negative eigenvalue.  e_k is read off Faddeev-LeVerrier.
    """
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            assert A[i][j] == A[j][i], "psd_exact: matrix is not symmetric"
    return all(e >= 0 for e in charpoly_coeffs(A))


def gap_at_least(P, r):
    """EXACT decision of `1 - lambda_std >= r`, with no eigenvalue computed.

    1 - lambda_std is the smallest eigenvalue of (I - S_P) on 1^perp.  Both (I - S_P) and
    (I - J/n) kill 1, so `(I - S_P) - r(I - J/n) >= 0 on 1^perp` iff it is PSD outright.
    """
    n = P.n
    L = P.laplacian()
    B = [[L[i][j] - r * ((F(1) if i == j else F(0)) - F(1, n)) for j in range(n)]
         for i in range(n)]
    return psd_exact(B)


def gap_exact_bounds(P, lo=F(0), hi=F(1), iters=60):
    """Rational bracket [lo, hi] on 1 - lambda_std by exact bisection on `gap_at_least`.
    Every endpoint is a rational number and every decision is exact."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if gap_at_least(P, mid):
            lo = mid
        else:
            hi = mid
    return lo, hi


# ------------------------------------------------------- eigen (FLOAT, labelled)

def jacobi(Af, sweeps=200, tol=1e-15):
    """Cyclic Jacobi on a symmetric matrix given as Fractions or floats.  FLOAT OUT.
    Returns (eigenvalues, V) with V[i][j] the i-th component of the j-th eigenvector.
    No verdict in this instrument rests on this routine."""
    A = [[float(x) for x in row] for row in Af]
    m = len(A)
    V = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    for _ in range(sweeps):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(m) for j in range(m) if i != j))
        if off < tol:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(m):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(m):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(m):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [A[i][i] for i in range(m)], V


def _chol_inv_sqrt(Nf):
    """L with N = L L^T (float Cholesky), returned together with L^{-1}."""
    m = len(Nf)
    L = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = Nf[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][i] = math.sqrt(max(s, 1e-300))
            else:
                L[i][j] = s / L[j][j]
    Li = [[0.0] * m for _ in range(m)]
    for i in range(m):
        Li[i][i] = 1.0 / L[i][i]
        for j in range(i):
            Li[i][j] = -sum(L[i][k] * Li[k][j] for k in range(j, i)) / L[i][i]
    return L, Li


def pencil_eigs(Q, N):
    """Generalized eigenpairs of (Q, N) with N positive definite.  FLOAT.
    Returns list of (eigenvalue, coefficient-vector c)."""
    m = len(Q)
    if m == 0:
        return []
    Nf = [[float(x) for x in row] for row in N]
    Qf = [[float(x) for x in row] for row in Q]
    _, Li = _chol_inv_sqrt(Nf)
    B = [[sum(Li[i][a] * Qf[a][b] * Li[j][b] for a in range(m) for b in range(m))
          for j in range(m)] for i in range(m)]
    for i in range(m):                                    # re-symmetrise
        for j in range(i + 1, m):
            v = (B[i][j] + B[j][i]) / 2
            B[i][j] = B[j][i] = v
    ev, V = jacobi(B)
    out = []
    for j in range(m):
        y = [V[i][j] for i in range(m)]
        c = [sum(Li[a][i] * y[a] for a in range(m)) for i in range(m)]   # c = L^{-T} y
        out.append((ev[j], c))
    out.sort(key=lambda t: t[0])
    return out


def cone_min(Q, N):
    """min over c >= 0, c != 0, of (c'Qc)/(c'Nc).  FLOAT — a SEARCH, not a verdict.

    The minimum over the closed cone is attained; on the relative interior of the face
    with support S it is a critical point of the restricted quotient, i.e. a generalized
    eigenvector of (Q_S, N_S) with all coordinates of one sign.  So enumerate the 2^m - 1
    supports and keep the best sign-definite eigenvector.  m = n-1 <= 6 here.
    Returns (value, c) with c >= 0, normalised to max entry 1.
    """
    m = len(Q)
    best = (float("inf"), None)
    for mask in range(1, 1 << m):
        idx = [i for i in range(m) if mask >> i & 1]
        Qs = [[Q[i][j] for j in idx] for i in idx]
        Ns = [[N[i][j] for j in idx] for i in idx]
        for lam, cs in pencil_eigs(Qs, Ns):
            if all(x >= -1e-11 for x in cs):
                sign = 1.0
            elif all(x <= 1e-11 for x in cs):
                sign = -1.0
            else:
                continue
            full = [0.0] * m
            for t, i in enumerate(idx):
                full[i] = max(sign * cs[t], 0.0)
            mx = max(full)
            if mx <= 0:
                continue
            full = [x / mx for x in full]
            if lam < best[0]:
                best = (lam, full)
    return best


def rationalise(c, den=2520):
    """Round a float coefficient vector to Fractions with a fixed denominator, clipped to
    >= 0 so monotonicity is preserved by construction."""
    out = [F(max(0, round(x * den)), den) for x in c]
    if all(x == 0 for x in out):
        out[0] = F(1)
    return out


# --------------------------------------------------------------- populations

def all_posets(n):
    """EVERY poset on {0..n-1} for which the identity is a linear extension."""
    pairs = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(pairs)):
        rel = frozenset(pairs[i] for i in range(len(pairs)) if mask >> i & 1)
        if all((a, d) in rel for (a, b) in rel for (c, d) in rel if b == c):
            out.append(Poset(n, rel, f"n{n}#{len(out)}"))
    return out


def named_posets(n):
    out = [Poset(n, [], f"antichain n={n}"),
           Poset(n, [(i, i + 1) for i in range(n - 1)], f"chain n={n}")]
    if n >= 3:
        out.append(Poset(n, [(i, i + 1) for i in range(n - 2)], f"chain{n-1}+pt n={n}"))
        ev = [i for i in range(n) if i % 2 == 0]
        od = [i for i in range(n) if i % 2 == 1]
        out.append(Poset(n, [(ev[i], ev[i + 1]) for i in range(len(ev) - 1)] +
                         [(od[i], od[i + 1]) for i in range(len(od) - 1)],
                         f"two interleaved chains n={n}"))
        out.append(Poset(n, [(0, i) for i in range(1, n)], f"one bottom + antichain n={n}"))
        out.append(Poset(n, [(i, n - 1) for i in range(n - 1)], f"antichain + one top n={n}"))
    if n >= 4:
        out.append(Poset(n, [(0, 2), (1, 2), (1, 3)], f"N-poset + {n-4}pt n={n}"))
        out.append(Poset(n, [(0, 2), (0, 3), (1, 2), (1, 3)], f"2+2 crown + {n-4}pt n={n}"))
    return out


def sample_posets(n, count, seed=12345):
    """A deterministic pseudo-random sample of posets on {0..n-1} with identity a linear
    extension.  Deterministic by construction: an LCG with a fixed seed, no `random`."""
    pairs = list(combinations(range(n), 2))
    st = seed
    out, seen = [], set()
    tries = 0
    while len(out) < count and tries < count * 400:
        tries += 1
        st = (1103515245 * st + 12345) % (1 << 31)
        rel = set()
        s2 = st
        for pr in pairs:
            s2 = (1103515245 * s2 + 12345) % (1 << 31)
            if (s2 >> 16) & 1:
                rel.add(pr)
        ch = True
        while ch:                                          # close it
            ch = False
            for (a, b) in list(rel):
                for (c, d) in list(rel):
                    if b == c and (a, d) not in rel:
                        rel.add((a, d))
                        ch = True
        key = frozenset(rel)
        if key in seen:
            continue
        seen.add(key)
        out.append(Poset(n, key, f"s{n}#{len(out)}"))
    return out


# ------------------------------------------------- the L2-FREE sweep bound

def sweep_bound_sq(dmax, r):
    """An EXACT upper bound on `Phi*_pref^2`, given `Delta_P` and `r = R(g)` for a
    MONOTONE g perp 1.  This is `mg-76b2` Lemma 3.1 with two changes, both free:

      (1) its `d_i <= 1` is kept as `d_i <= Delta_P`;
      (2) its Cauchy-Schwarz factor `sum_ij a_ij (h_i+h_j)^2` is evaluated rather than
          discarded:  sum_ij a_ij (h_i+h_j)^2 = 2 sum_i d_i h_i^2 - E(h)
                                            <= 2 Delta_P ||h||^2 - E(h),
          which gives `Phi^2 <= R(h)(2 Delta_P - R(h))` in place of `2 R(h)`.

    The truncation h of g has R(h) <= r, and t -> t(2D - t) increases on [0, D], so the
    correct bound for an arbitrary r is the sup of t(2D-t) over t in [0, r]:
    `r(2D - r)` when r <= D, and `D^2` otherwise.  Exact in Fractions.
    """
    return dmax * dmax if r >= dmax else r * (2 * dmax - r)
