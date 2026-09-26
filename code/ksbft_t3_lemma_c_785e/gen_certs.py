"""gen_certs.py (mg-785e; needs scipy -- a float LP only PROPOSES multipliers): writes certs.json, the rational
pointwise certificates (see certify.py) for the 13 LP-feasible survivors of mg-561a and for the window-local
refutation of Q12.  verify_certs.py re-checks them EXACTLY with no scipy.  Families (deterministic row order):
  S0        = MuLP.add_S0(all incomparable pairs, (u<v) index order)
  S0+SW2st  = S0 then add_SW(step, W) for every L-step and every 2-set W of other elements (combinations order)
  S0+SW2all = S0 then add_SW(pair, W) for every incomparable pair and every 2-set W
  window    = lambda restricted to pairs with both L-positions in [lo, hi]."""
import json, sys
from itertools import combinations
from fractions import Fraction as F
from certify import find, exact_check
from mulp import MuLP, inc
from survivors import survivors


def family(iv, L, fam):
    n = len(iv); m = MuLP(iv, L); m.add_S0()
    if fam == 'S0+SW2st':
        for k in range(n - 1):
            p = (L[k], L[k + 1])
            if inc(iv, *p):
                for W in combinations([w for w in range(n) if w not in p], 2): m.add_SW(p[0], p[1], list(W))
    elif fam == 'S0+SW2all':
        for u in range(n):
            for v in range(u + 1, n):
                if inc(iv, u, v):
                    for W in combinations([w for w in range(n) if w not in (u, v)], 2): m.add_SW(u, v, list(W))
    return m

def rat(x, den=10**6): return F(round(x * den), den)

if __name__ == '__main__':
    from local_q12 import solve_min
    out = []
    jobs = [(iv, L, fam, None) for iv, L, _ in survivors() for fam in ('S0', 'S0+SW2st')]
    from xyzlp import Q12, LQ12, mk
    jobs.append((Q12, mk(Q12, LQ12), 'S0+SW2all', (2, 5)))
    done = set()
    for iv, L, fam, win in jobs:
        key = (tuple(iv), tuple(L))
        if win is None and key in done: continue
        m = family(iv, L, fam)
        if win is None:
            r = find(m)
            if r is None or r[0] >= 3 - 1e-9: continue
            lam, y = r[1], r[2]
        else:
            pos = {v: i for i, v in enumerate(L)}; lo, hi = win
            _, lam, y = solve_min(m, lambda u, v: lo <= pos[u] <= hi and lo <= pos[v] <= hi)
        ok, ratio, Lr, Yr = exact_check(m, lam, y)
        assert ok, (iv, fam)
        if win is None: done.add(key)
        out.append(dict(P=iv, L=[iv[x] for x in L], family=fam, window=win,
                        lam={f'{u},{v}': str(x) for (u, v), x in zip(m.inv_pairs(), Lr) if x},
                        y={str(j): str(x) for j, x in enumerate(Yr) if x}, ratio=str(ratio)))
        print(fam, win, iv, 'ratio', ratio, float(ratio)); sys.stdout.flush()
    json.dump(out, open('certs.json', 'w'), indent=0)
