"""mg-9160 / S4 -- THE OPEN SET, ITS PRICE, AND THE VALUE NO ARITY CARRIES.

My ticket offers two exits:

    Either the classifier returns a grain from an open set, or it is honest
    about what it cannot express and REPORTS the 370 rather than silently
    returning NONE.

This probe builds the first, measures what it costs, and then argues that
NEITHER exit is the repair -- because both are TOTAL functions answering a
question about the world that nobody has answered.

  S4a  the open-set classifier over the corpus: no NONE, and the failure names
       the label instead of returning a symbol that means `no`.
  S4b  ITS PRICE, PREDICTED BEFORE IT EXISTED (P4).  An open value set splits
       every synonym pair there is, including both pairs A1f adjudicated SAME.
  S4c  THE SCOREBOARD, on the only 11 pairs this arc has ever adjudicated.
  S4d  the THIRD VERDICT, and why no number of symbols can carry it.

Exit code = number of S4 checks that fail.
"""

import sys
import textwrap
from itertools import combinations

import lib9160 as G

C = G.convention()       # mg-2ff6 -- the dated-population convention

BAD = 0
A = G.A

G.bar("mg-9160 / S4 -- THE OPEN SET AND ITS PRICE")
print("HEAD: %s" % G.head())

CORPUS = G.parent_corpus()

# ---------------------------------------------------------------------------
G.hdr("S4a  THE OPEN-SET CLASSIFIER OVER THE CORPUS")

words = {}
nonoun = 0
rows = 0
for p, r in CORPUS:
    t = G.read(p, r)
    if t is None:
        continue
    for _i, label, _n in A.count_rows(t):
        rows += 1
        kind, val = G.grain_open(label)
        if kind == "WORD":
            words[val] = words.get(val, 0) + 1
        else:
            nonoun += 1
CW = sorted(words)

FULL = set()
for p, r in CORPUS:
    t = G.read(p, r)
    if t is None:
        continue
    for _i, label, _n in A.count_rows(t):
        for w in G.B.grain_nouns(label):
            FULL.add(G.B.singular(w))
FULL = sorted(FULL)

print("  `grain_open` returns the grain NOUN.  Its value set is whatever the")
print("  corpus says, so there is no arity to run out of, and the failure case")
print("  is not a symbol meaning `this label has no grain` -- it is `NO-NOUN`")
print("  carrying the label that defeated the extractor.")
print()
G.pop("every count ROW of the reconstructed corpus", ref=G.RECON)
G.row("...count ROWS given a grain NOUN of their own", rows - nonoun,
      "printed line")
G.row("...count ROWS the extractor cannot read a noun from", nonoun,
      "printed line")
G.row("...distinct grain NOUNS that value set contains", len(CW),
      "de-pluralised noun")
G.row("...distinct grain NOUNS the corpus labels contain", len(FULL),
      "de-pluralised noun")
print()
print("  AND MY OWN REPAIR DROPS %d OF THEM BEFORE ANYTHING IS CLASSIFIED."
      % (len(FULL) - len(CW)))
print("  `grain_open` commits to ONE noun per label; A1d's extractor returns")
print("  the SET.  A label reading `...ROWS outside it, across 10 distinct")
print("  basenames` has two grain nouns and my function returns one of them.")
print("  So the open value set is open and still not wide enough for a LABEL")
print("  that carries two grains -- which is S3's finding arriving in S4 by a")
print("  different road, and it is a defect of MY function, not of the old one.")
print()
old = G.blocks(A._classify, FULL)
print("  THE 370, REPORTED RATHER THAN COUNTED.  My ticket asks for exactly")
print("  that.  `_classify` over the corpus's own %d grain nouns:" % len(FULL))
print()
for k in ("SITE", "EXECUTION", "BOTH", "NONE"):
    G.row("...grain NOUNS `_classify` answers %s" % k, len(old.get(k, [])),
          "de-pluralised noun")
print()
none = sorted(old.get("NONE", []))
print("  THE %d IT HAS NO ENTRY FOR, PRINTED IN FULL -- because `370` is a"
      % len(none))
