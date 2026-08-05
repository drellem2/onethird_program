#!/bin/sh
# mg-d53d -- the INDEPENDENT AUDIT of the mg-4adb rung repair.
# Pure Python 3, no dependencies, NO NETWORK except `git clone --shared`
# against this repository, which is local.  ABOUT 40 MINUTES, almost all of it
# G1's 255 runner executions and 551 e2 executions.  Set D53D_WORKERS to
# change how many sandboxes run at once (default 6).
set -e
cd "$(dirname "$0")"

# THE RUNG, AND THIS FILE IS HELD TO IT.  mg-4adb's repair is that a runner's
# gate must be its LAST COMMAND, because a POSIX script's exit status is its
# last command's -- so the statement that carries a checker's verdict out of
# the file is the CALL ITSELF, which is inside every population that
# enumerates the file.  An audit of that repair that did not obey it would be
# asking of somebody else's runner a question it had not asked of its own.
#
# So: every step but the last has an explicit `|| { ...; exit 1; }` guard,
# nothing is piped (a pipeline's status in POSIX sh is its LAST command's and
# `set -o pipefail` is not available in dash -- mg-c2b3), and G1 -- the
# section carrying this audit's primary claim -- IS THE LAST COMMAND.
# NOTHING MAY BE APPENDED BELOW IT.
#
# Each step both writes its transcript and prints it, because a call present
# in a script is not evidence of execution (mg-5040, on mg-4700's OPEN 2).

python3 selftest_d53d.py > out_selftest_d53d.txt || {
    cat out_selftest_d53d.txt; echo "selftest_d53d.py FAILED"; exit 1; }
cat out_selftest_d53d.txt

# G4 and G5 first: both are cheap, and G5 carries the floor item.  A section
# that reports a FINDING exits non-zero, so `|| :` would swallow exactly what
# this audit is for -- the guards below distinguish a finding (exit 1) from a
# crash (anything else) and let the run continue for a finding, because a
# reader is owed every section and not the first one that fired.
python3 g4_self.py > out_g4_self.txt || {
    test $? -eq 1 || { cat out_g4_self.txt; echo "g4_self.py CRASHED";
                       exit 1; }; }
cat out_g4_self.txt

python3 g5_fourth.py > out_g5_fourth.txt || {
    test $? -eq 1 || { cat out_g5_fourth.txt; echo "g5_fourth.py CRASHED";
                       exit 1; }; }
cat out_g5_fourth.txt

python3 g3_layer2.py > out_g3_layer2.txt || {
    test $? -eq 1 || { cat out_g3_layer2.txt; echo "g3_layer2.py CRASHED";
                       exit 1; }; }
cat out_g3_layer2.txt

python3 g2_red.py > out_g2_red.txt || {
    test $? -eq 1 || { cat out_g2_red.txt; echo "g2_red.py CRASHED";
                       exit 1; }; }
cat out_g2_red.txt

echo
echo "Headline lines, for the sections that have run.  G1's own two lines"
echo "are printed by G1 itself, below, because it is the last command and"
echo "nothing may be appended after it:"
grep -h '^G[2-5] TOTAL BAD:\|^G[2-5] PREDICTIONS SCORED:\|^selftest_d53d' \
    out_*.txt || true
echo
echo "A non-zero TOTAL BAD in this suite is a FINDING REPORTED, not a broken"
echo "instrument, and PREDICTIONS MISSED is neither -- a prediction that"
echo "missed is a result and is kept as written.  OUTCOMES.md scores all 25."
echo

# G1 IS THE LAST COMMAND.  Its exit status is this file's, and what carries
# it out is the call itself.
echo "G1 -- the deletion population, its own output, unfiltered:"
python3 g1_population.py
