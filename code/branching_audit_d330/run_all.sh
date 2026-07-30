#!/bin/sh
# The instrument for mg-d330 -- the independent audit of the mg-13b2 repair
# (ed9cde4).  Pure Python 3, no dependencies, NO NETWORK at all: there is no
# fetch script here, because every source this audit needs was fetched and
# committed by mg-db09 and mg-2060, and this audit measures the object itself.
#
# EXIT-CODE CONVENTION, and it is the whole point of the numbers below:
#   every e*.py exits 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
#   A non-zero exit means "this script has something to report", not "this
#   script is broken".  Both numbers are printed separately, every count names
#   its population, and ../../PREDICTIONS.txt holds the exit code predicted for
#   each script BEFORE it was run, with the misses kept as written.
#
# e4 RE-RUNS mg-a218's scripts in place with their stdout captured here.  It
# does not write into code/branching_audit_a218/ and must never be replaced by
# a call to that directory's own run_all.sh, which redirects into the committed
# outputs and would overwrite the record of what that audit found.
set -u
D=$(dirname "$0")
cd "$D"
WORST=0

run() {
    printf '%s\n' "----- $1 -----"
    python3 -u "$1" > "out_${1%.*}.txt" 2>&1
    RC=$?
    tail -1 "out_${1%.*}.txt"
    echo "exit $RC"
    [ "$RC" -le "$WORST" ] || WORST=$RC
}

run selftest_d330.py
run e1_vertexsets.py
run e2_labels.py
run e3_dispositions.py
run e4_rerun.py
run e5_seam.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
