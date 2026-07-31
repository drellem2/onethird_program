#!/bin/sh
# mg-7522 -- the three open sites of mg-05eb, repaired.
#
# Pure Python 3, no dependencies, no network.  About 20 minutes, almost all of
# it S2: the positive control runs the two repaired runners in full at every
# one of their eight sites, in both directions, and one of their targets takes
# ~47 s on its own.
#
# S2 EXECUTES TWO RUNNERS IN THE WORKING TREE and restores their committed
# transcripts by writing back exact bytes.  It refuses nothing and mutates no
# tracked file's source; S2d compares `git status --porcelain` before and after
# and goes red if anything moved.  RUN THIS ON A COMMITTED TREE anyway, because
# S4c reports the HEAD-anchored comparison and a dirty worktree makes that row
# a fact about your edits instead of about the repair.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects and has its own status read by
# an explicit `||` guard, then the transcript is `cat` so the terminal stream
# is unchanged.  That is the idiom this ticket exists to spread, and s5_self.py
# measures it on THIS FILE's bytes: if an edit puts a pipeline back, S5d goes
# red naming the line.  `set -o pipefail` is not used -- the shebang is
# `/bin/sh`, which on Linux is dash, and dash rejects the option.
set -e
cd "$(dirname "$0")"

python3 -B selftest7522.py > out_selftest_7522.txt || {
    cat out_selftest_7522.txt; echo "selftest7522.py FAILED"; exit 1; }
cat out_selftest_7522.txt

python3 -B s1_population.py > out_s1_population.txt || {
    cat out_s1_population.txt; echo "s1_population.py FAILED"; exit 1; }
cat out_s1_population.txt

python3 -B s2_status.py > out_s2_status.txt || {
    cat out_s2_status.txt; echo "s2_status.py FAILED"; exit 1; }
cat out_s2_status.txt

python3 -B s3_figure.py > out_s3_figure.txt || {
    cat out_s3_figure.txt; echo "s3_figure.py FAILED"; exit 1; }
cat out_s3_figure.txt

python3 -B s4_unpin.py > out_s4_unpin.txt || {
    cat out_s4_unpin.txt; echo "s4_unpin.py FAILED"; exit 1; }
cat out_s4_unpin.txt

python3 -B s5_self.py > out_s5_self.txt || {
    cat out_s5_self.txt; echo "s5_self.py FAILED"; exit 1; }
cat out_s5_self.txt
