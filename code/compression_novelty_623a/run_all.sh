#!/bin/sh
# Regenerates every transcript in this directory.  MEASURED runtime on the host that
# produced the committed transcripts: 32.8 s wall.  That figure was TIMED on the same
# invocation that wrote these transcripts, not estimated -- mg-17aa's D4 is a
# quoted-but-unmeasured runtime, and this suite is not going to repeat it.
set -e
cd "$(dirname "$0")"
python3 a1_identities.py 5     > out_a1_identities.txt
python3 a2_tightness.py 5 24   > out_a2_tightness.txt
python3 a3_sites.py            > out_a3_sites.txt
echo "a1/a2/a3 regenerated"
