"""eng.py (audit mg-5ecf of mg-afa4): independent engine. Shares NO code with code/ksbft_t_interval_orders_afa4.

Posets are (n, up) with up[x] = bitmask of elements strictly above x.
- gen(n): canonical interval multisets, own DFS; completeness is certified by recanon() (each output is
  its own canonical form, so distinct outputs are non-isomorphic) plus the OEIS A022493 count.
- seps(): separators S(a,a') computed from the COVER relation directly (no interval formula).
- badL(): exists a linear extension in which every consecutive incomparable pair has |S| >= 2?
  (DP over (ideal, last element)); optional dominance-precedence constraint.
- laws(): exact N(x before y) for all pairs, forward/backward counts over the ideal lattice.
"""
from fractions import Fraction as F
from functools import lru_cache


def from_intervals(iv):
    n = len(iv)
    up = [0] * n
    for x in range(n):
        for y in range(n):
            if iv[x][1] < iv[y][0]:
                up[x] |= 1 << y
    return n, up


def from_down(dn):
    n = len(dn)
    up = [0] * n
    for y in range(n):
        for x in range(n):
            if dn[y] >> x & 1:
                up[x] |= 1 << y
    return n, up


def downs(P):
    n, up = P
    dn = [0] * n
    for x in range(n):
        for y in range(n):
            if up[x] >> y & 1:
                dn[y] |= 1 << x
    return dn


def lt(P, x, y):
    return P[1][x] >> y & 1


def inc(P, x, y):
    return x != y and not lt(P, x, y) and not lt(P, y, x)


def has_2p2(P):
    n, up = P
    for a in range(n):
        for b in range(n):
            if not lt(P, a, b):
                continue
            for c in range(n):
                for d in range(n):
                    if len({a, b, c, d}) == 4 and lt(P, c, d) and inc(P, a, c) and inc(P, a, d) \
                            and inc(P, b, c) and inc(P, b, d):
                        return True
    return False


def has_3p1(P):
    n, up = P
    for a in range(n):
        for b in range(n):
            if not lt(P, a, b):
                continue
            for c in range(n):
                if not lt(P, b, c):
                    continue
                for d in range(n):
                    if d not in (a, b, c) and inc(P, d, a) and inc(P, d, b) and inc(P, d, c):
                        return True
    return False


def recanon(P):
    """Fishburn canonical representation computed from the poset alone: l(x) = rank of D(x) among the
    distinct down-sets, r(x) = rank of the largest down-set not containing... (standard: r(x) = number of
    distinct down-sets D with x not in D). Returns sorted multiset, or None if not an interval order."""
    n, up = P
    dn = downs(P)
    ds = sorted(set(dn), key=lambda m: bin(m).count("1"))
    for i in range(len(ds) - 1):  # down-sets must form a chain
        if ds[i] & ~ds[i + 1]:
            return None
    idx = {m: i + 1 for i, m in enumerate(ds)}
    iv = []
    for x in range(n):
        l = idx[dn[x]]
        r = sum(1 for m in ds if not (m >> x & 1))
        iv.append((l, r))
    return tuple(sorted(iv))


def gen(n):
    """All canonical interval multisets with n intervals: endpoints in 1..h, every point is a left end
    and a right end of some interval."""
    out = []
    for h in range(1, n + 1):
        types = [(l, r) for l in range(1, h + 1) for r in range(l, h + 1)]
        T = len(types)
        full = (1 << h) - 1

        def rec(i, left, chosen, lmask, rmask):
            if left == 0:
                if lmask == full and rmask == full:
                    out.append(tuple(chosen))
                return
            if i == T:
                return
            l, r = types[i]
            if ((1 << (l - 1)) - 1) & ~lmask:      # a left point < l is uncovered and never will be
                return
            if bin(full & ~lmask).count("1") > left or bin(full & ~rmask).count("1") > left:
                return
            for k in range(left, 0, -1):
                rec(i + 1, left - k, chosen + [(l, r)] * k, lmask | 1 << (l - 1), rmask | 1 << (r - 1))
            rec(i + 1, left, chosen, lmask, rmask)
        rec(0, n, [], 0, 0)
    return out


def covers(P):
    n, up = P
    cov = [0] * n  # cov[x] = mask of upper covers of x
    for x in range(n):
        m = up[x]
        c = m
        for y in range(n):
            if m >> y & 1:
                c &= ~up[y]
        cov[x] = c
    return cov


