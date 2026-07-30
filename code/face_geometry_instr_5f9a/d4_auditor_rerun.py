"""mg-04a8 part 4 -- RUN THE AUDITOR'S OWN DELETION TEST AGAINST THE REPAIR.

mg-d0e2 wrote `code/face_geometry_audit_d0e2/e1_deletion.py` specifically so it
would NOT be the subject's instrument: its nine mutations are re-derived from the
source text of `absorb_trace` rather than imported from `d2_deletion.py`, and its
README says in terms that running the subject's own test learns only that the
test is deterministic.  That file is the strongest available evidence about this
repair, and it costs one subprocess to use it.  So it is run here, unmodified,
and what it says is scored.

WHY IT IS RUN HERE RATHER THAN EDITED THERE.  Its committed transcripts are that
audit's record of its own run against the tree it audited, and this repair does
not rewrite them -- the same treatment mg-5f9a gave mg-1c80's `a6_mutations.py`.
But there is a difference worth stating: `a6_mutations.py` degraded to
`<-- MISSED` and still exited 0, while `e1_deletion.py` EXITS 1 against this
tree.  A script in the repository that exits 1 is a landmine unless somebody has
written down why, so the why is scored below rather than left in a paragraph.

TWO OF ITS PREDICTIONS NOW MISS, AND BOTH MISSES ARE THE REPAIR.  It predicted
that deleting the `shape` gate would leave the artifact byte-identical, because
when it was written nothing in the battery had a shape mismatch; it now changes
the artifact and fails a row.  Its `parity` prediction was the one MISS it
recorded against mg-5f9a -- predicted changed, observed identical -- and it now
observes changed.  A prediction that misses because the code was repaired between
its registration and its run is the outcome that item was asking for.

THIS FILE'S CLAIMS WOULD DIFFER UNDER: either constructed-pair row being removed
from `controls.py`, or its expected value being taken from the predicate instead
of from brute force -- both restore the state where those two deletions moved
nothing.  And under any OTHER claim of that audit going broken against this tree,
which would mean this repair disturbed something the audit had verified.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import BAR, head                                      # noqa: E402

SCORE = []

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.normpath(os.path.join(HERE, "..", "face_geometry_audit_d0e2"))

# The two mg-d0e2 found invisible.  Named here so the claim below is about them
# and not about "nine lines all said CHANGED".
WERE_INVISIBLE = ("delete gate 'shape'", "delete gate 'parity'")

LINE = re.compile(r"^  (delete gate '\w+'|delete '\w+' from gate_violations|"
                  r"stop counting signs_read|swap the two forced gates' order|"
                  r"invert diagonal_moves \(the routing\))\s+"
                  r"bytes\s+(\d+) ->\s+(\d+)\s+(CHANGED|BYTE-IDENTICAL)\s+"
                  r"exit (\d+)", re.M)


def claim(text, ok, differs_under, detail=""):
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    print("        WOULD DIFFER UNDER: %s" % differs_under)


def main():
    print(BAR)
    print("mg-04a8 part 4 -- mg-d0e2's own deletion test, unmodified, on this tree")
    print(BAR)

    if not os.path.isdir(AUDIT):
        raise SystemExit("cannot find %s" % AUDIT)
    proc = subprocess.run([sys.executable, "e1_deletion.py"], cwd=AUDIT,
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    print()
    print("--- its transcript, verbatim " + "-" * 48)
    print(out.rstrip())
    print("--- end of its transcript " + "-" * 51)
    print()

    head("WHAT IT SAYS ABOUT THIS TREE")
    rows = LINE.findall(out)
    claim("its nine mutations all ran and were parsed -- %d of 9" % len(rows),
          len(rows) == 9,
          "that audit's transcript format changing, which would make every "
          "claim below silently vacuous rather than wrong",
          "; ".join("%s %s->%s %s exit %s" % (n, a, b, c, d)
                    for n, a, b, c, d in rows))
    changed = [n for n, _a, _b, c, _d in rows if c == "CHANGED"]
    claim("THE DELETION TEST NOW BITES ON %d OF 9.  mg-d0e2 measured 7 of 9 "
          "against mg-5f9a" % len(changed),
          len(changed) == 9,
          "either of the two constructed-pair rows leaving controls.py, or its "
          "expected answer being taken from the predicate rather than from "
          "`absorbable_bruteforce` -- either one puts the `shape` and `parity` "
          "branches back out of reach of every population and the artifact "
          "stops moving when they are deleted")
    for name in WERE_INVISIBLE:
        hit = [r for r in rows if r[0] == name]
        ok = bool(hit) and hit[0][3] == "CHANGED" and hit[0][4] == "1"
        claim("%r -- which left the artifact BYTE-IDENTICAL at 20738 bytes "
              "before this repair -- now %s the artifact (%s -> %s bytes) and "
              "exits %s"
              % (name, hit[0][3].lower() if hit else "?",
                 hit[0][1] if hit else "?", hit[0][2] if hit else "?",
                 hit[0][4] if hit else "?"), ok,
              "the constructed pair for that branch no longer reaching it -- "
              "which is what `absorb_trace` returning a different gate on it "
              "would mean, and what the row in controls.py scores directly")

    head("AND WHY IT EXITS 1, WHICH IS NOT A FAILURE OF THIS REPAIR")
    broken = re.search(r"^E1 claims broken: (\d+)$", out, re.M)
    n_broken = int(broken.group(1)) if broken else -1
    row_claim = re.search(r"^  \[BROKEN\] the unmutated battery scores (\d+) rows",
                          out, re.M)
    claim("exactly %d claim of that audit is BROKEN against this tree, and it is "
          "its ROW COUNT: it asserts 41, the number it measured at 5988134, and "
          "this tree has %s -- the two constructed-pair rows this repair added"
          % (n_broken, row_claim.group(1) if row_claim else "?"),
          n_broken == 1 and row_claim is not None
          and row_claim.group(1) == "43",
          "any OTHER claim of that audit going broken -- that would mean this "
          "repair disturbed something the audit had verified, and it is the "
          "reason this is scored rather than asserted in prose",
          "its exit status is %d; a frozen count measured against a tree that "
          "has since gained rows is a stale number, not a refutation"
          % proc.returncode)
    head("AND WHAT THE REST OF THAT AUDIT SAYS -- did anything retreat?")
    for script, want_broken, why in (
            ("e2_parity.py", 0,
             "it re-derives where the predicate returns over all four "
             "populations, and the 297/306/82/172 split and the 57-of-297 "
             "disagreement are untouched by this repair"),
            ("e3_seams.py", 2,
             "its two remaining BROKEN claims are FROZEN LITERALS of the same "
             "kind as its row count -- it asserts the artifact says 'lines "
             "scanned: 62' and '40 row names among them', and the artifact now "
             "says 64 and 42.  Both are computed live by the row itself and "
             "both are correct: there are exactly 64 lines above it and 43 "
             "scored rows of which it is one")):
        p = subprocess.run([sys.executable, script], cwd=AUDIT,
                           capture_output=True, text=True)
        txt = p.stdout + p.stderr
        m = re.search(r"claims broken: (\d+)", txt)
        n = int(m.group(1)) if m else -1
        claim("%s: %d claim(s) broken against this tree (expected %d).  %s"
              % (script, n, want_broken, why), n == want_broken,
              "a claim of that audit about the MATHEMATICS or about the "
              "predicate's behaviour going broken -- that would be this repair "
              "disturbing something already verified, and it is the difference "
              "between a stale figure and a retreat",
              "exit %d; %s" % (p.returncode, (m.group(0) if m else "unparsed")))
    art = open(os.path.join(HERE, "..", "face_geometry",
                            "controls_output.txt")).read()
    claim("and the two extents those frozen literals disagree with are printed "
          "LIVE by the row that owns them, and are right: 'lines scanned: 64' "
          "with 64 lines above it, '42 row names' with 43 scored rows of which "
          "it is one",
          "lines scanned: 64 (the whole artifact above this row; 42 row names"
          in art
          and len([l for l in art.split("\n")[:art.split("\n").index(
              [x for x in art.split("\n") if "lines scanned: 64" in x][0])]]) == 64,
          "a checker printing an extent it did not measure -- the mg-a4ef/"
          "mg-7dd3 defect.  These two move whenever a row is added, which is "
          "how this repair moved them")

    claim("and the number it was frozen against is the one mg-5f9a PUBLISHED as "
          "43 while the artifact carried 41 (mg-d0e2's F3).  The artifact now "
          "genuinely carries 43, so the old figure is right for the wrong "
          "reason and is corrected at its sites rather than left to be read as "
          "confirmation",
          "43 rows -- lines whose marker STARTS the line" in out
          or (row_claim is not None and row_claim.group(1) == "43"),
          "the row population changing again without the doc sites being "
          "re-derived, which is the mg-8e30 defect (a figure measured before "
          "the edit that moved it)")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
