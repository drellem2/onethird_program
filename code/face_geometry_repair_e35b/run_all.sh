#!/bin/sh
# mg-e35b: regenerate this repair's transcript.
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured
# runtime 2026-07-31 on a 2024 laptop, on the tree that ships this comment:
# 2.6 s.  There is NO CI in this repository -- this runner is hand-invoked, like
# every other run_all.sh here, and saying otherwise is the wording mg-fcf1's
# minor finding was about.
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so `tee` succeeding would mask the verifier exiting 1 -- a
# committed transcript printing REFUTED under a runner that exited 0.  mg-f922
# found exactly that shape in this repository.  The status is captured and
# re-raised, so `set -e` is the whole failure protocol.
set -e
cd "$(dirname "$0")"

echo "== verify: every number the mg-e35b repair prints, re-derived =="
set +e
python3 verify_e35b.py > out_verify_e35b.txt 2>&1
status=$?
set -e
cat out_verify_e35b.txt
exit $status
