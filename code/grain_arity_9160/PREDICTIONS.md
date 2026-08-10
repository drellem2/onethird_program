# mg-9160 — predictions, committed before one line of `lib9160.py` exists

**Subject.** mg-03d1's finding, as `mg-9160` states it: `lib56dc._classify` is
*coarse by ARITY not vocabulary* (623 collapsed pairs over its own 43 words;
370 of the corpus's 400 grain words [pop `@9f1ecaa+eacc5e1`, FROZEN] with no entry at all), and *the same limit
sits one layer down in the population rule*, where 626 integers are never
classified because `lib56dc.count_rows` returns one label and one grain per
LINE.

The ticket ends `CORRECT MY FRAMING`. That is what this tree is for, and the
correction is the deliverable — not a reproduction with a decoration on it.

---

## 0. EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

**H1 — every figure below was handed to me.** My ticket body prints
903 / 280 / 623, 400 / 26 / 4 / 0 / 370, 86.0 %, 1191 / 246 / 626, the count of
5 different-grain rows, all six named axes with their verdicts, and both
false-distinction pairs. **Every reproduction in this tree is therefore a
FORMALITY.** Agreement between me and mg-03d1 on any of those numbers is not
independent confirmation and will not be reported as one.

**H2 — I read the parent's evidence before writing this.** I read
`code/grain_axis_audit_03d1/out_a1_axes.txt` sections A1c–A1f and
`out_a6_self.txt` sections AF1/AF2/AS in full, and `lib56dc.py`,
`lib03d1.py` and `libbf79.py` in full, before writing a single line of this
file. **No definition below is a discovery.** In particular A1e's own post-hoc
refinement — *two of the three EXPRESSIBLE axes are expressible only because
one pole is `NONE`* — is the parent's, not mine, and my ticket repeats it.

**H3 — what is NOT delivered by the ticket, and is therefore the only place
this tree can earn anything:** every number in §2 below. The ticket asserts a
CAUSE (`arity, not vocabulary`) and never quantifies it. A cause is a
decomposition, and nobody has computed the decomposition.

---

## 1. DERIVED ON PAPER, BEFORE THE DIRECTORY EXISTED

These are arithmetic, not bets. They are written here so that if the probe
disagrees with them the probe is wrong, and I have to say which.

**D1 — the arity floor.** A function with `k` values induces a partition of
`n` words into at most `k` blocks; two words are told apart iff they fall in
different blocks. Collapsed pairs = Σ C(n_i, 2), minimised when the blocks are
as equal as possible.

* `n = 43`, `k = 4` → blocks 11/11/11/10 → 3·55 + 45 = **210** collapsed, so at
  most 903 − 210 = **693** separated.
* `n = 400`, `k = 4` → blocks 100/100/100/100 → 4·4950 = **19 800** collapsed of
  79 800, so at most **60 000** separated.

**D2 — the six-axis constraint graph is a FOREST.** The axes A1e names, as
must-separate edges on the words they name:

```
row — site        file — line       item — species
pair — poset      mentions — names  site — executions
```

Eleven distinct vertices, six edges, and the only vertex of degree 2 is `site`
(in `row — site` and `site — executions`). No cycle. A forest is 2-colourable.

**D3 — resolution and synonymy trade off, and the trade is forced.** A
classifier keyed on the grain NOUN ITSELF has an open value set, so it
separates every pair of distinct nouns — including every pair of SYNONYMS. Its
false-distinction count is therefore not smaller than `_classify`'s; it is
**the number of true-synonym pairs in the vocabulary**, which is larger. There
is no assignment of words to symbols that both separates every genuinely
distinct pair and merges every synonym pair unless the assignment already
encodes which pairs are which. So the honest exit is not more values: it is a
**third verdict** — `SAME` / `DIFFERENT` / `UNADJUDICATED` — which a function
returning a grain symbol per word cannot carry no matter how many symbols it
has.

---

## 2. THE BETS

Probabilities are mine, written before running anything.

**P1 (0.97) — THE TICKET'S SLOGAN IS FALSE AT A MAJORITY OF THE PAIRS IT
CITES.** By D1 the arity floor over the classifier's own 43 words is 210. The
observed collapse is 623. So **≤ 210 of the 623 (33.7 %) are forced by
four-valuedness and ≥ 413 (66.3 %) are the shape of the partition — i.e. the
vocabulary.** `a property of its ARITY, NOT its VOCABULARY` is wrong about
two thirds of its own evidence. I filed the ticket's framing; I expect to be
the one refuting it.

**P2 (0.90) — `THERE IS NOWHERE IN A FOUR-VALUED FUNCTION TO PUT A THIRD
DISTINCTION` IS FALSE, AND I WILL EXHIBIT THE COUNTEREXAMPLE AND RUN IT.** By
D2 the six-axis graph is 2-colourable, so there is a **TWO**-valued assignment
of the existing vocabulary separating all six axes at once. I will build it,
run it through a classifier of exactly `_classify`'s form (two membership
tests), and print all six verdicts. Four values leave room for six
distinctions, not two.

