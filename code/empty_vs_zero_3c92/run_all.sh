#!/bin/sh
# mg-3c92 -- EMPTY IS NOT ZERO.  mg-9b6b's carry-forward proposes a rule for the
# whole estate: any arm that can return "no answer" and "the answer is zero"
# must print them differently.  This suite asks whether the estate exhibits the
# defect, and whether the rule can be enforced by looking.  Standard library
# only, ~60 s measured on this host (two full AST passes over 1 249 files).
#
# NOT A MERGE GATE, and the reason is not cost: build.sh's suites are unchanged
# because NOTHING HERE IS A PROPERTY THE ESTATE MUST HOLD.  61 collapses is a
# measurement, not a violation; z1 §5 says in as many words that COLLAPSE is
# not an accusation.  A census that gates is a census whose subjects learn to
# spell around it, and the first thing they would spell around is the one
# figure worth having -- z1 §3's 88.8%, which is only interesting while nobody
# is being scored on it.
#
# ARM ORDER IS NOT ARBITRARY.  z0 runs FIRST and carries D0, because z1's
# central figures are a 0, a 61 and a 24, and a broken walk, an unresolvable
# pin or a narrowed class returns a small number for free.  z0 also carries
# both wrong-direction controls (D8, D9) and the must-FIRE half (D1) without
# which every "not flagged" below is a property of the tool.
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's
# exit status, so a red arm would be invisible.  Each arm writes its own
# transcript and the status is read from the arm.  (Convention inherited from
# code/lever_shape_9b6b, which took it from code/frozen_density_0b96.)
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in z0_selftest z1_census
do
    (cd "$d" && python3 -B "$arm.py" > "out_$arm.txt" 2>&1)
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-3c92 empty-vs-zero suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
