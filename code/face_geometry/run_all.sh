#!/bin/sh
# mg-276d: regenerate every number quoted in
# docs/OneThird-Intrinsic-Face-Geometry-Probe.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.
# Measured runtime on a 2024 laptop, 2026-07-30: 19 s total -- controls.py 1.9 s
# (of which NEGATIVE CONTROL 4, added by mg-2789, is 1.4 s over the full 86-poset
# n <= 5 population, so the CI-adjacent battery stays in the order-seconds
# regime and needs no scoping), run_probe.py at n <= 6 the remaining 17.4 s.
set -e
cd "$(dirname "$0")"

echo "== controls (positive + negative), all posets n <= 5 =="
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
python3 controls.py 5 > controls_output.txt || {
    cat controls_output.txt; echo "controls.py FAILED"; exit 1; }
cat controls_output.txt

echo
echo "== probe, all posets up to isomorphism n <= 6 =="
python3 run_probe.py 6 > probe_output_n6.txt || {
    cat probe_output_n6.txt; echo "run_probe.py FAILED"; exit 1; }
cat probe_output_n6.txt
