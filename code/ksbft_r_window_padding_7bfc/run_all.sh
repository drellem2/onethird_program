#!/bin/sh
# mg-7bfc (KSBFT-R): regenerate every transcript quoted in docs/KSBFT-R-window-padding.md.
# One process, ~1 s, exact integers/Fractions, no randomness.
set -e
cd "$(dirname "$0")"
python3 pad.py > out_pad.txt
grep -q "SUMMARY: 0 failed checks" out_pad.txt
grep -q "NEGATIVE CONTROL: .* CAUGHT" out_pad.txt
grep -q "CONTROL: attach_low(F_12,3) is NOT prime .* CAUGHT" out_pad.txt
grep -q "CONTROL: module test finds it" out_pad.txt
echo "run_all: transcript regenerated, all checks pass, controls fire"
