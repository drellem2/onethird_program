#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument -- THE MISSING DIRECTION OF THE SELF-TEST.

mg-3b51's A3: selftest.py was described as failing loudly "if the document and
the instruments ever drift apart", but it never read the document.  Its
expected values are constants TRANSCRIBED from the document, so it fails if the
INSTRUMENTS drift from those constants -- and an edit to a number in the
markdown passed silently.  The guarantee was one-directional.

This module supplies the other direction.  It READS
docs/OneThird-Landscape-Where-This-Lives.md and extracts the figures the
document carries, from the sentences and table rows that carry them, by
anchored regular expressions.  selftest.py then asserts each extracted figure
against the same constant it asserts the instruments against, so the loop
closes:

    instruments  ->  constants  ->  document

Two ways a figure fails, and both are the point:
  * the number in the document changed          -> value mismatch
  * the sentence carrying it was rewritten away -> NOT FOUND (a hard failure,
    never a skip; a regex that silently matches nothing is the one-directional
    guarantee all over again)

COVERAGE BOUNDARY, stated because it is not total.  Only the figures in FIGURES
below are guarded -- the headline numbers of section 0, sections 3.2/3.3 and
every row of section 8's repair table.  Prose, attributions, status words, the
claim ledger's wording and any number not listed here are NOT covered.  A
"stated coverage boundary" is what this repo settled on for the same problem in
code/state_landing_control_2da3/COVERAGE.md; the goal is bounded and stated,
not total.

NUMBER FORMAT.  The document writes thousands with an ASCII space ("936 261")
and never with a comma, so within a captured group a comma separates LIST
elements and a space does not.  normalise() applies exactly that rule.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DOCUMENT = os.path.normpath(
    os.path.join(HERE, "..", "..", "docs",
                 "OneThird-Landscape-Where-This-Lives.md"))

# (name, where, pattern).  Every capturing group is a figure; groups are
# returned flattened, in order, as a tuple of ints (or tuples of ints for a
# comma-separated list).
FIGURES = [
    ("s0 E1 populations", "section 0 item 1",
     r"0 bad of \*\*([\d ]+) classes[^|]{0,40}?([\d ]+) pairs\*\*,"
     r" maximal-chains-to-linear-extensions 0 bad of ([\d ]+) "),

    ("s0 Brown levels", "section 0 item 2",
     r"`n ≤ 6`, ([\d ]+) levels: 0 disagreements\*\*"),

    ("s2 two-sided comparison", "section 2",
     r"\*\*0 disagreements at all ([\d ]+) levels to `n ≤ 6`\*\*\s+"
     r"\(([\d, ]+) by `n`\)"),

    ("s2 levels named zero", "section 2",
     r"\*\*([\d ]+) of ([\d ]+)\*\* levels carrying zero at `n = 6`"
     r" \(([\d ]+) of ([\d ]+) at `n = 5`\)"),

    ("s3.2 n=6 row", "section 3.2 table",
     r"\n\| 6 \| ([\d ]+) \| \*\*([\d ]+)\*\* \| \*\*0 bad of ([\d ]+)\*\*"),

    ("s3.3 n<=5 total row", "section 3.3 table",
     r"\*\*`n ≤ 5` total\*\*[^|]*\| \*\*([\d ]+)\*\* \| \*\*([\d ]+)\*\*"
     r" \| \*\*0 bad of ([\d ]+)\*\* \| \*\*0 bad of ([\d ]+) pairs\*\*"),

    ("s3.3 move counts", "section 3.3 prose",
     r"The move counts `([\d, ]+)` are the note's own"),

    ("R1a geometric vs the two rules", "section 8 row R1",
     r"equals the repaired rule \*\*0 bad of ([\d ]+)\*\* at `n = 6` and fails"
     r" the original rule on \*\*([\d ]+) of ([\d ]+)\*\* \(`n=4`\),"
     r" \*\*([\d ]+) of ([\d ]+)\*\* \(`n=5`\),"
     r" \*\*([\d ]+) of ([\d ]+)\*\* \(`n=6`\)"),

    ("R1b flats and spurious", "section 8 row R1",
     r"over \*\*all ([\d ]+) flats\*\* at `n = 6`.{0,120}?"
     r"\*\*([\d ]+) spurious flats\*\*"),

    ("R1c the witness", "section 8 row R1",
     r"witness `P = \{a<c, b<d\}`, `\\\|L\(P\)\\\| = ([\d ]+)`,"
     r" original sums to \*\*([\d ]+)\*\*"),

    ("R1d the identity", "section 8 row R1",
     r"exhibited as a set identity on \*\*([\d ]+) of ([\d ]+)\*\* classes at"
     r" `2 ≤ n ≤ 6`, and the sums agree there too"
     r" \(\*\*0 bad of ([\d ]+)\*\* at `n = 6` under each\)"),

    ("R2 E8 columns", "section 8 row R2",
     r"identity in the image: \*\*all ([\d ]+)/([\d ]+)\*\* at `n = 5`\."
     r" Injective: \*\*0 of ([\d ]+)\*\*"),

    ("R2 band vs F(P) at the antichain", "section 8 row R2",
     r"\*\*([\d ]+) vs ([\d ]+)\*\* and \*\*([\d ]+) vs ([\d ]+)\*\* at"
     r" `n = 2, 3` \(A000522 vs A000670\)"),

    ("R3 two-sided comparison", "section 8 row R3",
     r"\*\*0 disagreeing levels of ([\d ]+)\*\* to `n ≤ 6`"
     r" \(([\d, ]+) by `n`\), \*\*0 posets bad of ([\d ]+)\*\*"),

    ("R3 levels named zero", "section 8 row R3",
     r"\*\*([\d ]+) of ([\d ]+)\*\* levels at `n = 6`"
     r" \(\*\*([\d ]+) of ([\d ]+)\*\* at `n = 5`\)"),

    ("R4 the corrected populations", "section 8 row R4",
     r"\*\*([\d ]+)\*\* \(`2 ≤ n ≤ 6`, `identify_lattice\.py`'s own"
     r" range\); \*\*([\d ]+)\*\* \(`3 ≤ n ≤ 6`"),

    ("R4 rebuilt populations", "section 8 row R4",
     r"classes `([\d, ]+)`; moves `([\d, ]+)` \(total \*\*([\d ]+)\*\*\);"
     r" levels `([\d, ]+)`; product pairs `([\d, ]+)`"
     r" \(total \*\*([\d ]+)\*\*\)"),
]


def normalise(group):
    """A comma separates list elements; a space is a thousands separator."""
    if "," in group:
        return tuple(int(part.replace(" ", "")) for part in group.split(","))
    return int(group.replace(" ", ""))


def read(path=DOCUMENT):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def extract(text=None):
    """name -> tuple of figures, or None if the anchoring text is gone."""
    if text is None:
        text = read()
    out = {}
    for name, _where, pattern in FIGURES:
        m = re.search(pattern, text, re.DOTALL)
        out[name] = None if m is None else tuple(
            normalise(g) for g in m.groups())
    return out


def where(name):
    for n, w, _p in FIGURES:
        if n == name:
            return w
    return "?"


if __name__ == "__main__":
    print("document: %s" % DOCUMENT)
    got = extract()
    for name, w, _p in FIGURES:
        print("  %-42s %-24s %s"
              % (name, w, "NOT FOUND" if got[name] is None else got[name]))
