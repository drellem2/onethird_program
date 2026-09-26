#!/usr/bin/env python3
"""exhaustive_follow.py (mg-9268) -- EXHAUSTIVE completeness probe of the
search generator.  Every naturally labelled poset on n <= NMAX elements with
range <= D is built (add a maximal element, prune range > D), the
ordinal-indecomposable ones are put in canonical order HERE, deduplicated,
and walked through `aud D 58 follow`; each outcome is verified from scratch
as in follow_check.py (MISSED or CUT on an indecomposable poset = failure).
Independent of iso-class machinery: every labelled poset is tested.
usage: exhaustive_follow.py AUD D NMAX"""
import sys
from follow_check import verify, canonical, indecomposable
aud, D, NMAX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
seen = set(); polys = []; labelled = 0
def inc_ok(dm):
    n = len(dm)
    return all(n - 1 - bin(dm[x]).count("1") - sum(1 for y in range(n) if dm[y] >> x & 1) <= D for x in range(n))
def rec(dm):
    global labelled
    n = len(dm)
    if n >= 2:
        below = [{i for i in range(n) if dm[x] >> i & 1} for x in range(n)]
        order = canonical(below)
        if indecomposable(below, order):
            labelled += 1
            pos = {x: i for i, x in enumerate(order)}
            key = tuple(sum(1 << pos[y] for y in below[x]) for x in order)
            if key not in seen:
                seen.add(key); polys.append(list(key))
    if n == NMAX: return
    for m in range(1 << n):
        if all(dm[i] & ~m == 0 for i in range(n) if m >> i & 1):
            nd = dm + [m]
            if inc_ok(nd): rec(nd)
rec([])
verify(aud, D, polys, [], f"D={D} EXHAUSTIVE n<={NMAX}: {labelled} labelled indecomposable posets -> {len(polys)} canonical forms")
