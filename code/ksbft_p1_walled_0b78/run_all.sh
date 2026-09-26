#!/bin/sh
# mg-0b78 (KSBFT-P1): regenerate every transcript quoted in
# docs/KSBFT-P1-walled-routes-under-bounded-range.md. One process, ~15 s, exact, seeded.
set -e
cd "$(dirname "$0")"
python3 ranges.py > out_ranges.txt
python3 ranges2.py > out_ranges2.txt
python3 stanley_gap.py 150 > out_stanley_gap.txt
grep -q "controls: .* OK" out_ranges.txt
grep -q "control: C_m ⊔ C_m .* OK" out_stanley_gap.txt
grep -q "negative control: .* CAUGHT" out_stanley_gap.txt
grep -q "of which NOT flat: 0 " out_stanley_gap.txt
echo "run_all: all transcripts regenerated, controls fire"
