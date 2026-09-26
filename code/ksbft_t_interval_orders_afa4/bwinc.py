"""bwinc.py (mg-afa4): separator incidences over ALL linear extensions of all interval orders n<=NMAX
(no dominance constraint): max s_up(z), max s_down(z), slack 2m - T, and T <= 2n-4 ?"""
import sys
from collections import Counter
from iolib import *
from brightwell import covers, linexts
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
for n in range(3, NMAX + 1):
    mu = md = 0; slack = Counter(); t2n = 0; ex = None
    for iv in gen(n):
        if all(not inc(iv, a, b) for a in range(n) for b in range(n)): continue
        C = covers(iv)
        for L in linexts(iv):
            su = Counter(); sd = Counter(); T = 0; m = 0
            for i in range(n - 1):
                a, b = L[i], L[i + 1]
                if not inc(iv, a, b): continue
                m += 1
                for z in range(n):
                    if (a, z) in C and inc(iv, z, b): su[z] += 1; T += 1
                    if (z, b) in C and inc(iv, z, a): sd[z] += 1; T += 1
            mu = max(mu, max(su.values(), default=0)); md = max(md, max(sd.values(), default=0))
            slack[2 * m - T] += 1
            if T > 2 * n - 4: t2n += 1
            if max(su.values(), default=0) >= 2 and ex is None: ex = (iv, L, dict(su))
    print(f"n={n}: max s_up={mu} max s_down={md}; slack 2m-T distribution {dict(sorted(slack.items()))}; T>2n-4 on {t2n}"
          + (f"; s_up>=2 e.g. {ex}" if ex else ""))
