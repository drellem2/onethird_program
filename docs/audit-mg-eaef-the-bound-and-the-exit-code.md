# mg-eaef — independent audit of the mg-0b07 repair (`bfd7948`, item mg-f7e1)

**Subject:** `bfd7948` — *THE DISJUNCTION IS SPELLED WITH AN OPERATOR AND THE
BOUND IS A COUNT*. **Instrument:** `code/face_geometry_audit_eaef/`
(31 claims, 0 BROKEN, exit 0, 9 findings, ~6 min).

mg-0b07 left one open item: `clause` was not the floor, because
`[len(row) for row in A] != [len(row) for row in B]` is a disjunction Python
spells with no operator, and its ORDER half could be taken out with the width
half standing for a byte-identical artifact. It named two moves. **mg-f7e1 took
both**, so this audit checks both.

> **THE OPERATOR MOVE HOLDS AS FAR AS IT CAN GO, AND THE SUBJECT SAYS SO.** Both
> halves are really operands and each is really deletable alone; one of the two
> comes back byte-identical, printed as `NOT COVERED` on the row that carries
> its result. Reproduced here independently. Booked as a **disclosed limit**.
>
> **THE BOUND IS STATED WIDER THAN WHAT DELETION REACHES, TWICE.** On one of its
> two census rows the column `operands the sweep deletes` reads **2** for a file
> the sweep does **not visit** — the same transcript says `NOT SWEPT` twenty
> lines above. And the sentence the whole section exists to state — *DELETION
> ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO FURTHER* — names
> a floor it does not reach: **4 of the 15 explicit boolean operands** in
> `face_complex.py`'s deciding conditions are counted by **neither** census
> column, because the compound filter skips the forms `or` and `and` by name and
> an operator nested under a comprehension or a quantifier has no top-level
> handle. **All 4 change the artifact when deleted here** — they are the ones
> the battery would have seen.
>
> **AND THE INSTRUMENT THAT RAISED THE FINDINGS EXITS 1 AT HEAD.**
> `d2_deletion.py`, re-run in place with nothing edited, scores **1 BROKEN of
> 49**. The landing document says *92 claims, 0 BROKEN*. The claim that broke is
> the two-clause pin, and the commit that broke it is the repair itself.
>
> **WHAT IS CONFIRMED:** the declaration is still **DERIVED** after the
> restructuring, proved by changing the patch in two directions; and the
> re-measure re-derives at **8 UNDERSTATE / 3 AGREE / 0 OVERSTATE over 11**.

---

## 1. The operator move, re-run

The live guard, read out of the tree:

```python
    shape_A = [len(row) for row in A]
    shape_B = [len(row) for row in B]
    if len(shape_A) != len(shape_B) or any(
            a != b for a, b in zip(shape_A, shape_B)):
        return Trace(False, "shape", 0)
```

Each operand deleted alone, against a baseline regenerated in this run
(23,695 bytes, exit 0 — not read from `controls_output.txt`):

| deleted alone | artifact | exit | what it establishes |
|---|---|---|---|
| ORDER half `len(shape_A) != len(shape_B)` | **BYTE-IDENTICAL** | 0 | NOT COVERED |
| WIDTH half `any(a != b for a, b in zip(...))` | CHANGES | 1 | the battery covers it |

**FINDING E1 — the move bought a HANDLE, not a second covered half.** That is
what option 1 can buy and the subject prints it on the row rather than in a
paragraph. It is booked here as a **disclosed limit**, not a false claim: the
point of checking was that the move "should hold", and what holds is the
nameability, not the coverage.

## 2. Rung six — an explicit boolean operand the sweep does not reach

The subject's enumerator asks whether a **condition is** a `BoolOp` and then
takes its top-level operands. This audit **walks** for boolean operators. On
`face_complex.py`'s 73 deciding conditions:

| | count |
|---|---|
| explicit boolean operands in all | **15** |
| at the top level — the sweep's population, and the `operands` column | 11 |
| **nested under a comprehension or a quantifier** | **4** |

The four, each deleted alone with everything else standing:

| function | operand | artifact | exit |
|---|---|---|---|
| `proper_ideals` | `m != 0` | **CHANGES** | 1 |
| `proper_ideals` | `m != full` | **CHANGES** | 1 |
| `mat_eq` | `len(a) == len(b)` | **CHANGES** | 1 |
| `mat_eq` | `all(x == y for x, y in zip(a, b))` | **CHANGES** | 1 |

