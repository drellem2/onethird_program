#!/bin/sh
# The instrument for mg-2060 --- the independent audit of mg-db09.
# Pure Python 3, no dependencies, NO NETWORK.  ~20 min.
# `fetch2060.sh` is the one network script and this file does not call it.
set -e
D=$(dirname "$0")
cd "$D"
sh ./b0_repro.sh                          | tee out_b0_repro.txt   ; tail -1 out_b0_repro.txt
python3 -u selftest2060.py                | tee out_selftest.txt
python3 -u b1_branching.py  > out_b1_branching.txt  ; tail -1 out_b1_branching.txt
python3 -u b2_pathbasis.py  > out_b2_pathbasis.txt  ; tail -1 out_b2_pathbasis.txt
python3 -u b3_quotes.py     > out_b3_quotes.txt     ; tail -1 out_b3_quotes.txt
python3 -u b4_ours.py       > out_b4_ours.txt       ; tail -1 out_b4_ours.txt
python3 -u b5_successor.py  > out_b5_successor.txt  ; tail -1 out_b5_successor.txt
python3 -u b6_ledger.py     > out_b6_ledger.txt     ; tail -1 out_b6_ledger.txt
python3 -u b7_gz.py         > out_b7_gz.txt         ; tail -1 out_b7_gz.txt
