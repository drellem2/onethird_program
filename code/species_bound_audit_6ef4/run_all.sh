#!/bin/sh
# mg-6ef4 -- independent audit of the mg-5040 repair (mg-4700's three OPEN
# items).  Pure Python 3, no dependencies, NO NETWORK; `git` is used against
# this repository, which is local.  About 12 minutes, most of it t2, which
# executes three run_all.sh four times each.
#
# THIS FILE DOES NOT RELY ON `set -e` TO CARRY ANY VERDICT, and that is not a
# style choice -- it is T2's finding applied here.  `set -e` at the top of a
# runner is a statement OUTSIDE every deletion population this arc has used,
# and deleting it alone turns three red runners green with their findings
# printed in full.  Every step below reads its own status with an explicit
# `||` guard, so deleting `set -e` from this file changes no verdict.  It is
# still here, because two guards are better than one.
#
# Nothing is piped: a pipeline's exit status in POSIX sh is its LAST command's,
# and `set -o pipefail` is not available in dash (mg-c2b3).
#
# DO NOT KILL THIS RUN MID-PROBE.  t1 and t2 mutate the real worktree and the
# restore is inside the process.  A killed run leaves three `run_all.sh` with
# `set -e` deleted; `git checkout -- code/species_*/run_all.sh` puts them
# back.  This happened twice while the instrument was being written and is
# kept in OUTCOMES.md.
set -e
cd "$(dirname "$0")"

RC=0

python3 -B selftest6ef4.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftest6ef4.py FAILED"; exit 1; }
cat out_selftest.txt

python3 -B t1_bound.py     > out_t1_bound.txt     || RC=1
python3 -B t2_wiring.py    > out_t2_wiring.txt    || RC=1
python3 -B t3_census.py    > out_t3_census.txt    || RC=1
python3 -B t4_restore.py   > out_t4_restore.txt   || RC=1

echo
echo "Headline lines:"
grep -h '^T[1-4] TOTAL BAD:\|^T[1-4] PREDICTIONS MISSED:\|^selftest6ef4' \
    out_*.txt || true
echo
echo "A non-zero exit from t1..t4 is the instrument WORKING: each exits 1 when"
echo "it has a finding.  \`Tn TOTAL BAD\` counts outcomes that contradict"
echo "MG-5040'S OWN CLAIMS; \`Tn PREDICTIONS MISSED\` counts predictions in"
echo "PREDICTIONS.md that were wrong, and PREDICTIONS.md was committed before"
echo "any probe ran.  The two are separate on purpose."
echo
echo "This run's own exit status is RC, set by the guards above and not by"
echo "\`set -e\` -- see the note at the head of this file."
exit $RC
