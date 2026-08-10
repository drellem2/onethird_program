#!/bin/sh
# mg-789d -- run order.  s0 is forced: if it exits nonzero nothing below it is trustworthy.
set -e
cd "$(dirname "$0")"
python3 s0_selftest.py   | tee out_s0_selftest.txt
python3 s1_hunt.py       | tee out_s1_hunt.txt
python3 s2_reduce.py     | tee out_s2_reduce.txt
python3 s3_depth.py      | tee out_s3_depth.txt
python3 s4_theoremA.py   | tee out_s4_theoremA.txt
python3 s5_certify.py    | tee out_s5_certify.txt
python3 s6_aftermath.py  | tee out_s6_aftermath.txt
