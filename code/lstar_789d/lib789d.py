"""lib789d -- mg-789d's instrument for (L*):   M^2 > 2 gamma  ==>  mu_pref * Delta_P <= gamma.

WHY THIS FILE EXISTS AND HOW IT DIFFERS FROM libc50b.

mg-c50b's instrument works in the `psi_k` basis: the quadratic forms Q (cut form) and
N (bridge covariance) on the (n-1)-dimensional coefficient space, with the monotone
cone realised as {c >= 0}.  That is the corpus's own coordinate system.

This file works in **f-space** -- functions f : positions -> R -- because that is where
the structure the obstruction demands actually lives.  The dictionary is:

    f_i = sum_{k > i} c_k          (0-indexed positions i = 0..n-1)
    c_k = f_{k-1} - f_k            (k = 1..n-1)

    c' Q c = f' (I - A) f = (1/2) sum_{i,j} a_ij (f_i - f_j)^2      (Dirichlet energy)
    c' N c = || f - mean(f) ||^2                                    (n * Var f)
    {c >= 0}  =  {f nonincreasing in the natural labelling}

so that

    gamma    = min over f perp 1        of  E(f)/||f-fbar||^2   = lambda_2(I - A)
    mu_pref  = min over f nonincreasing of  the same
    Delta_P  = max_i (1 - a_ii)
    M        = sum_{i<j} (j-i) a_ij / floor(n^2/4)     (the normalised footrule)

The identity c'Qc = f'(I-A)f is VERIFIED against the psi-basis forms in s0, at every
poset of n <= 6 and on every family member -- it is a control, not an assumption.

Working in f-space buys three things the coefficient space does not give:

  (1) mu_pref becomes "min over consecutive-block partitions", i.e. the faces of the
      monotone cone are BLOCK STRUCTURES on positions, which is a combinatorial object
      of the poset and not a scalar;
  (2) the diagonal a_ii -- hence Delta_P -- is visible in the same coordinates as the
      energy, so the trade-off (L*) asserts can be written down;
  (3) the exact face enumeration gives mu_pref EXACTLY (both directions), where the
      parent's exhibited-vector search gives only an upper bound and the copositivity
      bracket only a lower one.

Every VERDICT is decided on integers (integer-matrix PSD), as in the parent.
"""

from fractions import Fraction
import math

# ---------------------------------------------------------------------------
# 1.  POSETS
# ---------------------------------------------------------------------------
#
# `dn[i]` = bitmask of {j : j <_P i}.  Naturality: dn[i] subset of {0..i-1}.
# Transitivity: dn[j] subset of dn[i] for every j in dn[i].


def downsets(dn, n):
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
    if n == 0:
        yield ()
        return
    for dn in gen_posets(n - 1):
        for D in downsets(dn, n - 1):
            yield dn + (D,)


def transitive_ok(dn, n):
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
    h = [1] * n
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if h[j] + 1 > h[i]:
                h[i] = h[j] + 1
    return max(h) if n else 0


