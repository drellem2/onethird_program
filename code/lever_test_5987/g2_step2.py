#!/usr/bin/env python3
"""mg-5987 `g2` — STEP 2: *does it imply the target on a class?*  And what does that cost?

`mg-9b6b`'s step 2 is: if the statement implies the conjecture on a class, it is not a lever —
it is the conjecture restricted, and the price is the orders it delivers.

THE FIRST HALF OF THAT TEST IS A TRIVIALITY AND SAYING SO IS THE POINT.  Every frozen-conditional
statement implies the conjecture on a class, because contraposition is an equivalence:

    frozen(P) ⟹ Q(P) ≤ C          is          Q(P) > C ⟹ ¬frozen(P) ⟹ δ(P) ≥ 1/3
                                              ────────────────────────────────────
                                              the conjecture, restricted to {Q > C}

so step 2 never returns NO on this kind of object and cannot be what separates `(R)` from anything
else.  WHAT SEPARATES THEM IS THE PRICE, and the price is a property of ONE number per order:

    floor_Q(n) = min{ Q(P) : P primitive non-chain on n elements }

because `{Q > C}` covers the whole of order `n` — i.e. delivers that order of the conjecture
outright — exactly when `floor_Q(n) > C`.  `(R)` died because `floor_d(n) = 2/n` DECAYS, so every
fixed ceiling swallows an initial segment of orders and the useful ceilings swallow 84 unreached
ones.  This arm measures the two floors nobody had computed.

⚠️  POPULATION: exhaustive over ALL isomorphism classes to n = 7, and over the PRIMITIVES at
    n = 8.  The n = 8 non-chain population is not swept and no number here is claimed for it.
"""

import json
import os
import sys
from fractions import Fraction

import lib5987 as M
import lib6ff4 as L

print("=" * 96)
print("mg-5987  g2 — STEP 2: THE CONTRAPOSITIVE, AND WHAT IT DELIVERS")
print("=" * 96)

print("""
§1. THE CONTRAPOSITIVE, INSTANTIATED AT ALL THREE RESIDUALS.  One line each, and the third is
    mg-0b96 §2's own reading of (1_D), reproduced here so the three can be read off one table.

    (R)_D      frozen ⟹ d(P) ≤ D                    ⟺   the conjecture on { d > D }
    (EQ)_C     frozen ⟹ max_x |h − rank_e| ≤ C      ⟺   the conjecture on { max_x |h − rank_e| > C }
    (B-cov)_C  frozen ⟹ Σ_x C_x ≤ C · E[inv_e]      ⟺   the conjecture on { Σ_x C_x / E[inv_e] > C }

    None of the three escapes step 2 as a yes/no question.  All three ARE the conjecture restricted.
""")

CL = L.all_classes(7)
DATA = {}          # n -> (population tag, [(bias, rho, d)])
for n in range(3, 8):
    for tag, pop in (("primitive", M.primitives(CL, n)), ("non-chain", M.non_chains(CL, n))):
        rows = []
        for d in pop:
            pr = M.profile(n, d)
            r = M.rank_of(M.barycentric(n, pr["h"]))
            rows.append((M.bias(n, pr, r), M.rho(n, d, pr, r), M.density(n, d)))
        DATA[(n, tag)] = rows
    print(f"   … swept n = {n}")

CL8 = L.all_classes(8)
rows = []
for d in M.primitives(CL8, 8):
    pr = M.profile(8, d)
    r = M.rank_of(M.barycentric(8, pr["h"]))
    rows.append((M.bias(8, pr, r), M.rho(8, d, pr, r), M.density(8, d)))
DATA[(8, "primitive")] = rows
print("   … swept n = 8, primitives only")

print("""
§2. THE FLOORS.  `floor_Q(n) = min{ Q(P) : P primitive non-chain at order n }`, exact.
""")
print("    n | primitives | floor of max|h−rank|      | floor of Σ C_x / E[inv]   | floor of d = 2/n")
print("   ---+------------+---------------------------+---------------------------+------------------")
FB, FR = {}, {}
for n in range(3, 9):
    rows = DATA[(n, "primitive")]
    FB[n] = min(r[0] for r in rows)
    FR[n] = min(r[1] for r in rows)
    fd = min(r[2] for r in rows)
    print(f"   {n:2d} | {len(rows):10d} | {str(FB[n]):9s} = {float(FB[n]):.5f}    |"
          f" {str(FR[n]):9s} = {float(FR[n]):.5f}    | {str(fd):6s} = {float(fd):.5f}"
          + ("   ✓ = 2/n" if fd == Fraction(2, n) else "   ✗"))
