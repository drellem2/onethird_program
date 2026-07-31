# mg-7e39's four findings, landed — `n/a` read as a claim, the construct at all six, the vocabulary derived, the population computed

**Target:** mg-7e39's audit (`dde93c5`) of the mg-6df0 repair (`77306a7`).
**Instrument:** `code/hodge_leverage_repair_3f3b/`, `sh run_all.sh`, ~30 s, exit 0.
**Predictions, committed before any repair:** `code/hodge_leverage_repair_3f3b/PREDICTIONS.md`.
**Committed transcript:** `code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt`.
**0 mathematical statements are touched.**

---

## Three of the four are one shape

F1, F5 and F2 are each **a statement that reads as a measurement and is not one**.

| | the statement | what it actually is |
|---|---|---|
| **F1** | *"no line here has two runs of two or more spaces to shift"*, printed over `K11 @ the STATE.md row` | a fact about `k_layout`, which shifts **whitespace columns**, at a site that is a **markdown pipe table** aligned by the padding inside its cells |
| **F5** | `ROW_NAMES`, the five gate-row headings the sweep hunts for | a **hand list**, against a gate that emits more — and a sweep that exists because a hand-picked *site* is a scope nobody chose picked its *vocabulary* the same way |
| **F2** | *"429 `.py` files swept"* | a figure **wrong at the commit that published it**: the tree at `77306a7` holds 448, and so did `803bd50` |

**F3** is the fourth and it is the parent's own finding one level up: the remedy was applied where the
defect was **found** — `1 touched of 6`, with 5 given a **disposition**. A disposition makes a *new*
occurrence red. It does not make an existing one right.

> **A matrix reports FIRE / SILENT / `n/a`, and only the first two are measured. `n/a` is prose, and
> it is where a matrix hides.**

---

## 1. F1 — `n/a` read as a claim, and the rule that makes the next one checkable

`K11 @ the STATE.md row` is now **`FIRES (rec)`**, and the matrix is **29 of 29 applicable cells
firing, 0 silent, 7 `n/a`** where it was 28 / 0 / 8. The site is the ledger row **and the header lines
it is read under** — three lines of a markdown pipe table — and `k_layout` now shifts alignment **in
either table format**: runs of two or more spaces for a whitespace-column table, and the padding
inside a pipe table's cells for a pipe table. The delimiter line `|:---|---:|` is deliberately left
alone: space there is the column's alignment *specifier*, and moving it changes what the table
**means**, which is a different kind from *"alignment shifted, no figure moved"*.

