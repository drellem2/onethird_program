#!/bin/sh
# mg-3b51 -- independent audit of mg-1953 / 6b1eacf.
# Pure Python 3, no third-party imports.  ~5 min end to end, dominated by A7.
set -e
cd "$(dirname "$0")"

python3 audit_r1_offAC.py  6 > out_r1_offAC.txt
python3 audit_r3_r4.py     6 > out_r3_r4.txt
python3 audit_r2_e8.py     5 > out_r2_e8.txt
python3 audit_scope_text.py  > out_scope_text.txt
python3 audit_r1_n7.py       > out_r1_n7.txt
python3 selftest.py        6 > out_selftest.txt

echo "--- all instruments done; self-test verdict: ---"
tail -1 out_selftest.txt
