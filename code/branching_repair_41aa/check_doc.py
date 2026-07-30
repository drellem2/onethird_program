"""check_doc -- does the repaired document actually say what this repair says?

mg-dea5 shipped a check of this shape and mg-aec7 had to fix an earlier one that
compared a string against a `print` statement instead of against the document.
So this file READS `docs/OneThird-Branching-Graphs-Where-This-Lives.md` off disk.

THE NEGATIVE HALF IS THE LOAD-BEARING HALF.  A repair that adds a correction
beside a false sentence and leaves the false sentence in force has not repaired
anything.  So each struck sentence is required to occur EXACTLY ONCE, and in a
block that also carries a strike marker -- `STRUCK`, `RE-SCOPED`, `CORRECTED`,
`the version this replaces`, and so on.  A struck sentence that has been quietly
deleted fails too: this repair quotes what it strikes where it stood.

Matching is done on WHITESPACE-FLATTENED blocks, with block-quote markers and
the narrow no-break spaces this repo's prose uses removed, so that a line wrap or
a re-flow does not turn a real check into a false pass or a false failure.

Exit 1 on any failure.
"""

import os
import re
import sys

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Branching-Graphs-Where-This-Lives.md")
YOUNG = os.path.join(HERE, "..", "branching_af28", "out_young.txt")

# Matched case-insensitively, so a prose "Re-scoped by mg-41aa" counts the same
# as a heading "RE-SCOPED".
MARKERS = ("struck", "re-scoped", "corrected (mg-41aa",
           "the version this replaces", "the reading this replaces",
           "this attack landed", "previously read", "previously continued",
           "previously added")

# must be present somewhere
PRESENT = [
    ("X1: the corrected class is named", "the **SKEW** cell posets `λ/μ`"),
    ("X1: corrected n=6 fraction", "**62/318**"),
    ("X1: corrected n=7 fraction", "**149/2 045**"),
    ("X1: corrected n=8 fraction", "**360/16 999**"),
    ("X1: af28's straight numbers are kept, not deleted",
     "6/318, 8/2 045, 12/16 999"),
    ("X1: the \"exactly\" is now tested",
     "The \"exactly\" is tested **in both directions**"),
    ("X1: the corrected fraction table is in section 0",
     "skew `λ/μ`, i.e. `J(P) = [μ, λ]`"),
    ("X2: the interval is exhibited",
     "interval `[(q), (q+p, q)]` of Young's lattice"),
    ("X3: section 3.6 is named by title",
     "*\"Tower of Algebras (not Preserving unities)\"*"),
    ("X3: the open question is named rather than answered",
     "THE OPEN QUESTION, NAMED RATHER THAN ANSWERED"),
    ("X3: row 3 is a hedge, not a no", "**This is a hedge, not a \"no\"**"),
    ("X4: the vacuity is stated", "no differential poset is finite"),
    ("X4: 28 of 33 is stated", "**28 of the 33**"),
    ("X5/X6/X7 are recorded as deliberately not repaired",
     "WHAT mg-41aa's REPAIR DELIBERATELY LEFT OPEN"),
    ("the repair banner is present", "Repaired 2026-07-30 by mg-41aa"),
    ("the repair instrument is cited", "code/branching_repair_41aa"),
    ("the repair document is cited", "OneThird-Branching-Graphs-Repair.md"),
]

# must occur EXACTLY ONCE, in a block that also carries a strike marker
QUOTED_ONLY = [
    ("X1: the false \"exactly\"", "are **exactly** the cell posets"),
    ("X2: the false grid sentence",
     "is **not** an interval of Young's lattice — `D_λ` has a minimum and "
     "`C_p ⊔ C_q` does not"),
    ("X4: the over-wide reading",
     "the **only** differential poset his construction can consume"),
    ("X3: the withdrawn bare negative",
     "**No tower.** §1, rows 1–2: Bergeron–Li's axiom (2) fails for the natural map"),
    ("X4: row 10's withdrawn reason",
     "the lattice it realises is the one Brown §4.3 provably cannot consume"),
    ("X1: the old bare-fraction sentence",
     "piece is the cell posets. That is a **vanishing** fraction"),
]

FAILS = []
N = [0]


def flatten(block):
    s = block.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    s = "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in s.split("\n"))
    return re.sub(r"\s+", " ", s).strip()


def norm(needle):
    return re.sub(r"\s+", " ",
                  needle.replace(" ", " ").replace(" ", " ")
                  .replace(" ", " ")).strip()


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("  %-3d %-62s %s" % (N[0], label, "PASS" if ok else "FAIL " + detail),
          file=OUT)


def main():
    raw = open(DOC, encoding="utf-8").read()
    blocks = [flatten(b) for b in re.split(r"\n\s*\n", raw)]
    whole = " ".join(blocks)

    print("=" * 78, file=OUT)
    print("CHECK_DOC  docs/OneThird-Branching-Graphs-Where-This-Lives.md", file=OUT)
    print("           %d bytes, %d lines, %d blocks"
          % (len(raw), raw.count("\n") + 1, len(blocks)), file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)

    print("  -- PRESENT: the repair landed ----------------------------------", file=OUT)
    for label, needle in PRESENT:
        check(label, norm(needle) in whole, "(not found)")
    print(file=OUT)

    print("  -- QUOTED ONLY: struck text survives, once, and marked as struck", file=OUT)
    for label, needle in QUOTED_ONLY:
        nd = norm(needle)
        hits = [b for b in blocks if nd in b]
        if not hits:
            check(label, False, "(GONE -- this repair quotes what it strikes)")
            continue
        marked = all(any(m in b.lower() for m in MARKERS) for b in hits)
        check(label, len(hits) == 1 and marked,
              "(blocks containing it: %d, all marked as struck: %s)"
              % (len(hits), marked))
    print(file=OUT)

    print("  -- THE INSTRUMENT'S OWN OUTPUT ---------------------------------", file=OUT)
    y = open(YOUNG, encoding="utf-8").read()
    check("out_young.txt no longer asserts the untested \"exactly\"",
          "an interval of Young's lattice are exactly the cell posets" not in y,
          "(still asserted)")
    check("out_young.txt names the corrected class",
          "SKEW cell posets lambda/mu" in y, "(not named)")
    check("out_young.txt prints the witness",
          "the 2-element ANTICHAIN is not any D_lambda: confirmed" in y,
          "(witness missing or refuted)")
    for n, straight, skew in ((6, 6, 62), (7, 8, 149), (8, 12, 360)):
        row = re.search(r"^\s*%d\s+(\d+)\s+(\d+)\*?\s+\d+\s" % n, y, re.M)
        got = (int(row.group(1)), int(row.group(2))) if row else None
        check("T2 row n=%d prints straight %d and skew %d" % (n, straight, skew),
              got == (straight, skew), "(got %r)" % (got,))
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("CHECK_DOC: %d checks, %d failed" % (N[0], len(FAILS)), file=OUT)
    for f in FAILS:
        print("  FAILED: %s" % f, file=OUT)
    print("=" * 78, file=OUT)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
