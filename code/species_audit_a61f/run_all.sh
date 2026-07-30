#!/bin/sh
# code/species_audit_a61f -- the independent audit instrument for mg-a61f.
# Pure Python 3, no dependencies, NO NETWORK.  ~2 minutes.
#
# fetch_sources.sh is the ONE script here that uses the network and it is NOT
# called from this file: a5_quotes.py reads the committed quotes_a61f.txt.
set -e
cd "$(dirname "$0")"
python3 selftesta61f.py   | tee out_selftest.txt
python3 a1_headline.py    > out_a1_headline.txt
python3 a2_bidigare.py    > out_a2_bidigare.txt
python3 a3_hopf.py        > out_a3_hopf.txt
python3 a4_counts.py      > out_a4_counts.txt
python3 a5_quotes.py      > out_a5_quotes.txt
python3 a6_boundary.py    > out_a6_boundary.txt
echo
grep -h "TOTAL BAD" out_a*.txt
