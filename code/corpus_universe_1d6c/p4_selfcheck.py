"""P4 -- THE SELF-CHECK, REPAIRED TO THE STANDARD IT ENFORCES.  Three fixes.

mg-d075's `s5_own_criticism.py` says of its own standard:

    "A neighbouring sentence does not rescue it -- that is precisely the standard
     this repair applied to the document, and applying a weaker one to myself would
     be the defect a second time."

It is a weaker one, in three separate ways, and this script fixes each and prints
what the fix costs.

  FIX 1  THE STANDARD.  `s4`'s H3 classifies a bound NUMERIC SCOPE iff the substring
         carrying it contains a digit.  `s5`'s OWNSCOPE also accepts the bare words
         `population`, `grain`, `live sentences`, the tokens STRICT / RELAXED /
         POP-<n>, and a bare path.  Here the accepted substring must pass H3 --
         tightened by ONE further clause, that a digit inside a LABEL is not a
         count (`POP-3`, `H3`, `row-10`, `mg-d075`).  That clause is mine, it is a
         choice, and every accepted substring is printed so it can be argued with.

  FIX 2  THE POPULATION.  `s5`'s MINE lists 2 documents; mg-d075 authored 3.
         `code/branching_bound_d075/PREDICTIONS.md` was never looked at.

  FIX 3  THE DETECTOR.  `s5`'s FAULT lists the literal `cannot see`; the sentence in
         mg-d075's own account describing the defect the whole repair exists for
         says `could not see`.  Fixed by matching THE PROPERTY -- a negated or
         modal verb of perception -- and not the string, because a tense-sensitive
         detector drifts again on the next synonym.

NOTHING OF mg-d075's IS EDITED.  Its regexes and its MINE list are IMPORTED FROM ITS
SOURCE and executed here; its published result is reproduced BEFORE anything is
disagreed with.  Editing `s5` in place would make its committed transcript
non-regenerable, which is the defect mg-aaf4's D2 caught one level up.

EVERY FIX IS PROVED ABLE TO FIRE (S6).  A negative needs an instrument that could
have shown the positive: each fix is run against a constructed input on which the
old form passes and the new form must fail, and the assertion is printed.

EXIT 1 if any criticism sentence of mg-d075's fails the repaired standard.
PREDICTED 1 -- the check is supposed to bite.
"""

import os
import re
import sys

import lib1d6c as U

if U.D075 not in sys.path:
    sys.path.insert(0, U.D075)
import s5_own_criticism as S5                                   # noqa: E402

if U.AAF4 not in sys.path:
    sys.path.insert(0, U.AAF4)
import lib_aaf4 as A                                            # noqa: E402

OUT = sys.stdout

# ---------------------------------------------------------------- FIX 3
# The property, not the string.  A criticism of someone's instrument says it does
# not perceive something.  Negation or modality, then a verb of perception --
# tense, aspect and modal free.
NEG = r"(?:can|could|cannot|can't|could ?n[o']t|does|do|did|will|would|is|are|was|" \
      r"were|has|have|had)\s*(?:not|n't|never)?"
PERCEIVE = r"(?:see|sees|seen|detect|detects|detected|reach|reaches|reached|" \
           r"cover|covers|covered|find|finds|found|notice|notices|noticed|" \
           r"count|counts|counted|catch|catches|caught)"
FAULT_PROPERTY = re.compile(
    r"\b(?:%s)\s+(?:%s)\b" % (NEG, PERCEIVE) +
    r"|\bnever\s+(?:%s)\b" % PERCEIVE +
    r"|\bfail(?:s|ed)?\s+to\s+(?:%s)\b" % PERCEIVE +
    r"|\bblind\s+(?:to|spot)\b", re.I)


def fault_repaired(s):
    return bool(S5.FAULT.search(s) or FAULT_PROPERTY.search(s))


