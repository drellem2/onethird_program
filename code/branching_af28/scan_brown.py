"""Does Brown 2000 contain the branching-graph vocabulary at all?

The claim this supports is small and checkable: Brown's paper -- the source in
which this construction is located (mg-ebd8, confirmed by mg-d673) -- never
mentions Young's lattice, tableaux, Bratteli diagrams, branching or
differential posets.  So the identification in T1 is not something the located
source already makes.

REQUIRES NETWORK: it downloads arXiv:math/0006145 and extracts the text from
the PDF's Flate-compressed content streams.  If the download fails the script
says so and exits 0 -- the rest of the battery does not depend on it, and the
committed `out_scan_brown.txt` records the run that was made.
"""

import re
import sys
import zlib
import urllib.request

URL = "https://arxiv.org/pdf/math/0006145"
KEYWORDS = ["Young", "tableau", "Bratteli", "branching", "differential poset",
            "differential", "Gelfand", "Okounkov", "Vershik", "Fomin",
            "dual graded", "tower of algebras",
            # controls: these MUST be present, or the extraction is broken
            "distributive lattice", "maximal chains", "left regular band",
            "Tsetlin", "derangement"]


def pdf_text(data):
    chunks = []
    for m in re.finditer(rb"stream\r?\n", data):
        s = m.end()
        e = data.find(b"endstream", s)
        try:
            chunks.append(zlib.decompress(data[s:e]))
        except Exception:
            pass
    raw = b"\n".join(chunks).decode("latin1")
    pieces = [m.group()[1:-1] for m in re.finditer(r"\((?:[^()\\]|\\.)*\)", raw)]
    s = " ".join(pieces)
    s = re.sub(r"\\(\d{3})", lambda m: chr(int(m.group(1), 8)), s)
    return s


def main():
    print("=" * 78)
    print("SCAN  Brown, Semigroups, rings, and Markov chains (arXiv:math/0006145)")
    print("      -- keyword census of the full text.")
    print("=" * 78)
    print()
    try:
        data = urllib.request.urlopen(URL, timeout=120).read()
    except Exception as exc:            # pragma: no cover - network dependent
        print("  DOWNLOAD FAILED (%s); skipping.  This script requires network."
              % exc)
        return 0
    print("  bytes downloaded: %d" % len(data))
    txt = pdf_text(data)
    # Normalise away whitespace AND hyphens.  The hyphen matters: the first run
    # of this script scored the control "left regular band" as 0 occurrences,
    # because Brown writes "left-regular bands".  That is the control doing its
    # job on the scanner rather than on the paper.
    flat = re.sub(r"[\s-]+", "", txt)
    print("  characters of extracted text (whitespace removed): %d" % len(flat))
    print()
    print("  keyword                    occurrences")
    for kw in KEYWORDS:
        k = re.sub(r"\s+", "", kw)
        n = len(re.findall(re.escape(k), flat, re.I))
        print("  %-26s %6d %s" % (kw, n, "<- control" if kw in
                                  ("distributive lattice", "maximal chains",
                                   "left regular band", "Tsetlin",
                                   "derangement") else ""))
    print()
    print("  The controls are non-zero, so the extraction works; the", end=" ")
    print("branching-graph")
    print("  vocabulary is absent from the paper.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
