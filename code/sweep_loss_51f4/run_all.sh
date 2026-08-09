#!/bin/sh
# Reproduces every out_*.txt for mg-51f4.  s3 is the long one (~30 min).
set -e
python3 -u s0_selftest.py    > out_s0_selftest.txt  2>&1 || echo "SELFTEST FAILED"
python3 -u s1_census.py 6    > out_s1_census.txt    2>&1
python3 -u s2_families.py 14 14 > out_s2_families.txt 2>&1
python3 -u s4_combined.py 22 15 > out_s4_combined.txt 2>&1
python3 -u s3_n7.py 7        > out_s3_n7.txt        2>&1
