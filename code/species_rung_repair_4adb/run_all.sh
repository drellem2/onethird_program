#!/bin/sh
# mg-4adb -- the repair of mg-6ef4's two OPEN items: the fifth rung (`set -e`,
# one line outside every deletion population) and the second layer (an
# unreadable regular file filed under ENCODING with `w3_scope` silent).
# Pure Python 3, no dependencies, NO NETWORK; `git` is used against this
# repository, which is local.
#
# TWO AND A HALF HOURS, and about two of them are v1.  That is not an
# accident of implementation, it is the population: v1 deletes EVERY LINE of
# three runners, one at a time, and EXECUTES the runner each time.  The count
# is not written here as a figure -- v1's section V1a prints it as
# `TOTAL RUNNER EXECUTIONS IN V1c`, computed from the files -- and most of
# the clock is code/species_repair_6f61/run_all.sh, which is half a minute a
# run.  A cheaper population would be a smaller one, and a smaller one is
# exactly what mg-6ef4's F3 was.  The transcripts are committed beside this
# file so that reading the result does not cost what producing it did.
#
# THIS FILE DOES NOT RELY ON `set -e` TO CARRY ANY VERDICT.  Every step reads
# its own status with an explicit `||`, and the last statement is an explicit
# `exit $RC`.  v3_self.py MEASURES that rather than asserting it: it deletes
# every line of this file, forces each step red one at a time, and deletes
# `set -e` to show the verdicts do not move.  `set -e` is still here, because
# two guards are better than one.
#
# Nothing is piped: a pipeline's exit status in POSIX sh is its LAST
# command's, and `set -o pipefail` is not available in dash (mg-c2b3).
#
# DO NOT KILL THIS RUN MID-PROBE.  v1 and v2 mutate the real worktree and the
# restore is inside the process.  A killed run can leave a `run_all.sh` with a
# line deleted, or a file at mode 000 in code/species_7d75.  To recover:
#     git checkout -- code/species_*/run_all.sh
#     git status --porcelain --untracked-files=all      # then remove leftovers
set -e
cd "$(dirname "$0")"

RC=0

python3 -B selftest4adb.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftest4adb.py FAILED"; exit 1; }
cat out_selftest.txt

python3 -B v1_population.py > out_v1_population.txt || RC=1
cat out_v1_population.txt

python3 -B v2_layer2.py > out_v2_layer2.txt || RC=1
cat out_v2_layer2.txt

python3 -B v3_self.py > out_v3_self.txt || RC=1
cat out_v3_self.txt

python3 -B v4_neighbours.py > out_v4_neighbours.txt || RC=1
cat out_v4_neighbours.txt

echo
echo "Headline lines:"
grep -h '^V[1-4] TOTAL BAD:\|^V[1-3] PREDICTIONS MISSED:\|^selftest4adb' \
    out_*.txt || true
echo
echo "\`Vn TOTAL BAD\` counts outcomes that contradict THIS REPAIR'S OWN"
echo "CLAIMS, so a repair that landed clean has four zeroes there."
echo "\`Vn PREDICTIONS MISSED\` counts predictions in PREDICTIONS.md that were"
echo "wrong, and PREDICTIONS.md was committed before any probe ran.  The two"
echo "are separate on purpose and neither is expected to be the other."
echo
echo "This run's own exit status is RC, set by the guards above and not by"
echo "\`set -e\` -- see the note at the head of this file, and v3_self.py"
echo "section V3c, which measures it."
exit $RC
