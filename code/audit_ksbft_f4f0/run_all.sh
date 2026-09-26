#!/bin/sh
# audit mg-f4f0 (of mg-785e, KSBFT-T3). Regenerates the deterministic transcripts and asserts headlines + controls.
# ~3 min single core. Stochastic probes (kc.py search, xclimb.py) re-run only with PROBES=1 (~25 min at 3 cores).
# FLOAT LP probe lp_indep.py runs only if $PY_SCIPY has scipy.
set -e
cd "$(dirname "$0")"
python3 certs_indep.py > out_certs_indep.txt
grep -q 'certificates: 14 valid, 0 invalid' out_certs_indep.txt
test "$(grep -c ': CAUGHT' out_certs_indep.txt)" -eq 6
grep -q 'valid(ratio<3): True' out_certs_indep.txt
python3 prop11.py 300 200 > out_prop11.txt
grep -q '3580 (pair, F) checks, 0 violations' out_prop11.txt
grep -q '400 (pair, w-order) checks, 0 violations; control A-only: fires on 83' out_prop11.txt
python3 canon_check.py > out_canon_check.txt
grep -q 'not fixed by canonical(): 0' out_canon_check.txt; grep -q '300 / 300' out_canon_check.txt
: > out_xlocal.txt; for n in 5 6 7 8 9 10; do python3 xlocal.py $n >> out_xlocal.txt; done
grep -q 'n=9 .*in region q,u_s,u_t<1/3: 20; twins 20; non-twin 0' out_xlocal.txt
grep -q 'n=10 .*in region q,u_s,u_t<1/3: 362; twins 333; non-twin 29; min w non-twin = 49/125; unbalanced (w<1/3) in region: 0' out_xlocal.txt
python3 mech.py > out_mech.txt
grep -q 'P\[\[2,5\]<\[3,4\]\] = 242/553' out_mech.txt
python3 xfail.py > out_xfail.txt
test "$(grep -c 'X-local form of Lemma C FAILS' out_xfail.txt)" -eq 2
grep -q 'control CAUGHT' out_xfail.txt
python3 lcc12.py > out_lcc12.txt
test "$(grep -c 'LCC on X  .*True' out_lcc12.txt)" -eq 2
python3 prop21.py > out_prop21.txt
python3 kc.py > out_kc.txt
grep -q "{('iii',): 22}" out_kc.txt; grep -q 'FIRES' out_kc.txt
if [ -n "$PROBES" ]; then
  ./run_kcsearch.sh
  python3 kc_ctl.py 150 > out_kc_ctl.txt
  python3 xclimb.py 200 3 11 12 > out_xclimb_n11_12.txt; python3 xclimb.py 200 4 13 13 > out_xclimb_n13.txt
  python3 xclimb.py 180 5 11 11 > out_xclimb_n11.txt; python3 xclimb.py 180 1 11 20 > out_xclimb_n11_20.txt
fi
if ${PY_SCIPY:-python3} -c 'import scipy' 2>/dev/null; then ${PY_SCIPY:-python3} lp_indep.py > out_lp_indep.txt; fi
echo 'audit_ksbft_f4f0: all assertions passed'
