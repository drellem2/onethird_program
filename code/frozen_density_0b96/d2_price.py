#!/usr/bin/env python3
"""mg-0b96 arm d2 — WHAT THE LEVER COSTS AT THE ONLY STRENGTH ROW 8 CAN USE, AND IT IS NOT A
LEMMA-SIZED PRICE.

`d1` shows a frozen-class ceiling `(1_D)` is the conjecture on `{d > D}` for every `D`.  That
alone does not close the question, because a WEAK ceiling might still be cheap and a strong one
expensive, and row 8 needs a specific strength.  This arm prices it, in exact rationals.

  m1  WHAT ROW 8 NEEDS.  `ε_sup = d·n/(n+1)` (`mg-0e8c`, `STATE.md:123`) and the wall is already
      down at `ε_sup ≤ ε_dem ≈ 2×10⁻²`, so the ceiling that would close it is
      `D_needed(n) = ε_dem·(n+1)/n`, a CONSTANT to two figures at every `n`.
  m2  WHAT PRIMITIVITY ALREADY FORCES FROM BELOW.  A minimal counterexample is primitive
      (`STATE.md:55`), primitive ⟹ `m ≥ n−1` ⟹ `d ≥ 2/n`.  The two meet at one `n`, and below it
      NO primitive poset satisfies the needed ceiling — so `(1_{D_needed})` would prove there is
      no primitive frozen poset below that `n` at all.
  m3  THE CROSSING, AND ITS RECONCILIATION WITH `mg-33f5`'s T2.  This arm gets `n ≥ 99`; `mg-33f5`
      §3 gets `T2 = 100` by `2/ε_spec`.  The two differ by exactly the `n/(n+1)` factor, which T2
      drops.  Both are printed, neither is called wrong, and the agreement to one unit is a second
      route to a threshold already on the record rather than a new number.
  m4  THE PRICE IN ORDERS, AGAINST THE CENSUS FRONTIER.  The conjecture is verified through
      `n = 14` (`mg-33f5`: Peczarski `n ≤ 11` refereed, Gupta `n ≤ 14` preprint).  A ceiling at
      row 8's strength delivers every order below the crossing.  The difference is the price.
  m5  WHAT THAT WOULD HAVE COST AS A CENSUS, as an ORDER-OF-MAGNITUDE ESTIMATE and labelled as
      one: `log₂ |posets on n|` grows like `n²/4`, and the exact `A000112(14) = 1 338 193 159 771`
      anchors the estimate at the frontier.

⚠️  NOTHING HERE IS A CLAIM THAT THE CEILING IS FALSE.  It is a claim about what proving it would
deliver.  A statement that hands you 84 unreached orders of the conjecture is not an ingredient of
a proof of the conjecture; it is a stronger statement wearing a lemma's clothes.

Exits 0 always unless the arithmetic self-checks fail (1), or an input is missing (2).
"""

import sys
from fractions import Fraction

import lib0b96 as X

NS = [12, 14, 15, 20, 30, 50, 80, 98, 99, 100, 150, 300]
VERIFIED_THROUGH = 14                      # mg-33f5 §1 (L2, preprint); refereed value is 11
A000112_14 = 1338193159771                 # mg-33f5 §1, checked there against OEIS A000112


