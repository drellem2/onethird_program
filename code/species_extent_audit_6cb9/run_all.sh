#!/bin/sh
# mg-6cb9 -- INDEPENDENT AUDIT of the mg-d633 repair (e8fbd4f) of mg-7dd3.
#
# ALL FOUR printed extents re-measured from both sides at sites of my own
# choosing, the cross-section check demonstrated FIRING and demonstrated
# SILENT, every "under what change would the answer differ?" sentence in the
# repair made to differ, and the placement of every correction checked from
# where its false belief lives.
#
# Pure Python 3, no dependencies, NO NETWORK.  About 3 minutes.
#
# THIS INSTRUMENT MUTATES THE WORKTREE IT IS RUN IN, one edit at a time, and
# restores it.  `git status --porcelain` is captured before every probe and
# compared after it; any difference stops the run with exit 2.  The self-test
# asserts that contract eight ways before anything else runs.  Run it on a
# clean tree.
set -e
cd "$(dirname "$0")"

python3 -B selftest6cb9.py             | tee out_selftest.txt
python3 -B a1_bothways.py              > out_a1_bothways.txt || true
python3 -B a2_crosssection.py          > out_a2_crosssection.txt || true
python3 -B a3_differ_and_placement.py  > out_a3_differ.txt || true

echo
echo "Headline lines:"
grep -h '^A[123] TOTAL BAD:\|^selftestd6cb9' out_*.txt || true
echo
echo "A1/A2/A3 TOTAL BAD are NOT zero and are not meant to be: each counts"
echo "the findings this audit is reporting, and each is followed IN THE"
echo "OUTPUT by its own extent.  The findings are listed in"
echo "docs/OneThird-Species-Hopf-Monoids-ExtentRepair-IndependentAudit.md."
