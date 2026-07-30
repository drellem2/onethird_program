# Landing mg-e7bc: a deletion at the level of the gate, read at the level of the return

**Item:** mg-9220. **Closes:** mg-e7bc's OUTSTANDING (both parts).
**Code:** `code/face_geometry/face_complex.py`, `code/face_geometry/controls.py`,
instrument in `code/face_geometry_instr_5f9a/` (`run_all.sh`, 112 s, 72 claims, 0 BROKEN).

mg-e7bc booked the mg-04a8 repair as real and did not re-open it: the repaired check
exits 1 on the broken artifact, and the deletion test bites 9 of 9 on that audit's own
mutations. What it left open is one thing, stated twice.

**The `shape` gate had two `return` statements. The deletion test deleted them together.
The artifact changed, and the result was read as a statement about each of them. Deleting
the first alone left the artifact byte-identical.**

---

## 1. The finding, reproduced rather than quoted

`d2_deletion.py`, section **PER RETURN**, against `c7f9673` — the last commit at which the
gate had two returns, pinned for the reason `PRE_REPAIR_REF` already gives:

| tag | deletion | artifact | exit | returns removed |
|---|---|---|---|---|
| R1 | **only** `if m != len(B)` | **23,680 — BYTE-IDENTICAL** | 0 | 1 |
| R2 | **only** `if len(A[i]) != len(B[i])` | 23,680 → 24,879 CHANGED | 1 | 1 |
| R3 | both, as `AFTER-5` used to | 23,680 → 24,879 CHANGED | 1 | **2** |

R3 is the line the repair published. **R1 and R2 are the two claims it was read as
making, and only one of them is true.** The cause is measured, not guessed: the pair built
for the gate is 2×2 against 3×3, and with the first return gone `len(A[0]) = 2 ≠ 3 =
len(B[0])` fires the *second*, returning `False` at gate `shape` identically.

R3 is **kept** — `SPECIMEN_TAGS` — for the reason `vacuous_check_as_shipped` keeps the
shipped label check: a bundled deletion is easier to recognise beside the un-bundled pair
than in a paragraph about it.

## 2. The inert return is deleted, and it is a merge rather than a cut

The ticket says *remove it, or show what it does*, and closes the second door: **removal,
not detection.** No pair was added to `controls.py`; no row was added anywhere; nothing
was written to notice the first return being reached.

It is **merged into the second's condition**, not cut, and the difference is measured in
the section `AND THE MERGE DID NOT QUIETLY NARROW THE GATE` — three implementations loaded
side by side (the pinned two-return one, this tree's merged one, and the pinned one with
its first return cut):

| pair | two returns | merged | first return **cut** |
|---|---|---|---|
| `A = []`, `B = [[1]]` | `(False, shape)` | `(False, shape)` | **`(True, parity)`** |
| `A = [[1]]`, `B = []` | `(False, shape)` | `(False, shape)` | **`IndexError`** |
| 2×2 vs a 3-row `B` whose first two rows are 2 wide | `(False, shape)` | `(False, shape)` | **`(True, parity)`** |

and over a population: **7,921 constructed pairs** — every matrix over {0, 1, −1} of order
≤ 2 plus four ragged and rectangular ones, crossed with itself, built in the instrument and
not taken from the battery, which has no ragged pair at all. The merged gate gives the
**same decision on 7,921 of 7,921**; the cut moves the decision on **199**. That is the
answer to "show what it does": nothing the battery can see, and *those* everywhere else.

**One label moves and it is disclosed.** 126 of the 7,921 differ in the *gate* — all
ragged pairs, all relabelled `diagonal`/`magnitude` → `shape`, because hoisting the width
test out of the loop tests row 1's width before row 0's diagonal. `gate_violations` and
`priority_gate` always called those pairs `shape`, so the merge **removes** a disagreement.
The merged form is the one four other shape guards in this repository already use.

**The artifact does not move for this.** `controls_output.txt` goes 23,680 → 23,684 bytes
on **one line**, and that line is the row's own prose: "which is the second `shape` return"
is no longer true, and now reads "which `m != len(B)` alone does not see".
`probe_output_n6.txt` is byte-identical. No mathematics moved, no row was added or removed,
no label changed.

## 3. The granularity is stated beside the test

Every mutation declares **the unit it removes**, and the number of `return` statements is
**counted from its own patch text** rather than asserted (`returns_removed`). It is printed
in the claim line — `[UNIT REMOVED: …]` — and in the `WOULD DIFFER UNDER`, which now names
the count explicitly: *"…and under this line being read at a granularity finer than the N
`return` statement(s) the patch takes out."*

