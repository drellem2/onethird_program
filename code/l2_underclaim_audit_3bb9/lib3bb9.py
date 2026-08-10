"""lib3bb9 — mg-3bb9's audit instrument for mg-b58d's UNDER-CLAIM reversal.

Written from the DEFINITIONS as stated in `docs/OneThird-L2-Conditionality-mg-28ff.md`
(§2, §4, §5) and in mg-29fe's `s3_counterfactual.py` DOCSTRING.  It shares no line of code
with `lib28ff.py`, `lib29fe.py` or `lib51f4.py`.

The definitions, all from the document:

    * population   = every poset on {0..n-1} for which the identity is a linear extension
                     ("naturally labelled"), i.e. every transitively closed subset of
                     {(i,j) : i < j}.
    * T[i][j]      = Pr[pos(i) = j] under a UNIFORM random linear extension.
    * S_P          = (T + T^T)/2                                       (lib28ff docstring)
    * a_ij         = (S_P)_ij  (i != j),   d_i = 1 - (S_P)_ii,   Delta_P = max_i d_i
    * E(h)         = <h,(I-S_P)h> = sum_{i<j} a_ij (h_i-h_j)^2
    * 1-lambda_std = min{ R(g) : g perp 1 }                     (algebraic connectivity)
    * mu_pref      = min{ R(g) : g perp 1, g monotone along e }  (a min over a CONE)
    * rho          = mu_pref / (1-lambda_std)
    * leak(A_k)    = E #{i : i < k <= pos(i)};  P is DECOMPOSABLE iff leak(A_k) = 0 for
                     some k in 1..n-1 (no linear extension moves anything across the cut).
    * psi_k(i)     = k/n - 1[i<k],  k = 1..n-1;  Q_kl = <psi_k,(I-S)psi_l>, N_kl = <psi_k,psi_l>

Exact arithmetic (`Fraction`) for S, Q, N, Delta and every certificate; floats only in the
eigen-solvers, which are used for the SURVEY and never for a certified verdict.
"""
from fractions import Fraction as F
from itertools import combinations
import math

# ------------------------------------------------------------------ posets


