"""window3.py (mg-785e): as window.py but with swap identities of every L-step conditioned on the order of 3 other
elements (SW3), and on every incomparable pair (SW2-all).  Is there a refutation of Q12 that charges only the
inversions of the containment step's window (no end pair)?"""
import sys
from itertools import combinations
from window import minlam, MuLP, inc
from xyzlp import Q12, LQ12, mk
iv = Q12; L = mk(Q12, LQ12); n = len(iv); pos = {v: i for i, v in enumerate(L)}
steps = [(L[k], L[k + 1]) for k in range(n - 1) if inc(iv, L[k], L[k + 1])]
pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if inc(iv, u, v)]
for fam in ('SW3(steps)', 'SW2(all pairs)'):
    m = MuLP(iv, L); m.add_S0()
    if fam == 'SW3(steps)':
        for p in steps:
            for W in combinations([w for w in range(n) if w not in p], 3): m.add_SW(p[0], p[1], list(W))
    else:
        for p in pairs:
            for W in combinations([w for w in range(n) if w not in p], 2): m.add_SW(p[0], p[1], list(W))
    print(fam, 'rows', len(m.eq)); sys.stdout.flush()
    for lo, hi in ((3, 4), (2, 5), (1, 7), (0, 11)):
        print(f'   window [{lo},{hi}]:', minlam(m, lambda u, v: lo <= pos[u] <= hi and lo <= pos[v] <= hi)); sys.stdout.flush()