print("""
    THE THIRD COLUMN IS THE CONTROL AND IT IS WHY THE OTHER TWO MATTER.  `d`'s floor is exactly
    `2/n` at every order — mg-0b96's primitivity bound, reproduced here from the census side — and
    it is a THEOREM and it DECAYS.  Both properties are load-bearing, and the second one runs the
    OPPOSITE WAY from the way it first reads: a decaying floor is what makes `(R)`'s price FINITE.
    `{d > D}` covers order `n` while `2/n > D` and stops covering it at `n = 2/D`, which is why
    mg-9b6b could write *"forbids up to n = 98"*.  A floor that does NOT decay is never overtaken
    by a fixed dial setting, so its delivery has no upper cutoff at all.  The other two floors sit
    between 0.30 and 0.45 across the whole reachable range and `g3` caps both at every `n` with an
    explicit primitive family — but a cap is not a decay, and §3 is where that bites.
""")
print("    the same floors over ALL non-chain classes rather than the primitives (n ≤ 7):")
print("    n |  non-chain | floor of max|h−rank| | floor of Σ C_x / E[inv]")
print("   ---+------------+----------------------+------------------------")
for n in range(3, 8):
    rows = DATA[(n, "non-chain")]
    print(f"   {n:2d} | {len(rows):10d} | {str(min(r[0] for r in rows)):20s} |"
          f" {str(min(r[1] for r in rows))}")
print("""
    The non-chain floor of Σ C_x / E[inv] is ZERO from n = 4 on, and that is not a rival
    measurement — it is the ordinal sums.  A poset with a cut has every pair indicator at an
    element either constant or confined to one summand, so its same-side covariance vanishes
    identically.  Pricing over that population would report *"delivers nothing"* for a reason that
    has nothing to do with (B-cov), which is exactly the mistake mg-f5be's primitivity objection
    exists to prevent, so every verdict below is over the PRIMITIVES.
""")

print("""
§3. THE PRICE, IN mg-9b6b's OWN CURRENCY: orders of the conjecture the contrapositive delivers.
    An order is delivered when the restricted class covers the WHOLE primitive population there.
    ⚠️  Read only to n = 8: this table cannot see an order it has not swept, so *"delivers"* below
    means *"delivers among n = 3…8"*.  What happens at every n is `g3`'s, via the family.
""")
print("    dial C  | (EQ)_C delivers          | (B-cov)_C delivers")
print("   ---------+--------------------------+---------------------------")
for C in (Fraction(1, 50), Fraction(1, 10), Fraction(1, 4), Fraction(3, 10),
          Fraction(2, 5), Fraction(1, 2), Fraction(4, 5), Fraction(1)):
    print(f"   {str(C):8s} | {str(M.delivers(FB, C)):24s} | {M.delivers(FR, C)}")
print("""
    And the (R) column, for the same reading, computed through lib9b6b — a CONSISTENCY CHECK on
    this arm's price machinery rather than a second measurement of mg-9b6b's figure:
""")
rd = [n for n in range(3, 400) if M.V.primitive_floor(n) > M.V.d_needed(n)]
print(f"    (R) at row 8's D_needed = ε_dem·(n+1)/n delivers n = 3…{max(rd)}"
      f" — {len(rd)} orders, {len([n for n in rd if n > 14])} of them UNREACHED (n > 14).")
print(f"    Over the same window this table sees, n = 3…8, (R) delivers all 6.")

print("""
§4. THE REFINEMENT THE ORDERS COUNTER CANNOT MAKE.  A count of delivered orders is binary per
    order: it returns 0 for a statement that settles nothing and ALSO for one that settles every
    primitive but one at every order.  Those are not the same object, and the difference is the
    whole question this directory was filed to answer — so the fraction is reported beside it.
""")
print("    dial C  | (EQ)_C settles                             | (B-cov)_C settles")
print("            | n=5      n=6      n=7      n=8             | n=5      n=6      n=7      n=8")
print("   ---------+--------------------------------------------+-----------------------------------------")
for C in (Fraction(1, 50), Fraction(1, 4), Fraction(2, 5), Fraction(1, 2), Fraction(4, 5)):
    cells = []
    for which in (0, 1):
        for n in (5, 6, 7, 8):
            s, t = M.coverage([r[which] for r in DATA[(n, "primitive")]], C)
            cells.append(f"{100.0 * s / t:5.1f}%")
    print(f"   {str(C):8s} | " + " ".join(cells[:4]) + "  | " + " ".join(cells[4:]))
