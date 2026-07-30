#!/bin/sh
# mg-7d75 -- species / Hopf monoids as the framework behind BOTH S_n
# representation theory and the poset-quotient story.
# Pure Python 3, no dependencies, no network.  ~1 minute.
set -e
cd "$(dirname "$0")"
python3 selftest.py            | tee out_selftest.txt
python3 t1_grading.py          > out_t1_grading.txt
python3 t2_operation.py        > out_t2_operation.txt
python3 t3_bidigare.py         > out_t3_bidigare.txt
python3 t4_one_operation.py    > out_t4_one_operation.txt
python3 t5_hopf_monoid.py      > out_t5_hopf_monoid.txt
python3 t6_fock_and_record.py  > out_t6_fock_and_record.txt
echo
echo "TOTAL BAD across the battery:"
grep -h "TOTAL BAD" out_t*.txt
