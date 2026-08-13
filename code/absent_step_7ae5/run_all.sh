#!/bin/sh
# mg-7ae5 — the whole instrument.  Exact rationals; no float on a decision path.
# Measured runtime on this host: see README §1 (measured by `time sh run_all.sh`,
# not by adding the parts).
set -e
cd "$(dirname "$0")"

python3 a0_selftest.py          > out_a0_selftest.txt
python3 a1_statement.py         > out_a1_statement.txt
python3 a2_price_hypothesis.py 6 > out_a2_price_hypothesis.txt
python3 a3_density.py 6         > out_a3_density.txt
python3 a4_novelty.py           > out_a4_novelty.txt

echo "a0 verdict: $(tail -2 out_a0_selftest.txt | head -1)"
