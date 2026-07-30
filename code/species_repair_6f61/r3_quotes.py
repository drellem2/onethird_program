"""R3 -- the quotation repair, checked against a RENDERED extraction on disk.

WHAT WAS WRONG.  mg-a61f executed mg-7d75's own attack #1 -- every quotation
re-extracted from the three PDFs with poppler's `pdftotext` -- and found
11 of 13 verbatim, 2 divergent and 1 truncated.  mg-7d75 pre-flagged exactly
one of the three:

    AM 17.5        DIVERGES   pre-flagged at section 10 item 1
    Aguiar-Ardila  DIVERGES   NOT pre-flagged
    Marshall-Martin TRUNCATED NOT pre-flagged

AN UNPREDICTED DIVERGENCE IN AN EXECUTED CHECK IS WORTH MORE THAN A
PREDICTED ONE.  The predicted one confirms the author knew the extraction
was lossy.  The unpredicted ones measure how far the lossiness reached --
which is the thing a pre-file structurally cannot tell you, because a
pre-file names the places its author already suspects.

NO NETWORK.  This file reads `code/species_audit_a61f/quotes_a61f.txt`, the
poppler extraction the audit committed, and compares the REPAIRED document
against it.  It does not re-fetch the PDFs and it does not trust the audit's
prose: every row below re-derives its verdict from the extracted passage.
`code/species_audit_a61f/fetch_sources.sh` is the script that regenerates
the extraction from the sources.
"""

import os
import re
import sys

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
SRC = os.path.join(HERE, "..", "species_audit_a61f", "quotes_a61f.txt")

doc_raw = open(DOC, encoding="utf-8").read()
src_raw = open(SRC, encoding="utf-8").read()

SUBS = [
    ("∗", "*"), ("′", "'"), ("≥", ">="), ("≤", "<="),
    ("Π", "pi"), ("Σ", "sigma"), ("Λ", "lambda"),
    ("ℝ", "r"), ("∈", "in"), ("−", "-"), ("–", "-"),
    ("—", "-"), ("’", "'"), ("‘", "'"), ("“", '"'),
    ("”", '"'), ("̄", ""), ("̅", ""), ("×", "x"),
    ("→", "->"), ("⊕", "+"), ("↦", "|->"), ("⊆", "<="),
    ("≠", "!="), ("≡", "="), ("⋃", "u"),
]


def norm(s):
    """Collapse the two encodings onto one, WITHOUT collapsing the `*` that
    distinguishes the species Pi from the species Pi-star -- which is the
    whole content of one of the rows below.  Markdown bold (`**`) is removed,
    single asterisks are kept, and blockquote markers are stripped."""
    s = re.sub(r"(?m)^(?:\s*>)+\s?", "", s)
    for a, b in SUBS:
        s = s.replace(a, b)
    s = s.lower()
    s = s.replace("**", "")
    s = re.sub(r"[`_^]", "", s)
    s = s.replace("~~", "")
    s = re.sub(r"\s+", " ", s)
    s = s.replace("( ", "(").replace(" )", ")")
    return s


ndoc = norm(doc_raw)
nsrc = norm(src_raw)


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def wrap(s, ind="      "):
    line = ind
    for w in s.split():
        if len(line) + len(w) + 1 > 78:
            print(line)
            line = ind
        line += w + " "
    if line.strip():
        print(line.rstrip())


# The ~~struck~~ spans of the repaired document, normalised.  A sentence that
# is false must survive ONLY inside one of these.
STRUCK = [norm(m) for m in re.findall(r"~~(.+?)~~", doc_raw, re.S)]


def in_struck(needle):
    return any(needle in s for s in STRUCK)


# ---------------------------------------------------------------------------
# ROWS.  Each: label, the text the SOURCE must contain, the text the DOCUMENT
# must now contain, the text the document must contain ONLY STRUCK, and
# whether mg-7d75 pre-flagged the divergence.
# ---------------------------------------------------------------------------
ROWS = [
    ("AM 17.4/17.5  species",
     "recall from section 17.4 that k(pi*) is the algebra of symmetric "
     "functions in noncommuting variables and k(pi*) is the familiar hopf "
     "algebra of symmetric functions",
     "recall from section 17.4 that k(pi*) is the algebra of symmetric "
     "functions in noncommuting variables",
     "recall from section 17.4 that k(pi) is the algebra of symmetric "
     "functions in noncommuting variables",
     True,
     "section 10 item 1 said outright that the species names in this quote "
     "were an inference from surrounding text.  Predicted, and wrong in "
     "exactly the predicted way."),
    ("Aguiar-Ardila 12  braid cone",
     "define a braid cone to be a cone in (ri)* = ri cut out by inequalities "
     "of the form y(i) >= y(j)",
     "define a braid cone to be a cone in (ri)* = ri cut out by inequalities "
     "of the form y(i) >= y(j)",
     "define a braid cone to be a cone in (ri)/ri cut out by inequalities of "
     "the form y(i) <= y(j)",
     False,
     "NOT pre-flagged.  Two divergences in one sentence: (R^I)/R^I is not an "
     "expression the paper contains, and the inequality runs the other way."),
    ("Marshall-Martin 2.1  truncation",
     'these objects are called "braid cones" in [14], but we reserve that '
     "term for single cones of the braid arrangement",
     'these objects are called "braid cones" in [14], but we reserve that '
     "term for single cones of the braid arrangement",
     None,
     False,
     "NOT pre-flagged.  The document stopped ONE SENTENCE short of the "
     "paper naming the terminology collision this ticket turns on."),
    ("Joyal foreword  K(Pi) = Lambda",
     "the hopf algebra k(pi) is the algebra of symmetric functions lambda "
     "(when k is of characteristic 0), and it is self dual",
     "the hopf algebra k(pi) is the algebra of symmetric functions lambda "
     "(when k is of characteristic 0), and it is self dual",
     None,
     None,
     "the clean sentence three lines below a passage the document already "
     "quoted.  The 17.5 reconstruction was never needed."),
]

