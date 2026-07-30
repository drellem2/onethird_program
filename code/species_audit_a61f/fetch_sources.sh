#!/bin/sh
# Regenerate quotes_a61f.txt.  THIS IS THE ONLY SCRIPT HERE THAT USES THE
# NETWORK, and run_all.sh does NOT call it.  a5_quotes.py reads the committed
# quotes_a61f.txt, so the audit reproduces offline.
#
# mg-7d75 section 10 item 1 asks an auditor to "re-read section 17.4, section
# 10.10, Theorem 10.13 and section 13.1.1 from rendered PDFs", because its own
# quotes came from a Flate-decode-and-string-scrape that "demonstrably drops fi
# and fl ligatures ... and drops mathematical symbols entirely".  This script
# uses poppler's pdftotext, which is a renderer-grade extractor, so the
# characters below are the ones on the page.
set -e
D=${1:-.}
cd "$D"
curl -sL -o am.pdf https://pi.math.cornell.edu/~maguiar/a.pdf
curl -sL -o aa.pdf https://arxiv.org/pdf/1709.07504
curl -sL -o mm.pdf https://ajc.maths.uq.edu.au/pdf/92/ajc_v92_p419.pdf
for f in am aa mm; do pdftotext -q $f.pdf $f.txt; done
echo "extracted: $(wc -l am.txt aa.txt mm.txt)"
echo "now grep the passages named in quotes_a61f.txt; line numbers there are"
echo "for the PDFs as served on 2026-07-30 and may drift if a source is revised."
