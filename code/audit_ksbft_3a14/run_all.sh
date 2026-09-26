#!/bin/sh
# run_all.sh (mg-3a14): independent re-computation for docs/AUDIT-mg-d707.md.
# Deterministic, single process.  ~5 min (n=7 exhaustive dominates).
set -e
cd "$(dirname "$0")"
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }
w out_indep_witness.txt python3 indep.py witness
w out_relax.txt python3 relax.py
w out_indep_all3to6.txt sh -c 'for k in 3 4 5 6; do python3 indep.py all $k; done'
w out_indep_all7.txt python3 indep.py all 7
