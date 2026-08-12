#!/usr/bin/env python3
"""mg-7564 d2 — DOES THE RELAXATION SURVIVE `n`?

`mg-9461` priced the chain question at `10x` using the measured `C_3^gap` values available
to it — `1.500, 1.473, 1.990, 2.386` at `n = 3..6`, EVERY ONE OF THEM OUT OF REGIME (0 of
4376 primitive posets at `n <= 6` has gap <= 1/50, mg-76b2 §7).

`mg-00b3` §0.4 then measured the SAME constant IN REGIME, on the staircase `S_n`.  Nothing
has carried those numbers back into the demand ladder.  This script does that, and only
that.

⚠️ EVERY INPUT HERE IS CITED, NOT MEASURED.  No poset is enumerated in this directory.
"""

from fractions import Fraction as F

import lib7564 as L

Lk = L.EPS_LEAK
ARCH = L.dem_III(Lk, F(1))          # 1/50 — the architecture's own demand


def dec(x, p=6):
    return f"{float(x):.{p}f}"


print("=" * 78)
print("mg-7564 d2 — DOES THE RELAXATION SURVIVE n?")
print("=" * 78)
print(f"Baseline: the architecture as written demands eps_spec <= {ARCH.v} "
      f"({dec(ARCH.v)}), wall {dec(L.wall(ARCH), 2)}x.")
print("A RELAXATION IS A ROW WITH eps_dem > 1/50.  A row at or below 1/50 is not a")
print("relaxation at all — it is the same demand or a tighter one.")

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("A. CHAIN (II), THE GAP-FORM — eps_dem = eps_leak / C_3^gap")
print("-" * 78)
print("   Chain (II) needs a UNIVERSAL C_3^gap over the class {gap <= eps_spec}")
print("   (mg-00b3 §0.5: its bound is RELATIVE).  So the worst row governs.")
print()
print(f"{'source':28} {'n':>3} {'in regime':>9} {'C_3^gap':>9} {'eps_dem':>10} "
      f"{'d*qbar <=':>11} {'wall':>7}  vs 1/50")
for n, g in L.C3GAP_MEASURED:
    e = L.dem_II(Lk, F(g).limit_denominator(10 ** 6))
    verdict = "RELAXES" if e.v > ARCH.v else "no gain"
    print(f"{'mg-94c3 §3 (L2 1st disj)':28} {n:>3} {'no':>9} {g:>9.4f} "
          f"{dec(e.v):>10} {dec(L.dq_from_spec(e), 8):>11} {dec(L.wall(e), 2):>7}  {verdict}")
print()
for n, minq, gap, inreg, g, c in L.STAIRCASE:
    e = L.dem_II(Lk, F(g).limit_denominator(10 ** 6))
    verdict = "RELAXES" if e.v > ARCH.v else "**NO GAIN — WORSE THAN THE BASELINE**"
    print(f"{'mg-00b3 §0.4 staircase S_n':28} {n:>3} {('YES' if inreg else 'no'):>9} "
          f"{g:>9.4f} {dec(e.v):>10} {dec(L.dq_from_spec(e), 8):>11} "
          f"{dec(L.wall(e), 2):>7}  {verdict}")

cross = L.dem_II(Lk, F(10))
print()
print(f"   CHAIN (II) MEETS THE BASELINE AT C_3^gap = 10 EXACTLY "
      f"(eps_dem = {cross.v}), and")
print("   `S_25` is PRIMITIVE, has gap 300/6773 = 0.0043572625 <= 1/50 — INSIDE the")
print("   budget — and forces C_3^gap >= 10.1654.  So on the class chain (II) is")
print("   invoked over, the universal g it needs is ALREADY above the crossing point,")
print("   by one exact in-regime witness (mg-00b3 §0.4 item 4, §0.5).")
print()
print("   ==> CHAIN (II) IS NOT A DEMAND RELAXATION.  Its 10x is the C_3^gap = 1")
print("       extreme point, which mg-94c3 measured FALSE at 1023 of 1032.")

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("B. CHAIN (IV), LITERAL PREFIX CAPTURE — eps_dem = 1 - (1-eps_leak)/c")
print("-" * 78)
print("   Chain (IV)'s condition is ABSOLUTE and per-poset (mg-00b3 §0.5), so `S_25`")
print("   does NOT kill it: there c = 0.9598890 > 40/49 and min_k Q_k = 300/6773 <=")
print("   1/5 with 4.5x to spare.  The governing number is instead the WORST c over")
print("   the class — and the worst c MEASURED IN REGIME is the staircase's at n=12.")
print()
print(f"{'source':28} {'n':>3} {'in regime':>9} {'c':>10} {'eps_dem':>10} "
      f"{'d*qbar <=':>11} {'wall':>7}  vs 1/50")
