#!/bin/sh
# mg-ec63 -- the ARC-WIDE truncate-before-probe sweep.
#
# Pure Python 3, no dependencies, no network.  IT IS SLOW: it runs 422 of the
# arc's own probes once each (S2) and the confirmed-biting subset two or three
# times more (S3).  Measured 2026-08-06 on an M-series laptop: about 90 minutes,
# almost all of it other tickets' probes doing their own work.  There is no way
# to make it fast that does not also make it a text rule, which is the thing
# this ticket exists to stop trusting.
#
# WHAT WRITES, AND WHAT IS RESTORED.  S2, S3 and S5 run other trees' probes,
# and S3 and S5 EMPTY one transcript before doing so, because reproducing the
# defect is the measurement.  Every probe's output is captured to memory and
# NEVER redirected onto a transcript, and every tree is restored with
# `git checkout --` in a `finally`.  S6e asserts the whole arc is byte-clean
# afterwards and goes red if it is not.
#
# THE ORDER IS THE POINT.  S2 and S3 measure AGAINST THE DEFECT.  Applying the
# structural fix first and sweeping afterwards destroys the evidence: once the
# probe reads a full transcript you cannot tell what it used to miss.  This
# suite therefore fixes NOTHING in any other tree, and says so in README.md
# under WHAT I DID NOT DO.
#
# WRITE TO A TEMP AND MOVE, rather than redirecting onto the transcript.  This
# runner uses mg-bf79's structural fix, and not as tidiness: S1 counts runners
# by how they write, S2 runs every probe of every truncating runner, and this
# suite is a member of the population `code/*/run_all.sh` the moment it exists.
# A plain `>` here would put THIS SUITE inside its own subject -- which is what
# mg-03d1's sweep did, and its own A4b prediction went from right to wrong the
# moment it happened.  S6a prints the count both with and without me either way.
#
# EVERY PROBE EXITS WITH ITS OWN FINDING COUNT.  A non-zero exit is how a probe
# here reports findings and is not a breakage.  The predicted codes are in
# PREDICTIONS.md, committed at 454f565 before any script here existed, and
# OUTCOMES.md scores what they actually do.
set -u
cd "$(dirname "$0")"

# THE TIMEOUT IS A CEILING ON WHAT THE SWEEP CAN SEE, so it is set here where
# it can be read, not buried in a default.  A probe killed before it reaches
# the line that opens its own transcript is recorded as not-reading when the
# truth is not-known, which makes S2b's counts LOWER BOUNDS.  120 s is the
# largest this suite can afford across 422 probes; some of the arc's own
# runners take ten minutes, so the bound is real and S6/SD6b names it.
EC63_TIMEOUT=${EC63_TIMEOUT:-120}
EC63_WORKERS=${EC63_WORKERS:-4}
export EC63_TIMEOUT EC63_WORKERS

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

run selftest_ec63.py  out_selftest_ec63.txt
run s1_population.py  out_s1_population.txt
run s2_bite.py        out_s2_bite.txt
run s3_sweep.py       out_s3_sweep.txt
run s4_damage.py      out_s4_damage.txt
run s5_control.py     out_s5_control.txt
run s6_self.py        out_s6_self.txt

echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^S[0-9] TOTAL\|^S5 CONTROL:\|^selftest_ec63 TOTAL:\|^FINDING:' \
    out_*.txt || true
