#!/bin/sh
# mg-9b6b -- what remains as a lever on row 8 once the density route is closed?  The route's LAST
# NAMED SURVIVOR is mg-0b96 §6's density-to-balance bound, and this suite prices every reading of
# it.  Standard library only, exact rationals on every verdict path, ~3.5 min measured on this host
# (three separate delta sweeps at n = 8 are most of it).
# NOT a merge gate: this is a research instrument, and build.sh's suites are unchanged.
#
# ⚠️  THE FROZEN CLASS IS EMPTY AT EVERY n ANY ENUMERATOR REACHES.  Nothing here is a measurement ON
# frozen posets and no arm claims one; e0 T6 establishes the emptiness on this instrument's own
# population, and e2 m1 makes that emptiness the SUBJECT rather than a caveat.
#
# ARM ORDER IS NOT ARBITRARY.  e0 runs first and carries both WRONG-DIRECTION controls -- the
# population warning, and the must-FIRE control at beta = 2/5 where the class is not empty.  If the
# second passed silently, every "empty" and every "no lever" below would be a property of the tool
# rather than of the question, and nothing in this directory would be falsifiable by this suite.
#
# EACH ARM RECOMPUTES ITS OWN delta SWEEP AND THAT IS DELIBERATE.  Caching it to a file would make
# three transcripts functions of a fourth artefact nobody regenerates; 3.5 minutes is the price of
# each arm being reproducible on its own.
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so a red
# arm would be invisible.  Each arm writes its own transcript and the status is read from the arm.
# (Convention inherited from code/frozen_density_0b96, which took it from code/boundary_epsilon_6ff4.)
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in e0_selftest e1_collapse e2_frontier e3_dial
do
    (cd "$d" && python3 -B "$arm.py" > "out_$arm.txt" 2>&1)
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-9b6b lever-shape suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
