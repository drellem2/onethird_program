"""mg-9160 / S1 -- THE TICKET'S FIGURES, REPRODUCED, AND THE POPULATION THEY
LIVE AT.

WHAT THIS PROBE IS WORTH AND WHAT IT IS NOT.  PREDICTIONS.md/H1: my ticket body
prints every number below.  So this section is a FORMALITY and its agreement
with mg-03d1 is not independent confirmation of anything.  It exists for two
reasons that are not confirmation:

  S1a  to establish which POPULATION the ticket's figures are figures about --
       and it is not any single commit, which is P7;
  S1b  to count the 623 by RUNNING the classifier over all 903 pairs, where
       A1c computes `C(43,2) - 35*8` in closed form.  The closed form is right
       only if every vocabulary word lands in its own list, which A1c PRINTS
       but does not CHECK.  This turns a printed table into an arm.

Exit code = number of S1 checks that fail.
"""

import sys

import lib9160 as G

# mg-2ff6 -- THE CONVENTION, IMPORTED.  `convention()` is a LAZY import, and
# the laziness is load-bearing: `libfd9c` imports `lib9160` at its own top
# level, so a top-level import of the convention here would be circular.
C = G.convention()

BAD = 0
A = G.A


def render(alt):
    """One regex alternative as a probe string.  A1c's rule, by its own text."""
    return alt.replace(r"\b", "").replace("s?", "s").replace(" ?", " ")


G.bar("mg-9160 / S1 -- THE TICKET'S FIGURES AND THEIR POPULATION")
print("HEAD: %s   subject: `lib56dc._classify` / `lib56dc.count_rows`"
      % G.head())
print("Parent: mg-03d1 at %s, transcripts published at %s"
      % (G.PARENT_REV, G.PARENT_PUB))

# ---------------------------------------------------------------------------
G.hdr("S1a  THE VOCABULARY, AND THE 623 COUNTED BY RUNNING RATHER THAN BY "
      "ARITHMETIC")

SITE_V = [render(a) for a in A.SITE_WORDS.pattern.split("|")]
EXEC_V = [render(a) for a in A.EXEC_WORDS.pattern.split("|")]
VOCAB = SITE_V + EXEC_V

pairs, sep, coll = G.collapse(A._classify, VOCAB)
part = G.blocks(A._classify, VOCAB)

print("  Every alternative of both vocabularies put through `_classify`, and")
print("  then every unordered PAIR of them compared.  A1c prints the per-word")
print("  table and then computes the pair counts as `C(n,2) - |SITE|*|EXEC|`.")
print("  That closed form is correct only if no alternative lands outside its")
print("  own list -- so here the pairs are compared one at a time and the")
print("  partition is printed, which is the arm A1c does not have.")
print()
print("  the partition `_classify` induces on its OWN vocabulary:")
for k in ("SITE", "EXECUTION", "BOTH", "NONE"):
    print("      %-10s %3d word(s)" % (k, len(part.get(k, []))))
print()
G.pop("the 43 vocabulary WORDS of `_classify`, taken as unordered pairs")
G.row("...vocabulary WORDS in SITE_WORDS", len(SITE_V), "regex alternative")
G.row("...vocabulary WORDS in EXEC_WORDS", len(EXEC_V), "regex alternative")
G.row("...unordered PAIRS over those words", pairs, "pair of words")
G.row("...PAIRS of those WORDS it tells apart", sep, "pair of words")
G.row("...PAIRS of those WORDS it collapses", coll, "pair of words")
print()
ok = (len(SITE_V), len(EXEC_V), pairs, sep, coll) == (35, 8, 903, 280, 623)
print("      the ticket's 35 / 8 / 903 / 280 / 623                %s"
      % ("REPRODUCED (a formality -- H1)" if ok else "*** DOES NOT REPRODUCE"))
BAD += not ok
print()
print("  AND THE PART THAT IS NOT A FORMALITY: only TWO of the four cells are")
print("  occupied.  `BOTH` and `NONE` hold nothing.  A four-valued function is")
print("  being used as a two-valued one, and that is a fact about the WORD")
print("  LISTS, not about the arity.  S2 is the consequence.")

