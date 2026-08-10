"""libc50b — mg-c50b's instrument for THE ANTI-CORRELATION.

Written from the CORPUS's definitions only:

  * `docs/OneThird-C3-PrefixCapture-mg-76b2.md` §2 (the dictionary, S_P, Phi_P, leak)
    and §3 (Lemma 3.1, the sweep, d_i = 1 - (S_P)_ii).
  * `docs/OneThird-L2-Conditionality-mg-28ff.md` §2 (the L2-free theorem, (M#), the
    psi_k basis and the closed forms for Q and N) and §3 (the footrule, (F)).
  * `docs/OneThird-SweepLoss-mg-51f4.md` §1 (Lambda_M, Lambda_F), §2 (the floor), §5.

`code/sweep_loss_51f4/lib51f4.py` was NOT opened before this file was written and its
census produced; see PREDICTIONS.md H3.  No source line is shared with lib28ff, lib76b2,
lib29fe, lib00b3 or lib81ff either -- none of them was opened.

DESIGN DECISION THAT MAKES THE EXACT PATH AFFORDABLE.  Every exact quantity here is an
INTEGER divided by a known denominator, never a `Fraction` carried through a loop:

    (S_P)_ij = PI[i][j] / LE            LE = #linear extensions
    a_ij     = AI[i][j] / (2*LE)        AI = PI + PI^T
    leak(A_k)= LK[k] / LE
    Q_kl     = QI[k][l] / (2*LE)
    N_kl     = NI[k][l] / n

so a test `Q - t N >= 0` with `t = a/b` becomes an INTEGER matrix test

    b*n*QI - 2*LE*a*NI  >=  0 .

Floats appear ONLY in the search for candidate monotone vectors and in reported values.
Every VERDICT ((F) holds/fails, (M#) holds/fails) is decided on integers.
"""

from fractions import Fraction
import math

# ----------------------------------------------------------------------------
# 1.  THE POPULATION -- naturally labelled posets
# ----------------------------------------------------------------------------
#
# A poset on {0,...,n-1} for which the identity is a linear extension is exactly a
# tuple `dn` with `dn[i]` = bitmask of {j : j <_P i}; naturality forces dn[i] subset
# of {0..i-1}, and transitivity forces dn[j] subset of dn[i] for every j in dn[i].
#
# Element n-1 is maximal in every such poset, so the posets on [n] are exactly the
# pairs (poset on [n-1], down-set D of it), D = the strict lower set of n-1.
# 1, 2, 7, 40, 357, 4824, 96428, ... -- this recursion IS the count.


def downsets(dn, n):
    """All order ideals of `dn` as bitmasks, ascending by popcount-free order."""
    out = []
    for D in range(1 << n):
        ok = True
        m = D
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            if dn[i] & ~D:
                ok = False
                break
        if ok:
            out.append(D)
    return out


def gen_posets(n):
    """Yield every naturally labelled poset on [n] as a tuple `dn` of length n."""
    if n == 0:
        yield ()
        return
    for dn in gen_posets(n - 1):
        for D in downsets(dn, n - 1):
            yield dn + (D,)


def transitive_ok(dn, n):
    """Control: naturality + transitivity of a `dn` tuple."""
    for i in range(n):
        if dn[i] >> i:
            return False
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if dn[j] & ~dn[i]:
                return False
    return True


def height(dn, n):
    """Longest chain, counted in ELEMENTS (an antichain has height 1)."""
    h = [1] * n
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if h[j] + 1 > h[i]:
                h[i] = h[j] + 1
    return max(h) if n else 0


def width(dn, n):
    """Largest antichain, by brute force over subsets (n <= 8 only)."""
    comp = [0] * n
    for i in range(n):
        comp[i] = dn[i]
        for j in range(n):
            if dn[j] >> i & 1:
                comp[i] |= 1 << j
    best = 0
    for S in range(1 << n):
        m, ok = S, True
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            if comp[i] & S:
                ok = False
                break
        if ok:
            best = max(best, bin(S).count("1"))
    return best


