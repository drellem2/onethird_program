#!/bin/sh
# Regenerate every number in
#   docs/OneThird-Counterexample-Under-The-Action-Repair.md            (mg-dea5)
# and the figures the repair writes into
#   docs/OneThird-Counterexample-Under-The-Action.md
#
# Pure Python 3, no dependencies.  Imports nothing from
# code/counterexample_probe_24a3/ (the target) or code/counterexample_audit_a7b4/
# (the audit) and shares no code with either.
#
# Cost, measured on the machine this was written on:
#   controls.py    ~30 s   12 positive controls + 4 negative controls that FIRE
#   theorem4.py    ~10 s   Theorem 4 for every weight, against the actual matrix
#   section4.py    ~3 min  the section 4 re-measurement, n = 5..8 exhaustively
#   cycles.py      ~90 s   majority cycles: exhaustive to n = 8, witnesses above
#   check_doc_repair.py     the prose against the outputs, and the STRUCK guard
#
# The only randomness is seeded: SEED = 20260730 for the permutation tests,
# SEED = 4242 for the cycle search (the target's own seed).  Every output file
# below reproduces byte-identically.
set -e
cd "$(dirname "$0")"
python3 -u controls.py  > out_controls.txt
python3 -u theorem4.py  > out_theorem4.txt
python3 -u section4.py  > out_section4.txt
python3 -u cycles.py    > out_cycles.txt
python3 -u cores.py     > out_cores.txt
python3 -u check_doc_repair.py > out_check_doc.txt
echo "wrote out_controls.txt out_theorem4.txt out_section4.txt out_cycles.txt out_cores.txt out_check_doc.txt"
