#!/bin/sh
# mg-aaf4 -- run every script of this audit, regenerate every transcript, and
# score each exit code against the value PREDICTIONS.md committed for it before
# the script existed.
#
# The predicted values are written here as literals so this file can be read
# against PREDICTIONS.md by eye, and they are NOT parsed out of that file: a
# runner that reads the prediction it is scored against can be made green by
# editing one document.  This is mg-d075's design and it is kept.
#
#   a1_population.py     1   (the parent's own deliverable holds unbounded sites)
#   a2_reproduce.py      0   (8/4/4, 9/4/5 and 10/10/0 all reproduce)
#   a3_criticism.py      1   (a criticism sentence carries no numeric scope --
#                             PREDICTED 1 on the first run AND 1 at the end, since
#                             this audit cannot edit the prose it audits)
#   a4_selfapply.py      1   (at least one charge fails self-application)
#   a5_donotdisturb.py   0   (the parent's suite re-runs green, transcripts unmoved)
#   selftest_aaf4.py     0   (every mutation caught, every mutation real)
#
# THIS RUNNER IS EXPECTED TO EXIT 1, AND THE REASON IS A RESULT.  `a5` was
# predicted 0 and returns 1: mg-d075's `out_s6_class.txt` does NOT regenerate
# byte-identical, because one figure in it counts commits across every ref in the
# repository.  PREDICTIONS.md P14 is refuted and is left exactly as written.  A
# runner made green by editing the prediction it missed would be worth nothing.
#
# An exit code alone is not evidence that a script ran -- a traceback also exits
# 1, and two scripts here are PREDICTED 1.  Every script must additionally have
# written at least one SUMMARY line.  That check is mg-d075's, found by mg-d075's
# own runner scoring a crash `ok`, and it is inherited here rather than re-earned.

set -u
HERE=$(cd "$(dirname "$0")" && pwd)
export PYTHONPATH="$HERE"
FAIL=0

run() {
    name=$1
    want=$2
    python3 "$HERE/$name.py" > "$HERE/out_$name.txt" 2>&1
    got=$?
    nsum=$(grep -c '^SUMMARY' "$HERE/out_$name.txt" 2>/dev/null || echo 0)
    if [ "$nsum" -lt 1 ]; then
        printf '  %-22s exit %d  predicted %d  NO SUMMARY -- DIED\n' \
               "$name" "$got" "$want"
        FAIL=$((FAIL + 1))
    elif [ "$got" -eq "$want" ]; then
        printf '  %-22s exit %d  predicted %d  SUMMARY lines %-2d  ok\n' \
               "$name" "$got" "$want" "$nsum"
    else
        printf '  %-22s exit %d  predicted %d  OFF PREDICTION\n' \
               "$name" "$got" "$want"
        FAIL=$((FAIL + 1))
    fi
}

echo "=============================================================================="
echo "mg-aaf4 run_all -- exit codes scored against PREDICTIONS.md (committed first)"
echo "=============================================================================="
run a1_population    1
run a2_reproduce     0
run a3_criticism     1
run a4_selfapply     1
run a5_donotdisturb  0
run selftest_aaf4    0
echo "=============================================================================="
echo "SUMMARY run_all: 6 scripts, $FAIL off prediction"
echo "SUMMARY run_all: a miss here is a REFUTED PREDICTION kept as written,"
echo "SUMMARY run_all: not a prediction rewritten to match the run."
echo "=============================================================================="
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)
