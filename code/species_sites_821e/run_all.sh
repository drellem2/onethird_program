#!/bin/sh
# mg-821e -- the repair of mg-6cb9's three OPEN items against mg-d633 / e8fbd4f.
#
#   OPEN 1  "EVERY REGULAR FILE" was true only because no tree had a
#           SUBDIRECTORY.  All three walks now recurse, so the claim is true by
#           construction rather than by accident of the tree.        -> P1
#   OPEN 2  the check that closes B1 was called by 0 of 3 species runners.  The
#           REMOVAL QUESTION is asked first and answered with measurements
#           (outcome 2), then the check is wired into all three and verified BY
#           RUNNING each of them and reading the check's own output. -> P3
#   OPEN 3  C4's anchors were a PRESENCE test over a document that writes 3 of
#           its 5 anchors more than once.  Each is now checked at the section a
#           reader meets it in.                                      -> P2
#
# Pure Python 3, no dependencies, NO NETWORK.  About 4 minutes, almost all of
# it P3's twelve `run_all.sh` executions.
#
# THIS INSTRUMENT MUTATES THE WORKTREE IT IS RUN IN, one edit at a time, and
# restores it.  `git status --porcelain` AND the full `git diff` are captured
# before every probe and compared after it; any difference stops the run with
# exit 2.  The self-test asserts that contract before anything else runs.  Run
# it on a tree you are willing to see edited, and do not kill it mid-probe:
# the restore is in the process, so a SIGTERM leaves the last mutation on disk
# (it happened, and it is in OUTCOMES.md).
set -e
cd "$(dirname "$0")"

# NOT `| tee`: in a pipeline `set -e` sees the exit status of `tee`, which is
# always 0, so a FAILING self-test would not stop the run.  Every other runner
# in this arc does exactly that, and this one did too until its own self-test
# went red and the run still exited 0 -- a control that exists and does
# nothing, which is the class this ticket is about.
python3 -B selftest821e.py > out_selftest.txt || {
    cat out_selftest.txt; echo "SELFTEST FAILED"; exit 1; }
cat out_selftest.txt
python3 -B p1_depth.py     > out_p1_depth.txt   || { echo "P1 FAILED"; exit 1; }
python3 -B p2_sites.py     > out_p2_sites.txt   || { echo "P2 FAILED"; exit 1; }
python3 -B p3_wiring.py    > out_p3_wiring.txt  || { echo "P3 FAILED"; exit 1; }

echo
echo "Headline lines:"
grep -h '^P[123] TOTAL BAD:\|^selftest821e' out_*.txt || true
echo
echo "Every one of those totals is followed IN THE OUTPUT by its own extent."
echo "P3a is the part that is not a probe: it is the REMOVAL QUESTION, asked"
echo "before the wiring rather than after it, with each candidate removal"
echo "measured and the outcome named.  A check with zero callers is the"
echo "cheapest moment to ask whether it should exist at all."
