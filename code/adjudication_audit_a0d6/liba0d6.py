"""liba0d6 — the instrument for `mg-a0d6`, THE INDEPENDENT AUDIT OF THE `mg-d19f`
ADJUDICATION.

**WRITTEN FROM SCRATCH AND IMPORTING NOTHING FROM THE SUBJECT.** It shares no source line
with `lib51f4`, `lib28ff`, `lib29fe`, `lib64cb` or `libd19f`, and it does not import them.
The reason is the whole ticket: the landing under audit (`095260c`) settles the adjudication
by reading `168 of 86278` **out of `mg-51f4`'s own transcript** (`out_s3_n7.txt`), which
means the number that decides which of two landed documents is false has been *carried*
through the entire exchange and never *recomputed*. An auditor that imports `lib51f4` cannot
find a defect that lives in `lib51f4`.

THE OBJECTS, RESTATED FROM THE SOURCE DOCUMENTS' OWN DEFINITIONS
---------------------------------------------------------------
`P` is a poset on `{0..n-1}` for which the identity permutation is a linear extension (a
"naturally labelled" poset). `T[x][a] = Pr[x occupies position a]` under a UNIFORM random
linear extension; `S = (T + T^T)/2`; `L = I - S` is the combinatorial Laplacian of the
weighted graph `a_ij = S_ij` (the diagonal works out because `T` is doubly stochastic).

    gamma(P)  = lambda_2(L)  -- the algebraic connectivity, = 1 - lambda_std
    A_k       = {0..k-1}, the prefix cuts
    leak(A)   = E|A \\ sigma(A)| with sigma(A) = {p[i] : i in A}
    M         = sum_k leak(A_k) / sum_k min(k, n-k)      -- the m-weighted profile MEAN
    f*(P)     = M^2 / (2 gamma)                          -- ROUTE (F)

`P` is PRIMITIVE (ordinal-sum-indecomposable w.r.t. the identity) iff no `k` in `1..n-1` has
every `x < k` below every `y >= k`.

HOW A VERDICT IS DECIDED — AND WHY NO FLOAT DECIDES ONE
------------------------------------------------------
Route (F) FAILS at `P` iff `f* > 1`, i.e. iff `M^2 > 2 gamma`, i.e. iff

    gamma  <  M^2 / 2 .

`gamma` is a min of a Rayleigh quotient over `1^perp`, so **any** exhibited `v ⊥ 1` gives
`gamma <= R(v)` — an exact UPPER bound needing no eigensolver at all. So a FAILURE is
certified by exhibiting one rational vector and checking `R(v) < M^2/2` in `Fraction`
arithmetic (`certify_fail`). The other direction, `gamma >= M^2/2`, is certified by an exact
PSD test of `L - t(I - J/n)` via the sign of every coefficient of `det(xI + A)`
(`is_psd_exact`) — no eigenvalue is computed there either.

Floats appear in exactly one place: `gamma_float`, whose job is to FIND candidates and to
order the population. Every published verdict is re-decided exactly. (`PREDICTIONS.md` E2.)
"""

from fractions import Fraction as F
from itertools import permutations

# ------------------------------------------------------------------ posets


def naturally_labelled(n):
    """Every poset on {0..n-1} for which the identity is a linear extension, as a frozenset
    of covering-closed strict pairs (x, y) with x < y.

    Built by adding the elements 0, 1, ... in order: because the identity is a linear
    extension, element `k` may only sit above elements `< k`, and the set below it must be a
    DOWN-SET of the poset already built. Distinct down-sets give distinct posets, so this is
    a bijection and the enumeration is exact.

    Returned as `(n, down)` where `down[x]` is the bitmask of elements strictly below `x`
    (transitively closed).
    """
    out = [tuple([0])]                                   # n = 1: one element, nothing below
    for k in range(1, n):
        nxt = []
        for down in out:
            for ideal in _down_sets_of(down, k):
                d = list(down) + [0]
                # k sits above every element of `ideal` and above everything below those.
                m = ideal
                for x in range(k):
                    if ideal >> x & 1:
                        m |= down[x]
                d[k] = m
                nxt.append(tuple(d))
        out = nxt
    return out


