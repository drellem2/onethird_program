#!/bin/sh
# The instrument for mg-db09.  Pure Python 3, no dependencies, NO NETWORK.
# `fetch_sources.sh` is the one network script and this file does not call it.
set -e
D=$(dirname "$0")
cd "$D"
python3 -u selftestdb09.py | tee out_selftest.txt
python3 -u t1_tl.py        > out_t1_tl.txt     ; tail -1 out_t1_tl.txt
python3 -u t2_gz.py        > out_t2_gz.txt     ; tail -1 out_t2_gz.txt
python3 -u t3_ours.py      > out_t3_ours.txt   ; tail -1 out_t3_ours.txt
python3 -u t4_quotes.py    > out_t4_quotes.txt ; tail -1 out_t4_quotes.txt
