#!/bin/sh
# mg-8eca: landing the two sites mg-8aae left open on the mg-8916 repair.
# One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on
# a 2024 laptop: 4 min 43 s, almost all of it the 9 runs of the audited runner,
# the 6 runs of the mg-8a5c instrument, and the runs of mg-8aae's and mg-8916's
# own instruments in R3.
#
# WHAT THIS INSTRUMENT IS FOR.  mg-8aae returned PARTIAL.  What held is not
# re-opened: the 12 of 12 survives the widening at row granularity and G-1 is
# closed against wording that audit chose.  What it left open was two checks
# whose measured property was INVARIANT UNDER THE FAILURE THEY GUARDED:
#
#   H-1  the census is a MULTISET, and a multiset is invariant under a
#        transposition, so exchanging two DECLARED figures in ordinary prose
#        left the runner at exit 0 at 2 of 2 sites.
#   H-2  `SUMMARY vs ROWS` scored `printed == derived` where
#        `printed = FORCE_SUMMARY or derived` -- `x == x` off the hook, and
#        the only demonstration it had ran THROUGH that hook.
#
# NEITHER IS A COVERAGE PROBLEM AND NEITHER IS FIXED BY CHECKING MORE THINGS.
# R1 makes the census positional and shows the new property moving under the
# exact mutation the old one sat still for.  R2 makes the summary check read
# the sentence it prints and fires it ON THE REAL ARTIFACT with no environment
# variable set -- then reinstates the removed lines and shows the same artifact
# going uncaught again, because DEMONSTRATING A CHECK FIRES VIA A TEST HOOK
# PROVES THE HOOK WORKS, NOT THE CHECK.
#
# REPRODUCTION CONTRACT, stated in terms of the FILES READ rather than a
# commit.  This transcript regenerates byte-identically for any tree in which
# STATE.md, docs/OneThird-Hodge-Side-Leverage.md,
# docs/state-history/attempt-mg-a3d4.md, code/hodge_leverage_landing_e1d0/,
# code/hodge_leverage_audit_8a5c/ and code/hodge_leverage_audit_8aae/ are
# unchanged.  It embeds no sha of its own.
#
# IT MUTATES THE TREE AND RESTORES IT, and REFUSES TO RUN against a dirty tree
# scoped to the files it will `git checkout --`.  A checkout over an
# uncommitted edit to one of them destroys it.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0.
set -e
cd "$(dirname "$0")"

echo "== mg-8eca: the two sites mg-8aae left open, measured on the artifact =="
status=0
python3 repair_8aae.py > out_repair_8eca.txt || status=$?
cat out_repair_8eca.txt
exit "$status"
