# mg-03d1 — predictions for the INDEPENDENT AUDIT of the mg-56dc label-vs-grain repair

**COMMITTED BEFORE ANY SCRIPT IN THIS DIRECTORY EXISTS.** Nothing below is
revised after the fact. A refuted prediction is a result and stays.

**This audit was PRE-FILED IN THE SAME ACTION AS ITS PARENT** (`mg-03d1` and
`mg-bf79` were created together by `pm-onethird`, and `mg-03d1` declares
`Depends: mg-bf79`). It is not a reaction to what the parent found.

---

## DISCLOSURES — measurements I had already taken when I wrote this file

These are **measurements, not predictions**, and are listed here so that nothing
below is a prediction of something I had already looked up. Laundering a
measurement into a prediction is the cheapest way to make a score look good and
it is not done here.

| # | what I had already measured or read, before writing this file |
|---|---|
| D1 | I read `lib56dc.py`'s `SITE_WORDS`, `EXEC_WORDS`, `_classify`, `grain_of`, `count_rows`, `_COUNT_ROW`. So I know by **reading** — not by prediction — that `rows`, `sites` and `basenames` are all alternatives of `SITE_WORDS`. Target 1 asks me to confirm this **by running it**, which is a different act, and A1a below is that run. |
| D2 | `SITE_WORDS` has **35** `\|`-separated alternatives and `EXEC_WORDS` has **8**. Counted with `len(pattern.split('\|'))` before writing this file. |
| D3 | `ls code/*/run_all.sh \| wc -l` = **108**. A crude grep for a `>` redirect matched **87** of them. The crude grep is not the probe and its 87 is not A4's answer. |
| D4 | I read `p1_grain.py` lines 260–365 (the P1f blind-spot test) and saw that the value printed under the label `blind-spot ROWS, PUBLISHED version` is the **literal `1`**, and that the value under `REPAIRED version` is `disagree - 1`. A2b is not a prediction that this is so; it is a prediction about **what that makes the probe do on inputs it has not been given**. |
| D5 | I read `code/runner_exit_repair_70c7/out_r4_property.txt` lines 9 and 27–33 and `out_r6_self.txt:56`. So I know the repaired labels say `ROWS` and `SITES` explicitly and that the HEAD-time figures printed there are 14 and 12. |
| D6 | I read line 30 of that transcript: `...ROWS outside it, across 10 distinct basenames  14` — a single count row carrying **two integers at two different grains**, one of them inside the label. AF below is a prediction of **how many** such rows exist, not of whether any does. |
| D7 | I read `mg-bf79`'s `OUTCOMES.md` in full, including its scored table and its eight self-reported defects. Every prediction below that overlaps a row of that table is written to be **re-derivable independently**, and I say in each case whether I am re-deriving or repeating. |

---

## A1 — THE CLASSIFIER'S AXES (target 1; the deliverable)

| id | prediction |
|---|---|
| **A1a** | Put to `lib56dc._classify` **at run time**, each of `rows`, `basenames`, `sites`, `lines`, `files`, `items`, `members`, `columns` returns **`SITE`**, and each of `executions`, `runs`, `invocations`, `iterations` returns **`EXECUTION`**. **12 of 12** as stated. |
| **A1b** | `_classify`'s output alphabet is exactly **4** symbols (`EXECUTION`, `SITE`, `BOTH`, `NONE`). It is built from **2** independent boolean tests, so it carries **at most 2 bits** and can express **exactly one grain distinction**: source-side vs run-side. Every distinction **within** either vocabulary is inexpressible **by construction**, not by an omission that a longer word list could fix. |
| **A1c** | Quotienting the classifier's own vocabulary: the **35** `SITE_WORDS` alternatives collapse to **1** cell and the **8** `EXEC_WORDS` alternatives collapse to **1** cell, so of the `C(43,2) = 903` pairwise distinctions between its own vocabulary words it can express **exactly the 280 cross-vocabulary ones** (35 × 8) and **0** of the 623 within-vocabulary ones. **I predict 903 / 280 / 623 exactly.** |
| **A1d** | Over every `out_*.txt` in `code/*/` I will extract the grain nouns actually used on count-row labels. I predict **at least 60 distinct grain nouns** occur, and that the classifier assigns **at most 4** distinct values to them, so it collapses **≥ 93%** of the distinctions that occur. |
| **A1e** | The grain distinctions that actually occur in this corpus include at least these **six axes**: `row / site`, `file / line`, `item / class`, `pair / poset`, `occurrence / name`, `site / execution`. I predict the classifier can express **exactly 1 of the 6** (`site / execution`) and **0 of the other 5** — and that for each of the other five, **both poles land in `SITE_WORDS`**, so each is a `SITE`-vs-`SITE` collapse of the same kind as O1's. |
| **A1f** | *The prediction I most expect to be refuted.* There is **at least one axis whose two poles straddle the classifier's own boundary in the wrong place** — i.e. a pair of words at the SAME grain where one is a `SITE_WORD` and the other is an `EXEC_WORD`, so the classifier reports a distinction that is not there. I predict **≥ 1** such pair and **≤ 6**. |