def main():
    print("=" * 100)
    print("mg-0b96  d2  the price of a frozen-class density ceiling at row 8's strength")
    print("=" * 100)
    print()
    ok = True

    print("m1  WHAT ROW 8 NEEDS:  D_needed(n) = eps_dem*(n+1)/n   at eps_dem = %s" % X.EPS_DEM)
    print("-" * 100)
    print("    eps_sup = d*n/(n+1) is mg-0e8c's supply bound (STATE.md:123).  The wall is already")
    print("    down -- proven, all n, L4-free -- wherever eps_sup <= eps_dem.  Inverting:")
    print()
    print("      %5s  %-14s %-12s" % ("n", "D_needed(n)", "as a decimal"))
    for n in NS:
        Dn = X.d_needed(n)
        print("      %5d  %-14s %.6f" % (n, Dn, float(Dn)))
    print()
    print("    It is eps_dem to two figures at every n, so `the ceiling row 8 needs' is")
    print("    d <~ 2e-2 and does not soften with n.")
    print()

    print("m2  WHAT PRIMITIVITY FORCES FROM BELOW:  d >= 2/n")
    print("-" * 100)
    print("    A minimal counterexample is PRIMITIVE (STATE.md:55, ledger row 2), primitive means")
    print("    the incomparability graph is connected, and a connected graph on n vertices has")
    print("    at least n-1 edges:  m >= n-1, so d = m/C(n,2) >= 2/n.")
    print()
    print("      %5s  %-14s %-14s %s" % ("n", "d >= 2/n", "D_needed(n)", "can a primitive poset meet it?"))
    for n in NS:
        lo, Dn = Fraction(2, n), X.d_needed(n)
        print("      %5d  %-14s %-14s %s" % (n, lo, Dn, "yes" if lo <= Dn else "NO -- impossible"))
    print()

    print("m3  THE CROSSING, AND mg-33f5's T2")
    print("-" * 100)
    cross = None
    n = 2
    while n < 10000:
        if Fraction(2, n) <= X.d_needed(n):
            cross = n
            break
        n += 1
    ok &= cross is not None
    print("    2/n <= eps_dem*(n+1)/n  <=>  2 <= eps_dem*(n+1)  <=>  n >= 2/eps_dem - 1")
    print("    first n at which a primitive poset can meet the needed ceiling:  n = %s" % cross)
    print()
    print("    mg-33f5 §3's T2 reads `2/eps_spec = 100'.  That drops the n/(n+1) factor between")
    print("    eps_sup and d; carrying it gives %s.  THE TWO ARE THE SAME THRESHOLD to one unit," % cross)
    print("    and this arm reaches it from the density side rather than the master-bound side.")
    print("    Neither is corrected here: T2 is stated at its own precision and is right there.")
    print()

    print("m4  THE PRICE, IN ORDERS OF THE CONJECTURE")
    print("-" * 100)
    print("    Suppose (1_D) at D = D_needed were PROVEN.  Then no primitive poset below n = %s" % cross)
    print("    is frozen -- its d would have to be both >= 2/n and <= D_needed(n).  A minimal")
    print("    counterexample is primitive, so the conjecture holds at every n < %s." % cross)
    print()
    print("      conjecture verified through n = %d                (mg-33f5: Gupta preprint;" % VERIFIED_THROUGH)
    print("                                                         refereed frontier is 11)")
    print("      the ceiling would deliver through n = %d" % (cross - 1))
    print("      orders it delivers that no census has reached:  %d ... %d  =  %d ORDERS"
          % (VERIFIED_THROUGH + 1, cross - 1, cross - 1 - VERIFIED_THROUGH))
    print()
    print("    ⚠️  AND IT DOES NOT STOP THERE.  Those are only the orders it settles OUTRIGHT.")
    print("    Above n = %s the same ceiling still bites: it forces any frozen primitive poset" % cross)
    print("    into the regime where L1b is already a theorem, which is what row 8 wants -- so")
    print("    the 84 orders are the FLOOR of what proving it buys, not the whole of it.")
    print()

    print("m5  WHAT THOSE ORDERS COST AS A CENSUS -- AN ESTIMATE, LABELLED AS ONE")
    print("-" * 100)
    print("    log2 |posets on n elements| ~ n^2/4 (Kleitman-Rothschild), anchored at the exact")
    print("    A000112(14) = %d from mg-33f5 §1." % A000112_14)
    print()
    print("      %5s  %-24s %s" % ("n", "log2 count, n^2/4", "anchor"))
    for n in (14, 20, 50, cross - 1):
        est = n * n / 4.0
        anchor = ""
        if n == 14:
            import math
            anchor = "exact log2 A000112(14) = %.1f" % math.log2(A000112_14)
        print("      %5d  %-24.1f %s" % (n, est, anchor))
    print()
    print("    ⚠️  THIS IS AN ASYMPTOTIC ESTIMATE AND NOT A COUNT.  n^2/4 at n = 14 gives 49.0")
    print("    against the exact 40.3, so the estimate is loose by ~9 bits at the one n where it")
    print("    can be checked -- and loose in the direction that OVERSTATES the cost.  What it is")
    print("    used for is the only thing it can carry: the census route to order %d is not" % (cross - 1))
    print("    large-but-feasible, it is out of reach by a margin no correction to the constant")
    print("    would close.")
    print()

    print("=" * 100)
    print("    THE PRICE, IN ONE LINE.  A frozen-class density ceiling at the only strength row 8")
    print("    can consume implies the (1/3)-(2/3) conjecture at every order below %s, which is" % cross)
    print("    %d orders past the frontier a 1.3e12-poset census reached.  d1 already showed it IS" % (cross - 1 - VERIFIED_THROUGH))
    print("    the conjecture on {d > D}; this is how much of the conjecture that is.")
    print("=" * 100)
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
