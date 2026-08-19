#!/bin/sh
# mg-06d1 — THE ALIAS-INDEX AGREEMENT CHECK.  ~31 s, and it is on the merge gate.
#
# mg-0d1b's INDEX.md records 11 quantities aliased across up to 13 names in up to 11 trees
# with ZERO disagreements in 12 measured groups, and named the consequence: every row is a
# control the arc has already paid for and has never cashed.  This suite cashes them.
#
# ORDER IS LOAD-BEARING, AND IT IS NOT THE NUMBERING.  g2 runs FIRST although it is
# numbered second, because g1's twelve tolerances are all stated over POP-PRIM and
# POP-PRIM *is* the primitivity predicate g2 checks.  If ten trees stop agreeing about
# which posets are primitive, no tolerance in g1 is stated over a population anyone can
# name, and g1's twelve `agree` lines would be measurements over a set in dispute.  g2
# costs 0.2 s against g1's 30 s, so the validity check is also the cheap one.
#
# EVERY ARM RUNS AND THE WORST EXIT WINS — not `&&`, for build.sh's own stated reason: a
# gate that reveals its findings one per merge attempt is a gate people stop reading.
#
# NO `set -e` AND NO `|| true`, DELIBERATELY.  The first draft of this file wrote
# `python3 ... || true; RC=$?`, which captures the exit status of `true` and is therefore
# 0 forever: a FAIL-OPEN merge gate, in the suite whose whole subject is a control that
# cannot fire.  It is recorded in README §5 as defect D2 rather than quietly fixed.  The
# `if ...; then RC=0; else RC=$?; fi` form below is the one that actually captures it.
#
# Exit 0 = the aliases agree at mg-0d1b's measured tolerances AND every falsification arm
# was satisfactory.  1 = a control fired (a real disagreement — see the transcript, and
# file a ticket).  2 = refused/broken (the instrument could not answer).
#
# `mkbaseline.py` is NOT run here.  A gate that regenerates its own expectations on demand
# is laundering with extra steps (mg-724a); the baseline is a committed file and moving it
# is a human act with a diff and a reason.
#
# --- mg-479c ---------------------------------------------------------------------------
# g3 JOINS, AND IT JOINS AHEAD OF g1 FOR THE REASON THE PARAGRAPH ABOVE ALREADY GIVES.  g1
# now compares in the CANONICAL frame — every pinned column goes through the normalisation
# declared for its name — so if those declarations are self-contradictory, or a pinned name
# has none, g1's twelve `agree` lines are comparisons in a frame nobody can name.  g3 is the
# arm that asks, and it is a validity precondition exactly as g2 is.
#
# MEASURED BEFORE IT WAS CHOSEN, as §1 of the README requires: g3 is 0.03 s (it does no
# recompute at all — JSON and exact Fraction arithmetic) and g1's six added arms are 0.1 s,
# because they reuse the SAME captured matrix the W arms do.  This suite ran 31.0 s before
# the change and 30.2 s after it on the same host in the same session, so the addition is
# below this host's run-to-run variance; `./build.sh` measures 42.8 s and 44.5 s on two runs
# against the 44.8 s mg-06d1 recorded, and BOTH samples are quoted rather than the better
# one.  Nothing was dropped to pay for it and nothing was deferred.
#
# `mknorm.py` is NOT run here either, and it refuses to run at all once NORMALISATION.json
# exists.  Seeding the 71 identity declarations was a one-shot derivation from mg-0d1b's
# measured agreement; a script that re-derives them on demand would absorb the next name
# added to the record silently, which is the defect mg-479c exists to close.
cd "$(dirname "$0")" || exit 2
STATUS=0

for arm in g2_predicate g3_normalisation g1_values
do
    if python3 -u "$arm.py" > "out_$arm.txt" 2>&1; then
        RC=0
    else
        RC=$?
    fi
    if [ "$RC" -gt "$STATUS" ]; then STATUS=$RC; fi
    if [ "$RC" -ne 0 ]; then cat "out_$arm.txt"; fi
done

echo "g2 $(tail -2 out_g2_predicate.txt | head -1)"
echo "g3 $(tail -1 out_g3_normalisation.txt)"
echo "g1 $(tail -2 out_g1_values.txt | head -1)"
echo "alias-agreement worst exit: $STATUS   (0 green · 1 a control fired · 2 refused/broken)"
exit "$STATUS"