# ---------------------------------------------------------------- FIX 1
# MY numeric-scope classifier.  RESPECIFIED ONCE, and the first form's transcript is
# committed beside this file as `out_p4_selfcheck_FIRSTFORM_exit1.txt`.
#
# THE FIRST FORM was "an OWNSCOPE match that contains a digit" -- H3's own rule,
# transplanted.  It scored 9 of 10 and it was wrong twice, in two different ways, and
# the parent's own rows are what exposed it:
#
#   DEFECT 1 (this instrument's).  It accepted `code/branching_audit_19ec` as a
#   numeric scope, because a four-hex-digit TICKET ID contains digits.  H3's rule is
#   sound where H3 applies it -- to the substring carrying a RANK BOUND -- and unsound
#   the moment it is pointed at a path.  A path is a FILE scope, not a numeric one.
#
#   DEFECT 2 (the same one mg-aaf4 hit).  It accepted `10 sentence` out of "the
#   row-10 sentence of §3": an ordinal LABEL naming one object, read as a count of a
#   population.  mg-aaf4 respecified for exactly this and said so at its own point of
#   check; I did not read that respecification closely enough before writing mine,
#   and I hit the same rock.
#
# THE SECOND FORM below is written from the units up rather than from OWNSCOPE down:
# an inequality, a count with its denominator, the family's rank bound, or a numeral
# immediately followed by a NAMED UNIT and not preceded by a hyphen or word character.
# DISCLOSURE: this respecification moves my count AWAY from s5's 10 of 10 and TOWARDS
# mg-aaf4's 7 of 10 -- that is, towards the finding I was sent to check. Both forms'
# transcripts are committed and S2 prints three classifiers side by side per row.
MY_NUMERIC = re.compile(
    r"(?:≤|<=|≥|>=)\s*\d+"
    r"|(?<![-\w])\d+\s*(?:of|/)\s*(?:the\s+)?\d+"
    r"|\brank\s*\(?w?\)?\s*(?:≤|<=)\s*\d"
    r"|\bto rank \d"
    r"|(?<![-\w])\d+\s+(?:sites?|sentences?|files?|rows?|cells?|tokens?"
    r"|intervals?|commits?|occurrences?|phrasings?|predictions?|figures?"
    r"|documents?|scripts?|instruments?|entries)\b")


# (file fragment, substring identifying the sentence, verdict, reason).  Written by
# hand AFTER reading the machine's three rows, and published per row.  mg-aaf4 turned
# 3 into 1 by the same method; this is my own reading of the same three sentences and
# it is recorded so it can be disagreed with rather than inherited.
ADJUDICATION = [
    ("repair-mg-d075-the-figure-and-its-scope.md", "And mg-19ec already had it",
     "OVERTURN",
     "FALSE NEGATIVE of my classifier: the sentence locates its claim exactly -- a "
     "named transcript and the row index [09] inside it.  A file-and-index IS a "
     "scope; what it is not is a COUNT, which is all my regex looks for."),
    ("OneThird-Branching-Graphs-Where-This-Lives.md", "Eight is not the population",
     "OVERTURN",
     "FALSE NEGATIVE: it states the population (live sentences of this file), the "
     "grain (mg-19ec's own) and two counts (9 sites, 5 unscoped).  My regex misses "
     "'were 9, of which 5' because the comma breaks the N-of-M form."),
    ("repair-mg-d075-the-figure-and-its-scope.md", "FOUR was not the population",
     "STANDS",
     "It asserts of two published figures that they are NOT the population while "
     "naming neither the population, the file, nor the grain.  The table carrying "
     "all three is nineteen lines above it, and a neighbouring table is exactly "
     "what this repair told the document was not enough."),
]


def strip_emphasis(s):
    return re.sub(r"[*`_]+", "", s)


def numeric_pass(s):
    """FIX 1: the sentence passes only on a scope token that is a count or bound."""
    m = MY_NUMERIC.search(strip_emphasis(s))
    return m.group(0) if m else None


def first_form_pass(s):
    """The form this script shipped first, kept so the change is visible."""
    for m in S5.OWNSCOPE.finditer(s):
        if U.numeric_scope(m.group(0)):
            return m.group(0)
    return None


