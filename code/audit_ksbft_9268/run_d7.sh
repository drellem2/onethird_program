#!/bin/sh
# run_d7.sh (mg-9268): the auditor's independent D=7 search (aud.c), 30 slices
# split at depth 9, at most $POGO_WORKER_CORES concurrent processes.
set -e
cd "$(dirname "$0")"
J=${POGO_WORKER_CORES:-3}
BIN=$(mktemp -d)/aud
cc -O2 -Wall -o "$BIN" aud.c
mkdir -p out_d7
seq 0 29 | xargs -P "$J" -I{} sh -c "$BIN 7 58 split:{}/30@9 > out_d7/aud_part_{}.txt"
python3 agg.py out_d7/aud_part_*.txt > out_aud_d7.txt
cat out_aud_d7.txt
