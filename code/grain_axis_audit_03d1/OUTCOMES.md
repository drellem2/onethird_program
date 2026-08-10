# mg-03d1 — outcomes

`PREDICTIONS.md` was committed at `9f1ecaa`, **before any script in this
directory existed**. Every figure below is printed by a probe in this directory
next to the predicate that produced it, and the transcripts are committed.
**Seven of the 31 scored rows carry a miss, and none has been revised.**
A refuted prediction is a result.

The seven disclosures (D1–D7) in `PREDICTIONS.md` are **measurements**, not
predictions, and are not scored. They are there so no row below is a prediction
of something I had already looked up.

---

## Predictions, scored

| id | prediction | outcome |
|---|---|---|
| **A1a** | `rows`/`basenames`/`sites`/`lines`/`files`/`items`/`members`/`columns` → `SITE`; `executions`/`runs`/`invocations`/`iterations` → `EXECUTION`. **12 of 12** | **HIT** — 12 of 12, by running `_classify` rather than reading `SITE_WORDS`. The addendum asked for the run and this is the run |
| **A1b** | 4 output symbols from 2 boolean tests; **exactly one** grain distinction expressible; every within-vocabulary distinction inexpressible **by construction** | **HIT** — 4 symbols reached by probe strings, 2 membership tests in the body. This is the finding the rest of A1 measures the size of |
| **A1c** | over the classifier's own 43 vocabulary words: **903** pairs, **280** told apart, **623** collapsed | **HIT — 903 / 280 / 623 exactly.** `rows`/`sites` is one member of a 623-member class, which is why a word-list fix repairs one defect's width again |
| **A1d** | ≥ **60** distinct grain words in the corpus; classifier collapses **≥ 93%** of the distinctions that occur | **PART HIT, PART MISS.** **400 distinct grain words over 1191 count rows in 517 transcripts [pop `@9f1ecaa+eacc5e1`, OBSERVED] — HIT, nearly seven times the floor.** **93% — MISS, it is 86.0%.** And the reason is mine: the metric I pre-registered counts a `SITE`/`NONE` pair as *told apart*, and `NONE` is not a grain — it is *I have no word for this label*. The stricter reading, over only the 30 words it has an entry for, is printed beside it and gives 76.1%. **The generous metric is the pre-registered one and it missed; the strict one does not rescue it** |
| **A1e** | of the 6 grain axes that occur in this corpus, the classifier expresses **exactly 1** and collapses 5, with **both poles in `SITE_WORDS`** for each collapse | **MISS — 3 of 6 expressible, 3 collapsed.** Two of the three "expressible" are expressible only because one pole classifies **`NONE`** (`species`, `names` are not words it knows), which is *absence of a word*, not a distinction drawn. Counted that way it is **1 of 6**, and that count is **post hoc and printed as such**. The pre-registered figure was 1 against a metric that gives 3 |
| **A1f** | *the one I most expected to be refuted* — **≥ 1 and ≤ 6** word pairs at the SAME grain split across the two vocabularies, so the classifier asserts a distinction the words do not carry | **HIT — 2 of 5 adjudicated candidates.** `steps`/`iterations` and `commands`/`invocations`. Adjudicated by hand with the reasoning printed, because there is no mechanical test for *same grain* and pretending there is would be this arc's own defect |
| **A2a** | re-running P1f's logic reproduces **2 summed, 1 before and 1 after** | **HIT** — re-derived against `lib56dc` directly rather than read off the parent's transcript |
| **A2b** | the published `1` is a **literal** and the repaired value is derived from it by subtraction; **exactly 1** of the inputs 0..3 makes the three printed rows contradict | **HIT — 1 of 4, at `disagree == 0`.** Which is **the input a successful repair would produce**: had the blind spot closed, the probe would have printed `PUBLISHED 1, REPAIRED 0, SUMMED 0` and reported a published defect it had just measured as absent. Demonstrated by re-executing the probe's own printing arithmetic, not by editing the subject |
| **A2c** | the survivor is the **inherited** one — label states ROWS, value **is** the row count — and not a second defect | **HIT** — `...ROWS outside it, across 10 distinct basenames`, holding 14, and 14 is the row count. The row is correct; the classifier calls it `SITE` because `rows` and `basenames` are both `SITE_WORDS` |
| **A2d** | recorded rather than tuned: **exactly 1** commit touches the parent's `PREDICTIONS.md`, its subject begins `predictions:`, P1g survives verbatim, `OUTCOMES.md` scores it MISS | **HIT — 1 commit, all four conditions.** Checked in the history, not in the prose. The patch-id of that commit is recorded in `out_a2_blindspot.txt` so a later reader can match it by content after the rebase that will displace its SHA |
| **A3a** | a second enumerator written here agrees with `lib56dc` on **0** disagreements at both grains; the `ROWS − SITES` gap at HEAD is **2** | **HIT** — 0 disagreements at `973ca61` and at HEAD; **10 ROWS / 9 SITES** at the pin and **14 / 12** at HEAD; gap 1 and 2. The parent's headline re-derives under an instrument that is not its own |
| **A3b** | across the artifacts, **0 rows** where the label's declared source-side noun contradicts the re-derived value's grain | **HIT at HEAD — 8 of 8 decidable rows agree — and the pinned revision shows 1**, which is the point: the ledger is measuring the thing, not passing everything. And the pinned row's stage is `header`, not `caps`: its label named **no grain at all** and the reader had to take one from the column header. That is worse than a wrong label |
| **A3c** | the repaired population is defined by a git property with **0** directory literals in the function and **≥ 11** members | **HIT — 0 literals, 7 → 11 with 0 lost**, re-derived. And the honest half: *ranges over* is what the deliverable **authored** and *is about* is what it **prints**, and those are still not the same set |
| **A3d** | **0** rule objects dropped besides the `proven` mg-dee4 named; **exactly 1** alternative dropped | **PART HIT, PART MISS.** 0 rule objects — HIT. **1 alternative dropped — MISS: 0 dropped and 7 gained**, measured `MARK` against `MARK_OLD` by name. I predicted the parent's own P3b figure without re-deriving which two objects it had differenced; the parent's 1 is a diff of `lib70c7`'s pre-consolidation rule against `lib7522`'s, mine is `MARK_OLD` against `MARK`. **Two different questions, and I predicted the answer to the other one** |
| **A3e** | **3** definitions of `figures` remain; `lib70c7.figures` **calls** `lib7522.figures`; **1001 of 1001** inputs agree | **HIT** — 3 definitions, one statement after the docstring in `lib70c7`, 1001 of 1001. **The duplication is removed, not reconciled**: agreement is by construction because there is one body, so the two cannot drift on a later edit. That is the distinction the brief asked for |
| **A3f** | `figures()` still reads an all-decimal short revision as a figure — **live** | **HIT — 3 of 4** candidate revisions read as figures. Reported-and-not-fixed by the parent, and still so |
| **A4a** | **≥ 90** of the 108 runners redirect with a plain `>` | **MISS — 86**, and the denominator moved to **109** because this audit's own runner joined the population. Predicted from the crude grep in disclosure D3 and rounded the wrong way; 21 runners redirect nothing at all. The miss is small and the population is the point |
| **A4b** | **exactly 1** runner writes `.new` and `mv`s it | **PART HIT, PART MISS — the named tree is right and the count is 2.** It was 1 when I pre-registered it, and became 2 when **this tree adopted the parent's fix in its own runner** — the auditor joined the set it was counting. Both totals are printed; **excluding myself to protect the prediction would be the population defect this arc keeps recording.** The same entry cost me a wedged suite: see AS7 |
| **A4c** | the number that matters — truncating runners whose own probes read `out_*.txt` — is between **6 and 30** | **MISS — 43, above the range.** I predicted a defect count from one instance, which is mg-56dc's T5d error and mg-bf79's P2d error, made a third time by the ticket auditing both. **43 of 108 runners carry the shape live** and it is an arc-wide runner idiom, not one script's slip |
| **A4d** | the `mv` fix converges: **≥ 4 of 6** transcripts byte-identical across two consecutive runs | **HIT, and stronger — 6 of 6.** Run twice at a fixed tree and then restored to committed bytes, with the restore asserted |
| **A5a** | the fix **distinguishes** the two revisions rather than re-syncing them: both derived, both printed, each used for its own question | **HIT — 4 of 4 structural checks.** The one that settles it is that a mismatch is declared **expected and not scored**; a re-sync would go red the next time anything republished the transcript |
| **A5b** | the four artifacts state *the revision this figure is a fact about* and do not claim to name a publishing commit | **HIT — 4 of 4** |
| **A5c** | *the one I expected to be closest* — the two revisions **currently differ** for ≥ 1 artifact, so the distinction is load-bearing at HEAD | **HIT** — pinned `973ca61`, publishing commit `eab14bc`. They differ now, so the fix is doing work rather than waiting to |
| **AFa** | ≥ **200** count rows arc-wide carry an unclassified second count inside the label | **HIT — 246 rows, 626 integers** across 517 transcripts [pop `@9f1ecaa+eacc5e1`, OBSERVED]. `every printed count` is short by 626 |
| **AFb** | between **3 and 40** such rows in the parent's own six transcripts | **HIT — 8** |
| **AFc** | **≥ 1** row whose embedded count is at a different grain from the row's own | **HIT — 5, and four of them are in `out_p1_grain.txt`** — the parent's own two-grain table, which is the instrument it correctly identifies as the honest one for O1. One line, two grains, one grain symbol |
| **AFd** | this is **not** the parent's defect #5, and its `p5_self.py` reports **0** findings of the AF shape, because its population is `count_rows` too | **HIT** — by construction and by absence. #5 is a *classified* row the classifier cannot resolve; AF is a count that is **never classified**. A self-check inherits the population rule of the check it applies, so the one thing it cannot find is a defect **of that rule** |
| **ASa** | **≥ 1** defect of the audited class in my own tooling, found by my own probe, recorded rather than smoothed away | **HIT — seven of them**, in `README.md` and `out_a6_self.txt`. **Three are the audited defect exactly**: AS1 attributed a value to the wrong noun on the same line, AS2 printed a population under the wrong tag, and AS7's population silently swallowed the auditor |
| **ASb** | **0** count rows of mine at classifier stage `header` or `-` on the final committed run, at the cost of at least one rewriting pass | **HIT — 0 on the final committed run, and it cost 28 of my own labels a rewrite**, one of them twice. Recorded as **AS3**: passing this check obliges me to describe grain distinctions the classifier has no word for **using only words it does have**. Not repaired, because the alternative is exempting myself from the rule I am auditing compliance with |
| **ASc** | `selftest03d1` and `a1`–`a6` all exit **0**: **7 of 7** | **MISS — 6 of 7.** `a4_sweep.py` exits **43**, its own finding count, by design. I pre-registered the exit codes before deciding what A4's exit code would *mean*, and a probe whose non-zero exit is how it reports findings cannot be predicted to exit 0. **The same shape as mg-56dc's own exit-code miss: reasoning about a probe's verdict from the part of it I was about to write** |
| **ASd** | at least one prediction in this file will MISS | **HIT — seven rows carry a miss.** A1d, A3d and A4b in part; A1e, A4a, A4c and ASc in whole |

