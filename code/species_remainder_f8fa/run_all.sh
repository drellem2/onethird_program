#!/bin/sh
# mg-f8fa -- the remainder of mg-a61f not carried by mg-6f61.
# Pure Python 3, no dependencies, NO NETWORK, ~15 s.
set -e
cd "$(dirname "$0")"

python3 selftestf8fa.py    | tee out_selftest.txt
python3 w1_opposite.py     | tee out_w1_opposite.txt
python3 w2_typemismatch.py | tee out_w2_typemismatch.txt
python3 w3_scope.py        | tee out_w3_scope.txt

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
echo "out_w3_scope_before.txt is the SAME detector run against the tree"
echo "before this repair: 12 problems.  It is committed on purpose -- a"
echo "checker written after the fix and never seen to fail is not a checker."
