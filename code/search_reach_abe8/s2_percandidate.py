"""s2 -- WHAT ONE CANDIDATE COSTS, measured and then extrapolated.

Every "posets per second" estimate of this problem silently assumes the per-
candidate cost is constant in n.  It is not: rejecting a poset means certifying
delta(P) >= 1/3, which means counting linear extensions, which is #P-complete
(Brightwell-Winkler 1991 -- recalled, not verified here).  The corpus's method,
and the only exact one available, is the down-set DP at cost Theta(#ideals * n).

This script measures three things:

  A. the wall-clock cost of the exact delta test in THIS implementation, n <= 9;
  B. the cost of the CHEAPEST correct rejection -- stop at the first balanced
     pair rather than computing delta -- and how much it actually saves;
  C. #ideals for a Kleitman-Rothschild-typical poset at n = 12..40, which is the
     per-candidate cost of the exact test at sizes no enumeration will reach.

Single process, one core.
"""

import random
import statistics
import sys
import time
from fractions import Fraction

import libabe8 as L

T0 = time.time()
THIRD = Fraction(1, 3)

print("=" * 78)
print("s2  WHAT ONE CANDIDATE COSTS  (mg-abe8)")
print("=" * 78)
print()

# ---------------------------------------------------------------------------
print("-" * 78)
print("A.  MEASURED wall-clock of the EXACT delta test, this implementation")
print("-" * 78)
print("Python 3, one core, exact Fraction arithmetic.  These are the calibration")
print("numbers for the cost model in s4; the C-speedup assumed there is stated")
print("there and is NOT measured here.")
print()

cur = L.all_posets_bruteforce(1)
pops = {1: cur}
for n in range(2, 10):
    cur = L.all_posets_by_extension(n, cur)
    pops[n] = cur

print("  n |  sample |  s / candidate |  candidates / s |  #ideals (mean)")
print("-" * 68)
percand = {}
rng = random.Random(20260807)
for n in range(4, 10):
    pop = pops[n]
    sample = pop if len(pop) <= 400 else rng.sample(pop, 400)
    t = time.time()
    ideals = 0
    for P in sample:
        L.delta(P)
        ideals += len(L.order_ideal_masks(P))
    dt = (time.time() - t) / len(sample)
    percand[n] = dt
    print("%3d | %7d | %14.3e | %15.1f | %15.1f"
          % (n, len(sample), dt, 1.0 / dt, ideals / len(sample)))
    sys.stdout.flush()

ratios = [percand[n] / percand[n - 1] for n in range(5, 10)]
print()
print("per-candidate cost multiplier per element: %s   (mean %.2f)"
      % (", ".join("%.2f" % r for r in ratios), statistics.mean(ratios)))
print("=> the per-candidate cost is itself EXPONENTIAL in n.  A model that holds")
print("   it constant understates the total by this factor per element.")

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("B.  THE CHEAPEST CORRECT REJECTION, and what it buys")
print("-" * 78)
print("""To reject P we need ONE incomparable pair with 1/3 <= p <= 2/3, not delta.
The restriction DP is shared, so the saving is only in the pair loop.  Measured
below: mean number of pairs examined before a balanced one is found, against the
number of incomparable pairs available.""")
print()
print("  n |  mean incomparable pairs |  mean pairs tried |  saving factor")
print("-" * 66)
for n in range(4, 10):
    pop = pops[n]
    sample = pop if len(pop) <= 600 else rng.sample(pop, 600)
    tot_pairs = 0
    tot_tried = 0
    m = 0
    for P in sample:
        pairs = P.incomparable_pairs()
        if not pairs:
            continue
        m += 1
        tot_pairs += len(pairs)
        e = L.restriction_counts(P)
        total = e[(1 << P.n) - 1]
        before = L.pair_before_counts(P, e)
        tried = 0
        for (x, y) in pairs:
            tried += 1
            p = Fraction(before[(x, y)], total)
            if min(p, 1 - p) >= THIRD:
                break
        tot_tried += tried
    print("%3d | %24.2f | %17.2f | %14.2fx"
          % (n, tot_pairs / m, tot_tried / m, tot_pairs / tot_tried))
    sys.stdout.flush()

print()
print("=> early exit saves a CONSTANT factor of a few.  It does not touch the")
print("   exponential: the DP that produces the marginals is the cost, and it is")
print("   Theta(#ideals * n) whether one pair is examined or all of them.")

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("C.  #IDEALS FOR A KR-TYPICAL POSET, n = 12..40")
print("-" * 78)
print("""Kleitman-Rothschild: almost every finite poset has three levels, |L1| ~ |L3|
~ n/4 and |L2| ~ n/2, with L1 < L3 entirely.  A MODEL, not the uniform measure --
every figure below is labelled KR-model and is directional.  The middle layer is
an antichain of size ~n/2, so #ideals >= 2^(n/2) unconditionally.""")
print()
print("   n |  (l1,l2,l3) |   mean #ideals |   log2 |  2^(n/2) lower bound")
print("-" * 74)
rng2 = random.Random(4242)
for n in list(range(12, 41, 4)):
    l1, l2, l3 = L.kr_layer_sizes(n)
    vals = [L.kr_ideal_count(L.kr_sample(n, rng2), l1, l2, l3) for _ in range(20)]
    mean = sum(vals) / len(vals)
    import math
    print("%4d | %11s | %14.4g | %6.2f | %20.4g"
          % (n, "(%d,%d,%d)" % (l1, l2, l3), mean, math.log2(mean), 2 ** (n / 2)))
    sys.stdout.flush()

print()
print("=> per-candidate cost at n = 34 is ~2^17 DP cells, ~10^5 operations, against")
print("   ~10^2 at n = 9.  Three orders of magnitude that a posets-per-second")
print("   estimate drops on the floor.  s4 carries it explicitly.")
print()
print("total wall %7.1fs, one core" % (time.time() - T0))
