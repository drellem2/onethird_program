"""lib76b2 — the instrument for mg-76b2 (ATTACK C_3).

Written from scratch for this ticket. It shares NO code with `lib2de0`, `lib_c4f5`,
`lib4d3b` or `core.py`: PREDICTIONS.md H7 records a suspected defect in `lib2de0.E_leak`
for non-prefix cuts, and an instrument that inherits the library it is checking cannot
find that class of defect.

DESIGN COMMITMENTS
------------------
* **Exact arithmetic for every verdict.**  `Fraction` throughout.  Floats appear only in
  (a) display columns and (b) the Jacobi eigen-routine, which is *never* the sole warrant
  for a verdict — every eigen-derived number is either re-checked exactly or labelled
  FLOAT at the print site.
* **Cheeger comparisons are squared, never rooted.**  `Phi <= sqrt(2R)` is checked as
  `Phi**2 <= 2*R` in `Fraction`, so no verdict ever passes through `math.sqrt`.
* **sigma(A) means the image of the set A**, i.e. `{p[i] for i in A}` — NOT `set(p[:|A|])`.
  For a prefix the two agree; for a general cut they do not, and `phi_star` ranges over
  general cuts.  `leak_naive_prefixstyle` reproduces the other convention on purpose so
  the two can be compared rather than argued about (P11).
* Every count names its POPULATION at the print site and the label is generated from the
  loop's own counter, never typed in.
"""

from fractions import Fraction as F
from itertools import combinations, permutations
import math

# ------------------------------------------------------------------ posets


