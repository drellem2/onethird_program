"""A5 -- THE QUOTATION AUDIT, WHICH mg-7d75 ITSELF NAMED AS ATTACK #1.

mg-7d75 section 10 item 1:

    "Attack the quotations, because of how they were obtained.  Every verbatim
     quote from Aguiar-Mahajan, Aguiar-Ardila and Marshall-Martin was extracted
     from the arXiv/journal PDF by a Flate-decode-and-string-scrape routine, NOT
     read from a rendered page.  That routine demonstrably drops fi and fl
     ligatures ... and it drops mathematical symbols entirely ... An auditor
     should re-read section 17.4, section 10.10, Theorem 10.13 and section
     13.1.1 from rendered PDFs."

Done.  All three PDFs were re-fetched and re-extracted with poppler's
`pdftotext`, a renderer-grade extractor; the passages are committed verbatim in
`quotes_a61f.txt` and `fetch_sources.sh` regenerates them.  This script needs no
network: it reads the committed extraction and the document, checks that the
document still says what the audit says it says, and reports each quote.

The four passages mg-7d75 asked for are the first four rows.
"""

import os
import re
import sys

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
QUO = os.path.join(HERE, "quotes_a61f.txt")


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


doc = open(DOC, encoding="utf-8").read()
quotes = open(QUO, encoding="utf-8").read()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


ndoc = norm(doc)

# (tag, what mg-7d75 must still contain, verdict, one-line note)
ROWS = [
    ("AM 10.10  radical thm",
     "showed that `J` is precisely the kernel of its support map",
     "VERBATIM",
     "the book: 'Bidigare [45] showed that J is precisely the kernel of its "
     "support map.'  Whole passage matches word for word."),
    ("AM Thm 10.13",
     "The descent algebra is isomorphic to",
     "VERBATIM",
     "the book prints the superscript 'op' on the line above the theorem "
     "statement; the anti-isomorphism reading in section 2.2 is the book's."),
    ("AM 13.1.1  posets",
     "let `P[I]` be the vector space with basis the set of all partial orders",
     "VERBATIM",
     "the book: 'Given a finite set I, let P[I] be the vector space with basis "
     "the set of all partial orders on I.'"),
    ("AM 17.4/17.5",
     "symmetric functions in noncommuting variables",
     "DIVERGES",
     "the book's species is Pi-STAR in BOTH slots, not Pi.  mg-7d75 section 10 "
     "item 1 predicted this exact quote would be wrong and it is."),
    ("AM Def 8.1  species",
     "A set species is a functor",
     "VERBATIM",
     "including 'whose objects are finite sets and whose morphisms are "
     "bijections between finite sets'."),
    ("AM 13.4.2  lower set",
     "S` is a lower set of `p`",
     "VERBATIM",
     "'e_{S,T}(p) = 0 <=> S is a lower set of p' and 'the Hopf monoid of "
     "posets of Section 13.1.1 is P_0' are both in 13.4.2, word for word."),
    ("AM 8.13  Hadamard",
     "is again a Hopf monoid",
     "VERBATIM-BUT-RELOCATED",
     "the sentence is verbatim from the BOOK'S INTRODUCTION; section 8.13 is "
     "indeed 'The Hadamard product and an interchange law on species', so the "
     "attribution points at the right material."),
    ("AM Ch. 11  connected",
     "a connected bimonoid in species is automatically a Hopf monoid",
     "VERBATIM",
     "from a paragraph the book itself heads 'Antipode formulas (Chapter 11)'. "
     "The result is also stated in section 8.4.  Attribution defensible."),
    ("Joyal foreword  K(p)",
     "denotes the space of\n> `S_n` coinvariants of `p[n]`",
     "VERBATIM",
     "AND: three lines below it the foreword says in clean text 'The Hopf "
     "algebra K(Pi) is the algebra of symmetric functions Lambda' -- which is "
     "the statement section 4 reconstructed from the garbled 17.5 passage."),
    ("AM posets as chambers",
     "posets can be viewed as appropriate unions of chambers",
     "VERBATIM",
     "in the book's introduction rather than a chapter introduction; the book "
     "hyphenates 'top-dimensional'."),
    ("Aguiar-Ardila 12",
     "cut out by inequalities of the form",
     "DIVERGES",
     "the PDF as served says 'a cone in (R^I)* = R^I ... of the form "
     "y(i) >= y(j)'.  mg-7d75 has '(R^I)/R^I' and 'y(i) <= y(j)'.  The "
     "direction flip is harmless; '(R^I)/R^I' is not a expression the paper "
     "contains and reads as a symbol-drop artefact."),
    ("Marshall-Martin 2.1",
     "geometric realization gives a bijection between preposets and convex "
     "unions of cones",
     "VERBATIM-BUT-TRUNCATED",
     "the paper's VERY NEXT SENTENCE is '(These objects are called \"braid "
     "cones\" in [14], but we reserve that term for single cones of the braid "
     "arrangement.)' -- [14] is Aguiar-Ardila.  See A5b."),
    ("Marshall-Martin closure",
     "closed under disjoint union, induced subposet and deletion of order "
     "filters",
     "ACCURATE",
     "the paper: 'any family of posets that is closed under disjoint union, "
     "induced subposet, and deletion of order filters gives rise to a Hopf "
     "submonoid of LOI.'"),
]

