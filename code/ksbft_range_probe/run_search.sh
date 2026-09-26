#!/bin/sh
# run_search.sh OBJ SEED -- annealing witnesses for D in 3 4 5 6 8, n = 12..24
# (one output file per (OBJ, SEED); HEURISTIC, see README)
set -e
OBJ=$1; SEED=$2
OUT=out/search_${OBJ}_s${SEED}.jsonl
: > "$OUT"
for D in 3 4 5 6 8; do
  ./probe search 12 24 "$D" "$OBJ" "$SEED" 1500000 6 >> "$OUT"
done
