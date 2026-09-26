#!/bin/sh
# run_all.sh (mg-ce69): regenerate every transcript cited by docs/KSBFT-Q2-both-ends.md.
# Census files come from mg-eedd's generator (../ksbft_one_pt/onept.c via ../ksbft_m_margin_6b81/pcert.c,
# `onept gen`, positive control OEIS A000112 in out_gen.txt) and live in a temp dir that is deleted.
# At most 3 processes (POGO_WORKER_CORES).  ~6 min wall.  Deterministic.  Exits 1 if a PROVEN check is
# violated or a firing control does not fire.
set -e
cd "$(dirname "$0")"
HERE=$(pwd)
T=$(mktemp -d)
PIDS=""
trap 'kill $PIDS 2>/dev/null; rm -rf "$T"' EXIT INT TERM HUP
cc -O2 -w -o "$T/pcert" ../ksbft_m_margin_6b81/pcert.c
cd "$T"
./pcert onept gen - p1.txt > gen.txt; for k in 2 3 4 5 6 7 8 9; do ./pcert onept gen p$((k-1)).txt p$k.txt >> gen.txt; done
cp p8.txt d3_8.txt; cp p8.txt d4_8.txt
for k in 9 10 11 12; do ./pcert onept gen d3_$((k-1)).txt d3_$k.txt 3 >> gen.txt; done
for k in 9 10 11; do ./pcert onept gen d4_$((k-1)).txt d4_$k.txt 4 >> gen.txt; done
split -l 61077 p9.txt p9part_
cp gen.txt "$HERE/out_gen.txt"
cd "$HERE"
P="$T/p3.txt $T/p4.txt $T/p5.txt $T/p6.txt $T/p7.txt $T/p8.txt"
# lane 1: gadget lemmas + swap ladder n<=8 + n=9 part aa
( python3 gadget.py $P > out_gadget.txt
  python3 swapladder.py $P $T/p9part_aa > out_swapladder_1.txt ) & PIDS="$PIDS $!"
( python3 swapladder.py $T/p9part_ab $T/p9part_ac > out_swapladder_2.txt
  python3 goodpair.py $P $T/p9part_aa $T/p9part_ab $T/p9part_ac > out_goodpair.txt ) & PIDS="$PIDS $!"
( python3 slstruct.py $P $T/p9part_aa $T/p9part_ab $T/p9part_ac > out_slstruct.txt
  python3 slstruct.py $T/d3_9.txt $T/d3_10.txt $T/d3_11.txt $T/d3_12.txt $T/d4_9.txt $T/d4_10.txt $T/d4_11.txt > out_slstruct_range.txt ) & PIDS="$PIDS $!"
wait
python3 goodpair.py --records > out_goodpair_records.txt
python3 slrecords.py > out_slrecords.txt
python3 longtail.py > out_longtail.txt
python3 bothends.py > out_bothends.txt
python3 ablate.py > out_ablate.txt
python3 witness.py > out_witness.txt
python3 explain.py > out_explain.txt
python3 summary.py | tee out_summary.txt
