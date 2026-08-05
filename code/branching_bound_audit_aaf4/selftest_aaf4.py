"""SELFTEST -- break the thing this audit measures, and require the audit to notice.

Every mutation asserts `mutated != original` BEFORE it asserts that a verdict
moved.  mg-fcb2 landed the reason: a corruption that is a no-op leaves the check
green and the row reads as a pass.  A green row here means the detector moved
because the text moved, not because nothing happened.

Two kinds of case:

  DOC   the living document is copied, broken at a named site, and re-counted.
  UNIT  a classifier of `lib_aaf4` is handed a string and required to classify it.

EXIT 0 if every case passes.  PREDICTED 0.
"""

import os
import re
import shutil
import sys

import lib_aaf4 as L

OUT = sys.stdout
TMP = os.path.join(L.HERE, ".selftest_tmp")
CASES = []
FAILS = []


def case(name, got, want, note=""):
    ok = got == want
    CASES.append((name, got, want, ok))
    if not ok:
        FAILS.append(name)
    print("    %-56s got %-9s want %-9s %s"
          % (name[:56], repr(got)[:9], repr(want)[:9], "ok" if ok else "FAIL"),
          file=OUT)
    if note:
        print("      %s" % note, file=OUT)


def mutate(text, old, new):
    assert old in text, "mutation target absent: %r" % old[:60]
    out = text.replace(old, new, 1)
    assert out != text, "MUTATION WAS A NO-OP: %r" % old[:60]
    return out