print("  count of a set nobody has been shown, and a count of an unseen set is")
print("  the thing this arc keeps finding.  6 per line, alphabetical:")
print()
for i in range(0, len(none), 6):
    print("      " + "".join("%-19s" % w for w in none[i:i + 6]).rstrip())
print()
print("      (that list is %d nouns; the ticket's figure is 370)" % len(none))
ok370 = len(none) == 370
BAD += not ok370

# ---------------------------------------------------------------------------
G.hdr("S4b  ITS PRICE -- P4, PREDICTED BEFORE THE FUNCTION EXISTED")

print("  D3 of PREDICTIONS.md: a classifier keyed on the noun separates every")
print("  pair of distinct nouns, INCLUDING SYNONYMS.  So it does not have a")
print("  smaller false-distinction count than `_classify` -- it has a larger")
print("  one, and A1f's two adjudicated same-grain pairs are the two cases")
print("  this arc has actually ruled on.")
print()
print("      %-24s %-14s %-14s %s"
      % ("adjudicated SAME", "_classify", "open set", "verdict on the open set"))
mine_wrong = old_wrong = 0
for a, b, why in G.SAME_GRAIN:
    oa, ob = A._classify(a + "s"), A._classify(b + "s")
    o_split = oa != ob
    n_split = G.grain_open("..." + a)[1] != G.grain_open("..." + b)[1]
    old_wrong += o_split
    mine_wrong += n_split
    print("      %-24s %-14s %-14s %s"
          % ("%s / %s" % (a, b), "%s/%s" % (oa[:4], ob[:4]),
             "%s/%s" % (a[:5], b[:5]),
             "*** FALSE DISTINCTION" if n_split else "merged"))
print()
G.pop("the 2 word PAIRS A1f adjudicated as ONE grain")
G.row("...PAIRS `_classify` wrongly splits", old_wrong, "adjudicated pair")
G.row("...PAIRS the open-set classifier wrongly splits", mine_wrong,
      "adjudicated pair")
print()
p4 = mine_wrong == 2
print("      P4 as pre-registered (my repair splits 2 of 2)      %s"
      % ("HIT" if p4 else "*** MISS"))
BAD += not p4
print()
print("  I KEEP THIS AND I DO NOT SPECIAL-CASE IT.  A hand list merging those")
print("  two words would make the ratio a fact about my hand list, which is")
print("  AS5's lesson, and `selftest9160.py` carries an arm ASSERTING that the")
print("  open-set classifier still splits them -- so if a future edit quietly")
print("  merges them the selftest goes red rather than the number improving.")

# ---------------------------------------------------------------------------
G.hdr("S4c  THE SCOREBOARD, ON THE ONLY 11 PAIRS THIS ARC HAS ADJUDICATED")

print("  `_classify` answers every pair of grain words with a definite")
print("  verdict.  So does the open-set classifier.  Both are total functions")
print("  and the question -- ARE THESE THE SAME GRAIN -- is a question about")
print("  the world.  Here is each one scored where the world's answer exists:")
print("  A1f's five adjudications and A1e's six axes, 11 pairs, all of them")
print("  mg-03d1's judgements and none of them mine.")
print()
ADJ = ([(a, b, "SAME", w) for a, b, w in G.SAME_GRAIN]
       + [(a, b, "DIFFERENT", w) for a, b, w in G.DIFF_GRAIN])
print("      %-22s %-9s %-12s %-10s %s"
      % ("pair", "truth", "_classify", "open set", "notes"))
sc_old = sc_new = 0
old_by_absence = 0
for a, b, truth, why in ADJ:
    oa, ob = A._classify(a + "s"), A._classify(b + "s")
    o = "DIFFERENT" if oa != ob else "SAME"
    n = ("DIFFERENT" if G.B.singular(a) != G.B.singular(b) else "SAME")
    sc_old += o == truth
    sc_new += n == truth
    absence = o == truth and truth == "DIFFERENT" and "NONE" in (oa, ob)
    old_by_absence += absence
    print("      %-22s %-9s %-12s %-10s %s"
          % ("%s / %s" % (a, b), truth,
             "%s%s" % (o[:4], "" if o == truth else " X"),
             "%s%s" % (n[:4], "" if n == truth else " X"),
             "one pole is NONE" if absence else ""))
