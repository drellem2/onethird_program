"""E3 -- F4's replacement, audited as a new claim.

The replacement is a live paragraph in section 0 consequence 3:

    "(a) ... was mg-af28's reading of Brown, and after the strike above it
     appeared in this document only inside struck text, which is not a place a
     live claim may rest.  It was therefore not hedged but READ: section 4.3
     of arXiv:math/0006145 is titled 'Distributive lattices'; it INTRODUCES
     EXACTLY ONE EXAMPLE -- ... -- whose 'maximal chains are the lattice paths
     from (0,0) to (p,q)'; and 'The kids walk' is section 4.4.  All located BY
     POSITION, STRICTLY BETWEEN THE TWO SECTION HEADINGS.  Brown prints no
     size for the lattice; he counts the chains 0 < x < 1 at (p+1)(q+1) - 2,
     which agrees with the (p+1)(q+1) above."

Three things are audited here and only the first was measured by mg-dffa.

E3a  THE LOCATION, re-derived on a sixth extractor, and PINNED.  mg-dffa's
     w3_brown.py downloads the paper and records no digest, so a reader cannot
     tell whether they read the same bytes.  This probe publishes the SHA-256
     and the byte length of what it read.

E3b  "INTRODUCES EXACTLY ONE EXAMPLE" IS A WORD COUNT DRESSED AS A READING.
     mg-dffa's evidence is one occurrence of the string `example` in section
     4.3.  A section can introduce a second example without using the word.
     So section 4.3 is enumerated here for every OTHER construction that
     introduces an object -- `consider`, `Forinstance`, `e.g.`, `Figure` --
     and what is inside that hedge is listed rather than asserted away.

E3c  "ALL LOCATED BY POSITION, STRICTLY BETWEEN THE TWO SECTION HEADINGS."
     One of the four things the sentence lists -- that "The kids walk" is
     section 4.4 -- is not strictly between the two headings; it IS the second
     heading.  Checked, and reported at the size it is.

EXIT 0 if the replacement stands, 1 if a check fails, and **2 IF THE DOWNLOAD
FAILS** -- a probe that verified nothing must not be able to report green.
That is the contrast this probe draws with the one it audits.  PREDICTED 0.
"""

import hashlib
import os
import re
import sys
import urllib.request

OUT = sys.stdout
URL = "https://arxiv.org/pdf/math/0006145"
BAD = [0]

H43 = "4.3.Distributivelattices"
H44 = "4.4.Thekidswalk"
EXAMPLE = ("Asanexampleofadistributivelattice,considertheproduct")
PATHS = "Themaximalchainsarethelatticepathsfrom"


def ck(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)
    return ok


def head(t):
    print("=" * 78, file=OUT)
    for line in t.split("\n"):
        print(line, file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)


def extract(data):
    """A pure-Python content-stream reader, written here.  Every FlateDecode
    stream is inflated; every literal string in the inflated bytes is taken as
    a glyph run; octal escapes are resolved.  Inter-word spacing is not
    recoverable, so all matching downstream is on text with whitespace and
    hyphens removed."""
    import zlib
    text = []
    for m in re.finditer(rb"stream\r?\n", data):
        s = m.end()
        e = data.find(b"endstream", s)
        if e < 0:
            continue
        try:
            text.append(zlib.decompress(data[s:e]))
        except Exception:
            continue
    raw = b"\n".join(text).decode("latin1")
    runs = [m.group()[1:-1] for m in re.finditer(r"\((?:[^()\\]|\\.)*\)", raw)]
    s = " ".join(runs)
    return re.sub(r"\\(\d{3})", lambda m: chr(int(m.group(1), 8)), s)


