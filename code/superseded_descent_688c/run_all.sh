#!/bin/sh
# mg-688c -- THE DESCENT SWEEP, end to end.
#
# ORDER MATTERS AND IT IS THE TICKET'S ORDER: bound the window (s0), then the
# stale-vs-current delta the ticket says to produce FIRST because everything
# depends on it (s1), then the sweep the ticket actually asks for (s2), then
# the controls that make its zero worth anything (s3).
#
# ~4 minutes on this host, almost all of it s2 walking 30k mail files and 5k
# work items.  s3 re-walks the commit population once for X5.
set -u
cd "$(dirname "$0")"
STATUS=0
for s in s0_window s1_delta s2_descent s3_controls; do
    printf '\n===== %s =====\n' "$s"
    python3 "$s.py" > "out_$s.txt" 2>&1 || STATUS=1
    tail -1 "out_$s.txt"
done
exit $STATUS
