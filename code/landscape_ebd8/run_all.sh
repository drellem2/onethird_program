#!/bin/sh
# Reproduces every number in docs/OneThird-Landscape-Where-This-Lives.md.
# Pure Python 3, no dependencies. Total ~12 minutes on a 2021 laptop.
set -e
cd "$(dirname "$0")"
python3 identify_lattice.py 6 > out_identify_lattice.txt   # ~6 min
python3 brown_theorem2.py  6 > out_brown_theorem2.txt      # ~5 min
python3 chains_in_JP.py    5 > out_chains_in_JP.txt        # ~40 s
echo "done"
