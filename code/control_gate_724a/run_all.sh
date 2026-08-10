#!/bin/sh
# mg-724a — the gate's runner.  This is what the refinery invokes on every merge, via
# ./build.sh at the repository root and via .pogo/refinery.toml, which both name this file.
#
#   out_gate.txt   the gate's own transcript
#
# THE EXIT CODE IS NOT THE CLASSIFIER.  This is the fourth runner in this lineage and the
# rule was paid for three times: `cmd | tee f` made `$?` tee's status and printed CLEAN over
# a control that had exited 1 (mg-9bc2); removing the pipe fixed WHOSE status was read and
# left standing the deeper error, that python exits 1 both when an instrument finds something
# and when it dies before reaching a decision (mg-9876); and mg-f8e5 arrived at the same rule
# from the other side after running five producers without their interpreter and reading the
# empty files the redirections left.  So: no pipe, and the run must be shown to have REACHED
# ITS OWN VERDICT before its exit code is read at all.
#
# WHAT THIS WRITES.  gate.py runs both subject suites, and those suites redirect into their
# OWN directories — so a local run leaves four tracked files modified in
# code/rendered_twin_pin_9bc2 and code/control_audit_9876.  That is their design and this
# ticket does not edit another ticket's directory to change it.  In the refinery it is
# harmless: the merge pipeline resets tracked modifications after gates and before the target
# checkout.  Locally, `git checkout -- code/` after a run.

set -u
cd "$(dirname "$0")/../.." || exit 1

OUT=code/control_gate_724a/out_gate.txt

python3 -u code/control_gate_724a/gate.py > "$OUT" 2>&1
RC=$?
cat "$OUT"

echo
echo "================================================================================"

VERDICT_LINE=$(grep -m1 '^GATE VERDICT: ' "$OUT" || true)
if [ -z "$VERDICT_LINE" ]; then
    echo "BROKEN — gate.py exited $RC WITHOUT printing a GATE VERDICT line.  It did not reach"
    echo "a decision, so this is neither green nor red and MUST NOT be read as either."
    echo "Read $OUT: a traceback and a finding are the same exit code."
    exit 2
fi
echo "gate exit    : $RC   (0 baseline matched · 1 gated field diverged · 2 refused/broken)"
echo "gate verdict : $VERDICT_LINE"

case "$RC" in
    0|1|2) ;;
    *)
        echo
        echo "BROKEN — gate.py exited $RC, which is not one of its three verdicts.  A runner"
        echo "that maps an unknown exit onto a green one is instance 1 of this arc's defect."
        exit 2
        ;;
esac
exit "$RC"
