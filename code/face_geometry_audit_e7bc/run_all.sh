#!/bin/sh
# mg-e7bc: INDEPENDENT AUDIT of the mg-d0e2 repair (mg-04a8 / c7f9673).
#
# Pure Python 3, no third-party packages.  Measured runtime 2026-07-30 on a 2024
# laptop: about 150 s total -- g1 2 s (seven runs of the label check as a
# subprocess, no battery), g2 26 s (twelve control batteries), g3 12 s (five
# batteries plus the in-process reversions), g4 110 s (two batteries plus a
# re-run of both of the repair's own scripts, one of which itself runs three of
# mg-d0e2's).
#
# WHAT IT IS FOR.  mg-d0e2 found a check that HELD on an artifact in which every
# scored row read [FAIL].  mg-04a8 says it repaired that.  g1 runs the repaired
# check ON THAT ARTIFACT and reports the process exit status, then runs it on
# five broken artifacts of this audit's own that differ from it in direction,
# scale, channel and kind.  g2 re-derives the nine deletion mutations from the
# source and adds two the ticket does not name.  g3 takes the repair's WOULD
# DIFFER UNDER statements and MAKES THE CHANGE.  g4 reports the artifact's own
# threshold, makes the control that carries it fire, checks seventeen anchored
# figure-statements across five sites, and re-runs the repair's transcripts.
#
# CLAIMS vs FINDINGS, and the exit status is only the first.  A BROKEN claim
# means this instrument is wrong.  A FINDING means mg-04a8 is.  An audit whose
# exit code conflates the two cannot be run in CI by anyone -- so this script
# exits nonzero on a broken claim of its own, and the findings are counted and
# printed where a reader will see them.
#
# NOTHING UNDER ../face_geometry IS WRITTEN.  Every mutation is applied to a
# copy in a temporary directory and every battery run captures stdout instead of
# tee-ing it.
#
# NOT `python3 x.py | tee out.txt`, and that is deliberate: a pipeline's exit
# status in POSIX sh is the LAST command's, so `tee` succeeding would mask a
# verifier exiting 1 -- a committed transcript saying BROKEN under a run_all.sh
# that exited 0.  mg-f922 found exactly that shape in this repository.
set -e
cd "$(dirname "$0")"

run() {
    out=$1
    shift
    set +e
    python3 "$@" > "$out" 2>&1
    status=$?
    set -e
    cat "$out"
    return $status
}

echo "== g1: THE PRIMARY MEASUREMENT -- the repaired check on the broken artifact =="
run out_g1_positive_control.txt g1_positive_control.py

echo
echo "== g2: the deletion test, re-derived, both directions, 9 + 2 =="
run out_g2_deletion.txt g2_deletion.py

echo
echo "== g3: the WOULD DIFFER UNDER statements, tested by making the change =="
run out_g3_differs_under.txt g3_differs_under.py

echo
echo "== g4: the threshold, the seam, and the re-run =="
run out_g4_seams.txt g4_seams.py
