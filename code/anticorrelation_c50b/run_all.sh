#!/bin/sh
# mg-c50b.  s1 ~6 min, s3 ~26 min; the rest are seconds.
set -e
python3 s0_selftest.py       > out_s0_selftest.txt
python3 s1_census.py 7       > out_s1_census.txt      # writes out_s1_store.pkl
python3 s2_theory.py 7       > out_s2_theory.txt
python3 s3_n8.py 0.85        > out_s3_n8.txt          # writes out_s3_survivors.pkl
python3 s4_lstar.py          > out_s4_lstar.txt
python3 s5_n8_scope.py       > out_s5_n8_scope.txt
python3 s6_p9.py             > out_s6_p9.txt
