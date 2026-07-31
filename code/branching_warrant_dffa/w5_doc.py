"""W5 -- did the four narrowings land in the document, and did the wide
sentences leave?

This repair's whole content is rewriting claim statements, so the check that it
happened must read the DOCUMENT off disk, not a print statement.  Same shape as
`code/branching_repair_41aa/check_doc.py`, and for the same reason mg-aec7 gave
that file: a repair that adds a narrowed sentence beside the wide one and
leaves the wide one in force has not narrowed anything.

  PRESENT   the narrowed / widened text, one entry per finding.
  GONE      the exact wide phrasings mg-5800 quoted, which must no longer occur
            ANYWHERE in the document -- not in a block quote, not struck.  This
            differs from mg-41aa's discipline on purpose: mg-41aa struck FALSE
            sentences and quotes them where they stood, because the reader
            needs to see what was withdrawn.  mg-5800's F1-F4 are not false
            sentences, they are true sentences stated too wide, and a
            too-wide sentence quoted in place still reads as an assertion.
            So these are edited, not struck, and the deliverable carries the
            before/after instead.
  INTACT    mg-41aa's struck quotations, which this repair must not disturb.

Exit 1 on any failure.
"""

import os
import re
import sys

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Branching-Graphs-Where-This-Lives.md")
REPAIRDOC = os.path.join(HERE, "..", "..", "docs",
                         "OneThird-Warrant-Repair-mg-dffa.md")

PRESENT = [
    ("F1/B1: the cell now says lattice isomorphism",
     "**Meet and join preserved on every pair, not the order alone**"),
    ("F1/B1: and names af28's own test at its own width",
     "tests the **order** isomorphism only, on every pair in both directions"),
    ("F1/B5: the cell scopes 'not re-derived' to af28",
     "cited and not re-derived in `code/branching_af28/`"),
    ("F1/B5: and records the two derivations that exist",
     "by mg-6ad0 on 67 of the 87 classes"),
    ("F1/B5: attributing rather than claiming them",
     "**mg-dffa LOCATED both results in those committed outputs; it did not "
     "re-run them"),
    ("F2: section 2's note says same KIND",
     "a contact of the same **kind**"),
    ("F2: and says it is not the same contact",
     "**It is a contact of the same kind and it is not the same contact.**"),
    ("F2: with the measured divergence",
     "**17 distinct `P`** up to isomorphism, of which **5 are not skew cell"),
    ("F2: row 10 narrowed the same way",
     "an index-set contact of the **same kind** as the one this document "
     "headlines"),
    ("F4: premise (a) re-affirmed outside the strike",
     "RE-AFFIRMED OUTSIDE THE STRIKE — AND READ"),
    ("F4: with Brown's own sentence quoted live",
     "As an example of a distributive lattice, consider the"),
    ("F4: and the scope of the reading stated",
     "the rest of Brown (2000) remains unread by this arc and B8 remains a "
     "keyword census"),
    ("the mg-dffa banner is present", "Repaired again 2026-07-31 by mg-dffa"),
    ("the evidence directory is cited", "code/branching_warrant_dffa"),
    ("the account document is cited", "OneThird-Warrant-Repair-mg-dffa.md"),
]

GONE = [
    ("F1/B1: the old 'order isomorphism' scope line",
     "44 partitions, `n ≤ 7`, order isomorphism checked on every pair in both "
     "directions, 0 bad"),
    ("F1/B5: the unscoped 'not re-derived here'",
     "is Brown's theorem, cited, not re-derived here"),
    ("F2: 'the index-set contact does extend'",
     "the index-set contact **does** extend"),
    ("F2: row 10's 'same index-set contact'",
     "the **same index-set contact** this document headlines"),
]

# mg-41aa's struck quotations.  Still exactly once, still marked.
INTACT = [
    ("X1's false \"exactly\"", "are **exactly** the cell posets"),
    ("X2's false grid sentence",
     "is **not** an interval of Young's lattice — `D_λ` has a minimum and "
     "`C_p ⊔ C_q` does not"),
    ("X4's over-wide reading",
     "the **only** differential poset his construction can consume"),
    ("X3's withdrawn bare negative",
     "**No tower.** §1, rows 1–2: Bergeron–Li's axiom (2) fails for the "
     "natural map"),
    ("X4's withdrawn row-10 reason",
     "the lattice it realises is the one Brown §4.3 provably cannot consume"),
    ("X1's old bare-fraction sentence",
     "piece is the cell posets. That is a **vanishing** fraction"),
]