def write(text, tag):
    p = os.path.join(TMP, tag + ".md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


def counts(path):
    st = L.strict_sites(path)
    rx = L.relaxed_sites(path)
    return (len(st), sum(1 for r in st if not r[3]),
            len(rx), sum(1 for r in rx if not r[3]), len(L.occurrences(path)))


def main():
    L.rule(OUT, "SELFTEST mg-aaf4 -- every mutation asserted a real change\n"
                "before its verdict is checked.")
    print(file=OUT)
    os.makedirs(TMP, exist_ok=True)
    base = open(L.DOC, encoding="utf-8").read()
    b = counts(write(base, "base"))
    L.rule(OUT, "  THE BASELINE.  Population: the living document as it\n"
                "  stands.  Grain: sentences (S) and occurrences (O).")
    print("    STRICT sites %d, unbounded %d | RELAXED sites %d, unbounded %d "
          "| occurrences %d" % b, file=OUT)
    print(file=OUT)

    L.rule(OUT, "  DOC CASES.  The document, broken one site at a time.")

    # M1 -- take the bound out of a bounded site.
    t = mutate(base,
               "of the **33** intervals `[0̂, w]` with `rank(w) ≤ 6`",
               "of the **33** intervals")
    m = counts(write(t, "m1"))
    case("M1 removing a rank bound makes that site UNBOUNDED",
         m[3], b[3] + 1, "RELAXED unbounded %d -> %d" % (b[3], m[3]))

    # M2 -- replace the bound with a softening word.
    t = mutate(base,
               "of the **33** intervals `[0̂, w]` with `rank(w) ≤ 6`",
               "of the **33** intervals, roughly all of them,")
    m = counts(write(t, "m2"))
    case("M2 a HEDGE is not a bound: the site stays UNBOUNDED",
         m[3], b[3] + 1, "`roughly` must not score as a scope")

    # M3 -- block-quote a whole unit.
    t = mutate(base,
               "| **B4** | **as whole lattices**",
               "> | **B4** | **as whole lattices**")
    m = counts(write(t, "m3"))
    case("M3 block-quoting a unit removes its site(s)", m[2] < b[2], True,
         "RELAXED sites %d -> %d" % (b[2], m[2]))

    # M4 -- strike a unit.  RESPECIFIED, and the first form's transcript is
    # committed as `out_selftest_aaf4_FIRSTFORM_exit1.txt`.  The first form put
    # the marker in the row's FIRST cell (`| **B4** |`) and the count did not
    # move, because the liveness rule is applied per CELL and the figure lives in
    # a different cell of the same row.  That is not a bug in the test; it is
    # mg-d075's own floor finding reproduced here by accident, from the other
    # side, and the fix is to strike the cell that actually carries the figure.
    t = mutate(base, "30 Young intervals `[∅, λ]` with `λ` of size ≤ 6",
               "**STRUCK** 30 Young intervals `[∅, λ]` with `λ` of size ≤ 6")
    m = counts(write(t, "m4"))
    case("M4 a STRUCK marker removes the site(s) OF ITS OWN CELL",
         m[2] < b[2], True,
         "RELAXED sites %d -> %d; the marker binds to the cell, not the row"
         % (b[2], m[2]))

    # M5 -- state the figure twice in one sentence: O moves, S does not.
    t = mutate(base,
               "T8 measures the illustrative case: Young–Fibonacci",
               "T8 measures the illustrative case (33 of them): Young–Fibonacci")
    m = counts(write(t, "m5"))
    case("M5 GRAIN O counts a second occurrence in one sentence",
         (m[4] - b[4], m[2] - b[2]), (1, 0),
         "occurrences +1, sentence-grain sites +0 -- the two grains separate")

    # M6 -- drop the name from a sentence: STRICT loses it, RELAXED keeps it.
    # RESPECIFIED with the first form kept: the first form stripped the name from
    # the line-435 cell, whose ONLY attribution is that name, so RELAXED lost the
    # site too and the case failed.  A relaxation can only rescue a sentence whose
    # UNIT still names the family -- which is the whole content of the 8-vs-9
    # difference -- so the target must be a multi-sentence cell.
    t = mutate(base,
               "on 28 of the 33 Young–Fibonacci intervals `[0̂, w]` with "
               "`rank(w) ≤ 6`",
               "on 28 of the 33 such intervals with `rank(w) ≤ 6`")
    m = counts(write(t, "m6"))
    case("M6 STRICT loses a site the unit still attributes; RELAXED keeps it",
         (b[0] - m[0], b[2] - m[2]), (1, 0),
         "this is the exact 8-vs-9 difference mg-d075 found in mg-19ec")

    # M7 -- a bound in the NEXT sentence does not rescue this one.
    t = mutate(base,
               "of the **33** intervals `[0̂, w]` with `rank(w) ≤ 6`, *\"28 are",
               "of the **33** intervals. They have `rank(w) ≤ 6`. *\"28 are")
    m = counts(write(t, "m7"))
    case("M7 a bound in the NEXT sentence does not bound this one",
         m[3] > b[3], True, "the s2.1 defect, reconstructed: %d -> %d unbounded"
         % (b[3], m[3]))

    print(file=OUT)
    L.rule(OUT, "  UNIT CASES.  The classifiers, handed strings.")

    case("U1 a bare `population` is KEYWORD ONLY, not a scope",
         L.scope_class("EIGHT was not the population."), "KEYWORD ONLY")
    case("U2 a count with its denominator is a NUMERIC SCOPE",
         L.scope_class("10 of 254 sentences."), "NUMERIC SCOPE")
    case("U3 `row-10 sentence` is a LABEL, not a count",
         L.scope_class("the row-10 sentence of the table"), "NONE",
         "the respecification recorded in lib_aaf4; first form scored this NUMERIC")
    case("U4 markdown bold between numeral and unit does not hide the count",
         L.scope_class("the list has **25** entries"), "NUMERIC SCOPE",
         "the respecification that moved the count AGAINST my own finding")
    case("U5 an inequality is a scope", L.scope_class("all `|λ| ≤ 6`"),
         "NUMERIC SCOPE")
    case("U6 a sentence with neither is NONE",
         L.scope_class("It misses the point entirely."), "NONE")
    case("U7 a QUOTED strike marker is a MENTION",
         [c for _, c in L.strike_evidence("units carrying a `**STRUCK` marker")],
         ["MENTION"])
    case("U8 an APPLIED strike marker is a USE",
         [c for _, c in L.strike_evidence("**STRUCK by mg-6ad0's X4**")],
         ["USE"])
    case("U9 the figure in words is detected",
         bool(L.FIG_WORD.search("thirty-three intervals")), True)
    case("U10 `16733` is not the figure", bool(L.FIG.search("arXiv:2404.16733")),
         False, "a word-boundary test, so an arXiv id is not a site")

    print(file=OUT)
    L.rule(OUT, "  THE MUTATIONS WERE REAL.  Every DOC case above raised\n"
                "  AssertionError if its target string was absent or if the\n"
                "  replacement left the text unchanged.  A no-op corruption\n"
                "  cannot reach a verdict here.")
    print("    doc cases : %d      unit cases : %d"
          % (7, len(CASES) - 7), file=OUT)
    print(file=OUT)

    shutil.rmtree(TMP)
    L.rule(OUT)
    print("SUMMARY selftest_aaf4: %d case(s), %d failure(s)"
          % (len(CASES), len(FAILS)), file=OUT)
    for f in FAILS:
        print("SUMMARY selftest_aaf4: FAILED %s" % f, file=OUT)
    L.rule(OUT)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
