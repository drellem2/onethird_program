"""mu_surv.py (mg-785e): the full-measure lift on all 13 LP-feasible survivors: eps* with S0 (unconditioned Swap
Identity, all pairs) and with S0 + SW2 on the L-steps (swap identities of each L-step conditioned on the relative
order of every 2 other elements).  eps* < 0 = refuted (float probe; see certify.py for exact certificates)."""
import sys, time
from itertools import combinations
from mulp import *
from survivors import survivors
for iv, L, v0 in survivors():
    n = len(iv); t0 = time.time()
    steps = [(L[k], L[k + 1]) for k in range(n - 1) if inc(iv, L[k], L[k + 1])]
    m = MuLP(iv, L); m.add_S0(); e0 = m.solve()[0]
    for p in steps:
        for W in combinations([w for w in range(n) if w not in p], 2): m.add_SW(p[0], p[1], list(W))
    e2 = m.solve()[0]
    print(f"n={n} e={len(m.E):6d} LP(561a)={v0:.5f}  S0-lift={e0:+.5f}  +SW2(steps)={e2:+.5f}  {'REFUTED' if e2 < 0 else 'feasible'}  [{time.time()-t0:.0f}s]  P={iv}")
    sys.stdout.flush()
