"""bwstats.py (mg-afa4): where are the Brightwell-good L-consecutive pairs (<=1 separator), over all
dominance-respecting linear extensions L of indecomposable twin-free interval orders.  Tests hypotheses:
H1 first incomparable consecutive pair is good; H1' last is good; H2 first or last; H3 >= 2 good pairs;
HT Brightwell's count  T = sum |S| <= 2*(#inc consecutive pairs) - 2 ; HC every consecutive pair incomparable."""
import sys
from collections import Counter
from iolib import *
from brightwell import covers, seps, linexts, dominance_ok
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
for n in range(3, NMAX + 1):
    c = Counter(); ex = {}
    for iv in gen(n):
        if decomposable(iv) or len(set(iv)) < n: continue
        C = covers(iv)
        for L in linexts(iv):
            if not dominance_ok(iv, L): continue
            c['L'] += 1
            prs = [(L[i], L[i + 1]) for i in range(n - 1) if inc(iv, L[i], L[i + 1])]
            S = [len(seps(iv, C, a, b)) for a, b in prs]
            good = [s <= 1 for s in S]
            for k, v in [('H1', good[0]), ("H1'", good[-1]), ('H2', good[0] or good[-1]), ('H3', sum(good) >= 2),
                         ('HT', sum(S) <= 2 * len(S) - 2), ('HC', len(prs) == n - 1)]:
                if not v:
                    c[k] += 1; ex.setdefault(k, (iv, L, S))
    print(f"n={n}: {c['L']} (P,L) pairs; failures: " + ", ".join(f"{k}={c[k]}" for k in ['H1', "H1'", 'H2', 'H3', 'HT', 'HC']))
    for k, v in ex.items(): print(f"    {k} e.g. iv={v[0]} L={v[1]} seps={v[2]}")
