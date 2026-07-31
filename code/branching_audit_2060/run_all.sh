#!/bin/sh
# The instrument for mg-2060 --- the independent audit of mg-db09.
# Pure Python 3, no dependencies, NO NETWORK.  ~20 min.
# `fetch2060.sh` is the one network script and this file does not call it.
set -e
D=$(dirname "$0")
cd "$D"
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
sh ./b0_repro.sh > out_b0_repro.txt || {
    cat out_b0_repro.txt; echo "b0_repro.sh FAILED"; exit 1; }
cat out_b0_repro.txt ; tail -1 out_b0_repro.txt
python3 -u selftest2060.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftest2060.py FAILED"; exit 1; }
cat out_selftest.txt
python3 -u b1_branching.py  > out_b1_branching.txt  ; tail -1 out_b1_branching.txt
python3 -u b2_pathbasis.py  > out_b2_pathbasis.txt  ; tail -1 out_b2_pathbasis.txt
python3 -u b3_quotes.py     > out_b3_quotes.txt     ; tail -1 out_b3_quotes.txt
python3 -u b4_ours.py       > out_b4_ours.txt       ; tail -1 out_b4_ours.txt
python3 -u b5_successor.py  > out_b5_successor.txt  ; tail -1 out_b5_successor.txt
python3 -u b6_ledger.py     > out_b6_ledger.txt     ; tail -1 out_b6_ledger.txt
python3 -u b7_gz.py         > out_b7_gz.txt         ; tail -1 out_b7_gz.txt
