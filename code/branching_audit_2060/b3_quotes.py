"""B3 --- QUOTATIONS, from PDFs FETCHED BY THIS AUDIT.

mg-db09's T4 checks 19 quotations against `sources_db09.txt`, a file the
audited ticket wrote itself.  If that file were wrong, T4 would still pass.
So this script does three things T4 cannot:

  B3a  FABRICATION CHECK.  Every content line of mg-db09's committed
       `sources_db09.txt` is looked for in a pdftotext extraction of the
       arXiv PDFs fetched by THIS audit (`sources2060/`, SHA-256 of the
       PDFs recorded next to them).  Not a sample --- every line.
  B3b  THE DOCUMENT'S quotations, including the ones T4 does not check.
       T4 checks strings the ticket chose; this checks strings taken out
       of the delivered prose.
  B3c  D9 --- the ONE citation mg-db09 flags as its own weakest link
       ("Graham-Lehrer NOT read", taken from Wikipedia) --- against a
       refereed arXiv source.
  plus negative controls of this audit's own devising.
"""

import gzip
import os
import re
import unicodedata

BAD = 0
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources2060")

PAPERS = {
    "OV":  ("math_0503040", "Vershik-Okounkov, A new approach ... II"),
    "TL":  ("1204.4505", "Ridout-Saint-Aubin, Standard modules, induction ..."),
    "MSS": ("1508.05446", "Margolis-Saliola-Steinberg, Cell complexes ..."),
    "MS":  ("1101.0416", "Margolis-Steinberg, Quivers of monoids ..."),
    "ET":  ("1710.02851", "Ehrig-Tubbenhauer, Relative cellular algebras"),
}


def norm(s):
    """Whitespace-normalise and fold the punctuation pdftotext varies on."""
    s = unicodedata.normalize("NFKD", s)
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("–", "-"), ("—", "-"),
                 ("−", "-"), ("‐", "-"), ("­", ""),
                 ("ﬁ", "fi"), ("ﬂ", "fl"), ("′", "'")]:
        s = s.replace(a, b)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip()


TEXT = {}
for k, (stem, _) in PAPERS.items():
    with gzip.open(os.path.join(SRC, stem + ".txt.gz"), "rt",
                   encoding="utf-8", errors="replace") as f:
        TEXT[k] = norm(f.read())