def seps(P, cov=None):
    """S[a][b] for a || b: {z : a <. z, z || b} u {z : z <. b, z || a}, as a count."""
    n, up = P
    if cov is None:
        cov = covers(P)
    S = [[None] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if inc(P, a, b):
                s = set()
                for z in range(n):
                    if cov[a] >> z & 1 and inc(P, z, b):
                        s.add(z)
                    if cov[z] >> b & 1 and inc(P, z, a):
                        s.add(z)
                S[a][b] = len(s)
    return S


def dominance_pred(P):
    """pred[y] = mask of x that must precede y: x || y, D(x) <= D(y), U(x) >= U(y), not both equal."""
    n, up = P
    dn = downs(P)
    pred = [0] * n
    for x in range(n):
        for y in range(n):
            if inc(P, x, y) and dn[x] & ~dn[y] == 0 and up[y] & ~up[x] == 0 and (dn[x], up[x]) != (dn[y], up[y]):
                pred[y] |= 1 << x
    return pred


def badL(P, S=None, dominance=False, want=False):
    n, up = P
    dn = downs(P)
    if S is None:
        S = seps(P)
    pred = dominance_pred(P) if dominance else [0] * n
    need = [dn[x] | pred[x] for x in range(n)]
    full = (1 << n) - 1
    # frontier: dict ideal -> set of last elements (with parent for reconstruction)
    layer = {}
    for x in range(n):
        if need[x] == 0:
            layer.setdefault(1 << x, {})[x] = None
    back = [layer]
    for _ in range(n - 1):
        nxt = {}
        for I, lasts in layer.items():
            for x in range(n):
                if I >> x & 1 or need[x] & ~I:
                    continue
                J = I | 1 << x
                for a in lasts:
                    if lt(P, a, x) or S[a][x] >= 2:
                        nxt.setdefault(J, {})[x] = (I, a)
                        if not want:
                            break
        layer = nxt
        back.append(layer)
    if full not in layer:
        return None
    if not want:
        return True
    # reconstruct
    x = next(iter(layer[full]))
    I = full
    seq = []
    for k in range(n - 1, -1, -1):
        seq.append(x)
        par = back[k][I][x]
        if par is None:
            break
        I, x = par
    return seq[::-1]


def laws(P):
    """(e, N) with N[x][y] = number of linear extensions with x before y."""
    n, up = P
    dn = downs(P)
    full = (1 << n) - 1
    f = {0: 1}
    order = [0]
    frontier = [0]
    seen = {0}
    while frontier:
        new = []
        for I in frontier:
            for x in range(n):
                if not I >> x & 1 and dn[x] & ~I == 0:
                    J = I | 1 << x
                    if J not in seen:
                        seen.add(J)
                        new.append(J)
                        order.append(J)
        frontier = new
    # forward counts in order of size (order is BFS by size)
    f = {I: 0 for I in order}
    f[0] = 1
    for I in order:
        for x in range(n):
            if not I >> x & 1 and dn[x] & ~I == 0:
                f[I | 1 << x] += f[I]
    g = {I: 0 for I in order}
    g[full] = 1
    for I in reversed(order):
        if I == full:
            continue
        s = 0
        for x in range(n):
            if not I >> x & 1 and dn[x] & ~I == 0:
                s += g[I | 1 << x]
        g[I] = s
    e = f[full]
    N = [[0] * n for _ in range(n)]
    for I in order:
        if I == full:
            continue
        for x in range(n):
            if not I >> x & 1 and dn[x] & ~I == 0:
                w = f[I] * g[I | 1 << x]
                rest = full & ~(I | 1 << x)
                row = N[x]
                for y in range(n):
                    if rest >> y & 1:
                        row[y] += w
    return e, N


def delta(P, LN=None):
    n, up = P
    e, N = LN or laws(P)
    best = F(0)
    for x in range(n):
        for y in range(x + 1, n):
            if inc(P, x, y):
                p = F(N[x][y], e)
                best = max(best, min(p, 1 - p))
    return best


def twin_free(P):
    n, up = P
    dn = downs(P)
    keys = [(dn[x], up[x]) for x in range(n)]
    return len(set(keys)) == n


def ordinal_indecomposable(P):
    """No proper nonempty down-set D with every element of D below every element outside."""
    n, up = P
    dn = downs(P)
    full = (1 << n) - 1
    for mask in range(1, full):
        comp = full & ~mask
        if all(up[x] & comp == comp for x in range(n) if mask >> x & 1):
            return False
    return True


def modules_prime(P):
    """True iff P has no nontrivial module (2 <= |M| < n)."""
    n, up = P
    dn = downs(P)
    full = (1 << n) - 1
    for a in range(n):
        for b in range(a + 1, n):
            M = (1 << a) | (1 << b)
            changed = True
            while changed:
                changed = False
                for v in range(n):
                    if M >> v & 1:
                        continue
                    rel = set()
                    for m in range(n):
                        if M >> m & 1:
                            rel.add((up[v] >> m & 1, dn[v] >> m & 1))
                    if len(rel) > 1:
                        M |= 1 << v
                        changed = True
            if M != full:
                return False
    return True
