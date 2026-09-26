#!/bin/sh
# mg-afa4: regenerate every transcript. ~3 min at POGO_WORKER_CORES=3.
set -e
cd "$(dirname "$0")"
python3 xcheck.py      > out_xcheck.txt
python3 brightwell.py 8 > out_brightwell.txt
python3 bwgeneral.py   > out_bwgeneral.txt
python3 bwhyp.py 7     > out_bwhyp.txt
python3 bwstats.py 7   > out_bwstats.txt
python3 bwinc.py 7     > out_bwinc.txt
python3 bwrules.py 7   > out_bwrules.txt
python3 bwrefine.py 7  > out_bwrefine.txt
python3 onesided.py 7  > out_onesided.txt
python3 tight.py 7     > out_tight.txt
python3 gaps.py 7      > out_gaps.txt
python3 kdfs.py 10     > out_kdfs.txt
python3 kladder.py 10  > out_kladder.txt
python3 obstruction.py > out_obstruction.txt
python3 zaguia3.py 8   > out_zaguia3.txt
python3 probe.py 8     > out_probe8.txt
python3 probe.py 9     > out_probe9.txt
# assertions: controls fire and the headline counts reproduce
grep -q "mismatches = 0" out_xcheck.txt
grep -q "CONTROL perturbed law detected: True" out_xcheck.txt
grep -q "T8: contains induced 2+2 = True" out_xcheck.txt
grep -q "injection violations = 0; CONTROL (above-separators only) violations = [1-9]" out_brightwell.txt
grep -q "bad L found: True" out_bwgeneral.txt
grep -q "census n=8: 5334 non-chain interval orders; bad L (any L): 0; bad L (dominance L): 0" out_kdfs.txt
grep -q "census n=9: 31239 non-chain interval orders; bad L (any L): 2; bad L (dominance L): 2" out_kdfs.txt
grep -q "surviving the Swap-Ladder constraints: 2 posets" out_kladder.txt
grep -q "semiorders among them: 0" out_zaguia3.txt
echo "run_all: all assertions passed"
