#!/bin/sh
# run_all.sh (mg-9268): regenerate every audit transcript except D=7
# (run_d7.sh).  At most $POGO_WORKER_CORES concurrent processes.
set -e
cd "$(dirname "$0")"
J=${POGO_WORKER_CORES:-3}
T=$(mktemp -d)
cc -O2 -Wall -o "$T/aud" aud.c
cc -O2 -Wall -o "$T/tree" ../ksbft_finite_state/tree.c
# mutant of the AUTHOR's program: certifying cut one too deep (firing control)
python3 - "$T/tree_badcut.c" <<'EOF'
import sys
s = open("../ksbft_finite_state/tree.c").read()
old = "  if (USE_DCUT && d > k) k = d;\n  return k < 0 ? 0 : k;"
assert old in s
open(sys.argv[1], "w").write(s.replace(old, "  if (USE_DCUT && d > k) k = d;\n  k++; if (k > N) k = N;   /* AUDIT MUTANT */\n  return k < 0 ? 0 : k;"))
EOF
cc -O2 -w -o "$T/tree_badcut" "$T/tree_badcut.c"
w(){ out=$1; shift; "$@" > "$out.tmp" && mv "$out.tmp" "$out"; }

# 1. node-for-node comparison aud vs tree.c (per-depth rows)
w out_compare.txt sh -c "
for D in 2 3 4 5; do for m in nolp lp; do M=\$m; [ \$m = lp ] && M=''; printf 'D=%s %-6s ' \$D \$m; sh cmp.sh $T/aud $T/tree \"\$D 58 \$M\" \"\$D 58 1 3 \$M\"; done; done
printf 'D=5 nolp nodcut '; sh cmp.sh $T/aud $T/tree '5 58 nolp nodcut' '5 58 1 3 nolp nodcut'
printf 'D=4 lp nodcut   '; sh cmp.sh $T/aud $T/tree '4 58 nodcut' '4 58 1 3 nodcut'
echo '== D=6 nolp and lp (single process each)'
$T/aud 6 58 nolp > $T/a6n & $T/tree 6 58 1 3 nolp > $T/t6n & $T/aud 6 58 > $T/a6 & wait
awk '/^depth/{print \$2,\$4,\$6,\$8,\$10,\$12}' $T/a6n > $T/x; awk '/^depth/{print \$2,\$4,\$6,\$8,\$10,\$12}' $T/t6n > $T/y
if cmp -s $T/x $T/y; then echo \"D=6 nolp IDENTICAL (\$(awk '{s+=\$2}END{print s}' $T/x) nodes)\"; else echo 'D=6 nolp DIFFER'; fi
echo 'D=6 lp: aud rows vs committed out_d6.txt (tree.c, 30 slices)   depth nodes cert lp cut | depth nodes cert lp cut'
paste \$(printf '%s' $T/a6) /dev/null | awk '/^depth/{print \$2,\$4,\$6,\$8,\$10}' > $T/p; awk '/^depth/{print \$2,\$3,\$4,\$5,\$6}' ../ksbft_finite_state/out_d6.txt > $T/q; paste -d'|' $T/p $T/q
tail -2 $T/a6
echo '== split validation: aud D=5 in 7 slices at depth 9 == unsplit'
for i in 0 1 2 3 4 5 6; do $T/aud 5 58 split:\$i/7@9 > $T/s5_\$i.txt; done
python3 agg.py $T/s5_*.txt | awk '/^depth/{print \$2,\$3,\$4,\$5,\$6,\$7}' > $T/x; $T/aud 5 58 | awk '/^depth/{print \$2,\$4,\$6,\$8,\$10,\$12}' > $T/y
cmp -s $T/x $T/y && echo 'SPLIT == UNSPLIT' || echo 'SPLIT DIFFERS'"

# 2. controls: wrong targets, cut mutants (both programs)
w out_controls.txt sh -c "
echo '== target [34/100, 66/100]: expect exactly the 2+1 forms [0,0,1],[0,0,2], and termination'
for D in 3 4 5; do echo \"-- D=\$D tree.c\"; $T/tree \$D 58 34 100 | grep -E 'COUNTEREX|RESULT|frontier [1-9]'; echo \"-- D=\$D aud\"; $T/aud \$D 58 34 100 | grep -E 'VIOL|RESULT|front [1-9]'; done
echo '== target [39/100, 61/100], D=3, cap 20: expect violations AND a non-empty frontier'
$T/aud 3 20 39 100 | grep -cE VIOL; $T/aud 3 20 39 100 | grep -E 'front [1-9]|RESULT'
echo '== MUTANT tree.c with certifying cut + 1: expect FOUND-VIOLATION'
for D in 3 4 5; do $T/tree_badcut \$D 58 | tail -1; done
echo '== MUTANT aud badcut: search alone stays CLEAN (only the probes can see it)'
for D in 3 4 5; do $T/aud \$D 58 badcut | tail -1; done
echo '== MUTANT aud badcut through the end-to-end probe: expect failures'
for D in 3 5 7; do python3 follow_check.py $T/aud \$D 1000 30 1 exact badcut | grep -E '^D='; done
echo '== the smallest badcut failure, dissected (D=3): P=[0,0,1,1,7,11]'
echo '[0,0,1,1,7,11]' | $T/aud 3 58 follow badcut
echo '[0,0,1,1,7,11]' | $T/aud 3 58 follow
echo '== MUTANT aud badcut through the sample probe: expect SAFE CUT FAILS'
$T/aud 4 58 badcut sample:20 > $T/sb; python3 sample_check.py 4 $T/sb 5 1 | grep -cE 'SAFE CUT|CONCLUSION'"

w out_check_controls.txt python3 check_controls.py out_controls.txt

# 3. end-to-end probes (exhaustive + random)
w out_follow.txt sh -c "
python3 exhaustive_follow.py $T/aud 2 10
python3 exhaustive_follow.py $T/aud 3 9
python3 exhaustive_follow.py $T/aud 4 8
python3 exhaustive_follow.py $T/aud 5 8
python3 exhaustive_follow.py $T/aud 6 8
python3 exhaustive_follow.py $T/aud 7 8
for D in 3 4 5 6 7; do python3 follow_check.py $T/aud \$D 3000 45 \$((100+D)) exact; done
for D in 3 5 7; do python3 follow_check.py $T/aud \$D 1000 30 \$((200+D)); done"

# 4. certificates sampled from real searches, re-verified + random continuations
w out_sample.txt sh -c "
$T/aud 4 58 sample:10 > $T/s4; python3 sample_check.py 4 $T/s4 5 1
$T/aud 5 58 sample:200 > $T/s5; python3 sample_check.py 5 $T/s5 3 2
$T/aud 6 58 sample:20000 > $T/s6; python3 sample_check.py 6 $T/s6 2 3
$T/aud 7 58 split:0/30@9 sample:100000 > $T/s7; python3 sample_check.py 7 $T/s7 2 4"

# 5. layer-size conjecture probe
w out_layer_conj.txt sh -c "python3 layer_conj.py 8 2; python3 layer_conj.py 7 3,4"
rm -rf "$T"
