#!/bin/sh
# The instrument for mg-957f -- the INDEPENDENT AUDIT of mg-7e58 (4372fae),
# which repaired mg-58da's provenance apparatus on mg-321d's G-1 and G-2:
#
#   G-1  g1_provenance.py asked "did the measuring half change?" and answered
#        with a FILE SHA, so mg-58da's own commit made it exit 1 on a finding
#        its own section (iv) refutes.
#   G-2  g4_fleet.py attributed by "committed sha vs WORKING-TREE sha", so the
#        instant 673b4c0 landed it said ed9cde4 had touched c1_branching.py.
#
# Pure Python 3, no dependencies, NO NETWORK.  Expect roughly 25-40 minutes:
# j1, j2 and j4 run mg-58da's and mg-a218's scripts inside real git clones,
# and g4_fleet.py alone takes about a minute a run.
#
# EXIT-CODE CONVENTION.  Every j*.py exits 0 iff SELF-ERRORS == 0 AND
# FINDINGS == 0.  A non-zero exit means "this script has something to report",
# never "this script is broken"; both numbers are printed separately and every
# count names its population.  PREDICTIONS.md holds the exit code predicted for
# each script BEFORE it was run, with the miss kept as written.
#
# j2 AND j4 ARE PREDICTED TO EXIT 1 AND DO.  j2 carries F-1 (the repair's new
# predicate cannot see a kernel that moved, and the predicate it replaced
# could) and j4 carries F-2 (G-3 is shut at one revision, not shut).  The
# things this audit does NOT close -- c3_withdrawal.py's redness and mg-321d's
# M-1 and M-2 -- are reported BY NAME in j3 and never counted as findings of
# this audit's own.
#
# NOTHING HERE WRITES INTO code/branching_audit_58da/,
# code/branching_audit_321d/, code/branching_audit_a218/,
# code/branching_repair_7e58/ OR code/branching_locate_db09/.  Every mutation
# happens in a temp git clone or a temp scratch tree, and every script run in
# those directories has its stdout captured here -- never redirected into a
# committed output.  j4 runs ./run_all.sh, which DOES overwrite committed
# outputs, and for that reason runs it only inside a clone.
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

run selftest_957f.py
run j1_attribution.py
run j2_silencing.py
run j3_setlevel.py
run j4_reproduce.py
run j5_doccheck.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
