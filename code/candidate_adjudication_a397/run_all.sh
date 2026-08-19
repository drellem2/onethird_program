#!/bin/sh
# mg-a397 — the adjudication, in the ticket's order: tee sites, then the directories with no
# falsification attempt, then the membership candidates.
#
# THERE IS NO `| tee` IN THIS FILE AND THAT IS NOT A STYLE CHOICE.  This directory's first arm
# exists because `cmd | tee f` makes `$?` TEE's status, and tee succeeds whatever it is fed.
# A runner that laundered its own arms' exit codes inside the suite that measures laundered
# exit codes would be the fourth instance of the thing mg-9876 is about.  Each arm redirects,
# and its status is read on the very next line.
#
# NOR IS THERE `|| true`.  mg-06d1's D2 — inside the suite whose subject is a control that
# cannot fire — wrote `cmd || true; RC=$?`, which captures the exit of `true` and is therefore
# 0 forever: a fail-open gate.  `set -e` is deliberately NOT set, because every arm must run
# even when an earlier one is red, and the WORST exit wins rather than the last.
#
# EXIT 0 nothing found · 1 an arm reported a finding · 2 an arm refused (a control of its own
# did not answer, or the tree was left dirty).  2 beats 1 beats 0, because a suite that cannot
# vouch for itself has not made a finding.
#
# a2 IS SLOW ON PURPOSE: it runs four real suites twice each under a 900 s budget.  Its cost
# is measured in the README and is why this directory is NOT wired into build.sh.

here=$(cd "$(dirname "$0")" && pwd)
cd "$here" || exit 2
STATUS=0

for arm in a1_index a2_tee a3_bare a4_membership a5_selftest
do
    printf '\n############################################################ %s\n' "$arm"
    python3 "$here/$arm.py" > "$here/out_$arm.txt" 2>&1
    RC=$?
    tail -n 12 "$here/out_$arm.txt"
    printf '%s exit %s\n' "$arm" "$RC"
    if [ "$RC" -gt "$STATUS" ]; then STATUS=$RC; fi
done

printf '\n############################################################ mg-a397\n'
printf 'worst arm exit: %s   (0 nothing found · 1 a finding · 2 an arm refused)\n' "$STATUS"
exit "$STATUS"
