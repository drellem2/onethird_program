"""xyzcheck.py (mg-785e): is the LP optimum a genuine point of the NONLINEAR system?
Evaluates every XYZ instance (and its dual) with its true product at the float optimum of xyzlp.build."""
import sys
from itertools import combinations
from xyzlp import *
import flp

def evalf(form, x):
    return sum((float(c) if k is None else float(c) * x[k]) for k, c in form.items())

def xyz_violations(iv, L, M, x, T, triples_only=True):
    n = len(iv); pos = {v: i for i, v in enumerate(L)}
    name2 = {nm: k for k, nm in enumerate(M.names)}
    def P(y, z):
        if lt(iv, y, z): return 1.0
        if lt(iv, z, y): return 0.0
        if pos[z] < pos[y]: return x[name2[f'x{iv[z]}{iv[y]}']]
        return 1 - x[name2[f'x{iv[y]}{iv[z]}']]
    out = []
    for trip, (ords, vs) in T.items():
        for xx in trip:
            y, z = [k for k in trip if k != xx]
            if not (inc(iv, xx, y) and inc(iv, xx, z)): continue
            j1 = sum(x[vs[o]] for o in ords if o.index(xx) < o.index(y) and o.index(xx) < o.index(z))
            j2 = sum(x[vs[o]] for o in ords if o.index(xx) > o.index(y) and o.index(xx) > o.index(z))
            out.append((j1 - P(xx, y) * P(xx, z), 'x<y,z', iv[xx], iv[y], iv[z]))
            out.append((j2 - P(y, xx) * P(z, xx), 'y,z<x', iv[xx], iv[y], iv[z]))
    return sorted(out)

if __name__ == '__main__':
    L = mk(Q12, LQ12)
    M, eps, T, nx = build(Q12, L, xyz=True)
    v, x, d = flp.solve(M, eps)
    V = xyz_violations(Q12, L, M, x, T)
    print(f"eps* ~ {v:.6f}; XYZ instances {len(V)}; most violated (slack = joint - product):")
    for r in V[:8]: print("  ", f"{r[0]:+.5f}", *r[1:])
