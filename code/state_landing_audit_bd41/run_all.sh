#!/bin/sh
# mg-bd41 — independent audit of mg-7735 / b68db5d (the landing of the mg-6a2f audit).
#
# Every script here was written from scratch for this audit.  None of them imports or
# reads anything under code/state_restructure_34bf/ or code/state_audit_6a2f/ in order
# to SOURCE a figure.  instrument_sensitivity.py executes two of the author's scripts,
# but only to test the commit's claims ABOUT those scripts — never to obtain a number.
#
# Instrument discipline (this arc has been bitten by all three):
#   * `wc -m` counts BYTES on this box (LC_CTYPE=C) and agrees exactly with `wc -c`, so
#     cross-checking them reads as confirmation while both are wrong.  Nothing here
#     shells out to wc: characters are len(str), bytes are len(bytes).
#   * Every figure names its UNIT and, for cells, its CONVENTION (raw / stripped).
#   * Every tally is over UNBOUNDED input.  No head/tail/sed -n/--limit anywhere; each
#     count prints the population it was taken over.
#
# ~8 s total.  instrument_sensitivity.py mutates STATE.md in the working tree and
# restores it under a finally + sha check; it refuses to run if STATE.md is dirty.
set -e
cd "$(git rev-parse --show-toplevel)/code/state_landing_audit_bd41"

echo "### 1. verify_landing_figures.py — every figure b68db5d writes about itself"
python3 verify_landing_figures.py
echo
echo "### 2. instrument_sensitivity.py — do the cited re-runs SEE the change?"
python3 instrument_sensitivity.py
echo
echo "### 3. multiset_whole.py — is mg-6a2f's completeness property still whole?"
python3 multiset_whole.py
