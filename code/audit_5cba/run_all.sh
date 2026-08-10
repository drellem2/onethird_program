#!/bin/sh
# mg-5cba -- INDEPENDENT AUDIT of mg-789d's refutation of (L*).
#
# a0 must pass before any verdict is taken from lib5cba.  a1 is the audit's core:
# it re-certifies mg-789d's counterexamples in exact rationals on an instrument that
# never opened lib789d.py.  a2..a6 are the rest of the ticket.
#
# TIMING: a3 and a4 are exhaustive over the 86278 primitive posets at n = 7 and take
# about 15 minutes each.  a1, a5, a6 are fast.
set -e
cd "$(dirname "$0")"
fail=0
for s in a0_selftest a1_witness a2_logic a3_corollaries a4_theoremA a5_scope a6_conditionals; do
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
