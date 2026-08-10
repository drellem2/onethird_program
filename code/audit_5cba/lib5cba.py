"""lib5cba -- mg-5cba's INDEPENDENT AUDIT instrument for mg-789d's refutation of (L*).

Written from the CORPUS's definitions, re-derived here, and NOT from `lib789d.py`
(unopened while this file was written; see out_a0_selftest.txt arm S0).  The only
prior instrument consulted for definitions is `code/anticorrelation_c50b/libc50b.py`
sections 1-3, which is the parent's *parent* and an independent implementation of
the same objects -- so agreement between this file and lib789d.py is agreement
between two files neither of which was copied from the other.

THE OBJECTS, restated so the audit does not inherit a definition by reference.

  P            a NATURALLY LABELLED poset on {0..n-1}: `dn[i]` = bitmask of the
               strict lower set of i, forced to be a subset of {0..i-1}.
  LE           # linear extensions of P.
  PI[i][j]     # linear extensions placing element i at position j.  (S_P)_ij = PI/LE.
  AI[i][j]     PI[i][j] + PI[j][i].          a_ij = AI/(2 LE),  A = (S_P + S_P^T)/2.
  d_i          1 - (S_P)_ii,   Delta_P = max_i d_i.
  leak(A_k)    k - sum_{i<k, j<k} (S_P)_ij   for k = 1..n-1.
  M            (sum_k leak(A_k)) / floor(n^2/4).
  primitive    leak(A_k) > 0 for every k = 1..n-1.

  psi_k        1_{[0,k)} - (k/n) 1,  k = 1..n-1: a basis of 1^perp.
  Q_kl         <psi_k, (I-A) psi_l> = sum_{i<min(k,l)} sum_{j>=max(k,l)} a_ij
                                    = QI[k][l] / (2 LE).
  N_kl         <psi_k, psi_l> = min(k,l) - kl/n = NI[k][l] / n.

  gamma        min over c != 0        of c'Qc / c'Nc   ( = 1 - lambda_2(A) ).
  mu_pref      min over c >= 0, c != 0 of c'Qc / c'Nc.
               {c >= 0} is exactly {f nonincreasing} because psi_k are the extreme
               rays of the monotone centred cone.

THE ONE INTEGER MATRIX.  For a rational t = a/b > 0,

        R(a,b) := b*n*QI - 2*LE*a*NI            ( = 2*LE*b*n * (Q - tN) )

  is an INTEGER matrix, and

        gamma   >= t   <==>   R(a,b) is PSD
        mu_pref >= t   <==>   R(a,b) is COPOSITIVE

  Both tests below are decided in integers / Fractions.  NO FLOAT IS ON ANY
  VERDICT PATH.  Floats appear only in `*_float` helpers used to *search* for
  candidates and to print approximations.

COPOSITIVITY, decided exactly and completely (this is the load-bearing routine).

  Claim.  A symmetric R (m x m) is NOT copositive
          <==>  for some nonempty S subset [m], the system

                    R_S y = 1_S      and      y < 0  (strictly, componentwise)

                is feasible.

  Proof.  (=>) If R is not copositive then min{c'Rc : c >= 0, sum c = 1} = v < 0 and
  is attained at some c* with support S (the simplex is compact).  KKT for that
  program gives 2 R c* = lam*1 + w, w >= 0, w_i c*_i = 0, so (R_S c*_S)_i = lam/2 for
  i in S; pairing with c*_S gives lam/2 = c*'Rc* = v.  Put y = c*_S / v: then
  R_S y = 1_S and y < 0 because c*_S > 0 and v < 0.
  (<=) If R_S y = 1_S with y < 0 then sum(y) < 0; put c = y/sum(y) > 0, extended by
  zeros.  Then sum c = 1, c >= 0, and c'Rc = y'R_S y / sum(y)^2 = y'1 / sum(y)^2
  = 1/sum(y) < 0.  []

  This criterion needs no nonsingularity assumption: when R_S is singular the
  question "is {y : R_S y = 1_S, y < 0} nonempty?" is a strict linear feasibility
  problem, solved here exactly by Fourier-Motzkin over the nullspace coordinates.
  A singular face is therefore DECIDED, not refused and not guessed.
"""

