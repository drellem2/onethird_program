#!/bin/sh
# mg-8d63 -- run order.  One script.  Exit 0 = all four arms pass; any nonzero exit means
# the onset figure this landing publishes is NOT earned and must not be quoted.
set -e
cd "$(dirname "$0")"
python3 s1_onset.py | tee out_s1_onset.txt
