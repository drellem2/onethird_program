#!/bin/sh
# run_all.sh (mg-e8b4): regenerate every transcript cited by
# docs/KSBFT-I-finite-state.md.  Deterministic (fixed seeds; the split is a
# deterministic round-robin).  Budget: at most 3 concurrent processes.
#   default:        controls + D<=6            (~2 min on this host)
#   RUN_D7=1 sh run_all.sh   also re-runs D=7 (120 slices, ~2 h wall on 3 cores)
set -e
cd "$(dirname "$0")"
J=${POGO_WORKER_CORES:-3}
TMP=$(mktemp -d)
BIN=$TMP/tree
cc -O2 -Wall -o "$BIN" tree.c
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }

# --- generation control: tree (certification off) == brute force, n <= 7, all D
w out_gen_control.txt python3 gen_control.py "$BIN" 7
# --- implementation control: independent Python re-implementation, same rules, D <= 4
w out_indep_tree.txt sh -c "for D in 2 3 4; do python3 indep_tree.py \$D 40 | grep ^depth | awk '{print \$2,\$4,\$6,\$8}' > $TMP/py_\$D; $BIN \$D 40 1 3 nolp | grep ^depth | awk '{print \$2,\$4,\$6,\$10}' > $TMP/c_\$D; echo \"== D=\$D  (depth nodes certified cutpruned): python vs C nolp\"; paste $TMP/py_\$D $TMP/c_\$D; if [ -s $TMP/py_\$D ] && cmp -s $TMP/py_\$D $TMP/c_\$D; then echo \"D=\$D IDENTICAL\"; else echo \"D=\$D DIFFER\"; fi; done"
# --- firing controls: each MUST print a failure / violation line
w out_controls.txt sh -c "
echo '== badcert (certify from one state only; UNSOUND on purpose) -> expect CHECK FAILED'; $BIN 4 45 1 3 check badcert | grep -m1 -E 'CHECK|RESULT';
echo '== badlp (accept LP value > -0.02 unverified; UNSOUND on purpose) -> expect CHECK FAILED'; $BIN 5 45 1 3 check badlp | grep -m1 -E 'CHECK|RESULT';
echo '== threshold 0.39 (> 1/3), depth cap 12 -> expect COUNTEREXAMPLE-TO-THRESHOLD lines'; $BIN 3 12 39 100 | grep -c COUNTEREXAMPLE-TO-THRESHOLD; $BIN 3 12 39 100 | grep -m2 COUNTEREXAMPLE;
echo '== soundness checks (own completion + 4 random canonical continuations per certified node), D<=5 -> expect clean';
for D in 2 3 4 5; do $BIN \$D 45 1 3 check | grep -E 'check mode|RESULT|FAIL'; done"
# --- the searches: D <= 5 single process, with and without the LP
w out_d1to5.txt sh -c "for D in 1 2 3 4 5; do $BIN \$D 58; done; for D in 4 5; do echo \"== D=\$D without LP\"; $BIN \$D 58 1 3 nolp | tail -4; echo \"== D=\$D without LP and without the d(last) cut\"; $BIN \$D 58 1 3 nolp nodcut | tail -4; done"
# --- D = 6: 30 slices
mkdir -p "$TMP/d6"
seq 0 29 | xargs -P "$J" -I{} sh -c "$BIN 6 58 1 3 split:{}/30@8 > $TMP/d6/part_{}.txt 2>/dev/null"
w out_d6.txt python3 aggregate.py 8 "$TMP"/d6/part_*.txt
# --- decay measurement (Q3)
w out_decay.txt python3 decay.py
# --- D = 7: 120 slices (opt-in; the committed out_d7/ is the run cited in the doc)
if [ "${RUN_D7:-0}" = 1 ]; then
  mkdir -p out_d7
  seq 0 119 | xargs -P "$J" -I{} sh -c "$BIN 7 58 1 3 split:{}/120@9 > out_d7/part_{}.txt 2>/dev/null"
fi
w out_d7.txt python3 aggregate.py 9 out_d7/part_*.txt
rm -rf "$TMP"
