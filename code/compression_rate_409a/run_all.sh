#!/bin/bash
# mg-409a -- COMPRESSION W4: pin the rate.
# r0 is a GATE: if it fails, nothing downstream is entitled to be read, so the run stops.
set -u
cd "$(dirname "$0")"

RC=0
echo "### r0_selftest.py  (GATE)"
if ! python3 r0_selftest.py > out_r0_selftest.txt 2>&1; then
    tail -20 out_r0_selftest.txt
    echo "!!! r0 FAILED -- r1..r6 not run"
    exit 1
fi
tail -4 out_r0_selftest.txt

for arm in r1_ceiling r2_bar r3_rate r4_quantifier r5_pairbias r6_twoprojection; do
    echo "### ${arm}.py"
    if python3 "${arm}.py" > "out_${arm}.txt" 2>&1; then
        tail -3 "out_${arm}.txt"
    else
        tail -20 "out_${arm}.txt"
        echo "!!! ${arm} reported a failure"
        RC=1
    fi
done

echo
echo "measured wall time is printed by the caller; see README for the population sizes."
exit $RC
