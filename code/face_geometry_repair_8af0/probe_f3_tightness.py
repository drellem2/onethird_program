#!/usr/bin/env python3
"""mg-36f5 -- F3's bound is TIGHT, and the routine that reports it CAN report 3.

PORTED from `polecat-z8af0`'s `forcing_8af0.py` (branch commit a82acb3, S3 and
S4), which was re-derived in parallel with this repair and never routed
anywhere.  See README.md, section "F3 — the bound is tight".  Two things on
that branch are not on main and are not implied by anything on main:

  (1) THE BOUND IS TIGHT AND "CONSECUTIVE" IS NOT THE DIVIDING LINE.
      `probe_f3_ridge_multiplicity.py` measures the PREMISE (every facet is a
      chain of masks of sizes 1..n-1) and it measures the BOUND (no ridge in
      >= 3 facets).  Neither of them, nor `verify_e35b.py`'s V4c, asks whether
      the premise can be WEAKENED -- so "the zero is forced by the premise" is
      on main with no measurement of how much of the premise it needs.  Swept
      over every level-size profile at n = 3, 4, 5 and 6, multiplicity <= 2
      holds on EXACTLY ONE profile at each n: the full profile 1..n-1.  At
      n = 5, [1, 2] is consecutive and gives 4 and [2, 3] is consecutive and
      gives 3, so the line is not consecutiveness.  I4's zero rests on the
      WHOLE of the premise, and the generalisation "consecutive profiles are
      enough" is closed rather than left looking open.

      z8af0's S4 was RESPECIFIED after firing on its author: its first form
      predicted the dividing line WAS consecutiveness, and the sweep refuted
      it on its own output.  That history is why the row is stated the way it
      is here, and the branch kept its failing transcript
      (`out_forcing_8af0_FIRSTFORM_exit1.txt`, branch commit a82acb3).

  (2) A NEGATIVE CONTROL ON THE MULTIPLICITY ROUTINE.  Main's
      "0 families with a ridge in >= 3 facets" is, on main today, the answer of
      a procedure that has never been observed to say anything else.  A routine
      that returned 2 unconditionally would print every number main prints.
      T2 constructs a family the routine reports 3 on.

WHAT THIS FILE DOES THAT z8af0's DID NOT, and why it is not optional.  z8af0
ran its control through a ridge-multiplicity routine it had written itself.  A
control on a private re-implementation does not observe THE PUBLISHED ROUTINE
reporting 3, so it leaves the published zero exactly as unwitnessed as it found
it -- the same defect one level up, which is this repair's own subject matter.
So `ridge_multiplicity` below is a thin wrapper over `face_complex.boundary_matrix`,
the function `top_laplacians` itself calls, and T1 MEASURES the wrapper against
`top_laplacians`'s own `ridge_facets` on all 2424 real builds rather than
asserting they agree.  T1 is the row that makes T2 mean anything.

POPULATION and GRAIN, three of them and they are different:
  * T1: the 404 posets with 2 <= n <= 6 x 6 incidence modes = 2424 builds.
    Grain: one build (its maximum ridge multiplicity, two ways).
  * T2: two constructed facet families over a 3-element ground set.  Grain: the
    family.
  * T3/T4: level-size profiles of length >= 2 over an n-element ground set,
    n = 3..6 (1 + 4 + 11 + 26 = 42 profiles).  Grain: one profile.

Exit 0 iff every row passes.
"""

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "face_geometry")))

from face_complex import (                                       # noqa: E402
    boundary_matrix, top_laplacians,
)
from posets import all_posets                                    # noqa: E402

MODES = ["true", "ridge_facets", "split_free_as_interior", "ridge_drop",
         "facet_offbyone", "facet_swap01"]
TAGS = {"true": "(uncorrupted)", "ridge_facets": "I1",
        "split_free_as_interior": "I2", "ridge_drop": "I3",
        "facet_offbyone": "I4", "facet_swap01": "swap01"}
NMAX = 6
SWEEP_NS = (3, 4, 5, 6)

FAILED = []
CHECKS = [0]


