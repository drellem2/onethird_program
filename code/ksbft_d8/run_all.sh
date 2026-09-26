#!/bin/bash
# run_all.sh (mg-c493): regenerate every transcript cited by
# docs/KSBFT-N-d8-feasibility.md.  At most $POGO_WORKER_CORES (default 3)
# concurrent processes.  About 15 minutes on this host.  Does NOT run D = 8.
#   out_memo_d2to5.txt   memo DP vs tree, D = 2..5, per-depth transcripts diffed
#   out_memo_d6.txt      memo DP vs tree at D = 6 (single process each)
#   out_control039.txt   threshold 0.39: tree, memo, memo:0 must all FAIL identically
#   out_memocheck.txt    every memo hit re-explored and compared (0 mismatches expected);
#                        the UNSOUND structural-only key (badmemo) must show mismatches
#   out_keystat_d*.txt   distinct future keys (M floor, S structural, X exact) per depth
#   out_projection.txt   D = 8 projection from D = 4..7
set -e
cd "$(dirname "$0")"
J=${POGO_WORKER_CORES:-3}
TMP=$(mktemp -d)
PIDS=(); trap 'kill "${PIDS[@]}" 2>/dev/null; rm -rf "$TMP"' EXIT INT TERM HUP
BIN=$TMP/dp
cc -O2 -Wall -o "$BIN" dp.c
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }
F='^depth|RESULT|counterexamples|total nodes'

# --- memo DP must reproduce the tree exactly (same per-depth node/cert/lp/cut counts)
w out_memo_d2to5.txt bash -c "for D in 2 3 4 5; do for m in memo memo:0; do
  $BIN \$D 58 > $TMP/t; $BIN \$D 58 1 3 \$m > $TMP/m
  echo \"== D=\$D \$m\"; grep -E 'memo \\(' $TMP/m; grep -E 'RESULT' $TMP/m
  if diff <(grep -E '$F' $TMP/t) <(grep -E '$F' $TMP/m) > /dev/null; then echo \"D=\$D \$m IDENTICAL to tree\"; else echo \"D=\$D \$m DIFFERS from tree\"; fi
done; done"
# --- firing control: threshold 0.39 must FAIL (FOUND-VIOLATION), identically with and without memo
w out_control039.txt bash -c "for m in run memo memo:0; do $BIN 3 12 39 100 \$m > $TMP/c_\$m; echo \"== D=3 cap 12 threshold 0.39 mode \$m\"; grep -E 'memo \\(|found|RESULT' $TMP/c_\$m; grep -m2 COUNTEREXAMPLE $TMP/c_\$m; done
  for m in memo memo:0; do if cmp -s <(grep -E '$F' $TMP/c_run) <(grep -E '$F' $TMP/c_\$m); then echo \"control \$m IDENTICAL to tree (and FAILS)\"; else echo \"control \$m DIFFERS\"; fi; done"
# --- memo self-check and its firing control
w out_memocheck.txt bash -c "for D in 3 4 5; do echo \"== D=\$D memocheck (exact key)\"; $BIN \$D 58 1 3 memocheck | grep -E 'memocheck|MISMATCH|RESULT';
  echo \"== D=\$D memocheck badmemo (structural key only; UNSOUND on purpose) -> expect mismatches\"; $BIN \$D 58 1 3 memocheck badmemo | grep -E 'memocheck|MISMATCH|RESULT'; done
  echo '== D=5 badmemo without check: per-depth counts vs tree'; $BIN 5 58 > $TMP/tb5; $BIN 5 58 1 3 memo badmemo > $TMP/mb5
  if diff <(grep -E '$F' $TMP/tb5) <(grep -E '$F' $TMP/mb5) > /dev/null; then echo 'badmemo IDENTICAL to tree (control did not fire)'; else echo 'badmemo DIFFERS from tree (control fires)'; diff <(grep -E '$F' $TMP/tb5) <(grep -E '$F' $TMP/mb5) | head -6; fi"
# --- D = 6: tree, memo and memocheck in parallel
( $BIN 6 58 > $TMP/t6 ) & P1=$!; PIDS+=($P1)
( $BIN 6 58 1 3 memo > $TMP/m6 ) & P2=$!; PIDS+=($P2)
( $BIN 6 58 1 3 memocheck > $TMP/c6 ) & P3=$!; PIDS+=($P3)
wait $P1 $P2 $P3
grep -E 'memocheck|MISMATCH|RESULT' $TMP/c6 | sed 's/^/D=6 /' >> out_memocheck.txt
w out_memo_d6.txt bash -c "grep -E 'memo \\(' $TMP/m6; cat $TMP/m6 | grep -E '$F'; if diff <(grep -E '$F' $TMP/t6) <(grep -E '$F' $TMP/m6) > /dev/null; then echo 'D=6 memo IDENTICAL to tree'; else echo 'D=6 memo DIFFERS from tree'; fi"
# --- key statistics D = 3..6 (full trees) and two D = 7 slices
for D in 3 4 5 6; do w out_keystat_d$D.txt $BIN $D 58 1 3 keystat; done
seq 0 1 | xargs -P "$J" -I{} bash -c "$BIN 7 58 1 3 split:{}/120@9 keystat > $TMP/ks7_{}.txt 2>/dev/null"
cat $TMP/ks7_0.txt $TMP/ks7_1.txt > out_keystat_d7_slices.txt
seq 0 1 | xargs -P "$J" -I{} bash -c "$BIN 6 58 1 3 split:{}/30@8 keystat > $TMP/ks6_{}.txt 2>/dev/null"
cat $TMP/ks6_0.txt $TMP/ks6_1.txt > out_keystat_d6_slices.txt
w out_projection.txt python3 project.py
