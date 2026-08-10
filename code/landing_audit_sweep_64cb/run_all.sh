#!/usr/bin/env bash
# mg-64cb — the landing/audit concurrency sweep.
#
# NO `| tee`. mg-c2b3 swept this arc and found 23 of 63 run_all.sh piping into tee with
# only 1 setting pipefail, so any of them can print FAILED and exit 0. Output is redirected
# and the exit code read directly.
#
# Order matters: s3 reads adjudicated.json written by nothing else, s4 and s5 read it, so
# s3 must run before them. A missing input is a hard failure here, not a skipped arm.
set -u
cd "$(dirname "$0")"

rc=0
run() {
  local name="$1"; shift
  echo "--- $name"
  if python3 -u "$name.py" > "out_$name.txt" 2>&1; then
    echo "    exit 0"
  else
    local e=$?
    echo "    exit $e   <-- see out_$name.txt"
    rc=$e
  fi
}

run s0_selftest
run s1_population
run s2_collisions
run s3_adjudicate
run s4_survival
run s5_cost
run s6_rule

echo
echo "=== HEADLINE, read back out of the transcripts rather than restated ==="
grep -h '^count CONCURRENT under either reading' out_s2_collisions.txt || true
grep -h '^count RESIDUE' out_s3_adjudicate.txt || true
grep -h '^count seed probes reading LIVE' out_s4_survival.txt || true
grep -h 'total arc-wide delay' out_s5_cost.txt || true
grep -h '^  count REFUSE ' out_s6_rule.txt || true

echo
echo "=== NOTHING OUTSIDE THIS DIRECTORY WAS EDITED ==="
# This ticket REPORTS on landings; it does not perform one. The check is the same one
# mg-fd9c used, and it is available to me precisely because I am not a landing.
git -C ../.. status --porcelain -- . ':(exclude)code/landing_audit_sweep_64cb' | head -20
echo "(empty above = clean)"

exit $rc
