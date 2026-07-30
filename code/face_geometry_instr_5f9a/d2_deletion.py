"""mg-5f9a part 2 -- THE DELETION TEST, run on BOTH sides of the repair.

This is the test that caught the last version, so it is the test this one has to
pass.  mg-1c80 stated it as: REMOVE THE GATE THE EXPLANATION NAMES AS DECISIVE
AND CONFIRM THE ARTIFACT CHANGES.  If it does not, the named gate is not what
the code is doing.

BOTH SIDES, because half of it is asking to be believed.  The BEFORE half runs
`main`'s own face_geometry tree, deletes `main`'s diagonal gate, and checks the
artifact against `main`'s committed `controls_output.txt` -- mg-1c80's M2,
re-run here rather than quoted.  The AFTER half does the corresponding deletions
on this tree.

PREDICTIONS ARE PRINTED BEFORE THE RESULTS and were written before the runs.
The interesting ones are the two marked (*): a gate deletion that changes no
DECISION must still change the ARTIFACT, because the artifact reports where the
code went and not only what it concluded.

Nothing under ../face_geometry is written: every mutation is applied to a copy
in a temporary directory, and every battery run captures stdout rather than
tee-ing it.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import (                                              # noqa: E402
    BAR, FG, head, mutate_tree, run_controls, write_main_tree,
)

SCORE = []

NEW_FILES = ["face_complex.py", "posets.py", "controls.py", "run_probe.py"]
MAIN_FILES = ["face_complex.py", "posets.py", "controls.py"]

# ----------------------------------------------------------------- this tree
NEW_DIAG = ('face_complex.py',
            '        if A[i][i] != B[i][i]:\n'
            '            return Trace(False, "diagonal", 0)\n',
            '')
NEW_MAG = ('face_complex.py',
           '            if abs(A[i][j]) != abs(B[i][j]):\n'
           '                return Trace(False, "magnitude", 0)\n',
           '            pass\n')
NEW_ORDER = ('face_complex.py',
             '        if A[i][i] != B[i][i]:\n'
             '            return Trace(False, "diagonal", 0)\n'
             '        for j in range(m):\n'
             '            if abs(A[i][j]) != abs(B[i][j]):\n'
             '                return Trace(False, "magnitude", 0)\n',
             '        for j in range(m):\n'
             '            if abs(A[i][j]) != abs(B[i][j]):\n'
             '                return Trace(False, "magnitude", 0)\n'
             '        if A[i][i] != B[i][i]:\n'
             '            return Trace(False, "diagonal", 0)\n')
NEW_SIGNS = ('face_complex.py',
             '            signs_read += 1\n',
             '            pass\n')

# ------------------------------------------------------- main's tree (before)
MAIN_DIAG = ('face_complex.py',
             '        if len(A[i]) != len(B[i]) or A[i][i] != B[i][i]:\n'
             '            return False\n',
             '        if len(A[i]) != len(B[i]):\n'
             '            return False\n')
MAIN_MAG = ('face_complex.py',
            '            if abs(A[i][j]) != abs(B[i][j]):\n'
            '                return False\n',
            '            pass\n')

PREDICTIONS = [
    ("BEFORE-1", "main: delete the s_i^2 = 1 gate (mg-1c80's M2 verbatim)",
     "artifact BYTE-IDENTICAL, exit 0 -- the finding this landing answers"),
    ("BEFORE-2", "main: delete the |s_i s_j| = 1 gate (mg-1c80's M1)",
     "artifact CHANGES, exit 1 -- that gate is what forbids I4's antichains"),
    ("AFTER-1*", "this tree: delete the s_i^2 = 1 gate from `absorb_trace`",
     "artifact CHANGES, exit 0 -- no decision moves, but the trace does"),
    ("AFTER-2", "this tree: delete the |s_i s_j| = 1 gate from `absorb_trace`",
     "artifact CHANGES, exit 1 -- as at main"),
    ("AFTER-3*", "this tree: test row i's magnitudes BEFORE row i's diagonal",
     "artifact CHANGES, exit 0 -- same answers, different trace"),
    ("AFTER-4", "this tree: stop counting the signs the union-find reads",
     "artifact CHANGES, exit 0 -- NC3's 1459 is printed"),
]


def claim(text, ok, detail=""):
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)


def run_case(tag, desc, tree_files, edits, baseline, base_code,
             want_change, want_exit):
    root = (write_main_tree(tree_files) if tree_files is MAIN_FILES
            else None)
    if root is None:
        cwd = mutate_tree(edits, tree_files)
    else:
        # main's tree, then the edits applied to that copy
        for fname, old, new in edits:
            path = os.path.join(root, fname)
            text = open(path).read()
            if text.count(old) != 1:
                raise SystemExit("%s: anchor occurs %d times in main's %s"
                                 % (tag, text.count(old), fname))
            open(path, "w").write(text.replace(old, new))
        cwd = root
    out, code = run_controls(cwd)
    changed = out != baseline
    claim("%s -- %s: artifact %s (predicted %s), exit %d (predicted %d)"
          % (tag, desc, "CHANGES" if changed else "BYTE-IDENTICAL",
             "CHANGES" if want_change else "BYTE-IDENTICAL", code, want_exit),
          changed == want_change and code == want_exit,
          "%d bytes out vs %d baseline; unmutated baseline exited %d"
          % (len(out), len(baseline), base_code))
    return out


def main():
    print(BAR)
    print("mg-5f9a part 2 -- the deletion test, before and after")
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    for tag, desc, pred in PREDICTIONS:
        print("   %-9s %-62s %s" % (tag, desc, pred))

    head("BEFORE -- `main`'s tree, where mg-1c80 found the artifact unmoved")
    repo = os.path.abspath(os.path.join(FG, "..", ".."))
    main_art = subprocess.run(
        ["git", "show", "main:code/face_geometry/controls_output.txt"],
        cwd=repo, capture_output=True, text=True).stdout
    base_dir = write_main_tree(MAIN_FILES)
    base_out, base_code = run_controls(base_dir)
    claim("main's committed controls_output.txt regenerates from main's sources",
          base_out == main_art,
          "%d bytes regenerated, %d committed, exit %d"
          % (len(base_out), len(main_art), base_code))
    run_case("BEFORE-1", "delete the s_i^2 = 1 gate", MAIN_FILES, [MAIN_DIAG],
             base_out, base_code, want_change=False, want_exit=0)
    run_case("BEFORE-2", "delete the |s_i s_j| = 1 gate", MAIN_FILES, [MAIN_MAG],
             base_out, base_code, want_change=True, want_exit=1)

    head("AFTER -- this tree, where the gate label is emitted by the code path")
    new_dir = mutate_tree([], NEW_FILES)
    new_base, new_code = run_controls(new_dir)
    committed = open(os.path.join(FG, "controls_output.txt")).read()
    claim("this tree's controls_output.txt regenerates byte-identically",
          new_base == committed,
          "%d bytes regenerated, %d committed, exit %d"
          % (len(new_base), len(committed), new_code))
    a1 = run_case("AFTER-1", "delete the s_i^2 = 1 gate", NEW_FILES, [NEW_DIAG],
                  new_base, new_code, want_change=True, want_exit=0)
    run_case("AFTER-2", "delete the |s_i s_j| = 1 gate", NEW_FILES, [NEW_MAG],
             new_base, new_code, want_change=True, want_exit=1)
    a3 = run_case("AFTER-3", "magnitudes before the diagonal", NEW_FILES,
                  [NEW_ORDER], new_base, new_code, want_change=True, want_exit=0)
    run_case("AFTER-4", "stop counting signs read", NEW_FILES, [NEW_SIGNS],
             new_base, new_code, want_change=True, want_exit=0)

    head("WHAT MOVED, AND WHAT DID NOT")
    for tag, out in (("AFTER-1", a1), ("AFTER-3", a3)):
        base_rows = [l for l in new_base.split("\n") if "[PASS]" in l
                     or "[CANNOT FAIL]" in l or "[FAIL]" in l]
        mut_rows = [l for l in out.split("\n") if "[PASS]" in l
                    or "[CANNOT FAIL]" in l or "[FAIL]" in l]
        claim("%s: every scored row keeps its label and its condition -- %d rows, "
              "%d label change(s)" % (tag, len(base_rows),
                                      sum(a.split(" ")[1] != b.split(" ")[1]
                                          for a, b in zip(base_rows, mut_rows))),
              len(base_rows) == len(mut_rows)
              and all(a.split(" ")[1] == b.split(" ")[1]
                      for a, b in zip(base_rows, mut_rows)))
        moved = [i for i, (a, b) in enumerate(zip(new_base.split("\n"),
                                                  out.split("\n"))) if a != b]
        claim("%s: the lines that DID move are the ones reporting where the "
              "predicate went -- %d line(s)" % (tag, len(moved)),
              len(moved) > 0,
              "; ".join("line %d" % (i + 1) for i in moved[:6]))

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
