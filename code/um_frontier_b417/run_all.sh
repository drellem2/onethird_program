#!/bin/sh
# mg-b417 -- THE u_M FRONTIER, and the fate of the DISJUNCTION.
#
# b0 must pass before any verdict is taken from libb417.  b1 is the headline and does
# NOT depend on the search: it certifies, on integers, that the DISJUNCTION is false at
# a poset that was already committed to this repository.  b2 is the search, b4 the
# exact stage that decides its champions, b3 the trend.
#
# ORDER MATTERS: b2 writes champions.json, which b3 and b4 both read.
#
# TIMING.  b0 sweeps n <= 7 exhaustively three times (the identity, the screen's
# direction, and W(7) against mg-c50b's exhaustive figure) and takes about 20 minutes.
# b2 is about 25 minutes.  b1 and b4 are a few minutes each.
set -e
cd "$(dirname "$0")"
fail=0
for s in b0_selftest b1_witness b2_climb b3_trend b4_certify; do
    printf '%-20s ' "$s"
    if python3 -u "$s.py" > "out_$s.txt" 2>&1; then
        echo "PASS"
    else
        echo "FAIL  (see out_$s.txt)"
        fail=1
    fi
done
if [ "$fail" -ne 0 ]; then
    echo
    echo "AT LEAST ONE STAGE FAILED -- this line is the verdict, and it is not CLEAN."
    exit 1
fi
echo
echo "ALL STAGES PASS"
