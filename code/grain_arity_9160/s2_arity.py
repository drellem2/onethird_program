"""mg-9160 / S2 -- THE CORRECTION.  ARITY IS A MINORITY OF THE COLLAPSE, AND
FOUR VALUES HAVE ROOM FOR SIX DISTINCTIONS.

My own ticket asserts a CAUSE:

    `_classify` IS TWO BOOLEAN MEMBERSHIP TESTS RETURNING FOUR SYMBOLS, SO ITS
    RESOLUTION IS A PROPERTY OF ITS ARITY, NOT ITS VOCABULARY.
    ...
    THERE IS NOWHERE IN A FOUR-VALUED FUNCTION TO PUT A THIRD DISTINCTION.

A cause is a decomposition, and nobody has computed the decomposition.  This
probe computes it, and both sentences are false at the evidence they cite.

  S2a  the ARITY FLOOR -- fewest pairs any four-valued function can collapse,
       and whether a function of `_classify`'s exact form can reach it;
  S2b  the decomposition: how much of the observed 623 is forced by four-ness
       and how much is the shape of the word lists;
  S2c  the same at the corpus's own 400 grain words;
  S2d  the six axes, as a graph -- and a TWO-valued vocabulary, exhibited and
       RUN, that expresses all six at once.

Exit code = number of S2 checks that fail.
"""

import sys

import lib9160 as G

BAD = 0
A = G.A


def render(alt):
    return alt.replace(r"\b", "").replace("s?", "s").replace(" ?", " ")


SITE_V = [render(a) for a in A.SITE_WORDS.pattern.split("|")]
EXEC_V = [render(a) for a in A.EXEC_WORDS.pattern.split("|")]
VOCAB = SITE_V + EXEC_V

G.bar("mg-9160 / S2 -- ARITY IS A MINORITY OF THE COLLAPSE")
print("HEAD: %s" % G.head())
print("Correcting: my own ticket body, mg-9160, quoted above in full.")

# ---------------------------------------------------------------------------
G.hdr("S2a  THE ARITY FLOOR, AND WHETHER `_classify`'S FORM CAN REACH IT")

print("  A k-valued function is a partition into at most k blocks; a pair is")
print("  collapsed iff both words share a block.  The sum of C(n_i,2) is")
print("  smallest at the most equal partition.  So no four-valued function on")
print("  43 words can collapse fewer than:")
print()
n = len(VOCAB)
floor4 = G.min_collapse(n, 4)
floor3 = G.min_collapse(n, 3)
G.pop("all four-valued FUNCTIONS on the 43 vocabulary words")
G.row("...PAIRS the best four-valued function still collapses", floor4,
      "pair of words")
