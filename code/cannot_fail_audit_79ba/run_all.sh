#!/bin/sh
# mg-79ba -- INDEPENDENT AUDIT of mg-17aa.  Runs every instrument and writes its
# transcript beside it.  122 s measured on this host, by running it.
#
# THIS COMMENT FIRST SAID ~40 s, WHICH I HAD NOT MEASURED -- mg-17aa's own D4,
# committed by its auditor inside the file that reports it, and corrected the
# same way mg-17aa corrected two of build.sh's.  The suite is slow because it
# runs `controls.py` (2.7 s) about forty times across sandboxes: a1 five worlds
# x two trees for the deletion test plus two pinned-blob runs, a2 five worlds,
# a3 four staged trees each running the battery AND verify_landing.py.
#
# NOT ADDED TO build.sh, deliberately, and the reason is measured rather than
# asserted: a1 and a3 assert that things go RED, so this suite's own green
# depends on defects it reports staying present.  A gate whose pass condition is
# "the defect I found is still there" is the wrong-direction shape this whole
# ticket is about, and adding it would be the ninth consecutive generation to
# ship its own defect class.  See README.md section 6.
set -e
cd "$(dirname "$0")"
for a in a1_cannot_fail a2_fixed_blindness a3_repair_blocked; do
    echo "### $a"
    python3 "$a.py" > "out_$a.txt" 2>&1 || true
    tail -3 "out_$a.txt"
done
