#!/bin/sh
# run_all.sh (audit mg-5ecf of mg-afa4 / KSBFT-T). ~3.5 min at POGO_WORKER_CORES=3. Exit 1 on any failed assertion.
# Independent engine (eng.py); shares no code with code/ksbft_t_interval_orders_afa4. Witness constructors only are
# imported read-only from mg-ce69 (Q_m) and mg-7bfc (hosts).
set -e
cd "$(dirname "$0")"
python3 controls.py     > out_controls.txt
python3 census_k.py 10  > out_census_k.txt
python3 census_delta.py 9 > out_census_delta.txt
python3 witnesses.py    > out_witnesses.txt
python3 props.py        > out_props.txt
python3 sl.py           > out_sl.txt
python3 misc.py         > out_misc.txt
# controls fire
grep -q "RESULT all controls pass" out_controls.txt
grep -q "CONTROL planted +1 in N\[0\]\[1\] detected: True" out_controls.txt
grep -q "badL found = True; author's L valid = True, bad = True" out_controls.txt
grep -q "violations = 653 (must be > 0)" out_witnesses.txt
grep -q "RESULT Thm 2.1(b) never violated; control fires" out_witnesses.txt
grep -q "RESULT pass" out_props.txt
grep -q "CONTROL planted SL2 violation rejected: True" out_sl.txt
grep -q "CONTROL (l(x) < l(y)) failures = [1-9]" out_misc.txt
# the author's headline figures, reproduced
grep -q "n=8: 5334 non-chain interval orders; bad L (any) = 0; bad L (dominance) = 0" out_census_k.txt
grep -q "n=9: 31239 non-chain interval orders; bad L (any) = 2; bad L (dominance) = 2" out_census_k.txt
grep -q "n=10: 201607 non-chain interval orders; bad L (any) = 26; bad L (dominance) = 24" out_census_k.txt
grep -q "n=10: posets with a bad dominance-L: 24, bad dominance-L total: 29; surviving SL1/SL2 + duals: 16 posets, 20 L" out_sl.txt
grep -q "n=9: population 5198" out_census_delta.txt
grep -q "failures: C1 = 934, C2 = 163, C7 = 3" out_census_delta.txt
grep -q "Doubling in interval form: .* violations = 0" out_misc.txt
echo "run_all: all assertions passed"
