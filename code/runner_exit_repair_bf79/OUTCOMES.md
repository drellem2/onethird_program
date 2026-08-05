# mg-bf79 — outcomes

`PREDICTIONS.md` was committed **before any script in this directory existed**.
Every figure below is printed by a probe in this directory next to the predicate
that produced it; the transcripts are committed. **Seven of the 26 scored rows
carry a miss, and none has been revised.** A refuted prediction is a result.

---

## Predictions, scored

| id | prediction | outcome |
|---|---|---|
| **P1a** | which was wrong: the **COUNT**, not the label; 9 is the site count; the repair prints both grains and leaves every `9` in prose standing | **HIT** — 9 SITES / 10 ROWS at `973ca61`, re-derived under `lib56dc`'s enumerator. Every `9` in prose stands |
| **P1b** | at `973ca61`, **9 distinct SITES and 10 ROWS** outside the two names | **HIT** — exactly, and the publishing commit is **derived** with `git log -1 -- <transcript>` and checked against the constant rather than named by hand |
| **P1c** | the row/site gap is **exactly 1 at every revision this probe reads**, not 0 and not 2, and the one line responsible is `selftestc2b3.py:155` | **PART HIT, PART MISS.** True of the **OUTSIDE** column at both revisions — the column the four artifacts publish. **FALSE of the ALL column, where the gap is 2 at both revisions** and `k2_consume.py:456` is equally responsible. It was already there at the publishing commit; I had not looked at the column I was not quoting. **This is mg-56dc/T1c's own recorded mistake — *I predicted a number for a column that has no stable value* — made again in the repair of it** |
| **P1d** | at HEAD both counts are strictly larger; **outside ROWS ≥ 12** and outside SITES = outside ROWS − 1 | **PART HIT, PART MISS.** Strictly larger — HIT (10→11 rows, 9→10 sites). **≥ 12 — MISS, it is 11.** The second half HIT: SITES = ROWS − 1. I predicted a threshold for a moving census from its direction of travel, which is a smaller version of the same error as P1c |
| **P1e** | **4 of 4** artifacts end up stating `9`, the word `sites` and a revision | **HIT** — 4 of 4, under a window of one line **in both directions applied to both conjuncts**, which took two goes and is recorded as defect 2 |
| **P1f** | the classifier over the whole repaired transcript: **0** rows `NONE`, **0** rows whose grain is header-only | **HIT** — 0 and 0, over 11 count rows; and 11 of 11 are at stage `label`, against 3 of 8 at `label` in the published version |
| **P1g** | ≥ 1 row where label-grain and re-derived value-grain differ **before** the repair and **0 after** | **MISS — 1 before and 1 after.** And the reason outranks the prediction: **the classifier's axis is SITE-vs-EXECUTION and O1 is ROW-vs-SITE, a distinction below its resolution.** `rows`, `basenames` and `sites` all classify SITE. It is 1 after because the row the test picks is labelled `ROWS`, holds the row value, and is **correct** — the test cannot tell it from the row it was built to catch. **P1f's test inherits the blind spot it measures** |
| **P1h** | mg-70c7's R5a stays **HIT**; no prediction verdict anywhere in this repository is changed | **HIT** — R5a said *sites* and the site count is 9; what was wrong was the transcript it cited. 0 verdicts changed |
| **P2a** | the old E1 population is `M.outs(M.TREE)` = **7** | **HIT** |
| **P2b** | the repaired population is defined by a **property** over the whole repository with **11** members: 7 transcripts, README, OUTCOMES, PREDICTIONS and the published document | **HIT** — 11, exactly those, derived by `--diff-filter=A` provenance with **no directory named anywhere in the function** |
| **P2c** | the old population is a **strict subset**; **0** lost | **HIT** |
| **P2d** | widening finds **≥ 1** count row in mg-70c7's own prose with no grain word, and the number is between **1 and 12** | **MISS — 0.** And it is **mg-56dc's own T2a miss, repeated by the ticket repairing it**: its OUTCOMES says *I reasoned that prose unchecked by a rule would fail it. It does not.* I read that sentence, listed it under what was already run, and predicted the same number for the same wrong reason. **A rule that is not run has not passed** — that is a statement about REACH, and predicting a DEFECT COUNT from it is a different claim |
| **P2e** | `r6_self.py` exits **1 on the first run** after the widening and **0** on the final one | **MISS — 0 on the first run.** It did exit 1 for exactly one run, and the cause was **not the widening**: the repaired README named a revision and E2's `figures()` read the seven-digit revision as a figure no transcript backs. Neither run is the `1` predicted |
| **P3a** | restoring `proven` takes `MARK` from **9** to **10**, exactly mg-dee4's D4 union | **HIT** — 9 → 10, and 10 = mg-dee4's published `9 subject + 1 self-only` |
| **P3b** | the by-name diff finds **0** rule objects dropped and **exactly 1** alternative dropped — *the prediction I most expect to be refuted* | **HIT.** 1 alternative, 0 rule objects — `_STRENGTH` and `s3_figure.MARK` are absent **by name in mg-70c7's own R3a rows**, and a drop a check asserts is not a silent one. And **0 gained**, confirmed behaviourally: 20 probe words, 0 reached by one rule and not the other |
| **P3c** | `proven` occurs ≥ 1 time, **every** occurrence classifies MENTION, so restoring it adds **0** violations and **0** committed transcript numbers change | **PART HIT, PART MISS.** 2 occurrences, 2 MENTIONs, **0** new violations — HIT. **0 numbers change — MISS: 3 move** under the controlled counterfactual. The inference was *every occurrence is a MENTION, therefore nothing moves*, and **it does not follow: a MENTION is still COUNTED, and `MENTIONs` is a printed row.** A rule that reaches one more string reaches it in the mention column too |
| **P4a** | exactly **1** implementation of `figures()` reachable from either library; `lib70c7.figures` **calls** `lib7522.figures` | **HIT** — 1 each, 1 body line each, delegation read out of the source with the docstring stripped |
| **P4b** | over 0..500 the disagreements go from **1** (the value `3`) to **0** | **HIT** — 1 → 0, and the third parameterised copy agrees with each subject copy at its own constant, which is what makes the comparison independent of both |
| **P4c** | unifying them **changes at least one number in a committed transcript of mg-70c7**, because R3c compares a `lib70c7`-computed count against a `lib7522`-computed one | **PART HIT, PART MISS. The claim is HIT and the REASON is a MISS.** `out_r2_anchor.txt`'s *distinct figures they print* goes **94 → 95** at a fixed corpus, the added figure being `3`. But **R3c's four counts do not move at all** — the value `3` never lands in a claim window in that population. Right answer, wrong mechanism; a prediction whose reason is wrong would have been wrong on a different repository, so it is not scored HIT |
| **PFa** | `alternatives()` is a **second rule kept in two copies**, and a by-name census finds **≥ 6** names defined in both libraries | **HIT** — 15, of which 6 are byte-identical after unparsing |
| **PFb** | the two `alternatives()` **agree on every input tested**; 0 disagreements | **HIT, and stronger than predicted** — their bodies are **identical**, so they agree by construction and the behavioural test over 9 regex sources is a formality rather than evidence. That is also why unifying them changes nothing |
| **PFc** | I will make `lib70c7.alternatives` call `lib7522.alternatives`, and **not** touch `lib56dc`'s third copy | **HIT** — and the third copy is not merely untouched, it is the **instrument**: `lib56dc.figures(line, small=)` is the only one of the three that can measure the other two without being either |
| **P5a** | this tree contains a defect of the class it repairs, found by its own `p5_self.py`, recorded rather than smoothed away | **HIT — six of them**, listed in `README.md` and in `out_p5_self.txt` |
| **P5b** | every count row this tree prints carries a grain word **on its own label**; **0** rows at stage `header` or `-` | **HIT — but only after the check made me rewrite 33 of my own labels**, which is the interesting half. The first run reported 33 of 103 rows at `prev` or `header`, including a two-grain table whose grain lived in its **column header** — the `header` stage, the defect this ticket repairs. That table is **transposed** so the grain is the row. 103 of 103 at `label` now |
| **P5c** | `selftestbf79.py`, `p1`–`p5` all exit **0** on the final committed run: **6 of 6** | **HIT** — 6 of 6 |
| **P5d** | **at least one prediction in this file will MISS** | **HIT — seven rows carry a miss.** P1c, P1d, P3c and P4c in part; P1g, P2d and P2e in whole. And the most useful of them is P1g, which was written expecting to catch a classifier error and instead measured a vocabulary gap |

