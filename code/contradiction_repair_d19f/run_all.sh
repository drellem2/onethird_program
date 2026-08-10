#!/usr/bin/env bash
# mg-d19f — the mg-51f4 / mg-28ff contradiction: adjudicated, then repaired.
#
# NO `| tee`. mg-c2b3 found 23 of 63 run_all.sh in this arc piping into tee with only 1
# setting pipefail, so any of them can print FAILED and exit 0. Output is redirected and the
# exit code read directly.
#
# Order matters: r3 checks the REPAIR, so it is meaningful only after the document is edited.
# It is run last and it is the arm that can fail this suite for a reason the author caused.
set -u
cd "$(dirname "$0")"

rc=0
run() {
  local name="$1"
  echo "--- $name"
  if python3 -u "$name.py" > "out_$name.txt" 2>&1; then
    echo "    exit 0"
  else
    local e=$?
    echo "    exit $e   <-- see out_$name.txt"
    rc=$e
  fi
}

run r0_selftest
run r1_adjudicate
run r2_literals
run r3_selfcheck

echo
echo "=== HEADLINE, read back out of the transcripts rather than restated ==="
grep -h '^SELFTEST' out_r0_selftest.txt || true
grep -h '^ADJUDICATION' out_r1_adjudicate.txt || true
grep -h '^  Published by mg-51f4' out_r2_literals.txt || true
grep -h '^SELFCHECK' out_r3_selfcheck.txt || true

echo
echo "=== EXACTLY ONE DOCUMENT OUTSIDE THIS DIRECTORY IS EDITED ==="
# This ticket IS a landing, so mg-fd9c's `git status must be empty` check is not available
# to it. What replaces it is the same check with the expected single exception named, and
# it is C4 of r3 -- read back here rather than re-implemented, so there is one definition.
grep -hA2 'C4  mg-28ff is NOT edited' out_r3_selfcheck.txt || true

exit $rc
