#!/bin/sh
# mg-561a: regenerate every transcript and assert the headline facts and controls. ~6 min at POGO_WORKER_CORES=3.
# csearch.py is a stochastic search and is NOT re-run here (out_csearch_s*.txt are its transcripts; s1-s3 were
# produced before the T11 seed was added, s11-s13 after).  Its finding, T11, is re-derived exactly by tiefam.py.
set -e
cd "$(dirname "$0")"
python3 xlp.py > /dev/null
python3 verify.py 8     > out_verify.txt
python3 verify3.py 8    > out_verify3.txt
python3 localcc.py 9    > out_localcc.txt
python3 enlarge.py 9    > out_enlarge.txt
python3 shape.py 9      > out_shape.txt
python3 contprobe.py 9  > out_contprobe.txt
python3 tiefam.py 14    > out_tiefam.txt
python3 kprime.py 10    > out_kprime.txt
python3 kts.py 10 20000 > out_kts.txt
python3 kstar.py 10     > out_kstar.txt
python3 general.py 20000 > out_general.txt
python3 kstar_gen.py 20000 > out_kstar_gen.txt
python3 lpcheck.py      > out_lpcheck.txt
python3 iis.py O9a      > out_iis_O9a.txt
python3 iis.py O9b      > out_iis_O9b.txt
python3 iis.py S10      > out_iis_S10.txt
python3 lpsurv.py       > out_lpsurv.txt
# --- assertions ---------------------------------------------------------------------------------
# Swap Identity: 0 violations everywhere; control (above-separators only) fires
! grep -q "'v1bad': [1-9]" out_verify.txt
grep -q "'v1ctrl': [1-9]" out_verify.txt
! grep -q "'v2bad': [1-9]" out_verify.txt
! grep -q "'v3bad': [1-9]" out_verify.txt
grep -q "'v3zbad': [1-9]" out_verify.txt            # Prop 2.2 genuinely needs Z = S (control)
# Thm 3.1 inequality: 0 violations; over-cancellation control fires
! grep -q "Thm 3.1 inequality violations [1-9]" out_verify3.txt
grep -q "CONTROL (over-cancellation) violations [1-9]" out_verify3.txt
# no-go: the 5-element path semiorder carries a locally compatible AB configuration
grep -q "n=5: .*LCC {'AB': 1}" out_localcc.txt
# containment two-separator pairs are never locally compatible for n <= 9
! grep -q "CONT_IN'): \[[0-9]*, [0-9]*, [1-9]" out_shape.txt
grep -q "slack > 0: 0; slack = 0: 1" out_tiefam.txt
# baseline reproduces mg-afa4 (control), and Lemma C kills everything
grep -q "census n=9: 31239 non-chain posets; posets with an R-bad dominance L: K 2, KC 0" out_kprime.txt
grep -q "census n=10: 201607 non-chain posets; posets with an R-bad dominance L: K 24, KC 0" out_kprime.txt
grep -q "n=10..13: 6634 non-chain posets; posets with an R-bad dominance L: K 547, KC 0" out_kprime.txt
# the PROVEN lemmas kill every K-bad L of the census n <= 10
grep -q "census n=9 .*2 posets, 2 K-bad dominance L; killed by {'TS': 2}; posets with a surviving L: 0" out_kstar.txt
grep -q "census n=10 .*24 posets, 29 K-bad dominance L; killed by {'3.1\*': 1, 'TS': 28}; posets with a surviving L: 0" out_kstar.txt
grep -q "staircase .*posets with a surviving L: 21" out_kstar.txt
# LP: O9a / O9b refuted by T1; the instrument is not trivially refuting (some survivors stay feasible)
grep -q "O9a                tools T1        : max eps = 0 " out_lpcheck.txt
grep -q "O9b                tools T1        : max eps = 0 " out_lpcheck.txt
grep -q "SUMMARY refuted/total per tool set: {'T1': '2/22', 'T1+T2': '2/22', 'T1+T2+T3': '9/22'}" out_lpsurv.txt
echo "run_all: all assertions passed"
