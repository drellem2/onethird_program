#!/usr/bin/env python3
"""mg-de37: does tau (min cross vertex cover at a prefix cut of the natural labelling) ever exceed
the range D?  Exhaustive over naturally labelled posets on n = NMAX elements (every (P, e) up to iso).
Reuses the enumerator of indep_de37.py.  Also asks the finer question tau > max over matched a of pi(a)."""
import sys
from indep_de37 import posets, rng, inc, mincover
n = int(sys.argv[1])
worst = {}; gt = 0; tot = 0; ex = None
for rel in posets(n):
    D = rng(n, rel)
    if D == 0: continue
    for k in range(1, n):
        edges = [(a, b) for a in range(k) for b in range(k, n) if inc(rel, a, b)]
        tau = mincover(None, None, edges); tot += 1
        if tau > worst.get(D, 0): worst[D] = tau
        if tau > D:
            gt += 1
            if ex is None: ex = (sorted(rel), k, D, tau)
print(f"n={n}: posets={len(posets(n)) if n<=7 else '-'} cuts={tot} max tau per D={dict(sorted(worst.items()))} cuts with tau>D: {gt} first example: {ex}")
