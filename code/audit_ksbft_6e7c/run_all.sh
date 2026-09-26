#!/bin/sh
# run_all.sh (audit mg-6e7c of mg-ce69): regenerate every transcript.  Census files from mg-eedd's generator
# (pcert onept gen) in a temp dir that is deleted; their completeness is certified INDEPENDENTLY by gencheck.py
# (sum n!/|Aut| = OEIS A001035, labelled posets).  At most 3 processes.  ~3 min wall.  Exit 1 on any failure.
set -e
cd "$(dirname "$0")"
T=$(mktemp -d)
PIDS=""
trap 'kill $PIDS 2>/dev/null || true; rm -rf "$T"' EXIT INT TERM HUP
cc -O2 -w -o "$T/pcert" ../ksbft_m_margin_6b81/pcert.c
( cd "$T"; ./pcert onept gen - p1.txt > gen.txt; for k in 2 3 4 5 6 7 8 9; do ./pcert onept gen p$((k-1)).txt p$k.txt >> gen.txt; done
  cp p8.txt d4_8.txt; ./pcert onept gen d4_8.txt d4_9.txt 4 >> gen.txt; split -l 61077 p9.txt p9part_ )
python3 - <<'PY' > "$T/records.txt"
import glob, json
seen = {}
for f in sorted(glob.glob("../ksbft_range_probe/out/*.jsonl")):
    for line in open(f):
        d = json.loads(line)["rec"]["down"]
        if len(d) >= 3: seen[tuple(d)] = 1
for k in seen: print(" ".join([str(len(k))] + [format(m, "x") for m in k]))
PY
( python3 census.py --small $T/p3.txt $T/p4.txt $T/p5.txt $T/p6.txt $T/p7.txt $T/p8.txt > out_census_small.txt
  python3 census.py $T/d4_9.txt > out_census_d4_9.txt
  python3 census.py $T/records.txt > out_census_records.txt
  python3 gencheck.py $T/p1.txt $T/p2.txt $T/p3.txt $T/p4.txt $T/p5.txt $T/p6.txt $T/p7.txt $T/p8.txt $T/p9.txt > out_gencheck.txt ) & PIDS="$PIDS $!"
python3 census.py $T/p9part_aa > out_census_p9a.txt & PIDS="$PIDS $!"
python3 census.py $T/p9part_ab $T/p9part_ac > out_census_p9b.txt & PIDS="$PIDS $!"
wait
python3 witnesses.py > out_witnesses.txt
python3 release.py $T/p3.txt $T/p4.txt $T/p5.txt $T/p6.txt $T/p7.txt > out_release.txt
python3 reduction.py $T/p4.txt $T/p5.txt $T/p6.txt $T/p7.txt $T/p8.txt > out_reduction.txt
python3 negative_control.py > out_negative_control.txt
python3 check.py > out_check.txt; st=$?; cat out_check.txt; exit $st
