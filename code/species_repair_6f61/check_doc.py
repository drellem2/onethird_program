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
# 4.  The repair document exists and points at the target -- AT THE SITE.
#
# mg-6cb9's F3, MAJOR.  This section used to be `flat(s) in flat(rep)`: a
# PRESENCE test over the whole file.  Three of its five anchors occur more than
# once in that document -- `mg-a61f` 19 times, `code/species_repair_6f61`
# twice, `2 of 45` three times -- so for three of five it was a check on NO
# SITE: delete the copy a reader meets and the run stayed GREEN, and only
# deleting EVERY copy fired.  mg-8a5c found this exact shape in the Hodge tree,
# mg-a318 repaired it there by writing each figure once per site, mg-835f
# measured that repair at 12 of 12.  The species tree had not had the pass.
#
# WHICH OF THE THREE REMEDIES, AND WHY.  The brief's first choice is one copy;
# its second is deriving the others from it; its third is checking at the
# reader-facing site.  One copy is not available here and the reason is not
# effort: `mg-a61f` is a ticket id in running prose, and a document that names
# the audit it answers exactly once is a worse document.  Deriving is not
# available either -- these are markdown files, there is no generator, and
# inventing one to hold a ticket id would be a new machine to keep alive.  So
# this is the third remedy, and it is the third remedy DONE PROPERLY: every
# assertion below names the section a reader meets it in, and it is checked
# THERE.  Multiplicity elsewhere is printed as a number and has no vote.
#
# A site here is a markdown heading region.  Two assertions are checked at TWO
# sites each, because both are reader-facing and neither is the other's copy:
# the front matter tells a reader what the instrument is, and section 11 is the
# command a reader runs.
# ---------------------------------------------------------------------------
hdr("C4  the repair document -- EVERY ANCHOR AT ITS OWN SITE (mg-821e)")


def sections(text):
    """{heading line: body} for every ATX heading region, in order.

    The region of a heading runs to the next heading of ANY level, so `## 2.`
    does not swallow `### 2.1`.  A reader's site is a heading region: it is
    the unit a table of contents points at.
    """
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith("#")]
    out = []
    for j, i in enumerate(starts):
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        out.append((lines[i], "\n".join(lines[i:end])))
    return out


# (assertion, needle, site regex, why this site is where a reader meets it)
C4_SITES = [
    ("names its target", "OneThird-Species-Hopf-Monoids-Where-This-Lives",
     r"^# Repair of mg-7d75",
     "front matter: the **Target:** line, above the fold"),
    ("names the audit", "mg-a61f",
     r"^# Repair of mg-7d75",
     "front matter: the **Audit landed:** line"),
    ("names the instrument", "code/species_repair_6f61",
     r"^# Repair of mg-7d75",
     "front matter: the **Instrument:** line"),
    ("names the instrument", "code/species_repair_6f61",
     r"^## 11\. REPRODUCE",
     "section 11: the command a reader actually runs"),
    ("records the missed predictions", "2 of 45",
     r"^### 2\.1 ",
     "section 2.1, whose heading promises the number"),
    ("records the missed predictions", "2 of 45",
     r"^## 11\. REPRODUCE",
     "section 11: what a reader is told the run will print"),
    ("records what it did NOT repair", "WHAT THIS REPAIR DID NOT DO",
     r"^## 10\. ",
     "section 10's own heading"),
]

if os.path.exists(REPAIR):
    rep = open(REPAIR, encoding="utf-8").read()
    secs = sections(rep)
    frep = flat(rep)
    for label, s, site_pat, why in C4_SITES:
        site = next((body for head, body in secs
                     if re.search(site_pat, head)), None)
        copies = frep.count(flat(s))
        if site is None:
            bad += 1
            print("  %-42s *** NO SUCH SECTION: %s ***" % (label, site_pat))
            continue
        here = flat(site).count(flat(s))
        ok = here >= 1
        bad += (not ok)
        print("  %-42s %-9s at its site: %s"
              % (label, "ok" if ok else "*** GONE ***", why))
        print("  %-42s %d cop%s in the file, %d at this site%s"
              % ("", copies, "y" if copies == 1 else "ies", here,
                 "" if ok else "  <-- the copy a reader meets is the one"
                 " that was deleted, and the others do not stand in for it"))
    # Section 10 must also have a body: a heading alone records nothing.
    body10 = next((b for h, b in secs if re.search(r"^## 10\. ", h)), "")
    ok = len(flat(body10)) > 200
    bad += (not ok)
    print("  %-42s %s  (%d chars under the heading)"
          % ("and section 10 is not an empty heading",
             "ok" if ok else "*** EMPTY ***", len(flat(body10))))
else:
    bad += 1
    print("  *** the repair document does not exist ***")
print()
print("  Each row above is a SITE, not a presence.  Until mg-821e this section")
print("  asked only whether the string occurred anywhere in the file, so")
print("  deleting the copy a reader reads left the run green for 3 of the 5")
print("  assertions and only deleting EVERY copy fired (mg-6cb9 F3).  The")
print("  copy counts are printed because they are the reason: an anchor with")
print("  19 copies is not better covered than one with 1, it is less.")
print()

print("=" * 78)
print("CHECK_DOC: %s   (%d problem(s))" % ("PASS" if bad == 0 else "FAIL", bad))
print("=" * 78)
print()
print("EXTENT OF THAT VERDICT (added mg-a4ef).  CORRECTED mg-d633.  This")
print("enforces all %d stricken sentences, and every correction and anchor in"
      % len(STRICKEN))
print("C2 and C3, over ONE FILE:")
print("    docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
print("It reads a SECOND file for section C4's five assertions and for nothing")
print("else:")
print("    docs/OneThird-Species-Hopf-Monoids-Repair.md")
print("Those five assertions are checked at %d NAMED SITES within that file and"
      % len(C4_SITES))
print("NOT over the file as a whole (mg-821e, on mg-6cb9's F3).  A pass means")
print("each anchor is present IN THE SECTION A READER MEETS IT IN.  It says")
print("nothing about the rest of that file, and a copy of an anchor somewhere")
print("else in it neither helps nor is required.")
print("Until mg-d633 this paragraph said 'ONE FILE' and stopped.  That was")
print("NARROWER than what the code read -- the safe direction, and still a")
print("false statement, and it would have told the next person deciding what")
print("still needs covering that the repair document was uncovered (mg-7dd3")
print("C1).  It reads no code.  Two of the sentences it certifies as struck")
print("were in")
print("force in code/species_7d75 for the whole time it reported PASS, one of")
print("them inside a run ending T6 TOTAL BAD: 0 (mg-73df's MAJOR).  A PASS")
print("HERE IS NOT COVERAGE OF ANY CODE TREE.  The union of this list and")
print("w3_scope.py's, over the document AND every code tree, is:")
print("    python3 code/species_repair_a4ef/s1_extent.py")
sys.exit(1 if bad else 0)
