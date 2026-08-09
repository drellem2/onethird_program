"""lib81ff — the instrument for mg-81ff (CHAIN (IV): is the literal capture fraction `c`
bounded away from its threshold?).

Written from scratch.  It shares NO code with `lib76b2`, `lib9461`, `lib_d3c7` or any
other library in this repository, and that is deliberate rather than decorative: the
FIRST thing this ticket must do is CHECK `mg-76b2`'s falling `min c`, and an instrument
that inherits `mg-76b2`'s library cannot check `mg-76b2`'s numbers — it can only re-print
them.  Every figure `mg-76b2` reports is recomputed here on a path with a different
enumeration, a different transport computation and a different eigenroutine, and `s0`
asserts the agreement rather than assuming it.

WHAT `c` IS.  `Op-Form §4.3`'s Prefix-capture conjecture, AS LITERALLY WORDED: some
prefix `A_k = {0..k-1}` captures a constant fraction of the dominant standard eigenvalue,

    rho(A_k) >= c * lambda_std,          rho(A) := <f_A, M f_A> / ||f_A||^2,
    f_A := 1_A - (|A|/n) 1               (the CENTRED prefix indicator; f_A lies in H).

Per poset this makes `c` a MAXIMUM over the n-1 prefixes and per population an INFIMUM
over the posets:

    c(P) := max_{1<=k<=n-1} rho(A_k) / lambda_std(P),        c(n) := min over the population.

`c(P)` is undefined where `lambda_std = 0` (the disconnected/ordinal-sum-decomposable
stratum) and those posets are excluded, exactly as `mg-76b2 s3 (C0)` excludes them.

THE ARITHMETIC IDENTITY THIS LIBRARY IS BUILT AROUND.  `I - M` is the Laplacian `L` of
the weighted graph `a_ij = M_ij`, because `M` is symmetric and doubly stochastic, so

    1 - lambda_std = lambda_2(L)   (the Fiedler value),      rho(A_k) = 1 - Q_k,
    Q_k := <f_k, L f_k> / ||f_k||^2   EXACT RATIONAL,        ||f_k||^2 = k(n-k)/n,

    c(P) = ( 1 - min_k Q_k ) / ( 1 - lambda_2(L) ).

    NOT `/ lambda_2`.  The denominator is `lambda_std`, which is `1 - lambda_2`; this
    line was written the wrong way round in the first draft of this file and `c_bracket`
    inherited the slip, which is why `s0 (E)` asserts the identity against `float_c`
    rather than trusting either.

DESIGN COMMITMENTS
------------------
* **`min_k Q_k` is EXACT** (`Fraction`), always.  Only `lambda_2` needs an eigenvalue.
* **Every verdict about `c` is CERTIFIED IN EXACT RATIONALS, never on the float.**  The
  direction a REFUTATION of chain (IV) needs is an UPPER bound on `c`, i.e. a LOWER bound
  on `lambda_2`, and a test vector gives only the other one — so a Rayleigh witness is
  NOT enough and this library does not pretend it is.  What it does instead is decide
  `lambda_2 > q` EXACTLY, for rational `q`, by Sylvester's criterion:

      lambda_2 = min_{x != 0} x^T A x / x^T G x   with   A = B^T L B,  G = B^T B
      for the RATIONAL basis  B = (e_0 - e_{n-1}, ..., e_{n-2} - e_{n-1})  of H,

      lambda_2 > q   <==>   A - qG  is POSITIVE DEFINITE   <==>  every pivot of its
                            exact symmetric elimination is > 0.

  Bisecting `q` gives an exact rational bracket `lo < lambda_2 <= hi` to any precision,
  hence an exact bracket on `c = (1 - min_k Q_k)/lambda_2` — `c <= (1-minQ)/lo` is the
  side that refutes a threshold and `c >= (1-minQ)/hi` the side that establishes one.
  `float_c` is used only to FIND candidates; every verdict is restated against the
  bracket.  No `math.sqrt` and no eigenvector appears on the verdict path.
* Populations are enumerated by EXTENSION (a naturally labelled poset on `[n]` is one on
  `[n-1]` plus a down-closed subset of it as `n-1`'s strict down-set), not by masking
  `2^C(n,2)` relations.  Each poset appears exactly once, and `n = 7` is reachable.
* Linear extensions are counted by a DOWN-SET DP, never by `n!` enumeration — but the
  `n!` path is kept (`transport_factorial`) SOLELY so `s0` can cross-check the DP against
  it exhaustively.  `mg-9461`'s `s0` caught a defect in exactly this DP that no
  numbers-only check at small `n` could see, so the control is not a formality.
"""

