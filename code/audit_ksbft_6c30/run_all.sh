#!/bin/sh
# audit mg-6c30: regenerate every transcript and assert the headline facts and every control. ~4 min at 3 cores.
set -e
cd "$(dirname "$0")"
python3 t_gen.py 9 > out_gen.txt
python3 badl.py 4 9 > out_badl_4_9.txt
python3 badl.py 10 10 > out_badl_10.txt
python3 props.py 2 1000 1000 > out_props.txt
python3 witnesses.py > out_witnesses.txt
python3 lcc.py 9 > out_lcc.txt
python3 lemmac_census.py > out_lemmac_census.txt
python3 rand_badl.py 3 3000 3000 > out_rand_badl.txt
python3 lemmac.py 3 3000 > out_lemmac.txt
python3 lpprobe.py Q12 > out_lpprobe.txt
python3 lpprobe2.py Q12 > out_lpprobe2.txt
python3 check.py
