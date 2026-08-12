#!/bin/sh
# mg-8bc7 -- audit of sections 1-4 of docs/imports/compression.tex.
#
# Runs every arm and writes its transcript beside it.  a0 runs FIRST and its failure is
# fatal: it is the arm that checks the instrument, and a verdict from an unchecked
# instrument is worth nothing.  Measured wall clock on this host: see README.md (do not
# quote a runtime here that has not been measured -- mg-17aa's D4).
set -e
cd "$(dirname "$0")"

RC=0
for arm in a0_selftest a1_fibers a2_energy a3_operator a4_parity a5_general; do
    printf '%s ... ' "$arm"
    if python3 "$arm.py" > "out_$arm.txt" 2>&1; then
        echo "ok"
    else
        echo "FAILED (see out_$arm.txt)"
        RC=1
        # a0 gates the rest: every later arm's verdict is decided by the routines a0 checks.
        if [ "$arm" = "a0_selftest" ]; then
            echo "a0 is the instrument self-test; refusing to run the audit arms against it."
            exit 1
        fi
    fi
done

echo
if [ "$RC" = "0" ]; then
    echo "ALL ARMS PASS"
else
    echo "SOME ARMS FAILED"
fi
exit "$RC"
