# mg-2c77 — predictions, registered BEFORE any probe runs

Independent audit of the mg-69d1 repair (`d01ff32`), pre-filed in the same
action as its parent.

Everything below was written from **reading** `d01ff32` and the sources it
touches. Nothing in this file was measured. Misses stay as written, with what
was wrong beside them, in the same table.

## What I read before predicting, and what that entitles me to

I read the repair's commit message, `README.md`, `PREDICTIONS.md`,
`out_p1_bound.txt`, `p3_reason.py`, `lib69d1.py`, `kern5f9a.py`'s new section,
`g1_provenance.py`'s section (v), and `face_complex.py` lines 50–150. So the
first two predictions below are **read off the code's branch structure and are
not foresight** — they are stated here as predictions because the honest form
is to register them before running, not to present them afterwards as insight.
Said plainly rather than dressed up.

The operand **counts** are foresight: I did not run a walker before writing
them.

## Exit codes

Each script exits 0 iff SELF-ERRORS == 0 and FINDINGS == 0. A predicted 1 is a
prediction that this audit has something to report, not that the script breaks.

| script | predicted | actual |
|---|---|---|
| `selftest_2c77.py` | 0 | |
| `q1_reason.py` | 0 | |
| `q2_bound_edge.py` | 0 | |
| `q3_operands.py` | **1** | |
| `q4_prerepair.py` | 0 | |
| `q5_discriminator.py` | **1** | |
| `run_all.sh` (worst) | **1** | |

## Q1 — the REASONS, not the rows

The repair replaced one reason with another and the new one is a claim with a
named input. Both inputs get built here, independently of `lib69d1`, and
scored **at `g1`'s own three rows** — `(head_c1, old_kern)`, `(old_c1,
head_kern)`, `(head_c1, head_kern)` — and not at `p3`'s, which hold the
un-bent side at **HEAD** where `g1` holds it at `REV_A218`.

| claim under test | predicted | actual |
|---|---|---|
| cancelling pair at g1's rows: c1 half / kern half / `both together` | MOVED / MOVED / **IDENTICAL** | |
| conspiring pair at g1's rows: c1 half / kern half / `both together` | IDENTICAL / IDENTICAL / **MOVED** | |
| p3's held-at-HEAD rows and g1's held-at-`REV_A218` rows give the same 6 verdicts | **yes** | |
| a MOVED row really books a `finding()` in g1 (so "caught" is a gate, not a printed word) | **yes** | |
| the row's `(script, kernel)` argument pair is unchanged from `4755d02` | **unchanged** | |

If the third row misses, `p3` measured rows that are not the rows the corrected
reason is about, and the reason would be unmeasured for the second time.

## Q2 — the bound, probed at its EDGE from outside

Not by reading the bound beside the sweep. By **perturbing the tree on each
side of the boundary the bound draws** and watching the sweep's own enumerated
population move or fail to move.

| probe | predicted | actual |
|---|---|---|
| the sweep's enumerated operand rows for `face_complex.py`, unperturbed | 11 | |
| add one operand to a **top-level** deciding condition in `face_complex.py` (inside the bound) → sweep rows | **12** | |
| add one operand to an `if` in `face_complex.py` that contains **no `return`** (outside the bound) → sweep rows | **11 — unmoved** | |
| that same outside operand, under the repair's 4-column classifier | **in NO column at all** | |
| add one operand to a **nested** position in a deciding condition (outside the bound) → sweep rows | **11 — unmoved** | |
| that nested operand, under the classifier | `not swept: nested` | |
| add one operand to `posets.py`, top level of a deciding condition (outside the bound, wrong file) → sweep rows | **11 — unmoved** | |
| that operand, under the classifier | `not swept: file` | |

The third row is the one that matters: it is a thing the sweep does not cover
which the **bound** correctly excludes and which the **census beside the
bound** does not account for at all.

## Q3 — all the operands, counted by me

`boolean_operands` walks only inside `deciding_conditions`, and
`deciding_conditions` admits exactly two forms: an `ast.If` with an
`ast.Return` somewhere inside it, and an `ast.Return` with a value. An `and` or
`or` in a `while`, in an assignment, in an `assert`, or in an `if` whose body
only raises or only assigns, is an explicit boolean operator and is in **none**
of the four columns.

`mg-eaef` wrote the qualifier every time: *"15 explicit boolean operand(s) **in
deciding conditions**"*. I predict the repair dropped it.

| claim | predicted | actual |
|---|---|---|
| `face_complex.py`, operands of every `ast.BoolOp` **anywhere in the file** | **32** | |
| `face_complex.py`, operands inside deciding conditions | 15 | |
| `posets.py`, operands anywhere in the file | **6** | |
| `posets.py`, operands inside deciding conditions | 2 | |
| operands of the two files in **no column of the repair's table** | **21** | |
| sites where the repair asserts the census over "every/all explicit boolean operand(s)" **without** the deciding-condition qualifier | **≥ 4** | |
| `not determined` reachable by ANY input | **NO — the branch is unreachable** | |
| deleting the `else: not determined` branch from the classifier: p1's totality claim | **stays GREEN** | |
| deleting the `not swept: nested` branch: p1's totality claim | goes RED (p1 already shows this; re-derived here) | |

Two findings predicted, hence exit 1:

* **Q3-A** — the census claim is stated over a population wider than the one it
  measures, which is `E5`'s own shape in the artifact that repairs `E5`.
* **Q3-B** — `not determined` is a named column no input can reach. The stated
  reason for printing it — *"an explicit `not determined` is checkable"* — is
  the part under test: a cell whose value is a constant of the control flow is
  not checkable, and `# pragma: no cover` on the branch says the repair knew
  the branch never runs.

