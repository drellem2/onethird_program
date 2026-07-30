#!/bin/sh
# Regenerate sources2060/.  THIS IS THE ONLY SCRIPT HERE THAT USES THE
# NETWORK, and run_all.sh does NOT call it.  b3_quotes.py and b5_successor.py
# read the committed gzipped extractions, so the whole instrument
# reproduces offline.
#
# Unlike mg-db09's fetch_sources.sh, this stores the WHOLE pdftotext
# extraction of each paper, not a line-numbered window.  A window is a
# claim about where a sentence is; the whole file is not, and it lets an
# auditor of this audit grep for anything, including sentences this audit
# chose not to quote.  The SHA-256 of each PDF is recorded so the
# extraction can be checked against the bytes that produced it.
set -e
D=$(cd "$(dirname "$0")" && pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
mkdir -p "$D/sources2060"
cd "$T"
fetch() {
    curl -sL --max-time 180 -o "$2.pdf" "https://arxiv.org/pdf/$1"
    pdftotext -q "$2.pdf" "$2.txt"
    gzip -9 -c "$2.txt" > "$D/sources2060/$2.txt.gz"
}
fetch math/0503040 math_0503040   # Vershik-Okounkov II
fetch 1204.4505    1204.4505      # Ridout-Saint-Aubin, Temperley-Lieb
fetch 1508.05446   1508.05446     # Margolis-Saliola-Steinberg
fetch 1101.0416    1101.0416      # Margolis-Steinberg
fetch 1710.02851   1710.02851     # Ehrig-Tubbenhauer, relative cellular
fetch math/0411395 math_0411395   # Cox-Martin-Parker-Xi, towers of recollement
shasum -a 256 *.pdf > "$D/sources2060/SHA256SUMS.txt"
echo "wrote sources2060/"
cat "$D/sources2060/SHA256SUMS.txt"
