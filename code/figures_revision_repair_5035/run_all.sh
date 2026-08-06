#!/bin/sh
# mg-5035 -- the repair of `figures()`'s false git-revision exclusion.
# Pure Python 3, no dependencies, no network.
#
# ABOUT TEN MINUTES on an idle host, and MUCH longer on a loaded one: F1c, F2
# and F3 call `git rev-parse` once per distinct token as an EVALUATION ORACLE,
# and F2 reads every tracked file twice (once per rule).  The results are
# memoised inside one process; they are not memoised across probes.
#
# WHAT WRITES.  Nothing outside this directory.  No probe here regenerates
# another tree's committed transcripts -- PREDICTIONS says so in advance, and
# the reason is that those transcripts are the evidence F2 and F3 measure.
# Four trees' transcripts WOULD read differently under the repaired rule and
# `f3_published.py` lists them by name instead of rewriting them.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects and has its own status read by
# an explicit `||` guard, then the transcript is `cat` so the terminal stream
# is unchanged.  `set -o pipefail` is not used: the shebang is `/bin/sh`, which
# is dash on Linux, and dash rejects the option.  There are no pipelines for it
# to protect, which is the point rather than the excuse.
#
# EVERY PROBE EXITS WITH ITS OWN BAD COUNT.  All five predicted codes are
# pre-registered in PREDICTIONS.md/P5a, committed before any of them existed.
set -u
cd "$(dirname "$0")"

# WRITE TO A TEMP AND MOVE.  Inherited from mg-bf79 and mg-03d1 rather than
# re-discovered: a plain `> out_f4_self.txt` TRUNCATES the file before the
# probe starts, and `f4_self.py` reads this tree's own transcripts to check
# that every count row names its grain -- so it would be blind to exactly the
# file it is writing.  F4e(2) states the residue this idiom leaves.
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

run selftest5035.py    out_selftest_5035.txt
run f1_rule.py         out_f1_rule.txt
run f2_contamination.py out_f2_contamination.txt
run f3_published.py    out_f3_published.txt
run f4_self.py         out_f4_self.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
# DEFECT OF THIS RUNNER, RECORDED RATHER THAN QUIETLY FIXED: the first version
# grepped `out_*.txt`, and when this script's own output is redirected to
# `out_run_all.txt` in the same directory that glob MATCHES ITS OWN TRANSCRIPT
# -- which already contains every line it is grepping for, because each probe
# is `cat`ed.  The summary printed everything TWICE.  A count that includes its
# own output is the shape mg-03d1's A3e caught in mg-ec63; caught here by
# reading the summary rather than by a check, which is why it is written down.
for _f in out_*.txt; do
    [ "$_f" = "out_run_all.txt" ] && continue
    grep -h '^F[0-9] TOTAL\|^selftest5035 TOTAL BAD:\|^FINDING:' "$_f"
done || true
