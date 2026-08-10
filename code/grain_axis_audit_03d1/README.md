# mg-03d1 — INDEPENDENT AUDIT of the mg-56dc label-vs-grain repair, as mg-bf79 landed it

**This audit was PRE-FILED IN THE SAME ACTION AS ITS PARENT.** `mg-03d1` and
`mg-bf79` were created together by `pm-onethird`; `mg-03d1` declares
`Depends: mg-bf79`. It is not a reaction to what the parent found — the
questions were written before the parent had answered any of them.

`PREDICTIONS.md` was committed **before any script in this directory existed**,
at `9f1ecaa`. Seven disclosures are kept in it as **measurements**, not
laundered into predictions. `OUTCOMES.md` scores every row and **no prediction
has been revised because the result disagreed.**

---

## THE HEADLINE

**The instrument is not coarse by one word. It is coarse by construction, and
the width of the gap is measurable.**

The parent established that `rows` and `sites` are the same word to
`lib56dc._classify`. Confirmed here by running it, and then pushed one step
further, which is what the addendum asked for:

`_classify` is **two boolean membership tests returning four symbols**. Its
resolution is a property of its **arity**, not of its **vocabulary**. Over its
own 43 vocabulary words it forms **903 unordered pairs**, tells apart the
**280** cross-vocabulary ones, and **collapses all 623 within-vocabulary
pairs**. `rows`/`sites` is *one member of a class with 623 members.*

So the popular repair — *add `rows` to a new ROW_WORDS* — buys exactly one more
axis and **repairs one defect's width again**, which is the failure the
addendum named in advance. There is nowhere in a four-valued function to put a
third distinction.

**And the same limit exists one layer down, in the population rule, where
nothing had looked.** `lib56dc.count_rows` returns **one label and one grain
per printed line**. Across the arc's **517** transcripts [pop `@9f1ecaa+eacc5e1`, OBSERVED] it returns **1191**
count rows — and **246** of those rows carry a **second count inside the
label**, **626 integers in total, which are never classified at all.** They are
not mis-classified; they are outside the population. **Five** of them are at a
different grain from the row they sit on — and four of those five are in
`mg-bf79`'s own two-grain table, the very instrument it correctly identifies as
the honest one for O1:

```
      973ca61 OUTSIDE rows   ROWS  10  SITES   9  GAP
```

One line, two grains, one grain symbol. Fixing the classifier does not reach
these, because the row rule gets there first.

---

## WHAT WAS ASKED, AND THE ANSWER IN ONE LINE EACH