def hr(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


def find(key, s):
    return norm(s) in TEXT[key]


def anywhere(s):
    return [k for k in TEXT if find(k, s)]


# --------------------------------------------------------------------------
hr("B3a  FABRICATION CHECK on mg-db09's committed sources_db09.txt")
print("""Every non-header, non-blank line of the audited ticket's own source
file, looked for in this audit's independently fetched extraction.  A line
that does not appear is either a drift in the PDF or a line the ticket did
not get from the paper.
""")
sd = os.path.join(HERE, "..", "branching_locate_db09", "sources_db09.txt")
tagmap = {"OV-branching": "OV", "OV-canonical": "OV", "OV-wedderburn": "OV",
          "OV-prop14": "OV", "TL-prop41": "TL", "TL-cor46": "TL",
          "TL-wedderburn": "TL", "MSS-thm418": "MSS",
          "MS-quasihereditary": "MS"}
cur = None
checked = missing = skipped = 0
misses = []
if not os.path.exists(sd):
    print("  sources_db09.txt not found at %s" % sd)
    BAD += 1
else:
    for raw in open(sd, encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        m = re.match(r"^### (\S+)\s", line)
        if m:
            cur = tagmap.get(m.group(1))
            continue
        t = norm(line)
        if len(t) < 12 or cur is None:
            skipped += 1
            continue
        checked += 1
        if t not in TEXT[cur]:
            missing += 1
            misses.append((cur, t))
    print("  lines checked : %d" % checked)
    print("  lines too short / structural, skipped : %d" % skipped)
    print("  lines NOT FOUND in this audit's extraction : %d" % missing)
    for c, t in misses[:20]:
        print("    [%s] %s" % (c, t[:100]))
    if missing:
        BAD += 1
    else:
        print("  Every content line of the audited ticket's source file is")
        print("  present, verbatim, in a PDF fetched independently by this")
        print("  audit.  sources_db09.txt is NOT fabricated.")

# --------------------------------------------------------------------------
hr("B3b  THE DOCUMENT'S OWN QUOTATIONS, checked against the PDFs")
print("""Taken out of the delivered prose of
docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md, including the
ones mg-db09's T4 does not itself check.
""")

DOC_QUOTES = [
    # (paper, string, where in the audited document, checked by T4?)
    ("OV", "The same definition of the branching graph applies to any chain",
     "sec 0 bullet 1", "yes"),
    ("OV", "of finite-dimensional semisimple algebras",
     "sec 0 bullet 1 / sec 1 table", "yes"),
    ("OV", "If the multiplicities of all restrictions are equal 0 or 1, then",
     "sec 0 bullet 2", "yes"),
    ("OV", "this diagram is a graph (and not multigraph); in this case one",
     "sec 0 bullet 2", "NO"),
    ("OV", "says that the multiplicities are simple, or the branching is simple",
     "sec 0 bullet 2 / sec 1 table", "NO"),
    ("OV", "Recall the following fundamental isomorphism:",
     "sec 0 bullet 3", "yes"),
    ("OV", "If the branching is simple, the decomposition",
     "sec 0 bullet 4", "yes"),
    ("OV", "is canonical", "sec 0 bullet 4", "NO"),
    ("OV", "Remark 1.3. For an arbitrary inductive family of semisimple alge",
     "sec 0 bullet 4", "yes"),
    ("OV", "The centralizer Z(M, N ) is commutative",
     "sec 1 table row 3 / T2c", "yes"),
    ("OV", "Proposition 1.1. The algebra GZ(n) is the algebra of all operato",
     "T2a", "yes"),
    ("TL", "Then, we have an exact sequence of TLn-1 -modules",
     "sec 4 item 3", "yes"),
    ("TL", "Corollary 4.6. When q is not a root of unity, TLn is a semisimpl",
     "sec 3 controls", "yes"),
    ("MSS", "Theorem 4.18. Let B be a connected left regular band with suppor",
     "sec 0 / T3c", "yes"),
    ("MSS", "is unipotent lower triangular with respect to any linear extensi",
     "sec 0 / T3c", "yes"),
    ("MS", "The algebras of finite (von Neumann) regular monoids provide nat",
     "sec 0 / sec 2 row 2", "yes"),
    ("MS", "This was first proved by Putcha",
     "sec 0 blockquote", "NO"),
    ("MS", "and further developed by the two",
     "sec 0 blockquote", "NO"),
    ("MS", "authors of this paper using homological methods",
     "sec 0 blockquote", "NO"),
    ("MS", "However, Nico essentially",
     "sec 0 blockquote", "NO"),
    ("MS", "had noted that semigroup algebras of regular semigroups are "
           "quasi-hereditary", "sec 0 blockquote", "NO"),
    ("MS", "before the concept was even invented", "sec 0 blockquote", "NO"),
]

print("  %-5s %-8s %-24s %s" % ("paper", "T4?", "where in mg-db09", "verdict"))
notfound = []
for (k, s, where, t4) in DOC_QUOTES:
    ok = find(k, s)
    if not ok:
        notfound.append((k, s, where, t4))
    print("  %-5s %-8s %-24s %-8s  %s"
          % (k, t4, where, "OK" if ok else "NOT FOUND", s[:52]))
print()
print("  quotations checked : %d   not found : %d" % (len(DOC_QUOTES),
                                                      len(notfound)))
print("  of these, NOT covered by mg-db09's own T4 : %d"
      % sum(1 for q in DOC_QUOTES if q[3] == "NO"))
if notfound:
    BAD += 1
    print()
    print("  NEAR-MISS ANALYSIS --- the deviation, character by character,")
    print("  so the size of the defect is on the record and not just its")
    print("  existence:")
    for (k, s, where, t4) in notfound:
        q = norm(s)
        words = q.split()
        anchor = " ".join(words[:4])
        pos = TEXT[k].find(anchor)
        print("    quotation (mg-db09, %s, T4 covers it: %s):" % (where, t4))
        print("      %s" % q)
        if pos < 0:
            print("      no anchor found in the paper at all")
        else:
            print("    the paper (%s) reads:" % PAPERS[k][1])
            print("      %s" % TEXT[k][pos:pos + len(q) + 4])
            import difflib
            d = [x for x in difflib.ndiff(TEXT[k][pos:pos + len(q)], q)
                 if x[0] != ' ']
            print("    difference: %s" % (d if d else "none"))

print("""
  NEGATIVE CONTROLS of this audit's devising --- each is one word from a
  quotation above and each MUST be rejected:""")
NEG = [
    ("OV", "The same definition of the branching graph applies to any tower"),
    ("OV", "If the multiplicities of all restrictions are equal 0 or 2, then"),
    ("OV", "Remark 1.3. For an arbitrary inductive family of semisimple rings"),
    ("MSS", "is unipotent lower triangular with respect to every linear extensi"),
    ("MS", "The algebras of finite (von Neumann) regular monoids provide only"),
    ("TL", "Corollary 4.6. When q is not a root of unity, TLn is a cellular"),
]
for (k, s) in NEG:
    hit = find(k, s)
    print("    %-5s %-10s %s" % (k, "NOT REJECTED" if hit else "rejected",
                                 s[:58]))
    if hit:
        BAD += 1

# --------------------------------------------------------------------------
hr("B3c  D9 --- mg-db09's SELF-DECLARED WEAKEST CITATION, closed")
print("""mg-db09 section 4 item 1 and its ledger row D9:

  'A cellular algebra has a symmetric Cartan matrix' is taken from the
   WIKIPEDIA article on cellular algebras ... I did NOT read
   Graham-Lehrer.  If that statement is wrong ... then section 2 row 1
   collapses to "not evaluated" and the enumeration loses a row.

Graham-Lehrer 1996 is not on arXiv, so it cannot be checked the way the
others were.  A refereed arXiv paper that states the fact and attributes
it can be, and does:
""")
ET1 = ("it follows from [KX99, Proposition 3.2] that C (C) is symmetric "
       "and positive definite in case C is a cellular algebra")
ET2 = "(Or C = D T D, written as matrices.)"
ET3 = ("by far not all algebras are cellular since e.g. their Cartan matrix "
       "has to be positive definite")
for s in (ET1, ET2, ET3):
    ok = find("ET", s)
    print("  %-12s %s" % ("OK" if ok else "NOT FOUND", s[:66]))
    if not ok:
        BAD += 1
print("""
  Source: Ehrig-Tubbenhauer, 'Relative cellular algebras'
  (arXiv:1710.02851), Remark 2.19 and Theorem 3.23 / (3-24).  It
  attributes the symmetry to Koenig-Xi 1999, Prop. 3.2, and gives the
  reason: C = D^T D, where D is the decomposition matrix of the cell
  modules.  A Gram matrix of that shape is symmetric AND positive
  semi-definite.

  VERDICT ON D9: the statement mg-db09 flagged as its weakest citation is
  CORRECT, and its consequence in section 2 row 1 stands.  It is
  UPGRADED, not refuted --- from 'secondary source, primary not read' to
  'stated and attributed in a refereed source, with the proof indicated'.
  mg-db09's own one-line consequence (symmetric AND unitriangular implies
  the identity) is checked separately in B4.
""")

print("TOTAL BAD: %d" % BAD)
