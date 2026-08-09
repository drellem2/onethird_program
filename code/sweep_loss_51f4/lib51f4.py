"""lib51f4 — the instrument for mg-51f4 (THE CHEEGER SWEEP'S LOSS).

Written from scratch for this ticket.  It shares NO source line with `lib28ff.py`,
`lib76b2.py`, `libA94.py`, `lib_d3c7.py`, `lib3969.py` or `lib9461.py`.

The independence that matters here is ALGORITHMIC, not lexical.  `mg-28ff` computes the
transport `T` by enumerating all `n!` permutations and filtering.  This instrument computes
it by a DOWN-SET dynamic program, which is a different algorithm with a different failure
mode -- and it is the reason (a) the agreement asserted in `selftest51f4` A2 is a real
cross-check rather than a tautology, and (b) named families can be pushed past `n = 10`,
where permutation enumeration is impossible.

THE OBJECTS (all as `mg-28ff` / `mg-76b2` define them; restated, not redefined)
-------------------------------------------------------------------------------
`P` is a poset on `{0..n-1}` for which the identity is a linear extension `e`.
`T[x][a] = Pr[x occupies position a]` under a uniform random linear extension;
`S_P = (T + T^T)/2`; the combinatorial Laplacian of the weighted graph `a_ij = (S_P)_ij`
is exactly `I - S_P`.  `gamma = 1 - lambda_std` is the algebraic connectivity of that graph.
`leak(A) = E|A \\ sigma(A)| = w(A, A^c)`, `Phi_P(A) = leak(A)/min(|A|,n-|A|)`,
`Delta_P = max_i (1 - (S_P)_ii)`.

THE OBJECTS THIS TICKET ADDS
----------------------------
`phi_k = Phi_P(A_k)` for the prefixes `A_k = {0..k-1}` -- THE PREFIX-CONDUCTANCE PROFILE.
`Phi*_pref = min_k phi_k`;  `M = sum_k leak(A_k) / sum_k min(k,n-k)`, the `m`-weighted MEAN
of the profile, which is exactly route (F)'s bound `E[D_F]/(2*floor(n^2/4))`.

    c_true(P) = Phi*_pref^2 / (2 gamma)          the truth, route-independent
    c_sharp(P) = sweep(mu_pref, Delta_P)/(2 gamma)   route (M#)
    f_star(P) = M^2 / (2 gamma)                  route (F)
    Lambda_M = c_sharp/c_true                    THE SWEEP'S LOSS
    Lambda_F = M/Phi*_pref                       THE MEDIANT LOSS   (f_star = Lambda_F^2 c_true)
    c_or(P)  = min(c_sharp, f_star)              THE DISJUNCTION -- what the theorem needs

DESIGN COMMITMENTS  (PREDICTIONS.md E3, E5, E9)
-----------------------------------------------
* No float ever decides a published verdict.  `gamma >= r` is decided WITHOUT computing an
  eigenvalue, by exact definiteness of the pencil `Q - rN` in the `psi` basis of `1^perp`
  (`N` is positive definite there, so Sylvester's criterion applies and the leading
  principal minors come out of one fraction-free Bareiss elimination over the integers).
  This is a DIFFERENT device from `mg-28ff`'s Faddeev-LeVerrier coefficient-sign test on the
  `n x n` Laplacian, and A6 asserts the two agree.
* Floats appear only in `cone_min`, whose job is to FIND a candidate monotone vector.  Every
  candidate is rationalised and re-verified exactly before it is believed.
"""

from fractions import Fraction as F
from itertools import combinations, permutations
import math

# ===================================================================== posets


