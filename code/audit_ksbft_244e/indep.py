"""mg-244e: independent audit instrument for KSBFT-R (mg-7bfc).
Shares NO code with code/ksbft_r_window_padding_7bfc. Different mechanics:
  e(S) = number of linear extensions of the induced subposet on bitmask S, memoised,
         computed TOP-DOWN by removing a maximal element (author: bottom-up level sweep);
  P[x before y] = e(P with x<y added) / e(P)  (author: ideal-lattice sum);
  slot law: P[pos(x)=k] = sum over size-(k-1) down-sets I with x minimal in P-I of e(I) e(P-I-x) / e(P).
Every poset is built from its defining relations as written in docs/KSBFT-R-window-padding.md
(1-indexed there; 0-indexed here), NOT from the author's constructors.
"""
import sys
from fractions import Fraction as Fr
from functools import lru_cache
from itertools import combinations
sys.setrecursionlimit(100000)


class Poset:
    def __init__(self, n, rel):
        self.n = n
        up = [set() for _ in range(n)]
        for a, b in rel:
            up[a].add(b)
        # transitive closure by DFS
        full = []
        for a in range(n):
            seen, st = set(), list(up[a])
            while st:
                c = st.pop()
                if c not in seen:
                    seen.add(c)
                    st.extend(up[c])
            assert a not in seen, "cycle"
            full.append(seen)
        self.above = full
        self.below = [set(b for b in range(n) if a in full[b]) for a in range(n)]
        self.upm = [sum(1 << b for b in full[a]) for a in range(n)]
        self.dnm = [sum(1 << b for b in self.below[a]) for a in range(n)]
        self._memo = {}

    def lt(self, a, b):
        return b in self.above[a]

    def comp(self, a, b):
        return self.lt(a, b) or self.lt(b, a)

    def e(self, S=None):
        if S is None:
            S = (1 << self.n) - 1
        memo, upm = self._memo, self.upm
        def rec(S):
            if S == 0:
                return 1
            r = memo.get(S)
            if r is not None:
                return r
            t, T = 0, S
            while T:
                x = (T & -T).bit_length() - 1
                T &= T - 1
                if upm[x] & S == 0:  # x maximal in S
                    t += rec(S & ~(1 << x))
            memo[S] = t
            return t
        return rec(S)

    def before(self, x, y):
        Q = Poset(self.n, [(a, b) for a in range(self.n) for b in self.above[a]] + [(x, y)])
        return Fr(Q.e(), self.e())

    def inc(self, x):
        return [y for y in range(self.n) if y != x and not self.comp(x, y)]

    def rng(self):
        return max(len(self.inc(x)) for x in range(self.n))

    def g_conn(self, comparability=False):
        seen, st = {0}, [0]
        while st:
            x = st.pop()
            for y in range(self.n):
                if y not in seen and (self.comp(x, y) == comparability):
                    seen.add(y); st.append(y)
        return len(seen) == self.n

    def is_module(self, M):
        for z in range(self.n):
            if z in M:
                continue
            kinds = set((self.lt(z, m), self.lt(m, z)) for m in M)
            if len(kinds) > 1:
                return False
        return True

    def proper_nonchain_module(self):
        """return a proper module with an incomparable pair, else a proper module (chain), else None"""
        found_chain = None
        for a, b in combinations(range(self.n), 2):
            M = {a, b}
            grew = True
            while grew:
                grew = False
                for z in range(self.n):
                    if z not in M and len(set((self.lt(z, m), self.lt(m, z)) for m in M)) > 1:
                        M.add(z); grew = True
            if len(M) < self.n:
                if any(not self.comp(u, v) for u, v in combinations(M, 2)):
                    return ("nonchain", sorted(M))
                found_chain = ("chain", sorted(M))
        return found_chain

    def ideals_by_size(self):
        lev = [{0}]
        for _ in range(self.n):
            nxt = set()
            for I in lev[-1]:
                for x in range(self.n):
                    if not (I >> x) & 1 and self.dnm[x] & ~I == 0:
                        nxt.add(I | (1 << x))
            lev.append(nxt)
        return lev

    def slot_law(self, x, lev=None):
        lev = lev or self.ideals_by_size()
        full = (1 << self.n) - 1
        out = []
        for k in range(self.n):
            s = 0
            for I in lev[k]:
                if not (I >> x) & 1 and self.dnm[x] & ~I == 0:
                    s += self.e(I) * self.e(full & ~I & ~(1 << x))
            out.append(Fr(s, self.e()))
        assert sum(out) == 1
        return out

    def minimal(self):
        return [x for x in range(self.n) if not self.below[x]]

    def maximal(self):
        return [x for x in range(self.n) if not self.above[x]]

    def delta(self):
        return max(min(p, 1 - p) for p in (self.before(a, b) for a, b in combinations(range(self.n), 2)
                                              if not self.comp(a, b)))


def fibrel(N, off=0):
    return [(off + i, off + j) for i in range(N) for j in range(N) if j - i >= 2]


def F(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


FAIL = []
def chk(c, msg):
    print(("  ok    " if c else "  FAIL  ") + msg)
    if not c:
        FAIL.append(msg)
