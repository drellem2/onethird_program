#!/bin/sh
# mg-a4ef -- the repair of mg-73df's MAJOR (X3 still in force AT SOURCE) and
# of the seam between mg-6f61 and mg-f8fa.
# Pure Python 3, no dependencies, NO NETWORK except `git archive` against this
# repository, which is local.  About 5 seconds.
set -e
cd "$(dirname "$0")"

python3 selftesta4ef.py | tee out_selftest.txt
python3 s1_extent.py    > out_s1_extent.txt || { echo "S1 FAILED"; exit 1; }
python3 s2_seam.py      > out_s2_seam.txt   || { echo "S2 FAILED"; exit 1; }

echo
echo "Headline lines:"
grep -h '^S[12] TOTAL BAD:\|^selftesta4ef' out_*.txt || true
echo
echo "S1's TOTAL BAD is followed IN THE OUTPUT by a statement of its extent."
echo "That is the whole point of this instrument: mg-73df's MAJOR is what a"
echo "TOTAL BAD: 0 means when nobody says what it ranged over."
