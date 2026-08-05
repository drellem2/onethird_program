"""A3 -- THE REPAIR READ AS A CLAIMANT, NOT AS DOCUMENTATION.

The brief, and this is the half it calls harder:

  "READ EVERY SENTENCE IN WHICH THE REPAIR FAULTS SOMEONE ELSE'S SCOPE FOR ITS
   OWN.  The parent faults Young-Fibonacci for naming no class while itself
   stating the YOUNG classification unbounded.  That is a specific self-
   application failure, and the ask is to check whether the repair does elsewhere
   what it criticises."

mg-d075 built `s5_own_criticism.py` for exactly this question and reported **10 of
10 criticism sentences carry their own scope, 0 unbounded**.  This script does not
dispute that arithmetic.  It disputes the STANDARD, and it disputes the POPULATION.

  THE STANDARD.  `s5`'s docstring says, in terms:

    "IT CARRIES ITS OWN SCOPE if the SAME sentence states the population or the
     grain of what it asserts: a numeric scope, a count with its denominator, a
     named file or predicate, or the words population / grain / live sentences /
     sites.  A neighbouring sentence does not rescue it -- THAT IS PRECISELY THE
     STANDARD THIS REPAIR APPLIED TO THE DOCUMENT, AND APPLYING A WEAKER ONE TO
     MYSELF WOULD BE THE DEFECT A SECOND TIME."

  The standard applied to the document is `s4_hedge.py`'s H3: every one of the ten
  sites is classified NUMERIC SCOPE or SOFTENING WORD, and only a NUMERIC SCOPE
  passes.  The standard `s5` applies to the repair's own sentences additionally
  accepts the bare words `population`, `grain`, `live sentences`, the tokens
  `STRICT`, `RELAXED`, `POP-<n>`, and a bare path `code/...`.  None of those is a
  numeric scope.  C2 measures the gap between the two standards on the parent's own
  ten sentences.

  THE POPULATION.  `s5`'s `MINE` is two files.  mg-d075 authored three prose
  documents; `PREDICTIONS.md` is not in `MINE`.  C3 runs the parent's OWN
  criticism predicate over the omitted file.

  AND MYSELF.  C4 turns the same predicate on this audit's own prose.  mg-d075
  predicted it would commit the defect it was repairing and it was right.  I
  predict the same of myself in `PREDICTIONS.md` P10.

EXIT 1 if any criticism sentence -- the parent's or mine -- carries no NUMERIC
scope of its own.  PREDICTED 1 on the first run AND 1 at the end (P10): I cannot
edit mg-d075's merged prose, so a check that gates on it cannot be turned green
without editing the thing under audit, and a check I could turn green that way
would not be an audit.
"""

import os
import re
import subprocess
import sys

import lib_aaf4 as L

OUT = sys.stdout
TMP = os.path.join(L.HERE, ".a3_tmp")
REL = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"

