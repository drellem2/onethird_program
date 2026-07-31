#!/bin/sh
# The instrument for mg-7e58 -- the repair of mg-58da's own provenance gear,
# on mg-321d's findings G-1 and G-2:
#
#   G-1  g1_provenance.py asked "did the measuring half change?" and answered
#        with a FILE SHA, so mg-58da's own commit made it exit 1 on a finding
#        its own section (iv) refutes.
#   G-2  g4_fleet.py attributed by "committed sha vs WORKING-TREE sha", so once
#        673b4c0 landed it said ed9cde4 had touched c1_branching.py.  It never
#        did.
#
# Pure Python 3, no dependencies, NO NETWORK.  Expect roughly 8-12 minutes:
# k1, k2 and k3 run mg-a218's and mg-58da's scripts many times over, several of
# them inside real git clones, and g4_fleet.py alone takes about a minute a run.
#
# EXIT-CODE CONVENTION.  Every k*.py exits 0 iff SELF-ERRORS == 0 AND
# FINDINGS == 0.  A non-zero exit means "this script has something to report",
# never "this script is broken"; both numbers are printed separately and every
# count names its population.  PREDICTIONS.md holds the exit code predicted for
# each script BEFORE it was run, with the misses kept as written.
#
# ALL FOUR ARE PREDICTED TO EXIT 0.  That is a stronger claim than usual and it
# is deliberate: this ticket's job is to make an apparatus right about itself,
# and an apparatus that still has something to report about itself has not
# finished.  The two OPEN items this repair does NOT close -- c3_withdrawal.py's
# redness and mg-d330's e4 presence test -- belong to g4, which is predicted to
# exit 1 and does, and k3 reports c3 by name rather than counting it as a
# finding of its own.
#
# NOTHING HERE WRITES INTO code/branching_audit_58da/,
# code/branching_audit_321d/, code/branching_audit_a218/ OR
# code/branching_locate_db09/.  Every mutation happens in a temp git clone or a
# temp tree, and every script run in those directories has its stdout captured
# here -- never redirected into a committed output.
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

run selftest_7e58.py
run k1_grain.py
run k2_selfprov.py
run k3_setlevel.py
run k4_doccheck.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
