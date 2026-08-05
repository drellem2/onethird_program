#!/bin/sh
# mg-8af0: regenerate this repair's transcripts.
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured
# runtime 2026-08-05 on a 2024 laptop, MEASURED ON THE TREE THAT SHIPS THIS
# COMMENT and not carried forward: 76 s wall -- forcing_8af0.py 5 s (810
# families at n <= 6), the repaired verify_e35b.py 9 s (V4b's n <= 6 sweep is
# new and is most of the rise from mg-e35b's 2.6 s), and face_geometry's own
# runner the remaining 60 s, of which run_probe.py at n <= 6 is 17 s.  So this
# stays in the order-a-minute regime and needs no scoping.  There is NO CI in
# this repository; this runner is hand-invoked, like every other run_all.sh
# here.
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so `tee` succeeding would mask a script exiting 1 -- a
# committed transcript printing REFUTED under a runner that exited 0.  mg-f922
# found exactly that shape in this repository.  Each status is captured and the
# worst is re-raised at the end.
set -e
cd "$(dirname "$0")"
worst=0

echo "== F3: the >= 3-facets zeros are FORCED, and the bound is not vacuous =="
set +e
python3 forcing_8af0.py > out_forcing_8af0.txt 2>&1
status=$?
set -e
cat out_forcing_8af0.txt
[ "$status" -gt "$worst" ] && worst=$status

echo
echo "== the repaired verifier (F1 + F2 + F3 landed) =="
sh ../face_geometry_repair_e35b/run_all.sh > out_verify_rerun.txt 2>&1
status=$?
cat out_verify_rerun.txt
[ "$status" -gt "$worst" ] && worst=$status

echo
echo "== the battery under repair, regenerated =="
sh ../face_geometry/run_all.sh > out_controls_rerun.txt 2>&1
status=$?
tail -20 out_controls_rerun.txt
[ "$status" -gt "$worst" ] && worst=$status

echo
echo "aggregate exit: $worst"
exit "$worst"
