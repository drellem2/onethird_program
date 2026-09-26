#!/bin/sh
# mg-785e: regenerate the transcripts and assert the headlines and controls.
# Pure-Python (exact) parts always run (~4 min).  Float probes (scipy/HiGHS) run only if scipy imports;
# set PY_SCIPY to an interpreter that has scipy (e.g. a venv) to re-run them.  They only PROPOSE multipliers /
# probe; every refutation claimed in the doc is re-checked exactly by verify_certs.py.
set -e
cd "$(dirname "$0")"
PY_SCIPY=${PY_SCIPY:-python3}
python3 probe8.py 10      > out_probe8.txt
python3 xyzlp.py          > out_xyzlp.txt
python3 verify_certs.py   > out_verify.txt
if $PY_SCIPY -c "import scipy" 2>/dev/null; then
  $PY_SCIPY bnb.py 400      > out_bnb.txt
  $PY_SCIPY xyzcheck.py     > out_xyzcheck.txt
  $PY_SCIPY mu_q12.py       > out_mu_q12.txt
  $PY_SCIPY mu_q12b.py      > out_mu_q12b.txt
  $PY_SCIPY window.py       > out_window.txt
  $PY_SCIPY window3.py      > out_window3.txt
  $PY_SCIPY local_q12.py    > out_local_q12.txt
  $PY_SCIPY mu_surv.py      > out_mu_surv.txt      # ~15 min
  $PY_SCIPY certify.py      > out_certify.txt      # ~15 min; gen_certs.py rewrites certs.json
  grep -q "^FEASIBLE value 0.01333" out_bnb.txt                     # XYZ does not kill Q12 (float)
  test "$(grep -c REFUTED out_mu_surv.txt)" = 13
  $PY_SCIPY mulp.py        > out_mulp.txt
  grep -q "ADJ (control, uniform => true max delta-margin): -0.1042" out_mulp.txt   # control: uniform reproduces the true margin
else
  echo "scipy not importable: float probes skipped (committed transcripts kept)"
fi
# --- assertions (exact) ---------------------------------------------------------------------------
grep -q "n=9: containment 2-sep pairs with q,u_s,u_t < 1/3: 20" out_probe8.txt
grep -q "twins s=t: 20; non-twin: 0" out_probe8.txt
grep -q "twins s=t: 333; non-twin: 29; min w over non-twin: 49/125" out_probe8.txt
grep -q "+TRI/JT : eps\* = 1/75" out_xyzlp.txt
grep -q "+XYZ(McCormick on L-boxes): eps\* = 1/75" out_xyzlp.txt
grep -q "certificates: 14 valid, 0 invalid" out_verify.txt
grep -q "control c1 (lambda x 9/10): CAUGHT" out_verify.txt
grep -q "control c2 (identities dropped): CAUGHT" out_verify.txt
grep -q "control c3 .*CAUGHT" out_verify.txt
echo "run_all: all assertions passed"
