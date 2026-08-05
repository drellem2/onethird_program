#!/bin/sh
# mg-65eb — the whole of this audit's evidence, in order.
#
# THE INDEPENDENT AUDIT of mg-a74f, the repair of mg-16eb's three OPENs on mg-0049.  The
# parent is merged and is not re-done here.
#
# THE SECTION NUMBERS ARE THE PREDICTION.  `PREDICTIONS.md` section 7 pins an exit code for
# every command below, committed at 880fc15 before any script in this directory existed, and
# the sections here are numbered to match that table row for row so a reader can put the two
# side by side without a key.  Where a section's observed code differs from the pinned one,
# README.md keeps the miss as written; nothing here is renumbered to fit a result.
#
# THIS AUDIT WRITES TO NOTHING IT AUDITS.  Section 0 proves that rather than asserting it.
# Every construction in six65eb.py and rerun65eb.py runs inside a THROWAWAY GIT WORKTREE
# checked out at the revision under test and deleted afterwards, so the four audited
# directories cannot be damaged even by a crash mid-run.  rows65eb.py's section C is the one
# exception and uses this cluster's snapshot / `finally` / post-restore-sha discipline.
#
# ~45 min, most of it sections 4, 10 and 12 (reproduce16eb.py runs three times in total: twice
# inside section 4, at both revisions, and once alone in section 12).
#
# SECTIONS 1, 3, 4, 6, 8, 10 and 12 need two real GFM renderers, installed OUTSIDE the repo.
# They are a dependency of this EVIDENCE only, never of any control:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_visibility_audit_65eb/run_all.sh
#
# Without them those sections exit 3 and say so; the exit code is printed on every section so
# a partial run cannot be read as a full one.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1

echo "### 0. THE AUDITED DIRECTORIES ARE UNMODIFIED BY THIS AUDIT — proof, not assertion"
echo "###    (an audit that edits what it measures is not evidence about it.  PREDICTIONS.md"
echo "###     section 7 row 0 says 'the three audited directories' and there are FOUR; the"
echo "###     miscount is this audit's own and all four are printed — see README.md)"
for d in code/state_delegation_repair_a74f code/state_delegation_repair_0049 \
         code/state_landing_control_2da3 code/state_delegation_audit_16eb; do
  n=$(git diff HEAD --stat -- "$d" | wc -c | tr -d ' ')
  echo "    git diff HEAD --stat -- $d/   ->   $n bytes of diff"
done
echo "    (0 bytes on every row above = this audit changed nothing it measures)"
echo

echo "### 1. rows65eb.py — THE ROW LEDGER: the property CLAIMED beside the quantity COMPUTED"
echo "###    for all 9 rows mg-a74f publishes, and a case that separates them (expect 1)"
python3 code/state_visibility_audit_65eb/rows65eb.py || echo "(section 1 exited $?)"
echo

echo "### 2. anchor65eb.py — THE FLOOR: the revisions this repair pins its own integrity"
echo "###    claim to, resolved rather than read (expect 1 — one anchor is STALE)"
python3 code/state_visibility_audit_65eb/anchor65eb.py || echo "(section 2 exited $?)"
echo

echo "### 2b. THE SAME PROGRAM AT bd24efc — the NEGATIVE CONTROL.  At a revision where this"
echo "###     repair's directory does not exist there is no stale anchor, and the same rule"
echo "###     over the same population exits 0 (expect 0)"
python3 code/state_visibility_audit_65eb/anchor65eb.py --rev bd24efc \
  || echo "(section 2b exited $?)"
echo

echo "### 3. six65eb.py — the six claims re-classified FROM SCRATCH, each probed by resolving"
echo "###    a reference or by building a tree, and the downgrade question answered (expect 0)"
python3 code/state_visibility_audit_65eb/six65eb.py || echo "(section 3 exited $?)"
echo

echo "### 4. rerun65eb.py — DO NOT DISTURB WHAT IS CONFIRMED.  Both confirmed figures"
echo "###    re-measured AT BOTH REVISIONS, and the set difference that says whether"
echo "###    anything regressed.  ~15 min (expect 0)"
python3 code/state_visibility_audit_65eb/rerun65eb.py || echo "(section 4 exited $?)"
echo

echo "### 5. delta_control.py — the repaired control on the clean working tree (expect 0)"
python3 code/state_landing_control_2da3/delta_control.py || echo "(section 5 exited $?)"
echo

echo "### 6. prose_a74f.py on the working tree — the checker this repair added (expect 0)"
python3 code/state_delegation_repair_a74f/prose_a74f.py || echo "(section 6 exited $?)"
echo

echo "### 7. prose_a74f.py at bd24efc — the same checker against a commit where the defects"
echo "###    are STILL PRESENT (expect 1, 4 findings)"
python3 code/state_delegation_repair_a74f/prose_a74f.py --rev bd24efc \
  || echo "(section 7 exited $?)"
echo

echo "### 8. visible_a74f.py — OPEN 1's instrument, run unmodified (expect 0).  Section 1"
echo "###    above reports three separations in this program's not-suppressed column; it is"
echo "###    run here anyway, because a separation is not a failure of the run"
python3 code/state_delegation_repair_a74f/visible_a74f.py || echo "(section 8 exited $?)"
echo

echo "### 9. claims_a74f.py — OPEN 2's six, mg-a74f's own probes, unmodified (expect 0)"
python3 code/state_delegation_repair_a74f/claims_a74f.py || echo "(section 9 exited $?)"
echo

echo "### 10. battery_a74f.py — mg-a74f's own battery, which re-runs mg-16eb's battery16eb.py"
echo "###     inside it (expect 0; battery16eb.py returns 0 even with 2 surprises)"
python3 code/state_delegation_repair_a74f/battery_a74f.py || echo "(section 10 exited $?)"
echo

echo "### 11. claims16eb.py — mg-16eb's OWN claim checker, run UNMODIFIED on the REPAIRED"
echo "###     tree.  NOTHING IN mg-a74f's SUITE RUNS THIS.  It reports 4 of the six still"
echo "###     BROKEN, and section 3 shows all four of those verdicts are the literal False"
echo "###     (expect 0 — it returns 0 whatever it finds, which is itself the point)"
python3 code/state_delegation_audit_16eb/claims16eb.py || echo "(section 11 exited $?)"
echo

echo "### 12. reproduce16eb.py — mg-0049's seven committed transcripts, regenerated and"
echo "###     diffed byte for byte on the working tree.  ~7 min (expect non-zero: 5 of 7)."
echo "###     Section 4 above measures the SAME thing at bd24efc, which is what says the"
echo "###     two that fail were already stale"
python3 code/state_delegation_audit_16eb/reproduce16eb.py || echo "(section 12 exited $?)"
echo

echo "### 13. THE AUDITED DIRECTORIES, AGAIN, AFTER EVERYTHING ABOVE HAS RUN"
for d in code/state_delegation_repair_a74f code/state_delegation_repair_0049 \
         code/state_landing_control_2da3 code/state_delegation_audit_16eb; do
  n=$(git diff HEAD --stat -- "$d" | wc -c | tr -d ' ')
  echo "    git diff HEAD --stat -- $d/   ->   $n bytes of diff"
done
echo "    (0 bytes on every row = every restore in every section above held)"
echo
echo "### DONE."
