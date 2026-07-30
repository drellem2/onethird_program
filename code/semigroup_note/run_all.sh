#!/bin/sh
# Regenerate the verification output for docs/OneThird-Semigroup-Walk-Family-Note.md.
# Pure Python 3, no dependencies, ~45 s.  Deterministic: the committed
# note_check_output.txt should reproduce byte-identically.
set -e
cd "$(dirname "$0")"
python3 -u note_check.py > note_check_output.txt
echo "wrote note_check_output.txt"
