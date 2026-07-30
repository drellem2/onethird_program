#!/bin/sh
# mg-f8fa -- the remainder of mg-a61f not carried by mg-6f61.
# Pure Python 3, no dependencies, NO NETWORK, ~15 s.
set -e
cd "$(dirname "$0")"

python3 selftestf8fa.py    | tee out_selftest.txt
python3 w1_opposite.py     | tee out_w1_opposite.txt
python3 w2_typemismatch.py | tee out_w2_typemismatch.txt
python3 w3_scope.py        | tee out_w3_scope.txt

echo
echo "out_w3_scope_before.txt is the SAME detector run against the tree"
echo "before this repair: 12 problems.  It is committed on purpose -- a"
echo "checker written after the fix and never seen to fail is not a checker."
