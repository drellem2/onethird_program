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
with better prose.  So four inputs are constructed, each one a thing somebody
would actually do to this repository, and each is run through BOTH the old
scored condition and the three rows that replace it.  Nothing under
code/face_geometry/ is written to: every mutation is applied to a private copy
in a temporary directory, and the copy is regenerated with `controls.py` where
the input is a source change.

THE FOUR INPUTS

  C1  a twelfth count is added to the ARTIFACT by hand, controls.py untouched
      -- mg-fcb2's own construction, verbatim.
  C2  a twelfth count is added to CONTROLS.PY and the artifact regenerated
      -- the same thing done the way the repository actually does it.
  C3  a classified count is reworded in the artifact (61/86 -> 61/87).
  C4  a classified count is reworded AT THE SOURCE and the artifact
      regenerated, with the number of printed values unchanged -- the input
      that separates V6a from V6b and V6c, none of which is redundant.

WHAT IS PREDICTED (PREDICTIONS.md, E5 and E6c, committed before this file
existed): the old condition prints PASS on all four; V6c catches C1 and C3,
V6b catches C2, and V6a is the only row that catches C4.

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
    TABLE, CENSUS_DECLARED, census, unanchored, regenerate,
)

# The old scored condition, transcribed from 5f542f0 so that this file does not
# depend on the defect still being present in the tree.
OLD_FORCED_EXPECTED = 3
OLD_LEN_EXPECTED = 11


def old_row(_artifact, _controls_src, table=TABLE):
    """`forced == 3 and len(table) == 11`, evaluated as mg-e35b wrote it.

    Both arguments are ignored, and that is the finding: the artifact and the
    source are not inputs to this condition.  They are in the signature so that
    the driver below can hand every row the same inputs and let the row show
    what it does with them.
    """
    forced = sum(1 for e in table if e[1].startswith("FORCED"))
    return forced == OLD_FORCED_EXPECTED and len(table) == OLD_LEN_EXPECTED


def new_rows(artifact, controls_src, fresh):
    """V6a / V6b / V6c, as `verify_e35b.py` scores them."""
    return {
        "V6a ANCHORED": not unanchored(artifact),
        "V6b CENSUS": census(controls_src) == CENSUS_DECLARED,
        "V6c REGENERATED": fresh == artifact,
    }


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


def run(name, mutate_artifact=None, mutate_source=None):
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
        return name, old_row(art, src), new_rows(art, src, fresh)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    print("mg-8af0 -- can the V6 row go red?  Four constructed inputs, old row "
          "and new rows scored on each.")
    print("population: 4 constructions x 4 rows = 16 cells.  grain: one "
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
    ]

    expected = {
        "C1": {"old": True, "V6a ANCHORED": True, "V6b CENSUS": True,
               "V6c REGENERATED": False},
        "C2": {"old": True, "V6a ANCHORED": True, "V6b CENSUS": False,
               "V6c REGENERATED": True},
        "C3": {"old": True, "V6a ANCHORED": False, "V6b CENSUS": True,
               "V6c REGENERATED": False},
        "C4": {"old": True, "V6a ANCHORED": False, "V6b CENSUS": True,
               "V6c REGENERATED": True},
    }

    rows = ["V6a ANCHORED", "V6b CENSUS", "V6c REGENERATED"]
    bad = []
    print("  %-64s %-9s %s" % ("construction", "old row",
                               "  ".join("%-16s" % r for r in rows)))
    for name, old, new in cases:
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
    print("  the old row is GREEN on 4 of 4 -- it took no input from either the "
          "artifact or the source, so no construction could have moved it.  "
          "That is mg-fcb2's F2, reproduced here rather than quoted.")
    print("  each replacement row is RED on at least one construction, and C4 "
          "is red for V6a alone -- so none of the three is redundant and each "
          "has been SHOWN to fire.")
    print()
    if bad:
        print("%d cells came out other than predicted:" % len(bad))
        for b in bad:
            print("  - %s" % b)
        return 1
    print("16/16 cells as predicted in PREDICTIONS.md E5/E6c.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
