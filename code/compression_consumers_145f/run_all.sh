#!/bin/sh
# mg-145f -- consumer enumeration for the cube-foliation energy identity.
# Every arm is exact rational arithmetic; there is no float anywhere in this directory.
# Measured runtime on this host: ~7 s total (e5 is ~5 s of it, the isomorphism canonisation).
set -e
cd "$(dirname "$0")"
rc=0
for a in e0_selftest e1_outputmap e2_covariance e3_density e4_adjacency e5_collisions; do
    echo "=== $a"
    if python3 "$a.py" > "out_$a.txt" 2>&1; then
        tail -1 "out_$a.txt"
    else
        rc=1
        echo "  ARM FAILED -- see out_$a.txt"
    fi
done
exit $rc
