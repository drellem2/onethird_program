#!/bin/sh
# Regenerate the verification output for
# docs/OneThird-Counterexample-Under-The-Action-IndependentAudit.md (mg-a7b4).
# Pure Python 3, no dependencies.  Shares no code with code/counterexample_probe_24a3/.
#
# Cost, measured on the machine this was written on:
#   selfcheck.py       ~2 min   (controls, incl. exact-rank spectrum checks at n<=5)
#   records.py         ~4 min   (per-poset records for n = 3..7, cached as .pkl)
#   the check_*.py     ~5 min
#   witness9.py        ~3 min   (the n = 9 witness + a 30,000-poset search at n = 8)
#
# Only the random searches in witness9.py/shrink_witness.py use randomness; both are
# seeded, so every number in the audit is reproducible.
set -e
cd "$(dirname "$0")"
rm -f records_n*.pkl
python3 -u selfcheck.py 7 > selfcheck_output.txt
python3 -u -c "import records; [records.build_all(n) for n in range(3, 8)]" > /dev/null
python3 -u check_bridge.py > out_bridge.txt
python3 -u check_main.py > out_main.txt
python3 -u check_sections.py > out_sections.txt
python3 -u check_egroups.py > out_egroups.txt
python3 -u check_prop5.py > out_prop5.txt
python3 -u check_spectral.py > out_spectral.txt
python3 -u check_leftovers.py > out_leftovers.txt
python3 -u shrink_witness.py 4000 > out_shrink.txt
python3 -u witness9.py 5000 > out_witness9.txt
echo "wrote selfcheck_output.txt and out_*.txt"