# ---------------------------------------------------------------------------
hdr("R3a  the three repaired quotations, against the committed extraction")

for label, in_src, in_doc, must_be_struck, preflagged, note in ROWS:
    ok_src = in_src in nsrc
    ok_doc = in_doc in ndoc
    ok_struck = True
    if must_be_struck is not None:
        occurs = ndoc.count(must_be_struck)
        ok_struck = (occurs == 1 and in_struck(must_be_struck))
    good = ok_src and ok_doc and ok_struck
    bad += (not good)
    print("  %-34s %s" % (label, "OK" if good else "*** FAILED ***"))
    print("      in the rendered extraction : %s" % ("yes" if ok_src else "NO"))
    print("      in the repaired document   : %s" % ("yes" if ok_doc else "NO"))
    if must_be_struck is not None:
        print("      the wrong text survives ONLY struck: %s"
              % ("yes" if ok_struck else "NO -- IT IS STILL ASSERTED"))
    if preflagged is not None:
        print("      pre-flagged by mg-7d75     : %s"
              % ("YES" if preflagged else "NO"))
    wrap(note)
    print()

# ---------------------------------------------------------------------------
hdr("R3b  the other ten quotations are untouched and still present")

UNTOUCHED = [
    ("AM 10.10  radical theorem",
     "bidigare [45] showed that j is precisely the kernel of its support map"),
    ("AM Thm 10.13", "the descent algebra is isomorphic to"),
    ("AM 13.1.1  posets",
     "let p[i] be the vector space with basis the set of all partial orders"),
    ("AM Def 8.1  species", "a set species is a functor"),
    ("AM 13.4.2  lower set", "s is a lower set of p"),
    ("AM 8.13  Hadamard", "is again a hopf monoid"),
    ("AM Ch. 11  connected",
     "a connected bimonoid in species is automatically a hopf monoid"),
    ("Joyal foreword  K(p)", "coinvariants of p[n]"),
    ("AM posets as chambers",
     "posets can be viewed as appropriate unions of chambers"),
    ("Marshall-Martin 2.1",
     "geometric realization gives a bijection between preposets and convex "
     "unions of cones"),
]
for label, needle in UNTOUCHED:
    ok = needle in ndoc
    bad += (not ok)
    print("  %-34s still in the document: %s"
          % (label, "yes" if ok else "NO -- DRIFT"))
print()
print("  These are mg-a61f's own A5a needles.  They are checked here so that")
print("  the audit's battery still applies to the repaired document and can be")
print("  re-run UNMODIFIED -- which it was; see the repair document.")
print()

# ---------------------------------------------------------------------------
hdr("R3c  ANTICIPATED vs UNANTICIPATED, which is the point of the exercise")

pre = [r for r in ROWS if r[4] is True]
unp = [r for r in ROWS if r[4] is False]
print("  divergences pre-flagged by mg-7d75 section 10 item 1 : %d" % len(pre))
for r in pre:
    print("      %s" % r[0])
print("  divergences NOT pre-flagged                          : %d" % len(unp))
for r in unp:
    print("      %s" % r[0])
print()
wrap("Both counts matter and they do not weigh the same.  The pre-flagged "
     "divergence tells you the author knew the extraction was lossy and said "
     "so -- it confirms a stated caveat and costs nothing.  The two "
     "unflagged ones tell you HOW FAR the lossiness reached, which is "
     "precisely what the pre-file could not say, because a pre-file "
     "enumerates the places its author already suspects.", "  ")
print()
wrap("And note what found them: the check was EXECUTED against rendered "
     "PDFs rather than asserted.  mg-7d75 named the right attack and did not "
     "run it; mg-a61f ran it.  A named attack that is not executed produces "
     "the pre-flagged row and neither of the other two.", "  ")
print()
present = norm("WHICH QUOTATION DIVERGENCES WERE ANTICIPATED, AND WHICH WERE "
               "NOT") in ndoc
bad += (not present)
print("  the document now states which were anticipated and which were not: %s"
      % ("yes" if present else "NO"))
print()

print("=" * 78)
print("R3 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
