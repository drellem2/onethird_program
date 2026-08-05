#!/bin/sh
# mg-fcb2: regenerate every transcript of this audit.
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured
# runtime 2026-08-05 on a 2024 laptop, on the tree that ships this comment:
# about 6 minutes, of which a2_dichotomy.py is roughly half (297 exact integer
# characteristic polynomials, the largest at |L(P)| = 120) and a4_hedges.py
# regenerates controls_output.txt four times for the deletion test.  There is NO
# CI in this repository; this runner is hand-invoked like every other one here.
#
# NOT `python3 x.py | tee out.txt`: a pipeline's exit status in POSIX sh is the
# LAST command's, so `tee` succeeding would mask a verifier exiting 1 -- a
# committed transcript printing REFUTED under a runner that exited 0.  Each step
# redirects and has its status captured and folded into WORST.
#
# `set -e` is deliberately NOT used: three of these scripts are PREDICTED to
# exit 1, because they carry refutations, and aborting on the first would leave
# the later transcripts unregenerated.  The exit status is accumulated instead
# and re-raised at the bottom, which is the whole failure protocol.
cd "$(dirname "$0")"

WORST=0
run() {
    printf '== %s ==\n' "$1"
    python3 "$1" > "$2" 2>&1
    st=$?
    cat "$2"
    printf '   -> %s exit %d (predicted %d)\n\n' "$1" "$st" "$3"
    if [ "$st" -gt "$WORST" ]; then WORST=$st; fi
}

# The instruments are checked BEFORE they are pointed at anything.  If this
# step fails, nothing below it means anything.
run selftest_fcb2.py        out_selftest_fcb2.txt        0
if [ "$WORST" -ne 0 ]; then
    echo "selftest_fcb2.py FAILED -- the instruments below are unchecked, stopping"
    exit "$WORST"
fi

run a1_counts.py            out_a1_counts.txt            1
run a2_dichotomy.py         out_a2_dichotomy.txt         0
run a3_standard_elsewhere.py out_a3_standard_elsewhere.txt 1
run a4_hedges.py            out_a4_hedges.txt            0
run a5_standing.py          out_a5_standing.txt          0
run a6_control_at_commit.py out_a6_control_at_commit.txt 0

echo "worst exit status: $WORST (predicted 1 -- a1 and a3 carry refutations)"
exit "$WORST"
