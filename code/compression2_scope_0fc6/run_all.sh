#!/bin/sh
# mg-0fc6 — SCOPING docs/imports/compression2.tex.  ~22 s measured on this host.
#
# NOT A GATE.  This instrument is not in build.sh: it prices a Daniel drop, it does not
# guard an invariant.  It is run by hand and its transcripts are committed.
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in a0_selftest.py a1_chain.py a2_realizability.py a3_pricing.py a4_operators.py; do
    echo
    echo "############################################################ $a"
    python3 "$a" | tee "out_${a%.py}.txt"
    RC=$?
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