**P3 (0.85) — AT THE CORPUS'S OWN WORDS THE SLOGAN IS ALSO A MINORITY CLAIM,
BUT THE TICKET'S REMEDY SURVIVES FOR A REASON IT DOES NOT GIVE.** By D1 the
floor at `n = 400, k = 4` is 19 800 of 79 800 (24.8 %) against an observed
68 596 (86.0 %) — again the minority. The remedy (`a grain from an open set`)
is right, but the argument for it is not `4 is one too few`; it is that the
arity needed to separate the genuinely distinct pairs is **of the order of the
number of distinct grains — hundreds, not five or six.** Adding `ROW_WORDS`
is wrong not because it buys one axis but because it is on the wrong scale by
two orders of magnitude.

**P4 (0.80) — MY OWN REPAIR COMMITS THE MIRROR DEFECT AT 2 OF 2 WHERE THE
INSTRUMENT IT REPLACES COMMITS IT AT 2 OF 5.** By D3, the open-set classifier
will return DIFFERENT for `steps`/`iterations` and for `commands`/
`invocations` — A1f's two adjudicated same-grain pairs. A remedy is an
artifact of the same kind as the defect it remedies; this is the defect,
predicted before the code exists, and I will keep it and report it rather than
special-case those two words.

**P5 (0.75) — THE POPULATION RULE COLLAPSES A SECOND TIME AND NOBODY HAS
COUNTED THAT ONE EITHER.** `count_rows` returns a LIST of trailing integers per
line and `grain_of` returns ONE grain for the line. So beyond the 626
label-internal integers there are trailing integers sharing a single grain
with their neighbours. I predict the count of integers in the repaired
population strictly exceeds 1191 + 626, i.e. that `sum(len(nums)) > 1191`.

**P6 (0.60) — THE POPULATION FIX REACHES 5 OF 5 WHERE THE CLASSIFIER FIX
REACHES 0 OF 5.** AF2's five different-grain rows are, by construction, invisible
to any repair of `_classify`. I predict the repaired population puts all five
second integers in scope with their own grain noun attached.

**P7 (0.55) — THE CORPUS HAS GROWN AND NONE OF THE TICKET'S CORPUS FIGURES
REPRODUCE AT HEAD.** 517 / 1191 / 400 / 626 were measured at `9f1ecaa`. Several
trees have landed since. I predict every one of those four reproduces EXACTLY
at `9f1ecaa` and NOT ONE of them reproduces at HEAD — and that reporting only
the HEAD number would read as a refutation of the ticket when it is a change of
population underfoot.

