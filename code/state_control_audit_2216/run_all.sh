#!/bin/sh
# mg-2216 — INDEPENDENT audit of bf17716 (mg-2da3): the working-tree control for
# b68db5d's delta, and the record corrections that ship with it.
#
# WHY AN AUDIT WITH ITS OWN MUTATIONS.  mg-2da3's deliverable IS an instrument.  Its
# evidence of sensitivity is `negative_control.py`, which its own author wrote — and a
# control validated only by its author is the defect being repaired, one level up.  So
# this audit does not re-run that negative control and call it verified.  It builds
# fourteen mutations of its own, none of them mg-2da3's, chosen to be SMALL where
# mg-2da3's are large: single characters, length-preserving substitutions, whitespace-only
# edits, a reordering that preserves the token multiset, and a hollowing-out of a certified
# README block that keeps the one line the control actually tests.
#
#   1. mutation_battery.py  — what can delta_control.py not see?  It runs delta_control.py
#                             15 times and the pinned battery once  (~3 s measured)
#   2. claims_audit.py      — the pinned battery's preserved purpose, the findability of
#                             the record correction, and the commit's own factual claims,
#                             including the two that read as fairness.  It runs the pinned
#                             battery once, verify_relocation.py once and the audited
#                             control's own run_all.sh twice  (~9 s measured)
#
# The runtimes above are measured wall-clock on this box, not estimates — see the audit
# document's MINOR 2, which is about a runtime figure that was one.
#
# mutation_battery.py MUTATES STATE.md and docs/state-history/README.md in the working
# tree and restores them under a `finally` + sha256 check; it refuses to run if either is
# already dirty.  claims_audit.py is read-only.  Both are written from the file format and
# from git, importing nothing from the instruments they audit.
#
# out_mutations.txt and out_claims.txt are this script's committed output and reproduce
# byte-identically at this commit.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 1. mutation_battery.py — what is the smallest change delta_control.py misses?"
python3 code/state_control_audit_2216/mutation_battery.py
echo
echo "### 2. claims_audit.py — the battery's purpose, the record, and the caveats"
python3 code/state_control_audit_2216/claims_audit.py
