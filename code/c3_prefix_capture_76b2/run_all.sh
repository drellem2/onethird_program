#!/bin/sh
# run_all.sh — the whole instrument for mg-76b2.  ~1 minute.
#
# Exit codes are PRE-REGISTERED here and re-checked against the run.  Every section is
# expected to exit 0: unlike mg-2de0's a2, this instrument has no section whose headline
# finding is a detector firing, so a non-zero exit anywhere is a real failure.
#
# NO TRUNCATION ON ANY OUTPUT PATH.  No head/tail/sed/grep between a script and its
# transcript, and a section that writes fewer than 20 lines is a hard failure regardless
# of its exit code -- "returned 0" and "examined nothing" must be different outcomes.

set -e
cd "$(dirname "$0")"

rc=0
for s in selftest76b2 s1_dictionary s2_sweep s3_c3 s4_budget; do
    printf '%s ... ' "$s"
    if python3 "$s.py" > "out_$s.txt" 2>&1; then
        got=0
    else
        got=$?
    fi
    lines=$(wc -l < "out_$s.txt" | tr -d ' ')
    if [ "$got" -ne 0 ]; then
        echo "FAILED (exit $got, expected 0)"
        rc=1
    elif [ "$lines" -lt 20 ]; then
        echo "FAILED (exit 0 but only $lines lines -- examined nothing)"
        rc=1
    else
        echo "ok (exit 0, $lines lines)"
    fi
done

echo
if [ "$rc" -eq 0 ]; then
    echo "run_all: every section exited 0 and wrote a non-trivial transcript"
else
    echo "run_all: FAILURES ABOVE"
fi
exit "$rc"
