#!/bin/sh
# mg-9bc2 — the rendered twin's pin control, and the proof that it can fail.
#
# THE CONTROL IS EXPECTED TO EXIT 1 (DRIFT) IN THE COMMIT THAT INTRODUCES IT, and that is
# the point of it.  Ledger rows 8 and 9 really have moved in STATE.md since the twin was
# last reconciled (276aead), so a green control here would mean the pin had been seeded at
# HEAD to make it green — which is the same unfalsifiable claim as `Generated 2026-07-19`,
# reinstalled one layer down.  See seed_pin.py's docstring for that decision.
#
# So this script does NOT `set -e` on the control.  It records both exit codes and reports.
#
#   out_control.txt          the control against the working tree
#   out_negative_control.txt the 11 mutations and which section caught each

set -u
cd "$(dirname "$0")/../.." || exit 1

# REDIRECT-THEN-CAT, NOT `| tee`.  The first version of this script piped both commands
# through tee, so `$?` was TEE's status and never the instrument's — tee succeeds whatever
# it is fed.  It printed `control exit : 0 … CLEAN` over a control that had just exited 1
# with two drifted rows.  A runner that launders its instrument's verdict into a green one
# is this ticket's own defect, in the script written to fix it, and it is why the exit codes
# below are read from the commands directly.  POSIX sh has no PIPESTATUS to reach for.

echo "=== twin_pin.py — the control ==="
python3 code/rendered_twin_pin_9bc2/twin_pin.py > code/rendered_twin_pin_9bc2/out_control.txt 2>&1
CONTROL=$?
cat code/rendered_twin_pin_9bc2/out_control.txt

echo
echo "=== negative_control.py — can it fail? ==="
python3 code/rendered_twin_pin_9bc2/negative_control.py \
    > code/rendered_twin_pin_9bc2/out_negative_control.txt 2>&1
NEGATIVE=$?
cat code/rendered_twin_pin_9bc2/out_negative_control.txt

echo
echo "================================================================================"
echo "control exit  : $CONTROL   (0 clean · 1 drift · 2 structural failure)"
echo "negative exit : $NEGATIVE   (0 = every mutation caught)"
echo
if [ "$CONTROL" -eq 2 ]; then
    echo "STRUCTURAL FAILURE — the pin mechanism is broken.  Read out_control.txt."
    exit 2
fi
if [ "$NEGATIVE" -ne 0 ]; then
    echo "THE NEGATIVE CONTROL FOUND A HOLE — the control cannot see something it should."
    echo "That is worse than drift: read out_negative_control.txt and record it in COVERAGE.md."
    exit 2
fi
if [ "$CONTROL" -eq 1 ]; then
    echo "DRIFT, and the instrument demonstrably fails when it should.  The drifted rows in"
    echo "out_control.txt section 2 are the worklist; row 9 is mg-2f44's."
    exit 0
fi
echo "CLEAN — the twin's pinned ledger rows all still match STATE.md."
exit 0
