#!/bin/bash
# mg-8d66 -- the k-foliation ceiling.  k0 is a GATE: k1..k5 do not run unless it passes.
set -u
cd "$(dirname "$0")"

python3 k0_selftest.py 2>&1 | tee out_k0_selftest.txt
RC=${PIPESTATUS[0]}
if [ "$RC" -ne 0 ]; then
  echo "GATE FAILED (rc=$RC) -- k1..k5 not run"
  exit 1
fi

FAIL=0
for arm in k1_counting k2_premise k3_monotone k4_ceiling k5_measure; do
  python3 "$arm.py" 2>&1 | tee "out_$arm.txt"
  RC=${PIPESTATUS[0]}
  if [ "$RC" -ne 0 ]; then
    echo "ARM $arm FAILED (rc=$RC)"
    FAIL=1
  fi
done
exit "$FAIL"
