"""onesided.py (mg-afa4): test T_up <= m and T_down <= m (m = #incomparable L-consecutive pairs), and
candidate injections for up-incidences, over all L of all non-chain interval orders n<=NMAX."""
import sys
from collections import Counter
from iolib import *
from brightwell import covers, linexts, dominance_ok
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
for n in range(3, NMAX + 1):
    c = Counter(); ex = {}
    for iv in gen(n):
        if all(not inc(iv, a, b) for a in range(n) for b in range(n)): continue
        C = covers(iv)
        for L in linexts(iv):
            dom = dominance_ok(iv, L)
            m = Tu = Td = 0
            for i in range(n - 1):
                a, b = L[i], L[i + 1]
                if not inc(iv, a, b): continue
                m += 1
                Tu += sum(1 for z in range(n) if (a, z) in C and inc(iv, z, b))
                Td += sum(1 for z in range(n) if (z, b) in C and inc(iv, z, a))
            for k, v in [('Tu<=m', Tu <= m), ('Td<=m', Td <= m), ('Tu<=m-1', Tu <= m - 1), ('Tu+Td<=2m-1', Tu + Td <= 2 * m - 1)]:
                kk = k + ('/dom' if dom else '/all')
                if not v: c[kk] += 1; ex.setdefault(kk, (iv, L, m, Tu, Td))
            c['N' + ('/dom' if dom else '/all')] += 1
    print(f"n={n}: {dict(sorted(c.items()))}")
    for k, v in ex.items():
        if n == NMAX: print("   ", k, v)
