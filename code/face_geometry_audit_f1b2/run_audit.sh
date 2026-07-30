#!/bin/sh
# mg-f1b2: regenerate every number quoted in
# docs/audit-mg-8a12-nc4-scoring-repair.md
#
# Pure Python 3, no third-party packages, exact integer arithmetic.  Measured on a
# 2024 laptop, 2026-07-30: 85 s wall total -- audit_scoring.py 68 s (it re-runs the
# whole split at n <= 6, 404 posets), audit_gates.py 4.0 s, audit_theorem_and_
# content.py 0.6 s, audit_injections.py 8.7 s (four full battery runs), audit_nmax2.py
# 3.4 s.  Nothing here writes into ../face_geometry: audit_injections.py patches a
# copy in a temporary directory and audit_nmax2.py only reads.
set -e
cd "$(dirname "$0")"

python3 audit_scoring.py            | tee out_scoring.txt
python3 audit_gates.py              | tee out_gates.txt
python3 audit_theorem_and_content.py | tee out_theorem.txt
python3 audit_injections.py         | tee out_injections.txt
python3 audit_nmax2.py              | tee out_nmax.txt
