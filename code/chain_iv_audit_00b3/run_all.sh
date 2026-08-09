#!/bin/sh
# mg-00b3 — the whole instrument, in order.  a0 first: nothing below it is worth
# reading until every control passes.  Total ~4 min on a cold cache (the n = 7 sweep
# dominates and is cached outside the repository afterwards).
set -e
cd "$(dirname "$0")"
python3 a0_controls.py   > out_a0_controls.txt   ; echo "a0 ok"
python3 a1_population.py > out_a1_population.txt ; echo "a1 ok"
python3 a2_reversal.py   > out_a2_reversal.txt   ; echo "a2 ok"
python3 a3_regime.py     > out_a3_regime.txt     ; echo "a3 ok"
python3 a4_identity.py   > out_a4_identity.txt   ; echo "a4 ok"
