#!/bin/sh
# mg-3da1 — WHAT THE IMAGE RESULT CLOSES, AND WHAT IT DOES NOT.  ~11 s on this host.
#
# NOT A GATE.  This instrument is not in build.sh: like code/image_geometry_c776/ it answers a
# scoping question rather than guarding an invariant, it is run by hand, and its transcripts
# are committed.
#
# It shares NO CODE with the instrument it corroborates.  lib_c776.py and lib8b32 are not
# imported here and neither is anything else in code/: a defect in a shared poset enumerator
# would move both readings the same way and the agreement would be an artifact.  What the two
# directories share is OEIS A001035 and the definitions, and d0 checks this library against
# A001035 and against brute force before any arm that produces a finding runs.
#
# The arms are ordered so that each rests only on the ones before it:
#   d0  controls on lib3da1 — the external anchor, second and third routes, planted defects
#   d1  THE GENERALISATION — no realizability restriction of ANY kind can tighten a linear
#       ceiling over M_n, because realizability is vacuous at the vertices; plus the control
#       showing what a restriction that DOES tighten looks like
#   d2  what a direction sweep over the image is worth as evidence — measured, against a
#       planted world where a separation exists
#   d3  THE CORRECTION — inside the cell the image tightens by exactly d, so this work item's
#       own title overstates the closure by one clause
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in d0_selftest.py d1_vacuous_realizability.py d2_sweep_power.py d3_cell_correction.py; do
    echo
    echo "############################################################ $a"
    # REDIRECT-THEN-CAT, NOT `| tee`: in POSIX sh `$?` after a pipeline is the LAST command's
    # exit code, so `python3 arm.py | tee out.txt` reports TEE's status and a red arm reads
    # green.  Taken from code/image_geometry_c776/run_all.sh, which is the directory this one
    # corroborates, deliberately: a runner that reported green on a red arm here would be a
    # corroboration instrument that cannot disagree.
    python3 -B "$a" > "out_${a%.py}.txt" 2>&1
    RC=$?
    cat "out_${a%.py}.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
