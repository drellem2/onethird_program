#!/bin/sh
# mg-5644 — INDEPENDENT AUDIT of mg-bee1 (a2d5a81 + 2a29f30), the SIXTH control in this
# lineage.
#
# THE QUESTION IS NOT "is mg-bee1's fix correct".  Five controls in, each was blind in a
# different place: a pinned revision (at the INPUT), author-chosen substrings (at the
# MUTATION SET), a vacuous control group (at the POPULATION), a restatement labelled a
# control (at the PROPOSITION), and a real property bounded to a SECTION while stated
# universally.  Five for five, the blind spot MOVED rather than closed.  So the question is
# WHICH LAYER IS UNCONTROLLED NOW, answered per layer and verified rather than inherited.
#
# ~6 min.  Sections 1, 2 and 5 MUTATE tracked files in the working tree —
# docs/state-history/attempt-mg-276d.md and code/state_landing_control_2da3/delta_control.py
# — and restore them under a `finally` + sha256 check.  Each refuses to run on a dirty tree,
# because a crash would then restore the wrong bytes.  Sections 3 and 4 mutate nothing.
#
# SECTION 3 needs two real GFM renderers, which is the point of it: mg-218d established that
# this control's presentation model can be measured rather than argued, and B1 below is a
# claim about what a reader is shown, so it is measured the same way.  Install them OUTSIDE
# the repo — they are a dependency of this audit only, never of the control:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_delegation_audit_5644/run_all.sh
#
# Without them section 3 prints the install line and exits 3; every other section is
# unaffected and B1 still stands on section 1.
set -e
cd "$(git rev-parse --show-toplevel)"
cd code/state_delegation_audit_5644

echo "### 1. delegated5644.py — B1: six mutations on the surface mg-bee1 CREATED"
python3 delegated5644.py
echo
echo "### 2. norm5644.py      — B2: the L0 probes, and every character of the population"
python3 norm5644.py
echo
echo "### 3. render5644.py    — B1 measured against two real GFM renderers, not a model"
python3 render5644.py || echo "(section 3 exited $?)"
echo
echo "### 4. l2pop5644.py     — mg-bee1's L2 negative, tested BY CONSTRUCTION"
python3 l2pop5644.py
echo
echo "### 5. mg-218d's SIXTEEN, re-run UNMODIFIED on mg-218d's own harness"
echo "###    (not this audit's — the point is that nothing of mg-218d's was edited)"
cd "$(git rev-parse --show-toplevel)"
python3 code/state_layer_audit_218d/layers218d.py
