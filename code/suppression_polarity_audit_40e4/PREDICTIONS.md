# mg-40e4 — predictions for the INDEPENDENT AUDIT of mg-5f7c, committed before any script of this audit exists

**Target: mg-5f7c**, merged. On `main` it is carried by `bdeab76` (predictions), `4564bdd`
(repair+instrument), `5ad75a8` (docs), `0498b2b` and `7f0546b` (evidence).

**Audit anchor: `6fb424f`** — mg-5f7c's own pre-repair anchor, used here for the same reason
it used it, and re-resolved rather than trusted.

---

## 0. WHAT I HAVE ALREADY MEASURED, DISCLOSED AS MEASUREMENTS RATHER THAN LAUNDERED INTO PREDICTIONS

These were taken while reading, before this file was written. None is scored below.

* **M0 — the two GFM renderers were NOT installed on this host.**
  `node code/state_layer_audit_218d/render218d.js marked /dev/null` exited 1 with
  `MODULE_NOT_FOUND: marked`. I installed `marked` and `markdown-it` into a scratchpad
  directory **outside the repository** and the bridge then exits 0. Every renderer-dependent
  figure below is therefore reachable; if I had not installed them, sections of this audit
  would have been "not run" and would have had to say so.
* **M1 — mg-5f7c's five commits exist TWICE in this object store**, as the pre-rebase branch
  twins (`e3fb80e`, `4fd4f32`, `98478d4`, `e545a2c`, `e84ab66`) and as the copies the refinery
  landed on `main`. All five pairs have the **same `git patch-id --stable`** and **different
  tree shas**. That is displacement, and patch-id is what adjudicates it. `git merge-base
  --is-ancestor` says "no" for all five twins and is a false negative.
* **M2 — everything below is derived from READING mg-5f7c's four scripts, two documents and
  five transcripts.** No construction has been run and no figure has been re-derived at the
  time of writing. The hypotheses in §2 are hypotheses about code I have read, which is
  exactly the state in which a prediction is worth pre-registering.
* **M3 — mg-5f7c's committed `out_offsets.txt` prints `32 OF 50` and `0 OF 10`.** I have read
  those two numbers. They are mg-5f7c's, and §2 P6 predicts what **my own** arithmetic returns
  over a population I resolve myself; taking its number and confirming it is not an audit.

## 0b. WHAT I WILL NOT DO, SAID IN ADVANCE