## A2 — P1f's BLIND-SPOT TEST (target 2)

| id | prediction |
|---|---|
| **A2a** | Re-running `p1_grain.py` at my HEAD reproduces the parent's reported shape: `blind-spot ROWS, both versions summed` = **2**, printed as **1** published and **1** repaired. |
| **A2b** | The **published `1` is a hard-coded literal and the repaired value is derived from it by subtraction**, so the probe cannot report a published count it did not already assume. I predict I can exhibit an input on which the three printed values are **mutually inconsistent**: with `disagree == 0` it prints `PUBLISHED 1`, `REPAIRED 0`, `SUMMED 0`, and **1 + 0 ≠ 0**. I will demonstrate this by re-executing the probe's own printing arithmetic over `disagree ∈ {0,1,2,3}` rather than by editing the repo, and predict **exactly 1 of those 4 inputs is inconsistent**. |
| **A2c** | The surviving post-repair disagreement is **the inherited one and not a second defect**: the row `p1_grain.py` selects after the repair is the first label matching `/outside/i`, its label contains the word **`ROWS`**, and the value it holds **is** the row count at that revision. So the row is **correct** and the test flags it only because `rows` and `basenames` classify `SITE`. **Not a second unrelated defect.** |
| **A2d** | The parent **recorded rather than tuned**: `PREDICTIONS.md` (committed at `bba2a3c`, before any script existed) contains the P1g prediction in its unrevised form, `git log` shows `PREDICTIONS.md` has **exactly 1** commit touching it, and `OUTCOMES.md` scores P1g **MISS**. I predict 1 commit and a scored MISS. |

## A3 — THE FOUR, AT THE STATED POPULATIONS AND GRAINS (target 3)

| id | prediction |
|---|---|
| **A3a** | **O1.** With a `(site, target)` enumerator **written from scratch in this directory**, sharing no code with `lib56dc`, I re-derive the outside-the-two-names census at HEAD and get **the same ROW count and the same SITE count** as `lib56dc.exec_site_rows`/`exec_sites` — **0 disagreements**. The gap `ROWS − SITES` at HEAD I predict is **2**. |
| **A3b** | **O1 label/grain ledger.** Across the four artifacts that publish this figure, **every** count row that holds the row value carries `ROWS` on its own label and **every** row that holds the site value carries `SITES`, at classifier stage `label`. **0 rows** where the label's declared source-side noun contradicts the re-derived value's grain. |
| **A3c** | **O2 (the self-rule).** The strictest self-rule now ranges over a population defined by **a git property, with no directory literal in the function body**, and its size at HEAD is **11 or more**. I predict **≥ 11** and that a grep of the population function's own source for the string `runner_exit_repair_bf79` finds **0**. |
| **A3d** | **O3 (the consolidation).** A by-name diff of the two rule sets finds **0** rule objects dropped besides the `proven` that mg-dee4 named, and **exactly 1** alternative dropped. I am **re-deriving** the parent's P3b here, not repeating it. |
| **A3e** | **O4 (`figures()`).** **3** definitions of `figures` remain reachable in `code/*/lib*.py`. `lib70c7.figures` **calls** `lib7522.figures` — so the duplication is removed **by delegation, not by deletion**, and there is exactly **1 implementation body** between them. I predict over inputs `0..1000` rendered as text, `lib70c7.figures` and `lib7522.figures` agree on **1001 of 1001**. |
| **A3f** | **O4, the live defect.** `figures()`'s comment claims to exclude *a git revision* and does not. I predict `figures` returns a non-empty result for the all-decimal 7-character token `1234567` — i.e. **an all-decimal short revision still reads as a figure at HEAD**. Still live, unfixed, and correctly reported as such. |

## A4 — THE `>`-BEFORE-PROBE SWEEP (parent defect #7; the parent fixed its own and did not sweep)

