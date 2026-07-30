#!/bin/sh
# mg-276d: regenerate every number quoted in
# docs/OneThird-Intrinsic-Face-Geometry-Probe.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.
# Total runtime on a 2024 laptop: ~11 seconds.
set -e
cd "$(dirname "$0")"

echo "== controls (positive + negative), all posets n <= 5 =="
python3 controls.py 5 | tee controls_output.txt

echo
echo "== probe, all posets up to isomorphism n <= 6 =="
python3 run_probe.py 6 | tee probe_output_n6.txt
