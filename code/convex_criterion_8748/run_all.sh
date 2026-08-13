#!/bin/sh
# mg-8748 — WHICH CONVEX COMBINATIONS OF COMPRESSIONS ARE CANONICAL.  ~50 s measured on this
# host (c0 1 s · c1 17 s · c2 7 s · c3 25 s · c4 1 s).
#
# NOT A GATE.  This instrument is not in build.sh and must not be added to it: it holds a
# CRITERION, it does not guard an invariant, and nothing in the repository can regress against
# it.  build.sh's own header states the test — a suite belongs there when its rows READ files
# other tickets keep editing.  Every row here reads its own construction.
#
# It is run by hand and its transcripts are committed.  They are deterministic: the one seeded
# arm (c2.3's random statistics) seeds 20260813 explicitly, and every verdict is on exact
# rationals, so a re-run reproduces them byte for byte apart from nothing at all.
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in c0_selftest.py c1_convex.py c2_nested.py c3_transverse.py c4_filter.py; do
    echo
    echo "############################################################ $a"
    python3 "$a" | tee "out_${a%.py}.txt"
    RC=$?
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