class Pos:
    """A poset on {0..n-1} for which the identity is a linear extension."""

    __slots__ = ("n", "name", "up", "down", "_m")

    def __init__(self, n, rel, name=""):
        self.n = n
        self.name = name
        up = [0] * n            # up[x] = bitmask of strict upper covers-and-above
        rel = set(rel)
        # transitive closure by repeated bit propagation
        for (x, y) in rel:
            assert x < y, f"{name}: identity is not a linear extension ({x},{y})"
            up[x] |= 1 << y
        for x in range(n - 1, -1, -1):
            m = up[x]
            add = 0
            for y in range(x + 1, n):
                if m >> y & 1:
                    add |= up[y]
            up[x] = m | add
        self.up = up
        down = [0] * n
        for x in range(n):
            for y in range(n):
                if up[x] >> y & 1:
                    down[y] |= 1 << x
        self.down = down
        self._m = {}

    def __repr__(self):
        return f"Pos(n={self.n}, {self.name or self.rel_pairs()})"

    def rel_pairs(self):
        return tuple((x, y) for x in range(self.n) for y in range(self.n)
                     if self.up[x] >> y & 1)

    # ---------------------------------------------------- down-set machinery

    def downsets(self):
        """Every down-set as a bitmask, in increasing popcount order.

        A down-set D satisfies:  y in D  and  x < y  =>  x in D.
        Built by growing from the empty set, so the state space visited is EXACTLY the
        down-set lattice and nothing else -- `selftest` A9 asserts the count against a
        brute-force subset scan and against `2^n`.
        """
        if "ds" not in self._m:
            n = self.n
            seen = {0}
            frontier = [0]
            order = [0]
            while frontier:
                nxt = []
                for D in frontier:
                    for x in range(n):
                        if D >> x & 1:
                            continue
                        if self.down[x] & ~D:
                            continue                    # x not minimal in complement
                        E = D | (1 << x)
                        if E not in seen:
                            seen.add(E)
                            nxt.append(E)
                            order.append(E)
                frontier = nxt
            self._m["ds"] = order
        return self._m["ds"]

    def _fg(self):
        """f[D] = # linear extensions of the sub-poset D;  g[D] = # of the complement."""
        if "fg" not in self._m:
            n = self.n
            ds = self.downsets()
            f = {0: 1}
            for D in ds:
                if D == 0:
                    continue
                tot = 0
                for x in range(n):
                    if D >> x & 1 and not (self.up[x] & D):     # x maximal in D
                        tot += f[D ^ (1 << x)]
                f[D] = tot
            full = (1 << n) - 1
            g = {full: 1}
            for D in reversed(ds):
                if D == full:
                    continue
                tot = 0
                for x in range(n):
                    if not (D >> x & 1) and not (self.down[x] & ~D):   # x minimal outside
                        tot += g[D | (1 << x)]
                g[D] = tot
            self._m["fg"] = (f, g)
        return self._m["fg"]

    def nle(self):
        """Number of linear extensions, exact integer."""
        return self._fg()[0][(1 << self.n) - 1]

    def Tint(self):
        """N * T, as an integer matrix:  Tint[x][a] = #{linear extensions with pos(x)=a}."""
        if "Ti" not in self._m:
            n = self.n
            f, g = self._fg()
            M = [[0] * n for _ in range(n)]
            for D in self.downsets():
                a = bin(D).count("1")
                if a >= n:
                    continue
                fD = f[D]
                if not fD:
                    continue
                for x in range(n):
                    if D >> x & 1:
                        continue
                    if self.down[x] & ~D:
                        continue
                    M[x][a] += fD * g[D | (1 << x)]
            self._m["Ti"] = M
        return self._m["Ti"]

    def S(self):
        """S_P = (T + T^T)/2, exact Fractions."""
        if "S" not in self._m:
            n, N = self.n, self.nle()
            Ti = self.Tint()
            self._m["S"] = [[F(Ti[i][j] + Ti[j][i], 2 * N) for j in range(n)]
                            for i in range(n)]
        return self._m["S"]

    def delta_max(self):
        """Delta_P = max_i (1 - (S_P)_ii) = 1 - min_i Pr[pos(i) = i]."""
        if "dm" not in self._m:
            S = self.S()
            self._m["dm"] = max(F(1) - S[i][i] for i in range(self.n))
        return self._m["dm"]

    # ------------------------------------------------------- leaks & profile

    def leak_pref(self, k):
        """leak(A_k) with A_k = {0..k-1}.

        From the DEFINITION as an expected escape count,
        `leak(A_k) = E #{i < k : pos(i) >= k} = (1/N) sum_{i<k} sum_{a>=k} Tint[i][a]`,
        NOT from the matrix -- so `leak == cut weight` is a real cross-check (A3).
        """
        key = ("lk", k)
        if key not in self._m:
            n, N = self.n, self.nle()
            Ti = self.Tint()
            tot = 0
            for i in range(k):
                for a in range(k, n):
                    tot += Ti[i][a]
            self._m[key] = F(tot, N)
        return self._m[key]

    def profile(self):
        """[phi_1, ..., phi_{n-1}] with phi_k = leak(A_k)/min(k, n-k).  Exact."""
        if "pr" not in self._m:
            n = self.n
            self._m["pr"] = [self.leak_pref(k) / min(k, n - k) for k in range(1, n)]
        return self._m["pr"]

    def phi_star_pref(self):
        p = self.profile()
        v = min(p)
        return v, p.index(v) + 1

    def phi_max_pref(self):
        return max(self.profile())

    def M_mean(self):
        """M = sum_k leak(A_k) / sum_k min(k,n-k) -- the m-weighted MEAN of the profile,
        and exactly route (F)'s bound E[D_F]/(2 floor(n^2/4))."""
        if "M" not in self._m:
            n = self.n
            num = sum(self.leak_pref(k) for k in range(1, n))
            den = sum(min(k, n - k) for k in range(1, n))
            self._m["M"] = num / den
        return self._m["M"]

    def E_footrule(self):
        """E[sum_i |i - pos(i)|].  From the transport, exact."""
        if "DF" not in self._m:
            n, N = self.n, self.nle()
            Ti = self.Tint()
            tot = 0
            for i in range(n):
                for a in range(n):
                    tot += Ti[i][a] * abs(i - a)
            self._m["DF"] = F(tot, N)
        return self._m["DF"]

    # -------------------------------------------------------- structure

    def cut_points(self):
        """k with A_k entirely below its complement -- the ordinal-sum decompositions."""
        n = self.n
        out = []
        for k in range(1, n):
            below = (1 << k) - 1
            above = ((1 << n) - 1) ^ below
            if all((self.up[x] & above) == above for x in range(k)):
                out.append(k)
        return out

    def is_primitive(self):
        return not self.cut_points()

    def is_chain(self):
        return self.nle() == 1

    # -------------------------------------------------------- energies

    def energy(self, v):
        """<v,(I-S)v> = sum_{i<j} a_ij (v_i - v_j)^2."""
        S, n = self.S(), self.n
        t = F(0)
        for i in range(n):
            for j in range(i + 1, n):
                if S[i][j]:
                    t += S[i][j] * (v[i] - v[j]) ** 2
        return t

    def rayleigh(self, v):
        s = sum(v)
        assert s == 0, "rayleigh: vector not centred"
        nn = sum(x * x for x in v)
        assert nn != 0
        return self.energy(v) / nn


