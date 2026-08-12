#!/bin/sh
# mg-7c78 — Daniel's adjacent-triples observation, both readings.  Standard library only,
# ~2 min measured on this host.  NOT a merge gate: this is a research instrument, and only
# code/facts_registry_03cf/ gates the FACTS.md entries it produced.
#
# THE ARMS COME IN TWO FAMILIES BECAUSE THE TICKET'S PREMISE WAS CORRECTED MID-RUN.
#   a*  the MISFILED reading -- adjacent ELEMENT POSITIONS inside one linear extension.  Kept,
#       not deleted, for two reasons: everything they measure is TRUE, and a5/a6 turned up the
#       delta = 1/3 boundary class being width 2 with ZERO 3-element antichains, which is what
#       kills one of the corrected reading's branches in b0.
#   b*  Daniel's ACTUAL object -- adjacent LINEAR EXTENSIONS (pm-onethird's correction of
#       2026-08-12 22:41Z, quoting Daniel verbatim).
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so a
# red arm would be invisible.  Each arm writes its own transcript and the status is read from the
# arm, not from the plumbing.
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in a0_selftest a1_existence a2_single_extension a3_symmetry_breaking \
           a4_reversibility_bound a5_boundary_class a6_e_locality \
           b0_mutual_adjacency b1_sequence b2_the_trick
do
    (cd "$d" && python3 "$arm.py" > "out_$arm.txt" 2>&1)
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-7c78 adjacent-triples suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
