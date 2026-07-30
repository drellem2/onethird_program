#!/bin/sh
# mg-276d: regenerate every number quoted in
# docs/OneThird-Intrinsic-Face-Geometry-Probe.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.
# Measured runtime on a 2024 laptop, 2026-07-30: 19 s total -- controls.py 1.9 s
# (of which NEGATIVE CONTROL 4, added by mg-2789, is 1.4 s over the full 86-poset
# n <= 5 population, so the CI-adjacent battery stays in the order-seconds
# regime and needs no scoping), run_probe.py at n <= 6 the remaining 17.4 s.
set -e
cd "$(dirname "$0")"

echo "== controls (positive + negative), all posets n <= 5 =="
python3 controls.py 5 | tee controls_output.txt

echo
echo "== probe, all posets up to isomorphism n <= 6 =="
python3 run_probe.py 6 | tee probe_output_n6.txt
