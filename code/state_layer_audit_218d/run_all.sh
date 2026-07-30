#!/bin/sh
# mg-218d — independent audit of mg-4acd / e4426c9, the FIFTH control in this lineage.
#
# THE QUESTION.  Each of the first four controls was blind in a different way — a pinned
# revision (blind at the INPUT), author-chosen substrings (at the MUTATION SET), a vacuous
# control group (at the POPULATION), a restatement labelled a control (at the PROPOSITION).
# mg-4acd closed the LOCATOR gap mg-babf found.  This audit assumes the blind spot MOVED
# rather than closed, and asks WHICH LAYER IS UNCONTROLLED NOW.
#
# ~2 min, most of it the layer battery's sixteen full runs of the control.
# Every script here MUTATES STATE.md, docs/state-history/README.md,
# docs/state-history/attempt-mg-276d.md and (in two rows) delta_control.py in the working
# tree, and restores them under a `finally` + sha256 check.  Each refuses to run if any
# file it would touch is already dirty.
#
# SECTION 3 needs a real markdown renderer, which is the point of it: COVERAGE.md says of
# presentation.py "the way to test it is to install a GFM renderer and compare", and this
# is that comparison.  The renderers are installed OUTSIDE the repo and are NOT a
# dependency of the control — only of this audit:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_layer_audit_218d/run_all.sh
#
# Without them section 3 prints how to install them and exits 3; sections 1, 2 and 4 are
# unaffected and stand on their own.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 1. layers218d.py    — sixteen mutations at the layers mg-4acd does NOT claim"
python3 code/state_layer_audit_218d/layers218d.py
echo
echo "### 2. coverage218d.py  — COVERAGE.md checked against the code, not against itself"
python3 code/state_layer_audit_218d/coverage218d.py
echo
echo "### 3. render218d.py    — the presentation MODEL against two real GFM renderers"
python3 code/state_layer_audit_218d/render218d.py || echo "(section 3 exited $?)"
echo
echo "### 4. the two predecessor batteries, re-run UNMODIFIED (necessary, not sufficient)"
python3 code/state_control_audit_babf/mutations_babf.py
python3 code/state_control_audit_2216/mutation_battery.py
