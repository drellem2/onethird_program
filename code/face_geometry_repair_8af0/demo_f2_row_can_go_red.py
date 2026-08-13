#!/usr/bin/env python3
"""mg-8af0 -- the V6 row, before and after, driven with inputs that SHOULD move it.

mg-fcb2's F2: `verify_e35b.py:402` scored

    forced == 3 and len(table) == 11

against the literal `table` beside it, under the heading "EVERY COUNT THIS
REPAIR PRINTS".  A control that cannot fail reports success regardless of
input.  This file is the evidence that the replacement CAN fail, and that the
thing it replaced could not.

WHY A SEPARATE FILE, AND WHY IT MUTATES COPIES.  A repaired control that has
never been watched fire is not evidence of anything -- it is the same green row
with better prose.  So six inputs are constructed, four of them things somebody
would actually do to this repository and one of them the defect this repair was
about put back, and each is run through BOTH the scored condition and the four
rows that replace it.  Nothing under
code/face_geometry/ is written to: every mutation is applied to a private copy
in a temporary directory, and the copy is regenerated with `controls.py` where
the input is a source change.

THE SIX INPUTS

  C1  a twelfth count is added to the ARTIFACT by hand, controls.py untouched
      -- mg-fcb2's own construction, verbatim.
  C2  a twelfth count is added to CONTROLS.PY and the artifact regenerated
      -- the same thing done the way the repository actually does it.
  C3  a classified count is reworded in the artifact (61/86 -> 61/87).
  C4  a classified count is reworded AT THE SOURCE and the artifact
      regenerated, with the number of printed values unchanged -- the input
      that separates V6a from V6b and V6c, none of which is redundant.
  C5  NOTHING in the repository changes and the literal in the verifier does
      (mg-8af0's own F1/F3 edits take it from 3-of-11 to 4-of-12).  The one
      input the old condition has ever been able to respond to.
  C6  mg-fcb2's F1 PUT BACK at the source -- `% (N, N, ...)` supplied to
      "corrupted on %d/%d posets" -- and the artifact regenerated, which it does
      BYTE-IDENTICALLY because both operands are 86.  Added by mg-fa8a, landing
      mg-d3f3's F-2.

WHAT IS PREDICTED (PREDICTIONS.md, E5 and E6c, committed before this file
existed): the old condition prints PASS on C1-C4 and FAIL on C5; V6c catches C1
and C3, V6b catches C2, and V6a is the only row that catches C4.

WHAT C6 IS PREDICTED TO DO, and it is not in that document because the row it
scores did not exist when that document was written: C6 is GREEN on the old
condition AND on V6a, V6b and V6c -- four greens for a defect put back at the
source -- and RED on V7b alone.  mg-d3f3 ran the same construction against all
35 scored artefacts of this repair and scored 0 red; this file now carries the
one column that answers it.  C6 is also the ONLY construction here that leaves
controls_output.txt byte-identical, which is why "the defect is visible in the
artifact" was never a property of the defect -- only of the other five inputs.

Exit 0 iff that matrix is exactly what happens.  A cell coming out GREEN where
this file says RED is a refutation of the repair, not of the demonstration.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))
REPAIR = os.path.normpath(os.path.join(HERE, "..", "face_geometry_repair_e35b"))
sys.path.insert(0, REPAIR)

from verify_e35b import (                                        # noqa: E402
    TABLE, CENSUS_DECLARED, RATIO_SITE, census, ratio_operands, unanchored,
    regenerate,
)

# The old scored condition, transcribed from 5f542f0 so that this file does not
# depend on the defect still being present in the tree.  Only the VERDICT
# column is transcribed, because it is the only column the condition reads --
# which is itself worth seeing written down.
OLD_FORCED_EXPECTED = 3
OLD_LEN_EXPECTED = 11
OLD_TABLE_VERDICTS = [
    "COULD MOVE",               # dichotomy 297 = 288 + 9 + 0
    "FORCED BY MATHEMATICS",    # swap01 GAUGE 72/72
    "COULD MOVE",               # NOT-GAUGE on 288 of 297
    "COULD MOVE",               # non-identity witness 72/72
    "COULD MOVE",               # vacuity I1/I2/I3
    "COULD MOVE",               # vacuity I4
    "FORCED BY THE CODE PATH",  # target byte-identical 344/344
    "FORCED BY CONSTRUCTION",   # >= 3 facets, I1/I2/I3 zeros
    "COULD MOVE",               # >= 3 facets, I4 zero  <- mg-fcb2's F3
    "COULD MOVE",               # coverage 61/86
    "COULD MOVE",               # M4/M5 82/86
]
CURRENT_VERDICTS = [e[1] for e in TABLE]


def old_row(_artifact, _controls_src, verdicts=OLD_TABLE_VERDICTS):
    """`forced == 3 and len(table) == 11`, evaluated as mg-e35b wrote it.

    Both of the first two arguments are ignored, and that is the finding: the
    artifact and the source are not inputs to this condition.  They are in the
    signature so that the driver below can hand every row the same inputs and
    let the row show what it does with them.
    """
    forced = sum(1 for v in verdicts if v.startswith("FORCED"))
    return forced == OLD_FORCED_EXPECTED and len(verdicts) == OLD_LEN_EXPECTED


def new_rows(artifact, controls_src, fresh):
    """V6a / V6b / V6c / V7b, as `verify_e35b.py` scores them."""
    ratios, _ = ratio_operands(controls_src)
    at_site = [(a, b) for _, ex, a, b in ratios if RATIO_SITE in ex]
    return {
        "V6a ANCHORED": not unanchored(artifact),
        "V6b CENSUS": census(controls_src) == CENSUS_DECLARED,
        "V6c REGENERATED": fresh == artifact,
        "V7b OPERAND": (all(a != b for _, _, a, b in ratios)
                        and len(at_site) == 1 and at_site[0][0] != at_site[0][1]),
    }


def revert_f1(src):
    """mg-fcb2's F1, put back at the source: `% (N, N, ...)` at the site.

    THE ONE CONSTRUCTION IN THIS FILE THAT MOVES NO BYTE OF THE ARTIFACT.
    `site_rows[3][1]` and `N` are both 86, so C6 regenerates
    controls_output.txt byte-identically (41081 = 41081) and the sentence goes
    back to printing its own denominator.  mg-d3f3 measured this against all 35
    artefacts of the mg-8af0 repair and scored 0 red; the column added below is
    the row that answers it.
    """
    old = "% (site_rows[3][1], N, dich_rows"
    new = "% (N, N, dich_rows"
    if src.count(old) != 1:
        raise AssertionError("the F1 site is not where this construction "
                             "expects it: %d matches for %r" % (src.count(old), old))
    return src.replace(old, new)


def sandbox():
    """A private copy of code/face_geometry/ that can be mutated freely."""
    d = tempfile.mkdtemp(prefix="mg8af0-")
    for f in os.listdir(PROBE):
        if f.endswith(".py") or f.endswith(".txt"):
            shutil.copy(os.path.join(PROBE, f), os.path.join(d, f))
    return d


def add_print_at_end_of_section(src):
    """Insert one new printed count at the end of `negative_control_incidence`.

    Located by `ast`, not by a line number, so this stays valid as the section
    is edited.  The inserted statement prints two integers, so it moves the
    census by exactly 2 specifiers -- which is the quantity C2 is about.
    """
    import ast
    fn = next(f for f in ast.walk(ast.parse(src))
              if isinstance(f, ast.FunctionDef)
              and f.name == "negative_control_incidence")
    lines = src.splitlines(keepends=True)
    at = fn.body[-1].end_lineno            # 1-based, inclusive
    lines.insert(at, '    print("    * A TWELFTH COUNT, added by mg-8af0\'s '
                     'demonstration: %d of %d posets" % (len(ps) - 1, len(ps)))\n')
    return "".join(lines)


def run(name, mutate_artifact=None, mutate_source=None,
        verdicts=OLD_TABLE_VERDICTS):
    """Apply one construction and score every row against it."""
    d = sandbox()
    try:
        src_path = os.path.join(d, "controls.py")
        art_path = os.path.join(d, "controls_output.txt")
        src = open(src_path).read()
        if mutate_source is not None:
            src = mutate_source(src)
            open(src_path, "w").write(src)
            art = regenerate(d)                       # the repository's own route
            open(art_path, "w").write(art)
        art = open(art_path).read()
        if mutate_artifact is not None:
            art = mutate_artifact(art)
            open(art_path, "w").write(art)
        fresh = regenerate(d)
        # The artifact this construction produces, against the one COMMITTED
        # under code/face_geometry/.  Measured for every construction and
        # reported for C6, because C6's whole claim is that a real defect can
        # be put back and leave this number unmoved -- and an asserted byte
        # count is the thing this file exists to refuse.
        committed = open(os.path.join(PROBE, "controls_output.txt")).read()
        return (name, old_row(art, src, verdicts), new_rows(art, src, fresh),
                (len(art), len(committed)))
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    print("mg-8af0 -- can the V6 row go red?  Six constructed inputs, old row "
          "and new rows scored on each.")
    print("population: 6 constructions x 5 rows = 30 cells.  grain: one "
          "(construction, row) cell, GREEN = the row passed = the input did not "
          "move it.")
    print()

    cases = [
        run("C1 twelfth count added to the ARTIFACT by hand",
            mutate_artifact=lambda a: a + "    * A TWELFTH COUNT, added by hand: "
                                          "5 of 86 posets\n"),
        run("C2 twelfth count added to CONTROLS.PY, artifact regenerated",
            mutate_source=add_print_at_end_of_section),
        run("C3 a classified count reworded in the ARTIFACT (61/86 -> 61/87)",
            mutate_artifact=lambda a: a.replace(
                "coverage at `le_to_facet` is 61/86",
                "coverage at `le_to_facet` is 61/87")),
        run("C4 the same count reworded AT THE SOURCE (backticks dropped), "
            "artifact regenerated, printed values unchanged",
            mutate_source=lambda s: s.replace(
                "`le_to_facet` is %d/%d, of which %d carry evidence",
                "le_to_facet is %d/%d, of which %d carry evidence")),
        # THE ONE INPUT THE OLD ROW DOES RESPOND TO, and it is not an input to
        # the repository at all: an edit to the literal in its own file.
        # mg-8af0's F3 relabel (I4's zero COULD MOVE -> FORCED) plus F1's
        # twelfth entry take it from 3-of-11 to 4-of-12, which is the only way
        # this condition has ever been able to go red.
        run("C5 mg-8af0's OWN edit to the table literal (3/11 -> 4/12), "
            "repository untouched", verdicts=CURRENT_VERDICTS),
        # C6 IS THE CONSTRUCTION THIS FILE DID NOT HAVE (mg-d3f3 F-2, added by
        # mg-fa8a).  Every construction above changes something a reader could
        # see in the artifact; C6 changes the EXPRESSION and no byte, which is
        # what made mg-fcb2's F1 survive a repair aimed at exactly it.
        run("C6 mg-fcb2's F1 PUT BACK at the source (% (N, N, ...)), artifact "
            "regenerated byte-identically", mutate_source=revert_f1),
    ]

    expected = {
        "C1": {"old": True, "V6a ANCHORED": True, "V6b CENSUS": True,
               "V6c REGENERATED": False, "V7b OPERAND": True},
        "C2": {"old": True, "V6a ANCHORED": True, "V6b CENSUS": False,
               "V6c REGENERATED": True, "V7b OPERAND": True},
        "C3": {"old": True, "V6a ANCHORED": False, "V6b CENSUS": True,
               "V6c REGENERATED": False, "V7b OPERAND": True},
        "C4": {"old": True, "V6a ANCHORED": False, "V6b CENSUS": True,
               "V6c REGENERATED": True, "V7b OPERAND": True},
        "C5": {"old": False, "V6a ANCHORED": True, "V6b CENSUS": True,
               "V6c REGENERATED": True, "V7b OPERAND": True},
        "C6": {"old": True, "V6a ANCHORED": True, "V6b CENSUS": True,
               "V6c REGENERATED": True, "V7b OPERAND": False},
    }

    rows = ["V6a ANCHORED", "V6b CENSUS", "V6c REGENERATED", "V7b OPERAND"]
    bad = []
    print("  %-64s %-9s %s" % ("construction", "old row",
                               "  ".join("%-16s" % r for r in rows)))
    for name, old, new, sizes in cases:
        key = name.split()[0]
        got = dict(new)
        got["old"] = old
        cells = ["GREEN" if old else "RED  "]
        for r in rows:
            cells.append("GREEN           " if new[r] else "RED             ")
        print("  %-64s %-9s %s" % (name[:64], cells[0], "  ".join(cells[1:])))
        for k, want in expected[key].items():
            if got[k] != want:
                bad.append("%s / %s: expected %s, got %s"
                           % (key, k, "GREEN" if want else "RED",
                              "GREEN" if got[k] else "RED"))

    print()
    print("  the old row is GREEN on C1-C4 -- it took no input from either the "
          "artifact or the source, so no construction ON THE REPOSITORY could "
          "move it.  It is RED on C5, where nothing in the repository changed "
          "and the literal beside it did.  That is mg-fcb2's F2 in one line, "
          "reproduced here rather than quoted.")
    print("  each replacement row is RED on at least one construction, and C4 "
          "is red for V6a alone and C6 for V7b alone -- so none of the four is "
          "redundant and each has been SHOWN to fire.")
    c6 = [c for c in cases if c[0].startswith("C6")][0]
    print("  C6's artifact is %d bytes against the COMMITTED %d -- %s, so the "
          "defect is back at the source and no byte of controls_output.txt "
          "moved.  MEASURED here, not asserted: it is the premise every green "
          "cell on the C6 row depends on." 
          % (c6[3][0], c6[3][1],
             "IDENTICAL" if c6[3][0] == c6[3][1] else "THEY DIFFER"))
    print("  NOT SHOWN: that the V6 rows catch every way a count could be "
          "added.  V6b is a tripwire on the SET of printed positions, so "
          "substituting a different expression into an existing %d -- which is "
          "exactly what mg-fcb2's F1 was -- moves none of them.  C6 is that "
          "input and the row above it is empty of reds: old row, V6a, V6b and "
          "V6c are ALL GREEN with F1 back at the source.")
    print("  THE SENTENCE THAT USED TO CLOSE THIS PARAGRAPH WAS FALSE AND IS "
          "WITHDRAWN (mg-d3f3 F-1, corrected by mg-fa8a).  It read `That is why "
          "F1 needed a row of its own (V7) and not just a census.`  V7 is "
          "GREEN WITH F1 PRESENT -- it checks that the site count is 86 and "
          "that the artifact prints 86/86, and both are true of the tautology "
          "too, which is the whole content of mg-8af0's own E1.  V7's own "
          "in-file comment never claimed otherwise (`what this row CANNOT do is "
          "tell whether 86/86 is the right answer for the right reason`); the "
          "prose around it did.  What F1 needed is a row that reads the OPERAND "
          "of the `%` and not its digits, and that row is V7b, watched going "
          "red on C6 above and nowhere else.")
    print()
    if bad:
        print("%d cells came out other than predicted:" % len(bad))
        for b in bad:
            print("  - %s" % b)
        return 1
    print("%d/%d cells as predicted -- E5/E6c for C1-C5, and this "
          "file's own docstring for C6 (mg-fa8a)."
          % (len(cases) * 5, len(cases) * 5))
    return 0


if __name__ == "__main__":
    sys.exit(main())
