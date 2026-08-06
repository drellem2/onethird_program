#!/bin/sh
# mg-1d26 -- the verdict path's other 551 lines, certified: the six deletions
# outside mg-4adb's certified population that turned a red gate green, four of
# them silently, and the one that made the checker READ NO DOCUMENT AND RETURN
# 0.  Pure Python 3, no dependencies, NO NETWORK.  `git` is used against this
# repository, which is local.  About 25 minutes, almost all of it P2's sweep.
set -e
cd "$(dirname "$0")"

# THE GATE IS THE LAST COMMAND OF THIS FILE, and nothing may be appended below
# it -- mg-4adb's rung, obeyed by the instrument that widens mg-4adb's
# population.  A POSIX script's exit status is its last command's, so what
# carries P2's verdict out of this file is the CALL ITSELF.
#
# AND THAT IS WHY P2 HAS NO out_p2_widened.txt.  Redirecting it to a transcript
# and `cat`ing the transcript afterwards would put a `cat` after the gate -- a
# command whose status is 0 whatever P2 returned.  That is the defect mg-c2b3
# found in these runners as a `tee`, mg-6ef4 found again as `set -e`, and
# mg-4adb repaired by making the gate the last command; an author who broke it
# to obtain a tidier artifact would have written this ticket's finding into its
# own instrument.  The whole-suite transcript `out_run_all_1d26.txt` is the
# committed evidence for P2, and every row of both sweeps is in it.
python3 selftest1d26.py > out_selftest_1d26.txt || {
    cat out_selftest_1d26.txt; echo "selftest1d26.py FAILED"; exit 1; }
cat out_selftest_1d26.txt

python3 p1_population.py > out_p1_population.txt \
    || { cat out_p1_population.txt; echo "P1 FAILED"; exit 1; }
cat out_p1_population.txt

python3 p3_vacuous.py > out_p3_vacuous.txt \
    || { cat out_p3_vacuous.txt; echo "P3 FAILED"; exit 1; }
cat out_p3_vacuous.txt

echo
echo "P2 -- the widened sweep, before and after.  Its output is NOT redirected"
echo "and its exit status is this file's:"
python3 p2_widened.py
