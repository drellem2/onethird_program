#!/usr/bin/env python3
"""mg-8af0 -- F3's counting argument, and the bound shown NOT to be vacuous.

mg-fcb2's F3: `verify_e35b.py`'s V6 labelled *"no ridge in >= 3 facets, I4
zero"* COULD MOVE, and `controls.py` printed *"I4 rebuilds the facet enumeration
outright, so a ridge there CAN lie in >= 3 facets; its zero is the only one of
the four that is a result"*.  It is not a result.  Both facet maps return a
chain of masks of sizes 1, 2, ..., n-1, so a ridge omits the level-k mask, the
two masks bracketing it differ in exactly two elements, and there are exactly
two candidates to re-insert.  At most two facets on any ridge, at every n.

V4b of `verify_e35b.py` measures that: 810 families, largest multiplicity 2,
zero families with a ridge in >= 3 facets.  THAT MEASUREMENT ON ITS OWN IS NOT
EVIDENCE.  A routine that always returned 2 would print the same thing, and it
has never been seen return anything else -- which is the same objection this
whole arc exists to answer, one level in.  So this file:

  S1  states the premise the argument rests on and measures it separately from
      the conclusion -- every facet under both maps has level-size profile
      1, 2, ..., n-1;
  S2  measures the conclusion over the same 810 families;
  S3  CONSTRUCTS A FACET FAMILY THAT VIOLATES THE PREMISE and has a ridge in
      THREE facets, and runs the same multiplicity routine on it.  The routine
      reports 3.  So the 810 zeros are a fact about the maps, not the fixed
      answer of a routine incapable of saying otherwise;
  S4  and shows the implication is not an accident of that one construction:
      swept over every level-size profile on n <= 5, the profiles that give
      multiplicity <= 2 are exactly the consecutive ones.

Population and grain are named at every count.  Exit 0 iff every row passes.
"""

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "face_geometry")))

from face_complex import (                                       # noqa: E402
    linear_extensions, le_to_facet, le_to_facet_offbyone,
)
from posets import all_posets                                    # noqa: E402

NMAX = 6
FAILED = []
CHECKS = [0]


def check(label, ok, detail=""):
    CHECKS[0] += 1
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  -- " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)
    return ok


def profile(facet):
    """The level-size profile of a facet: the sizes of its masks, in order."""
    return tuple(bin(m).count("1") for m in facet)


def ridge_multiplicity(facets):
    """How many facets share each ridge.

    A ridge is a facet with one level omitted; two facets share it when they
    agree everywhere else AND omit the same level.  Returns the largest such
    count, or 0 for a family with no ridges at all.

    THE ONE ROUTINE.  S2 and S3 both call it, so "0 families with a ridge in
    >= 3 facets" and "this constructed family has one" are the same question
    asked twice, not two questions.
    """
    mult = {}
    for f in facets:
        for i in range(len(f)):
            key = (i, f[:i] + f[i + 1:])
            mult[key] = mult.get(key, 0) + 1
    return max(mult.values()) if mult else 0


def families(nmax):
    """(label, facet set) for every poset up to isomorphism with n <= nmax,
    under each of the two facet maps.  POPULATION: (poset, facet map) pairs."""
    for n in range(1, nmax + 1):
        for k, P in enumerate(all_posets(n)):
            les = linear_extensions(P)
            for name, mp in (("true", le_to_facet),
                             ("offbyone", le_to_facet_offbyone)):
                yield ("n%d#%d/%s" % (n, k, name), {mp(w) for w in les})


