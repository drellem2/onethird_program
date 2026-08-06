"""mg-03d1 / A1 -- HOW MANY GRAIN AXES IS THE SIXTH INSTRUMENT BLIND TO?

TARGET 1 of the addendum, and the deliverable of this audit.

The parent established that `rows` and `sites` are the same word to
`lib56dc._classify`.  The addendum asks the question the parent did not:
SITE-vs-EXECUTION is ONE distinction -- how many others occur in this corpus,
and which of them can the classifier express?

The answer this probe argues for, and prints the working of, is that the
question "which words is it missing" is the wrong question.  `_classify` is
built from TWO boolean membership tests and returns FOUR symbols.  Its
resolution is a property of its ARITY, not of its VOCABULARY, so no word list
repairs it -- and the popular fix (add `rows` to a new ROW_WORDS) repairs
exactly one defect's width again, which is what the addendum warns against.

Exit code = number of A1a rows that classify other than as pre-registered.
"""

import itertools
import re
import sys

import lib03d1 as B

BAD = 0
A = B.A

print("mg-03d1 / A1 -- THE CLASSIFIER'S AXES")
print("Subject: `lib56dc._classify`, the sixth instrument the brief sent me to")
print("run.  Repository HEAD: %s" % B.head())

# ---------------------------------------------------------------------------
B.hdr("A1a  THE RESOLUTION GAP, CONFIRMED BY RUNNING IT AND NOT BY READING IT")

print("  The addendum asks me to put `rows` and `basenames` to `_classify`")
print("  myself rather than take the parent's word.  Done here.  PREDICTED in")
print("  PREDICTIONS.md/A1a before this file existed: 12 of 12 as listed.")
print()
EXPECT = [("rows", "SITE"), ("basenames", "SITE"), ("sites", "SITE"),
          ("lines", "SITE"), ("files", "SITE"), ("items", "SITE"),
          ("members", "SITE"), ("columns", "SITE"),
          ("executions", "EXECUTION"), ("runs", "EXECUTION"),
          ("invocations", "EXECUTION"), ("iterations", "EXECUTION")]
agree = 0
for w, want in EXPECT:
    got = A._classify(w)
    ok = got == want
    agree += ok
    print("      `%-12s`  ->  %-9s   pre-registered %-9s  %s"
          % (w, got, want, "" if ok else "*** NOT AS PRE-REGISTERED"))
BAD += len(EXPECT) - agree
print()
print("  population: the 12 probe WORDS listed in PREDICTIONS.md/A1a")
B.plain("...probe WORDS classifying as pre-registered", agree)
print("      ^ one unit of that number is one probe word")
print()
print("  SO: `rows`, `basenames` and `sites` are ONE SYMBOL to this instrument.")
print("  A count labelled `sites` holding a ROW value is, to it, a row with the")
print("  right grain word on it.  IT PASSES.  Confirmed by running it.")

# ---------------------------------------------------------------------------
B.hdr("A1b  AND THE LIMIT IS THE ARITY, NOT THE VOCABULARY")

print("  `_classify` is four lines long and its whole body is:")
print()
print("      e = bool(EXEC_WORDS.search(text));  s = bool(SITE_WORDS.search(text))")
print("      BOTH if e and s;  EXECUTION if e;  SITE if s;  else NONE")
print()
print("  TWO independent boolean tests, so the function's image has at most")
print("  four members and it partitions every possible label into at most four")
print("  cells.  A partition into four cells can express exactly ONE binary")
print("  distinction plus the two degenerate cells (`BOTH`, `NONE`).")
print()
seen = set()
for probe in ("rows", "runs", "runs of rows", "poset", ""):
    seen.add(A._classify(probe))
print("  population: probe STRINGS chosen to reach every arm of the function")
B.plain("distinct output WORDS `_classify` can return", len(seen))
print("      ^ one unit of that number is one output symbol")
B.plain("...boolean CHECKS the body performs", 2)
print("      ^ one unit of that number is one regex membership test")
print()
print("  THIS IS THE FINDING.  The gap is not that `rows` is missing from some")
print("  list -- `rows` is PRESENT, and that is the problem.  No addition to")
print("  either word list can make `rows` and `sites` different, because the")
print("  function has nowhere to put the difference.  A fix that adds a third")
print("  vocabulary buys exactly one more axis and is the same shape of repair")
print("  that produced this defect: one defect's width.")

