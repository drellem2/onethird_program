#!/bin/sh
# mg-7dd3 -- independent audit of the mg-a4ef repair (106e121) of mg-73df.
# Pure Python 3, no dependencies.  NO NETWORK except `git show` / `git diff`
# against this repository, which is local.  About 3 minutes, almost all of it
# d5, which builds a scratch copy of docs/ and five code trees per mutation.
#
# TOTAL BAD here counts FINDINGS AGAINST THE AUDITED WORK, following
# code/species_audit_73df.  d2, d3, d5 and d6 are EXPECTED to be nonzero:
# that is what this audit found.  The self-test is the only file whose exit
# code is a statement about this instrument rather than about the repair.
cd "$(dirname "$0")"

python3 selftest7dd3.py  | tee out_selftest.txt
python3 d1_source.py     > out_d1_source.txt     2>&1 || true
python3 d2_extent.py     > out_d2_extent.txt     2>&1 || true
python3 d3_seam.py       > out_d3_seam.txt       2>&1 || true
python3 d4_survivals.py  > out_d4_survivals.txt  2>&1 || true
python3 d5_mutations.py  > out_d5_mutations.txt  2>&1 || true
python3 d6_exitcodes.py  > out_d6_exitcodes.txt  2>&1 || true

echo
echo "Headline lines:"
grep -h '^D[0-9] TOTAL BAD:\|^D5 PREDICTIONS MISSED:\|^selftest7dd3:' \
     out_*.txt || true
echo
echo "Every D above prints its own EXTENT under its total.  That is the"
echo "finding this audit exists to check, applied to itself."