class Poset:
    """A poset on {0,...,n-1} whose identity permutation is a linear extension.

    `rel` is the strict order, given as pairs (x, y) meaning x < y.  The labelling is the
    distinguished order e = 0 1 2 ... n-1, exactly as the source's Step 1 fixes it.
    """

    def __init__(self, n, rel, name=""):
        self.n = n
        self.name = name
        rel = set(rel)
        changed = True
        while changed:                       # transitive closure
            changed = False
            for (a, b) in list(rel):
                for (c, d) in list(rel):
                    if b == c and (a, d) not in rel:
                        rel.add((a, d))
                        changed = True
        for (x, y) in rel:
            assert x < y, f"{name}: identity is not a linear extension ({x},{y})"
        self.rel = frozenset(rel)
        self._cache = {}

    def __repr__(self):
        return f"Poset(n={self.n}, {self.name or sorted(self.rel)})"

    def leq(self, x, y):
        return x == y or (x, y) in self.rel

    # ---- linear extensions

    def linear_extensions(self):
        if "le" not in self._cache:
            self._cache["le"] = [
                p for p in permutations(range(self.n))
                if all(p.index(x) < p.index(y) for (x, y) in self.rel)
            ]
        return self._cache["le"]

    def is_chain(self):
        return len(self.linear_extensions()) == 1

    # ---- transport, exactly

    def T(self):
        """T_P with (T_P)_{xa} = Pr[x occupies position a].  Exact Fractions."""
        if "T" not in self._cache:
            les = self.linear_extensions()
            N = len(les)
            M = [[0] * self.n for _ in range(self.n)]
            for p in les:
                for a in range(self.n):      # position a holds element p[a]
                    M[p[a]][a] += 1
            self._cache["T"] = [[F(M[x][a], N) for a in range(self.n)]
                                for x in range(self.n)]
        return self._cache["T"]

    def M(self):
        """The symmetrised transport matrix (T_P + T_P^T)/2.  Exact.

        This is the source's S_P before restriction to H; restriction is unnecessary for
        every quadratic form used here because (I - M) annihilates constants.
        """
        if "M" not in self._cache:
            T = self.T()
            n = self.n
            self._cache["M"] = [[(T[i][j] + T[j][i]) / 2 for j in range(n)]
                                for i in range(n)]
        return self._cache["M"]

    def weights(self):
        """a_ij for i != j — the weighted graph whose Laplacian is I - M."""
        if "w" not in self._cache:
            M = self.M()
            n = self.n
            self._cache["w"] = {(i, j): M[i][j]
                                for i in range(n) for j in range(i + 1, n)
                                if M[i][j] != 0}
        return self._cache["w"]

    # ---- energies and conductance, exactly

    def energy(self, f):
        """<f, (I-M) f> = sum over unordered pairs of a_ij (f_i - f_j)^2.  Exact."""
        tot = F(0)
        for (i, j), a in self.weights().items():
            tot += a * (f[i] - f[j]) ** 2
        return tot

    def leak(self, A):
        """E_sigma |A \\ sigma(A)| with sigma(A) = {p[i] : i in A}.  Exact.

        Computed straight from the definition, NOT from the matrix, so that
        `energy(indicator) == leak` is a real cross-check and not a tautology.
        """
        A = frozenset(A)
        key = ("leak", A)
        if key not in self._cache:
            les = self.linear_extensions()
            tot = 0
            for p in les:
                img = {p[i] for i in A}
                tot += len(A) - len(A & img)
            self._cache[key] = F(tot, len(les))
        return self._cache[key]

    def leak_naive_prefixstyle(self, A):
        """The OTHER convention: |A| - |A & set(p[:|A|])|.  Present only so that P11 can
        be measured instead of asserted.  Agrees with `leak` when A is a prefix."""
        A = frozenset(A)
        les = self.linear_extensions()
        a = len(A)
        tot = 0
        for p in les:
            tot += a - len(A & set(p[:a]))
        return F(tot, len(les))

    def phi(self, A):
        """Phi_P(A) = E|A \\ sigma(A)| / min(|A|, n-|A|).

        Equals Delta_1(A, A^c) by Op-Form Lemma 2.1 (the normalisation is min(|A|,|A^c|)
        in both).  Defined for 0 < |A| < n.
        """
        a = len(frozenset(A))
        assert 0 < a < self.n
        return self.leak(A) / min(a, self.n - a)

    def phi_star(self):
        """min Phi_P(A) over ALL cuts 0 < |A| < n.  Exact, brute force over 2^n."""
        if "phi*" not in self._cache:
            best, arg = None, None
            for size in range(1, self.n):
                for S in combinations(range(self.n), size):
                    v = self.phi(S)
                    if best is None or v < best:
                        best, arg = v, S
            self._cache["phi*"] = (best, frozenset(arg))
        return self._cache["phi*"]

    def phi_star_prefix(self):
        """min Phi_P(A_k) over PREFIXES A_k = {0,...,k-1}, 1 <= k <= n-1.  Exact.

        Prefixes and suffixes give the same set of values: Phi is a function of the cut
        {A, A^c} because |A \\ sigma(A)| = |A^c \\ sigma(A^c)| pointwise (checked in
        selftest76b2), and min(|A|,|A^c|) is symmetric.  So this is also the minimum over
        suffix cuts.
        """
        if "phi*pref" not in self._cache:
            best, arg = None, None
            for k in range(1, self.n):
                v = self.phi(range(k))
                if best is None or v < best:
                    best, arg = v, k
            self._cache["phi*pref"] = (best, arg)
        return self._cache["phi*pref"]

    def rho_prefix(self, k):
        """Rayleigh quotient of the centred prefix indicator f = 1_{A_k} - (k/n)1:

            rho(A_k) = <f, M f> / ||f||^2,      1 - rho(A_k) = <f,(I-M)f> / ||f||^2.

        Returned as `1 - rho`, exactly.  ||f||^2 = k(n-k)/n.
        """
        n = self.n
        assert 0 < k < n
        f = [F(1) - F(k, n) if i < k else -F(k, n) for i in range(n)]
        return self.energy(f) / (F(k * (n - k), n))

    # ---- ordinal-sum structure

    def cut_points(self):
        """The k with 1 <= k <= n-1 such that A_k is an EXACT ordinal-sum split, i.e.
        every element of A_k is below every element of its complement."""
        out = []
        for k in range(1, self.n):
            if all((x, y) in self.rel for x in range(k) for y in range(k, self.n)):
                out.append(k)
        return out

    def is_primitive(self):
        """Ordinal-sum-indecomposable with respect to the distinguished order."""
        return not self.cut_points()


def connected(P):
    """Is the weighted graph with weights a_ij connected?  EXACT — `a_ij != 0` is a
    Fraction comparison, no float anywhere.  `1 - lambda_std = 0` iff disconnected, which
    is why this exists: it gives the stratification of s3 (C0) without an eigenvalue."""
    n = P.n
    adj = {i: set() for i in range(n)}
    for (i, j) in P.weights():
        adj[i].add(j)
        adj[j].add(i)
    seen, stack = {0}, [0]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return len(seen) == n


# ------------------------------------------------------------ populations


def all_posets(n):
    """EVERY poset on {0..n-1} for which the identity is a linear extension.

    Enumerated by walking the 2^C(n,2) candidate strict-order sets and keeping the
    transitively closed ones, so each poset of the population appears exactly once.
    """
    pairs = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(pairs)):
        rel = frozenset(pairs[i] for i in range(len(pairs)) if mask >> i & 1)
        if all((a, d) in rel for (a, b) in rel for (c, d) in rel if b == c):
            out.append(Poset(n, rel, f"P{len(out)}"))
    return out


