#!/bin/sh
# run_all.sh -- regenerate every transcript in out/ (mg-2912).  ~3.5 CPU-hours, ~1.5 h wall.
# Runs the five enumerations and three annealing runs 3 at a time
# (POGO_WORKER_CORES budget), then the readers.  No clock or randomness in the
# enumerations; the annealer is seeded, so its transcripts are reproducible.
set -e
cd "$(dirname "$0")"
clang++ -O2 -std=c++17 -o probe probe.cpp
mkdir -p out
enum() { ( time ./probe enum "$1" "$2" "out/$3" ) > "out/summary_$4.txt" 2>&1; }
enum 11 99 all all_n11 & A=$!
enum 18 3 d3 d3 &       B=$!
enum 15 4 d4 d4 &       C=$!
wait $A $B $C
enum 13 5 d5 d5 &       A=$!
enum 12 6 d6 d6 &       B=$!
./run_search.sh M 11 & C=$!
wait $A $B $C
./run_search.sh M 29 &      A=$!
./run_search.sh delta 13 &  B=$!
wait $A $B
python3 check.py controls > out/controls.txt
python3 check.py rederive out/*_n*.jsonl out/search_*.jsonl > out/rederive.txt
python3 report.py out/summary_all_n11.txt out/summary_d3.txt out/summary_d4.txt out/summary_d5.txt out/summary_d6.txt > out/report.txt
python3 fib.py 81 > out/fib.txt
python3 structure.py 36/100 out/*_n*.jsonl out/search_delta_*.jsonl > out/structure.txt
python3 structure.py 35/100 out/*_n*.jsonl out/search_delta_*.jsonl >> out/structure.txt
python3 searchtab.py out/search_*.jsonl > out/searchtab.txt
python3 d1bound.py 6 out/*_n*.jsonl out/search_*.jsonl > out/d1bound.txt
