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

import re
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
    # THE REGEX THAT FAILED, RE-RUN HERE RATHER THAN DESCRIBED IN A README.  A defect an
    # author fixed before the first commit leaves no trace, and this one is the single
    # clearest argument that this classifier is not mg-20ee's census renamed — so it is a
    # measurement that runs every time, not a sentence somebody can delete without noticing.
    out.append("")
    out.append("  THE ADDRESS REGEX THAT FAILED, RE-MEASURED ON EVERY RUN")
    out.append("  " + "-" * 74)
    out.append("  A1 as first written was  (?<=[\\w./-]):\\d+\\b  — a colon-and-digits after any")
    out.append("  word character.  Under it:")
    out.append("")
    naive_checks = []
    for wid, want_naive, a, b in [
        ("W12", L.BENIGN_ADDR, "A1 TOTAL BAD:1\n", "A1 TOTAL BAD:0\n"),
        ("W3", L.BENIGN_ADDR, "the guard is at build.sh:342\n", "the guard is at build.sh:352\n"),
        ("W9", L.VERDICT_NUMBER, "A1 TOTAL BAD: 1\n", "A1 TOTAL BAD: 0\n"),
    ]:
        got = L.classify(a, b, L.naive_mask)[0]
        naive_checks.append((wid, want_naive, got))
        out.append("    %-4s naive -> %-20s shipped -> %-20s"
                   % (wid, got, L.classify(a, b)[0]))
    out.append("")
    out.append("  SO THE NAIVE MASK GRADES `TOTAL BAD:1 -> 0` AS A BENIGN ADDRESS MOVE — it turns")
    out.append("  the exact number this ticket is about into mg-20ee's already-counted family, and")
    out.append("  it does so while still handling build.sh:342 correctly, which is what makes the")
    out.append("  defect invisible in the cases an author checks first.  W12 is the world that")
    out.append("  holds the shipped regex narrow and W3 is the one that holds it wide enough.")
    out.append("")
    for wid, want_naive, got in naive_checks:
        ok = (got == want_naive)
        if not ok:
            fails += 1
        out.append("  %-66s %s" % ("the naive mask still grades %s as %s" % (wid, want_naive),
                                   "ok" if ok else "*** FAILED ***"))
    # mg-5491's DECLARATION, BOUNDED THE SAME WAY THE CLASSIFIER IS.  The worlds that must
    # NOT be a declaration are the ones that matter: this estate's instruments quote each
    # other, so the marker WILL appear inside transcripts that are not declaring anything —
    # report.py prints it in its own §3b, and out_owners_937c.txt and this file's own
    # transcript quote it below.  D3 is the world that stops those exempting themselves.
    out.append("")
    out.append("  mg-5491 — WHAT IS AND IS NOT A DECLARATION")
    out.append("  " + "-" * 74)
    head20 = "\n".join("line %d" % i for i in range(L.DECLARATION_WINDOW + 4))
    marked = "# " + L.DECLARATION + " it reads a stream outside this repository"
    decl_worlds = [
        ("D0", "a `#`-commented marker on line 2, with a reason",
         "== a transcript ==\n" + marked + "\nbody\n",
         "it reads a stream outside this repository"),
        ("D1", "the same marker with no `#` and no indent",
         L.DECLARATION + " the producer can no longer see what it saw\n",
         "the producer can no longer see what it saw"),
        ("D2", "MALFORMED: the marker with nothing after it -> \"\", which is NOT None",
         "# " + L.DECLARATION + "\n", ""),
        ("D3", "BOUNDARY: a QUOTATION past the window exempts nothing  <- None ON PURPOSE",
         head20 + "\n" + marked + "\n", None),
        ("D4", "BOUNDARY: prose that means it but is not the literal  <- None ON PURPOSE",
         "# A TRUE RECORD.  DO NOT RE-RUN THIS.\n", None),
        ("D5", "BOUNDARY: the marker mid-sentence is a mention, not a declaration",
         "# the marker is spelled " + L.DECLARATION + " and it goes at the top\n", None),
    ]
    for wid, what, text, want in decl_worlds:
        got = L.declaration(text)
        ok = (got == want)
        if not ok:
            fails += 1
        out.append("  %-4s %-20s %s" % (wid, "ok" if ok else "*** FAILED *** %r" % (got,), what))

    # mg-aff1's WALK DETECTOR, BOUNDED THE SAME WAY.  The worlds that must NOT be a walk
    # line are again the ones that matter: a NOTE is an assertion about somebody else's
    # transcript, so a detector that over-fires is louder than one that under-fires and
    # wrong in the direction that cannot be quietly absorbed.  V4 and V5 are the two
    # refuted widenings run on the SAME strings, so the boundary is shown rather than
    # claimed — `naive_mask`'s arrangement, one detector along.
    out.append("")
    out.append("  mg-aff1 — WHAT IS AND IS NOT A HISTORY-WALK LINE")
    out.append("  " + "-" * 74)
    walk_worlds = [
        ("V0", True, "a bare masked sha at line start — the shape that always worked",
         "<sha> apply: THE FINDING WAS ALREADY APPLIED"),
        ("V1", True, "a LABELLED sha — `by <sha>  <subject>`, mg-aff1's subject",
         "by <sha>  repair: THE VERDICT IS LEAVE-AND-RECORD"),
        ("V2", True, "a labelled sha with a COLON behind it, not a space",
         "at <sha>: ## Kill-shot 2 — Standard dominance — **GREEN**"),
        ("V3", True, "the widest true label on the record, 13 characters",
         "the tip      <sha> <date>  docs: re-scope C3"),
        ("V4", True, "`HEAD's subject :` — the shape mg-937c §6.4 named",
         "HEAD's subject    : instrument: THE CLASSIFIER FOR VERDICT-STALENESS"),
        ("V5", False, "BOUNDARY: a FINDING sentence quoting a sha  <- NOT A WALK ON PURPOSE",
         "FINDING: a passage deleted by <sha> survives UNMARKED at t1_tl.py:<L>"),
        ("V6", False, "BOUNDARY: a sha behind a punctuated label  <- NOT A WALK ON PURPOSE",
         "N20 H8: the <sha> table's two ROW LABELS exchanged (E2b)"),
        ("V7", False, "BOUNDARY: a BARE COMMIT SUBJECT — the shape still open, §6.4",
         "instrument: THE CLASSIFIER FOR VERDICT-STALENESS, AND THE FIVE WORLDS"),
        ("V8", False, "BOUNDARY: a verdict line with no sha at all",
         "  Q2  check_doc.py  delete C4's anchor   1  0  *** MISSED ***"),
    ]
    for wid, want, what, text in walk_worlds:
        got = L.is_walk_line(text)
        ok = (got == want)
        if not ok:
            fails += 1
        out.append("  %-4s %-20s %s" % (wid, "ok" if ok else "*** FAILED *** %r" % (got,), what))
    out.append("")
    out.append("  AND THE TWO WIDENINGS THAT LOOK RIGHT UNTIL THEY ARE RUN, ON THE SAME STRINGS")
    out.append("  " + "-" * 74)
    out.append("  %-4s %-9s %-9s %-9s %s" % ("id", "shipped", "anywhere", "subject", "the string"))
    for wid, _want, _what, text in walk_worlds:
        out.append("  %-4s %-9s %-9s %-9s %s"
                   % (wid, L.is_walk_line(text), L.walk_anywhere(text),
                      L.walk_bare_subject(text), text[:44]))
    out.append("")
    out.append("  `anywhere` DROPS THE WINDOW and takes V5 with it — a FINDING that quotes a sha")
    out.append("  is not a walk, and annotating it would put mg-e720's cause on somebody else's")
    out.append("  finding.  `subject` takes V7 and it is the reason V7 is still open: it also")
    out.append("  takes any `word: text` line, and no rule over the line's own text tells the")
    out.append("  two apart.  Both are re-measured over the whole record in out_owners_937c.txt")
    out.append("  §6.4, where the counts are, so neither refutation rests on these 9 strings.")
    # THE WINDOW IS A PLATEAU AND NOT A TUNING, RE-DERIVED HERE RATHER THAN ASSERTED: the
    # regex is rebuilt at every width from 13 to 24 and must give the SAME nine answers.  A
    # constant that only works at the value its author picked is a fit to a corpus.
    plateau = []
    for k in range(13, 25):
        alt = re.compile(r"^(?:HEAD:\s*)?[A-Za-z ]{0,%d}<sha>[:,]?\s+\S" % k)
        plateau.append(tuple(bool(alt.match(t) or L.HEAD_SUBJECT.match(t))
                             for _i, _w, _wh, t in walk_worlds))
    shipped = tuple(L.is_walk_line(t) for _i, _w, _wh, t in walk_worlds)
    walk_checks = [
        ("the window is a PLATEAU: widths 13..24 give the shipped answer, all 12 of them",
         all(p == shipped for p in plateau)),
        # NOT `anywhere is strictly wider`, WHICH IS WHAT THIS CHECK SAID FIRST AND IT CAME
        # BACK RED ON V4.  The two rules are not nested: `anywhere` drops the window and
        # gains V5/V6, and it has no notion of the `HEAD's subject` literal, so it LOSES V4.
        # Dropping the window is not a superset — it is a different rule, and the check now
        # says which way each disagreement runs instead of asserting containment.
        ("`anywhere` gains V5/V6 and LOSES V4 — the two rules are not nested",
         all(L.walk_anywhere(t) for _i, _w, _wh, t in walk_worlds
             if L.is_walk_line(t) and not L.HEAD_SUBJECT.match(t))
         and L.walk_anywhere("FINDING: a passage deleted by <sha> survives UNMARKED")
         and not L.walk_anywhere("HEAD's subject    : instrument: THE CLASSIFIER")),
        ("a bare subject is NOT a walk line under the shipped rule",
         not L.is_walk_line("census+repair: THE FOUR ROWS RE-DERIVED FROM THE TREE")),
    ]
    for label, ok in walk_checks:
        if not ok:
            fails += 1
        out.append("  %-66s %s" % (label, "ok" if ok else "*** FAILED ***"))

    out.append("")
    out.append("=" * 78)
    out.append("mg-30bd selftest: %d world(s) + %d assertion(s), %d failed"
               % (len(WORLDS) + len(decl_worlds) + len(walk_worlds),
                  len(checks) + len(naive_checks) + len(walk_checks), fails))
    out.append("=" * 78)
    print("\n".join(out))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
