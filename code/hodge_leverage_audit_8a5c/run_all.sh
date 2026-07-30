#!/bin/sh
# mg-8a5c: INDEPENDENT AUDIT of e16e41c + 61de121 (mg-8e30), the repair that
# landed mg-f922 B/C/E/F/G.  One step, one output.  Pure Python 3 + git.
# Measured runtime 2026-07-30: 4 s (it runs the audited instrument seven times).
#
# PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  Not because the three
# figures were expected to be stale -- T1 was expected to CONFIRM, and does --
# but because the repair's correction deliberately prints the figure chain
# beside the live figure and the chain's tail IS the live figure, so a
# presence-test gate was expected to have a hole.  An exit of 0 would have meant
# the gate distinguishes them.
#
# IT MUTATES THE TREE AND RESTORES IT.  T3 writes to STATE.md, the deliverable
# and the row-history file, runs code/hodge_leverage_landing_e1d0/run_all.sh
# against the mutated tree, and `git checkout --`s every file back.  It REFUSES
# TO RUN against a dirty tree, and the restoration is CHECKED by sha256 rather
# than asserted.  `git status` is clean after a run except for this directory.
#
# REPRODUCTION CONTRACT, in terms of the FILES READ rather than a commit.
# out_audit_8e30.txt regenerates BYTE-IDENTICALLY at any tree in which STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
# docs/OneThird-Hodge-Side-Leverage-Mg3c24Repair-IndependentAudit.md and
# code/hodge_leverage_landing_e1d0/ are unchanged.  It embeds NO sha of its own:
# the one place a commit id would naturally be printed -- T4's blame column --
# prints the blame of a LINE, which is a fact about history and does not move.
# If one of those files changes, lines here WILL change; the diff is the signal.
#
# THE RUNNER REPORTS THE AUDITOR'S STATUS.  It redirects rather than piping into
# tee, captures the status and exits with it -- mg-f922 finding F, one
# generation on, applied to the instrument that reports it.
set -e
cd "$(dirname "$0")"

echo "== mg-8a5c: the mg-8e30 repair, re-measured from the POST-commit tree =="
status=0
python3 audit_repair_8e30.py > out_audit_8e30.txt || status=$?
cat out_audit_8e30.txt
exit "$status"
