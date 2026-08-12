#!/bin/sh
# mg-ac0c — run every arm and write its transcript beside it.
#
# a0 FIRST and its exit code is the gate: if a control fired, nothing below it means anything.
# Total runtime is under 2 s — this instrument enumerates no posets (see README §1).

cd "$(dirname "$0")" || exit 2
STATUS=0

echo "=== a0_selftest (controls; a red here voids everything below) ==="
python3 a0_selftest.py > out_a0_selftest.txt 2>&1
RC=$?
tail -3 out_a0_selftest.txt
[ "$RC" -gt "$STATUS" ] && STATUS=$RC
if [ "$RC" -ne 0 ]; then
    echo "a0 RED — refusing to run the rest; see out_a0_selftest.txt"
    exit "$STATUS"
fi

for arm in a1_enumeration a2_closure a3_novelty; do
    echo "=== $arm ==="
    python3 "$arm.py" > "out_$arm.txt" 2>&1
    RC=$?
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
    [ "$RC" -ne 0 ] && echo "  $arm exited $RC — see out_$arm.txt"
done

echo
echo "worst exit: $STATUS"
exit "$STATUS"
