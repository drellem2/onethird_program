#!/bin/sh
# run_all.sh -- the mg-b2af suite.
#
# The exit convention is taken from code/branching_audit_e34a/run_all.sh so
# that the ruler for "did this pass" is somebody else's: every script exits 0
# iff SELF-ERRORS == 0 and FINDINGS == 0.  A non-zero exit means THAT SCRIPT
# HAS SOMETHING TO REPORT, never that it is broken.
#
# Two of these are EXPECTED to exit 1, and PREDICTIONS.md says so in advance:
#   t1 -- three published figures reproduce at no commit
#   t3 -- the sentence under test is in a commit message and cannot be edited
#
# NO `set -e`.  A suite that stops at the first non-zero exit would run t1 and
# nothing else, and the exits above are results rather than failures.  Each
# script's status is captured and printed, and the worst is the suite's.

cd "$(dirname "$0")" || exit 2

worst=0
for s in selftest_b2af t1_population t2_gate t3_term t4_preserve; do
    printf '===> %s\n' "$s"
    python3 "$s.py" > "out_$s.txt" 2>&1
    rc=$?
    printf '     exit %d   %s\n' "$rc" \
        "$(grep '^TOTAL BAD:' "out_$s.txt" 2>/dev/null | tail -1)"
    [ "$rc" -gt "$worst" ] && worst=$rc
done

printf 'worst exit: %d\n' "$worst"
exit "$worst"
