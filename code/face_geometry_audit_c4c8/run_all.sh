#!/bin/sh
# mg-c4c8: INDEPENDENT AUDIT of the mg-e7bc repair (mg-9220 / b6bc2ef).
#
# Pure Python 3, no third-party packages.  Measured runtime 2026-07-31 on a 2024
# laptop: about 230 s total -- h1 70 s (fifty-seven control batteries: one
# baseline and one per `return` in face_complex.py), h2 46 s (twenty-two
# batteries plus 28,900 predicate pairs over three implementations), h3 113 s
# (six runs of the label check as a subprocess, plus all four of the repair's
# own scripts and mg-e7bc's g1 re-run as processes), h4 0.5 s (no battery: it
# parses trees and walks git history).
#
# WHAT IT IS FOR.  mg-9220 says the deletion test is now PER RETURN and that the
# inert return is gone.  h1 deletes every `return` in face_complex.py one at a
# time and reports the artifact for each.  h2 re-derives mg-d0e2's nine at their
# own unit, runs them on the live tree, and then asks the same question one level
# down: every CLAUSE of every condition that decides a return.  h3 re-runs the
# negative control as a process and reports the exit code, then runs three
# corruptions no list names, and re-runs all four of the repair's scripts to
# check the landing's '72 claims (d1 17, d2 33, d3 6, d4 16)' against the rows
# that produce it.  h4 checks every DECLARED unit against its own patch -- the
# declaration is now the claim the evidence rests on -- and audits the
# provenance of the two pinned commits.
#
# CLAIMS vs FINDINGS, and the exit status is only the first.  A BROKEN claim
# means THIS instrument is wrong.  A FINDING means mg-9220 is.  An audit whose
# exit code conflates the two cannot be run in CI by anyone -- so this script
# exits nonzero on a broken claim of its own, and the findings are counted and
# printed where a reader will see them.
#
# NOTHING UNDER ../face_geometry IS WRITTEN.  Every mutation is applied to a copy
# in a temporary directory and every battery run captures stdout instead of
# tee-ing it.
#
# NOT `python3 x.py | tee out.txt`, and that is deliberate: a pipeline's exit
# status in POSIX sh is the LAST command's, so `tee` succeeding would mask a
# verifier exiting 1 -- a committed transcript saying BROKEN under a run_all.sh
# that exited 0.  mg-f922 found exactly that shape in this repository.
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

echo "== h1: THE PRIMARY MEASUREMENT -- every \`return\`, deleted alone =="
run out_h1_per_return.txt h1_per_return.py

echo
echo "== h2: the nine at their own unit, and the level below a return =="
run out_h2_the_nine_and_the_clause.txt h2_the_nine_and_the_clause.py

echo
echo "== h3: the negative control, re-run, plus three corruptions =="
run out_h3_control.txt h3_control.py

echo
echo "== h4: every declared unit against its patch, and the pinned commits =="
run out_h4_declared_unit.txt h4_declared_unit.py
