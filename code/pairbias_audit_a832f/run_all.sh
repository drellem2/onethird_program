#!/bin/sh
# mg-832f -- INDEPENDENT AUDIT of mg-6bc2's eps_spec derivation.
# Exact rationals throughout; no numpy on this machine, so the simplex is hand-written.
# ~14 min total, dominated by the n=7 sweeps.
set -e
cd "$(dirname "$0")"
python3 selftesta832.py          > out_selftesta832.txt          # NC1-NC3 + library
python3 a1_unitmap.py            > out_a1_unitmap.txt            # unit map + LP over S_n
python3 a2_realizable.py 6       > out_a2_realizable.txt         # poset sweep, n <= 6
python3 a2_realizable.py 7       > out_a2_realizable_n7.txt      # poset sweep, n = 7
python3 a3_perslot.py            > out_a3_perslot.txt            # mg-131e re-derived
python3 a4_boundary_structure.py 6 > out_a4_boundary_structure.txt
python3 a4_boundary_structure.py 7 > out_a4_boundary_structure_n7.txt
echo "done"
