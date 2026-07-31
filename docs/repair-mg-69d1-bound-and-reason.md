# mg-69d1 — two open sites: a bound wider than its sweep, and a reason that is inverted

**Repair of:** mg-eaef **E5** and **E4** (on `bfd7948`, item mg-f7e1) and
mg-e34a **E-1** (on `4755d02`, item mg-76cc).
**Instrument:** `code/repair_69d1/` — 5 scripts, 40 self-test assertions,
worst exit 0.
**Neither site deferred.**

---

## What was open

| | audit | finding | one sentence |
|---|---|---|---|
| **OPEN 1** | mg-eaef | **E5**, **E4** | the instrument's stated bound is **wider than the sweep it describes**, and 4 of `face_complex.py`'s 15 explicit boolean operands are in **neither** census column |
| **OPEN 2** | mg-e34a | **E-1** | the `both together` row `mg-76cc` added is **right**, and the **reason** given for it is **inverted** |

They look unrelated. They are the same shape, and §4 is about that.

---

## 1. OPEN 1 — the bound, narrowed to the sweep

### The sentence

It read:

> DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO FURTHER

Read as written, that is a guarantee about **every** explicit boolean operand.
It is not one. It now reads:

> DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS OF THE DECIDING CONDITIONS IN
> THE FILES THIS SWEEP VISITS, AND NOTHING ELSE

Both clauses are load-bearing and each answers one half of the finding:
*top-level* answers **E5**, *in the files this sweep visits* answers **E4**.

The sentence lives in four places and all four moved: `d2_deletion.py`'s bound
section and its module docstring, `face_complex.absorb_trace`'s docstring,
`code/face_geometry_instr_5f9a/run_all.sh`, and
`docs/landing-mg-0b07-implicit-disjunction.md`. `p1 (i)` finds them by
`git grep` over the **working tree**, untracked files included, so a copy
nobody remembered is still in the population.

### All 17, in exactly one named column

| file | swept | not swept: file | not swept: nested | not determined | all |
|---|---|---|---|---|---|
| `face_complex.py` | 11 | 0 | 4 | 0 | **15** |
| `posets.py` | 0 | 2 | 0 | 0 | **2** |
| **ALL** | **11** | **2** | **4** | **0** | **17** |

**`not determined` is a column, not an omission.** It reads 0 on this tree and
is printed anyway. *Neither column* is not a third state — it is the absence of
an answer, and that absence is exactly the ambiguity a stated bound exists to
remove. An explicit *not determined* is checkable; an empty cell is not.

The 6 not-swept operands are printed **individually**, with function, kind and
text. A count of what is uncovered that cannot be pointed at is the same silence
as no count at all:

```
   posets.py        _is_transitively_closed  guard  not swept: file    b == c
   posets.py        _is_transitively_closed  guard  not swept: file    (a, d) not in rel
   face_complex.py  proper_ideals            value  not swept: nested  m != 0
   face_complex.py  proper_ideals            value  not swept: nested  m != full
   face_complex.py  mat_eq                   value  not swept: nested  len(a) == len(b)
   face_complex.py  mat_eq                   value  not swept: nested  all(x == y for x, y in zip(a, b))
```

**Why they were in neither.** `deciding_clauses` asks whether the **condition
is** a `BoolOp` and takes its top-level operands, so a nested `or` is not in
`operands`. `implicit_disjunctions` skips the forms `or` and `and` **by name**,
on the assumption that anything spelled with an operator is deletable — so a
nested `or` is not in `compounds` either. The new walker, `boolean_operands`,
applies **no filter at all**: it walks for `ast.BoolOp` and takes every value of
every one it finds. That is the only reason it cannot miss them.

**The partition is total by construction, and the total is re-derived.**
`operand_columns` appends every operand to exactly one list and its fall-through
is a *named column*, not a `continue`. `operand_columns_total` walks the sources
a **second** time, and `d2` compares the two numbers in a scored claim. That is
not the classifier checking its own arithmetic.

### E4 — the column that said `deletes`

`operands` read **2** for `posets.py`, under a heading that said *operands the
sweep deletes*, and the sweep deletes **0** there. The same transcript printed
`NOT SWEPT` twenty lines above. Two populations about one thing, derived
separately, twenty lines apart.