PARENT_MINE = [os.path.join(L.PARENT, "README.md"),
               os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md")]
PARENT_OMITTED = [os.path.join(L.PARENT, "PREDICTIONS.md")]
MY_PROSE = [os.path.join(L.HERE, "PREDICTIONS.md"),
            os.path.join(L.HERE, "README.md")]

# --------------------------------------------------------------------------
# The parent's own predicate, TRANSCRIBED from `s5_own_criticism.py` as read --
# not imported, and not paraphrased.  Every alternative below is checked to be
# literally present in the parent's source before it is used (block C0), so a
# mis-transcription cannot become a finding.
PARENT_FAULT_SRC = [
    r"\bmisses\b", r"\bmissed\b", r"cannot see", r"\bdrops\b", r"\bdropped\b",
    r"\bunbounded\b", r"\bdisagree", r"\bdefect\b", r"\bfails\b", r"\bfailed\b",
    r"\bblind\b", r"under-collect", r"over-collect", r"\bhollow\b", r"\btautolog",
    r"too narrow", r"too wide", r"\bwrong\b", r"no instrument computes",
    r"\bnot the population\b", r"\bnever computes\b", r"\bdoes not carry\b",
    r"\bno bound\b", r"\binvalid\b", r"\bartefact\b",
]
PARENT_TARGET_SRC = [
    r"\bmg-(?!d075)[0-9a-f]{4}\b", r"the parent\b", r"the predecessor\b",
    r"the census\b", r"the instrument\b", r"its own instrument",
    r"the published audit",
]
PARENT_OWNSCOPE_SRC = [
    r"\bpopulation\b", r"\bgrain\b", r"live sentences?\b",
    r"\b\d+ of (?:the )?\d+\b", r"\b\d+ sites?\b", r"\b\d+ sentences?\b",
    r"\b\d+ tokens?\b", r"\b\d+ occurrences?\b",
    r"rank\s*\(?w?\)?\s*(?:≤|<=)\s*\d", r"to rank \d", r"`?n`?\s*(?:≤|<=)\s*\d",
    r"code/[a-z0-9_]+", r"docs/[A-Za-z0-9_.\-]+", r"out_[a-z0-9_]+\.txt",
    r"\b\d+ (?:files?|rows?|cells?|figures?|commits?|intervals?|phrasings?)\b",
    r"STRICT", r"RELAXED", r"POP-\d", r"\b\d+ -> \d+\b", r"\b\d+/\d+\b",
]

PARENT_FAULT = re.compile("|".join(PARENT_FAULT_SRC), re.I)
PARENT_TARGET = re.compile("|".join(PARENT_TARGET_SRC), re.I)
PARENT_OWNSCOPE = re.compile("|".join(PARENT_OWNSCOPE_SRC), re.I)

# My own, wider, fault predicate.  The parent's regex says `cannot see` and the
# parent's own prose says `could not see`; a detector that misses the tense of the
# sentence it was written for is the shape of defect this arc collects.
MY_FAULT = re.compile(
    PARENT_FAULT.pattern +
    r"|could not see|can(?:not|'t) tell|\bomits?\b|\bomitted\b|\bsilent(?:ly)?\b"
    r"|\bshort by\b|hand-written literal|\bfired on\b|\bloosen"
    r"|\bnever (?:prints|spells|computes|says)\b|\bno list\b|\bmis-?scoped\b"
    r"|\bunder(?:count|state)|\bstale\b|\bdid not\b|\bdoes not\b|\bcould have\b"
    r"|\bnot (?:evidence|proof|new evidence)\b|\bdestroy\b|\bnobody\b", re.I)
MY_TARGET = re.compile(
    r"\bmg-(?!aaf4)[0-9a-f]{4}\b|the parent\b|the predecessor\b|the census\b"
    r"|the instrument\b|its own instrument|the published audit|that audit\b"
    r"|the repair\b|the arc\b|this lineage\b|\bPOP-\d\b|\bs\d_[a-z_]+\.py\b", re.I)


# THE HAND ADJUDICATION.  Written against the sentences, keyed on a distinctive
# substring so that a sentence which moves invalidates its own adjudication rather
# than silently keeping a verdict that was made about different words.  mg-19ec's
# own census says it plainly: "This is a CENSUS, not a verdict ... the deliverable
# adjudicates every site above by hand."  A classifier over prose over-collects in
# both directions and the honest thing is to print both numbers.
ADJUDICATION = [
    ("The POP-1 block of the same transcript", "SCOPE",
     "FALSE NEGATIVE OF MY CLASSIFIER.  The sentence names the transcript file "
     "AND the row index [09] inside it.  That is a fully determinate scope -- "
     "narrower than a count -- and it is not numeric only because it identifies "
     "one object rather than counting a population."),
    ("The brief for this repair told me not to inherit 8", "NO SCOPE",
     "STANDS.  'FOUR was not the population, and EIGHT is not either' asserts of "
     "two published figures that they are not the population, and names in its "
     "own sentence neither the population, nor the file, nor the grain.  The "
     "table two lines above it carries all three.  This is the same shape as the "
     "defect it is announcing: the figure here, the scope over there."),
    ("Counted over the live sentences of this file at the grain", "SCOPE",
     "FALSE NEGATIVE OF MY CLASSIFIER.  The sentence names the file, names the "
     "grain, and states 9 and 5 -- it carries more scope than most sentences my "
     "regex passes.  It fails only because the numerals appear as 'were 9' and "
     "'of which 5' rather than as '9 sites'."),
]


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT,
                          capture_output=True, text=True).stdout