# ======================================================= the psi basis / pencil

def psi(n, k):
    """psi_k(i) = k/n - 1[i<k]:  centred, NON-DECREASING in i, and {sum c_k psi_k : c>=0}
    is exactly the monotone cone inside 1^perp."""
    return [F(k, n) - (1 if i < k else 0) for i in range(n)]


def pencil(P, closed_form=True):
    """(Q, N) with Q_kl = <psi_k,(I-S)psi_l>, N_kl = <psi_k,psi_l>, exact.

    `closed_form=False` evaluates the two forms literally from the vectors, which is what
    A4 compares the closed form against.
    """
    n = P.n
    if not closed_form:
        S = P.S()
        B = [psi(n, k) for k in range(1, n)]
        Q = [[F(0)] * (n - 1) for _ in range(n - 1)]
        Nm = [[F(0)] * (n - 1) for _ in range(n - 1)]
        for a in range(n - 1):
            for b in range(n - 1):
                u, v = B[a], B[b]
                q = F(0)
                for i in range(n):
                    for j in range(i + 1, n):
                        if S[i][j]:
                            q += S[i][j] * (u[i] - u[j]) * (v[i] - v[j])
                Q[a][b] = q
                Nm[a][b] = sum(u[i] * v[i] for i in range(n))
        return Q, Nm
    S = P.S()
    Q = [[F(0)] * (n - 1) for _ in range(n - 1)]
    for a in range(n - 1):
        k = a + 1
        for b in range(n - 1):
            l = b + 1
            lo, hi = min(k, l), max(k, l)
            t = F(0)
            for i in range(lo):
                for j in range(hi, n):
                    t += S[i][j]
            Q[a][b] = t
    Nm = [[F(min(a + 1, b + 1)) - F((a + 1) * (b + 1), n) for b in range(n - 1)]
          for a in range(n - 1)]
    return Q, Nm


def from_coeffs(n, c):
    v = [F(0)] * n
    for a, ca in enumerate(c):
        if ca:
            p = psi(n, a + 1)
            for i in range(n):
                v[i] += ca * p[i]
    return v


def is_monotone(v):
    return all(v[i] <= v[i + 1] for i in range(len(v) - 1))


# ============================================ EXACT definiteness (Bareiss/Sylvester)

