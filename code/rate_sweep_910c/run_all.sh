#!/bin/sh
# mg-910c -- the RATE sweep.  ~2 s.  Nothing on disk is mutated by any of these.
set -e
D=$(dirname "$0")
python3 "$D/r1_census.py"
echo
python3 "$D/r2_classify.py"
echo
python3 "$D/r3_control.py"
