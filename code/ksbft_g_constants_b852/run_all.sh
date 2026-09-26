#!/bin/sh
# mg-b852 -- the whole instrument (~2 s).  Seeded randomness only in the Lemma 4.4 control.
set -e
cd "$(dirname "$0")"
python3 constants.py > out_constants.txt.tmp && mv out_constants.txt.tmp out_constants.txt
grep -E 'PASS|FAIL|FIRES' out_constants.txt
