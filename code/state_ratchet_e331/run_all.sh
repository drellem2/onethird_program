#!/bin/sh
# mg-e331 — the ratchet's runner.  `./build.sh` at the repository root names this file, and
# `./build.sh` is what the refinery invokes as this repository's quality gate on every merge.
#
#   out_ratchet.txt   the ratchet's own transcript
#
# THE EXIT CODE IS NOT THE CLASSIFIER — the rule this arc paid for four times and which is
# stated in full in code/control_gate_724a/run_all.sh.  python exits 1 both when an
# instrument finds something and when it dies before reaching a decision, so the run must be
# shown to have REACHED ITS OWN VERDICT before its exit code is read at all.  No pipe: `cmd
# | tee f` makes `$?` tee's status, which is how a control that exited 1 was reported CLEAN
# (mg-9bc2).
#
# WHAT THIS DOES NOT RUN.  `p1_growth.py` and `x1_positive_control.py` are NOT invoked here.
# They are the evidence the threshold rests on and the demonstration that the threshold
# bites; they read git history and, in one arm, the whole merge gate, and putting them on
# every merge's critical path would buy nothing a committed transcript does not already give.
# What DOES run on every merge is the ratchet itself AND its own falsification (§3 of
# ratchet.py), because an unexercised mechanism is this ticket's entire subject.

set -u
cd "$(dirname "$0")/../.." || exit 1

OUT=code/state_ratchet_e331/out_ratchet.txt

python3 -u code/state_ratchet_e331/ratchet.py > "$OUT" 2>&1
RC=$?
cat "$OUT"

echo
echo "================================================================================"

VERDICT_LINE=$(grep -m1 '^RATCHET VERDICT: ' "$OUT" || true)
if [ -z "$VERDICT_LINE" ]; then
    echo "BROKEN — ratchet.py exited $RC WITHOUT printing a RATCHET VERDICT line.  It did"
    echo "not reach a decision, so this is neither green nor red and MUST NOT be read as"
    echo "either.  Read $OUT: a traceback and a finding are the same exit code."
    exit 2
fi
echo "ratchet exit    : $RC   (0 within the band · 1 the ratchet fired · 2 refused/broken)"
echo "ratchet verdict : $VERDICT_LINE"

case "$RC" in
    0|1|2) ;;
    *)
        echo
        echo "BROKEN — ratchet.py exited $RC, which is not one of its three verdicts.  A"
        echo "runner that maps an unknown exit onto a green one is instance 1 of this arc's"
        echo "defect."
        exit 2
        ;;
esac
exit "$RC"
