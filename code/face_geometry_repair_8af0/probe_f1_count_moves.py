#!/usr/bin/env python3
"""mg-8af0 -- the two inputs that move the repaired site count, constructed.

mg-fcb2's F1: the coverage sentence in NEGATIVE CONTROL 4 read

    "the named load-bearing site is corrupted on %d/%d posets" % (N, N, ...)

-- THE SAME EXPRESSION TWICE.  It printed 86/86 on the shipped population, and
it would have printed 86/86 with the corruption deleted.  mg-8af0 replaces the
numerator with `mutation_applied_at_site` asked of every poset.  On the shipped
population the digits DO NOT CHANGE (86/86 before, 86/86 after), which is why
no reader could have caught this from the artifact and why fixing the string
without fixing the verifier that was supposed to enumerate it would have been
worthless.  This file is where the difference is visible.

TWO CONSTRUCTED INPUTS, both of them things the number is supposed to be about:

  A  ADMIT n = 1.  `le_to_facet` takes the prefixes w[:1..n-1] and
     `le_to_facet_offbyone` the prefixes of w[1:]; on a one-letter word BOTH
     return the empty chain, so the site is not corrupted there.  Truth over
     1 <= n <= 5: 86 of 87.  The tautology prints 87/87 -- a FALSE SENTENCE,
     not merely an unmovable one.
  B  MAKE THE CORRUPTION A NO-OP.  With `le_to_facet_offbyone` bound to
     `le_to_facet`, nothing at the site is corrupted at all.  Truth: 0 of 86.
     The tautology prints 86/86.

POPULATION and GRAIN, for every count below: a set of posets up to isomorphism
(86 for 2 <= n <= 5, 87 for 1 <= n <= 5); one poset per unit.  "Corrupted at
the site" means the facet LIST built under `facet_offbyone` differs from the
true one -- the same question `mutation_applied_at_site` asks, rebuilt here
from `top_laplacians` so that this file does not inherit an answer from the
function it is checking.

Exit 0 iff all six cells come out as stated.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))
sys.path.insert(0, PROBE)

import face_complex                                             # noqa: E402
from face_complex import top_laplacians                         # noqa: E402
from posets import all_posets                                   # noqa: E402

MODE = "facet_offbyone"


def site_corrupted(ps):
    """The repaired numerator: posets whose facet LIST the off-by-one changes."""
    return sum(1 for P in ps
               if top_laplacians(P, incidence_mode=MODE)["facets"]
               != top_laplacians(P)["facets"])


def tautology(ps):
    """The numerator as mg-e35b shipped it: the denominator, again."""
    return len(ps)


def main():
    rows = []

    base = [P for n in range(2, 6) for P in all_posets(n)]
    rows.append(("SHIPPED  2 <= n <= 5", tautology(base), site_corrupted(base),
                 len(base), 86,
                 "the digits agree -- this is why the artifact could not "
                 "reveal the defect"))

    wide = [P for n in range(1, 6) for P in all_posets(n)]
    rows.append(("A  n = 1 ADMITTED, 1 <= n <= 5", tautology(wide),
                 site_corrupted(wide), len(wide), 86,
                 "both facet maps return the empty chain at n = 1, so the "
                 "tautology's SENTENCE is false, not just unmovable"))

    orig = face_complex.le_to_facet_offbyone
    face_complex.le_to_facet_offbyone = face_complex.le_to_facet
    try:
        rows.append(("B  CORRUPTION MADE A NO-OP", tautology(base),
                     site_corrupted(base), len(base), 0,
                     "nothing at the site is corrupted; the tautology still "
                     "reports the whole population"))
    finally:
        face_complex.le_to_facet_offbyone = orig

    print("mg-8af0 -- the site count, as shipped and as repaired, on three "
          "populations")
    print("grain: one poset.  'corrupted' = the facet LIST built under "
          "facet_offbyone differs from the true one.")
    print()
    print("  %-30s %-14s %-14s %s" % ("population", "tautology", "measured",
                                      "note"))
    bad = []
    for label, taut, meas, n, want, note in rows:
        print("  %-30s %-14s %-14s %s"
              % (label, "%d/%d" % (taut, n), "%d/%d" % (meas, n), note))
        if meas != want:
            bad.append("%s: measured %d, stated %d" % (label, meas, want))
        if taut != n:
            bad.append("%s: the tautology did not print n/n (%d/%d)"
                       % (label, taut, n))

    print()
    print("  THE TAUTOLOGY PRINTS n/n ON ALL THREE.  The measured numerator "
          "moves on two of the three, and on population A the two answers "
          "DISAGREE (86 vs 87): the shipped sentence was false there, which is "
          "the half of mg-fcb2's F1 that a count-cannot-move finding does not "
          "by itself establish.")
    print("  NOT SHOWN HERE: that 86/86 is the right answer on the shipped "
          "population for the right reason.  It is re-derived independently in "
          "verify_e35b.py's V7 from the same definition; two routes to one "
          "number is what that row is, and it is not a proof that the "
          "definition is the one the sentence should be using.")

    if bad:
        print()
        print("%d cells came out other than stated:" % len(bad))
        for b in bad:
            print("  - %s" % b)
        return 1
    print()
    print("6/6 cells as stated (PREDICTIONS.md E1, E2, E3).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
