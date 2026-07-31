#!/bin/sh
# mg-ff3e: mg-9207's E2/E2b/E3 -- the census was position-aware for FIGURES and
# not for LABELS, so exchanging the labels was silent at 3 of 3.
# One step, one output.
#
# Pure Python 3 + git, no third-party packages.
#
# WHAT THIS INSTRUMENT IS FOR.  Three generations of one shape have now been
# repaired on this artifact, and two of the three repairs moved the defect to
# the adjacent field:
#
#   mg-8916  the census is a MULTISET  -> mg-8aae exchanged two FIGURES
#   mg-8eca  the census is a SEQUENCE  -> mg-9207 exchanged the two LABELS
#
# Making it position-aware for labels would buy one more generation.  What
# GENERATES the instances is that the gate compares a PROJECTION of the section
# and each repair enlarged the projection by ONE NAMED FIELD; the complement
# was always everything else.  The only projection with an empty kernel is the
# identity, so the comparison is made lossless: the section is cut into
# (SEGMENTS, FIGURES) along a seam the record itself defines, both halves are
# compared positionally, and `rejoin(segments, figures) == raw` is a gate row
# so that "the two halves are the whole record" is MEASURED.
#
# R1 runs the seven label-side exchanges ON DISK against the real runner with
# no environment variable set.  R2 deletes the new comparison -- whole, and
# then each of its two rows alone -- and shows what goes back to being silent.
# R3 maps every field of every record.  R4 re-runs the instruments that raised
# it, unmodified.  R5 prints what is not covered, and checks THIS deliverable
# for the defect it repairs.
#
# REPRODUCTION CONTRACT, in terms of the FILES READ rather than a commit.  This
# transcript regenerates byte-identically for any tree in which STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
# code/hodge_leverage_landing_e1d0/ and code/hodge_leverage_audit_9207/ are
# unchanged.  It embeds no sha of its own.
#
# IT MUTATES THE TREE AND RESTORES IT, and REFUSES TO RUN against a dirty tree
# scoped to the files it will restore.  A restore over an uncommitted edit to
# one of them destroys it.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0
# (mg-c2b3).
set -e
cd "$(dirname "$0")"

echo "== mg-ff3e: the LABEL half of an exchange, measured on the artifact =="
status=0
python3 repair_9207.py --full > out_repair_ff3e.txt || status=$?
cat out_repair_ff3e.txt
exit "$status"
