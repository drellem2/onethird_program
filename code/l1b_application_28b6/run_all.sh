#!/bin/sh
# mg-28b6 — the two arms behind mg-0e8c's restatement of row 8.  Standard library only,
# ~0.3 s measured.
#   c0  is the restatement APPLIED, at every canonical site, right now — plus a sweep for the
#       discharged existence phrasing appearing anywhere in those files without a rider
#   c1  planted worlds — seven that must fire or refuse, and one WRONG-DIRECTION world that
#       must stay green because it measures c0's stated structure-not-truth limit
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so a
# red arm would be invisible and this script would be green forever -- mg-06d1's D2, a fail-open
# merge gate.  Each arm writes its transcript and the status is read from the arm.
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in c0_application c1_controls
do
    python3 "$d/$arm.py" > "$d/out_$arm.txt" 2>&1
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-28b6 l1b-application suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
