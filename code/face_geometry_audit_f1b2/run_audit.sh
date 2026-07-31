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

# mg-7522: every step below used to pipe into `tee` instead of redirecting.
# A pipeline's exit status in POSIX sh is its LAST command's, which is tee's
# and is 0 -- so a step could print failures, exit non-zero, and leave this
# runner exiting 0 with `set -e` never seeing anything.  Each step now
# redirects and has its own status read by an explicit `||` guard, then the
# transcript is `cat` so the terminal stream is unchanged.
#
# THIS FILE IS THE POINT OF mg-7522.  mg-c2b3 swept the arc for exactly this
# defect and repaired 17 runners; its population was "files named
# `run_all.sh`", and this file is not one, so it was still swallowing at HEAD
# after the sweep said the arc was clean.  A population defined by a naming
# convention is not defined by the property under repair.
#
# `set -o pipefail` is not used: the shebang is `/bin/sh`, which on Linux is
# dash, and dash rejects the option -- it would abort the runner at the line
# meant to make it safer.
python3 audit_scoring.py > out_scoring.txt || {
    cat out_scoring.txt; echo "audit_scoring.py FAILED"; exit 1; }
cat out_scoring.txt
python3 audit_gates.py > out_gates.txt || {
    cat out_gates.txt; echo "audit_gates.py FAILED"; exit 1; }
cat out_gates.txt
python3 audit_theorem_and_content.py > out_theorem.txt || {
    cat out_theorem.txt; echo "audit_theorem_and_content.py FAILED"; exit 1; }
cat out_theorem.txt
python3 audit_injections.py > out_injections.txt || {
    cat out_injections.txt; echo "audit_injections.py FAILED"; exit 1; }
cat out_injections.txt
python3 audit_nmax2.py > out_nmax.txt || {
    cat out_nmax.txt; echo "audit_nmax2.py FAILED"; exit 1; }
cat out_nmax.txt
