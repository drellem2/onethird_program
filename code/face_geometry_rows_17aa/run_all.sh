#!/bin/sh
# mg-17aa: regenerate this ticket's transcripts.
#
# Measured runtime on a 2024 laptop, 2026-08-10, on the tree that ships this
# comment (measured here, not carried forward from another ticket's file):
# 13.6 s total -- verify_17aa.py 7.8 s (the n = 6 arm is most of it: 318 further
# posets x four mutations, |L(P)| up to 720) and demo_wrong_way.py 5.0 s (two
# full runs of the control battery as subprocesses).  The battery itself went
# 2.22 s -> 2.65 s under this ticket, re-measured on this tree: the exhibit row
# runs eight extra light sweeps of the 86-poset population.
#
# THE ORDER MATTERS AND IT IS NOT THIS FILE'S ORDER.  Both scripts here READ the
# battery's committed artifact.  If controls.py has been edited, regenerate in
# this order or the derived controls disagree with the tree and g1/d3 go red for
# a reason that is not this ticket's:
#
#   1. code/face_geometry/run_all.sh                 (controls_output.txt)
#   2. retag_rows -> pc_all_pass.txt (audit_e7bc) and
#      positive_control_all_fail.txt (instr_5f9a)   -- the two DERIVED controls
#   3. code/face_geometry_landing_da45/run_all.sh    (out_verify.txt)
#   4. this file
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so tee succeeding would mask a verifier exiting 1 and commit a
# transcript saying BROKEN under a runner that exited 0 (mg-f922 found that
# shape in this repository).  The status is captured and re-raised instead.
#
# Nothing outside code/face_geometry_rows_17aa/ is written by either script:
# demo_wrong_way.py builds its mutated tree in a temp directory and reads the
# pre-mg-17aa controls.py out of git BY BLOB SHA.
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

echo "== verify: absorb == 0 is forced on all four rows, and what remains can fail =="
run out_verify_17aa.txt verify_17aa.py

echo
echo "== demo: the control that goes red when the section becomes more honest =="
run out_demo_wrong_way.txt demo_wrong_way.py
