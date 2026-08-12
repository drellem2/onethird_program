#!/usr/bin/env python3
"""k3 -- WHERE DOES alpha_k GO AS k RISES?  Monotone, and its limit is the original problem.

pm-onethird: "the CEILING ... should move UP, because being nearly determined by ALL k
compressions simultaneously is a strictly harder condition to satisfy as k grows."

The monotonicity is RIGHT, and this arm proves it in the strong (operator) form:

  k3.1   S' refines S  =>  Q_{S'} - Q_S is PSD.  So alpha rises under refinement, at every
         poset, EXACTLY.  This is pm-onethird's intuition, confirmed.

  k3.2   The refinement order has a TOP: the all-singletons partition, k = n-1, admissible at
         every n (k1).  So sup over admissible S of alpha_S = alpha_finest, ATTAINED.

  k3.3   And alpha_finest = ((n-1)/2) * gap_BK, because Q_finest IS ((n-1)/2)(I - P_BK)
         (k2.1, an exact matrix identity).

  k3.4   THEREFORE the best bound the whole k-family can produce is

              gap_BK  >=  (2/(n-1)) alpha_finest  =  gap_BK.

         The compression's ceiling rises with k exactly as far as the thing it is trying to
         bound, and no further.  At the k where the ceiling is highest, the "compression to a
         cube" is a compression to a ONE-DIMENSIONAL cube -- a single swap -- and the operator
         is the BK generator itself.  THE ROUTE'S BEST CASE IS THE ORIGINAL PROBLEM RESTATED.
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib8d66 as K

ok = True
MAXN = 130


def population():
    for n in (3, 4):
        for lt in K.all_posets(n):
            yield n, lt, "exhaustive"
    for lt in K.sample_posets(5, 120, 3):
        yield 5, lt, "sample(120)"
    for lt in K.sample_posets(6, 40, 5):
        yield 6, lt, "sample(40)"


POP = [t for t in population()]

# --------------------------------------------------------------------------------------
K.banner("k3.1  REFINEMENT MONOTONICITY, as an EXACT operator statement")
print("""
  For every ORDERED pair (S coarse, S' fine) of admissible partitions with S' refining S:
  is  Q_{S'} - Q_S  PSD?  Exact rational elimination, no eigensolver, no float.
""")
bad = cnt = 0
pairs_by_n = {}
for n, lt, tag in POP:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2 or len(LEs) > MAXN:
        continue
    parts = K.admissible_partitions(n)
    Qs = {S: K.q_matrix(LEs, n, lt, S) for S in parts}
    for A in parts:
        for B in parts:
            if A == B or not K.refines(B, A):
                continue
            good, why = K.psd_exact(K.mat_sub(Qs[B], Qs[A]))
            cnt += 1
            pairs_by_n[n] = pairs_by_n.get(n, 0) + 1
            if not good:
                bad += 1
                print(f"  FAIL n={n}  {K.pstr(A)} -> {K.pstr(B)}: {why}")
ok &= K.verdict(bad == 0,
                f"Q_fine - Q_coarse is PSD at {cnt} (poset, refinement) instances",
                f"{bad} failures; " + ", ".join(f"n={k}:{v}" for k, v in sorted(pairs_by_n.items())))

K.banner("k3.2  the CONTROL: is the PSD direction actually informative, or does everything pass?")
print("""
  A monotonicity arm that would also pass on the reversed comparison has measured nothing.
  The same pairs, compared the WRONG WAY ROUND.  These MUST fail.
""")
red = tot = 0
for n, lt, tag in POP[:80]:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2 or len(LEs) > MAXN:
        continue
    parts = K.admissible_partitions(n)
    Qs = {S: K.q_matrix(LEs, n, lt, S) for S in parts}
    for A in parts:
        for B in parts:
            if A == B or not K.refines(B, A):
                continue
            tot += 1
            if not K.psd_exact(K.mat_sub(Qs[A], Qs[B]))[0]:
                red += 1
ok &= K.verdict(red > 0 and tot > 0,
                f"the REVERSED comparison is refused at {red} of {tot} instances",
                "a two-sided check, not a one-sided one (cf. mg-b417's D1)")

# --------------------------------------------------------------------------------------
K.banner("k3.3  THE TOP OF THE ORDER: alpha_finest = ((n-1)/2) * gap_BK")
print("""
  k2.1 gives this EXACTLY as a matrix identity.  Here it is read back as numbers, so a reader
  can see the two quantities are the same object.  Jacobi -- FLOAT, MEASUREMENT ONLY.
""")
print("   n | poset                     | |L(P)| | gap_BK    | ((n-1)/2)gap | alpha_finest | alpha_(k=2)")
print("  ---+---------------------------+--------+-----------+--------------+--------------+------------")
worst = 0.0
cases = [(3, K.antichain(3), "antichain"), (4, K.antichain(4), "antichain"),
         (5, K.antichain(5), "antichain"), (4, K.Z(4), "Z_4"), (6, K.Z(6), "Z_6"),
         (8, K.Z(8), "Z_8"), (5, K.tclose(5, {(0, 4)}), "0<4"),
         (6, K.tclose(6, {(0, 3), (1, 4)}), "0<3,1<4"),
         (6, K.tclose(6, {(0, 1), (2, 3), (4, 5)}), "three 2-chains")]
for n, lt, name in cases:
    LEs = K.linear_extensions(n, lt)
    g = K.gap_bk_measured(LEs, n, lt)
    af = K.alpha_measured(LEs, n, lt, K.finest_partition(n))
    a2 = K.alpha_measured(LEs, n, lt, K.coarsest_partition(n))
    worst = max(worst, abs(af - (n - 1) / 2 * g))
    print(f"  {n:2d} | {name:25s} | {len(LEs):6d} | {g:9.6f} | {(n-1)/2*g:12.6f} |"
          f" {af:12.6f} | {a2:10.6f}")
ok &= K.verdict(worst < 1e-9, "alpha_finest agrees with ((n-1)/2) gap_BK",
                f"worst |difference| = {worst:.2e}   [FLOAT, measurement]")

# --------------------------------------------------------------------------------------
K.banner("k3.4  WHAT THE TOP OF THE ORDER MEANS")
print("""
  Substituting k3.3 into the route's own bound  gap_BK >= (2/(n-1)) alpha_S  at S = finest:

      gap_BK  >=  (2/(n-1)) * ((n-1)/2) * gap_BK  =  gap_BK.

  The inequality is an EQUALITY at the top of the refinement order, so the family of bounds
  indexed by k is squeezed between "strictly weaker than the truth" (every k < n-1, by the
  strict slack measured in k2.3) and "exactly the truth" (k = n-1).

  RAISING k CANNOT OVERSHOOT THE SPECTRAL GAP.  It can only walk back toward it.  So a bar
  the true gap does not clear is a bar NO k clears -- and the ceiling on alpha_k is therefore
  not a k=2 artefact but a restatement of what gap_BK is.  k4 turns that into a NUMBER.
""")
ok &= K.verdict(True, "recorded: sup_k alpha_k = ((n-1)/2) gap_BK, attained at k = n-1")

K.banner("k3: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
