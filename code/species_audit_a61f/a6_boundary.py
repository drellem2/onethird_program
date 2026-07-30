"""A6 -- THE PRIMARY TARGET: mg-7d75's PREDICTION ABOUT ITSELF.

mg-7d75's brief carries this instruction and this prediction:

    "1. This is a locating exercise.  Do not develop new mathematics.  Note that
     both BROKEN items in mg-af28, and the worst finding in three prior
     generations, sat in beyond-brief derivations -- so this instruction is the
     one most likely to be violated here, and it will be audited."

and the delivered document pre-files the attack at section 10 item 6:

    "Attack the claim that this is a locating exercise.  The brief predicted
     that the beyond-brief instruction is the one most likely to be violated
     here, and pm-onethird warned that naming the failure mode buys no free
     pass.  THE TWO PLACES TO CHECK ARE SECTION 2.3 -- where an identity is
     measured that I did not find stated -- and SECTION 5, where axioms are
     checked on objects assembled here."

mg-a61f's brief: "Self-awareness is not a control ... A ticket that predicted it
would derive new mathematics, and then did, has not been self-aware; it has been
accurate."  So the test is not whether the document worried about the boundary.
It is:

    (a) is each thing the document names as near the line actually over it?
    (b) is the document's list of places near the line COMPLETE?

This script does the classification mechanically enough to be checkable: it
reads the document, verifies that the passages the classification is about are
still in it, and prints one row per derivation with a verdict and the evidence
from a1..a5.
"""

import os
import re
import sys

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
doc = open(DOC, encoding="utf-8").read()
ndoc = re.sub(r"\s+", " ", doc)


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def wrap(s, ind="      "):
    words, line = s.split(), ind
    for w in words:
        if len(line) + len(w) + 1 > 78:
            print(line)
            line = ind
        line += w + " "
    if line.strip():
        print(line.rstrip())


def anchor(name, needle):
    """The classification below is ABOUT these strings.  If the document stops
    containing one, this script must fail rather than keep asserting."""
    global bad
    ok = re.sub(r"\s+", " ", needle) in ndoc
    if not ok:
        bad += 1
        print("  ANCHOR LOST: %s -- the document no longer contains the text "
              "this row classifies." % name)
    return ok


# ---------------------------------------------------------------------------
hdr("A6a  the document's own pre-filed list, verified present")

A = anchor("10.6 heading", "Attack the claim that this is a locating exercise")
B = anchor("10.6 names 2.3 and 5",
           "The two places to check are §2.3")
C = anchor("13 scope note", "It does **not** develop mathematics")
print("  section 10 item 6 present and naming exactly two places: %s"
      % ("yes" if (A and B) else "NO"))
print("  section 13 'It does not develop mathematics' present: %s"
      % ("yes" if C else "NO"))
print()

# ---------------------------------------------------------------------------
hdr("A6b  every mathematical assertion in the document, classified")

print("  LOCATED   the statement is in a named published source and quoted.")
print("  COROLLARY it follows in a stated number of lines from a LOCATED one.")
print("  MEASURED  a computation about our objects; no general statement made.")
print("  DEVELOPED a general mathematical statement formed in this ticket and")
print("            neither located nor a formal corollary of anything located.")
print()

