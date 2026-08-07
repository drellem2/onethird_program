#!/bin/sh
# mg-abe8 -- reach of a constraint-pruned search for a frozen counterexample.
#
# Single process, one core, no fan-out (mayor's load note, 2026-08-07 20:53).
# Total wall-clock under 7 minutes on a 2024 Apple laptop.  Nothing here runs a
# search: the whole point is that the search is the thing being costed.
set -e
cd "$(dirname "$0")"

python3 selftestabe8.py    > out_selftestabe8.txt   2>&1 || { cat out_selftestabe8.txt; exit 1; }
python3 s1_census.py       > out_s1_census.txt      2>&1
python3 s2_percandidate.py > out_s2_percandidate.txt 2>&1
python3 s3_largen.py       > out_s3_largen.txt      2>&1
python3 s4_reach.py        > out_s4_reach.txt       2>&1

echo "ok -- see out_*.txt, OUTCOMES.md, and"
echo "     docs/OneThird-SearchReach-mg-abe8.md"