# ----------------------------------------------------------------------------
# 2.  THE TRANSPORT  S_P  -- down-set dynamic program, exact integers
# ----------------------------------------------------------------------------


def transport(dn, n):
    """Return (LE, PI) with (S_P)_ij = PI[i][j]/LE, PI[i][j] = #{linear extensions
    placing element i at position j}.

    f(D) = #linear extensions of P|D  (D an order ideal)
    g(D) = #linear extensions of P\\D (the complementary filter)
    and element i sits at position |D| in f(D)*g(D + i) extensions.
    """
    full = (1 << n) - 1
    ids = downsets(dn, n)
    idset = set(ids)
    f = {0: 1}
    for D in ids:
        if D == 0:
            continue
        tot = 0
        m = D
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            # i maximal in D  <=>  D without i is still an order ideal
            if (D ^ (1 << i)) in idset:
                tot += f[D ^ (1 << i)]
        f[D] = tot
    g = {full: 1}
    for D in reversed(ids):
        if D == full:
            continue
        tot = 0
        for i in range(n):
            if not (D >> i & 1) and not (dn[i] & ~D):
                tot += g[D | (1 << i)]
        g[D] = tot
    LE = f[full]
    PI = [[0] * n for _ in range(n)]
    for D in ids:
        k = bin(D).count("1")
        fD = f[D]
        if not fD:
            continue
        for i in range(n):
            if not (D >> i & 1) and not (dn[i] & ~D):
                PI[i][k] += fD * g[D | (1 << i)]
    return LE, PI


# ----------------------------------------------------------------------------
# 3.  THE ROUTE INVARIANTS -- all exact
# ----------------------------------------------------------------------------


