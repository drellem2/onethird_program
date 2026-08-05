#!/bin/sh
# mg-d075 -- run every script of this repair, regenerate every transcript, and
# exit 0 ONLY IF each script's exit code equals the value PREDICTIONS.md committed
# for it before the script existed.  A suite that is green because it forgot what
# it predicted is not evidence of anything.
#
# The predicted values are written here as literals so this file can be read
# against PREDICTIONS.md by eye, and they are NOT read out of that file: a runner
# that parses the prediction it is being scored against can be made green by
# editing one document.
#
#   s1_census.py         1   (EIGHT IS NOT THE POPULATION -- exits 1 when B != 8)
#   s2_reproduce.py      0   (the parent's 8/4/4 reproduces exactly)
#   s3_bound.py          0   (0 unbounded, no site lost, no figure lost)
#   s4_hedge.py          0   (no new phrasing hedges without enumerating)
#   s5_own_criticism.py  0   (FINAL value; PREDICTED 1 on the first run, and the
#                             first run's transcript is committed beside this
#                             file as out_s5_own_criticism_FIRSTRUN_exit1.txt)
#   s6_class.py          0   (reports; does not gate)
#   selftest_d075.py     0   (every mutation caught, every mutation real)
#
# Run from anywhere.  Do not `cd` into this directory on this machine -- a
# directory-entry hook blocks; the scripts are invoked by absolute path instead.

set -u
HERE=$(cd "$(dirname "$0")" && pwd)
export PYTHONPATH="$HERE"
FAIL=0

run() {
    name=$1
    want=$2
    python3 "$HERE/$name.py" > "$HERE/out_$name.txt" 2>&1
    got=$?
    # AN EXIT CODE ALONE IS NOT ENOUGH.  A script that dies on a traceback exits
    # 1, and s1_census is PREDICTED 1 -- so for one run of this suite a crash was
    # scored "ok".  Every script must also have written at least one SUMMARY line
    # to its transcript: a crash cannot fake that, because the SUMMARY lines are
    # the last thing each script prints.
    nsum=$(grep -c '^SUMMARY' "$HERE/out_$name.txt" 2>/dev/null || echo 0)
    if [ "$got" -eq "$want" ] && [ "$nsum" -ge 1 ]; then
        printf '  %-22s exit %d  predicted %d  SUMMARY lines %-2d  ok\n' \
               "$name" "$got" "$want" "$nsum"
    elif [ "$nsum" -lt 1 ]; then
        printf '  %-22s exit %d  predicted %d  NO SUMMARY -- DIED\n' \
               "$name" "$got" "$want"
        FAIL=$((FAIL + 1))
    else
        printf '  %-22s exit %d  predicted %d  OFF PREDICTION\n' "$name" "$got" "$want"
        FAIL=$((FAIL + 1))
    fi
}

echo "=============================================================================="
echo "mg-d075 run_all -- exit codes scored against PREDICTIONS.md (committed first)"
echo "=============================================================================="
run s1_census        1
run s2_reproduce     0
run s3_bound         0
run s4_hedge         0
run s5_own_criticism 0
run s6_class         0
run selftest_d075    0
echo "=============================================================================="
echo "SUMMARY run_all: 7 scripts, $FAIL off prediction"
echo "=============================================================================="
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)
