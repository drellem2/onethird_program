#!/bin/sh
# mg-132a: a figure's provenance is WHERE IT WAS COMPUTED, not where it came to
# rest.  One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Runtime ~5 s.  READ-ONLY: it
# mutates nothing but its own transcript, so unlike the mg-3f3b suite it has no
# restore path to get wrong.
#
# WHAT THIS INSTRUMENT IS FOR.  `repair_7e39.py` repaired mg-7e39's F2 with a
# check keyed on `git log -1`.  That check is RED at `94ecf9d` on the two
# transcripts it was built to protect -- and THEY WERE RIGHT WHEN WRITTEN.  A
# merge rebased them onto a tree that had grown, so the commit that PUBLISHES
# each figure is no longer the commit it was MEASURED at.
#
#   A1  every published figure against the tree it was MEASURED at, with the
#       publishing commit reported beside it rather than in place of it.
#   A2  the controls: each rung of the verdict lattice shown FIRING, including
#       on `77306a7` where the original defect is still present.
#   A3  this deliverable put through its own rule, and the gap it does NOT
#       close, named.
#
# ⚠️ RE-RUN IT AFTER A MERGE.  `sh run_all.sh --at <rev>` audits any commit.
# The step that broke the check this repairs was not a run, it was a MERGE, and
# nothing in a repository can run after one.  A committed `0 REFUTED` is a
# measurement at the run's commit and says nothing about the tree you are
# holding now.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how a
# transcript recording a refutation came to be committed beside an exit 0
# (mg-c2b3).
set -e
cd "$(dirname "$0")"

echo "== mg-132a: the anchor is the commit a figure was MEASURED at =="
status=0
# ⚠️ stderr goes INTO the transcript.  A crash and a fired check are both exit
# 1, and a transcript that keeps only stdout ends mid-section with no reason.
python3 anchor_132a.py "$@" > out_anchor_132a.txt 2>&1 || status=$?
cat out_anchor_132a.txt
exit "$status"
