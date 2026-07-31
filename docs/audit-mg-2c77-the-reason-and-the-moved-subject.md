# mg-2c77 — independent audit of the mg-69d1 repair (`d01ff32`)

> **THE REASON IS RIGHT AND THE COMPARISON THAT CONFIRMED THE KERNEL HALF NO
> LONGER COMPARES WHAT IT NAMES.** Both inputs the corrected reason names were
> built independently, plus a second conspiring pair of a different shape and a
> third input that is neither — 12 row readings, every one as the sentence says.
> The narrowed bound holds at its edge: one operand moved across each of its
> three clauses and the sweep saw exactly the one inside. **But `mg-69d1`
> touched `g1_provenance.py`, and `libe34a` derives the subject of `mg-e34a`'s
> pre-repair comparison as *the last commit that touched `g1_provenance.py`*.**
> `REPAIR_REV` moved from `4755d02` to `d01ff32`, both sides of the comparison
> are now `mg-76cc`'s already-repaired predicate, and `0 backwards at either
> grain over 7 inputs` — the confirmation that the kernel half is genuinely
> back — is not re-derived by this run. It is the same number reached by a
> different measurement. `k1_prerepair.py` says so itself in two findings; it
> was not re-run.
>
> **AND THE CENSUS BESIDE THE NARROWED BOUND IS STILL WIDE.** `explicit boolean
> operand` denotes **39** operands in the census's two files. The table
> classifies **17**. **22 are in no column** — 20 in `face_complex.py`, 2 in
> `posets.py`, named individually. The bound sentence itself is correct; it is
> the census printed beside it that carries `mg-eaef`'s `E4` state one rung out,
> in the artifact that repairs `E4`.

Instrument: `code/audit_2c77/` — 6 scripts, 48 self-test assertions, worst exit
1 (predicted 1). Full record: `code/audit_2c77/README.md`.

---

## The two halves of the repair, scored

| | `mg-69d1` claimed | this audit found |
|---|---|---|
| **OPEN 2 — the reason** | a cancelling pair moves both halves and passes `both together`; a conspiring pair passes both halves and is caught by `both together` alone | **CONFIRMED**, on an instrument that imports none of `lib69d1`, and on a second conspiring pair of a different shape |
| **OPEN 1 — the bound** | deletion reaches the top-level boolean operands of the deciding conditions in the files this sweep visits, and nothing else | **CONFIRMED at the edge**, by perturbation rather than by comparison |
| **OPEN 1 — the census** | ALL 17 ARE CLASSIFIED | **WIDE.** 39 denoted, 17 classified, 22 in no column |
| **the confirmation to preserve** | *(not re-run)* | **the numbers hold and the comparison does not** |

## A-1 — the moved subject

`libe34a` is written the right way round:

```python
# REPAIR_REV is the last commit that touched g1_provenance.py; PRE_REV is its
# first parent.  Written this way because mg-76cc's own lib carries the
# pre-repair revision as a literal, and a literal cannot notice that the file
# moved again.
REPAIR_REV = last_touching(G1_REL)
PRE_REV    = resolve(REPAIR_REV + "^")
```

The comment is exactly right about the failure mode it was avoiding. It did not
anticipate the file moving **for a reason that is not a repair of the
predicate** — `mg-69d1` edited `g1_provenance.py` to correct a *sentence*.

| | `REPAIR_REV` | `PRE_REV` | `== lib76cc.REV_957F` |
|---|---|---|---|
| at `e5787e1` (the repair's parent) | `4755d02` | `e006581c` | **yes** |
| at `d01ff32` | `d01ff32` | `e5787e1` | **no** |

`k1` still prints `Backwards at the exit grain: 0`, `Backwards at the finding
grain: 0`, `Files named by an old finding and by no new one: 0`, over 7 inputs.
Every number is what `mg-e34a` booked. **Every number is now about a different
pair of revisions**, and the two of them differ only in prose.

The remedy is not to write the revision down — `libe34a`'s comment explains why
that is worse. It is for the derivation to name *the repair it is about* rather
than *the last edit to the file*. That is a ticket, not a line, and it is left
open here.

## A-2 — the census, counted

`kern5f9a.boolean_operands` walks only inside `deciding_conditions`; a deciding
condition is an `if` with a `return` somewhere inside it, or a `return` with a
value. Everything else is outside all four columns.

| file | every `and`/`or` operand | in a deciding condition | **in no column** |
|---|---|---|---|
| `face_complex.py` | 35 | 15 | **20** |
| `posets.py` | 4 | 2 | **2** |
| **ALL** | **39** | **17** | **22** |

All 22 named in `out_q3_operands.txt` — `Poset.__init__`'s transitive closure,
`canonical_key`, `order_ideals`, `sur_iso` twice, `chains_of_ideals` twice,
`down_laplacian_from_boundary`, `top_laplacians` twice, and `cover_string`.

The claim is written without the deciding-condition qualifier at **15 sites in
files `d01ff32` touched**. `mg-eaef` was not consistent about the qualifier
either — my own control for that premise self-errored and the miss is kept —
so the finding rests on the subtraction, not on anyone's wording.

## A-3, A-4, A-5 — three checks that do less than they say

* **`p1 (v)`'s column deletion.** It prints *"with `not swept: nested` deleted
  from the classifier"* and drops a key from the result dict. Delete the branch
  from `operand_columns` itself and the totality claim stays **GREEN** at 17 of
  17, because the 4 nested operands fall through into `not determined`. The
  numbers are right for what the row does; the sentence names something else.
* **`not determined` is unreachable by any input.** `not op.top` and `op.top`
  are exhaustive over a bool; `0` of `614` operands across `444` python files
  reach it. It is right to print the column — what fails is the stated reason,
  which reads as a claim about the tree.
* **The live-assertion rule is blind where the repair writes.** A fresh,
  uncorrected assertion is reported as refuted at **6 of 9** insertion points
  under `code/repair_69d1/` and **2 of 18** elsewhere, because every file there
  says `mg-69d1`, which is a correction marker. `mg-69d1`'s own `miss #2`
  records this check being replaced for being a path list; the marker set is a
  path list again, spelled differently.

