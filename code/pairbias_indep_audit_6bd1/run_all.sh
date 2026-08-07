#!/bin/sh
# mg-6bd1 — INDEPENDENT AUDIT of mg-345e. Run every instrument, in order.
set -e
cd "$(dirname "$0")"
python3 selftest6bd1.py      > out_selftest6bd1.txt 2>&1
python3 b1_ledger.py         > out_b1_ledger.txt
python3 b2_algebra.py        > out_b2_algebra.txt
python3 b3_census_scope.py   > out_b3_census_scope.txt
python3 b4_branches_and_arch.py > out_b4_branches_and_arch.txt
python3 b5_depth2_walk.py    > out_b5_depth2_walk.txt
echo "all instruments ran; see out_*.txt"
