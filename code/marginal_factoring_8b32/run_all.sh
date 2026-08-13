#!/bin/sh
# mg-8b32 — WHICH FUNCTIONS FACTOR THROUGH THE PAIR MARGINALS.  ~70 s measured on this host.
#
# NOT A GATE.  This instrument is not in build.sh: it answers a scoping question Daniel asked,
# it does not guard an invariant.  It is run by hand and its transcripts are committed.
#
# The arms are ordered so that each rests only on the ones before it:
#   b0  controls on the library, against routes that share no code with it
#   b1  THE ANSWER — P = {pi = 1}, so every function of P factors.  The witness, rebuilt.
#   b2  the tiered table with a verdict per row
#   b3  the support-level witness the ticket asks for, built INSIDE hypothesis (1)
#   b4  why the surplus that survives still does not buy a bound, and what the target becomes
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in b0_selftest.py b1_forced_poset.py b2_tier_table.py b3_witnesses.py b4_tightness.py; do
    echo
    echo "############################################################ $a"
    # REDIRECT-THEN-CAT, NOT `| tee`: in POSIX sh `$?` after a pipeline is the LAST command's
    # exit code, so `python3 arm.py | tee out.txt` reports TEE's status and a red arm reads
    # green.  This runner is the thing that would have to notice, so it does not use a pipe.
    python3 "$a" > "out_${a%.py}.txt" 2>&1
    RC=$?
    cat "out_${a%.py}.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
