#!/bin/sh
# run_all.sh (mg-eedd): regenerate every transcript cited by docs/KSBFT-J-one-pt.md.
# Deterministic (no clock, fixed seed in `brute`).  Budget: at most 3 concurrent processes
# (POGO_WORKER_CORES=3).  ~12 min on this host, ~7 of them in the range<=3 n=16 generation.
# Poset lists (up to ~250 MB) live in a temp dir and are deleted; only transcripts are kept.
set -e
cd "$(dirname "$0")"
HERE=$(pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT INT TERM HUP
BIN=$T/onept
cc -O2 -Wall -o "$BIN" onept.c
w(){ out=$1; shift; "$@" > "$T/out.tmp" && mv "$T/out.tmp" "$HERE/$out"; }
scan3(){ # scan3 FILE TAG [indec] -> merged table on stdout
  for i in 0 1 2; do "$BIN" scan "$1" $i 3 $3 > "$T/$2_$i.txt" & done; wait
  python3 "$HERE/merge.py" "$T/$2_0.txt" "$T/$2_1.txt" "$T/$2_2.txt"; }

# 1. controls on the counter itself
w out_controls.txt sh -c "
  echo '== fib: exact P[x2<x1] in the Fibonacci poset F_M must equal f(M-1)/f(M+1)';
  for m in 1 2 3 4 5 6 7 8 10 15 20; do $BIN fib \$m; done;
  echo '== brute: ideal-DP counts vs brute-force permutation counts, P and every P-v';
  $BIN brute 6 300; $BIN brute 7 100; $BIN brute 8 20;
  echo '== W*(4,4,2) of mg-3af9/mg-b447 (c1<c2<{x,y}; b1<..<b4; A<B except x<b1,x<b2), labels c1 c2 x y b1 b2 b3 b4 = bits 0..7';
  echo '   expected: every-v FAILS, and the failing v are exactly bits 2 (x) and 4 (b1): W = eb';
  printf '8 0 1 3 3 b 1b 3f 7f\n' > $T/wstar.txt; ONEPT_PRINT_EVERY=1 $BIN scan $T/wstar.txt 0 1 | grep -v '^AGG'"

# 2. exhaustive: every isomorphism class, n = 3..10 (the generator's count is checked against A000112)
"$BIN" gen - "$T/p1.txt" > "$T/gen.txt"
for k in 2 3 4 5 6 7 8 9 10; do "$BIN" gen "$T/p$((k-1)).txt" "$T/p$k.txt" >> "$T/gen.txt"; done
w out_gen_all.txt sh -c "cat $T/gen.txt; echo 'A000112 (n=1..10): 1 2 5 16 63 318 2045 16999 183231 2567284'"
: > "$HERE/out_census_all.txt"; : > "$HERE/out_census_indec.txt"
for k in 3 4 5 6 7 8 9 10; do
  { echo "######## n=$k, ALL non-chains (every isomorphism class)"; scan3 "$T/p$k.txt" a$k; } >> "$HERE/out_census_all.txt"
  { echo "######## n=$k, INDECOMPOSABLE non-chains (incomparability graph connected)"; scan3 "$T/p$k.txt" i$k indec; } >> "$HERE/out_census_indec.txt"
done

# 3. firing control: narrow the interval to [2/5, 3/5]; exists-v must now FAIL somewhere.
#    The subshell matters: in POSIX sh an assignment prefixed to a FUNCTION call persists after
#    it returns, and a first version of this script ran section 4 under the narrow interval.
: > "$HERE/out_control_narrow.txt"
for k in 3 4 5 6 7 8; do
  { echo "######## n=$k, INDECOMPOSABLE, interval [2/5,3/5] (CONTROL: exists-v row must be nonzero)"; ( ONEPT_LO=2/5; export ONEPT_LO; scan3 "$T/p$k.txt" c$k indec ); } >> "$HERE/out_control_narrow.txt"
done

[ -z "$ONEPT_LO" ] || { echo "ONEPT_LO leaked into section 4" >&2; exit 1; }
# 4. range-restricted classes past n = 10: range <= 3 to n = 16, range <= 4 to n = 13
cp "$T/p8.txt" "$T/d3_8.txt"; : > "$T/g3.txt"
for k in 9 10 11 12 13 14 15 16; do "$BIN" gen "$T/d3_$((k-1)).txt" "$T/d3_$k.txt" 3 >> "$T/g3.txt"; done
cp "$T/p10.txt" "$T/d4_10.txt"; : > "$T/g4.txt"
for k in 11 12 13; do "$BIN" gen "$T/d4_$((k-1)).txt" "$T/d4_$k.txt" 4 >> "$T/g4.txt"; done
w out_gen_range.txt cat "$T/g3.txt" "$T/g4.txt"
rm -f "$T"/p[1-9].txt "$T"/p10.txt
: > "$HERE/out_census_range.txt"
for k in 11 12 13 14 15 16; do
  { echo "######## n=$k, range <= 3, INDECOMPOSABLE"; scan3 "$T/d3_$k.txt" r3$k indec; } >> "$HERE/out_census_range.txt"
done
for k in 11 12 13; do
  { echo "######## n=$k, range <= 4, INDECOMPOSABLE"; scan3 "$T/d4_$k.txt" r4$k indec; } >> "$HERE/out_census_range.txt"
done
