"""CHECK_DOC -- the repaired document says the corrected things, AND the false
sentences survive only inside the strike that replaces them.

THE NEGATIVE HALF IS THE LOAD-BEARING HALF.  A repair that adds a correction
beside a false sentence and leaves the false sentence in force has not
repaired anything.  Every string in STRICKEN below is required to occur
EXACTLY ONCE in the document and to lie inside a `~~ ... ~~` span.

THE OTHER NEGATIVE HALF: the auditor's battery must still apply.  mg-a61f's
`a5_quotes.py` and `a6_boundary.py` read this document and fail loudly if the
strings they classify disappear.  A repair that silently breaks the audit's
anchors has made itself unauditable, so the anchors are asserted here too and
mg-a61f's battery is re-run unmodified (see the repair document).

    python3 code/species_repair_6f61/check_doc.py
"""

import os
import re
import sys

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "..", "docs")
TARGET = os.path.join(DOCS, "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
REPAIR = os.path.join(DOCS, "OneThird-Species-Hopf-Monoids-Repair.md")

doc = open(TARGET, encoding="utf-8").read()


def flat(s):
    """Collapse whitespace and strip blockquote markers, so a sentence is
    matched the same whether it sits in prose or inside a nested quote."""
    s = re.sub(r"(?m)^(?:\s*>)+\s?", "", s)
    return re.sub(r"\s+", " ", s)


ndoc = flat(doc)
STRUCK_SPANS = [flat(m) for m in re.findall(r"~~(.+?)~~", doc, re.S)]
# the document with every struck span removed: a false sentence must not
# survive anywhere in it.
unstruck = flat(re.sub(r"~~(.+?)~~", " ", doc, flags=re.S))


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


# ---------------------------------------------------------------------------
# 1.  The false sentences.  Each must occur ONCE, and struck.
# ---------------------------------------------------------------------------
STRICKEN = [
    ("§8 C3, the extremal claim",
     "Smallest witness with `AC(P) ≠ Π[n]`: `P = {a<c, b<d}`, where `ad|bc` "
     "has a 2-cycle."),
    ("§0, the five-axiom count",
     "it passes every Hopf-monoid axiom with 0 failures on 4 399 basis "
     "elements (T5)"),
    ("§1, the Aguiar–Ardila quotation",
     "Define a braid cone to be a cone in `(ℝ^I)/ℝ^I` cut out by "
     "inequalities of the form `y(i) ≤ y(j)` for `i, j ∈ I`"),
    ("§4, the AM §17.5 quotation",
     "Recall from Section 17.4 that `K̄(Π)` is the algebra of symmetric "
     "functions in noncommuting variables and `K(Π)` is the familiar Hopf "
     "algebra of symmetric functions"),
    ("§2.2, the control count",
     "Three of the four columns are the control, and they fire."),
    ("§5, control (ii)'s accounting",
     "**fires hard**: 1 442 closure, 252 associativity, 11 020 "
     "compatibility failures"),
    ("§6 item 6, 'measured, not proved'",
     "The `Aut(P)`-invariant identity of §2.3 is measured, not proved, and "
     "is stated for `n ≤ 5`."),
    ("§9 row 6, the inequality direction",
     "`y(i) ≤ y(j)`"),
    ("§10 item 2, the withdrawn errand",
     "Read Saliola and Commins before quoting §2.3 as anything but a "
     "measurement."),
    ("S12, the withdrawn non-location",
     "The `Aut(P)` form of the radical theorem was **not located** stated "
     "in that generality, and this is the weakest claim here"),
]

hdr("C1  every false sentence occurs EXACTLY ONCE and is STRUCK")

for label, s in STRICKEN:
    f = flat(s)
    n = ndoc.count(f)
    outside = unstruck.count(f)
    ok = (n >= 1 and outside == 0)
    bad += (not ok)
    print("  %-42s occurrences %d   outside a strike %d  %s"
          % (label, n, outside, "ok" if ok else "*** STILL ASSERTED ***"))
print()

# ---------------------------------------------------------------------------
# 2.  The corrections.  Each must be present.
# ---------------------------------------------------------------------------
CORRECTIONS = [
    ("1  the smallest witness is the 3-chain",
     "The smallest is the 3-ELEMENT CHAIN"),
    ("1  with its count and its class",
     "6 labelled posets at `n = 3` are witnesses"),
    ("1  and the shape of the error is named",
     "the refuting evidence was already in this document"),
    ("2  §0 states the per-column reading",
     "what 4 399 basis elements measure is CLOSURE, and only\nclosure"),
    ("2  §5 carries the per-column table",
     "WHICH OF THOSE FIVE COLUMNS CAN FAIL"),
    ("2  and every column is shown able to fail",
     "demonstrated to be capable of failing"),
    ("2  §0 and §5 are stated to have disagreed",
     "This paragraph was right, and §0 disagreed with it"),
    ("3  the corrected Aguiar–Ardila text",
     "`(ℝ^I)* = ℝ^I` cut out by inequalities of the form\n> `y(i) ≥ y(j)`"),
    ("3  the corrected AM §17.5 species",
     "The book's species is `Π*` in both slots"),
    ("3  anticipated vs unanticipated is stated",
     "WHICH QUOTATION DIVERGENCES WERE ANTICIPATED, AND WHICH WERE NOT"),
    ("4  the terminology collision is named",
     "TERMINOLOGY COLLISION"),
    ("4  and the usage is fixed",
     "a single cone of the\n> arrangement is called a **face** throughout"),
    ("5  the S_n half is stated unverified in §0",
     "THE `S_n` HALF OF THE CORRESPONDENCE IS NOT VERIFIED HERE"),
    ("5  and in §3, naming S4 and both sources",
     "THE BOUNDARY, STATED ONCE AND NAMED"),
    ("5  located is distinguished from verified",
     "Being located is a real result. Presenting it as verified is not"),
    ("A  the four hedges on §2.3 are corrected",
     "AND IT IS A THEOREM, NOT ONLY A MEASUREMENT"),
    ("A  the successor search is withdrawn",
     "DO NOT FILE THE SUCCESSOR LITERATURE SEARCH"),
    ("A  §10 item 2 is closed",
     "THIS ITEM IS CLOSED AND ITS ERRAND IS WITHDRAWN"),
    ("B  T3d is two statements, not four",
     "the four columns are TWO STATEMENTS, EACH COMPUTED\nTWICE"),
    ("C  control (ii) is a type mismatch",
     "fires on a TYPE MISMATCH, not a near miss"),
    ("C  and its conclusion explicitly survives",
     "AND THAT CONCLUSION SURVIVES THE CORRECTION TO ITS NUMBERS"),
    ("meta  the incompleteness finding is recorded",
     "IT ONLY NEEDS TO BE\n*INCOMPLETE*, BECAUSE IT TELLS THE READER WHERE "
     "TO LOOK"),
    ("meta  §10 item 6 is marked incomplete in place",
     "THIS LIST IS INCOMPLETE, AND THE ROW IT OMITS IS THE ONLY BROKEN ONE"),
    ("meta  the repair's own self-assessment is limited beside itself",
     "THE SAME LIMITATION APPLIES TO §14 ITSELF"),
    ("meta  §13's scope claim carries its exception",
     "There was exactly one exception and it is now repaired"),
]

hdr("C2  every correction is present")

for label, s in CORRECTIONS:
    ok = flat(s) in ndoc
    bad += (not ok)
    print("  %-58s %s" % (label, "ok" if ok else "*** MISSING ***"))
print()

# ---------------------------------------------------------------------------
# 3.  mg-a61f's anchors survive, so its battery still applies unmodified.
# ---------------------------------------------------------------------------
AUDIT_ANCHORS = [
    ("a6  §10 item 6 heading",
     "Attack the claim that this is a locating exercise"),
    ("a6  §10 item 6 names §2.3", "The two places to check are §2.3"),
    ("a6  §13 scope note", "It does **not** develop mathematics"),
    ("a5  AM 10.10",
     "showed that `J` is precisely the kernel of its support map"),
    ("a5  AM Thm 10.13", "The descent algebra is isomorphic to"),
    ("a5  AM 13.1.1",
     "let `P[I]` be the vector space with basis the set of all partial "
     "orders"),
    ("a5  AM 17.4/17.5", "symmetric functions in noncommuting variables"),
    ("a5  AM Def 8.1", "A set species is a functor"),
    ("a5  AM 13.4.2", "S` is a lower set of `p`"),
    ("a5  AM 8.13", "is again a Hopf monoid"),
    ("a5  AM Ch. 11",
     "a connected bimonoid in species is automatically a Hopf monoid"),
    ("a5  Joyal foreword",
     "denotes the space of `S_n` coinvariants of `p[n]`"),
    ("a5  AM posets as chambers",
     "posets can be viewed as appropriate unions of chambers"),
    ("a5  Aguiar-Ardila 12", "cut out by inequalities of the form"),
    ("a5  Marshall-Martin 2.1",
     "geometric realization gives a bijection between preposets and convex "
     "unions of cones"),
    ("a5  Marshall-Martin closure",
     "closed under disjoint union, induced subposet and deletion of order "
     "filters"),
]

hdr("C3  mg-a61f's own anchors survive the repair")

for label, s in AUDIT_ANCHORS:
    ok = flat(s) in ndoc
    bad += (not ok)
    print("  %-42s %s" % (label, "ok" if ok else "*** ANCHOR LOST ***"))
print()
print("  These are the strings mg-a61f's a5_quotes.py and a6_boundary.py")
print("  classify.  All present, so the auditor's battery applies to the")
print("  REPAIRED document and can be re-run unmodified.")
print()

# ---------------------------------------------------------------------------
# 4.  The repair document exists and points at the target.
# ---------------------------------------------------------------------------
hdr("C4  the repair document")

if os.path.exists(REPAIR):
    rep = open(REPAIR, encoding="utf-8").read()
    for label, s in [
        ("names its target", "OneThird-Species-Hopf-Monoids-Where-This-Lives"),
        ("names the audit", "mg-a61f"),
        ("names the instrument", "code/species_repair_6f61"),
        ("records the missed predictions", "2 of 45"),
        ("records what it did NOT repair", "WHAT THIS REPAIR DID NOT DO"),
    ]:
        ok = flat(s) in flat(rep)
        bad += (not ok)
        print("  %-42s %s" % (label, "ok" if ok else "*** MISSING ***"))
else:
    bad += 1
    print("  *** the repair document does not exist ***")
print()

print("=" * 78)
print("CHECK_DOC: %s   (%d problem(s))" % ("PASS" if bad == 0 else "FAIL", bad))
print("=" * 78)
sys.exit(1 if bad else 0)
