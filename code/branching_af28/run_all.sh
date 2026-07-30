#!/bin/sh
# mg-af28 -- does this construction meet the towers-of-algebras / branching-graph
# programme?  Pure Python 3, no dependencies.  About 6 minutes.
#
# scan_brown.py needs network (it downloads arXiv:math/0006145); if the download
# fails it says so and exits 0, and nothing else depends on it.
set -e
cd "$(dirname "$0")"
python3 selftest.py       > out_selftest.txt
python3 t_young.py        > out_young.txt
python3 t_branching.py    > out_branching.txt
python3 t_lrb_reps.py     > out_lrb_reps.txt
python3 scan_brown.py     > out_scan_brown.txt
echo "done: out_selftest.txt out_young.txt out_branching.txt out_lrb_reps.txt out_scan_brown.txt"