class Poset:
    """Every field is exact.  `*_i` fields are integers over the stated denominator."""

    __slots__ = ("n", "dn", "LE", "PI", "AI", "LK", "QI", "NI", "dI", "DeltaI",
                 "sumLK", "floor_n2_4", "_gamma")

    def __init__(self, dn, n):
        self.n = n
        self.dn = dn
        LE, PI = transport(dn, n)
        self.LE = LE
        self.PI = PI
        # a_ij = AI[i][j] / (2 LE)
        AI = [[PI[i][j] + PI[j][i] for j in range(n)] for i in range(n)]
        self.AI = AI
        # d_i = 1 - (S_P)_ii  = dI[i]/LE ;  Delta_P = DeltaI/LE
        self.dI = [LE - PI[i][i] for i in range(n)]
        self.DeltaI = max(self.dI) if n else 0
        # leak(A_k) = LK[k]/LE,  k = 1..n-1
        LK = [0] * n
        for k in range(1, n):
            s = 0
            for i in range(k):
                for j in range(k):
                    s += PI[i][j]
            LK[k] = k * LE - s
        self.LK = LK
        self.sumLK = sum(LK)
        self.floor_n2_4 = (n * n) // 4
        # Q_kl = QI[k][l]/(2 LE),  N_kl = NI[k][l]/n ,  k,l = 1..n-1
        m = n - 1
        QI = [[0] * m for _ in range(m)]
        for a in range(m):
            k = a + 1
            for b in range(a, m):
                l = b + 1
                lo, hi = min(k, l), max(k, l)
                s = 0
                for i in range(lo):
                    row = AI[i]
                    for j in range(hi, n):
                        s += row[j]
                QI[a][b] = QI[b][a] = s
        self.QI = QI
        self.NI = [[n * min(a + 1, b + 1) - (a + 1) * (b + 1) for b in range(m)]
                   for a in range(m)]
        self._gamma = None

    # ---- exact scalars -----------------------------------------------------
    def Delta(self):
        return Fraction(self.DeltaI, self.LE)

    def leak(self, k):
        return Fraction(self.LK[k], self.LE)

    def phi(self, k):
        return Fraction(self.LK[k], self.LE * min(k, self.n - k))

    def Phi_star(self):
        return min(self.phi(k) for k in range(1, self.n))

    def M(self):
        return Fraction(self.sumLK, self.LE * self.floor_n2_4)

    def primitive(self):
        return all(self.LK[k] > 0 for k in range(1, self.n))

    # ---- the exact spectral decision ---------------------------------------
    def gap_ge(self, t):
        """EXACT: is gamma = 1 - lambda_std  >=  t ?   (t a Fraction >= 0)

        gamma = min_{c != 0} c^T Q c / c^T N c because {psi_k} spans 1^perp and N > 0.
        So gamma >= t  <=>  Q - t N  PSD  <=>  b*n*QI - 2*LE*a*NI  PSD  for t = a/b.
        """
        a, b = t.numerator, t.denominator
        n, LE = self.n, self.LE
        m = n - 1
        c1, c2 = b * n, 2 * LE * a
        R = [[c1 * self.QI[i][j] - c2 * self.NI[i][j] for j in range(m)] for i in range(m)]
        return psd_int(R, m)

    def gamma_float(self):
        if self._gamma is None:
            m = self.n - 1
            Q = [[self.QI[i][j] / (2.0 * self.LE) for j in range(m)] for i in range(m)]
            N = [[self.NI[i][j] / float(self.n) for j in range(m)] for i in range(m)]
            self._gamma = gen_eig_min(Q, N, m)[0]
        return self._gamma

    def gamma_bracket(self, steps=64):
        """EXACT rational bracket [lo, hi] on gamma, by bisection on gap_ge."""
        lo = Fraction(0)
        hi = Fraction(2)          # gamma <= 2 always (Rayleigh of I - S_P, S_P dstoch)
        for _ in range(steps):
            mid = (lo + hi) / 2
            if self.gap_ge(mid):
                lo = mid
            else:
                hi = mid
        return lo, hi

    # ---- route (F): exact, one PSD decision --------------------------------
    def F_fails(self):
        """EXACT.  (F) reads M^2 <= 2 gamma; it FAILS iff gamma < M^2/2."""
        M = self.M()
        return not self.gap_ge(M * M / 2)

    def f_star_float(self):
        M = float(self.M())
        return M * M / (2.0 * self.gamma_float())

    def c_true_float(self):
        b = float(self.Phi_star())
        return b * b / (2.0 * self.gamma_float())

    # ---- route (M#) --------------------------------------------------------
    def sweep(self, mu):
        """t(2 Delta - t) on [0, Delta], Delta^2 past it -- the THEOREM's two branches
        (mg-28ff repair 7).  Exact for a Fraction `mu`."""
        D = self.Delta()
        return mu * (2 * D - mu) if mu <= D else D * D

    def mu_upper(self):
        """An EXHIBITED monotone vector's Rayleigh quotient: an UPPER bound on mu_pref,
        exact.  Returns (mu_ub, c) with c >= 0 integral.

        Search is float; the returned bound is exact, computed from the rationalised c.
        """
        m = self.n - 1
        Q = [[self.QI[i][j] / (2.0 * self.LE) for j in range(m)] for i in range(m)]
        N = [[self.NI[i][j] / float(self.n) for j in range(m)] for i in range(m)]
        cands = []
        # (i) the singletons psi_k  -- always available, always feasible
        for k in range(m):
            v = [0] * m
            v[k] = 1
            cands.append(v)
        # (ii) every pair
        for i in range(m):
            for j in range(i + 1, m):
                sub = [[Q[i][i], Q[i][j]], [Q[j][i], Q[j][j]]]
                nb = [[N[i][i], N[i][j]], [N[j][i], N[j][j]]]
                _, vec = gen_eig_min(sub, nb, 2)
                if vec is None:
                    continue
                s = 1.0 if (vec[0] + vec[1]) >= 0 else -1.0
                a0, a1 = s * vec[0], s * vec[1]
                if a0 < 0 or a1 < 0:
                    continue
                v = [0] * m
                v[i], v[j] = a0, a1
                cands.append(v)
        # (iii) active-set descent from the full support
        S = list(range(m))
        for _ in range(m):
            if not S:
                break
            sq = [[Q[i][j] for j in S] for i in S]
            sn = [[N[i][j] for j in S] for i in S]
            _, vec = gen_eig_min(sq, sn, len(S))
            if vec is None:
                break
            if sum(vec) < 0:
                vec = [-x for x in vec]
            v = [0.0] * m
            for idx, i in enumerate(S):
                v[i] = vec[idx] if vec[idx] > 0 else 0.0
            if any(x > 0 for x in v):
                cands.append(v)
            keep = [S[idx] for idx in range(len(S)) if vec[idx] > 1e-12]
            if len(keep) == len(S) or not keep:
                break
            S = keep
        best = None
        for v in cands:
            mx = max(v)
            if mx <= 0:
                continue
            cint = [int(round(1024 * x / mx)) for x in v]
            if all(x == 0 for x in cint):
                continue
            num = 0
            for i in range(m):
                if not cint[i]:
                    continue
                for j in range(m):
                    if cint[j]:
                        num += cint[i] * cint[j] * self.QI[i][j]
            den = 0
            for i in range(m):
                if not cint[i]:
                    continue
                for j in range(m):
                    if cint[j]:
                        den += cint[i] * cint[j] * self.NI[i][j]
            if den <= 0:
                continue
            # R = (num/(2LE)) / (den/n) = n*num / (2*LE*den)
            r = Fraction(self.n * num, 2 * self.LE * den)
            if best is None or r < best[0]:
                best = (r, cint)
        return best

    def M_sharp_verdict(self):
        """EXACT verdict for (M#).  Returns one of 'HOLDS', 'FAILS', 'REFUSE'.

        HOLDS  is certified from an exhibited monotone vector (an UPPER bound on
               mu_pref, hence on the sweep): if 2 gamma >= sweep(mu_ub) then c# <= 1.
        FAILS  is certified ONLY from a copositivity lower bound on mu_pref
               (PREDICTIONS.md E3): if 2 gamma < sweep(mu_lo) then c# > 1.
        REFUSE is emitted when neither certificate closes -- never a guess.
        """
        ub = self.mu_upper()
        if ub is None:
            return "REFUSE", None, None
        mu_ub, _ = ub
        s_ub = self.sweep(mu_ub)
        if self.gap_ge(s_ub / 2):
            return "HOLDS", mu_ub, None
        lo, hi, undec = self.mu_lower_bracket(mu_ub)
        if lo is not None and lo > 0:
            s_lo = self.sweep(lo)
            if not self.gap_ge(s_lo / 2):
                return "FAILS", mu_ub, lo
        return "REFUSE", mu_ub, lo

    def copositive(self, t):
        """EXACT: is Q - t N copositive over the monotone cone {c >= 0}?
        Equivalently mu_pref >= t.  Returns (verdict, n_undecided_faces).

        min_{x>=0, sum x = 1} x^T R x is attained; at its support S the KKT
        stationarity is R_S y = e with value 1/sum(y), and every solution of that
        system on every face is enumerated.  A SINGULAR face whose value could be
        negative is REFUSED, never guessed (PREDICTIONS.md E4).
        """
        a, b = t.numerator, t.denominator
        n, LE = self.n, self.LE
        m = n - 1
        R = [[Fraction(b * n * self.QI[i][j] - 2 * LE * a * self.NI[i][j],
                       b * 2 * n * LE) for j in range(m)] for i in range(m)]
        undecided = 0
        ok = True
        for S in range(1, 1 << m):
            idx = [i for i in range(m) if S >> i & 1]
            sub = [[R[i][j] for j in idx] for i in idx]
            y, singular = solve_ones(sub, len(idx))
            if singular:
                # consistent-singular faces all share the same value 1/sum(y);
                # inconsistent ones have no interior stationary point at all.
                if y is None:
                    continue
                sy = sum(y)
                if sy > 0 and all(v >= 0 for v in y):
                    if Fraction(1, 1) / sy < 0:
                        ok = False
                    continue
                undecided += 1
                continue
            sy = sum(y)
            if sy == 0:
                undecided += 1
                continue
            x = [v / sy for v in y]
            if any(v < 0 for v in x):
                continue
            if Fraction(1, 1) / sy < 0:
                ok = False
        return (ok and undecided == 0), undecided

    def mu_lower_bracket(self, mu_ub, steps=30):
        """EXACT lower bound on mu_pref by bisection on `copositive`."""
        lo = Fraction(0)
        hi = mu_ub
        undec_total = 0
        for _ in range(steps):
            mid = (lo + hi) / 2
            cop, u = self.copositive(mid)
            undec_total += u
            if cop:
                lo = mid
            else:
                hi = mid
            if hi - lo < Fraction(1, 10 ** 12):
                break
        return lo, hi, undec_total

    def c_sharp_float(self, mu):
        return float(self.sweep(mu)) / (2.0 * self.gamma_float())


