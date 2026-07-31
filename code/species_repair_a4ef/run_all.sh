#!/bin/sh
# mg-a4ef -- the repair of mg-73df's MAJOR (X3 still in force AT SOURCE) and
# of the seam between mg-6f61 and mg-f8fa.
# Pure Python 3, no dependencies, NO NETWORK except `git archive` against this
# repository, which is local.  About 5 seconds.
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
python3 selftesta4ef.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftesta4ef.py FAILED"; exit 1; }
cat out_selftest.txt
python3 s1_extent.py    > out_s1_extent.txt || { echo "S1 FAILED"; exit 1; }
python3 s2_seam.py      > out_s2_seam.txt   || { echo "S2 FAILED"; exit 1; }

# mg-821e, on mg-6cb9's F2.  THE CROSS-SECTION CHECK, WIRED.
# `e2_crosssection.py` is what closes mg-7dd3's B1: a claim struck in one
# section of a document and standing un-struck in another, which no
# per-section checker can see by construction.  B1 lived in a document THIS
# TREE checks.  The check existed, was correct, was named in every artifact a
# reader meets -- and was called by 0 of the 3 species run_all.sh, so the
# runner that would catch the next B1 did not execute it (mg-6cb9 F2, MAJOR).
# The removal question was asked BEFORE wiring and is answered, with
# measurements, in code/species_sites_821e/p3_wiring.py section P3a and in
# section 2 of docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md: OUTCOME 2,
# the generator is not removable.  The OUTPUT is printed, not just the call
# made: a call present in a script is not evidence of execution.
E2OUT=$(python3 ../species_extent_d633/e2_crosssection.py) || {
    echo "$E2OUT" | grep 'STANDING UN-STRUCK' || true
    echo "E2 CROSS-SECTION FAILED -- a struck claim stands un-struck elsewhere"
    exit 1
}
echo "cross-section check (mg-821e), its own output:"
echo "$E2OUT" | grep -E 'strike\(s\) measured|^E2 TOTAL BAD:'

echo
echo "Headline lines:"
grep -h '^S[12] TOTAL BAD:\|^selftesta4ef' out_*.txt || true
echo
echo "S1's TOTAL BAD is followed IN THE OUTPUT by a statement of its extent."
echo "That is the whole point of this instrument: mg-73df's MAJOR is what a"
echo "TOTAL BAD: 0 means when nobody says what it ranged over."