def relabel_natural(rel, n):
    """`rel[i]` = bitmask of strict predecessors, arbitrary labelling -> natural one.

    Returns a `dn` tuple in natural labelling (topological order), or None if `rel`
    is not a poset.  Used to build families without hand-computing labels.
    """
    # transitive closure
    cl = list(rel)
    for _ in range(n):
        new = []
        for i in range(n):
            m, acc = cl[i], cl[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                acc |= cl[j]
            new.append(acc)
        if new == cl:
            break
        cl = new
    for i in range(n):
        if cl[i] >> i & 1:
            return None
    order, placed = [], 0
    seen = 0
    while placed < n:
        prog = False
        for i in range(n):
            if seen >> i & 1:
                continue
            if cl[i] & ~seen == 0:
                order.append(i)
                seen |= 1 << i
                placed += 1
                prog = True
        if not prog:
            return None
    pos = {v: p for p, v in enumerate(order)}
    dn = []
    for p in range(n):
        v = order[p]
        m, mask = cl[v], 0
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            mask |= 1 << pos[j]
        dn.append(mask)
    return tuple(dn)


# ---------------------------------------------------------------------------
# 2.  TRANSPORT
# ---------------------------------------------------------------------------


def transport(dn, n):
    """(LE, PI) with PI[i][j] = #linear extensions placing element i at position j."""
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


# ---------------------------------------------------------------------------
# 3.  LINEAR ALGEBRA -- pure python, symmetric Jacobi
# ---------------------------------------------------------------------------


def jacobi_eig(Ain, m, tol=1e-14, sweeps=100):
    """All eigenvalues/vectors of a symmetric m x m matrix.  Returns (vals, V) with
    V[:, t] the eigenvector for vals[t], vals ascending."""
    A = [row[:] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    for _ in range(sweeps):
        off = 0.0
        for p in range(m):
            for q in range(p + 1, m):
                off += A[p][q] * A[p][q]
        if off <= tol * tol:
            break
        for p in range(m):
            for q in range(p + 1, m):
                if abs(A[p][q]) < 1e-300:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(m):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(m):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
                for k in range(m):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    vals = [A[i][i] for i in range(m)]
    idx = sorted(range(m), key=lambda i: vals[i])
    return [vals[i] for i in idx], [[V[r][i] for i in idx] for r in range(m)]


def cholesky(Ain, m):
    """Lower Cholesky of a PD matrix, or None."""
    L = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = Ain[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 1e-15:
                    return None
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def gen_eig_min(Qm, Nm, m):
    """(lambda_min, vector) of the pencil Q v = lambda N v with N PD.  None if N not PD."""
    L = cholesky(Nm, m)
    if L is None:
        return None, None
    # B = L^-1 Q L^-T
    Y = [[0.0] * m for _ in range(m)]           # Y = L^-1 Q
    for j in range(m):
        for i in range(m):
            s = Qm[i][j] - sum(L[i][k] * Y[k][j] for k in range(i))
            Y[i][j] = s / L[i][i]
    B = [[0.0] * m for _ in range(m)]           # B = Y L^-T  (solve B L^T = Y)
    for i in range(m):
        for j in range(m):
            s = Y[i][j] - sum(B[i][k] * L[j][k] for k in range(j))
            B[i][j] = s / L[j][j]
    for i in range(m):
        for j in range(i + 1, m):
            avg = 0.5 * (B[i][j] + B[j][i])
            B[i][j] = B[j][i] = avg
    vals, V = jacobi_eig(B, m)
    y = [V[r][0] for r in range(m)]
    # v = L^-T y
    v = [0.0] * m
    for i in range(m - 1, -1, -1):
        s = y[i] - sum(L[k][i] * v[k] for k in range(i + 1, m))
        v[i] = s / L[i][i]
    return vals[0], v


def psd_int_exact(R, m):
    """EXACT: is the integer symmetric m x m matrix R positive semidefinite?

    Symmetric CONGRUENCE reduction (repeated Schur complement) in exact Fractions.
    At each step a positive diagonal entry is pivoted to the front and the trailing
    block is replaced by its Schur complement -- a congruence, so it preserves
    definiteness exactly.  When no positive diagonal remains, R is PSD iff the whole
    remaining block is zero (a PSD matrix with a zero diagonal entry has a zero row).
    """
    A = [[Fraction(R[i][j]) for j in range(m)] for i in range(m)]
    for k in range(m):
        p = -1
        for i in range(k, m):
            if A[i][i] > 0:
                p = i
                break
        if p < 0:
            for i in range(k, m):
                for j in range(k, m):
                    if A[i][j] != 0:
                        return False
            return True
        if p != k:
            A[k], A[p] = A[p], A[k]
            for r in range(m):
                A[r][k], A[r][p] = A[r][p], A[r][k]
        d = A[k][k]
        for i in range(k + 1, m):
            f = A[i][k] / d
            if f:
                for j in range(k + 1, m):
                    A[i][j] -= f * A[k][j]
        for i in range(k + 1, m):
            A[k][i] = Fraction(0)
            A[i][k] = Fraction(0)
    return True


# ---------------------------------------------------------------------------
# 4.  THE POSET OBJECT
# ---------------------------------------------------------------------------


class P789:
    """Every scalar exact; float shadows only where labelled `_float`."""

    __slots__ = ("n", "dn", "LE", "PI", "AI", "LK", "dI", "DeltaI", "sumLK",
                 "floor_n2_4", "_gam", "_A", "_mu")

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
        self.sumLK = sum(LK)
        self.floor_n2_4 = (n * n) // 4
        self._gam = None
        self._A = None
        self._mu = None

    # ---- exact scalars ----
    def Delta(self):
        return Fraction(self.DeltaI, self.LE)

    def M(self):
        return Fraction(self.sumLK, self.LE * self.floor_n2_4)

    def phi(self, k):
        return Fraction(self.LK[k], self.LE * min(k, self.n - k))

    def Phi_star(self):
        return min(self.phi(k) for k in range(1, self.n))

    def primitive(self):
        return all(self.LK[k] > 0 for k in range(1, self.n))

    # ---- f-space forms ----
    def Amat(self):
        """a_ij = AI[i][j]/(2 LE) as floats."""
        if self._A is None:
            n, LE = self.n, self.LE
            self._A = [[self.AI[i][j] / (2.0 * LE) for j in range(n)] for i in range(n)]
        return self._A

    def energy_float(self, f):
        A = self.Amat()
        n = self.n
        s = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                d = f[i] - f[j]
                s += A[i][j] * d * d
        return s

    def var_float(self, f):
        n = self.n
        mb = sum(f) / n
        return sum((x - mb) ** 2 for x in f)

    # ---- gamma ----
    def gap_ge(self, t):
        """EXACT: gamma >= t ?    t = a/b Fraction >= 0.

        gamma = min_{f perp 1} f'(I-A)f / ||f||^2.  Both (I-A) and (I - J/n) kill the
        constants, so the condition extends to a PSD test on all of R^n:

            b*n*(2*LE*I - AI)  -  2*LE*a*(n*I - J)   PSD    (integer matrix).
        """
        a, b = t.numerator, t.denominator
        n, LE = self.n, self.LE
        R = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                lhs = (2 * LE if i == j else 0) - self.AI[i][j]
                rhs = (n if i == j else 0) - 1
                R[i][j] = b * n * lhs - 2 * LE * a * rhs
        return psd_int_exact(R, n)

    def gamma_float(self):
        if self._gam is None:
            n = self.n
            A = self.Amat()
            L = [[(1.0 if i == j else 0.0) - A[i][j] for j in range(n)] for i in range(n)]
            vals, _ = jacobi_eig(L, n)
            self._gam = vals[1]
        return self._gam

    def gamma_bracket(self, steps=60):
        lo, hi = Fraction(0), Fraction(2)
        for _ in range(steps):
            mid = (lo + hi) / 2
            if self.gap_ge(mid):
                lo = mid
            else:
                hi = mid
        return lo, hi

    # ---- mu_pref, EXACT by face enumeration ----
    def mu_faces(self, max_faces=1 << 20):
        """EXACT value of mu_pref = min over NONINCREASING f of E(f)/||f-fbar||^2,
        by enumerating the faces of the monotone cone.

        A face is a partition of the positions 0..n-1 into CONSECUTIVE BLOCKS; f is
        constant on each block.  On the relative interior of a face the minimiser is a
        generalised eigenvector of the reduced pencil, so

            mu_pref = min over block partitions B with strictly-decreasing minimiser
                      of  lambda_min( L~(B), N~(B) ).

        Returns (mu, blocks, vec).  Cost 2^(n-1) faces.
        """
        if self._mu is not None:
            return self._mu
        n = self.n
        A = self.Amat()
        best = None
        for cutmask in range(1 << (n - 1)):
            blocks = []
            start = 0
            for i in range(n - 1):
                if cutmask >> i & 1:
                    blocks.append((start, i + 1))
                    start = i + 1
            blocks.append((start, n))
            r = len(blocks)
            if r < 2:
                continue
            # reduced forms
            Lt = [[0.0] * r for _ in range(r)]
            for s in range(r):
                for t in range(r):
                    acc = 0.0
                    for i in range(blocks[s][0], blocks[s][1]):
                        for j in range(blocks[t][0], blocks[t][1]):
                            acc -= A[i][j]
                    Lt[s][t] = acc
                Lt[s][s] += blocks[s][1] - blocks[s][0]
            sz = [b[1] - b[0] for b in blocks]
            Nt = [[(sz[s] if s == t else 0) - sz[s] * sz[t] / n for t in range(r)]
                  for s in range(r)]
            # Nt is PSD with kernel = constants; deflate by fixing sum sz_s v_s = 0
            # via the substitution v_r = -(sum_{s<r} sz_s v_s)/sz_r
            rr = r - 1
            T = [[0.0] * rr for _ in range(r)]
            for s in range(rr):
                T[s][s] = 1.0
                T[r - 1][s] = -sz[s] / sz[r - 1]
            Lp = [[sum(T[a][i] * Lt[a][b] * T[b][j] for a in range(r) for b in range(r))
                   for j in range(rr)] for i in range(rr)]
            Np = [[sum(T[a][i] * Nt[a][b] * T[b][j] for a in range(r) for b in range(r))
                   for j in range(rr)] for i in range(rr)]
            lam, y = gen_eig_min(Lp, Np, rr)
            if lam is None:
                continue
            v = [sum(T[s][j] * y[j] for j in range(rr)) for s in range(r)]
            # orient: strictly decreasing?
            if v[0] < v[-1]:
                v = [-x for x in v]
            ok = all(v[s] > v[s + 1] + 1e-12 for s in range(r - 1))
            if not ok:
                continue
            if best is None or lam < best[0]:
                best = (lam, blocks, v)
        self._mu = best
        return best

    def mu_upper_exact(self, blocks):
        """EXACT rational UPPER bound on mu_pref from an exhibited block partition:
        the best f constant on `blocks` -- computed exactly by minimising the reduced
        Rayleigh quotient over the FLOAT eigenvector rationalised to integers."""
        res = self._reduced_int(blocks)
        return res

    def _reduced_int(self, blocks):
        n, LE = self.n, self.LE
        r = len(blocks)
        lam, y = None, None
        # get the float minimiser on this face, then rationalise
        A = self.Amat()
        Lt = [[0.0] * r for _ in range(r)]
        for s in range(r):
            for t in range(r):
                acc = 0.0
                for i in range(blocks[s][0], blocks[s][1]):
                    for j in range(blocks[t][0], blocks[t][1]):
                        acc -= A[i][j]
                Lt[s][t] = acc
            Lt[s][s] += blocks[s][1] - blocks[s][0]
        sz = [b[1] - b[0] for b in blocks]
        Nt = [[(sz[s] if s == t else 0) - sz[s] * sz[t] / n for t in range(r)]
              for s in range(r)]
        rr = r - 1
        T = [[0.0] * rr for _ in range(r)]
        for s in range(rr):
            T[s][s] = 1.0
            T[r - 1][s] = -sz[s] / sz[r - 1]
        Lp = [[sum(T[a][i] * Lt[a][b] * T[b][j] for a in range(r) for b in range(r))
               for j in range(rr)] for i in range(rr)]
        Np = [[sum(T[a][i] * Nt[a][b] * T[b][j] for a in range(r) for b in range(r))
               for j in range(rr)] for i in range(rr)]
        lam, y = gen_eig_min(Lp, Np, rr)
        if lam is None:
            return None
        v = [sum(T[s][j] * y[j] for j in range(rr)) for s in range(r)]
        if v[0] < v[-1]:
            v = [-x for x in v]
        # expand to an f on positions, rationalise to integers with denominator 2^20
        f = [0] * n
        for s, (a, b) in enumerate(blocks):
            for i in range(a, b):
                f[i] = v[s]
        scale = max(abs(x) for x in f) or 1.0
        DEN = 1 << 16
        fi = [int(round(DEN * x / scale)) for x in f]
        if max(fi) == min(fi):
            return None
        # exact Rayleigh:  E = (1/(2*2LE)) sum_ij AI_ij (fi-fj)^2 ;  V = ||fi - mean||^2
        num = 0
        for i in range(n):
            for j in range(i + 1, n):
                d = fi[i] - fi[j]
                num += self.AI[i][j] * d * d
        # E(f) = num / (2 LE)     [ (1/2) * sum over ordered pairs = sum over i<j ]
        s1 = sum(fi)
        den = n * sum(x * x for x in fi) - s1 * s1     # = n * ||fi - mean||^2
        if den <= 0:
            return None
        # ratio = (num/(2LE)) / (den/n) = n*num / (2*LE*den)
        return Fraction(n * num, 2 * self.LE * den), fi

    # ---- mu_pref, FAST UPPER bound (the direction that certifies (L*)) ----
    def mu_ub_float(self):
        """Best exhibited nonincreasing f: an UPPER bound on mu_pref, in floats.

        Screening on an UPPER bound is what makes the counterexample hunt RIGOROUS in
        the direction it has to be: mu_pref <= mu_ub, so every poset with
        mu_pref * Delta > gamma also has mu_ub * Delta > gamma.  Nothing is missed by
        the screen; candidates it passes are then treated exactly.

        DEFECT OF MY OWN, REPAIRED HERE AND RECORDED.  The first version of this method
        returned lambda_min of the face's SUBSPACE without checking that the minimiser is
        nonincreasing.  On the face with every cut present that subspace is all of R^n, so
        the method returned gamma at every poset -- not an upper bound on mu_pref at all,
        but a lower one, and the hunt built on it read rho = 1 everywhere.  My own n = 6
        validation did not catch it because I scored it as `max(mu_ub - mu_exact)`, which
        is blind to mu_ub < mu_exact: a one-sided control read as if it were two-sided.
        s0 arm A5b now compares BOTH directions at every primitive poset of n <= 7.

        Only faces whose minimiser is genuinely in the cone are recorded, so the value
        returned is the Rayleigh quotient of an EXHIBITED nonincreasing f.

        Returns (mu_ub, blocks).
        """
        n = self.n
        A = self.Amat()

        def face_val(blocks):
            r = len(blocks)
            if r < 2:
                return None, None
            Lt = [[0.0] * r for _ in range(r)]
            for s in range(r):
                for t in range(r):
                    acc = 0.0
                    for i in range(blocks[s][0], blocks[s][1]):
                        for j in range(blocks[t][0], blocks[t][1]):
                            acc -= A[i][j]
                    Lt[s][t] = acc
                Lt[s][s] += blocks[s][1] - blocks[s][0]
            sz = [b[1] - b[0] for b in blocks]
            Nt = [[(sz[s] if s == t else 0) - sz[s] * sz[t] / n for t in range(r)]
                  for s in range(r)]
            rr = r - 1
            T = [[0.0] * rr for _ in range(r)]
            for s in range(rr):
                T[s][s] = 1.0
                T[r - 1][s] = -sz[s] / sz[r - 1]
            Lp = [[sum(T[a][i] * Lt[a][b] * T[b][j] for a in range(r) for b in range(r))
                   for j in range(rr)] for i in range(rr)]
            Np = [[sum(T[a][i] * Nt[a][b] * T[b][j] for a in range(r) for b in range(r))
                   for j in range(rr)] for i in range(rr)]
            lam, y = gen_eig_min(Lp, Np, rr)
            if lam is None:
                return None, None
            v = [sum(T[s][j] * y[j] for j in range(rr)) for s in range(r)]
            if v[0] < v[-1]:
                v = [-x for x in v]
            return lam, v

        def blocks_of(cuts):
            bl, start = [], 0
            for i in sorted(cuts):
                bl.append((start, i))
                start = i
            bl.append((start, n))
            return bl

        best = [float("inf"), None]

        def offer(bl):
            """Record this face ONLY if its minimiser is genuinely nonincreasing, i.e.
            only if the f it exhibits lies in the monotone cone -- that is the whole
            content of the repair recorded in this method's docstring."""
            lam, v = face_val(bl)
            if lam is None:
                return None
            if all(v[s] - v[s + 1] >= -1e-11 for s in range(len(v) - 1)):
                if lam < best[0]:
                    best[0], best[1] = lam, bl
            return v

        # (i) single cuts -- the prefix indicators 1_{A_k}, always in the cone
        for k in range(1, n):
            offer(blocks_of({k}))
        # (ii) every pair of cuts
        for k in range(1, n):
            for l in range(k + 1, n):
                offer(blocks_of({k, l}))
        # (iii) active-set descent from the FULL cut set: solve on the face, merge the
        #       adjacent blocks whose gap has gone the wrong way, repeat.  Each iterate
        #       is offered, and `offer` discards the ones outside the cone.
        cuts = set(range(1, n))
        for _ in range(2 * n):
            bl = blocks_of(cuts)
            v = offer(bl)
            if v is None:
                break
            keep = set()
            for s in range(len(bl) - 1):
                if v[s] - v[s + 1] > 1e-11:
                    keep.add(bl[s][1])
            if not keep or keep == cuts:
                break
            cuts = keep
        return (best[0], best[1])

    # ---- convenience ----
    def rho_float(self):
        mb = self.mu_faces()
        return mb[0] / self.gamma_float()

    def summary_float(self):
        g = self.gamma_float()
        mb = self.mu_faces()
        mu = mb[0]
        D = float(self.Delta())
        M = float(self.M())
        return dict(gamma=g, mu=mu, Delta=D, M=M, rho=mu / g, rhoD=mu * D / g,
                    uF=M / math.sqrt(2 * g) if g > 0 else float("inf"),
                    Ffails=M * M > 2 * g, blocks=mb[1])


# ---------------------------------------------------------------------------
# 5.  FAMILIES
# ---------------------------------------------------------------------------


def fam_chain_plus_points(nchain, npts):
    """chain(nchain) with `npts` isolated points.  n = nchain + npts."""
    n = nchain + npts
    rel = [0] * n
    for i in range(1, nchain):
        rel[i] = 1 << (i - 1)
    return relabel_natural(rel, n), n


def fam_bipartite_minus(a, b, drops):
    """Complete bipartite poset K_{a,b} (a minimals below b maximals) with the listed
    (min, max) relations DROPPED.  drops is a list of (i, j), i<a, j<b."""
    n = a + b
    rel = [0] * n
    dset = set(drops)
    for j in range(b):
        m = 0
        for i in range(a):
            if (i, j) not in dset:
                m |= 1 << i
        rel[a + j] = m
    return relabel_natural(rel, n), n


def fam_bipartite_plus_points(a, b, drops, npts):
    n = a + b + npts
    rel = [0] * n
    dset = set(drops)
    for j in range(b):
        m = 0
        for i in range(a):
            if (i, j) not in dset:
                m |= 1 << i
        rel[a + j] = m
    return relabel_natural(rel, n), n


def fam_blocks(sizes, drops=()):
    """A `height = len(sizes)` layered poset: consecutive layers completely related,
    with (layer, i, j) triples in `drops` removing the cover (layer i -> layer+1 j)."""
    n = sum(sizes)
    off = []
    s = 0
    for z in sizes:
        off.append(s)
        s += z
    rel = [0] * n
    dset = set(drops)
    for L in range(1, len(sizes)):
        for j in range(sizes[L]):
            m = 0
            for i in range(sizes[L - 1]):
                if (L - 1, i, j) not in dset:
                    m |= 1 << (off[L - 1] + i)
            rel[off[L] + j] = m
    return relabel_natural(rel, n), n
