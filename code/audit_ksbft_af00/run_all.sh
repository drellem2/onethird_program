#!/bin/sh
# mg-af00: regenerate the audit transcript (~70 s, one process, exact, seeded)
set -e; cd "$(dirname "$0")"
python3 check_af00.py 300 > out_check_af00.txt
python3 check_af00_ctl.py >> out_check_af00.txt
grep -q "mismatches: 0" out_check_af00.txt
grep -q "'support_bad': 0, 'l51_bad': 0, 'l52_bad': 0, 'ms_bad': 0" out_check_af00.txt
grep -q "planted false) FIRES: [1-9]" out_check_af00.txt
[ "$(grep -c 'planted false) FIRES: [1-9]' out_check_af00.txt)" = 2 ]
python3 subfamily_af00.py > out_subfamily_af00.txt
! grep -q MISMATCH out_subfamily_af00.txt
echo "run_all: transcript regenerated, controls fire"
