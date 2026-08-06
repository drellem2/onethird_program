#!/bin/bash
# mg-2de0 — run the whole audit and write every transcript IN FULL.
#
# NO TRUNCATION. mg-bf79 recorded a defect where run_all.sh truncated a transcript
# BEFORE the probe that reads it ran, hiding nine of that instrument's own labels. There is
# no head/tail/sed on any output path here, and each section's exit code is captured and
# printed so "returned 0" and "examined nothing" are distinguishable.
#
# NO ASSOCIATIVE ARRAYS. The first version of this file used `declare -A`, which does not
# exist in the bash 3.2 that macOS ships. Under `set -u` it died on line 21 with
# "selftest: unbound variable" AND STILL REPORTED EXIT 0 to the caller -- the runner
# returned success having executed no section at all. That is precisely the
# returned-0-vs-examined-nothing conflation this arc has been repairing, committed by this
# instrument, in this instrument's own runner, on its first execution. It is recorded in the
# README rather than quietly fixed. The guard below is the fix: a section that writes no
# output is a hard failure, independent of its exit code.
#
# Exit codes are MEANINGFUL and pre-registered:
#   selftest  0 = all red-drills fired correctly            (1 = the instrument is untrusted)
#   a1        0 = Lemma A confirmed, 0 exceptions            (1 = Lemma A is dead, and B with it)
#   a2        1 = EXPECTED: Lemma B's I2 is false (62 grid cells). 0 would mean the
#                 detector stopped detecting and the audit's headline is unsupported.
#   a3        0 = non-vacuity numbers confirmed
#   a4        0 = requirement comparison confirmed
#   a5        0 = Linial-as-used confirmed on the finite population

set -u
cd "$(dirname "$0")"

SECTIONS="selftest:selftest2de0.py:out_selftest_2de0.txt:0
a1:a1_lemma_a.py:out_a1_lemma_a.txt:0
a2:a2_lemma_b.py:out_a2_lemma_b.txt:1
a3:a3_nonvacuity.py:out_a3_nonvacuity.txt:0
a4:a4_requirements.py:out_a4_requirements.txt:0
a5:a5_linial.py:out_a5_linial.txt:0"

bad=0
summary=""

while IFS=: read -r key script out expect; do
  [ -z "$key" ] && continue
  echo "### running $script -> $out"
  python3 "$script" > "$out" 2>&1
  got=$?
  lines=$(wc -l < "$out" | tr -d ' ')
  echo "###   exit $got (expected $expect), $lines lines written"

  # A section that wrote nothing EXAMINED nothing, whatever its exit code says.
  if [ "$lines" -lt 10 ]; then
    echo "###   EXAMINED NOTHING: $out has $lines lines. Hard failure regardless of exit."
    summary="$summary  EMPTY $key: exit $got but only $lines lines of output
"
    bad=$((bad + 1))
    continue
  fi

  if [ "$got" = "$expect" ]; then
    summary="$summary  ok   $key: exit $got == expected $expect ($lines lines)
"
  else
    summary="$summary  WRONG $key: exit $got != expected $expect ($lines lines)
"
    bad=$((bad + 1))
  fi
done <<EOF
$SECTIONS
EOF

echo
echo "=============================================================================="
echo "EXIT CODES vs PRE-REGISTERED EXPECTATIONS"
echo "=============================================================================="
printf '%s' "$summary"
echo
if [ "$bad" = 0 ]; then
  echo "ALL 6 SECTIONS ON THEIR PRE-REGISTERED EXIT CODES, ALL NON-EMPTY."
else
  echo "$bad SECTION(S) OFF PRE-REGISTERED EXIT CODE OR EMPTY — audit not reproduced."
fi
exit "$bad"
