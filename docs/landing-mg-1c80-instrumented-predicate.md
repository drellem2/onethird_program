# Landing mg-1c80's F1: the predicate reports its own reason

**Item:** mg-5f9a. **Closes:** mg-1c80's F1 (the OUTSTANDING half of that audit).
**Code:** `code/face_geometry/face_complex.py`, `code/face_geometry/controls.py`,
instrument in `code/face_geometry_instr_5f9a/` (`run_all.sh`, 38 s, 34 claims, 0 BROKEN).

## The defect, and why this is the third attempt at it

NEGATIVE CONTROL 4 keeps one row (I4) scoring `absorb == 0`, and it prints a sentence
saying why the absorbability predicate answered as it did. Three generations:

| | what it printed | how it failed |
|---|---|---|
| mg-8a12 | "the predicate had to decide on the off-diagonal signs and could have returned absorbable" | false; mg-f1b2 refuted it |
| mg-da45 | a per-row gate split from `deciding_gate` | **a priority relabelling.** `deciding_gate` tested all diagonals then all magnitudes; the predicate interleaves the two **by row**. The two orders named different gates on **57 of the 297** biting pairs, and mg-1c80's M2 — delete the gate the artifact called decisive — regenerated the artifact **byte-identically** |
| mg-5f9a (here) | nothing asserted alongside the predicate | — |

The common shape: **a reason produced beside the procedure it is about.** A reason that
survives deleting the thing it names is not the code's reason.

## What was done — not a third reason

mg-1c80's instruction was explicit: instrument the predicate, or print nothing. The
predicate is instrumented.

`face_complex.absorb_trace(A, B)` **is** the predicate now. It returns
`Trace(absorbable, gate, signs_read)`, where `gate` is a literal written **at the
`return` statement that fired** and `signs_read` is how many off-diagonal constraints the
union-find loop actually consumed. `absorbable_by_diagonal_twist` is a one-line wrapper
over it, so there is one implementation and one execution order. **`controls.py` now
defines no gate procedure at all** — `deciding_gate` is deleted and nothing replaced it,
not even a local alias, since an alias is one more place for the two to drift apart. The
rows call `absorb_trace` directly, and `d1` checks the absence in the AST rather than
trusting it.

**Three questions mg-da45 answered with one function are now three functions**, and
keeping them apart is most of the repair:

- `diagonal_moves(A, B)` — did the diagonal move? A property of the two matrices. It is
  the hypothesis of the [CANNOT FAIL] theorem and it holds at every *n*. **It drives the
  routing**, and it says nothing about what the code tested first. (`deciding_gate`
  served as both, which is how a routing quantity came to be printed as a trace.)
- `absorb_trace(...).gate` — a fact about **one execution**. Order-dependent, and every
  row that quotes it says so.
- `gate_violations(A, B)` — the set of gates violated, computed **exhaustively**, so it
  is order-free. This is what measures whether the gate a trace names was load-bearing.

**What the rows now rest on is `signs_read`**, which no ordering can move. "No sign was
consulted" was previously inferred from a sign-mismatch count computed outside the
predicate; it is now the predicate's own counter, and it reads **0 over all 297 pairs**.

## The verification mg-1c80 asked for, run on both sides

`d2_deletion.py`, six predictions registered before the runs, 6 of 6 correct
(12 claims scored, 0 BROKEN):

| | mutation | artifact | exit |
|---|---|---|---|
| BEFORE-1 | **`main`'s tree**: delete the `s_i^2 = 1` gate (mg-1c80's M2, verbatim) | **BYTE-IDENTICAL** | 0 |
| BEFORE-2 | `main`'s tree: delete the `\|s_i s_j\| = 1` gate | CHANGES | 1 |
| AFTER-1 | **this tree**: delete the `s_i^2 = 1` gate from `absorb_trace` | **CHANGES** | 0 |
| AFTER-2 | this tree: delete the `\|s_i s_j\| = 1` gate | CHANGES | 1 |
| AFTER-3 | this tree: test row *i*'s magnitudes **before** row *i*'s diagonal | CHANGES | 0 |
| AFTER-4 | this tree: stop counting the signs the union-find reads | CHANGES | 0 |

The BEFORE half is mg-1c80's finding re-run rather than quoted — `main`'s committed
`controls_output.txt` regenerates from `main`'s sources first (17,964 bytes), then the
deletion leaves it at 17,964 identical bytes.

AFTER-1 and AFTER-3 are the ones that matter: they change **no decision** — all 43 scored
rows keep their labels and conditions, exit stays 0 — and they still move the artifact, on
exactly the two lines that report where the predicate went (row I4 and the gate table).
That is what "the reason is produced by the code path" means operationally.

## Numbers, re-measured here rather than carried

`d1_trace.py` (16 claims, 0 BROKEN), on NEGATIVE CONTROL 4's own population, 86 posets
*n* ≤ 5, with the pair (E·L^rel·E, D−A) rebuilt from `face_complex` and `controls.py`
never imported:

