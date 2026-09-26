#!/bin/sh
# run_all.sh (mg-cfba): regenerate every fast transcript for docs/KSBFT-S-nested-balance.md.
# ~1.5 min, <= 1 process at a time (the searches are separate: run_search.sh).  Exit 1 on a failed assertion.
set -e
cd "$(dirname "$0")"
cc -O2 -o nb nb.c
python3 xcheck.py        > out_xcheck.txt
grep -q "mismatches 0" out_xcheck.txt
python3 witnesses.py     > out_witnesses.txt
python3 families.py      > out_families.txt
grep -q "NB failures 0" out_families.txt
python3 io.py            > out_io.txt
grep -q "2+2 (control, must be True)    contains induced 2+2: True" out_io.txt
: > out_randprime.txt
for s in 1 2 3 4; do python3 randprime.py $s 400 >> out_randprime.txt; done
python3 records.py       > out_records.txt
grep -q "records (non-chain, n>=3): 2534; NB failures 0" out_records.txt
python3 primal.py        > out_primal.txt
echo "run_all: OK"
