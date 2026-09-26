"""exact.py -- independent exact analysis of one finite poset (mg-2912).

Written separately from probe.cpp and sharing no code with it.  Two
independent counting methods:

  * brute(P)  -- enumerate every permutation, keep the linear extensions
                 (n <= 8).  No ideals, no DP: the reference for everything.
  * dp(P)     -- memoised recursion over order ideals, removing MAXIMAL
                 elements (probe.cpp adds minimal elements forward and
                 backward, so the traversal differs too).

A poset is given as `down`: down[i] = bitmask of the elements strictly below
i (transitively closed).  All outputs are Python ints / Fractions.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import sqrt

C_BFT_FLOAT = (5 - sqrt(5)) / 10


def up_of(down):
    n = len(down)
    return [sum(1 << j for j in range(n) if down[j] >> i & 1) for i in range(n)]


def incomparable(down, x, y):
    return x != y and not (down[x] >> y & 1) and not (down[y] >> x & 1)


def rng(down):
    n = len(down)
    return max((sum(incomparable(down, x, y) for y in range(n)) for x in range(n)), default=0)


def brute(down):
    """e, S[x] = sum over extensions of position(x) (1-based), B[x][y] = #(x before y)."""
    n = len(down)
    e = 0
    S = [0] * n
    B = [[0] * n for _ in range(n)]
    for perm in permutations(range(n)):
        pos = [0] * n
        for k, v in enumerate(perm):
            pos[v] = k + 1
        if all(pos[u] < pos[v] for v in range(n) for u in range(n) if down[v] >> u & 1):
            e += 1
            for x in range(n):
                S[x] += pos[x]
                for y in range(n):
                    if pos[x] < pos[y]:
                        B[x][y] += 1
    return e, S, B


def dp(down):
    n = len(down)
    up = up_of(down)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def N(I):
        # number of linear extensions of the subposet on ideal I
        if I == 0:
            return 1
        tot = 0
        for x in range(n):
            if I >> x & 1 and (up[x] & I) == 0:  # x maximal in I
                tot += N(I & ~(1 << x))
        return tot

    @lru_cache(maxsize=None)
    def Nc(F):
        # number of linear extensions of the filter F (complement of an ideal)
        if F == 0:
            return 1
        tot = 0
        for x in range(n):
            if F >> x & 1 and (down[x] & F) == 0:  # x minimal in F
                tot += Nc(F & ~(1 << x))
        return tot

    e = N(full)
    S = [0] * n
    B = [[0] * n for _ in range(n)]
    # enumerate ideals by DFS removing maximal elements from the full set
    seen = set()
    stack = [full]
    while stack:
        J = stack.pop()
        if J in seen:
            continue
        seen.add(J)
        for x in range(n):
            if J >> x & 1 and (up[x] & J) == 0:
                I = J & ~(1 << x)
                # x occupies position |J| in the extensions passing through I -> J
                c = N(I) * Nc(full & ~J)
                S[x] += bin(J).count("1") * c
                for w in range(n):
                    if I >> w & 1:
                        B[w][x] += c
                stack.append(I)
    return e, S, B


def analyse(down, method="dp"):
    n = len(down)
    e, S, B = (brute if method == "brute" else dp)(down)
    best = None
    pairs = []
    for x in range(n):
        for y in range(x + 1, n):
            if incomparable(down, x, y):
                b = min(B[x][y], B[y][x])
                if best is None or b > best:
                    best, pairs = b, [(x, y)]
                elif b == best:
                    pairs.append((x, y))
    ordr = sorted(range(n), key=lambda v: (S[v], v))
    d = [Fraction(S[v], e) - (i + 1) for i, v in enumerate(ordr)]
    M = max(abs(t) for t in d)
    return {
        "n": n,
        "pi": rng(down),
        "e": e,
        "delta": Fraction(best, e) if best is not None else None,
        "pairs": pairs,
        "h": [Fraction(s, e) for s in S],
        "ord": ordr,
        "d": d,
        "M": M,
        "B": B,
    }


def bal(res, down, x, y):
    if not incomparable(down, x, y):
        return Fraction(0)
    B, e = res["B"], res["e"]
    return Fraction(min(B[x][y], B[y][x]), e)


def delta_minus_cbft_gt(q, c=Fraction(0)):
    """Exact test  q > C_BFT + c  with C_BFT = (5 - sqrt5)/10 irrational.

    q - c > (5 - sqrt5)/10  <=>  sqrt5 > 5 - 10(q - c) =: t.
    If t < 0 it holds; otherwise compare 5 > t^2.
    """
    t = 5 - 10 * (Fraction(q) - Fraction(c))
    return t < 0 or t * t < 5


def dp_first(down, v):
    """number of linear extensions in which v is the first element"""
    n = len(down)
    if down[v]:
        return 0
    rest = [i for i in range(n) if i != v]
    idx = {u: k for k, u in enumerate(rest)}
    sub = [sum(1 << idx[u] for u in rest if down[w] >> u & 1) for w in rest]
    return dp(sub)[0] if sub else 1
