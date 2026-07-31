#!/bin/sh
# code/species_audit_73df -- the independent audit instrument for mg-73df.
#
# Pure Python 3, no dependencies, NO NETWORK.  ~100 s.  It reads the audited
# trees and the audited document; it writes only its own out_*.txt.
#
# c4_scope.py shells out to `git archive 83ac472` to get the PRE-REPAIR tree
# for its control (a), and to `python3 code/species_remainder_f8fa/w3_scope.py`
# for its control (b).  Both are local; neither touches the network.  If git
# is unavailable the control is recorded as SKIPPED and counted as a fault,
# not silently passed.
set -e
cd "$(dirname "$0")"
# mg-c2b3: every step in this file that is followed by a bare `cat` of its
# own transcript used to pipe into `tee` instead of redirecting.  A pipeline's
# exit status in POSIX sh is its LAST command's, which is tee's and is 0 --
# so the step could print failures, exit 1, and leave this runner exiting 0.
# Each now redirects and has its status read by an explicit `||` guard.  The
# other steps in this file were already guarded and are untouched.
# `set -o pipefail` is not used: `/bin/sh` is dash on Linux, which rejects the
# option and would abort the runner at the line meant to make it safer.
# This note deliberately avoids writing the old pipeline out, so that a plain
# grep for it over the arc still counts only the sites that still have one.
python3 selftest73df.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftest73df.py FAILED"; exit 1; }
cat out_selftest.txt
python3 c1_columns.py     > out_c1_columns.txt
python3 c2_pinned.py      > out_c2_pinned.txt
python3 c3_bidigare.py    > out_c3_bidigare.txt
python3 c4_scope.py       > out_c4_scope.txt
python3 c5_doc.py         > out_c5_doc.txt
echo
echo "Headline lines:"
grep -h "TOTAL BAD\|PREDICTIONS MISSED\|STILL ASSERTED AT SOURCE" out_c*.txt
echo
echo "TOTAL BAD counts FINDINGS AGAINST THE AUDITED WORK, not faults in this"
echo "instrument.  C1's missed predictions are reported on their own line and"
echo "are deliberately NOT folded into it: a miss is a finding, and a finding"
echo "counted as a fault gets edited away."
