#!/bin/sh
# mg-5f7c — the whole repair, in order, with every exit code checked against PREDICTIONS.md.
#
#     sh code/state_suppression_repair_5f7c/run_all.sh
#
# Sections 1-4 and 8 need nothing but python3 and git.  Section 5 needs the two GFM
# renderers and prints the install line and exits 3 without them; the polarity claim does not
# depend on them, which is why section 1 is renderer-free and comes first.
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_suppression_repair_5f7c/run_all.sh
#
# Run it on a COMMITTED tree: section 4 mutates two tracked files under its own restore
# discipline and refuses to start on a dirty one.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
D=code/state_suppression_repair_5f7c
A=code/state_delegation_repair_a74f
rc=0

run() {                 # run <expected-exit> <label> <command...>
    want=$1; shift
    label=$1; shift
    echo
    echo "################################################################################"
    echo "### $label   (PREDICTIONS.md: exit $want)"
    echo "################################################################################"
    "$@"
    got=$?
    if [ "$got" -eq "$want" ]; then
        echo "--- exit $got, as pre-registered"
    else
        echo "--- exit $got, PRE-REGISTERED $want  <<< MISS"
        rc=1
    fi
}

run 0 "1. polarity_5f7c.py — sixteen constructions, renderer-free" \
    python3 "$D/polarity_5f7c.py"

run 1 "2. offsets_5f7c.py --rev 6fb424f — the defect at the anchor" \
    python3 "$D/offsets_5f7c.py" --rev 6fb424f

run 0 "3. offsets_5f7c.py — the tree" \
    python3 "$D/offsets_5f7c.py"

run 0 "4. prose_5f7c.py — C1 and C2 under restore discipline" \
    python3 "$D/prose_5f7c.py"

run 0 "5. visible_a74f.py — nine rows, two renderers, mg-16eb's rule beside them" \
    python3 "$A/visible_a74f.py"

run 0 "6. prose_a74f.py — the tree" \
    python3 "$A/prose_a74f.py"

run 1 "7. prose_a74f.py --rev bd24efc — the four findings mg-a74f was written against" \
    python3 "$A/prose_a74f.py" --rev bd24efc

# Section 8 was NOT in PREDICTIONS.md's exit table and was added after it; that is disclosed
# in README.md rather than smoothed over.  It is the can-this-go-red check: the same suite,
# run against the instrument as it was at the anchor, must FAIL.  A suite that cannot go red
# is not evidence that the tree passes it.
run 1 "8. polarity_5f7c.py --rev 6fb424f — the suite proving it can go red" \
    python3 "$D/polarity_5f7c.py" --rev 6fb424f

echo
echo "################################################################################"
if [ "$rc" -eq 0 ]; then
    echo "### every section exited as PREDICTIONS.md said it would"
else
    echo "### AT LEAST ONE SECTION MISSED ITS PRE-REGISTERED EXIT CODE"
fi
echo "################################################################################"
exit $rc
