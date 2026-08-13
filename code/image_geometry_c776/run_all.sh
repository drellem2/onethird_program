#!/bin/sh
# mg-c776 — THE IMAGE OF `P -> pi(Unif(L(P)))` INSIDE THE MARGINAL BODY.  ~55 s on this host.
#
# NOT A GATE.  This instrument is not in build.sh: it answers mg-8b32's C4, the scoping question
# STATE.md row 8 becomes once the fiber-level questions are closed.  It guards no invariant, it
# is run by hand, and its transcripts are committed.
#
# The arms are ordered so that each rests only on the ones before it:
#   c0  controls on the library, against routes that share no code with it — including lib8b32,
#       which is imported HERE and nowhere else in this directory
#   c1  THE CHARACTERISATION — the image is Fix(r) for an idempotent retraction r of M_n, and
#       equivalently the set of vertex-barycentres of the box-faces of M_n
#   c2  the shape of answer the ticket wanted most does NOT exist: conv(R_n) = M_n, so no
#       inequality valid on the image cuts anything off the body
#   c3  what the image looks like inside hypothesis (1), and the one number the scoping turns on
#   c4  how far the ceiling-carrying point sits from the image, and which way r moves it
cd "$(dirname "$0")" || exit 2
STATUS=0
for a in c0_selftest.py c1_retraction.py c2_no_inequality.py c3_boundary.py c4_distance.py; do
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