**No browser is run.** Every "what a reader is shown" column in my own suite is my reading of
the HTML and CSS specifications, exactly as mg-5f7c disclosed for its own (its defect #4). Where
that reading is load-bearing I name the spec rule, so a reader can disagree with a citation
rather than with an assertion.

---

## 1. THE FRAMING, CORRECTED BEFORE IT IS TESTED

My ticket's framing is that mg-5f7c was required to **decide** the polarity rather than make
the documents agree, and that a repair that inverted the guard and rewrote the docs to match
would look identical to a correct one. **That framing is right about the requirement and wrong
about the risk in this instance**, and I record the correction before measuring:

mg-5f7c could not have made the documents agree by rewriting them, because a **third**
document — `DECLARED`/`NOT_COVERED`, printed by the instrument on every run — already said
fail-open, and because **the same bug failed closed on one input and open on another**, so
there was no consistent behaviour for a rewritten document to describe. The decision was still
required, and mg-5f7c made it and argued it. **My audit therefore aims at the argument and at
whether the repaired instrument actually holds the posture it decided on**, not at whether a
polarity inversion was smuggled in.

---

## 2. PREDICTIONS

Scored in `README.md`. Misses kept as written.

### The polarity, in the direction the parent's own argument calls dangerous

| # | prediction |
|---|---|
| **P1** | **THE REPAIRED INSTRUMENT STILL FAILS CLOSED, and I can construct the witness.** S5 is tested as `re.search(r"display\s*:\s*none\|visibility\s*:\s*hidden", attr.get("style",""))` — a substring match over the style attribute's **value**, with no CSS parsing. I predict `<div style="xdisplay:none">` (an unknown property, dropped whole by any CSS parser) is reported **S5** by the tree's `suppressors()`, on a document with **no stylesheet**, that a browser paints in full. I predict the same for a CSS **custom property** `--display:none` and for a declaration inside a CSS **comment** `/* display:none */`. This is mg-5f7c's own P06 defect — a name matched as text — one level down, on the line the repair rewrote. |
| **P2** | **The `hidden`/`open` half of the repair is sound at the value level.** I predict I can build **no** witness where an attribute *value* containing the word `hidden` or `open` causes S4 or S1 to fire. If I find one, P2 is a miss and mg-5f7c's repair is incomplete on the shape it was aimed at. |
| **P3** | **The DECLARED SET itself over-detects, and mg-5f7c's own polarity table records the over-detection as correct.** `<textarea>` content is the control's default **value and is painted**; the reader sees it. `polarity_5f7c.py`'s **P16 labels that row `browser BLANK`**. I predict the tree reports **S3** for a marker inside a `<textarea>`, that a reader is shown it, and therefore that P16's browser column is a row name that is not its measurement. |
| **P4** | **The same at S1.** The `<summary>` of a `<details>` carrying no `open` is **painted** — it is the closed widget's own label. I predict a marker inside `<summary>` is reported **S1**, i.e. SUPPRESSED, for content a reader is shown in full. |
| **P5** | **`NOT_COVERED` does not bound what the instrument can miss, so premise 2 of mg-5f7c's own argument is FALSE.** `_TAG` is `<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>`, whose `[^>]*` stops at the first `>` **inside an attribute value**. I predict `<div title="a>b" hidden>` is reported `(none)` — a miss produced by an **in-set** mechanism (S4) and a parser, not by anything in `NOT_COVERED`'s seven lines. mg-5f7c's README says *"the whole of what it can miss is enumerated under `NOT_COVERED`"* and *"under-detection here is bounded and declared"*. |
| **P6** | **The DECISION survives the argument.** I predict that after P1–P5 the answer *fail open* is still the right one — because premise 1 (the printed declared set) and premise 3 (one bug, both directions) do not depend on premise 2 — so my verdict is **decision CONFIRMED, argument PARTLY REFUTED**, and not a reopening of the polarity. If the measurements push me to the other posture, this prediction is a miss and the miss is the finding. |

### The byte offset spent as an index

| # | prediction |
|---|---|
| **P7** | Re-deriving from my own arithmetic over the population *5 documents × 2 renderers × 5 cited sections at `6fb424f`*, I predict **32 of 50** observations were walked from a position that is not the marker's, and that the 18 that were not split as **V1's 10 + the 8 `H1`s**. This is the same integer mg-5f7c prints (disclosed as read in M3); the audit content is that it is re-derived, and a **disagreement** would be the finding. |
| **P8** | I predict **0 of the 10 published renderer rows** of mg-a74f change their `not-suppressed` figure at the true offset — and that this remains true under **my** definition of the true offset, which is the repaired code's (`index[unesc.index(marker)]`), not `offsets_5f7c.py`'s (`out.find(marker)`). |
| **P9** | **Those two definitions are not the same function**, and mg-5f7c substituted one for the other without saying so. I predict they nevertheless **agree on all 50** observations, i.e. `out.find(marker) >= 0` everywhere, so section B's population is not silently reduced. **If any observation has `out.find(marker) < 0`, section B dropped it from its comparison and still printed `0 of 10` — and that is a defect of the audit instrument, not of the repair.** |
| **P10** | **THE POPULATION OF PUBLISHED FIGURES IS LARGER THAN 50, and mg-5f7c audited the smaller one.** mg-a74f's `out_run_all.txt` is not the only committed artifact carrying figures produced by the defective marker walk: **mg-65eb's own transcripts** (`code/state_visibility_audit_65eb/`) publish `not-suppressed` figures computed by the same pre-repair code. I predict ≥1 such committed artifact outside mg-5f7c's stated population. **I predict none of their figures moves either** — the ticket's "check whether it had already corrupted a published figure" is answered NO over the larger population as well — and if one does move, the corrupted output is still standing. |

### The instrument's own defect class, and the no-forecast requirement

| # | prediction |
|---|---|
| **P11** | **mg-5f7c issues no forecast of the next gap.** I predict 0 sentences in the five files it added that predict where the next defect will be, and that the nearest thing to one (`A5` / `P13` / `V8`) is a standing row that can go red, not a forecast. Falsifier: any forward-looking sentence about an unfound defect that does not say what would falsify it. |
| **P12** | Re-scoring mg-5f7c's own 13-row prediction table from its committed transcripts reproduces **11 held, 2 missed (A6, B3)**, with no prediction quietly rewritten between `PREDICTIONS.md` and `README.md`. I diff the two files' prediction texts to check that. |
| **P13** | Re-running mg-5f7c's own `run_all.sh` **with the renderers installed** reproduces **8 of 8 pre-registered exit codes** and a `git status --porcelain` that is empty afterwards. |
| **P14** | **My own suite will contain at least one defect of this class**, found by my own selftest rather than by a reader, and it will be recorded rather than smoothed away. This prediction has no falsifier that could be checked by anyone but me, so it is scored **only** by whether the README's defects section is non-empty. |

## 3. WHAT WOULD HAVE REVEALED A PROBLEM HAD ONE EXISTED

Stated in advance so that a negative below is not an absence of looking:

* **A polarity inversion smuggled into the repair** would show as the tree's `suppressors()`
  reporting a mechanism on P13/P14/V8 — an out-of-set suppression scored as suppression. My
  §Q1 runs those shapes as **my own** constructions, not by importing mg-5f7c's list.
* **Docs made to match an inverted guard** would show as the repaired code disagreeing with
  the *printed* `DECLARED`/`NOT_COVERED` text, which I parse out of the tree and evaluate
  against my constructions independently of both READMEs.
* **A corrupted published figure left standing** would show as a non-empty `moves` list in Q2
  over either population. The instrument that could show it is the same walk run at both
  offsets on the same rendered bytes, which is why Q2 renders rather than reads transcripts.
* **A prediction table rewritten to fit the result** would show as a text diff between
  `PREDICTIONS.md`'s prediction column and `README.md`'s scoring table. Q3 does that diff.
