#!/bin/bash
# mg-3c24 -- INDEPENDENT AUDIT of mg-a2bd (the strike of ledger row G'').
#
# One script, one output.  ~35 s on an M-series Mac (measured, not estimated).
# The output carries no wall-clock line and regenerates byte-for-byte.
#
#   out_audit_join.txt
#     A  the poset population, rebuilt (1,2,5,16,63,318)
#     B  the strike: G'' as a PER-LEVEL claim -- the 754 pairs and the 55
#     C  the strike: G'' under the PER-FACE reading -- 3901 of 7989
#     D  ROW G''' -- the row mg-a2bd added BEYOND its brief -- tested
#     E  Theorem J: the full-spectrum join identity on all 48 846 links
#     F  Theorem G exactly, and where gamma_i(A_n) is attained
#
# rebuild.py shares NO code with code/hodge_leverage/ or code/face_geometry/
# and imports nothing from them: its own poset canonicalisation, its own face
# enumeration (ordered partitions, not chains of ideals), its own link weights
# (products of linear-extension counts, not facet counting), EXACT rational
# inertia of W - tD instead of a floating-point Jacobi sweep, and Householder +
# QL instead of cyclic Jacobi where a full spectrum is needed.
#
# This directory contains NO mutation and scores NO control.  It is a
# REPLICATION, and it is labelled as one.
set -e
cd "$(dirname "$0")"
echo "[1/1] independent rebuild of the mg-a2bd landing ..."
python3 -u audit_join.py > out_audit_join.txt
echo "done."
