# `code/audit_2c77/` — the independent audit of the mg-69d1 repair

Subject: **`d01ff32`** — *"THE BOUND IS NARROWED TO THE SWEEP WITH ALL 17
OPERANDS IN A NAMED COLUMN, AND THE ROW'S REASON IS INVERTED NO LONGER"*.
Pre-filed in the same action as its parent.

## The verdict in one table

| | what was asked | what was found |
|---|---|---|
| **the reason** | build what the corrected reason names | **IT HOLDS.** Both inputs built independently, plus a second conspiring pair of a different shape and a third input that is neither. 12 row readings, every one as the sentence says |
| **the bound** | probe its edge from outside | **IT HOLDS.** One operand moved across each of the bound's three clauses; the sweep saw exactly the one inside it. All 11 sweep rows remove exactly one operand and never one from outside |
| **the pre-repair predicate** | re-run it | **THE NUMBERS HOLD AND THE COMPARISON DOES NOT.** `0 / 0 / 0` over 7 inputs — but the comparison's subject moved onto `mg-69d1`'s own commit, so `0` answers a different question |
| **the census beside the bound** | count the operands myself | **STATED WIDER THAN IT MEASURES.** 39 explicit boolean operands in the two files, 17 classified, **22 in no column** |
| **`not determined`** | is it a named state or an empty cell | **A named state no input can reach.** 0 of 614 operands over 444 files |
| **`p1 (v)`'s column deletion** | *(nobody asked)* | **The sentence names an operation the code does not perform** |
| **the live-assertion rule** | *(nobody asked)* | **Blind at 66% of points inside `code/repair_69d1/` and 11% outside it** |

Worst exit of the suite: **1**. Predicted **1**.

## The five findings, most severe first

### A-1 — `mg-e34a`'s pre-repair comparison no longer compares `mg-76cc`'s repair

`libe34a` derives its subject rather than writing it down:

```
REPAIR_REV = the last commit that touched g1_provenance.py
PRE_REV    = its first parent
```

and **`mg-69d1` touched `g1_provenance.py`**.

| | `REPAIR_REV` | `PRE_REV` | agrees with `lib76cc.REV_957F` (`g1 BEFORE mg-76cc`) |
|---|---|---|---|
| at `e5787e1`, the repair's parent | `4755d02` — mg-76cc's repair | `e006581c` | **yes** |
| at `d01ff32` and after | `d01ff32` — mg-69d1's own | `e5787e1` | **no** |

So `the predicate as it stood before the repair` now means *before mg-69d1*, and
both sides of the comparison are `mg-76cc`'s **already-repaired** predicate,
differing only in the prose `mg-69d1` edited. The three coverage numbers still
read `0 / 0 / 0` — and *"the pre-repair predicate run against 7 inputs with 0
going backwards at either grain"* is **not re-derived by this run**. It is the
same number reached by a different measurement.

`k1_prerepair.py` reports this itself, in two findings that are not in its
committed transcript. `mg-69d1` re-ran `k4_cancel.py` from that suite and did
not re-run `k1`.

This is `mg-eaef`'s `E8` — *a pin the repair itself invalidated* — one file
over, and it is the reason the standing rule says to run the pre-repair
predicate when a repair touches a predicate.

### A-2 — the census beside the bound is stated wider than the population it classifies

`kern5f9a.boolean_operands` walks only inside `deciding_conditions`, and a
deciding condition is exactly *an `if` with a `return` somewhere inside it* or
*a `return` with a value*. An `and` in a `while`, in an assignment, or in an
`if` whose body assigns and breaks is an explicit boolean operator and is in
**none** of the four columns.

| file | operands of every `and`/`or`, anywhere | in a deciding condition | **in no column** |
|---|---|---|---|
| `face_complex.py` | 35 | 15 | **20** |
| `posets.py` | 4 | 2 | **2** |
| **ALL** | **39** | **17** | **22** |

All 22 are named individually in `out_q3_operands.txt`. The claim is written
without the deciding-condition qualifier at **15 sites in files `d01ff32`
touched**, including `kern5f9a.py`'s own section header (*"EVERY explicit
boolean operand, in exactly one NAMED column"*) and `p1_bound.py`'s finding
population (*"the 17 explicit boolean operands of the census's two files"*).

