# mg-3f3b — predictions, written before the first run

**Written against the artifact as `mg-7e39` audited it, and committed in the same commit as
`repair_7e39.py`, before any transcript of it exists anywhere in the tree.** The instrument is
designed to run in two states — `PRE` (mg-7e39's four findings live) and `POST` (repaired) — and
detects which it is in by the **structure** each repair introduces, never by the absence of the
string it replaced. Both columns are predicted here.

mg-6df0 kept six misses in its own predictions file. The convention is kept: **anything below that
the run contradicts stays written as it stands, with the observation beside it.**

---

## What is being predicted, and why each one can fail

| | |
|---|---|
| **F1** | `n/a` is not a measurement. The prediction that matters is not "K11 fires" — mg-7e39 already showed that. It is that **an independently written derivation and the artifact's now agree at every one of the remaining cells**, i.e. that fixing the cell mg-7e39 named did not leave a second one of the same shape |
| **F3** | that the construct is **0 of 6** live, not 1 of 6 — and that the two sites which *measure* the construct end up **declared** rather than deleted, because deleting them deletes the measurement |
| **F5** | that the vocabulary **follows the gate** rather than copying it, shown by renaming a row in a copy of the gate's source |
| **F2** | that the population is right **at the commit that publishes it**, which is a different claim from "right at HEAD" and is the one that failed |

---

## S0 — preflight

| row | PRE | POST |
|---|---|---|
| `S0a` the runner is green unmutated | exit 0 | exit 0 |

If this is not exit 0, nothing below is attributable and the run should be read as void.

## S1 — F1: every `n/a` read as a claim

| row | PRE | POST |
|---|---|---|
| matrix cells parsed out of the runner's stdout | 36 | 36 |
| the artifact says `n/a` | **8** | **7** |
| `S1a` every `n/a` reason carries a count measured at the site | **REFUTED** — I expect **5 or more** of the 8 to be countless sentences (`"no column header line inside this site"`, `"no marked quotation carrying a figure at this site"`, `"no line here has two runs of two or more spaces to shift"`, both K08 rows, K12) | **CONFIRMED**, 7 of 7 |
| `S1b` my derivation and the artifact agree at every `n/a` cell | **REFUTED**, exactly 1 disagreement: `K11 @ the STATE.md row` | **CONFIRMED**, 0 disagreements |
| `S1c` my pipe-table shift at `K11 @ the STATE.md row`, on disk | exit 1, ≥1 SITE RECORD row refuted, 0 FIGURE rows | identical — **the gate never had this hole; only the matrix said it had nothing to catch** |
| `S1d` the artifact's own cell at `K11 @ the STATE.md row` | `n/a` | `FIRES (rec)` |
| `S1e` control: the pipe-table clause removed and nothing else | not applicable | `n/a` returns — **CONFIRMED** |

**The prediction I am least sure of is `S1a` in the PRE state.** I have not counted the artifact's
reasons against the rule; five is a guess from their shape. If the number is smaller the rule is
weaker than I think it is, and that is worth knowing in the direction that costs me something.

**`S1c` is predicted identical in both states, and that is the point of printing it.** F1
understates coverage and hides no hole. If `S1c` were exit 0 in the PRE state the finding would be
a hole in the gate rather than a hole in the matrix, and the whole framing would be wrong.

## S2 — F3: the construct at all six

| row | PRE | POST |
|---|---|---|
| `S2a` occurrences still live of the 5 mg-7e39 measured | **REFUTED**, 5 live | **CONFIRMED**, 0 live |
| `S2b` files performing the construct through a declared function | 0 → **REFUTED** | ≥ 3 → **CONFIRMED** |
| `S2c` the whole tree by the parent's rule + derived vocabulary | **REFUTED**, 5 hits (4 dispositioned by the parent, 1 the hand list could not see) | **CONFIRMED**, 0 hits and an **empty disposition table** |

**The exposure numbers are predicted, not read:** `SITE RECORD` and `FIGURE CENSUS` each select
**6 of the live gate rows by substring and 3 by heading**; `READ AT THE SITE` selects **12 and 12**,
i.e. 0 rows it was never meant to select. That last one is the construct with **no cost**, and it is
repaired anyway, because a construct whose cost is currently zero is a construct whose cost is one
row's rewording away from three.

## S3 — F5: the vocabulary, derived

| row | PRE | POST |
|---|---|---|
| the gate's live rows name | 6 | 6 |
| the sweep uses | 5 | 6 |
| `S3a` the sweep's vocabulary is the gate's set | **REFUTED** | **CONFIRMED** |
| `S3b` renaming a row in a copy of the gate's source moves the vocabulary | not applicable | **CONFIRMED** |
| `S3c` a source with no derivable row headings is a refusal | not applicable | **CONFIRMED** |
| `S3d` occurrences only the extra name finds | 1 (`audit_a318_repair.py:326`) | **0 — because that line is repaired by S2** |

**`S3d` is predicted to go to zero, and that is not the vocabulary failing.** The vocabulary's value
is measured in the PRE column; in the POST column the same derivation over a repaired tree finds
nothing, which is what a repair looks like from a sweep.

## S4 — F2: the population at the commit that publishes it

| row | PRE | POST |
|---|---|---|
| `.py` under `code/` at `77306a7` | 448 | 448 |
| `.py` under `code/` at `803bd50` | 448 | 448 |
| `S4a` every committed transcript agrees with the tree at **its own** publishing commit | **REFUTED**, 1 stale (`out_repair_6df0.txt`: 429 against 448) | **CONFIRMED** |
| `S4b` population figures carried as numbers in this arc's prose | **REFUTED**, 2 (`repair_6df0/README.md`, the mg-6df0 report) | **CONFIRMED**, 0 |
| `S4c` the historical fact from git | 429 published, 448 present, **19 missing** | identical — a historical fact does not move |

**The number at HEAD is deliberately not predicted.** It is whatever the branch this lands on holds,
and predicting it would be committing the defect: a population figure written down before the commit
that publishes it exists.

**`S4a` is keyed on each transcript's OWN publishing commit, not on HEAD.** A check keyed on HEAD
goes red the next time anybody merges a `.py` file anywhere, which is a check nobody can keep green
and therefore a check nobody reads. This one can only go red if a transcript is committed beside a
tree it does not describe — which is exactly F2.

## S5 — this deliverable, checked for its own four shapes

| row | prediction |
|---|---|
| `S5a` this file's own decline reasons all carry a count | **CONFIRMED** |
| `S5c` this file identifies no gate row by a substring outside `by_substring` | **CONFIRMED** |

`S5b` and `S5d` are `MEASURED`, not predicted — they are statements about what this file does, and a
row that cannot fail is not evidence. They are printed because a reader should be able to see the
answer without reading the source, not because they score anything.

## S6 — the ordering

`S6a` is `MEASURED`. In the commit that lands this file it reports **0 commits from the probe to
HEAD** and becomes a real ordering statement only afterwards — which is stated rather than hidden,
because a row that reads as evidence on the commit that creates it is the shape this arc keeps
finding.

---

## Predicted overall

- **PRE**: exit 1. Refuted: `S1a`, `S1b`, `S2a`, `S2b`, `S2c`, `S3a`, `S4a`, `S4b` — **8**.
- **POST**: exit 0, 0 refuted.

## What would make me wrong in a way that matters

1. **`S1b` finds a second disagreement.** Then F1's repair is a cell, not a rule, and this
   deliverable has committed the defect it is repairing at the same grain the parent did.
2. **`S1e` does not restore the `n/a`.** Then the cell is moving for some reason other than the
   clause, and `S1d` is uncontrolled.
3. **`S2a` is confirmed but a re-run of a touched instrument changes its verdict.** Three of the
   five sites are in *other deliverables'* shipped instruments. If applying `heading()` there moves
   a **verdict** rather than a printed line, the repair has silently rewritten somebody else's
   evidence, and that is worse than the disposition it replaces. The report must state, per file,
   what moved.
4. **`S4a` goes green only because the transcript was regenerated.** Regenerating it is the repair —
   but if the regenerated figure still disagrees with the tree at the commit it lands in, the
   publication step is not computing it and F2 is live in the deliverable that repairs F2.

---

# OBSERVED — appended after the runs, with nothing above this line edited

The predictions above are **left exactly as they were committed at `1d1d5b1`**, before any repair.
What follows is what the runs did, including the four places the predictions were wrong.

## The PRE run — against the artifact as mg-7e39 audited it

**Exit 1, 9 refuted where 8 were predicted.** The extra one is `S5c`, this instrument reporting
itself, which is the right direction for the surprise to be in.

| row | predicted | observed |
|---|---|---|
| `S1a` | REFUTED, "5 or more" countless of 8 | REFUTED, **6 of 8** — inside the range, guessed low |
| `S1b` | REFUTED, **exactly 1** disagreement | ⚠️ **REFUTED with 3** — see MISS 1 |
| `S1c` | exit 1, SITE RECORD refuted, 0 FIGURE rows | exactly that, in both states |
| `S1d` | `n/a` | `n/a` |
| `S2a` | REFUTED, 5 live | ⚠️ **REFUTED with 4** — see MISS 2 |
| `S2c` | REFUTED, 5 hits | ⚠️ **REFUTED with 10, 6 undispositioned** — see MISS 3 |
| `S3a` | REFUTED, gate 6 vs hand list 5 | REFUTED — but the "6" was **garbage**, see MISS 4 |
| `S4a` | REFUTED, 1 stale (429 vs 448) | exactly that |
| `S4b` | REFUTED, 2 carried | exactly that |
| `S4c` | 429 published, 448 present, 19 missing | exactly that, from `git ls-tree` |

## The four misses, kept as written above

### MISS 1 — `S1b` found **three** disagreements, and two of them were mine

`K10 @ H8` and `K10 @ the STATE.md row` came out as further instances of F1. **They were not.** This
instrument's independent `K10` derivation treated markdown **emphasis** as a marked quotation; the
pattern `*...*` matched across `**bold**` markers, so `**+1 630**` read as a quoted figure. With
emphasis removed from the pattern list, both cells agree with the artifact — **0 marked quotations
carrying a figure at either site**, which is what the artifact said.

> **Reading an `n/a` as a claim manufactures a finding exactly as easily as a narrow derivation
> hides a cell.** The predictions above named "`S1b` finds a second disagreement" as the outcome
> that would matter. It found two, and both were the instrument's.

### MISS 2 — `S2a` reported **4** live, not 5, because it asked the artifact what its scope was

The first version of `S2` called the sweep's own `substring_hits`, which is scoped by the sweep's
`ROW_NAMES` — **the hand list under test**. So `audit_a318_repair.py:326` read as *repaired* when it
was merely **invisible**. An instrument that takes its vocabulary from the artifact it is measuring
cannot report that the artifact's vocabulary is too small. `S2` now uses its own rule over its own
vocabulary.

### MISS 3 — `S2c` reported **10** hits, and 4 of them were the sweep's rule being wrong

Four were in `audit_7e39.py` — `ford += "FIGURE ORDER" in bad`, where `bad = {row_kind(d) for ...}`
is a set of **headings**. That is the remedy, spelled `row_kind(` instead of `heading(` and bound in
a comprehension, and the sweep's rule recognised neither.

> **A rule that recognises only one spelling of the remedy reports the other spelling as the disease
> — in the grammar of a finding about the code.** The sweep reported four false positives against
> the very audit that raised the finding it was sweeping for.

The remaining hit was `audit_7e39.py:800`, a genuine deliberate measurement, now routed through
`by_substring`.

### MISS 4 — `S3a`'s "the gate prints 6" was produced by a broken parse

The first `printed` derivation split each live row on `": "` and took what followed, which for a
figure row is the whole tail — so it reported names like `READ AT THE SITE = +2 744, MEASURED THIS
RUN = +2 744` and `is WRITTEN ONCE`, ten of them. The number 6 in the predictions came from mg-7e39,
not from this instrument, and this instrument could not reproduce it.

**Fixing it produced the deliverable's largest single finding.** The gate has **seven** row kinds,
not six: `WRITTEN ONCE` was emitted as `'{label}' is WRITTEN ONCE`, which no regex over the gate's
print calls could see. And the `READ AT THE SITE` rows carried **no ` -- ` separator at all**, so
`heading()` — the remedy — returned the whole row and selected **0 of 34** where the substring test
selected **12**.

> **A derived vocabulary derived from the wrong thing is a hand list with extra steps**, and **a
> remedy can degenerate into the construct without anybody writing the construct.**

## The POST run

**Exit 0, 0 refuted**, as predicted — after four defects in *this* instrument, found by its own runs
and fixed before the transcript was committed:

1. the `FIX_F1` detector read a **sentence** that the repaired docstring also quotes — mg-6df0 wrote
   this exact hazard down and this file walked into it anyway. Keyed on the mutation now;
2. the `S1e` control removed the pipe-table clause and **left its decline reason**, which counts what
   the clause found — a `NameError`, not the pre-repair state. **Reverting a derivation means
   reverting what it says about itself**;
3. `S3a` compared against the **live** rows where the claim is about the **declaration**;
4. `S5a` scanned every `return None, "..."` in the file and reported two "countless reasons" that were
   a 3-tuple in `probe_on_disk` and a runaway regex match. **A check that reports the wrong
   population is the finding it is checking for, one level in.** Scoped by AST now.

## The one prediction that mattered most, and it held

> *"`S2a` is confirmed but a re-run of a touched instrument changes its verdict. … If applying
> `heading()` there moves a **verdict** rather than a printed line, the repair has silently rewritten
> somebody else's evidence, and that is worse than the disposition it replaces."*

It was **one edit away from happening**. `heading()` at `audit_a318_repair.py:326` would have turned
`read_fired == 12` into `0`, because the row it keys on had no heading. The gate's row grammar is
repaired first; the instrument was re-run by hand at this tree; **12 of 12 and 10 of 12, identical to
the committed transcript** (`out_a318_rerun.txt`). And `out_audit_a318.txt` is **not** regenerated
from that run, because the rest of it moves for four reasons that have nothing to do with this repair.
