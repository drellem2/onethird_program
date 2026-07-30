"""Cross-check every number quoted in docs/OneThird-Counterexample-Under-The-Action.md
against the committed probe/selftest outputs.

The point is narrow and worth stating: this does NOT re-derive the mathematics.  It
checks that the prose quotes the instrument correctly -- the failure mode this arc has
hit six generations running is a true computation described by a false sentence.
Run after run_all.sh.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Counterexample-Under-The-Action.md")
PROBE = os.path.join(HERE, "probe_output.txt")
SELF = os.path.join(HERE, "selftest_output.txt")

# (label, string that must appear in the doc, string that must appear in the output)
# Each pair asserts: the doc claims X, and the instrument printed X.
CHECKS = [
    # -- section 2, the transitivity theorem and the general-poset sweep
    ("no cycle in exhaustive range", "0 of 2447",
     "0 cyclic majority digraphs out of 2447 posets"),
    ("witness n=11 e(P)", "78474", "n = 11, e(P) = 78474"),
    ("witness cycle", "5 → 9 → 6 → 5", "majority 3-CYCLE  5 -> 9 -> 6 -> 5"),
    ("witness edge 1", "597/1189", "p(5,9) = 597/1189"),
    ("witness edge 2", "599/1189", "p(9,6) = 599/1189"),
    ("witness edge 3", "1784/3567", "p(6,5) = 1784/3567"),
    ("random search budget", "4200 random posets", "4200 random posets"),
    # -- section 3, the concentration ratio
    ("R table n=5", "`4/5`", "5          62          1        4/5           11          17.7%"),
    ("R table n=6", "`3/4`", "6         317          1        3/4          124          39.1%"),
    ("R table n=7", "`24/35`", "7        2044          1      24/35         1232          60.3%"),
    ("R<1 count n=7", "1232", "1232"),
    ("R<1 pct n=7", "60.3%", "60.3%"),
    ("family C6+C6", "`128/231`", "C_6 + C_6                12      924        3/2    128/231"),
    ("family C5+C5", "`64/105`", "C_5 + C_5                10      252        3/2     64/105"),
    ("family C4+C4", "`24/35`", "C_4 + C_4                 8       70        3/2      24/35"),
    ("family C3+C3", "`4/5`", "C_3 + C_3                 6       20        3/2        4/5"),
    # -- section 4, the quotient side
    ("qmass z n=7", "+2.64", "z=+2.64"),
    ("qfrac z n=7", "+4.49", "z=+4.49"),
    ("saturation n=7", "20 of 671", "7           671             20           3.0%"),
    ("tie n=7", "rank 1 of 5 tied with 4", "rank 1 of 5   TIED WITH 4"),
    ("tie n=6", "rank 1 of 4 tied with 3", "rank 1 of 4   TIED WITH 3"),
    ("tie n=5", "rank 1 of 3 tied with 2", "rank 1 of 3   TIED WITH 2"),
    # -- section 5.1, convexity
    ("convex blocks count", "3,246,401", "0 bad of 3246401 (level, block) pairs"),
    ("convex subsets count", "281,977", "0 bad of 281977 (poset, subset) pairs"),
    # -- section 5.2, lambda_2 and delta_walk
    ("lambda2 = max s", "0 bad of 2442", "0 bad of 2442 non-chain posets"),
    ("all-chain levels", "65,481", "0 bad of 65481 all-chain levels other than the finest"),
    ("per-pair rho n=6", "0.9945", "6        2195     0.9945"),
    ("per-pair mean err n=6", "0.00939", "0.00939"),
    ("max err n=6", "`5/114`", "5/114"),
    ("max err n=5", "`5/132`", "5/132"),
    ("max err n=4", "`1/40`", "1/40"),
    ("rho all non-chains n=6", "0.9855", "6         317       0.9855"),
    ("rho controlled n=6", "0.8919", "0.8919"),
    ("not one-sided pairs n=6", "759 of 2195", "6              2195              759               37"),
    ("not one-sided posets n=6", "37 of 317", "759               37"),
    ("false positive poset", "0<2 0<3 1<2 2<4 3<4 3<5", "d_walk=12/37    delta=5/14"),
    # -- section 5.3, primitivity
    ("2-block partitions", "139,765", "0 bad of 139765 2-block partitions"),
    ("primitive equivalence", "0 bad of 2447 posets",
     "PRIMITIVE <==> all-positive excess: 0 bad of 2447 posets"),
    # -- section 5.5, no free lunch
    ("no-free-lunch cases", "0 bad of 57", "0 bad of 57 (poset, t) cases at n<=4"),
    ("uniform-move not uniformising", "717 of 2195",
     "717 of 2195 pairs have min(pi,1-pi) = min(p,1-p) exactly"),
    ("worst gap", "`5/114`", "worst gap 5/114"),
    # -- section 6, the ladder (primitive non-chains at n=6)
    ("ladder N", "`N = 184`", "primitive non-chains, N=184"),
    ("I0 fibers", "| `I0` | 54 |", "I0     e(P) alone"),
    ("lambda2 rho", "−0.139", "lambda_2             -0.139"),
    ("lambda2 p", "0.0565", "0.0565"),
    ("filter selectivity", "**0.5%**", "delta_walk                12/37         0.5%"),
    # -- section 6, the wash-out trend and the no-witness fact
    ("trend n=7 N", "| **1351** |", "7    primitive non-chains     1351"),
    ("trend n=7 singleton", "**7.3%**", "5.1%       7.3%       7.3%"),
    ("trend n=7 fibers", "**626**", "7             1        626            0"),
    ("no witnesses n=7", "not one contains two posets with different `\u03b4`",
     "NONE: at n=7 every I4-fiber has constant delta."),
    ("lambda2 n=7", "`\u03c1 = \u22120.020`", "lambda_2             -0.020    0.4268"),
    # -- section 5.4, the frozen floor
    ("extremal e=3 n=7", "5 of 8", "n=7: 5 of 8 extremal posets have e(P) = 3"),
    ("extremal e=3 n=6", "4 of 5", "n=6: 4 of 5 extremal posets have e(P) = 3"),
]

# Entries whose DOC STRING WAS STRUCK from the document by the mg-dea5 repair.
#
# The struck sentences are still in the file -- quoted verbatim inside a
# "> **STRUCK" epitaph, so the retraction is legible where the claim stood -- and
# the arithmetic behind them is still correct, which is why they were listed here
# in the first place.  But a checker that finds a string and cannot tell live prose
# from an epitaph certifies a retracted claim, and that is exactly the hole mg-a7b4
# named about this file (audit finding 1: "check_doc.py cannot catch this: its entry
# for these rows checks that the string 'rank 1 of 5 tied with 4' appears in both the
# prose and the output.  It does, and the arithmetic behind it is right.  The defect
# is entirely in the quantifier.")
#
# So for these entries the doc-side assertion is INVERTED: the string must appear,
# and EVERY occurrence of it must lie inside a struck block.  If a future edit puts
# one of them back into live prose, this file fails.
STRUCK = {
    "random search budget",     # "4200 random posets" -- false at n = 9 and n = 10
    "tie n=5", "tie n=6", "tie n=7",   # the e(P)-controlled "exact tie" universal
}


# Sentences the mg-dea5 repair INSTALLED in this document, and the mg-a893 landing
# of mg-0a11's audit added to.  They must be PRESENT and OUTSIDE every epitaph.
#
# mg-0a11's M13 is why this list exists.  The whole point of the mg-dea5 repair is
# the quantifier in headline 3 -- "picks out EXACTLY the delta-extremal posets",
# replacing an exact-tie universal measured on a vacuous control.  That sentence
# could be reverted to "picks out SOME OF the delta-extremal posets" and this file,
# whose entire subject is this document, exited 0: nothing in CHECKS or STRUCK
# mentions it.  A checker that does not require the repair it certifies to still be
# in the document certifies the document it was pointed at, not the repair.
LIVE = [
    ("headline 3 quantifier",
     "`qmass = 1` picks out **exactly** the `\u03b4`-extremal\n   posets"),
    ("section 4 perfect, both inclusions",
     "the `qmass = 1` members are **exactly** the extremal ones"),
    ("section 4 vacuity definition",
     "Call an `e`-group **vacuous** if every member of it"),
    ("section 4 dependence correction",
     "**the honest exact `p` is `1/5`**"),
    ("section 4 core column",
     "| 8 | **9** | 20 | 6 | 6 | **perfect** | `1/38760` | `1` | 5 | **`1/5`** |"),
    ("section 2 exhaustive cycle result",
     "The smallest `n` carrying a majority cycle is exactly 9."),
]


def struck_regions(doc):
    """Spans of the doc occupied by a '> **STRUCK' blockquote."""
    spans = []
    lines = doc.split("\n")
    pos = 0
    start = None
    for line in lines:
        stripped = line.lstrip()
        if start is None and stripped.startswith("> **STRUCK"):
            start = pos
        elif start is not None and not stripped.startswith(">"):
            spans.append((start, pos))
            start = None
        pos += len(line) + 1
    if start is not None:
        spans.append((start, pos))
    return spans


def only_inside(doc, needle, spans):
    """True iff `needle` occurs at least once and every occurrence is in a span."""
    i = doc.find(needle)
    if i < 0:
        return False
    while i >= 0:
        if not any(a <= i < b for a, b in spans):
            return False
        i = doc.find(needle, i + 1)
    return True


def main():
    doc = open(DOC).read()
    out = open(PROBE).read() + open(SELF).read()
    bad = []
    spans = struck_regions(doc)
    for label, in_doc, in_out in CHECKS:
        struck = label in STRUCK
        d = only_inside(doc, in_doc, spans) if struck else (in_doc in doc)
        o = in_out in out
        if not (d and o):
            bad.append((label, d, o, in_doc, in_out))
        print("  [%s] %-34s doc:%s out:%s%s"
              % ("ok  " if (d and o) else "FAIL", label,
                 "yes" if d else "NO ", "yes" if o else "NO ",
                 "   STRUCK: quoted only inside its epitaph" if struck else ""))
    print()
    print("  (%d struck entries: the instrument still prints the figure, and the doc"
          % len(STRUCK))
    print("   must carry the sentence ONLY inside a '> **STRUCK' block.  See STRUCK.)")
    print()
    print("  LIVE -- the repaired sentences must still BE the document (mg-a893):")
    for label, sentence in LIVE:
        hits, i = [], doc.find(sentence)
        while i >= 0:
            hits.append(i)
            i = doc.find(sentence, i + 1)
        live = [i for i in hits if not any(a <= i < b for a, b in spans)]
        ok = bool(live)
        if not ok:
            bad.append(("live: " + label, False, True, sentence, ""))
        print("  [%s] %-34s %s"
              % ("ok  " if ok else "FAIL", label,
                 "live" if ok else "MISSING, STRUCK OR REWORDED"))
    print()
    # global guards
    guards = []
    if "FAIL" in open(PROBE).read():
        guards.append("probe_output.txt contains a FAILing structural check")
    if "ALL CONTROLS PASS" not in open(SELF).read():
        guards.append("selftest_output.txt does not end in ALL CONTROLS PASS")
    # the conditionality discipline: no unconditional claim about a counterexample
    for pat in (r"the counterexample is", r"counterexamples are frozen and have",
                r"we have shown that no counterexample"):
        if re.search(pat, doc, re.I):
            guards.append("doc contains an unconditional counterexample claim: %s" % pat)
    for g in guards:
        print("  [FAIL] GUARD: %s" % g)
    if bad or guards:
        print("\n%d quoted figure(s) unverified, %d guard(s) tripped" % (len(bad), len(guards)))
        for label, d, o, a, b in bad:
            if not d:
                print("    doc is missing: %r" % a)
            if not o:
                print("    output is missing: %r" % b)
        return 1
    print("ALL %d QUOTED FIGURES VERIFIED against the committed outputs; guards clean."
          % len(CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
