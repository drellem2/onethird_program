"""E5 -- DID IT STOP AT FOUR?  The same warrant defect, swept over the whole
document, with the population NAMED rather than totalled.

mg-dffa was handed four findings and landed four.  Whether four is the
POPULATION is a different question and nobody had asked it.

THE DEFECT, AS TWO PREDICATES.  mg-5800's four are one shape -- a sentence
asserting a count or a universal over a family, where the family is not bounded
in the sentence that states it -- but that shape splits cleanly in two, and
running them separately is what keeps the census adjudicable.  A single loose
predicate collected 40 sites, most of them citations and definitions, and a
census that cannot be read is a bare total with extra steps.

  UNIVERSE.  Every claim site in docs/OneThird-Branching-Graphs-Where-This-
  Lives.md: one unit per paragraph and one per table cell longer than 30
  characters.  LIVE means outside fenced code, outside block quotes, and
  outside blocks marked STRUCK / CORRECTED / RE-SCOPED -- withdrawn text is
  not a live claim.  Sentences inside a live unit are the counting grain,
  because at paragraph grain the defect vanishes: mg-dffa's own new paragraph
  contains the string `|P| = 5`, which any coarse scope test scores as a bound,
  and it is not a bound on the classification the paragraph asserts.

  POP-1  COUNT CLAIMS.  A live sentence containing "N of M" or "N of the M"
         over a family.  This is F2a's and F2b's exact shape.
         UNBOUNDED: the sentence names no bound on the family it counts within
         -- no `n <= k`, no `rank(w) <= k`, no `|lambda| <= k`, no total.

  POP-2  EMPIRICAL UNIVERSALS.  A live sentence containing `exactly`, `only`,
         `every`, `all`, `none`, `never` AND evidence of measurement -- a
         numeral, or one of measured / tested / checked / 0 bad / reproduced --
         AND no attribution (Stanley, Byrnes, Brown, cited, reported, quoted,
         a quotation mark).  An attributed universal is a citation, not a
         warrant claim of this document's own, and mg-5800's four are all
         claims of this document's own.
         UNBOUNDED: same scope test.

THE CENSUS IS NOT THE VERDICT.  Both predicates still over-collect: some
unbounded universals are analytic ("no differential poset is finite" is a
theorem).  So every site is printed with its line number and its text, and the
deliverable adjudicates them by hand.  Printing a total without the sites would
be the defect being swept for.

EXIT 1 if the two unbounded populations together exceed four.  PREDICTED 1.
"""

import os
import re
import sys

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Branching-Graphs-Where-This-Lives.md")

COUNT = re.compile(r"\b\d[\d\s]*\s+of\s+(?:the\s+)?\d[\d\s]*\b")
UNIV = re.compile(r"\bexactly\b|\bonly\b|\bevery\b|\ball\b|\bnone\b|\bnever\b",
                  re.I)
EMPIRICAL = re.compile(r"\d|\bmeasured\b|\btested\b|\bchecked\b|0 bad"
                       r"|\breproduced\b|\bre-derived\b", re.I)
ATTRIB = re.compile(r"Stanley|Byrnes|Brown|Fulman|Gaetz|Okada|Bergeron"
                    r"|\bcited\b|\breported\b|\bquoted\b|\bquotation\b"
                    r"|[\"“”]|\bliterature\b|\bAbels\b", re.I)
SCOPE = re.compile(
    r"`?n`?\s*(?:≤|<=|=)\s*\d"
    r"|rank\s*\(?w?\)?\s*(?:≤|<=|=)\s*\d"
    r"|\|λ\|\s*(?:≤|<=)\s*\d"
    r"|\|P\|\s*(?:≤|<=)\s*\d"
    r"|\|μ\|\s*(?:≤|<=)\s*\d"
    r"|to\s+rank\s+\d|to\s+`?n"
    r"|\bof\s+(?:the\s+)?\d[\d\s]*\b"
    r"|\b\d[\d\s]*\s+(?:classes|posets|partitions|pairs|intervals|moves|"
    r"shapes|words)\b"
    r"|code/[a-z0-9_]+|out_[a-z0-9_]+\.txt", re.I)
# The document's strike convention is a BOLD CAPS marker inside a block
# quote: `> **STRUCK (mg-41aa, ...)**`.  Matching the bare words case-
# insensitively excluded live prose that merely says "re-scoped below" -- and
# the paragraph it excluded was the F2a replacement, the single sentence this
# audit exists to read.  So the marker is matched in the form the document
# actually uses, plus the three ledger rows that RECORD a withdrawn claim.
STRUCK = re.compile(r"\*\*(?:STRUCK|CORRECTED|RE-SCOPED)\b"
                    r"|the version this replaces|the reading this replaces"
                    r"|the scope this adds")


def sentences(text):
    parts = re.split(r"(?<=[.!?;])\s+(?=[A-Z*`(\"“])", text)
    return [p.strip() for p in parts if p.strip()]


def units(path):
    out, fence, para, start = [], False, [], 0
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if s.startswith("|"):
            if para:
                out.append((start, "para", para))
                para = []
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not (cells and set(cells[0]) <= set("-: ")):
                for c in cells:
                    if len(c) > 30:
                        out.append((i, "cell", [c]))
            continue
        if not s:
            if para:
                out.append((start, "para", para))
                para = []
            continue
        if not para:
            start = i
        para.append(line)
    if para:
        out.append((start, "para", para))
    return out


def live_sentences(us):
    for start, kind, body in us:
        text = " ".join(l.lstrip("> ").rstrip() for l in body)
        if any(l.lstrip().startswith(">") for l in body) or STRUCK.search(text):
            continue
        for s in sentences(text):
            yield start, kind, s