**The cell is demonstrated on disk, and it is demonstrated in BOTH states.** `S1c` derives the shift
independently — in the instrument, from the kind title, not from the artifact's code — splices it
into `STATE.md` through the artifact's own write-back, and runs the real runner: **exit 1, `SITE
RECORD @ the STATE.md row` refuted, every FIGURE row green.** That result is the *same* before the
repair. **The gate never had this hole.** F1 understates coverage rather than hiding a gap — which is
precisely why it is a finding about the *instrument* and not about the *gate*, and why the repair is
worth making anyway: a matrix that reads as complete over a cell it never tried is the same shape as
the enumeration mg-6df0 exists to have widened.

**`S1e` is the control.** The pipe-table clause is removed from `k_layout` and **nothing else**, on
disk; the cell reads `n/a` again; the clause is restored byte-identically. The cell moves with that
clause, so the clause is what is doing the work.

### And the general rule, because one cell is not a repair

Each of the eight `n/a` reasons was read as a claim. **Two of the eight carried a number.** The other
six were sentences — *"no column header line inside this site"*, *"no marked quotation carrying a
figure at this site"* — which a reader cannot check against the site without reading the source of
the derivation that wrote them.

There is no mechanical test for *"is this sentence about the site rather than about my code"*. There
**is** one for *"does this sentence carry a number measured at the site"*, and a reason that carries
its own count is one a reader can check. So:

- every `n/a` reason is restated as a claim **with the count it rests on** — *"12 marked quotation(s)
  at this site and 0 of them carry a figure token"*, *"1 of this site's 3 table row(s) carry a figure
  INSIDE the site, and an exchange needs two"*;
- and **`kind_matrix` makes a decline with no measurement in it RED**. Fail-closed, in the same
  direction as `site_extents`: the way this defect survives is by reading like an answer.

**7 of 7 now carry a count.**

### ⚠️ Reading an `n/a` as a claim can manufacture a finding as easily as hide one

The first version of this instrument's independent `K10` derivation treated markdown **emphasis** as
a marked quotation. The pattern `*...*` matched across `**bold**` markers, so `**+1 630**` read as a
quoted figure, and this file reported the artifact's `K10` declines at **H8** and at **the STATE.md
row** as two further instances of F1. **They were mine, and the artifact was right at both cells.**
The pattern is gone; the miss is kept in `PREDICTIONS.md`, which named *"`S1b` finds a second
disagreement"* in advance as the outcome that would matter.

---

## 2. F3 — the construct, at all six, and what the answer cost

**6 instances existed at `803bd50`. mg-6df0 touched 1. Five were live in the commit it landed in**,
four of them selecting **6 gate rows where 3 were meant**. All five are repaired here, and the
repairs are of **two different kinds**, because two of the five were not defects:

| site | repair |
|---|---|
| `audit_a318_repair.py:326` (`READ AT THE SITE`) | `heading()` |
| `audit_8916_repair.py:518` (`FIGURE CENSUS`) | `heading()` |
| `repair_835f.py:309` (`FIGURE CENSUS`) | `heading()` |
| `audit_ec07.py:714` (`SITE RECORD`) | **`by_substring()`** — it *measures* the construct; `heading()` would delete the measurement |
| `repair_ec07.py:303` (`SITE RECORD`) | **`by_substring()`** — mg-6df0's own `R1a`, the same measurement |
| ⚠️ `audit_a318_repair.py:342` (`WRITTEN ONCE`) | `heading()` — **a sixth, in nobody's population.** It appeared only once the vocabulary came from the gate's own declaration; see §3 |
| ⚠️ `audit_7e39.py:800` (`SITE RECORD`) | **`by_substring()`** — mg-7e39's own audit measures the construct too, and its file joined the tree after mg-6df0 counted |

`by_substring` is a declared function whose name is what it does, and `substring_hits` recognises it
**by name**. That is the point: **a reason on a line is not a structure.** A disposition has to be
read, has to be maintained, and has to be re-keyed every time the line moves. A function name is
something a sweep can see. `DISPOSITIONS` is now **empty**, and kept empty so that a genuinely new
occurrence anywhere is still red.

### ⚠️ A remedy can degenerate into the construct without anybody writing the construct

Every heading-keyed test in this arc is `heading(d).endswith(NAME)`, and `heading()` is
`d.split(" -- ")[0]`. **The gate's `READ AT THE SITE` rows carried no ` -- ` separator.** So
`heading()` returned the whole row, and `heading(d).endswith("READ AT THE SITE")` selected **0 of 34**
live rows where the substring test selected **12** — the remedy, silently degenerated into the defect
it replaces, arrived at by accident rather than by anyone writing it.

Applying `heading()` at `audit_a318_repair.py:326` without noticing would have turned that
instrument's `read_fired == 12` verdict into `0` — **rewriting another deliverable's evidence in the
act of repairing it**, which `PREDICTIONS.md` named in advance as the way this repair could be worse
than the disposition it replaced.

**So the row grammar is repaired first**, the gate now **declares** `ROW_KINDS`, and a row whose
heading ends in none of them makes the run **red**. `S2d` classifies what each repaired binding feeds
— a printed line or a recorded verdict — and the one file whose bindings feed a verdict was **re-run
by hand at this tree**: `12 of 12` and `10 of 12`, identical to the committed transcript, before and after
(`code/hodge_leverage_repair_3f3b/out_a318_rerun.txt`).

**`out_audit_a318.txt` is deliberately NOT regenerated from that run.** The rest of it differs from
the committed transcript for reasons that have nothing to do with this repair — `out_verify.txt` has
grown across four deliverables, mg-835f's widening closed that audit's `G-1` so its three `U1` probes
now fire, and `.md` files added since join its Appendix-A sweep. **A committed transcript is the
record of what an instrument found at its own commit.** Overwriting it under cover of a one-line
repair would be the disturbance, not the disclosure of it.

**`audit_ec07.py:714` is dead code at HEAD** — mg-ec07's `A5b` still stops early on the site-boundary
change mg-6df0 introduced, so `A7` never runs. The repair is to the source, and that is stated rather
than dressed up as a behavioural result.

---

## 3. F5 — the vocabulary, and why "derived" was not enough

`ROW_NAMES` named **five** by hand. The gate emits more, and the name the hand list missed —
`READ AT THE SITE` — is **where the construct entered this arc**.

**This repair's first answer was a regex over the gate's `print` calls.** It returned **six**: better
than five, and still short. The gate has **seven** row kinds, and the seventh was emitted as
`'{label}' is WRITTEN ONCE`, so a pattern wanting capitals straight after the label could not see it.

> **A derived vocabulary derived from the wrong thing is a hand list with extra steps.** A regex over
> another file's print statements is still a *second reader* of that file's grammar, and it can fall
> behind it — which is the same failure as a hand list, arrived at more expensively.

So the **gate declares its own vocabulary**: `ROW_KINDS`, one tuple, used to fail closed on any row
whose heading ends in none of it, and read by `row_vocabulary()` **by AST**. The derivation is
**fail-closed**: an empty result is a `SystemExit`, not an empty sweep, because *a sweep that finds
nothing and a tree that holds nothing read exactly the same* — F1's shape on this axis.

**Widening the vocabulary from six to seven immediately found a seventh occurrence of the
construct**, `audit_a318_repair.py:342` (`"WRITTEN ONCE" in l`), which **no vocabulary in this arc had
ever been able to see** — not the hand list, not the regex. It is repaired.

`S3b` shows the vocabulary is **derived and not copied**: one row heading renamed in a *copy* of the
gate's source, and the sweep's vocabulary follows it. A hand list returns the same five whatever the
gate emits.

### And the sweep's rule had the mirror-image defect

`substring_hits` recognised the remedy **only when it was spelled `heading(`**, and only in a plain
`x = ...` binding. An equally correct remedy spelled `row_kind(...)` inside a set comprehension —
`bad = {row_kind(d) for ok, d in rows if not ok}` — read as **the defect**. The sweep reported **four
false positives in `audit_7e39.py`, the very audit that raised this finding.**

> **A rule that recognises only one spelling of the remedy reports the other spelling as the disease,
> and it does it in the grammar of a finding about the code.**

The rule now recognises `heading(...)`, `row_kind(...)` and the inline `x.split(" -- ")[0]`, in
assignments, augmented assignments and comprehension targets.

---

## 4. F2 — the population, computed at the commit that publishes it

**"429 `.py` files swept" was not a figure that went stale.** The tree at `77306a7` — the commit that
*ships* that transcript — holds **448**, and so did `803bd50` before it. Nineteen files were in the
population and not in the number **on the day it was written**. The instrument was live and re-derived
the count every run; what was frozen was the figure **in the evidence**, which is the one a reader
meets.

The repair separates the two ways a figure gets published:

| | |
|---|---|
| **a transcript** | is **recomputed by the publication step**. `run_all.sh` regenerates it; the count is never typed |
| **prose** | has **no publication step**, so it must **point** at a transcript line rather than carry a number |

`code/hodge_leverage_repair_6df0/README.md` and the mg-6df0 report now point, with a dated correction
note recording what they used to say and why it was wrong. And the sweep's own line prints the
population **with the tree it was walked from** — the count, the `HEAD` it was taken at, and whether
that `HEAD` describes the working directory at all. **A count is only a fact about a named tree.**

**`S4a` is the standing check**, and it is keyed on **each transcript's own publishing commit**, from
`git ls-tree` — not on `HEAD`. A check keyed on `HEAD` goes red the next time anybody merges a `.py`
file anywhere, which is a check nobody can keep green and therefore a check nobody reads. This one can
only go red if a transcript is committed beside a tree it does not describe — **which is exactly what
F2 is**.

---

## What is not landed

- **mg-6df0's `PREDICTIONS.md` is untouched.** Predictions are kept as written; that is the whole
  value of committing them first.
- **X2 remains open and declared.** The ledger's other rows are outside the `STATE.md` site and their
  verdict labels can still be exchanged in silence; covering them freezes tens of thousands of
  characters of unrelated verdicts behind a reseal. The cost is measured, not argued.
- **`audit_ec07.py` and `repair_9207.py` still stop early** on the site-boundary change mg-6df0
  introduced. Both need the same one line — `with_site(files, name, new_site)` — and neither is
  changed here beyond the construct repair, because they are other deliverables' instruments.

## The rule this generation costs

> **Read every `n/a` you write as a claim, derive every vocabulary you sweep with from a declaration
> rather than from a second reading, and compute every population figure at the commit that publishes
> it.**

And the one this deliverable added to it:

> **A remedy is only applied where its precondition holds.** `heading()` is `split(" -- ")[0]`, so a
> row without that separator has no heading, and every heading-keyed test over it silently becomes the
> substring test it was written to replace. **Check that the grammar the remedy assumes is the grammar
> the artifact emits — and make the artifact declare it, so the check is a rule and not a reading.**
