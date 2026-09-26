"""lib.py (mg-ce69): shared exact helpers for docs/KSBFT-Q2-both-ends.md.

Poset format as in the other KSBFT instruments: "n m_0 .. m_{n-1}", m_i = strict down-set bitmask (hex).
Everything is exact (Python ints / Fractions).  `analyse` is an ideal DP written for this ticket; `extensions`
enumerates linear extensions explicitly and is used as the independent cross-check on small posets.
"""
from fractions import Fraction
from functools import lru_cache

THIRD, TWOTHIRD = Fraction(1, 3), Fraction(2, 3)


def parse(s):
    a = s.split()
    return [int(t, 16) for t in a[1:1 + int(a[0])]]


def fmt(dn):
    return " ".join([str(len(dn))] + [format(m, "x") for m in dn])


def closure(dn):
    """transitive closure of a list of (not necessarily closed) down-masks"""
    n = len(dn)
    dn = list(dn)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            m = dn[i]
            for j in range(n):
                if m >> j & 1:
                    m |= dn[j]
            if m != dn[i]:
                dn[i] = m
                changed = True
    for i in range(n):
        assert not dn[i] >> i & 1, "cycle"
    return dn


def upmasks(dn):
    n = len(dn)
    return [sum(1 << j for j in range(n) if dn[j] >> i & 1) for i in range(n)]


def inc(dn, up, a, b):
    return a != b and not dn[a] >> b & 1 and not up[a] >> b & 1


def rng(dn):
    up = upmasks(dn)
    n = len(dn)
    return max(sum(inc(dn, up, a, b) for b in range(n)) for a in range(n))


def width_ge3(dn):
    up = upmasks(dn)
    n = len(dn)
    return any(inc(dn, up, a, b) and inc(dn, up, a, c) and inc(dn, up, b, c)
               for a in range(n) for b in range(a + 1, n) for c in range(b + 1, n))


def restrict(dn, keep):
    """induced subposet on the sorted list `keep`; returns new down-masks (relabelled 0..)."""
    idx = {v: i for i, v in enumerate(keep)}
    return [sum(1 << idx[w] for w in keep if dn[v] >> w & 1) for v in keep], keep


def analyse(dn):
    """e(P); B[a][b] = #ext with a before b; pos[a][j] = #ext with exactly j elements before a."""
    n = len(dn)
    up = upmasks(dn)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def N(I):
        if I == 0:
            return 1
        return sum(N(I & ~(1 << x)) for x in range(n) if I >> x & 1 and not up[x] & I)

    @lru_cache(maxsize=None)
    def Nc(F):
        if F == 0:
            return 1
        return sum(Nc(F & ~(1 << x)) for x in range(n) if F >> x & 1 and not dn[x] & F)

    e = N(full)
    B = [[0] * n for _ in range(n)]
    pos = [[0] * n for _ in range(n)]
    seen = {full}
    stack = [full]
    while stack:
        J = stack.pop()
        k = bin(J).count("1")
        for x in range(n):
            if J >> x & 1 and not up[x] & J:
                I = J & ~(1 << x)
                c = N(I) * Nc(full & ~J)
                pos[x][k - 1] += c
                for w in range(n):
                    if I >> w & 1:
                        B[w][x] += c
                if I not in seen:
                    seen.add(I)
                    stack.append(I)
    return e, B, pos


def extensions(dn):
    n = len(dn)
    out = []

    def rec(placed, seq):
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for x in range(n):
            if not placed >> x & 1 and dn[x] & ~placed == 0:
                seq.append(x)
                rec(placed | 1 << x, seq)
                seq.pop()
    rec(0, [])
    return out


def balanced(p):
    return THIRD <= p <= TWOTHIRD


def connected(dn):
    n = len(dn)
    up = upmasks(dn)
    seen, stack = 1, [0]
    while stack:
        v = stack.pop()
        for w in range(n):
            if not seen >> w & 1 and inc(dn, up, v, w):
                seen |= 1 << w
                stack.append(w)
    return seen == (1 << n) - 1


def chain_bottom(dn, S):
    rest = set(S)
    out = []
    while rest:
        mins = [v for v in rest if not any(dn[v] >> u & 1 for u in rest)]
        if len(mins) != 1:
            break
        out.append(mins[0])
        rest.discard(mins[0])
    return out


def e_of(dn, keep):
    d, _ = restrict(dn, sorted(keep))
    return analyse(d)[0] if d else 1


def windows(dn):
    """bottom windows {x} u Inc(x) for minimal x, top windows dually"""
    n = len(dn)
    up = upmasks(dn)
    bot = [[x] + [y for y in range(n) if inc(dn, up, x, y)] for x in range(n) if dn[x] == 0]
    top = [[x] + [y for y in range(n) if inc(dn, up, x, y)] for x in range(n) if up[x] == 0]
    return bot, top


def bal_pairs(dn, e, B):
    n = len(dn)
    up = upmasks(dn)
    return [(a, b, Fraction(B[a][b], e)) for a in range(n) for b in range(a + 1, n)
            if inc(dn, up, a, b) and balanced(Fraction(B[a][b], e))]


def win_holds(dn, e, B, side):
    """WIN at one end: some balanced pair inside {x} u Inc(x) for an extreme x of that end"""
    bot, top = windows(dn)
    W = bot if side == "bot" else top
    bp = bal_pairs(dn, e, B)
    return any(a in w and b in w for w in W for a, b, _ in bp)
