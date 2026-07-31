#!/bin/sh
# mg-97fb: the independent audit of the mg-3f3b `n/a`-and-vocabulary repair.
# One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Runtime ~5 min, most of it the
# gate re-run as a subprocess once per probe and one `git show` per `.py` file
# per commit swept.
#
# WHAT THIS INSTRUMENT IS FOR.  mg-3f3b landed four repairs; this audit is
# built to be able to REFUTE them, which means it must be able to reach the
# places their own evidence cannot.
#
#   A2  every `n/a` the repaired matrix prints, read as a CLAIM about its
#       site, with the case it says is impossible CONSTRUCTED -- on disk,
#       from the KIND TITLE, and never from the `k_*` function that declines
#       the cell.  A construction that fires through the ASSERTION half, or
#       one line outside the declared site, is not the kind the cell declines
#       and is reported as a survivor with its boundary named.
#   A3  the `n/a` that was DELETED (8 -> 7), diffed against the pre-repair
#       matrix run from ITS OWN COMMIT'S WORKTREE, and the cell that moved
#       rebuilt here.  An `n/a` replaced by a FIRE nobody built is worse than
#       the `n/a`.
#   B1  EXISTED / TOUCHED / LIVE for the construct, at each named commit, by
#       an AST rule of mine over a vocabulary of mine -- and the 1-of-6 vs
#       0-of-6 reconciliation, counted rather than adopted.
#   B2  the four that select 6 gate rows where 3 were meant, ROW BY ROW, each
#       extra named.
#   C1  the vocabulary, DERIVED from what the gate prints and diffed against
#       the hand list, with the gate's fail-closed rule made to fail.
#   C2  the `.py` population recomputed from `git ls-tree` at each publishing
#       commit -- including the artifact's own two, at HEAD.
#   D   what must not be disturbed: the cutters written from the DISCLOSURE
#       SENTENCES, the refusal probed ONE ROW AT A TIME against a control at
#       the commit where the defect is present, and 29 of 29 cells firing.
#   E   the floor -- two things no list in the brief names.
#   F   this instrument, checked for the shapes it audits.
#
# IT MUTATES THE TREE AND RESTORES IT.  Every on-disk probe reports its own
# `restored byte-identical` flag and `F1b` makes a single False red: a probe
# that rewrites the artifact while auditing it is the failure mg-3f3b named
# for itself, and asserting the restore is not the same as checking it.
#
# IT CREATES DETACHED GIT WORKTREES under a temp dir and removes them in a
# `finally`.  An old gate pointed at today's documents would confound a change
# in the DERIVATION with a change in the TEXT, so each historical run gets its
# own commit's documents.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0
# (mg-c2b3).
#
# ⚠️ REPRODUCTION CONTRACT, in FILES rather than in a commit.  This transcript
# regenerates for any tree in which STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
# code/hodge_leverage_landing_e1d0/ and code/hodge_leverage_repair_6df0/ are
# unchanged.  THREE GROUPS OF ROWS ARE DELIBERATELY NOT FROZEN and they are
# the point of the deliverable: B1's HEAD count, C2's HEAD population and
# C2d's publishing-commit rows all read git, so they are MEASUREMENTS AT THE
# COMMIT THE RUN HAPPENED AT and stay measurements afterwards.  C2d is the
# finding that says why that distinction matters.
set -e
cd "$(dirname "$0")"

echo "== mg-97fb: every n/a as a claim, the construct counted, the vocabulary and the population =="
status=0
# ⚠️ stderr goes INTO the transcript.  A crash and a fired check are both
# exit 1, and a transcript that keeps only stdout ends mid-section with no
# reason in it.
python3 audit_97fb.py > out_audit_97fb.txt 2>&1 || status=$?
cat out_audit_97fb.txt
exit "$status"
