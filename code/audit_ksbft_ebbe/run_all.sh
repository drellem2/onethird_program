#!/bin/sh
# run_all.sh (audit mg-ebbe of mg-cfba / KSBFT-S). One process, ~20 s. Exit 1 on any failed assertion.
# Census files come from mg-6b81's generator (pcert onept gen) in a temp dir that is deleted; their counts are
# asserted against OEIS A000112 here, and labelled completeness was certified independently by audit mg-6e7c.
set -e
cd "$(dirname "$0")"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT INT TERM HUP
cc -O2 -o aud aud.c
cc -O2 -w -o "$T/pcert" ../ksbft_m_margin_6b81/pcert.c
( cd "$T"; ./pcert onept gen - p1.txt > /dev/null; for k in 2 3 4 5 6 7 8 9; do ./pcert onept gen p$((k-1)).txt p$k.txt > /dev/null; done )
EXP="1 2 5 16 63 318 2045 16999 183231"; GOT=""
for k in 1 2 3 4 5 6 7 8 9; do GOT="$GOT $(wc -l < "$T/p$k.txt" | tr -d ' ')"; ./aud < "$T/p$k.txt" > "$T/a$k.txt"; done
[ "$(echo $GOT)" = "$EXP" ] || { echo "FAIL census counts $GOT != A000112 $EXP"; exit 1; }
echo "census counts n=1..9: $GOT (= OEIS A000112)" > out_census.txt
python3 census.py "$T"/a1.txt "$T"/a2.txt "$T"/a3.txt "$T"/a4.txt "$T"/a5.txt "$T"/a6.txt "$T"/a7.txt "$T"/a8.txt "$T"/a9.txt >> out_census.txt
./aud -control < "$T/p7.txt" | awk '{for(i=1;i<=NF;i++){if($i~/^trap=/&&$i!="trap=0")t++; if($i~/^dbl=/&&$i!="dbl=0")d++}} END{print "CONTROL (planted: top-only trap rule, tripling) n=7 posets flagged: trap",t+0," dbl",d+0}' >> out_census.txt
cat "$T"/a*.txt | python3 -c "
import sys
bad=[k for l in sys.stdin for k in ('NB','PNB','DNB','trap','dbl') if (lambda kv:(kv['chain']=='0' and kv[k]!='1') if k in ('NB','PNB','DNB') else kv[k]!='0')(dict(t.split('=') for t in l.split(' | ')[1].split()))]
print('census n<=9 failures (NB/PNB/DNB/Lemma1.1/Doubling):',len(bad)); sys.exit(1 if bad else 0)" >> out_census.txt
grep -q "CONTROL (planted.*trap [1-9].*dbl [1-9]" out_census.txt || { echo "FAIL: census controls did not fire"; exit 1; }
python3 xcheck.py "$T"/p2.txt "$T"/p3.txt "$T"/p4.txt "$T"/p5.txt "$T"/p6.txt "$T"/p7.txt > out_xcheck.txt
python3 witnesses.py > out_witnesses.txt
python3 goodpair.py > out_goodpair.txt
python3 records.py > out_records.txt
echo "ALL OK"
