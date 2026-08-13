#!/usr/bin/env python3
"""mg-30bd — THE PLANTED WORLDS THAT BOUND THE CLASSIFIER.

An instrument whose only output is a number needs the worlds it must NOT catch written down
beside the worlds it must, or the number is unfalsifiable — mg-f771's `g1_controls.py` is
the shape and this is the same shape over a different verdict.

FIVE WORLDS MUST COME OUT BENIGN.  Those five are the ENTIRE reason this instrument is not
just a re-run of mg-20ee's census: an address that moved, a sha that moved, a date that
moved, a timing that moved and a checkout root that moved are the four families the corpus
already knows about, and a classifier that graded any of them a verdict move would report
the population mg-20ee already measured under a new name.

TWO WORLDS ARE BOUNDARIES AND THEY ARE THE ONES THAT WERE WRONG FIRST.  W12 holds the
address mask narrow — the first version of `ADDRESS` was `(?<=[\\w./-]):\\d+\\b` and it ate
`TOTAL BAD:1`, which is the exact number this whole ticket is about, turning the motivating
instance BENIGN.  W13 holds it wide enough — an address that moves ON a verdict line must
stay benign, or every one of mg-20ee's 32 pinnings would be re-reported here as a verdict
move and this instrument would measure nothing new.

Pure strings in, buckets out.  No git, no sandbox, no corpus: this file is a fixed point by
construction, which is what lets it sit in `run_all.sh` beside a report that is not.
"""

import sys

import lib30bd as L

ROOT_A = "/Users/daniel/.pogo/polecats/p28b6"
ROOT_B = "/private/tmp/claude-501/x/scratchpad/ref"

WORLDS = [
    # id, expected bucket, what it is, committed text, regenerated text
    ("W0", L.IDENTICAL, "the same bytes twice",
     "VERDICT: GREEN -- 3 findings\n",
     "VERDICT: GREEN -- 3 findings\n"),

    ("W1", L.BENIGN_F771, "a wall-clock timing (mg-f771 N2)  <- BENIGN ON PURPOSE",
     "A1 TOTAL BAD: 1\n  ran in 0.53s\n",
     "A1 TOTAL BAD: 1\n  ran in 1.21s\n"),

    ("W2", L.BENIGN_F771, "a foreign checkout root (mg-f771 N1)  <- BENIGN ON PURPOSE",
     "read %s/code/a/b.py\nVERDICT: GREEN\n" % ROOT_A,
     "read %s/code/a/b.py\nVERDICT: GREEN\n" % ROOT_B),

    ("W3", L.BENIGN_ADDR, "a LINE ADDRESS moved -- mg-c824/mg-20ee's family  <- BENIGN ON PURPOSE",
     "the guard is at build.sh:342\nA1 TOTAL BAD: 1\n",
     "the guard is at build.sh:352\nA1 TOTAL BAD: 1\n"),

    ("W4", L.BENIGN_ADDR, "the as-of block's sha moved  <- BENIGN ON PURPOSE",
     "corpus read at 5a62e8c\nVERDICT: GREEN\n",
     "corpus read at f2117f1\nVERDICT: GREEN\n"),

    ("W5", L.BENIGN_ADDR, "the as-of block's date and clock moved  <- BENIGN ON PURPOSE",
     "measured on 2026-08-10 at 04:43:26\nVERDICT: GREEN\n",
     "measured on 2026-08-13 at 12:00:07\nVERDICT: GREEN\n"),

    ("W6", L.VERDICT_TOKEN, "a *** MISSED *** row stopped firing -- mg-6cb9's Q2 exactly",
     "  Q2  check_doc.py  delete C4's anchor   1  0  *** MISSED ***\n",
     "  Q2  check_doc.py  delete C4's anchor   1  1  ok\n"),

    ("W7", L.VERDICT_TOKEN, "VERDICT: GREEN became VERDICT: RED",
     "VERDICT: GREEN -- 20 entries\n",
     "VERDICT: RED -- 20 entries\n"),

    ("W8", L.VERDICT_TOKEN, "a selftest assertion started failing",
     "  e2_crosssection.py exits 0 unmutated   ok\n",
     "  e2_crosssection.py exits 0 unmutated   *** FAILED ***\n"),

    ("W9", L.VERDICT_NUMBER, "A1 TOTAL BAD: 1 -> 0 -- mg-6cb9's headline",
     "A1 TOTAL BAD: 1\n",
     "A1 TOTAL BAD: 0\n"),

    ("W10", L.NON_VERDICT, "a corpus-size count on a line carrying no token",
     "E2 POPULATION EXAMINED: 530 markdown file(s)\n",
     "E2 POPULATION EXAMINED: 531 markdown file(s)\n"),

    ("W11", L.NON_VERDICT, "a repo-relative path moved (mg-f771 W7) on a non-verdict line",
     "reads code/face_geometry/controls.py\n",
     "reads code/face_geometry/controls_output.txt\n"),

    ("W12", L.VERDICT_NUMBER,
     "BOUNDARY: `TOTAL BAD:1` has no space and MUST NOT be eaten as an address",
     "A1 TOTAL BAD:1\n",
     "A1 TOTAL BAD:0\n"),

    ("W13", L.BENIGN_ADDR,
     "BOUNDARY: an address that moved ON a verdict line is still a pinning  <- BENIGN ON PURPOSE",
     "  PASS  the anchor is at STATE.md:209\n",
     "  PASS  the anchor is at STATE.md:210\n"),

    ("W14", L.NON_VERDICT,
     "the TAIL after a normalised checkout root differs (mg-f771 W6), no token on the line",
     "cannot read %s/code/g/BASELINE.json.no-such-file\n" % ROOT_A,
     "cannot read %s/code/g/BASELINE.json.OTHER\n" % ROOT_B),

    ("W15", L.NON_VERDICT,
     "verdict lines REORDERED and nothing else -- layout is not a verdict move",
     "VERDICT: GREEN\n  A HELD\n  B FAILS\n",
     "VERDICT: GREEN\n  B FAILS\n  A HELD\n"),

    ("W16", L.VERDICT_TOKEN,
     "mg-6cb9's two real rows, verbatim: EXTENT WIDER stopped firing",
     "  Q10  w3_scope.py  WIDE X4 in species_7d75/sub/leak.md  0  0  *** EXTENT WIDER ***\n"
     "  Q17  s1_extent.py WIDE X3 in species_7d75/sub/leak.md  0  0  *** EXTENT WIDER ***\n",
     "  Q10  w3_scope.py  WIDE X4 in species_7d75/sub/leak.md  0  0  extent TRUE here\n"
     "  Q17  s1_extent.py WIDE X3 in species_7d75/sub/leak.md  0  0  extent TRUE here\n"),

    ("W17", L.NON_VERDICT,
     "a count moved on a line with a token, but the token multiset did not -- reported as\n"
     "       NON-VERDICT only because the LINE has no number of its own; see W18",
     "checked the population\n  530 files\n",
     "checked the population\n  531 files\n"),

    ("W18", L.VERDICT_NUMBER,
     "THE STATED COST: a corpus-size count sharing a line with a token reads as a verdict\n"
     "       move.  Over-inclusive ON PURPOSE, and it is why the bucket is split in two",
     "  PASS -- 530 file(s) checked\n",
     "  PASS -- 531 file(s) checked\n"),
]


