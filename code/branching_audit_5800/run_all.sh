#!/bin/sh
# mg-5800 -- independent audit of mg-41aa / 504ab6c.
# Pure Python 3, no dependencies.  About 4 minutes; a6_quotes.py needs network.
set -e
cd "$(dirname "$0")"

python3 selftest5800.py > out_selftest.txt || { echo "SELFTEST FAILED"; exit 1; }
python3 a1_counts.py  8   > out_a1_counts.txt      # ~20 s
python3 a2_exactly.py 6   > out_a2_exactly.txt     # ~4 min
python3 a3_grid.py    6   > out_a3_grid.txt
python3 a4_yf.py          > out_a4_yf.txt
python3 a5_b1b5.py    7 5 > out_a5_b1b5.txt        # ~30 s
python3 a6_quotes.py      > out_a6_quotes.txt      # needs network
python3 a7_doc.py         > out_a7_doc.txt

# Does any instrument in this repo TEST Bergeron-Li conditions (3), (4), (5)?
# mg-41aa says they are untested by everyone.  This is the grep behind that.
{
  echo "grep for a TEST (not a mention) of Bergeron-Li (3),(4),(5) in:"
  echo "  code/branching_af28/  code/branching_audit_6ad0/  code/branching_repair_41aa/"
  grep -rn "projectiv\|Mackey\|idempotent condition" \
      ../branching_af28/ ../branching_audit_6ad0/ ../branching_repair_41aa/ \
      2>/dev/null || echo "(no hits)"
  echo
  echo "Every hit above is a PRINT statement naming the conditions, not a test."
  echo "mg-41aa's 'untested by anyone' holds inside this repo."
} > out_a6_grep.txt

echo "done.  Headline lines:"
grep -h '^SUMMARY\|^SELFTEST 5800:\|^A7:' out_*.txt || true