**The narrowed BOUND sentence is not affected and is correct** — it names *the
deciding conditions*, and `q2` confirms it at its edge. The defect is in the
census printed beside it, which is `mg-eaef`'s `E4` state — operands in neither
column — one rung out, in the artifact that repairs `E4`.

### A-3 — `p1 (v)`'s deletion test names an operation it does not perform

`p1 (v)` prints

> with `not swept: nested` **deleted from the classifier**: … total: GOES RED

and what it does is `{c: v for c, v in cols.items() if c != "not swept: nested"}`
— it drops a key from the **result dict** and re-sums. The classifier is never
re-run.

| column | how it is deleted | sum | independent walk | verdict |
|---|---|---|---|---|
| — none — | as shipped | 17 | 17 | GREEN |
| `not swept: nested` | p1's: drop the result key | 13 | 17 | **RED** |
| `not swept: nested` | the branch, out of the source | 17 | 17 | **GREEN** |
| `not determined` | p1's: drop the result key | 17 | 17 | GREEN |
| `not determined` | the branch, out of the source | 17 | 17 | GREEN |

Delete the branch the sentence names and the totality claim stays **green**,
because the 4 nested operands fall through into `not determined`. The row's
numbers are right for what the row does; the sentence beside it names something
else — which is the shape of the defect this repair was written to fix.

The finding has a second half worth keeping: `not determined` **is**
load-bearing, against an edit to the classifier, and no sentence in the repair
claims that.

### A-4 — `not determined` is a named state no input can reach

```
if   fname not in swept_files:  ...
elif not op.top:                ...
elif op.top:                    ...
else:                           # pragma: no cover
    cols["not determined"].append(op)
```

`op.top` is `node is cond` — a bool — so `not op.top` and `op.top` are
exhaustive and the `else` is unreachable for **every** input. Confirmed three
ways: the branch structure, `0` of `614` operands across `444` python files
under `code/`, and the deletion pair above.

The ticket asked that the column be *an explicit named state rather than an
empty cell*. **It is**, and the repair is right to print it. What fails is the
stated reason — *"an explicit `not determined` is CHECKABLE"* and *"nothing
lands there **on this tree**"*. Both read as claims about the tree. The `0` is a
property of the control flow that no tree can move.

### A-5 — the rule that decides `live assertion` is blind where the repair writes

Both `p1 (i)` and `p3 (i)` end in a gate of the form *the old sentence is
asserted at 0 live sites*, and `live` is decided by *no correcting marker within
25 lines, in the same file*. The markers include `mg-69d1`. Every file
`mg-69d1` wrote says `mg-69d1`.

A fresh, uncorrected assertion planted at three points per file:

| insertion points in | blind | tried | rate |
|---|---|---|---|
| `code/repair_69d1/` — the fix | 6 | 9 | **66%** |
| everywhere else tried | 2 | 18 | 11% |

`p3_reason.py` is blind at **3 of 3**.

`mg-69d1`'s own `miss #2` records that this check began as a **path list**
exempting the three files the sentence was live in, and was replaced for being
vacuous by construction. `p3 (i-b)` demonstrates non-vacuity by running the rule
against HEAD and finding live assertions in `mg-eaef`'s files — which is where
the **old** defect lived. Non-vacuity in the directory the defect came from is
not non-vacuity in the directory the fix goes to.

## What HOLDS, and it is the larger half

**The corrected reason is right, and it is right for a second input nobody
built.** Every claim it makes was constructed and measured at `g1`'s own rows:

| input | c1 half | kern half | `both together` | caught at |
|---|---|---|---|---|
| **cancelling** — kern `dim L(n,p)` +1, c1 dims −1 | MOVED | MOVED | **IDENTICAL** | 2 of 3 rows |
| **conspiring A** — integer default of 0 (mg-69d1's, rebuilt here) | IDENTICAL | IDENTICAL | **MOVED** | 1 of 3 rows |
| **conspiring B** — **new here**: boolean default of `False`, adds a vertex | IDENTICAL | IDENTICAL | **MOVED** | 1 of 3 rows |
| **one-sided** — kern alone, neither case the reason names | IDENTICAL | MOVED | MOVED | 2 of 3 rows |

`p3` scores the pairs at `(bent, HEAD)` where `g1` scores them at
`(bent, REV_A218)`, and its docstring calls them *"the same three (script,
kernel) rows g1's HALVES uses"*. They are not the same rows — and **0 of 12 row
readings differ**, so nothing rests on it. Said because it was checked, not
because it turned up anything.

