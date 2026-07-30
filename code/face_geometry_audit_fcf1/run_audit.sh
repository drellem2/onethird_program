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

echo "== A-F: reproduce the fire, absorbability, vacuity, mg-5630's premise =="
python3 audit_nc4.py 5 | tee out_nc4.txt

echo
echo "== G-L: unproved remainders, tautologies, line-F re-run, brute force =="
python3 audit_extra.py | tee out_extra.txt

echo
echo "== M-P: the gauge finding, with a positive control on the detector =="
python3 audit_gauge.py | tee out_gauge.txt
