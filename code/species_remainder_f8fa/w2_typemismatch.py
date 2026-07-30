"""W2 -- CONTROL (ii) FIRES ON A TYPE MISMATCH.  ITS CONCLUSION SURVIVES.

mg-a61f's X5.  Corrected in the document by mg-6f61 (section 5, section 6 item
5, S7) and NOT at source: `t5_hopf_monoid.py` still printed the three counts
with no reading attached, and `code/species_7d75/README.md` still presented
them under "Conventions that have bitten this repo before" as measuring "how
differently" the two products behave -- which is the near-miss reading the
audit refuted.

THE CLAIM, measured here as a SET EQUALITY and not as a coincidence of counts:

    { pairs (x, y) on which the Tits product fails product closure }
      =
    { pairs (x, y) whose two ground sets are both NON-EMPTY }

mu_{S,T} takes its two factors on DISJOINT ground sets.  The Tits product
intersects blocks.  Across disjoint non-empty sets every block intersection is
empty, so the Tits product returns the EMPTY composition on a non-empty ground
set, which is not a face of it.  The failure is of the map's TYPE, and no
count on either side can be made larger or smaller by the two products being
nearer to or further from each other.

PREDICTIONS, written before the run:

  P1  every failing pair has both ground sets non-empty
  P2  every pair with both ground sets non-empty fails -- so the two sets are
      EQUAL, not merely equinumerous
  P3  on every failing pair the Tits product is the empty composition
  P4  the pairs with an empty side are NOT vacuous (there are some) and none
      of them fails
  P4b CONTROL on the control: with the guard removed -- the raw Tits product
      everywhere -- the count is NOT 1 442, because the Tits product of
      anything with the empty composition is empty.  If removing the guard
      leaves the count where it was, the guard is not what confines the
      failures and P1/P2 are being read off the wrong mechanism.
  P5  CONTROL: a type-CORRECT corruption of the product -- concatenation with
      the last block of x merged into the first block of y, mg-6f61's control
      (v) -- has 0 product-closure failures.  The product-closure column
      separates type-correctness, NOT nearness.  If P5 misses, the column is
      measuring something else and this reading is wrong.

WHAT IS NOT WITHDRAWN.  The conclusion control (ii) was cited for -- that the
band product is invisible to the Hopf structure, so nothing mg-ebd8 or mg-af28
measured about the walk is a Hopf-theoretic invariant -- is RIGHT, and this
file strengthens rather than weakens it: a type mismatch is a stronger
separation than a near miss, and it holds at every ground set rather than on
[4].
"""

import sys

from kernf8fa import (elems_F, decompositions, tits_product, concat,
                      poset_union, hdr)

GROUND = 4
bad = 0

universe = {}
for m in range(1 << GROUND):
    I = frozenset(k for k in range(GROUND) if m >> k & 1)
    if I not in universe:
        universe[I] = set(elems_F(I))


def mu_tits(x, y):
    """Control (ii) exactly as `t5_hopf_monoid.py` defines it, guard included:
    the Tits product when both faces are non-empty, and concatenation when
    either is -- because the Tits product of anything with the empty
    composition is the empty composition, and the control was written to
    corrupt the product rather than to delete it.

    The guard is worth naming: it is the reason the failures land exactly on
    the both-non-empty pairs rather than on all 11 301.  Without it the
    control fails 11 300 of 11 301 and measures nothing at all."""
    if x[1] and y[1]:
        return (poset_union(x[0], y[0]), tits_product(x[1], y[1]))
    return (poset_union(x[0], y[0]), concat(x[1], y[1]))


def mu_hopf(x, y):
    return (poset_union(x[0], y[0]), concat(x[1], y[1]))


def mu_merge(x, y):
    """mg-6f61's control (v): concatenate, then merge the last block of x with
    the first block of y.  Type-CORRECT -- it returns a composition of the
    union -- and wrong."""
    F, G = tuple(x[1]), tuple(y[1])
    if F and G:
        H = F[:-1] + (F[-1] | G[0],) + G[1:]
    else:
        H = F + G
    return (poset_union(x[0], y[0]), H)


