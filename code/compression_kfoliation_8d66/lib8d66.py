"""lib8d66 -- W5's instrument for the k-FOLIATION question of mg-8d66.

THE OBJECT.  mg-409a priced `alpha = lam_min(2I - Pi_o - Pi_e)` on `1-perp` against a bar of
2..3 and found a ceiling of 1.  `pm-onethird` asks whether that ceiling is an artefact of
`k = 2`: partition the n-1 adjacent swap positions into k classes of PAIRWISE NON-ADJACENT
positions, one projection per class, and study `alpha_k = lam_min(kI - sum_i Pi_i)`.

INDEPENDENCE, STATED FIRST BECAUSE A READER MUST PRICE IT.  Everything on a verdict path in
this file is built here from scratch, and two constructions are built by a DIFFERENT ROUTE
from the two prior instruments on purpose:

  * linear extensions are enumerated by choosing the LAST element (maximal elements of the
    remaining set) where `lib409a` and `lib8bc7` both choose the first;
  * fibers are computed as ORBITS under the class's legal swaps (breadth-first), where both
    prior instruments compute them as level sets of a position-group content key.

`lib409a` and `lib8bc7` are imported by `k0_selftest` ONLY, as second and third
implementations to check this one against.  No verdict in `k1`..`k5` routes through them.

EXACTNESS.  Fractions on every verdict path.  `jacobi_eigenvalues` is the only float and it is
used for MEASUREMENT (arm `k5`, and agreement checks that are labelled as such) and never for
a verdict.  Every verdict here is a rational identity, an exact PSD test, or an exhibited
rational witness.

CONVENTION.  Swap positions are 0-indexed: position `p` in `0..n-2` exchanges the elements at
word positions `p` and `p+1`.  A CLASS is a set of pairwise non-adjacent swap positions; a
PARTITION (admissible partition) is a partition of `{0..n-2}` into classes.  `blocks_o`/
`blocks_e` of `lib409a` are exactly the classes `{0,2,4,...}` and `{1,3,5,...}` in this
convention -- the unique admissible partition with `k = 2` (see `k1`).
"""

from fractions import Fraction
from itertools import combinations, product

# ======================================================================================
# posets
# ======================================================================================


def tclose(n, pairs):
    """Transitive closure of a set of strict relations."""
    rel = set(pairs)
    again = True
    while again:
        again = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d))
                    again = True
    return frozenset(rel)


def is_poset(rel):
    for (a, b) in rel:
        if a == b or (b, a) in rel:
            return False
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c and (a, d) not in rel:
                return False
    return True


def all_posets(n):
    """Every labeled poset on 0..n-1."""
    prs = list(combinations(range(n), 2))
    for ch in product((0, 1, 2), repeat=len(prs)):
        rel = set()
        for (a, b), c in zip(prs, ch):
            if c == 1:
                rel.add((a, b))
            elif c == 2:
                rel.add((b, a))
        if is_poset(rel):
            yield frozenset(rel)


def sample_posets(n, k, seed):
    """k pseudo-random labeled posets on n elements, deterministic in `seed`.

    Own LCG constants, written out so a run reproduces without depending on a library RNG.
    """
    state = (seed * 2654435761 + 1) & 0xFFFFFFFF

    def rnd():
        nonlocal state
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        return state / 0x100000000

    seen, out, guard = set(), [], 0
    while len(out) < k and guard < 80 * k:
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
        rel = tclose(n, base)
        if rel in seen:
            continue
        seen.add(rel)
        out.append(rel)
    return out


def antichain(n):
    return frozenset()


def Z(n):
    """Z_n: ordinal sum of n/2 two-element antichains.  mg-409a's extremal object."""
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


# ======================================================================================
# linear extensions -- built BACKWARDS (choose the last element), deliberately not the
# route lib409a / lib8bc7 take
# ======================================================================================


def linear_extensions(n, lt):
    succs = [set() for _ in range(n)]
    for (i, j) in lt:
        succs[i].add(j)
    out, left, tail = [], set(range(n)), []

    def rec():
        if not left:
            out.append(tuple(tail[::-1]))
            return
        for v in sorted(left):
            if not (succs[v] & left):          # v is maximal in what remains
                left.discard(v)
                tail.append(v)
                rec()
                tail.pop()
                left.add(v)

    rec()
    return sorted(out)


def swap(L, p):
    M = list(L)
    M[p], M[p + 1] = M[p + 1], M[p]
    return tuple(M)


def legal(L, p, lt):
    a, b = L[p], L[p + 1]
    return (a, b) not in lt and (b, a) not in lt


# ======================================================================================
# admissible partitions of the swap positions {0..n-2}
# ======================================================================================