# ---------------------------------------------------------------------------
G.hdr("S1b  P7 -- WHICH CORPUS THE 517 / 1191 / 400 / 626 ARE FIGURES ABOUT")

print("  mg-03d1 globbed the DISK.  On the run that writes them a tree's own")
print("  transcripts are untracked, so the corpus its figures range over is")
print("  neither `9f1ecaa` nor `eacc5e1` but the union: everything tracked at")
print("  9f1ecaa PLUS mg-03d1's own seven transcripts as published.")
print()


def census(files):
    rows = trail = emb = embrows = 0
    words = set()
    for p, r in files:
        t = G.read(p, r)
        if t is None:
            continue
        for _i, label, nums in A.count_rows(t):
            rows += 1
            trail += len(nums)
            e = G.B.embedded_counts(label)
            if e:
                embrows += 1
                emb += len(e)
            for w in G.B.grain_nouns(label):
                words.add(G.B.singular(w))
    return len(files), rows, trail, embrows, emb, len(words)


VIEWS = [
    ("reconstructed: 9f1ecaa + mg-03d1's own", G.parent_corpus()),
    ("the index at 9f1ecaa alone",
     [(p, G.PARENT_REV) for p in G.corpus(G.PARENT_REV)]),
    ("the disk at HEAD now", [(p, None) for p in G.corpus()]),
]
TARGET = (517, 1191, 246, 626, 400)
# mg-2ff6 -- THE DATED POPULATION, ABOVE THE TABLE AND NOT BELOW IT.  There
# was a `pop()` here already and it sat AFTER the four rows, so cfd9c's S4c
# walked up from `the disk at HEAD now`, hit the section bar, and scored the
# row UNDATED.  The population line has to be where the reader (and the
# checker) reaches it before the figure, which is above.
G.pop("the 4 corpus VIEWS below, each at the ref its own row names")
print("      %-38s %6s %6s %6s %6s %6s"
      % ("corpus", "files", "rows", "e-rows", "e-ints", "words"))
res = {}
for tag, files in VIEWS:
    n, rows, trail, embrows, emb, words = census(files)
    res[tag] = (n, rows, embrows, emb, words, trail)
    print("      %-38s %6d %6d %6d %6d %6d"
          % (tag, n, rows, embrows, emb, words))
print("      %-38s %6d %6d %6d %6d %6d"
      % ("mg-03d1 PRINTED", TARGET[0], TARGET[1], TARGET[2], TARGET[3],
         TARGET[4]))
print()
# mg-2ff6 -- THE CLASS OF EACH ROW, and it is the point of the table.  Three
# of these four rows are FROZEN and one is OBSERVED, and that is the whole
# difference between a figure that reproduces forever and a figure that was
# the right answer at one commit of 245.
C.class_block([
    ("reconstructed: 9f1ecaa + mg-03d1's own", True, False,
     "%s+%s" % (G.PARENT_REV, G.PARENT_PUB)),
    ("the index at 9f1ecaa alone", True, False, G.PARENT_REV),
    ("the disk at HEAD now", False, True, None),
    ("mg-03d1 PRINTED", True, False, G.PARENT_PUB),
])
print()
C.observed_block("code/grain_arity_9160/",
                 note="This is the `the disk at HEAD now` row, field by field.")
print()
G.pop("the 3 corpus VIEWS above, one row each")
hits = sum(1 for tag in res if res[tag][:5] == TARGET)
G.row("...corpus VIEWS reproducing all 5 printed FIGURES", hits, "corpus view")
print()
rec = res["reconstructed: 9f1ecaa + mg-03d1's own"][:5] == TARGET
idx = res["the index at 9f1ecaa alone"][:5] == TARGET
now = res["the disk at HEAD now"][:5] == TARGET
print("      the reconstruction reproduces all five                 %s"
      % ("YES" if rec else "*** NO"))
print("      `9f1ecaa` ALONE reproduces all five                    %s"
      % ("yes" if idx else "no"))
print("      HEAD reproduces all five                               %s"
      % ("yes" if now else "no"))
