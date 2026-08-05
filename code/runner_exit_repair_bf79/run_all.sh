#!/bin/sh
# mg-bf79 -- mg-56dc's four openings, repaired, plus the floor item nothing named.
#
# Pure Python 3, no dependencies, no network.  About one minute.  The slow part
# is P3d, which runs three probes of two other trees twice each -- once at HEAD
# and once under a controlled counterfactual.
#
# WHAT WRITES, AND WHAT IS RESTORED.  Two probes write:
#
#   P3d  writes the PRE-REPAIR `MARK` line into `runner_exit_repair_7522/
#        lib7522.py`, runs three probes under it, and restores the exact bytes
#        in a `finally`.  It asserts the byte-identity of that restore itself
#        and goes red if it fails.  This is mg-7522's own S2 idiom.
#   selftestbf79  writes a `mkdtemp` fixture under this directory and `git add
#        -N`s it so `git ls-files` can see it, then removes both in a `finally`
#        and checks `git status --porcelain` is unchanged across its own run.
#
# No other tracked file's bytes are modified by any probe here.  RUN THIS ON A
# COMMITTED TREE anyway: P1 and P4 report figures derived at HEAD, and a dirty
# worktree makes those rows facts about your edits rather than about the arc.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects and has its own status read by an
# explicit `||` guard, then the transcript is `cat` so the terminal stream is
# unchanged.  `set -o pipefail` is not used -- the shebang is `/bin/sh`, which
# on Linux is dash, and dash rejects the option; there are no pipelines for it
# to protect, which is the point rather than an excuse.
#
# EVERY PROBE EXITS WITH ITS OWN BAD COUNT.  A non-zero exit is how a probe here
# reports findings and is not a breakage.  All six are predicted to exit 0 in
# PREDICTIONS.md/P5c, committed before any of them existed; OUTCOMES.md scores
# that against what they actually do.
set -u
cd "$(dirname "$0")"

# WRITE TO A TEMP AND MOVE, rather than redirecting onto the transcript.  This
# is not tidiness -- it closes a hole `p5_self.py` found in itself.  A plain
# `> out_p5_self.txt` TRUNCATES the file before the probe starts, so `p5_self.py`
# -- whose whole job is to check every count THIS TREE prints -- could not see
# its own transcript, and its own output was the one artifact its strictest rule
# excluded.  That is O2's shape (a population that excludes the thing it is
# about) inside the repair of O2, and it hid NINE offending rows of mine until
# the probe was run once outside this runner.
#
# With the move, the previous run's bytes survive for the duration of the probe,
# so two consecutive runs converge and the committed transcripts are from such a
# pair.
#
# AND THE LIMIT OF THAT, because the first version of this comment overclaimed it
# and an overclaiming comment is this ticket's own subject.  The `mv` runs on the
# non-zero path as well as the zero one, so a probe that merely REPORTS FINDINGS
# leaves no `.new`.  A probe KILLED mid-write does -- the `mv` never runs -- and
# one did survive a `timeout` during this ticket's own development.  It is
# harmless rather than harmless-by-design: `lib70c7.outs()` globs `out_*.txt`,
# and `out_p1_grain.txt.new` does not end in `.txt`, so no corpus picks it up.
# The stale temp is overwritten by the next run. That is the whole guarantee, and
# it is smaller than "cannot leave a `.new` behind", which is what this said
# before it was measured.
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

run selftestbf79.py  out_selftest_bf79.txt
run p1_grain.py      out_p1_grain.txt
run p2_population.py out_p2_population.txt
run p3_ruleset.py    out_p3_ruleset.txt
run p4_figures.py    out_p4_figures.txt
run p5_self.py       out_p5_self.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^P[0-9] TOTAL\|^selftestbf79 TOTAL BAD:\|^FINDING:' out_*.txt || true
