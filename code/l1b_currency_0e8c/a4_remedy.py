#!/usr/bin/env python3
"""mg-0e8c a4 -- THE FROZEN BOUNDARY, AND THE REMEDY CHECKED AGAINST ITS OWN DEFECT.

TWO JOBS.

  D1  THE FROZEN BOUNDARY.  a3/C2 found the frozen class at n <= 6 is EXACTLY the chains.  That
      is a fact about small n and it must be stated with the number that says HOW FAR small n is
      from the regime -- `min delta over posets carrying an incomparable pair` -- because
      "frozen is empty at n <= 6" invites the reading that frozen is nearly reachable there, and
      the distance is the only thing that settles it.

  D2  THE REMEDY IS AN ARTIFACT OF THE SAME KIND AS THE DEFECT.  The defect is a wall stated in
      a form its own proven constant discharges.  So the restatement must be checked against
      exactly that: does `eps_sup` discharge the RESTATED row?  If the restatement names a bar
      -- `eps <= eps_dem` -- then the check is whether the proven constant clears it, and the
      answer must be NO or the restatement has reproduced the defect it repairs.

      The check is one comparison and it is trivial arithmetic.  It is here anyway, because the
      failure being guarded against is not that the arithmetic is hard; it is that nobody runs
      it.  The original row was written by people who knew both numbers.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib0e8c as L                                        # noqa: E402

print("=" * 78)
print("mg-0e8c a4 -- THE FROZEN BOUNDARY, AND THE REMEDY AGAINST ITS OWN DEFECT")
print("=" * 78)

# ---- D1 --------------------------------------------------------------------------------
print("""
D1  THE FROZEN BOUNDARY.  delta(P) = max over incomparable pairs of min(p, 1-p); frozen is
    delta < 1/3 STRICT.  A chain has no incomparable pair, so its max is over the empty set and
    `frozen` is vacuous there.  The column that matters is the last one.
""")
print("   n   posets   frozen   frozen with >=1 incomparable pair   min delta over such posets")
for n in range(2, 7):
    tot = froz = froz_nt = 0
    dmin, dmin_rel = None, None
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        d, ninc = L.delta_P(n, exts, rel)
        tot += 1
        if d < Fraction(1, 3):
            froz += 1
            if ninc > 0:
                froz_nt += 1
        if ninc > 0 and (dmin is None or d < dmin):
            dmin, dmin_rel = d, rel
    print("   %d   %-8d %-8d %-34d %s  (= %.4f, at rel %s)"
          % (n, tot, froz, froz_nt, dmin, float(dmin), sorted(dmin_rel)))

print("""
  READING.  The frozen class at n <= 6 is EXACTLY the chains, and the distance to the boundary is
  ZERO AND STILL EXCLUDING: from n = 3 on, the most-decided poset carrying any incomparable pair
  sits at delta = 1/3 EXACTLY -- ON the boundary, and `frozen` is delta < 1/3 STRICT, so it is
  outside the hypothesis by the same hair that puts the eta = 0 witness outside M_n(eta)
  (STATE.md:21's restored eta).  It is not that small n nearly reaches frozen and misses by a
  margin; it reaches the boundary exactly and the strictness excludes it.  That is the honest
  scope line for every frozen census in this repository at these n -- including a3/C2's
  zero-violation result, which is a measurement over the CHAINS and says nothing whatever about
  a real frozen poset.

  THIS DOES NOT WEAKEN THE VERDICT.  The discharge of row 8 by eps_sup is Op-Form Claim 6.1 plus
  the master bound, both proven for all n; neither consumes this population.  The census is here
  so that no reader mistakes a3/C2's green for evidence about frozen posets.
""")

# ---- D2 --------------------------------------------------------------------------------
print("-" * 78)
print("""
D2  THE REMEDY, CHECKED AGAINST THE DEFECT IT REPAIRS.

    THE DEFECT.  Row 8 as stated:  frozen => `1 - lambda_std <= eps_spec` for an EXPLICIT
    ABSOLUTE CONSTANT, UNIFORM IN n.  Is it discharged by the proven constant?
""")
eps_sup = Fraction(1)
eps_dem = Fraction(2, 100)


def verdict(label, discharged):
    print("      %-58s %s" % (label, "DISCHARGED by eps_sup" if discharged
                              else "NOT discharged by eps_sup"))


print("      proven constant eps_sup < %s (Op-Form Claim 6.1, all n, L4-independent)" % eps_sup)
print()
verdict("row 8 AS STATED   (an explicit absolute constant exists)", True)
print("          -- because eps_sup IS such a constant.  The row asks for existence; existence")
print("             is proven.  And at eps = 1 the spectral half is VACUOUS besides (a2).")
print()
print("    THE RESTATEMENT.  frozen => `E[inv_e] <= (eps/6)(n^2-1)` for a constant eps <= eps_dem.")
verdict("row 8 RESTATED    (a constant at or below eps_dem = %s)" % eps_dem,
        eps_sup <= eps_dem)
print("          -- because eps_sup = %s > eps_dem = %s, by a factor of %s."
      % (eps_sup, eps_dem, eps_sup / eps_dem))
print("""
    SO THE RESTATEMENT DOES NOT REPRODUCE THE DEFECT.  The proven constant fails the restated
    row's bar by ~50x, which is precisely the quantity that is open.  A reader who checks
    whether we have a uniform constant now finds that we do AND that the row does not ask for
    one -- which is the whole repair.

    AND THE RESTATEMENT IS IN THE INVERSION FORM, NOT THE SPECTRAL ONE, FOR A SECOND REASON
    a2 supplies: at any eps the spectral form is the WEAKER of the two (the master bound runs
    inversions -> spectrum, one way, a3/C3), so stating the wall spectrally states less than the
    architecture consumes.  At the proven constant it states nothing at all.
""")
