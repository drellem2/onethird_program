#!/bin/sh
# mg-6f61 -- the repair of mg-7d75 under mg-a61f's audit.
# Pure Python 3, no dependencies, NO NETWORK.  About 30 seconds, of which
# r2_columns.py is 27.
#
# r3_quotes.py reads code/species_audit_a61f/quotes_a61f.txt -- the poppler
# extraction the audit committed -- rather than re-fetching the PDFs.
# code/species_audit_a61f/fetch_sources.sh is the script that regenerates it,
# and it is the only network script in this cluster.
set -e
cd "$(dirname "$0")"

python3 selftest6f61.py > out_selftest.txt || { echo "SELFTEST FAILED"; exit 1; }
python3 r1_smallest.py  > out_r1_smallest.txt
python3 r2_columns.py   > out_r2_columns.txt          # ~27 s
python3 r3_quotes.py    > out_r3_quotes.txt
python3 check_doc.py    > out_check_doc.txt || { echo "CHECK_DOC FAILED"; exit 1; }

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

echo "done.  Headline lines:"
grep -h '^R[0-9] TOTAL BAD:\|^R2 PREDICTIONS MISSED:\|^CHECK_DOC:\|^selftest6f61' out_*.txt || true
echo
echo "R2 PREDICTIONS MISSED is NOT expected to be zero.  Both misses are"
echo "explained in out_r2_columns.txt R2e and in the repair document; a"
echo "battery whose expectations are written after the run cannot be wrong."
