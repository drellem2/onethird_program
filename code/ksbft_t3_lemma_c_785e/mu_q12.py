import sys
from itertools import combinations
from mulp import *
from xyzlp import Q12, LQ12, mk
iv = Q12; L = mk(Q12, LQ12); n = len(iv); ix = {t: i for i, t in enumerate(iv)}
a, a2, s, t = ix[(3, 4)], ix[(2, 5)], ix[(5, 6)], ix[(5, 8)]
b, b2 = ix[(5, 8)], ix[(6, 7)]           # the dual containment step
pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if inc(iv, u, v)]
def run(name, f):
    m = MuLP(iv, L); m.add_S0(); f(m); v, x = m.solve(); print(f"{name:60s} eps* = {v}"); sys.stdout.flush(); return v
run('S0', lambda m: None)
run('S0 + PT(containment steps, pointwise)', lambda m: (m.add_PT(a, a2), m.add_PT(b2, b)))
run('S0 + PT(every pair, pointwise)', lambda m: [m.add_PT(u, v) for u, v in pairs])
run('S0 + SW(steps, W={s,t})', lambda m: (m.add_SW(a, a2, [s, t]), m.add_SW(b2, b, [ix[(2,5)], ix[(4,5)]])))
def sw1(m, prs):
    for u, v in prs:
        for w in range(n):
            if w not in (u, v): m.add_SW(u, v, [w])
run('S0 + SW(all pairs, |W|=1)', lambda m: sw1(m, pairs))
def sw2(m, prs):
    for u, v in prs:
        for W in combinations([w for w in range(n) if w not in (u, v)], 2): m.add_SW(u, v, list(W))
run('S0 + SW(all pairs, |W|=2)', lambda m: sw2(m, pairs))
