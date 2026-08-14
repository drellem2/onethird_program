#!/bin/sh
# mg-7c32 — the four arms behind docs/OneThird-CyclicBias-mg-7c32.md.  Standard
# library only, ~75 s measured on this host (c0 0.4s, c1 27s, c2 22s, c3 26s).
#
#   c0  the planted defects: every check here, run against a broken library
#   c1  step 1 — db IS the cyclic-orientation bias, by two routes that share no line
#   c2  step 3 — the telescope, at every base point and under two bracketings
#   c3  step 2 exhaustive, and what the average cyclic bias reduces to
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit
# status, so a red arm would be invisible to `set -e` and this script would be green
# forever (mg-06d1's D2).  Each arm writes its own transcript and the status is read
# from the arm, not from the plumbing.
#
# c0 RUNS FIRST ON PURPOSE.  It is the only arm that can distinguish "the checks pass"
# from "the checks cannot fail", and it costs 0.4 s of the 75.
d=$(cd "$(dirname "$0")" && pwd)
STATUS=0
for arm in c0_selftest c1_identity c2_telescope c3_bound
do
    ( cd "$d" && python3 "$arm.py" ) > "$d/out_$arm.txt" 2>&1
    RC=$?
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-7c32 cyclic-bias suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
