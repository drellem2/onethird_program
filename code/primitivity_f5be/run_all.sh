#!/bin/sh
# mg-f5be -- DANIEL'S PRIMITIVITY OBJECTION.  Arms p0-p3; p4 (n=8) is run separately.
set -e
cd "$(dirname "$0")"
for a in p0_selftest p1_chain p2_primitive p3_frozen; do
    echo "### $a"
    python3 "$a.py" | tee "out_$a.txt"
done
echo
echo "p4_n8.py is the n = 8 extension (~20 min).  Run it directly:  python3 p4_n8.py"
