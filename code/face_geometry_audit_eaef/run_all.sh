#!/bin/sh
# mg-eaef: independent audit of the mg-0b07 repair (`bfd7948`, item mg-f7e1) --
# regenerate every transcript.
#
# Pure Python 3, no third-party packages.  Measured runtime 2026-07-31 on a 2024
# laptop: ~6 min.  Most of it is e3 and e5, which run the SUBJECT'S OWN
# `d2_deletion.py` four times at ~65 s each (once in place, unedited, to read
# its exit code; and three times in a copy whose MUTATION table has one token
# rewritten); the rest is ~20 full control batteries at ~2.1 s each.
#
# WHAT IT IS FOR.  mg-f7e1 answers mg-0b07's open item by taking BOTH of the
# moves that audit named: the `shape` guard's implicit disjunction is spelled
# with an `or`, and the deletion test's limit is stated as a count.  This audit
# asks whether each move's claim is true of the code.
#
#   e1  the operator move, re-run: each side deleted alone.  Then the two rungs
#       below it -- a nested boolean operand, and a decision hoisted out of the
#       condition into an assignment.
#   e2  the stated bound against the operands deletion ACTUALLY reaches.
#   e3  the derived declaration, under two changes of patch (mg-0b07's test,
#       re-run here with different anchors after the restructuring).
#   e4  the 8 understate / 3 agree / 0 overstate, re-derived over its 11.
#   e5  THE FLOOR ITEM -- the subject's own instrument's exit code at HEAD, and
#       the one-line remedy it names and does not run.
#
# NOT `python3 x.py | tee out.txt`, and that is deliberate (mg-f922).  A
# pipeline's exit status in POSIX sh is the LAST command's, so `tee` succeeding
# would mask a verifier exiting 1 -- a committed transcript saying BROKEN under
# a run_all.sh that exited 0.  Here the status is captured and re-raised.
#
# CLAIMS vs FINDINGS.  A [BROKEN] claim means THIS audit is wrong and fails the
# run.  A [FINDING] means mg-f7e1 is; it is printed and counted and does not.
#
# Nothing under ../face_geometry or ../face_geometry_instr_5f9a is written:
# every mutation goes to a copy in a temporary directory, and the one run that
# happens in place (e5's, of the subject's own d2_deletion.py) only reads.
set -e
cd "$(dirname "$0")"

run() {
    out=$1
    shift
    set +e
    python3 "$@" > "$out" 2>&1
    status=$?
    set -e
    cat "$out"
    return $status
}

echo "== selftest: this audit's own primitives, on hand-counted inputs =="
run out_selftest_eaef.txt selftest_eaef.py

echo
echo "== e1: each side of the respelled `or`, then rungs six and seven =="
run out_e1_operand.txt e1_operand.py

echo
echo "== e2: the stated bound against what deletion reaches =="
run out_e2_bound.txt e2_bound.py

echo
echo "== e3: is the declaration still DERIVED after the restructuring? =="
run out_e3_derived.txt e3_derived.py

echo
echo "== e4: the 8 of 11, re-derived, with the population named =="
run out_e4_remeasure.txt e4_remeasure.py

echo
echo "== e5: THE FLOOR ITEM -- the exit code, and the unrun remedy =="
run out_e5_floor.txt e5_floor.py
