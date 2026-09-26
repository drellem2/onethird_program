"""mg-0b78 (KSBFT-P1): exact poset toolkit used as an INSTRUMENT only.

Posets are (n, lt) with lt[i][j] = True iff i < j (strict, transitively closed).
Everything is exact (fractions.Fraction); linear extensions are counted by a DP over
down-sets (bitmask ideals), so pair probabilities are exact at the sizes used here.
"""
from fractions import Fraction as Fr
from functools import lru_cache


def closure(n, rel):
    lt = [[False] * n for _ in range(n)]
    for i, j in rel:
        lt[i][j] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]:
                        lt[i][j] = True
    for i in range(n):
        assert not lt[i][i], "relation has a cycle"
    return lt


def inc(n, lt, x):
    return [y for y in range(n) if y != x and not lt[x][y] and not lt[y][x]]


def rng(n, lt):
    """range pi(P) = max_x #incomparables of x"""
    return max((len(inc(n, lt, x)) for x in range(n)), default=0)


def width(n, lt):
    """max antichain via Dilworth / bipartite matching: w = n - max matching"""
    match = [-1] * n

    def aug(u, seen):
        for v in range(n):
            if lt[u][v] and not seen[v]:
                seen[v] = True
                if match[v] < 0 or aug(match[v], seen):
                    match[v] = u
                    return True
        return False
    m = sum(1 for u in range(n) if aug(u, [False] * n))
    return n - m


def down_masks(n, lt):
    return [sum(1 << y for y in range(n) if lt[y][x]) for x in range(n)]


def count_les(n, lt):
    dm = down_masks(n, lt)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def f(I):
        if I == full:
            return 1
        return sum(f(I | (1 << x)) for x in range(n)
                   if not (I >> x) & 1 and (dm[x] & I) == dm[x])
    return f(0)


def pair_prob(n, lt, x, y):
    """exact P[x before y] for a uniform linear extension"""
    dm = down_masks(n, lt)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def f(I):  # number of completions from ideal I in which x comes before y
        if (I >> x) & 1:
            # x placed; if y not placed yet then all completions count
            if not (I >> y) & 1:
                return g(I)
            return 0  # unreachable by construction
        if (I >> y) & 1:
            return 0
        return sum(f(I | (1 << z)) for z in range(n)
                   if not (I >> z) & 1 and (dm[z] & I) == dm[z])

    @lru_cache(maxsize=None)
    def g(I):
        if I == full:
            return 1
        return sum(g(I | (1 << z)) for z in range(n)
                   if not (I >> z) & 1 and (dm[z] & I) == dm[z])
    return Fr(f(0), g(0))


def delta(n, lt):
    """delta(P) = max over incomparable pairs of min(p, 1-p); None for a chain"""
    best = None
    for x in range(n):
        for y in range(x + 1, n):
            if not lt[x][y] and not lt[y][x]:
                p = pair_prob(n, lt, x, y)
                v = min(p, 1 - p)
                best = v if best is None or v > best else best
    return best


def disjoint_union(*ps):
    n = sum(p[0] for p in ps)
    lt = [[False] * n for _ in range(n)]
    off = 0
    for m, l in ps:
        for i in range(m):
            for j in range(m):
                lt[off + i][off + j] = l[i][j]
        off += m
    return n, lt


def ordinal_sum(*ps):
    n = sum(p[0] for p in ps)
    lt = [[False] * n for _ in range(n)]
    off = 0
    offs = []
    for m, l in ps:
        offs.append((off, m))
        for i in range(m):
            for j in range(m):
                lt[off + i][off + j] = l[i][j]
        off += m
    for a, (oa, ma) in enumerate(offs):
        for b, (ob, mb) in enumerate(offs):
            if a < b:
                for i in range(ma):
                    for j in range(mb):
                        lt[oa + i][ob + j] = True
    return n, lt


def chain(m):
    return m, closure(m, [(i, i + 1) for i in range(m - 1)])


def antichain(m):
    return m, [[False] * m for _ in range(m)]
