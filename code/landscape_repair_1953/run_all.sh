#!/bin/sh
# mg-1953 -- REPAIR of mg-ebd8 / 714aceb's DERIVATIONS.
# Reproduces every number added to docs/OneThird-Landscape-Where-This-Lives.md
# by the repair (its section 8).  Pure Python 3, no dependencies, ~1 min.
set -e
cd "$(dirname "$0")"

python3 closed_form_outside_AC.py 6 > out_closed_form_outside_AC.txt   # ~5 s
python3 repaired_claims.py 6       > out_repaired_claims.txt           # ~19 s
python3 selftest.py 6              > out_selftest.txt                  # ~30 s

tail -1 out_selftest.txt
echo "done"
