#!/bin/sh
# mg-365a — was the oscillation discharged, and by what?
#
# THE CONTROLS RUN FIRST AND THE MEASUREMENT SECOND, which is the opposite of the order a
# reader wants and the right order for the machine.  d1's finding is a ZERO, and a zero is
# what a broken walk, an unresolvable pin or a narrowed watched-class predicate returns for
# free.  d0 is what separates the finding from its failure mode, so it runs before anything
# is written into a transcript a later reader might quote.
#
# EVERY FIGURE IS A FUNCTION OF `lib365a.AS_OF_365A`, so both transcripts reproduce
# byte-identically on an unchanged pin and neither conflicts on a rebase.  d0's world D8
# checks that by running d1 twice and comparing, rather than by asserting it here.
#
# NOT IN build.sh, DELIBERATELY.  Nothing consumes these transcripts, the subject is a
# question put to pm-onethird rather than a property the gate must hold, and this directory
# reports on two others without editing either.  Adding it to the gate would make a
# measurement binding by the back door.
set -e
cd "$(dirname "$0")"

python3 d0_selftest.py    > out_d0_selftest.txt
python3 d1_discharge.py   > out_d1_discharge.txt

echo "mg-365a: d0 and d1 written."
