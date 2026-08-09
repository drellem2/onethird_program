"""s3 — ITEM 4 (the two added steps) and the EXACT completion of ITEM 2.

mg-28ff §2: "Both extra steps are free and both are load-bearing.  Without them the route
below FAILS: with the un-sharpened `2*Delta_P*R(g)` form the constant already exceeds 1 at
n = 5 (6 of 275 primitive posets - b4 R5)."

That cites ONE cell of a 2x2.  The two steps are:
    (S1)  keep  d_i <= Delta_P  where mg-76b2 rounded d_i up to 1
    (S2)  EVALUATE the Cauchy-Schwarz factor, i.e. keep the `-E(h)` that mg-76b2 discarded

giving four bounds on Phi*_pref^2, all of which I write in terms of
    rho = mu_pref/(1-lambda_std) >= 1   and   Delta_P <= 1 :

    V11  both steps      R(2*Delta-R)  ->  c = rho*Delta - rho^2 (1-lambda)/2
    V10  S1 only         2*Delta*R     ->  c = rho*Delta                     <- R5's cell
    V01  S2 only         R(2-R)        ->  c = rho - rho^2 (1-lambda)/2
    V00  neither         2R            ->  c = rho                           <- mg-76b2's own

V00 = rho is EXACTLY 1 iff mu_pref = 1-lambda_std, which IS L2's first disjunct.  So the
un-sharpened sweep applied to a monotone vector certifies C_3 = 1 at PRECISELY the
L2-exhibiting posets and nowhere else: without the two steps the quantifier move buys
NOTHING AT ALL.  That is a stronger statement than "exceeds 1 at n = 5", and this script
measures whether it is true.

EXACTNESS.  mu_pref is bracketed here by bisection on an EXACT COPOSITIVITY test of
Q - t*N over the monotone cone, so BOTH directions are exact.  mg-28ff computes mu_pref by
a float support enumeration and labels its extremal direction a MEASUREMENT (§6, §10);
this script does not need that concession.
"""
import time
from fractions import Fraction as F
from lib29fe import (all_natural_posets, is_decomposable, Poset, bracket_gap,
                     bracket_mu_pref)

ITERS = 34
print("=" * 92)
print("s3  ITEM 4 — the 2x2 counterfactual on the two added steps, EXACT")
print("=" * 92)
print("rho and the four variants are bracketed exactly (copositivity for mu_pref, PSD for")
print("the gap).  A poset is scored FAIL for a variant only when the variant's LOWER")
print("bracket end already exceeds 1, so every failure count below is a LOWER BOUND on the")
print("true count and no failure is an artefact of bracket slack.")
print()

summary = {}
for n in range(2, 7):
    t0 = time.time()
    prim = [r for r in all_natural_posets(n) if not is_decomposable(n, r)]
    cnt = {"V11": 0, "V10": 0, "V01": 0, "V00": 0}
    mx = {"V11": None, "V10": None, "V01": None, "V00": None}
    l2_fail = 0
    for rel in prim:
        P = Poset(n, rel)
        glo, ghi = bracket_gap(P, iters=ITERS)
        mlo, mhi = bracket_mu_pref(P, iters=ITERS)
        D = P.Delta
        # rho bracket: mu/(1-lambda).  low = mlo/ghi, high = mhi/glo
        rlo, rhi = mlo / ghi, mhi / glo
        # L2's first disjunct fails iff rho > 1; score it only when CERTAIN
        if rlo > 1:
            l2_fail += 1
        # variant values.  For a FAIL we need the variant's LOWER bound > 1.
        # V00 = rho ; V10 = rho*Delta ; V01 = rho - rho^2 g/2 ; V11 = rho*Delta - rho^2 g/2
        # rho^2*g/2 is SUBTRACTED, so its UPPER bound (rhi^2 * ghi/2) gives the lower bd.
        sub_hi = rhi * rhi * ghi / 2
        lowb = {"V00": rlo, "V10": rlo * D,
                "V01": rlo - sub_hi, "V11": rlo * D - sub_hi}
        sub_lo = rlo * rlo * glo / 2
        highb = {"V00": rhi, "V10": rhi * D,
                 "V01": rhi - sub_lo, "V11": rhi * D - sub_lo}
        for k in cnt:
            if lowb[k] > 1:
                cnt[k] += 1
            if mx[k] is None or highb[k] > mx[k]:
                mx[k] = highb[k]
    summary[n] = (len(prim), cnt, mx, l2_fail)
    print(f"  n={n} done ({len(prim)} primitive, {time.time()-t0:.1f}s)")

print()
print("-" * 92)
print("TABLE — posets where each variant's constant EXCEEDS 1 (i.e. the route FAILS there)")
print("-" * 92)
print(f"{'n':>3} {'primitive':>10} | {'V11 both':>10} {'V10 S1only':>11} "
      f"{'V01 S2only':>11} {'V00 neither':>12} | {'L2 fails':>9}")
for n in range(2, 7):
    k, cnt, mx, l2f = summary[n]
    print(f"{n:>3} {k:>10} | {cnt['V11']:>10} {cnt['V10']:>11} {cnt['V01']:>11} "
          f"{cnt['V00']:>12} | {l2f:>9}")

print()
print("-" * 92)
print("TABLE — the MAXIMUM constant each variant reaches (upper bracket end)")
print("-" * 92)
print(f"{'n':>3} | {'V11 both':>10} {'V10 S1only':>11} {'V01 S2only':>11} {'V00 neither':>12}")
for n in range(2, 7):
    k, cnt, mx, l2f = summary[n]
    print(f"{n:>3} | {float(mx['V11']):>10.6f} {float(mx['V10']):>11.6f} "
          f"{float(mx['V01']):>11.6f} {float(mx['V00']):>12.6f}")

print()
print("VERDICT ON ITEM 4:")
print(f"  * V10 (mg-28ff's own R5 cell: Delta_P kept, -E(h) discarded) first exceeds 1 at "
      f"n = {min([n for n in range(2,7) if summary[n][1]['V10'] > 0], default=None)}, "
      f"at {summary[5][1]['V10']} of 275 primitive posets at n=5.")
print(f"  * V01 (the UNTESTED cell: -E(h) kept, Delta_P discarded) first exceeds 1 at "
      f"n = {min([n for n in range(2,7) if summary[n][1]['V01'] > 0], default='never n<=6')}.")
print(f"  * V00 (neither step - mg-76b2's own form) first exceeds 1 at "
      f"n = {min([n for n in range(2,7) if summary[n][1]['V00'] > 0], default=None)}, and its")
print(f"    failure count EQUALS the L2-failure count at every n:",
      all(summary[n][1]['V00'] == summary[n][3] for n in range(2, 7)))
print(f"  * V11 (both steps) failures at n<=6:",
      {n: summary[n][1]['V11'] for n in range(2, 7)})
print("=" * 92)
