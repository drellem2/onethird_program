#!/bin/sh
# mg-5371 -- the whole instrument (~15 s, single core).  Seeded randomness only in the two probes.
set -e
cd "$(dirname "$0")"
python3 family.py          > out_family.txt
python3 consequences.py    > out_consequences.txt
python3 semiorder_probe.py 12,2 14,3 16,4 18,5 20,6 > out_semiorder.txt
python3 lc_chain_probe.py 400 > out_lc_chain.txt
python3 lc_dilworth_probe.py  > out_lc_dilworth.txt
grep -hE 'PASS|FAIL|FIRES|MATCH' out_*.txt