def _down_sets_of(down, k):
    """Every down-set (order ideal) of the poset on {0..k-1} given by `down`, as bitmasks."""
    res = []
    for m in range(1 << k):
        ok = True
        for x in range(k):
            if (m >> x & 1) and (down[x] & ~m):
                ok = False
                break
        if ok:
            res.append(m)
    return res


def is_primitive(n, down):
    """No cut point: no k in 1..n-1 with every x < k below every y >= k."""
    for k in range(1, n):
        cut = True
        for y in range(k, n):
            if (down[y] & ((1 << k) - 1)) != (1 << k) - 1:
                cut = False
                break
        if cut:
            return False
    return True


def rel_pairs(n, down):
    return sorted((x, y) for y in range(n) for x in range(n) if down[y] >> x & 1)


# ------------------------------------------------- transport, by down-set DP


def transport_counts(n, down):
    """(cnt, N) with cnt[x][a] = #{linear extensions placing x at position a} and N the
    number of linear extensions.

    A down-set dynamic program over the 2^n masks: `f[S]` counts the linear orders of the
    down-set `S`, `g[S]` counts the completions of `S`, and a linear extension putting `x` at
    position `|S|` is exactly a pair (order of `S`, completion of `S + x`).
    """
    full = (1 << n) - 1
    isdown = bytearray(full + 1)
    for m in range(full + 1):
        ok = 1
        for x in range(n):
            if (m >> x & 1) and (down[x] & ~m):
                ok = 0
                break
        isdown[m] = ok
    f = [0] * (full + 1)
    f[0] = 1
    for m in range(1, full + 1):                      # subsets precede supersets numerically
        if not isdown[m]:
            continue
        t = 0
        for x in range(n):
            if m >> x & 1:
                p = m ^ (1 << x)
                if isdown[p]:
                    t += f[p]
        f[m] = t
    g = [0] * (full + 1)
    g[full] = 1
    for m in range(full - 1, -1, -1):
        if not isdown[m]:
            continue
        t = 0
        for x in range(n):
            if not (m >> x & 1):
                q = m | (1 << x)
                if isdown[q]:
                    t += g[q]
        g[m] = t
    cnt = [[0] * n for _ in range(n)]
    for m in range(full + 1):
        if not isdown[m] or not f[m]:
            continue
        a = bin(m).count("1")
        for x in range(n):
            if not (m >> x & 1):
                q = m | (1 << x)
                if isdown[q]:
                    cnt[x][a] += f[m] * g[q]
    return cnt, f[full]


def transport_counts_bruteforce(n, down):
    """The same thing by FILTERING all n! permutations. Deliberately the slow, obviously
    correct route: it is the cross-check that keeps `transport_counts` from being believed
    on its own (`PREDICTIONS.md` E1/E5)."""
    cnt = [[0] * n for _ in range(n)]
    N = 0
    for p in permutations(range(n)):
        pos = [0] * n
        for a, x in enumerate(p):
            pos[x] = a
        if all(pos[x] < pos[y] for y in range(n) for x in range(n) if down[y] >> x & 1):
            N += 1
            for a, x in enumerate(p):
                cnt[x][a] += 1
    return cnt, N


# ------------------------------------------------------------- the scalars


def leak_prefix_numerators(n, cnt):
    """`N * leak(A_k)` for k = 1..n-1, as integers.

    `leak(A_k) = E|A_k \\ sigma(A_k)|` = the expected number of positions `a < k` whose
    occupant is an element `x >= k`. Read straight off the transport.
    """
    out = []
    for k in range(1, n):
        t = 0
        for x in range(k, n):
            for a in range(k):
                t += cnt[x][a]
        out.append(t)
    return out


def leak_prefix_from_extensions(n, down, k):
    """`leak(A_k)` from the DEFINITION over linear extensions, as an exact Fraction. Never
    used in the sweep; it exists so that the transport route can be falsified (E1)."""
    tot, N = 0, 0
    for p in permutations(range(n)):
        pos = [0] * n
        for a, x in enumerate(p):
            pos[x] = a
        if all(pos[x] < pos[y] for y in range(n) for x in range(n) if down[y] >> x & 1):
            N += 1
            img = {p[i] for i in range(k)}
            tot += k - len({i for i in range(k)} & img)
    return F(tot, N)


