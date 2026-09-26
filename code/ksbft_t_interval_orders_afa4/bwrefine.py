"""bwrefine.py (mg-afa4): refined forms of Claim K over all L of all non-chain interval orders n<=NMAX.
K_B: some inc consecutive pair with A=empty and |B|<=1.  K_A: dual.  K_AB: both K_A and K_B hold.
K_0: some inc consecutive pair with |S|=0."""
import sys
from collections import Counter
from iolib import *
from brightwell import covers, linexts
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
for n in range(3, NMAX + 1):
    f = Counter(); ex = {}; tot = 0
    for iv in gen(n):
        if all(not inc(iv, a, b) for a in range(n) for b in range(n)): continue
        C = covers(iv)
        for L in linexts(iv):
            tot += 1; AB = []
            for i in range(n - 1):
                a, b = L[i], L[i + 1]
                if not inc(iv, a, b): continue
                A = sum(1 for z in range(n) if (a, z) in C and inc(iv, z, b))
                B = sum(1 for z in range(n) if (z, b) in C and inc(iv, z, a))
                AB.append((A, B))
            kb = any(A == 0 and B <= 1 for A, B in AB); ka = any(B == 0 and A <= 1 for A, B in AB)
            for k, v in [('K_B', kb), ('K_A', ka), ('K_AB', ka and kb), ('K_0', any(A + B == 0 for A, B in AB)),
                         ('K', any(A + B <= 1 for A, B in AB))]:
                if not v: f[k] += 1; ex.setdefault(k, (iv, L, AB))
    print(f"n={n}: {tot} (P,L); failures " + ", ".join(f"{k}={f[k]}" for k in ['K', 'K_A', 'K_B', 'K_AB', 'K_0']))
    for k in ['K_A', 'K_B', 'K_AB']:
        if k in ex and n >= NMAX - 1: print("    ", k, ex[k])