# ----------------------------------------------------------------------------
# 4.  EXACT LINEAR ALGEBRA ON INTEGERS / RATIONALS
# ----------------------------------------------------------------------------


def psd_int(R, m):
    """EXACT: is the symmetric integer matrix R positive semidefinite?

    Symmetric Gaussian elimination.  A negative diagonal entry refutes at once; a zero
    diagonal entry forces its whole row to vanish (else the 2x2 minor is negative);
    otherwise pivot and eliminate.  Exact in Fractions, no float, no char-poly -- and
    cross-checked against brute-force principal minors in s0.
    """
    A = [[Fraction(R[i][j]) for j in range(m)] for i in range(m)]
    live = list(range(m))
    while live:
        p = None
        for i in live:
            if A[i][i] < 0:
                return False
            if A[i][i] > 0 and p is None:
                p = i
        if p is None:
            for i in live:
                for j in live:
                    if A[i][j] != 0:
                        return False
            return True
        piv = A[p][p]
        rest = [i for i in live if i != p]
        for i in rest:
            f = A[p][i] / piv
            if f:
                for j in rest:
                    A[i][j] -= f * A[p][j]
        live = rest
    return True


def psd_minors(R, m):
    """Independent PSD device for the selftest: ALL principal minors >= 0."""
    for S in range(1, 1 << m):
        idx = [i for i in range(m) if S >> i & 1]
        if det_frac([[Fraction(R[i][j]) for j in idx] for i in idx], len(idx)) < 0:
            return False
    return True