| # | asked | answer |
|---|---|---|
| **1** | confirm the resolution gap yourself; then **how many other axes is it blind to?** | Confirmed by running it (12 of 12 as pre-registered). **623 of its own 903 vocabulary pairs collapsed; 3 of the 6 grain axes that occur in this corpus are collapsed, and only 1 of the 6 is separated by two words it actually knows.** Of the corpus's own **400** grain words [pop `@9f1ecaa+eacc5e1`, OBSERVED], **370 classify `NONE`** — it has no entry for them, and it collapses **86.0%** of the pairs they form (**76.1%** counting only the 30 it has an entry for). |
| **2** | did P1f's blind-spot test inherit the blind spot, and is the survivor the inherited one? | **Yes, and yes.** Re-derived from `lib56dc` directly, not read off the parent's transcript: **2 flagged rows, 1 before and 1 after.** The post-repair row is `...ROWS outside it, across 10 distinct basenames` — its label states ROWS, it holds 14, and **14 is the row count**. The row is *correct*; only the classifier is confused. **Not a second defect.** Recorded and not tuned: `PREDICTIONS.md` has **exactly 1 commit**, P1g survives verbatim, `OUTCOMES.md` scores it MISS. |
| **3a** | O1 — count one loop both ways yourself | A **second enumerator** written in this directory: **0 disagreements** with `lib56dc` at both revisions. At the pinned `973ca61`: **10 ROWS / 9 SITES**. At HEAD: **14 ROWS / 12 SITES**. The parent's headline re-derives. |
| **3b** | O1 — for every printed count, the LABEL, the GRAIN, and whether they agree | Full ledger below. At HEAD **8 of 8** decidable rows agree. At `973ca61` **1 disagrees** — and it is the defect O1 names. **The label-reading instrument passes both versions.** |
| **3c** | O2 — what does the strictest self-rule range over, and what is it about? | **0 directory literals** in `published_by`. **7 → 11 artifacts, 0 lost**, re-derived. And the honest answer to *are those the same set*: **no.** It ranges over what this deliverable **authored**; it is about what this deliverable **prints**. Closer, and not the same. |
| **3d** | O3 — diff the rule set by NAME; anything else dropped? | **0 alternatives dropped**, 7 gained, `proven` present. **0 rule objects** lost: `_STRENGTH` and `MARK` are absent from `lib70c7` **by name in its own published rows**, and a drop a check asserts is not a silent one. |
| **3e** | O4 — is one copy gone, or do two remain? | **The duplication is REMOVED, not reconciled.** `lib70c7.figures` has **one statement after its docstring** and it is `return _L().figures(line)`. **1001 of 1001** inputs agree — by construction, because there is one body. The third copy, `lib56dc.figures(line, small=)`, is the **instrument**, deliberately independent. |
| **3f** | the live, reported-and-not-fixed defect | **Still live.** `figures()`'s deleted comment claimed to exclude *a git revision*; **3 of 4** candidate short revisions still read as figures. |
| **#7** | confirm the `>`-before-probe fix, **and sweep the arc** | Fix confirmed by running the parent's suite **twice**: **6 of 6 transcripts byte-identical**, then restored to committed bytes. **THE SWEEP IS THE FINDING: of 109 runners under `code/`, 86 truncate before the probe, 2 have the structural fix — the parent's and this audit's — and in 43 of them a probe of the same run reads a transcript that run has already emptied.** |
| **#8** | does the pin fix distinguish two revisions, or re-sync them? | **It distinguishes them, and the distinction is load-bearing at HEAD.** The pinned revision is `973ca61`; the transcript's current publishing commit is `eab14bc`; **they differ now.** A mismatch is declared *expected and not scored*, and what is scored instead — *does the figure still re-derive at the revision the prose pins it to* — survives republication. A re-sync would have looked identical the day it landed and been wrong today. |
| **5th** | preserve — outranks everything | **Preserved. 0 regressions.** `out_k1_census.txt`'s staleness header survives and its row still reads `DIFFERS`; **3 of 3** sites carry the note; T5d's kept miss survives verbatim; **0** of mg-56dc's transcripts were republished by mg-bf79 or by me. |

---

## THE LEDGER — LABEL, GRAIN OF THE VALUE, AGREE?

The brief's first instruction, taken literally. **The grain of the value is
never read off the label.** Every quantity the artifact could be reporting is
re-derived at HEAD by this directory's own enumerator, each tagged with the
grain of one unit of it; a printed number is then assigned the grain of
*whatever it equals*. A number that equals the row count and not the site count
**is** a row count, whatever it is called.

`out_r4_property.txt`, at HEAD:

```
 LN  LABEL                                     VALUE  LABEL-GRAIN(stage)   VALUE-GRAIN  AGREE?
 27  (site,target) ROWS naming a `*.sh`           56  row       (caps  )   row          yes
 28  distinct executing SITES behind those row    53  site      (caps  )   site         yes
 29  ...ROWS the two-name rule matches            42  row       (caps  )   row          yes
 30  ...ROWS outside it, across 10 distinct ba    14  row       (caps  )   row          yes
 31  ...distinct SITES outside it                 12  site      (caps  )   site         yes
 32  ...of those SITES, READING the exit statu     4  site      (caps  )   site         yes
 86  SITES the two-name rule found                 4  site      (caps  )   site         yes
 87  ...SITES still found under the property       4  site      (caps  )   site         yes
```

and the same artifact **at the revision the four artifacts pin**, `973ca61`:

```
 20  ...outside it, across 6 distinct basenames   10  site   (header)   row          *** NO ***
```

**The defect is visible at the pinned revision and gone at HEAD.** Note the
stage: at `973ca61` the label named **no grain of its own** — its only grain
noun (`basenames`) belonged to the embedded count — so a reader had to take the
grain from the **column header**, which offers `sites`. That is worse than a
wrong label and it is why `9` propagated into four artifacts.

