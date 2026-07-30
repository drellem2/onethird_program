#!/bin/sh
# mg-446b: independent audit instrument for mg-8fd1 / 97cb533.
# No import from code/unified_gate_8fd1/ or code/hodge_leverage/ anywhere.
# Total ~4 min.
set -e
cd "$(dirname "$0")"
python3 audit_quotes.py     > out_quotes.txt      # target 1, textual fidelity
python3 audit_l1.py         > out_l1.txt          # target 1, N2 re-derived + quantifier test
python3 audit_l2.py 6       > out_l2.txt          # target 2, the population from scratch
python3 audit_crosscheck.py > out_crosscheck.txt  # target 2, pipeline numbers re-derived
python3 audit_proof.py      > out_proof.txt       # target 2/4, the theorem's PROOF attacked
python3 audit_beyond.py     > out_beyond.txt      # target 2, n = 7,8,9 and method quality
python3 audit_scope.py      > out_scope.txt       # targets 3 and 4
