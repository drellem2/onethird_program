#!/bin/sh
# mg-d0e2 -- INDEPENDENT AUDIT of mg-5f9a (5cae82c), the third attempt at one
# sentence in NEGATIVE CONTROL 4.  Regenerates every number quoted in
# docs/audit-mg-5f9a-deletion-test.md.
#
# Pure Python 3, no third-party packages.  Measured 2026-07-30 on a 2024 laptop:
# 26 s total -- e1 20 s (ten full control batteries, nine of them on mutated
# copies), e2 3 s, e3 3 s.
#
# WHAT IT IS FOR.  mg-1c80 caught the SECOND generation of this defect with one
# test: delete from the predicate the gate the artifact's explanation names, and
# see whether the artifact moves.  It did not, and that was the proof.  mg-5f9a
# was told to make that test bite and reports it biting on two gates.
# `face_complex.ABSORB_GATES` names four.  e1 runs it on all four.
#
# NOTHING UNDER ../face_geometry IS WRITTEN by any of these.  Every mutation is
# applied to a copy in a temporary directory; every battery run captures stdout
# as bytes.
#
# NOT `python3 x.py | tee out.txt`.  A pipeline's exit status in POSIX sh is the
# LAST command's, so tee would mask a verifier exiting 1 -- a committed
# transcript reading BROKEN under a run_all.sh that exited 0.  mg-f922 found
# that shape in this repository and mg-5f9a's own runner avoids it; so does this
# one.  The status is captured and re-raised, so `set -e` is the whole failure
# protocol.
#
# EXIT STATUS IS ABOUT THIS AUDIT, NOT ABOUT ITS SUBJECT.  A [FINDING] line is a
# defect in mg-5f9a and does NOT fail this script; a [BROKEN] line is a claim of
# this audit's own that did not hold, and does.  An audit that exits 1 whenever
# it finds something cannot be re-run by the person fixing it.
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

echo "== e1: the deletion test, on every gate the explanation names =="
run out_e1_deletion.txt e1_deletion.py

echo
echo "== e2: the gate whose deletion moved nothing, and what that costs =="
run out_e2_parity.txt e2_parity.py

echo
echo "== e3: seams of a twice-corrected artifact, and the check that cannot fail =="
run out_e3_seams.txt e3_seams.py
