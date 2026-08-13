"""mg-8748 — WHICH CONVEX COMBINATIONS OF COMPRESSIONS ARE CANONICAL.  Shared machinery.

This library is written INDEPENDENTLY of `lib0fc6.py` and `lib8d66.py`.  That is not tidiness:
the fact this ticket is keeping alive was measured once, at one poset, by one implementation
(`mg-0fc6` `a4.3b` — the `n = 4` antichain, 3 levels, 5 random `f`).  A second implementation
agreeing with the first is evidence; a second script importing the first is a restatement.
`c0` cross-checks `linear_extensions` against `lib0fc6` at every labelled poset `n <= 5`.

THE OBJECTS.  A **compression** here is a conditional expectation `E[· | C]` for a partition `C`
of a finite probability space — equivalently the orthogonal projection onto the functions
constant on each block.  Everything below is exact: `Fraction` throughout, no float anywhere on a
verdict path.

THE TWO ROUTES TO NESTEDNESS, and the whole claim that the criterion is CHEAP:

    cheap      `refines(C_a, C_b)` — every block of `C_b` is inside a block of `C_a`.  O(N).
    expensive  `Pi_a Pi_b = Pi_b Pi_a = Pi_a` — matrix identity.  O(N^3) in exact rationals.

`c0` measures that they agree.  If they ever disagree, the cheap claim is gone and the entry in
`docs/FACTS.md` has to say so — that condition was filed in `PREDICTIONS.md` before this file
was written.
"""

from fractions import Fraction
from itertools import combinations, permutations

# ================================================================= posets, independently

def tclose(n, pairs):
    """Transitive closure of `pairs` as a strict-less-than matrix."""
    lt = [[False] * n for _ in range(n)]
    for (i, j) in pairs:
        lt[i][j] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]:
                        lt[i][j] = True
    return tuple(tuple(r) for r in lt)


def is_poset(lt):
    n = len(lt)
    for i in range(n):
        if lt[i][i]:
            return False
        for j in range(n):
            if lt[i][j] and lt[j][i]:
                return False
            if lt[i][j]:
                for k in range(n):
                    if lt[j][k] and not lt[i][k]:
                        return False
    return True


def all_posets(n):
    """Every LABELLED poset on `{0..n-1}`, by closing every antisymmetric relation.

    Independent of `lib0fc6.all_posets`: that one enumerates over upper-triangular choices under
    a relabelling; this one enumerates over all `2^(n(n-1)/2)` orientations of the pairs, closes,
    and dedups.  Same set, different route.
    """
    pairs = list(combinations(range(n), 2))
    seen = set()
    out = []
    for mask in range(3 ** len(pairs)):
        rel = []
        m = mask
        for (i, j) in pairs:
            d = m % 3
            m //= 3
            if d == 1:
                rel.append((i, j))
            elif d == 2:
                rel.append((j, i))
        lt = tclose(n, rel)
        if lt in seen or not is_poset(lt):
            continue
        # the closure of an orientation may add pairs; keep only relations whose closure is
        # itself, which is automatic here, and dedup
        seen.add(lt)
        out.append(lt)
    return out


def posets_upto_iso(n):
    """One representative of EVERY isomorphism class, by orienting each pair `i < j` upward.

    Every finite poset admits a topological labelling, so every isomorphism class has a
    representative here; the enumeration is `2^C(n,2)` masks rather than `3^C(n,2)`, which is
    what makes `n = 6` reachable.  Representatives are NOT unique — the same class can appear
    under several labellings — so counts from this function are counts of LABELLINGS unless
    deduplicated, and no row in this instrument counts them.
    """
    pairs = list(combinations(range(n), 2))
    seen = set()
    out = []
    for mask in range(1 << len(pairs)):
        rel = [p for k, p in enumerate(pairs) if mask >> k & 1]
        lt = tclose(n, rel)
        if lt in seen:
            continue
        seen.add(lt)
        out.append(lt)
    return out


def chain(n):
    return tclose(n, [(i, i + 1) for i in range(n - 1)])


def antichain(n):
    return tclose(n, [])


