#!/bin/sh
# c0_repro.sh -- reproduce the TARGET's committed outputs against the REPAIRED
# code, on this audit's own copy, and diff byte for byte.
#
# mg-e8b8 claims: "`t2`, `t3` and `t4` are untouched and their outputs are
# byte-identical; mg-2060's `b0_repro.sh` regenerates all five and still
# reports 5 of 5 IDENTICAL, against the repaired code."  This script checks
# that claim without using mg-2060's script.
#
# Exit 0 iff all five committed outputs regenerate byte-identically.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/../branching_locate_db09"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

echo "=========================================================================="
echo "c0  REPRODUCTION of code/branching_locate_db09/ against its committed"
echo "    outputs, on a scratch copy"
echo "=========================================================================="
echo
cp -R "$SRC"/. "$WORK"/
( cd "$WORK" && sh ./run_all.sh > /dev/null 2>&1 )
RC=$?
echo "    run_all.sh exit code: $RC"
echo

BAD=0
N=0
for f in out_selftest.txt out_t1_tl.txt out_t2_gz.txt out_t3_ours.txt out_t4_quotes.txt; do
    N=$((N + 1))
    if diff -q "$SRC/$f" "$WORK/$f" > /dev/null 2>&1; then
        echo "      $f  IDENTICAL"
    else
        echo "      $f  DIFFERS"
        diff "$SRC/$f" "$WORK/$f" | head -8
        BAD=$((BAD + 1))
    fi
done
echo
echo "    identical: $((N - BAD)) of $N, population: the five committed out_*.txt"
echo "    files of code/branching_locate_db09/"
echo

echo "    the document's stated instrument facts, checked against the run:"
A=$(grep -c 'assert' "$WORK/out_selftest.txt" 2>/dev/null || true)
COUNT=$(grep -o '[0-9][0-9 ]*' "$WORK/out_selftest.txt" | tr -d ' ' | tail -1)
echo "      out_selftest.txt last number (the assertion count): $COUNT"
echo "      the document says 699 520"
if [ "$COUNT" = "699520" ]; then
    echo "      -> agrees"
else
    echo "      -> DISAGREES"
    BAD=$((BAD + 1))
fi
# The document says "four test scripts, all four `TOTAL BAD: 0`".  The
# self-test is NOT one of the four and does not print a TOTAL BAD line at all
# -- it prints "selftest: N assertions, all passed".  The first version of
# this check counted it as a fifth and reported 4 of 5; that was this script's
# error, not the document's, and the population is corrected here.
TB=0
TBOK=0
for f in out_t1_tl.txt out_t2_gz.txt out_t3_ours.txt out_t4_quotes.txt; do
    L=$(grep -c '^TOTAL BAD: 0$' "$WORK/$f" 2>/dev/null || true)
    TB=$((TB + 1))
    if [ "$L" -ge 1 ]; then TBOK=$((TBOK + 1)); fi
done
echo "      test-script outputs ending TOTAL BAD: 0 -- $TBOK of $TB, population:"
echo "      the four TEST-script outputs t1..t4 (the self-test is not one of the"
echo "      four and prints no TOTAL BAD line)"
if [ "$TBOK" -ne "$TB" ]; then BAD=$((BAD + 1)); fi
if grep -q 'all passed' "$WORK/out_selftest.txt"; then
    echo "      out_selftest.txt reports 'all passed'  -- yes"
else
    echo "      out_selftest.txt reports 'all passed'  -- NO"
    BAD=$((BAD + 1))
fi

echo
echo "--------------------------------------------------------------------------"
echo "FINDINGS: $BAD, population: the five output files plus the two stated facts"
echo "TOTAL BAD: $BAD"
[ "$BAD" -eq 0 ] || exit 1
exit 0
