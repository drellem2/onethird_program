import sys
from itertools import combinations
from mulp import *
from xyzlp import Q12, LQ12, mk
iv = Q12; L = mk(Q12, LQ12); n = len(iv); ix = {t: i for i, t in enumerate(iv)}; pos = {v: i for i, v in enumerate(L)}
pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if inc(iv, u, v)]
steps = [(L[k], L[k+1]) for k in range(n-1) if inc(iv, L[k], L[k+1])]
def run(name, prs, k=2):
    m = MuLP(iv, L); m.add_S0()
    for u, v in prs:
        for W in combinations([w for w in range(n) if w not in (u, v)], k): m.add_SW(u, v, list(W))
    v, x = m.solve(); print(f"{name:50s} eps* = {v}"); sys.stdout.flush(); return v
run('SW2 on L-steps only', steps)
run('SW2 on non-step pairs only', [p for p in pairs if p not in steps and p[::-1] not in steps])
a, a2 = ix[(3, 4)], ix[(2, 5)]; b, b2 = ix[(5, 8)], ix[(6, 7)]
run('SW2 on the two containment steps', [(a, a2), (b, b2)])
for p in steps:
    run(f'SW2 on single step {iv[p[0]]},{iv[p[1]]}', [p])
