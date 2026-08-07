#!/usr/bin/env bash
# run_all.sh — the mg-5827 superseded-figure sweep, all steps, declared exit values.
#
# Writes transcripts NEXT TO ITSELF, via `.new` + `mv`, so a partially-written transcript is
# never mistaken for a complete one and a concurrent reader never sees a half file.
#
# Re-entrancy guard: the arc has destroyed its own transcripts before by having one runner's
# sweep execute another runner over the file it was writing (mg-18dc). The guard is on the
# DIRECTORY, and it is checked by PATH rather than by an inherited environment variable,
# because an exported variable is inherited by anything this script invokes and a guard that
# travels is not a guard.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK="$HERE/.running"
if [ -e "$LOCK" ]; then
  echo "REFUSING TO START: $LOCK exists — another run of THIS directory is in flight." >&2
  exit 2
fi
: > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

cd "$HERE/../.." || exit 2          # repository root; every path below is repo-relative

FAIL=0
step () {   # step <name> <expected-exit> <script...>
  local name="$1" want="$2"; shift 2
  local out="$HERE/out_${name}.txt"
  echo "=== $name (declared exit $want) ==="
  python3 "$@" > "$out.new" 2>&1
  local got=$?
  mv "$out.new" "$out"
  if [ "$got" != "$want" ]; then
    echo "  MISSED ITS DECLARED EXIT: got $got, want $want" >&2
    FAIL=1
  else
    echo "  exit $got as declared"
  fi
}

# s1 exits 0 when every control lands on its expectation. It is declared 0 because a control
# suite that is EXPECTED to fail is not a control suite.
step selftest 0 "$HERE/s1_control.py"

# s2 reports and never gates.
step retrospective 0 "$HERE/s2_retrospective.py"

# s3 is the gate. DECLARED 0 — the corpus is repaired as of mg-5827. If this ever exits 1 the
# gate has found a site, which is the instrument working, not the runner failing.
step gate 0 "$HERE/s3_gate.py"

echo
if [ "$FAIL" = 0 ]; then echo "ALL STEPS ON DECLARED EXIT VALUES."; else echo "AT LEAST ONE STEP OFF ITS DECLARED EXIT VALUE."; fi
exit "$FAIL"
