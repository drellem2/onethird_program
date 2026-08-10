"""mg-17aa -- THE CONTROL THAT GOES RED WHEN THE SECTION BECOMES MORE HONEST,
demonstrated by running it rather than by arguing about it.

mg-e35b declined to score NEGATIVE CONTROL 4's vacuity split and gave the
reason:

    "a row scoring 'the split separates' would go RED the day somebody FIXED
     the blindness -- the wrong direction for a control to point."

The ticket that landed this file was told not to build a row of that shape.
What it found instead is that the section ALREADY HAD ONE, one screen above the
sentence, pointing straight at the item mg-e35b was deferring:

    check("routing check on the mg-8a12 repair: the MOVED-DIAGONAL split
           SEPARATES on this population ...",
          0 < len(forced_rows) < len(muts))

`len(muts)` is 4.  Extending the [CANNOT FAIL] treatment to the fourth row --
the deferred item, in one line -- makes that read `0 < 4 < 4`, and the battery
exits 1 on a tree from which a forced clause has just been honestly removed.

WHAT THIS SCRIPT DOES.  It takes the PRE-mg-17aa `controls.py` -- pinned BY BLOB
SHA, not by a branch name, because `main` moves and a demo pinned to a moving
ref demonstrates whatever main happens to say today (mg-a71f) -- applies the
SMALLEST edit that extends the treatment to all four rows, and runs the battery.
The edit is one character class: the routing predicate `diag_preserved == 0`
becomes `diag_preserved >= 0`, which is True for every row.  Nothing else is
touched, so whatever goes red is what that tree does when the deferred item
lands.

TWO ROWS GO RED AND THEY ARE NOT THE SAME KIND OF RED, which is the finding:

  the [CANNOT FAIL] row      -- a REAL failure.  Its condition asserts
                                `theorem_diag == theorem_app`, i.e. that the
                                diagonal moves on every biting pair of every
                                forced row.  It does not: row I4's diagonal
                                SURVIVES on the 3 antichains.  The single-gate
                                argument is genuinely too narrow to cover the
                                fourth row, and widening it is the mathematical
                                content of mg-17aa.
  the routing row            -- a WRONG-DIRECTION failure.  Nothing about the
                                mathematics moved; the row set stopped
                                separating because every row was correctly
                                labelled.  A control that reports that as a
                                failure is worse than no control, and it is the
                                shape mg-e35b refused to add.

Run: python3 demo_wrong_way.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "code", "face_geometry")

# The blob of code/face_geometry/controls.py as it stood at 744cfd5, the commit
# this ticket branched from -- i.e. the tree carrying mg-e35b's deferral.  A
# BLOB sha and not a commit-or-branch ref: `main` moves, and mg-f8e5's
# c1_rebase.py:48 is the worked example of a probe that quietly re-aimed itself
# when it did.
PINNED_BLOB = "da160f680e9a96f2628b3a20fdc983d03b65eb0d"

# The minimal extension: route every row to the theorem.  This is the deferred
# item stated as an edit -- "extend the [CANNOT FAIL] row to all four".
FROM = "    forced = (diag_preserved == 0)"
TO = "    forced = (diag_preserved >= 0)   # mg-17aa demo: all four rows"

BAR = "=" * 78
SCORE = []


def claim(text, ok, detail=""):
    SCORE.append(ok)
    print("  [%s] %s%s" % ("HOLDS" if ok else "BROKEN", text,
                           ("\n        " + detail) if detail else ""))


def main():
    print(BAR)
    print("mg-17aa -- THE PRE-EXISTING WRONG-DIRECTION CONTROL, RUN")
    print(BAR)

    blob = subprocess.run(["git", "cat-file", "-p", PINNED_BLOB],
                          cwd=REPO, capture_output=True, text=True)
    claim("the pinned pre-mg-17aa controls.py is readable at blob %s "
          "(%d bytes)" % (PINNED_BLOB[:12], len(blob.stdout)),
          blob.returncode == 0 and len(blob.stdout) > 10000,
          "exit %d" % blob.returncode)
    if blob.returncode != 0:
        return 2
    src = blob.stdout

    claim("it carries the deferral in its own words -- the routing row's "
          "condition is a strict two-sided bound on the number of forced rows",
          "0 < len(forced_rows) < len(muts))" in src,
          "the exact literal `0 < len(forced_rows) < len(muts))` is present")
    claim("and it routes on ONE of the predicate's two forced gates",
          FROM in src, "the exact literal %r is present" % FROM.strip())
    if FROM not in src:
        return 2

    tmp = tempfile.mkdtemp(prefix="mg17aa_demo_")
    try:
        for f in ("face_complex.py", "posets.py"):
            shutil.copy(os.path.join(SRC, f), tmp)
        # ... but face_complex.py and posets.py must be the PINNED tree's too,
        # or the demo is a mix.  mg-17aa touches neither, which is checked
        # below rather than assumed.
        for f in ("face_complex.py", "posets.py"):
            p = subprocess.run(
                ["git", "diff", "%s" % PINNED_COMMIT, "--",
                 "code/face_geometry/" + f],
                cwd=REPO, capture_output=True, text=True)
            claim("%s is byte-identical to the pinned tree's, so this demo is "
                  "not a mix of two trees" % f, p.stdout.strip() == "",
                  "git diff is %d bytes" % len(p.stdout))
        patched = src.replace(FROM, TO)
        claim("the minimal extension applies as exactly one substitution",
              patched.count(TO) == 1 and patched != src,
              "one line changed, %d bytes -> %d" % (len(src), len(patched)))
        with open(os.path.join(tmp, "controls.py"), "w") as fh:
            fh.write(patched)

        r = subprocess.run([sys.executable, "controls.py", "5"], cwd=tmp,
                           capture_output=True, text=True)
        out = r.stdout + r.stderr
        fails = [l.strip() for l in out.split("\n") if l.strip().startswith("[FAIL]")]
        print("\n  the patched pre-mg-17aa battery exits %d with %d FAIL row(s):"
              % (r.returncode, len(fails)))
        for f in fails:
            print("    - " + f[:150])
        print()

        claim("THE DEFERRED ITEM, APPLIED AS ONE LINE TO THE TREE THAT DEFERRED "
              "IT, TURNS THE BATTERY RED: exit %d, %d rows FAIL"
              % (r.returncode, len(fails)),
              r.returncode != 0 and len(fails) == 2,
              "this is why the item could not be 'just delete the clause': the "
              "clause's removal is one line and the consequences are two rows")

        routing = [f for f in fails if "routing check" in f]
        theorem = [f for f in fails if "PROVEN PROPERTY" in f]
        claim("one of the two is the ROUTING row -- `0 < 4 < 4` -- and NOTHING "
              "ABOUT THE MATHEMATICS MOVED to make it red.  It went red because "
              "the row set stopped separating, i.e. because every row became "
              "correctly labelled: the wrong direction for a control to point, "
              "and the shape mg-e35b refused to add one screen below it",
              len(routing) == 1,
              routing[0][:200] if routing else "routing row not among the FAILs")
        claim("the other is the [CANNOT FAIL] row, and that one is a REAL "
              "failure: its condition asserts the diagonal moves on every "
              "biting pair of every forced row, and row I4's diagonal SURVIVES "
              "on the 3 antichains.  The single-gate argument does not cover "
              "the fourth row -- widening it to |s_i s_j| = 1 is the "
              "mathematical content of mg-17aa, and no amount of re-scoring "
              "would have supplied it",
              len(theorem) == 1,
              theorem[0][:200] if theorem else "[CANNOT FAIL] row not among the FAILs")

        # AND THE SHIPPED TREE, for contrast: the same extension, with the
        # theorem widened and the routing row replaced, exits 0.
        r2 = subprocess.run([sys.executable, "controls.py", "5"], cwd=SRC,
                            capture_output=True, text=True)
        out2 = r2.stdout + r2.stderr
        claim("and the SHIPPED tree -- same extension, theorem widened to both "
              "forced gates, routing row replaced by an exhibited-falsifier row "
              "-- exits 0 with all four rows forced",
              r2.returncode == 0
              and "the corruptions I1, I2, I3, I4 are NOT" in out2
              and "falsifiability check" in out2,
              "exit %d" % r2.returncode)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


# The commit the pinned blob was read from.  Used only to check that the two
# modules this demo copies from the live tree are unchanged since it; the
# controls.py under test comes from the BLOB and not from this ref.
PINNED_COMMIT = "744cfd5"


if __name__ == "__main__":
    sys.exit(main())
