#!/bin/sh
# run_all.sh (mg-d707): regenerate every transcript cited by
# docs/KSBFT-B-case-c-attack.md.  Deterministic (fixed seeds, no clock).
# Budget: at most 3 concurrent processes (POGO_WORKER_CORES=3).  ~2 min.
set -e
cd "$(dirname "$0")"
BIN=$(mktemp -d)/census
cc -O2 -Wall -o "$BIN" census.c -lm
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }
w out_census_all.txt sh -c "for k in 2 3 4 5 6 7 8; do $BIN all \$k; done"
w out_fib.txt sh -c "for m in 1 2 3 5 8; do $BIN fib \$m | head -3; done"
w out_local_model.txt python3 local_model.py
w out_threshold.txt python3 threshold.py
BINX=$BIN
export BINX
w out_search_M.txt  sh -c 'for n in 10 14 18; do for D in 3 4 5 6 7 8 9; do for s in 1 2 3; do $BINX search $n $D 120000 $s M  | head -1; done; done; done' &
w out_search_B4.txt sh -c 'for n in 10 14 18; do for D in 3 4 5 6 7 8 9; do for s in 1 2 3; do $BINX search $n $D 120000 $s B4 | head -1; done; done; done' &
w out_search_B5.txt sh -c 'for n in 10 14 18; do for D in 3 4 5 6 7 8 9; do for s in 1 2 3; do $BINX search $n $D 120000 $s B5 | head -1; done; done; done' &
wait
w out_search_B6.txt sh -c 'for n in 10 14 18; do for D in 3 4 5 6 7 8 9; do for s in 1 2 3; do $BINX search $n $D 120000 $s B6 | head -1; done; done; done' &
w out_search_delta.txt sh -c 'for n in 10 14 18; do for D in 3 4 5 6 7 8 9; do for s in 1 2 3; do $BINX search $n $D 120000 $s delta | head -1; done; done; done' &
wait
# summary: per (n, D) the best value over seeds
w out_search_summary.txt sh -c 'for f in M B4 B5 B6 delta; do echo "== objective $f: min over 3 seeds, by (n, D)"; awk "{split(\$2,a,\"=\");split(\$3,b,\"=\");split(\$5,c,\"=\"); k=a[2]\" \"b[2]; if(!(k in m)||c[2]<m[k])m[k]=c[2]} END{for(k in m)print \"n=\" k \" best=\" m[k]}" out_search_$f.txt | sort -t= -k2 -n | sort -n -k1.3 -k2.3; done'
rm -rf "$(dirname "$BIN")"
