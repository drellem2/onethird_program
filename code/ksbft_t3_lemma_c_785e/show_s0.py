"""show_s0.py (mg-785e): print the small S0 (unconditioned Swap Identity) certificate of a survivor in words."""
import sys
from certify import *
from survivors import survivors
S = survivors()
idx = int(sys.argv[1]) if len(sys.argv) > 1 else 7
iv, L, v0 = S[idx]; n = len(iv)
m = MuLP(iv, L); prs = [(u, v) for u in range(n) for v in range(u + 1, n) if inc(iv, u, v)]
m.add_S0(prs)
r = find(m); ok, ratio, Lm, Y = exact_check(m, r[1], r[2])
print('P =', iv); print('L =', [iv[x] for x in L]); print('exact:', ok, ratio)
for (u, v), x in zip(m.inv_pairs(), Lm):
    if x: print(f'  lambda {x}  on inversion P[{iv[v]} before {iv[u]}]')
for (u, v), x in zip(prs, Y):
    if x:
        A, B = seps_typed(iv, m.C, u, v); A2, B2 = seps_typed(iv, m.C, v, u)
        print(f'  y {x}  Swap identity ({iv[u]},{iv[v]}): S={[iv[z] for z in A+B]} ; reverse S={[iv[z] for z in A2+B2]}')
