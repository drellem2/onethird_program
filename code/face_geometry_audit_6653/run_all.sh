#!/bin/sh
# mg-6653: independent audit of mg-f2e1 (ba3ec79) -- regenerate both outputs.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on a
# 2024 laptop: 11.6 s total -- verify_claims.py 1.0 s (git + a tree scan),
# attack_banner.py 10.1 s (five full runs of the face-geometry control battery,
# ~2.0 s each, each on a private temp copy; the committed tree is never
# modified).  Both outputs regenerate byte-identically.
#
# STATUS 2026-07-30 (mg-7d5a, landing this audit).  NEITHER output regenerates
# any more, and that is inherent rather than a defect: both instruments measure
# the LIVE tree and the LIVE history, so their transcripts are frozen at the
# commit they were run against (ba3ec79) while what they measure keeps moving.
#
#   attack_banner.py -- ATTACKS B and C now report "attack repelled" instead of
#   "ATTACK SUCCEEDS": A2 is repaired, and the control scans the artifact's byte
#   stream rather than ROW_NAMES.  ATTACK A still fires, so it is still a
#   control and not a tautology.  The prose block at the foot of that script is
#   mg-6653's verdict on ba3ec79 and still describes the pre-repair state.
#
#   verify_claims.py -- its history counts move with every commit and its 38/38
#   scan sees files that did not exist at ba3ec79.  Its FINDINGS are unaffected;
#   only the transcript is.
#
# Both committed transcripts are deliberately NOT regenerated: an audit's
# findings are what it found, and rewriting them would erase the evidence for
# the repair that followed.  The post-repair run of the attack battery is
# committed beside the repair, at
# code/face_geometry_landing_7d5a/out_attack_banner_after_repair.txt.
#
# verify_claims.py scores CLAIMS mg-f2e1 makes about the tree, the diff and the
# history.  attack_banner.py scores whether a grep on controls_output.txt can
# still be fooled.  Neither re-opens the probe's mathematics.
set -e
cd "$(dirname "$0")"

echo "== mg-6653: mg-f2e1's claims, re-measured =="
python3 verify_claims.py | tee out_verify_claims.txt

echo
echo "== mg-6653: adversarial battery against E5's CONTROL ON THE ARTIFACT =="
python3 attack_banner.py | tee out_attack_banner.txt