**FINDING E2.** Rung six is real and it is load-bearing. The registered
prediction for this table was BYTE-IDENTICAL on all four — on the assumption
that anything the sweep skips is something the battery cannot see. That was
wrong in the direction that matters, and the miss is kept in `PREDICTIONS.md`.

**FINDING E5.** The bound sentence names `explicit boolean operands` as the
level deletion reaches. Deletion reaches 11 of the 15. The other 4 are on
**neither** side of the census: not in `operands` (11), because their condition
is not a `BoolOp`; not in `compounds` (11), because the form filter skips `or`
and `and` **by name**, on the assumption that anything spelled with an operator
is deletable.

## 3. Rung seven — the decision that is not in a condition at all

`deciding_conditions` reads the test of an `if` and the value of a `return`.
Two assignments are neither, so the comprehensions that build the things being
compared are outside all five census columns — including the expression-node
total, which is offered as the one that depends on no classification.

Measured: the patch below moves the module's syntax-node count by **+8** and the
census's 1,002 by **+0**.

```diff
-    shape_B = [len(row) for row in B]
+    shape_B = [len(row) for row in B[:len(A)]]
```

| | result |
|---|---|
| artifact | **BYTE-IDENTICAL**, exit 0 |
| returns / statements / boolean operands removed | 0 / 0 / 0 |
| the predicate on `[[0,1],[1,0]]` vs `[[0,1],[1,0],[0,0]]` | live: `False` at gate `shape` → mutant: **`True` at gate `parity`** |
| brute force over all 2^m sign vectors | `False` |

**FINDING E3.** mg-0b07's defect, reinstated from a statement, invisible to the
battery and to every number the subject prints. The subject's own
`SELF_DEFECT_BRANCHES` entry 9 concedes the node total "bounds how much is there
and does not name what"; here it does not bound how much is there either.

**The eighth rung, named:** `zip` truncating at the shorter shape profile is a
decision with no operand, no operator and no statement of its own. That is why
the chasing does not terminate, and why a **stated** bound is the right move —
the objection is to its width, not to its existence.

## 4. The bound against the sweep, per file

| file | `operands` column says | the sweep deletes |
|---|---|---|
| `face_complex.py` | 11 | 11 |
| `posets.py` | **2** | **0** |

**FINDING E4.** The column is documented in the subject's kernel as *operands
the sweep can delete* and headed in the landing document *operands the sweep
deletes*. The same transcript prints, twenty lines earlier:

> `NOT SWEPT, and named rather than left out silently: posets.py has 2 more
> deciding clause(s) (_is_transitively_closed c1, _is_transitively_closed c2).`

Both statements are in one document and they disagree. The qualifier that
travels with the claim — *"posets.py adds 1 more, which no claim here covers"* —
is about the `compounds` column and not this one. A bound stated too generously
is worse than none, because it is read as a guarantee.

## 5. What is confirmed

**The declaration is still DERIVED.** A runnable copy of the subject's
instrument, one token of its `MUTATIONS` table rewritten, its own
`d2_deletion.py` run, the declaration read out of its own stdout — with no
declaration touched. Two directions, chosen to move different axes:

| direction | edit | declaration |
|---|---|---|
| W — widen the same unit | `AFTER-6` takes the `if` as well as the `return` | (1,0,0,7) → **(1,1,0,18)** |
| K — change the kind and the function | `AFTER-4` repointed at an operand of `gate_violations` | (0,1,0,4) in `absorb_trace` → **(0,0,1,11)** in `gate_violations` |

Each edit moved **1 of 11** declarations, and it is the row that was edited.
**FINDING E6 — confirmed, not a defect.** A restructuring did not revert it to
a written value.

**The re-measure.** mg-9220's eleven declarations executed out of `b6bc2ef`'s
own source, each patch applied to the tree that commit applied it to, the unit
computed by this audit's differ, the direction computed rather than inferred:

**8 UNDERSTATE / 3 AGREE / 0 OVERSTATE, population 11.** The three that agree
are `BEFORE-1`, `AFTER-3` and `AFTER-4`. **FINDING E7 — confirmed.**

