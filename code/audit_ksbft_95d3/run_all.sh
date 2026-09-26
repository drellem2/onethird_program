#!/bin/sh
# run_all.sh (mg-95d3): independent audit instrument for mg-eedd (KSBFT-J).  <= 3 processes.
# Regenerates every out_*_95d3.txt.  Poset lists live in a temp dir and are deleted.
set -e
cd "$(dirname "$0")"; HERE=$(pwd)
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT INT TERM HUP
BIN=$T/indep; cc -O2 -Wall -o "$BIN" indep_95d3.c
scan3(){ # scan3 FILE [args...]
  f=$1; shift
  for i in 0 1 2; do "$BIN" scan "$f" $i 3 "$@" > "$T/s$i.txt" & done; wait
  python3 "$HERE/merge_95d3.py" "$T/s0.txt" "$T/s1.txt" "$T/s2.txt"; }
{
echo "== counter vs brute-force permutations (random posets, P and every P-v)"
"$BIN" brute 6 200; "$BIN" brute 7 60; "$BIN" brute 8 10; "$BIN" brute 7 60 ctrl
} > out_controls_95d3.txt
{ "$BIN" gen -1 10 "$T/all_"; echo "A000112 n=1..10: 1 2 5 16 63 318 2045 16999 183231 2567284"; } > "$T/g1.txt" &
"$BIN" gen 3 16 "$T/d3_" > "$T/g3.txt" &
"$BIN" gen 4 13 "$T/d4_" > "$T/g4.txt" &
wait
"$BIN" gen 2 14 "$T/d2_" > "$T/g2.txt"
cat "$T/g1.txt" "$T/g2.txt" "$T/g3.txt" "$T/g4.txt" > out_gen_95d3.txt
python3 classify_pi2_95d3.py "$T/d2_" 14 "$T/d3_" 8 > out_classify_pi2_95d3.txt
python3 sharp_95d3.py > out_sharp_95d3.txt
: > out_census_95d3.txt
for k in 3 4 5 6 7 8 9 10; do echo "#### n=$k ALL non-chains" >> out_census_95d3.txt; scan3 "$T/all_$k.txt" >> out_census_95d3.txt; done
for k in 3 4 5 6 7 8 9 10; do echo "#### n=$k INDECOMPOSABLE non-chains" >> out_census_95d3.txt; scan3 "$T/all_$k.txt" indec >> out_census_95d3.txt; done
for k in 11 12 13 14 15 16; do echo "#### n=$k range<=3 INDECOMPOSABLE" >> out_census_95d3.txt; scan3 "$T/d3_$k.txt" indec >> out_census_95d3.txt; done
for k in 11 12 13; do echo "#### n=$k range<=4 INDECOMPOSABLE" >> out_census_95d3.txt; scan3 "$T/d4_$k.txt" indec >> out_census_95d3.txt; done
# firing controls: interval [2/5,3/5].  exists_v_fail must be > 0; decomp_equiv_mismatch must be 0 (Prop 1.2 is
# interval-free); indec_equiv_mismatch > 0 shows the equivalence test can fire.
: > out_control_narrow_95d3.txt
for k in 3 4 5 6 7 8; do echo "#### n=$k ALL non-chains, interval [2/5,3/5]" >> out_control_narrow_95d3.txt; scan3 "$T/all_$k.txt" 2 5 >> out_control_narrow_95d3.txt; done
for k in 3 4 5 6 7 8; do echo "#### n=$k INDECOMPOSABLE, interval [2/5,3/5]" >> out_control_narrow_95d3.txt; scan3 "$T/all_$k.txt" indec 2 5 >> out_control_narrow_95d3.txt; done
python3 check_95d3.py > out_check_95d3.txt; cat out_check_95d3.txt | tail -1