## What holds

The corrected reason, at `g1`'s own rows:

| input | c1 half | kern half | `both together` |
|---|---|---|---|
| cancelling | MOVED | MOVED | **IDENTICAL** |
| conspiring A (`mg-69d1`'s, rebuilt) | IDENTICAL | IDENTICAL | **MOVED** |
| **conspiring B — new here** | IDENTICAL | IDENTICAL | **MOVED** |
| one-sided (neither case) | IDENTICAL | MOVED | MOVED |

`p3` scored these at `(bent, HEAD)` where `g1` scores them at
`(bent, REV_A218)`, and called them the same rows. **0 of 12 verdicts differ.**
Checked because the docstring made a claim, reported because it was checked.

The bound at its edge: unperturbed 11 sweep rows; +1 operand inside all three
clauses → **12**; +1 nested, +1 in a non-returning `if`, +1 in `posets.py` →
**11, 11, 11**. All 11 sweep rows applied remove exactly one operand and **0**
remove anything from outside the bound.

## Standing

`PREDICTIONS.md` was committed in `20a0e17` before any script existed. Five
misses are kept there. **Miss #5 is `A-1`**: I predicted `q4` would exit 0. I
had read that the repair touched the predicate and did not follow that through
to the instrument that derives its subject *from* the predicate's history.

Two items no list in the ticket named: `q5` entirely, and whether `not
determined` is *reachable* rather than merely *named*. `A-3` was planned by
nobody — it fell out of performing `q3 (iv)`'s deletion the way the sentence
describes rather than the way the code does.

This document and `code/audit_2c77/README.md` both contain the phrase `explicit
boolean operand`, so they join the population `q3 (iii)` counts (mg-6ef4). The
transcripts are regenerated after they were written.
