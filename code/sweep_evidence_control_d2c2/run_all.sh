#!/bin/sh
# mg-d2c2 — runner for the control a4_sweep.py §4 does not have.
#
#   out_p1_names.txt        which directories the sweep names, read out of the sweep
#   out_p2_control.txt      the §3 evidence probe against five worlds with known answers
#   out_p3_adjudicate.txt   real gap or detector artefact, per directory, with exhibits
#
# NOT IN ./build.sh, AND THE REASON IS THE SUBJECT OF THE SUITE.  p2 is SCORED INVERTED:
# its green records that a4_sweep.py's §3 probe is wrong in both directions.  Wire that into
# the merge gate and the gate turns RED on the day somebody REPAIRS the probe — a control
# that punishes the repair it exists to motivate.  code/audit_successor_consolidation_9134,
# code/audit_successor_arming_a518 and code/control_gate_724a each refuse a build.sh entry
# for their own reason ("RED ON ARRIVAL"); this is a fourth reason and not the same one.
#
# WHAT RUNS IT INSTEAD: a person, on demand, plus the committed transcripts, which record
# what it said on 2026-08-12 against a population of 202 directories under code/.
#
# THE EXIT CODE IS NOT THE CLASSIFIER.  python3 exits non-zero both when a check fires and
# when it dies before deciding anything, so each producer is required to leave its own
# DECISION LINE — the line it can only print by reaching the end of its reasoning.  A run
# that exits 0 without one did not run, and is BROKEN, never green.  No pipe into tee:
# `cmd | tee f` makes $? tee's status, which is how a control that exited 1 was once
# reported CLEAN in this repository (mg-9bc2).

set -u
cd "$(dirname "$0")/../.." || exit 1

DIR=code/sweep_evidence_control_d2c2
BROKEN=0
FINDINGS=0

run() {
    script="$1"; out="$2"; needle="$3"
    printf '=== %s ===\n' "$script"
    python3 -u "$DIR/$script" > "$DIR/$out" 2>&1
    rc=$?
    cat "$DIR/$out"
    if ! grep -q "$needle" "$DIR/$out"; then
        printf '\n!! %s exited %s WITHOUT its decision line (%s).\n' "$script" "$rc" "$needle"
        printf '!! The run did not reach a verdict.  BROKEN, not a finding.\n'
        BROKEN=$((BROKEN + 1))
        return
    fi
    if [ "$rc" -ne 0 ]; then
        FINDINGS=$((FINDINGS + 1))
    fi
    printf '\n-- %s exit %s, decision line present\n\n' "$script" "$rc"
}

run p1_names.py            out_p1_names.txt        "^P1 NAMES — "
run p2_two_sided_control.py out_p2_control.txt     "^P2 CONTROL — "
run p3_adjudicate.py       out_p3_adjudicate.txt   "^P3 ADJUDICATION — "

echo "================================================================================"
echo "broken producers        : $BROKEN   (a run that never reached its own verdict)"
echo "producers with findings : $FINDINGS"
echo
grep -h '^P[123] ' "$DIR"/out_p1_names.txt "$DIR"/out_p2_control.txt \
    "$DIR"/out_p3_adjudicate.txt 2>/dev/null
echo

if [ "$BROKEN" -ne 0 ]; then
    echo "SUITE BROKEN — $BROKEN producer(s) never reached a verdict.  Neither green nor red."
    exit 2
fi
if [ "$FINDINGS" -ne 0 ]; then
    echo "SUITE: $FINDINGS producer(s) reported a finding.  Read the decision lines above:"
    echo "p2 is SCORED INVERTED, so a finding there most likely means the probe was REPAIRED."
    exit 1
fi
echo "SUITE CLEAN — every producer reached its verdict and reported what this directory's"
echo "transcripts record."
exit 0
