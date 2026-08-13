#!/bin/sh
# mg-5987 — run every arm, in order, writing one transcript each.
#
# g0 is FIRST and its exit code is the one to watch: every number in g1–g3 is a function of
# `profile()` and the closed forms, and g0 is what says those are what they claim to be.
#
# ~5 min, dominated by g2's n = 8 primitive sweep (12 524 classes, exact rationals throughout).
# Two consecutive runs are byte-identical: no clock, no randomness, no sampling anywhere.
set -e
cd "$(dirname "$0")"

worst=0
for arm in g0_selftest g1_step1 g2_step2 g3_dial; do
    echo "### $arm"
    python3 -B "$arm.py" > "out_$arm.txt" 2>&1 || worst=$?
    tail -3 "out_$arm.txt"
done
echo "worst arm exit: $worst"
exit $worst
