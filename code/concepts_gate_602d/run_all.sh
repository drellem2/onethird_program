#!/bin/sh
# mg-602d — the two arms behind docs/CONCEPTS.md.  Standard library only, ~0.2 s measured.
#   c0  the conceptual document asked its own two rules: pointers, markers, length, links,
#       and whether STATE.md links to it at all
#   c1  planted worlds, both directions -- six that must fire, one that must REFUSE, and one
#       WRONG-DIRECTION world that must stay green because it measures c0's stated limit
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so a
# red arm would be invisible and this script would be green forever -- mg-06d1's D2, a fail-open
# merge gate.  Each arm writes its transcript and the status is read from the arm.
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in c0_concept_discipline c1_controls
do
    python3 "$d/$arm.py" > "$d/out_$arm.txt" 2>&1
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-602d concepts-gate suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
