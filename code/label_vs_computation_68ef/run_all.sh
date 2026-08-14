#!/bin/sh
# mg-68ef -- can a check compare what a table HEADER claims against what the arm beneath it
# COMPUTES?
#
# Order matters.  m0 runs FIRST because m1's headline is a ZERO, and a zero is what a narrowed
# class, a broken segmenter or a matcher that never fires returns for free.
#
# NOT IN build.sh, and the reason is not cost (~40 s).  Nothing here is a property the estate must
# hold: the subject is a question put to pm-onethird about whether a class is checkable, and a
# measurement that gates is one its subjects learn to spell around.
#
# Every figure is a function of AS_OF except m1.6, the reflexive scan, which must read the
# worktree because this directory is younger than the pin -- an exemption by arithmetic, declared
# at the section.  There is no clock and no randomness anywhere in the suite, so two consecutive
# runs are byte-identical on all three transcripts.
set -e
cd "$(dirname "$0")"
worst=0
for arm in m0_selftest m1_reach m2_exhibits; do
    echo "=== $arm ==="
    python3 "$arm.py" >/dev/null 2>&1 || { rc=$?; [ "$rc" -gt "$worst" ] && worst=$rc; }
    tail -3 "out_$arm.txt"
done
echo "worst suite exit: $worst"
exit "$worst"
