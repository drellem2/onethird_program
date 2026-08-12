#!/bin/sh
# mg-9134 — runner for the clean-verdict-tag consolidation controls.
#
#   out_consolidate.txt   the transcript, committed beside the code
#
# NOT IN ./build.sh, FOR mg-a518's REASON AND NOT A NEW ONE.  Every input this
# suite reads lives OUTSIDE this repository — `~/.macguffin`, the installed
# `pogo` binary, `~/.config/pogo/config.toml` — and none of them is something the
# author of an unrelated mathematics branch can see, reproduce or fix.  Wire it
# into the merge gate and the first person to land a commit on a machine whose
# pogod is mid-restart gets a red gate they cannot act on.  code/control_gate_724a
# and code/state_ratchet_e331 refuse that construction by name ("RED ON ARRIVAL");
# code/audit_successor_arming_a518/run_all.sh refuses it again; this is the fourth.
#
# WHAT RUNS IT INSTEAD: a person, on demand, plus the committed transcript, which
# records what it said on 2026-08-12 when the consolidation landed.
#
# THE EXIT CODE IS NOT THE CLASSIFIER.  python3 exits 1 both when a check fires
# and when it dies before reaching a decision, so the run is shown to have REACHED
# ITS OWN VERDICT before its exit code is read at all.  No pipe into tee: `cmd |
# tee f` makes $? tee's status, which is how a control that exited 1 was once
# reported CLEAN in this repository (mg-9bc2).

set -u
cd "$(dirname "$0")/../.." || exit 1

OUT=code/audit_successor_consolidation_9134/out_consolidate.txt

python3 -u code/audit_successor_consolidation_9134/consolidate_9134.py > "$OUT" 2>&1
RC=$?
cat "$OUT"

echo
echo "================================================================================"

VERDICT_LINE=$(grep -m1 '^CONSOLIDATION VERDICT: ' "$OUT" || true)
if [ -z "$VERDICT_LINE" ]; then
    echo "BROKEN — consolidate_9134.py exited $RC WITHOUT printing a CONSOLIDATION VERDICT"
    echo "line.  It did not reach a decision, so this is neither green nor red and MUST NOT"
    echo "be read as either.  Read $OUT: a traceback and a finding are the same exit code."
    exit 2
fi
echo "controls exit   : $RC   (0 every check behaved · 1 one did not · 2 refused/broken)"
echo "$VERDICT_LINE"
exit "$RC"
