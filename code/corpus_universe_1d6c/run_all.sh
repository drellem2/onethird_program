#!/bin/sh
# mg-1d6c -- the whole suite.  ~30 s, no network, no dependencies.
#
# THIS RUNNER EXITS 1 AND IS SUPPOSED TO.  Four of its six steps are PREDICTED 1
# in PREDICTIONS.md: they exit 1 because the thing they check is true -- the glob's
# universe differs from its description, the published figure understates the
# population, published figures inherit it, and the repaired self-check bites.  A
# runner made green by weakening a check that fires is the defect this arc exists
# to catch.
#
# TRANSCRIPTS ARE WRITTEN TO A TEMPORARY FILE AND MOVED INTO PLACE ONLY WHEN THE
# STEP HAS EXITED (mg-ec63's finding: `> out_x.txt` truncates the transcript before
# the probe runs, so a killed probe leaves a zero-byte file that reads as a pass).

set -u
cd "$(dirname "$0")" || exit 2

RC=0
run() {
    name="$1"; expected="$2"
    printf '%-24s ' "$name"
    if python3 "$name" > ".out_$name.tmp" 2>&1; then rc=0; else rc=$?; fi
    mv ".out_$name.tmp" "out_$(basename "$name" .py).txt"
    if [ "$rc" -eq "$expected" ]; then
        printf 'exit %d  (predicted %d)  OK\n' "$rc" "$expected"
    else
        printf 'exit %d  (predicted %d)  *** OFF PREDICTION ***\n' "$rc" "$expected"
        RC=1
    fi
    [ "$rc" -ne 0 ] && RC=1
    return 0
}

echo "=========================================================================="
echo "mg-1d6c  THE CORPUS UNIVERSE, THE CONSUMERS, AND THE DECLARED EXCLUSION"
echo "=========================================================================="
run selftest1d6c.py   0
run p1_glob.py        1
run p2_population.py  1
run p3_consumers.py   1
run p4_selfcheck.py   1
run p5_declaration.py 0
echo "=========================================================================="
echo "run_all exit $RC  (predicted 1 -- four steps are predicted 1 and are"
echo "supposed to be; see PREDICTIONS.md section 2)"
echo "=========================================================================="
exit $RC