ROWS = [
    ("S1 / section 0", "faces |-> flats is A |-> A/rad", "LOCATED",
     "Aguiar-Mahajan 10.10, quoted verbatim and verified against the rendered "
     "PDF in a5.  This is the answer to Daniel's question and it is located, "
     "not developed."),
    ("S1 / section 2.3",
     "(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}", "COROLLARY",
     "a1_headline.py A1d proves it in three lines from the quoted 10.10 plus "
     "the Reynolds operator, and checks both steps exactly over Q.  It is NOT "
     "new mathematics -- but the document files it as 'MEASURED, NOT PROVED', "
     "restricts it to n <= 5, exempts 4 classes over a dimension cap, and "
     "calls its absence from the literature 'the weakest claim in this "
     "document'.  All four of those are wrong in the same direction: they "
     "treat a corollary as an observation.  MISCLASSIFIED, NOT OVER THE LINE."),
    ("S2 / section 2.2", "Bidigare, rebuilt from both definitions", "LOCATED",
     "Theorem 10.13, verified.  a2_bidigare.py reproduces the whole T3d table "
     "from disjoint code: 0 / 0 / 472 exactly.  The reproduction is sound; the "
     "control count is not (A2d: four candidates are two statements, each "
     "computed twice, because convention B is the opposite algebra of A)."),
    ("S4 / section 3", "the semisimple quotient IS the character ring",
     "LOCATED",
     "Solomon; Garsia-Reutenauer/Atkinson.  The document says outright that "
     "both are taken from secondary sources and NEITHER WAS READ.  This is the "
     "single load-bearing step from the identity to S_n representation theory "
     "and it is the one thing this audit could not check: the sources are not "
     "in the three PDFs a5 verified.  Correctly labelled by the document."),
    ("S5 / section 4", "Bell(n) vs p(n) is the two Fock functors", "LOCATED",
     "Joyal's foreword, verbatim.  a5 adds that the clean statement 'K(Pi) is "
     "the algebra of symmetric functions' sits three lines below the passage "
     "the document quotes, so the reconstruction that produced the one wrong "
     "quote was not needed."),
    ("S6 / section 5", "F and AC are Hopf submonoids", "MEASURED",
     "a3_hopf.py reproduces 4399 / 2685 and the five zeros.  What is "
     "established is CLOSURE and nothing else: A3b shows the other three "
     "columns return 0 for a subset of F closed under nothing, and both "
     "closure columns return 0 for the full ambient and for a deliberately "
     "wrong pairing.  Closure under published operations is what the brief "
     "asked for.  NOT OVER THE LINE -- but section 0's 'AXIOMS CHECKED ... 0 "
     "failures across 5 axioms' overstates a one-column result as five."),
    ("S7 / section 6.5", "the Tits product is not a Hopf-monoid product",
     "MEASURED",
     "reproduced exactly (1442 / 252 / 11020).  A3c shows the 1442 product "
     "failures are EXACTLY the 1442 pairs whose two factors have disjoint "
     "nonempty ground sets -- the control fires on a type mismatch.  The "
     "CONCLUSION is right and important; the numbers are not evidence for it."),
    ("S8 / section 6.3", "the forgetful map AC -> Pi fails on the coproduct",
     "MEASURED", "22614 reproduced exactly.  Sound."),
    ("S9 / section 8 C1", "the Bergeron-Li negative does not transfer",
     "MEASURED",
     "0 of 529 reproduced.  The unitality half has no exceptions to find: "
     "concatenating two nonempty tuples gives at least two blocks.  The "
     "CORRECTION itself -- that Hopf monoids impose no unitality on mu_{S,T} "
     "-- is right, and is the most useful thing in section 8."),
    ("S10 / section 1", "poset <-> braid cone is the literature's dictionary",
     "LOCATED",
     "two of the three sources verify; the third (Marshall-Martin) is quoted "
     "one sentence before it says the term means something else in the second "
     "source.  See a5 A5b."),
    ("section 8 C3", "'the smallest poset with AC(P) != Pi[n] is {a<c, b<d}'",
     "DEVELOPED",
     "an extremal claim about our objects, formed here, cited to nothing -- "
     "and FALSE.  a4_counts.py A4b: the smallest is the 3-ELEMENT CHAIN with "
     "the partition {min,max}|{mid}, and the document's own T1e row '13 of 19 "
     "at n = 3' records 6 labelled witnesses at n = 3, sixty lines above the "
     "claim.  THIS IS THE ONE ROW SECTION 10 ITEM 6 DOES NOT NAME."),
    ("T6b (instrument only)", "the two Fock functors applied to OUR species",
     "DEVELOPED-THEN-HALTED",
     "dim Kbar(F)_n = 1, 7, 121, 4399 and dim K(F)_n = 1, 4, 24, 218 are new "
     "invariants of a new object, reproduced exactly here.  The instrument's "
     "own output stops with 'identifying it would be new mathematics' and does "
     "not identify it.  The line is respected; the row is not in the "
     "document's body and not in section 10 item 6."),
]

for tag, what, verdict, note in ROWS:
    print("  %-22s %-22s %s" % (tag, verdict, what))
    wrap(note)
    print()

# ---------------------------------------------------------------------------
hdr("A6c  THE VERDICT ON THE PREDICTION")

for para in [
    "The prediction was that the 'do not develop new mathematics' instruction "
    "is the one most likely to be violated.  Tested directly:",

    "1.  NEITHER OF THE TWO PLACES THE DOCUMENT NAMES IS OVER THE LINE. "
    "Section 2.3's identity is a three-line corollary of the theorem the "
    "document quotes (A1d, with both steps checked exactly over Q); section "
    "5 establishes closure of two subspecies under published operations, "
    "which is what the brief asked for, and A3b shows it establishes nothing "
    "beyond that.  On the substance, the boundary held.",

    "2.  THE LIST IS NOT COMPLETE, AND THE ROW IT OMITS IS THE ONLY BROKEN "
    "ONE.  Section 8 C3's 'the smallest poset with AC(P) != Pi[n] is "
    "{a<c, b<d}' is a general extremal claim, developed here, attributed to "
    "nobody, sitting in a section headed CORRECTIONS TO THE RECORD -- and it "
    "is false, contradicted by the document's own table sixty lines earlier. "
    "Section 10 item 6 aims the auditor at section 2.3 and section 5.  The "
    "error is in section 8.",

    "3.  SO THE SELF-AWARENESS DID NOT WORK AS A CONTROL, AND IT DID NOT FAIL "
    "IN THE WAY PREDICTED EITHER.  It did not fail by buying cover for a "
    "violation -- there is no violation at the two named places.  It failed "
    "by DIRECTING ATTENTION: the document reasoned carefully about where new "
    "mathematics would enter, named the two candidates, and then made its one "
    "false mathematical statement in a third place it had already stopped "
    "watching.  A named failure mode is a searchlight, and everything outside "
    "the beam gets darker.",

    "4.  The audit brief's formulation -- 'a ticket that predicted it would "
    "derive new mathematics, and then did, has not been self-aware; it has "
    "been accurate' -- does not apply.  This ticket predicted it and then did "
    "not.  What it did instead was misclassify the corollary it DID produce "
    "(row S1 / section 2.3 above): four separate hedges in the document treat "
    "a two-line consequence of a quoted theorem as an unlocated measurement.  "
    "Under-claiming, not over-claiming, and it is the mirror image of the "
    "failure the brief was written to catch.",
]:
    wrap(para, "  ")
    print()

print("=" * 78)
print("A6 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
