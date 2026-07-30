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
#   scan sees files that did not exist at ba3ec79.
#
#   ^^ CORRECTED 2026-07-30 (mg-e720 F3 / B2, landed by mg-ae62).  The sentence
#   that stood here read "Its FINDINGS are unaffected; only the transcript is",
#   and that is FALSE AS WRITTEN -- this block was added to correct a
#   regeneration claim and introduced a new false claim in the same block.
#   TWO SCORED ROWS FLIP TO REFUTED, and the landing that wrote this block is
#   the cause:
#
#     REFUTED CLAIMS: 7 at ba3ec79 (the committed transcript) -> 9 at d5a3043
#     and at every commit since.  The two rows that flip are
#       - "the five named LIVE sites are all in fact flagged"
#       - "the section-2 sentence now reads n<=5 for the Lemma-1 cross-check"
#
#     WHY, and it is not a change in the facts.  THIS INSTRUMENT MATCHES ROWS BY
#     HARD-CODED (file, line) PAIRS -- verify_claims.py:238-249 for the LIVE
#     enumeration, and :329, which greps a fixed window of Probe lines
#     (cur[140:150], i.e. lines 141-150).  d5a3043 rewrote the Probe's
#     section-head changelog, +20/-7, a net +13 lines ABOVE every one of those
#     anchors.  So the Probe's 38/38 sites moved 408 -> 421, 815 -> 828,
#     822 -> 835, and the "(F3, repaired ...)" sentence moved from 140 to 153,
#     out of the window at :329 (it now reads at line 158).  The paragraphs
#     still carry the truncation flag and the sentence still reads n <= 5; only
#     the LINE NUMBERS this script asserts they sit on are stale.
#
#     SO: mg-6653's SUBSTANTIVE FINDINGS are unaffected -- and its SCORING IS
#     NOT, which is exactly what this block exists to tell a reader.  The
#     row-matching is by line number and HAS AGED OUT.  From d5a3043 onwards, a
#     REFUTED on those two rows means "the anchor moved", not "the claim
#     failed"; every other row is scored as it was.
#
#     THIS CORRECTION CLOSES THE FINDING, IT DOES NOT RELOCATE IT: the false
#     sentence is gone, the two affected rows are named, the mechanism is named
#     at its own file:line, and nothing here now asserts a stability the
#     instrument does not have.  What it does NOT do is re-anchor the matching
#     by content -- that would change what the frozen transcript scores, which
#     this arc does not do to a committed audit.  Re-anchoring is a separate,
#     un-filed question and is not claimed as done.
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