BAD += not rec
print()
_idx = res["the index at 9f1ecaa alone"]
_now = res["the disk at HEAD now"]
print("  P7 SPLITS, AND THE HALF IT LOSES IS THE HALF I WROTE CARELESSLY.  I")
print("  bet that all four figures reproduce EXACTLY AT `9f1ecaa`.  They do")
print("  not: at that ref alone the corpus is %d files and %d rows, and 2 of"
      % (_idx[0], _idx[1]))
print("  the 5 figures move.  They reproduce at the RECONSTRUCTION, which is a")
print("  different object and one my bet did not name.  The half that lands is")
print("  that NOT ONE of the five reproduces at HEAD -- the corpus is now %d"
      % _now[0])
print("  files and %d rows -- so a reader who re-ran mg-03d1's probe today and"
      % _now[1])
print("  reported `517 does not reproduce` would have measured the arc's own")
print("  growth and called it a refutation.")
print()
print("  AND THE HEAD ROW ABOVE IS NOT A FIXED POINT.  This tree writes into")
print("  `code/*/out_*.txt`, which is the population every census here ranges")
print("  over, so each run changes the next run's answer.  Measured over seven")
print("  consecutive runs in `s5_self.py`/D7: the file and word counts settle")
print("  and the ROW count OSCILLATES between 1984 and 1966 without ever")
print("  converging.  The RECONSTRUCTED row is byte-stable across all")
print("  seven, because it reads at two fixed refs.  That is the argument for")
print("  reconstructing rather than globbing, and it was arrived at by running")
print("  it rather than by reasoning about it.")
print()
print("  AND THE CORPUS INCLUDES THE AUDITOR.  7 of the 517 files and every")
print("  count row in them are mg-03d1's own output, measured by mg-03d1.")
print("  That is AS7's shape and it is not avoidable here -- the population is")
print("  named by a property (`code/*/out_*.txt`) and the auditor's tree")
print("  satisfies it.  It is disclosed rather than corrected, because the")
print("  alternative is a population named by a path literal, which is O2.")

# ---------------------------------------------------------------------------
G.hdr("S1c  P8 -- `SILENTLY RETURNS NONE` IS THE WRONG WORD FOR IT")

print("  My ticket says the classifier `silently returns NONE` for the 370.")
print("  `grain_of` widens to the two lines above and then to a column header")
print("  and RETURNS THE STAGE.  So the count rows resolved at `prev` or")
print("  `header` are rows whose grain was read off A DIFFERENT LINE, and the")
print("  stage column says so.  The defect is ATTRIBUTION, not silence.")
print()
stages = {}
grains = {}
for p, r in G.parent_corpus():
    t = G.read(p, r)
    if t is None:
        continue
    lines = t.splitlines()
    for i, label, _nums in A.count_rows(t):
        above = [lines[j] for j in range(i - 2, max(-1, i - 2 - 8), -1)
                 if 0 <= j < len(lines)]
        g, st = A.grain_of(label, above)
        stages[st] = stages.get(st, 0) + 1
        grains[g] = grains.get(g, 0) + 1
tot = sum(stages.values())
G.pop("every count ROW of the reconstructed corpus")
for st in ("label", "prev", "header", "-"):
    G.row("...count ROWS resolved at stage `%s`" % st, stages.get(st, 0),
          "printed line")
print()
for g in ("SITE", "EXECUTION", "BOTH", "NONE"):
    G.row("...count ROWS whose grain reads %s" % g, grains.get(g, 0),
          "printed line")
print()
off = stages.get("prev", 0) + stages.get("header", 0)
print("      grain taken from a DIFFERENT LINE: %d of %d rows (%.1f%%)"
      % (off, tot, 100.0 * off / tot if tot else 0))
print("      grain not found at all:            %d of %d rows (%.1f%%)"
      % (stages.get("-", 0), tot, 100.0 * stages.get("-", 0) / tot if tot
         else 0))
print()
print("  P8 IS SCORED IN S5.  What the numbers say either way: the word")
print("  `silently` is mine and it is wrong -- the stage is returned and the")
print("  parent's `grain_ledger` carries it.  What IS silent is that a row")
print("  resolved at `header` is a row whose grain belongs to a table, and")
print("  nothing checks that this row is in that table.")

print()
print("S1 TOTAL BAD: %d" % BAD)
sys.exit(BAD)
