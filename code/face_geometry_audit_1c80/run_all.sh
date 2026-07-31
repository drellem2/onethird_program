#!/bin/sh
# mg-1c80 -- regenerate every number quoted in
# docs/audit-mg-da45-nc4-gate-repair.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured on a
# 2024 laptop, 2026-07-30: 26 s wall total -- a1_gates.py 0.6 s, a2_antichain.py
# 1.1 s, a3_n6_population.py 6.4 s, a4_witness.py 0.7 s, a5_claims.py 1.6 s,
# a6_mutations.py 16 s (eight full battery runs on patched copies).
#
# Nothing here writes into ../face_geometry.  a5_claims.py and a6_mutations.py run
# `controls.py` as a subprocess, in place and on temporary copies respectively;
# no script in this directory imports it.  No script re-runs mg-da45's own
# verifier (`code/face_geometry_landing_da45/`) -- its committed output is read
# as text where it is quoted, and every number is remeasured here instead.
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
python3 a1_gates.py > out_gates.txt || {
    cat out_gates.txt; echo "a1_gates.py FAILED"; exit 1; }
cat out_gates.txt
python3 a2_antichain.py > out_antichain.txt || {
    cat out_antichain.txt; echo "a2_antichain.py FAILED"; exit 1; }
cat out_antichain.txt
python3 a3_n6_population.py > out_n6.txt || {
    cat out_n6.txt; echo "a3_n6_population.py FAILED"; exit 1; }
cat out_n6.txt
python3 a4_witness.py > out_witness.txt || {
    cat out_witness.txt; echo "a4_witness.py FAILED"; exit 1; }
cat out_witness.txt
python3 a5_claims.py > out_claims.txt || {
    cat out_claims.txt; echo "a5_claims.py FAILED"; exit 1; }
cat out_claims.txt
python3 a6_mutations.py > out_mutations.txt || {
    cat out_mutations.txt; echo "a6_mutations.py FAILED"; exit 1; }
cat out_mutations.txt
