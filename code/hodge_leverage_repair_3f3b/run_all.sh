#!/bin/sh
# mg-3f3b: mg-7e39's four findings -- `n/a` read as a claim, the construct at
# all six, the vocabulary derived, and the population re-derived at the commit
# that publishes it.  One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Runtime ~30 s, most of it the
# runner re-run as a subprocess once per probe.
#
# WHAT THIS INSTRUMENT IS FOR.  Three of the four findings are one shape: a
# STATEMENT THAT READS AS A MEASUREMENT AND IS NOT ONE.
#
#   F1  an `n/a` reason phrased as a property of the SITE that is a property
#       of the DERIVATION.  A matrix reports FIRE / SILENT / n/a and only the
#       first two are measured; `n/a` is prose, and it is where a matrix
#       hides.
#   F5  a sweep vocabulary hand-listed at five where the gate prints six.  A
#       sweep built because a hand-picked SITE is a scope nobody chose picked
#       its VOCABULARY the same way.
#   F2  a population figure carried in prose that was already wrong at the
#       commit which published it -- 429 against 448, not drift.
#   F3  the remedy applied at the line the defect was found on: 1 touched of
#       6, with 5 given a disposition instead of a repair.
#
# So the scoring is deliberately not "is the named cell fixed":
#   S1  reads EVERY `n/a` the runner prints as a claim and tries it with a
#       mutation derived here from the KIND TITLE, and reverts the repaired
#       clause alone as the control.
#   S2  reports the construct at ALL SIX sites, with what each selects that it
#       was never meant to, and sweeps the whole tree by the parent's own rule.
#   S3  renames a gate row in a COPY of the gate's source and shows the sweep's
#       vocabulary follow it -- derived rather than copied.
#   S4  re-derives the population from `git ls-tree` AT A NAMED COMMIT, and
#       separates a figure a publication step recomputes from a figure prose
#       carries.
#   S5  checks this deliverable for all four shapes.
#   S6  re-derives the probe-before-repair ordering from `git log`.
#
# REPRODUCTION CONTRACT, in terms of the FILES READ rather than a commit.  This
# transcript regenerates for any tree in which STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
# code/hodge_leverage_landing_e1d0/ and code/hodge_leverage_repair_6df0/ are
# unchanged.  It embeds no sha of its own.  ⚠️ THREE ROWS ARE DELIBERATELY NOT
# FROZEN, and they are the point of the deliverable: S4's HEAD population, S4a
# and S6a all read git, so they become measurements at the commit that lands
# this file and stay measurements afterwards.  A population figure that is
# frozen in a transcript is F2.
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

echo "== mg-3f3b: n/a as a claim, the construct at all six, the vocabulary, the population =="
status=0
# ⚠️ stderr goes INTO the transcript.  A crash and a fired check are both
# exit 1, and a transcript that keeps only stdout ends mid-section with no
# reason in it.
python3 repair_7e39.py > out_repair_3f3b.txt 2>&1 || status=$?
cat out_repair_3f3b.txt
exit "$status"
