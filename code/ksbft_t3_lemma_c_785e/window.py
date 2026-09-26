"""window.py (mg-785e): can the certificate charge ONLY inversions near the containment step?
Restrict lambda to L-ordered incomparable pairs with both ends in an L-window around the step [3,4] < [2,5] of Q12
(identity family: S0 + SW2 on every L-step, unrestricted).  min sum lambda < 3 => a window-local refutation."""
import sys
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from mulp import *
from xyzlp import Q12, LQ12, mk

def minlam(m, allowed):
    N = len(m.E); ip = m.inv_pairs(); R = m.eq; nl, ny = len(ip), len(R)
    rr, cc, vv = [], [], []
    for i, (u, v) in enumerate(ip):
        if not allowed(u, v): continue
        for k, p in enumerate(m.P):
            if p[v] < p[u]: rr.append(k); cc.append(i); vv.append(-1.0)
    for j, r in enumerate(R):
        for k, c in r.items():
            rr.append(k); cc.append(nl + j); vv.append(-float(c)); rr.append(k); cc.append(nl + ny + j); vv.append(float(c))
    A = coo_matrix((vv, (rr, cc)), shape=(N, nl + 2 * ny)).tocsr()
    c = np.concatenate([np.ones(nl), np.zeros(2 * ny)])
    bnd = [(0, None) if allowed(*ip[i]) else (0, 0) for i in range(nl)] + [(0, None)] * (2 * ny)
    res = linprog(c, A_ub=A, b_ub=-np.ones(N), bounds=bnd, method='highs')
    return res.fun if res.status == 0 else None

if __name__ == '__main__':
    iv = Q12; L = mk(Q12, LQ12); n = len(iv); pos = {v: i for i, v in enumerate(L)}
    steps = [(L[k], L[k + 1]) for k in range(n - 1) if inc(iv, L[k], L[k + 1])]
    m = MuLP(iv, L); m.add_S0()
    for p in steps:
        for W in combinations([w for w in range(n) if w not in p], 2): m.add_SW(p[0], p[1], list(W))
    print('all pairs:', minlam(m, lambda u, v: True))
    for lo, hi in ((3, 4), (2, 5), (1, 6), (1, 7), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 11), (2, 11), (4, 11), (5, 11), (0, 11)):
        print(f'window L-positions [{lo},{hi}] ({[iv[L[k]] for k in (lo, hi)]}):', minlam(m, lambda u, v: lo <= pos[u] <= hi and lo <= pos[v] <= hi))
        sys.stdout.flush()
