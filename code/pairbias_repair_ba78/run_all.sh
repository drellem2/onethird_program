#!/bin/sh
# mg-ba78 -- regenerate every transcript in this directory.  Aggregate exit is
# the worst of the three; the self-test is first so a broken library is reported
# before any figure is printed.
set -e
cd "$(dirname "$0")"

run() {
    out="$1"; shift
    "$@" > "$out" 2>&1 && rc=0 || rc=$?
    echo "EXIT=$rc" >> "$out"
    echo "$* -> exit $rc"
    return $rc
}

run out_selftest_ba78.txt python3 selftest_ba78.py
run out_r1_repair.txt     python3 r1_repair.py 3 4 5 6
run out_r2_isolate.txt    python3 r2_isolate.py 3 4 5 6