---

## THE THREE THINGS THE PARENT DID NOT ESTABLISH

1. **The gap is not one word wide.** 623 collapsed pairs in the classifier's
   own vocabulary; **370 of the corpus's 400 grain words [pop `@9f1ecaa+eacc5e1`, OBSERVED] with no entry at
   all**; 3 of 6 real axes collapsed. O1 was a **sample from a class**, not a
   gap in a list.
2. **The truncate-before-probe shape is an arc-wide runner idiom.** The parent
   fixed its own and said so. **43 of 109 trees carry it live**, and only the
   parent's runner and this one have the structural fix.
3. **A count inside another count's label is in no population.** 626 integers
   across the arc; 4 of the 5 mixed-grain cases are in the parent's own
   two-grain table.

**And a note on those three numbers.** 517, 1191 and 400 are larger than the
510, 1068 and 363 the same probes printed before this tree was written, because
**this audit's seven transcripts joined the corpus it measures.** Both readings
are true of the tree they name; the committed ones are the committed run's. It
is the same shape as **AS7** below and it is stated rather than smoothed,
because a census that quietly excluded its own author is the defect this whole
arc keeps finding.

---

## AND ONE AXIS THE INSTRUMENT ASSERTS THAT IS NOT THERE

The blind spot has a mirror. `steps`/`iterations` and `commands`/`invocations`
are each one grain — a loop's steps *are* its iterations — and the classifier
splits them across SITE and EXECUTION. **2 of 5** adjudicated candidate pairs.
Adjudicated by hand with the reasoning printed, because there is no mechanical
test for *same grain* and pretending there is would be this arc's own defect.

---

## SEVEN DEFECTS OF THIS INSTRUMENT, RECORDED RATHER THAN SMOOTHED AWAY

Printed in full in `out_a6_self.txt`. In one line each:

1. **AS1 — the audited defect, run backwards by the auditor.** `label_grain`
   took the **last** grain noun of a label, so on
   `...ROWS outside it, across 10 distinct basenames` it read `basenames` — the
   *embedded* count's noun — and reported the repaired artifact as **defective
   on 2 of 8 rows where the artifact is right**. A value attributed to the
   wrong noun on the same line, which is O1. Repaired by preferring the
   CAPITALISED grain noun and returning the stage.
2. **AS2 — a population under the wrong tag is a count about somebody else.**
   A3c put my *parent's* tag `(mg-bf79)` to `published_by` and printed **9**
   under a label saying *the E1 population*. E1's population is
   `published_by('(mg-70c7)')` and is **11**. I was two minutes from reporting
   *the parent's headline 7 → 11 does not reproduce*. Both tags are printed now.
3. **AS3 — the self-rule forces my labels into the vocabulary of the instrument
   I am auditing.** `row()` requires every label to classify at stage `label`
   under `grain_of`, whose whole vocabulary is 43 words. My subject is
   distinctions it has **no word for**, and to pass my own check I must describe
   them using only words it does. **Not repaired** — the alternative is to
   exempt myself from the rule I am auditing compliance with. It is A1's finding
   happening to me.
4. **AS4 — a preservation check wrong by one character.** A5d matched
   `MISS -- 38 members`; the text says `MISS — 38 members` with an **em dash**,
   and it reported a **preserved** artifact as `*** LOST ***` — under the
   brief's own weighting, the highest-severity verdict this audit can return.
   Written from my *quotation* of the text rather than from the text. mg-aaf4
   recorded the same shape, wrong by one tense.
5. **AS5 — `grain_nouns` over-collects and is not trimmed after the fact.**
   A1d's 400 words include `about`, `actual`, `bfd`. Trimming would make the
   collapse ratio a fact about my trimming, so the vocabulary is printed whole
   and the stricter ratio is printed beside the pre-registered one. **The
   pre-registered metric is the generous one and it MISSED.**
6. **AS6 — A4b's `bites` test is a static approximation.** It asks whether any
   probe of a tree mentions `out_*.txt`, not whether *that* probe reads *the
   transcript this run truncated first*. **43 is an upper bound on a
   lower-bound question**, stated rather than defended as exact.
