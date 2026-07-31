#!/bin/sh
# mg-a74f — the whole of this repair's evidence, in order.
#
# This repair answers mg-16eb's three OPENs on mg-0049.  It EDITS three files —
# delta_control.py, mg-0049's README.md and render0049.py — and it edits NOTHING in
# code/state_delegation_audit_16eb/, the auditor's own directory.  Section 0 proves that
# rather than asserting it, because a battery edited by the party it tests is not evidence
# about that party.
#
# Sections 1, 5 and 6 mutate the working tree through their own restore discipline (a
# snapshot, a `finally`, a hard abort on a post-restore sha mismatch) and delta_control.py
# refuses to run on a dirty tree — so RUN THIS ON A COMMITTED TREE.
#
# Sections 4, 6 and 7 need two real GFM renderers, installed OUTSIDE the repo.  They are a
# dependency of this EVIDENCE only, never of the control:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_delegation_repair_a74f/run_all.sh
#
# Without them those sections print the install line and exit 3; everything else is
# unaffected and the repair still stands on sections 2, 3 and 5.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1

echo "### 0. THE AUDITOR'S DIRECTORY IS UNMODIFIED — proof, not assertion"
echo "###    (mg-16eb wrote the battery this repair is scored on; if this repair had"
echo "###     edited it, section 5 would be worthless)"
git diff HEAD --stat -- code/state_delegation_audit_16eb/ | sed 's/^/    /'
echo "    (empty above = 0 bytes of diff)"
echo

echo "### 1. delta_control.py — the repaired control on the clean working tree (expect 0)"
python3 code/state_landing_control_2da3/delta_control.py || echo "(section 1 exited $?)"
echo

echo "### 2. prose_a74f.py at bd24efc — the checker against a commit where the defects"
echo "###    are STILL PRESENT (expect 4 findings, exit 1)"
python3 code/state_delegation_repair_a74f/prose_a74f.py --rev bd24efc \
  || echo "(section 2 exited $? — non-zero is the point)"
echo

echo "### 3. prose_a74f.py on the working tree — the same checker, repaired (expect 0)"
python3 code/state_delegation_repair_a74f/prose_a74f.py || echo "(section 3 exited $?)"
echo

echo "### 4. visible_a74f.py — OPEN 1: suppression over a DECLARED set, and mg-16eb's own"
echo "###    rule imported unmodified beside it (expect 0)"
python3 code/state_delegation_repair_a74f/visible_a74f.py || echo "(section 4 exited $?)"
echo

echo "### 5. battery_a74f.py — mg-16eb's OWN eight rows, on mg-16eb's OWN harness,"
echo "###    unmodified.  Section 1 of it is that battery re-run verbatim (expect 0)"
python3 code/state_delegation_repair_a74f/battery_a74f.py || echo "(section 5 exited $?)"
echo

echo "### 6. claims_a74f.py — OPEN 2: the six, one row each, classified, and probed at"
echo "###    BOTH bd24efc and the tree (expect 0)"
python3 code/state_delegation_repair_a74f/claims_a74f.py || echo "(section 6 exited $?)"
echo

echo "### 7. reproduce16eb.py, RE-RUN UNMODIFIED — which of mg-0049's seven committed"
echo "###    out_*.txt still reproduce, and which do not.  ~10 min.  EXPECT 5 of 7:"
echo "###    the two that do not are out_coverage218d.txt and out_selftest_negative.txt,"
echo "###    and section 8 shows they were ALREADY stale at bd24efc"
python3 code/state_delegation_audit_16eb/reproduce16eb.py \
  || echo "(section 7 exited $? — read the rows, not the exit code)"
echo

echo "### 8. THE SAME CHECK AT bd24efc, IN A THROWAWAY WORKTREE — the measurement that"
echo "###    separates 'this repair broke two transcripts' from 'two were already stale'"
W=$(mktemp -d)/pre
git worktree add --detach "$W" bd24efc >/dev/null 2>&1 && {
  (cd "$W" && python3 code/state_delegation_audit_16eb/reproduce16eb.py | tail -20)
  git worktree remove --force "$W" >/dev/null 2>&1
} || echo "    (could not create a worktree at bd24efc; section 8 skipped)"
echo
