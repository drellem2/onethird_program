#!/bin/sh
# mg-1c80 -- regenerate every number quoted in
# docs/audit-mg-da45-nc4-gate-repair.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured on a
# 2024 laptop, 2026-07-30: 26 s wall total -- a1_gates.py 0.6 s, a2_antichain.py
# 1.1 s, a3_n6_population.py 6.4 s, a4_witness.py 0.7 s, a5_claims.py 1.6 s,
# a6_mutations.py 16 s (eight full battery runs on patched copies).
#
# Nothing here writes into ../face_geometry.  a5_claims.py and a6_mutations.py run
# `controls.py` as a subprocess, in place and on temporary copies respectively;
# no script in this directory imports it.  No script re-runs mg-da45's own
# verifier (`code/face_geometry_landing_da45/`) -- its committed output is read
# as text where it is quoted, and every number is remeasured here instead.
set -e
cd "$(dirname "$0")"

python3 a1_gates.py         | tee out_gates.txt
python3 a2_antichain.py     | tee out_antichain.txt
python3 a3_n6_population.py | tee out_n6.txt
python3 a4_witness.py       | tee out_witness.txt
python3 a5_claims.py        | tee out_claims.txt
python3 a6_mutations.py     | tee out_mutations.txt