# ---------------------------------------------------------------------------
B.hdr("A1c  THE COLLAPSE, COUNTED OVER THE CLASSIFIER'S OWN VOCABULARY")


def render(alt):
    """One regex alternative rendered as a probe STRING a human can read."""
    s = alt.replace(r"\b", "")
    s = s.replace("s?", "s").replace(" ?", " ")
    return s


SITE_V = [render(a) for a in A.SITE_WORDS.pattern.split("|")]
EXEC_V = [render(a) for a in A.EXEC_WORDS.pattern.split("|")]
print("  Every alternative of both vocabularies, rendered as a probe string and")
print("  put back through the classifier.  Printed in full so that the ratio")
print("  below is checkable rather than assertable:")
print()
for i in range(0, max(len(SITE_V), len(EXEC_V)), 3):
    print("      " + "  ".join("%-22s" % ("`%s`=%s" % (w, A._classify(w)))
                               for w in SITE_V[i:i + 3]))
print()
for w in EXEC_V:
    print("      `%-16s` = %s" % (w, A._classify(w)))
print()
nS, nE = len(SITE_V), len(EXEC_V)
tot = (nS + nE) * (nS + nE - 1) // 2
cross = nS * nE
within = tot - cross
print("  population: the %d vocabulary WORDS of the classifier itself, taken"
      % (nS + nE))
print("  as unordered pairs")
B.plain("...vocabulary WORDS in SITE_WORDS", nS)
print("      ^ one unit of that number is one regex alternative")
B.plain("...vocabulary WORDS in EXEC_WORDS", nE)
print("      ^ one unit of that number is one regex alternative")
B.plain("...unordered PAIRS over those words", tot)
print("      ^ one unit of that number is one pair of vocabulary words")
B.plain("...PAIRS of those WORDS it tells apart (cross-list)", cross)
print("      ^ one unit of that number is one pair of vocabulary words")
B.plain("...PAIRS of those WORDS it collapses (within-list)", within)
print("      ^ one unit of that number is one pair of vocabulary words")
print()
print("  `rows`/`sites` is one of those %d collapsed pairs.  O1 is one member"
      % within)
print("  of a class with %d members, and a fix aimed at the member is aimed at"
      % within)
print("  the wrong thing.")

# ---------------------------------------------------------------------------
B.hdr("A1d  AND THE COLLAPSE OVER THE GRAIN WORDS THAT ACTUALLY OCCUR")

print("  The vocabulary is the classifier's own.  This is the corpus's.  Every")
print("  count row of every `code/*/out_*.txt` on disk, its label's grain word")
print("  extracted by SHAPE (last content word, plus the word before an")
print("  `of`/`in`/`per`) rather than from a hand list -- a hand list of")
print("  interesting nouns is how this check would become what it audits.")
print()
paths = B.all_transcripts()
nouns = {}
rows_seen = 0
for p in paths:
    try:
        txt = B.read(p)
    except OSError:
        continue
    for _i, label, _n in A.count_rows(txt):
        rows_seen += 1
        for w in B.grain_nouns(label):
            nouns.setdefault(B.singular(w), set()).add(w)
print("  population: every count ROW of every `code/*/out_*.txt` on disk")
B.plain("...ARTIFACTS in that corpus", len(paths))
print("      ^ one unit of that number is one transcript file")
B.plain("...count ROWS in them", rows_seen)
print("      ^ one unit of that number is one printed line")
B.plain("...distinct grain WORDS extracted from their labels", len(nouns))
print("      ^ one unit of that number is one de-pluralised noun")
print()
cls = {}
for n in nouns:
    cls.setdefault(A._classify(n), []).append(n)
for k in ("SITE", "EXECUTION", "BOTH", "NONE"):
    B.plain("...of those grain WORDS classifying %-9s" % k, len(cls.get(k, [])))
