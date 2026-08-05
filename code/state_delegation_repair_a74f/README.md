# mg-a74f — mg-16eb's three OPENs on mg-0049, answered

mg-16eb audited mg-0049, the delegated presentation record, and its verdict was **dropped
with no successor** on 2026-07-30. This is the successor. mg-16eb's own conclusion is not in
question and is not re-litigated here: **the repair is real and nothing retreated** — its
seven committed `out_*.txt` reproduced byte for byte, 7 of 7, and 8 of 8 rows came out as
predicted.

What is repaired here is what it left open.

* **OPEN 1** — the visibility instrument measures bytes in the HTML and calls it what a
  reader is shown.
* **OPEN 2** — 6 of the 17 claims mg-0049 added do not hold. Enumerate them individually,
  classify each, repair each by its class, and treat the six as a claim-generation problem
  rather than six slips.
* **OPEN 3** — the blind spot moved three times, every time onto ground the repair itself
  laid. Ask not "did I close the gap" but "what surface does this fix create, and what is
  now measurable only through it?"

**`PREDICTIONS.md` was committed before any script in this directory existed** (`cfd2af5`),
and every figure below is scored against it, misses included. The pre-repair revision is
pinned at **`bd24efc`**.

> **RE-ANCHORED BY mg-0120, and the sentence that carried it was wrong about itself.** This
> line used to name `739f7bd` and to justify it with *"a sha, not `HEAD~n`, so a rebase
> cannot quietly move it."* A rebase moved it. `739f7bd` was written on the branch
> `polecat-a74f`; the refinery rebases before merging, so what landed on `main` is
> `cfd2af5` — **the same change under a different sha**, and `739f7bd` is reachable only
> from a branch a reader of `main` does not have.
>
> A sha is immune to *renumbering*, which is what `HEAD~n` suffers, and not to
> *displacement*, which is what a rebase does; the sentence claimed the second immunity and
> had earned only the first. mg-65eb found the pointer broken and re-derived the property at
> `cfd2af5`. mg-0120 established that the two commits are the **same change** rather than
> two commits that happen to look alike: `git patch-id --stable` gives
> `17a7bca3c7be2fc4f9ab736294b06230a11c5cc0` for both, while their trees and their parents
> differ — which is what a rebase is. **So the property was never violated and only the
> pointer rotted.** Those are different defects needing different repairs and
> `git merge-base --is-ancestor` cannot tell them apart; `code/state_claims_repair_0120/`
> holds the diagnosis, the repository-wide re-measurement (57 more anchors displaced the
> same way) and a constructed case where identifying the twin by commit SUBJECT picks the
> wrong commit and `patch-id` does not.

---

## OPEN 1 — the instrument now measures the property its row names

**The two repairs mg-16eb offers are "measure the claimed property" or "narrow the claim to
the measured one", and it forbids a third: keep the wording and swap the intent.** A static
walk over serialised HTML cannot decide what a browser paints — that needs the cascade,
layout, and whatever JavaScript does after load — so the claimed property is not available to
an instrument of this kind and **the second repair is the honest one**.

`visible_a74f.py` reports **`not-suppressed`**: not suppressed by any mechanism in a
**declared set of five**, printed on every run, alongside a printed list of what the set does
**not** cover. The phrase "shown to a reader" is not a column heading anywhere in the file.
The instrument **fails open** — a suppression mechanism outside the set is scored NOT
SUPPRESSED — and saying so on every run is why the column is not called `shown`.

