#!/bin/sh
# mg-30bd — the two things in this directory that ARE a fixed point.  Standard library only.
#   selftest_30bd  19 planted worlds bounding the classifier: five that must come out BENIGN
#   report         the count, read off the frozen sweep record.  Pure function of that file.
#
# WHAT IS *NOT* HERE IS `sweep.py`, AND THAT IS THE WHOLE SHAPE OF THIS DIRECTORY.  The sweep
# re-runs 192 suites in isolated clones, takes hours, executes instrument code across the
# whole corpus, and ITS ANSWER MOVES AS THE CORPUS MOVES — that motion is the property being
# measured, so it cannot also be an invariant.  Putting it in a runner would make this
# directory a member of the population it counts, on its first re-run.  `out_sweep_30bd.txt`
# and `sweep_30bd.jsonl` are ONE DATED RUN, exactly as mg-20ee's `out_ground_truth.txt` is,
# and `report.py` is deterministic given them.  Re-take the measurement with:
#
#     python3 -B sweep.py --workers 6 --timeout 900 --pass2
#
# THIS SUITE IS NOT IN `build.sh` AND MUST NOT BE ADDED WITHOUT ONE THING CHANGING FIRST.
# It reports a POPULATION OF FINDINGS, and a finding is not a gate: a runner that exited 1
# on a non-empty list would ask the next branch to repair every entry to get green, which is
# mg-e35b's red-on-improvement shape.  `report.py` therefore exits 0 with findings and 2 only
# when it has no record to read.  If a successor ever wants this in the gate, the thing to
# gate is "the list has not GROWN", and that needs a committed baseline this ticket does not
# have the standing to declare — mg-30bd is tagged `declares-remainder` and this is one of
# the things it declares.
#
# NO PIPELINE ON THE STATUS PATH (mg-c2b3): `python3 x.py | tee out.txt` returns TEE's exit
# status, so a red arm would be invisible.  Each arm redirects and its status is read
# directly.  The write is via `.partial` + `mv` for mg-f771's reason: a plain redirect
# truncates the target before python starts, and a tracked out_*.txt observed mid-truncation
# is a defect this estate has already paid for twice.
d=$(cd "$(dirname "$0")" && pwd)
TMPS=""
trap 'rm -f $TMPS' EXIT INT TERM HUP
STATUS=0
for arm in selftest_30bd:out_selftest_30bd report:out_verdict_staleness
do
    script=${arm%%:*}
    out=${arm##*:}
    tmp="$d/.$out.txt.partial"
    TMPS="$TMPS $tmp"
    python3 -B "$d/$script.py" > "$tmp"
    RC=$?
    mv "$tmp" "$d/$out.txt"
    cat "$d/$out.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-30bd verdict-staleness suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