from fractions import Fraction
from itertools import combinations

# Instrumentation: how many SINGULAR faces the copositivity routine met, and how
# many of them it DECIDED (rather than refused).  These must be equal.
SINGULAR_FACES = 0
SINGULAR_FACES_DECIDED = 0

# ---------------------------------------------------------------------------
# 1.  Population
# ---------------------------------------------------------------------------


def order_ideals(dn, n):
    """Every order ideal of `dn`, as a bitmask, in increasing numeric order."""
    out = []
    for D in range(1 << n):
        m, ok = D, True
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
    """Every naturally labelled poset on [n], as a tuple `dn` of length n.

    Element n-1 is maximal in any naturally labelled poset, so a poset on [n] is a
    poset on [n-1] plus an order ideal of it (the strict lower set of n-1).
    """
    if n == 0:
        yield ()
        return
    for dn in gen_posets(n - 1):
        for D in order_ideals(dn, n - 1):
            yield dn + (D,)


def is_natural_transitive(dn, n):
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
    """Longest chain counted in ELEMENTS."""
    h = [1] * n
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if h[j] + 1 > h[i]:
                h[i] = h[j] + 1
    return max(h) if n else 0


# ---------------------------------------------------------------------------
# 2.  Transport: PI[i][j] = #linear extensions putting element i at position j
# ---------------------------------------------------------------------------


def transport(dn, n):
    """Return (LE, PI).  Independent DP: ideals bucketed by popcount.

    up[D]   = #linear extensions of the ideal D (as a poset in its own right)
    down[D] = #linear extensions of the complementary filter [n]\\D
    Element i sits at position |D| in up[D]*down[D | 1<<i] extensions, for every
    ideal D with i not in D and the lower set of i inside D.
    """
    full = (1 << n) - 1
    ideals = order_ideals(dn, n)
    bysize = {}
    for D in ideals:
        bysize.setdefault(bin(D).count("1"), []).append(D)
    idset = set(ideals)

    up = {0: 1}
    for k in range(1, n + 1):
        for D in bysize.get(k, ()):
            t = 0
            m = D
            while m:
                i = (m & -m).bit_length() - 1
                m &= m - 1
                E = D ^ (1 << i)
                if E in idset:
                    t += up[E]
            up[D] = t
    down = {full: 1}
    for k in range(n - 1, -1, -1):
        for D in bysize.get(k, ()):
            t = 0
            for i in range(n):
                if not (D >> i & 1) and not (dn[i] & ~D):
                    t += down[D | (1 << i)]
            down[D] = t
    LE = up[full]
    PI = [[0] * n for _ in range(n)]
    for D in ideals:
        u = up[D]
        if not u:
            continue
        k = bin(D).count("1")
        for i in range(n):
            if not (D >> i & 1) and not (dn[i] & ~D):
                PI[i][k] += u * down[D | (1 << i)]
    return LE, PI


# ---------------------------------------------------------------------------
# 3.  Exact linear algebra over Fraction
# ---------------------------------------------------------------------------


def psd_int(R, m):
    """EXACT: is the symmetric matrix R (entries int/Fraction) positive SEMIdefinite?

    Symmetric Gaussian elimination.  A zero diagonal entry forces its whole row to
    vanish (else the 2x2 minor [[0,x],[x,d]] = -x^2 < 0); a negative diagonal entry
    is an immediate refusal; otherwise pivot and take the Schur complement.
    """
    A = [[Fraction(R[i][j]) for j in range(m)] for i in range(m)]
    live = list(range(m))
    while live:
        # refuse on any negative diagonal
        for i in live:
            if A[i][i] < 0:
                return False
        p = None
        for i in live:
            if A[i][i] > 0:
                p = i
                break
        if p is None:
            # every live diagonal is 0 -> every live off-diagonal must be 0
            for i in live:
                for j in live:
                    if A[i][j] != 0:
                        return False
            return True
        d = A[p][p]
        rest = [i for i in live if i != p]
        for i in rest:
            f = A[i][p] / d
            if f:
                for j in rest:
                    A[i][j] -= f * A[p][j]
        live = rest
    return True


