#!/bin/sh
# The instrument for mg-321d -- the INDEPENDENT AUDIT of mg-58da (673b4c0),
# which repaired code/branching_audit_a218/c1_branching.py after mg-d330
# reported that a re-run raised 24 findings where its own parser had gone
# blind.
#
#   h1  were the two questions actually kept SEPARATE, and is each answered?
#       B re-derived by re-running at the named revision; A re-derived by
#       classifying all 24 cells one at a time on this instrument's reader.
#   h2  is the narrowing at the GRAIN of the blindness?  Two sites where
#       mg-58da's own provenance apparatus asks a question at the grain of a
#       container rather than of the thing asked about.
#   h3  was the agreement across ALL FIVE re-established, or only the changed
#       one re-run?  The five named from disk, attributed by commit, all run.
#   h4  the two things this audit chose, which the ticket's lists do not name.
#   h5  does this audit's OWN document say what its own run said?  Every
#       published figure read back AT ITS SITE and compared against the
#       committed out_h*.txt, with each gate deletion-tested.  Runs last
#       because it reads the outputs the four above have just written.
#
# Pure Python 3, no dependencies, NO NETWORK.  ~3 min.
#
# THIS INSTRUMENT IS NOT ONE OF THE FIVE.  It lives in its own directory, no
# run_all.sh but this one invokes it, and it writes into
# code/branching_audit_a218/, code/branching_audit_58da/ and
# code/branching_locate_db09/ never -- every re-run happens in a scratch tree
# under $TMPDIR, and the members that are run in place have their stdout
# captured here and never redirected into a committed out_*.txt.
#
# EXIT-CODE CONVENTION.  Every h*.py exits 0 iff SELF-ERRORS == 0 AND
# FINDINGS == 0.  A non-zero exit means "this script has something to report",
# never "this script is broken".  Both numbers print separately and every
# count names its population.  PREDICTIONS.md holds the exit code AND the
# substantive answer predicted for each script BEFORE it was run, with the
# misses kept as written.
#
# h2, h3 and h4 ARE PREDICTED TO EXIT 1 and do.
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

run selftest_321d.py
run h1_questions.py
run h2_grain.py
run h3_setlevel.py
run h4_mine.py
run h5_doccheck.py

echo
echo "worst exit code: $WORST"
exit "$WORST"