**The instrument it replaces scores the blank page 5 of 5.** `render16eb.py`'s `SHOWN TO A
READER` column is bytes-that-survive-tag-stripping minus one mechanism (a `<details>` with no
`open`). Its tag regex requires a letter after `<`, and `<!--` has a `!`. Applied — by
importing `render16eb.py` **unmodified** and calling its own two functions — to mg-0049's own
**R8**, the whole target inside a **closed** HTML comment:

| document | bytes-in-html | not-suppressed | by | mg-16eb's `SHOWN` |
|---|---|---|---|---|
| V0 unmutated | 5/5 | 5/5 | — | 5/5 |
| **V1 the whole file in a CLOSED HTML comment (mg-0049's R8)** | 5/5 | **0/5** | S2 | **5/5** |
| V2 `<details><summary>` at the top (mg-16eb's B3) | 5/5 | 0/5 | S1 | 0/5 |
| **V3 `<div hidden>` at the top** | 5/5 | **0/5** | S4 | **5/5** |
| **V4 `<div style="display:none">` at the top** | 5/5 | **0/5** | S5 | **5/5** |

Both renderers, 50 section observations, **0 rows off this repair's committed predictions**,
**6 of 10 renderer rows where the two instruments disagree**.

**V1 settles it.** Every party in this arc agrees a reader is shown nothing of that document:
`render0049.py` scores it `ANY 0/5`, `delta_control.py` exits 1 on it and calls it damage, and
mg-16eb's own audit calls it "R1's and R8's blank page". mg-16eb's replacement instrument —
the one laid to draw the distinction — scores it **5 of 5 SHOWN**. V3 and V4 are the same
defect on two mechanisms nobody in this arc has used. V2 is the one shape it was written
against, and it gets that one right.

`render0049.py` is narrowed to match: its header now reads **WHAT IS IN THE RENDERED PAGE**,
its `ANY` row says "somewhere in the page", it prints **NOT MEASURED HERE — whether a reader
is SHOWN any of it**, and its R5 verdict says so at length. Its 100 comparisons and every
number in them are unchanged.

## OPEN 2 — the six, one row each, by class

`claims_a74f.py` reports each of the six with a probe at `bd24efc` that the defect is still
present and a probe at the tree that it is gone. **12 of 12 probes hold.**

| # | where | class | repair | before → after |
|---|---|---|---|---|
| 1 | `delta_control.py:233` names `guards_only_0049.py` | **FALSE** | **correct the fact** | path absent from the tree → `split_0049.py`, which exists |
| 2 | `delta_control.py:234` "all six rows" | **FALSE** | **correct the fact** | six (mg-5644's population) → nine (`mutations_0049.ROWS`) |
| 3 | `delta_control.py:798` "cannot drift apart quietly in EITHER direction" | **FALSE** | **implement the missing behaviour** | `DELEGATED_PRESENTATION` iterated by nothing → iterated, with a key check at both grains |
| 4 | `delta_control.py:346` exit 1 is "NO LONGER PRESENTED TO A READER" | **FALSE**, in **both** directions | **narrow to the measured property** | the reader → the state-set predicate, with B3 and C1 printed beside it |
| 5 | mg-0049 `README.md:105-106` "re-run in section 7" | **FALSE** | **correct the fact** | 7 (`coverage218d.py`) → 8 (mg-5644's battery) |
| 6 | `render0049.py:11` R5 "SUPPRESSES NOTHING" | **TRUE OF A DIFFERENT PROPERTY** | **narrow to the measured property** | "suppresses nothing" → "the text is in the page" |

**5 FALSE, 1 TRUE-OF-A-DIFFERENT-PROPERTY, 0 UNSUPPORTED, 0 TRUE-BUT-UNEVIDENCED.** Two of
mg-16eb's three buckets are empty and that is the finding, not an omission: **not one of the
six was a claim nobody could check. Every one was checkable by a program and none of the six
was checked by one.**

Claim 3 is the only one repaired by changing behaviour, and it is measured by construction
rather than by reading the diff: mg-16eb's **own** battery, on mg-16eb's **own** harness,
with `git diff` over `code/state_delegation_audit_16eb/` printed at 0 bytes, now reports

> `8 of 8 rows run; 6 behaved as this audit predicted; 2 did not` — **A1 and A2**, exit 0 → 2.

That line is the repair, in the auditor's words, in a file this repair did not touch. It is
mg-5644's `Q1`/`Q2` shape and the precedent is deliberate.

### The claim-generation problem

| file | did a program read its prose as claims at `bd24efc`? | of the six |
|---|---|---|
| `delta_control.py` | no — every checker reads it as the ground-truth box | **4** |
| mg-0049 `README.md` | no — nothing reads it | 1 |
| `render0049.py` | no — nothing reads it | 1 |
| `COVERAGE.md` | **yes — `coverage218d.py`, 40 of 40** | **0** |

`COVERAGE.md` names `split_0049.py` and "all nine rows" **correctly**, in the same paragraph
where `delta_control.py` gets both wrong. The difference is not care.

`prose_a74f.py` is the missing program, over a **computed** population of three directories
(its own included, so it reads its own prose):

* **P1** every repo-relative path named in the text exists at the revision being read
* **P2** every `section N` reference to a `run_all.sh` resolves, and every mg-id and script
  basename on the referencing line occurs in that section
* **P4** every "all *N* rows" phrase equals that script's own `ROWS`, derived from its AST
* **P3** every module-level dict of `delta_control.py` keyed by repo paths is iterated by
  some `for` in that file — a pinned table nothing visits cannot fail in the direction that
  would need visiting

**4 findings at `bd24efc`, 0 on the tree.** What it covers of the six: claim 1 (P1), claim 2
(P4), claim 3's code half (P3), and **one of the two rows** of claim 5 (P2). **Three and a
half of six.** It covers neither claim 4 nor claim 6 and it cannot — both are a name for a
measured property that claims more than the measurement, and that is caught by putting the
instrument to a construction, never by a reference-checker.

## OPEN 3 — the surface this repair creates

mg-16eb's finding is that **a repair does not only close a gap; it builds new surface, and
the next gap appears on the surface it just built.** Four new surfaces, each named with the
property now measurable only through it and the way it fails:

1. **`prose_a74f.py`'s four checks.** A path reference, a `run_all.sh` section reference, an
   "all *N* rows" phrase and the shape of `delta_control.py`'s pinned tables are now checked
   in three directories. **Everything else in that prose is adjacent to checked text and is
   not checked** — every other count, every "cannot", every "measured over N", every claim
   about a reader. The run prints that list. **Predicted next gap: a false claim of a shape
   P1/P2/P3/P4 does not cover, in a file this checker walks, read as covered because its
   neighbours are.**
2. **`prose_a74f.py`'s exemption list.** Two files are excluded from P1, P2 and P4 because
   their prose is a *report* of the six broken claims and a checker that reads a report of a
   defect as a fresh instance of it is measuring the wrong thing. The list is **fail-closed
   in both directions** — an entry naming a file outside the population fails, and an entry
   that suppresses nothing fails — and the count each entry suppresses is printed on every
   run. **Predicted next gap: a third file that quotes a defect and is not on the list, whose
   quotation is then reported as a finding — or a file added to the list for a weaker reason
   than these two.**
3. **The section-2c cross-check.** `DELEGATED_PRESENTATION` is now iterated and cross-checked
   at two grains. The check is written for two tables **by name**. **Predicted next gap: a
   third pinned table** — which is why P3 derives its population from the file's own AST
   rather than from a list, so a third table joins by existing. P3 is then itself the gap:
   it checks that a table is **iterated**, not that the iteration **checks** anything.
4. **`visible_a74f.py`'s declared suppression set.** "Suppressed" now means "by one of five
   named mechanisms". **Predicted next gap: a mechanism outside the set** — a stylesheet,
   `aria-hidden`, off-screen positioning, `color: transparent`, JavaScript, the difference
   between shown and shown *yet*. The instrument **fails open** on every one of them, which
   is exactly why its column is named `not-suppressed`.

### Every instrument this repair adds, and whether its row name is its measurement

Printed by `claims_a74f.py`, nine rows. Eight match. The one that does not is
`visible_a74f.py`'s `r16 SHOWN` column, which keeps mg-16eb's name for mg-16eb's rule **on
purpose**, so that the mismatch is legible rather than laundered.

### What this repair deliberately did NOT do

**B3 and C1 do not move, and that was stated in `PREDICTIONS.md` before the run rather than
discovered after it.** They refute what the exit-code *table* said, in opposite directions:
B3 under-fires (a page a reader is shown nothing of, exit 2, "re-baseline this instrument")
and C1 over-fires (a section a reader is shown every line of, exit 1, printing "SHOWN NOTHING
OF IT", and `--emit-baseline` does not clear it). This repair **narrows the sentence to the
predicate the code applies** and prints both constructions beside it, in the exit-code table,
in `is_presented()`'s docstring, in the FAIL line the code emits and in the PASS summary.
**Changing the predicate itself would move the classification of every delegated section and
is a different ticket. It is named as open here rather than left for the next auditor.**

---

## Two defects of this repair's own instruments, recorded rather than smoothed away

1. **`prose_a74f.py`'s P3 began as a hand list of two table names, compared for equality.**
   Run at `bd24efc`, it *passed* — asserting that both tables were cross-checked at a
   revision where one was iterated by nothing. A hand list standing in for a derived property
   is the defect class this deliverable exists to repair, and it was in the repair. It is now
   derived from the file's own `for` statements, and at `bd24efc` it fails, correctly.
2. **P4 did not exist** until the pre-repair run showed that P1 and P2 between them covered
   only two of the six claims. It was added, and the prediction it was added against — that
   the pre-repair count would be 1 — was not written before the fact.

## Three misses against `PREDICTIONS.md`

1. **P2 was predicted to find 2 at `bd24efc`; it finds 1.** Both rows of mg-0049's README
   said "section 7". P2's fail-closed rule is that every mg-id on the referencing line must
   occur in the named section; the mg-5644 row fails and the **mg-218d row passes, wrongly**,
   because section 7 runs `coverage218d.py` and its echoed title says `mg-218d`. Deciding
   that the row is about mg-218d's *battery* rather than mg-218d's *coverage checker* needs
   the sentence's meaning. The instrument does not have it and is not given a rule
   reverse-engineered to hit 2.
2. **P3 was predicted to be 0 at both revisions; it is 1 at `bd24efc`.** That is defect 1
   above: the prediction was correct about the instrument as designed and the instrument was
   wrong.
3. **Two of mg-0049's seven committed transcripts were predicted unchanged and do not
   reproduce — and it is not this repair's doing.** See below.

## The committed evidence, and a staleness that predates this repair

`reproduce16eb.py`, re-run **unmodified** on the repaired tree, reports **5 of 7**:

| file | reproduces? | why |
|---|---|---|
| `out_battery_0049.txt`, `out_split.txt`, `out_5644_rerun.txt` | identical | untouched |
| `out_render.txt` | identical **after regeneration** | moved by this repair (claim 6); regenerated and committed |
| `out_control.txt` | identical **after regeneration** | moved by this repair (two new check lines); regenerated and committed |
| **`out_coverage218d.txt`** | **DIFFERS** | `over 383 lines` → `over 387 lines` — **STATE.md grew after mg-16eb's run** |
| **`out_selftest_negative.txt`** | **DIFFERS** | `STATE.md at rest: 177464 bytes` → `186710` — same cause |

**The last two are measured to predate this repair.** Section 8 of `run_all.sh` creates a
throwaway worktree at `bd24efc` and runs `reproduce16eb.py` there: **5 of 7, the same two
differing, producing the same two sha256s.** So mg-16eb's `7 of 7 IDENTICAL` was true at the
commit it was run on and was already false at `bd24efc`, before this repair existed.

**They are not regenerated here.** Re-baselining another deliverable's transcripts for a
reason unrelated to this ticket would erase the finding, and the finding is the useful part:
**a committed reproduction figure in this repository is a measurement at its own commit, not
a live property, and every merge that rebases a branch onto a larger tree can stale one.**
mg-16eb's own `out_reproduce.txt` is not edited: it is the auditor's transcript and it is
correct about the tree it was run on. The same warning applies to **this** directory's
transcripts, including after the merge that lands them.

## Running it

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_delegation_repair_a74f/run_all.sh
```

Run it on a **committed** tree: sections 1, 5 and 6 mutate tracked files through their own
restore discipline, and `delta_control.py` refuses to run on a dirty tree. Sections 4, 6 and
7 need the renderers; without them those sections print the install line and exit 3, and the
repair still stands on sections 2, 3 and 5. Section 7 takes about ten minutes.

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before any script here existed |
| `visible_a74f.py` | OPEN 1 — suppression over a declared set, with mg-16eb's rule imported unmodified beside it |
| `prose_a74f.py` | OPEN 2's structural half — an external checker for prose claims, runnable at any revision |
| `battery_a74f.py` | mg-16eb's eight rows, on mg-16eb's harness, unmodified, twice |
| `claims_a74f.py` | OPEN 2 — the six, one row each, classified, probed at both revisions |
| `run_all.sh` | all of it, in order, including the `bd24efc` control |
| `out_*.txt` | the committed transcripts of one full run |
