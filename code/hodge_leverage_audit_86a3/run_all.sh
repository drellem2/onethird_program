#!/bin/sh
# Independent audit of mg-a3d4 (docs/OneThird-Hodge-Side-Leverage.md), mg-86a3.
# Pure Python 3, no third-party packages.  Total ~10 min.
set -e
cd "$(dirname "$0")"
python3 audit_identities.py 6    > out_identities.txt
python3 audit_theoremG.py        > out_theoremG.txt
python3 audit_sweep.py 6         > out_sweep.txt
python3 audit_brown.py 5         > out_brown.txt
python3 audit_brown_family.py 4  > out_brown_family.txt
python3 audit_n6_brown.py        > out_n6_brown.txt
python3 audit_controls.py 5      > out_controls.txt
python3 audit_families.py        > out_families.txt
python3 audit_robustness.py      > out_robustness.txt