print("""
    ⚠️  READ THE 100.0% ROWS AS WHAT THEY ARE.  A row at 100% across the sweep is a statement that
    delivers those orders outright — coverage and counter agree there.  The rows that matter are
    the ones just BELOW 100%: at C = 2/5 the counter says (EQ) delivers NOTHING, and the coverage
    says it settles 99.8% of the primitives at n = 8 — 25 posets of 12 524 stand between *"zero
    price"* and *"the whole order"*.  That is the refinement, and it is not a decoration: an
    escape carried by 25 posets is not the same object as an escape carried by half the class, and
    mg-9b6b's counter returns the same 0 for both.  Both residuals also have settings where the
    coverage is genuinely small — (EQ) at C = 4/5 settles 80% at n = 8 — so the counter is not
    always wrong here, only unable to tell which case it is in.

    AND THE COVERAGE RISES WITH `n` AT FIXED `C` — 90.3 → 99.8% for (EQ) at C = 2/5 — so the
    exceptional set is shrinking as a FRACTION even though `g3` shows it is never empty.
""")

print("""
    THE EXCEPTIONS, COUNTED RATHER THAN INFERRED FROM THE PERCENTAGE.  A rounded 99.8% is not a
    number anybody can check a claim against, and the claim this arc rests on is about the SIZE of
    the exceptional set — so it is printed as posets, at the settings the verdict is stated at.
""")
for which, name, C in ((0, "(EQ)   ", Fraction(2, 5)), (1, "(B-cov)", Fraction(4, 5))):
    for n in (7, 8):
        vals = [r[which] for r in DATA[(n, "primitive")]]
        s, t = M.coverage(vals, C)
        print(f"    {name} at C = {str(C):3s}, n = {n}:  {t - s:5d} of {t} primitives NOT settled"
              f"  ({100.0 * (t - s) / t:.2f}%)")

print("""
§4b. THE TWO THRESHOLDS, WRITTEN OUT — the exact constants §3's table is read at.  `g3` needs
     them for its dial and READS THEM FROM THIS ARM rather than carrying a copy: a figure typed
     twice is a figure that goes stale in one of its two homes (mg-2959's finding, and the reason
     this arm writes `floors.json` instead of `g3` quoting a number from this transcript).
""")
ALL_B, ALL_R = min(FB.values()), min(FR.values())
print(f"    (EQ)_C     delivers every swept order (n = 3…8) iff  C < {ALL_B} = {float(ALL_B):.5f}"
      f"   (the floor at n = 8)")
print(f"    (B-cov)_C  delivers every swept order (n = 3…8) iff  C < {ALL_R} = {float(ALL_R):.5f}"
      f"   (the floor at n = 4)")
print( "    ⚠️  NOT the same constant, and not the one an eye would pick off §2's table: both minima")
print( "    are at the ENDS of the swept range and the (B-cov) one is at n = 4, because neither")
print( "    floor is monotone in n.")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "floors.json"), "w") as fh:
    json.dump({"bias": {str(n): str(FB[n]) for n in FB},
               "rho": {str(n): str(FR[n]) for n in FR}}, fh, indent=2, sort_keys=True)
    fh.write("\n")

print("""
§5. VERDICT ON STEP 2.

    Neither escapes step 2 as a question.  Both ARE the conjecture restricted, exactly as (R) is,
    and by the same one-line contraposition.  What differs is that the price CANNOT BE COMPUTED in
    mg-9b6b's currency, and the reason is precise rather than a shortage of sweep:

        the currency is UNREACHED orders (n > 14, above the census frontier);
        an unreached order is delivered iff floor_Q(n) > C at that n;
        so the currency is a function of the floor ABOVE n = 14 —

    and for `(R)` that floor is a THEOREM (`2/n`), while for these two it is a CENSUS that stops at
    n = 8, every order of which is already verified.  No further sweeping fixes this: n = 12 is
    still inside the verified range.  What the census DOES settle is the two ends, and `g3` pins
    them — 0 orders at every n above an explicit cap, every swept order below the measured floor.
""")
sys.exit(0)
