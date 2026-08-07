#!/bin/sh
# run_all.sh -- the whole instrument for mg-94c3's independent audit of mg-76b2.
# ~2 minutes.
#
# Exit codes are PRE-REGISTERED here and re-checked against the run.  Every
# section is expected to exit 0.  No section of this audit has a detector-fires
# headline, so a non-zero exit anywhere is a real failure and not a finding.
#
# NO TRUNCATION ON ANY OUTPUT PATH.  No head/tail/sed/grep between a script and
# its transcript, and a section writing fewer than 20 lines is a hard failure
# regardless of its exit code -- "returned 0" and "examined nothing" must be
# different outcomes.

set -e
cd "$(dirname "$0")"

rc=0
for s in selftesta94c3 a1_algebra a2_dictionary a3_currency a4_census; do
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
        echo "ok ($lines lines)"
    fi
done

if [ "$rc" -eq 0 ]; then
    echo "ALL SECTIONS OK"
else
    echo "SOME SECTION FAILED"
fi
exit "$rc"
