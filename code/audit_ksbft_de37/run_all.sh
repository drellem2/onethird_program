#!/bin/sh
# run_all.sh (mg-de37): independent re-computation for docs/AUDIT-mg-b447.md.
# Deterministic, single process, ~15 s.  Writes then moves, so a failure keeps the committed transcript.
set -e
cd "$(dirname "$0")"
python3 indep_de37.py 6 > out_indep_de37.txt.tmp && mv out_indep_de37.txt.tmp out_indep_de37.txt
python3 tau_search_de37.py 7 > out_tau_search_de37.txt.tmp && mv out_tau_search_de37.txt.tmp out_tau_search_de37.txt
grep -q "violations (each must be 0): {'K': 0, 'flip': 0, 'thm31': 0, 'uid': 0, 'bw': 0, 'onept': 0}" out_indep_de37.txt
test "$(grep -c SILENT out_indep_de37.txt)" = 0
grep -q 'FIRES' out_indep_de37.txt
grep -q 'cuts with tau>D: 0 ' out_tau_search_de37.txt