def linear_extensions(n, lt):
    """Every linear extension, as a tuple of element tuples, in lexicographic order."""
    out = []
    order = []
    used = [False] * n

    def rec():
        if len(order) == n:
            out.append(tuple(order))
            return
        for x in range(n):
            if used[x]:
                continue
            if any(lt[y][x] and not used[y] for y in range(n)):
                continue
            used[x] = True
            order.append(x)
            rec()
            order.pop()
            used[x] = False

    rec()
    return out


def bk_edges(Lx, n, lt):
    """Positions `p` at which swapping `Lx[p], Lx[p+1]` stays a linear extension."""
    return [p for p in range(n - 1) if not lt[Lx[p]][Lx[p + 1]]]


def swap(Lx, p):
    t = list(Lx)
    t[p], t[p + 1] = t[p + 1], t[p]
    return tuple(t)


def pair_probs(LEs, n):
    """`p_xy = Pr[x before y]` over the uniform measure on `LEs`, exact."""
    N = len(LEs)
    out = {}
    for (i, j) in combinations(range(n), 2):
        c = sum(1 for Lx in LEs if Lx.index(i) < Lx.index(j))
        out[(i, j)] = Fraction(c, N)
    return out


def pair_probs_measure(mu, n):
    """The same, for a general measure `mu: order -> weight`."""
    out = {}
    for (i, j) in combinations(range(n), 2):
        s = Fraction(0)
        for Lx, w in mu.items():
            if Lx.index(i) < Lx.index(j):
                s += w
        out[(i, j)] = s
    return out


# ================================================================= partitions and refinement

def partition_of(LEs, key):
    """The partition of `LEs` induced by a key function, as a tuple of block ids."""
    seen = {}
    out = []
    for Lx in LEs:
        k = key(Lx)
        if k not in seen:
            seen[k] = len(seen)
        out.append(seen[k])
    return tuple(out)


def refines(coarse, fine):
    """True iff `fine` refines `coarse` — every block of `fine` sits inside one of `coarse`.

    THE CHEAP ROUTE.  One pass, no matrix.  A family is a FILTRATION iff this holds along it.
    """
    seen = {}
    for c, f in zip(coarse, fine):
        if f in seen:
            if seen[f] != c:
                return False
        else:
            seen[f] = c
    return True


def is_filtration(parts):
    """True iff `parts` is nested coarsest-first: `parts[k+1]` refines `parts[k]`, every k."""
    return all(refines(parts[k], parts[k + 1]) for k in range(len(parts) - 1))


def nestedness(a, b):
    """Classify an unordered pair of partitions.  The CRITERION, in one call.

    Returns one of:
        'equal'       same sigma-algebra
        'a<b'         `b` refines `a`  (Ran Pi_a subset Ran Pi_b) — NESTED
        'b<a'         `a` refines `b`                              — NESTED
        'transverse'  neither refines the other                    — NOT NESTED
    """
    ab = refines(a, b)
    ba = refines(b, a)
    if ab and ba:
        return "equal"
    if ab:
        return "a<b"
    if ba:
        return "b<a"
    return "transverse"


# ================================================================= exact linear algebra

def cond_exp_matrix(part):
    """The conditional-expectation matrix of a partition, exact rationals.

    `(Pi f)(i) = mean of f over i's block`.  Symmetric (blocks are uniform) and idempotent.
    """
    N = len(part)
    blocks = {}
    for i, b in enumerate(part):
        blocks.setdefault(b, []).append(i)
    M = [[Fraction(0)] * N for _ in range(N)]
    for _b, idx in blocks.items():
        w = Fraction(1, len(idx))
        for i in idx:
            for j in idx:
                M[i][j] = w
    return M


def identity(N):
    return [[Fraction(1) if i == j else Fraction(0) for j in range(N)] for i in range(N)]


def matmul(A, B):
    N = len(A)
    K = len(B)
    Bt = list(zip(*B))
    return [[sum(A[i][k] * Bt[j][k] for k in range(K)) for j in range(len(B[0]))]
            for i in range(N)]


def lincomb(Ms, cs):
    N = len(Ms[0])
    return [[sum(c * M[i][j] for M, c in zip(Ms, cs)) for j in range(N)] for i in range(N)]


