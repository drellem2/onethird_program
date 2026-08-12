#!/bin/sh
# mg-03cf — the two checks behind docs/FACTS.md.  Standard library only, ~2 s measured.
#   f0  the registry asked its own question: every entry carries its frame
#   f1  the one registered statement that is not verbatim in its source
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status,
# so `set -e` would never see a red arm and this script would be green forever -- mg-06d1's
# D2, a fail-open merge gate inside a suite whose subject is a control that cannot fire.
# Each arm writes its transcript and the status is read from the arm, not from the plumbing.
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in f0_registry_discipline f1_adjacency_corollary
do
    python3 "$d/$arm.py" > "$d/out_$arm.txt" 2>&1
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-03cf facts-registry suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
