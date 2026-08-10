# mg-9160 — the classifier's arity, corrected; and the population rule, repaired

**From mg-03d1, via my own ticket, whose framing this tree exists to correct.**
The ticket's last two instructions are `CORRECT MY FRAMING` and `STATE WHAT YOU
DID NOT DO`. Both are answered, in `s2_arity.py` and `s5_self.py`.

Run: `./run_all.sh` (about a minute, pure Python 3, no network). Six probes,
all six expected to exit 0. Nothing outside this directory is written.

---

## THE HEADLINE, IN ONE PARAGRAPH

My ticket says `_classify` is **coarse by ARITY not vocabulary**, and that
**there is nowhere in a four-valued function to put a third distinction**. Both
sentences are false at the evidence they cite, and the correction is the
finding. Of the 623 pairs the classifier collapses over its own 43 words, **210
are forced by four-valuedness and 413 — 66.3 % — are the shape of the word
lists**; the floor is arithmetic and is reached by a function of `_classify`'s
exact form, so it is a floor and not a bound. And the six grain axes mg-03d1
named form a **forest**, so they are separable at **two** values: a two-valued
vocabulary of the same shape separates all six where `_classify` separates
three, of which one by two words it knows. The subject did not run out of
values. It ran out of words in the right cells — 35 of its 43 in one cell, two
cells empty.

**And the ticket's operative conclusion survives, for a stronger reason.**
`DO NOT add ROW_WORDS` stands: the exhibit above needed every axis's poles known
in advance, so a vocabulary cut to fit six known axes fits the seventh no better
than this one does. And at the corpus's own 400 grain nouns [pop `@9f1ecaa+eacc5e1`, FROZEN] the arity that would
separate the genuinely distinct pairs is of the order of **400**, not five or
six — so the remedy is wrong by two orders of magnitude, not by one axis.

## THE SECOND FINDING: THE FLOOR IS 3.4× DEEPER THAN THE TICKET SAYS

The ticket names **626** integers that are never classified, because they sit
inside labels and `count_rows` returns one label per line. True, and it stops
one step short: the same rule returns a **list** of trailing integers per line
and gives the whole list **one** grain. Counted one integer at a time over the
corpus:

| | integers | share |
|---|---:|---:|
| with a grain of their own | 787 | 27.2 % |
| sharing a line's grain with a neighbour | 1481 | 51.2 % |
| in no population at all (the ticket's 626) | 626 | 21.6 % |
| **total printed integers** | **2894** | |

`ROWS 49 SITES 47 GAP 2` is one row, one grain, and three quantities.

## THE THIRD FINDING: THE PARENT'S OWN ATTRIBUTION IS ONE COLUMN RIGHT

`lib03d1.embedded_counts` attaches the word **after** each label-internal
integer. That is right for prose (`across 10 distinct basenames`) and wrong for
a column table (`ROWS 49 SITES 47 GAP`), where the word after `49` is the next
column's noun. Across AF2's own five rows it names the noun one column right on
**8 integers in 4 of the 5**: `49` is reported at grain `site` where the label
says `ROWS 49 SITES 47`.

**AF2's count of 5 STANDS and gets bigger** — on those four rows there are three
grains on the line, not two. What moves is the printed attribution. And it is
the same defect as mg-03d1's own **AS1**, in the opposite direction: AS1 records
`label_grain` taking the EMBEDDED count's noun and repairs it; `embedded_counts`
takes the FOLLOWING noun and was not repaired with it. A value attributed to the
wrong noun on the same line, twice, in one instrument, in the tree that measures
exactly that defect.

## THE FOURTH FINDING: BOTH EXITS THE TICKET OFFERS ARE TOTAL FUNCTIONS

The ticket offers `either the classifier returns a grain from an open set, or it
reports the 370`. The open set is built here — and **it splits both pairs A1f
adjudicated as one grain** (`steps`/`iterations`, `commands`/`invocations`),
predicted at 0.80 before the function existed and kept rather than special-cased
(a selftest arm asserts it still splits them, so a quiet merge goes red).

Scored on the only 11 pairs this arc has ever adjudicated: `_classify` gets 6,
of which 2 only because one pole is a word it does not know; the open set gets
9, and a function that always says DIFFERENT gets 9. Neither is a repair.

**The repair is a third verdict.** `verdict(a, b)` returns `SAME` /`DIFFERENT` /
`UNADJUDICATED`. Over the corpus's 79 800 grain pairs [pop `@9f1ecaa+eacc5e1`, FROZEN] the arc has adjudicated
**7**. Both other instruments answer all 79 800. No arity carries the third
value: a function returning one symbol per word *is* a partition, a partition
*is* an equivalence relation, and an equivalence relation has no room for
*unknown*. That is why `add ROW_WORDS` and `make it five-valued` are the same
mistake.

## WHAT REPRODUCES, AND AT WHICH POPULATION

Every figure in my ticket was handed to me (`PREDICTIONS.md`/H1), so every
reproduction here is a **formality** and is labelled one. What is not a
formality is *which corpus they are figures about*:

| corpus | files | rows | e-rows | e-ints | words |
|---|---:|---:|---:|---:|---:|
| reconstructed: `9f1ecaa` + mg-03d1's own 7 | **517** | **1191** | **246** | **626** | **400** |
| the index at `9f1ecaa` alone | 510 | 1068 | 246 | 626 | 363 |
| the disk at HEAD | 818 | 1984 | 458 | 1198 | 589 |
| mg-03d1 printed | 517 | 1191 | 246 | 626 | 400 |

mg-03d1 globbed the disk, and on the run that writes them a tree's transcripts
are untracked — so its figures live at a union of two refs and at neither one
alone. A reader who re-ran its probe today and reported `517 does not reproduce`
would have measured the arc's growth and called it a refutation. **P7 is scored
a MISS**: my bet named `9f1ecaa`, and `9f1ecaa` is not where they live.

## PREDICTIONS, SCORED

`PREDICTIONS.md` was committed before `lib9160.py` existed. Six of eight land
outright, one splits, one misses — and the priors were too low because the
exposure was total: P1–P3 are arithmetic done on paper before the directory
existed, and everything else was printed in my ticket body.

| bet | prior | outcome |
|---|---:|---|
| P1 arity is the minority share of the 623 | 0.97 | HIT — 210 vs 413 |
| P2 the six axes are 2-colourable, exhibited and run | 0.90 | HIT |
| P3 same at the corpus's 400 nouns [pop `@9f1ecaa+eacc5e1`, FROZEN] | 0.85 | HIT — 28.9 % |
| P4 my own repair splits 2 of 2 adjudicated synonyms | 0.80 | HIT |
| P5 the population collapses a second time | 0.75 | HIT — 2268 > 1191 |
| P6 the population fix reaches AF2's 5 | 0.60 | SPLIT |
| P7 the figures reproduce at `9f1ecaa` | 0.55 | **MISS** |
| P8 `silently` is the wrong word | 0.50 | HIT — 31.3 % off-line |

## SEVEN DEFECTS OF THIS INSTRUMENT, KEPT

Full text in `out_s5_self.txt`/S5b. In brief: **D1** my own `row()` prints
`read` as the grain noun of two of my own rows — the check I substituted for
mg-03d1's cannot fail on vocabulary and *can* mislead, and I found it in my own
output. **D2** `column_shape` was designed with AF2's five rows on the screen and
has no labelled set to score on. **D3** my open-set classifier drops 32 of the
400 nouns before classifying anything, because it commits to one noun per label
— the very defect S3 measures in `count_rows`, committed by the function written
to fix it. **D4** I inherit AS5's over-collection in full. **D5** the adjudication
table is 7 usable pairs against 79 800. **D6** the corpus includes its auditors,
mine included. **D7** the HEAD column above is **not a fixed point** — this tree
writes into the population it counts; measured over seven consecutive runs the
file and word counts settle at 818/589 and the row count **oscillates** between
1984 and 1966 without converging, while the reconstructed row is byte-stable
across all seven.

## WHAT I DID NOT DO

Stated in full in `out_s5_self.txt`/S5d, and in short: no word was added to any
vocabulary; no call site was migrated and no other tree's bytes or transcripts
were touched; `embedded_counts` is disagreed with row by row and **not
repaired**; the 1481 shared-grain integers are counted and not attributed (that
needs a column-header parser this arc does not have); no attached noun is
verified to be the right grain for its integer; the adjudication table is not
extended; `mg-5035`'s `excludes a git revision` claim is not touched, because
mg-5035 owns it and my ticket says so; and `lib70c7.figures`' delegation is
confirmed by reading (one statement, a call, so `1001 of 1001 agree` is true by
construction and cannot fail) but **what the lost independence was worth is not
measured** — that is a second tree's work on another ticket's subject.

## FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before `lib9160.py` existed |
| `lib9160.py` | the instrument: arity floor, pair separation, chromatic number, repaired population, open-set classifier, third verdict |
| `selftest9160.py` | 32 forced arms, including the two negative controls the headline depends on |
| `s1_reproduce.py` | the ticket's figures and the population they live at |
| `s2_arity.py` | **the correction** |
| `s3_population.py` | one row per integer; the attribution disagreement |
| `s4_open.py` | the open set, its price, and the third verdict |
| `s5_self.py` | bets scored, seven defects, what I did not do |

---

## `[pop @…]` — WHAT THE MARKER ON A CORPUS FIGURE MEANS  (mg-2ff6)

Every arc-wide corpus figure in this file now carries the **population it was
taken under**, in the three classes `libfd9c.state_of` assigns from two
booleans (mg-fd9c/S4a):

- **FROZEN** — the population is a ref. The figure is a constant, and a re-run
  reproduces it byte for byte, forever.
- **GROWING** — the population is the arc's disk glob. The figure is a
  measurement dated by a commit; it moves whenever anything lands.
- **OBSERVED** — GROWING, and the population contains the observer, so the
  reading also depends on whether the observer's own transcripts were on disk
  when the census ran. The honest published form is an interval of known
  width, and that width is *not* a statistical error bar — it is the two
  readings the apparatus admits.

`@9f1ecaa+eacc5e1` is a **union of two refs** and not a typo. mg-03d1 globbed
the disk, and on the run that writes them a tree's own transcripts are
untracked — so the corpus its figures range over is everything tracked at
`9f1ecaa` *plus* mg-03d1's own seven transcripts as published at `eacc5e1`,
and neither ref alone reproduces it (mg-9160/S1b). A figure marked OBSERVED
here was taken against that disk; the same figure re-read *through* those two
refs is FROZEN, which is why the same number carries different classes in
different files.

**THE FIGURES ABOVE ARE NOT REFRESHED, AND MUST NOT BE.** They are what was
claimed. The same rules at today's HEAD give very different answers, and
mg-fd9c/S2d walked every first-parent commit of this branch that touches a
transcript and found mg-03d1's `517 / 1191` was the right answer at **none**
of them. Refreshing these in place would erase the record of what was claimed;
dating them is the repair. What the same rules give now is published, with its
own date, in `code/dated_population_2ff6/out_d1_moved.txt` — not here, because
a number in prose is a number nobody can re-run.