def is_class(S):
    """A class is a set of PAIRWISE NON-ADJACENT swap positions."""
    S = sorted(S)
    return all(S[i + 1] - S[i] >= 2 for i in range(len(S) - 1))


def admissible_partitions(n):
    """Every partition of {0..n-2} into classes of pairwise non-adjacent positions.

    Equivalently: every partition of the path P_{n-1} into independent sets, i.e. every
    proper colouring of P_{n-1} counted up to colour names.  Returned as a sorted list of
    sorted tuples-of-tuples, so the enumeration order is an observation not an accident.
    """
    m = n - 1

    def rec(i, blocks):
        if i == m:
            yield sorted(tuple(b) for b in blocks)
            return
        for b in blocks:
            if (i - 1) not in b:               # only the immediate predecessor can clash
                b.append(i)
                yield from rec(i + 1, blocks)
                b.pop()
        blocks.append([i])
        yield from rec(i + 1, blocks)
        blocks.pop()

    return sorted(tuple(p) for p in rec(0, []))


def finest_partition(n):
    return tuple((p,) for p in range(n - 1))


def coarsest_partition(n):
    """The unique k = 2 admissible partition: even positions, odd positions."""
    ev = tuple(p for p in range(n - 1) if p % 2 == 0)
    od = tuple(p for p in range(n - 1) if p % 2 == 1)
    return tuple(sorted(b for b in (ev, od) if b))


def refines(fine, coarse):
    """True iff every block of `fine` sits inside some block of `coarse`."""
    cs = [set(b) for b in coarse]
    return all(any(set(b) <= c for c in cs) for b in fine)


# ======================================================================================
# fibers as ORBITS (not as content keys) -- and the cube check
# ======================================================================================


def orbit_fibers(LEs, n, lt, S):
    """Partition of L(P) into orbits under the legal swaps at positions in class S.

    Returns (label_of_index, list_of_index_lists).  Breadth-first from each unvisited state.
    """
    idx = {L: i for i, L in enumerate(LEs)}
    lab = [-1] * len(LEs)
    blocks = []
    for start in range(len(LEs)):
        if lab[start] >= 0:
            continue
        b, queue = [], [start]
        lab[start] = len(blocks)
        while queue:
            u = queue.pop()
            b.append(u)
            for p in S:
                if legal(LEs[u], p, lt):
                    v = idx[swap(LEs[u], p)]
                    if lab[v] < 0:
                        lab[v] = len(blocks)
                        queue.append(v)
        blocks.append(sorted(b))
    return lab, blocks


def free_positions(L, lt, S):
    return [p for p in S if legal(L, p, lt)]


# ======================================================================================
# functions on L(P), exactly
# ======================================================================================


def mean(v):
    return sum(v) / Fraction(len(v))


def variance(v):
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / Fraction(len(v))


def e_cond_var(vals, LEs, n, lt, S):
    """E Var(f | C_S) = <f, (I - Pi_S) f>, exactly, over the ORBIT fibers of class S."""
    N = len(LEs)
    _, blocks = orbit_fibers(LEs, n, lt, S)
    tot = Fraction(0)
    for b in blocks:
        m = sum(vals[i] for i in b) / Fraction(len(b))
        tot += sum((vals[i] - m) ** 2 for i in b) / Fraction(N)
    return tot


def q_form(vals, LEs, n, lt, part):
    """<f, Q_part f> = sum over classes of E Var(f | C_i),  Q_part = kI - sum_i Pi_i."""
    return sum(e_cond_var(vals, LEs, n, lt, S) for S in part)


def bk_energy(vals, LEs, n, lt):
    """E_BK(f) = 1/(2(n-1)N) sum_L sum_p legal (f(tau_p L) - f(L))^2.

    lib409a's normalisation at its :266, which is the note's at compression.tex:106.
    """
    idx = {L: i for i, L in enumerate(LEs)}
    tot = Fraction(0)
    for L in LEs:
        fL = vals[idx[L]]
        for p in range(n - 1):
            if legal(L, p, lt):
                tot += (vals[idx[swap(L, p)]] - fL) ** 2
    return tot / Fraction(2 * (n - 1) * len(LEs))


def pair_indicator(LEs, x, y):
    """f_xy = 1{x before y}.  Theorem E's test function, and THE WITNESS OF THIS TICKET."""
    out = []
    for L in LEs:
        px, py = L.index(x), L.index(y)
        out.append(Fraction(1) if px < py else Fraction(0))
    return out


def pair_stats(LEs, n, lt, x, y):
    """(p, P_adjacent) for the incomparable pair (x, y), exactly.

    p = P(x before y);  P_adjacent = P(x and y occupy consecutive positions).
    """
    N = len(LEs)
    before = adj = 0
    for L in LEs:
        px, py = L.index(x), L.index(y)
        if px < py:
            before += 1
        if abs(px - py) == 1:
            adj += 1
    return Fraction(before, N), Fraction(adj, N)


