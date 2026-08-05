# mg-5f7c — predictions, committed before any script of this repair exists

**Pre-repair anchor: `6fb424f`** — the commit this branch is built on, and an ancestor of
`main` at the time of writing (`main` was `eab14bc`). Every "before" figure below is a figure
at `6fb424f`.

**This file's own sha will be displaced.** The refinery rebases before merging, so the commit
that carries this file onto `main` will not be the sha it has on `polecat-z5f7c`. That is
displacement, not loss, and the check for it is `git patch-id --stable`, not
`git merge-base --is-ancestor`, which returns a false negative after a rebase. This is
mg-a74f's `739f7bd` lesson (`code/state_delegation_repair_a74f/README.md:24-42`) restated in
advance rather than rediscovered afterwards.

---

## 0. THE DECISION, MADE BEFORE THE REPAIR AND NOT DISCOVERED BY IT

mg-5f7c says `visible_a74f.py` fails CLOSED on `<div class="hidden">` while its docstring and
`README.md` both say it fails OPEN, and that **which of the two to change is the question**.

**Decision: the CODE is wrong and both documents are right. The instrument must fail OPEN,
and it is being made to.** The reasoning is in `README.md` under "Which way, and why"; it is
written out there rather than here because it is an argument, not a prediction. The one line
of it that belongs in a predictions file is the part that can be checked against the
repository rather than argued: **`DECLARED` S4 already says `inside an element carrying the
`hidden` ATTRIBUTE`, and `NOT_COVERED` already says `display:none` on a class is OUTSIDE the
set.** So the docstring, the README *and the instrument's own printed declared set* all agree
with each other; the code disagrees with all three. There is no third document to reconcile.

**And there is no single posture to document even if I wanted to.** D1 fails closed
(`class="hidden"` scored SUPPRESSED) and D2 fails open (`<details title="open me">` scored
NOT SUPPRESSED) and **they are one bug** — an attribute *name* matched by regex over the
attribute *text*, values included. Documenting the behaviour as-is would require the sentence
"this instrument fails closed on some inputs and open on others, depending on what words
appear inside unrelated attribute values", which is not a safety posture.

---

## 1. MEASUREMENTS ALREADY TAKEN, DISCLOSED AS MEASUREMENTS

These were run at `6fb424f` before this file was written. They are **not** predictions and
are not scored as any. They are here so that no figure below can be read as foresight it did
not require.

* **M0** — the mg-a74f target, rendered by `marked`, is **10258 bytes**; `html.unescape` of
  it is **10098**. Markers `H2`–`H5` sit **112, 120, 120 and 128 bytes** later in the raw
  HTML than in the unescaped string; `H1` sits at the same offset in both. On `markdown-it`
  the shrinkage is 120 bytes and the four displacements are 100 each.
* **M1** — **32 of the 50** section observations in mg-a74f's published run were walked at an
  offset that is not the marker's position in the string being walked. The remaining 18 are
  V1's ten (inside a comment nothing is entity-escaped) and the eight `H1`s.
* **M2** — **0 of the 10 published renderer rows change** when the same walk is done at the
  true offset. All five documents apply their mechanism to the *whole* document, so a
  displaced position inside it returns the same verdict.
* **M3** — as shipped: `<div class="hidden">` scores `not-suppressed 0/5` by S4 on both
  engines; `<details title="open me">` scores `5/5` by nothing; `<div hidden>` behind 3000
  `&` scores `5/5` by nothing, and the same document without the `&` scores `0/5` by S4.
  These four are mg-65eb's own constructions, re-run here rather than quoted.

---

## 2. PREDICTIONS — the repaired instrument

Scored in `README.md`, misses kept as written.

