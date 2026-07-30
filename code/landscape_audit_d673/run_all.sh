#!/bin/sh
# mg-d673 -- independent audit of mg-ebd8 / 714aceb.
# Pure Python 3, no third-party imports.  Shares no code with
# code/landscape_ebd8/ (the target), code/semigroup_note/, code/face_geometry/,
# code/unified_gate_8fd1/ or code/hodge_leverage/.
#
# diag_p2_cross.py is FORENSICS ONLY -- it imports the target's module to
# locate a disagreement, and no verdict rests on it.  It is not run here.
set -e
cd "$(dirname "$0")"
python3 audit_populations.py     6  | tee out_populations.txt
python3 audit_spectrum.py       40  | tee out_spectrum.txt
python3 audit_e6_e8_m0.py        5  | tee out_e6_e8_m0.txt
python3 audit_identifications.py 5  | tee out_identifications.txt
python3 audit_addenda.py            | tee out_addenda.txt
