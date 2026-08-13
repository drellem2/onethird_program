#!/bin/sh
# mg-502f — THE SELF-RED SWEEP.  0.4 s, standard library only, no network.
#
#   s0_controls.py  27 planted worlds — the mechanism, the detector, the guard
#   s1_sweep.py     the estate, swept: which tracked scripts run the gate into its own input
#
# ORDER IS LOAD-BEARING AND IT IS NOT THE NUMBERING THIS TIME EITHER.  s0 is first because
# s1's GREEN is worth exactly the demonstration that its rules can produce a RED, and
# because s0's §M is the only thing here that establishes the mechanism is real rather than
# remembered — it hands mg-f771's own `verdict_for` the real committed bytes of a real
# transcript against the empty and half-written states a shell redirect leaves it in.
#
# THE WRITE IS A `mv` AND THAT IS THIS SUITE'S OWN SUBJECT, NOT TIDINESS.  `python3
# s1_sweep.py > out_s1_sweep.txt` would truncate a tracked `code/**/out_*.txt` for the
# duration of the run — the precondition this suite exists to enumerate, committed inside
# the enumerator.  This suite does not run `./build.sh`, so the truncation would not redden
# anything by itself; it would still be the shape, in the file written to find the shape.
# mg-f771's own runner reached this line first and for the same reason, and mg-ec63 and
# mg-bf79 reached it earlier still from two other directions.  `.tmp` + `mv` is their fix.
#
# STDOUT ONLY, NO `2>&1`.  s1's population counts — how many tracked files, how many .py —
# are on stderr on purpose: this instrument reads every tracked script in the estate, so a
# tracked transcript recording "1164 python files" would move on any branch that adds a
# file, and mg-f771's control would grade that a disagreement.  That is f771's own D4, and
# folding stderr in here would re-earn it.  Nothing is lost: both arms catch their own
# exceptions and print the traceback to STDOUT, so a crash is still in the transcript.
#
# NO PIPE.  `python3 x.py | tee out.txt` returns TEE's status — mg-9bc2, mg-9876, mg-06d1's
# D2 — and this suite would then be green forever.
#
# EVERY ARM RUNS AND THE WORST EXIT WINS, for build.sh's own stated reason: a gate that
# reveals its findings one per merge attempt is a gate people stop reading.
#
# Exit 0 = no tracked script runs `./build.sh` into a file the gate reads, and every planted
# world scored as required.  1 = an arm fired.  2 = refused/broken.
set -u
d=$(cd "$(dirname "$0")" && pwd)
TMPS=""
trap 'rm -f $TMPS' EXIT INT TERM HUP
STATUS=0
for arm in s0_controls s1_sweep
do
    tmp="$d/.out_$arm.txt.partial"
    TMPS="$TMPS $tmp"
    python3 -u "$d/$arm.py" > "$tmp"
    RC=$?
    mv "$tmp" "$d/out_$arm.txt"
    cat "$d/out_$arm.txt"

    VERDICT_LINE=$(grep -m1 '^VERDICT: ' "$d/out_$arm.txt" || true)
    if [ -z "$VERDICT_LINE" ]; then
        echo
        echo "BROKEN — $arm.py exited $RC WITHOUT printing a VERDICT line.  It did not reach"
        echo "a decision, so this is neither green nor red and MUST NOT be read as either."
        echo "Read $d/out_$arm.txt: a traceback and a finding are the same exit code."
        STATUS=2
        continue
    fi
    case "$RC" in
        0|1|2) ;;
        *)
            echo
            echo "BROKEN — $arm.py exited $RC, which is not one of its three verdicts."
            RC=2
            ;;
    esac
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-502f self-red sweep: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
