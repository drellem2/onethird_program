#!/usr/bin/env python3
"""mg-8af0 -- the "no ridge in >= 3 facets" zeros are FORCED on ALL FOUR rows.

mg-fcb2's F3 (unpredicted by that audit's own predictions, and the one finding
of the three that is about the MATHEMATICS rather than about an instrument):
mg-e35b labelled I4's zero COULD MOVE and wrote that it "is the only one of the
four that is a result".  It cannot move at any n.

THE FORCING, in two cases, because one case does not cover it.

  n >= 3.  Every facet built by `le_to_facet` OR by `le_to_facet_offbyone` is a
    strictly increasing chain of masks of sizes 1, 2, ..., n-1 -- the first
    takes the prefixes of w[:-1], the second the prefixes of w[1:], and both
    are prefix families.  A ridge is such a chain with the level of some size k
    deleted.  A facet containing that ridge is the ridge with a mask of size k
    re-inserted, and it must sit between the surviving levels of sizes k-1 and
    k+1 (taking size 0 to be the empty set and size n to be the full set).
    Those two sets differ in exactly two elements, so there are EXACTLY TWO
    candidates.  Hence no ridge lies in more than 2 facets -- for either map,
    under any of the four mutations, at every n >= 3.

  n = 2.  THE ARGUMENT ABOVE DOES NOT APPLY, and mg-8af0's brief stated the
    forcing as if it did (PREDICTIONS.md E4 recorded that before this file was
    written).  A facet is a chain of length 1, its unique ridge is the EMPTY
    chain, and every facet contains it -- there is no "level to re-insert".
    The bound holds for a different reason: |L(P)| <= 2 when n = 2, so there
    are at most 2 facets in total.

Both halves are checked below rather than argued: the PREMISE (every facet is a
chain of masks of sizes 1..n-1) and the BOUND (no ridge lies in >= 3 facets),
over every mode and every poset 2 <= n <= 6.

POPULATION and GRAIN.  Two populations, and they are different:
  * the 404 posets up to isomorphism with 2 <= n <= 6, times 5 incidence modes
    plus the uncorrupted build = 2424 (poset, mode) builds.  Grain: one build,
    for the maximum-multiplicity figure.
  * the facets those builds produce.  Grain: one facet, for the premise.
The brief's "810 families over n <= 6" is a THIRD population -- 405 posets with
1 <= n <= 6 times the 2 facet maps -- and is reproduced separately below so
that the number in the brief and the numbers here are not confused.

Exit 0 iff the premise holds everywhere and the maximum multiplicity is 2.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))
sys.path.insert(0, PROBE)

from face_complex import (                                       # noqa: E402
    top_laplacians, le_to_facet, le_to_facet_offbyone, linear_extensions,
)
from posets import all_posets                                    # noqa: E402

MODES = ["true", "ridge_facets", "split_free_as_interior", "ridge_drop",
         "facet_offbyone", "facet_swap01"]
TAGS = {"true": "(uncorrupted)", "ridge_facets": "I1",
        "split_free_as_interior": "I2", "ridge_drop": "I3",
        "facet_offbyone": "I4", "facet_swap01": "swap01"}
NMAX = 6


def main():
    print("mg-8af0 -- ridge multiplicity under every incidence mode, 2 <= n <= %d"
          % NMAX)

    builds = 0
    facets_seen = 0
    premise_bad = []
    per_mode_max = {m: 0 for m in MODES}
    ge3 = {m: 0 for m in MODES}
    degenerate_n2 = 0

    for n in range(2, NMAX + 1):
        for P in all_posets(n):
            for mode in MODES:
                td = top_laplacians(P, incidence_mode=mode)
                builds += 1
                for f in td["facets"]:
                    facets_seen += 1
                    sizes = [bin(m).count("1") for m in f]
                    if sizes != list(range(1, n)):
                        premise_bad.append((n, mode, f))
                mult = max((len(v) for v in td["ridge_facets"].values()),
                           default=0)
                per_mode_max[mode] = max(per_mode_max[mode], mult)
                ge3[mode] += sum(1 for v in td["ridge_facets"].values()
                                 if len(v) >= 3)
            if n == 2 and len(linear_extensions(P)) == 2:
                degenerate_n2 += 1

    print("  builds: %d (poset, mode) pairs over %d posets x %d modes; facets "
          "examined: %d" % (builds, builds // len(MODES), len(MODES),
                            facets_seen))
    print()
    print("  %-14s %-24s %s" % ("mode", "max ridge multiplicity",
                                "ridges in >= 3 facets"))
    for m in MODES:
        print("  %-14s %-24d %d" % (TAGS[m], per_mode_max[m], ge3[m]))
    print()
    print("  PREMISE (every facet is a chain of masks of sizes 1..n-1): %d "
          "violations over %d facets" % (len(premise_bad), facets_seen))
    print("  n = 2 DEGENERATE CASE (unique ridge is the empty chain, contained "
          "in every facet): %d poset with 2 facets -- the bound there is "
          "|L(P)| <= 2, not the two-re-insertions argument" % degenerate_n2)

    # The brief's number, on the brief's population, kept separate on purpose.
    fam = 2 * sum(len(all_posets(n)) for n in range(1, NMAX + 1))
    print("  mg-8af0's brief says '810 families over n <= 6': %d posets with "
          "1 <= n <= 6 x 2 facet maps = %d.  Different population from the two "
          "above; reproduced here so the three are not read as one."
          % (fam // 2, fam))

    ok = (not premise_bad
          and all(per_mode_max[m] == 2 for m in MODES)
          and all(ge3[m] == 0 for m in MODES))
    print()
    print("  CONCLUSION: the zero is FORCED for I4 exactly as it is for "
          "I1/I2/I3, and mg-e35b's 'its zero is the only one of the four that "
          "is a result' is REFUTED.  What is NOT shown here: that the bound "
          "holds for n > 6.  The argument in the docstring is general and the "
          "sweep is not; the sweep is what makes the PREMISE a checked fact "
          "rather than a reading of two functions.")
    if not ok:
        print("REFUTED: premise violations %d; per-mode max %s; >=3 counts %s"
              % (len(premise_bad), per_mode_max, ge3))
        return 1
    print("  premise 0 violations, maximum multiplicity 2 on every mode.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
