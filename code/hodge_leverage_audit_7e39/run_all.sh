#!/bin/sh
# mg-7e39 -- INDEPENDENT AUDIT of the mg-6df0 repair (the mg-ec07 verdict).
#
#   sh run_all.sh            # ~2 min
#
# It MUTATES THE WORKING TREE (STATE.md, the deliverable, the history file,
# verify_landing.py and site_records.txt) and restores every one of them
# byte-identically after each probe.  The restore is checked after each probe
# and again at the end, and a failed restore is exit 2 rather than a warning.
# Run it on a clean tree.
set -e
cd "$(dirname "$0")"
python3 audit_7e39.py