print("      ^ one unit of each of those numbers is one de-pluralised noun")
N = len(nouns)
pairs = N * (N - 1) // 2
tell = sum(len(a) * len(b) for a, b in itertools.combinations(
    [v for v in cls.values()], 2))
B.plain("...unordered PAIRS of grain words in the corpus", pairs)
print("      ^ one unit of that number is one pair of corpus grain words")
B.plain("...PAIRS of grain WORDS it can tell apart", tell)
print("      ^ one unit of that number is one pair of corpus grain words")
B.plain("...PAIRS of grain WORDS it collapses", pairs - tell)
print("      ^ one unit of that number is one pair of corpus grain words")
pct = 100.0 * (pairs - tell) / pairs if pairs else 0.0
print()
print("      collapse rate over the corpus's own grain words:   %.1f%%" % pct)
print()
print("  AND THE STRICTER READING, printed because the pre-registered metric")
print("  above is the GENEROUS one and saying so is cheaper than defending it.")
print("  `NONE` is not a grain -- it is `I have no word for this label`.  A")
print("  SITE/NONE pair is not a distinction the classifier DREW, it is one")
print("  side of it going unanswered.  Counting only pairs where BOTH poles got")
print("  a grain symbol:")
print()
gen = sum(len(cls.get(k, [])) for k in ("SITE", "EXECUTION", "BOTH"))
gpairs = gen * (gen - 1) // 2
gtell = len(cls.get("SITE", [])) * len(cls.get("EXECUTION", []))
print("  population: the %d corpus grain WORDS the classifier has an entry for"
      % gen)
B.plain("...unordered PAIRS over those grain words", gpairs)
print("      ^ one unit of that number is one pair of corpus grain words")
B.plain("...PAIRS of grain WORDS it genuinely tells apart", gtell)
print("      ^ one unit of that number is one pair of corpus grain words")
gpct = 100.0 * (gpairs - gtell) / gpairs if gpairs else 0.0
print("      collapse rate on the words it can speak about:     %.1f%%" % gpct)
print()
print("  AND THE CELL THAT MATTERS MOST IS `NONE`: %d of the %d grain words"
      % (len(cls.get("NONE", [])), N))
print("  this corpus actually uses are words the classifier HAS NO ENTRY FOR.")
print("  For those, `grain_of` walks to `prev` and then to `header` looking for")
print("  a word it does know -- so a label with an unknown grain noun is")
print("  answered by a DIFFERENT LINE's grain word, and reported at a stage")
print("  that says so.  The stage is the honest part of that design.")
print()
print("  A sample of 40 of the `NONE` grain words, alphabetically, so the")
print("  number above is checkable:")
print()
none_w = sorted(cls.get("NONE", []))
for i in range(0, min(40, len(none_w)), 6):
    print("      " + "  ".join("%-11s" % w for w in none_w[i:i + 6]))

# ---------------------------------------------------------------------------
B.hdr("A1e  THE SIX AXES THIS CORPUS ACTUALLY DISTINGUISHES")

print("  Pre-registered in PREDICTIONS.md/A1e.  For each axis: both poles put")
print("  to `_classify`, and the verdict is whether the two symbols DIFFER.")
print("  Where they do not, the classifier cannot express that axis at all.")
print()
AXES = [
    ("row / site", "rows", "sites",
     "O1 itself: 14 (site,target) rows behind 12 source lines"),
    ("file / line", "files", "lines",
     "`806 deletion rows` vs the files they fall in -- mg-d53d's arc"),
    ("item / class", "items", "species",
     "mg-4adb's species vs its rungs"),
    ("pair / poset", "pairs", "poset",
     "mg-0ba7's `0 crossings over 10 ordered tree pairs`"),
    ("occurrence / name", "mentions", "names",
     "mg-bf79's own P3c: a MENTION is still COUNTED"),
    ("site / execution", "sites", "executions",
     "F1, the one axis the instrument was built for"),
]
express = 0
for name, a, b, why in AXES:
    ca, cb = A._classify(a), A._classify(b)
    ok = ca != cb
    express += ok
    print("      %-18s `%-10s`=%-9s  `%-10s`=%-9s  -> %s"
          % (name, a, ca, b, cb, "EXPRESSIBLE" if ok else "*** COLLAPSED"))
    print("          occurs as: %s" % why)
