#!/bin/sh
# run_all.sh (mg-6b81): regenerate every transcript cited by docs/KSBFT-M-margin-induction.md.
# Deterministic (no clock enters any output except the "real" lines of out_timing.txt).
# Serial: at most 1 process.  ~15 min and ~2 GB RAM on this host, most of it D=4 at t=15 and D=5
# at t=13.  Poset lists live in a temp dir and are deleted; only transcripts are kept.
set -e
cd "$(dirname "$0")"
HERE=$(pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT INT TERM HUP
B=$T/pcert
cc -O2 -Wall -Wno-unused-but-set-variable -Wno-unused-variable -o "$B" pcert.c
w(){ out=$1; shift; "$@" > "$T/out.tmp" && mv "$T/out.tmp" "$HERE/$out"; }
: > "$HERE/out_timing.txt"
tm(){ /usr/bin/time -p "$@" 2>>"$HERE/out_timing.txt"; }

# 0. generators: pruned (non-CUT prefixes, Lemma 2.5) for D = 3, 4, 5; full census for n <= 8 and
#    range<=3 to n = 13 (the cross-check of the pruned generator and the e2e test population).
cd "$T"
"$B" gencut - c3_1.txt 3 > gen3.txt; for k in $(seq 2 13); do "$B" gencut c3_$((k-1)).txt c3_$k.txt 3 >> gen3.txt; done
"$B" gencut - c4_1.txt 4 > gen4.txt; for k in $(seq 2 15); do tm "$B" gencut c4_$((k-1)).txt c4_$k.txt 4 >> gen4.txt; done
"$B" gencut - c5_1.txt 5 > gen5.txt; for k in $(seq 2 13); do tm "$B" gencut c5_$((k-1)).txt c5_$k.txt 5 >> gen5.txt; done
"$B" onept gen - p1.txt > genall.txt; for k in 2 3 4 5 6 7 8; do "$B" onept gen p$((k-1)).txt p$k.txt >> genall.txt; done
cp p8.txt d3_8.txt; for k in 9 10 11 12 13; do "$B" onept gen d3_$((k-1)).txt d3_$k.txt 3 >> genall.txt; done
cd "$HERE"
w out_gen.txt sh -c "cat $T/genall.txt; echo 'A000112 (n=1..8): 1 2 5 16 63 318 2045 16999'; cat $T/gen3.txt $T/gen4.txt $T/gen5.txt"

# 1. controls
w out_controls.txt sh -c "
  echo '== counter controls inherited from mg-eedd (onept.c, included verbatim)';
  for m in 2 5 10 20; do $B onept fib \$m; done; $B onept brute 7 100; $B onept brute 8 20;
  echo '== CUT filter + pruned generator: full range<=3 census filtered by CUT must equal gencut counts';
  for k in 9 10 11 12 13; do echo \"t=\$k full-census\"; $B cert $T/d3_\$k.txt 0 1 3 | grep 'AGG CT'; done;
  echo '   (AGG CT t total CUT fail failCUT: total - CUT must equal the gencut count in out_gen.txt)';
  echo '== e2e (Theorem 2.3 end to end, every indecomposable P in range<=3, n = 12, 13, every size-11 ideal Q)';
  echo '   AGG E #P #Q #pairs bracket-violations #certified certified-but-unbalanced-in-P #uncertified';
  for k in 12 13; do $B e2e $T/d3_\$k.txt 0 1 11 3 0; done;
  echo '== e2e FIRING control: s = t-D+1 violates Lemma 2.2; bracket violations and bad certificates MUST appear';
  for k in 12 13; do $B e2e $T/d3_\$k.txt 0 1 11 3 1; done;
  echo '== e2e range<=4 (P = indecomposable members of the D=4 n=13 non-CUT list, t = 11), then its firing control';
  $B e2e $T/c4_13.txt 0 1 11 4 0; $B e2e $T/c4_13.txt 0 1 11 4 1;
  echo '== cert FIRING control: interval narrowed to [2/5,3/5] and [7/20,13/20]; failures MUST appear at D=3, t=13';
  ONEPT_LO=2/5 $B cert $T/c3_13.txt 0 1 3 | grep 'AGG CT\|AGG CW';
  ONEPT_LO=7/20 $B cert $T/c3_13.txt 0 1 3 | grep 'AGG CT\|AGG CW'"

# 2. the certificate, D = 3 (t <= 13), D = 4 (t <= 15), D = 5 (t <= 13)
w out_cert_d3.txt sh -c "for k in \$(seq 5 13); do $B cert $T/c3_\$k.txt 0 1 3; done"
w out_cert_d4.txt sh -c "for k in \$(seq 5 15); do $B cert $T/c4_\$k.txt 0 1 4 | grep -v '^FAIL'; done"
w out_cert_d5.txt sh -c "for k in \$(seq 5 13); do $B cert $T/c5_\$k.txt 0 1 5 | grep -v '^FAIL'; done"

# 3. base cases: delta(P) - 1/3 on every indecomposable member of the non-CUT lists (which contain
#    every indecomposable P of range <= D, Lemma 2.5), plus every class n <= 8 (all ranges)
w out_base.txt sh -c "
  for k in 3 4 5 6 7 8; do echo \"## all classes n=\$k (every range)\"; $B delta $T/p\$k.txt 0 1 1/50; done;
  for k in \$(seq 3 11); do echo \"## D=3 n=\$k\"; $B delta $T/c3_\$k.txt 0 1 0/1; done;
  for k in \$(seq 3 15); do echo \"## D=4 n=\$k\"; $B delta $T/c4_\$k.txt 0 1 0/1; done;
  for k in 12 13; do echo \"## range<=3 (full census) n=\$k, threshold 1/60\"; $B delta $T/d3_\$k.txt 0 1 1/60; done"

# 4. transport error against distance (covariance decay), range <= 3, n = 10..13
w out_decay.txt sh -c "for k in 10 11 12 13; do echo \"## range<=3 indecomposable n=\$k\"; $B decay $T/d3_\$k.txt 0 1; done"
