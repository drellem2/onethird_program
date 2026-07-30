#!/bin/sh
# mg-8916: landing the two sites mg-835f left open on the mg-a318 repair.
# One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on
# a 2024 laptop: ~30 s, almost all of it the 13 runs of the audited runner and
# the 2 runs of the mg-8a5c audit instrument.
#
# WHAT THIS INSTRUMENT IS FOR.  mg-835f returned PARTIAL.  Its primary target
# HELD and is not re-opened: 12 of 12 reader-facing figures corrupted on disk
# make the run red and 12 of 12 restorations make it green again.  What it left
# open was one level out from that gate and one sentence short of a summary:
#
#   G-1  a wrong figure written into the same site in ORDINARY PROSE was
#        invisible at 3 of the 3 sites, at exit 0.
#   G-2  the mg-8a5c instrument's own BOTTOM LINE asserted a primary target its
#        own T1 row refuted, in the same transcript.
#
# BOTH ARE MEASURED HERE IN BOTH DIRECTIONS.  R1 writes the wrong prose figure
# to disk at each site, length-preservingly, runs the REAL runner, restores,
# checks the restoration by sha256 and runs it AGAIN.  R2 runs the mg-8a5c
# instrument twice -- once as it stands, once with its summary FORCED to
# disagree with its rows -- because a summary-versus-rows check that has never
# been shown to fire is the vacuous-check defect this arc has produced three
# times.
#
# REPRODUCTION CONTRACT, stated in terms of the FILES READ rather than a
# commit.  This transcript regenerates byte-identically for any tree in which
# STATE.md, docs/OneThird-Hodge-Side-Leverage.md,
# docs/state-history/attempt-mg-a3d4.md, code/hodge_leverage_landing_e1d0/ and
# code/hodge_leverage_audit_8a5c/ are unchanged.  It embeds no sha of its own.
#
# IT MUTATES THE TREE AND RESTORES IT, and REFUSES TO RUN against a dirty tree
# scoped to the three files it will `git checkout --`.  A checkout over an
# uncommitted edit to one of them destroys it.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0.
set -e
cd "$(dirname "$0")"

echo "== mg-8916: the two sites mg-835f left open, measured in both directions =="
status=0
python3 repair_835f.py > out_repair_8916.txt || status=$?
cat out_repair_8916.txt
exit "$status"