def named_posets(n):
    """Named families at a single n, for the n=7 spot checks."""
    out = [Poset(n, [], f"antichain n={n}"),
           Poset(n, [(i, i + 1) for i in range(n - 1)], f"chain n={n}")]
    if n >= 3:
        out.append(Poset(n, [(i, i + 1) for i in range(n - 2)], f"chain_{n-1}+pt n={n}"))
        h = n // 2
        out.append(Poset(n, [(i, j) for i in range(h) for j in range(h, n)],
                         f"ordsum A{h}<A{n-h} n={n}"))
        ev = [i for i in range(n) if i % 2 == 0]
        od = [i for i in range(n) if i % 2 == 1]
        out.append(Poset(n, [(ev[i], ev[i + 1]) for i in range(len(ev) - 1)] +
                         [(od[i], od[i + 1]) for i in range(len(od) - 1)],
                         f"two_chains(interleaved) n={n}"))
    if n >= 4:
        out.append(Poset(n, [(0, 2), (1, 2), (1, 3)], f"N-poset+{n-4}pts n={n}"))
    return out


# ------------------------------------------------------ eigen (FLOAT — labelled)


def jacobi(Afrac, sweeps=200, tol=1e-14):
    """Cyclic Jacobi eigen-decomposition of a symmetric matrix given as Fractions.

    Returns (eigenvalues, eigenvectors-as-columns-list) in FLOAT.  Every consumer of this
    routine must label its output FLOAT at the print site.  No verdict in this instrument
    rests on it alone.
    """
    return _jacobi_float([[float(x) for x in row] for row in Afrac], sweeps, tol)


def _jacobi_float(A0, sweeps=200, tol=1e-14):
    """Cyclic Jacobi on a FLOAT symmetric matrix.  Returns (eigenvalues, eigenvectors)."""
    n = len(A0)
    A = [row[:] for row in A0]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-18:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    vals = [A[i][i] for i in range(n)]
    vecs = [[V[i][j] for i in range(n)] for j in range(n)]     # vecs[j] = j-th vector
    return vals, vecs


def H_basis(n):
    """An orthonormal basis of H = 1^perp, in exact Fractions where possible.

    Helmert columns b_k = (1,...,1,-k,0,...,0)/sqrt(k(k+1)) with k leading ones,
    k = 1..n-1.  Returned in FLOAT because the normalisation is irrational; the
    *span* is exact and that is all the restriction needs.
    """
    B = []
    for k in range(1, n):
        col = [1.0] * k + [-float(k)] + [0.0] * (n - k - 1)
        s = math.sqrt(k * (k + 1))
        B.append([x / s for x in col])
    return B                                  # B[j] is the j-th basis vector


def standard_spectrum(P):
    """(lambda_std, dominant standard eigenvectors, multiplicity) — FLOAT.

    lambda_std = max over f in H = 1^perp of <f,Mf>/||f||^2.  Obtained by RESTRICTING M
    to an orthonormal basis of H and diagonalising the (n-1)x(n-1) restriction, rather
    than diagonalising M and trying to spot the trivial representation afterwards.  The
    latter fails exactly when the top eigenvalue is degenerate and the trivial rep sits
    inside the degenerate block — which is the case at every chain (M = I).

    Multiplicity is counted in a 1e-9 window and is REPORTED, never silently collapsed:
    where it exceeds 1, "the dominant standard eigenvector" is not a well-defined object
    and any monotonicity verdict there is a statement about a basis choice.
    """
    n = P.n
    if n < 2:
        return None, [], 0
    B = H_basis(n)
    M = P.M()
    Mf = [[float(M[i][j]) for j in range(n)] for i in range(n)]
    m = n - 1
    MH = [[sum(B[a][i] * Mf[i][j] * B[b][j] for i in range(n) for j in range(n))
           for b in range(m)] for a in range(m)]
    vals, vecs = _jacobi_float(MH)
    lam_std = max(vals)
    dom = []
    for lam, v in zip(vals, vecs):
        if lam_std - lam < 1e-9:
            dom.append([sum(v[a] * B[a][i] for a in range(m)) for i in range(n)])
    return lam_std, dom, len(dom)


def is_monotone(v, tol=1e-9):
    """Is v (or -v) non-decreasing along e = 0,1,...,n-1?  FLOAT, with a tolerance."""
    up = all(v[i] <= v[i + 1] + tol for i in range(len(v) - 1))
    dn = all(v[i] >= v[i + 1] - tol for i in range(len(v) - 1))
    return up or dn


