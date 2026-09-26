"""EMPIRICAL: the per-chain counts N_C(x) for chains C that could sit in a MINIMUM chain
partition of Pi(x) (C subset of Pi(x), width(Pi(x) - C) = width(Pi(x)) - 1).
Is there always SOME such C with N_C(x) log-concave?  Is every such N_C(x) log-concave?"""
import random, itertools
from lib import *
from lc_chain_probe import rand_poset, dist, is_unimodal

def width_of(P, mask):
    el = [i for i in range(P.n) if (mask >> i) & 1]
    best = 0
    for r in range(len(el), 0, -1):
        for comb in itertools.combinations(el, r):
            if all(not P.comparable(a, b) for a, b in itertools.combinations(comb, 2)):
                return r
    return 0

rng = random.Random(53712)
st = dict(pairs=0, fail_lc=0, fail_uni=0, x_with_no_lc_chain=0, xs=0)
ex = None
for t in range(300):
    n = rng.randint(5, 9)
    P = rand_poset(n, rng.choice([0.15, 0.25, 0.35]), rng)
    for x in range(n):
        Pi = sum(1 << y for y in range(n) if y != x and not P.comparable(x, y))
        wPi = width_of(P, Pi)
        if wPi < 2: continue
        st['xs'] += 1
        el = [y for y in range(n) if (Pi >> y) & 1]
        any_lc = False
        for r in range(1, len(el) + 1):
            for comb in itertools.combinations(el, r):
                if not all(P.comparable(a, b) for a, b in itertools.combinations(comb, 2)): continue
                M = sum(1 << y for y in comb)
                if width_of(P, Pi & ~M) != wPi - 1: continue
                st['pairs'] += 1
                d = dist(P, x, M)
                if is_logconcave(d): any_lc = True
                else:
                    st['fail_lc'] += 1
                    if not is_unimodal(d):
                        st['fail_uni'] += 1
                        if ex is None: ex = (n, P.below, x, M, d)
        if not any_lc: st['x_with_no_lc_chain'] += 1
print(st)
print("first non-unimodal Dilworth-chain example:", ex)
