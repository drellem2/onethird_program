"""Cross-check the repair's prose against the repair's own outputs.

Narrow, and worth stating narrowly: this does NOT re-derive the mathematics.  It
checks that two documents quote this instrument correctly --

    docs/OneThird-Counterexample-Under-The-Action-Repair.md          (the repair)
    docs/OneThird-Counterexample-Under-The-Action.md                 (the repaired passages)

-- and, separately, that the sentences the repair STRUCK from the target document
appear there ONLY inside a "> **STRUCK" epitaph.  That second half is the point.
mg-a7b4's finding 1 was that the target's own check_doc.py verified the string
"rank 1 of 5 tied with 4" in the prose against the same string in the output, and
passed, while the sentence containing it was false.  A checker that cannot tell
live prose from a retraction certifies retractions.  So: struck strings must be
present (the retraction has to be legible where the claim stood) and every
occurrence must be inside an epitaph.

Run after run_all.sh.  Exit 1 on any failure.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "..", "docs")
TARGET = os.path.join(DOCS, "OneThird-Counterexample-Under-The-Action.md")
REPAIR = os.path.join(DOCS, "OneThird-Counterexample-Under-The-Action-Repair.md")
OUTS = ("out_section4.txt", "out_theorem4.txt", "out_cycles.txt", "out_controls.txt")

# (label, string that must appear in BOTH docs' union, string the instrument printed)
CHECKS = [
    # -- the primary measurement
    ("n=8 exact p", "1/38760", "1/38760"),
    ("n=7 exact p", "1/286", "1/286"),
    ("n=6 exact p", "1/7", "1/7"),
    ("n=8 group", "6 of 20", "8        9    20     6       6      YES"),
    ("n=7 group", "3 of 13", "7        9    13     3       3      YES"),
    ("n=6 group", "1 of 7", "6        9     7     1       1      YES"),
    ("n=8 population", "6420", "8         16998        10578            0           6420           12"),
    ("n=8 extremal count", "12 extremal posets at `n = 8`", "6420           12"),
    ("bonferroni 3", "7.7 × 10⁻⁵", "7.74e-05"),
    ("bonferroni 7", "1.8 × 10⁻⁴", "0.000181"),
    ("joint", "1.29 × 10⁻⁸", "1.29e-08"),
    # -- vacuity
    ("vacuity row", "counterexamples to V", "counterexamples to V"),
    ("e=3 at n=8", "| 1 | 2 | 3 | 4 | 5 | 6 |", "8                   6                    6                    0"),
    # -- the powered test
    ("qmass rho|e n=8", "-0.273", "-0.273"),
    ("qmass rho|e n=7", "-0.261", "-0.261"),
    ("qmass rho|e n=6", "-0.287", "-0.287"),
    ("qmass tau n=8", "-0.205", "-0.205"),
    ("qmass z n=8", "-16.60", "-16.60"),
    ("qfrac rho|e n=8", "+0.018", "0.018"),
    ("qfrac rho|e n=7", "+0.011", "0.011"),
    ("qfrac rho|e n=6", "-0.009", "-0.009"),
    ("perm p n=6", "0.0800", "0.0800"),
    # -- the raw table extended
    ("raw qmass z n=8", "+3.72", "z=+3.72"),
    ("raw qfrac z n=8", "+6.91", "z=+6.91"),
    ("saturation n=8", "36 of 6420", "8          6420           36"),
    # -- the deflation
    ("argmax n=7", "583", "583"),
    ("argmax n=6", "83", "83"),
    # -- Theorem 4 general
    ("theorem4 cases", "972", "(poset, weight) cases: 972"),
    ("theorem4 nonuniform", "891", "NOT the uniform-move weight: 891"),
    ("theorem4 matrix cases", "228", "(poset, weight) cases: 228"),
    # -- cycles
    ("n<=8 exhaustive", "19,440", "19440 non-chain posets at n <= 8"),
    ("n=8 classes", "16,998", "16998"),
    ("n=9 witness e", "1431", "e(P) = 1431"),
    ("n=9 margins", "80/159", "80/159"),
    ("n=10 e", "7134", "e(P) = 7134"),
    ("n=11 e", "78474", "78474"),
    # -- controls
    ("lemma control", "2583 levels", "2583 levels, 0 bad"),
    ("N2 fires", "190 mismatches", "190 mismatches under the mutation"),
    ("N1 fires", "34 disagreements", "34 disagreements under the mutation"),
    ("N3 fires", "25 posets differ", "25 posets where the two differ"),
    ("A001035", "6129859", "6129859"),
    ("A000112", "16999", "16999"),
]

# Sentences the repair struck from the TARGET document.  Must be present, and every
# occurrence must be inside a "> **STRUCK" epitaph.
STRUCK = [
    "tied with every other member of its group",
    "not weakly, but by an",
    "no cycle in 4200 random posets at each of `n = 8, 9, 10`",
    "rank 1 of 5 tied with 4 at `n = 7`",
]

# Sentences that MUST be live in the target document after the repair.
LIVE = [
    "The smallest `n` carrying a majority cycle is exactly 9.",
    "For **any** probability weight on the `P`-compatible moves",
    "Corrected verdict on the quotient side",
]


def struck_regions(doc):
    spans = []
    pos = 0
    start = None
    for line in doc.split("\n"):
        s = line.lstrip()
        if start is None and s.startswith("> **STRUCK"):
            start = pos
        elif start is not None and not s.startswith(">"):
            spans.append((start, pos))
            start = None
        pos += len(line) + 1
    if start is not None:
        spans.append((start, pos))
    return spans


def only_inside(doc, needle, spans):
    i = doc.find(needle)
    if i < 0:
        return None                      # absent altogether
    while i >= 0:
        if not any(a <= i < b for a, b in spans):
            return False                 # live somewhere
        i = doc.find(needle, i + 1)
    return True


def norm(s):
    """Unicode minus / times / non-breaking hyphen -> ASCII, for figure matching."""
    return (s.replace("−", "-").replace("–", "-").replace("—", "-")
             .replace("×", "x").replace("’", "'"))


def main():
    target = open(TARGET).read()
    repair = open(REPAIR).read()
    prose = norm(target + "\n" + repair)
    out = norm("\n".join(open(os.path.join(HERE, f)).read() for f in OUTS))

    print("=" * 78)
    print("CHECK: the repair's prose against the repair's outputs")
    print("=" * 78)
    bad = []
    for label, in_doc, in_out in CHECKS:
        d = norm(in_doc) in prose
        o = norm(in_out) in out
        if not (d and o):
            bad.append((label, d, o, in_doc, in_out))
        print("  [%s] %-26s doc:%s out:%s"
              % ("ok  " if (d and o) else "FAIL", label,
                 "yes" if d else "NO ", "yes" if o else "NO "))

    print()
    print("=" * 78)
    print("CHECK: struck sentences are quoted ONLY inside their epitaphs")
    print("=" * 78)
    spans = struck_regions(target)
    print("  %d '> **STRUCK' block(s) found in the target document" % len(spans))
    for s in STRUCK:
        v = only_inside(target, s, spans)
        state = {True: "ok  ", False: "FAIL", None: "FAIL"}[v]
        why = {True: "quoted, and only inside an epitaph",
               False: "APPEARS IN LIVE PROSE",
               None: "ABSENT -- the retraction is not legible"}[v]
        if v is not True:
            bad.append(("struck: " + s[:40], False, True, s, ""))
        print("  [%s] %-46s %s" % (state, s[:46], why))

    print()
    print("=" * 78)
    print("CHECK: the replacement sentences are live")
    print("=" * 78)
    for s in LIVE:
        v = only_inside(target, s, spans)
        ok = (v is False)                # present and NOT inside an epitaph
        if not ok:
            bad.append(("live: " + s[:40], False, True, s, ""))
        print("  [%s] %-46s %s" % ("ok  " if ok else "FAIL", s[:46],
                                   "live" if ok else "missing or struck"))

    print()
    print("=" * 78)
    print("GUARDS")
    print("=" * 78)
    guards = []
    ctl = open(os.path.join(HERE, "out_controls.txt")).read()
    if "ALL CONTROLS PASS, AND ALL FOUR NEGATIVE CONTROLS FIRE." not in ctl:
        guards.append("out_controls.txt does not end clean")
    # Precise per-file failure markers.  A blanket "does the word FAIL appear"
    # test is not usable here: several of these files legitimately print the word
    # (out_section4.txt's own title is "THE GROUPS WHERE THE TEST CAN FAIL").
    for f, markers in (("out_theorem4.txt", ("   FAIL ",)),
                       ("out_cycles.txt", ("Traceback", "AssertionError")),
                       ("out_section4.txt", ("Traceback", "AssertionError")),
                       ("out_controls.txt", ("  FAIL ",))):
        body = open(os.path.join(HERE, f)).read()
        for m in markers:
            if m in body:
                guards.append("%s contains %r" % (f, m))
    if "FAILURES: 0" not in open(os.path.join(HERE, "out_theorem4.txt")).read():
        guards.append("out_theorem4.txt does not report FAILURES: 0")
    # the conditionality discipline the target set for itself, applied to the repair
    for pat in ("the counterexample is", "counterexamples are frozen and have",
                "we have shown that no counterexample",
                "qmass = 1 detects a counterexample",
                "the extremal posets are counterexamples"):
        if pat.lower() in repair.lower():
            guards.append("repair contains an unconditional claim: %r" % pat)
    # the repair must not claim a filter or a mechanism it does not have
    for pat in ("is a filter", "explains why", "mechanism is established"):
        if pat.lower() in repair.lower():
            guards.append("repair overclaims: %r" % pat)
    for g in guards:
        print("  [FAIL] %s" % g)
    if not guards:
        print("  all guards clean")

    print()
    if bad or guards:
        print("%d check(s) failed, %d guard(s) tripped" % (len(bad), len(guards)))
        for label, d, o, a, b in bad:
            if not d:
                print("    prose is missing / misplaced: %r" % a)
            if not o:
                print("    output is missing: %r" % b)
        return 1
    print("ALL %d QUOTED FIGURES VERIFIED, %d STRUCK SENTENCES CONFINED TO THEIR"
          % (len(CHECKS), len(STRUCK)))
    print("EPITAPHS, %d REPLACEMENTS LIVE, GUARDS CLEAN." % len(LIVE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
