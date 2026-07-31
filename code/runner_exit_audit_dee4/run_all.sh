#!/bin/sh
# mg-dee4 -- the independent audit of mg-7522's repair of mg-05eb's three sites.
# Pure Python 3, no dependencies, no network.  About 6 minutes.
#
# NO PIPELINES.  This tree audits a repair of a pipeline defect and it ships a
# runner, so it is a member of its own population.  Every step below redirects
# and reads its own status through an explicit `||` guard, then `cat`s the
# transcript so the terminal stream is unchanged.  `selftestdee4.py` runs
# `a1_outside.py`'s own P2 predicate over this file and goes red if a pipeline
# of any kind ever appears in it.
#
# `set -o pipefail` is not used: the shebang is `/bin/sh`, which on Linux is
# dash, and dash rejects the option -- it would abort the runner at the line
# meant to make it safer.  There are no pipelines for it to protect anyway,
# which is the point.
#
# A1 through A5 each exit non-zero when they have findings.  That is the
# WHOLE OUTPUT of this audit, so a non-zero exit here is the expected state
# and not a breakage: the predicted codes are in PREDICTIONS.md.
set -u
cd "$(dirname "$0")"

run() {
    _p=$1
    _o=$2
    echo "### $_p"
    python3 -B "$_p" > "$_o" 2>&1 || {
        echo "    (exit $? -- see $_o; a non-zero exit is how a probe reports"
        echo "     findings, and the predicted codes are in PREDICTIONS.md)"; }
    cat "$_o"
    echo
}

run selftestdee4.py   out_selftest_dee4.txt
run a1_outside.py     out_a1_outside.txt
run a2_direct.py      out_a2_direct.txt
run a3_anchor.py      out_a3_anchor.txt
run a4_superlatives.py out_a4_superlatives.txt
run a5_floor.py       out_a5_floor.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL BAD line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^A[0-9] TOTAL BAD:\|^selftestdee4 TOTAL BAD:\|^FINDING:' out_*.txt || true
