"""tight.py (mg-afa4): dominance-respecting L on twin-free indecomposable interval orders with exactly one
Brightwell-good pair; print the intervals along L with per-step (A,B) to see where the unique good pair sits."""
import sys
from iolib import *
from brightwell import covers, linexts, dominance_ok
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
shown = 0
for n in range(4, NMAX + 1):
    cnt = 0
    for iv in gen(n):
        if decomposable(iv) or len(set(iv)) < n: continue
        C = covers(iv)
        for L in linexts(iv):
            if not dominance_ok(iv, L): continue
            row = []
            for i in range(n - 1):
                a, b = L[i], L[i + 1]
                if not inc(iv, a, b): row.append('<'); continue
                A = sum(1 for z in range(n) if (a, z) in C and inc(iv, z, b)); B = sum(1 for z in range(n) if (z, b) in C and inc(iv, z, a))
                row.append((A, B))
            good = [x for x in row if x != '<' and sum(x) <= 1]
            if len(good) == 1:
                cnt += 1
                if shown < 14:
                    shown += 1
                    print(f"n={n}: " + "  ".join(f"{iv[L[i]]}" + (f" -{row[i]}- " if i < n - 1 else "") for i in range(n)))
    print(f"n={n}: {cnt} (P,L) with exactly one good pair")
