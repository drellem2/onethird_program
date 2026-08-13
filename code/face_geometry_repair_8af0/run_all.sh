#!/bin/sh
# mg-8af0: regenerate this repair's transcripts.  Four of them since mg-36f5.
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  RE-MEASURED
# 2026-08-13 on the tree that ships THIS comment, step by step and not carried
# forward: demo_f2 26.95 s, probe_f1 0.15 s, probe_f3 12.26 s, probe_f3_tightness
# 5.60 s -- 37.6 s for the whole runner.  The previous figures (~12 / 0.4 / 8.3 /
# 4.9, "~26 s total") were taken on 2026-08-05 and 2026-08-13 respectively and
# are superseded rather than adjusted.  demo_f2 is the cost and it roughly
# DOUBLED at mg-fa8a, from five constructions to six: each one regenerates
# controls_output.txt inside a temporary directory, which is the point of it, and
# C6 is the construction that puts mg-fcb2's F1 back at the source.  There is NO
# CI in this repository -- this runner is hand-invoked, like every other
# run_all.sh here except code/face_geometry_repair_e35b/run_all.sh, which
# build.sh gates.
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so `tee` succeeding would mask a probe exiting 1 (mg-f922,
# mg-c2b3).  Each step redirects and has its status read by an explicit guard,
# and the FIRST non-zero status is the one re-raised -- a later pass cannot
# overwrite an earlier refutation.
set -e
cd "$(dirname "$0")"
rc=0

step() {
    name=$1
    script=$2
    out=$3
    echo "== $name =="
    if python3 "$script" > "$out" 2>&1; then
        :
    else
        s=$?
        if [ "$rc" -eq 0 ]; then rc=$s; fi
    fi
    cat "$out"
}

step "F2: can the V6 row go red?  six constructions, old row and new" \
     demo_f2_row_can_go_red.py out_demo_f2.txt
echo
step "F1: the site count on three populations, tautology vs measured" \
     probe_f1_count_moves.py out_probe_f1.txt
echo
step "F3: ridge multiplicity under every mode, 2 <= n <= 6" \
     probe_f3_ridge_multiplicity.py out_probe_f3.txt
echo
step "F3: the bound is TIGHT, and the routine is watched reporting 3 (mg-36f5)" \
     probe_f3_tightness.py out_probe_f3_tightness.txt

exit $rc
