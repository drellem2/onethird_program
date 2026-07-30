#!/bin/sh
# Regenerate every number in
#   docs/OneThird-Counterexample-Under-The-Action-IndependentAudit-mg0a11.md
#
# Pure Python 3, no dependencies.  Imports nothing from
#   code/counterexample_probe_24a3/    (the target,  mg-24a3)
#   code/counterexample_audit_a7b4/    (the audit,   mg-a7b4)
#   code/counterexample_repair_dea5/   (the subject, mg-dea5)
# and shares no code with any of them.
#
# Cost, measured on the machine this was written on:
#   check_population.py    ~15 s   the population, the e-groups, the exact p
#   check_independence.py  ~15 s   THE PRIMARY FINDING: cores, not members
#   check_cycles.py        ~15 s   the negatives, and an attack on each
#   check_deflation.py     ~10 s   the beyond-brief material (repair section 5)
#   check_locator.py       ~ 2 s   mutation battery, 14 + 4 self-mutations
#   check_doc_audit.py             this audit's prose against its own outputs
#   check_powered.py       ~12 min on the first run, seconds afterwards
#                                  (it caches the whole-population qmass pass
#                                   in .records.pkl -- delete it to force a
#                                   cold rebuild)
set -e
cd "$(dirname "$0")"
python3 -u check_population.py   > out_population.txt
python3 -u check_independence.py > out_independence.txt
python3 -u check_cycles.py       > out_cycles.txt
python3 -u check_deflation.py    > out_deflation.txt
# out_locator.txt is read by check_doc_audit.py, and check_locator.py copies the
# tree while it runs -- so write it via a temp file rather than truncating it.
python3 -u check_locator.py      > out_locator.tmp && mv out_locator.tmp out_locator.txt
python3 -u check_powered.py      > out_powered.txt
python3 -u check_doc_audit.py    > out_check_doc.txt
echo "wrote out_population.txt out_independence.txt out_cycles.txt out_deflation.txt out_locator.txt out_powered.txt out_check_doc.txt"
