"""local_q12.py (mg-785e): the window-[2,5] refutation of Q12 (charged pairs among [2,3],[3,4],[2,5],[4,5]),
identity family S0 + SW2 on every incomparable pair.  Prints the certificate's support and prunes the
identity family pair by pair (deletion filter over the conditioned pairs) to a minimal set of pairs."""
import sys
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from mulp import *
from xyzlp import Q12, LQ12, mk

def solve_min(m, allowed):
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
    if res.status != 0: return None, None, None
    return res.fun, res.x[:nl], res.x[nl:nl + ny] - res.x[nl + ny:]

iv = Q12; L = mk(Q12, LQ12); n = len(iv); pos = {v: i for i, v in enumerate(L)}
pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if inc(iv, u, v)]
allowed = lambda u, v: 2 <= pos[u] <= 5 and 2 <= pos[v] <= 5

def build(cpairs, s0=True):
    m = MuLP(iv, L); lab = []
    if s0:
        m.add_S0(); lab += [('S0', None, None)] * len(m.eq)
    for p in cpairs:
        for W in combinations([w for w in range(n) if w not in p], 2):
            k0 = len(m.eq); m.add_SW(p[0], p[1], list(W)); lab += [('SW', p, W)] * (len(m.eq) - k0)
    return m, lab

if __name__ == '__main__':
    keep = list(pairs)
    m, lab = build(keep); v, lam, y = solve_min(m, allowed); print('start', v, len(keep), 'conditioned pairs'); sys.stdout.flush()
    i = 0
    while i < len(keep):
        trial = keep[:i] + keep[i + 1:]
        m, lab = build(trial); v2, _, _ = solve_min(m, allowed)
        if v2 is not None and v2 < 3 - 1e-6: keep = trial
        else: i += 1
    print('minimal conditioned pairs:', [(iv[u], iv[v]) for u, v in keep])
    m, lab = build(keep); v, lam, y = solve_min(m, allowed); print('min sum lambda', v)
    ip = m.inv_pairs()
    print('lambda:', [(iv[u], iv[v], round(x, 4)) for (u, v), x in zip(ip, lam) if x > 1e-7])
    agg = {}
    for j, x in enumerate(y):
        if abs(x) > 1e-7:
            t = lab[j]; key = (t[0], (iv[t[1][0]], iv[t[1][1]]) if t[1] else None, tuple(iv[w] for w in t[2]) if t[2] else None)
            agg[key] = agg.get(key, 0) + abs(x)
    for k, w in sorted(agg.items(), key=lambda z: -z[1]): print('  ', k, round(w, 4))