| # | prediction |
|---|---|
| **A1** | After the repair, `<div class="hidden">` scores `not-suppressed` **5/5 on both engines**, by `(nothing)`. |
| **A2** | After the repair, `<details title="open me">` scores `not-suppressed` **0/5 on both engines**, by **S1**. |
| **A3** | After the repair, `<div hidden>` behind 3000 `&` scores `not-suppressed` **0/5 on both engines**, by **S4** — the same answer as the same document with no `&`. |
| **A4** | After the repair, mg-a74f's five published rows V0–V4 report **exactly the figures already committed** in `out_run_all.txt`: 5/5, 0/5, 0/5, 0/5, 0/5 not-suppressed, on both engines. (This follows from M2, which is a measurement of the *old* code; the prediction is that the *new* code agrees with it, which M2 does not establish.) |
| **A5** | An embedded `<style>.h{display:none}</style>` with `<div class="h">` — a real suppression a browser honours, and the first entry of `NOT_COVERED` — scores `not-suppressed` **5/5 on both engines** after the repair. **This is the fail-open posture shown rather than claimed, and it is the row that would falsify the decision in §0 if it came out 0/5.** |
| **A6** | The renderer-free polarity suite runs the **pre-repair `suppressors()`, read out of `6fb424f` with `git show` and executed unmodified**, beside the repaired one, on the same documents, and the two disagree on **exactly the D1 and D2 documents and no others** among the documents drawn from mg-a74f's own five. |
| **A7** | `visible_a74f.py`'s own committed self-check that `unescape_with_map` reproduces `html.unescape` byte for byte holds on **every document of every row of every engine** — 0 failures. |

## 3. PREDICTIONS — `prose_a74f.py`, the three lower-priority findings

| # | prediction |
|---|---|
| **B1** | At `6fb424f`, P1 in working-tree mode resolves a path reference against a set that includes **untracked** files, so an untracked file satisfies a claim the check calls "exists at this revision". A constructed reference to an untracked path **passes** before and **FAILS** after. |
| **B2** | At `6fb424f`, adding one key `"note": "..."` to a `delta_control.py` pinned table removes that table from P3's population entirely: the printed table count drops by **1** and the finding count does **not** rise. After the repair the table stays in the population and the count does not drop. |
| **B3** | P4 attributes each `all N rows` phrase to the nearest `.py` basename in the preceding 400 characters. **I predict at least one phrase in the working-tree population has more than one distinct script named in its 400-character window**, i.e. at least one attribution that is decided by proximity alone. If that count is 0 the prediction is a miss and is kept as one. |
| **B4** | After the repair, `prose_a74f.py` reports the **same finding count on the working tree** as before it (0), and the same at `--rev bd24efc`. The three repairs change *what the checks can see*, not what they find on a tree that is already clean. |

## 4. WHAT I AM NOT PREDICTING, AND WHY

mg-a74f predicted its next gap would be "a mechanism outside the declared set". Two of the
three defects mg-65eb found were **inside** the declared set and the third was not a mechanism
at all, and mg-5f7c's judgement is that **the failed prediction did more damage than the three
defects, because it aimed the next reader away**.

**So this repair issues no replacement prediction of where the next gap will be.** The rule
mg-5f7c gives is that such a prediction is allowed only if it says what would falsify it, and
I cannot write a falsifiable one about a gap whose shape is unknown by definition — the honest
form of "the next gap will be somewhere I am not looking" is silence, not a shorter list.

What replaces it is **A5**, which is not a forecast at all: it is a standing row that fires on
every run and goes 0/5 the moment the instrument starts scoring an out-of-set mechanism as
suppression. A row that can go red is worth more than a sentence about the future.

## 5. EXIT CODES, PRE-REGISTERED

| section | script | expected exit |
|---|---|---|
| 1 | `polarity_5f7c.py` (renderer-free) | **0** |
| 2 | `offsets_5f7c.py --rev 6fb424f` (the defect at the anchor) | **1** |
| 3 | `offsets_5f7c.py` (the tree) | **0** |
| 4 | `prose_5f7c.py` (the three constructions, under restore) | **0** |
| 5 | `visible_a74f.py` (needs the renderers; 3 without them) | **0** |
| 6 | `prose_a74f.py` (the tree) | **0** |
| 7 | `prose_a74f.py --rev bd24efc` | **1** |
