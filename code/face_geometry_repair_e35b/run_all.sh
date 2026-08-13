#!/bin/sh
# mg-e35b: regenerate this repair's transcripts.
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured
# runtime 2026-07-31 on a 2024 laptop, on the tree that ships this comment:
# 2.6 s.
#
# --- mg-843d ---------------------------------------------------------------
# TWO THINGS CHANGED HERE AND THE SECOND IS THE ONE THAT MATTERS.
#
# (1) A SECOND STEP.  `demo_v6d_row_can_go_red.py` watches V6d fire on four
#     mutations of a throwaway copy of code/face_geometry/.  It is in the
#     runner rather than beside it because a demonstration nothing runs is a
#     claim that rots -- which is this ticket's whole subject.
#
# (2) THIS RUNNER IS NO LONGER HAND-INVOKED.  It is the seventh LOOPED suite of
#     `build.sh`, so it runs on every merge request.  The sentence that used to
#     be here -- "this runner is hand-invoked, like every other run_all.sh
#     here" -- was true when mg-fcf1's minor finding was written and stopped
#     being true today; the wording that finding was about was a runner
#     claiming a CI that did not exist, and a runner denying a gate that does
#     is the same defect pointed the other way.  There is still no CI in this
#     repository: `build.sh` is a merge gate the refinery invokes, and the
#     distinction is drawn in build.sh's own header.
#
# WHY IT IS GATED AT ALL: `verify_e35b.py` carries V6a/V6b/V6c/V6d, four
# tripwires on files OTHER tickets keep editing -- controls.py and
# controls_output.txt.  V6b fired correctly on `de86fee` and sat red for three
# days because nothing ran it.  See build.sh's mg-843d block for the decision
# and its cost.
#
# MEASURED, 2026-08-13, on the tree that ships this comment: 7.2 s for the
# verifier and 35.0 s for the demonstration, 42 s in total.  The demonstration
# is 83% of that and is the removable half if the cost is ever judged wrong --
# removing it is a decision with a number attached, which is more than the
# suite's absence from the gate ever had.
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so `tee` succeeding would mask the verifier exiting 1 -- a
# committed transcript printing REFUTED under a runner that exited 0.  mg-f922
# found exactly that shape in this repository.  The status is captured and
# re-raised.
#
# EVERY STEP RUNS AND THE WORST EXIT WINS, for the reason build.sh gives about
# its own suites: short-circuiting on the first red hides whether the second is
# red too, and a gate that reveals its findings one per merge attempt is one
# people stop reading.
cd "$(dirname "$0")"
STATUS=0

echo "== verify: every number the mg-e35b repair prints, re-derived =="
python3 verify_e35b.py > out_verify_e35b.txt 2>&1
RC=$?
cat out_verify_e35b.txt
[ "$RC" -gt "$STATUS" ] && STATUS=$RC

echo
echo "== demo: V6d watched firing, on four mutations of a throwaway copy =="
python3 demo_v6d_row_can_go_red.py > out_demo_v6d.txt 2>&1
RC=$?
cat out_demo_v6d.txt
[ "$RC" -gt "$STATUS" ] && STATUS=$RC

exit "$STATUS"