7. **AS7 — A4d took its subject by position and ran itself.** It picked
   `newmv[0]`, the first tree whose runner writes `.new` and moves it — which
   was the parent's **until this tree adopted the same fix**, at which point it
   was mine, alphabetically first. The probe ran its own runner, which ran the
   probe, which ran its own runner. **The population silently included the
   auditor the instant the auditor started complying with the thing being
   audited** — O2's shape a third time, in the sweep that measures O2's runner
   defect. Found by the suite's first full run wedging, not by reading.
   Repaired by *naming* the subject; and A4a now prints **both** totals,
   because excluding myself to protect prediction A4b would be the same defect
   wearing the other face.

**Seven consecutive deliverables in this lineage have now found their own
defect class in their own tooling. Three of this audit's seven — AS1, AS2 and
AS7 — are the audited defect itself, committed by the auditor.**

---

## WHAT I DID NOT DO

* **I did not repair anything.** Every finding above is reported at its
  population and grain and left in place. `p1_grain.py`'s hard-coded `1`, the
  43 truncating runners, the 626 uncounted integers and `figures()`'s false
  exclusion are **all live**. Repairing another ticket's committed transcripts
  is rewriting its evidence, and the brief's fifth item says so.
* **I did not repair the 28 labels of my own that failed the self-rule by
  changing the rule.** I reworded the labels, which is what the parent did to
  33 of its own, and recorded the cost as **AS3**.
* **I did not sweep the 43 trees for what the shape actually hid.** A4 shows
  the shape is present and that a probe of that tree reads `out_*.txt`; it does
  not open each tree and re-run it to see which labels went missing. That is a
  ticket, not a paragraph.
* **I did not test the classifier against a THIRD vocabulary.** A1b argues no
  vocabulary fixes it. That is an argument from the function's arity, not a
  measurement of a proposed fix, and it is stated as such.
* **I did not re-run the parent's whole suite as a regression gate.** A4d runs
  it twice to answer *does the `mv` converge* and restores the committed bytes.
  Where I re-derive one of its figures I say so; where I repeat one I say whose
  it is.

## A CORRECTION TO THE FRAMING — MINE, THE PARENT'S, AND THE PM'S

* **The addendum says the gap is `EXACTLY ONE DEFECT WIDE — the one it was
  pointed at`.** That is right about the *repair* and wrong about the
  *instrument*. The instrument's gap is 623 vocabulary pairs and 3 of 6 live
  axes wide. What is one defect wide is the **fix**, which is the thing the
  addendum was warning about, so the framing is right in intent and understated
  in fact.
* **The parent calls P1f's surviving 1 a defect of that probe.** It is, but the
  more useful statement is the one its own prose reaches and then steps past:
  **a label-reading test cannot audit a label.** The probe is not
  under-engineered; the method is the wrong method for the question, and the
  right one — two-grain re-derivation — is already in the same file.
* **My own PREDICTIONS.md/A1e said the classifier could express 1 of 6 axes and
  the probe says 3.** That is a MISS and it stays one. Two of the three are
  "expressible" only because one pole classifies `NONE`, which is *absence of a
  word*, not a distinction drawn. Both numbers are printed. **The refinement is
  post hoc and does not rescue the row.**

## SHAs

The refinery **rebases** before merging, so every SHA recorded here will be
displaced on `main`. **Ancestry gives a false negative after a rebase.** Where
this audit checks that a commit's content survived it uses
`git patch-id --stable`, and `out_a2_blindspot.txt` records the patch-id of the
parent's pre-registration commit so a later reader can match it by content.

## Running it

```sh
sh code/grain_axis_audit_03d1/run_all.sh
```

Pure Python 3, no dependencies, no network. **About five minutes**; the slow
part is A4d, which runs another tree's whole suite twice. **Two consecutive
runs of this suite produce 7 of 7 byte-identical transcripts** — the parent's
`.new`-and-`mv` fix, adopted here and verified on this tree as well as on
its. One probe writes and
restores — see the header of `run_all.sh`. Run it on a committed tree: A1, A3
and A5 report figures derived at HEAD.

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
