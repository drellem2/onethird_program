"""eng.py (audit mg-6c30): independent engine for the audit of mg-561a (KSBFT-T2).
Shares NO code with ksbft_t_interval_orders_afa4/iolib.py, ksbft_t2_two_separator_561a/t2lib.py or
audit_ksbft_5ecf/eng.py.

- gen(n): canonical interval orders (Fishburn form: endpoints 1..h, every point is a left AND a right end),
  as sorted tuples of (l, r); certified by counts == OEIS A022493.
- Poset(iv): relation matrices, covers, separators A(x,y), B(x,y) from the COVER relation.
- count(): exact linear-extension counts by DP over (down-closed set, automaton state).
"""
from fractions import Fraction as Fr
from functools import lru_cache

A022493 = {1: 1, 2: 2, 3: 5, 4: 15, 5: 53, 6: 217, 7: 1014, 8: 5335, 9: 31240, 10: 201608}


def gen(n):
    """Yield every canonical interval multiset of size n (each exactly once)."""
    for h in range(1, n + 1):
        types = [(l, r) for l in range(1, h + 1) for r in range(l, h + 1)]  # sorted by l then r
        T = len(types)
        # for pruning: for each type index i, the set of left points / right points still coverable by types >= i
        out = []

        def rec(i, left, cnt, needL, needR):
            # needL / needR: bitmask of points (1..h) not yet covered as left / right end
            if cnt == n:
                if needL == 0 and needR == 0:
                    yield tuple(out)
                return
            if i == T:
                return
            rem = n - cnt
            if bin(needL).count('1') > rem or bin(needR).count('1') > rem:
                return
            l, r = types[i]
            # left points < l that are still uncovered can never be covered (types sorted by l)
            if needL & ((1 << l) - 2):
                return
            for m in range(rem, -1, -1):
                if m:
                    out.extend([(l, r)] * m)
                    nl = needL & ~(1 << l); nr = needR & ~(1 << r)
                else:
                    nl, nr = needL, needR
                yield from rec(i + 1, left, cnt + m, nl, nr)
                if m:
                    del out[-m:]
        full = ((1 << (h + 1)) - 2)
        yield from rec(0, None, 0, full, full)


class Poset:
    def __init__(self, n, lt):
        """lt[x][y] True iff x < y (strict, transitive)."""
        self.n = n
        self.lt = lt
        self.inc = [[x != y and not lt[x][y] and not lt[y][x] for y in range(n)] for x in range(n)]
        self.cov = [[lt[x][y] and not any(lt[x][c] and lt[c][y] for c in range(n)) for y in range(n)] for x in range(n)]
        self.dn = [sum(1 << w for w in range(n) if lt[w][v]) for v in range(n)]
        self.upm = [sum(1 << w for w in range(n) if lt[v][w]) for v in range(n)]
        self._A = {}; self._B = {}

    @classmethod
    def from_iv(cls, iv):
        n = len(iv)
        P = cls(n, [[iv[x][1] < iv[y][0] for y in range(n)] for x in range(n)])
        P.iv = iv
        return P

    def A(self, x, y):
        """above-separators of the ordered incomparable pair (x,y): x covered by z, z || y."""
        k = (x, y)
        if k not in self._A:
            self._A[k] = frozenset(z for z in range(self.n) if self.cov[x][z] and self.inc[z][y])
        return self._A[k]

    def B(self, x, y):
        """below-separators: w covered by y, w || x."""
        k = (x, y)
        if k not in self._B:
            self._B[k] = frozenset(w for w in range(self.n) if self.cov[w][y] and self.inc[w][x])
        return self._B[k]

    def S(self, x, y):
        return self.A(x, y) | self.B(x, y)

    def dominates(self, x, y):
        """x dominates y (x weaker/earlier): down(x) <= down(y), up(x) >= up(y), not twins, x || y."""
        if not self.inc[x][y]: return False
        dx, dy, ux, uy = self.dn[x], self.dn[y], self.upm[x], self.upm[y]
        return (dx & ~dy) == 0 and (uy & ~ux) == 0 and not (dx == dy and ux == uy)

    # ---- exact counting ----
    def count(self, step=None, start=0, accept=None):
        """number of linear extensions; with an automaton (step(state, v) -> state or None to reject),
        returns dict final_state -> count."""
        n = self.n; dn = self.dn
        cur = {(0, start): 1}
        for _ in range(n):
            nxt = {}
            for (I, s), c in cur.items():
                for v in range(n):
                    if not (I >> v) & 1 and (dn[v] & ~I) == 0:
                        t = s if step is None else step(s, v)
                        if t is None: continue
                        key = (I | (1 << v), t)
                        nxt[key] = nxt.get(key, 0) + c
            cur = nxt
        res = {}
        for (I, s), c in cur.items():
            res[s] = res.get(s, 0) + c
        return res

    def e(self):
        return self.count()[0]

    def before_counts(self):
        """M[x][y] = #LE with x before y, via one ideal DP with forward/backward counts."""
        n = self.n; dn = self.dn; full = (1 << n) - 1
        fw = {0: 1}
        order = [0]
        # BFS by size
        layer = {0: 1}
        layers = [layer]
        for _ in range(n):
            nl = {}
            for I, c in layer.items():
                for v in range(n):
                    if not (I >> v) & 1 and (dn[v] & ~I) == 0:
                        J = I | (1 << v); nl[J] = nl.get(J, 0) + c
            layers.append(nl); layer = nl
        fwd = {}
        for L in layers: fwd.update(L)
        bwd = {full: 1}
        for L in reversed(layers[:-1]):
            for I in L:
                s = 0
                for v in range(n):
                    if not (I >> v) & 1 and (dn[v] & ~I) == 0:
                        s += bwd[I | (1 << v)]
                bwd[I] = s
        # #LE with x before y = sum over ideals I containing x, not y, with y addable... simpler:
        # count of LE where x placed at transition I -> I|x and y not in I: sum fwd[I]*bwd[I|x] over I without x,y
        M = [[0] * n for _ in range(n)]
        for I, c in fwd.items():
            for x in range(n):
                if not (I >> x) & 1 and (dn[x] & ~I) == 0:
                    t = c * bwd[I | (1 << x)]
                    for y in range(n):
                        if y != x and not (I >> y) & 1:
                            M[x][y] += t
        return M, bwd[0]


def lambdas(P, a, a2, S=None):
    """(|L1|, |L2|, |L3|) for ordered pair (a,a2): L1 = a before a2 no S strictly between, L2 = some S between,
    L3 = a2 before a."""
    S = P.S(a, a2) if S is None else frozenset(S)
    def step(s, v):
        if s >= 3: return s
        if v == a: return 1
        if v == a2: return 5 if s == 0 else (3 if s == 1 else 4)
        if s == 1 and v in S: return 2
        return s
    r = P.count(step)
    return r.get(3, 0), r.get(4, 0), r.get(5, 0)
