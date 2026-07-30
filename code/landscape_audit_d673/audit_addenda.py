#!/usr/bin/env python3
"""
mg-d673 INDEPENDENT AUDIT of mg-ebd8 / 714aceb -- addenda.

Small checks that finish the picture:

  A. Jenca-Sarkoci Example 3.7 -- the target says "P = B_2, the 4-element
     Boolean lattice" gives |O(P)| = 11 and 2 spheres, "both hit exactly".
     Recomputed here with my own AC(P) and my own Moebius function.

  B. THE POPULATIONS THE TARGET'S OWN CLAIMS ARE ABOUT.  The document says its
     P1 test covers "all 405 classes at n <= 6" (ledger E3) and that P2
     "passes on 405 posets" (sec 6 item 5).  Neither number is the population
     of the test it is attached to.  Computed here from the target's own
     committed output file.

  C. 922 073 -- the pair count the note's sec 2 sweep and the target both
     quote at n = 5.  Recomputed as sum over the 63 isomorphism classes of
     |F(P)|^2, independently, so a disagreement can surface.

  D. |free LRB on n generators| = sum_k n!/(n-k)! (OEIS A000522) against
     |F(antichain)| = the ordered Bell number (OEIS A000670).  This is what
     makes "a proper submonoid of ours" impossible at the antichain for
     n = 2, 3: the band is bigger than the whole ambient monoid.
"""

import re
import os
from math import factorial

from audit_populations import (iso_classes, F_of_P, AC_by_acyclicity,
                               moebius_bottom_to_top, linear_extensions,
                               is_connected)

print("=" * 78)
print("mg-d673 AUDIT -- ADDENDA")
print("=" * 78)
print()

# --- A. Jenca-Sarkoci Example 3.7 -------------------------------------------
print("-" * 78)
print("A. Jenca-Sarkoci Example 3.7: P = B_2, the 4-element Boolean lattice")
print("   (0 < a, 0 < b, a < 1, b < 1), recomputed with my own instruments")
print("-" * 78)
# elements 0,1,2,3 = bottom, a, b, top
B2 = frozenset({(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)})
ac = AC_by_acyclicity(B2, 4)
mu = moebius_bottom_to_top(ac)
e = len(linear_extensions(B2, 4))
print("   |AC(P)| = |O(P)| = %d      (target/JS say 11)   %s"
      % (len(ac), "OK" if len(ac) == 11 else "*** MISMATCH ***"))
print("   mu(0,1)                 = %d      (target says -2)     %s"
      % (mu, "OK" if mu == -2 else "*** MISMATCH ***"))
print("   spheres = |mu|          = %d      (JS say 2)           %s"
      % (abs(mu), "OK" if abs(mu) == 2 else "*** MISMATCH ***"))
print("   e(P) = %d, connected = %s, sphere dimension n-3 = %d"
      % (e, is_connected(B2, 4), 4 - 3))
print()

# --- B. populations ---------------------------------------------------------
print("-" * 78)
print("B. THE POPULATIONS THE DOCUMENT'S CLAIMS ARE ABOUT")
print("-" * 78)
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "..", "landscape_ebd8", "out_identify_lattice.txt")
rows = []
if os.path.exists(out):
    with open(out) as f:
        for line in f:
            m = re.match(r"^(\d)\s+(\d+)\s+(\d+)\s+(.*)$", line)
            if m:
                rows.append((int(m.group(1)), int(m.group(2)), m.group(4)))
print("   read from the target's OWN committed out_identify_lattice.txt:")
p1 = 0
p2 = 0
for (n, cls, rest) in rows:
    p1 += cls
    if "n/a" not in rest:
        p2 += cls
    print("     n=%d: %3d classes   P2 %s" % (n, cls, "n/a (not run)" if "n/a" in rest else "run"))
print()
print("   P1 population (rows n=2..6)                    = %d" % p1)
print("   P2 population (rows n=3..6; P2 is n/a for n<3) = %d" % p2)
print("   all isomorphism classes with 1 <= n <= 6       = %d"
      % (1 + 2 + 5 + 16 + 63 + 318))
print()
print("   ledger E3 says the two definitions agree 'on all 405 classes at")
print("   n <= 6'                                        -> actual %d   %s"
      % (p1, "OK" if p1 == 405 else "*** the number is %d ***" % p1))
print("   sec 6 item 5 says P2 'passes on 405 posets'    -> actual %d   %s"
      % (p2, "OK" if p2 == 405 else "*** the number is %d ***" % p2))
print()

# --- C. 922 073 -------------------------------------------------------------
print("-" * 78)
print("C. THE PAIR COUNTS, RECOMPUTED (sum over iso classes of |F(P)|^2)")
print("-" * 78)
TARGET_PAIRS = {1: 1, 2: 13, 3: 321, 4: 13853, 5: 922073}
tot = 0
for n in range(1, 6):
    s = sum(len(F_of_P(rel, n)) ** 2 for rel in iso_classes(n))
    tot += s
    t = TARGET_PAIRS[n]
    print("   n=%d: sum |F(P)|^2 = %8d   target/note quote %8d   %s"
          % (n, s, t, "OK" if s == t else "*** MISMATCH ***"))
print("   total over n=1..5                    = %d" % tot)
print("   (the document's sec 0 and its L2 table quote '922 073 pairs' as the")
print("    n <= 5 figure; 922 073 is the n = 5 ROW.  The n <= 5 total is %d.)"
      % tot)
print()

# --- D. free LRB vs ordered Bell -------------------------------------------
print("-" * 78)
print("D. |free LRB on n generators| vs |F(antichain)| = ordered Bell number")
print("-" * 78)
print("%4s %14s %18s %10s" % ("n", "free LRB (A000522)", "F(antichain) (A000670)",
                              "band bigger?"))
for n in range(1, 7):
    fl = sum(factorial(n) // factorial(n - k) for k in range(n + 1))
    ob = len(F_of_P(frozenset(), n)) if n <= 5 else 4683
    print("%4d %14d %18d %10s" % (n, fl, ob, "YES" if fl > ob else "no"))
print()
print("   The document says Bjorner's greedoid band at the antichain 'is the")
print("   free LRB' AND is 'a proper submonoid of ours', in the same table")
print("   cell.  At n = 2 and n = 3 the free LRB is strictly LARGER than the")
print("   whole of F(antichain), so it cannot be a submonoid of it.")
print()
print("=" * 78)