for n, c in [(16, 0.9999)]:   # mg-81ff §5 — N(16), its one in-regime family
    e = L.dem_IV(Lk, F(c).limit_denominator(10 ** 7))
    print(f"{'mg-81ff §5 N-family':28} {n:>3} {'YES':>9} {c:>10.7f} {dec(e.v):>10} "
          f"{dec(L.dq_from_spec(e), 8):>11} {dec(L.wall(e), 2):>7}  RELAXES")
for n, minq, gap, inreg, g, c in L.STAIRCASE:
    e = L.dem_IV(Lk, F(c).limit_denominator(10 ** 7))
    verdict = "RELAXES" if e.v > ARCH.v else "no gain"
    print(f"{'mg-00b3 §0.4 staircase S_n':28} {n:>3} {('YES' if inreg else 'no'):>9} "
          f"{c:>10.7f} {dec(e.v):>10} {dec(L.dq_from_spec(e), 8):>11} "
          f"{dec(L.wall(e), 2):>7}  {verdict}")

worst_c = min(c for n, _, _, inreg, _, c in L.STAIRCASE if inreg)
e_worst = L.dem_IV(Lk, F(worst_c).limit_denominator(10 ** 7))
e_ceil = L.dem_IV(Lk, F(1))
print()
print(f"   WORST c MEASURED IN REGIME: {worst_c} (S_12).")
print(f"     eps_dem = {dec(e_worst.v)}   d*qbar <= {dec(L.dq_from_spec(e_worst), 8)} "
      f"= 1 in {float(1 / L.dq_from_spec(e_worst)):.4g}")
print(f"     wall {dec(L.wall(e_worst), 2)}x, against the baseline's "
      f"{dec(L.wall(ARCH), 2)}x — a relaxation of "
      f"{dec(e_worst.v / ARCH.v, 2)}x, not 10x.")
print(f"   CEILING, c -> 1: eps_dem = {e_ceil.v} = {dec(e_ceil.v)}, "
      f"d*qbar <= {L.dq_from_spec(e_ceil)} = 1 in 15, wall {dec(L.wall(e_ceil), 2)}x.")
print()
print("   ⚠️ THE WORST-c ROW IS A MEASUREMENT OVER A POPULATION OF THREE FAMILIES, NOT")
print("      A BOUND.  The class {gap <= 1/50} is NON-EMPTY BUT UNENUMERABLE — 0 of")
print("      86277 at n = 7, first reached at n = 10 (mg-81ff §6) — so c over the class")
print("      is UNMEASURED, not unmeasurable.  On the FULL population min c FALLS")
print("      (0.750, 0.618, 0.536, 0.453, 0.413 at n = 3..7) and is BELOW 4/5 at every")
print("      one, where chain (IV) does not close at all; those posets are 23x-33x")
print("      outside the regime and the refutation does not transfer (mg-81ff §3).")

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("C. THE LADDER, AS ONE PICTURE")
print("-" * 78)
LADDER = [
    ("frozen product today (the two-atom law)",     F(1),            "SUPPLY side"),
    ("chain (IV), c -> 1 — the ENUMERATION's ceiling", e_ceil.v,     "CONJECTURE-gated"),
    ("chain (IV), worst c measured IN REGIME (S_12)", e_worst.v,     "3 families, not a bound"),
    ("chain (II), C_3^gap = 1 — the extreme point", L.dem_II(Lk, F(1)).v,
                                                                     "MEASURED FALSE 1023/1032"),
    ("chain (II), C_3^gap = 10.1654 IN REGIME (S_25)",
     L.dem_II(Lk, F(10.1654).limit_denominator(10 ** 6)).v,          "worse than baseline"),
    ("chain (I) = (III) at C_3 = 1 — AS WRITTEN",   ARCH.v,          "PROVEN on L2 1st disj"),
]
print(f"{'row':46} {'eps_dem':>9} {'d*qbar <=':>11} {'as':>12} {'wall':>7}  status")
for label, e, status in LADDER:
    sp = L.Spec(e)
    dq = L.dq_from_spec(sp)
    print(f"{label:46} {dec(e, 5):>9} {dec(dq, 8):>11} "
          f"{'1 in ' + f'{float(1 / dq):.4g}':>12} {dec(L.wall(sp), 2):>7}  {status}")
print()
print("   EVERY ROW ABOVE THE BASELINE IS GATED ON THE PREFIX-CAPTURE CONJECTURE,")
print("   WHICH IS NOT ONE OF THE SOURCE'S FOUR MAIN OPEN LEMMAS (mg-9461 §0.2).")
print("   And the largest wall any of them reaches is 5x, so:")
print("   NO ROW ON THIS LADDER CLOSES THE WALL.")

print("\n" + "=" * 78)
print("d2 COMPLETE")
print("=" * 78)
