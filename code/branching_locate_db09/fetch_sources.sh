#!/bin/sh
# Regenerate sources_db09.txt.  THIS IS THE ONLY SCRIPT HERE THAT USES THE
# NETWORK, and run_all.sh does NOT call it.  t4_quotes.py reads the committed
# sources_db09.txt, so the whole instrument reproduces offline.
#
# The extractor is poppler's pdftotext, which is renderer-grade: the characters
# it emits are the ones on the page.  mg-af28 and mg-7d75 both had quotation
# defects found by their audits, both caused by a Flate-decode-and-scrape
# routine that dropped fi/fl ligatures and mathematical symbols.  What
# pdftotext still does is break lines mid-sentence, which is why every
# comparison in t4_quotes.py is whitespace-normalised.
#
# Line numbers below are for the PDFs as served on 2026-07-30 and will drift if
# a source is revised.  If a window moves, re-grep for the quoted sentence
# rather than trusting the number.
set -e
D=${1:-.}
cd "$D"
curl -sL --max-time 120 -o ov2.pdf https://arxiv.org/pdf/math/0503040
curl -sL --max-time 120 -o tl.pdf  https://arxiv.org/pdf/1204.4505
curl -sL --max-time 120 -o mss.pdf https://arxiv.org/pdf/1508.05446
curl -sL --max-time 120 -o ms.pdf  https://arxiv.org/pdf/1101.0416
for f in ov2 tl mss ms; do pdftotext -q $f.pdf $f.txt; done

python3 - <<'PY'
out = []


def window(tag, path, start, end, url):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    out.append("### %s  [%s]  lines %d-%d of the pdftotext extraction"
               % (tag, url, start, end))
    out.extend(lines[start - 1:end])
    out.append("")


window("OV-branching", "ov2.txt", 268, 305, "arXiv:math/0503040")
window("OV-canonical", "ov2.txt", 280, 318, "arXiv:math/0503040")
window("OV-wedderburn", "ov2.txt", 316, 348, "arXiv:math/0503040")
window("OV-prop14", "ov2.txt", 346, 366, "arXiv:math/0503040")
window("TL-prop41", "tl.txt", 1285, 1300, "arXiv:1204.4505")
window("TL-cor46", "tl.txt", 1653, 1670, "arXiv:1204.4505")
window("TL-wedderburn", "tl.txt", 4222, 4258, "arXiv:1204.4505")
window("MSS-thm418", "mss.txt", 4645, 4665, "arXiv:1508.05446")
window("MS-quasihereditary", "ms.txt", 40, 66, "arXiv:1101.0416")
open('sources_db09.txt', 'w').write('\n'.join(out))
print("wrote sources_db09.txt")
PY

echo "sources:"
echo "  arXiv:math/0503040  Vershik-Okounkov, A new approach ... II"
echo "  arXiv:1204.4505     Ridout-Saint-Aubin, Standard modules, induction"
echo "                      and the Temperley-Lieb algebra"
echo "  arXiv:1508.05446    Margolis-Saliola-Steinberg, Cell complexes, poset"
echo "                      topology and the representation theory of algebras"
echo "  arXiv:1101.0416     Margolis-Steinberg, Quivers of monoids with basic"
echo "                      algebras"
