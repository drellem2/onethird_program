#!/bin/sh
# mg-40e4 — the whole audit, in order, with every exit code checked against the value this
# runner declares for it.
#
#     sh code/suppression_polarity_audit_40e4/run_all.sh
#
# Sections 1-3 and 5 need nothing but python3 and git.  Section 4 needs the two GFM renderers
# and exits 3 with the install line without them; no figure of section 4 can be produced from
# the transcripts alone, so it does not guess.
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/suppression_polarity_audit_40e4/run_all.sh
#
# DISCLOSURE: these exit codes are NOT pre-registered.  mg-40e4's PREDICTIONS.md pre-registers
# findings, not exits, and inventing an exit table after the fact and calling it
# pre-registered is the shape this arc keeps finding.  Section 6 re-runs mg-5f7c's OWN runner,
# whose eight exits ARE pre-registered, and checks them.
#
# Sections 2, 3 and 5 exit 1 BY DESIGN: this audit's findings stand, and a runner that went
# green while they stand would be reporting the absence of its own results.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
D=code/suppression_polarity_audit_40e4
rc=0

# THIS GUARD IS A DEFECT OF THIS RUNNER, FOUND BY THIS RUNNER, AND KEPT AS ONE.  The first
# full pass of mg-40e4 reported `AT LEAST ONE SECTION MISSED ITS PRE-REGISTERED EXIT CODE`
# for mg-5f7c — a repair that reproduces perfectly.  The cause was this file: it was still
# untracked, so the tree was dirty, so section 4 of mg-5f7c's runner (`prose_5f7c.py`, which
# refuses to start on a dirty tree) exited 2, and the failure arrived wearing mg-5f7c's name.
# AN AUDIT THAT MAKES ITS SUBJECT FAIL BY EXISTING IS NOT MEASURING ITS SUBJECT.  Repaired by
# refusing to start rather than by another retry: the condition is named here, at the top,
# with the files that cause it.
DIRTY=$(git status --porcelain)
if [ -n "$DIRTY" ]; then
    echo "REFUSING TO START: the tree is dirty and section 6 re-runs mg-5f7c's runner, whose"
    echo "own section 4 refuses to start on a dirty tree.  Run this on a COMMITTED tree, or"
    echo "the exit-code miss you get back will be this runner's and will be reported as"
    echo "mg-5f7c's.  The tree:"
    echo "$DIRTY"
    exit 2
fi

run() {                 # run <expected-exit> <label> <command...>
    want=$1; shift
    label=$1; shift
    echo
    echo "################################################################################"
    echo "### $label   (expected exit $want)"
    echo "################################################################################"
    "$@"
    got=$?
    if [ "$got" -eq "$want" ]; then
        echo "--- exit $got, as declared"
    else
        echo "--- exit $got, DECLARED $want  <<< MISS"
        rc=1
    fi
}

run 0 "1. selftest_40e4.py — the controls on this audit's own instruments" \
    python3 "$D/selftest_40e4.py"

run 1 "2. q1_polarity_40e4.py — the polarity on two axes, 28 constructions" \
    python3 "$D/q1_polarity_40e4.py"

run 1 "3. q1_polarity_40e4.py --rev 6fb424f — the same suite at the pre-repair anchor" \
    python3 "$D/q1_polarity_40e4.py" --rev 6fb424f

run 0 "4. q2_offsets_40e4.py — the offset re-derived, over an enlarged population" \
    python3 "$D/q2_offsets_40e4.py"

run 1 "5. q3_claims_40e4.py — the four claims about the repository and about itself" \
    python3 "$D/q3_claims_40e4.py"

run 0 "6. mg-5f7c's OWN run_all.sh — does the repair still reproduce at HEAD?" \
    sh code/state_suppression_repair_5f7c/run_all.sh

echo
echo "################################################################################"
echo "### git status --porcelain after the run (section 6 mutates the tree under a"
echo "### restore discipline; a non-empty result here is a finding):"
git status --porcelain
echo "################################################################################"
if [ "$rc" -eq 0 ]; then
    echo "### every section exited as this runner declared"
else
    echo "### AT LEAST ONE SECTION MISSED ITS DECLARED EXIT CODE"
fi
echo "################################################################################"
exit $rc
