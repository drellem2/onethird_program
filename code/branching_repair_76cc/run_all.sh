#!/bin/sh
# The instrument for mg-76cc -- the two sites mg-957f left open on mg-7e58:
#
#   OPEN 1  THE KERNEL HALF OF THE PREDICATE IS GONE.  g1's file-sha finding
#           covered c1_branching.py AND kern_a218.py; what replaced it pinned
#           the kernel on both sides of its own comparison, so a kernel that
#           moved reached neither.  This is the first site in this arc where a
#           repair REMOVED DETECTION rather than relocating a defect.   (r1)
#
#   OPEN 2  G-3 IS SHUT AT ONE REVISION, with 1 of 5 committed outputs
#           reproducing.                                                (r2)
#
# and two things that are not either of them:
#
#   r3  THE STANDING INSTRUCTION, APPLIED TO THIS REPAIR ITSELF -- the
#       pre-repair predicates run against the same inputs, because a check
#       that used to fire and now does not is invisible from the new side.
#   r4  THIS DELIVERABLE, CHECKED FOR THE DEFECT IT REMEDIES.
#
# Pure Python 3, no dependencies, NO NETWORK.
#
# EXIT-CODE CONVENTION.  Every r*.py exits 0 iff SELF-ERRORS == 0 AND
# FINDINGS == 0.  A non-zero exit means "this script has something to report",
# never "this script is broken"; both numbers are printed separately and every
# count names its population.  PREDICTIONS.md holds the exit code predicted for
# each script BEFORE it was run, with the misses kept as written.
#
# NO PIPE ANYWHERE (mg-c2b3): each script's stdout is REDIRECTED, its exit code
# read from $? on the next line, and the worst propagated.  r4 (iv) runs this
# very file with a red stub in it and checks that the red survives.
#
# NOTHING HERE WRITES INTO code/branching_audit_58da/,
# code/branching_audit_a218/, code/branching_audit_321d/,
# code/branching_audit_957f/, code/branching_repair_7e58/ OR
# code/branching_locate_db09/.  Every mutation happens in a temp git clone or a
# temp scratch tree.  r2 runs mg-58da's own run_all.sh, and it runs it IN A
# CLONE, because that script redirects into the very files under test.
#
# r2 and r3 each run mg-58da's g4_fleet.py more than once and it takes about a
# minute and a half a time; the whole of this file is several minutes.
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

run selftest_76cc.py
run r1_kernel.py
run r2_reproduce.py
run r3_prerepair.py
run r4_doccheck.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
