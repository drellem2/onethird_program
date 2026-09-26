"""mg-5371 shared exact machinery: posets as lists of predecessor bitmasks,
exact linear-extension statistics by downset DP (Fractions / ints)."""
from functools import lru_cache
from fractions import Fraction
import itertools, random

def closure(n, rel):
    """rel: set of (i,j) meaning i<j. Returns below[j] = bitmask of i<j (transitive)."""
    below = [0]*n
    for (i, j) in rel:
        below[j] |= 1 << i
    changed = True
    while changed:
        changed = False
        for j in range(n):
            b = below[j]
            nb = b
            m = b
            while m:
                i = (m & -m).bit_length()-1
                m &= m-1
                nb |= below[i]
            if nb != b:
                below[j] = nb; changed = True
    for j in range(n):
        assert not (below[j] >> j) & 1, "cycle"
    return below

class Poset:
    def __init__(self, n, below):
        self.n = n; self.below = below
        self.full = (1 << n) - 1
        self._up = {}
        self._down = {}
    def e_down(self, S):
        """number of linear extensions of the subposet on downset S"""
        d = self._down
        if S in d: return d[S]
        if S == 0: return 1
        tot = 0
        m = S
        while m:
            i = (m & -m).bit_length()-1; m &= m-1
            # i maximal in S: nothing in S above i
            ok = True
            T = S & ~(1 << i)
            # need: no j in S with i in below[j]
            mm = T
            while mm:
                j = (mm & -mm).bit_length()-1; mm &= mm-1
                if (self.below[j] >> i) & 1: ok = False; break
            if ok: tot += self.e_down(T)
        d[S] = tot
        return tot
    def e_up(self, S):
        """extensions of the subposet on filter complement-of-downset: S is a downset, count ext of P\\S"""
        return self.e_down_general(self.full & ~S)
    def e_down_general(self, T):
        # extensions of subposet induced on T (any set) -- count by removing minimal elements
        d = self._up
        if T in d: return d[T]
        if T == 0: return 1
        tot = 0
        m = T
        while m:
            i = (m & -m).bit_length()-1; m &= m-1
            if self.below[i] & T == 0:
                tot += self.e_down_general(T & ~(1 << i))
        d[T] = tot
        return tot
    def is_down(self, S):
        m = S
        while m:
            i = (m & -m).bit_length()-1; m &= m-1
            if self.below[i] & ~S: return False
        return True
    def downsets(self):
        # enumerate downsets by DFS
        out = []
        seen = set()
        stack = [0]
        while stack:
            S = stack.pop()
            if S in seen: continue
            seen.add(S); out.append(S)
            for i in range(self.n):
                if not (S >> i) & 1 and (self.below[i] & ~S) == 0:
                    stack.append(S | (1 << i))
        return out
    def total(self):
        return self.e_down_general(self.full)
    def placements(self, x):
        """list of (S, weight): S downset not containing x with below[x] subset S,
        weight = #extensions where the set of elements before x is exactly S."""
        res = []
        for S in self.downsets():
            if (S >> x) & 1: continue
            if self.below[x] & ~S: continue
            res.append((S, self.e_down_general(S) * self.e_down_general(self.full & ~S & ~(1 << x))))
        return res
    def comparable(self, a, b):
        return (self.below[a] >> b) & 1 or (self.below[b] >> a) & 1

def popcount(v): return bin(v).count("1")

def width(P):
    # max antichain by brute force (small n)
    n = P.n; best = 0
    for mask in range(1 << n):
        k = popcount(mask)
        if k <= best: continue
        ok = True
        el = [i for i in range(n) if (mask >> i) & 1]
        for a, b in itertools.combinations(el, 2):
            if P.comparable(a, b): ok = False; break
        if ok: best = k
    return best

def is_logconcave(seq):
    """no internal zeros and a_k^2 >= a_{k-1} a_{k+1}"""
    idx = [i for i, v in enumerate(seq) if v]
    if not idx: return True
    lo, hi = idx[0], idx[-1]
    for i in range(lo, hi+1):
        if seq[i] == 0: return False
    for i in range(lo+1, hi):
        if seq[i]*seq[i] < seq[i-1]*seq[i+1]: return False
    return True
