#!/bin/sh
# mg-0120 — the repair of the AUDITOR'S OWN RECORD.
#
# THE BRIEF, in one line.  mg-16eb's `claims16eb.py` is named "THE CLAIMS mg-0049 ADDED,
# CHECKED", and six of the seventeen rows it prints carried the verdict as a literal.  A
# constant returns the same answer on every tree, so for those six the quantity computed was
# not a measurement.  This suite computes all six, PROVES EACH CAN GO BOTH WAYS, re-derives
# the figure the arc publishes, and repairs the integrity anchor mg-65eb found rotted.
#
# ~15 min.  NOTHING IS WRITTEN TO THE WORKING TREE.  Every construction is applied inside a
# throwaway `git worktree` (or, for section 4's collision control, a throwaway repository
# under a temp directory) and removed on the way out.  There is no restore step, so there is
# no restore step that can fail.
#
# SECTIONS 1, 2 AND 5 NEED TWO REAL GFM RENDERERS, installed OUTSIDE the repo.  They are a
# dependency of the EVIDENCE only, never of the control:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_claims_repair_0120/run_all.sh
#
# Without them, two of the six rows report UNPROBED and their flip constructions report
# `not attempted` — never silently as holding, and never as proven.
#
# READ THE EXIT CODES.  Section 3 exits 1 BY DESIGN: the figure this arc publishes is 6 and
# the re-derived figure is 7, and a program that reported that as a pass would be committing
# the defect it was written to find.  Section 6 exits 1 because `presentation.py:24` is
# genuinely BROKEN on the repaired tree and nobody has repaired it.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 1. flip_0120.py — EVERY REPAIRED VERDICT SHOWN RETURNING BOTH ANSWERS.  Tier 1 is"
echo "###    the same function at bd24efc and at the working tree; tier 2 is a constructed"
echo "###    input per row; section 3 of it puts two stand-ins pinned to the literal False"
echo "###    and the literal True through the identical path and requires NOT PROVEN."
python3 code/state_claims_repair_0120/flip_0120.py || echo "(section 1 exited $?)"
echo

echo "### 2. claims16eb.py — mg-16eb's OWN claim checker, REPAIRED, on the repaired tree."
echo "###    17 rows over three states.  It exits 0; the BROKEN row is reported, not fatal,"
echo "###    which is how mg-16eb wrote it."
python3 code/state_delegation_audit_16eb/claims16eb.py || echo "(section 2 exited $?)"
echo

echo "### 3. rests0120.py — THE QUESTION THE TICKET EXISTS FOR: what rests on the pinned"
echo "###    rows.  The answer is the cardinality SIX, and it DOES NOT SURVIVE — run at"
echo "###    bd24efc with every verdict computed, mg-16eb's own program says SEVEN."
echo "###    EXPECTED EXIT 1."
python3 code/state_claims_repair_0120/rests0120.py || echo "(section 3 exited $?)"
echo

echo "### 4. anchors0120.py — the integrity anchor DIAGNOSED BY CONTENT (displaced by a"
echo "###    rebase, not lost), the twin rule's own control CONSTRUCTED, and every anchor"
echo "###    in the repository re-measured against main rather than against HEAD."
python3 code/state_claims_repair_0120/anchors0120.py || echo "(section 4 exited $?)"
echo

echo "### 5. anchors0120.py --ref HEAD — the SAME RULE AGAINST A DIFFERENT REFERENCE."
echo "###    An anchor is reachable RELATIVE TO SOMETHING, so the reference is part of the"
echo "###    measurement.  This run is committed because the first draft of this line"
echo "###    PREDICTED the anchor under repair would come out LIVE here, and it does NOT:"
echo "###    this branch descends from main, not from polecat-a74f, so 739f7bd is displaced"
echo "###    against both.  What DOES move between the two references is the population"
echo "###    (373 -> 377 distinct tokens) and the LIVE count (256 -> 258), because HEAD"
echo "###    reaches this repair's own unmerged commits and main does not.  THAT is the"
echo "###    hazard: an anchor measured against HEAD on a polecat branch is measured against"
echo "###    a tree no reader of main has."
python3 code/state_claims_repair_0120/anchors0120.py --ref HEAD || echo "(section 5 exited $?)"
echo

echo "### 6. mg-16eb's OWN suite, re-run UNMODIFIED except for the file this repair edits."
echo "###    Sections 1-3 and 5 of it touch nothing this repair changed; section 4 is the"
echo "###    repaired claims16eb.py.  Run it to see the repair in its own harness."
echo "###    (Not run here: it re-runs mg-5644's and mg-218d's whole batteries and takes"
echo "###    ~25 minutes.  The command is printed rather than a figure being claimed for it.)"
echo "    sh code/state_delegation_audit_16eb/run_all.sh"
echo