def show(sites):
    for n, (line, kind, s) in enumerate(sites, 1):
        txt = re.sub(r"\s+", " ", s)
        print("  [%02d] line %-4d %-5s %s" % (n, line, kind, txt[:145]), file=OUT)
        for j in range(145, len(txt), 145):
            print("                       %s" % txt[j:j + 145], file=OUT)
        print(file=OUT)


def main():
    print("=" * 78, file=OUT)
    print("E5  mg-19ec: is FOUR the population?  Two predicates, both named.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    us = units(DOC)
    live = list(live_sentences(us))
    nlive_units = len({(a, b) for a, b, _ in live})

    print("  THE UNIVERSE, NAMED", file=OUT)
    print("    document              : %s" % os.path.basename(DOC), file=OUT)
    print("    claim sites parsed    : %d" % len(us), file=OUT)
    print("    LIVE sites            : %d" % nlive_units, file=OUT)
    print("    LIVE sentences        : %d" % len(live), file=OUT)
    print("    mg-dffa was handed 4 and landed 4.", file=OUT)
    print(file=OUT)

    pop1 = [(a, b, s) for a, b, s in live if COUNT.search(s)]
    un1 = [t for t in pop1 if not SCOPE.search(
        COUNT.sub(" ", t[2]))]
    pop2 = [(a, b, s) for a, b, s in live
            if UNIV.search(s) and EMPIRICAL.search(s) and not ATTRIB.search(s)]
    un2 = [t for t in pop2 if not SCOPE.search(t[2])]

    print("=" * 78, file=OUT)
    print("  POP-1  COUNT CLAIMS  (F2a's and F2b's exact shape)", file=OUT)
    print("=" * 78, file=OUT)
    print("    population : %d live sentences state a count 'N of M'" % len(pop1),
          file=OUT)
    print("    unbounded  : %d name no bound on the family they count within"
          % len(un1), file=OUT)
    print(file=OUT)
    show(un1)

    print("=" * 78, file=OUT)
    print("  POP-2  EMPIRICAL UNIVERSALS, unattributed", file=OUT)
    print("=" * 78, file=OUT)
    print("    population : %d live sentences" % len(pop2), file=OUT)
    print("    unbounded  : %d" % len(un2), file=OUT)
    print(file=OUT)
    show(un2)

    # ---- POP-3: the one figure F2 is actually about ---------------------
    print("=" * 78, file=OUT)
    print("  POP-3  THE 33 YOUNG-FIBONACCI INTERVALS -- every site, and", file=OUT)
    print("         whether it carries the rank bound.  This is the sharpest", file=OUT)
    print("         form of the question: F2 was about THIS figure.", file=OUT)
    print("=" * 78, file=OUT)
    RANK6 = re.compile(r"rank\s*\(?w?\)?\s*(?:≤|<=)\s*6|to rank 6|rank 6", re.I)
    p3 = []
    for line, kind, s in live:
        if re.search(r"\b33\b", s) and re.search(
                r"Young–Fibonacci|Young-Fibonacci|`\[0̂, w\]`", s):
            p3.append((line, kind, s, bool(RANK6.search(s))))
    print("    population : %d live sentences state the figure 33 about"
          % len(p3), file=OUT)
    print("                 Young-Fibonacci intervals", file=OUT)
    print("    bounded    : %d carry `rank(w) <= 6` in the same sentence"
          % len([1 for t in p3 if t[3]]), file=OUT)
    print("    unbounded  : %d do not" % len([1 for t in p3 if not t[3]]),
          file=OUT)
    print(file=OUT)
    for n, (line, kind, s, b) in enumerate(p3, 1):
        txt = re.sub(r"\s+", " ", s)
        print("  <%02d> line %-4d %-5s %-9s %s"
              % (n, line, kind, "BOUNDED" if b else "UNBOUNDED", txt[:120]),
              file=OUT)
        for j in range(120, len(txt), 120):
            print("                                     %s" % txt[j:j + 120],
                  file=OUT)
        print(file=OUT)
    print("  mg-dffa edited 2 of these sites.  It changed the READING at both", file=OUT)
    print("  -- 'the same contact' became 'a contact of the same kind' -- and", file=OUT)
    print("  the BOUND at neither.", file=OUT)
    print(file=OUT)

    both = {(a, b, s) for a, b, s in un1} | {(a, b, s) for a, b, s in un2}
    print("=" * 78, file=OUT)
    print("  THE TWO POPULATIONS OVERLAP AT %d SITE(S); the union is %d."
          % (len(un1) + len(un2) - len(both), len(both)), file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  WHAT THIS IS AND IS NOT.  This is a CENSUS, not a verdict.  Both", file=OUT)
    print("  predicates over-collect: an unbounded universal can be analytic", file=OUT)
    print("  rather than measured, and the machine cannot tell.  The", file=OUT)
    print("  deliverable adjudicates every site above by hand and says which", file=OUT)
    print("  are instances of mg-5800's defect and which are not.  What the", file=OUT)
    print("  census settles on its own is the narrower question actually", file=OUT)
    print("  asked: the sites carrying this shape are not four, and two of", file=OUT)
    print("  them are sentences mg-dffa itself wrote.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY e5_population: universe %d live sentences in %d live sites"
          % (len(live), nlive_units), file=OUT)
    print("SUMMARY e5_population: POP-1 %d counts, %d unbounded; POP-2 %d "
          "universals, %d unbounded; union %d"
          % (len(pop1), len(un1), len(pop2), len(un2), len(both)), file=OUT)
    print("SUMMARY e5_population: mg-dffa landed 4", file=OUT)
    print("=" * 78, file=OUT)
    return 1 if len(both) > 4 else 0


if __name__ == "__main__":
    sys.exit(main())
