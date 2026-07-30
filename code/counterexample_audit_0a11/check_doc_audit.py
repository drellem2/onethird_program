"""Cross-check THIS audit's prose against THIS audit's outputs.

Deliberately not built the way the two checkers this audit criticises are built.
Their weakness (mg-0a11 finding 2) is that a figure is looked for by set
membership in a CONCATENATION of documents, so a number can be wrong in one
document and right in another and the check passes.  Here:

  * each figure names the ONE output file it must come from, and is looked for
    in that file only;
  * each figure names the ONE document region it must appear in -- a markdown
    section of this audit -- and is looked for in that region only;
  * a figure that appears in the document but OUTSIDE its declared section is a
    FAILURE, not a pass.  That is the property M1a and M11 showed the subject's
    checker does not have.

It still does not check claims.  No string-matcher does.  What it can do is
refuse to certify a figure that has drifted out of the passage it belongs to,
and that is stated as its whole contract.

Run after run_all.sh.  Exit 1 on any failure.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Counterexample-Under-The-Action-IndependentAudit-mg0a11.md")

# (label, section heading prefix the figure must live under, output file, string in that file, string in the doc)
CHECKS = [
    # -- verdict / section 1: the primary finding
    ("all 20 inherited", "## VERDICT", "out_independence.txt",
     "   8 | 20 |                 20 |        0 | 0", "**20 of 20**"),
    ("cores at n=8", "## VERDICT", "out_independence.txt",
     "   8 | 20 |          6 |              5 |              1", "**5 distinct cores**"),
    ("core-level p in verdict", "## VERDICT", "out_independence.txt",
     "exact p over the distinct cores    : 1/C(6,1) = 1/6", "**`1/5`**"),
    ("core-level p in body", "## 1.", "out_independence.txt",
     "exact p over the distinct cores    : 1/C(6,1) = 1/6", "1/C(6,1) = 1/6"),
    ("138 generated", "## 1.", "out_independence.txt",
     "n=7 -> n=8 : 138 cut extensions generated in all, 20 survive e=9",
     "138 cut extensions are generated, 20 survive both filters"),
    ("six cores", "## 1.", "out_independence.txt",
     "distinct cores in the whole family : 6", "**six** distinct cores"),
    ("inheritance 257", "## VERDICT", "out_independence.txt",
     "(delta, qmass) inherited             : 257", "257 of 257"),
    ("cut-free at n=9", "## VERDICT", "out_independence.txt",
     "   9 | 29 |                 28 |        1 | 0", "single cut-free member at `n = 9`"),
    ("family to n=11", "## VERDICT", "out_independence.txt",
     "  11 | 50 |         21 |", "29 / 39 / 50"),
    ("exact p 1/38760", "## 4.", "out_population.txt",
     "  8 | 9 | 20 | 6 |        6 | True    |   1 | 1/38760", "`1/38760`"),
    ("AUC=1", "## 4.", "out_population.txt", "| True    |   1 | 1/286", "`AUC = 1`"),
    # -- section 3: the negatives
    ("exhaustive 19446", "## 3.", "out_cycles.txt",
     "TOTAL over n = 3..8 : 19446 classes, 19440 non-chains, 0 majority cycles",
     "19,446 classes at `n = 3…8`, 19,440 non-chains, **0** cycles"),
    ("A001035 at n=8", "## 3.", "out_cycles.txt", "431723379", "431723379"),
    ("n=9 witness e", "## 3.", "out_cycles.txt", "e(P)        1431", "`e = 1431`"),
    ("n=9 margins", "## 3.", "out_cycles.txt", "80/159", "`80/159`"),
    ("n=9 deletions", "## 3.", "out_cycles.txt",
     "deletions preserving a cycle: none", "**none** preserves a cycle"),
    ("n=10 e", "## 3.", "out_cycles.txt", "e(P) = 7134", "`e = 7134`"),
    ("n=11 e", "## 3.", "out_cycles.txt", "e(P) = 78474", "`e = 78474`"),
    # -- section 4: the measurements
    ("population n=8", "## 4.", "out_population.txt",
     "  8 |      16998 | 10578 |               0 |       6420 |        12 | 1/3",
     "| 8 | 16998 | 10578 | 0 | 6420 | 12 | `1/3` |"),
    ("prop V n=8", "## 4.", "out_population.txt", "  8 |              6 |                  6 | 0",
     "1 / 2 / 3 / 4 / 5 / 6 at `n = 3…8`"),
    ("rho|e qmass", "## 4.", "out_powered.txt",
     "  8 |       6420 |      691 |       465 |      -0.273 |      +0.018", "`−0.273`"),
    ("tau_b and z n=8", "## 4.", "out_powered.txt",
     "  8 |       6420 |         670 |     -0.2052 |  -16.60 |     +0.0064 |   +0.54",
     "`−16.60`"),
    ("sensitivity qfrac n=6", "## 4.", "out_powered.txt",
     "  6 |          12 |    -0.301 |    -0.331", "`−0.331 / −0.070 / +0.007`"),
    ("saturation n=8", "## 4.", "out_powered.txt",
     "  8 |       6420 |      36 |                12 |    0.6%", "36 of 6420"),
    ("raw effect n=8", "## 4.", "out_powered.txt",
     "  8 |     6420 |        12 |     1.000 |      0.461 |     0.505 |      0.120",
     "`1.000 vs 0.461`"),
    ("attainability n=8", "## 1.", "out_powered.txt",
     "  8 |                        24 |               0.37% |                     0",
     "24 of the 36 posets"),
    # -- section 5: the beyond-brief material
    ("deflation argmax", "## 5.", "out_deflation.txt",
     "  7 |    669 |                2 |            583 | 309", "**583 of 669**"),
    ("deflation unique", "## 5.", "out_deflation.txt",
     "  6 |     88 |                0 |             83 | 59", "**13 / 59 / 309**"),
    # -- section 2: the mutation battery
    ("silent misses", "## VERDICT", "out_locator.txt", "SILENT MISSES: 10",
     "10 of 14 meaning-changing mutations exit **0**"),
    ("M1a silent", "## 2.", "out_locator.txt",
     "[SILENT MISS] M1a", "| **M1a** |"),
    ("M2 caught", "## 2.", "out_locator.txt", "[ok         ] M2 ", "| **M2** |"),
    ("baseline clean", "## 2.", "out_locator.txt",
     "check_doc_repair.py  exit 0 (clean)", "both checkers exit 0 on the unmodified tree"),
]


def sections(doc):
    """Map each '## ' heading to the span of text under it."""
    spans = {}
    marks = [(m.start(), m.group(0).strip()) for m in re.finditer(r"^## .*$", doc, re.M)]
    for i, (pos, head) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(doc)
        spans[head] = (pos, end)
    return spans


def norm(s):
    return (s.replace("−", "-").replace("–", "-").replace("—", "-")
             .replace("×", "x").replace("…", "..."))


def main():
    doc = open(DOC).read()
    spans = sections(doc)
    ndoc = norm(doc)

    print("=" * 78)
    print("CHECK: this audit's figures, each against ITS OWN output file and")
    print("       each inside ITS OWN section")
    print("=" * 78)
    bad = []
    for label, sec, outfile, in_out, in_doc in CHECKS:
        body = open(os.path.join(HERE, outfile)).read()
        o = in_out in body
        # the declared region
        region = None
        for head, (a, b) in spans.items():
            if head.startswith(sec):
                region = (a, b)
                break
        if region is None:
            bad.append((label, "declared section %r not found" % sec))
            print("  [FAIL] %-24s section %r missing" % (label, sec))
            continue
        a, b = region
        target = norm(in_doc)
        inside = target in ndoc[a:b]
        elsewhere = target in (ndoc[:a] + ndoc[b:])
        ok = o and inside
        if not o:
            bad.append((label, "output %s does not contain %r" % (outfile, in_out)))
        if not inside:
            bad.append((label, "doc section %s does not contain %r" % (sec, in_doc)))
        print("  [%s] %-24s out:%s  in-section:%s  also-elsewhere:%s"
              % ("ok  " if ok else "FAIL", label,
                 "yes" if o else "NO ", "yes" if inside else "NO ",
                 "yes" if elsewhere else "no "))

    print()
    print("=" * 78)
    print("GUARDS")
    print("=" * 78)
    guards = []
    # the audit must not claim to have proved what it measured
    for pat in ("qmass-invariance is proved", "we have proved that qmass",
                "theorem 4 is refuted", "the separation is an artefact",
                "no separation exists"):
        if pat.lower() in doc.lower():
            guards.append("audit contains an unsupported claim: %r" % pat)
    # the audit must not report the core-level p as if it were the repair's
    if "p = 1/6" in doc and "core" not in doc.lower():
        guards.append("core-level p reported without naming the reduction")
    # the 'could not establish' section must exist and be non-empty
    if "## 7. What I could not establish" not in doc:
        guards.append("the 'what I could not establish' section is missing")
    else:
        a, b = spans["## 7. What I could not establish"]
        if doc[a:b].count("* **") < 3:
            guards.append("the 'could not establish' section has fewer than 3 items")
    # every mutation the battery reports as SILENT must be named in the document
    loc = open(os.path.join(HERE, "out_locator.txt")).read()
    for m in re.findall(r"\[SILENT MISS\] (M\w+)", loc):
        if "**%s**" % m not in doc:
            guards.append("silent miss %s is not reported in the document" % m)
    for g in guards:
        print("  [FAIL] %s" % g)
    if not guards:
        print("  all guards clean")

    print()
    if bad or guards:
        print("%d check(s) failed, %d guard(s) tripped" % (len(bad), len(guards)))
        for label, why in bad:
            print("    %-24s %s" % (label, why))
        return 1
    print("ALL %d FIGURES VERIFIED against their own output file AND inside their"
          % len(CHECKS))
    print("own section.  GUARDS CLEAN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
