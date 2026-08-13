#!/bin/sh
# mg-6ff4 — eps_spec at the boundary class delta = 1/3 exactly.  Standard library only,
# ~25 min measured on this host (c1 at n = 9 and c2's width-<=3 sweep to n = 10 are most of it).
# NOT a merge gate: this is a research instrument, and build.sh's five suites are unchanged.
#
# ⚠️  delta = 1/3 is OUTSIDE the frozen hypothesis, which is STRICT.  Nothing this suite prints
# is a frozen-class number.  Each arm says so in its own transcript, which is the point: the
# caution has to travel with the figures, not sit in a README nobody opens next to the number.
#
# ARM ORDER IS NOT ARBITRARY.  c0 runs first and includes the two WRONG-DIRECTION controls -- a
# deliberately wrong reference order, and a constructed frozen pair table -- because if either
# of those passes silently, every figure the later arms print is unfalsifiable by this suite.
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so a
# red arm would be invisible.  Each arm writes its own transcript and the status is read from
# the arm, not from the plumbing.  (Convention inherited from code/adjacent_triples_7c78.)
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in c0_selftest c1_census c2_reach c3_gap c4_e_choice c5_supply_scope
do
    (cd "$d" && python3 "$arm.py" > "out_$arm.txt" 2>&1)
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-6ff4 boundary-epsilon suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
