#!/bin/sh
# mg-d3f3: regenerate this audit's transcripts.
#
# Pure Python 3, no third-party packages.  Measured 2026-08-13 on a 2024 laptop,
# on the tree that ships this comment: a0 13.9 s, a1 86.5 s, a2 39.6 s,
# a3 46.3 s, a4 1.0 s, a5 4.3 s -- 192 s in total.  a1 and a2 are the cost of
# running `verify_e35b.py` and `controls.py` over a dozen mutated copies of the
# tree, which is the whole method: no verdict here is re-implemented, every one
# is read out of the repository's own scorer.
#
# THERE IS NO CI IN THIS REPOSITORY and this runner is hand-invoked.  It is
# deliberately NOT added to build.sh: an audit's transcripts are a record of what
# was true at the commit that took them, and a gate that regenerates them would
# make them a status board instead -- which is the reasoning mg-8af0 gave for
# leaving mg-fcb2's `[REFUTED]` A1.4a alone, and it applies to this audit too.
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so `tee` succeeding would mask a step exiting 1 (mg-f922,
# mg-c2b3).  Each step redirects and its status is read by an explicit guard.
#
# EVERY STEP RUNS AND THE FIRST NON-ZERO STATUS IS RE-RAISED, so a later pass
# cannot overwrite an earlier refutation.
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

step "a0: the harness, controlled before the audit uses it" \
     a0_selftest.py out_a0_selftest.txt
echo
step "a1: F1 put back, and the whole candidate space asked whether it noticed" \
     a1_f1_revert.py out_a1_f1_revert.txt
echo
step "a2: the V6b row name against the V6b measurement" \
     a2_census_scope.py out_a2_census_scope.txt
echo
step "a3: the declared limit against the measured one" \
     a3_disclosure.py out_a3_disclosure.txt
echo
step "a4: order on main, and the eight declared omissions" \
     a4_order_and_scope.py out_a4_order_and_scope.txt
echo
step "a5: E10's fourth row, built and scored" \
     a5_e10_row4.py out_a5_e10_row4.txt

exit $rc