from fractions import Fraction as F
from itertools import permutations
import math

# --------------------------------------------------------------- posets


class Poset:
    """A poset on {0..n-1} whose identity permutation is a linear extension.

    Stored as `down[x]` = bitmask of the STRICT down-set of x (transitively closed).
    Because the identity is a linear extension, `down[x]` is a subset of {0..x-1}.
    """

    __slots__ = ("n", "down", "_c")

    def __init__(self, n, down):
        self.n = n
        self.down = tuple(down)
        self._c = {}

    # ---- presentation

    def relations(self):
        """The strict order as a sorted list of pairs (x, y) with x < y."""
        return sorted((x, y) for y in range(self.n) for x in range(self.n)
                      if self.down[y] >> x & 1)

    def cover_string(self):
        return repr(self.relations())

    def __repr__(self):
        return f"Poset(n={self.n}, rel={self.relations()})"

    # ---- down-set lattice

    def downsets(self):
        """Every down-closed subset, as bitmasks, in increasing order of popcount."""
        if "ds" not in self._c:
            out = []
            for S in range(1 << self.n):
                ok = True
                x = S
                while x:
                    b = x & -x
                    i = b.bit_length() - 1
                    if self.down[i] & ~S:
                        ok = False
                        break
                    x ^= b
                if ok:
                    out.append(S)
            out.sort(key=lambda S: bin(S).count("1"))
            self._c["ds"] = out
        return self._c["ds"]

    def is_downset(self, S):
        x = S
        while x:
            b = x & -x
            i = b.bit_length() - 1
            if self.down[i] & ~S:
                return False
            x ^= b
        return True

    # ---- transport, exactly, by down-set DP

    def transport(self):
        """T with T[x][a] = Pr[x occupies position a], over uniform linear extensions.

        DP over the down-set lattice.  `e[S]` counts linear extensions of the induced
        order on the down-set S; `g[S]` counts them on the complement of S (an up-set).
        Element x sits at position a iff the set of elements before it is a down-set S
        with |S| = a, x not in S, and S | {x} down-closed.
        """
        if "T" not in self._c:
            n, ds = self.n, self.downsets()
            full = (1 << n) - 1
            e = {}
            for S in ds:                       # increasing popcount
                if S == 0:
                    e[S] = 1
                    continue
                tot = 0
                x = S
                while x:
                    b = x & -x
                    i = b.bit_length() - 1
                    # peel i only if it is MAXIMAL in S, i.e. S\{i} is still down-closed.
                    # `down[i] subset of S\{i}` is NOT that test — it is true of every
                    # i in S, minimal ones included, and peeling on it walks sets that
                    # are not down-sets at all.  s0 (C) keeps that mutant caught.
                    if self.is_downset(S ^ b):
                        tot += e[S ^ b]
                    x ^= b
                e[S] = tot
            g = {}
            for S in reversed(ds):             # decreasing popcount
                if S == full:
                    g[S] = 1
                    continue
                tot = 0
                for i in range(n):
                    if S >> i & 1:
                        continue
                    if self.down[i] & ~S:
                        continue
                    tot += g[S | (1 << i)]
                g[S] = tot
            N = e[full]
            T = [[0] * n for _ in range(n)]
            for S in ds:
                a = bin(S).count("1")
                for i in range(n):
                    if S >> i & 1:
                        continue
                    if self.down[i] & ~S:
                        continue
                    T[i][a] += e[S] * g[S | (1 << i)]
            self._c["T"] = ([[F(T[i][a], N) for a in range(n)] for i in range(n)], N)
        return self._c["T"]

    def n_linear_extensions(self):
        return self.transport()[1]

    def transport_factorial(self):
        """The same T by BRUTE FORCE over all n! permutations.  Control only — `s0`
        cross-checks the DP against this exhaustively; nothing else calls it."""
        n = self.n
        les = [p for p in permutations(range(n))
               if all(p.index(x) < p.index(y) for (x, y) in self.relations())]
        T = [[0] * n for _ in range(n)]
        for p in les:
            for a in range(n):
                T[p[a]][a] += 1
        return [[F(T[i][a], len(les)) for a in range(n)] for i in range(n)], len(les)

    def M(self):
        """(T + T^T)/2 — symmetric and doubly stochastic.  Exact."""
        if "M" not in self._c:
            T, _ = self.transport()
            n = self.n
            self._c["M"] = [[(T[i][j] + T[j][i]) / 2 for j in range(n)]
                            for i in range(n)]
        return self._c["M"]

    def weights(self):
        """a_ij (i < j) — the weighted graph whose Laplacian is I - M."""
        if "w" not in self._c:
            M, n = self.M(), self.n
            self._c["w"] = {(i, j): M[i][j] for i in range(n)
                            for j in range(i + 1, n) if M[i][j]}
        return self._c["w"]

    # ---- quadratic forms, exactly

    def energy(self, f):
        """<f, L f> = sum_{i<j} a_ij (f_i - f_j)^2.  Exact for rational f."""
        tot = F(0)
        for (i, j), a in self.weights().items():
            d = f[i] - f[j]
            tot += a * d * d
        return tot

    def rayleigh(self, f):
        """R(f) = <f,Lf>/||f||^2 for f perp 1.  Exact.  An upper bound on lambda_2."""
        s = sum(f)
        assert s == 0, "rayleigh() requires f perp 1"
        nrm = sum(x * x for x in f)
        assert nrm != 0
        return self.energy(f) / nrm

    def prefix_Q(self, k):
        """Q_k = <f_k, L f_k> / ||f_k||^2 with f_k the CENTRED prefix indicator.
        Exact.  rho(A_k) = 1 - Q_k."""
        n = self.n
        assert 0 < k < n
        f = [F(n - k, n) if i < k else F(-k, n) for i in range(n)]
        return self.energy(f) / F(k * (n - k), n)

    def min_prefix_Q(self):
        """min_k Q_k, exact, with the argmin.  = 1 - max_k rho(A_k)."""
        if "mq" not in self._c:
            best, arg = None, None
            for k in range(1, self.n):
                q = self.prefix_Q(k)
                if best is None or q < best:
                    best, arg = q, k
            self._c["mq"] = (best, arg)
        return self._c["mq"]

    # ---- ordinal-sum structure

    def cut_points(self):
        """k with 1<=k<=n-1 such that A_k = {0..k-1} is an exact ordinal-sum split."""
        n = self.n
        out = []
        for k in range(1, n):
            lo = (1 << k) - 1
            if all(self.down[y] & lo == lo for y in range(k, n)):
                out.append(k)
        return out

    def is_primitive(self):
        return not self.cut_points()

    def connected(self):
        """Is the weighted graph a_ij connected?  EXACT — `1 - lambda_std = 0` iff not."""
        n = self.n
        adj = {i: set() for i in range(n)}
        for (i, j) in self.weights():
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

    # ---- the spectral side

    def laplacian_float(self):
        n = self.n
        M = self.M()
        return [[float((1 if i == j else 0) - M[i][j]) for j in range(n)]
                for i in range(n)]

    def fiedler(self):
        """(lambda_2(L), an eigenvector for it) — FLOAT, by Jacobi on L restricted to H.

        Restriction to H = 1^perp is done with an explicit orthonormal basis rather than
        by diagonalising L and discarding the constant afterwards, because the constant
        vector sits in a degenerate block at every chain (L = 0 there) and "spot the
        trivial rep" fails exactly in the cases this ticket cares about.
        """
        if "fied" not in self._c:
            n = self.n
            B = h_basis(n)
            L = self.laplacian_float()
            m = n - 1
            LH = [[sum(B[a][i] * L[i][j] * B[b][j]
                       for i in range(n) for j in range(n))
                   for b in range(m)] for a in range(m)]
            vals, vecs = jacobi(LH)
            k = min(range(m), key=lambda t: vals[t])
            v = [sum(vecs[k][a] * B[a][i] for a in range(m)) for i in range(n)]
            self._c["fied"] = (vals[k], v)
        return self._c["fied"]

    def float_c(self):
        """c(P) on the float path — for SEARCH only.  None on the lambda_std = 0 stratum.

        `connected()` is the EXACT predicate for that stratum (mg-76b2 s3 (C0) proves the
        three candidate predicates coincide, and s0 here re-checks it), so the exclusion
        never rests on a float tolerance.
        """
        if not self.connected():
            return None
        lam2, _ = self.fiedler()
        lam_std = 1.0 - lam2
        if lam_std <= 1e-12:
            return None
        mq, _ = self.min_prefix_Q()
        return (1.0 - float(mq)) / lam_std

    # ---- the exact spectral side: Sylvester's criterion, no float, no sqrt

    def _AG(self):
        """(A, G) = (B^T L B, B^T B) for the rational basis B of H = 1^perp given by
        b_i = e_i - e_{n-1}, i = 0..n-2.  Both exact and symmetric; G is positive
        definite, so lambda_2 = min generalised eigenvalue of (A, G)."""
        if "AG" not in self._c:
            n, M = self.n, self.M()
            m = n - 1
            L = [[(F(1) if i == j else F(0)) - M[i][j] for j in range(n)]
                 for i in range(n)]
            # (B^T L B)_{ab} = L[a][b] - L[a][n-1] - L[n-1][b] + L[n-1][n-1]
            A = [[L[a][b] - L[a][n - 1] - L[n - 1][b] + L[n - 1][n - 1]
                  for b in range(m)] for a in range(m)]
            G = [[F(2) if a == b else F(1) for b in range(m)] for a in range(m)]
            self._c["AG"] = (A, G)
        return self._c["AG"]

    def lambda2_gt(self, q):
        """EXACT: is lambda_2(L) > q?  By positive-definiteness of A - qG.

        Symmetric Gaussian elimination in `Fraction`; a non-positive pivot is a
        certificate of NOT positive definite.  No float, no sqrt, no eigenvector.
        """
        A, G = self._AG()
        q = F(q)
        m = len(A)
        S = [[A[i][j] - q * G[i][j] for j in range(m)] for i in range(m)]
        for i in range(m):
            p = S[i][i]
            if p <= 0:
                return False
            for r in range(i + 1, m):
                fac = S[r][i] / p
                if fac:
                    for c2 in range(i, m):
                        S[r][c2] -= fac * S[i][c2]
        return True

    def lambda2_bracket(self, prec=F(1, 10**9), hi=None):
        """EXACT rational (lo, hi) with lo < lambda_2 <= hi and hi - lo <= prec.

        Bisection on the `lambda2_gt` predicate.  The initial upper end is 1 because
        L = I - M with M doubly stochastic has spectrum in [0, 2] and lambda_2 <= 1 for
        every poset in this population (asserted, not assumed: the loop widens if the
        predicate says otherwise).
        """
        key = ("br", prec)
        if key in self._c:
            return self._c[key]
        lo, hg = F(0), F(1) if hi is None else F(hi)
        while self.lambda2_gt(hg):
            hg *= 2
        while hg - lo > prec:
            mid = (lo + hg) / 2
            if self.lambda2_gt(mid):
                lo = mid
            else:
                hg = mid
        self._c[key] = (lo, hg)
        return lo, hg

    def c_bracket(self, prec=F(1, 10**9)):
        """EXACT rational (c_lo, c_hi) with c_lo <= c(P) <= c_hi.

        c = (1 - min_k Q_k) / lambda_std = (1 - min_k Q_k) / (1 - lambda_2).  Numerator
        exact; the bracket `lo < lambda_2 <= hi` gives `1-hi <= lambda_std < 1-lo`, and c
        is DECREASING in lambda_std, so

            c_lo = num / (1 - lo),      c_hi = num / (1 - hi).

        `c_hi` is the side that REFUTES a threshold on c; `c_lo` is the side that would
        establish one.  Returns None on the lambda_std = 0 stratum.
        """
        if not self.connected():
            return None
        lo, hg = self.lambda2_bracket(prec)
        mq, _ = self.min_prefix_Q()
        num = 1 - mq
        if hg >= 1:
            return None
        return (num / (1 - lo), num / (1 - hg))