| id | prediction |
|---|---|
| **A4a** | Of the **108** `run_all.sh` under `code/*/`, I predict **≥ 90** redirect a probe's stdout onto a tracked transcript with a plain `>`, which truncates before the probe runs. |
| **A4b** | **Exactly 1** — `runner_exit_repair_bf79`'s — writes `.new` and `mv`s. The parent fixed its own and did not sweep, so I predict **1**. |
| **A4c** | The number that matters is not A4a: it is how many of the truncating runners contain a probe that **reads its own tree's `out_*.txt`**, which is where the shape actually bites. I predict that number is between **6 and 30**, and **≥ 1** of them is a tree whose probe's whole job is a census over transcripts. |
| **A4d** | The `mv` fix **converges**: running `run_all.sh` in `runner_exit_repair_bf79` twice in a row leaves the second run's transcripts byte-identical to the first run's for **≥ 4 of the 6** transcripts (P1/P4 quote HEAD-derived figures and my HEAD differs from the parent's, so I do not predict 6 of 6). |

## A5 — "A PUBLISHER IS NOT A PIN" (parent defect #8)

| id | prediction |
|---|---|
| **A5a** | The fix **distinguishes the two revisions rather than merely re-syncing them**: `p1_grain.py` at HEAD both (i) derives a transcript's publishing commit with `git log -1 -- <path>` and (ii) carries a separate constant for *the revision the figure is a fact about*, and prints **both**. I predict **both** appear and are **used for different questions**. |
| **A5b** | The four artifacts state *the revision this figure is a fact about* and **do not claim to name a publishing commit**. I predict **4 of 4**. |
| **A5c** | And the check that separates a real fix from a re-sync: the two revisions are **currently different** for at least one of the four artifacts — i.e. the publishing commit has already moved away from the pinned one — so the distinction is **load-bearing at HEAD and not merely stated**. I predict **≥ 1 artifact where they differ**, and **this is the prediction I expect to be closest**. |

## AF — THE FLOOR ITEM NOTHING IN THE BRIEF NAMES

**A count printed *inside another count's label* is invisible to the census that
claims to cover every printed count.** `_COUNT_ROW` yields **one grain per
line**, and a line like `...ROWS outside it, across 10 distinct basenames  14`
carries **two** counts at **two** grains — `basenames` and `ROWS`. The classifier
assigns the line a single grain, so the embedded count is never classified at
all: it is not a mis-classified count, it is a count **outside the population**.
That is O2's shape (a population that excludes part of what it is about) sitting
inside the instrument that measures O1.

| id | prediction |
|---|---|
| **AFa** | Across every `out_*.txt` under `code/*/`, the number of count rows whose **label** contains a digit — i.e. rows carrying an unclassified second count — is **≥ 200**. |
| **AFb** | Within `runner_exit_repair_bf79`'s own six transcripts the number is **≥ 3 and ≤ 40**. |
| **AFc** | At least **1** such row has an embedded count whose grain noun classifies **differently** from the row's own grain, so the single grain the instrument reports for that line is wrong for one of the two numbers on it. I predict **≥ 1**. |
| **AFd** | This is **not** a restatement of the parent's defect #5 (P1f inherits its blind spot). #5 is about a *classified* row the classifier cannot resolve; AF is about a count that is **never classified**. I predict the parent's `p5_self.py` reports **0** findings of the AF shape, because its population is `count_rows` too. |

## AS — THIS AUDIT'S OWN TOOLING

| id | prediction |
|---|---|
| **ASa** | This instrument contains **≥ 1** instance of the defect class it audits, found by my own `a6_self.py`, recorded rather than smoothed away. Five consecutive deliverables in this lineage found one; the sixth found eight. |
| **ASb** | **Every count row this tree prints names its population and its grain**, and my own self-check finds **0** rows at classifier stage `header` or `-` on the final committed run. I predict this costs me at least one rewriting pass, as it cost the parent 33 labels. |
| **ASc** | Exit codes on the final committed run: `selftest03d1.py`, `a1`–`a6` all exit **0**. **7 of 7.** |
| **ASd** | **At least one prediction in this file will MISS.** |

---

## WHAT THIS AUDIT WILL NOT ESTABLISH

* It will not establish that the classifier is *repairable by a longer word
  list*. A1b predicts the opposite — the limit is the arity of the output, not
  the size of the vocabulary — and if A1b holds then every "add `rows` to a new
  ROW_WORDS" fix repairs exactly one defect's width again, which is what the
  addendum warns against.
* It will not re-run the parent's whole suite as a regression gate. Where I
  re-derive one of its figures I say so; where I repeat one I say whose it is.
* **SHAs.** The refinery rebases before merging, so any SHA the parent recorded
  will differ on `main`. Ancestry gives a **false negative** after a rebase.
  Where this audit checks that a commit's content survived, it checks
  `git patch-id --stable`, not `merge-base --is-ancestor`.
