#!/bin/sh
# run_all.sh (mg-2198): independent audit of mg-5371 (docs/KSBFT-L-heavy-atom.md).
# Deterministic, single process, ~1 s. Imports nothing from the audited instrument.
# Writes then moves, so a failure keeps the committed transcript.
set -e
cd "$(dirname "$0")"
python3 audit_2198.py > out_audit_2198.txt.tmp && mv out_audit_2198.txt.tmp out_audit_2198.txt
grep -q 'ALL (after \[F\]): PASS' out_audit_2198.txt
[ "$(grep -c 'FIRES' out_audit_2198.txt)" -ge 3 ]
echo "run_all (mg-2198): ALL PASS, 3 negative controls fired"