def main():
    out = []
    fails = 0
    out.append("=" * 78)
    out.append("mg-30bd selftest -- the worlds the classifier must catch, and the five it must not")
    out.append("=" * 78)
    out.append("")
    out.append("  %-4s %-20s %-20s %s" % ("id", "expected", "got", "what it is"))
    out.append("  " + "-" * 74)
    for wid, want, what, a, b in WORLDS:
        got, _detail = L.classify(a, b)
        ok = (got == want)
        if not ok:
            fails += 1
        out.append("  %-4s %-20s %-20s %s" % (wid, want, got if ok else got + " ***", what))
    out.append("")

    # THE TOKEN SET IS ITSELF ASSERTED, because it is the instrument.  A token that is not
    # all-caps would make the case rule a lie, and a duplicate would silently double-weight
    # one word in the multiset comparison.
    out.append("  the token set, asserted rather than trusted")
    out.append("  " + "-" * 74)
    checks = [
        ("every token is ALL-CAPS", all(t.isupper() and t.isalpha() for t in L.TOKENS)),
        ("no duplicates", len(set(L.TOKENS)) == len(L.TOKENS)),
        ("no token shorter than 3 characters", all(len(t) >= 3 for t in L.TOKENS)),
        ("lower-case `pass` is NOT a token", not L.is_verdict_line("this pass is fine")),
        ("`PASSED` inside `BYPASSED` is NOT a token", not L.is_verdict_line("BYPASSED")),
        ("a bare prose line is not a verdict line", not L.is_verdict_line("THE SUBJECT IS A COMMITTED REPORT")),
        ("`*** MISSED ***` is a verdict line", L.is_verdict_line("  *** MISSED ***")),
    ]
    for label, ok in checks:
        if not ok:
            fails += 1
        out.append("  %-66s %s" % (label, "ok" if ok else "*** FAILED ***"))
    out.append("")
    out.append("=" * 78)
    out.append("mg-30bd selftest: %d world(s) + %d assertion(s), %d failed"
               % (len(WORLDS), len(checks), fails))
    out.append("=" * 78)
    print("\n".join(out))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
