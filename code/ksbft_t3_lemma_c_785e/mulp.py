"""mulp.py (mg-785e): the FULL-MEASURE lift.  Variables: mu(sigma) >= 0 for every linear extension sigma of P
(sum 1).  A counterexample with 2/3-order L needs mu = uniform and mu(v before u) <= 1/3 - eps for every
L-inversion.  Replace 'uniform' by a chosen family of BIJECTION IDENTITIES (each true for the uniform measure):
  S0      unconditioned Swap Identity (Thm 1.1 of mg-561a): mu(Lambda_1(a,a')) = mu(Lambda_1(a',a)), all pairs;
  S0cov   the same for the 'exchange-valid' sets V: the exchange tau_{a,a'} is a bijection V(a before a') -> V(a' before a)
          (identical to S0: V cap {a before a'} = Lambda_1).
  SW(k)   Swap Identity CONDITIONED on the relative order of a set W of other elements (|W| <= k, W chosen near
          the pair): tau preserves the order of all other elements, so mu(Lambda_1(a,a') & F) = mu(Lambda_1(a',a) & tau F)
          with tau F = F for F determined by the order of W.
  PT(pairs) POINTWISE exchange invariance for chosen pairs: mu(sigma) = mu(tau sigma) for sigma in V(a,a').
  ADJ     pointwise invariance under every adjacent transposition of incomparable elements (=> mu uniform; control).
max eps.  eps* <= 0 / infeasible: the family refutes L (a proof, since each identity is a theorem)."""
import sys
from itertools import combinations
from fractions import Fraction as F
from t3lib import *

def extensions(iv):
    n = len(iv); dn = downmasks(iv); out = []
    def rec(I, seq):
        if len(seq) == n: out.append(tuple(seq)); return
        for v in range(n):
            if not I >> v & 1 and dn[v] & ~I == 0:
                seq.append(v); rec(I | 1 << v, seq); seq.pop()
    rec(0, []); return out

class MuLP:
    def __init__(self, iv, L):
        self.iv = iv; self.n = len(iv); self.L = L; self.pos = {v: i for i, v in enumerate(L)}
        self.E = extensions(iv); self.idx = {s: i for i, s in enumerate(self.E)}
        self.P = [{v: i for i, v in enumerate(s)} for s in self.E]
        self.C = covers(iv)
        self.eq = []      # list of dict(var->coef) == 0
    def inv_pairs(self):
        iv, pos = self.iv, self.pos
        return [(u, v) for u in range(self.n) for v in range(self.n) if inc(iv, u, v) and pos[u] < pos[v]]
    def swap(self, k, a, b):
        s = list(self.E[k]); p = self.P[k]; s[p[a]], s[p[b]] = b, a; return self.idx.get(tuple(s))
    def lam1(self, a, a2):
        """indices of extensions in Lambda_1(a,a') (a before a', no separator between)"""
        A, B = seps_typed(self.iv, self.C, a, a2); S = A + B; out = []
        for k, p in enumerate(self.P):
            if p[a] < p[a2] and not any(p[a] < p[z] < p[a2] for z in S): out.append(k)
        return out
    def add_S0(self, pairs=None):
        iv = self.iv
        for a, a2 in (pairs or [(u, v) for u in range(self.n) for v in range(u + 1, self.n) if inc(iv, u, v)]):
            r = {}
            for k in self.lam1(a, a2): r[k] = r.get(k, 0) + 1
            for k in self.lam1(a2, a): r[k] = r.get(k, 0) - 1
            self.eq.append(r)
    def add_SW(self, a, a2, W):
        """Swap identity conditioned on the relative order of W (W disjoint from {a,a'})."""
        l1 = self.lam1(a, a2); l3 = self.lam1(a2, a)
        key = lambda k: tuple(sorted(W, key=lambda w: self.P[k][w]))
        g = {}
        for k in l1: g.setdefault(key(k), {}); g[key(k)][k] = g[key(k)].get(k, 0) + 1
        for k in l3: g.setdefault(key(k), {}); g[key(k)][k] = g[key(k)].get(k, 0) - 1
        for r in g.values(): self.eq.append(r)
    def add_PT(self, a, a2):
        for k in self.lam1(a, a2):
            j = self.swap(k, a, a2); assert j is not None
            self.eq.append({k: 1, j: -1})
    def add_ADJ(self):
        for k, s in enumerate(self.E):
            for i in range(self.n - 1):
                if inc(self.iv, s[i], s[i + 1]):
                    j = self.swap(k, s[i], s[i + 1])
                    if j > k: self.eq.append({k: 1, j: -1})
    def solve(self):
        import numpy as np
        from scipy.optimize import linprog
        from scipy.sparse import coo_matrix
        N = len(self.E); nv = N + 1; eps = N
        ip = self.inv_pairs()
        R, Cc, V = [], [], []
        for i, (u, v) in enumerate(ip):
            for k, p in enumerate(self.P):
                if p[v] < p[u]: R.append(i); Cc.append(k); V.append(1.0)
            R.append(i); Cc.append(eps); V.append(1.0)
        Aub = coo_matrix((V, (R, Cc)), shape=(len(ip), nv)).tocsr(); bub = np.full(len(ip), 1 / 3)
        R, Cc, V = [], [], []
        for i, r in enumerate(self.eq):
            for k, c in r.items(): R.append(i); Cc.append(k); V.append(float(c))
        for k in range(N): R.append(len(self.eq)); Cc.append(k); V.append(1.0)
        Aeq = coo_matrix((V, (R, Cc)), shape=(len(self.eq) + 1, nv)).tocsr()
        beq = np.zeros(len(self.eq) + 1); beq[-1] = 1
        c = np.zeros(nv); c[eps] = -1
        bounds = [(0, None)] * N + [(-1, 1)]
        res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds, method='highs')
        if res.status == 2: return None, None
        self.res = res
        return -res.fun, res.x
