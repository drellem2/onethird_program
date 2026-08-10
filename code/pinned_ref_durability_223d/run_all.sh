#!/bin/sh
# mg-223d -- THE DURABILITY OF THE ARC'S PINNED REFS.
# Pure Python 3, no dependencies, no network reads except one `git ls-remote`.
# ABOUT TWO MINUTES.
#
# WHAT WRITES.  NOTHING OUTSIDE THIS DIRECTORY, and — for a suite whose subject
# is the ref namespace — NO REF EITHER.  Both are CHECKED here rather than
# asserted: `git status --porcelain` and `git tag -l 'pin/*'` are taken before
# and after and compared.  A suite that quietly created the tags it recommends
# would be the defect it reports, one level up.
#
# THE TAGS ARE MADE BY `mktags.sh`, WHICH IS NOT RUN HERE.  With no arguments
# it prints the commands and creates nothing; `--yes` creates them locally;
# `--push` sends them to origin, which is the only half that survives this
# machine.  `R4d` measures which half actually happened.
#
# `x1_gc.py` IS NOT RUN HERE EITHER.  It clones this repository and runs
# `git gc --prune=now`, which is the operation this whole ticket is about, and
# running it inside a worktree would be the joke telling itself.  Run it
# yourself:
#
#     python3 x1_gc.py --sandbox /tmp/223d-gc
#
# Its committed transcript is therefore a DATED measurement, not a regenerated
# one — the same class mg-fd9c's `out_x1_orbit.txt` is in, and it is declared
# rather than hidden.
#
# EVERY NUMBER IN EVERY TRANSCRIPT HERE IS A FACT ABOUT THE OBJECT STORE AS OF
# THE RUN.  That is not a caveat for this tree, it is the subject: a
# reachability report has no meaning without a date, and the Ledger header on
# every transcript says so.
#
# WRITE TO A TEMP AND MOVE.  `> out_x.txt` truncates before the probe starts,
# and mg-1abe's census found that the resulting empty file is bucketed as
# DIFFERS rather than as a failure.  `.new` + `mv` is mg-bf79's fix.
#
# EXPECTED EXIT CODES, stated before the run so a change is visible rather than
# absorbed: r0 = 0, r1 = 1 (the AT-RISK finding), r2 = 1 (the cause is uniform,
# which is a FINDING about the subject: it is a class), r3 = 2, r4 = 0 once the
# tags exist and 3 before, r5 = 0.  A FINDING here is this suite working.
set -u
cd "$(dirname "$0")"

BEFORE=$(git -C ../.. status --porcelain | grep -v 'code/pinned_ref_durability_223d/' || true)
TAGS_BEFORE=$(git -C ../.. tag -l 'pin/*' | sort)

rm -f ./out_*.txt.new
run() {
    _p=$1
    _o=$2
    echo "### $_p"
    python3 -B "$_p" > "$_o.new" 2>&1 || {
        echo "    (exit $? -- see the header for the expected code; a FINDING"
        echo "     is this suite working, and is not a MISS)"; }
    mv -f "$_o.new" "$_o"
    cat "$_o"
    echo
}

run r0_selftest.py     out_r0_selftest.txt
run r1_population.py   out_r1_population.txt
run r2_cause.py        out_r2_cause.txt
run r3_reconstruct.py  out_r3_reconstruct.txt
run r4_durable.py      out_r4_durable.txt
run r5_self.py         out_r5_self.txt

echo "=========================================================================="
echo "NOTHING OUTSIDE THIS DIRECTORY WAS WRITTEN, AND NO REF WAS CREATED"
echo "-- CHECKED, NOT ASSERTED"
echo "=========================================================================="
AFTER=$(git -C ../.. status --porcelain | grep -v 'code/pinned_ref_durability_223d/' || true)
TAGS_AFTER=$(git -C ../.. tag -l 'pin/*' | sort)
if [ "$BEFORE" = "$AFTER" ]; then
    echo "      git status outside code/pinned_ref_durability_223d/: UNCHANGED"
else
    echo "      *** CHANGED OUTSIDE THIS TREE ***"
    printf 'before:\n%s\nafter:\n%s\n' "$BEFORE" "$AFTER"
fi
if [ "$TAGS_BEFORE" = "$TAGS_AFTER" ]; then
    echo "      refs/tags/pin/*: UNCHANGED by this suite ($(printf '%s\n' "$TAGS_AFTER" | grep -c . ) present)"
else
    echo "      *** THIS SUITE CREATED OR DELETED A TAG -- IT MUST NOT ***"
    printf 'before:\n%s\nafter:\n%s\n' "$TAGS_BEFORE" "$TAGS_AFTER"
fi

echo
echo "=========================================================================="
echo "SUMMARY -- every FINDING and every TOTAL, from the transcripts"
echo "=========================================================================="
grep -h '^TOTAL BAD:\|^FINDINGS \|^\[FINDING' out_r*.txt || true
