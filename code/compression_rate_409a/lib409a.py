"""lib409a -- W4's instrument for the RATE question of docs/imports/compression.tex sections 4-5.

INDEPENDENCE, STATED FIRST BECAUSE IT IS THE THING A READER MUST PRICE.
Everything on a verdict path in this file is built here from scratch: posets, linear
extensions, the two compressions, the fibers, the projections Pi_o / Pi_e, the operator
M = 2I - Pi_o - Pi_e, and the BK Dirichlet form.  `lib8bc7` (mg-8bc7's W2 audit) is imported
by ONE arm, r0, and ONLY as a CROSS-CHECK of this file's constructions against a second
implementation.  No verdict in r1..r5 routes through it.  That is deliberate: W2's own D6
records that its a2/a3/a5 share one library and are therefore not independent witnesses of
each other, and this ticket's whole subject is a claim whose truth depends on W2's.

EXACTNESS.  Fractions everywhere on a verdict path.  The only float in this file is
`jacobi_eigenvalues`, which is used for MEASUREMENT (how big is alpha, really) and never for
a verdict.  Every verdict statement here is either a rational comparison or an exhibited
rational test vector.
"""

from fractions import Fraction
from itertools import combinations, product

# --------------------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------------------


def close_rel(n, pairs):
    """Transitive closure of a set of strict relations."""
    rel = set(pairs)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d))
                    changed = True
    return frozenset(rel)


def is_order(n, rel):
    """Irreflexive, transitive, antisymmetric."""
    for (a, b) in rel:
        if a == b or (b, a) in rel:
            return False
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c and (a, d) not in rel:
                return False
    return True


def all_posets(n):
    """Every labeled poset on 0..n-1.  3^C(n,2) candidates; practical to n = 5."""
    prs = list(combinations(range(n), 2))
    for ch in product((0, 1, 2), repeat=len(prs)):
        rel = set()
        for (a, b), c in zip(prs, ch):
            if c == 1:
                rel.add((a, b))
            elif c == 2:
                rel.add((b, a))
        if is_order(n, rel):
            yield frozenset(rel)


def sample_posets(n, k, seed):
    """k pseudo-random labeled posets on n elements, deterministic in `seed`.

    A linear congruential stream, written out rather than imported, so a run is reproducible
    without depending on a library's RNG staying put across versions.
    """
    state = seed & 0xFFFFFFFF
    def rnd():
        nonlocal state
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return state / 0x7FFFFFFF
    seen = set()
    out = []
    guard = 0
    while len(out) < k and guard < 60 * k:
        guard += 1
        perm = list(range(n))
        for i in range(n - 1, 0, -1):
            j = int(rnd() * (i + 1))
            perm[i], perm[j] = perm[j], perm[i]
        p = 0.15 + 0.5 * rnd()
        base = set()
        for a in range(n):
            for b in range(a + 1, n):
                if rnd() < p:
                    base.add((perm[a], perm[b]))
        rel = close_rel(n, base)
        if rel in seen:
            continue
        seen.add(rel)
        out.append(rel)
    return out


def antichain(n):
    return frozenset()


