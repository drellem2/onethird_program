#!/bin/sh
# mg-dffa -- the warrant repair of mg-5800's F1-F4 on mg-41aa / 504ab6c.
# Pure Python 3, no dependencies.  About five seconds.
# w3_brown.py needs network (it downloads arXiv:math/0006145); if the download
# fails it says so and exits 0, and nothing else depends on it.
#
# `set -e` is deliberate and it is NOT the whole of the exit contract: every
# probe below returns non-zero on its own failures, and the explicit `||` guards
# name which one failed rather than letting the runner die anonymously.
set -e
cd "$(dirname "$0")"

python3 selftestdffa.py > out_selftest.txt   || { echo "SELFTEST FAILED"; exit 1; }
python3 w1_ledger.py    > out_w1_ledger.txt  || { echo "W1 FAILED"; exit 1; }
python3 w2_family.py    > out_w2_family.txt  || { echo "W2 FAILED"; exit 1; }
python3 w3_brown.py     > out_w3_brown.txt   || { echo "W3 FAILED"; exit 1; }   # needs network
python3 w4_control.py   > out_w4_control.txt || { echo "W4 FAILED"; exit 1; }
python3 w5_doc.py       > out_w5_doc.txt     || { echo "W5 FAILED"; exit 1; }

echo "done.  Headline lines:"
grep -h '^SUMMARY\|^SELF-TEST:' out_*.txt || true
