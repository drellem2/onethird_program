#!/usr/bin/env python3
"""mg-0b96 arm d4 — THE ANSWER IS NOT A FLAT NO, AND SAYING SO IS THE POINT OF THIS ARM.

An upper bound on `d` under freezing that owes nothing to the conjecture DOES exist.  It is this,
and it is elementary:

    LEMMA.  If `x ≠ y` have the same strict down-set and the same strict up-set, the transposition
    `(x y)` is an automorphism of `P`, so `Pr[x < y] = 1/2` and `δ(P) ≥ 1/2`.  Hence a FROZEN poset
    has no two such elements.

    COROLLARY (the bound).  Two elements comparable to NOTHING have equal (empty) up- and
    down-sets, so a frozen poset has at most one of them.  At least `n − 1` elements therefore
    carry a comparability, so `P` has at least `⌈(n−1)/2⌉` comparable pairs and

        d(P)  ≤  1 − ⌈(n−1)/2⌉ / C(n,2)   =   1 − Θ(1/n).

    KIND `U`: proved for every finite poset, no census in it, no conjecture in it.

`mg-345e`'s P5 grep reports zero frozen-conditional upper bounds on `d` anywhere in this corpus.
This is one, so the honest verdict is not "no bound exists" but "the bound that exists is worth
`1 − Θ(1/n)`, and the strength row 8 needs is priced in `d2` at the conjecture through order 98".
Filing it matters because the next arc to arrive at `d` will otherwise either re-derive it and
mistake it for a door, or read `mg-345e`'s zero as saying it cannot exist.

  m1  THE LEMMA, EXHAUSTIVELY VERIFIED — every poset with an interchangeable pair has `δ ≥ 1/2`.
  m2  THE BOUND, and the population fact it rests on, measured.
  m3  THE PRICE — what `ε_sup` that bound delivers, against `ε_dem`, and which way it moves in `n`.
  m4  THE CEILING OF THE WHOLE FAMILY OF SUCH ARGUMENTS: `max{ d(P) : P rigid }`, exhaustive.  Every
      "some small structure forces a balanced pair" argument is bounded by this, because rigidity
      is the weakest thing all of them force.
  m5  WHAT WOULD HAVE TO BE TRUE FOR THE LEVER TO WORK, stated as a target rather than a finding.

Exits 0 if the lemma and the bound hold on the population, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction

import lib0b96 as X
import lib6ff4 as L

NMAX = 8
NMAX_LEMMA = 7


def interchangeable_pairs(n, down):
    """Pairs `x ≠ y` with the same strict down-set and the same strict up-set (each read with the
    other element removed, which is the same thing here: equal up/down sets force `x ∥ y`)."""
    up = L.ups(n, down)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            if down[i] == down[j] and up[i] == up[j]:
                out.append((i, j))
    return out


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else NMAX
    print("=" * 100)
    print("mg-0b96  d4  the one unconditional upper bound on d under freezing, and what it is worth")
    print("=" * 100)
    print()

    try:
        C = L.all_classes(nmax)
    except Exception as exc:                                       # pragma: no cover
        print("REFUSED: the imported enumerator did not run: %r" % (exc,))
        print("VERDICT: REFUSED")
        return 2

    ok = True
    half = Fraction(1, 2)

    print("m1  THE LEMMA -- an interchangeable pair forces delta >= 1/2, so it forces NOT FROZEN")
    print("-" * 100)
    print("    x != y with the same strict down-set and up-set: (x y) is an automorphism, so")
    print("    Pr[x < y] = 1/2 exactly.  Verified by computing delta rather than by trusting the")
    print("    symmetry argument -- the argument is the warrant, this is the check on the code.")
    print()
    print("      %4s %10s %14s %14s %s" % ("n", "posets", "with a pair", "delta < 1/2", "verdict"))
    for n in range(2, NMAX_LEMMA + 1):
        withpair = viol = 0
        for down in C[n]:
            if not interchangeable_pairs(n, down):
                continue
            withpair += 1
            le, dlt, _t = L.delta_at_most(n, down, bound=Fraction(1))
            if not le or dlt < half:
                viol += 1
        ok &= viol == 0
        print("      %4d %10d %14d %14d %s"
              % (n, len(C[n]), withpair, viol, "OK" if viol == 0 else "FIRED"))
    print()

    print("m2  THE BOUND -- at most one element comparable to nothing, so d <= 1 - ceil((n-1)/2)/C(n,2)")
    print("-" * 100)
    print("      %4s %-22s %-12s %-10s %s" % ("n", "bound on d", "decimal", "measured", "max d over posets"))
    print("      %4s %-22s %-12s %-10s %s" % ("", "", "", "max d", "with <= 1 isolated element"))
    attained = []
    for n in range(3, nmax + 1):
        cn2 = n * (n - 1) // 2
        bound = 1 - Fraction(-(-(n - 1) // 2), cn2)
        best = Fraction(-1)
        for down in C[n]:
            up = L.ups(n, down)
            iso = sum(1 for i in range(n) if down[i] == 0 and up[i] == 0)
            if iso <= 1:
                best = max(best, X.density(n, down))
        held = best <= bound
        ok &= held
        attained.append(best == bound)
        print("      %4d %-22s %-12.6f %-10s %s"
              % (n, bound, float(bound), best,
                 ("OK -- ATTAINED" if best == bound else "OK -- not attained") if held
                 else "BOUND VIOLATED"))
    print()
    print("    The right column is the SAME class the bound is proved for, measured, and the")
    print("    sharpness verdict is READ OFF IT rather than asserted beside it:")
    print("      attained at %d of the %d values of n swept  --  the bound is %s on its own class."
          % (sum(attained), len(attained),
             "SHARP" if all(attained) else "sharp at some n and not at others"))
    print("    ⚠️  Sharp ON THIS CLASS is not sharp on the frozen class, which is empty; what is")
    print("    measured is that the elementary argument cannot be tightened without a new idea,")
    print("    not that a frozen poset attains it.")
    print()

    print("m3  THE PRICE -- what that bound is worth in row 8's own currency")
    print("-" * 100)
    print("    eps_sup = d*n/(n+1), and the wall is down at eps_sup <= eps_dem = %s." % X.EPS_DEM)
    print()
    print("      %5s %-16s %-14s %-14s %s" % ("n", "d bound", "eps_sup at it", "eps_dem", "short by a factor"))
    for n in (8, 15, 20, 50, 99, 300):
        cn2 = n * (n - 1) // 2
        bound = 1 - Fraction(-(-(n - 1) // 2), cn2)
        e = X.eps_sup(n, bound)
        print("      %5d %-16.6f %-14.6f %-14s %.1f x"
              % (n, float(bound), float(e), X.EPS_DEM, float(e / X.EPS_DEM)))
    print()
    print("    AND IT MOVES THE WRONG WAY.  The bound is 1 - Theta(1/n): it improves on the")
    print("    trivial d <= 1 by an amount that SHRINKS as n grows, while what row 8 needs is a")
    print("    constant 2e-2 at every n.  At n = 99 -- the first n at which a primitive poset")
    print("    could even meet the needed ceiling (d2 m3) -- it is short by a factor of ~49.")
    print()

    print("m4  THE CEILING OF EVERY ARGUMENT OF THIS SHAPE:  max{ d(P) : P rigid }")
    print("-" * 100)
    print("    Peczarski (2017): a poset with a non-trivial automorphism satisfies the conjecture,")
    print("    so a frozen poset is RIGID.  Rigidity is the weakest thing any `this small structure")
    print("    forces a balanced pair' argument can force, so max d over rigid posets is a CEILING")
    print("    on what the whole family of such arguments can ever deliver.")
    print()
    print("      %4s %10s %14s %12s %14s" % ("n", "posets", "rigid", "max d", "1 - 2/n"))
    for n in range(3, nmax + 1):
        best = Fraction(-1)
        cnt = 0
        for down in C[n]:
            if X.is_rigid(n, down):
                cnt += 1
                best = max(best, X.density(n, down))
        print("      %4d %10d %14d %12s %14s"
              % (n, len(C[n]), cnt, str(best) if best >= 0 else "none", 1 - Fraction(2, n)))
    print()
    print("    ⚠️  This is an FP ceiling over the n it reaches and is NOT extrapolated.  What")
    print("    carries past it is d3 m5's explicit family, which is rigid by construction at every")
    print("    n it covers and has d -> 1.")
    print()

    print("m5  WHAT WOULD HAVE TO BE TRUE, stated as a target and not as a finding")
    print("-" * 100)
    print("    For the density lever to close row 8, some argument would have to rule out every")
    print("    frozen poset of density between 2e-2 and 1 - Theta(1/n).  By d1 that argument IS")
    print("    the (1/3)-(2/3) conjecture on {d > 2e-2}; by d2 it delivers the conjecture at every")
    print("    order below 99; by d3 no class exclusion on the record reaches into that band at")
    print("    all, and there is an explicit poset in it at every n >= 15.")
    print()
    print("    THE ONE THING THAT WOULD CHANGE THIS VERDICT, named so it can be looked for: a")
    print("    result of the form `delta(P) >= f(d)' with f increasing and f(2e-2) >= 1/3 -- i.e.")
    print("    a DENSITY-TO-BALANCE bound rather than a structure-to-balance one.  Nothing of that")
    print("    shape appears in mg-33f5's survey or in this corpus.  It is not ruled out here.")
    print()

    print("=" * 100)
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
