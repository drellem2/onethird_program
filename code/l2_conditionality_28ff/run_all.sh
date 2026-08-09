#!/bin/sh
# mg-28ff — run every arm of the L2-conditionality instrument, in order.
# Total runtime is a few minutes; every verdict is exact rational arithmetic.
set -e
cd "$(dirname "$0")"
python3 -u selftest28ff.py  | tee out_selftest28ff.txt
python3 -u b1_footrule.py   | tee out_b1_footrule.txt
python3 -u b2_census.py     | tee out_b2_census.txt
python3 -u b3_routes.py     | tee out_b3_routes.txt
python3 -u b4_ruled_out.py  | tee out_b4_ruled_out.txt
python3 -u b5_trend.py      | tee out_b5_trend.txt