def det_frac(A, m):
    A = [row[:] for row in A]
    det = Fraction(1)
    for c in range(m):
        p = None
        for r in range(c, m):
            if A[r][c] != 0:
                p = r
                break
        if p is None:
            return Fraction(0)
        if p != c:
            A[c], A[p] = A[p], A[c]
            det = -det
        det *= A[c][c]
        inv = Fraction(1) / A[c][c]
        for r in range(c + 1, m):
            f = A[r][c] * inv
            if f:
                for k in range(c, m):
                    A[r][k] -= f * A[c][k]
    return det


def solve_ones(A, m):
    """Solve A y = (1,...,1) exactly.  Returns (y, singular_flag); y is None when the
    system is inconsistent."""
    if m == 0:
        return [], False
    M = [[Fraction(A[i][j]) for j in range(m)] + [Fraction(1)] for i in range(m)]
    piv_cols = []
    r = 0
    for c in range(m):
        p = None
        for i in range(r, m):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = Fraction(1) / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(m + 1)]
        piv_cols.append(c)
        r += 1
    for i in range(r, m):
        if M[i][m] != 0:
            return None, True
    if r < m:
        y = [Fraction(0)] * m
        for i, c in enumerate(piv_cols):
            y[c] = M[i][m]
        return y, True
    y = [Fraction(0)] * m
    for i, c in enumerate(piv_cols):
        y[c] = M[i][m]
    return y, False


# ----------------------------------------------------------------------------
# 5.  FLOAT LINEAR ALGEBRA -- SEARCH ONLY, never on a verdict path
# ----------------------------------------------------------------------------


def jacobi(A, m, iters=100):
    """Symmetric eigenproblem by cyclic Jacobi.  Returns (eigvals, eigvecs-as-columns)."""
    a = [row[:] for row in A]
    v = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    for _ in range(iters):
        off = 0.0
        for i in range(m):
            for j in range(i + 1, m):
                off += a[i][j] * a[i][j]
        if off < 1e-30:
            break
        for p in range(m):
            for q in range(p + 1, m):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(m):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(m):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(m):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    return [a[i][i] for i in range(m)], v