def _lead_minors(A):
    """The leading principal minors of a rational symmetric matrix, exactly.

    Fraction-free Bareiss over a common denominator: after `k` elimination steps the pivot
    `B[k][k]` IS the `(k+1)`-st leading principal minor of the integer matrix, so one
    elimination yields all `m` of them.  A zero pivot means that minor vanishes, and the
    list is truncated with `None` from there (which `pos_definite` reads as "not PD").
    """
    m = len(A)
    if m == 0:
        return []
    den = 1
    for row in A:
        for x in row:
            den = den * x.denominator // math.gcd(den, x.denominator)
    B = [[int(x * den) for x in row] for row in A]
    minors = []
    prev = 1
    for k in range(m):
        if B[k][k] == 0:
            minors.append(F(0))
            minors.extend([None] * (m - k - 1))
            return minors
        minors.append(F(B[k][k], den ** (k + 1)))
        for i in range(k + 1, m):
            for j in range(k + 1, m):
                B[i][j] = (B[i][j] * B[k][k] - B[i][k] * B[k][j]) // prev
        prev = B[k][k]
    return minors


def pos_definite(A):
    """Is the symmetric rational matrix A POSITIVE DEFINITE?  EXACT (Sylvester)."""
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            assert A[i][j] == A[j][i], "pos_definite: not symmetric"
    ms = _lead_minors(A)
    for d in ms:
        if d is None or d <= 0:
            return False
    return True


def pos_semidefinite(A):
    """Is the symmetric rational matrix A POSITIVE SEMIDEFINITE?  EXACT.

    Sylvester's criterion needs ALL principal minors (not just leading ones) for the
    semidefinite case, so this enumerates them.  Used only where a boundary case is
    possible; `gap_at_least` uses the strict test on the pencil, where N > 0.
    """
    m = len(A)
    for r in range(1, m + 1):
        for idx in combinations(range(m), r):
            sub = [[A[i][j] for j in idx] for i in idx]
            if _det(sub) < 0:
                return False
    return True


def _det(A):
    m = len(A)
    if m == 0:
        return F(1)
    Bm = [row[:] for row in A]
    det = F(1)
    for k in range(m):
        p = None
        for i in range(k, m):
            if Bm[i][k] != 0:
                p = i
                break
        if p is None:
            return F(0)
        if p != k:
            Bm[k], Bm[p] = Bm[p], Bm[k]
            det = -det
        det *= Bm[k][k]
        inv = Bm[k][k]
        for i in range(k + 1, m):
            fct = Bm[i][k] / inv
            if fct:
                for j in range(k, m):
                    Bm[i][j] -= fct * Bm[k][j]
    return det


def gap_at_least(P, r):
    """EXACT decision of `gamma = 1 - lambda_std >= r`, no eigenvalue computed.

    gamma is the least eigenvalue of (I - S_P) restricted to 1^perp.  In the psi basis the
    restriction is the pencil (Q, N) with N positive definite, so
        gamma >= r   <=>   Q - rN  is positive semidefinite.
    Decided by the signs of ALL principal minors of Q - rN.
    """
    Q, Nm = pencil(P)
    m = len(Q)
    A = [[Q[i][j] - r * Nm[i][j] for j in range(m)] for i in range(m)]
    return pos_semidefinite(A)


def gap_greater(P, r):
    """EXACT decision of `gamma > r` (Sylvester, leading minors only -- fast path)."""
    Q, Nm = pencil(P)
    m = len(Q)
    A = [[Q[i][j] - r * Nm[i][j] for j in range(m)] for i in range(m)]
    return pos_definite(A)


