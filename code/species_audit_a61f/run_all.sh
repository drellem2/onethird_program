#!/bin/sh
# code/species_audit_a61f -- the independent audit instrument for mg-a61f.
# Pure Python 3, no dependencies, NO NETWORK.  ~2 minutes.
#
# fetch_sources.sh is the ONE script here that uses the network and it is NOT
# called from this file: a5_quotes.py reads the committed quotes_a61f.txt.
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
python3 selftesta61f.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftesta61f.py FAILED"; exit 1; }
cat out_selftest.txt
python3 a1_headline.py    > out_a1_headline.txt
python3 a2_bidigare.py    > out_a2_bidigare.txt
python3 a3_hopf.py        > out_a3_hopf.txt
python3 a4_counts.py      > out_a4_counts.txt
python3 a5_quotes.py      > out_a5_quotes.txt
python3 a6_boundary.py    > out_a6_boundary.txt
echo
grep -h "TOTAL BAD" out_a*.txt
