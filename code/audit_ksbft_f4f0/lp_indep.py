"""lp_indep.py (audit mg-f4f0; needs scipy -- FLOAT, a probe): independent certificate LP for Q12 (mg-785e sec 3.3,
sec 6 'k = 0 fails at Q12, min sum lambda = 3.125').  Own rows (certs_indep.Rows, own engine), own LP:
   min sum_i lambda_i  s.t.  sum_i lambda_i [inv_i(sigma)] + sum_r y_r R_r(sigma) >= 1 for every extension sigma,
   lambda >= 0 on the allowed charged pairs, y free.   (Prop 1.2: optimum < 3  <=> refutation.)"""
import sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack
from certs_indep import build, Lidx
from eng import inc

Q12 = [(1,1),(1,2),(2,3),(2,5),(3,4),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)]
LQ = [(1,1),(1,2),(2,3),(3,4),(2,5),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)]

def solve(m, L, allowed):
    pos = {v: i for i, v in enumerate(L)}; N = len(m.E)
    pairs = [(u, v) for u in range(m.n) for v in range(m.n) if inc(m.iv, u, v) and pos[u] < pos[v] and allowed(pos[u], pos[v])]
    r, c, d = [], [], []
    for i, (u, v) in enumerate(pairs):
        for k, p in enumerate(m.pos):
            if p[v] < p[u]: r.append(k); c.append(i); d.append(1.0)
    Al = coo_matrix((d, (r, c)), shape=(N, len(pairs)))
    r, c, d = [], [], []
    for j, row in enumerate(m.rows):
        for k, x in row.items(): r.append(k); c.append(j); d.append(float(x))
    Ay = coo_matrix((d, (r, c)), shape=(N, len(m.rows)))
    A = hstack([Al, Ay]).tocsr()
    cost = np.concatenate([np.ones(len(pairs)), np.zeros(len(m.rows))])
    bounds = [(0, None)] * len(pairs) + [(None, None)] * len(m.rows)
    res = linprog(cost, A_ub=-A, b_ub=-np.ones(N), bounds=bounds, method='highs')
    return res.fun if res.status == 0 else None

if __name__ == '__main__':
    L = Lidx(Q12, LQ)
    for fam in ('S0', 'S0+SW2st', 'S0+SW2all'):
        t0 = time.time(); m = build(Q12, L, fam)
        for lab, al in (('all pairs', lambda i, j: True), ('containment step only [3,4]', lambda i, j: i == 3 and j == 4),
                        ('window [2,5]', lambda i, j: 2 <= i <= 5 and 2 <= j <= 5), ('window [0,5]', lambda i, j: j <= 5),
                        ('window [1,7]', lambda i, j: 1 <= i and j <= 7)):
            v = solve(m, L, al)
            print(f'Q12 rows={fam:10s} ({len(m.rows):4d}) charged={lab:28s} min sum lambda = {("%.4f" % v) if v is not None else "INFEASIBLE (no certificate at any ratio)"}  {"REFUTED (<3)" if v is not None and v < 3 - 1e-9 else "not refuted"}', flush=True)
