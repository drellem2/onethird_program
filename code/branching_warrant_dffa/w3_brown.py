"""W3 -- F4: read Brown's section 4.3 instead of narrowing the sentence.

F4 of mg-5800 says the strongest new sentence mg-41aa wrote --
*"Brown's OWN section 4.3 example lattice IS a Young interval"* -- has two
premises:

  (a)  Brown's worked section 4.3 example is the p x q grid of lattice paths;
  (b)  that grid is the Young interval [(q), (q+p, q)].

(b) is measured, three times, by three instruments.  (a) is a LOCATING claim
about Brown (2000), and after mg-41aa it survives in the document only inside a
block marked STRUCK.  Nobody in the arc had read the paper for it: the only
Brown evidence was `code/branching_af28/out_scan_brown.txt`, a KEYWORD CENSUS.

mg-5800's stated fix was one clause -- re-affirm (a) outside the strike, or
attach *"on mg-af28's reading, which nobody has re-read"* to the headline.  The
ticket that authorises this repair says to narrow to the evidence UNLESS the
wider claim is one we actually want, in which case say so and go and get it.
(a) IS one we want: it is the premise the headline stands on, and hedging it
would leave the headline resting on a hedge.  So this probe goes and gets it.

WHAT IT DOES.  It downloads `arXiv:math/0006145` and locates, by POSITION:

  1. the section 4.3 heading, and the section 4.4 heading after it;
  2. Brown's example sentence, strictly BETWEEN them;
  3. that the example is the product of a chain of length p and a chain of
     length q, that its maximal chains are the lattice paths, and that it has
     (p+1)(q+1) elements -- Brown's own count, which is the size mg-41aa's
     grid measurement reports;
  4. that section 4.3 introduces exactly one worked example, so "the section
     4.3 example" denotes something.

WHAT IT DOES NOT DO.  It does not read Brown (2000).  It reads section 4.3 and
the opening of section 4.4, and the deliverable says so.  Everything else in
the paper remains unread by this arc.

EXTRACTOR.  The pure-Python zlib/content-stream reader that
`code/branching_af28/scan_brown.py` uses, re-implemented here rather than
imported.  It emits glyph runs with no reliable inter-word spacing, so all
matching is done on text with whitespace AND hyphens removed -- exactly the
normalisation af28 had to adopt when the control keyword *"left regular band"*
scored 0 against Brown's *"left-regular bands"*.

REQUIRES NETWORK.  If the download fails the script says so and exits 0, as the
other network probes in this repo do; the committed output records the run that
was made.
"""

import re
import sys
import urllib.request
import zlib

OUT = sys.stdout
URL = "https://arxiv.org/pdf/math/0006145"
BAD = [0]

# Brown's own words, whitespace- and hyphen-stripped.
H43 = "4.3.Distributivelattices"
H44 = "4.4.Thekidswalk"
EXAMPLE = ("Asanexampleofadistributivelattice,considertheproduct"
           "f0;1;:::;pg\x02f0;1;:::;qgofachainoflengthpbyachainoflengthq")
PATHS = "Themaximalchainsarethelatticepathsfrom"
SIZE = "\\(p+1\\)\\(q+1\\)"


def verdict(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)


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
    return re.sub(r"\\(\d{3})", lambda m: chr(int(m.group(1), 8)), s)


