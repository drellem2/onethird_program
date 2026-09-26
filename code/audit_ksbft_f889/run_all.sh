#!/bin/sh
# run_all.sh (mg-f889): independent audit instrument for mg-6b81 (KSBFT-M).  Serial, 1 process.
# indep_f889.py shares NO code with pcert.c/onept.c.  Step 5 alone re-runs the AUTHOR's pcert (to
# obtain the t=14/15 lists, which are too large for indep_f889.py to generate) and then applies MY
# certifier to a 1% stride sample of pcert's t=15 list.  ~70 min; ~1 GB of temp files, deleted.
set -e
cd "$(dirname "$0")"; HERE=$(pwd)
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT INT TERM HUP
export OUT=$T
P=python3
# 1. generator: canonical-form control (A000112), unpruned census filtered by CUT, pruned lists
$P indep_f889.py full 8 8 > out_a000112.txt
AUDIT_BROKEN_CANON=1 $P indep_f889.py full 8 5 > out_control_brokencanon.txt
$P indep_f889.py full 3 12 > out_full3.txt
$P indep_f889.py gen 3 13 > out_gen3.txt
$P indep_f889.py gen 4 13 > out_gen4.txt
# 2. certificates (Theorem 2.4) D=3 t=9..12, D=4 t=10..13, and the narrowed-interval firing control
{ for t in 9 10 11 12; do $P indep_f889.py cert 3 $t; done; $P indep_f889.py cert 3 11 8; } > out_cert3.txt
{ for t in 10 11 12 13; do $P indep_f889.py cert 4 $t; done; } > out_cert4.txt
AUDIT_LO=2/5 $P indep_f889.py cert 3 11 > out_control_narrow.txt
# 3. base cases and the exceptional list
$P indep_f889.py base 3 11 > out_base3.txt
$P indep_f889.py gen 8 8 > /dev/null; $P indep_f889.py base 8 8 > out_base_all8.txt
$P witness_f889.py > out_witness.txt
# 4. Theorem 2.4 end to end on random large P, and its firing control (s = t-D+1)
{ $P indep_f889.py e2e 3 11 22 40 0; $P indep_f889.py e2e 3 11 22 40 1; $P indep_f889.py e2e 3 11 30 15 0
  $P indep_f889.py e2e 4 15 22 6 0; $P indep_f889.py e2e 4 15 22 6 1; } > out_e2e.txt
# 5. D=4 at t=14,15: lists from the AUTHOR's generator; the author's cert re-run; MY certifier on
#    pcert's 14 t=14 failures, its named t=14/15 extremes, and a 1% stride sample of t=15
cc -O2 -w -o "$T/pcert" ../ksbft_m_margin_6b81/pcert.c
cd "$T"; ./pcert gencut - p4_1.txt 4 > pgen4.txt
for k in $(seq 2 15); do ./pcert gencut p4_$((k-1)).txt p4_$k.txt 4 >> pgen4.txt; done
./pcert cert p4_14.txt 0 1 4 > pc14.txt; ./pcert cert p4_15.txt 0 1 4 | grep -v '^FAIL' > pc15.txt
for k in 12 13 14 15; do echo "## D=4 n=$k"; ./pcert delta p4_$k.txt 0 1 0/1; done > pdelta.txt
grep '^FAIL' pc14.txt | sed 's/.*Q=//; s/ best.*//' > fail14.txt
awk 'NR%100==37' p4_15.txt > samp15.txt
cd "$HERE"
{ echo "== author's pcert, re-run (NOT independent)"; cat "$T/pgen4.txt"; grep -v '^FAIL' "$T/pc14.txt"; cat "$T/pc15.txt"; cat "$T/pdelta.txt"; } > out_pcert_rerun.txt
for t in 14 15; do grep "AGG CW $t" ../ksbft_m_margin_6b81/out_cert_d4.txt | awk '{for(i=6;i<=NF;i++) printf "%s ",$i; print ""}' > "$T/w$t.txt"; done
{ $P indep_f889.py sample 4 14 "$T/fail14.txt" 100 1
  $P indep_f889.py sample 4 14 "$T/w14.txt" 1 1
  $P indep_f889.py sample 4 15 "$T/w15.txt" 1 1
  $P indep_f889.py sample 4 15 "$T/samp15.txt" 1000000 1; } > out_sample_d4.txt
# 6. assert everything
$P check_controls_f889.py > out_check_controls_f889.txt