def mateq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A[0])))


def is_symmetric(A):
    return all(A[i][j] == A[j][i] for i in range(len(A)) for j in range(len(A)))


def is_projection(A):
    """Exact: symmetric and idempotent."""
    return is_symmetric(A) and mateq(matmul(A, A), A)


def apply_mat(A, f):
    return [sum(A[i][j] * f[j] for j in range(len(f))) for i in range(len(A))]


def mean(f):
    return sum(f) / len(f)


def var(f):
    m = mean(f)
    return sum((x - m) ** 2 for x in f) / len(f)


def norm2(f):
    """`‖f‖²` in the UNIFORM inner product `⟨f,g⟩ = (1/N) Σ f g` — the one `Var` lives in."""
    return sum(x * x for x in f) / len(f)


def quad(A, f):
    """`⟨f, A f⟩` in the same uniform inner product."""
    return sum(f[i] * v for i, v in enumerate(apply_mat(A, f))) / len(f)


# ================================================================= compression2's scales

def dyadic_nodes(n):
    """Internal nodes `(lo, mid, hi)` of the balanced binary tree over positions `[0,n)`."""
    out = []

    def rec(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        out.append((lo, mid, hi))
        rec(lo, mid)
        rec(mid, hi)

    rec(0, n)
    return out


def merge_word(Lx, star_rank, node):
    """The A/C merge word at one node — which half of `L*`'s block each element came from."""
    lo, mid, hi = node
    w = []
    for x in Lx:
        r = star_rank[x]
        if lo <= r < hi:
            w.append("A" if r < mid else "C")
    return "".join(w)


def scale_levels(n):
    """Nodes grouped by SCALE — block size `hi - lo` — coarsest (the root) first."""
    lv = {}
    for nd in dyadic_nodes(n):
        lv.setdefault(nd[2] - nd[0], []).append(nd)
    return [lv[s] for s in sorted(lv, reverse=True)]


def scale_filtration(LEs, star, n):
    """`compression2`'s scale family as PARTITIONS, coarsest first.

    `parts[k]` = conditioning on the merge words of the `k` coarsest scales.  `parts[0]` is the
    trivial partition (one block: nothing recorded) and the finest is the point partition, which
    is the operator form of the note's losslessness claim.
    """
    star_rank = [0] * n
    for i, x in enumerate(star):
        star_rank[x] = i
    levels = scale_levels(n)
    parts = []
    for k in range(len(levels) + 1):
        keep = [nd for lv in levels[:k] for nd in lv]
        parts.append(partition_of(LEs, lambda Lx, keep=keep: tuple(
            merge_word(Lx, star_rank, nd) for nd in keep)))
    return parts


# ================================================================= compression.tex's pair

def parity_foliation(LEs, n, lt, parity):
    """`C_o` / `C_e`: the fibers of freezing everything except the free 2-blocks at positions
    of the given parity.  Two extensions are in the same fiber iff they agree away from the
    swaps at those positions.  `parity = 0` is `C_o` (positions 0, 2, 4, ... 0-indexed).
    """
    def key(Lx):
        t = list(Lx)
        # canonicalise every free block at a position of this parity by sorting the two entries
        for p in range(parity, n - 1, 2):
            if not lt[t[p]][t[p + 1]] and not lt[t[p + 1]][t[p]]:
                if t[p] > t[p + 1]:
                    t[p], t[p + 1] = t[p + 1], t[p]
        return tuple(t)

    return partition_of(LEs, key)


# ================================================================= reporting

FAILURES = []


def banner(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def verdict(ok, label, extra=""):
    tag = "GREEN" if ok else "RED  "
    print(f"  [{tag}] {label}" + (f"   {extra}" if extra else ""))
    if not ok:
        FAILURES.append(label)
    return ok


def note(*lines):
    print()
    for ln in lines:
        print("       " + ln)


def finish():
    print()
    if FAILURES:
        print(f"RESULT: RED — {len(FAILURES)} check(s) failed:")
        for f in FAILURES:
            print(f"   - {f}")
        return 1
    print("RESULT: GREEN — all checks passed")
    return 0
