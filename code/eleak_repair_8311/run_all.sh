#!/bin/bash
# mg-8311 — run the whole E_leak ruling-and-repair instrument, transcripts IN FULL.
#
# NO TRUNCATION on any output path: no head, no tail, no sed. Each section's exit code is
# captured and printed against a PRE-REGISTERED expectation, and a section that writes no
# output is a hard failure independent of its exit code -- so "returned 0" and "examined
# nothing" are distinguishable. That guard exists because mg-2de0's own runner once
# returned exit 0 having executed no section at all (recorded in that instrument's README).
#
# NO ASSOCIATIVE ARRAYS: macOS ships bash 3.2 and `declare -A` does not exist there.
#
# Exit codes are MEANINGFUL and pre-registered:
#   r1  0 = the 2-chain witness reproduces AND both symmetries hold for the definition.
#           1 would mean the ticket's finding is WRONG, which the ticket says to report as
#           the result rather than work around.
#   r2  0 = the divergence count and the population were both re-derived without a
#           self-inconsistency. NOTE: r2 does NOT fail if my count disagrees with the
#           ticket's 8178; that comparison is reported as a MEAS line, because the ticket
#           forbids treating its own figure as an input.
#   r3  0 = the definition matches the matrix identity on every pair, the AST census found
#           the call sites where it expected them, and no published assertion of mg-2de0
#           needs the old convention.
#   r4  0 = mg-2de0's population reproduces at 431/12702 and every one of its published Phi
#           assertions holds under the repaired reading.
#
# r4 imports lib2de0 for the POSET POPULATION ONLY. Its two columns are both computed by
# lib8311, so r4 prints the same before/after table whether lib2de0.E_leak on disk is the
# repaired version or the defective one. That is deliberate: the before/after comparison
# must not silently become a before/before comparison once the repair lands.

set -u
cd "$(dirname "$0")"

SECTIONS="r1:r1_witness.py:out_r1_witness.txt:0
r2:r2_divergence.py:out_r2_divergence.txt:0
r3:r3_ruling.py:out_r3_ruling.txt:0
r4:r4_consequences.py:out_r4_consequences.txt:0"

bad=0
summary=""

while IFS=: read -r key script out expect; do
    echo "### running $script -> $out"
    python3 "$script" > "$out" 2>&1
    rc=$?
    lines=$(wc -l < "$out" | tr -d ' ')
    echo "###   exit $rc (expected $expect), $lines lines written"
    note=""
    if [ "$rc" != "$expect" ]; then
        note="EXIT MISMATCH"
        bad=$((bad + 1))
    fi
    if [ "$lines" = "0" ]; then
        note="$note EMPTY OUTPUT"
        bad=$((bad + 1))
    fi
    summary="$summary
  $(if [ -z "$note" ]; then echo "ok  "; else echo "BAD "; fi) $key: exit $rc == expected $expect ($lines lines) $note"
done <<EOF
$SECTIONS
EOF

echo
echo "=============================================================================="
echo "EXIT CODES vs PRE-REGISTERED EXPECTATIONS"
echo "=============================================================================="
echo "$summary"
echo
if [ "$bad" = "0" ]; then
    echo "ALL 4 SECTIONS ON THEIR PRE-REGISTERED EXIT CODES, ALL NON-EMPTY."
else
    echo "$bad SECTION(S) OFF THEIR PRE-REGISTERED EXIT CODE OR EMPTY."
fi
exit $([ "$bad" = "0" ] && echo 0 || echo 1)
