#!/bin/sh
# mg-d633 -- the two printed extents that were WIDER than what the code reads,
# repaired and then MEASURED IN BOTH DIRECTIONS, plus the cross-section check
# a struck claim needs and no per-section checker can do.
# Pure Python 3, no dependencies, NO NETWORK.  About 2 minutes, almost all of
# it E3's 27 sandbox copies.
set -e
cd "$(dirname "$0")"

python3 selftestd633.py    | tee out_selftest.txt
python3 e1_extents.py      > out_e1_extents.txt   || { echo "E1 FAILED"; exit 1; }
python3 e2_crosssection.py > out_e2_crosssection.txt || { echo "E2 FAILED"; exit 1; }
python3 e3_bothways.py     > out_e3_bothways.txt  || { echo "E3 FAILED"; exit 1; }

echo
echo "Headline lines:"
grep -h '^E[123] TOTAL BAD:\|^selftestd633' out_*.txt || true
echo
echo "Every one of those totals is followed IN THE OUTPUT by its own extent."
echo "That was mg-a4ef's remedy.  mg-7dd3 measured it and found two of the"
echo "four extent lines WIDER than what the code read, which is worse than"
echo "printing none.  E1 measures every extent line against an instrumented"
echo "open(); E3 probes every one of them from inside AND outside.  A"
echo "structural remedy is not done when it ships -- it is done when its"
echo "single point has been measured in both directions."
