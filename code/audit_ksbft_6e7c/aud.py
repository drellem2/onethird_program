"""aud.py (audit mg-6e7c of mg-ce69): independent exact helpers.  Shares no code with
code/ksbft_q2_both_ends_ce69/.  Poset format "n m_0 .. m_{n-1}" (hex strict down-masks, any labelling).

Two independent probability engines:
  probs(dn)     -- forward/backward ideal counts; #(a before b) = sum over ideals I with a in I, b minimal
                   outside I of fwd(I) * bwd(I + b)   (b is placed right after the prefix I).
  prob_aug(dn,a,b) -- e(P + {a<b}) / e(P): add the relation, re-close, count by a plain memoised recursion.
  brute(dn)     -- explicit enumeration of linear extensions (small posets only).
"""
from fractions import Fraction
from functools import lru_cache
import itertools

T1, T2 = Fraction(1, 3), Fraction(2, 3)


def parse(s):
    a = s.split()
    n = int(a[0])
    return close([int(t, 16) for t in a[1:1 + n]])


def close(dn):
    n = len(dn)
    dn = list(dn)
    for k in range(n):           # Warshall on bitmasks
        for i in range(n):
            if dn[i] >> k & 1:
                dn[i] |= dn[k]
    assert all(not dn[i] >> i & 1 for i in range(n)), "cycle"
    return dn


def ups(dn):
    n = len(dn)
    u = [0] * n
    for i in range(n):
        for j in range(n):
            if dn[i] >> j & 1:
                u[j] |= 1 << i
    return u


def incp(dn, up, a, b):
    return a != b and not (dn[a] >> b & 1) and not (up[a] >> b & 1)


def rangeD(dn):
    up = ups(dn)
    n = len(dn)
    return max(sum(incp(dn, up, a, b) for b in range(n)) for a in range(n))


def conn(dn):
    """incomparability graph connected (= 'indecomposable' in the KSBFT docs)"""
    n = len(dn)
    up = ups(dn)
    seen = {0}
    st = [0]
    while st:
        v = st.pop()
        for w in range(n):
            if w not in seen and incp(dn, up, v, w):
                seen.add(w)
                st.append(w)
    return len(seen) == n


def count_ext(dn):
    n = len(dn)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def c(placed):
        if placed == full:
            return 1
        return sum(c(placed | 1 << x) for x in range(n)
                   if not placed >> x & 1 and dn[x] & ~placed == 0)
    return c(0)


def prob_aug(dn, a, b, e=None):
    d2 = list(dn)
    d2[b] |= 1 << a
    d2 = close(d2)
    return Fraction(count_ext(d2), e if e is not None else count_ext(dn))


def probs(dn):
    """returns e, Bc with Bc[a][b] = #extensions with a before b"""
    n = len(dn)
    full = (1 << n) - 1
    # all ideals reachable, forward counts
    fwd = {0: 1}
    layer = [0]
    order = []
    while layer:
        nxt = {}
        for I in layer:
            order.append(I)
            for x in range(n):
                if not I >> x & 1 and dn[x] & ~I == 0:
                    J = I | 1 << x
                    nxt[J] = nxt.get(J, 0) + fwd[I]
        for J, v in nxt.items():
            fwd[J] = v
        layer = list(nxt)
    bwd = {full: 1}
    for I in reversed(order):
        if I == full:
            continue
        bwd[I] = sum(bwd[I | 1 << x] for x in range(n) if not I >> x & 1 and dn[x] & ~I == 0)
    e = fwd[full]
    Bc = [[0] * n for _ in range(n)]
    for I in order:
        for b in range(n):
            if not I >> b & 1 and dn[b] & ~I == 0:
                w = fwd[I] * bwd[I | 1 << b]
                J = I
                while J:
                    a = (J & -J).bit_length() - 1
                    Bc[a][b] += w
                    J &= J - 1
    return e, Bc


def brute(dn):
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


def chainbot(dn, S):
    """chain bottom of the subposet S (list): repeatedly the unique minimal element"""
    rest = set(S)
    out = []
    while rest:
        mins = [v for v in rest if not any(dn[v] >> w & 1 for w in rest if w != v)]
        if len(mins) != 1:
            break
        out.append(mins[0])
        rest.remove(mins[0])
    return out, (len(rest) == 0)


def ladders(dn, up, P, dual=False):
    """nested ladders.  primal: x||b, down(x) <= down(b), W = Up[b] - Up[x] (closed up-sets).
    Returns (x, b, chain, full, r) with r[i] = P[x<b_i]  (dual: P computed in the dual, i.e. P[b_i<x])."""
    n = len(dn)
    if dual:
        dn, up = up, dn
    out = []
    for x in range(n):
        for b in range(n):
            if not incp(dn, up, x, b) or dn[x] & ~dn[b]:
                continue
            W = [w for w in range(n) if (w == b or up[b] >> w & 1) and not (w == x or up[x] >> w & 1)]
            ch, full = chainbot(dn, W)
            assert ch[0] == b
            r = [P(c, x) if dual else P(x, c) for c in ch]
            out.append((x, b, ch, full, r))
    return out


def autcount(dn):
    """|Aut(P)| by backtracking on down/up masks"""
    n = len(dn)
    up = ups(dn)
    deg = [(bin(dn[i]).count("1"), bin(up[i]).count("1")) for i in range(n)]
    cnt = 0
    img = [-1] * n
    used = 0

    def ok(i, j):
        for k in range(i):
            if (dn[i] >> k & 1) != (dn[j] >> img[k] & 1) or (up[i] >> k & 1) != (up[j] >> img[k] & 1):
                return False
        return True

    def rec(i, used):
        nonlocal cnt
        if i == n:
            cnt += 1
            return
        for j in range(n):
            if not used >> j & 1 and deg[j] == deg[i] and ok(i, j):
                img[i] = j
                rec(i + 1, used | 1 << j)
        img[i] = -1
    rec(0, 0)
    return cnt