**Score: 19 HIT, 4 PART HIT / PART MISS, 3 MISS**, out of 26 scored rows.
Seven rows carry a miss in whole or in part: P1c, P1d, P1g, P2d, P2e, P3c, P4c.

---

## The one thing a prediction did not anticipate at all

**That the instrument the brief sent me to run over the whole artifact cannot see
the defect it was sent to check.** `PREDICTIONS.md` says, under *what this repair
will NOT establish*, that the classifier reads labels and *a wrong label makes it
confidently wrong* — which is right in shape and wrong in mechanism. It is not
that the classifier is fooled by a wrong label. It is that **`rows` and `sites`
are the same word to it**, so the label O1 is about is not wrong in a dimension it
has. P1g was written expecting to catch a classifier error and instead measured a
vocabulary gap. That is the finding this deliverable would most want an auditor to
attack.

---

## Six defects of this instrument, recorded rather than smoothed away

Summarised in `README.md` and printed in full in `out_p5_self.txt`. In one line
each:

1. the provenance query's `\(` was a **BRE group**, so the population silently
   became my auditor's artifacts as well as mine — 15 where 11 was meant;
2. the revision-and-grain check was **line-local twice**, which is mg-dee4's F4
   reproduced while checking that mg-70c7 had repaired it;
3. the alternative diff compared **regex source against prose rendering** and
   reported 3 phantom gains;
4. the moved-numbers claim **attributed arc drift to this ticket** until a
   controlled counterfactual separated 3 from 5 — mg-56dc's own defect #1;
5. **P1f's blind-spot test inherits the blind spot it measures**;
6. the T2 fixture was **invisible to its own `git ls-files` population**, which is
   `lib70c7.outs()`'s recorded defect from the other side.

**Five consecutive deliverables in this lineage had found their own defect class
in their own tooling. This is the sixth, and the count went up.** That is a
property of writing the disclosure section before you are sure it will be short.

---

## Reported and not fixed

* **`figures()`'s stated exclusion of "a git revision" is false** and always was.
  Not fixed: over 451 transcripts, a magnitude rule would drop 25 genuine figures
  and a resolves-as-an-object rule would drop 6 for an accident of the object
  database. `selftestbf79.py` asserts the false exclusion **as false**, so a later
  fix turns that row red and names itself.
* **`captured_var` is mg-dee4's F6 value arm kept in two identical copies.** Out of
  scope — O4 names `figures()`, and `captured_var` is reached by probes whose
  transcripts this ticket does not regenerate.
* **mg-56dc's README cites `6aa043a` for its predictions commit and that commit is
  not reachable from HEAD** (the reachable counterpart is `abb95b0`). Observed in
  `PREDICTIONS.md` before any script existed and **not repaired**: an audit's tree
  is its evidence, and this ticket closes four of that audit's five findings.