```
row  corruption               bites | trace: diag mag par | mg-da45 priority | differ | both | signs
I1   ridge_facets                72 |         15   57   0 |     72    0    0 |     57 |   72 |     0
I2   split_free_as_interior      82 |         82    0   0 |     82    0    0 |      0 |   82 |     0
I3   ridge_drop                  82 |         82    0   0 |     82    0    0 |      0 |   82 |     0
I4   facet_offbyone              61 |         58    3   0 |     58    3    0 |      0 |   58 |     0
ALL                             297 |        237   60   0 |    294    3    0 |     57 |  294 |     0
```

mg-1c80's 57 of 297 reproduces exactly. So does the reason it does not matter to any
conclusion: **294 of the 297 pairs violate both forced gates**, so on those the gate a
trace names is a fact about the order and nothing else — which the artifact now says in
the same sentence that prints the split. The decision is also re-decided without the
union-find (378/378 by BFS 2-colouring, 180/180 by brute force over all 2^m sign vectors)
and against `main`'s own predicate (378/378 identical): **the refactor decided nothing
differently.**

## What did NOT change

- **No mathematics.** The predicate's decision is identical on every pair tested.
- **No scoring.** 43 rows, same labels, 2 [CANNOT FAIL], 0 failures, exit 0; row I4 keeps
  `absorb == 0` in its condition (removing it is a scoring change and still belongs to its
  own item); `forced = (diag_preserved == 0)` and the routing row's condition are
  untouched. The routing *values* are unchanged too (I1/I2/I3 forced, I4 scored) — only
  their source moved from `deciding_gate` to `diagonal_moves`, which is the point.
- **No other item's artifact was edited.** mg-1c80's audit doc and instrument, and
  mg-fcf1's, are left as the records they are.

The [CANNOT FAIL] theorem row keeps its argument — `s_i^2 = 1` pins the diagonal, so a
moved diagonal is never absorbable, at every *n* — and now adds what that argument is
**not**: a claim about which test fires. It states, measured, that the implementation
realises the implication redundantly (236 of 236 of those pairs violate the magnitude gate
too), so deleting the `s_i^2 = 1` gate changes no answer on any of them. The mathematics
stands; the gate name was never evidence for it.

## Disclosures

1. **mg-1c80's `a6_mutations.py` no longer applies to five of its eight patches.** Its
   anchors are the source lines this landing rewrote, and it reports
   `PATCH DID NOT APPLY (0 occurrences)` for M1, M2, M3, M5 and M7 (it degrades to
   `<-- MISSED` and exits 0; its committed `out_mutations.txt` is the record of its own
   run at 1d922a1 and is not touched). The successors are here: **M1 → AFTER-2, M2 →
   AFTER-1, M3 → AFTER-3/AFTER-4, M5 → R1, M7/M8 → R2.**
2. **mg-da45's `verify_landing.py` still passes: 25 claims, 0 BROKEN, exit 0**, without
   being edited — every number it re-measures independently is still printed, and every
   dead-premise occurrence still sits inside a denial. Its committed `out_verify.txt` is
   regenerated (its own `run_all.sh` says it reads the live tree and will drift). Two
   caveats a reader should have: its closing prose ("the file now MEASURES which gate
   settled it") is *mg-da45's* sentence and is the one this ticket corrects — it is that
   landing's artifact and was left alone; and its check "the routing still routes on the
   diagonal gate (`forced = (diag_preserved == 0)`)" is a text anchor that passes while
   `diag_preserved`'s *source* changed. The values are identical, verified in `d1` part D.
3. **mg-1c80's F2 was fixed as a side effect and is disclosed as one.** Instrumenting the
   sign count meant widening the sign census from the diagonal-preserved branch (3 pairs)
   to all 297, since the routing row prints it as "anywhere". `R2` verifies the widening
   does something: with mg-1c80's M8 sign-only mismatch injected on the diagonal-**moved**
   pairs, the printed total moves **0 → 110**, where under mg-da45's scope it stayed 0.
   F2 was not this ticket's item; it is closed and named rather than left implied.
4. **mg-1c80's F3, F4 and F5 are NOT addressed here.** F4's "off-diagonal" wording
   survives at the one site that still prints it, where it is provably exact (the branch
   is the diagonal-preserved one, so every magnitude mismatch is off-diagonal);
   `entry_mismatches`'s docstring now says the function counts the whole matrix. F3 (the
   "forced at every n" half that is argued only for antichains) and F5 stand open.
5. **`run_all.sh` here does not use `| tee`.** A pipeline's status is the last command's,
   so `tee` would mask a verifier exiting 1 — a committed transcript reading BROKEN under
   a script that exited 0. mg-f922 found that shape in this repository; the status is
   captured and re-raised instead.