**P8 (0.50) — THE `NONE` ANSWERS ARE NOT SILENT, THEY ARE ANSWERED BY ANOTHER
LINE.** The ticket says the classifier `silently returns NONE` for the 370.
`grain_of` widens to `prev` and then to `header`, and returns the stage. I
predict a substantial share of corpus count rows are resolved at `prev` or
`header` — each one a grain read off a DIFFERENT LINE — so the defect is not
silence, it is **attribution**, and the stage column is the honest part of the
design. Under 50 % because I do not know the distribution.

---

## 3. MY OWN ERRORS, FILED IN ADVANCE

**E1 — my floor may be a bound.** D1 assumes all four cells of `_classify` are
reachable. They are reachable only if some probe string can be in BOTH word
lists. If none can, `BOTH` is unreachable, `k = 3` in practice, and my 210 is
wrong (it would be 3 blocks: 15/14/14 → 105+91+91 = 287). **CHECK IT by
exhibiting a string that classifies `BOTH`, or correct the floor.**

**E2 — I inherit AS5.** The grain-noun extractor over-collects (`about`,
`anyway`, `bfd` are among the 400). I import mg-03d1's `grain_nouns` rather
than restating it, so every ratio I print over the 400 is a ratio over an
over-collected vocabulary, exactly as the parent's is. Not trimmed, for the
parent's reason.

**E3 — my headline's scope.** *Two colours suffice* is a statement about the
SIX AXES mg-03d1 NAMED. If the corpus's real axis graph has an odd cycle it is
not 2-colourable and my exhibit generalises to nothing. The scope must appear
in the same sentence as the result, every time, or I have committed a sample
read as an enumeration — this arc's most-repeated defect.

**E4 — two populations, one comparison.** 623 ranges over 903 pairs of
vocabulary words; 68 596 ranges over 79 800 pairs of corpus words [pop `@9f1ecaa+eacc5e1`, FROZEN]. Any sentence
putting those two numbers side by side without naming both populations is O1
committed by me, in the tree that measures O1.

**E5 — `same grain` has no mechanical test.** A1f adjudicated by hand and said
so. My `UNADJUDICATED` verdict does not remove the hand judgement; it makes the
absence of one reportable. If I ever print a synonym ratio as though it were
measured, that is this error.

**E6 — being IN the population is not being classified CORRECTLY.** The
population repair puts 626 integers in scope and attaches the noun that follows
each one. Whether that noun is the right grain for that integer is a fact about
the code that printed it, and I do not measure it — the parent's `grain_ledger`
docstring makes exactly this distinction and I inherit it.

**E7 — the self-rule I am NOT adopting.** `lib03d1.row()` requires every label
of that tree to classify at stage `label` under `lib56dc.grain_of`, and AS3
records the cost: *my subject is grain distinctions it has no word for, and to
pass my own check I must describe them using only words it does.* I do not
adopt that rule. My labels are checked against MY OWN open-set extractor and
the extracted noun is printed beside each row. That is a weaker check in one
respect — it cannot fail on vocabulary — and I say so rather than claiming the
stronger one.

**E8 — the thing I will most want to overstate.** If P1 and P2 both land, the
temptation is to write *the ticket was wrong*. It was wrong about the CAUSE and
right about the FIX, and those are different sentences. The remedy the ticket
forbids (`add ROW_WORDS`) stays forbidden under my correction, for a stronger
reason.

---

## 4. WHAT THIS TREE WILL NOT DO — STATED BEFORE IT IS TEMPTING

* **O4's `excludes a git revision` claim.** mg-5035 owns it. The ticket says so.
  I will not re-derive it and I will not print a number about it.
* **Editing `lib56dc`, `lib03d1`, `libbf79` or `lib70c7`.** An auditor's tree is
  its evidence. The classifier is measured here and repaired HERE, in a new
  file; the call sites in other trees are not migrated, and no transcript of
  another tree is regenerated.
* **`lib70c7.figures` delegating to `lib7522`'s** — *agreement by delegation is
  not agreement*. That is a real live item in my ticket and it is a statement
  about mg-70c7's tree, not about the classifier. I will state its status and
  measure nothing about it.

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
