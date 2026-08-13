#!/bin/sh
# mg-1953 -- REPAIR of mg-ebd8 / 714aceb's DERIVATIONS.
# Reproduces every number added to docs/OneThird-Landscape-Where-This-Lives.md
# by the repair (its section 8).  Pure Python 3, no dependencies, ~1 min.
set -e
cd "$(dirname "$0")"

python3 closed_form_outside_AC.py 6 > out_closed_form_outside_AC.txt   # ~5 s
python3 repaired_claims.py 6       > out_repaired_claims.txt           # ~19 s
python3 selftest.py 6              > out_selftest.txt                  # ~30 s

# The self-test now reads the document as well as the instruments (mg-3b51 A3).
# A new guard owes evidence that it can FAIL: this mutates every number under
# the stated coverage boundary and every sentence carrying one.  ~1 s.
python3 negative_control_document.py > out_negative_control_document.txt

# mg-3b51's OWN scope instrument, re-run UNMODIFIED against the document as
# mg-aec7 left it.  Evidence that the A1/A3/A4 landing did not re-open the
# locating, from the auditor's code rather than this author's: status words
# still 1 of 11 changed (E8, which the brief ordered), NOT CLAIMED row still
# identical, row Q still enumerates 7 -- and its D5 detector for A4, which
# reported "states a CONTACT CRITERION: False" against 6b1eacf, now reports
# True.  ~1 s.
#
# THE CORPUS REVISION IS PASSED HERE AND IS DELIBERATELY NOT mg-3b51's OWN
# (mg-0e77).  This transcript exists to DISAGREE with
# ../landscape_repair_audit_3b51/out_scope_text.txt -- False -> True on D5 is
# the whole content of the re-run.  Pinning both at one commit would not repair
# this transcript, it would delete the comparison.  1db0be9 is the commit that
# landed mg-aec7's document; e924590 is mg-3b51's.  Two transcripts, two pins.
( cd ../landscape_repair_audit_3b51 \
  && python3 audit_scope_text.py ../.. 1db0be9 ) > out_scope_text_3b51_rerun.txt

tail -3 out_selftest.txt
tail -1 out_negative_control_document.txt
echo "done"