print()
print("  population: the 6 named grain AXES of PREDICTIONS.md/A1e")
B.plain("...AXES of grain WORDS it can express", express)
print("      ^ one unit of that number is one axis")
B.plain("...AXES of grain WORDS it collapses", len(AXES) - express)
print("      ^ one unit of that number is one axis")
print()
print("  I PRE-REGISTERED 1 OF 6 AND THE PROBE SAYS 3.  That is a MISS and it")
print("  stays a miss.  The reason is worth more than the row: two of the three")
print("  `EXPRESSIBLE` axes are expressible only because ONE POLE CLASSIFIES")
print("  `NONE` -- `species` and `names` are not words the instrument knows.")
print("  What it distinguished there was HAS-A-GRAIN-WORD from HAS-NONE, which")
print("  is not the axis I named.  Counted that way:")
print()
genuine = sum(1 for _n, a, b, _w in AXES
              if A._classify(a) != A._classify(b)
              and "NONE" not in (A._classify(a), A._classify(b)))
B.plain("...AXES separated by two known grain WORDS", genuine)
print("      ^ one unit of that number is one axis")
print()
print("  THAT REFINEMENT IS POST HOC AND DOES NOT RESCUE A1e.  The figure I")
print("  pre-registered was 1 against the metric I pre-registered, and that")
print("  metric gives 3.  Both numbers are printed above.")
print()
print("  THE THREE IT COLLAPSES ALL COLLAPSE THE SAME WAY: both poles land in")
print("  SITE_WORDS, or both land in NONE, and every one of them is a")
print("  same-cell distinction of exactly O1's kind.  O1 was not a gap in a")
print("  word list; it was a sample from a class.")

# ---------------------------------------------------------------------------
B.hdr("A1f  AND ONE AXIS IT REPORTS THAT IS NOT THERE")

print("  The blind spot has a mirror, and it is the prediction I most expected")
print("  to be refuted: a pair of words at the SAME grain, split across the two")
print("  vocabularies, so the classifier asserts a distinction the words do not")
print("  carry.  ADJUDICATED BY HAND, with the reasoning printed so a reader")
print("  can reject any row -- there is no mechanical test for `same grain`,")
print("  and pretending there is would be this arc's own defect.")
print()
CAND = [
    ("steps", "iterations", True,
     "a loop's steps ARE its iterations; `6 steps` and `6 iterations` of the "
     "same loop are one number"),
    ("commands", "invocations", True,
     "`3 commands issued` and `3 invocations` count the same events"),
    ("runners", "runs", False,
     "a runner is a FILE and a run is an EVENT -- correctly split"),
    ("scripts", "executions", False,
     "a script is a file; an execution is an event -- correctly split"),
    ("checks", "iterations", False,
     "a check is written once and may iterate -- correctly split"),
]
straddle = 0
for a, b, same, why in CAND:
    ca, cb = A._classify(a), A._classify(b)
    hit = same and ca != cb
    straddle += hit
    print("      `%-10s`=%-9s vs `%-12s`=%-9s  same grain: %-3s  %s"
          % (a, ca, b, cb, "yes" if same else "no",
             "*** FALSE DISTINCTION" if hit else ""))
    print("          %s" % why)
print()
print("  population: the 5 candidate WORD pairs adjudicated above")
B.plain("...PAIRS asserting a distinction not in the words", straddle)
print("      ^ one unit of that number is one adjudicated word pair")
print()
print("  So the instrument is not merely coarse in one direction.  It collapses")
print("  %d of the %d pairs its own vocabulary can form AND splits at least %d"
      % (within, tot, straddle))
print("  pairs that are one grain.  Both errors are invisible to a check that")
print("  only asks `does the label carry a grain word`.")

print()
print("A1 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
