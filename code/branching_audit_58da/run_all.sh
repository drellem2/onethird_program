#!/bin/sh
# The instrument for mg-58da -- the two questions mg-d330 left open about
# mg-a218's c1_branching.py:
#
#   A. are the 24 findings its parser now raises REAL?   (g3)
#   B. does the 198-cell reproduction still stand?       (g1, g2)
#
# and the set-level property that lives BETWEEN mg-a218's five scripts rather
# than inside any one of them (g4).
#
# Pure Python 3, no dependencies, NO NETWORK.  There is no fetch script here
# and no fifth Temperley-Lieb kernel: this ticket's questions are about
# parsing and provenance, not about the mathematics, which four instruments in
# this tree already measure and agree on.
#
# EXIT-CODE CONVENTION.  Every g*.py exits 0 iff SELF-ERRORS == 0 AND
# FINDINGS == 0.  A non-zero exit means "this script has something to report",
# never "this script is broken"; both numbers are printed separately and every
# count names its population.  PREDICTIONS.md holds the exit code predicted for
# each script BEFORE it was run, with the misses kept as written.
#
# g4 IS PREDICTED TO EXIT 1 and does: c3_withdrawal.py is red on the repaired
# tree for a reason that is mg-d330's second finding and is not closed here.
#
# NOTHING HERE WRITES INTO code/branching_audit_a218/ OR
# code/branching_locate_db09/.  g1, g2, g3 and part of g4 re-run mg-a218's
# c1_branching.py in a scratch directory against target text they supply, and
# g4 runs the five in place with their stdout captured here -- never redirected
# into their committed outputs, which are the record of what those audits found
# and not live gates.
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

run selftest_58da.py
run g1_provenance.py
run g2_redo.py
run g3_findings.py
run g4_fleet.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
