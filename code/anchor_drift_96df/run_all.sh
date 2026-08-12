#!/bin/sh
# mg-96df -- THE ANCHOR-DRIFT ADJUDICATION, end to end.
#
# ORDER MATTERS.  a0 earns the match ladder on planted text before a1 is
# allowed to use it on the corpus; a2's controls read the notes a1's numbers
# went into, and one of its arms (X5) measures the transcripts a1 has just
# written, so it must run last.
#
# READ-ONLY IN THE CITED REPO.  Every content read is `git show <rev>:<path>`
# in ~/research/one_third_width_three (override with $ONETHIRD_WIDTH_THREE).
# Nothing here fetches, checks out, or writes there.
#
# ~3 seconds on this host.
set -u
cd "$(dirname "$0")"
STATUS=0
for s in a0_selftest a1_anchors a2_controls; do
    printf '\n===== %s =====\n' "$s"
    python3 "$s.py" > "out_$s.txt" 2>&1 || STATUS=1
    tail -3 "out_$s.txt"
done
exit $STATUS
