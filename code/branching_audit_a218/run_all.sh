#!/bin/sh
# The instrument for mg-a218 -- the independent audit of the mg-db09 repair
# (mg-e8b8 / 2e66d03).  Pure Python 3, no dependencies, NO NETWORK at all --
# there is no fetch script in this directory, because every source this audit
# needs was already fetched and committed by mg-db09 and by mg-2060 and this
# audit reads those.
#
# EXIT-CODE CONVENTION, and it is the whole point of the numbers below:
#   every c*.py exits 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
#   A non-zero exit means "this script has something to report", not "this
#   script is broken".  Both numbers are printed separately, every count names
#   its population, and PREDICTIONS.md holds the exit code predicted for each
#   script BEFORE any of them was run.
set -u
D=$(dirname "$0")
cd "$D"
WORST=0

run() {
    printf '%s\n' "----- $1 -----"
    if [ "${1##*.}" = "sh" ]; then sh "./$1" > "out_${1%.*}.txt" 2>&1
    else python3 -u "$1" > "out_${1%.*}.txt" 2>&1
    fi
    RC=$?
    tail -1 "out_${1%.*}.txt"
    echo "exit $RC"
    [ "$RC" -le "$WORST" ] || WORST=$RC
}

run selftest_a218.py
run c0_repro.sh
run c1_branching.py
run c2_vertexsets.py
run c3_withdrawal.py
run c4_seam.py
run c5_record.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