def M_exact(n, cnt, N):
    """M = sum_k leak(A_k) / sum_k min(k, n-k), exact."""
    num = sum(leak_prefix_numerators(n, cnt))
    den = sum(min(k, n - k) for k in range(1, n))
    return F(num, N * den)


def laplacian_exact(n, cnt, N):
    """L = I - S with S = (T + T^T)/2, exact rationals."""
    return [[(F(1) if i == j else F(0)) - F(cnt[i][j] + cnt[j][i], 2 * N)
             for j in range(n)] for i in range(n)]


def energy_exact(L, v):
    n = len(L)
    return sum(L[i][j] * v[i] * v[j] for i in range(n) for j in range(n))


# --------------------------------------------------------- the float screen


def gamma_float(n, cnt, N):
    """lambda_2 of L = I - S, in floats, by a Jacobi rotation sweep written here. Its ONLY
    job is to find candidates and to order the population; no verdict rests on it."""
    A = [[(1.0 if i == j else 0.0) - (cnt[i][j] + cnt[j][i]) / (2.0 * N)
          for j in range(n)] for i in range(n)]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(60):
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
    eigs = sorted((A[i][i], i) for i in range(n))
    lam, idx = eigs[1]                                   # eigs[0] is the constant vector, 0
    return lam, [V[k][idx] for k in range(n)]


# ------------------------------------------------------- exact certification


def certify_fail(L, t, vfloat, dens=(360360, 2520, 10**6, 10**8)):
    """EXACT certificate that `gamma < t`, hence that route (F) fails when `t = M^2/2`.

    `gamma = min_{v ⊥ 1} R(v)`, so ANY exhibited `v ⊥ 1` gives `gamma <= R(v)`. We
    rationalise the float eigenvector at a few denominators, re-centre it EXACTLY so that
    `v ⊥ 1` holds as a rational identity rather than approximately, and check
    `<v, L v>  <  t <v, v>` in `Fraction` arithmetic. No eigenvalue is computed and no float
    enters the decision. Returns the witness vector, or None if no rationalisation certifies.
    """
    n = len(L)
    for den in dens:
        v = [F(round(x * den), den) for x in vfloat]
        mean = sum(v) / n
        v = [x - mean for x in v]                        # v ⊥ 1 exactly
        nrm = sum(x * x for x in v)
        if nrm == 0:
            continue
        if energy_exact(L, v) < t * nrm:
            return v
    return None


def charpoly_shifted(A):
    """Coefficients of `det(xI + A)` for symmetric rational `A`, by Faddeev-LeVerrier on
    `-A` (so the roots are `-lambda`). Returns [1, c1, ..., cm]."""
    n = len(A)
    B = [[-A[i][j] for j in range(n)] for i in range(n)]  # det(xI + A) = det(xI - B)
    Mm = [[F(0)] * n for _ in range(n)]                   # M_0 = 0
    c = [F(1)]                                            # c_0 = 1
    for k in range(1, n + 1):
        # M_k = B M_{k-1} + c_{k-1} I
        Mm = [[sum(B[i][l] * Mm[l][j] for l in range(n)) + (c[-1] if i == j else F(0))
               for j in range(n)] for i in range(n)]
        tr = sum(sum(B[i][l] * Mm[l][i] for l in range(n)) for i in range(n))
        c.append(-tr / k)
    return c


def is_psd_exact(A):
    """A symmetric rational `A` is PSD iff every coefficient of `det(xI + A)` is >= 0: those
    coefficients are the sums of principal minors of each order, and a monic polynomial with
    non-negative coefficients has no positive real root, so `A` has no negative eigenvalue.
    Exact, and it computes no eigenvalue."""
    return all(x >= 0 for x in charpoly_shifted(A))


def certify_hold(L, t):
    """EXACT certificate that `gamma >= t`, i.e. that route (F) HOLDS (`f* <= 1` at
    `t = M^2/2`). On `1^perp` the operator `L - t(I - J/n)` acts as `L - tI`, and `1` is in
    both kernels, so PSD of the whole matrix is exactly `lambda_2(L) >= t`."""
    n = len(L)
    A = [[L[i][j] - t * ((F(1) if i == j else F(0)) - F(1, n)) for j in range(n)]
         for i in range(n)]
    return is_psd_exact(A)
