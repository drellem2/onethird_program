#!/bin/sh
# mg-0d1b — THE ALIASED-SCALAR SWEEP.  ~90 s.
#
# ORDER IS LOAD-BEARING: x3 writes alias_groups.json and x2 reads it, so that the INDEX's
# rows are established BY MEASUREMENT and not by the author's vocabulary.  Running x2
# alone against a stale alias_groups.json would index yesterday's clustering, so x2 is
# never run on its own here.
#
# Exit 0 = x0's planted worlds all CAUGHT and x3's arms all pass.  x1 and x2 are censuses
# and always exit 0; their output is the deliverable, not their status.
set -e
cd "$(dirname "$0")"
python3 -u x0_selftest.py    > out_x0_selftest.txt    2>&1 || { cat out_x0_selftest.txt; exit 1; }
python3 -u x1_population.py  > out_x1_population.txt  2>&1
python3 -u x3_values.py      > out_x3_values.txt      2>&1 || { cat out_x3_values.txt; exit 1; }
python3 -u x2_index.py       > out_x2_index.txt       2>&1
echo "x0 $(grep '^x0 RESULT' out_x0_selftest.txt)"
echo "x1 $(tail -1 out_x1_population.txt)"
echo "x3 $(tail -1 out_x3_values.txt)"
echo "x2 $(tail -1 out_x2_index.txt)"
