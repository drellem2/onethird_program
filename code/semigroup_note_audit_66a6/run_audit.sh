#!/bin/sh
# mg-66a6: independent audit of docs/OneThird-Semigroup-Walk-Family-Note.md
# (deliverable of mg-6016, commits ac5c51e and 3c9d930).
#
# Shares NO code with code/semigroup_note/ (the artefact under audit), nor with
# code/face_geometry/ or code/hodge_leverage/.  Pure Python 3, no dependencies,
# ~45 s total on an M-series laptop.  Deterministic: the committed out_*.txt
# files reproduce byte-identically (the one randomised sweep is seeded).
set -e
cd "$(dirname "$0")"
python3 -u audit_worked_example.py > out_worked_example.txt 2>&1 || true
python3 -u audit_antichain.py      > out_antichain.txt      2>&1 || true
python3 -u audit_sweeps.py 5       > out_sweeps.txt         2>&1 || true
python3 -u audit_theorem.py        > out_theorem.txt        2>&1 || true
echo "--- totals ---"
grep -h "checks, .* FAILURES" out_worked_example.txt out_antichain.txt \
     out_sweeps.txt out_theorem.txt