`Q3-B` is one of my two **floor, not scope** items: the ticket asks that `not
determined` be *an explicit named state rather than an empty cell*. It is.
Whether any input can ever put an operand in it is a different question and no
list here names it.

## Q4 — do not disturb what is confirmed

`mg-e34a`'s `k1_prerepair.py` re-run at `d01ff32`, against the same 7 inputs.
The repair edited `g1_provenance.py`, which **is** the predicate `k1` runs on
both sides, and `mg-69d1` re-ran `k4_cancel.py` but not `k1`.

| claim | predicted | actual |
|---|---|---|
| `k1_prerepair.py` exit at `d01ff32` | 0 | |
| inputs declared | 7 | |
| OLD FIRES / NEW SILENT at the **exit** grain | 0 | |
| OLD FIRES / NEW SILENT at the **finding** grain | 0 | |
| a file named by an old finding and by no new one | 0 | |

Any regression here outranks everything above.

## Q5 — the quotation discriminator, over the repair's own files

**My second floor item, and no list names it.** `p1 (i)` and `p3 (i)` tell an
assertion of the old sentence from a quotation of it by looking for any of
`mg-69d1`, `mg-e34a`, `under test`, `inverted`, `INVERTED` within 25 lines, in
the same file. `miss #2` in the repair's own `PREDICTIONS.md` records that this
started life as a **path list** which exempted the three files the defect was
live in, and was replaced because that made it vacuous by construction.

Every file under `code/repair_69d1/` says `mg-69d1` many times.

| probe | predicted | actual |
|---|---|---|
| plant a **live** assertion of the wide sentence in `code/repair_69d1/README.md` → `p1 (i)` flags it | **NO — reported as refuted** | |
| plant the same in `code/face_geometry_instr_5f9a/d2_deletion.py` (marker-sparse) → flagged | **YES** | |
| plant a live assertion of the **old reason** in `code/repair_69d1/p3_reason.py` → `p3 (i)` flags it | **NO — reported as refuted** | |
| plant the same in `code/branching_audit_58da/g1_provenance.py` → flagged | **NO — g1 carries `mg-69d1` too** | |

If those come out as predicted, the marker window is a path list again, spelled
differently: it exempts by ticket id exactly the directories where a repair
writes its new prose, which is where a newly-wrong reason would be written.

## What I am NOT predicting, because I do not measure it

* Whether the corrected reason is **complete** — whether every conspiring pair
  is caught by `both together`. The repair states this limit itself in
  `p4 (iii)`. I build a **second, differently-shaped** conspiring pair, which
  strengthens the demonstration and still does not make it a proof.
* Whether the narrowed bound is the **narrowest** true one.
* `mg-eaef`'s `E8`, `E9`, rung seven, `mg-e34a`'s `E-2` — named as open by the
  repair and left open here.