def all_natural_posets(n):
    """Every transitively closed R subset of {(i,j) : i<j}, as a frozenset of pairs."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    for mask in range(1 << len(pairs)):
        rel = set(p for b, p in enumerate(pairs) if mask >> b & 1)
        ok = True
        for (i, j) in rel:
            for (k, l) in rel:
                if j == k and (i, l) not in rel:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(frozenset(rel))
    return out


def linear_extensions(n, rel):
    """All permutations pi with pi consistent with rel: pos[i] = index of i in the order."""
    below = [set() for _ in range(n)]
    for (i, j) in rel:
        below[j].add(i)
    res = []
    order = []
    placed = set()

    def rec():
        if len(order) == n:
            res.append(tuple(order))
            return
        for v in range(n):
            if v in placed:
                continue
            if below[v] <= placed:
                placed.add(v)
                order.append(v)
                rec()
                order.pop()
                placed.discard(v)

    rec()
    return res


class P3bb9:
    def __init__(self, n, rel):
        self.n = n
        self.rel = rel
        exts = linear_extensions(n, rel)
        self.n_ext = len(exts)
        N = len(exts)
        cnt = [[0] * n for _ in range(n)]
        for e in exts:
            for pos, v in enumerate(e):
                cnt[v][pos] += 1
        self.T = [[F(cnt[i][j], N) for j in range(n)] for i in range(n)]
        self.S = [[(self.T[i][j] + self.T[j][i]) / 2 for j in range(n)] for i in range(n)]
        self.Delta = max(1 - self.S[i][i] for i in range(n))
        # leak(A_k) = sum_{i<k} sum_{j>=k} T[i][j]
        self.leak = [sum(self.T[i][j] for i in range(k) for j in range(k, n))
                     for k in range(1, n)]

    def decomposable(self):
        return any(L == 0 for L in self.leak)

    def IminusS(self):
        n = self.n
        return [[(1 if i == j else 0) - self.S[i][j] for j in range(n)] for i in range(n)]

    def energy(self, f):
        """<f,(I-S)f> exactly, f a list of Fractions."""
        M = self.IminusS()
        n = self.n
        return sum(f[i] * M[i][j] * f[j] for i in range(n) for j in range(n))


def psi(n, k):
    return [F(k, n) - (1 if i < k else 0) for i in range(n)]


def pencil(P):
    """(Q, N) over k,l = 1..n-1 in the psi basis, exact Fractions."""
    n = P.n
    M = P.IminusS()
    B = [psi(n, k) for k in range(1, n)]
    m = n - 1
    Q = [[sum(B[a][i] * M[i][j] * B[b][j] for i in range(n) for j in range(n))
          for b in range(m)] for a in range(m)]
    N = [[sum(B[a][i] * B[b][i] for i in range(n)) for b in range(m)] for a in range(m)]
    return Q, N


def from_coeffs(n, c):
    """sum_k c_k psi_k — the generic element of the monotone cone when c >= 0."""
    B = [psi(n, k) for k in range(1, n)]
    return [sum(c[a] * B[a][i] for a in range(n - 1)) for i in range(n)]


# --------------------------------------------------------- float eigen (survey only)


def _jacobi(A):
    """Eigenvalues/vectors of a small symmetric float matrix.  Returns (vals, vecs cols)."""
    m = len(A)
    a = [row[:] for row in A]
    v = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    for _ in range(200):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(m) for j in range(m) if i != j))
        if off < 1e-15:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
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
    vals = [a[i][i] for i in range(m)]
    return vals, v


def _chol(Nf):
    m = len(Nf)
    L = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = Nf[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def _forward(L, b):
    m = len(L)
    y = [0.0] * m
    for i in range(m):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    return y


def gen_eigs(Qf, Nf):
    """Generalized symmetric eigenpairs of Q x = lam N x, N positive definite.  Floats."""
    m = len(Qf)
    L = _chol(Nf)
    # C = L^-1 Q L^-T
    tmp = [_forward(L, [Qf[i][j] for i in range(m)]) for j in range(m)]   # columns
    C = [_forward(L, [tmp[j][i] for j in range(m)]) for i in range(m)]
    C = [[(C[i][j] + C[j][i]) / 2 for j in range(m)] for i in range(m)]
    vals, vecs = _jacobi(C)
    out = []
    for idx in range(m):
        y = [vecs[i][idx] for i in range(m)]
        # x = L^-T y
        x = [0.0] * m
        for i in reversed(range(m)):
            x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, m))) / L[i][i]
        out.append((vals[idx], x))
    out.sort(key=lambda t: t[0])
    return out


def l2_first_disjunct(Q, N, tol=1e-8):
    """Does the TOP STANDARD EIGENSPACE meet the monotone cone?  (L2's first disjunct.)

    This is decided WITHOUT computing mu_pref: take the eigenspace of the pencil's smallest
    eigenvalue (= 1-lambda_std) and ask whether it contains a nonzero vector with all
    coefficients >= 0 in the psi basis, i.e. a nondecreasing vector.  Returns
    (holds: bool, dim: int).  This matters because deciding L2 as `mu_pref == 1-lambda_std`
    makes "V00 fails iff L2 fails" TRUE BY CONSTRUCTION; this test does not.
    """
    m = len(Q)
    Qf = [[float(x) for x in row] for row in Q]
    Nf = [[float(x) for x in row] for row in N]
    eigs = gen_eigs(Qf, Nf)
    lam0 = eigs[0][0]
    basis = [v for (lam, v) in eigs if lam <= lam0 + tol * max(1.0, abs(lam0))]
    d = len(basis)
    if d == 1:
        v = basis[0]
        return (all(x >= -1e-9 for x in v) or all(x <= 1e-9 for x in v)), 1
    # d >= 2: is there a nonzero v in span(basis) with v >= 0?  Decided by alternating
    # projection between the subspace and the nonnegative orthant (POCS), from several
    # starts, plus the basis vectors themselves.  A "yes" is CONSTRUCTIVE (a witness is
    # exhibited and checked); only a "no" rests on the search.
    import math as _m
    # Euclidean-orthonormal basis of the span
    onb = []
    for b in basis:
        w = b[:]
        for u in onb:
            d0 = sum(w[i] * u[i] for i in range(m))
            w = [w[i] - d0 * u[i] for i in range(m)]
        nr = _m.sqrt(sum(x * x for x in w))
        if nr > 1e-12:
            onb.append([x / nr for x in w])

    def proj(v):
        out = [0.0] * m
        for u in onb:
            d0 = sum(v[i] * u[i] for i in range(m))
            for i in range(m):
                out[i] += d0 * u[i]
        return out

    starts = [u[:] for u in onb] + [[-x for x in u] for u in onb]
    starts.append([1.0] * m)
    seed = 12345
    for _ in range(24):
        y = []
        for _i in range(m):
            seed = (1103515245 * seed + 12345) % (1 << 31)
            y.append(seed / (1 << 30) - 1.0)
        starts.append(proj(y))
    for v0 in starts:
        v = v0[:]
        for _it in range(400):
            v = [x if x > 0 else 0.0 for x in v]
            v = proj(v)
            nr = max(abs(x) for x in v)
            if nr < 1e-12:
                break
            v = [x / nr for x in v]
        nr = max(abs(x) for x in v)
        if nr > 1e-12 and all(x >= -1e-9 for x in v):
            return True, d
    return False, d


def gap_float(Q, N):
    """1 - lambda_std = smallest generalized eigenvalue of the pencil (float)."""
    Qf = [[float(x) for x in row] for row in Q]
    Nf = [[float(x) for x in row] for row in N]
    return gen_eigs(Qf, Nf)[0][0]


def mu_pref_float(Q, N):
    """min over the CONE c >= 0 of c'Qc/c'Nc, by face enumeration (float).

    The minimum over the cone is attained in the relative interior of some face, where the
    KKT conditions say the restricted pencil has c_S as an eigenvector with c_S > 0.  So the
    minimum is the least such face eigenvalue.  Returns (value, coefficient vector).
    """
    m = len(Q)
    Qf = [[float(x) for x in row] for row in Q]
    Nf = [[float(x) for x in row] for row in N]
    best = None
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            Qs = [[Qf[i][j] for j in S] for i in S]
            Ns = [[Nf[i][j] for j in S] for i in S]
            for lam, x in gen_eigs(Qs, Ns):
                mx = max(abs(t) for t in x)
                if mx == 0:
                    continue
                xn = [t / mx for t in x]
                if all(t > 1e-9 for t in xn) or all(t < -1e-9 for t in xn):
                    sgn = 1.0 if xn[0] > 0 else -1.0
                    full = [0.0] * m
                    for a, i in enumerate(S):
                        full[i] = sgn * xn[a]
                    if best is None or lam < best[0]:
                        best = (lam, full)
    return best


# ------------------------------------------------------- EXACT certificates


def principal_minors_any_negative(M):
    """True iff some principal minor of the exact symmetric matrix M is < 0.

    Certifies NOT positive semidefinite.
    """
    m = len(M)
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            if det([[M[i][j] for j in S] for i in S]) < 0:
                return True
    return False


def psd_exact(M):
    """Exact PSD test: every principal minor >= 0."""
    m = len(M)
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            if det([[M[i][j] for j in S] for i in S]) < 0:
                return False
    return True


def det(M):
    """Exact determinant by fraction-free-ish Gaussian elimination on Fractions."""
    m = len(M)
    A = [row[:] for row in M]
    d = F(1)
    for col in range(m):
        piv = None
        for r in range(col, m):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            return F(0)
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
            d = -d
        d *= A[col][col]
        inv = F(1) / A[col][col]
        for r in range(col + 1, m):
            f = A[r][col] * inv
            if f:
                for c2 in range(col, m):
                    A[r][c2] -= f * A[col][c2]
    return d


def simplex_min(M):
    """EXACT min of c'Mc over {c >= 0, sum c = 1}, M symmetric rational.

    The minimum is attained at a stationary point of some face.  On face S the stationary
    condition is M_S x = t*1 with x > 0 and value 1/(1'x) when 1'x > 0; degenerate faces are
    covered because every face's own sub-faces are enumerated too, and the vertices (r = 1)
    give M_ii.  M is STRICTLY COPOSITIVE iff this minimum is > 0.
    """
    m = len(M)
    best = None
    for i in range(m):                      # vertices, always, even on singular faces
        if best is None or M[i][i] < best:
            best = M[i][i]
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            Ms = [[M[i][j] for j in S] for i in S]
            ones = [F(1)] * r
            x = solve(Ms, ones)
            if x is None:
                continue
            if all(t > 0 for t in x):
                s = sum(x)
                val = F(1) / s
                if best is None or val < best:
                    best = val
            elif all(t < 0 for t in x):
                s = sum(x)
                val = F(1) / s          # negative value: c = x/s is >= 0 and c'Mc = 1/s < 0
                if best is None or val < best:
                    best = val
    return best


def solve(A, b):
    """Exact solve A x = b; None if singular."""
    m = len(A)
    M = [A[i][:] + [b[i]] for i in range(m)]
    for col in range(m):
        piv = None
        for r in range(col, m):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        inv = F(1) / M[col][col]
        for c2 in range(col, m + 1):
            M[col][c2] *= inv
        for r in range(m):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                for c2 in range(col, m + 1):
                    M[r][c2] -= f * M[col][c2]
    return [M[i][m] for i in range(m)]


def sub(Q, N, t):
    """Q - t*N, exact."""
    m = len(Q)
    return [[Q[i][j] - t * N[i][j] for j in range(m)] for i in range(m)]


def bracket_gap_exact(Q, N, iters=40):
    """Rational bracket on 1-lambda_std: PSD(Q - tN) iff t <= 1-lambda_std."""
    lo, hi = F(0), F(2)
    for _ in range(iters):
        mid = (lo + hi) / 2
        if psd_exact(sub(Q, N, mid)):
            lo = mid
        else:
            hi = mid
    return lo, hi


def bracket_mu_exact(Q, N, iters=40):
    """Rational bracket on mu_pref: (Q - tN) strictly copositive iff t < mu_pref."""
    lo, hi = F(0), F(2)
    for _ in range(iters):
        mid = (lo + hi) / 2
        v = simplex_min(sub(Q, N, mid))
        if v is not None and v > 0:
            lo = mid
        else:
            hi = mid
    return lo, hi
