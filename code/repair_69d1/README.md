# `code/repair_69d1/` — the instrument for mg-69d1

Two open sites, from two independent audits, both repaired in this ticket.
Neither deferred.

| | site | what was wrong | where the repair is |
|---|---|---|---|
| **OPEN 1** | mg-eaef, **E5** and **E4** | the stated bound is **wider than the sweep**, and 4 of 15 explicit boolean operands are in **neither** census column | `kern5f9a.py`, `d2_deletion.py`, `face_complex.py`, `run_all.sh`, `docs/landing-mg-0b07-…md` |
| **OPEN 2** | mg-e34a, **E-1** | the `both together` row is right and its stated **reason is inverted** | `g1_provenance.py`, `lib76cc.py`, `r1_kernel.py`, `docs/repair-mg-76cc-…md` |

## What each script does

| script | what it measures | exit |
|---|---|---|
| `selftest_69d1.py` | 40 assertions over constructed inputs — the classifier, `drop_boolean_operand`, every bend's refusal on 0 and on many, the conspiring pair's no-op property, `read_literal`, the grep parser | 0 |
| `p1_bound.py` | the narrowed sentence over every live site; all 17 operands in exactly one named column with the population re-derived by an independent walk; the `swept` column against the sweep's **own rows**, name by name; the 4 nested operands deleted one at a time against the control battery; the control run where the defect is still present | 0 |
| `p2_rerun.py` | `d2_deletion.py`, `g1_provenance.py` and **mg-e34a's own `k4_cancel.py`** run unmodified as subprocesses, stdout captured, committed transcripts untouched | 0 |
| `p3_reason.py` | **both** inputs the corrected reason names, built and measured: a cancelling pair and a conspiring pair, each against g1's three rows | 0 |
| `p4_kinds.py` | the **kinds** of artifact this repair emits, each with a disposition; and this deliverable checked for the defects it remedies | 0 |

## OPEN 1 — the bound, narrowed

The sentence read

> DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO FURTHER

which is read as *every explicit boolean operand is on the reached side*. It is
not. It now reads

> DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS OF THE DECIDING CONDITIONS IN
> THE FILES THIS SWEEP VISITS, AND NOTHING ELSE

and every explicit boolean operand is in exactly one **named** column:

| file | swept | not swept: file | not swept: nested | not determined | all |
|---|---|---|---|---|---|
| `face_complex.py` | 11 | 0 | 4 | 0 | 15 |
| `posets.py` | 0 | 2 | 0 | 0 | 2 |
| **ALL** | **11** | **2** | **4** | **0** | **17** |

**`not determined` is a column and not an omission.** It reads 0 on this tree
and is printed anyway. An explicit *not determined* is checkable; an empty cell
is the absence of an answer, and that absence is exactly the ambiguity a stated
bound exists to remove. The 6 not-swept operands are named individually, because
a count of what is uncovered that cannot be pointed at is the same silence as no
count at all.

**The partition is total by construction and the total is re-derived.**
`operand_columns` appends every operand to exactly one list and its
fall-through is a named column, not a `continue`; `operand_columns_total` walks
the sources a **second** time and the two numbers are compared. Deleting the
`not swept: nested` column makes the totality claim go red — `p1 (v)`.

**E4's per-file half.** The `operands` column read 2 for `posets.py`, under a
heading that said *operands the sweep deletes*, and the sweep deletes 0 there.
The two populations were derived twenty lines apart. They now share one
constant, `SWEEP_FILES` in `d2_deletion.py`, read by the sweep and by the table
that describes it — and the claim compares the `swept` column to the sweep's own
rows **function-by-function and text-by-text**, not count-by-count.

**Why the narrowing is not cosmetic.** The 4 nested operands, deleted one at a
time with everything else standing: **4 of 4 CHANGE the artifact**, exit 1. They
are not idle, so leaving them implicitly on the covered side was a real
over-claim. `p1 (iv)`, with an empty-baseline guard so that two failed runs
cannot compare `IDENTICAL`.

## OPEN 2 — the reason, corrected; the row, untouched

The reason read

> then both are moved together, because two changes that cancel would pass each
> half on its own

and it names an input. Built, both ways:

| input | c1 half | kern half | `both together` |
|---|---|---|---|
| **cancelling** — kern's `dim L(n,p)` one too big, c1's dims one too small | MOVED | MOVED | **IDENTICAL** |
| **conspiring** — kern gains a name the shipped c1 never reads; c1 reads it with a default of 0 | IDENTICAL | IDENTICAL | **MOVED** |

The halves catch a cancelling pair. `both together` is what catches the pair
that passes them. The row's `(script, kernel)` argument pair is **unchanged**;
what changed is the sentence, in five places, and the row's own label
(`cancellation` → `conspiracy`), which was a one-word reason naming the case the
row does not catch.

**The conspiring pair is new.** Nothing in mg-76cc built it, and nothing in
mg-e34a built it either — that audit built the cancelling pair, which is what
its finding needed. Without a conspiring pair, *"the row is load-bearing"* is an
assertion of exactly the kind this ticket is about.

## The mechanism both sites share

> A repair's output is more than one artifact. Verification that covers the
> primary one and not its accompanying explanation leaves the explanation
> unaudited **by construction**.

mg-f7e1 shipped a sweep **and a sentence about the sweep**; only the sweep was
measured. mg-76cc shipped a row **and a reason for it**; only the row was
measured. `p4` enumerates the **kinds** — rows, reasons, labels, docstrings,
comments, source anchors in other files, transcripts, documents, commit text —
and gives each a disposition.

That enumeration earned its keep: renaming one label moved
`lib76cc.HALF_BOTH_ROW`, an exact **source anchor in a file this repair was not
about**, which `r1_kernel.py`'s deletion test uses. Nothing in "fix the reason
for the row" named that kind of artifact.

**Commit text is the one kind that cannot be repaired.** `bfd7948` carries the
wide bound and `4755d02` carries the inverted reason, and a commit message
cannot be changed without rewriting history. Its disposition is a **pointer**:
both revisions are named in the repaired tree, so a reader arriving from
`git log` reaches the correction. `p4 (ii)` checks that and says plainly that
this branch honestly cannot exhibit the fix.

## What this repair does NOT close

* **mg-eaef's E8** — `d2_deletion.py` exits 1 at HEAD, and has since `bfd7948`,
  on the claim `AND THE PIN IS WHAT IT SAYS IT IS`. `p2 (i)` requires it to be
  the **only** broken claim in that run, so a second break is a finding here.
* **mg-eaef's E9** — the covering pair for the uncovered `order` half is still
  unrun.
* **mg-eaef's E3 / rung seven** — a decision in no condition at all is outside
  every column in the table above; the `expression nodes in all` total is where
  it is counted, and that total bounds how much is there without naming what.
* **mg-e34a's E-2** — the two half rows are promoted to findings that say the
  198 cells must be re-taken while `both together` prints IDENTICAL on the same
  run. That is a defect of the findings, not of the reason, and it is not this
  ticket.

## Running it

```sh
sh code/repair_69d1/run_all.sh      # about 100 s
```

No pipes, no network, no third-party packages. Each script's stdout is
redirected and its status re-read, so a red verifier cannot hide under a green
runner (mg-c2b3, mg-f922).
