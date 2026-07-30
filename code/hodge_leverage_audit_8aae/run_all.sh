#!/bin/sh
# mg-8aae: INDEPENDENT AUDIT of the mg-8916 repair of mg-835f.
# One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on
# a 2024 laptop: ~4 min, almost all of it the ~50 runs of the audited runner,
# the 3 runs of the mg-8a5c instrument and the one ~100 s run of mg-835f's own
# instrument in A6.
#
# WHAT THIS INSTRUMENT IS FOR.  mg-8916 closed mg-835f's two open sites: G-1 (a
# wrong figure in ordinary prose beside the site was invisible at 3 of 3 sites)
# by WIDENING the gate into a census, and G-2 (a bottom line asserting a target
# its own rows refuted) by DERIVING the sentence from the rows.  This audit is
# not a re-run of mg-8916's R1-R4 -- a repair scored only by its author's
# instrument is scored by the author.  Every probe is built here.
#
#   A1  which of the three dispositions was taken, and is it SAID; the printed
#       extent re-counted by a SECOND tokenizer sharing no regex with the first
#   A2  mg-835f's 12 of 12, at ROW granularity: for each of the 12 the runner
#       must go red AND the `READ AT THE SITE` row FOR THAT FIGURE must be the
#       row that failed, or the widening absorbed the check beside it
#   A3  a wrong prose figure on THIS instrument's wording, in slots chosen by a
#       procedure and CONTROLLED GREEN before use, both directions
#   A4  the one no line of the brief names: the census is a MULTISET, so a
#       PERMUTATION of two declared figures is invisible
#   A5  `SUMMARY vs ROWS` forced apart by the repair's hook (it fires) and then
#       by editing the SENTENCE instead of the verdict variable (it does not)
#   A6  mg-835f's OWN instrument, unmodified, re-run here rather than quoted
#   A7  the rule applied to the repair's own summary: believe the rows
#   A8  the seam check, and its threshold
#
# PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  See PREDICTIONS.md,
# which also keeps the three misses that were THIS INSTRUMENT'S OWN defects.
#
# REPRODUCTION CONTRACT, stated in terms of the FILES READ rather than a
# commit.  This transcript regenerates byte-identically for any tree in which
# STATE.md, docs/OneThird-Hodge-Side-Leverage.md,
# docs/state-history/attempt-mg-a3d4.md,
# docs/OneThird-Hodge-Side-Leverage-Mg835fRepair.md,
# docs/OneThird-Hodge-Side-Leverage-Mg8a5cRepair-IndependentAudit.md,
# code/hodge_leverage_landing_e1d0/, code/hodge_leverage_audit_8a5c/,
# code/hodge_leverage_audit_835f/ and code/hodge_leverage_repair_8916/ are
# unchanged.  It embeds no sha of its own.
#
# IT MUTATES THE TREE AND RESTORES IT, and REFUSES TO RUN against a dirty tree
# scoped to the four files it will `git checkout --`.  A checkout over an
# uncommitted edit to one of them destroys it.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0.
set -e
cd "$(dirname "$0")"

echo "== mg-8aae: independent audit of the mg-8916 repair of mg-835f =="
status=0
python3 audit_8916_repair.py > out_audit_8916.txt || status=$?
cat out_audit_8916.txt
exit "$status"
