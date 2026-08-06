#!/bin/sh
# mg-03d1 -- the INDEPENDENT AUDIT of the mg-56dc label-vs-grain repair as
# mg-bf79 landed it.  Pure Python 3, no dependencies, no network.
#
# ABOUT FIVE MINUTES.  The slow part is A4d, which runs another tree's whole
# suite TWICE to check that its `mv` fix converges.
#
# WHAT WRITES, AND WHAT IS RESTORED.  One probe writes:
#
#   A4d  runs `code/runner_exit_repair_bf79/run_all.sh` twice, which
#        regenerates that tree's six committed transcripts, and then restores
#        the exact committed bytes with `git checkout --` in a `finally`.  It
#        asserts `git status --porcelain` is unchanged across its own run and
#        goes RED if the restore fails.  That is mg-7522's S2 idiom.  The
#        brief forbids LEAVING another ticket's evidence regenerated; it does
#        not forbid running it, and `does it converge` is a question you can
#        only answer by running it twice.
#
# No other tracked file's bytes are modified by any probe here.  RUN THIS ON A
# COMMITTED TREE: A1, A3 and A5 report figures derived at HEAD, and a dirty
# worktree makes those rows facts about your edits rather than about the arc.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects and has its own status read by
# an explicit `||` guard, then the transcript is `cat` so the terminal stream
# is unchanged.  `set -o pipefail` is not used: the shebang is `/bin/sh`, which
# is dash on Linux, and dash rejects the option.  There are no pipelines for it
# to protect, which is the point rather than the excuse.
#
# EVERY PROBE EXITS WITH ITS OWN FINDING COUNT.  A non-zero exit is how a probe
# here reports findings and is not a breakage.  A4 is PREDICTED non-zero -- it
# counts trees carrying the arc's truncate-before-probe shape, which is a
# finding about the arc and not a fault of this tree.  All seven exit codes are
# pre-registered in PREDICTIONS.md/ASc, committed before any of them existed.
set -u
cd "$(dirname "$0")"

# WRITE TO A TEMP AND MOVE.  Adopted from `runner_exit_repair_bf79/run_all.sh`
# rather than re-discovered: a plain `> out_a6_self.txt` TRUNCATES the file
# before the probe starts, so `a6_self.py` -- whose AS7 checks every count row
# THIS TREE prints -- would have its own transcript as the one artifact its
# strictest rule could not see.  That is the parent's defect #7, and A4 of this
# audit measures how much of the arc still carries it (43 trees where the shape
# bites, at the run committed here).  Adopting the fix and then counting the
# trees that have not is the only honest order to do those two things in.
#
# THE LIMIT, because the parent's first version of this comment overclaimed it:
# the `mv` runs on the non-zero path too, so a probe that merely REPORTS
# FINDINGS leaves no `.new`.  A probe KILLED mid-write does.  It is harmless
# rather than harmless-by-design -- `out_a6_self.txt.new` does not end in
# `.txt`, so no `out_*.txt` corpus picks it up -- and the next run overwrites
# it.  That is the whole guarantee.
rm -f ./out_*.txt.new
run() {
    _p=$1
    _o=$2
    echo "### $_p"
    python3 -B "$_p" > "$_o.new" 2>&1 || {
        echo "    (exit $? -- see $_o; a non-zero exit is how a probe reports"
        echo "     findings, and the predicted codes are in PREDICTIONS.md)"; }
    mv -f "$_o.new" "$_o"
    cat "$_o"
    echo
}

run selftest03d1.py out_selftest_03d1.txt
run a1_axes.py      out_a1_axes.txt
run a2_blindspot.py out_a2_blindspot.txt
run a3_ledger.py    out_a3_ledger.txt
run a4_sweep.py     out_a4_sweep.txt
run a5_pin.py       out_a5_pin.txt
run a6_self.py      out_a6_self.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^A[0-9] TOTAL\|^selftest03d1 TOTAL BAD:\|^FINDING:' out_*.txt || true