# ------------------------------------------------------- float linear algebra
#
# Present ONLY to find candidates fast.  Nothing in this file's verdict path calls it:
# `lambda2_gt` / `lambda2_bracket` / `c_bracket` are exact and independent of it.


def h_basis(n):
    """An orthonormal basis of H = 1^perp (Gram-Schmidt on e_i - e_{i+1}).  FLOAT."""
    B = []
    for i in range(n - 1):
        v = [0.0] * n
        v[i], v[i + 1] = 1.0, -1.0
        for b in B:
            c = sum(v[j] * b[j] for j in range(n))
            v = [v[j] - c * b[j] for j in range(n)]
        nrm = math.sqrt(sum(x * x for x in v))
        B.append([x / nrm for x in v])
    return B


def jacobi(Ain, iters=100, tol=1e-14):
    """(eigenvalues, eigenvectors-as-rows) of a small symmetric matrix.  FLOAT."""
    m = len(Ain)
    A = [row[:] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    for _ in range(iters):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(m) for j in range(m) if i != j))
        if off < tol:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                if abs(A[p][q]) < 1e-18:
                    continue
                theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
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
    vals = [A[i][i] for i in range(m)]
    vecs = [[V[k][i] for k in range(m)] for i in range(m)]
    return vals, vecs


# --------------------------------------------------------------- populations