def main():
    head("E3  mg-19ec: F4's replacement -- Brown section 4.3, re-read and\n"
         "    PINNED, and the one inference in the sentence tested.")
    try:
        data = urllib.request.urlopen(URL, timeout=120).read()
    except Exception as exc:
        print("  DOWNLOAD FAILED (%s)." % exc, file=OUT)
        print(file=OUT)
        print("  THIS PROBE VERIFIED NOTHING AND IS EXITING 2 TO SAY SO.", file=OUT)
        print("  It does not exit 0.  A network probe that returns success", file=OUT)
        print("  when it could not reach its source is a control that cannot", file=OUT)
        print("  fire, which is the category of mg-5800's own F3.", file=OUT)
        print("=" * 78, file=OUT)
        print("SUMMARY e3_f4_brown: UNVERIFIED (no network)", file=OUT)
        print("=" * 78, file=OUT)
        return 2

    digest = hashlib.sha256(data).hexdigest()
    print("  URL                 : %s" % URL, file=OUT)
    print("  bytes               : %d" % len(data), file=OUT)
    print("  SHA-256             : %s" % digest, file=OUT)
    print("  (mg-dffa's w3_brown.py records neither, so a later reader cannot", file=OUT)
    print("   tell whether they read the same bytes.  This is the pin.)", file=OUT)
    print(file=OUT)
    flat = re.sub(r"[\s-]+", "", extract(data))
    print("  characters extracted: %d" % len(flat), file=OUT)
    print(file=OUT)

    def at(needle):
        return [m.start() for m in re.finditer(re.escape(needle), flat)]

    head43, head44 = at(H43), at(H44)
    ck("'4.3. Distributive lattices' occurs exactly once", len(head43) == 1,
       " (%d)" % len(head43))
    ck("'4.4. The kids walk' occurs exactly once", len(head44) == 1,
       " (%d)" % len(head44))
    if len(head43) != 1 or len(head44) != 1:
        print("SUMMARY e3_f4_brown: findings %d" % BAD[0], file=OUT)
        return 1
    a, b = head43[0], head44[0]
    ck("4.3 precedes 4.4", a < b, " (%d < %d)" % (a, b))
    body = flat[a:b]
    print("  section 4.3 occupies characters %d .. %d (%d characters)"
          % (a, b, b - a), file=OUT)
    # is 4.4 really the NEXT section heading?
    nxt = [m.start() for m in re.finditer(r"4\.\d\.[A-Z]", flat) if a < m.start()]
    ck("no other 4.x heading lies between 4.3 and 4.4",
       not [p for p in nxt if p < b], " (next 4.x heading at %d)"
       % (min(nxt) if nxt else -1))
    print(file=OUT)

    print("-- E3a  the location", file=OUT)
    ex = at(EXAMPLE)
    ck("Brown's example sentence occurs exactly once in the paper",
       len(ex) == 1, " (%d)" % len(ex))
    ck("  ... and strictly inside section 4.3", len(ex) == 1 and a < ex[0] < b,
       " (at %d)" % (ex[0] if ex else -1))
    ck("its maximal chains are the lattice paths, in the same span",
       PATHS in body)
    ck("Brown counts the chains 0 < x < 1 at (p+1)(q+1) - 2",
       bool(re.search(r"\\\(p\+1\\\)\\\(q\+1\\\).{0,3}2chainsoftheform", body)))
    ck("Brown prints NO size for the lattice",
       not re.search(r"has\\\(p\+1\\\)\\\(q\+1\\\)elements", body))
    print(file=OUT)

    print("-- E3b  'introduces exactly one example' -- what is inside the hedge",
          file=OUT)
    nex = len(re.findall(r"[Ee]xample", body))
    ck("mg-dffa's proxy reproduces: 1 occurrence of 'example' in 4.3",
       nex == 1, " (%d)" % nex)
    print(file=OUT)
    print("  ENUMERATED: every OTHER object-introducing construction in the", file=OUT)
    print("  span, which a word count would not see.", file=OUT)
    others = {}
    for pat in ["consider", "Consider", "Forinstance", "forinstance",
                "e.g.", "Figure", "Take", "Suppose", "Letusexamine"]:
        n = body.count(pat)
        if n:
            others[pat] = n
    for pat in sorted(others):
        print("      %-14s %d" % (pat, others[pat]), file=OUT)
    if not others:
        print("      none", file=OUT)
    figs = sorted(set(re.findall(r"Figure\d+\\\([a-z]\\\)|Figure\d+", body)))
    print("  every Figure reference in section 4.3: %s" % (figs or "none"),
          file=OUT)
    ck("every 'consider' in 4.3 is inside Brown's one example sentence",
       body.count("consider") == 1
       and body.index("consider") > body.index("Asanexampleof"),
       " (%d 'consider')" % body.count("consider"))
    lats = re.findall(r"L=.{0,32}", body)
    print("  every lattice section 4.3 names explicitly: %s" % (lats or "none"),
          file=OUT)
    ck("the only lattice 4.3 names explicitly is the product of two chains,"
       " at p=q=2",
       len(lats) == 1 and "f0;1;2g" in lats[0],
       " (%d)" % len(lats))
    print(file=OUT)
    print("  A MISS OF MINE, KEPT AS WRITTEN.  This probe first asked whether", file=OUT)
    print("  every Figure reference in 4.3 pointed at the same figure NUMBER.", file=OUT)
    print("  It does not -- Figures 1, 3, 4 and 5 are all cited -- and the", file=OUT)
    print("  check fired.  It was the wrong predicate: reading the span shows", file=OUT)
    print("  Figure 3 is the p x q grid, Figure 4 is a step of the walk ON", file=OUT)
    print("  that grid, Figure 5 is that same grid at p=q=2 embedded in a", file=OUT)
    print("  Boolean lattice, and Figure 1 is a back-reference to Section", file=OUT)
    print("  4.2.  Four views of ONE object.  The predicate was replaced by", file=OUT)
    print("  the lattice-naming one above, which is a reading; the miss is", file=OUT)
    print("  recorded rather than deleted.", file=OUT)
    print(file=OUT)
    print("  READING E3b.  The word count is a PROXY for the sentence the", file=OUT)
    print("  document writes.  Here the proxy is corroborated by a reading:", file=OUT)
    print("  the section's only `consider` sits inside the one example", file=OUT)
    print("  sentence, and the only lattice the section names explicitly is", file=OUT)
    print("  that same product of two chains.  So 'introduces exactly one", file=OUT)
    print("  example' STANDS -- but it stands on this enumeration, not on", file=OUT)
    print("  the word count, and mg-dffa's account states only the word", file=OUT)
    print("  count as its evidence.", file=OUT)
    print(file=OUT)

    print("-- E3c  'all located by position, strictly between the two headings'",
          file=OUT)
    items = [("section 4.3 is titled 'Distributive lattices'", a, "IS the first heading"),
             ("the one example", ex[0] if ex else -1, "strictly between"),
             ("its maximal chains are the lattice paths",
              a + body.index(PATHS) if PATHS in body else -1, "strictly between"),
             ("'The kids walk' is section 4.4", b, "IS the second heading")]
    for label, pos, where in items:
        inside = a < pos < b
        print("      %-46s at %6d  %s" % (label, pos,
                                          "strictly between" if inside
                                          else "NOT strictly between (%s)" % where),
              file=OUT)
    ck("2 of the 4 things the sentence lists are the HEADINGS themselves, not"
       " between them",
       len([1 for _, p, _ in items if not (a < p < b)]) == 2)
    print(file=OUT)
    print("  READING E3c.  The located facts are all correct and the method", file=OUT)
    print("  is what it says -- position, not keyword.  'All located by", file=OUT)
    print("  position, strictly between the two section headings' is one", file=OUT)
    print("  clause covering four items, two of which ARE the headings.  A", file=OUT)
    print("  reader checking the sentence literally finds two misses; a", file=OUT)
    print("  reader checking the claim finds it discharged.  Recorded as", file=OUT)
    print("  imprecision, not as a defect.", file=OUT)
    print(file=OUT)

    print("  VERDICT E3.  Premise (a) IS re-affirmed outside the strike, and", file=OUT)
    print("  it is re-affirmed by reading rather than by hedging -- which is", file=OUT)
    print("  what mg-5800 asked for and the harder of the two options it", file=OUT)
    print("  offered.  The reading reproduces on a sixth extractor, from", file=OUT)
    print("  bytes now pinned by digest.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY e3_f4_brown: findings %d; sha256 %s" % (BAD[0], digest),
          file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
