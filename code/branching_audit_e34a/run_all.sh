#!/bin/sh
# The instrument for mg-e34a -- the INDEPENDENT AUDIT of mg-76cc (4755d02),
# which repaired mg-957f's two open sites on mg-7e58.
#
# Pure Python 3, no dependencies, NO NETWORK.
#
# EXIT-CODE CONVENTION.  Every k*.py exits 0 iff SELF-ERRORS == 0 AND
# FINDINGS == 0.  A non-zero exit means "this script has something to
# report", never "this script is broken"; the two numbers are printed
# separately and every count names its population.  PREDICTIONS.md holds the
# exit code predicted for each script BEFORE it was run, with the misses kept
# as written.
#
# k1 and k4 ARE PREDICTED TO EXIT 1 and do.  k1 books the cancelling pair;
# k4 books the rationale that names it and mg-76cc's own finding reader.
#
# NO PIPE ANYWHERE (mg-c2b3): each script's stdout is redirected, `$?` is read
# on the next line and the worst is propagated.  `cmd | tee out` would report
# tee's exit code and a red script would come back green.
#
# NOTHING HERE WRITES INTO code/branching_audit_58da/,
# code/branching_audit_a218/, code/branching_audit_957f/,
# code/branching_repair_76cc/ or code/branching_locate_db09/.  Every run that
# mutates anything happens in a clone under the system temp directory.
#
# k2 runs mg-58da's own run_all.sh in a clone and takes about a minute and a
# half; k1 makes 21 pinned g1 runs across 7 clones.  Several minutes in all.
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

run selftest_e34a.py
run k1_prerepair.py
run k2_five.py
run k3_undisturbed.py
run k4_cancel.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
