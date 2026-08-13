#!/bin/sh
# run_a4_census.sh -- THE ONE SECTION OF THIS AUDIT THAT build.sh RUNS ON EVERY MERGE (mg-d72e).
#
# WHY A SECOND RUNNER AND NOT `run_all.sh`.  `run_all.sh` is the instrument: five sections,
# 26.38 s measured on this host, and it is what you run to re-take mg-94c3's audit.  This
# file exists because the gate wants ONE of those sections and wants it for a reason that
# does not apply to the other four -- see build.sh's mg-d72e entry, which carries the
# numbers.  Adding `run_all.sh` to the gate instead would buy the same coverage for a4_census
# at 100x the cost, and the cost was measured before that was decided rather than after.
#
# THE SAME DISCIPLINE AS `run_all.sh`, deliberately, because a section that is graded one way
# by the instrument and another way by the gate is two controls that can disagree:
#
#   * exit 0 is PRE-REGISTERED.  a4_census has no detector-fires headline, so non-zero is a
#     real failure and not a finding.
#   * NO TRUNCATION on the output path -- no head/tail/sed/grep between the script and its
#     transcript.
#   * a section writing fewer than 20 lines is a hard failure REGARDLESS of its exit code,
#     because "returned 0" and "examined nothing" must be different outcomes.
#
# THE FAILURE THIS RUNNER IS MOST LIKELY TO SEE, and it is not a defect in mg-94c3's audit:
# a4_census reads the corpus AT A DECLARED COMMIT (`AS_OF`, mg-c824's pinning) via `git show`,
# so if that commit ever becomes unreachable the section exits 1 and prints which path it
# could not read at which commit.  Measured: exit 1, 32 lines, with the commit in the message.
# `7b7d093` is an ancestor of `main` (checked, mg-d72e), so reaching that state needs a
# history rewrite and not routine gc.  If it ever happens, the repair is to re-pin `AS_OF`
# in a4_census.py -- not to drop this suite from the gate.
#
# THE TRANSCRIPT IS WATCHED.  `out_a4_census.txt` is a tracked `code/**/out_*.txt` that a
# suite now rewrites, so mg-f771's g0 compares what this runner just wrote against the
# committed copy on every gate run.  That is the whole point of the addition and it is why
# the write goes to the tracked path rather than to a temporary.

set -e
cd "$(dirname "$0")"

s=a4_census
printf '%s ... ' "$s"
if python3 "$s.py" > "out_$s.txt" 2>&1; then
    got=0
else
    got=$?
fi
lines=$(wc -l < "out_$s.txt" | tr -d ' ')
if [ "$got" -ne 0 ]; then
    echo "FAILED (exit $got, expected 0)"
    echo "SECTION FAILED"
    exit 1
elif [ "$lines" -lt 20 ]; then
    echo "FAILED (exit 0 but only $lines lines -- examined nothing)"
    echo "SECTION FAILED"
    exit 1
fi
echo "ok ($lines lines)"
echo "SECTION OK"
exit 0