def check(label, ok, detail=""):
    CHECKS[0] += 1
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  -- " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)
    return ok


def ridge_multiplicity(facets):
    """The largest number of facets sharing a ridge, THROUGH THE LIBRARY.

    This is `top_laplacians`'s own computation with the poset removed from in
    front of it: ridges are the (n-3)-faces obtained by deleting one level from
    a facet, the incidence is `boundary_matrix` -- the same function, not a copy
    of it -- and a ridge's facet list is that row's column keys.  T1 measures
    the agreement; nothing here asserts it.

    Takes any set of equal-length chains, which is the point: no poset produces
    a family that violates the premise, so a control has to be built by hand.
    """
    faces = sorted(set(facets))
    ridge_set = set()
    for f in faces:
        for i in range(len(f)):
            ridge_set.add(f[:i] + f[i + 1:])
    M, _nr, _nc = boundary_matrix(faces, sorted(ridge_set))
    return max((len(row) for row in M.values()), default=0)


def profile(facet):
    """The level-size profile of a facet: the sizes of its masks, in order."""
    return tuple(bin(m).count("1") for m in facet)


def chains_with_profile(n, prof):
    """Every strictly increasing chain of masks over an n-element ground set
    whose level sizes are exactly `prof`."""
    levels = [[m for m in range(1, 1 << n) if bin(m).count("1") == k]
              for k in prof]
    out = set()
    for chain in itertools.product(*levels):
        if all(chain[i] & chain[i + 1] == chain[i]
               for i in range(len(chain) - 1)):
            out.add(tuple(chain))
    return out


def sweep(n):
    """(profile, is_full, max multiplicity, family size) for every profile of
    length >= 2.

    The family size is carried because an EMPTY family has multiplicity 0,
    which is <= 2, so a sweep that silently built nothing would pass the
    tightness rows below while measuring nothing at all.  It is checked, not
    assumed."""
    rows = []
    for size in range(2, n):
        for prof in itertools.combinations(range(1, n), size):
            fs = chains_with_profile(n, prof)
            rows.append((prof, prof == tuple(range(1, n)),
                         ridge_multiplicity(fs), len(fs)))
    return rows


def kind(prof, n):
    if prof == tuple(range(1, n)):
        return "THE FULL PROFILE 1..n-1"
    if prof == tuple(range(prof[0], prof[0] + len(prof))):
        return "consecutive but partial"
    return "gapped"


