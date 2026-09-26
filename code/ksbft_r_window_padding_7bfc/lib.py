"""mg-7bfc (KSBFT-R): exact poset toolkit, used as an INSTRUMENT only.

A poset is (n, lt) with lt[i][j] True iff i < j (strict, transitively closed).
All counts are exact Python integers; probabilities are fractions.Fraction.

One pass over the down-set lattice gives everything:
  F(I) = number of ways to build ideal I from the empty set (linear extensions of I),
  G(I) = number of ways to complete I to the whole poset (extensions of P \\ I).
  #{sigma : x before y}  = sum over ideals I with x,y not in I and I+x an ideal of F(I) G(I+x),
  N_i(x) = #{sigma : sigma(x) = i} = sum over such I with |I| = i-1 of F(I) G(I+x).
"""
from fractions import Fraction as Fr


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


def ranges(n, lt):
    return [len(inc(n, lt, x)) for x in range(n)]


def rng(n, lt):
    return max(ranges(n, lt), default=0)


def indecomposable(n, lt):
    """incomparability graph connected (= not an ordinal sum), n >= 2"""
    if n < 2:
        return False
    seen, stack = {0}, [0]
    while stack:
        x = stack.pop()
        for y in inc(n, lt, x):
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return len(seen) == n


class Exact:
    """exact linear-extension statistics of a poset by DP over its ideals"""

    def __init__(self, n, lt):
        self.n, self.lt = n, lt
        dm = [sum(1 << y for y in range(n) if lt[y][x]) for x in range(n)]
        self.dm = dm
        levels = [{0: 1}]
        for _ in range(n):
            nxt = {}
            for I, c in levels[-1].items():
                for x in range(n):
                    if not (I >> x) & 1 and (dm[x] & I) == dm[x]:
                        J = I | (1 << x)
                        nxt[J] = nxt.get(J, 0) + c
            levels.append(nxt)
        full = (1 << n) - 1
        G = {full: 1}
        for k in range(n - 1, -1, -1):
            for I in levels[k]:
                s = 0
                for x in range(n):
                    if not (I >> x) & 1 and (dm[x] & I) == dm[x]:
                        s += G[I | (1 << x)]
                G[I] = s
        self.levels, self.G = levels, G
        self.e = G[0]
        assert self.e == levels[n][full]

    def _addable(self, I, x):
        return not (I >> x) & 1 and (self.dm[x] & I) == self.dm[x]

    def before(self, x, y):
        """P[x before y]"""
        tot = 0
        for lev in self.levels:
            for I, c in lev.items():
                if (I >> y) & 1 == 0 and self._addable(I, x):
                    tot += c * self.G[I | (1 << x)]
        return Fr(tot, self.e)

    def slot_law(self, x):
        """N_1..N_n of x (list index i-1)"""
        N = [0] * self.n
        for k, lev in enumerate(self.levels[:-1]):
            for I, c in lev.items():
                if self._addable(I, x):
                    N[k] += c * self.G[I | (1 << x)]
        assert sum(N) == self.e
        return N

    def height(self, x):
        N = self.slot_law(x)
        return Fr(sum((i + 1) * v for i, v in enumerate(N)), self.e)

    def pairs(self):
        n, lt = self.n, self.lt
        out = {}
        for x in range(n):
            for y in range(x + 1, n):
                if not lt[x][y] and not lt[y][x]:
                    out[(x, y)] = self.before(x, y)
        return out

    def delta(self):
        ps = self.pairs()
        if not ps:
            return None
        return max(min(p, 1 - p) for p in ps.values())


def balanced(p):
    return Fr(1, 3) <= p <= Fr(2, 3)


# ---------------------------------------------------------------- constructions

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
    offs, off = [], 0
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


def fib(N):
    """Fibonacci poset F_N: x_i < x_j iff j - i >= 2 (0-indexed)"""
    return N, [[j - i >= 2 for j in range(N)] for i in range(N)]