def added_sentences():
    """The sentences mg-d075 added to the living document -- re-derived."""
    for row in git("log", "--format=%H\t%s", "--", REL).strip().split("\n"):
        h, _, subj = row.partition("\t")
        if "mg-d075" not in subj:
            break
    os.makedirs(TMP, exist_ok=True)
    p = os.path.join(TMP, "base.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (h, REL)))
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    old = {norm(s) for _, _, s, _ in L.live_sentences(p)}
    return [(REL, a, norm(s)) for a, _, s, _ in L.live_sentences(L.DOC)
            if norm(s) not in old]


def pop_of(paths):
    out = []
    for path in paths:
        if not os.path.exists(path):
            continue
        out += [(L.rel(path), l, re.sub(r"\s+", " ", s).strip())
                for l, _, s, _ in L.live_sentences(path)]
    return out


def show(rows, out, label_std):
    for i, (f, l, s, cls, ptxt, ntxt) in enumerate(rows, 1):
        print("    [%02d] %-46s line %-4d %s"
              % (i, os.path.basename(f)[:46], l, cls), file=out)
        if ptxt:
            print("         parent's OWNSCOPE matched : %r" % ptxt, file=out)
        print("         %-25s : %s" % (label_std, ntxt or "-- NONE --"), file=out)
        print("         ", end="", file=out)
        L.wrap(out, s, 100, 9)
        print(file=out)


def classify(pop, fault, target):
    rows = []
    for f, l, s in pop:
        if not (fault.search(s) and target.search(s)):
            continue
        cls = L.scope_class(s)
        pm = PARENT_OWNSCOPE.search(s)
        rows.append((f, l, s, cls, pm.group(0) if pm else "",
                     L.numeric_scope_text(s)))
    return rows


def main():
    L.rule(OUT, "A3  THE REPAIR READ AS A CLAIMANT.  Every sentence in which\n"
                "    mg-d075 faults someone else's scope, checked for its own\n"
                "    -- against the standard mg-d075 applied to the DOCUMENT,\n"
                "    not the one it applied to itself.")
    print(file=OUT)
    fails = 0

    # ---------------------------------------------------------------- C0
    L.rule(OUT, "  C0  THE TRANSCRIPTION, CHECKED.  Every alternative of the\n"
                "      parent's three regexes is asserted present in the\n"
                "      parent's own source before it is used against it.")
    src = open(os.path.join(L.PARENT, "s5_own_criticism.py"),
               encoding="utf-8").read()
    missing = [a for a in PARENT_FAULT_SRC + PARENT_TARGET_SRC + PARENT_OWNSCOPE_SRC
               if a not in src]
    print("    alternatives transcribed : %d"
          % len(PARENT_FAULT_SRC + PARENT_TARGET_SRC + PARENT_OWNSCOPE_SRC),
          file=OUT)
    print("    not found in the source  : %d" % len(missing), file=OUT)
    for a in missing:
        print("      MISSING %r" % a, file=OUT)
    if missing:
        fails += 1
    print(file=OUT)

    # ---------------------------------------------------------------- C1
    L.rule(OUT, "  C1  THE PARENT'S OWN RESULT, REPRODUCED FIRST.\n"
                "      Population: `MINE` (2 files) + the sentences mg-d075\n"
                "      added to the living document.  Grain: one sentence.")
    add = added_sentences()
    pop = pop_of(PARENT_MINE) + [(REL, l, s) for _, l, s in add]
    parent_rows = classify(pop, PARENT_FAULT, PARENT_TARGET)
    parent_unb = [r for r in parent_rows if not PARENT_OWNSCOPE.search(r[2])]
    print("    population, my reader                    : %d live sentences"
          % len(pop), file=OUT)
    print("    sentences mg-d075 added to the living doc: %d" % len(add), file=OUT)
    print("    criticism sentences (parent's predicate) : %d" % len(parent_rows),
          file=OUT)
    print("    unbounded by the PARENT'S OWN OWNSCOPE   : %d" % len(parent_unb),
          file=OUT)
    print("    mg-d075 published                        : 10 of 254, 0 unbounded",
          file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- C2
    L.rule(OUT, "  C2  THE SAME SENTENCES, SCORED BY THE STANDARD mg-d075\n"
                "      APPLIED TO THE DOCUMENT.  H3's separation: a NUMERIC\n"
                "      SCOPE passes, a keyword does not.")
    kw = [r for r in parent_rows if r[3] != "NUMERIC SCOPE"]
    show(parent_rows, OUT, "NUMERIC scope in sentence")
    print("    criticism sentences                              : %d"
          % len(parent_rows), file=OUT)
    print("    pass the parent's OWNSCOPE (keywords allowed)    : %d"
          % (len(parent_rows) - len(parent_unb)), file=OUT)
    print("    pass H3's standard (a NUMERIC scope in sentence) : %d"
          % (len(parent_rows) - len(kw)), file=OUT)
    print("    THE GAP -- pass as itself, fail as the document  : %d"
          % len(kw), file=OUT)
    print(file=OUT)
    # --------------------------------------------------- C2b, the adjudication
    L.rule(OUT, "  C2b  THE ADJUDICATION.  A classifier over prose is not a\n"
                "       verdict.  Every KEYWORD-ONLY row above is adjudicated\n"
                "       BY HAND here, with the reason, and both numbers are\n"
                "       published -- the machine's and the adjudicated one.")
    verdicts = 0
    for key, verdict, reason in ADJUDICATION:
        hits = [r for r in parent_rows if key in r[2]]
        if len(hits) != 1:
            print("    KEY NOT UNIQUE (%d hits): %r -- the sentence moved and this"
                  % (len(hits), key), file=OUT)
            print("    adjudication no longer applies to it.", file=OUT)
            fails += 1
            continue
        r = hits[0]
        print("    %-46s line %-4d machine=%-13s hand=%s"
              % (os.path.basename(r[0])[:46], r[1], r[3], verdict), file=OUT)
        print("      ", end="", file=OUT)
        L.wrap(OUT, reason, 100, 6)
        if verdict == "NO SCOPE":
            verdicts += 1
        print(file=OUT)
    adj_kw = [r for r in parent_rows if r[3] != "NUMERIC SCOPE"]
    print("    machine: %d of %d criticism sentences carry no NUMERIC scope"
          % (len(adj_kw), len(parent_rows)), file=OUT)
    print("    hand   : %d of %d carry no scope of ANY determinate kind"
          % (verdicts, len(parent_rows)), file=OUT)
    print(file=OUT)

    print("""    THE FINDING.  `s5`'s docstring states that applying a weaker
    standard to itself "would be the defect a second time".  The standard it
    applies to itself accepts the bare word `population` where the standard it
    applies to the document requires `rank(w) <= 6`.  The sentences above marked
    KEYWORD ONLY are the ones that separate the two.  This is not an arithmetic
    error in mg-d075 -- its 10 of 10 is correct FOR ITS OWN REGEX.  It is the
    regex that is weaker than the sentence describing it says it is.""",
          file=OUT)
    print(file=OUT)
    if kw:
        fails += 1

    # ---------------------------------------------------------------- C3
    L.rule(OUT, "  C3  THE OMITTED FILE.  mg-d075 authored 3 prose documents;\n"
                "      `s5`'s MINE lists 2.  This is the third, run through\n"
                "      the parent's OWN criticism predicate.")
    omitted = pop_of(PARENT_OMITTED)
    orows = classify(omitted, PARENT_FAULT, PARENT_TARGET)
    okw = [r for r in orows if r[3] != "NUMERIC SCOPE"]
    ounb = [r for r in orows if not PARENT_OWNSCOPE.search(r[2])]
    print("    file                                     : %s"
          % L.rel(PARENT_OMITTED[0]), file=OUT)
    print("    live sentences, my reader                : %d" % len(omitted),
          file=OUT)
    print("    criticism sentences, PARENT'S predicate  : %d" % len(orows), file=OUT)
    print("    of those, unbounded by PARENT'S OWNSCOPE : %d" % len(ounb), file=OUT)
    print("    of those, no NUMERIC scope (H3 standard) : %d" % len(okw), file=OUT)
    print(file=OUT)
    show(orows, OUT, "NUMERIC scope in sentence")
    print("""    The parent's self-check population was short by one authored
    document, and the omitted document is not empty of the thing being counted.
    Whether any of these is a defect is an adjudication; that they were never
    looked at is not.""", file=OUT)
    print(file=OUT)
    if okw:
        fails += 1

    # ---------------------------------------------------------------- C4
    L.rule(OUT, "  C4  MYSELF.  The same predicate, widened, turned on this\n"
                "      audit's own prose.  PREDICTIONS.md P10 says in advance\n"
                "      that it fires on me.")
    minepop = pop_of(MY_PROSE)
    mrows = classify(minepop, MY_FAULT, MY_TARGET)
    mkw = [r for r in mrows if r[3] != "NUMERIC SCOPE"]
    print("    population : %d live sentences of mine" % len(minepop), file=OUT)
    print("    criticism sentences, MY wider predicate  : %d" % len(mrows), file=OUT)
    print("    of those with NO numeric scope of my own : %d" % len(mkw), file=OUT)
    print(file=OUT)
    show(mkw, OUT, "NUMERIC scope in sentence")
    if mkw:
        fails += 1
    print("""    I DO NOT REPAIR THE ONES IN `PREDICTIONS.md`.  It is a
    pre-registration commit and this lineage does not reword those.  Ones in my
    README are mine to fix and are fixed where fixing them does not turn a
    finding into a slogan; the residue is printed above rather than deleted.""",
          file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- C5
    L.rule(OUT, "  C5  THE WIDER PREDICATE OVER THE PARENT'S SENTENCES.\n"
                "      What the parent's own FAULT regex cannot see.")
    wrows = classify(pop + omitted, MY_FAULT, MY_TARGET)
    seen = {(r[0], r[1], r[2]) for r in parent_rows + orows}
    extra = [r for r in wrows if (r[0], r[1], r[2]) not in seen]
    extra_kw = [r for r in extra if r[3] != "NUMERIC SCOPE"]
    print("    criticism sentences, PARENT'S predicate  : %d"
          % len(parent_rows + orows), file=OUT)
    print("    criticism sentences, MY predicate        : %d" % len(wrows), file=OUT)
    print("    seen only by mine                        : %d" % len(extra), file=OUT)
    print("    of those, no NUMERIC scope               : %d" % len(extra_kw),
          file=OUT)
    print(file=OUT)
    print("    A worked example the parent's own regex misses by ONE TENSE:",
          file=OUT)
    tense = [r for r in extra if "could not see" in r[2]]
    show(tense[:2], OUT, "NUMERIC scope in sentence")
    print("      `FAULT` in `s5_own_criticism.py` contains `cannot see`; the",
          file=OUT)
    print("      parent's own account says `could not see`.  Present : %s"
          % ("cannot see" in open(os.path.join(
              L.PARENT, "s5_own_criticism.py"), encoding="utf-8").read()), file=OUT)
    print(file=OUT)

    if os.path.isdir(TMP):
        for f in os.listdir(TMP):
            os.remove(os.path.join(TMP, f))
        os.rmdir(TMP)

    L.rule(OUT)
    print("SUMMARY a3_criticism: C1 parent population %d sentences, %d criticism, "
          "%d unbounded by the parent's own OWNSCOPE"
          % (len(pop), len(parent_rows), len(parent_unb)), file=OUT)
    print("SUMMARY a3_criticism: C2 %d of %d parent criticism sentences pass as "
          "themselves and FAIL the standard applied to the document"
          % (len(kw), len(parent_rows)), file=OUT)
    print("SUMMARY a3_criticism: C3 omitted file %s: %d criticism sentence(s), "
          "%d with no numeric scope"
          % (os.path.basename(PARENT_OMITTED[0]), len(orows), len(okw)), file=OUT)
    print("SUMMARY a3_criticism: C4 MY OWN prose: %d criticism sentence(s), "
          "%d with no numeric scope of my own" % (len(mrows), len(mkw)), file=OUT)
    print("SUMMARY a3_criticism: C5 my predicate sees %d sentence(s) the parent's "
          "cannot" % len(extra), file=OUT)
    print("SUMMARY a3_criticism: failures %d" % fails, file=OUT)
    L.rule(OUT)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