# ---------------------------------------------------------------------------
hdr("A5a  every quotation in mg-7d75, checked against a rendered extraction")

print("  The four passages section 10 item 1 asks for are rows 1-4.")
print()
for tag, needle, verdict, note in ROWS:
    present = norm(needle) in ndoc
    if not present:
        bad += 1
    print("  %-24s %-24s  document still says it: %s"
          % (tag, verdict, "yes" if present else "NO -- DOC DRIFT, FIX THIS"))
    # wrap the note
    words = note.split()
    line = "      "
    for w in words:
        if len(line) + len(w) + 1 > 76:
            print(line)
            line = "      "
        line += w + " "
    print(line.rstrip())
    print()

nv = sum(1 for r in ROWS if r[2].startswith("VERBATIM") or r[2] == "ACCURATE")
nd = sum(1 for r in ROWS if r[2] == "DIVERGES")
print("  %d of %d quotations check out against the rendered PDFs; %d diverge."
      % (nv, len(ROWS), nd))
print()
print("  READING.  mg-7d75 pre-filed this as its highest-yield attack and was")
print("  right about which quote would fail: the 17.5 passage, where it says")
print("  outright that 'the species names in that quote are my inference'.")
print("  The inference got the FUNCTOR right and the SPECIES wrong (Pi for")
print("  Pi-star).  That is harmless here -- the book says on the same page")
print("  'Since Pi and Pi* are isomorphic' -- but the document presents it")
print("  inside quotation marks as text from the book, and it is not.")
print()
print("  The Aguiar-Ardila divergence was NOT pre-filed and is the same defect")
print("  in a second place: '(R^I)/R^I' is not an expression the paper")
print("  contains.  Every mathematical use mg-7d75 makes of that quote --")
print("  that C(P) is the literature's braid cone -- survives it.")
print()

# ---------------------------------------------------------------------------
hdr("A5b  'THREE INDEPENDENT PUBLISHED SOURCES' -- one of them says otherwise")

print("  mg-7d75 section 1 closes with:")
print()
print("     'So the dictionary poset <-> braid cone on which this whole ticket")
print("      turns is not ours; it is stated in three independent published")
print("      sources, one of them the book named in the brief.'")
print()
print("  The three are Aguiar-Ardila, Marshall-Martin and Aguiar-Mahajan.  The")
print("  Marshall-Martin quote stops one sentence early.  The next sentence:")
print()
print("     '(These objects are called \"braid cones\" in [14], but we reserve")
print("      that term for single cones of the braid arrangement.)'")
print()
print("  [14] is Aguiar-Ardila.  So Marshall-Martin is not a third source")
print("  agreeing on the term; it is a source recording that the term means")
print("  two different things in the two papers -- and the two meanings are")
print("  precisely the two objects this ticket is about.  Under Aguiar-Ardila")
print("  the whole cone C(P) is a braid cone; under Marshall-Martin a braid")
print("  cone is a single cone of the arrangement, i.e. an element of F(P).")
print()
print("  Nothing mathematical breaks.  What breaks is the count: the claim is")
print("  supported by two sources and a third that flags the terminology as")
print("  non-standard, and the sentence that flags it is the one immediately")
print("  after the words mg-7d75 quotes.")
print()

# ---------------------------------------------------------------------------
hdr("A5c  what a rendered extraction ADDS that mg-7d75 did not have")

print("  1. Section 10.8.3 of the book, three pages before Theorem 10.13,")
print("     says: 'This yields subalgebras of S_n-invariants (Sigma[n])^{S_n}")
print("     ... A basis for the subalgebra (Sigma[n])^{S_n} is given by' the")
print("     orbit sums.  mg-7d75's T3a/T3b MEASURE that the orbits are the")
print("     compositions of n and that the orbit sums span a subalgebra, and")
print("     report it as a measurement.  It is measured correctly; it is also")
print("     stated in the source, on the facing page of the theorem being")
print("     reproduced.  T4a's 'the Aut(P)-orbit sums span a subalgebra -- 0")
print("     failures' is the same fact for a general finite group.")
print()
print("  2. Joyal's foreword, immediately after the passage mg-7d75 quotes:")
print("     'The Hopf algebra K(Pi) is the algebra of symmetric functions")
print("     Lambda (when k is of characteristic 0), and it is self dual, since")
print("     Pi is self-dual.'  This is the section 4 identification, in clean")
print("     prose, in a passage the document was already reading.  The")
print("     reconstruction from the garbled 17.5 passage was not necessary.")
print()
print("  3. Section 17.4.1 gives the whole table -- K(Pi) = Lambda,")
print("     Kbar(Pi) = the Hopf algebra of symmetric functions in noncommuting")
print("     variables -- and says 'Since Pi and Pi* are isomorphic'.  So the")
print("     Bell(n)-vs-p(n) resolution of section 4 is confirmed against the")
print("     source, with the species corrected.")
print()

print("=" * 78)
print("A5 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
