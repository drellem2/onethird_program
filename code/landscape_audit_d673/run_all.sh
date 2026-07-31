#!/bin/sh
# mg-d673 -- independent audit of mg-ebd8 / 714aceb.
# Pure Python 3, no third-party imports.  Shares no code with
# code/landscape_ebd8/ (the target), code/semigroup_note/, code/face_geometry/,
# code/unified_gate_8fd1/ or code/hodge_leverage/.
#
# diag_p2_cross.py is FORENSICS ONLY -- it imports the target's module to
# locate a disagreement, and no verdict rests on it.  It is not run here.
set -e
cd "$(dirname "$0")"
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
python3 audit_populations.py 6 > out_populations.txt || {
    cat out_populations.txt; echo "audit_populations.py FAILED"; exit 1; }
cat out_populations.txt
python3 audit_spectrum.py 40 > out_spectrum.txt || {
    cat out_spectrum.txt; echo "audit_spectrum.py FAILED"; exit 1; }
cat out_spectrum.txt
python3 audit_e6_e8_m0.py 5 > out_e6_e8_m0.txt || {
    cat out_e6_e8_m0.txt; echo "audit_e6_e8_m0.py FAILED"; exit 1; }
cat out_e6_e8_m0.txt
python3 audit_identifications.py 5 > out_identifications.txt || {
    cat out_identifications.txt; echo "audit_identifications.py FAILED"; exit 1; }
cat out_identifications.txt
python3 audit_addenda.py > out_addenda.txt || {
    cat out_addenda.txt; echo "audit_addenda.py FAILED"; exit 1; }
cat out_addenda.txt