G.row("...PAIRS the best four-valued function tells apart",
      n * (n - 1) // 2 - floor4, "pair of words")
print()
print("  E1's CONTROL, BECAUSE THE FLOOR DEPENDS ON IT.  `_classify`'s four")
print("  cells are (in EXEC only), (in SITE only), (in BOTH), (in NEITHER).")
print("  If nothing can land in BOTH the function is three-valued in practice")
print("  and the floor is %d, not %d.  So: a string that classifies BOTH."
      % (floor3, floor4))
print()
print("      `_classify('rows executed')`               = %s"
      % A._classify("rows executed"))
print("      `_classify('zzzz')`                        = %s"
      % A._classify("zzzz"))
both_ok = A._classify("rows executed") == "BOTH"
print("      all four cells reachable                    %s"
      % ("YES -- the floor is %d" % floor4 if both_ok
         else "*** NO -- the floor is %d" % floor3))
BAD += not both_ok
print()
print("  AND THE FLOOR IS REACHED BY A FUNCTION OF EXACTLY THIS FORM, not by")
print("  some other four-valued function.  Below: the 43 words dealt round-")
print("  robin into the four cells, expressed as two membership sets, run")
print("  through `two_test` -- two boolean tests, four symbols, same shape.")
print()
ex, si = G.balanced_sets(VOCAB, 4)
bal = G.two_test(ex, si)
bp, bs, bc = G.collapse(bal, VOCAB)
part = G.blocks(bal, VOCAB)
print("      cells: " + "  ".join("%s=%d" % (k, len(v))
                                  for k, v in sorted(part.items())))
G.pop("the 43 vocabulary WORDS under a BALANCED four-cell assignment")
G.row("...PAIRS that assignment collapses", bc, "pair of words")
reach = bc == floor4
print("      the floor is ACHIEVED by `_classify`'s own form   %s"
      % ("YES" if reach else "*** NO"))
BAD += not reach

# ---------------------------------------------------------------------------
G.hdr("S2b  THE DECOMPOSITION -- AND THE TICKET'S SLOGAN IS FALSE AT TWO "
      "THIRDS OF ITS OWN EVIDENCE")

pairs, sep, coll = G.collapse(A._classify, VOCAB)
forced = floor4
shape = coll - forced
print("  The observed collapse, the floor, and the difference.  The floor is")
print("  what FOUR-VALUEDNESS costs whatever words you choose.  The remainder")
print("  is what THESE words cost -- 35 in one cell, 8 in another, two cells")
print("  empty.  That remainder is the vocabulary, by definition.")
print()
G.pop("the 903 unordered PAIRS of the classifier's own vocabulary")
G.row("...PAIRS `_classify` actually collapses", coll, "pair of words")
G.row("...PAIRS forced by four-valuedness alone", forced, "pair of words")
G.row("...PAIRS attributable to the WORD LISTS", shape, "pair of words")
print()
print("      forced by arity     %5.1f%% of the collapse" % (100.0 * forced / coll))
print("      the word lists      %5.1f%% of the collapse" % (100.0 * shape / coll))
print()
print("  MY TICKET SAYS `A PROPERTY OF ITS ARITY, NOT ITS VOCABULARY`.  AT THE")
print("  VERY PAIRS IT COUNTS, THE VOCABULARY IS THE MAJORITY SHARE.  I filed")
print("  that framing; it is wrong; the number above is the correction.")
p1 = shape > forced
print("      P1 as pre-registered (>= 413 to the word lists)     %s"
      % ("HIT -- %d" % shape if shape >= 413 else "*** MISS -- %d" % shape))
BAD += not p1

# ---------------------------------------------------------------------------
G.hdr("S2c  THE SAME DECOMPOSITION AT THE CORPUS'S OWN 400 GRAIN WORDS")

words = set()
for p, r in G.parent_corpus():
    t = G.read(p, r)
    if t is None:
        continue
    for _i, label, _n in A.count_rows(t):
        for w in G.B.grain_nouns(label):
            words.add(G.B.singular(w))
CW = sorted(words)
cp, cs, cc = G.collapse(lambda w: A._classify(w), CW)
cfloor = G.min_collapse(len(CW), 4)
cpart = G.blocks(lambda w: A._classify(w), CW)
print("  The corpus's vocabulary, not the classifier's: every grain noun of")
print("  every count row of the reconstructed corpus, extracted by shape with")
print("  mg-03d1's own `grain_nouns` (imported, not restated -- and it over-")
print("  collects, which is its AS5 and my E2).")
print()
print("      cells: " + "  ".join("%s=%d" % (k, len(v))
                                  for k, v in sorted(cpart.items())))
G.pop("the grain WORDS of the reconstructed corpus, as unordered pairs")
G.row("...distinct grain WORDS in the corpus", len(CW), "de-pluralised noun")
G.row("...unordered PAIRS over them", cp, "pair of grain words")
G.row("...PAIRS `_classify` collapses", cc, "pair of grain words")
G.row("...PAIRS forced by four-valuedness alone", cfloor, "pair of grain words")
G.row("...PAIRS attributable to the WORD LISTS", cc - cfloor,
      "pair of grain words")
print()
print("      collapse rate                                    %5.1f%%"
      % (100.0 * cc / cp))
print("      the floor's own rate at k=4                      %5.1f%%"
      % (100.0 * cfloor / cp))
print("      forced by arity: %5.1f%% of the collapse" % (100.0 * cfloor / cc))
print()
print("  E4, HONOURED HERE: 623 ranges over 903 pairs of VOCABULARY words and")
print("  the number above ranges over the pairs of CORPUS words below.  They")
print("  are two populations and the only sentence that may hold both is this")
print("  one.  (the second population's size: %d pairs)" % cp)
print()
print("  AND THE PART THAT SAVES THE TICKET'S REMEDY.  The floor is not the")
print("  whole story in the other direction either: separating every pair of")
print("  %d genuinely distinct grains needs %d values, not five and not six."
      % (len(CW), len(CW)))
print("  So `either the classifier returns a grain from an open set` is right,")
print("  and the reason is not `4 is one too few` -- it is that the arity")
print("  needed is of the order of the number of grains, which is why adding")
print("  ROW_WORDS is wrong by two orders of magnitude rather than by one axis.")
p3 = cc - cfloor > cfloor
print()
print("      P3 as pre-registered (arity the minority share)     %s"
      % ("HIT" if p3 else "*** MISS"))
BAD += not p3

# ---------------------------------------------------------------------------
G.hdr("S2d  `NOWHERE TO PUT A THIRD DISTINCTION` -- THE SIX AXES ARE A FOREST")

AXES = [
    ("row", "site", "O1 itself: 14 (site,target) rows behind 12 source lines"),
    ("file", "line", "mg-d53d's arc: 806 deletion rows vs the files"),
    ("item", "specy", "mg-4adb's species vs its rungs"),
    ("pair", "poset", "mg-0ba7's 0 crossings over 10 ordered tree pairs"),
    ("mention", "name", "mg-bf79's P3c: a MENTION is still COUNTED"),
    ("site", "execution", "F1, the axis the instrument was built for"),
]
edges = [(a, b) for a, b, _ in AXES]
verts = sorted({v for e in edges for v in e})

print("  A1e's six axes as MUST-SEPARATE edges.  Eleven vertices, six edges,")
print("  one vertex of degree two (`site`).  No cycle -- so a forest, so two-")
print("  colourable.  `chromatic` brute-forces it rather than asserting it,")
print("  and the selftest's triangle control shows the routine can say 3.")
print()
k, colouring = G.chromatic(verts, edges)
G.pop("the 6 named grain AXES, as a graph on 11 grain WORDS")
G.row("...grain WORDS the six axes name", len(verts), "grain word")
G.row("...AXES to be separated", len(edges), "axis")
G.row("...VALUES a classifier needs to separate all six", k, "classifier value")
print()
print("      the colouring found: " + "  ".join(
    "%s=%d" % (v, colouring[v]) for v in verts))
print()
print("  AND IT IS EXHIBITED, NOT ARGUED.  Below, the colouring is turned into")
print("  two membership sets and run through `two_test` -- two boolean tests,")
print("  four symbols, the same shape as `_classify`.  Only two of its four")
print("  cells are used, which is the point: TWO values are enough for six")
print("  distinctions and the subject has FOUR.")
print()
ex2 = {v for v in verts if colouring[v] == 0}
si2 = {v for v in verts if colouring[v] == 1}
alt = G.two_test(ex2, si2)
print("      %-10s %-10s %-12s %-12s %s"
      % ("pole A", "pole B", "_classify", "exhibit", "axis"))
old_ok = new_ok = 0
for a, b, why in AXES:
    oa, ob = A._classify(a + "s"), A._classify(b + "s")
    na, nb = alt(a), alt(b)
    o = oa != ob
    nn = na != nb
    old_ok += o
    new_ok += nn
    print("      %-10s %-10s %-12s %-12s %s"
          % (a, b, "%s/%s%s" % (oa[:4], ob[:4], "" if o else " X"),
             "%s/%s%s" % (na[:4], nb[:4], "" if nn else " X"), why[:26]))
print()
G.pop("the 6 named grain AXES, put to two classifiers of the SAME form")
G.row("...AXES `_classify` separates", old_ok, "axis")
G.row("...AXES the two-valued exhibit separates", new_ok, "axis")
print()
print("  A1e's refinement applies to the middle column and not to mine: two of")
print("  the axes `_classify` `separates` are separated only because one pole")
print("  is NONE -- absence of a word, not a distinction drawn.  Every axis in")
print("  the right-hand column is separated by two words the exhibit KNOWS.")
print()
p2 = new_ok == len(AXES) and k == 2
print("      P2 as pre-registered (2 colours, all six separated)  %s"
      % ("HIT" if p2 else "*** MISS"))
BAD += not p2
print()
print("  SO `THERE IS NOWHERE IN A FOUR-VALUED FUNCTION TO PUT A THIRD")
print("  DISTINCTION` IS FALSE.  There is room for six in a TWO-valued one.")
print("  What the subject ran out of was not values, it was words in the right")
print("  cells -- 35 of its 43 words in one cell and two cells empty.")
print()
print("  E3, THE SCOPE, IN THE SAME BREATH AS THE RESULT: this is a statement")
print("  about THE SIX AXES mg-03d1 NAMED.  It is not a statement about the")
print("  corpus.  S2c is the corpus, and there the answer is %d values, which"
      % len(CW))
print("  no fixed vocabulary supplies.")
print()
print("  AND WHAT THAT DOES **NOT** LICENCE.  `Two colours suffice` is not a")
print("  proposal to re-cut SITE_WORDS.  Every axis above needed its poles")
print("  known IN ADVANCE; the colouring was computed FROM the answer.  A")
print("  vocabulary cut to fit six known axes fits the seventh no better than")
print("  this one does -- which is exactly why the ticket's `DO NOT DO THAT`")
print("  about ROW_WORDS stands after the correction, and stands harder.")

print()
print("S2 TOTAL BAD: %d" % BAD)
sys.exit(BAD)
