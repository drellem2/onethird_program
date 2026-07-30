#!/bin/sh
# mg-c6bc — independent audit of mg-a893 (90db267).
#
# Pure Python 3, no dependencies, about 4 minutes.  Exact integer and rational
# arithmetic throughout.  kern6bc.py imports nothing from the repair, the
# target or mg-0a11's audit: the definitions are rebuilt from the documents.
#
# Every output file below reproduces byte-identically across runs.
set -e
cd "$(dirname "$0")"

python3 selftest6bc.py  > out_selftest.txt
python3 a1_recount.py   > out_a1_recount.txt
python3 a2_theorem.py   > out_a2_theorem.txt
python3 a3_duality.py   > out_a3_duality.txt
python3 a4_extend.py    > out_a4_extend.txt
python3 a5_battery.py   > out_a5_battery.txt

# mg-0a11's battery, re-run UNMODIFIED from this worktree, to confirm that
# mg-a893's committed out_battery_0a11_rerun.txt is what that battery actually
# produces here.  The comparison is the point; the file is not re-committed.
python3 ../counterexample_audit_0a11/check_locator.py > out_battery_0a11_recheck.txt
diff out_battery_0a11_recheck.txt \
     ../counterexample_repair_dea5/out_battery_0a11_rerun.txt \
  && echo "mg-a893's committed re-run is byte-identical to a fresh one here."
