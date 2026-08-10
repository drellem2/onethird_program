#!/bin/sh
# mg-9876 — the audit of how code/rendered_twin_pin_9bc2's instruments get VALIDATED.
#
# THIS RUNNER IS A CONTROL AND IT IS THE FOURTH THING IN THIS LINEAGE TO BE ONE.  The first
# laundered green in the audited directory was ITS runner: `cmd | tee f` made `$?` tee's
# status, and it printed CLEAN over a control that had exited 1.  That was repaired there by
# redirect-then-cat, which fixes the pipe and leaves the deeper error standing — the exit
# code was still being asked a question it cannot answer.  A python process exits 1 when it
# finds drift AND when it dies in a traceback, so `1` means both "the instrument worked" and
# "the instrument never ran".  a2's auxiliary probe demonstrates the audited runner calling a
# crash `DRIFT` and exiting 0.
#
# SO NOTHING HERE IS CLASSIFIED BY EXIT CODE ALONE.  Each producer must also leave its OWN
# DECISION LINE in its transcript — the line it can only print by reaching the end of its
# reasoning.  A run that exits 0 without one did not run, and is reported as BROKEN, never as
# green.  mg-f8e5 reached the same rule from the other direction after running five producers
# without their interpreter and reading the empty files the redirections left.
#
#   out_a1_census.txt         the arm list and the machine completeness check
#   out_a2_discriminate.txt   every arm run against a known-bad input
#   out_a3_auditor_selftest.txt   six planted worlds: how this instrument can fail
#   out_a4_sweep.txt          the same smells counted across code/

set -u
here="$(cd "$(dirname "$0")" && pwd)"
cd "$here/../.." || exit 1

BROKEN=0
FINDINGS=0

# run <script> <transcript> <decision-line-grep>
run() {
    script="$1"; out="$2"; needle="$3"
    printf '=== %s ===\n' "$script"
    python3 -u "code/control_audit_9876/$script" > "code/control_audit_9876/$out" 2>&1
    rc=$?
    cat "code/control_audit_9876/$out"
    if ! grep -q "$needle" "code/control_audit_9876/$out"; then
        printf '\n!! %s exited %s WITHOUT its decision line (%s).\n' "$script" "$rc" "$needle"
        printf '!! The run did not reach a verdict.  This is BROKEN, not a finding.\n'
        BROKEN=$((BROKEN + 1))
        return
    fi
    if [ "$rc" -ne 0 ]; then
        FINDINGS=$((FINDINGS + 1))
    fi
    printf '\n-- %s exit %s, decision line present\n\n' "$script" "$rc"
}

run a1_census.py            out_a1_census.txt          "^CENSUS "
run a2_discriminate.py      out_a2_discriminate.txt    "^VERDICT: "
run a3_auditor_selftest.py  out_a3_auditor_selftest.txt "planted worlds scored as required"
run a4_sweep.py             out_a4_sweep.txt           "^SWEEP "

echo "================================================================================"
echo "broken producers : $BROKEN   (a run that never reached its own verdict)"
echo "producers with findings : $FINDINGS"
echo

if [ "$BROKEN" -ne 0 ]; then
    echo "BROKEN — $BROKEN producer(s) did not reach a verdict.  Nothing above is evidence."
    echo "A runner that maps 'did not run' onto 'found nothing' is instance 1 of this"
    echo "ticket, and refusing to do that is the only reason this branch exists."
    exit 2
fi

if [ "$FINDINGS" -ne 0 ]; then
    echo "FINDINGS PRESENT — $FINDINGS producer(s) reported something.  Read the transcripts."
    echo "a2 exits non-zero while ANY arm is laundered; a3 exits non-zero if this"
    echo "instrument's own scoring rule stopped returning the known answer, and THAT is the"
    echo "one to read first."
    exit 1
fi

echo "ALL GREEN — every registered arm was shown to go RED against a known-bad input, and"
echo "the auditor returned the known verdict in all six planted worlds."
exit 0
