#!/bin/sh
# mg-6f61 -- the repair of mg-7d75 under mg-a61f's audit.
# Pure Python 3, no dependencies, NO NETWORK.  About 30 seconds, of which
# r2_columns.py is 27.
#
# r3_quotes.py reads code/species_audit_a61f/quotes_a61f.txt -- the poppler
# extraction the audit committed -- rather than re-fetching the PDFs.
# code/species_audit_a61f/fetch_sources.sh is the script that regenerates it,
# and it is the only network script in this cluster.
set -e
cd "$(dirname "$0")"

python3 selftest6f61.py > out_selftest.txt || { echo "SELFTEST FAILED"; exit 1; }
python3 r1_smallest.py  > out_r1_smallest.txt
python3 r2_columns.py   > out_r2_columns.txt          # ~27 s
python3 r3_quotes.py    > out_r3_quotes.txt
python3 check_doc.py    > out_check_doc.txt || { echo "CHECK_DOC FAILED"; exit 1; }

echo "done.  Headline lines:"
grep -h '^R[0-9] TOTAL BAD:\|^R2 PREDICTIONS MISSED:\|^CHECK_DOC:\|^selftest6f61' out_*.txt || true
echo
echo "R2 PREDICTIONS MISSED is NOT expected to be zero.  Both misses are"
echo "explained in out_r2_columns.txt R2e and in the repair document; a"
echo "battery whose expectations are written after the run cannot be wrong."
