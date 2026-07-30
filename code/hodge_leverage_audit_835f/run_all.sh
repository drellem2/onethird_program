#!/bin/sh
# mg-835f: INDEPENDENT AUDIT of b80dea0 + 7f66005 (mg-a318), the repair that
# landed mg-8a5c's F-1 (both halves) and F-2.  One step, one output.
# Pure Python 3 + git, plus `wc` and `perl` in A4 (deliberately: the point of
# that section is that the three measurement routes share no implementation).
# Measured runtime 2026-07-30: ~2 min, almost all of it the 63 runs of the
# audited runner and one run of the mg-2da3 control.
#
# PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  The site battery was
# predicted to pass 12 of 12 -- and does -- but a gate that reads ONE NAMED
# statement per site cannot see a figure written elsewhere in the same section,
# and this arc's own history is that the next correction ADDS a mention rather
# than corrupting the existing one.  An exit of 0 would have meant the gate
# reads everything a reader reads.
#
# IT MUTATES THE TREE AND RESTORES IT.  A1, A2 and A6 write to STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md and docs/state-history/attempt-mg-a3d4.md,
# run code/hodge_leverage_landing_e1d0/verify_landing.py against the mutated
# tree, and `git checkout --` every file back inside a `finally`.  It REFUSES TO
# RUN if any of those three is already dirty -- scoped to the files it will
# restore, which is negative_control.py's convention: a `git checkout --` over an
# uncommitted edit destroys it.  Every restoration is CHECKED by sha256, and
# every mutation is LENGTH-PRESERVING, because four of the five figures are
# lengths of the text being mutated and an insertion would move the measurement
# rather than test the gate.  `git status` is clean after a run except for this
# directory.
#
# THE RUNNER REPORTS THE AUDITOR'S STATUS.  It redirects rather than piping into
# tee, captures the status and exits with it -- mg-f922 finding F, still applied.
set -e
cd "$(dirname "$0")"

echo "== mg-835f: the mg-a318 repair, mutated AT EACH SITE against the real gate =="
status=0
# stderr is folded into the transcript on purpose: a run that dies mid-way
# otherwise leaves a TRUNCATED out_audit_a318.txt with the traceback on a
# terminal nobody kept, which is a committed artifact that looks like a short
# run rather than a failed one.  (It happened here, in A4, on a bad format spec.)
python3 audit_a318_repair.py > out_audit_a318.txt 2>&1 || status=$?
cat out_audit_a318.txt
exit "$status"