def attach_low(W, R):
    """PAD_R: W plus one new element z with z || w_0..w_{R-1} and z < w_j for j >= R.
    Valid (transitively closed) when w_0..w_{R-1} is a down-set of W: then nothing is
    forced below z, and every w_j (j >= R) is above z. Returns (n, lt), z = index n-1."""
    n0, l0 = W
    n = n0 + 1
    lt = [[False] * n for _ in range(n)]
    for i in range(n0):
        for j in range(n0):
            lt[i][j] = l0[i][j]
    z = n0
    for j in range(R, n0):
        lt[z][j] = True
    # validity: the set {0..R-1} must be a down-set (no j >= R below some i < R)
    for i in range(R):
        for j in range(R, n0):
            assert not l0[j][i], "first R elements are not a down-set"
    # transitivity check
    for a in range(n):
        for b in range(n):
            if lt[a][b]:
                for c in range(n):
                    if lt[b][c]:
                        assert lt[a][c]
    return n, lt


def comp_connected(n, lt):
    """comparability graph connected (P is not a disjoint union)"""
    if n < 2:
        return True
    seen, stack = {0}, [0]
    while stack:
        x = stack.pop()
        for y in range(n):
            if y not in seen and (lt[x][y] or lt[y][x]):
                seen.add(y)
                stack.append(y)
    return len(seen) == n


def _rel(lt, a, b):
    return 1 if lt[a][b] else (-1 if lt[b][a] else 0)


def module_closure(n, lt, S):
    """smallest module (autonomous set) containing S"""
    M = set(S)
    changed = True
    while changed:
        changed = False
        for z in range(n):
            if z in M:
                continue
            rs = {_rel(lt, z, m) for m in M}
            if len(rs) > 1:
                M.add(z)
                changed = True
    return M


def nontrivial_modules(n, lt):
    """list the minimal module generated by each pair, keeping the proper ones (size < n)"""
    out = set()
    for a in range(n):
        for b in range(a + 1, n):
            M = module_closure(n, lt, {a, b})
            if len(M) < n:
                out.add(frozenset(M))
    return sorted(out, key=len)


def prime(n, lt):
    """no module of size between 2 and n-1 (substitution-indecomposable)"""
    return not nontrivial_modules(n, lt)


def from_dn(dn):
    n = len(dn)
    rel = [(j, i) for i in range(n) for j in range(n) if (dn[i] >> j) & 1]
    lt = closure(n, rel)
    for i in range(n):
        assert sum(1 << j for j in range(n) if lt[j][i]) == dn[i], ("not a down-set list", dn)
    return n, lt


def attach_both(N, R):
    """F_N with z || x_0..x_{R-1}, z < x_R..; and dually z' || x_{N-R}..x_{N-1}, z' > x_0..x_{N-R-1}"""
    n = N + 2
    z, zp = N, N + 1
    rel = [(i, j) for i in range(N) for j in range(N) if j - i >= 2]
    rel += [(z, j) for j in range(R, N)] + [(j, zp) for j in range(N - R)]
    if R < N - R:
        rel += [(z, zp)]
    return n, closure(n, rel)


def hub(W, U, k):
    """HUB PADDING: W + chain c_1<..<c_k, plus c_k > u for every u in U (U a down-set of W).
    W keeps indices 0..m-1; chain is m..m+k-1, c_k = m+k-1."""
    m, lw = W
    for u in U:
        for v in range(m):
            assert not (lw[v][u] and v not in U), "U must be a down-set"
    n = m + k
    rel = [(i, j) for i in range(m) for j in range(m) if lw[i][j]]
    rel += [(m + i, m + i + 1) for i in range(k - 1)]
    rel += [(u, m + k - 1) for u in U]
    return n, closure(n, rel)


def K_leak(E, A):
    """E|A minus sigma(A)| : expected number of A-elements outside the first |A| positions.
    Computed as sum over x in A of P[pos(x) > |A|]."""
    a = len(A)
    tot = Fr(0)
    for x in A:
        N = E.slot_law(x)
        tot += Fr(sum(N[a:]), E.e)
    return tot
