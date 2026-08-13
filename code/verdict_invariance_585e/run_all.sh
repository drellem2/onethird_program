#!/bin/sh
# mg-585e — can a self-exempting transcript be made non-oscillating?  Standard library only.
#   v1  the oscillation, counted over the record instead of over five runs
#   v2  where in the transcript it lives, located by running the real g0 on controlled trees
#   v3  the candidate answer, built and run on both verdicts and priced
#   v0  the controls — and they run LAST, see below
#
# NOT IN build.sh.  This directory demonstrates and prices a change to ANOTHER ticket's
# instrument; it does not make it, so there is nothing here for the merge gate to enforce.
# Adding an arm to the gate that grades a proposal would make the proposal binding by the
# back door.  README §6 says who owns the decision.
#
# v0 RUNS LAST, WHICH IS THE OPPOSITE OF EVERY OTHER SELFTEST IN THIS ESTATE.  Its §4 scans
# the transcripts the other three arms have just written for an absolute path — mg-f771's own
# subject — and a scan of the PREVIOUS run's transcripts grades a tree nobody is committing.
# The cost is that a broken library is not caught before the arms use it; it is bought back
# by every arm catching its own exceptions and printing the traceback INTO its transcript.
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so
# a red arm would be invisible and this script green forever (mg-06d1 D2).
#
# STDOUT ONLY, and the reason is one estate over: g0 uses stderr as a jitter channel, and v3
# §3 READS that stderr to show the outcome survives the move.  Folding it into a tracked
# transcript would put a run-dependent count into a committed file — the defect this whole
# directory is about, committed by the directory reporting it.
d=$(cd "$(dirname "$0")" && pwd)
TMPS=""
trap 'rm -f $TMPS; exit' EXIT INT TERM HUP
STATUS=0
for arm in v1_oscillation v2_partition v3_invariant v0_selftest
do
    tmp="$d/.out_$arm.txt.partial"
    TMPS="$TMPS $tmp"
    python3 "$d/$arm.py" > "$tmp"
    RC=$?
    mv "$tmp" "$d/out_$arm.txt"
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-585e verdict-invariance suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
