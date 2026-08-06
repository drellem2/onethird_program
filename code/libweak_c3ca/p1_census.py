"""P1 — the empirical shadow of (LIB-weak): what do the MOST-frozen posets we
can reach actually do to E[inv_e]/n^2?

(LIB-weak) is a statement about frozen posets (delta < 1/3), a class the
1/3-2/3 conjecture says is EMPTY.  It therefore cannot be tested directly.
The nearest testable thing is the CRITICAL family: the posets that attain the
minimum of delta, which for every n verified so far is exactly 1/3.  If
E_maj/n^2 stays bounded away from 0 on that family as n grows, then
(LIB-weak) — if true — must be DISCONTINUOUS at delta = 1/3, because it is
false in the limit from above.  If it decays, (LIB-weak) looks like the
continuation of a trend.

POPULATION: every naturally labelled poset on n elements, n = 3..6
             (= every transitively closed subset of {(i,j) : i<j}).
             Isomorphism classes are counted once per compatible labelling.
GRAIN:       one naturally labelled poset.
QUANTITY:    E_maj = sum over incomparable pairs of min(p, 1-p), which equals
             E[inv_e] whenever the majority order is a linear order, and is a
             lower bound on E[inv_r] for EVERY reference order r otherwise.
"""

import sys
from collections import defaultdict

from lib_c3ca import delta_and_emaj, naturally_labelled_posets

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
EPS = 1e-12

print("P1 census — POPULATION: all naturally labelled posets on n elements;")
print("            GRAIN: one naturally labelled poset (iso classes repeat).")
print()

for n in range(3, NMAX + 1):
    seen = 0
    chains = 0
    best_delta = 1.0
    # max E_maj/n^2 within each delta band
    crit_best = (-1.0, None)      # among delta == min delta (i.e. == 1/3)
    all_best = (-1.0, None)
    band = defaultdict(lambda: -1.0)
    frozen_found = []
    for pairs in naturally_labelled_posets(n):
        seen += 1
        delta, emaj, m = delta_and_emaj(n, pairs)
        if delta is None:
            chains += 1
            continue
        if delta < best_delta - EPS:
            best_delta = delta
        if delta < 1 / 3 - EPS:
            frozen_found.append((sorted(pairs), delta, emaj))
        r = emaj / (n * n)
        if r > all_best[0]:
            all_best = (r, (sorted(pairs), delta, emaj, m))
        b = round(delta, 6)
        if r > band[b]:
            band[b] = r
    # second pass for the critical family, now that best_delta is known
    for pairs in naturally_labelled_posets(n):
        delta, emaj, m = delta_and_emaj(n, pairs)
        if delta is None:
            continue
        if abs(delta - best_delta) < EPS:
            r = emaj / (n * n)
            if r > crit_best[0]:
                crit_best = (r, (sorted(pairs), delta, emaj, m))

    print(f"n = {n}:  {seen} naturally labelled posets ({chains} chains, delta undefined)")
    print(f"  min delta over the population        : {best_delta:.9f}"
          f"   ({'== 1/3 exactly' if abs(best_delta - 1/3) < 1e-9 else 'NOT 1/3'})")
    print(f"  frozen posets found (delta < 1/3)    : {len(frozen_found)}"
          "   [the conjecture predicts 0; a nonzero count here would be a"
          " counterexample, not a bug to hide]")
    r, info = crit_best
    pr, pdelta, pemaj, pm = info
    print(f"  CRITICAL family (delta = min): max E_maj/n^2 = {r:.6f}"
          f"   (E_maj = {pemaj:.6f}, {pm} incomparable pairs)")
    print(f"    witness relation set: {pr}")
    r, info = all_best
    pr, pdelta, pemaj, pm = info
    print(f"  whole population:    max E_maj/n^2 = {r:.6f} at delta = {pdelta:.6f}"
          f"  ({'antichain' if pm == n*(n-1)//2 else 'not the antichain'})")
    print(f"  E_maj/n^2 by delta band (max within band):")
    for b in sorted(band):
        print(f"    delta = {b:.6f} : {band[b]:.6f}")
    print()
