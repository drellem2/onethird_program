#!/bin/sh
# mg-0b96 -- is any UPPER bound on the incomparability density d available for a FROZEN poset,
# from anything that is not the (1/3)-(2/3) conjecture itself?  Standard library only, exact
# rationals on every verdict path, ~2.5 min measured on this host (d3 at n = 9 is most of it).
# NOT a merge gate: this is a research instrument, and build.sh's suites are unchanged.
#
# ⚠️  THE FROZEN CLASS IS EMPTY AT EVERY n ANY ENUMERATOR REACHES.  Nothing here is a measurement
# ON frozen posets and no arm claims one; d0 T6 establishes the emptiness on this instrument's own
# population so that no later zero is read as a clean sweep.
#
# ARM ORDER IS NOT ARBITRARY.  d0 runs first and carries the two WRONG-DIRECTION controls -- the
# population warning, and the must-say-YES control on a non-empty pseudo-frozen class.  If the
# second of those passed silently, every NO in this directory would be a property of the tool
# rather than of the question, and the later arms would be unfalsifiable by this suite.
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so a
# red arm would be invisible.  Each arm writes its own transcript and the status is read from the
# arm.  (Convention inherited from code/boundary_epsilon_6ff4.)
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in d0_selftest d1_equivalence d2_price d3_literature d4_unconditional
do
    (cd "$d" && python3 -B "$arm.py" > "out_$arm.txt" 2>&1)
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-0b96 frozen-density no-hunt suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