hdr("W2a  the Tits product's product-closure failures, classified")
print()
print("  Exhaustive over every ground set I subset [%d], every decomposition"
      % GROUND)
print("  I = S + T, and every pair (x, y) in F[S] x F[T].")
print()

tot = 0
fail_both = fail_empty = 0
both = empty = 0
fail_not_empty_comp = 0
for I, els in universe.items():
    for (S, T) in decompositions(I):
        for x in universe[S]:
            for y in universe[T]:
                tot += 1
                bothsides = bool(S) and bool(T)
                both += bothsides
                empty += (not bothsides)
                z = mu_tits(x, y)
                if z not in els:
                    if bothsides:
                        fail_both += 1
                        if z[1] != ():
                            fail_not_empty_comp += 1
                    else:
                        fail_empty += 1

fail = fail_both + fail_empty
print("  pairs tested                                       %6d" % tot)
print("  product-closure FAILURES                           %6d" % fail)
print("  pairs with BOTH ground sets non-empty              %6d" % both)
print("  pairs with an EMPTY side                           %6d" % empty)
print()
print("   failures with both ground sets non-empty          %6d" % fail_both)
print("   failures with an empty side                       %6d" % fail_empty)
print("   of the failures, ones NOT returning the empty")
print("     composition                                     %6d"
      % fail_not_empty_comp)
print()

checks = [
    ("P1  every failure has both ground sets non-empty", fail_empty == 0),
    ("P2  every both-non-empty pair fails (SET EQUALITY)", fail_both == both),
    ("P3  every failure returns the EMPTY composition",
     fail_not_empty_comp == 0),
    ("P4  the empty-side pairs are non-vacuous and all pass",
     empty > 0 and fail_empty == 0),
]
for label, ok in checks:
    bad += (not ok)
    print("  %-52s %s" % (label, "ok" if ok else "*** MISSED ***"))
print()
print("  So the failure count is not a measurement of how near the Tits")
print("  product comes to being mu_{S,T}.  It is the number of pairs on which")
print("  mu_{S,T} is defined and the Tits product is not, and it would be the")
print("  same number for ANY map that returns the empty composition there.")
print()

hdr("W2b  the CONTROL -- the column separates type-correctness, not nearness")
print()
print("  P5: a type-CORRECT corruption must NOT fire on product closure.")
print()
def mu_tits_unguarded(x, y):
    return (poset_union(x[0], y[0]), tits_product(x[1], y[1]))


for name, mu, expect in (("mu_{S,T}, uncorrupted (concatenation)", mu_hopf, 0),
                         ("control (v): last block of x merged into first"
                          " of y", mu_merge, 0),
                         ("control (ii), the Tits product", mu_tits, both),
                         ("P4b: control (ii) with its guard REMOVED",
                          mu_tits_unguarded, tot - 1)):
    f = 0
    for I, els in universe.items():
        for (S, T) in decompositions(I):
            for x in universe[S]:
                for y in universe[T]:
                    if mu(x, y) not in els:
                        f += 1
    ok = (f == expect)
    bad += (not ok)
    print("  %-54s %6d  %s" % (name, f, "ok" if ok else "*** MISSED ***"))
print()
print("  A wrong product that respects the type fails product closure 0 times")
print("  and a right-shaped product on the wrong type fails it %d times."
      % both)
print("  The column is a TYPE check.  It is not a distance.")
print()

hdr("W2c  what is NOT withdrawn")
print()
print("  The conclusion control (ii) was cited for stands, and this file makes")
print("  it stronger rather than weaker:")
print()
print("    THE BAND PRODUCT IS INVISIBLE TO THE HOPF STRUCTURE.")
print()
print("  mu_{S,T} is defined on factors with DISJOINT ground sets; the Tits")
print("  product intersects blocks; across disjoint sets every intersection is")
print("  empty.  That is a statement about the two maps' domains, true at")
print("  EVERY ground set rather than measured on [4], and no re-count can")
print("  weaken it.  Nothing downstream that cites it -- mg-ebd8's and")
print("  mg-af28's spectral work, lambda_2, Delta_AT -- needs revising.")
print()
print("=" * 78)
print("W2 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