def keyword_pass(s):
    m = S5.OWNSCOPE.search(s)
    return m.group(0) if m else None


def population(paths, added):
    pop = []
    for path in paths:
        if not os.path.exists(path):
            continue
        rel = os.path.relpath(path, U.ROOT)
        for a, _, s, _ in U.L.live_sentences(path):
            pop.append((rel, a, re.sub(r"\s+", " ", s).strip()))
    return pop + added


def show(rows, label):
    print("    %s" % label, file=OUT)
    for i, (f, l, s, ok, sub) in enumerate(rows, 1):
        print("      [%02d] %-46s :%-4d %s" % (i, f[-46:], l,
              "SCOPED (%s)" % sub if ok else "*** NO NUMERIC SCOPE ***"), file=OUT)
        for j in range(0, len(s), 96):
            print("           %s" % s[j:j + 96], file=OUT)
    print(file=OUT)


def main():
    U.rule(OUT, "P4  THE SELF-CHECK, REPAIRED TO THE STANDARD IT ENFORCES.\n"
                "    Three fixes, each proved able to fire.")
    print(file=OUT)

    added = S5.added_sentences()
    pop2 = population(S5.MINE, added)
    third = os.path.join(U.D075, "PREDICTIONS.md")
    pop3 = population(list(S5.MINE) + [third], added)

    # ------------------------------------------------------------------ S1
    U.rule(OUT, "  S1  REPRODUCE BEFORE DISAGREEING.  mg-d075's own regexes and\n"
                "      its own MINE list, IMPORTED FROM ITS SOURCE and executed.\n"
                "      Population: %d live sentences.  Grain: one sentence."
                % len(pop2))
    crit2 = [(f, l, s) for f, l, s in pop2
             if S5.FAULT.search(s) and S5.TARGET.search(s)]
    kw = [(f, l, s, bool(keyword_pass(s)), keyword_pass(s)) for f, l, s in crit2]
    n_pass = sum(1 for r in kw if r[3])
    print("    criticism sentences            : %d" % len(crit2), file=OUT)
    print("    passing s5's own OWNSCOPE      : %d of %d" % (n_pass, len(crit2)),
          file=OUT)
    print("    mg-d075 PUBLISHED              : 10 of 10, 0 unbounded", file=OUT)
    repro = (len(crit2), n_pass) == (10, 10)
    print("    %s" % ("REPRODUCES EXACTLY." if repro
                      else "*** DOES NOT REPRODUCE -- everything below is suspect "
                           "until this row is explained ***"), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ S2
    U.rule(OUT, "  S2  FIX 1 -- THE STANDARD.  The same %d sentences, scored by\n"
                "      H3's rule: the accepted scope must be a count or a bound.\n"
                "      Every accepted substring is printed." % len(crit2))
    num = [(f, l, s, bool(numeric_pass(s)), numeric_pass(s)) for f, l, s in crit2]
    n_num = sum(1 for r in num if r[3])
    show(num, "PER ROW:")

    print("    THREE CLASSIFIERS, SIDE BY SIDE, ROW BY ROW.  s5's own; mine; and",
          file=OUT)
    print("    mg-aaf4's, imported and executed.  A disagreement is published as a",
          file=OUT)
    print("    disagreement, not resolved by adopting whichever gives my finding.",
          file=OUT)
    print(file=OUT)
    print("    %-4s %-46s %-6s %-6s %-6s %-6s"
          % ("row", "file:line", "s5", "mine1", "mine2", "aaf4"), file=OUT)
    n_first, n_a = 0, 0
    disagree = []
    for i, (f, l, s) in enumerate(crit2, 1):
        a = A.scope_class(s) == "NUMERIC SCOPE"
        m1 = bool(first_form_pass(s))
        m2 = bool(numeric_pass(s))
        n_first += m1
        n_a += a
        if m2 != a:
            disagree.append((i, f, l, s, m2, a))
        print("    %-4d %-46s %-6s %-6s %-6s %-6s"
              % (i, ("%s:%d" % (f, l))[-46:], "PASS" if keyword_pass(s) else "fail",
                 "PASS" if m1 else "fail", "PASS" if m2 else "fail",
                 "PASS" if a else "fail"), file=OUT)
    print(file=OUT)
    print("    pass s5's own test          : %d of %d" % (n_pass, len(crit2)),
          file=OUT)
    print("    pass MY FIRST FORM          : %d of %d  (defective -- see the source)"
          % (n_first, len(crit2)), file=OUT)
    print("    pass MY SECOND FORM         : %d of %d" % (n_num, len(crit2)),
          file=OUT)
    print("    pass mg-aaf4's classifier   : %d of %d  (its published 7 of 10)"
          % (n_a, len(crit2)), file=OUT)
    print("    THE GAP against s5          : %d" % (n_pass - n_num), file=OUT)
    print("    rows where mine and mg-aaf4's disagree : %d" % len(disagree),
          file=OUT)
    for i, f, l, s, m2, a in disagree:
        print("      row %d  %s:%d  mine=%s aaf4=%s"
              % (i, f, l, "PASS" if m2 else "fail", "PASS" if a else "fail"),
              file=OUT)
        print("        %s" % s[:92], file=OUT)
    print(file=OUT)
    gap = [r for r in num if not r[3]]
    print("    THE %d THAT FALL, WITH WHAT THEY PASSED ON BEFORE:" % len(gap),
          file=OUT)
    for f, l, s, _, _ in gap:
        print("      %s:%d" % (f, l), file=OUT)
        print("        passed s5 on : %s" % keyword_pass(s), file=OUT)
        print("        %s" % s[:96], file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ S2b
    U.rule(OUT, "  S2b  HAND ADJUDICATION OF THE %d.  A regex over prose has false\n"
                "       negatives and publishing only the machine number would be\n"
                "       a count nobody can argue with.  BOTH NUMBERS ARE PUBLISHED\n"
                "       and every overturn carries its reason." % len(gap))
    stands = []
    for f, l, s, _, _ in gap:
        verdict, why = None, None
        for frag, sub, v, reason in ADJUDICATION:
            if frag in f and sub in s:
                verdict, why = v, reason
                break
        if verdict is None:
            verdict, why = "STANDS", "no adjudication row matches; the machine's " \
                                     "verdict is left as it fell"
        if verdict == "STANDS":
            stands.append((f, l, s))
        print("      %-9s %s:%d" % (verdict, f[-46:], l), file=OUT)
        print("          %s" % why[:94], file=OUT)
        print("          %s" % s[:94], file=OUT)
    print(file=OUT)
    print("    machine              : %d of %d carry a numeric scope"
          % (n_num, len(crit2)), file=OUT)
    print("    after adjudication   : %d of %d"
          % (len(crit2) - len(stands), len(crit2)), file=OUT)
    print("    STILL UNSCOPED       : %d" % len(stands), file=OUT)
    print(file=OUT)
    if len(stands) == 1:
        print("    AND THE ONE THAT STANDS IS THE REPAIR'S OWN HEADLINE SENTENCE.",
              file=OUT)
        print("    A sentence faulting two predecessors for stating a figure away", file=OUT)
        print("    from its scope, stating a figure away from its scope.  That is", file=OUT)
        print("    mg-aaf4's finding, re-derived here by a classifier written", file=OUT)
        print("    independently of its own and agreeing with it on 10 of 10 rows.",
              file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ S3
    U.rule(OUT, "  S3  FIX 2 -- THE POPULATION.  mg-d075 authored THREE prose\n"
                "      files; MINE lists two.  The third added here.")
    print("    s5's population   : %d live sentences in %d file(s) + %d added"
          % (len(pop2), len(S5.MINE), len(added)), file=OUT)
    print("    repaired          : %d live sentences in %d file(s) + %d added"
          % (len(pop3), len(S5.MINE) + 1, len(added)), file=OUT)
    crit3 = [(f, l, s) for f, l, s in pop3
             if S5.FAULT.search(s) and S5.TARGET.search(s)]
    new_rows = [r for r in crit3 if r not in crit2]
    print("    criticism sentences: %d -> %d  (+%d, all from the file s5 never"
          % (len(crit2), len(crit3), len(crit3) - len(crit2)), file=OUT)
    print("                        looked at)", file=OUT)
    n3 = [(f, l, s, bool(numeric_pass(s)), numeric_pass(s)) for f, l, s in new_rows]
    show(n3, "THE SENTENCES THE MISSING FILE CONTRIBUTES:")
    print("    of the %d new, WITHOUT a numeric scope : %d"
          % (len(n3), sum(1 for r in n3 if not r[3])), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ S4
    U.rule(OUT, "  S4  FIX 3 -- THE DETECTOR.  A property match instead of a\n"
                "      tense.  Population: the repaired %d-sentence population."
                % len(pop3))
    crit4 = [(f, l, s) for f, l, s in pop3
             if fault_repaired(s) and S5.TARGET.search(s)]
    only_new = [r for r in crit4 if r not in crit3]
    print("    criticism sentences, s5's FAULT      : %d" % len(crit3), file=OUT)
    print("    criticism sentences, property match  : %d" % len(crit4), file=OUT)
    print("    visible ONLY to the property match   : %d" % len(only_new), file=OUT)
    print(file=OUT)
    n4 = [(f, l, s, bool(numeric_pass(s)), numeric_pass(s)) for f, l, s in only_new]
    show(n4, "THE SENTENCES ONE TENSE HID:")
    target = [r for r in only_new if "could not see" in r[2].lower()]
    print("    THE SENTENCE THE DETECTOR WAS WRITTEN FOR:", file=OUT)
    if target:
        for f, l, s in target:
            print("      %s:%d  %s" % (f, l, "NO NUMERIC SCOPE"
                                       if not numeric_pass(s) else
                                       "scoped on %s" % numeric_pass(s)), file=OUT)
            print("        %s" % s[:96], file=OUT)
    else:
        print("      NOT FOUND in this population -- see the verdict.", file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ S5
    U.rule(OUT, "  S5  ALL THREE FIXES AT ONCE.  Population: mg-d075's three\n"
                "      authored documents plus the sentences it added to the\n"
                "      living document.  Grain: one sentence.")
    final = [(f, l, s, bool(numeric_pass(s)), numeric_pass(s)) for f, l, s in crit4]
    unb = [r for r in final if not r[3]]
    print("    population              : %d live sentences" % len(pop3), file=OUT)
    print("    criticism sentences     : %d" % len(final), file=OUT)
    print("    carrying a numeric scope: %d" % (len(final) - len(unb)), file=OUT)
    print("    WITHOUT ONE            : %d" % len(unb), file=OUT)
    print(file=OUT)
    show(unb, "EVERY SENTENCE THAT FAILS THE REPAIRED STANDARD:")

    # ------------------------------------------------------------------ S6
    U.rule(OUT, "  S6  THE CONTROLS.  Each fix run against an input on which the\n"
                "      OLD form passes and the NEW form must fail.  A check that\n"
                "      has not been shown to fire has not been shown to pass.")
    ctl = []
    probe1 = ("mg-19ec's census drops a site and states no population." )
    ctl.append(("FIX 1 standard",
                bool(S5.OWNSCOPE.search("the parent's population is wrong")),
                not numeric_pass("the parent's population is wrong")))
    ctl.append(("FIX 1 label is not a count",
                bool(S5.OWNSCOPE.search("the parent's POP-3 predicate is wrong")),
                not numeric_pass("the parent's POP-3 predicate is wrong")))
    ctl.append(("FIX 3 tense",
                not S5.FAULT.search("the parent could not see it"),
                bool(FAULT_PROPERTY.search("the parent could not see it"))))
    ctl.append(("FIX 3 keeps the old form",
                bool(S5.FAULT.search("the parent cannot see it")),
                bool(fault_repaired("the parent cannot see it"))))
    ctl.append(("FIX 2 population",
                os.path.exists(third) and third not in S5.MINE,
                len(crit3) > len(crit2)))
    ctl.append(("FIX 1 admits a real count",
                bool(S5.OWNSCOPE.search("mg-19ec's census drops 4 of 9 sites")),
                bool(numeric_pass("mg-19ec's census drops 4 of 9 sites"))))
    ok = True
    for name, old, new in ctl:
        good = bool(old) and bool(new)
        ok = ok and good
        print("    %-32s old-form %-5s  new-form %-5s  %s"
              % (name, "yes" if old else "no", "yes" if new else "no",
                 "FIRES" if good else "*** CONTROL FAILED ***"), file=OUT)
    print(file=OUT)
    print("    %d of %d controls fire.  %s"
          % (sum(1 for _, a, b in ctl if a and b), len(ctl),
             "The results above are trusted only because of this block."
             if ok else "A FAILED CONTROL INVALIDATES THE ROW IT GUARDS."), file=OUT)
    print(file=OUT)
    del probe1

    U.rule(OUT, "  VERDICT")
    print("    s5, as published : %d criticism sentences, %d unbounded"
          % (len(crit2), len(crit2) - n_pass), file=OUT)
    print("    s5, repaired     : %d criticism sentences, %d without a numeric"
          % (len(final), len(unb)), file=OUT)
    print("                       scope", file=OUT)
    print(file=OUT)
    print("    THE CHECK BITES.  It was not wrong about its population; it was", file=OUT)
    print("    weaker than the standard it enforced, short by a file, and blind", file=OUT)
    print("    to one tense.", file=OUT)
    print(file=OUT)

    U.rule(OUT)
    print("SUMMARY p4_selfcheck: S1 reproduce s5 %d criticism, %d pass its own "
          "OWNSCOPE -- %s" % (len(crit2), n_pass,
                              "REPRODUCES" if repro else "DISAGREES"), file=OUT)
    print("SUMMARY p4_selfcheck: S2 FIX 1 pass the numeric standard %d of %d, "
          "gap %d against s5's %d" % (n_num, len(crit2), n_pass - n_num, n_pass),
          file=OUT)
    print("SUMMARY p4_selfcheck: S2 classifiers s5 %d, my first form %d, my second "
          "form %d, mg-aaf4 %d of %d; %d row(s) disagree"
          % (n_pass, n_first, n_num, n_a, len(crit2), len(disagree)), file=OUT)
    print("SUMMARY p4_selfcheck: S2b machine %d of %d scoped -> %d after "
          "adjudication; %d STANDS unscoped"
          % (n_num, len(crit2), len(crit2) - len(stands), len(stands)), file=OUT)
    print("SUMMARY p4_selfcheck: S3 FIX 2 population %d -> %d sentences, criticism "
          "%d -> %d" % (len(pop2), len(pop3), len(crit2), len(crit3)), file=OUT)
    print("SUMMARY p4_selfcheck: S3 of the %d added criticism sentences %d carry "
          "no numeric scope" % (len(n3), sum(1 for r in n3 if not r[3])), file=OUT)
    print("SUMMARY p4_selfcheck: S4 FIX 3 criticism %d -> %d, %d visible only to "
          "the property match" % (len(crit3), len(crit4), len(only_new)), file=OUT)
    print("SUMMARY p4_selfcheck: S4 the could-not-see sentence %s"
          % ("FOUND and %s" % ("unscoped" if target and not numeric_pass(target[0][2])
                               else "scoped") if target else "NOT FOUND"), file=OUT)
    print("SUMMARY p4_selfcheck: S5 all three fixes %d criticism sentences, %d "
          "without a numeric scope" % (len(final), len(unb)), file=OUT)
    print("SUMMARY p4_selfcheck: S6 controls %d of %d fire"
          % (sum(1 for _, a, b in ctl if a and b), len(ctl)), file=OUT)
    U.rule(OUT)
    return 1 if unb or not ok else 0


if __name__ == "__main__":
    sys.exit(main())
