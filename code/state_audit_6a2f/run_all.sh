#!/bin/sh
# mg-6a2f — independent audit of mg-34bf / 57f962f (the STATE.md restructure).
#
# Every script here was written from scratch for this audit.  None of them imports,
# reads or executes anything under code/state_restructure_34bf/ — not the relocation
# spec, not the builder's splitter, and NOT the author's completeness checker.  The
# only inputs are `git show 97cb533:STATE.md` (the parent commit), `git show
# 57f962f:STATE.md`, and the committed docs/state-history/*.md.
#
# ~5 s total.  No dataset, no enumeration.
set -e
cd "$(git rev-parse --show-toplevel)"
echo "### 1. relocation_check.py  — was anything LOST?"
python3 code/state_audit_6a2f/relocation_check.py
echo
echo "### 2. stated_properties.py — every number mg-34bf states about itself"
python3 code/state_audit_6a2f/stated_properties.py
echo
echo "### 3. insertions.py        — what was ADDED (the other direction)"
python3 code/state_audit_6a2f/insertions.py
echo
echo "### 4. additions_and_drift.py — retraction adjacency (all 58 rows) + citations"
python3 code/state_audit_6a2f/additions_and_drift.py
echo
echo "### 5. deictic_refs.py      — references re-pointed by relocation"
python3 code/state_audit_6a2f/deictic_refs.py
echo
echo "### 6. cut_points.py        — 'nothing was cut mid-sentence'"
python3 code/state_audit_6a2f/cut_points.py
