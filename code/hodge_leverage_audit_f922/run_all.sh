#!/bin/sh
# mg-f922: INDEPENDENT AUDIT of mg-e1d0 (bbe83b5), the landing that closes
# mg-3c24 -- the audit of 1e61031 (mg-a2bd's strike of ledger row G-double-prime).
# One step, one output.  Pure Python 3 + git, no third-party packages.
# Measured runtime 2026-07-30: 2.4 s (it also runs two other instruments).
#
# WHAT THIS AUDITS AND WHAT IT DOES NOT.  mg-3c24 found 0 BROKEN mathematics and
# reproduced every committed number from a route sharing no code.  Nothing here
# re-derives that and nothing here re-opens it -- T4 exists precisely to check
# that the REPAIR did not disturb it in either direction, which is the failure
# mode a strike-repair has that a normal repair does not.  What is measured is
# the repair: four documentary findings, the places a reader meets them, and the
# repair's own evidence artifact.
#
# PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  This instrument exits
# non-zero whenever any FINDING is present, and the audit was undertaken on the
# expectation that F1(b) -- record the ENLARGEMENT, not just strike the false
# sentence -- is the half a repair skips.  An exit of 0 would have meant the
# landing was clean and the brief's premise wrong; both were checkable outcomes.
#
# IT RUNS TWO OTHER INSTRUMENTS AND RESTORES WHAT THEY WRITE.  T7 executes
# code/hodge_leverage_landing_e1d0/{verify_landing.py,run_all.sh} and T8 executes
# code/state_landing_control_2da3/run_all.sh; both of those rewrite their own
# committed transcript, so this file `git checkout --`s each one back afterwards.
# `git status` is clean after a run except for this directory.  That is checked,
# not asserted: run it twice and diff.
#
# REPRODUCTION CONTRACT, stated precisely because F-E and F-F below are about a
# transcript whose contract was not.  out_audit.txt regenerates BYTE-IDENTICALLY
# at any commit where STATE.md, docs/OneThird-Hodge-Side-Leverage.md,
# docs/state-history/attempt-mg-a3d4.md and the two instruments named above are
# unchanged.  It embeds NO commit sha for HEAD -- the HEAD row of T1's table
# prints the word "HEAD" -- so this transcript cannot be un-reproducible merely
# by being committed, which is the failure it reports in the artifact it audits.
# If one of those files changes, lines here WILL change: a finding that stops
# firing is a repair, and a check that stops passing is a regression.  Either
# way the diff is the signal.
set -e
cd "$(dirname "$0")"

echo "== mg-f922: auditing the mg-3c24 repair (mg-e1d0, bbe83b5) =="
# NOT `python3 audit_repair.py | tee out_audit.txt`.  A pipeline's status is the
# LAST command's, so under that form the runner exits 0 however the verifier
# exits and `set -e` never sees it -- measured in T7 on the artifact this audit
# examines, whose verifier exits 1 while its runner exits 0.  Redirect, capture,
# then print.
python3 audit_repair.py > out_audit.txt 2>&1 && rc=0 || rc=$?
cat out_audit.txt
exit "$rc"
