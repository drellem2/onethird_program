#!/bin/sh
# mg-8af0: regenerate this repair's transcripts.  Four of them since mg-36f5.
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured
# runtime 2026-08-05 on a 2024 laptop, on the tree that ships this comment:
# ~21 s total -- demo_f2 ~12 s (it regenerates controls_output.txt several times
# over inside a temporary directory, which is the point of it), probe_f1 ~0.4 s,
# probe_f3 ~8.3 s at n <= 6.  mg-36f5 adds probe_f3_tightness, measured 4.9 s on
# 2026-08-13 on the tree that ships THIS comment, so ~26 s total.  There is NO CI
# in this repository -- this runner is hand-invoked, like every other run_all.sh
# here.
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

step "F2: can the V6 row go red?  five constructions, old row and new" \
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
