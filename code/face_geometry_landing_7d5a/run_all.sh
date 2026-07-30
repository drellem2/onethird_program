#!/bin/sh
# mg-7d5a: landing the mg-6653 audit of ba3ec79 -- regenerate both outputs.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on
# a 2024 laptop: 11.6 s total -- verify_landing.py 1.1 s (git + a tree scan),
# the re-run of mg-6653's own attack battery 10.5 s (five full runs of the
# face-geometry control battery on private temp copies; the committed tree is
# never modified).
#
# verify_landing.py re-measures every fact this landing asserts: the four
# refutations of the struck sentence, the 38/38 population WITH ITS METHOD, row
# 135's growth, and the Probe changelog against the hunks ba3ec79 contains.
# Nothing in it is inherited from mg-6653 or from the ticket.
#
# The second step re-runs mg-6653's OWN attack_banner.py, unmodified, against
# the repaired controls.py.  That script is the auditor's instrument, not this
# landing's, which is the point: the repair is scored by the thing that broke
# it.  ATTACKS B and C flip from "ATTACK SUCCEEDS" to "attack repelled" and
# ATTACK A still holds, so the control did not become a tautology.  The prose
# block at the foot of that script is mg-6653's frozen verdict on ba3ec79 and
# still describes the pre-repair state; the per-attack verdicts above it are
# the live result.
#
# verify_landing.py's own transcript, out_verify.txt, is the ONE file its tree
# scan skips -- a scanner that counted its own output could not regenerate
# byte-identically even once.  It says so in its own output.
#
# WHAT "REGENERATES" MEANS HERE, stated because the audit this lands has just
# been re-run and did not.  Both outputs regenerate byte-identically AT THIS
# COMMIT -- verified, two runs each.  They will NOT after later commits land:
# verify_landing.py measures the live tree and the live history, so its
# transcript freezes while what it measures moves.  That is why the STATE.md
# paragraph it supports names a CLASS and points at this scanner, instead of
# freezing a count into prose that nothing re-runs.
set -e
cd "$(dirname "$0")"

echo "== mg-7d5a: this landing's claims, re-measured =="
python3 verify_landing.py | tee out_verify.txt

echo
echo "== mg-7d5a: mg-6653's attack battery, re-run against the repaired control =="
python3 ../face_geometry_audit_6653/attack_banner.py \
    | tee out_attack_banner_after_repair.txt
