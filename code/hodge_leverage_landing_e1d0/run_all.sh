#!/bin/sh
# mg-e1d0: landing mg-3c24, the audit of 1e61031 (mg-a2bd's strike of ledger
# row G-double-prime).  One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-30 on
# a 2024 laptop: 0.9 s (a handful of `git show`s and two file reads).
#
# WHAT THIS INSTRUMENT IS FOR.  mg-3c24 found 0 BROKEN mathematics and every
# committed number reproduced from a route sharing no code.  Its four findings
# are all of one kind: a claim a document makes ABOUT ITSELF, about another
# document, or about a ticket.  None of them can be checked by recomputing
# posets, and all of them can be checked against git and the tree -- so that is
# what this does.  Nothing here re-derives mg-3c24's mathematics and nothing
# here re-opens it.
#
# EVERY NUMBER THIS LANDING WRITES INTO PROSE IS PRINTED HERE FIRST, and none
# is inherited from mg-3c24 or from the ticket.  That matters more than usual
# for this landing: F1 is *a commit enlarged a mismatch while asserting it was
# unchanged*, i.e. a finding about a number nobody re-measured, and quoting the
# audit's numbers to close it would repeat the shape.
#
# THE OUTPUT HAS TWO KINDS OF LINE, and the difference is the point:
#
#   [CONFIRMED] / [REFUTED] on the AUDITED COMMIT -- re-measured from git at
#   1e61031 and its parent.  These are frozen: they will read the same at any
#   future commit, because git does not move.
#
#   [CONFIRMED] / [REFUTED] on a line marked GATE -- measured against the LIVE
#   tree, i.e. against what this landing leaves behind.  Every GATE fails at
#   this landing's parent and passes at this landing.  They are the reason the
#   run is worth committing: they score the repair rather than describing it.
#
# So this transcript regenerates byte-identically AT THIS COMMIT (verified, two
# runs) and will NOT after later commits land on either file -- the same caveat
# mg-7d5a recorded for its own scanner.  A GATE line that stops passing is a
# regression, not a stale artifact; that is what it is for.
set -e
cd "$(dirname "$0")"

echo "== mg-e1d0: this landing's claims, re-measured from git and the tree =="
python3 verify_landing.py | tee out_verify.txt
