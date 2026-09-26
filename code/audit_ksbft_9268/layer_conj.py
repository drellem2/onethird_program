#!/usr/bin/env python3
"""layer_conj.py (mg-9268) -- probe of KSBFT-I's CONJECTURE that a poset of
range <= D has at most C(D+1, floor((D+1)/2)) down-sets of any one size.
Exhaustive over all naturally labelled posets on n <= NMAX elements (built
by adding maximal elements, pruning range > D), plus random larger posets.
usage: layer_conj.py NMAX"""
import sys, random
from math import comb
from follow_check import downsets, rand_poset, canonical, masks
NMAX = int(sys.argv[1])
best = {}
def rng_ok(dm, D):
    n = len(dm)
    return all(n - 1 - bin(dm[x]).count("1") - sum(1 for y in range(n) if dm[y] >> x & 1) <= D for x in range(n))
def rec(dm, D):
    n = len(dm)
    if n:
        m = max(len(L) for L in downsets(dm, n))
        if m > best.get((D, 'ex'), (0,))[0]: best[(D, 'ex')] = (m, list(dm))
    if n == NMAX: return
    for msk in range(1 << n):
        if all(dm[i] & ~msk == 0 for i in range(n) if msk >> i & 1):
            ndm = dm + [msk]
            if rng_ok(ndm, D): rec(ndm, D)
for D in tuple(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 else (2, 3):
    rec([], D)
    print(f"D={D} exhaustive n<={NMAX}: max same-size down-sets {best[(D,'ex')][0]}  bound C(D+1,floor) = {comb(D+1,(D+1)//2)}  witness {best[(D,'ex')][1]}")
r = random.Random(5)
for D in range(2, 8):
    m = 0
    for _ in range(3000):
        b = rand_poset(r.randint(D + 1, 26), D, r)
        if b is None: continue
        dm = masks(b, canonical(b)); m = max(m, max(len(L) for L in downsets(dm, len(dm))))
    print(f"D={D} random (3000 draws, n<=26): max {m}  bound {comb(D+1,(D+1)//2)}")
