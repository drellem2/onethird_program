#!/bin/sh
# run_all.sh (mg-e015): independent re-computation for docs/AUDIT-mg-c929.md.
# Deterministic, single process, ~15 s.  Writes then moves, so a failure keeps the committed transcript.
set -e
cd "$(dirname "$0")"
python3 indep_e015.py 6 > out_indep_e015.txt.tmp && mv out_indep_e015.txt.tmp out_indep_e015.txt
grep -c FAIL out_indep_e015.txt | grep -qx 0 || { echo "a FAIL line is present"; exit 1; }
grep -q 'FIRES' out_indep_e015.txt