def all_posets(n):
    """EVERY naturally labelled poset on {0..n-1}, each exactly once.

    Enumerated BY EXTENSION, not by masking 2^C(n,2) relations: because the identity is a
    linear extension, nothing sits above n-1, so a poset on [n] is a poset on [n-1] plus
    a choice of DOWN-CLOSED subset of it as the strict down-set of n-1.  The bijection is
    what makes n = 7 (96 428 posets) reachable at all; `s0` checks the counts against the
    2^C(n,2) path at n <= 5 and against mg-76b2's published population at n <= 6.
    """
    if n == 0:
        return [Poset(0, [])]
    out = []
    for P in all_posets(n - 1):
        for D in P.downsets():
            down = list(P.down) + [D]
            out.append(Poset(n, down))
    return out


def all_posets_bymask(n):
    """The SAME population by the 2^C(n,2) transitive-closure route.  Control only."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    for mask in range(1 << len(pairs)):
        rel = {pairs[i] for i in range(len(pairs)) if mask >> i & 1}
        if all((a, d) in rel for (a, b) in rel for (c, d) in rel if b == c):
            down = [0] * n
            for (x, y) in rel:
                down[y] |= 1 << x
            out.append(Poset(n, down))
    return out


def poset_from_relations(n, rel):
    """Build from a list of strict pairs (x, y), x < y.  Transitively closed here."""
    down = [0] * n
    rel = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d))
                    changed = True
    for (x, y) in rel:
        assert x < y, f"identity is not a linear extension ({x},{y})"
        down[y] |= 1 << x
    return Poset(n, down)


C_THRESH_EXIST = F(4, 5)          # c > 1 - eps_leak            (mg-76b2 sec.5 prose)
C_THRESH_SELF = F(40, 49)         # c >= (1-eps_leak)/(1-eps_spec)  (s3_c3.py, sec.7)
EPS_LEAK = F(1, 5)
EPS_SPEC = EPS_LEAK ** 2 / 2
