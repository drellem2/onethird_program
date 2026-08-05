#!/bin/sh
# run_all.sh -- the mg-6e58 suite.
#
# The exit convention is mg-b2af's, which took it from mg-e34a: every script
# exits 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  A non-zero exit means THAT
# SCRIPT HAS SOMETHING TO REPORT, never that it is broken.
#
# Three scripts are EXPECTED to exit 1, and PREDICTIONS.md says so in advance:
#   p2 -- the denominator is wrong at this tree, which is the finding
#   p3 -- the STILL-OPEN sentence is in another ticket's document
#   p4 -- the OLDEST gate cannot fire, and this branch does not edit it
#
# NO `set -e`.  A suite that stopped at the first non-zero exit would run p1
# and nothing else, and those exits are results rather than failures.
#
# `p1` and the closure half of `selftest` READ `man git-log` on this machine.
# On a host with no git man pages they RAISE rather than fall back to a
# remembered list -- see lib6e58.man_text().  That is deliberate: this ticket
# exists because a population was narrower than its label, and a silent
# fallback is exactly that.

cd "$(dirname "$0")" || exit 2

worst=0
for s in selftest_6e58 p1_ways p2_population p3_unrestricted p4_gate; do
    printf '===> %s\n' "$s"
    python3 "$s.py" > "out_$s.txt" 2>&1
    rc=$?
    printf '     exit %d   %s\n' "$rc" \
        "$(grep '^TOTAL BAD:' "out_$s.txt" 2>/dev/null | tail -1)"
    [ "$rc" -gt "$worst" ] && worst=$rc
done

printf 'worst exit: %d\n' "$worst"
exit "$worst"