**Score: 24 HIT, 3 PART HIT / PART MISS, 4 MISS**, out of 31 scored rows.
Seven rows carry a miss in whole or in part: **A1d, A1e, A3d, A4a, A4b, A4c,
ASc**.

---

## The most useful miss

**A4c.** I predicted between 6 and 30 trees where the truncate-before-probe
shape bites and there are **43**. I predicted it from the one instance in front
of me — the parent's own tree — which is exactly the error mg-56dc records as
T5d (*I predicted from the one instance in front of me*, 2–8 against 38) and
mg-bf79 records as P2d. **Three consecutive tickets in this lineage have
predicted a population size from an instance, and this one did it while
auditing the other two for it.**

## The one thing no prediction anticipated at all

**That the row rule, not the classifier, is the binding constraint.**
`PREDICTIONS.md`/A1b predicted the classifier's limit was its arity rather than
its vocabulary, which held. What it did not see is that `count_rows` has the
*same* shape of limit one layer down — **one label and one grain per line** —
so a line carrying two counts at two grains is not a hard case for the
classifier, it is a case the classifier is never shown. **626 integers arc-wide
are in no population**, and four of the five that are demonstrably at a
different grain from their own row are in the parent's own two-grain table.
Repairing `_classify` would not reach a single one of them.

## Reported and not fixed

* **`p1_grain.py`'s `blind-spot ROWS, PUBLISHED version` is the literal `1`**,
  and the `REPAIRED` value is that literal subtracted from the measurement. On
  `disagree == 0` the three rows contradict each other. Live, and not repaired
  here: the parent's transcripts are its evidence, not my worksheet.
* **43 runners carry the truncate-before-probe shape.** Live. Fixing them would
  rewrite 43 trees' committed transcripts, every one of them another ticket's
  evidence.
* **626 integers arc-wide are printed inside labels and classified by nothing.**
  Live. It is a defect of the population rule, and the population rule's
  docstring defends itself well; what it does not do is state the cost, which is
  this number.
* **`figures()`'s stated exclusion of *a git revision* is false and always was.**
  Live, as the parent reported. `selftest03d1.py` asserts it **as false**, so a
  later real fix turns that row red and names itself.
* **`singular('species') == 'specy'`.** My own de-pluraliser is crude; the
  self-test asserts the wrong answer rather than deleting the case, so the
  crudeness stays visible to a reader of `out_selftest_03d1.txt`.

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
