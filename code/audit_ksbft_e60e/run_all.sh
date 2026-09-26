#!/bin/sh
# run_all.sh (mg-e60e): independent re-computation for docs/AUDIT-mg-f218.md.
# Deterministic, one process at a time, ~10 s for N=3..7 (N=8 only with FULL=1; single core, see out_indep_8.txt for its time).
# Writes then moves, so a failure keeps the committed transcript.
set -e
cd "$(dirname "$0")"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT INT TERM HUP
cc -O2 -Wall -o "$TMP/ind" indep_e60e.c -lm
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }
w out_indep_3to7.txt sh -c "for k in 3 4 5 6 7; do $TMP/ind \$k; done"
w out_indep_3to7_xy.txt sh -c "for k in 4 5 6 7; do $TMP/ind \$k xy; done"
[ -n "$FULL" ] && w out_indep_8.txt "$TMP/ind" 8 xy
w out_family.txt python3 family_e60e.py 11
# verdict lines: every K0/K1/K2/(F-b)/(2.5) count must be 0, every negative control must fire
if grep -h 'viol=' out_indep_*.txt | grep -Ev 'K0 \(gap>=2 possible <=> N nonempty\) viol=0 \| K1 c1<=piN\*c2 viol=0 \| K2 p<=\(piN\+1\)P\[gap>=2\] viol=0 \| NEG CONTROL .* FIRES|\(F-b\) S/2>=C_BFT\+R/\(5\+3sqrt5\) viol=0 \| \(2\.5\) R>=gap\(x,y\)\+gap\(y,z\) viol=0' | grep -q .; then echo "AUDIT CHECK FAILED"; exit 1; fi
grep -q 'ALL OK' out_family.txt
grep -q 'FIRES' out_family.txt
echo "run_all (mg-e60e): all checks 0, negative controls fired"
