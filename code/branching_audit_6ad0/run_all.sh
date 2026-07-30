#!/bin/sh
# mg-6ad0: independent audit instrument for mg-af28 / 358beff.
# Pure Python 3, no dependencies.  ~30 s without network, plus two network steps.
set -e
cd "$(dirname "$0")"

python3 selftest6ad0.py    > out_selftest.txt   || { echo "SELFTEST FAILED"; exit 1; }
python3 a1_contact.py      > out_a1_contact.txt
python3 a2_intervals.py    > out_a2_intervals.txt
python3 a3_hypotheses.py   > out_a3_hypotheses.txt
python3 a4_algebra.py      > out_a4_algebra.txt
python3 a5_scan.py         > out_a5_scan.txt        # needs network
python3 a6_quotes.py       > out_a6_quotes.txt      # needs network

echo "done.  Headline lines:"
grep -h '^SUMMARY' out_*.txt || true
