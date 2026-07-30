#!/bin/sh
# mg-6653: independent audit of mg-f2e1 (ba3ec79) -- regenerate both outputs.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on a
# 2024 laptop: 11.6 s total -- verify_claims.py 1.0 s (git + a tree scan),
# attack_banner.py 10.1 s (five full runs of the face-geometry control battery,
# ~2.0 s each, each on a private temp copy; the committed tree is never
# modified).  Both outputs regenerate byte-identically.
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