## 6. The floor item: the exit code, and the unrun remedy

Chosen here, named by no list in the ticket.

**FINDING E8 — the subject's own instrument does not regenerate at HEAD.**

```
run in place, nothing edited:  exit 1
summary line               :  49 claim(s) scored; 1 BROKEN.
committed transcript says  :  49 claim(s) scored; 0 BROKEN.
```

The broken claim is *AND THE PIN IS WHAT IT SAYS IT IS*. Read out of git here:
**8** commits have touched `face_complex.py`; **2** have a two-clause `shape`
guard — `b6bc2ef` and **`bfd7948`, the repair itself** — and the newest is not
the pin. The guard is located by the gate label it **returns**, not by an anchor
of source text, so the respelling does not hide a commit from the count.

The commit discloses a **smaller** consequence: that the line *"of the 7 commits
that ever touched `face_complex.py`"* will not regenerate once it lands. What
actually happens is that the claim's **truth condition** fails, the claim reads
`[BROKEN]`, and `d2_deletion.py` exits 1 instead of 0 — and the claim's own
`WOULD DIFFER UNDER` names the event exactly: *"a later commit reintroducing a
two-clause condition"*. `d1`, `d3` and `d4` regenerate byte-identically at
exit 0; `run_all.sh` fails on `d2`.

**FINDING E9 — the remedy is one line, it works, and nothing runs it.** The
subject names the covering pair at `UNREACHED_GATE_PAIRS` and asserts that
adding it *"makes clause 1 go CHANGES, its registered prediction MISS, and the
coverage claim go red saying so"*. Spliced in and run here:

| tree | new pair | ORDER clause deleted alone | exit |
|---|---|---|---|
| HEAD | without | BYTE-IDENTICAL | 0 |
| HEAD | **with** | **CHANGES** | 1 |
| `b6bc2ef` — the defect still present | without | BYTE-IDENTICAL | 0 |
| `b6bc2ef` — **the defect still present** | **with** | **CHANGES** | 1 |

The last row is the point: the control is demonstrated **against a commit where
the defect is still present**, not only against a tree that has been repaired
around it. Declining to add it is defensible — the uncovered row is the
subject's whole argument — but the assertion about what would happen was
unmeasured, in a commit whose case is that unmeasured assertions are how this
lineage keeps going wrong. Unrun, `NOT COVERED` cannot be told apart from *not
coverable*.

## 7. This audit's own misses, kept

Two, both defects in this instrument and both caught by a `[BROKEN]` claim
rather than by inspection:

* `e2`'s "the sweep does not visit `posets.py`" claim was first written as a
  count of a name over the **whole transcript** when it was about the sweep's
  **rows** — the same substitution of a convenient population for the intended
  one that this audit is looking for, committed by this audit. Restated over the
  enumeration line it is about; the original is kept in a comment at the site.
* `e5`'s spliced control row was first written as an unterminated string
  literal, so both patched trees produced a **0-byte artifact** and both
  comparisons read `IDENTICAL` — which is exactly the "the run failed the same
  way" reading a deletion test must never make. Both claims went BROKEN,
  correctly. A guard now raises rather than comparing when a baseline is empty.

Registered predictions, hits and misses: `code/face_geometry_audit_eaef/PREDICTIONS.md`.

## 8. Disclosures

* **The rung-6 and rung-7 patches are demonstrations, not proposals.** Nothing
  in `code/face_geometry/` is changed by this audit. Making the sweep reach
  nested operands is a change to the subject's enumerator and is out of scope
  here; the finding is that the bound as written does not describe the sweep as
  built.
* **E8 is about the tree as committed at HEAD.** It reproduces from `bfd7948`
  onwards, because `bfd7948` is itself the commit that makes the pin claim
  false; no later commit is required.
* **`gate_violations` and `diagonal_moves` are untouched here**, as in the
  subject. Their returns are inert whole (mg-c4c8 F3), and both of their guards
  appear in this audit's tables only as members of the enumerated populations.
* **mg-0b07's B2, B4, A1 and A2 are not re-opened.** A1's drift is the *smaller*
  half of E8 and is named as such rather than re-filed.
* **No `| tee`** (mg-f922): `run_all.sh` captures each status and re-raises it.
