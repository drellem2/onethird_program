#!/bin/sh
# mg-9bc2 — the rendered twin's pin control, and the proof that it can fail.
#
# THE CONTROL WAS EXPECTED TO EXIT 1 (DRIFT) IN THE COMMIT THAT INTRODUCED IT, and that was
# the point of it.  Ledger rows 8 and 9 really had moved in STATE.md since the twin was
# last reconciled (276aead), so a green control there would have meant the pin had been
# seeded at HEAD to make it green — the same unfalsifiable claim as `Generated 2026-07-19`,
# reinstalled one layer down.  See seed_pin.py's docstring for that decision.
#
# IT STILL EXITS 1, AND FOR A SMALLER REASON.  mg-2f44 reconciled ROW 9 — the row mg-07fd's
# audit found the twin rendering pre-repair — and re-pinned that row and only that row, so
# the worklist is now ROW 8 ALONE.  Row 8 is the second drifted row mg-9bc2's first run
# surfaced and NO TICKET NAMES IT; it is left drifted deliberately rather than re-pinned,
# because re-pinning a row nobody reconciled is the one move this instrument forbids.
# DRIFT IS THE NORMAL CONDITION of a hand-maintained rendering between reconciliations.
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

# THE EXIT CODE IS NOT THE CLASSIFIER, AND THE `tee` REPAIR DID NOT GO FAR ENOUGH (mg-9876).
# Removing the pipe fixed WHOSE status was read.  It left standing the deeper error: a python
# process exits 1 when twin_pin.py finds drift AND when twin_pin.py dies in a traceback, so
# `1` meant both "the instrument worked" and "the instrument never reached a decision".
# mg-9876 demonstrated it — renaming STATE.md's ledger header makes `parse_state_ledger`
# raise, and this script reported `DRIFT, and the instrument demonstrably fails when it
# should` and exited 0 over a traceback.  Exit 127 fell through to `CLEAN`.
#
# So the control must first be shown to have REACHED ITS VERDICT.  mg-f8e5 arrived at the
# same rule from the other side: in this arc a non-zero exit is the normal state of an
# instrument that found what it was sent to find, so the question is never the code, it is
# whether the run got to its own decision.
VERDICT_LINE=$(grep -m1 '^VERDICT: ' code/rendered_twin_pin_9bc2/out_control.txt || true)
if [ -z "$VERDICT_LINE" ]; then
    echo
    echo "BROKEN — twin_pin.py exited $CONTROL WITHOUT printing a VERDICT line.  It did not"
    echo "reach a decision, so there is no verdict to report and this is NOT drift and NOT"
    echo "clean.  Read out_control.txt: a traceback and a finding are the same exit code."
    exit 2
fi
echo "control verdict: $VERDICT_LINE"
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
    # THE ROWS ARE READ OUT OF SECTION 2, NEVER TYPED.  This branch used to end with the
    # sentence "Row 9 was mg-2f44's and is RECONCILED; row 8 is the one no ticket names yet"
    # — an expected value typed by the author, in the runner, one file away from
    # negative_control.py's own rule that nothing may name a drifted row as a literal.  It
    # was already half wrong, and nothing would ever have said so.
    WORKLIST=$(sed -n 's/^.*since the twin was last reconciled: //p' \
                   code/rendered_twin_pin_9bc2/out_control.txt)
    echo "DRIFT, and the instrument demonstrably fails when it should."
    echo "The worklist, READ OUT OF SECTION 2 rather than typed here: ${WORKLIST:-(none)}"
    if [ -z "$WORKLIST" ]; then
        echo
        echo "BROKEN — the control exited 1 but section 2 named no drifted row, so the drift"
        echo "grade came from somewhere else (section 3) and this branch's message would be"
        echo "a worklist of nothing presented as a worklist."
        exit 2
    fi
    exit 0
fi
if [ "$CONTROL" -ne 0 ]; then
    echo "BROKEN — twin_pin.py exited $CONTROL, which is not one of its three verdicts."
    echo "A runner that maps an unknown exit onto CLEAN is instance 1 of this ticket."
    exit 2
fi
# THE WORKLIST LINE IS PRINTED ON A CLEAN RUN TOO, AND THAT IS NOT COSMETIC (mg-188d).
# It used to be printed ONLY in the DRIFT branch above, so the field existed exactly when
# the twin was broken and vanished the moment it was fixed.  mg-724a's merge gate reads
# `twin.worklist` by exactly-once anchored match — 0 matches means REFUSED — so the FIRST
# CLEAN TWIN IN THIS PAGE'S HISTORY took the gate to `GATE VERDICT: REFUSED` (exit 2) and
# blocked the merge with a message saying the GATE was broken rather than that the twin was
# clean.  Measured on this branch before it was fixed, not argued.  It was NOT fail-open,
# which is exactly why it would have survived: the merge still failed.  A gate whose
# load-bearing field is observable only in the failing state cannot report its own success —
# mg-e331's D4 and mg-9876's `a probe satisfied by the good input is UNFALSIFIABLE`, one
# directory over.  `(none)` rather than an empty tail so the line cannot be mistaken for a
# truncated one; lib724a reads that token as the EMPTY SET.
echo "The worklist, READ OUT OF SECTION 2 rather than typed here: (none)"
echo "CLEAN — the twin's pinned ledger rows all still match STATE.md."
exit 0
