#!/bin/sh
# mg-81ff — run every script and refresh every transcript.  ~20 min, pure Python 3.
# s0 FIRST and its exit status is honoured: nothing below it is worth reading if the
# controls fail.
set -e
cd "$(dirname "$0")"
python3 -u s0_selftest.py  > out_s0_selftest.txt
python3 -u s1_minc.py      > out_s1_minc.txt
python3 -u s2_regime.py    > out_s2_regime.txt
python3 -u s3_identity.py  > out_s3_identity.txt
grep -h "VERDICT" out_s0_selftest.txt out_s1_minc.txt out_s2_regime.txt out_s3_identity.txt