def monotone_in_span(dom, tol=1e-9):
    """Does the dominant standard eigenspace contain a monotone vector?  Three-valued.

    'YES'       — a monotone vector was exhibited.
    'NO'        — the eigenspace is one-dimensional and neither +v nor -v is monotone.
    'UNDECIDED' — multiplicity > 1 and neither the basis vectors nor the projection of the
                  source's own centred expected-rank observable u_a = a - (n+1)/2 onto the
                  eigenspace is monotone.  This instrument does NOT solve the feasibility
                  problem in general and says so rather than guessing.

    L2 as the source states it is EXISTENTIAL ("a dominant standard eigenvector is
    monotone"), so 'YES' is a hit for L2 and 'UNDECIDED' is silence, not a miss.
    """
    if not dom:
        return "UNDECIDED"
    n = len(dom[0])
    for v in dom:
        if is_monotone(v, tol):
            return "YES"
    if len(dom) == 1:
        return "NO"
    # Gram-Schmidt the eigenspace, then project the centred linear observable onto it.
    basis = []
    for v in dom:
        w = v[:]
        for b in basis:
            c = sum(w[i] * b[i] for i in range(n))
            w = [w[i] - c * b[i] for i in range(n)]
        nr = math.sqrt(sum(x * x for x in w))
        if nr > 1e-9:
            basis.append([x / nr for x in w])
    u = [a - (n - 1) / 2.0 for a in range(n)]
    proj = [0.0] * n
    for b in basis:
        c = sum(u[i] * b[i] for i in range(n))
        proj = [proj[i] + c * b[i] for i in range(n)]
    if math.sqrt(sum(x * x for x in proj)) > 1e-9 and is_monotone(proj, tol):
        return "YES"
    return "UNDECIDED"


# --------------------------------------------------------- the Cheeger sweep


def sweep_sets(f, tol=0.0):
    """Every GENUINE threshold set {i : f_i > t} of f, excluding empty and full.

    DEFECT FOUND AND FIXED IN PLACE, KEPT IN THE HISTORY (see README s2/D1).  The first
    version of this routine returned `order[cut:]` for each cut of the sorted order.  An
    order-slice is not a level set: where f ties, slicing SPLITS the tie and returns sets
    that no threshold ever produces.  On the antichain at n = 4 the dominant standard
    eigenvector is (a,a,a,-3a) -- monotone, ties everywhere -- and the old routine offered
    {1,2} and {2} as "threshold sets" of it, which is how s2's (S3) came to report three
    monotone sweeps landing outside the prefix family.  The sets were the artifact; the
    theorem was not.

    The error direction matters and is stated rather than buried: too MANY sets makes the
    sweep lemma (S1) EASIER to satisfy and the prefix claim (S3) HARDER, so (S1)'s clean
    pass under the old routine was flattered and had to be re-run.

    `tol` groups near-equal values, for FLOAT input where an exact tie is not exact.
    """
    n = len(f)
    order = sorted(range(n), key=lambda i: f[i])
    out, seen = [], set()
    for cut in range(1, n):
        lo, hi = f[order[cut - 1]], f[order[cut]]
        if hi - lo <= tol:                 # not a real level: the tie is unbroken
            continue
        S = frozenset(order[cut:])
        if S not in seen:
            seen.add(S)
            out.append(S)
    return out


def is_prefix_or_suffix(S, n):
    """Is S = {0..k-1} or {k..n-1}?"""
    s = sorted(S)
    return s == list(range(len(s))) or s == list(range(n - len(s), n))


def sweep_best(P, f, tol=0.0):
    """The best threshold set of f with |S| <= n/2, by Phi.  Exact when f is Fractions.

    Returns (S, Phi(S)).  This is the set the standard proof of the hard half of Cheeger
    produces; `s2_sweep.py` checks Phi(S)^2 <= 2 * R(f) on it in exact arithmetic.
    """
    n = P.n
    best, arg = None, None
    for S in sweep_sets(f, tol):
        for T in (S, frozenset(range(n)) - S):
            if not (0 < len(T) <= n // 2):
                continue
            v = P.phi(T)
            if best is None or v < best:
                best, arg = v, T
    return arg, best


def rayleigh(P, f):
    """R(f) = <f,(I-M)f> / ||f - mean||^2 for f not constant.  Exact for Fraction f."""
    n = P.n
    m = sum(f) / n
    g = [x - m for x in f]
    nrm = sum(x * x for x in g)
    return P.energy(f) / nrm


# --------------------------------------------------------------- reporting


def frac_str(x, places=6):
    return f"{x} = {float(x):.{places}f}" if x is not None else "n/a"
