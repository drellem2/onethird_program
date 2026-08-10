#!/bin/sh
# mg-5e82 -- the independent re-audit of mg-b417/cb417's n = 12 verdict.
#
# Runs every arm and writes its transcript beside it.  The worst exit wins: a suite
# that reports one finding per invocation is a suite people stop running.
#
# MEASURED RUNTIME on the host that produced the committed transcripts: 52.2 s wall
# (three runs: 52.2 / 54.4 / 52.2).  a3 (~25 s) and a7 (~13 s) are the copositivity
# bisections and are 73% of it; a5's n <= 6 sweep is another ~9 s.
#
# THIS LINE FIRST READ 66.3 s AND THAT NUMBER WAS NEVER MEASURED.  I wrote it into the
# comment that claims it was measured, in a suite whose subject is a bound nobody
# computed, and found it by running `time` in the next breath.  It is mg-17aa's D4
# committed again by an author who had just read mg-17aa's D4.  Kept, not silently
# corrected: the defect is that the sentence and the measurement were written in the
# wrong order, and deleting the evidence would leave only the sentence.
set -u
cd "$(dirname "$0")"
RC=0
for arm in a0_selftest a1_witness a2_gamma a3_mu a4_routes a5_scope a6_provenance a7_frontier; do
    printf '=== %s ===\n' "$arm"
    python3 "$arm.py" > "out_$arm.txt" 2>&1
    rc=$?
    tail -2 "out_$arm.txt"
    [ $rc -gt $RC ] && RC=$rc
done
printf '\n=== run_all exit %d ===\n' "$RC"
exit $RC
