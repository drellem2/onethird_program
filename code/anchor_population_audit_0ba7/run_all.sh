#!/bin/sh
# run_all.sh -- the mg-0ba7 suite.
#
# The exit convention is taken from code/repair_b2af/run_all.sh, which took it
# from code/branching_audit_e34a/run_all.sh, so that the ruler for "did this
# pass" is somebody else's twice over: every script exits 0 iff
# SELF-ERRORS == 0 and FINDINGS == 0.  A non-zero exit means THAT SCRIPT HAS
# SOMETHING TO REPORT, never that it is broken.
#
# Four are EXPECTED to exit non-zero and PREDICTIONS.md predicted three of
# them in advance:
#   a1 -- the published population is short by a letter
#   a3 -- anchors spent with no gate, outside the directory t2's rule walks
#   a4 -- PREDICTED 0, exits 1; the miss is kept
#   a6 -- the floor: revisions produced without the word `log`
#
# NO `set -e`.  The exits above are RESULTS, not failures, and a suite that
# stopped at the first one would run a1 and nothing else.
#
# a3 runs k2_five.py twice in a clone; it takes about four minutes and the
# rest of the suite takes about one.

cd "$(dirname "$0")" || exit 2

worst=0
for s in selftest_0ba7 a1_population a2_oldest a3_gate a4_labels \
         a5_resolution a6_floor; do
    printf '===> %s\n' "$s"
    python3 -W ignore "$s.py" > "out_$s.txt" 2>&1
    rc=$?
    printf '     exit %d   %s\n' "$rc" \
        "$(grep '^TOTAL BAD:' "out_$s.txt" 2>/dev/null | tail -1)"
    [ "$rc" -gt "$worst" ] && worst=$rc
done

printf 'worst exit: %d\n' "$worst"
exit "$worst"
