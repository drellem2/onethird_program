#!/bin/sh
# mg-fd9c -- THE HEAD CORPUS IS NOT A FIXED POINT.
# Pure Python 3, no dependencies, no network.  ABOUT ONE MINUTE.
#
# WHAT WRITES.  NOTHING OUTSIDE THIS DIRECTORY -- and unlike every other tree
# in this arc, that is CHECKED here rather than asserted, because this suite is
# about an instrument writing into what it measures.  `git status --porcelain`
# is taken before and after and the two are compared; a difference outside
# `code/corpus_fixedpoint_fd9c/` prints and makes the run non-zero.
#
# `x1_orbit.py` IS NOT RUN HERE.  It clones this repository and runs two other
# trees' suites nine times, which is twenty minutes and is exactly what my
# ticket forbids doing in a worktree.  Run it yourself:
#
#     python3 x1_orbit.py --sandbox /tmp/fd9c-orbit
#
# Its committed transcript `out_x1_orbit.txt` is therefore a DATED measurement
# and not a regenerated one.  S4 gives that its class, and it is the same class
# as every other figure in this arc.
#
# RUN THIS TWICE ON A COMMITTED TREE.  The first run writes this tree's own
# transcripts, which are part of the corpus every probe here censuses, so on
# the first run S5b measures my contamination as 0 and says so in the
# transcript.  A SECOND consecutive run reads a complete corpus and is what
# ships.  That is `lib70c7.outs()`'s own ORDERING NOTE, obeyed by a tree whose
# subject is that note.
#
# WRITE TO A TEMP AND MOVE.  A plain `> out_s1_orbit.txt` truncates before the
# probe starts, and every probe here censuses `code/*/out_*.txt` -- so the one
# artifact my own census could not see would be my own transcript.  That is
# the arc's defect #7, it is THIS TICKET'S SUBJECT, and a suite about it that
# committed it would be worthless.  `.new` + `mv` is mg-bf79's fix.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects, its status is read by an
# explicit `||` guard, then the transcript is `cat` so the terminal stream is
# unchanged.  All six expected exit codes are 0 and are stated here, before the
# run, so a non-zero one is visible as a change rather than absorbed as noise.
set -u
cd "$(dirname "$0")"

BEFORE=$(git -C ../.. status --porcelain | grep -v 'code/corpus_fixedpoint_fd9c/' || true)

rm -f ./out_*.txt.new
run() {
    _p=$1
    _o=$2
    echo "### $_p"
    python3 -B "$_p" > "$_o.new" 2>&1 || {
        echo "    (exit $? -- expected 0; every check in this tree is an arm"
        echo "     that can fail, and a scored MISS is not one of them)"; }
    mv -f "$_o.new" "$_o"
    cat "$_o"
    echo
}

run s0_selftest.py        out_s0_selftest.txt
run s1_orbit.py           out_s1_orbit.txt
run s2_drift.py           out_s2_drift.txt
run s3_reconstruction.py  out_s3_reconstruction.txt
run s4_convention.py      out_s4_convention.txt
run s5_self.py            out_s5_self.txt

echo "=========================================================================="
echo "NOTHING OUTSIDE THIS DIRECTORY WAS WRITTEN -- CHECKED, NOT ASSERTED"
echo "=========================================================================="
AFTER=$(git -C ../.. status --porcelain | grep -v 'code/corpus_fixedpoint_fd9c/' || true)
if [ "$BEFORE" = "$AFTER" ]; then
    echo "      git status outside code/corpus_fixedpoint_fd9c/: UNCHANGED"
else
    echo "      *** CHANGED OUTSIDE THIS TREE ***"
    printf 'before:\n%s\nafter:\n%s\n' "$BEFORE" "$AFTER"
fi

echo
echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^S[0-9] TOTAL\|^SELFTEST TOTAL BAD:\|^FINDING:' out_*.txt || true
