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
python3 verify_landing_claims.py | tee out_verify.txt

echo
echo "== mg-e720: eight attack routes on the repaired artifact_banner_check =="
python3 attack_artifact_check.py | tee out_attack.txt
