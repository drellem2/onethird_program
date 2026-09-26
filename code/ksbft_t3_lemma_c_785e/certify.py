"""certify.py (mg-785e): EXACT pointwise certificates in the full-measure lift.
A certificate for (P, L) is rational lambda_i >= 0 (one per L-ordered incomparable pair i = (u,v)) and rational
y_r (one per identity row r of the chosen family; each row is a function R_r on linear extensions with
E_uniform[R_r] = 0 by a bijection) such that, for EVERY linear extension sigma,
      G(sigma) := sum_i lambda_i [sigma puts v before u] + sum_r y_r R_r(sigma) >= 1,     and   sum_i lambda_i <= 3.
Taking expectations under the uniform measure: sum_i lambda_i P(inversion i) >= 1, so some L-inversion has
probability >= 1/3: L is not the 2/3-order of a counterexample.  The check is exact (Fractions, every sigma).
The multipliers come from a float LP (scipy) and are rounded; the exact check alone is the proof."""
import sys
from fractions import Fraction as F
from itertools import combinations
from mulp import *

def rows_of(m):
    return m.eq          # list of dict ext_index -> coef (each has uniform expectation 0)

def find(m):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    N = len(m.E); ip = m.inv_pairs(); R = rows_of(m); nl, ny = len(ip), len(R)
    # variables: lambda (nl, >=0), y+ (ny), y- (ny)
    rr, cc, vv = [], [], []
    for i, (u, v) in enumerate(ip):
        for k, p in enumerate(m.P):
            if p[v] < p[u]: rr.append(k); cc.append(i); vv.append(-1.0)
    for j, r in enumerate(R):
        for k, c in r.items():
            rr.append(k); cc.append(nl + j); vv.append(-float(c)); rr.append(k); cc.append(nl + ny + j); vv.append(float(c))
    A = coo_matrix((vv, (rr, cc)), shape=(N, nl + 2 * ny)).tocsr()
    c = np.concatenate([np.ones(nl), np.zeros(2 * ny)])
    res = linprog(c, A_ub=A, b_ub=-np.ones(N), bounds=[(0, None)] * (nl + 2 * ny), method='highs')
    if res.status != 0: return None
    lam = res.x[:nl]; y = res.x[nl:nl + ny] - res.x[nl + ny:]
    return res.fun, lam, y

def exact_check(m, lam, y, den=10**6):
    ip = m.inv_pairs(); R = rows_of(m); N = len(m.E)
    L = [F(round(x * den), den) if x > 1e-12 else F(0) for x in lam]
    Y = [F(round(x * den), den) for x in y]
    G = [F(0)] * N
    for i, (u, v) in enumerate(ip):
        if L[i]:
            for k, p in enumerate(m.P):
                if p[v] < p[u]: G[k] += L[i]
    for j, r in enumerate(R):
        if Y[j]:
            for k, c in r.items(): G[k] += Y[j] * c
    g = min(G)
    tot = sum(L)
    ok = g > 0 and tot / g < 3
    return ok, tot / g if g > 0 else None, L, Y

if __name__ == '__main__':
    from survivors import survivors
    for iv, Lx, v0 in survivors():
        n = len(iv)
        steps = [(Lx[k], Lx[k + 1]) for k in range(n - 1) if inc(iv, Lx[k], Lx[k + 1])]
        for fam in ('S0', 'S0+SW2(steps)'):
            m = MuLP(iv, Lx); m.add_S0()
            if fam != 'S0':
                for p in steps:
                    for W in combinations([w for w in range(n) if w not in p], 2): m.add_SW(p[0], p[1], list(W))
            r = find(m)
            if r is None or r[0] >= 3 - 1e-9:
                print(f"n={n} {fam:14s}: no certificate (min sum lambda = {None if r is None else round(r[0], 6)})"); sys.stdout.flush(); continue
            ok, ratio, L, Y = exact_check(m, r[1], r[2])
            print(f"n={n} {fam:14s}: float min sum lambda = {r[0]:.6f}; EXACT check {'PASSES' if ok else 'FAILS'}: "
                  f"sum lambda / min G = {ratio} ({float(ratio):.6f} < 3); support: {sum(1 for x in L if x)} pairs, {sum(1 for x in Y if x)} identity rows  P={iv}")
            sys.stdout.flush()
            break