def gap_bracket(P, lo=F(0), hi=F(2), iters=48):
    """Rational bracket [lo, hi] on gamma by exact bisection.  Every decision exact."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if gap_greater(P, mid):
            lo = mid
        else:
            hi = mid
    return lo, hi


def gap_float(P):
    """gamma as a float, for SEARCH and RANKING only.  Never decides a verdict."""
    Q, Nm = pencil(P)
    m = len(Q)
    if m == 0:
        return 0.0
    Qf = [[float(x) for x in row] for row in Q]
    Nf = [[float(x) for x in row] for row in Nm]
    Li = _chol_inv(Nf)
    B = [[sum(Li[i][a] * Qf[a][b] * Li[j][b] for a in range(m) for b in range(m))
          for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            v = (B[i][j] + B[j][i]) / 2
            B[i][j] = B[j][i] = v
    ev, _ = _jacobi(B)
    return min(ev)


# ------------------------------------------------------------ float helpers

def _chol_inv(Nf):
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
    return Li


def _jacobi(A0, sweeps=100, tol=1e-14):
    A = [row[:] for row in A0]
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


def cone_min(P):
    """min over MONOTONE g perp 1 of R(g), i.e. min_{c>=0} c'Qc/c'Nc.  FLOAT -- a SEARCH.

    The minimum over the closed cone is attained on the relative interior of some face, where
    it is a generalized eigenvector of the restricted pencil with coefficients of one sign.
    Enumerate the 2^(n-1)-1 supports.  Returns (value, coefficient vector c >= 0).
    """
    Q, Nm = pencil(P)
    m = len(Q)
    best = (float("inf"), None)
    for mask in range(1, 1 << m):
        idx = [i for i in range(m) if mask >> i & 1]
        Qs = [[float(Q[i][j]) for j in idx] for i in idx]
        Ns = [[float(Nm[i][j]) for j in idx] for i in idx]
        Li = _chol_inv(Ns)
        r = len(idx)
        B = [[sum(Li[i][a] * Qs[a][b] * Li[j][b] for a in range(r) for b in range(r))
              for j in range(r)] for i in range(r)]
        for i in range(r):
            for j in range(i + 1, r):
                v = (B[i][j] + B[j][i]) / 2
                B[i][j] = B[j][i] = v
        ev, V = _jacobi(B)
        for j in range(r):
            y = [V[i][j] for i in range(r)]
            cs = [sum(Li[a][i] * y[a] for a in range(r)) for i in range(r)]
            if all(x >= -1e-11 for x in cs):
                sg = 1.0
            elif all(x <= 1e-11 for x in cs):
                sg = -1.0
            else:
                continue
            full = [0.0] * m
            for t, i in enumerate(idx):
                full[i] = max(sg * cs[t], 0.0)
            mx = max(full)
            if mx <= 0:
                continue
            full = [x / mx for x in full]
            if ev[j] < best[0]:
                best = (ev[j], full)
    return best



def cone_min_greedy(P, rounds=40):
    """A CHEAP upper bound on mu_pref for large n: coordinate descent on the Rayleigh
    quotient over the monotone cone, started from the Fiedler coefficients clipped to >= 0
    and from every step vector.  FLOAT — a SEARCH.  `cone_min` enumerates 2^(n-1) supports
    and is unusable past n ~ 16; this is what replaces it there, and A13 asserts the two
    agree at every n where both can run.
    """
    Q, Nm = pencil(P)
    m = len(Q)
    Qf = [[float(x) for x in row] for row in Q]
    Nf = [[float(x) for x in row] for row in Nm]

    def rq(c):
        num = sum(c[i] * Qf[i][j] * c[j] for i in range(m) for j in range(m))
        den = sum(c[i] * Nf[i][j] * c[j] for i in range(m) for j in range(m))
        return num / den if den > 0 else float("inf")

    starts = []
    Li = _chol_inv(Nf)
    B = [[sum(Li[i][a] * Qf[a][b] * Li[j][b] for a in range(m) for b in range(m))
          for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            v = (B[i][j] + B[j][i]) / 2
            B[i][j] = B[j][i] = v
    ev, V = _jacobi(B)
    k0 = min(range(m), key=lambda j: ev[j])
    y = [V[i][k0] for i in range(m)]
    c0 = [sum(Li[a][i] * y[a] for a in range(m)) for i in range(m)]
    for sg in (1.0, -1.0):
        starts.append([max(sg * x, 0.0) for x in c0])
    starts.append([1.0] * m)
    for k in range(m):
        e = [0.0] * m
        e[k] = 1.0
        starts.append(e)
    best = (float("inf"), None)
    for c in starts:
        if max(c) <= 0:
            continue
        c = [x / max(c) for x in c]
        cur = rq(c)
        for _ in range(rounds):
            improved = False
            for k in range(m):
                old = c[k]
                for f in (0.0, 0.25, 0.5, 0.75, 1.25, 1.5, 2.0, 4.0):
                    c[k] = old * f if old > 0 else (f - 1.0 if f > 1 else 0.0)
                    if c[k] < 0 or max(c) <= 0:
                        c[k] = old
                        continue
                    v = rq(c)
                    if v < cur - 1e-15:
                        cur, old, improved = v, c[k], True
                c[k] = old
            if not improved:
                break
        if cur < best[0]:
            best = (cur, [x / max(c) for x in c])
    return best


def rationalise(c, den=5040):
    out = [F(max(0, round(x * den)), den) for x in c]
    if all(x == 0 for x in out):
        out[0] = F(1)
    return out


def _solve(A, b):
    """Exact solve A x = b for square rational A.  Returns None if A is singular."""
    m = len(A)
    Mx = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(m):
        p = None
        for i in range(k, m):
            if Mx[i][k] != 0:
                p = i
                break
        if p is None:
            return None
        Mx[k], Mx[p] = Mx[p], Mx[k]
        pv = Mx[k][k]
        for i in range(m):
            if i == k or Mx[i][k] == 0:
                continue
            fct = Mx[i][k] / pv
            for j in range(k, m + 1):
                Mx[i][j] -= fct * Mx[k][j]
    return [Mx[i][m] / Mx[i][i] for i in range(m)]


def simplex_min(A):
    """EXACT min of `c' A c` over the standard simplex {c >= 0, sum c = 1}, or None if a
    singular face makes the enumeration inconclusive.

    The minimiser lies in the relative interior of some face `S`, where the KKT condition
    for the single equality constraint reads `(A c)_k = lambda` for every `k in S`.  With
    `A_S` invertible that pins `c_S = A_S^{-1} 1 / (1' A_S^{-1} 1)` and the objective value
    to `lambda = 1/(1' A_S^{-1} 1)`.  Enumerating all `2^m - 1` faces therefore enumerates
    every candidate, and the minimum of the valid ones is the answer.

    `A` copositive  <=>  simplex_min(A) >= 0, because `c' A c` is 2-homogeneous.
    """
    m = len(A)
    best = None
    singular = False
    for mask in range(1, 1 << m):
        idx = [i for i in range(m) if mask >> i & 1]
        r = len(idx)
        # the BORDERED system  [[A_S, -1],[1', 0]] [c; lambda] = [0; 1]
        B = [[A[i][j] for j in idx] + [F(-1)] for i in idx]
        B.append([F(1)] * r + [F(0)])
        sol = _solve(B, [F(0)] * r + [F(1)])
        if sol is None:
            singular = True             # a continuum of KKT points on this face
            continue
        c, lam = sol[:r], sol[r]
        if any(ci < 0 for ci in c):
            continue
        if best is None or lam < best:
            best = lam                  # c'A_S c = lambda * (1'c) = lambda
    if singular:
        return None                     # refuse to answer rather than guess
    return best if best is not None else F(0)


def copositive(A):
    """EXACT: is the symmetric rational matrix A copositive (c'Ac >= 0 for all c >= 0)?

    Returns True/False, or raises if a singular face left the enumeration inconclusive in a
    way that could change the answer (the caller then nudges the threshold).
    """
    v = simplex_min(A)
    if v is None:
        raise ValueError("simplex_min inconclusive (singular face)")
    return v >= 0


def mu_at_least(P, t):
    """EXACT decision of `mu_pref >= t`:  Q - tN copositive over c >= 0."""
    Q, Nm = pencil(P)
    m = len(Q)
    A = [[Q[i][j] - t * Nm[i][j] for j in range(m)] for i in range(m)]
    return copositive(A)


def mu_bracket(P, lo=F(0), hi=F(2), iters=30):
    """EXACT rational bracket on mu_pref by bisection on `mu_at_least`.

    This is the direction `mu_pref` was only MEASURED in by `mg-28ff` (its Sec 10 records
    the cone minimum as a float search whose lower use is a measurement).  Bracketing it
    exactly is what turns "route (M#) fails here" from a measurement into a theorem.
    """
    for _ in range(iters):
        mid = (lo + hi) / 2
        try:
            ok = mu_at_least(P, mid)
        except ValueError:
            mid = mid + F(1, 10 ** 15)
            ok = mu_at_least(P, mid)
        if ok:
            lo = mid
        else:
            hi = mid
    return lo, hi


def mu_pref_exact_upper(P):
    """An EXACT rational upper bound on mu_pref, with the monotone witness that achieves it.

    The float cone minimiser is rationalised (clipped to >= 0, so monotone BY CONSTRUCTION)
    and its Rayleigh quotient recomputed exactly; the named vectors are tried too and the
    best exact value is returned.  Being an UPPER bound is the direction route (M#) needs,
    and every published (M#) certificate rests on this number, never on the float.
    """
    n = P.n
    cands = []
    val, c = (cone_min(P) if n <= 14 else cone_min_greedy(P))
    if c is not None:
        cands.append(rationalise(c))
    for k in range(1, n):                      # every single step vector
        e = [F(0)] * (n - 1)
        e[k - 1] = F(1)
        cands.append(e)
    cands.append([F(1)] * (n - 1))             # the centred position vector g_pos
    best = None
    bestv = None
    for c in cands:
        v = from_coeffs(n, c)
        if all(x == 0 for x in v):
            continue
        r = P.rayleigh(v)
        if best is None or r < best:
            best, bestv = r, v
    return best, bestv


# ================================================== the sweep and the constants

def sweep_bound_sq(dmax, r):
    """`mg-76b2` Lemma 3.1 as `mg-28ff` sharpened it: an EXACT upper bound on Phi*_pref^2
    given Delta_P and r = R(g) for a monotone g perp 1.  Taken as read (mg-28ff Sec 2);
    this ticket does not re-derive it, it measures what it loses."""
    return dmax * dmax if r >= dmax else r * (2 * dmax - r)


class Rec:
    """Every published quantity for one poset, all exact except where named FLOAT."""

    __slots__ = ("P", "n", "gamma_lo", "gamma_hi", "dmax", "phistar", "argk", "phimax",
                 "M", "mu", "c_true_lo", "c_true_hi", "c_sharp_lo", "c_sharp_hi",
                 "f_lo", "f_hi", "primitive")

    def __repr__(self):
        return (f"Rec({self.P.name} n={self.n} gamma~{float(self.gamma_lo):.6f} "
                f"c_true~{float(self.c_true_lo):.6f} c#~{float(self.c_sharp_lo):.6f} "
                f"f*~{float(self.f_lo):.6f})")


def measure(P, iters=40):
    """Fill a Rec.  Every constant comes out as an exact rational BRACKET, because gamma is
    an algebraic number: the bracket endpoints are rationals and every comparison that
    produced them was exact."""
    r = Rec()
    r.P, r.n = P, P.n
    r.primitive = P.is_primitive()
    r.dmax = P.delta_max()
    r.phistar, r.argk = P.phi_star_pref()
    r.phimax = P.phi_max_pref()
    r.M = P.M_mean()
    if not r.primitive:
        r.gamma_lo = r.gamma_hi = F(0)
        r.mu = None
        r.c_true_lo = r.c_true_hi = r.c_sharp_lo = r.c_sharp_hi = r.f_lo = r.f_hi = None
        return r
    r.gamma_lo, r.gamma_hi = gap_bracket(P, iters=iters)
    mu, _ = mu_pref_exact_upper(P)
    r.mu = mu
    sw = sweep_bound_sq(r.dmax, mu)
    r.c_true_lo = r.phistar ** 2 / (2 * r.gamma_hi)
    r.c_true_hi = r.phistar ** 2 / (2 * r.gamma_lo)
    r.c_sharp_lo = sw / (2 * r.gamma_hi)
    r.c_sharp_hi = sw / (2 * r.gamma_lo)
    r.f_lo = r.M ** 2 / (2 * r.gamma_hi)
    r.f_hi = r.M ** 2 / (2 * r.gamma_lo)
    return r


def floor_msharp(r):
    """THE FLOOR (mg-51f4, PREDICTIONS P1):  c_sharp(P) >= Delta_P - gamma/2, ALWAYS.

    Returned as the exact rational lower bracket `Delta_P - gamma_hi/2`.
    """
    return r.dmax - r.gamma_hi / 2


def floor_footrule(n, gamma_lo):
    """The structural floor for route (F):  f* >= rho_n^2 gamma / 2, with
    rho_n = (n^2-1)/(6 floor(n^2/4)), from leak(A_k) >= gamma k(n-k)/n."""
    rho = F(n * n - 1, 6 * (n * n // 4))
    return rho * rho * gamma_lo / 2


# ==================================================================== populations

def all_posets(n):
    """EVERY poset on {0..n-1} for which the identity is a linear extension.

    Enumerated over transitively-closed subsets of the n(n-1)/2 forward pairs, with the
    closure test done on up-set bitmasks.
    """
    pairs = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(pairs)):
        up = [0] * n
        ok = True
        for t, (x, y) in enumerate(pairs):
            if mask >> t & 1:
                up[x] |= 1 << y
        for x in range(n):
            m = up[x]
            need = 0
            for y in range(n):
                if m >> y & 1:
                    need |= up[y]
            if need & ~m:
                ok = False
                break
        if ok:
            out.append(Pos(n, [(x, y) for t, (x, y) in enumerate(pairs) if mask >> t & 1],
                           f"n{n}#{len(out)}"))
    return out


def brute_T(P):
    """Transport by permutation enumeration -- the SLOW, INDEPENDENT path (A2)."""
    n = P.n
    les = [p for p in permutations(range(n))
           if all(p.index(x) < p.index(y)
                  for x in range(n) for y in range(n) if P.up[x] >> y & 1)]
    M = [[0] * n for _ in range(n)]
    for p in les:
        for a, x in enumerate(p):
            M[x][a] += 1
    return M, len(les)


# ------------------------------------------------------------------- families
#
# EVERY function below returns a NAMED FAMILY.  A number computed on one of these is a
# value AT A FAMILY MEMBER and is NEVER a maximum over posets of that size.
# (PREDICTIONS.md E1.)

def fam_antichain(n):
    return Pos(n, [], f"antichain n={n}")


def fam_chain(n):
    return Pos(n, [(i, i + 1) for i in range(n - 1)], f"chain n={n}")


def fam_chain_plus_point(n):
    """A chain on {0..n-2} with one element made incomparable to everything.

    The isolated element is placed LAST in e so the identity stays a linear extension.
    """
    return Pos(n, [(i, i + 1) for i in range(n - 2)], f"chain(n-1)+point n={n}")


def fam_two_chains(n):
    ev = [i for i in range(n) if i % 2 == 0]
    od = [i for i in range(n) if i % 2 == 1]
    rel = [(ev[i], ev[i + 1]) for i in range(len(ev) - 1)]
    rel += [(od[i], od[i + 1]) for i in range(len(od) - 1)]
    return Pos(n, rel, f"two interleaved chains n={n}")


def fam_near_ordinal_antichains(n, missing=1):
    """THE NEAR-ORDINAL SUM.  A = {0..h-1}, B = {h..n-1}, both antichains, every relation
    a < b present EXCEPT `missing` of them (taken as (h-1, h), (h-2, h), ...).

    Removing even one relation makes the poset primitive, but the cut at h stays thin, so
    gamma -> 0 while the OTHER prefixes stay fat.  This is PREDICTIONS P7's candidate.
    """
    h = n // 2
    rel = [(a, b) for a in range(h) for b in range(h, n)]
    drop = [(h - 1 - t, h) for t in range(missing)]
    rel = [p for p in rel if p not in drop]
    return Pos(n, rel, f"near-ordinal antichains (missing {missing}) n={n}")


def fam_near_ordinal_chains(n, missing=1):
    """Two CHAINS in ordinal sum with `missing` cross relations removed."""
    h = n // 2
    rel = [(i, i + 1) for i in range(h - 1)] + [(i, i + 1) for i in range(h, n - 1)]
    cross = [(a, b) for a in range(h) for b in range(h, n)]
    drop = [(h - 1 - t, h) for t in range(missing)]
    rel += [p for p in cross if p not in drop]
    return Pos(n, rel, f"near-ordinal chains (missing {missing}) n={n}")


def fam_bipartite_ladder(n):
    """A = {0..h-1} below B = {h..n-1} with a < b iff a and b are NOT paired
    (a perfect matching of non-relations).  Primitive, and the cut at h is thin."""
    h = n // 2
    rel = [(a, b) for a in range(h) for b in range(h, n) if b - h != a]
    return Pos(n, rel, f"bipartite ladder (matching removed) n={n}")


def fam_near_ordinal_plus_point(n, missing=1):
    """THE COMBINED FAMILY: the near-ordinal sum of two antichains on {0..n-2}, plus ONE
    isolated element placed last in e.

    The near-ordinal part supplies the thin bottleneck that kills route (F); the isolated
    element supplies the non-monotone Fiedler direction that kills route (M#).  It is the
    only construction I found on which BOTH route constants rise together, so it is the
    candidate for a poset at which the DISJUNCTION fails.
    """
    m = n - 1
    h = m // 2
    rel = [(a, b) for a in range(h) for b in range(h, m)]
    drop = [(h - 1 - t, h) for t in range(missing)]
    rel = [p for p in rel if p not in drop]
    return Pos(n, rel, f"near-ordinal antichains + isolated point n={n}")


def fam_one_bottom(n):
    return Pos(n, [(0, i) for i in range(1, n)], f"one bottom + antichain n={n}")


def fam_one_top(n):
    return Pos(n, [(i, n - 1) for i in range(n - 1)], f"antichain + one top n={n}")


FAMILIES = [
    ("antichain", fam_antichain),
    ("chain(n-1)+point", fam_chain_plus_point),
    ("two interleaved chains", fam_two_chains),
    ("near-ordinal antichains, 1 missing", lambda n: fam_near_ordinal_antichains(n, 1)),
    ("near-ordinal antichains, 2 missing", lambda n: fam_near_ordinal_antichains(n, 2)),
    ("near-ordinal chains, 1 missing", lambda n: fam_near_ordinal_chains(n, 1)),
    ("bipartite ladder", fam_bipartite_ladder),
    ("near-ordinal antichains + point", fam_near_ordinal_plus_point),
    ("one bottom + antichain", fam_one_bottom),
    ("antichain + one top", fam_one_top),
]
