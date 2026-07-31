#!/bin/sh
# mg-d633 -- the two printed extents that were WIDER than what the code reads,
# repaired and then MEASURED IN BOTH DIRECTIONS, plus the cross-section check
# a struck claim needs and no per-section checker can do.
# Pure Python 3, no dependencies, NO NETWORK.  About 2 minutes, almost all of
# it E3's 27 sandbox copies.
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
python3 selftestd633.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftestd633.py FAILED"; exit 1; }
cat out_selftest.txt
python3 e1_extents.py      > out_e1_extents.txt   || { echo "E1 FAILED"; exit 1; }
python3 e2_crosssection.py > out_e2_crosssection.txt || { echo "E2 FAILED"; exit 1; }
python3 e3_bothways.py     > out_e3_bothways.txt  || { echo "E3 FAILED"; exit 1; }

echo
echo "Headline lines:"
grep -h '^E[123] TOTAL BAD:\|^selftestd633' out_*.txt || true
echo
echo "Every one of those totals is followed IN THE OUTPUT by its own extent."
echo "That was mg-a4ef's remedy.  mg-7dd3 measured it and found two of the"
echo "four extent lines WIDER than what the code read, which is worse than"
echo "printing none.  E1 measures every extent line against an instrumented"
echo "open(); E3 probes every one of them from inside AND outside.  A"
echo "structural remedy is not done when it ships -- it is done when its"
echo "single point has been measured in both directions."
