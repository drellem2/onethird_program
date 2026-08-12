#!/bin/sh
# mg-0e8c -- run every arm, in order.  a1 FIRST and its exit status gates the rest: nothing
# this instrument reports means anything if the conventions are wrong, and the whole subject
# here is a claim stated in the wrong currency.
set -e
cd "$(dirname "$0")"
python3 a1_selftest.py  | tee out_a1_selftest.txt
python3 a2_vacuity.py   | tee out_a2_vacuity.txt
python3 a3_currency.py  | tee out_a3_currency.txt
python3 a4_remedy.py    | tee out_a4_remedy.txt
echo "all arms complete"
