#!/bin/sh
# mg-56dc -- the independent audit of mg-70c7's grain-and-population repair.
# Pure Python 3, no dependencies, no network.  About four minutes, almost all
# of it T4c/T4d: three whole-repository population censuses at three revisions.
#
# NO PIPELINES.  This tree audits a repair of a pipeline defect and it ships a
# runner, so it is a member of its own population.  Every step below redirects
# and has its own status read by an explicit `||` guard, then the transcript is
# `cat` so the terminal stream is unchanged.  `selftest56dc.py` measures that
# on THIS FILE's bytes and goes red if a pipeline of any kind appears in it.
#
# `set -o pipefail` is not used: the shebang is `/bin/sh`, which on Linux is
# dash, and dash rejects the option -- it would abort the runner at the line
# meant to make it safer.  There are no pipelines for it to protect, which is
# the point rather than an excuse.
#
# T3 WRITES FIXTURES into a `mkdtemp` under this directory and removes them in
# a `finally`; T1c re-runs mg-70c7's `r4_property.py`, which writes nothing.
# No tracked file's bytes are modified by any probe here.
#
# T1 through T5 each exit with their FINDING count.  A non-zero exit is how a
# probe here reports findings and is the expected state, not a breakage: the
# predicted codes were committed in PREDICTIONS.md before any probe existed.
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

run selftest56dc.py  out_selftest_56dc.txt
run t1_grain.py      out_t1_grain.txt
run t2_strictest.py  out_t2_strictest.txt
run t3_population.py out_t3_population.txt
run t4_standing.py   out_t4_standing.txt
run t5_fixture.py    out_t5_fixture.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^T[0-9] TOTAL\|^selftest56dc TOTAL BAD:\|^FINDING:' out_*.txt || true
