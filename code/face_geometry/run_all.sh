#!/bin/sh
# mg-276d: regenerate every number quoted in
# docs/OneThird-Intrinsic-Face-Geometry-Probe.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.
# Measured runtime on a 2024 laptop, 2026-08-10 (re-measured by mg-17aa on the
# tree that ships this comment, not carried forward -- mg-e35b's own figures
# were 19.4 / 2.2 on 2026-07-31): 20.8 s total -- controls.py 2.6 s, run_probe.py
# at n <= 6 the remaining 18.2 s.  So this battery stays in the order-seconds
# regime and needs no scoping.  WHAT MOVED AND WHY: mg-17aa's falsifiability row
# runs eight extra light sweeps of the 86-poset population -- one per row to
# check the exhibit route reproduces the main sweep's counters, one no-op world,
# and one mis-predicted world per localised row -- which is +0.4 s of the +1.4.
# The rest is measurement noise between two dates and is not attributed.
#
# IT IS NOT "CI-ADJACENT", and this comment said it was until mg-e35b (mg-fcf1's
# minor finding).  There is NO CI in this repository -- no .github/, no
# .gitlab-ci.yml, no .circleci/, no Makefile -- and the only runners are
# hand-invoked run_all.sh scripts like this one.  "CI-adjacent" was aspirational
# and read as a description, which is the same defect this battery exists to
# catch, one layer out: text that claims more than what is there.
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