The fix is structural, not editorial. `SWEEP_FILES` in `d2_deletion.py` is now
the single constant the sweep runs over **and** the table describing it reads,
and the scored claim compares the `swept` column to the sweep's own enumerated
rows **function-by-function and text-by-text** — not count-by-count, which is
what let 2 match 0 in the first place. The census column is headed `top-level`,
which is what it counts.

### Why the narrowing is not cosmetic

The 4 nested operands, each deleted alone with everything else standing:

| function | operand | artifact | exit |
|---|---|---|---|
| `proper_ideals` | `m != 0` | **CHANGES** | 1 |
| `proper_ideals` | `m != full` | **CHANGES** | 1 |
| `mat_eq` | `len(a) == len(b)` | **CHANGES** | 1 |
| `mat_eq` | `all(x == y for x, y in zip(a, b))` | **CHANGES** | 1 |

**4 of 4.** They are not idle, so leaving them implicitly on the covered side
was a real over-claim and not a wording problem. `p1 (iv)` measures this with an
**empty-baseline guard**: a mutation producing no artifact would otherwise
compare `IDENTICAL` to another failure, which is the one reading a deletion test
must never make. (mg-eaef made exactly that mistake once and kept it; so does
this instrument's own miss list.)

This table is mg-eaef's E2 re-derived. Its registered prediction was
`BYTE-IDENTICAL` on all four, and the miss is that audit's, kept as written —
the assumption that what the sweep skips is what the battery cannot see was
wrong in the direction that matters.

### The control, where the defect is still present

Two directions, because a control shown only against a repaired tree cannot tell
*not covered* from *not coverable*:

* the old pair of columns recomputed on **`bfd7948`'s** sources — the commit
  that stated the wide bound — leaves **4** operands in neither, the same 4 the
  tree at HEAD has. The **source** did not change. What changed is that all 17
  now have a printed answer.
* the classifier with `not swept: nested` **deleted**: 3 columns, sum 13,
  independent walk 17 — the totality claim **goes red**. The column is what
  makes it true.

---

## 2. OPEN 2 — the reason, corrected; the row, untouched

`mg-76cc` added a third row to `g1`'s section (v) and gave it a reason:

> then both are moved together, because two changes that cancel would pass each
> half on its own.

**A rationale is a claim, and this one names an input.** mg-e34a built it.
`p3` builds it again, and builds the other one too:

| input | c1 half | kern half | `both together` |
|---|---|---|---|
| **cancelling** — kern's `dim L(n,p)` one too big, c1's vertex dims one too small | MOVED | MOVED | **IDENTICAL** |
| **conspiring** — kern gains a name the shipped c1 never reads; c1 reads it with a default of `0` | IDENTICAL | IDENTICAL | **MOVED** |

The first row is why the sentence was inverted: the two **halves** are what
catch a cancelling pair, and the row named `cancellation` is the only one of the
three that a cancelling pair **passes**.

The second row is **new**. Nothing in mg-76cc built a conspiring pair, and
nothing in mg-e34a built one either — that audit built what its finding needed.
Without it, *"the row is load-bearing"* is an assertion of exactly the kind this
ticket is about. Built here, it passes both halves and is caught by `both
together` and by nothing else.

Each pair is verified to be the **kind** of pair it is called before any row
rests on it: the cancelling halves must each move the measurement and must
restore it together; each conspiring half must be a **no-op** on its own, which
the self-test also checks on strings — the kernel half only appends a module
assignment, and the c1 half reads it with a default of `0`, not `1`.

### What moved, and what did not

The row's `(script, kernel)` argument pair is **unchanged**. What moved:

* `g1_provenance.py`'s module docstring
* `g1_provenance.py`'s printed section (v)
* the row's **label**, `cancellation` → `conspiracy` — a one-word reason that
  named the case the row does *not* catch
* `docs/repair-mg-76cc-kernel-half-and-five-outputs.md`
* `r1_kernel.py`'s failure message, which called it *"the cancellation case"*
* `lib76cc.HALF_BOTH_ROW` — see §4

`r1_kernel.py`'s **other** sentence, *"a cancelling pair cannot pass"*, is
**true** and is left standing: it is a claim about section (v) as a whole, and
section (v) does catch a cancelling pair — at 2 of its 3 rows. mg-e34a excluded
it by hand; `p3 (iii)` scores it instead, and scores the conspiring pair the
same way (caught at 1 of 3).

---

## 3. This deliverable, checked for the defects it remedies

This repair **states bounds** and **gives reasons**, which is what the two
defects are made of. `p4 (iii)` turns both checks on it.

**Every bound this instrument states, with how it is kept narrow:**

1. `p1 (i)`'s quotation discriminator is a **proximity test, not a path list**,
   and it cannot tell a quotation from an assertion that cites the ticket
   nearby. Stated at the site, with the window printed beside the result, and
   shown **non-vacuous** by `p3 (i-b)`: run unchanged against `HEAD` it reports
   exactly the 4 live assertions mg-e34a booked.
2. `not determined` reads 0 on this tree, so the column is **printed and not
   exercised**. Said in the transcript rather than inferred from a table with no
   such row; `p1 (v)` exercises the partition a different way, by deleting a
   column and requiring the claim to go red.
3. `p1 (iv)`'s `CHANGES` is about the **control battery's artifact**, which is
   the grain `d2`'s own sweep uses — not about the mathematics.
4. `d2_deletion.py` **exits 1 at HEAD** for mg-eaef's E8, which this repair does
   **not** close. `p2` names the claim and requires it to be the **only** broken
   one, so a second break is a finding rather than noise.
5. The conspiring pair is **one constructed input, not a class**. It shows the
   row catches something no half catches. It does not show it catches every
   conspiracy, and that line is drawn in the transcript.

**Every reason this instrument gives names an input that was BUILT** — the
conspiring pair, the cancelling pair, the 4 nested deletions, the deleted
column, and the pre-repair census at `bfd7948`. `p4 (iii)` gates on it.

**And what that section cannot do**, said plainly: both lists are written by the
author of the thing they are about. Every entry names a section that runs, so
they are checkable; they are not independent. The independent check is an audit.

---

## 4. The mechanism, which is the thing to carry

mg-e34a's auditor stated it:

> **the repair added a ROW and a REASON, and only the row was checked.**

Generalised:

> **A repair's output is more than one artifact. Verification that covers the
> primary one and not its accompanying explanation leaves the explanation
> unaudited by construction.**

Not by oversight — *by construction*, because the verification was aimed at a
different artifact. Both open sites are instances. mg-f7e1 shipped a sweep **and
a sentence about the sweep**; the sweep was measured and the sentence was not.
mg-76cc shipped a row **and a reason for it**; the row was measured and the
reason was not.

So `p4 (i)` enumerates the **kinds** of output — not the same-kind defects — and
gives each a disposition:

| kind | emitted | what checked it |
|---|---|---|
| code / rows | yes | `p1 (ii)(iii)(iv)`, `p3 (iii)`, d2's two new claims |
| reasons / rationales | yes | `p3 (iii)` builds both inputs; `p1 (i)(iii)` scores the bound against the sweep |
| labels | yes | `p2 (ii)` reads it out of g1's stdout; `p3 (iii)` measures the case it names |
| docstrings | yes | the same `git grep` — a docstring is not exempt |
| comments | yes | the same grep; and `SWEEP_FILES` is a **constant**, not a comment |
| **source anchors in other files** | yes | see below |
| committed transcripts | yes | regenerated; `p2` scores each subject's own stdout |
| landing / repair documents | yes | the same grep; corrections stand **beside** what they correct |
| commit text | **no** | immutable — disposition is a pointer, `p4 (ii)` |

**The enumeration earned its keep on row six.** Renaming the label moved
`lib76cc.HALF_BOTH_ROW`, an exact source span in a file this repair was not
about, which `r1_kernel.py`'s deletion test uses to remove that row. Left alone
it would have raised `expected exactly 1 occurrence` and taken a whole section
of `mg-76cc`'s instrument red — on a repair that changed one word of prose.
Nothing in *"fix the reason for the row"* named that kind of artifact. The
enumeration did.

**Commit text is the branch that honestly cannot exhibit the fix.** `bfd7948`
carries the wide bound and `4755d02` carries the inverted reason, and neither
can be changed without rewriting history. The disposition is a **pointer**: both
revisions are named in the repaired tree, so a reader arriving from `git log`
reaches the correction. `p4 (ii)` checks that the pointer exists and says the
reason plainly rather than leaving a gap.

---

## 5. What is NOT closed here

* **mg-eaef E8** — `d2_deletion.py` exits 1 at HEAD, and has since `bfd7948`, on
  `AND THE PIN IS WHAT IT SAYS IT IS`. Out of scope; **named** and required to
  be the only break.
* **mg-eaef E9** — the covering pair for the uncovered `order` half is still
  unrun. Declining to add it remains the subject's argument.
* **mg-eaef E3 / rung seven** — a decision in no condition at all is outside
  every column in §1's table. `expression nodes in all` is where it is counted,
  and that total bounds how much is there without naming what. The chasing does
  not terminate, which is why a **stated** bound is the right move; the
  objection was to its width, not to its existence.
* **mg-e34a E-2** — the two half rows are promoted to findings saying the 198
  cells must be re-taken while `both together` prints `IDENTICAL` on the same
  run. A defect of the findings, not of the reason.

## 6. Disclosures

* **`code/face_geometry/face_complex.py` is edited** — its `absorb_trace`
  docstring carried the wide bound. The change is prose only; the artifact
  regenerates and `d2`'s 51 claims are unaffected by it.
* **Transcripts are regenerated by each instrument's own runner, not one file
  at a time — and that was learned the hard way here.** `out_g1_provenance.txt`
  was regenerated alone first, because it is the only one of `mg-58da`'s five
  that this repair changes. `mg-76cc`'s `r2_reproduce.py` measures a
  **set-level** property those five share: they must all name **one** HEAD
  revision, so a single normalisation explains every differing line. With g1 at
  `e494515b` and the other four still at `e006581c`, that normalisation covered
  `5 of 9` differing lines instead of `9 of 9`; `r2` went to **3 findings**, and
  `r4_doccheck.py` then booked the document's own `9 of 9` as a figure appearing
  in no transcript. **One edit, two instruments red, neither of them the one
  being repaired.** Fixed by running `mg-58da`'s and `mg-76cc`'s own runners.
  *This is §4's lesson landing on §4's author:* `committed transcript` looked
  like one kind of artifact and behaves like a **set**, and enumerating the
  kinds is not enough when a kind's members carry an invariant between them.
  `p4 (i)`'s transcript row says so, and `PREDICTIONS.md` keeps it as miss #4.
* **Regenerated:** `out_d2_deletion.txt`; `mg-58da`'s five (`selftest`, `g1`,
  `g2`, `g3`, `g4` — the last four only for the revision they name);
  `mg-76cc`'s `out_r1_kernel.txt`, `out_r2_reproduce.txt`, `out_r4_doccheck.txt`.
  Each records the revision it was run at, which is this branch's HEAD
  **before** the commit that lands them; a committed record can never be fresher
  than one commit, and that is stated here rather than presented as staleness
  nobody noticed.
* **`mg-58da`'s `run_all.sh` exits 1 on `g4_fleet.py`, as it did before**, on
  `c3_withdrawal.py` being red on the repaired tree — mg-d330's second finding,
  which is not closed here and is not touched. The finding count is unchanged
  at 3; only the revision the transcripts name moved.
* **mg-e34a's own instrument is run unmodified and is NOT edited.** `k4_cancel.py`
  still books its rationale finding, because it counts every copy of the
  sentence in the tree including the copies in its **own** transcript and
  prediction file — which are the record of what it found, and a repair does not
  get to edit an audit's record. `p2 (iii)` scores its **measurement** instead,
  and the three rows read exactly as they did before: this repair did not touch
  the row.
* **No `| tee`** (mg-f922, mg-c2b3): `run_all.sh` redirects each stdout and
  re-reads `$?`.
* **Nothing under `code/face_geometry/` is written by any run here.** Every
  mutation is applied to a copy in a temporary directory.

Registered predictions, hits and the three misses: `code/repair_69d1/PREDICTIONS.md`.
