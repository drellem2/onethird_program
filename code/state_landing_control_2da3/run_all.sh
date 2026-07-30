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
# mg-7870 REPAIRED THE CERTIFYING MECHANISM.  mg-2216 audited this instrument with fourteen
# independent mutations and EIGHT exited 0, including a 1,556-character correction-block body
# and 38% of the certified ledger cell: the check enumerated substrings, and enumeration is
# transparent to length-preserving edits and to block bodies whose headers survive.  Each
# certified region now carries a SHA-256 of its normalised bytes.  COVERAGE.md, beside this
# script, states which regions are digested, what the normalisation is, and what is
# deliberately not covered — read that first.
#
# mg-4acd EXTENDED THE CERTIFICATION FROM THE BYTES TO WHAT A READER SEES.  mg-babf audited
# the digest and it HELD — mg-2216's five survivors all fire, and five probes of the
# normalisation all landed correctly — but the blind spot had moved one layer up, into the
# LOCATOR: four mutations changed NO CERTIFIED BYTE and exited 0, including this file's own
# certified F1 block HTML-commented out of the rendered README.  Each region now carries a
# SECOND digest, of a four-field PRESENTATION RECORD (state / heading / position / presented),
# computed by presentation.py beside this script.  A region nobody is shown is a FAIL.
# COVERAGE.md states what the presentation layer does NOT cover, and what the mechanism COSTS:
# presentation.py is a MODEL of a renderer, not a renderer, and that is the layer nothing
# above it now controls.  Read COVERAGE.md first.
#
# SECTION 0 is presentation.py's own self-test.  It checks the MODEL against its own stated
# subset — every claim the header makes about which constructs are modelled and which are
# default-denied has a case — and it emphatically does NOT check the model against a real
# renderer, which is impossible here and is the residual risk COVERAGE.md names.
#
# ~25 s total, most of it the two full runs of the pinned battery that negative_control.py
# performs for contrast.  negative_control.py MUTATES STATE.md and the state-history README
# in the working tree and restores them under a finally + sha256 check; it refuses to run
# if either is already dirty.  out_control.txt is this script's committed output.
#
# THE EVIDENCE THAT THE REPAIR WORKS IS NOT IN THIS SCRIPT, and deliberately so: an author's
# own negative control cannot establish sensitivity, because the author picks the mutations.
# It is two INDEPENDENT batteries, each written before the repair it tests, by someone else,
# each re-run UNMODIFIED and captured verbatim:
#     python3 code/state_control_audit_babf/mutations_babf.py     -> out_battery_babf_rerun.txt
#         15 mutations, 11 of 11 expected-catch CAUGHT, 0 SILENT MISSES (was 6), 0 noisy
#     python3 code/state_control_audit_2216/mutation_battery.py   -> out_battery_2216_rerun_4acd.txt
#         14 mutations, 10 caught, 0 MISSED, 2 tolerated, 2 NOISY — M12 and M13, a published
#         tolerance REVERSED on purpose and argued in COVERAGE.md, not folded in quietly
# Neither is run here because both mutate the same two files and each takes ~30 s on its own.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 0. presentation.py     — does the model match its own DECLARED SUBSET?"
python3 code/state_landing_control_2da3/presentation.py
echo
echo "### 1. delta_control.py    — does b68db5d's delta hold IN THE WORKING TREE?"
python3 code/state_landing_control_2da3/delta_control.py
echo
echo "### 2. negative_control.py — can it fail?  (and can the pinned battery?)"
python3 code/state_landing_control_2da3/negative_control.py
