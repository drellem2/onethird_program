#!/bin/sh
# mg-2da3 — the working-tree control for b68db5d's delta, and the proof that it can fail.
#
# WHAT THIS IS NOT.  It is not a replacement for code/state_audit_6a2f/run_all.sh and it
# does not "fix" it.  That battery pins 97cb533 / 60f4dac / 57f962f on purpose: it exists
# to reproduce mg-6a2f's audit of a specific historical state, and pinning is a FEATURE
# there.  Pointing it at the working tree would destroy the thing it is for.
#
# WHAT WENT WRONG was a citation, not an instrument.  b68db5d re-ran that pinned battery
# and described the result as certifying its own new edits — "reproduces out_audit.txt
# BYTE-IDENTICALLY with these edits applied".  A revision-pinned instrument re-run in a
# later commit is a control that CANNOT FAIL, and it fails silently in the good direction:
# the command succeeds, the bytes match, and nothing surfaces it.  mg-bd41 demonstrated it
# by gutting STATE.md 175,552 -> 37,958 bytes and getting the identical 96,291 bytes out.
#
# So the missing piece was never a repair to that battery.  It was a SECOND instrument,
# for the delta, that reads the tree it is changing.  This is that instrument, plus the
# negative control that proves it fails when the tree is mutated.
#
# THE CONVENTION THIS ESTABLISHES lives in STATE.md's Appendix A ("Re-running a
# revision-pinned instrument..."), and the correction to b68db5d's frozen sentence lives
# in docs/state-history/README.md, which is where this cluster's corrections to frozen
# commit messages already go.
#
# ~25 s total, most of it the two full runs of the pinned battery that negative_control.py
# performs for contrast.  negative_control.py MUTATES STATE.md and the state-history README
# in the working tree and restores them under a finally + sha256 check; it refuses to run
# if either is already dirty.  out_control.txt is this script's committed output.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 1. delta_control.py    — does b68db5d's delta hold IN THE WORKING TREE?"
python3 code/state_landing_control_2da3/delta_control.py
echo
echo "### 2. negative_control.py — can it fail?  (and can the pinned battery?)"
python3 code/state_landing_control_2da3/negative_control.py
