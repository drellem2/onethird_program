#!/bin/sh
# mg-4700 -- INDEPENDENT AUDIT of mg-821e, which repaired mg-6cb9's three OPEN
# items against mg-d633 / e8fbd4f.
#
#   OPEN 1  "EVERY REGULAR FILE" was true only because no tree had a
#           SUBDIRECTORY.  A contingent extent and a sound one look identical
#           from the outside, so this plants directories and RUNS the
#           checkers -- and hunts for a second condition nobody stated.  -> Q1
#   OPEN 2  the check that closes B1 was called by 0 of 3 species runners.
#           Verified by EXECUTING all three run_all.sh and reading the
#           check's own output in each, not by grepping the call.          -> Q2
#   OPEN 3  C4's anchors were a PRESENCE test.  Each is deleted at the site a
#           reader meets it in, every other copy left standing.            -> Q3
#   and     DO NOT DISTURB WHAT IS CONFIRMED: mg-6cb9's own battery, run
#           unmodified, and its published transcripts against the live run. -> Q4
#
# Pure Python 3, no dependencies, NO NETWORK.  About 6 minutes, almost all of
# it Q2's twenty-one `run_all.sh` executions.
#
# THIS INSTRUMENT MUTATES THE WORKTREE IT IS RUN IN, one edit at a time, and
# restores it.  `git status --porcelain` AND the full `git diff` are captured
# before every probe and compared after it; a difference stops the run.  The
# self-test asserts that contract in BOTH directions before anything else runs.
# Run it on a tree you are willing to see edited, and do not kill it mid-probe:
# the restore is in the process, so a SIGTERM leaves the last mutation on disk.
set -e
cd "$(dirname "$0")"

# NOT `| tee`.  In a pipeline `set -e` sees the exit status of `tee`, which is
# always 0, so a FAILING self-test would not stop the run.  mg-821e's 41ac5d4
# fixed exactly this in its own runner and recorded that every other runner in
# this arc still has it; Q2e measures two of those.  Repeating the defect in
# the file that reports it would be its own kind of answer.
python3 -B selftest4700.py > out_selftest.txt || {
    cat out_selftest.txt; echo "SELFTEST FAILED"; exit 1; }
cat out_selftest.txt

python3 -B q1_depth.py    > out_q1_depth.txt    || { echo "Q1 has findings"; }
python3 -B q2_wiring.py   > out_q2_wiring.txt   || { echo "Q2 has findings"; }
python3 -B q3_sites.py    > out_q3_sites.txt    || { echo "Q3 has findings"; }
python3 -B q4_standing.py > out_q4_standing.txt || { echo "Q4 has findings"; }

echo
echo "Headline lines:"
grep -h '^Q[1234] TOTAL BAD:\|^Q[1234] PREDICTIONS MISSED:\|^selftest4700' \
    out_*.txt || true
echo
echo "Q1..Q4 exit 1 when they HAVE a finding, so a non-zero exit from any of"
echo "them is this audit working and not this audit broken -- the four"
echo "\`|| { echo ... }\` above say so rather than hiding it.  Every total is"
echo "followed IN ITS OWN OUTPUT by the extent that total ranges over."
echo
echo "PREDICTIONS MISSED is NOT expected to be zero.  PREDICTIONS.md was"
echo "written and committed before a single probe ran and has not been edited;"
echo "the misses are named in OUTCOMES.md.  A battery whose expectations are"
echo "written after the run cannot be wrong."
