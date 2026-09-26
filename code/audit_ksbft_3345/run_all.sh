#!/bin/sh
# run_all.sh (audit mg-3345 of mg-5f14): regenerate every transcript cited by docs/AUDIT-mg-3345.md.
# indep.py / extra.py / remark26.py: explicit enumeration of linear extensions (no DP).
# rec44.py / wincount.py: own ideal DP.  Census files d5_9, d6_9 from mg-eedd's generator
# (../ksbft_m_margin_6b81/pcert.c, `onept gen`; control OEIS A000112 reproduced in its gen log).
# At most 2 processes.  ~25 s wall (measured 22 s).
set -e
cd "$(dirname "$0")"
T=$(mktemp -d); PIDS=""
trap 'kill $PIDS 2>/dev/null || true; rm -rf "$T"' EXIT INT TERM HUP
python3 indep.py "3 0 0 2" "5 0 0 2 2 b" "6 0 0 2 2 3 f" "9 0 0 2 2 3 b 2b 2f 7f" "8 0 0 0 4 4 6 16 2f" > out_indep.txt
python3 extra.py > out_extra.txt
python3 remark26.py > out_remark26.txt
python3 rec44.py > out_rec44.txt
cc -O2 -w -o "$T/pcert" ../ksbft_m_margin_6b81/pcert.c
( cd "$T" && ./pcert onept gen - p1.txt > gen.txt && for k in 2 3 4 5 6 7 8; do ./pcert onept gen p$((k-1)).txt p$k.txt >> gen.txt; done
  ./pcert onept gen p8.txt d5_9.txt 5 >> gen.txt; ./pcert onept gen p8.txt d6_9.txt 6 >> gen.txt )
cp "$T/gen.txt" out_gen.txt
python3 wincount.py "$T/d5_9.txt" > out_wincount_d5_9.txt & PIDS="$PIDS $!"
python3 wincount.py "$T/d6_9.txt" > out_wincount_d6_9.txt & PIDS="$PIDS $!"
wait
# assertions: the figures the audit relies on
grep -q "win_fail': 1, 'br_fail': 1" out_wincount_d5_9.txt
grep -q "win_fail': 2, 'br_fail': 4, 'min3_nobal': 46" out_wincount_d6_9.txt
grep -q "'fires': 44, 'j0_att': 44, 'bottom': 41, 'top': 3" out_rec44.txt
grep -q "subset of cap_U {x<u}: False" out_extra.txt      # FIRES: section 3.2 inclusion fails at j=k+1
grep -q "subset of cap_U {x<u}: True" out_extra.txt       # control: holds at j=k
python3 negative_control.py > out_negative_control.txt
echo "audit mg-3345: all assertions hold"
