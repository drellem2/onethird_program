#!/bin/sh
# mg-19ec -- independent audit of the mg-dffa warrant narrowing (645b5a4).
# Pure Python 3, no dependencies.  About 25 seconds.  e3 needs network.
#
# THE EXIT CONTRACT, AND WHY IT IS THIS ONE.
#
# This runner is NOT green when every probe exits 0.  It is green when every
# probe's exit code equals the code PREDICTED FOR IT in PREDICTIONS.md, which
# was committed before any probe here ran (170094f).  Three of the eight are
# predicted to exit 1: they carry findings, and a runner that went red on them
# would be reporting the findings as breakage.  A probe predicted to fire and
# then not firing is equally a miss, and this runner reports that too -- which
# a plain `set -e` cannot do in either direction.
#
# The audited instrument's own runner is green with F4's premise unread,
# because its network probe returns 0 when it cannot reach arXiv (see E7a).
# So here e3_f4_brown.py returns 2 when it cannot reach arXiv, that 2 is not
# the prediction, and this runner goes RED on a probe that verified nothing.
set -u
cd "$(dirname "$0")"

MISSES=0

expect() {                       # expect <predicted-exit> <script>
    want="$1"; shift
    out="out_$(basename "$1" .py).txt"
    python3 "$1" > "$out"
    got=$?
    if [ "$got" -eq "$want" ]; then
        printf '  %-22s predicted %s  got %s  ok\n' "$1" "$want" "$got"
    else
        printf '  %-22s predicted %s  got %s  MISS\n' "$1" "$want" "$got"
        MISSES=$((MISSES + 1))
    fi
}

echo "mg-19ec: exit code against the prediction committed before the run"
expect 0 selftest19ec.py
expect 0 e1_f1_cells.py
expect 1 e2_f2_clauses.py
expect 0 e3_f4_brown.py
expect 0 e4_f3_control.py
expect 1 e5_population.py
expect 0 e6_standing.py
expect 1 e7_instrument.py

echo
echo "Headline lines:"
grep -h '^SUMMARY\|^SELF-TEST:' out_*.txt || true
echo
if [ "$MISSES" -eq 0 ]; then
    echo "PREDICTIONS: 8 of 8 matched."
else
    echo "PREDICTIONS: $MISSES MISSED.  The misses are the result, not an error."
fi
exit "$MISSES"
