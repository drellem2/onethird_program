#!/bin/sh
# mg-f771 — the two arms behind the gate's own fixed point.  Standard library only.
#   g0  after a gate run, does any COMMITTED transcript disagree with this tree?
#   g1  planted worlds — six the normaliser must catch, three it must not, two refusals
#
# g0 REFUSES unless BUILD_SH_RAN_THE_SUITES=1, because its subject is the side effect of a
# gate run and a green without one would mean only "nobody hand-edited these".  `build.sh`
# sets it; set it by hand if you have just run the suites yourself.  g1 needs no handshake
# -- its worlds are hand-authored pairs and a sandbox.
#
# NO PIPELINE ON THE STATUS PATH.  `python3 x.py | tee out.txt` returns TEE's exit status, so
# a red arm would be invisible and this script would be green forever -- mg-06d1's D2, a
# fail-open merge gate.  Each arm writes its transcript and the status is read from the arm.
#
# THE WRITE IS ATOMIC, AND THAT IS NOT TIDINESS -- IT IS THIS SUITE'S OWN SUBJECT.  Every
# other suite in the gate writes `python3 arm.py > out_arm.txt`, and the shell TRUNCATES the
# target before python starts.  This suite's arms are inside their own watched class, so
# with a plain redirect g0 would open its own transcript, find it EMPTY, and grade the
# committed copy as disagreeing with the tree -- on every run, forever, in the file written
# to detect exactly that.  Measured, not anticipated: it is why this line is a `mv`.
d=$(cd "$(dirname "$0")" && pwd)
TMPS=""
trap 'rm -f $TMPS' EXIT INT TERM HUP
STATUS=0
for arm in g0_fixed_point g1_controls
do
    tmp="$d/.out_$arm.txt.partial"
    TMPS="$TMPS $tmp"
    # STDOUT ONLY.  `2>&1` is what every other suite writes and it is WRONG HERE: g0 uses
    # stderr as its jitter channel -- how many transcripts moved and which were graded NOISE
    # is a function of wall-clock rounding, not of repo state, and folding it into the
    # tracked transcript made this arm grade its own committed copy DISAGREES on run 2
    # (README D4).  Nothing is lost from the record: both arms catch their own exceptions and
    # print the traceback to STDOUT, so a crash is still in the transcript.
    python3 "$d/$arm.py" > "$tmp"
    RC=$?
    mv "$tmp" "$d/out_$arm.txt"
    cat "$d/out_$arm.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "mg-f771 gate-fixed-point suite: worst arm exit $STATUS   (0 green · 1 fired · 2 refused)"
exit "$STATUS"
