"""iolib.py (mg-afa4): interval orders as canonical interval multisets, exact pair laws.

An interval order is given by its CANONICAL representation (Fishburn): intervals [l,r],
1<=l<=r<=h, every point 1..h is the left end of some interval and the right end of some
interval; x<y iff r(x)<l(y).  The multiset of canonical intervals is a complete isomorphism
invariant, so enumerating such multisets enumerates unlabelled interval orders exactly once.
Control: counts must be OEIS A022493 (1,2,5,15,53,217,1014,5335,31240,201608).
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from functools import lru_cache

A022493 = [1, 1, 2, 5, 15, 53, 217, 1014, 5335, 31240, 201608]

def gen(n):
    """yield canonical interval lists (sorted by (l,r)) of all unlabelled interval orders on n points."""
    for h in range(1, n + 1):
        ivs = [(l, r) for l in range(1, h + 1) for r in range(l, h + 1)]
        for ms in combinations_with_replacement(ivs, n):
            if {l for l, _ in ms} == set(range(1, h + 1)) and {r for _, r in ms} == set(range(1, h + 1)):
                yield list(ms)

def canon(iv):
    """canonical representation of an arbitrary interval list (x<y iff r(x)<l(y))."""
    n = len(iv)
    dn = [frozenset(j for j in range(n) if iv[j][1] < iv[i][0]) for i in range(n)]
    up = [frozenset(j for j in range(n) if iv[i][1] < iv[j][0]) for i in range(n)]
    D = sorted(set(dn), key=len); U = sorted(set(up), key=lambda s: -len(s))
    return sorted((D.index(dn[i]) + 1, U.index(up[i]) + 1) for i in range(n))

def downmasks(iv):
    n = len(iv)
    return [sum(1 << j for j in range(n) if iv[j][1] < iv[i][0]) for i in range(n)]

def laws(dn):
    """exact e(P) and N[x][y] = #extensions with x before y, via the ideal lattice."""
    n = len(dn); full = (1 << n) - 1
    @lru_cache(None)
    def g(I):          # completions from ideal I
        if I == full: return 1
        return sum(g(I | 1 << v) for v in range(n) if not I >> v & 1 and dn[v] & ~I == 0)
    f = {0: 1}; layer = [0]; ideals = [0]
    while layer:       # f(I) = ways to build I
        nxt = {}
        for I in layer:
            for v in range(n):
                if not I >> v & 1 and dn[v] & ~I == 0:
                    J = I | 1 << v; nxt[J] = nxt.get(J, 0) + f[I]
        f.update(nxt); layer = list(nxt); ideals += layer
    e = g(0)
    N = [[0] * n for _ in range(n)]
    for I in ideals:
        for v in range(n):
            if not I >> v & 1 and dn[v] & ~I == 0:
                w = f[I] * g(I | 1 << v)
                rest = full & ~I & ~(1 << v)
                for y in range(n):
                    if rest >> y & 1: N[v][y] += w
    g.cache_clear()
    return e, N

def lt(iv, a, b): return iv[a][1] < iv[b][0]
def inc(iv, a, b): return a != b and not lt(iv, a, b) and not lt(iv, b, a)

def prob(iv):
    dn = downmasks(iv); e, N = laws(dn); n = len(iv)
    return {(a, b): F(N[a][b], e) for a in range(n) for b in range(n) if inc(iv, a, b)}, e

def bal(p): return F(1, 3) <= p <= F(2, 3)

def delta(P):
    return max((min(p, 1 - p) for p in P.values()), default=None)

def decomposable(iv):
    """ordinal-decomposable iff some cut point: every interval ends before every other starts."""
    n = len(iv)
    for S in range(1, n):
        pass
    xs = sorted(range(n), key=lambda i: iv[i][1])
    # a prefix A (by right end) with all of A below all of B
    for k in range(1, n):
        A, B = xs[:k], xs[k:]
        if max(iv[a][1] for a in A) < min(iv[b][0] for b in B): return True
    return False

def gen_fast(n):
    """same output set as gen(n) (canonical multisets), with pruning: intervals chosen in (l,r)-sorted order,
    left endpoints must be used consecutively 1,2,..,h; right-endpoint coverage checked at the end."""
    def rec(pre, h, rem, lastl, lastr, rused):
        if rem == 0:
            if lastl == h and rused == (1 << (h + 1)) - 2: yield list(pre)
            return
        missing_r = bin(((1 << (h + 1)) - 2) & ~rused).count('1')
        if missing_r > rem + 0 or h - lastl > rem: return
        for l in (lastl, lastl + 1):
            if l < 1 or l > h: continue
            for r in range(l if l > lastl else max(l, lastr), h + 1):
                pre.append((l, r)); yield from rec(pre, h, rem - 1, l, r, rused | 1 << r); pre.pop()
    for h in range(1, n + 1):
        yield from rec([], h, n, 0, 0, 0)
