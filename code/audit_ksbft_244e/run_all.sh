#!/bin/sh
# mg-244e: audit of KSBFT-R (mg-7bfc). Independent of code/ksbft_r_window_padding_7bfc (no shared code).
# ~1 min, exact Fractions, deterministic (fixed seeds). Asserts every control fires.
set -e
cd "$(dirname "$0")"
python3 audit.py > out_audit.txt
python3 texists.py > out_texists.txt
grep -q "SUMMARY: 0 failed checks" out_audit.txt
grep -q "NEGATIVE CONTROL: closed form .* CAUGHT" out_audit.txt
grep -q "CONTROL: probe-B certificate on bare F_12 CERTIFIES" out_audit.txt
grep -q "CONTROL: the uniform-law detector FIRES" out_audit.txt
grep -q "POSITIVE CONTROL: .* FIRES" out_texists.txt
echo "run_all: transcripts regenerated, 0 failed checks, all controls fire"
