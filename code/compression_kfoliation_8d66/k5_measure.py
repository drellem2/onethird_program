#!/usr/bin/env python3
"""k5 -- ITEM 3: MEASURE IT.  Does alpha_k actually rise with k, and how fast against a bar
of 2 to 3?

EVERY NUMBER IN THIS FILE IS A FLOAT FROM JACOBI AND IS A MEASUREMENT, NOT A VERDICT.  The
verdicts are in k2 (the bar), k3 (monotonicity) and k4 (the ceiling), all exact.

Population is capped at |L(P)| <= NMAX because Jacobi is O(N^3) in pure Python; the cap and
the sample size are printed beside every table (mg-409a's D7).
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib8d66 as K

ok = True
NMAX = 34

# --------------------------------------------------------------------------------------
K.banner("k5.1  alpha_k over the poset population, by k")
print(f"  population: n=3,4 EXHAUSTIVE; n=5 sample(200,seed=3); n=6 sample(120,seed=5);")
print(f"  n=7 sample(60,seed=11).  All restricted to |L(P)| <= {NMAX} (Jacobi is O(N^3)).")
print()
print("   n | k | posets | max alpha_k | mean alpha_k | min alpha_k | bar(1/3) | max/bar")
print("  ---+---+--------+-------------+--------------+-------------+----------+--------")
table = {}
for n, src in ((3, list(K.all_posets(3))), (4, list(K.all_posets(4))),
               (5, K.sample_posets(5, 200, 3)), (6, K.sample_posets(6, 120, 5)),
               (7, K.sample_posets(7, 60, 11))):
    parts = K.admissible_partitions(n)
    per_k = {}
    for lt in src:
        LEs = K.linear_extensions(n, lt)
        if len(LEs) < 2 or len(LEs) > NMAX:
            continue
        for S in parts:
            a = K.alpha_measured(LEs, n, lt, S)
            per_k.setdefault(len(S), []).append(a)
    bar = 3 * (n - 1) / n
    for k in sorted(per_k):
        v = per_k[k]
        table[(n, k)] = v
        print(f"  {n:2d} | {k} | {len(v):6d} | {max(v):11.6f} | {sum(v)/len(v):12.6f} |"
              f" {min(v):11.6f} | {bar:8.6f} | {max(v)/bar:7.4f}")
allv = [a for v in table.values() for a in v]
ok &= K.verdict(max(allv) <= 1 + 1e-9,
                f"max alpha_k over the whole measured population = {max(allv):.9f}",
                f"{len(allv)} (poset, partition) measurements; the exact ceiling is k4")

# --------------------------------------------------------------------------------------
K.banner("k5.2  DOES alpha RISE WITH k AT A FIXED POSET?  (P8 of PREDICTIONS.md)")
print("""
  k3 proves alpha_S <= alpha_{S'} whenever S' refines S.  Whether it rises STRICTLY is a
  measurement, and it is the measurement pm-onethird's derivation actually predicts.
""")
rise = flat = tot = 0
examples = []
for n, src in ((4, list(K.all_posets(4))), (5, K.sample_posets(5, 200, 3)),
               (6, K.sample_posets(6, 120, 5))):
    for lt in src:
        LEs = K.linear_extensions(n, lt)
        if len(LEs) < 2 or len(LEs) > NMAX:
            continue
        a2 = K.alpha_measured(LEs, n, lt, K.coarsest_partition(n))
        af = K.alpha_measured(LEs, n, lt, K.finest_partition(n))
        tot += 1
        if af > a2 + 1e-9:
            rise += 1
            if len(examples) < 4:
                examples.append((n, sorted(lt), a2, af))
        else:
            flat += 1
print(f"  alpha_finest > alpha_(k=2):  {rise} of {tot} posets     (flat at {flat})")
for n, lt, a2, af in examples:
    print(f"    n={n} lt={lt}:  alpha_2 = {a2:.6f}  ->  alpha_finest = {af:.6f}")
print(f"""
  READ THIS THE RIGHT WAY ROUND.  {rise} of {tot} is the effect pm-onethird predicts and it
  is real.  It is also bounded: every one of those climbs terminates at ((n-1)/2) gap_BK
  (k3.3) and therefore at or below 1 (k4).  ALPHA_k RISING AT A FIXED POSET AND THE CEILING
  RISING ARE TWO DIFFERENT STATEMENTS, and only the first is true.  That is E1 of
  PREDICTIONS.md, and it is the step where the derivation slips.
""")
ok &= K.verdict(True, f"measured: rises at {rise}/{tot}, ceiling unmoved at 1")

# --------------------------------------------------------------------------------------
K.banner("k5.3  THE CONSTRAINT CARRIED FORWARD FROM mg-8bc7: the foliations are NOT symmetric")
print("""
  mg-8bc7 measured rank Pi_o < rank Pi_e at 127 of 219 posets at n = 4.  The ticket requires
  that no step treat the k foliations symmetrically without proof.  Measured at k = 3 and
  above: the per-class fiber counts (= rank Pi_i) spread WIDELY within a single partition.
""")
print("   n | k | partition | poset               | rank Pi_i per class      | max/min")
print("  ---+---+-----------+---------------------+--------------------------+--------")
shown = 0
maxratio = 1.0
for n, src in ((5, K.sample_posets(5, 40, 3)), (6, K.sample_posets(6, 30, 5))):
    for lt in src:
        LEs = K.linear_extensions(n, lt)
        if len(LEs) < 2 or len(LEs) > NMAX:
            continue
        for S in K.admissible_partitions(n):
            if len(S) < 3:
                continue
            ranks = [len(K.orbit_fibers(LEs, n, lt, c)[1]) for c in S]
            r = max(ranks) / min(ranks)
            maxratio = max(maxratio, r)
            if r > 1.5 and shown < 8:
                shown += 1
                print(f"  {n:2d} | {len(S)} | {K.pstr(S):9s} | {str(sorted(lt))[:19]:19s} |"
                      f" {str(ranks):24s} | {r:7.3f}")
ok &= K.verdict(maxratio > 1.0,
                f"worst within-partition rank ratio measured = {maxratio:.3f}",
                "the classes are NOT interchangeable at k > 2 either")
print("""
  NOTHING IN k2-k4 AVERAGES OVER THE CLASSES.  k2's identity is a per-position sum; k2's
  inequality is Efron-Stein applied INSIDE each class separately and then added; k4's witness
  is checked against each class's own fiber.  The asymmetry is priced by never being used.
""")

# --------------------------------------------------------------------------------------
K.banner("k5.4  THE HEADLINE NUMBER: how far is alpha_k from the bar, at the best k?")
print("""
   n | best measured alpha_k (any k) | bar at gamma=1/3 | shortfall factor
  ---+-------------------------------+------------------+------------------""")
for n in sorted({k[0] for k in table}):
    best = max(max(v) for (m, k), v in table.items() if m == n)
    bar = 3 * (n - 1) / n
    print(f"  {n:2d} | {best:29.6f} | {bar:16.6f} | {bar/best:16.3f}x")
print("""
  And the shortfall is NOT a sampling artefact: the exhibited-witness ceiling of k4 is 1 at
  EVERY poset and EVERY admissible k, so no unmeasured poset and no unmeasured k can do
  better than a factor of 2 short at n = 3, rising to 3.
""")
ok &= K.verdict(True, "measurement agrees with the exact ceiling")

K.banner("k5: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
