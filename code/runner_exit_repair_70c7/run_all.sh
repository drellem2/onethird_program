#!/bin/sh
# mg-70c7 -- the six findings of mg-dee4 against 1ee1f1b, repaired.
#
# Pure Python 3, no dependencies, no network.  About 4 minutes, almost all of
# it R5c: the forced-failure control runs `code/branching_audit_a218/c0_repro.sh`
# in full, twice, and that script regenerates another tree's five outputs.
#
# R5c WRITES A SCRATCH `_mg70c7_arm.sh` INTO code/branching_audit_a218/ and
# deletes it in a `finally`.  No tracked file's bytes are modified by any probe
# here.  RUN THIS ON A COMMITTED TREE anyway, because R2a reports the
# worktree-against-the-pin figure and a dirty worktree makes that row a fact
# about your edits instead of about the arc.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects and has its own status read by
# an explicit `||` guard, then the transcript is `cat` so the terminal stream is
# unchanged.  `r6_self.py` measures that on THIS FILE's bytes under the WIDENED
# P2 predicate, so if an edit puts a pipeline back it goes red naming the line.
# `set -o pipefail` is not used -- the shebang is `/bin/sh`, which on Linux is
# dash, and dash rejects the option.
set -e
cd "$(dirname "$0")"

python3 -B selftest70c7.py > out_selftest_70c7.txt || {
    cat out_selftest_70c7.txt; echo "selftest70c7.py FAILED"; exit 1; }
cat out_selftest_70c7.txt

python3 -B r1_grain.py > out_r1_grain.txt || {
    cat out_r1_grain.txt; echo "r1_grain.py FAILED"; exit 1; }
cat out_r1_grain.txt

python3 -B r2_anchor.py > out_r2_anchor.txt || {
    cat out_r2_anchor.txt; echo "r2_anchor.py FAILED"; exit 1; }
cat out_r2_anchor.txt

python3 -B r3_strength.py > out_r3_strength.txt || {
    cat out_r3_strength.txt; echo "r3_strength.py FAILED"; exit 1; }
cat out_r3_strength.txt

python3 -B r4_property.py > out_r4_property.txt || {
    cat out_r4_property.txt; echo "r4_property.py FAILED"; exit 1; }
cat out_r4_property.txt

python3 -B r5_population.py > out_r5_population.txt || {
    cat out_r5_population.txt; echo "r5_population.py FAILED"; exit 1; }
cat out_r5_population.txt

python3 -B r6_self.py > out_r6_self.txt || {
    cat out_r6_self.txt; echo "r6_self.py FAILED"; exit 1; }
cat out_r6_self.txt
