#!/bin/sh
# mg-fa83 — the runner.  NOT IN ./build.sh, and §7 of the README says why with a number.
#
#   out_w0_selftest.txt    the witness machinery, broken on purpose
#   out_w1_witnesses.txt   the census: rules that pass a gated control and are wrong
#
# ORDER IS LOAD-BEARING.  w0 runs FIRST because everything w1 prints is a statement about
# the estate ONLY IF the sandbox is faithful, and w0 is what says it is.  A w1 transcript
# committed beside a red w0 is a page of numbers about a broken instrument.
#
# THE EXIT CODE IS NOT THE CLASSIFIER — the rule this arc paid for four times (see
# code/control_gate_724a/run_all.sh).  python exits 1 both when an instrument finds
# something and when it dies before reaching a decision, so each run is shown to have
# REACHED ITS OWN VERDICT before its exit code is read at all.  No pipe: `cmd | tee f`
# makes `$?` tee's status, which is how a control that exited 1 was once reported CLEAN
# (mg-9bc2).
#
# w1 EXITS 0 EVEN WHEN EVERY WITNESS PASSES, and that is deliberate rather than lax: every
# finding it prints is a property of SOMEBODY ELSE'S control, and an arm that went red on
# them would make this branch red for a defect it reports rather than introduces —
# mg-e35b's red-on-improvement wearing the measurement's clothes.  w0 is the arm that may
# go red, because a hole there is this directory's own.

set -u
cd "$(dirname "$0")/../.." || exit 1

DIR=code/coarse_unit_fa83
WORST=0

run() {
    script="$1"
    out="$2"
    marker="$3"
    python3 -u "$DIR/$script" > "$DIR/$out" 2>&1
    rc=$?
    cat "$DIR/$out"
    echo
    echo "================================================================================"
    line=$(grep -m1 "^$marker" "$DIR/$out" || true)
    if [ -z "$line" ]; then
        echo "BROKEN — $script exited $rc WITHOUT printing a '$marker' line.  It did not"
        echo "reach a decision, so this is neither green nor red and MUST NOT be read as"
        echo "either.  Read $DIR/$out: a traceback and a finding are the same exit code."
        WORST=2
        return
    fi
    echo "$script exit    : $rc"
    echo "$script verdict : $line"
    if [ "$rc" -gt "$WORST" ]; then WORST=$rc; fi
    echo
}

run w0_selftest.py   out_w0_selftest.txt   "SELFTEST VERDICT: "
run w1_witnesses.py  out_w1_witnesses.txt  "VERDICT: "

echo "================================================================================"
echo "worst exit: $WORST"
exit "$WORST"