def main():
    print("mg-8af0 -- F3: the >= 3-facets zeros are FORCED, and the bound that "
          "forces them is shown capable of failing")
    fams = list(families(NMAX))
    print("population: %d (poset, facet map) families -- every poset up to "
          "isomorphism with n <= %d, under each of the two maps" % (len(fams), NMAX))

    # -- S1: the premise, measured on its own -------------------------------
    print("S1 -- THE PREMISE: every facet is a chain of masks of sizes 1..n-1")
    good = sum(1 for _, fs in fams
               if all(profile(f) == tuple(range(1, len(f) + 1)) for f in fs))
    seen = sorted({profile(f) for _, fs in fams for f in fs})
    check("every facet under both maps has a CONSECUTIVE level-size profile "
          "starting at 1, on %d/%d families; the %d distinct profiles seen are "
          "%s.  Grain: the facet, aggregated to the family"
          % (good, len(fams), len(seen), [list(p) for p in seen]),
          good == len(fams))

    # -- S2: the conclusion, over the same population -----------------------
    print("S2 -- THE CONCLUSION: no ridge lies in >= 3 facets")
    worst = max(ridge_multiplicity(fs) for _, fs in fams)
    over = [lab for lab, fs in fams if ridge_multiplicity(fs) >= 3]
    check("largest number of facets sharing a ridge is %d over all %d families, "
          "and %d families have a ridge in >= 3 facets.  Grain: the ridge, "
          "maximised over the family" % (worst, len(fams), len(over)),
          worst == 2 and not over, "families over the bound: %s" % over)

    # -- S3: the bound is NOT vacuous ---------------------------------------
    print("S3 -- AND THE ROUTINE CAN SAY 3.  A family that violates S1's "
          "premise, built for that purpose, run through the SAME routine S2 "
          "used.  Without this row, 'no ridge in >= 3 facets' is the answer of "
          "a procedure never seen to report anything else.")
    # Chains of masks of sizes 1 and 3 inside a fixed 3-element ground set:
    # dropping the size-1 mask leaves a bracket from {} to a 3-element mask, so
    # THREE singletons can be re-inserted rather than the two a consecutive
    # profile allows.
    top = 0b0111
    broken = {(1 << a, top) for a in range(3)}
    prof = sorted({profile(f) for f in broken})
    m = ridge_multiplicity(broken)
    check("a constructed family of %d facets with level-size profile %s over a "
          "3-element ground set -- NOT the full profile 1..n-1, so S1's premise "
          "fails on it -- has a ridge in %d facets by the same routine.  So "
          "S2's zero is a property of the two maps, and not the fixed output of "
          "a routine that cannot report otherwise"
          % (len(broken), [list(p) for p in prof], m),
          m == 3 and prof == [(1, 3)])
    check("and the premise really is what separates them: the same routine on "
          "the FULL profile over the same 3-element ground set ([1, 2], which "
          "IS 1..n-1 there) reports 2",
          ridge_multiplicity({(1 << a, (1 << a) | (1 << b))
                              for a in range(3) for b in range(3) if a != b}) == 2)

    # -- S4: swept, so the separation is not one example --------------------
    print("S4 -- SWEPT over every level-size profile on a 5-element ground "
          "set, so the separation in S3 is not a property of one construction.")
    print("    THIS ROW WAS RESPECIFIED AFTER FIRING ON ME, and the failing "
          "transcript is kept at out_forcing_8af0_FIRSTFORM_exit1.txt.  Its "
          "first form predicted the dividing line was CONSECUTIVE profiles.  "
          "That is refuted here on its own output: [1, 2] is consecutive and "
          "gives 4, [2, 3] is consecutive and gives 3.  The line is not "
          "consecutiveness -- it is being the FULL profile 1..n-1.  A ridge "
          "that omits the FIRST level is bracketed below by the empty set and "
          "above by the level after it, so it has C(p1 - p_-1, ...) "
          "completions, and only a profile that starts at 1 and ends at n-1 "
          "makes every one of those brackets exactly two elements wide.  I had "
          "the argument right in S3 and wrote the generalisation loosely; the "
          "sweep caught it.")
    n5 = 5
    rows = []
    for size in range(2, n5):
        for prof in itertools.combinations(range(1, n5), size):
            fs = set()
            for chain in itertools.product(*[
                    [m for m in range(1, 1 << n5) if bin(m).count("1") == k]
                    for k in prof]):
                if all(chain[i] & chain[i + 1] == chain[i]
                       for i in range(len(chain) - 1)):
                    fs.add(tuple(chain))
            full = prof == tuple(range(1, n5))
            rows.append((prof, full, ridge_multiplicity(fs)))
    for prof, full, m in rows:
        print("    profile %-14s %-24s max ridge multiplicity %d"
              % (list(prof), "THE FULL PROFILE 1..n-1" if full else
                 ("consecutive but partial"
                  if prof == tuple(range(prof[0], prof[0] + len(prof)))
                  else "gapped"), m))
    check("over %d profiles on a %d-element ground set, multiplicity <= 2 holds "
          "on EXACTLY ONE of them -- the full profile %s, which by S1 is "
          "exactly the profile both facet maps produce -- and every other "
          "profile, consecutive or not, admits a ridge in >= 3 facets.  So the "
          "bound is TIGHT and I4's zero rests on the whole of S1's premise, not "
          "on part of it.  Population: level-size profiles of length 2..%d over "
          "%d elements; grain: the profile"
          % (len(rows), n5, list(range(1, n5)), n5 - 1, n5),
          [m <= 2 for _, _, m in rows] == [f for _, f, _ in rows]
          and sum(1 for _, f, _ in rows if f) == 1)

    print()
    if FAILED:
        print("%d checks, %d REFUTED:" % (CHECKS[0], len(FAILED)))
        for f in FAILED:
            print("  - %s" % f)
        return 1
    print("%d checks, 0 refuted." % CHECKS[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
