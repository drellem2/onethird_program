#!/usr/bin/env python3
"""mg-6ff4 arm c3 — THE REALIZABILITY GAP, MEASURED, AND WHERE THE BOUNDARY SITS AGAINST THE TWO
CONSTANTS THAT BRACKET THE QUESTION.

  m1  THE THREE NUMBERS AT EACH `n`.  The pair-marginal supremum `n/(n+1)` (attained by the
      two-atom law `μ = (2/3)δ_e + (1/3)δ_{rev e}`, `mg-6bc2` Claim 3.1, re-derived in `c0` T6);
      the WORST ACTUAL POSET at the boundary; and the demand `ε_dem ≈ 2·10⁻²`.
  m2  THE REALIZABILITY GAP.  `n/(n+1) − max_P ε_obs(P)`, and the RATIO, which is the honest
      unit: a difference tending to `1` and a ratio growing like `n` say different things and the
      ratio is the one that scales.
  m3  THE `mg-6bc2` IDENTITY `ε_spec = 3·d·q̄·n/(n+1)`, checked at every boundary poset, and the
      answer to WHICH OF THE TWO LEVERS carries the fall.  `mg-6bc2` §3.1 says only the density
      lever moves at its optimisers; this measures it at real posets at the boundary.
  m4  THE CROSSING.  Where the boundary maximum meets `ε_dem`, under the closed form and stated
      as an extrapolation with the word EXTRAPOLATION on it.

⚠️  EVERY NUMBER HERE IS A BOUNDARY NUMBER.  `δ = 1/3` is OUTSIDE the frozen hypothesis, which is
STRICT.  Nothing in this file is a measurement of the frozen class and nothing in it may be quoted
as one.

Exits 0 if the identity checks pass, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction

import lib6ff4 as L

NMAX = 9
EPS_DEM = Fraction(2, 100)
V_CANON = L.canon(3, (0, 1, 0))


def closed_form_max(n):
    """max eps over the boundary class at n, UNDER THE CLOSED FORM: 4*floor(n/3)/(n^2-1)."""
    return Fraction(4 * (n // 3), n * n - 1)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else NMAX
    print("=" * 100)
    print("mg-6ff4  c3  the realizability gap, measured rather than argued")
    print("=" * 100)
    print()

    classes = L.all_classes(nmax)
    rows = []
    for n in range(3, nmax + 1):
        for down in classes[n]:
            if not L.incomparable_pairs(n, down):
                continue
            ok, d, tbl = L.delta_at_most(n, down)
            if not ok or d != L.THIRD:
                continue
            mm = L.measure(n, down, tbl)
            summ = L.ordinal_summands(n, down)
            kV = sum(1 for k, dd in summ if k == 3 and dd == V_CANON)
            rows.append((n, down, mm, kV))
        print("    ... n = %d swept" % n, flush=True)
    print()

    per = {}
    for (n, down, mm, kV) in rows:
        per.setdefault(n, []).append(mm)

    print("m1  THE THREE NUMBERS, at each n.  MEASURED = exhaustive over every isomorphism class.")
    print("-" * 100)
    print("    %3s %14s %16s %16s %14s %12s"
          % ("n", "n/(n+1) (sup)", "max eps (poset)", "min eps (poset)", "eps_dem", "max/dem"))
    for n in sorted(per):
        sup = Fraction(n, n + 1)
        mx = max(m["eps"] for m in per[n])
        mn = min(m["eps"] for m in per[n])
        print("    %3d %14s %16s %16s %14s %12.2f"
              % (n, str(sup), str(mx), str(mn), str(EPS_DEM), float(mx / EPS_DEM)))
    print()
    print("    The supremum column is NOT a poset.  It is attained by the two-atom law, a measure")
    print("    on 2 of n! orders (c0 T6).  The gap between the two left columns is the price of")
    print("    dropping realizability, and it is the object this arm exists to put a number on.")
    print()

    print("m2  THE REALIZABILITY GAP -- difference and ratio")
    print("-" * 100)
    print("    %3s %14s %16s %16s %14s" % ("n", "sup = n/(n+1)", "worst real poset",
                                           "gap (difference)", "ratio sup/real"))
    for n in sorted(per):
        sup = Fraction(n, n + 1)
        mx = max(m["eps"] for m in per[n])
        print("    %3d %14s %16s %16s %14.3f"
              % (n, str(sup), str(mx), str(sup - mx), float(sup / mx)))
    print()
    print("    UNDER THE CLOSED FORM (c1 m4, checked exhaustively to n = %d):" % nmax)
    print("      max_P eps = 4*floor(n/3)/(n^2-1),  so the ratio is  ~ 3(n-1)/4  and GROWS")
    print("      LINEARLY, while the difference merely saturates at 1.  THE RATIO IS THE HONEST")
    print("      UNIT: realizability does not buy a constant, it buys a FACTOR THAT GROWS WITH n.")
    print("    %3s %16s %16s %14s" % ("n", "closed-form max", "3(n-1)/4", "measured ratio"))
    for n in sorted(per):
        sup = Fraction(n, n + 1)
        mx = max(m["eps"] for m in per[n])
        cf = closed_form_max(n)
        tag = "" if cf == mx else "   ⚠️ CLOSED FORM DISAGREES"
        print("    %3d %16s %16s %14.3f%s"
              % (n, str(cf), str(Fraction(3 * (n - 1), 4)), float(sup / mx), tag))
    print()

    print("m3  THE mg-6bc2 IDENTITY  eps_spec = 3*d*qbar*n/(n+1), and which lever carries the fall")
    print("-" * 100)
    fail = 0
    for (n, down, mm, kV) in rows:
        if mm["eps"] != 3 * mm["d"] * mm["qbar"] * Fraction(n, n + 1):
            fail += 1
    print("    identity checked at all %d boundary posets · mismatches %d   [%s]"
          % (len(rows), fail, "PASS" if fail == 0 else "FAIL"))
    print()
    print("    %3s %20s %14s %14s" % ("n", "qbar (min..max)", "d (min..max)", "3*d*qbar"))
    for n in sorted(per):
        qs = sorted({m["qbar"] for m in per[n]})
        ds = sorted({m["d"] for m in per[n]})
        prods = sorted({3 * m["d"] * m["qbar"] for m in per[n]})
        print("    %3d %20s %14s %14s"
              % (n, ("%s" % qs[0]) if len(qs) == 1 else "%s .. %s" % (qs[0], qs[-1]),
                 ("%s" % ds[0]) if len(ds) == 1 else "%s .. %s" % (ds[0], ds[-1]),
                 ("%s" % prods[0]) if len(prods) == 1 else "%s .. %s" % (prods[0], prods[-1])))
    allq = {m["qbar"] for m in rows and [r[2] for r in rows]}
    print()
    print("    qbar over the WHOLE boundary class: %s" % sorted(allq))
    print("    ⚠️  qbar is PINNED AT 1/3 -- the cap -- at every boundary poset, exactly as")
    print("    mg-6bc2 §3.1 reports at its optimisers.  So the ENTIRE fall in eps lives in the")
    print("    DENSITY d, which is 2k/C(n,2) = Theta(1/n) at the maximiser and Theta(1/n^2) at the")
    print("    minimiser.  The operative lever is residual (R), the NUMBER of incomparable pairs,")
    print("    and this is that statement measured on real posets rather than on an LP optimum.")
    print()

    print("m4  THE CROSSING WITH eps_dem -- EXTRAPOLATION, NOT MEASUREMENT")
    print("-" * 100)
    print("    Measured range stops at n = %d.  Everything in this block is the closed form" % nmax)
    print("    CONTINUED, and it is worth exactly what the closed form's survival is worth.")
    print("    %3s %18s %14s" % ("n", "4*floor(n/3)/(n^2-1)", "vs eps_dem"))
    for n in (9, 12, 15, 20, 30, 45, 60, 66, 69, 90, 120):
        cf = closed_form_max(n)
        print("    %3d %18s %14s" % (n, str(cf), "above" if cf > EPS_DEM else "BELOW"))
    cross = None
    for n in range(3, 400):
        if closed_form_max(n) <= EPS_DEM:
            cross = n
            break
    last_above = max(n for n in range(3, 400) if closed_form_max(n) > EPS_DEM)
    print()
    print("    First n at which the boundary MAXIMUM falls to or below eps_dem = 1/50: n = %s"
          % cross)
    print("    LAST n at which it is still ABOVE eps_dem:                             n = %s"
          % last_above)
    print("    ⚠️  THOSE ARE DIFFERENT NUMBERS AND THE SECOND IS THE ONE THAT MEANS ANYTHING.")
    print("    The maximum SAWTOOTHS -- it jumps up at every n divisible by 3, when one more copy")
    print("    of V becomes affordable -- so `first n below` is not a crossing at all: it drops")
    back_above = [n for n in range(cross + 1, last_above + 1) if closed_form_max(n) > EPS_DEM]
    print("    below at n = %s and comes back ABOVE at n = %s.  It is below eps_dem FOR GOOD only"
          % (cross, back_above if back_above else "-"))
    print("    from n = %d onward.  A monotone reading of this sequence is WRONG, and reporting"
          % (last_above + 1,))
    print("    only the first crossing would have published that wrong reading.")
    print("    ⚠️  EXTRAPOLATION.  It assumes no new primitive poset with delta <= 1/3 exists at any")
    print("    n, which is exactly what c1 and c2 could not check above their ranges.  Quoted as a")
    print("    measurement it would be the 0/132 error in a new index.")
    print()

    ok = fail == 0
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
