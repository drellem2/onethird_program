# mg-3f3b — `n/a` as a claim, the construct at all six, the vocabulary, the population

Target: mg-7e39's **F1**, **F3**, **F5** and **F2** on `code/hodge_leverage_landing_e1d0/verify_landing.py`
and `code/hodge_leverage_repair_6df0/repair_ec07.py` (the refusal keyed on the row's heading, landed by
mg-6df0 / `77306a7`, audited by `dde93c5`).

    sh run_all.sh          # ~30 s, exit 0

Report: `docs/OneThird-Hodge-Side-Leverage-Mg6df0RepairAudit-Repair.md`.
Predictions, written before the first run and before any repair, **with the misses kept as
written**: `PREDICTIONS.md`.
Committed transcript: `out_repair_3f3b.txt`.

## Three of the four findings are one shape

| | |
|---|---|
| **F1** | an `n/a` reason phrased as a property of the **site** that is a property of the **derivation**. `K11 @ the STATE.md row` declined with *"no line here has two runs of two or more spaces to shift"* — a fact about `k_layout`, which shifts whitespace columns, at a site that is a **markdown pipe table** aligned by its cell padding |
| **F5** | a sweep vocabulary **hand-listed at five** where the gate emits more. A sweep built because a hand-picked *site* is a scope nobody chose picked its *vocabulary* the same way |
| **F2** | a population figure **carried in prose** that was already wrong at the commit which published it — not drift after the run |

Each reads as a measurement and is not one. **F3** is the fourth, and it is the parent's own finding
one level up: `heading()` was applied at the line the defect was found on — **1 touched of 6**.

## What changed in the artifacts

| | |
|---|---|
| `k_layout` | shifts alignment **in either table format**. The first clause is the whitespace-column table it always handled; the second is the **padding inside a markdown pipe table's cells**, which is what alignment *is* at the `STATE.md` site. The delimiter line is deliberately not touched — moving space in `\|:---\|` changes what the table means |
| every `n/a` reason | restated as a **claim about the site carrying the count it rests on**, and `kind_matrix` now makes a decline **with no measurement in it RED**. There is no mechanical test for *"is this sentence about the site"*; there is one for *"can a reader check it against the site"* |
| `ROW_KINDS` | the gate **declares its row vocabulary** and fails closed on any row whose heading ends in none of it. See below — this replaced a regex over the gate's `print` calls, which is a hand list with extra steps |
| the row grammar | the `READ AT THE SITE` rows are emitted **with the ` -- ` separator every heading-keyed test depends on**. Without it `heading()` returns the whole row and the remedy silently degenerates into the construct |
| `row_vocabulary()` | `repair_ec07.py`'s `ROW_NAMES`, **derived from `ROW_KINDS` by AST** and fail-closed on an empty result — a sweep with an empty vocabulary finds nothing and reads exactly like a tree with nothing in it |
| `substring_hits()` | recognises the remedy in **every spelling it is written in** — `heading(...)`, `row_kind(...)`, and the inline `x.split(" -- ")[0]` — and in comprehension targets. It used to recognise only the first, and reported four **false positives** in `audit_7e39.py`, the audit that raised the finding |
| `by_substring()` | the **one declared place** the construct is performed on purpose, in each file that has to measure it. A sweep now meets a name; it used to meet a line number in a disposition table |
| `DISPOSITIONS` | **empty**, and kept empty so a new occurrence anywhere is still red |
| `population_line()` | the sweep prints its population **with the tree it was walked from** — the count, the HEAD, and whether that HEAD describes the working directory at all |

## The evidence

| | |
|---|---|
| `S1a` | every `n/a` reason the runner prints **carries a count measured at the site**. It began at 2 of 8 |
| `S1b` | every `n/a` cell tried again with a mutation of the same kind **derived here from the kind title**, not from the artifact's code. 0 disagreements |
| `S1c` | the pipe-table shift **on disk**: exit 1, `SITE RECORD` refuted, every FIGURE row green — **and the same in the PRE state**, which is the point. F1 understates coverage; the gate never had this hole |
| `S1d` / `S1e` | the artifact's own cell moves `n/a` → `FIRES (rec)`, and **reverting that clause alone puts it back** |
| `S2a` | the five occurrences mg-7e39 measured live, **each repaired and named**, with what each selected that it was never meant to |
| `S2c` | the tree swept by **my** rule over **my** vocabulary — not the sweep's, whose scope is the thing under test |
| `S3b` | a gate row renamed in a **copy** of the gate's source and the vocabulary **follows it**. A hand list returns the same five whatever the gate emits |
| `S3c` | a source with no derivable vocabulary is a **refusal**, not an empty sweep |
| `S4a` | every committed transcript that publishes a population is compared to the tree at **its own publishing commit**, from `git ls-tree` |
| `S4b` | **0** population figures carried as numbers in this arc's prose |
| `S6a` | **the probes precede the repairs in git** — re-derived from `git log`, not asserted |

## Three things this run got wrong, kept because they are the finding's own shape

**1. `n/a` read as a claim can manufacture a finding as easily as hide one.** The first version of this
instrument's `K10` derivation treated markdown **emphasis** as a marked quotation. `*...*` matched
across `**bold**` markers, so `**+1 630**` read as a quoted figure and this file reported the
artifact's `K10` declines at **H8** and at **the STATE.md row** as two more instances of F1. **They
were mine.** The artifact was right at both cells. The pattern is gone and the miss is in
`PREDICTIONS.md`.

**2. A derived vocabulary derived from the wrong thing is a hand list with extra steps.** This
repair's first answer to F5 was a regex over the gate's `print` calls. It returned **six** names —
better than the hand list's five, and still short, because a seventh row kind was emitted as
`'{label}' is WRITTEN ONCE` and the pattern wanted capitals straight after the label. The gate now
**declares** `ROW_KINDS` and fails closed on any row that does not use it. Widening the vocabulary
from six to seven immediately found **a seventh occurrence of the construct** —
`audit_a318_repair.py:342` — which no vocabulary in this arc had ever been able to see.

**3. A remedy can degenerate into the construct without anybody writing the construct.** Every
heading-keyed test in this arc is `heading(d).endswith(NAME)`, and `heading()` is
`d.split(" -- ")[0]`. The gate's `READ AT THE SITE` rows carried **no ` -- ` separator**, so
`heading()` returned the whole row and that test selected **0 of 34** rows where the substring test
selected **12**. Applying `heading()` at `audit_a318_repair.py:326` without noticing would have
turned its `read_fired == 12` verdict into `0` — **rewriting another deliverable's evidence in the
act of repairing it**, which `PREDICTIONS.md` named in advance as the way this repair could be worse
than the disposition it replaced.

## What is not repaired here

- **mg-6df0's `PREDICTIONS.md` is untouched.** Predictions are kept as written; that is the whole
  value of committing them first.
- **mg-ec07's `A5b` still stops early** on the site-boundary change mg-6df0 introduced, so
  `audit_ec07.py:714` — repaired here — is **dead code at HEAD**. The repair is to the source, and
  that is stated rather than dressed up as a behavioural result.
- **X2 remains open and declared**: the ledger's other rows are outside the `STATE.md` site, and
  covering them freezes tens of thousands of characters of unrelated verdicts behind a reseal.
