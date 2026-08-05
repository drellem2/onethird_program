# mg-bf79 — predictions, written before any script of this repair exists

This file is committed **before** `libbf79.py`, before any `p*.py`, before
`run_all.sh` and before a single transcript of this tree exists. The order is
checkable from `git log`: the commit carrying this file is the one whose subject
begins `predictions: mg-bf79`, and no other commit of this tree precedes it.

**An independent audit of this repair is already filed and waiting on it**
(`mg-03d1`, `Depends: mg-bf79`, filed in the same action as `mg-bf79` itself).
So these predictions are written to be **refuted**, not to be right. A
prediction that turns out wrong is scored **MISS** in `OUTCOMES.md` and is
**never revised here**.

---

## What was already run before this file was written — the full list

Nothing in this directory has been executed, because nothing in it exists. What
*has* been run against the repository, in this order, is:

1. `mg show mg-bf79`, `mg show mg-03d1` — the brief and the pre-filed audit.
2. `git log --oneline --all --grep='mg-56dc'` and `--grep='mg-70c7'`,
   `git show --stat` on `d456f58` and `973ca61` — to see what a repair ticket in
   this lineage touches.
3. `git merge-base --is-ancestor <c> HEAD` for eight commits, and
   `git log -1 --format='%H %s' -- code/runner_exit_repair_70c7/out_r4_property.txt`.
   **Three results from that plumbing are already known and are therefore not
   predicted below:** `973ca61` **is** an ancestor of HEAD and **is** the
   publishing commit of `out_r4_property.txt`; `d456f58` is an ancestor;
   and `6aa043a` — the commit `code/runner_exit_audit_56dc/README.md` cites as
   the one that carries its predictions — is **NOT** an ancestor of HEAD, its
   reachable counterpart being `abb95b0`.
4. Reading, with no execution: `lib70c7.py`, `r4_property.py`, `r6_self.py`,
   `out_r4_property.txt`, `lib7522.py` (the `MARK` / `figures` region),
   `lib56dc.py` (`count_rows`, `grain_of`), `t1_grain.py`, `t2_strictest.py`,
   `out_t1_grain.txt`, mg-70c7's `README.md`, `OUTCOMES.md`, `PREDICTIONS.md`
   and `docs/repair-mg-70c7-grain-and-population.md`.

No probe, no census, no `figures()`, no `MARK` was executed. Every number below
is a prediction from reading, not a measurement rounded into one.

---

## The four things being repaired, and the one nothing names

| | what | from |
|---|---|---|
| **O1** | a count labelled `executing sites` prints **(site, target) ROWS** | mg-56dc T1c/T1d |
| **O2** | the strictest self-rule, E1, ranges over **one directory's transcripts** | mg-56dc T2a |
| **O3** | the merged "one rule object" **drops `proven`** | mg-56dc T2b |
| **O4** | `lib70c7.figures()` and `lib7522.figures()` **disagree on 3** | mg-56dc T2d |
| **F** | **the floor item, named in no list**: `figures()` is not the only rule kept in two copies | mine |

---

## O1 — the label and the grain

| id | prediction |
|---|---|
| **P1a** | **Which was wrong: the COUNT, not the label.** The four artifacts state **9** and **9 is the distinct-SITE count**, so the label `executing sites` names the grain the artifacts publish and the transcript printed the other one. The repair therefore prints **both grains, each under its own grain word**, and leaves every `9` in prose standing. |
| **P1b** | Re-derived at `973ca61` — the commit that published the transcript and the commit the four artifacts' figure was measured at — the outside-the-two-names counts will be **9 distinct SITES** and **10 (site, target) ROWS**. |
| **P1c** | **The row/site gap is exactly 1 at every revision this probe reads**, and the one line responsible is `code/runner_exit_c2b3/selftestc2b3.py:155`, which names two `*.sh`. Not 0, not 2. |
| **P1d** | At **HEAD** the same two counts will be **strictly larger** than at `973ca61` — the census ranges over the whole repository and the arc has landed `mg-56dc`, `mg-f3ff`, `mg-c067`, `mg-fcb2` since. Specifically I predict **HEAD outside ROWS ≥ 12** and **HEAD outside SITES = HEAD outside ROWS − 1**. |
| **P1e** | Because HEAD moves and `973ca61` does not, the repaired sentence in all four artifacts will name **a revision** as well as a grain. **4 of 4** artifacts will end up stating `9`, the word `sites`, and a revision. |
| **P1f** | The sixth instrument's classifier, run over the **whole** repaired `out_r4_property.txt` rather than over one row: **0** count rows classified `NONE`, and **0** rows whose grain word is only reachable from a column header. |
| **P1g** | The classifier will nonetheless **disagree with the value's true grain on at least one row that it classifies confidently**, because it reads labels — I predict **≥ 1** row where label-grain and re-derived value-grain differ *before* the repair and **0** after. |
| **P1h** | mg-70c7's `OUTCOMES.md` row **R5a stays HIT**. Its prediction said *sites* and the site count was 9; what was wrong was the transcript it cited, not the score. **No prediction verdict anywhere in this repository is changed by this ticket.** |

