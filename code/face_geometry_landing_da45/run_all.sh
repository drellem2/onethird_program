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
python3 verify_landing.py | tee out_verify.txt
