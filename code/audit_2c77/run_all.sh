#!/bin/sh
# run_all.sh -- the mg-2c77 audit suite.
#
# NO `| tee` ANYWHERE (mg-c2b3, mg-f922).  Each script's stdout is REDIRECTED
# and its status re-read from $?, so a red verifier cannot hide under a green
# runner.  The worst status is carried out at the end and this runner exits on
# it.
#
# `set -e` is NOT used, and that is deliberate (mg-5040's fifth rung, mg-6ef4):
# with `set -e` the first non-zero script would end the run and the remaining
# ones would never be scored, which is indistinguishable from their passing.
# Every script runs; every status is recorded; the worst one is the exit code.
#
# Expected worst status is 1.  Three of the five scripts have something to
# report.  A worst status of 0 from this suite would mean the findings went
# away, which is a result to look at and not a result to celebrate.

cd "$(dirname "$0")" || exit 2
WORST=0

run() {
    name="$1"
    printf '%-24s ' "$name"
    python3 -W ignore "$name" > "out_${name%.py}.txt" 2>&1
    rc=$?
    printf 'exit %d\n' "$rc"
    if [ "$rc" -gt "$WORST" ]; then WORST=$rc; fi
}

run selftest_2c77.py
run q1_reason.py
run q2_bound_edge.py
run q3_operands.py
run q4_prerepair.py
run q5_discriminator.py

echo "----------------------------------------------------------------------"
echo "worst status: $WORST"
exit "$WORST"
