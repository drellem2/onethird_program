#!/bin/sh
# run_all.sh (mg-7d8e): independent referee checks of notes/lemma-W-polynomial-range-bound.tex.
# Deterministic, single process, ~3 s.  Writes then moves, so a failure keeps the committed transcript.
set -e
cd "$(dirname "$0")"
python3 audit_7d8e.py > out_audit_7d8e.txt.tmp && mv out_audit_7d8e.txt.tmp out_audit_7d8e.txt
grep -q 'NEG CONTROL .* FIRES' out_audit_7d8e.txt
grep -q 'poset count .* OK' out_audit_7d8e.txt
echo "run_all (mg-7d8e): ALL OK, negative control fired"
