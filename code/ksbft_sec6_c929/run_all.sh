#!/bin/sh
# mg-c929 -- the whole instrument (~50 s).  No randomness, no clock.
# Writes each transcript to a temp file and moves it, so a failing script
# leaves the committed transcript untouched.
set -e
cd "$(dirname "$0")"
python3 s1_sec6_checks.py 6    > out_s1_sec6_checks.txt.tmp     && mv out_s1_sec6_checks.txt.tmp out_s1_sec6_checks.txt
python3 s2_parallel_chains.py 11 > out_s2_parallel_chains.txt.tmp && mv out_s2_parallel_chains.txt.tmp out_s2_parallel_chains.txt
python3 s3_constants.py        > out_s3_constants.txt.tmp       && mv out_s3_constants.txt.tmp out_s3_constants.txt
grep '^VERDICT' out_s1_sec6_checks.txt
