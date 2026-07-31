#!/bin/sh
# mg-da45: closing mg-f1b2's F1 -- regenerate this landing's transcript.
#
# Pure Python 3, no third-party packages.  Measured runtime 2026-07-30 on a 2024
# laptop: 7.9 s -- the gate rebuild over all 86 posets n <= 5 plus the n = 6
# antichain (720 x 720), and two full runs of the face-geometry control battery
# (2.0 s each) launched as subprocesses to check the artifact regenerates and
# the scoring shape did not move.
#
# WHAT IT IS FOR.  mg-8a12 routed NEGATIVE CONTROL 4's rows on a number it took
# from mg-fcf1's audit output rather than measuring, and the number carried a
# false reason with it.  So verify_landing.py imports `face_complex` and
# `posets` and NOTHING ELSE: the corrected `controls.py` is run as a
# subprocess and read as text, never imported, so it cannot supply the evidence
# that it is correct.
#
# It exits 1 if any claim this landing prints is false.  The single [REFUTED]
# row is not a failure -- it is mg-8a12's printed claim, re-measured and found
# false, which is the finding this landing exists to close.
#
# The committed tree is never modified: the control battery is run with its
# stdout captured, not tee'd.  out_verify.txt regenerates byte-identically at
# this commit and will drift when controls.py's counts next change -- it reads
# the live tree, which is the point of it.
set -e
cd "$(dirname "$0")"

echo "== mg-da45: this landing's claims, re-measured without importing controls.py =="
# mg-c2b3: every step in this file that is followed by a bare `cat` of its
# own transcript used to pipe into `tee` instead of redirecting.  A pipeline's
# exit status in POSIX sh is its LAST command's, which is tee's and is 0 --
# so the step could print failures, exit 1, and leave this runner exiting 0.
# Each now redirects and has its status read by an explicit `||` guard.  The
# other steps in this file were already guarded and are untouched.
# `set -o pipefail` is not used: `/bin/sh` is dash on Linux, which rejects the
# option and would abort the runner at the line meant to make it safer.
# This note deliberately avoids writing the old pipeline out, so that a plain
# grep for it over the arc still counts only the sites that still have one.
python3 verify_landing.py > out_verify.txt || {
    cat out_verify.txt; echo "verify_landing.py FAILED"; exit 1; }
cat out_verify.txt
