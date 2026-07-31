#!/bin/sh
# mg-fcf1: regenerate every number quoted in
# docs/audit-mg-2789-negative-control-4.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.
# Nothing here imports code/face_geometry/ -- rebuild.py builds the face
# complex from the definitions by the ideal-lattice route, because
# le_to_facet is one of the sites under audit.
#
# Measured runtime, 2026-07-30: 19 s total (audit_nc4.py 16 s, audit_extra.py
# 1 s, audit_gauge.py 2 s).
set -e
cd "$(dirname "$0")"

# mg-7522: every step below used to pipe into `tee` instead of redirecting.
# A pipeline's exit status in POSIX sh is its LAST command's, which is tee's
# and is 0 -- so a step could print failures, exit non-zero, and leave this
# runner exiting 0 with `set -e` never seeing anything.  Each step now
# redirects and has its own status read by an explicit `||` guard, then the
# transcript is `cat` so the terminal stream is unchanged.
#
# mg-c2b3 swept the arc for exactly this defect and did not reach this file:
# its population was "files named `run_all.sh`" and this one is not.  A
# population defined by a naming convention is not defined by the property
# under repair, which is the whole of mg-7522's OPEN 1.
#
# `set -o pipefail` is not used: the shebang is `/bin/sh`, which on Linux is
# dash, and dash rejects the option -- it would abort the runner at the line
# meant to make it safer.
echo "== A-F: reproduce the fire, absorbability, vacuity, mg-5630's premise =="
python3 audit_nc4.py 5 > out_nc4.txt || {
    cat out_nc4.txt; echo "audit_nc4.py FAILED"; exit 1; }
cat out_nc4.txt

echo
echo "== G-L: unproved remainders, tautologies, line-F re-run, brute force =="
python3 audit_extra.py > out_extra.txt || {
    cat out_extra.txt; echo "audit_extra.py FAILED"; exit 1; }
cat out_extra.txt

echo
echo "== M-P: the gauge finding, with a positive control on the detector =="
python3 audit_gauge.py > out_gauge.txt || {
    cat out_gauge.txt; echo "audit_gauge.py FAILED"; exit 1; }
cat out_gauge.txt
