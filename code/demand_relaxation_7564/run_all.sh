#!/bin/bash
# mg-7564 -- the demand-side ladder.  d0 is a GATE: d1..d3 do not run unless it passes.
#
# RUN THIS AS bash, NOT sh.  It reads ${PIPESTATUS[0]} to recover the python exit code
# from behind the `| tee`, and POSIX sh has no PIPESTATUS -- under `sh run_all.sh` the
# gate would read tee's status, which is 0 whatever it was fed.  That is mg-9876's §2
# smell exactly; this file is on that sweep's candidate list and this comment is the
# adjudication.  The shebang is the fix; the comment is so nobody "simplifies" it.
set -u
cd "$(dirname "$0")"

python3 d0_selftest.py 2>&1 | tee out_d0_selftest.txt
RC=${PIPESTATUS[0]}
if [ "$RC" -ne 0 ]; then
  echo "GATE FAILED (rc=$RC) -- d1, d2 not run"
  exit 1
fi

FAIL=0
for arm in d1_ladder d2_evaporation d3_ceiling; do
  python3 "$arm.py" 2>&1 | tee "out_$arm.txt"
  RC=${PIPESTATUS[0]}
  if [ "$RC" -ne 0 ]; then
    echo "ARM $arm FAILED (rc=$RC)"
    FAIL=1
  fi
done
exit "$FAIL"