| tag | ret | unit removed |
|---|---|---|
| BEFORE-1 | 0 | one **clause** of a compound condition; the `return` it guards stays |
| BEFORE-2 | 1 | one `return` — the magnitude gate |
| AFTER-1 | 1 | one `return` — gate `diagonal` |
| AFTER-2 | 1 | one `return` — gate `magnitude` |
| AFTER-3 | 0 | **no statement**: the *order* of two gates, both returns kept |
| AFTER-4 | 0 | one statement, and not a `return`: the `signs_read` counter |
| AFTER-5 | 1 | one `return` — gate `shape`, which is one return since this commit |
| AFTER-6 | 1 | one `return` — the `parity` contradiction branch |
| R1, R2 | 1, 1 | each of the pinned tree's two `shape` returns, alone |
| R3 | **2** | the pair — **specimen**, excluded from the claim *by name* |

A claim requires that **no mutation removes more than one `return`**, the specimen aside.
Before this commit `AFTER-5` removed two and that claim would have been BROKEN — which is
the point: the bundling was invisible because nothing counted it.

**And the table is checked against the source it deletes from** (`d1_trace.py`, AST): the
4 rejecting returns of `absorb_trace` are each deleted by **exactly one** mutation of the
AFTER table, and the remaining return accepts. A return added without a mutation of its
own, or two bundled again, is BROKEN there — the one place the bundling could have been
caught without running anything. `d1`'s frozen "6 returns" literal is gone with it: what is
required now is the property the sentence claims (every label a literal at the return
site), not a number that only had to be edited to 5.

## 4. What this cost, stated plainly

**Two independently written deletion instruments were anchored to the text this commit
removed**, and both now stop at their first mutation with `anchor occurs 0 times`:
mg-d0e2's `e1_deletion.py` and mg-e7bc's `g2_deletion.py` (and `g3_differs_under.py`, whose
`s1` mutation *is* the experiment that produced the finding). Neither audit was edited —
their transcripts are their record of their own runs, the treatment mg-5f9a gave mg-1c80's
`a6_mutations.py` and mg-04a8 gave mg-d0e2's.

`d4_auditor_rerun.py` therefore runs each **twice**, and scores both:

- **against this tree** — each stops at its first mutation, and the anchor it names is
  quoted in the claim, so the abort is attributed to this commit rather than found later;
- **against the pinned commit it was written for**, materialised whole with `git archive`
  — `e1_deletion.py` at `c7f9673` still says **9 of 9 CHANGED**, and `g2_deletion.py` at
  `9d712be` still reproduces **E1 byte-identical / E2 CHANGED**, which is the finding this
  commit acts on, measured on the tree it is about.

Nothing either audit measured is withdrawn. But after this commit **no independently
written deletion instrument applies to the live tree**; the per-return table in `d2` is
this lineage's own. That is the price of removing the text they were anchored to, it is
the price the ticket asked for, and re-anchoring either audit would buy the independence
back.

## Numbers, re-measured here rather than carried

- Battery: **43 scored rows**, 2 [CANNOT FAIL], 0 failures, exit 0, **23,684 bytes**
  (23,680 before; one line, four characters). `probe_output_n6.txt` **byte-identical**.
- Instrument: `run_all.sh`, **112 s, 72 claims, 0 BROKEN**, exit 0 (d1 17, d2 33, d3 6,
  d4 16). No `| tee` (mg-f922).
- `absorb_trace`: **5 returns** — `shape` 1, `diagonal` 1, `magnitude` 1, `parity` 2 (a
  rejecting contradiction branch and the accepting one). **4 rejecting, 4 mutations.**
- Equivalence: **7,921 pairs, 7,921 same decision, 126 gate relabellings, all ragged**;
  the cut moves **199** decisions.

## Disclosures

1. **The merge changes the trace label on ragged pairs** — `diagonal`/`magnitude` →
   `shape`, 126 of 7,921. It is a real behaviour change, it is in the direction of the two
   procedures that always disagreed with the old order, and no population in the battery
   contains such a pair. Stated in `absorb_trace`'s docstring, not only here.
2. **`d1_trace.py` still carries no `WOULD DIFFER UNDER` on 15 of its 17 claims**
   (mg-e7bc's F3). The two added here carry one; that is two statements written to the
   standard, not the standard applied to the file, and F3 stays open.
3. **Three derived artifacts were regenerated** because the artifact moved:
   `positive_control_all_fail.txt`, `code/face_geometry_audit_e7bc/pc_all_pass.txt` and
   `code/face_geometry_landing_da45/out_verify.txt` (one line, the byte count). The second
   is inside an audit directory — it is a *generated control* whose own claim says a
   control describing a previous artifact tests nothing about this one, and no transcript
   or finding of that audit was touched.
4. **mg-e7bc's `g4_seams.py` is not run by `d4`**: `g4` re-runs `d4`, and `d4` running
   `g4` would not terminate. Its own `run_all.sh` runs it. The two figure-sites it anchors
   in `docs/landing-mg-d0e2-vacuous-check.md` are updated by this commit, with the
   mg-04a8-era values kept beside them.
5. **mg-e7bc's other findings stand open**: the scope-of-guard finding on a deleted row
   line, the 29 untested `WOULD DIFFER UNDER` statements, and its F3–F8. This item was the
   OUTSTANDING granularity pair and nothing else.
6. **No mathematics was touched**, no row was added, and no existing row changed its label
   or its condition.
