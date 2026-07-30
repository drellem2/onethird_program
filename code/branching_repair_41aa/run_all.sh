#!/bin/sh
# mg-41aa -- the repair of mg-af28 under mg-6ad0's audit.
# Pure Python 3, no dependencies.  About 4 minutes, of which r1b_skew8.py is 3.
# r3_rescope.py needs network (it downloads arXiv:math/0612170); if the download
# fails it says so and exits 0, and nothing else depends on it.
set -e
cd "$(dirname "$0")"

python3 selftest41aa.py  > out_selftest.txt   || { echo "SELFTEST FAILED"; exit 1; }
python3 r1_exactly.py    > out_r1_exactly.txt
python3 r1b_skew8.py     > out_r1b_skew8.txt          # ~3 min
python3 r2_grid.py       > out_r2_grid.txt
python3 r3_rescope.py    > out_r3_rescope.txt         # needs network
python3 check_doc.py     > out_check_doc.txt  || { echo "CHECK_DOC FAILED"; exit 1; }

# The skew count at n = 8 is computed once, by r1b_skew8.py, and fed to
# r1_exactly.py's corrected table rather than hard-coded anywhere.
SKEW8_COUNT=$(sed -n 's/^SKEW8 \([0-9]*\)$/\1/p' out_r1b_skew8.txt)
export SKEW8_COUNT
python3 r1_exactly.py    > out_r1_exactly.txt

echo "done.  Headline lines:"
grep -h '^SUMMARY\|^CHECK_DOC:\|^SELF-TEST:' out_*.txt || true
