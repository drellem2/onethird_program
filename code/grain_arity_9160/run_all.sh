#!/bin/sh
# mg-9160 -- THE CLASSIFIER'S ARITY, and the population rule one layer down.
# Pure Python 3, no dependencies, no network.  ABOUT ONE MINUTE.
#
# WHAT WRITES.  NOTHING OUTSIDE THIS DIRECTORY.  No probe here runs another
# tree's runner, edits another tree's bytes, or regenerates another tree's
# transcripts.  `lib56dc`, `lib03d1`, `libbf79` and `lib70c7` are IMPORTED and
# read; none is written.  A `git status --porcelain` outside
# `code/grain_arity_9160/` is unchanged across a full run, and that is a
# property of the probes and not of a restore step -- there is no restore step
# because there is nothing to restore.
#
# RUN THIS ON A COMMITTED TREE.  S1b reports the corpus at HEAD beside the
# reconstruction, and a dirty worktree makes the HEAD column a fact about your
# edits rather than about the arc.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects, its status is read by an
# explicit `||` guard, and then the transcript is `cat` so the terminal stream
# is unchanged.  `set -o pipefail` is not used: the shebang is `/bin/sh`, which
# is dash on Linux, and dash rejects the option.  There are no pipelines for it
# to protect.
#
# EVERY PROBE EXITS WITH ITS OWN CHECK-FAILURE COUNT, AND A MISSED PREDICTION
# IS NOT ONE.  P7 MISSES and P6 SPLITS and `s5_self.py` still exits 0: a bet
# that cannot lose is not a bet, and an exit code that punishes a recorded miss
# is an exit code that rewards tuning the bet.  All six expected exit codes are
# 0 and are stated here, before the run, so a non-zero one is visible as a
# change rather than absorbed as noise.
set -u
cd "$(dirname "$0")"

# WRITE TO A TEMP AND MOVE.  Adopted from `grain_axis_audit_03d1/run_all.sh`,
# which adopted it from `runner_exit_repair_bf79`.  A plain `> out_s5_self.txt`
# TRUNCATES the file before the probe starts, and every probe in this tree
# ranges over `code/*/out_*.txt` -- so the one artifact my own census could not
# see would be my own transcript.  That is the arc's defect #7 and this tree
# would commit it on its first run.
rm -f ./out_*.txt.new
run() {
    _p=$1
    _o=$2
    echo "### $_p"
    python3 -B "$_p" > "$_o.new" 2>&1 || {
        echo "    (exit $? -- expected 0; every check in this tree is an arm"
        echo "     that can fail, and a scored MISS is not one of them)"; }
    mv -f "$_o.new" "$_o"
    cat "$_o"
    echo
}

run selftest9160.py   out_selftest_9160.txt
run s1_reproduce.py   out_s1_reproduce.txt
run s2_arity.py       out_s2_arity.txt
run s3_population.py  out_s3_population.txt
run s4_open.py        out_s4_open.txt
run s5_self.py        out_s5_self.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^S[0-9] TOTAL\|^SELFTEST TOTAL BAD:\|^FINDING:' out_*.txt || true