def cholesky(N, m):
    L = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = N[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    return None
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def gen_eig_min(Q, N, m):
    """Smallest generalized eigenvalue of (Q, N) with N > 0, and its eigenvector."""
    if m == 0:
        return float("inf"), None
    L = cholesky(N, m)
    if L is None:
        return float("inf"), None
    # B = L^-1 Q L^-T
    Y = [[0.0] * m for _ in range(m)]
    for j in range(m):
        for i in range(m):
            Y[i][j] = (Q[i][j] - sum(L[i][k] * Y[k][j] for k in range(i))) / L[i][i]
    B = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            B[i][j] = (Y[j][i] - sum(L[i][k] * B[k][j] for k in range(i))) / L[i][i]
    for i in range(m):
        for j in range(i + 1, m):
            avg = 0.5 * (B[i][j] + B[j][i])
            B[i][j] = B[j][i] = avg
    vals, vecs = jacobi(B, m)
    k = min(range(m), key=lambda i: vals[i])
    z = [vecs[i][k] for i in range(m)]
    x = [0.0] * m
    for i in range(m - 1, -1, -1):
        x[i] = (z[i] - sum(L[j][i] * x[j] for j in range(i + 1, m))) / L[i][i]
    return vals[k], x


def mu_exhaustive(P):
    """mu_pref by FULL face enumeration in floats: min over every nonempty support S of
    lambda_min(Q_S, N_S) restricted to faces whose bottom eigenvector is signed.

    The minimiser over the closed cone lies in the relative interior of some face S*,
    where it is a local -- hence the global -- minimiser of the Rayleigh quotient on
    span(S*).  So the true mu_pref appears in this list.  SEARCH ONLY: used to audit
    `mu_upper`, never on a verdict path.
    """
    m = P.n - 1
    Q = [[P.QI[i][j] / (2.0 * P.LE) for j in range(m)] for i in range(m)]
    N = [[P.NI[i][j] / float(P.n) for j in range(m)] for i in range(m)]
    best = float("inf")
    bestv = None
    for S in range(1, 1 << m):
        idx = [i for i in range(m) if S >> i & 1]
        sq = [[Q[i][j] for j in idx] for i in idx]
        sn = [[N[i][j] for j in idx] for i in idx]
        lam, vec = gen_eig_min(sq, sn, len(idx))
        if vec is None:
            continue
        if sum(vec) < 0:
            vec = [-x for x in vec]
        if any(x < -1e-11 for x in vec):
            continue
        if lam < best:
            best = lam
            bestv = (idx, vec)
    return best, bestv


def exact_ub_from(P, idx, vec, scale=1 << 20):
    """Rationalise an EXHIBITED nonnegative cone vector and return its EXACT Rayleigh
    quotient -- an upper bound on mu_pref valid however bad the float search was."""
    m = P.n - 1
    mx = max(vec) if vec else 0
    if mx <= 0:
        return None
    c = [0] * m
    for pos, i in enumerate(idx):
        v = vec[pos]
        c[i] = int(round(scale * v / mx)) if v > 0 else 0
    if all(x == 0 for x in c):
        return None
    num = den = 0
    for i in range(m):
        if not c[i]:
            continue
        for j in range(m):
            if c[j]:
                num += c[i] * c[j] * P.QI[i][j]
                den += c[i] * c[j] * P.NI[i][j]
    if den <= 0:
        return None
    return Fraction(P.n * num, 2 * P.LE * den)


def m_sharp_exact(P, mu_ub):
    """EXACT (M#) verdict given an EXACT upper bound mu_ub on mu_pref.
    'FAILS' is emitted only behind a copositivity LOWER bound (PREDICTIONS.md E3)."""
    if mu_ub is None:
        return "REFUSE", None
    if P.gap_ge(P.sweep(mu_ub) / 2):
        return "HOLDS", None
    lo, hi, undec = P.mu_lower_bracket(mu_ub)
    if lo > 0 and not P.gap_ge(P.sweep(lo) / 2):
        return "FAILS", lo
    return "REFUSE", lo