print()
G.pop("the 11 word PAIRS this arc has adjudicated, in A1e and A1f")
G.row("...PAIRS `_classify` gets right", sc_old, "adjudicated pair")
G.row("...of those, PAIRS right only because one pole is NONE",
      old_by_absence, "adjudicated pair")
G.row("...PAIRS the open-set classifier gets right", sc_new, "adjudicated pair")
print()
print("  NEITHER COLUMN IS A REPAIR.  The open set scores higher because this")
print("  arc's adjudications are mostly DIFFERENT and a function that always")
print("  says DIFFERENT scores well on them.  `_classify` scores %d, of which"
      % sc_old)
print("  %d are right only because one pole is a word it does not know."
      % old_by_absence)
print("  A constant function scores %d here.  The scoreboard is 11 pairs long"
      % len(G.DIFF_GRAIN))
print("  and there are %d pairs in the corpus."
      % (len(FULL) * (len(FULL) - 1) // 2))

# ---------------------------------------------------------------------------
G.hdr("S4d  THE THIRD VERDICT, AND WHY NO ARITY CARRIES IT")

tot = adjud = 0
for a, b in combinations(FULL, 2):
    tot += 1
    if G.verdict(a, b)[0] != "UNADJUDICATED":
        adjud += 1
print("  Both instruments above answer all %d pairs.  The arc has adjudicated"
      % tot)
print("  %d of them.  `verdict` returns the third value at the rest:" % adjud)
print()
# mg-2ff6 -- FROZEN at the reconstruction.  `79800` is not a figure about
# today's corpus and never was; it is C(400,2) over the 400 nouns of
# `9f1ecaa + eacc5e1`.  The same rule at HEAD gives a number more than
# twice as large, and the difference is the arc's growth and not a defect.
C.class_block([("the reconstructed corpus's grain-noun PAIRS", True, False,
                G.RECON)])
G.pop("the unordered PAIRS of the corpus's %d grain NOUNS" % len(FULL),
      ref=G.RECON)
G.row("...PAIRS in the corpus vocabulary", tot, "pair of grain nouns")
G.row("...PAIRS this arc has ADJUDICATED", adjud, "pair of grain nouns")
G.row("...PAIRS answered UNADJUDICATED", tot - adjud, "pair of grain nouns")
G.row("...PAIRS `_classify` answers with a definite verdict", tot,
      "pair of grain nouns")
G.row("...PAIRS the open-set classifier answers definitely", tot,
      "pair of grain nouns")
print()
print("      the arc has ruled on %.4f%% of its own grain pairs"
      % (100.0 * adjud / tot))
print()
for t in [
    "THAT IS THE HONEST FORM OF `623` AND OF `370`.  623 is the number of "
    "pairs `_classify` calls the same grain.  %d is the number of pairs "
    "anyone has actually decided.  The gap between them is not a defect of "
    "the classifier -- it is what the classifier is standing in for."
    % adjud,

    "AND NO NUMBER OF SYMBOLS CARRIES IT.  A function returning one symbol "
    "per word IS a partition; a partition IS an equivalence relation; and an "
    "equivalence relation has no room for `unknown` -- every pair is in a "
    "block or is not.  Five values do not help.  Four hundred do not help. "
    "This is why `add ROW_WORDS` is the wrong axis and why `make it "
    "five-valued` is the wrong axis in the same way: both stay inside the "
    "shape that cannot express the thing that is missing.",

    "SO THE TICKET'S SECOND EXIT IS THE RIGHT ONE AND ITS FIRST IS NOT.  "
    "`Report the 370 rather than silently returning NONE` is a change of "
    "SHAPE -- it makes what is unanswered visible.  `Return a grain from an "
    "open set` is a change of ARITY, and S4b is what that buys: a function "
    "that splits `steps` from `iterations` at every one of the pairs anyone "
    "has ruled on.",
]:
    body = textwrap.wrap(" ".join(t.split()), 70)
    print("  * " + body[0])
    for extra in body[1:]:
        print("    " + extra)
    print()

print("S4 TOTAL BAD: %d" % BAD)
sys.exit(BAD)
