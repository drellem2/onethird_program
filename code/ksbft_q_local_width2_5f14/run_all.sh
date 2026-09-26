#!/bin/sh
# run_all.sh (mg-5f14): regenerate every transcript cited by docs/KSBFT-Q-local-width2.md.
# Census files come from mg-eedd's generator (../ksbft_one_pt/onept.c via ../ksbft_m_margin_6b81/pcert.c,
# `onept gen`, positive control OEIS A000112) and live in a temp dir.  At most 3 processes
# (POGO_WORKER_CORES); ~1 h wall at 3 cores, most of it d5_11 and d6_10.  Deterministic.
set -e
cd "$(dirname "$0")"
HERE=$(pwd)
T=$(mktemp -d)
PIDS=""
trap 'kill $PIDS 2>/dev/null; rm -rf "$T"' EXIT INT TERM HUP
cc -O2 -w -o "$T/pcert" ../ksbft_m_margin_6b81/pcert.c
cd "$T"
./pcert onept gen - p1.txt > gen.txt; for k in 2 3 4 5 6 7 8 9; do ./pcert onept gen p$((k-1)).txt p$k.txt >> gen.txt; done
for D in 3 4 5 6; do cp p8.txt d${D}_8.txt; done
for k in 9 10 11 12 13; do ./pcert onept gen d3_$((k-1)).txt d3_$k.txt 3 >> gen.txt; done
for k in 9 10 11 12; do ./pcert onept gen d4_$((k-1)).txt d4_$k.txt 4 >> gen.txt; done
for k in 9 10 11; do ./pcert onept gen d5_$((k-1)).txt d5_$k.txt 5 >> gen.txt; done
for k in 9 10; do ./pcert onept gen d6_$((k-1)).txt d6_$k.txt 6 >> gen.txt; done
cp gen.txt "$HERE/out_gen.txt"
cd "$HERE"
( for f in p3 p4 p5 p6 p7 p8 p9; do python3 probe.py "$T/$f.txt"; done > out_all.txt ) & PIDS="$PIDS $!"
( for k in 9 10 11 12 13; do python3 probe.py "$T/d3_$k.txt"; done > out_d3.txt
  for k in 9 10 11 12; do python3 probe.py "$T/d4_$k.txt"; done > out_d4.txt ) & PIDS="$PIDS $!"
( for k in 9 10 11; do python3 probe.py "$T/d5_$k.txt"; done > out_d5.txt
  for k in 9 10; do python3 probe.py "$T/d6_$k.txt"; done > out_d6.txt ) & PIDS="$PIDS $!"
wait
{ NEGCTRL=1 python3 probe.py "$T/p3.txt" "$T/p4.txt" "$T/p5.txt" "$T/p6.txt" "$T/p7.txt" | grep -h "file\|LL_VIOL\|MONO"
  MONOCTRL=1 python3 probe.py "$T/p3.txt" "$T/p5.txt" | grep -h "file\|MONO" | grep -v WIT; } > out_negctrl.txt
python3 min3.py "$T/p7.txt" "$T/p8.txt" "$T/p9.txt" > out_min3.txt
python3 records.py > out_records.txt
python3 show.py "3 0 0 2" "5 0 0 2 2 b" "6 0 0 2 2 3 f" "9 0 0 2 2 3 b 2b 2f 7f" "8 0 0 0 4 4 6 16 2f" \
  "11 0 0 2 2 3 b 2b 2f af bf 1ff" > out_witnesses.txt
python3 summary.py > out_summary.txt
cat out_summary.txt
