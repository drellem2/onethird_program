#!/bin/sh
# mg-99f4 — IS ANY SEPARATOR IN THE ARBITRARY-SUBSET CLASS CONSUMABLE?  ~4 s on this host.
#
# NOT A GATE.  This instrument is not in build.sh: like code/image_geometry_c776/ and
# code/image_closure_3da1/ it answers a scoping question rather than guarding an invariant, it
# is run by hand, and its transcripts are committed.
#
# IT IMPORTS NOTHING FROM code/.  Not lib8b32, whose b2.3 tier table is the object under study;
# not lib0fc6, whose a1.6 crossover is this directory's external anchor.  A shared poset
# enumerator would move the separation reading and the bound reading together, and the whole
# finding is that those two readings are independent.  What is shared with the estate is OEIS
# A001035, the definitions, and two PUBLISHED NUMBERS that s0 and s2 check against.
#
# The arms are ordered so that each rests only on the ones before it:
#   s0  controls on lib99f4 — A001035, a second route to e(P), the set/poset inverse, four
#       planted defects (one INERT and printed as such), and the reproduction of mg-0fc6's
#       published crossover to the unit
#   s1  THE DICHOTOMY — separation and consumability are supported on disjoint parts of the
#       domain, so the ticket's demonstrated separation is worth zero bits; plus the resolution
#       census and the two-question screen, run on all four on-record TIER-2 separators
#   s2  THE ACCEPTANCE CONDITION for the prefix-code branch, stated BEFORE anything is built —
#       the crossover law, its elasticity, the required-constant table, and the shape dichotomy
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in s0_selftest.py s1_dichotomy.py s2_crossover.py; do
    echo
    echo "############################################################ $a"
    # REDIRECT-THEN-CAT, NOT `| tee`: in POSIX sh `$?` after a pipeline is the LAST command's
    # exit code, so `python3 arm.py | tee out.txt` reports TEE's status and a red arm reads
    # green.  Taken from code/image_closure_3da1/run_all.sh.
    python3 -B "$a" > "out_${a%.py}.txt" 2>&1
    RC=$?
    cat "out_${a%.py}.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
