#!/bin/sh
# mg-5040 -- the repair of mg-4700's three OPEN items.
# Pure Python 3, no dependencies, NO NETWORK except `git archive` and `git
# log` against this repository, which are local.  About 25 minutes: r2
# executes three `run_all.sh` about twenty times between them, on purpose,
# because a call present in a script is not evidence of execution.
set -e
cd "$(dirname "$0")"

# EVERY STEP BELOW IS ONE STATEMENT WITH ONE RETURN (mg-5040's own OPEN 2,
# applied to itself -- see r4_self.py R4b, which SPLITS THIS FILE and fails if
# it finds a multi-part block).  Nothing is piped: a pipeline's status in
# POSIX sh is its LAST command's, so `python3 x.py | tee out.txt` exits 0
# however red x.py was (mg-c2b3).  Each step redirects to its transcript and
# `set -e` reads the status; the transcript is printed afterwards by a
# separate `cat`, which is a heading and carries no verdict.
python3 -B selftest5040.py > out_selftest.txt
cat out_selftest.txt

python3 -B r1_bound.py > out_r1_bound.txt
cat out_r1_bound.txt

python3 -B r2_wiring.py > out_r2_wiring.txt
cat out_r2_wiring.txt

python3 -B r3_summaries.py > out_r3_summaries.txt
cat out_r3_summaries.txt

python3 -B r4_self.py > out_r4_self.txt
cat out_r4_self.txt

echo
echo "Headline lines:"
grep -h '^R[1-4] TOTAL BAD' out_r*.txt
echo
echo "Each of those totals is followed IN ITS OWN OUTPUT by a statement of"
echo "what it ranged over.  A total with no population is what mg-73df's"
echo "MAJOR was, and what every ticket in this arc since has been about."
