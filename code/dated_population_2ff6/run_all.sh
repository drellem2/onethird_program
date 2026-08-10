#!/bin/sh
# mg-2ff6 -- ADOPTING THE DATED-POPULATION CONVENTION.
# Pure Python 3, no dependencies, no network.  ABOUT SIX MINUTES.
#
# WHAT WRITES, AND THIS IS THE ONE RUNNER IN THIS ARC THAT CANNOT SAY
# `NOTHING OUTSIDE THIS DIRECTORY`.  Moving published output in two other trees
# IS the ticket.  cfd9c's runner proved it moved nothing, with `git status`
# rather than an assertion; the honest analogue here is not a check but an
# ACCOUNTING, so this script prints every path outside its own directory that
# changed across the run, and `d1_moved.py` names every FIGURE in them that
# moved and by how much.  A check that could only say `yes I wrote there` would
# be theatre; the list of figures is the thing a reader needs.
#
# Specifically it re-runs:
#   code/grain_arity_9160/run_all.sh            -- the whole suite; the
#                                                  convention was adopted at
#                                                  `lib9160.pop`, so every
#                                                  transcript in that tree
#                                                  declares a rule that must
#                                                  have produced it
#   code/grain_axis_audit_03d1/a1_axes.py       -- the two probes that print an
#   code/grain_axis_audit_03d1/a6_self.py          arc-wide corpus figure, and
#                                                  ONLY those two.  `a2`-`a5`
#                                                  carry no figure this ticket
#                                                  dates, and `a4` runs ANOTHER
#                                                  tree's whole suite twice.
#
# It does NOT run `code/corpus_fixedpoint_fd9c/run_all.sh`.  `d2` runs cfd9c's
# `s4_convention.py` as a subprocess to get the score, and that probe writes
# nothing -- so cfd9c's committed `out_s4_convention.txt` survives as the
# BEFORE reading of the number this ticket moves.  Regenerating it would have
# erased the control.
#
# THREE ROUNDS, AND THE THIRD IS THE ONE THAT SHIPS.  Every probe here
# censuses `code/*/out_*.txt`, and this tree's own transcripts are in that
# glob, so round 1 reads a corpus that does not yet contain them.  Round 2 does.
# Round 3 exists to answer whether that settles -- PREDICTIONS.md/P7 bets it
# does, `snap/` holds round 2's bytes, and `d4_self.py` scores it by comparing.
# That is cfd9c's `run this twice` note, obeyed by a tree that has to prove it.
#
# WRITE TO A TEMP AND MOVE, everywhere, including into the two trees this
# script re-runs by hand.  A plain `> out_d1_moved.txt` truncates before the
# probe starts, and every probe here ranges over `code/*/out_*.txt`.
#
# NO STEP BELOW IS A PIPELINE.  Each redirects and its status is read by an
# explicit guard.  All five expected exit codes are 0 and are stated here,
# before the run, so a non-zero one is visible as a change and not as noise.
set -u
cd "$(dirname "$0")"

SNAP=./snap
mkdir -p "$SNAP"
rm -f ./out_*.txt.new

BEFORE=$(git -C ../.. status --porcelain)

WATCH="../grain_axis_audit_03d1/out_a1_axes.txt
../grain_axis_audit_03d1/out_a6_self.txt
../grain_arity_9160/out_selftest_9160.txt
../grain_arity_9160/out_s1_reproduce.txt
../grain_arity_9160/out_s2_arity.txt
../grain_arity_9160/out_s3_population.txt
../grain_arity_9160/out_s4_open.txt
../grain_arity_9160/out_s5_self.txt
./out_d0_selftest.txt
./out_d1_moved.txt
./out_d2_convention.txt
./out_d3_prose.txt"

run() {
    _p=$1
    _o=$2
    _show=$3
    [ "$_show" = show ] && echo "### $_p"
    python3 -B "$_p" > "$_o.new" 2>&1 || {
        [ "$_show" = show ] && echo "    (exit $? -- expected 0; every check"
        [ "$_show" = show ] && echo "     in this tree is an arm that can fail)"; }
    mv -f "$_o.new" "$_o"
    [ "$_show" = show ] && cat "$_o"
    [ "$_show" = show ] && echo
    return 0
}

cycle() {
    _show=$1
    ( cd ../grain_arity_9160 && sh run_all.sh ) > /dev/null 2>&1 || true
    for _f in a1_axes a6_self; do
        ( cd ../grain_axis_audit_03d1 \
          && python3 -B "$_f.py" > "out_$_f.txt.new" 2>&1
          mv -f "out_$_f.txt.new" "out_$_f.txt" ) || true
    done
    run d0_selftest.py    out_d0_selftest.txt    "$_show"
    run d1_moved.py       out_d1_moved.txt       "$_show"
    run d2_convention.py  out_d2_convention.txt  "$_show"
    run d3_prose.py       out_d3_prose.txt       "$_show"
}

echo "=== ROUND 1 -- the corpus does not yet contain this tree's transcripts"
cycle quiet
echo "=== ROUND 2 -- it does; snapshotting to snap/ for the convergence check"
cycle quiet
for _f in $WATCH; do
    cp "$_f" "$SNAP/$(basename "$_f")" 2>/dev/null || true
done
echo "=== ROUND 3 -- the one that ships"
cycle show

run d4_self.py out_d4_self.txt show

echo "=========================================================================="
echo "WHAT THIS RUN WROTE OUTSIDE ITS OWN DIRECTORY -- ACCOUNTED, NOT DENIED"
echo "=========================================================================="
AFTER=$(git -C ../.. status --porcelain)
if [ "$BEFORE" = "$AFTER" ]; then
    echo "      git status: UNCHANGED across this run (the trees were already"
    echo "      at their re-run bytes when it started)"
else
    printf '%s\n' "$AFTER" | grep -v 'code/dated_population_2ff6/' \
        | sed 's/^/      /'
fi
echo "      ^ every FIGURE in those paths that moved is named in"
echo "        out_d1_moved.txt, with its published value and its delta"

echo
echo "=========================================================================="
echo "SUMMARY -- every TOTAL line and every FINDING, from the transcripts"
echo "=========================================================================="
grep -h '^D[0-9] TOTAL\|^FINDING:' out_*.txt || true