`MOVED` really is a catch: `g1`'s finding-booking block, executed here on
synthetic input, books 0/1/2 findings for 0/1/2 moved rows, and `g1` exits 0 iff
findings are 0.

**The narrowed bound holds at its edge.** One operand moved across each clause:

| probe | sweep rows | column |
|---|---|---|
| unperturbed | 11 | — |
| **inside** all three clauses | **12** | `swept` |
| nested under a comprehension | 11 | `not swept: nested` |
| in an `if` that does not return | 11 | **NO COLUMN** ← this is A-2 |
| top level, in `posets.py` | 11 | `not swept: file` |

And `AND NOTHING ELSE`: all 11 sweep rows applied, each removing exactly one
operand, **0** of them removing anything from outside the bound.

## The scripts

| script | what it measures | exit |
|---|---|---|
| `selftest_2c77.py` | 48 assertions: my walkers against the shipped ones **span for span**, the position key, every bend's refusal on 0 and on many, the IDENTICAL/MOVED test on inputs whose answer is known, the empty-baseline guard | 0 |
| `q1_reason.py` | the kinds of output `d01ff32` emitted with a disposition each; 4 inputs × 3 rows × 2 row signatures; the row's argument pair against `4755d02`; `lib76cc.HALF_BOTH_ROW`; `g1`'s finding block executed | 0 |
| `q2_bound_edge.py` | the bound's three clauses probed one operand at a time from outside; `AND NOTHING ELSE` differenced over all 11 sweep rows | 0 |
| `q3_operands.py` | both operand populations walked here; the shipped classifier fed from outside; `not determined` asked three ways; both column deletions | **1** |
| `q4_prerepair.py` | `mg-e34a`'s `k1_prerepair.py` re-run unmodified; three coverage numbers gated separately; the finding SET against the committed transcript; what the comparison's subject now is | **1** |
| `q5_discriminator.py` | the shipped live-assertion rule, read out of `p1`/`p3` and applied to planted assertions | **1** |

## Standing

* **Floor, not scope.** Two items no list in the ticket names: `q5` entirely,
  and `q3 (iv)`'s question of whether `not determined` is *reachable* rather
  than merely *named*. `A-3` was not planned by anyone — it fell out of doing
  `q3 (iv)`'s deletion the way the sentence describes.
* **Predictions before probes.** `PREDICTIONS.md` was committed in `20a0e17`,
  before any script here existed. Five misses are kept there with what was
  wrong beside each. Miss #5 is the largest and it is `A-1`.
* **No bare totals.** Every count names its population; the 22 uncovered
  operands are named individually.
* **Nothing is written.** No run touches `code/face_geometry/`,
  `code/face_geometry_instr_5f9a/`, `code/branching_audit_58da/`,
  `code/branching_audit_a218/`, `code/branching_audit_e34a/`,
  `code/branching_repair_76cc/` or `code/repair_69d1/`. Every mutation is in a
  temporary directory or in memory. No `| tee` (mg-c2b3, mg-f922); `run_all.sh`
  redirects and re-reads `$?`, and does **not** use `set -e` (mg-5040's fifth
  rung).

## What this audit did NOT settle

* Whether `both together` catches **every** conspiring pair. Two were built,
  of two different shapes. That is a stronger demonstration than one and it is
  still not a proof.
* `mg-eaef`'s `E8`, `E9` and rung seven, and `mg-e34a`'s `E-2` — named as open
  by the repair and left open here.
* Whether the narrowed bound is the **narrowest** true one.
* `A-1`'s remedy. `libe34a`'s derivation is the *right* shape — a literal
  cannot notice that a file moved — and it now needs to name the repair it is
  about rather than the last edit to the file. That is a ticket, not a line.

## Running it

```sh
sh code/audit_2c77/run_all.sh      # about 80 s; worst exit 1
```

No pipes, no network, no third-party packages.
