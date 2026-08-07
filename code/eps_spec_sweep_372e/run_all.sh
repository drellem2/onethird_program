#!/bin/sh
# mg-372e — the whole sweep, ~1 s, no dependencies beyond python3.
set -e
here=$(cd "$(dirname "$0")" && pwd)
python3 "$here/s1_census.py"    | tee "$here/out_s1_census.txt"
python3 "$here/s2_classify.py"  | tee "$here/out_s2_classify.txt"
cd "$here" && python3 s3_control.py | tee out_s3_control.txt