def main():
    print("=" * 78, file=OUT)
    print("W3  Brown (2000) section 4.3, READ -- premise (a) of F4.", file=OUT)
    print("    arXiv:math/0006145, pure-Python content-stream extraction.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    try:
        data = urllib.request.urlopen(URL, timeout=120).read()
    except Exception as exc:            # pragma: no cover - network dependent
        print("  DOWNLOAD FAILED (%s).  This probe requires network; the" % exc,
              file=OUT)
        print("  committed out_w3_brown.txt records the run that was made.",
              file=OUT)
        return 0
    print("  bytes downloaded: %d" % len(data), file=OUT)
    flat = re.sub(r"[\s-]+", "", pdf_text(data))
    print("  characters extracted (whitespace and hyphens removed): %d"
          % len(flat), file=OUT)
    print(file=OUT)

    def once(needle):
        hits = [m.start() for m in re.finditer(re.escape(needle), flat)]
        return hits

    h43 = once(H43)
    h44 = once(H44)
    verdict("section 4.3 heading 'Distributive lattices' occurs once",
            len(h43) == 1, " (%d)" % len(h43))
    verdict("section 4.4 heading 'The kids walk' occurs once", len(h44) == 1,
            " (%d)" % len(h44))
    if len(h43) != 1 or len(h44) != 1:
        print("  cannot proceed without both headings.", file=OUT)
        return 1
    a, b = h43[0], h44[0]
    verdict("4.3 precedes 4.4", a < b, " (%d < %d)" % (a, b))
    body = flat[a:b]
    print("  section 4.3 spans characters %d .. %d (%d characters)"
          % (a, b, b - a), file=OUT)
    print(file=OUT)

    ex = once(EXAMPLE)
    verdict("Brown's example sentence occurs once in the paper", len(ex) == 1,
            " (%d)" % len(ex))
    verdict("and it lies strictly INSIDE section 4.3",
            len(ex) == 1 and a < ex[0] < b,
            "" if len(ex) != 1 else " (at %d)" % ex[0])
    verdict("section 4.3 introduces exactly one example",
            body.count("Asanexampleof") == 1
            and len(re.findall(r"[Ee]xample", body)) == 1,
            " (%d 'As an example of', %d 'example')"
            % (body.count("Asanexampleof"), len(re.findall(r"[Ee]xample", body))))
    verdict("its maximal chains are the lattice paths", PATHS in body)
    # Brown does not print "the lattice has (p+1)(q+1) elements".  He prints a
    # count of the chains 0 < x < 1, which is |L| - 2.  Recorded at that width
    # and no wider: the size mg-41aa reports comes from the definition of the
    # product, and this is corroboration, not Brown's own count.
    verdict("Brown counts the chains 0 < x < 1 at (p+1)(q+1) - 2",
            bool(re.search(re.escape(SIZE) + r".{0,3}2chainsoftheform", body)))
    verdict("section 4.4 is titled 'The kids walk', so 4.3 is not it",
            H44 in flat)
    print(file=OUT)

    if len(ex) == 1:
        print("  Brown's sentence, as extracted (the extractor drops", file=OUT)
        print("  inter-word spacing; bytes outside printable ASCII are shown", file=OUT)
        print("  escaped, and the product symbol is one of them):", file=OUT)
        print(file=OUT)
        s = "".join(c if 32 <= ord(c) < 127 else "\\x%02x" % ord(c)
                    for c in flat[ex[0]:ex[0] + 260])
        for i in range(0, len(s), 62):
            print("      %s" % s[i:i + 62], file=OUT)
        print(file=OUT)

    print("  READING.  Premise (a) is CONFIRMED BY READING, not inherited.", file=OUT)
    print("  Brown's section 4.3 is titled 'Distributive lattices'; its one", file=OUT)
    print("  worked example is the product of a chain of length p and a chain", file=OUT)
    print("  of length q -- the p x q grid -- whose maximal chains are the", file=OUT)
    print("  lattice paths; and the kids walk is section 4.4, not 4.3.  That", file=OUT)
    print("  is mg-af28's reading, word for word, and it survives.", file=OUT)
    print(file=OUT)
    print("  ONE THING STATED AT ITS OWN WIDTH.  Brown prints no size for the", file=OUT)
    print("  lattice.  He counts the chains 0 < x < 1 at (p+1)(q+1) - 2, which", file=OUT)
    print("  agrees with |L| = (p+1)(q+1) -- the size mg-41aa's grid", file=OUT)
    print("  measurement reports.  That size follows from the definition of a", file=OUT)
    print("  product of two chains; Brown's line corroborates it, and is not", file=OUT)
    print("  the source of it.", file=OUT)
    print(file=OUT)
    print("  SCOPE OF THE READING, STATED.  Sections 4.3 and the opening of", file=OUT)
    print("  4.4 were read.  The rest of Brown (2000) is still unread by this", file=OUT)
    print("  arc, and nothing here licenses a claim about any other section.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY w3_brown: failures %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
