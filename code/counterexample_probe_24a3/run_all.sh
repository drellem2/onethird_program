#!/bin/sh
# Regenerate the verification output for docs/OneThird-Counterexample-Under-The-Action.md
# (mg-24a3).  Pure Python 3, no dependencies.  Deterministic: the committed
# probe_output.txt and selftest_output.txt reproduce byte-identically.
#
# Cost, measured on the machine this was written on:
#   selftest.py  ~4 min   (controls, including exact-rank spectrum checks at n<=4)
#   probe.py     ~7 min   (all 2447 posets on 3..7 elements, plus named families
#                          to n=12 and one n=11 witness)
set -e
cd "$(dirname "$0")"
python3 -u selftest.py > selftest_output.txt
echo "wrote selftest_output.txt"
python3 -u probe.py > probe_output.txt
echo "wrote probe_output.txt"