def two_block_ordinal_sum(n):
    """Z_n: the ordinal sum of n/2 two-element antichains, {0,1} < {2,3} < ... (n even).

    THE EXTREMAL OBJECT OF THIS WHOLE TICKET: alpha(Z_n) = 1, the universal ceiling.
    """
    assert n % 2 == 0
    base = set()
    for j in range(n // 2):
        for k in range(j + 1, n // 2):
            for a in (2 * j, 2 * j + 1):
                for b in (2 * k, 2 * k + 1):
                    base.add((a, b))
    return frozenset(base)


def incomparable(n, lt):
    return [(a, b) for a, b in combinations(range(n), 2)
            if (a, b) not in lt and (b, a) not in lt]


# --------------------------------------------------------------------------------------
# linear extensions, the BK chain
# --------------------------------------------------------------------------------------


def linear_extensions(n, lt):
    preds = [set() for _ in range(n)]
    for (i, j) in lt:
        preds[j].add(i)
    out, placed, seq = [], set(), []

    def rec():
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for v in range(n):
            if v not in placed and preds[v] <= placed:
                placed.add(v)
                seq.append(v)
                rec()
                seq.pop()
                placed.discard(v)

    rec()
    return out


def swap(L, i):
    M = list(L)
    M[i], M[i + 1] = M[i + 1], M[i]
    return tuple(M)


def legal(L, i, lt):
    a, b = L[i], L[i + 1]
    return (a, b) not in lt and (b, a) not in lt


# --------------------------------------------------------------------------------------
# the two compressions -- built from the note's own definitions at :14 and :47
# --------------------------------------------------------------------------------------


def blocks_o(n):
    """C_o = (I_2, I_4, ...): the position groups {0,1},{2,3},... (+ trailing singleton)."""
    g = [(2 * j, 2 * j + 1) for j in range(n // 2)]
    if n % 2 == 1:
        g.append((n - 1,))
    return g


def blocks_e(n):
    """C_e = (I_1, I_3, ...): {0}, then {1,2},{3,4},... (+ trailing singleton if n even)."""
    g = [(0,)] + [(2 * j + 1, 2 * j + 2) for j in range((n - 1) // 2)]
    if n % 2 == 0 and n >= 2:
        g.append((n - 1,))
    return g


def fiber_of(L, groups):
    return tuple(tuple(sorted(L[p] for p in g)) for g in groups)


def fiber_map(LEs, groups):
    """compressed state -> list of indices into LEs."""
    out = {}
    for k, L in enumerate(LEs):
        out.setdefault(fiber_of(L, groups), []).append(k)
    return out


def prefix_flags(L, groups):
    """The compressed record C(L) itself, as the note writes it: the tuple of prefixes."""
    flags, seen = [], []
    for g in groups:
        seen.extend(L[p] for p in g)
        flags.append(frozenset(seen))
    return tuple(flags)


# --------------------------------------------------------------------------------------
# functions on L(P), exactly
# --------------------------------------------------------------------------------------


def pair_indicator(n, lt, LEs, x, y):
    """f_xy = 1{x <_L y} -- the pair-orientation indicator Theorem E uses as its test
    function, and a linear statistic in the note's sense (c = delta_{xy})."""
    pos = [{v: i for i, v in enumerate(L)} for L in LEs]
    return [Fraction(1) if p[x] < p[y] else Fraction(0) for p in pos]


def linear_stat(n, lt, LEs, c):
    """f(L) = sum_{x<y, incomparable} c[(x,y)] * 1{x <_L y}."""
    pos = [{v: i for i, v in enumerate(L)} for L in LEs]
    out = []
    for p in pos:
        s = Fraction(0)
        for (x, y), cc in c.items():
            if p[x] < p[y]:
                s += cc
        out.append(s)
    return out


def position_stat(LEs, w):
    """f(L) = sum_x w[x] * pos_L(x).  A pair-orientation linear statistic (see README S3)."""
    out = []
    for L in LEs:
        s = Fraction(0)
        for i, v in enumerate(L):
            s += w[v] * Fraction(i)
        out.append(s)
    return out


def mean(vals):
    return sum(vals) / Fraction(len(vals))


def center(vals):
    m = mean(vals)
    return [v - m for v in vals]


def variance(vals):
    m = mean(vals)
    return sum((v - m) ** 2 for v in vals) / Fraction(len(vals))


def e_cond_var(vals, LEs, groups):
    """E Var(f | C) = <f, (I - Pi) f>, exactly."""
    N = len(LEs)
    tot = Fraction(0)
    for _, idxs in fiber_map(LEs, groups).items():
        m = sum(vals[k] for k in idxs) / Fraction(len(idxs))
        v = sum((vals[k] - m) ** 2 for k in idxs) / Fraction(len(idxs))
        tot += Fraction(len(idxs), N) * v
    return tot


def bk_energy(vals, LEs, n, lt):
    """E_BK(f) = 1/(2(n-1)N) sum_L sum_i (f(tau_i L) - f(L))^2 -- the note's normalization
    at :106 (one of the n-1 adjacent positions uniformly)."""
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    tot = Fraction(0)
    for L in LEs:
        fL = vals[idx[L]]
        for i in range(n - 1):
            if legal(L, i, lt):
                tot += (vals[idx[swap(L, i)]] - fL) ** 2
    return tot / Fraction(2 * (n - 1) * N)


def rayleigh_M(vals, LEs, n):
    """R_M(f) = <f, M f> / <f, f> with M = 2I - Pi_o - Pi_e, on 1-perp.

    <f, M f> = E Var(f | C_o) + E Var(f | C_e) -- exactly the left side of the note's :234.
    Returns None for a constant f.
    """
    v = variance(vals)
    if v == 0:
        return None
    num = e_cond_var(vals, LEs, blocks_o(n)) + e_cond_var(vals, LEs, blocks_e(n))
    return num / v


def rayleigh_BK(vals, LEs, n, lt):
    v = variance(vals)
    if v == 0:
        return None
    return bk_energy(vals, LEs, n, lt) / v


# --------------------------------------------------------------------------------------
# the operator M, as a matrix (measurement paths only)
# --------------------------------------------------------------------------------------


def M_matrix(LEs, n):
    """M = 2I - Pi_o - Pi_e as an N x N rational matrix."""
    N = len(LEs)
    A = [[Fraction(0)] * N for _ in range(N)]
    for k in range(N):
        A[k][k] = Fraction(2)
    for groups in (blocks_o(n), blocks_e(n)):
        for _, idxs in fiber_map(LEs, groups).items():
            w = Fraction(1, len(idxs))
            for a in idxs:
                for b in idxs:
                    A[a][b] -= w
    return A


def jacobi_eigenvalues(A, sweeps=200, tol=1e-13):
    """Symmetric Jacobi.  FLOAT -- measurement only, never a verdict."""
    N = len(A)
    B = [[float(A[i][j]) for j in range(N)] for i in range(N)]
    import math
    for _ in range(sweeps):
        off = 0.0
        for i in range(N):
            for j in range(i + 1, N):
                off += B[i][j] * B[i][j]
        if off <= tol * tol:
            break
        for p in range(N):
            for q in range(p + 1, N):
                if abs(B[p][q]) < 1e-18:
                    continue
                theta = (B[q][q] - B[p][p]) / (2.0 * B[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(N):
                    bkp, bkq = B[k][p], B[k][q]
                    B[k][p] = c * bkp - s * bkq
                    B[k][q] = s * bkp + c * bkq
                for k in range(N):
                    bpk, bqk = B[p][k], B[q][k]
                    B[p][k] = c * bpk - s * bqk
                    B[q][k] = s * bpk + c * bqk
    return sorted(B[i][i] for i in range(N))


def alpha_measured(LEs, n):
    """lam_min of M restricted to 1-perp = SECOND smallest eigenvalue of M.

    M is PSD with M*1 = 0, so the smallest eigenvalue is the 0 carried by the constants.
    FLOAT.  Measurement only.
    """
    if len(LEs) < 2:
        return None
    ev = jacobi_eigenvalues(M_matrix(LEs, n))
    return ev[1]


# --------------------------------------------------------------------------------------
# exact linear algebra for the restricted (linear-statistic) Rayleigh minimum
# --------------------------------------------------------------------------------------


def gram(vectors):
    k = len(vectors)
    return [[sum(a * b for a, b in zip(vectors[i], vectors[j])) for j in range(k)]
            for i in range(k)]


def apply_M(vals, LEs, n):
    """M f, pointwise and exactly."""
    N = len(LEs)
    out = [Fraction(2) * v for v in vals]
    for groups in (blocks_o(n), blocks_e(n)):
        for _, idxs in fiber_map(LEs, groups).items():
            m = sum(vals[k] for k in idxs) / Fraction(len(idxs))
            for k in idxs:
                out[k] -= m
    return out


def min_gen_eig(A, B, sweeps=200):
    """min lam with A v = lam B v, B positive definite.  FLOAT.  Measurement only.

    Cholesky B = L L^T, then the ordinary symmetric problem on L^-1 A L^-T.
    Returns None if B is singular to working precision (a degenerate span).
    """
    import math
    k = len(A)
    if k == 0:
        return None
    Bf = [[float(B[i][j]) for j in range(k)] for i in range(k)]
    Lc = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1):
            s = Bf[i][j] - sum(Lc[i][m] * Lc[j][m] for m in range(j))
            if i == j:
                if s <= 1e-12:
                    return None
                Lc[i][i] = math.sqrt(s)
            else:
                Lc[i][j] = s / Lc[j][j]
    Af = [[float(A[i][j]) for j in range(k)] for i in range(k)]
    # Y = L^-1 A
    Y = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            Y[i][j] = (Af[i][j] - sum(Lc[i][m] * Y[m][j] for m in range(i))) / Lc[i][i]
    # C = Y L^-T
    C = [[0.0] * k for _ in range(k)]
    for j in range(k):
        for i in range(k):
            C[i][j] = (Y[i][j] - sum(C[i][m] * Lc[j][m] for m in range(j))) / Lc[j][j]
    for i in range(k):
        for j in range(i + 1, k):
            avg = 0.5 * (C[i][j] + C[j][i])
            C[i][j] = C[j][i] = avg
    return jacobi_eigenvalues([[Fraction(0)] * 0] if k == 0 else
                              [[__F(C[i][j]) for j in range(k)] for i in range(k)],
                              sweeps=sweeps)[0]


def __F(x):
    return Fraction(x).limit_denominator(10 ** 12)


# --------------------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------------------


def banner(t):
    print()
    print("=" * 88)
    print(t)
    print("=" * 88)


def verdict(ok, label, extra=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + extra) if extra else ""))
    return ok


def frac(x, d=9):
    return f"{float(x):.{d}f}"
