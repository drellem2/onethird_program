#!/bin/sh
# mg-a518 — runner for the audit-successor arming controls.
#
#   out_controls.txt   the transcript, committed beside the code
#
# THIS SUITE IS DELIBERATELY **NOT** IN ./build.sh, AND THE REASON IS THE TICKET'S
# OWN REASON.  mg-a882's decision closes on: "a gate that goes red for a non-reason
# is how gates get turned off, which would cost more than the blind spot does."
# Every input this suite reads lives OUTSIDE this repository — `~/.macguffin`, the
# installed `pogo` binary, and `~/.config/pogo/config.toml` — and none of them is
# something the author of an unrelated branch can see, reproduce, or fix.  Wire
# this into the merge gate and the first person to land a mathematics commit on a
# machine whose pogod is mid-restart gets a red gate they cannot act on.  That is
# the construction code/control_gate_724a/gate.py refuses in its own docstring,
# and code/state_ratchet_e331/CEILING.json refuses again under the name
# "RED ON ARRIVAL".  It is refused a third time here.
#
# WHAT RUNS IT INSTEAD: a person, on demand, when they want to know whether the
# widening still holds — and the committed transcript, which records what it said
# on 2026-08-12 when the arming landed.  A transcript is weaker than a gate and it
# is what this measurement can honestly be.
#
# THE EXIT CODE IS NOT THE CLASSIFIER — this repository's standing rule (stated in
# full in code/control_gate_724a/run_all.sh).  python3 exits 1 both when a control
# fires and when it dies before reaching a decision, so the run is shown to have
# REACHED ITS OWN VERDICT before its exit code is read at all.  No pipe into tee:
# `cmd | tee f` makes $? tee's status, which is how a control that exited 1 was
# once reported CLEAN in this repository (mg-9bc2).

set -u
cd "$(dirname "$0")/../.." || exit 1

OUT=code/audit_successor_arming_a518/out_controls.txt

python3 -u code/audit_successor_arming_a518/controls_a518.py > "$OUT" 2>&1
RC=$?
cat "$OUT"

echo
echo "================================================================================"

VERDICT_LINE=$(grep -m1 '^CONTROLS VERDICT: ' "$OUT" || true)
if [ -z "$VERDICT_LINE" ]; then
    echo "BROKEN — controls_a518.py exited $RC WITHOUT printing a CONTROLS VERDICT line."
    echo "It did not reach a decision, so this is neither green nor red and MUST NOT be"
    echo "read as either.  Read $OUT: a traceback and a finding are the same exit code."
    exit 2
fi
echo "controls exit   : $RC   (0 every arm behaved · 1 an arm did not · 2 refused/broken)"
echo "$VERDICT_LINE"
exit "$RC"
