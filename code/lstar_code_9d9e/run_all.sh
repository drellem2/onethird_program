#!/bin/sh
# mg-9d9e — DOES THE `L*` CODE BEAT ceil(log2 n!) AT THE n YOU CLAIM IT?  ~20 s on this host.
#
# NOT A GATE.  Like code/subset_consumability_99f4/, code/image_geometry_c776/ and
# code/image_closure_3da1/, this instrument answers a scoping question rather than guarding an
# invariant, it is run by hand, and its transcripts are committed.
#
# IT IMPORTS NOTHING FROM code/.  Not lib99f4, whose crossover table is this directory's
# starting point; not lib0fc6, whose merge tree is the object under study; not lib8748, whose
# F24 variance identity s3 re-measures.  The predecessor's reason applies one step along: a
# shared enumerator would move the code reading and the poset reading together.  What is shared
# with the estate is OEIS A001035, the definitions, and TWO PUBLISHED NUMBERS the arms check
# against (mg-0fc6 a1.6's 16,777,063; mg-9b6b's boundary family).
#
# NO CLOCK AND NO random MODULE.  The one sampled population uses a hand-written LCG, so two
# runs on two hosts produce byte-identical transcripts.
#
# The arms are ordered so that each rests only on the ones before it:
#   s0  controls on lib9d9e — A001035 by a second algorithm, e(P) by three routes, the tape's
#       bijectivity, KRAFT exactly (which went RED on this arm's own construction and is
#       reported rather than repaired), GIBBS at every poset, and five planted defects
#   s1  THE TICKET'S TEST, RUN — seven codes, six families, n = 6..12; compression2's own tape
#       read as a code; the boundary family priced in both bound shapes; and the per-node
#       conditional entropies that are the note's real object
#   s2  WHERE THE TEST BITES AND WHERE IT CANNOT — the antichain theorem, the shape-A ceiling
#       and the two readings of 16,777,063, the empty target class, and one code put to Q2
#   s3  THE F24-MULTIPLIER BRANCH under mg-99f4's own two-question screen — a SCOPING
#       measurement, not a closure
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in s0_selftest.py s1_run_the_test.py s2_where_the_test_bites.py s3_f24_screen.py; do
    echo
    echo "############################################################ $a"
    # REDIRECT-THEN-CAT, NOT `| tee`: in POSIX sh `$?` after a pipeline is the LAST command's
    # exit code, so `python3 arm.py | tee out.txt` reports TEE's status and a red arm reads
    # green.  Taken from code/subset_consumability_99f4/run_all.sh.
    python3 -B "$a" > "out_${a%.py}.txt" 2>&1
    RC=$?
    cat "out_${a%.py}.txt"
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "worst arm exit: $STATUS   (0 green)"
exit "$STATUS"
