#!/bin/sh
# run_all.sh (mg-f218): regenerate every transcript cited by
# docs/KSBFT-H-lemma-W.md.  Deterministic (no randomness, no clock).
# At most 3 concurrent processes (POGO_WORKER_CORES=3).  ~5 min (n=8 dominates).
set -e
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT INT TERM HUP
cc -O2 -Wall -o "$TMP/lemw" lemw.c
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }
w out_lemw_3to7.txt sh -c "for k in 3 4 5 6 7; do $TMP/lemw \$k; done"
w out_lemw_8.txt "$TMP/lemw" 8 &
w out_window.txt python3 window.py &
w out_fibw.txt python3 fibw.py 6 &
wait
# the censuses' verdict lines must read 0 / >0; a transcript that says otherwise fails the run
if grep -h 'violations=' out_lemw_3to7.txt out_lemw_8.txt | grep -v 'must be' | grep -vq 'violations=0  K1 (c1<=piN\*c2) violations=0  K2 (p<=(pi+1)P\[gap>=2\]) violations=0'; then echo "LEMMA W CHECK FAILED"; exit 1; fi
if grep -h 'K1m' out_lemw_3to7.txt out_lemw_8.txt | grep -q 'violations=0 '; then echo "NEGATIVE CONTROL DID NOT FIRE"; exit 1; fi
echo "run_all: K0/K1/K2 = 0 for N=3..8, negative control fired"
