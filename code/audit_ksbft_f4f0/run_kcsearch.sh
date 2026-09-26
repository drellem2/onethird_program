#!/bin/sh
# 2 shards x 400 s (core budget 3; the third core is left for the X-local hill-climb)
PIDS=""; trap 'kill $PIDS 2>/dev/null; exit' EXIT INT TERM HUP
python3 kc.py 400 11 > out_kcsearch_s11.txt 2>&1 & PIDS="$PIDS $!"
python3 kc.py 400 12 > out_kcsearch_s12.txt 2>&1 & PIDS="$PIDS $!"
wait