def main():
    print("mg-36f5 -- F3: the >= 3-facet bound is TIGHT, and the routine that "
          "reports it is shown reporting 3")

    # -- T1: the control's routine IS the published routine ------------------
    print("T1 -- CALIBRATION.  `ridge_multiplicity` below vs `top_laplacians`'s "
          "own `ridge_facets`, on every real build.  Without this row the "
          "control in T2 is a fact about a private re-implementation.")
    builds = 0
    disagree = {m: [] for m in MODES}
    for n in range(2, NMAX + 1):
        for k, P in enumerate(all_posets(n)):
            for mode in MODES:
                td = top_laplacians(P, incidence_mode=mode)
                builds += 1
                published = max((len(v) for v in td["ridge_facets"].values()),
                                default=0)
                wrapped = ridge_multiplicity(td["facets"])
                if published != wrapped:
                    disagree[mode].append((n, k, len(td["les"]),
                                           published, wrapped))
    for m in MODES:
        print("    %-14s %d disagreement(s) over %d builds"
              % (TAGS[m], len(disagree[m]), builds // len(MODES)))
    quiet = [m for m in MODES if m != "ridge_drop"]
    check("the wrapper reproduces the published incidence EXACTLY on %d of the "
          "%d builds under all five modes that leave the incidence bookkeeping "
          "alone (%s).  Population: %d posets 2 <= n <= %d x %d modes; grain: "
          "one build"
          % (builds - builds // len(MODES), builds,
             ", ".join(TAGS[m] for m in quiet), builds // len(MODES), NMAX,
             len(MODES)),
          all(not disagree[m] for m in quiet),
          "disagreements: %s" % {TAGS[m]: disagree[m] for m in quiet
                                 if disagree[m]})
    rd = disagree["ridge_drop"]
    check("and I3 `ridge_drop` disagrees on EXACTLY %d builds, BY CONSTRUCTION "
          "and only DOWNWARD: that mode deletes a ridge row AFTER the incidence "
          "is computed, and on every one of the %d the deleted ridge was the "
          "only multiplicity-2 ridge there is -- all %d have |L(P)| = 2, and "
          "the published figure is BELOW the wrapper's on every one.  So the "
          "one place the two routines differ cannot manufacture a >= 3"
          "AND THIS IS WHY T1 IS NOT A TAUTOLOGY: a calibration row that "
          "compared a value with itself could not have produced these 15, so "
          "the agreement above is an observation and not a restatement"
          % (len(rd), len(rd), len(rd)),
          len(rd) == 15
          and all(les == 2 for _n, _k, les, _p, _w in rd)
          and all(p < w for _n, _k, _les, p, w in rd),
          "|L(P)| values %s; (published, wrapper) pairs %s"
          % (sorted({les for _n, _k, les, _p, _w in rd}),
             sorted({(p, w) for _n, _k, _les, p, w in rd})))

    # -- T2: the routine can say 3 -------------------------------------------
    print("T2 -- NEGATIVE CONTROL.  A family that VIOLATES the premise, built "
          "for that purpose, through the routine T1 just calibrated.  Main's "
          "'0 ridges in >= 3 facets' is otherwise the answer of a procedure "
          "never observed to report anything else.")
    # Chains of masks of sizes 1 and 3 in a 3-element ground set: dropping the
    # size-1 level leaves a bracket from the empty set to a 3-element mask, so
    # THREE singletons can be re-inserted where the full profile allows two.
    top = 0b0111
    broken = {(1 << a, top) for a in range(3)}
    broken_prof = sorted({profile(f) for f in broken})
    m_broken = ridge_multiplicity(broken)
    check("a family of %d facets with level-size profile %s over a 3-element "
          "ground set -- NOT the full profile 1..n-1, so the premise fails on "
          "it -- has a ridge in %d facets.  THE ZERO IS A PROPERTY OF THE FACET "
          "MAPS AND NOT THE FIXED OUTPUT OF THE ROUTINE"
          % (len(broken), [list(p) for p in broken_prof], m_broken),
          m_broken == 3 and broken_prof == [(1, 3)])
    full3 = chains_with_profile(3, (1, 2))
    m_full3 = ridge_multiplicity(full3)
    check("and the premise is what separates them: the FULL profile [1, 2] "
          "over the SAME 3-element ground set, same routine, reports %d"
          % m_full3, m_full3 == 2)

    # -- T3: the tightness sweep, at the branch's n --------------------------
    print("T3 -- TIGHTNESS at n = 5, the sweep z8af0 ran.  Every level-size "
          "profile, not one construction.")
    rows5 = sweep(5)
    for prof, _full, m, sz in rows5:
        print("    profile %-14s %-24s %3d facets   max ridge multiplicity %d"
              % (list(prof), kind(prof, 5), sz, m))
    check("over %d profiles on a 5-element ground set, multiplicity <= 2 holds "
          "on EXACTLY ONE -- the full profile %s, which is exactly the profile "
          "both facet maps produce -- so the bound is TIGHT and I4's zero rests "
          "on the WHOLE of the premise"
          % (len(rows5), list(range(1, 5))),
          [m <= 2 for _p, _f, m, _s in rows5] == [f for _p, f, _m, _s in rows5]
          and sum(1 for _p, f, _m, _s in rows5 if f) == 1)
    consec_partial = [(p, m) for p, f, m, _s in rows5
                      if not f and p == tuple(range(p[0], p[0] + len(p)))]
    check("and 'CONSECUTIVE' IS NOT THE DIVIDING LINE: %d of these profiles are "
          "consecutive but partial and every one of them admits a ridge in >= 3 "
          "facets -- %s.  The generalisation 'the premise can be weakened to "
          "consecutive' is CLOSED, not open"
          % (len(consec_partial),
             ", ".join("%s gives %d" % (list(p), m) for p, m in consec_partial)),
          consec_partial and all(m >= 3 for _p, m in consec_partial))
    check("this reproduces z8af0's S4 transcript row for row: %s.  z8af0's "
          "routine was hand-rolled and this one goes through "
          "`face_complex.boundary_matrix`, so the agreement is evidence rather "
          "than a copy"
          % [m for _p, _f, m, _s in rows5],
          [m for _p, _f, m, _s in rows5] == [4, 6, 4, 3, 6, 4, 3, 3, 3, 3, 2])

    # -- T4: and it is not a fact about n = 5 --------------------------------
    print("T4 -- AND TIGHTNESS IS NOT A FACT ABOUT n = 5.  The same sweep at "
          "n = %s." % list(SWEEP_NS))
    ok4 = True
    total = 0
    empty = []
    smallest = None
    for n in SWEEP_NS:
        rows = sweep(n)
        total += len(rows)
        empty += [(n, p) for p, _f, _m, s in rows if s == 0]
        lo = min(s for _p, _f, _m, s in rows)
        smallest = lo if smallest is None else min(smallest, lo)
        good = ([m <= 2 for _p, _f, m, _s in rows] == [f for _p, f, _m, _s in rows]
                and sum(1 for _p, f, _m, _s in rows if f) == 1)
        ok4 = ok4 and good
        print("    n=%d  %2d profiles, multiplicity <= 2 on %d of them, the "
              "full profile %s among them: %s; smallest family %d facets"
              % (n, len(rows), sum(1 for _p, _f, m, _s in rows if m <= 2),
                 list(range(1, n)),
                 "yes" if any(f and m <= 2 for _p, f, m, _s in rows) else "NO",
                 lo))
    check("at every one of n = %s, multiplicity <= 2 holds on exactly one "
          "profile and it is the full one -- %d profiles in total.  NOT SHOWN: "
          "n > 6, and n = 3 carries no separating content (it has exactly one "
          "profile of length >= 2 and that profile IS the full one), so the "
          "separation is measured at n = 4, 5 and 6"
          % (list(SWEEP_NS), total), ok4)
    check("AND NO SWEPT FAMILY IS EMPTY -- %d profiles, smallest family %d "
          "facets.  An empty family has multiplicity 0, which is <= 2, so a "
          "sweep that built nothing would pass the two rows above while "
          "measuring nothing; this is the row that stops that reading"
          % (total, smallest if smallest is not None else -1),
          not empty and smallest is not None and smallest > 0,
          "empty families: %s" % empty)

    # -- T5: the rows above, run against a routine that cannot say anything --
    print("T5 -- WRONG-DIRECTION WORLD.  The T2 and T3 predicates re-scored "
          "against a STUB that returns 2 for every family -- the exact "
          "instrument this port exists to rule out.  The rows must go RED.")
    stub = lambda _facets: 2                                   # noqa: E731
    stub_control = stub(broken) == 3
    stub_rows5 = [(p, f, stub(chains_with_profile(5, p)))
                  for p, f, _m, _s in rows5]
    stub_tight = ([m <= 2 for _p, _f, m in stub_rows5]
                  == [f for _p, f, _m in stub_rows5])
    stub_consec = all(m >= 3 for p, f, m in stub_rows5
                      if not f and p == tuple(range(p[0], p[0] + len(p))))
    print("    T2 negative control under the stub: %s (needs RED)"
          % ("GREEN" if stub_control else "RED"))
    print("    T3 tightness under the stub:        %s (needs RED)"
          % ("GREEN" if stub_tight else "RED"))
    print("    T3 'not consecutive' under the stub:%s (needs RED)"
          % ("GREEN" if stub_consec else " RED"))
    check("all three go RED under a routine that cannot report anything but 2, "
          "so none of them is satisfied by the instrument this repair is about. "
          " NOT SHOWN: that they are red on every wrong instrument -- one stub "
          "is one world, and it is the world main's zero would come from",
          not stub_control and not stub_tight and not stub_consec)

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