# ======================================================================================
# matrices, exact
# ======================================================================================


def pi_matrix(LEs, n, lt, S):
    N = len(LEs)
    A = [[Fraction(0)] * N for _ in range(N)]
    _, blocks = orbit_fibers(LEs, n, lt, S)
    for b in blocks:
        w = Fraction(1, len(b))
        for i in b:
            for j in b:
                A[i][j] += w
    return A


def q_matrix(LEs, n, lt, part):
    """Q_part = k I - sum_i Pi_i, exact rationals."""
    N = len(LEs)
    A = [[Fraction(0)] * N for _ in range(N)]
    for i in range(N):
        A[i][i] = Fraction(len(part))
    for S in part:
        _, blocks = orbit_fibers(LEs, n, lt, S)
        for b in blocks:
            w = Fraction(1, len(b))
            for i in b:
                for j in b:
                    A[i][j] -= w
    return A


def bk_matrix(LEs, n, lt):
    """P_BK: pick p uniform in {0..n-2}, swap if legal.  Exact rationals."""
    idx = {L: i for i, L in enumerate(LEs)}
    N = len(LEs)
    A = [[Fraction(0)] * N for _ in range(N)]
    for i, L in enumerate(LEs):
        stay = n - 1
        for p in range(n - 1):
            if legal(L, p, lt):
                A[i][idx[swap(L, p)]] += Fraction(1, n - 1)
                stay -= 1
        A[i][i] += Fraction(stay, n - 1)
    return A


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]


def mat_scale(A, c):
    return [[c * A[i][j] for j in range(len(A))] for i in range(len(A))]


def identity(N):
    return [[Fraction(1) if i == j else Fraction(0) for j in range(N)] for i in range(N)]


def proj_perp_one(N):
    """I - P_1, the orthogonal projection onto 1-perp."""
    w = Fraction(1, N)
    return [[(Fraction(1) if i == j else Fraction(0)) - w for j in range(N)]
            for i in range(N)]


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))


def psd_exact(A):
    """EXACT: is the rational symmetric matrix A positive semidefinite?

    Symmetric Gaussian elimination.  A zero pivot forces its whole row to vanish (else A has
    a negative 2x2 minor); a negative pivot is an immediate refusal.  Returns (ok, why).
    """
    N = len(A)
    B = [row[:] for row in A]
    live = list(range(N))
    while live:
        i = live[0]
        piv = B[i][i]
        if piv < 0:
            return False, f"negative pivot at {i}: {piv}"
        if piv == 0:
            for j in live[1:]:
                if B[i][j] != 0:
                    return False, f"zero pivot at {i} with nonzero off-diagonal at {j}"
            live.pop(0)
            continue
        rest = live[1:]
        for a in rest:
            f = B[a][i] / piv
            if f == 0:
                continue
            for b in rest:
                B[a][b] -= f * B[i][b]
        live = rest
    return True, "psd"


def jacobi_eigenvalues(A, sweeps=200, tol=1e-13):
    """Symmetric Jacobi.  FLOAT -- measurement only, never a verdict."""
    import math
    N = len(A)
    B = [[float(A[i][j]) for j in range(N)] for i in range(N)]
    for _ in range(sweeps):
        off = sum(B[i][j] * B[i][j] for i in range(N) for j in range(i + 1, N))
        if off <= tol * tol:
            break
        for p in range(N):
            for q in range(p + 1, N):
                if abs(B[p][q]) < 1e-18:
                    continue
                th = (B[q][q] - B[p][p]) / (2.0 * B[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
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


def alpha_measured(LEs, n, lt, part):
    """lam_min of Q_part on 1-perp = SECOND smallest eigenvalue (Q is PSD, Q1 = 0).

    FLOAT.  Measurement only.
    """
    if len(LEs) < 2:
        return None
    return jacobi_eigenvalues(q_matrix(LEs, n, lt, part))[1]


def gap_bk_measured(LEs, n, lt):
    """1 - lam_2(P_BK).  FLOAT.  Measurement only."""
    if len(LEs) < 2:
        return None
    ev = jacobi_eigenvalues(bk_matrix(LEs, n, lt))
    return 1.0 - ev[-2]


# ======================================================================================
# reporting
# ======================================================================================


def banner(t):
    print()
    print("=" * 90)
    print(t)
    print("=" * 90)


def verdict(ok, label, extra=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + extra) if extra else ""))
    return ok


def frac(x, d=9):
    return f"{float(x):.{d}f}"


def pstr(part):
    return "|".join("".join(str(p) for p in b) for b in part)