## O2 — the population of the strictest self-rule

| id | prediction |
|---|---|
| **P2a** | The old E1 population is `M.outs(M.TREE)` = **7** transcripts. |
| **P2b** | The repaired population is defined by a **property** — *an artifact this deliverable publishes* — evaluated over the whole repository, not by a wider path. It will have **11** members: the 7 transcripts, `README.md`, `OUTCOMES.md`, `PREDICTIONS.md` and `docs/repair-mg-70c7-grain-and-population.md`. |
| **P2c** | The old population will be a **strict subset** of the new one; **0** members lost. |
| **P2d** | Widening it will find **≥ 1** count row in mg-70c7's own reader-facing prose with no grain word in the window. **I will repair the prose rather than narrow the rule**, and I predict the number of such rows is between **1 and 12**. |
| **P2e** | `r6_self.py` will exit **0** on the final run and **1** on the first run after the widening, and both runs are reported. |

## O3 — the rule set, diffed by name

| id | prediction |
|---|---|
| **P3a** | Restoring `proven` takes `MARK` from **9** alternatives to **10**, which is exactly mg-dee4's D4 union. |
| **P3b** | Diffing the rule set **by name** before and after the consolidation finds **0** rule OBJECTS dropped and **exactly 1** alternative dropped — `proven` — i.e. mg-56dc found the whole of it. This is the prediction I most expect to be refuted, because "one silent drop implies the diff was never taken". |
| **P3c** | `proven` occurs in the sources and prose the marker rule ranges over **≥ 1** time, and **every** such occurrence classifies as a **MENTION**, not a USE — so restoring it adds **0** new violations and **0** committed transcript numbers of mg-7522 or mg-70c7 change. |

## O4 — two copies of `figures()`

| id | prediction |
|---|---|
| **P4a** | After the repair there is **exactly 1** implementation of `figures()` reachable from either library: `lib70c7.figures` will **call** `lib7522.figures` rather than restate it. |
| **P4b** | Over the integers **0..500**, the number of values on which the two names disagree goes from **1** (the value `3`) to **0**. |
| **P4c** | Unifying them **changes at least one number** in a committed transcript of mg-70c7, because `r3_strength.py` R3c compares a `lib70c7`-computed count against a `lib7522`-computed one and the two predicates were not the same. |

## F — the floor item, which nothing in either brief names

| id | prediction |
|---|---|
| **PFa** | `figures()` is **not** the only rule mg-70c7 kept in two copies. **`alternatives()` is defined in both `lib7522.py` and `lib70c7.py`** — and it is a *rule*, not a helper: it produces the published figure *"nine alternatives against three"*. I predict a by-name census of function definitions finds **≥ 6** names defined in both libraries. |
| **PFb** | Unlike `figures()`, the two `alternatives()` **agree on every input tested** — which is the brief's own sentence, *"two copies that agree today are a future disagreement"*, observed rather than quoted. I predict **0** disagreements over the pattern corpus tested. |
| **PFc** | I will make `lib70c7.alternatives` call `lib7522.alternatives` too, and **not** touch `lib56dc`'s third copy, because mg-56dc's tree is the committed evidence of an audit. |

## The instrument itself

| id | prediction |
|---|---|
| **P5a** | **This tree will contain a defect of the class it repairs**, found by its own `p5_self.py`, and it will be recorded rather than smoothed away. Five consecutive deliverables in this lineage have done so; I predict a sixth. |
| **P5b** | Every count row this tree prints carries a grain word **on its own label** — stage `label`, not `prev`, not `header`. **0** rows at stage `header` or `-`. |
| **P5c** | `selftestbf79.py`, `p1`–`p5` all exit **0** on the final committed run: **6 of 6**. |
| **P5d** | **At least one prediction in this file will MISS.** If all of them hit, that is itself a finding about the predictions and will be said in `OUTCOMES.md`. |

---

## What this repair will NOT establish, said in advance

* **That the classifier is right.** It reads labels; a wrong label makes it
  confidently wrong. P1g is the only handle on that here, and checking the
  classifier is `mg-03d1`'s job by name.
* **That a whole-repository census reproduces.** It does not — P1d predicts it
  moves. What is claimed is that a figure pinned to a revision reproduces at
  that revision.
* **That `9` is the interesting number.** It is the number four artifacts
  publish; whether the *quantity* is the right one to publish is a question
  about meaning and is not asked here.
* **mg-56dc's own tree.** Not modified. Its `README.md` cites `6aa043a` for its
  predictions commit and that commit is **not reachable from HEAD** (the
  reachable counterpart is `abb95b0`) — noted here because it was observed, and
  **not repaired**, because an audit's tree is its evidence.