def solve_exact(Msub, rhs, k):
    """Solve Msub y = rhs exactly.  Return (particular, nullbasis) or None if
    inconsistent.  `particular` is a list of Fractions, `nullbasis` a list of
    vectors spanning ker(Msub)."""
    A = [[Fraction(Msub[i][j]) for j in range(k)] + [Fraction(rhs[i])] for i in range(k)]
    piv = []
    r = 0
    for c in range(k):
        p = None
        for i in range(r, k):
            if A[i][c]:
                p = i
                break
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        d = A[r][c]
        A[r] = [x / d for x in A[r]]
        for i in range(k):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == k:
            break
    for i in range(r, k):
        if A[i][k] != 0 and all(A[i][c] == 0 for c in range(k)):
            return None
    free = [c for c in range(k) if c not in piv]
    x = [Fraction(0)] * k
    for i, c in enumerate(piv):
        x[c] = A[i][k]
    basis = []
    for fc in free:
        z = [Fraction(0)] * k
        z[fc] = Fraction(1)
        for i, c in enumerate(piv):
            z[c] = -A[i][fc]
        basis.append(z)
    return x, basis


def _fm_strict_feasible(rows, d):
    """Exact Fourier-Motzkin.  `rows` is a list of (coeffs[d], const) meaning
    coeffs . z + const < 0.  Return True iff the system has a solution."""
    rows = [(list(c), Fraction(k)) for c, k in rows]
    for _ in range(d):
        pos, neg, zer = [], [], []
        for c, k in rows:
            if c[0] > 0:
                pos.append((c, k))
            elif c[0] < 0:
                neg.append((c, k))
            else:
                zer.append((c[1:], k))
        new = list(zer)
        for cp, kp in pos:
            for cn, kn in neg:
                a, b = cp[0], -cn[0]          # a > 0, b > 0
                # z0 < -(kp + cp[1:].z)/a   and   z0 > -(kn + cn[1:].z)/b
                cc = [b * x + a * y for x, y in zip(cp[1:], cn[1:])]
                kk = b * kp + a * kn
                new.append((cc, kk))
        rows = new
        if len(rows) > 4000:               # guard: never hit at these sizes
            raise RuntimeError("Fourier-Motzkin blowup")
    for c, k in rows:
        if k >= 0:
            return False
    return True


def copositive_int(R, m):
    """EXACT and COMPLETE: is the symmetric matrix R copositive (c'Rc >= 0 for all
    c >= 0)?  Returns (verdict, witness) where witness is None on True and a
    strictly-positive c with c'Rc < 0 on False.

    Uses the criterion proved in this module's docstring: R fails copositivity iff
    for some nonempty support S the system  R_S y = 1_S, y < 0  is feasible.
    """
    global SINGULAR_FACES, SINGULAR_FACES_DECIDED
    idx = list(range(m))
    for size in range(1, m + 1):
        for S in combinations(idx, size):
            Msub = [[R[i][j] for j in S] for i in S]
            sol = solve_exact(Msub, [1] * size, size)
            if sol is None:
                continue
            x, basis = sol
            if not basis:
                if all(v < 0 for v in x):
                    tot = sum(x)
                    c = [Fraction(0)] * m
                    for a, i in enumerate(S):
                        c[i] = x[a] / tot
                    return False, c
                continue
            # y = x + sum z_t basis[t] ;  need y_a < 0 for every a
            SINGULAR_FACES += 1
            SINGULAR_FACES_DECIDED += 1
            rows = []
            for a in range(size):
                rows.append(([b[a] for b in basis], x[a]))
            if _fm_strict_feasible(rows, len(basis)):
                return False, None      # feasible: witness not extracted (never hit)
    return True, None


# ---------------------------------------------------------------------------
# 4.  The poset object
# ---------------------------------------------------------------------------


