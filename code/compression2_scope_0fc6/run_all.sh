#!/bin/sh
# mg-0fc6 — SCOPING docs/imports/compression2.tex.  ~35 s measured on this host.
#
# NOT A GATE.  This instrument is not in build.sh: it prices a Daniel drop, it does not
# guard an invariant.  It is run by hand and its transcripts are committed.
#
# ⚠️  RUNNING THIS REGENERATES out_a0/out_a1/out_a2, WHICH ARE THE EVIDENCE AS COMMITTED
# FROM p0fc6's WORKTREE.  mg-0fc6's second polecat was instructed not to regenerate them and
# did not; a re-run is fine (they are deterministic) but it is not a check of anything and
# it is not how they were produced.  a3, a4 and a5 were run in q0fc6's worktree.
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in a0_selftest.py a1_chain.py a2_realizability.py a3_pricing.py a4_operators.py \
         a5_scale_gap.py; do
    echo
    echo "############################################################ $a"
    python3 "$a" | tee "out_${a%.py}.txt"
    RC=$?
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