MARKERS = ("struck", "re-scoped", "corrected (mg-41aa",
           "the version this replaces", "the reading this replaces",
           "previously read", "previously continued", "previously added")

FAILS = []
N = [0]


def flatten(block):
    s = block.replace(" ", " ").replace(" ", " ").replace("\xa0", " ")
    s = "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in s.split("\n"))
    return re.sub(r"\s+", " ", s).strip()


def norm(needle):
    return re.sub(r"\s+", " ", needle.replace(" ", " ")
                  .replace(" ", " ").replace("\xa0", " ")).strip()


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("  %-3d %-60s %s" % (N[0], label, "PASS" if ok else "FAIL " + detail),
          file=OUT)


def main():
    raw = open(DOC, encoding="utf-8").read()
    blocks = [flatten(b) for b in re.split(r"\n\s*\n", raw)]
    whole = " ".join(blocks)

    print("=" * 78, file=OUT)
    print("W5  docs/OneThird-Branching-Graphs-Where-This-Lives.md", file=OUT)
    print("    %d bytes, %d lines, %d blocks"
          % (len(raw), raw.count("\n") + 1, len(blocks)), file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)

    print("  -- PRESENT: the four narrowings landed ------------------------",
          file=OUT)
    for label, needle in PRESENT:
        check(label, norm(needle) in whole, "(not found)")
    print(file=OUT)

    print("  -- GONE: the wide phrasings are not in force anywhere ---------",
          file=OUT)
    for label, needle in GONE:
        hits = whole.count(norm(needle))
        check(label, hits == 0, "(%d occurrences remain)" % hits)
    print(file=OUT)

    print("  -- INTACT: mg-41aa's strikes, undisturbed ---------------------",
          file=OUT)
    for label, needle in INTACT:
        nd = norm(needle)
        hits = [b for b in blocks if nd in b]
        marked = bool(hits) and all(
            any(m in b.lower() for m in MARKERS) for b in hits)
        check(label, len(hits) == 1 and marked,
              "(blocks: %d, all marked: %s)" % (len(hits), marked))
    print(file=OUT)

    print("  -- THE ACCOUNT DOCUMENT ---------------------------------------",
          file=OUT)
    try:
        acct = open(REPAIRDOC, encoding="utf-8").read()
    except OSError:
        acct = ""
    check("docs/OneThird-Warrant-Repair-mg-dffa.md exists", bool(acct),
          "(missing)")
    a = flatten(acct)
    # The requirement mg-5800 sets is per FINDING, not per occurrence: each of
    # F1..F4 must carry the sentence as written, the evidence that exists, and
    # the sentence as narrowed.  F1 and F2 each cover two sites, so the raw
    # counts are 6 / 5 / 6 -- checking a count would be checking the shape this
    # document happens to have rather than the thing that was asked for.
    heads = re.findall(r"^## (\d+)\. (F\d)\b", acct, re.M)
    check("it gives F1..F4 a section each",
          [h[1] for h in heads] == ["F1", "F2", "F3", "F4"],
          "(%r)" % ([h[1] for h in heads],))
    bodies = re.split(r"^## \d+\. F\d\b", acct, flags=re.M)[1:]
    for f, body in zip(["F1", "F2", "F3", "F4"], bodies):
        for part in ("AS WRITTEN", "THE EVIDENCE THAT EXISTS", "AS NARROWED"):
            check("%s carries '%s'" % (f, part), part in body, "(absent)")
    check("it states what it located rather than measured",
          "LOCATED, NOT MEASURED" in a, "(absent)")
    check("it states what it could NOT establish",
          "WHAT THIS REPAIR DID NOT ESTABLISH" in acct, "(absent)")
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("W5: %d checks, %d failed" % (N[0], len(FAILS)), file=OUT)
    for f in FAILS:
        print("  FAILED: %s" % f, file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY w5_doc: checks %d, failures %d" % (N[0], len(FAILS)),
          file=OUT)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
