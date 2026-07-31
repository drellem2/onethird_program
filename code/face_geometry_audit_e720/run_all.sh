#!/bin/sh
# mg-e720: independent audit of mg-7d5a (commit d5a3043) -- regenerate both outputs.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on
# a 2024 laptop, wall clock: 14.8 s total -- verify_landing_claims.py 8.6 s
# (~200 `git show` invocations for the ls-tree scan; 3.4 s of it is CPU),
# attack_artifact_check.py 5.1 s (eight full runs of the face-geometry control
# battery at n <= 4, each on a private temp copy; the committed tree is never
# modified).  Order-seconds, so no scoping is needed.
#
# verify_landing_claims.py re-measures every checkable claim mg-7d5a makes about
# git, about the tree and about its own diff.  attack_artifact_check.py attacks
# the repaired artifact_banner_check by eight routes, four of which no previous
# generation tried.  Neither re-opens the probe's mathematics, which mg-e0ce,
# mg-5630, mg-f7bc and mg-86a3 rebuilt and which nothing here touches.
#
# WHAT "REGENERATES" MEANS HERE, and it is stronger than the last two
# generations could claim.  Both outputs regenerate byte-identically AT ANY
# COMMIT, not only at this one, because both instruments read a FIXED object:
# verify_landing_claims.py scans `git ls-tree -r d5a3043` rather than the
# working tree, and attack_artifact_check.py mutates a temp copy of
# code/face_geometry at whatever revision is checked out -- so the only way to
# move these numbers is to change controls.py, which is the thing being scored.
# mg-7d5a's own scanner reads the live tree and its transcript froze on contact
# with this audit; that is why the count it defends had to be re-derived here
# from the commit instead of from the tree.
#
# STATE.md is NOT edited by this audit.
set -e
cd "$(dirname "$0")"

echo "== mg-e720: mg-7d5a's claims about git, the tree and its own diff =="
# mg-c2b3: every step in this file that is followed by a bare `cat` of its
# own transcript used to pipe into `tee` instead of redirecting.  A pipeline's
# exit status in POSIX sh is its LAST command's, which is tee's and is 0 --
# so the step could print failures, exit 1, and leave this runner exiting 0.
# Each now redirects and has its status read by an explicit `||` guard.  The
# other steps in this file were already guarded and are untouched.
# `set -o pipefail` is not used: `/bin/sh` is dash on Linux, which rejects the
# option and would abort the runner at the line meant to make it safer.
# This note deliberately avoids writing the old pipeline out, so that a plain
# grep for it over the arc still counts only the sites that still have one.
python3 verify_landing_claims.py > out_verify.txt || {
    cat out_verify.txt; echo "verify_landing_claims.py FAILED"; exit 1; }
cat out_verify.txt

echo
echo "== mg-e720: eight attack routes on the repaired artifact_banner_check =="
python3 attack_artifact_check.py > out_attack.txt || {
    cat out_attack.txt; echo "attack_artifact_check.py FAILED"; exit 1; }
cat out_attack.txt
