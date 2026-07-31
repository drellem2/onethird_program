#!/bin/sh
# mg-6df0: mg-ec07's E-5, E-4 and E-2 -- the blessing path's refusal excluded
# the three rows that license the whole claim by a SUBSTRING TEST, and the
# same-kind enumeration was over KINDS rather than SITES x KINDS.
# One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Runtime ~2 min, most of it
# `audit_ec07.py` re-run unmodified in R4.
#
# WHAT THIS INSTRUMENT IS FOR.  Two of the three findings it repairs are the
# same shape at different levels:
#
#   E-5  a fix applied where the defect was FOUND (mg-ff3e's own scoring code)
#        and not where it OCCURS (forty lines away, in the file being
#        repaired).  A fix with a scope nobody chose.
#   E-4  an enumeration over KINDS where the population is SITES x KINDS.  A
#        table with one cell per row reads as complete.
#
# So the scoring is deliberately not "does the reported line work now":
#   R1  runs the blessing path on disk, with `partition` bent lossy, and then
#       REVERTS THE FIX ALONE and shows the blessing come back.
#   R2  sweeps the TREE for the construct, with every hit repaired or
#       dispositioned BY ITS EXACT LINE, so a new occurrence anywhere is red.
#   R3  reads the runner's own SITES x KINDS matrix and bridges three cells to
#       disk -- including X2, which is still silent and is DECLARED with the
#       cost of covering it measured rather than argued.
#   R4  re-runs `audit_ec07.py` unmodified and reports which of ITS rows move,
#       including two findings predicted to be re-emitted.
#   R5  re-measures the printed extent independently.
#   R6  checks this deliverable for both shapes, and re-derives from git that
#       the probes were committed BEFORE the fix.
#
# REPRODUCTION CONTRACT, in terms of the FILES READ rather than a commit.  This
# transcript regenerates for any tree in which STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
# code/hodge_leverage_landing_e1d0/ and code/hodge_leverage_audit_ec07/ are
# unchanged.  It embeds no sha of its own.  ⚠️ One row is deliberately NOT
# frozen: R6a reads `git log`, so it becomes a measurement at the commit that
# lands the probe file and stays one afterwards.
#
# IT MUTATES THE TREE AND RESTORES IT, sha256-verified, and REFUSES TO RUN
# against a dirty tree scoped to the five files it restores.  A restore over an
# uncommitted edit destroys it.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0
# (mg-c2b3).
set -e
cd "$(dirname "$0")"

echo "== mg-6df0: the refusal, the product, and the extent =="
status=0
# ⚠️ stderr goes INTO the transcript.  A crash and a fired check are both
# exit 1, and a transcript that keeps only stdout ends mid-section with no
# reason in it -- which is how this instrument's own first run looked
# (mg-9207 J-3, one level down).
python3 repair_ec07.py > out_repair_6df0.txt 2>&1 || status=$?
cat out_repair_6df0.txt
exit "$status"