class P5:
    __slots__ = ("n", "dn", "LE", "PI", "AI", "LK", "QI", "NI", "dI", "DeltaI")

    def __init__(self, dn, n):
        self.n = n
        self.dn = dn
        LE, PI = transport(dn, n)
        self.LE, self.PI = LE, PI
        self.AI = [[PI[i][j] + PI[j][i] for j in range(n)] for i in range(n)]
        self.dI = [LE - PI[i][i] for i in range(n)]
        self.DeltaI = max(self.dI) if n else 0
        LK = [0] * n
        for k in range(1, n):
            s = 0
            for i in range(k):
                for j in range(k):
                    s += PI[i][j]
            LK[k] = k * LE - s
        self.LK = LK
        m = n - 1
        QI = [[0] * m for _ in range(m)]
        for a in range(m):
            for b in range(a, m):
                lo, hi = min(a + 1, b + 1), max(a + 1, b + 1)
                s = 0
                for i in range(lo):
                    row = self.AI[i]
                    for j in range(hi, n):
                        s += row[j]
                QI[a][b] = QI[b][a] = s
        self.QI = QI
        self.NI = [[n * min(a + 1, b + 1) - (a + 1) * (b + 1) for b in range(m)]
                   for a in range(m)]

    # -- exact scalars -------------------------------------------------------
    def Delta(self):
        return Fraction(self.DeltaI, self.LE)

    def M(self):
        return Fraction(sum(self.LK), self.LE * ((self.n * self.n) // 4))

    def primitive(self):
        return all(self.LK[k] > 0 for k in range(1, self.n))

    # -- the one integer matrix ---------------------------------------------
    def Rmat(self, t):
        t = Fraction(t)
        a, b = t.numerator, t.denominator
        m = self.n - 1
        c1, c2 = b * self.n, 2 * self.LE * a
        return [[c1 * self.QI[i][j] - c2 * self.NI[i][j] for j in range(m)]
                for i in range(m)], m

    def gamma_ge(self, t):
        """EXACT.  gamma >= t ?"""
        R, m = self.Rmat(t)
        return psd_int(R, m)

    def mu_ge(self, t):
        """EXACT.  mu_pref >= t ?"""
        R, m = self.Rmat(t)
        return copositive_int(R, m)[0]

    def F_fails(self):
        """EXACT.  (F) reads M^2 <= 2 gamma; it FAILS iff gamma < M^2/2."""
        M = self.M()
        return not self.gamma_ge(M * M / 2)

    def gamma_bracket(self, steps=40):
        lo, hi = Fraction(0), Fraction(2)
        for _ in range(steps):
            mid = (lo + hi) / 2
            if self.gamma_ge(mid):
                lo = mid
            else:
                hi = mid
        return lo, hi

    def mu_bracket(self, steps=30, lo=None, hi=None):
        lo = Fraction(0) if lo is None else Fraction(lo)
        hi = Fraction(2) if hi is None else Fraction(hi)
        for _ in range(steps):
            mid = (lo + hi) / 2
            if self.mu_ge(mid):
                lo = mid
            else:
                hi = mid
        return lo, hi

    # -- float helpers, SEARCH ONLY, never on a verdict path ------------------
    def Qf(self):
        m = self.n - 1
        return [[self.QI[i][j] / (2.0 * self.LE) for j in range(m)] for i in range(m)]

    def Nf(self):
        m = self.n - 1
        return [[self.NI[i][j] / float(self.n) for j in range(m)] for i in range(m)]

    def Af(self):
        n = self.n
        return [[self.AI[i][j] / (2.0 * self.LE) for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------------------
# 5.  Float spectral helpers (SEARCH ONLY)
# ---------------------------------------------------------------------------


def jacobi_eig(Ain, n, sweeps=100):
    """Symmetric eigendecomposition by cyclic Jacobi.  Returns (evals, evecs) with
    evecs[k] the k-th eigenvector.  Pure python; SEARCH ONLY."""
    A = [row[:] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                off += A[i][j] * A[i][j]
        if off < 1e-30:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-18:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + (theta * theta + 1.0) ** 0.5)
                c = 1.0 / (t * t + 1.0) ** 0.5
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
    ev = [A[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: ev[i])
    return [ev[i] for i in order], [[V[r][i] for r in range(n)] for i in order]


def gamma_float(p):
    """1 - lambda_2(A) by direct eigendecomposition of A (independent of Q,N)."""
    ev, _ = jacobi_eig(p.Af(), p.n)
    return 1.0 - ev[-2]


def mu_pref_float(p):
    """mu_pref in f-space by FACE ENUMERATION over consecutive-block partitions,
    WITH the monotonicity check on the minimiser -- the check whose absence is
    mg-789d's own defect D1.

    A face of the monotone cone {f_1 >= ... >= f_n} is a partition of the positions
    into consecutive blocks; its span is the block-constant vectors.  The cone
    minimiser lies in the relative interior of its own face, so it is the minimum
    generalised eigenvector of (I-A, P) restricted to that span -- but ONLY faces
    whose minimiser is genuinely nonincreasing may be counted, otherwise the
    all-singletons face returns gamma and the method silently reports rho = 1.
    """
    n = p.n
    A = p.Af()
    best = None
    bestvec = None
    for mask in range(1 << (n - 1)):
        # bit k set  <=>  a cut between position k and k+1
        blocks, cur = [], [0]
        for k in range(n - 1):
            if mask >> k & 1:
                blocks.append(cur)
                cur = [k + 1]
            else:
                cur.append(k + 1)
        blocks.append(cur)
        r = len(blocks)
        if r == 1:
            continue
        # basis: indicator of each block, weight w_b = |block|
        w = [len(b) for b in blocks]
        # G_ab = <1_a, (I-A) 1_b> ;  H_ab = <1_a, 1_b> - w_a w_b / n
        G = [[0.0] * r for _ in range(r)]
        for a in range(r):
            for b in range(r):
                s = 0.0
                for i in blocks[a]:
                    for j in blocks[b]:
                        s += A[i][j]
                G[a][b] = (w[a] if a == b else 0.0) - s
        H = [[(w[a] if a == b else 0.0) - w[a] * w[b] / float(n) for b in range(r)]
             for a in range(r)]
        # reduce to the centred subspace: drop the last coordinate via
        # sum_b w_b x_b = 0  ->  x_{r-1} = -(sum_{b<r-1} w_b x_b)/w_{r-1}
        d = r - 1
        T = [[0.0] * d for _ in range(r)]
        for b in range(d):
            T[b][b] = 1.0
            T[r - 1][b] = -w[b] / float(w[r - 1])
        GG = [[sum(T[i][a] * G[i][j] * T[j][b] for i in range(r) for j in range(r))
               for b in range(d)] for a in range(d)]
        HH = [[sum(T[i][a] * H[i][j] * T[j][b] for i in range(r) for j in range(r))
               for b in range(d)] for a in range(d)]
        # generalised problem GG x = lam HH x with HH SPD: Cholesky whitening
        L = [[0.0] * d for _ in range(d)]
        ok = True
        for i in range(d):
            for j in range(i + 1):
                s = HH[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    if s <= 1e-14:
                        ok = False
                        break
                    L[i][i] = s ** 0.5
                else:
                    L[i][j] = s / L[j][j]
            if not ok:
                break
        if not ok:
            continue
        # W = L^{-1} GG L^{-T}
        Linv = [[0.0] * d for _ in range(d)]
        for i in range(d):
            Linv[i][i] = 1.0 / L[i][i]
            for j in range(i):
                Linv[i][j] = -sum(L[i][k] * Linv[k][j] for k in range(j, i)) / L[i][i]
        W = [[sum(Linv[a][i] * GG[i][j] * Linv[b][j] for i in range(d) for j in range(d))
              for b in range(d)] for a in range(d)]
        ev, evec = jacobi_eig(W, d)
        lam = ev[0]
        y = evec[0]
        x = [sum(Linv[i][a] * y[i] for i in range(d)) for a in range(d)]
        xb = [0.0] * r
        for b in range(d):
            xb[b] = x[b]
        xb[r - 1] = -sum(w[b] * x[b] for b in range(d)) / float(w[r - 1])
        # THE MONOTONICITY CHECK (D1).  Accept either sign of the eigenvector.
        for sgn in (1.0, -1.0):
            v = [sgn * t for t in xb]
            if all(v[a] >= v[a + 1] - 1e-11 for a in range(r - 1)):
                if best is None or lam < best:
                    best = lam
                    f = []
                    for a in range(r):
                        f += [v[a]] * w[a]
                    bestvec = f
                break
    return best, bestvec
