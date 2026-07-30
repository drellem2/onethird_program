# Independent audit mg-c4c8: the deletion test, per return and one level below it

**Item:** mg-c4c8, pre-filed in the same action as its parent mg-e7bc.
**Subject:** `b6bc2ef` — mg-9220's repair of mg-e7bc's OUTSTANDING, both parts.
**Instrument:** `code/face_geometry_audit_c4c8/` (`run_all.sh`, ~230 s, **23 claims, 0
BROKEN, exit 0**; h1 4, h2 5, h3 8, h4 6). **Six findings.** The mutation enumeration is
read out of `ast` rather than taken from anyone's list — the subject and both prior audits
patch by `text.replace(old, new)` with `old` a literal copied out of the source, which runs
the mutations its author chose and cannot enumerate the ones that exist. Nothing under
`code/face_geometry/` is written; every battery run goes to a copy in a temporary
directory.

> **Verdict: the repair is real at the unit it claims. `absorb_trace`'s six `return`
> statements, each deleted ALONE by this audit's own harness, all move the artifact; the
> inert return is REMOVED from the source rather than annotated; the negative control
> re-run as a process still exits 1; and both pinned commits are what their docstrings say.
> But the granularity error recurs at the third level in the statement the repair wrote —
> the two returns became two CLAUSES of one condition, and deleting the first clause alone
> leaves the artifact byte-identical, exit 0, every row green — and the DECLARED UNIT, which
> is now what the evidence rests on, understates its own patch on 8 of the 11 mutations.**

---

## 1. The primary target — per return, and what "all nine" turns out to mean

### 1a. Every `return` in the file, deleted alone

`h1_per_return.py`. Population enumerated from the syntax tree, not from a list: **56
`return` statements in `code/face_geometry/face_complex.py`**, of which **11 are in the
four functions mg-d0e2's nine mutations touch**. Each is replaced — alone — by `pass` at
its own indentation (not deleted as lines: many are the only statement of their block, and
removing the lines would remove the enclosing `if`, which is a *larger* unit and would put
this instrument in the error it was written to look for). The whole battery is then run and
the artifact compared byte for byte.

| # | return | artifact | exit | bytes |
|---|---|---|---|---|
| 46 | `absorb_trace` gate `shape` | CHANGES | 1 | 24,887 |
| 47 | `absorb_trace` gate `diagonal` | CHANGES | 0 | 23,684 |
| 48 | `absorb_trace` gate `magnitude` | CHANGES | 1 | 23,534 |
| 49 | `absorb_trace.find` — the union-find root | CHANGES | 1 | 4,030 |
| 50 | `absorb_trace` `parity` contradiction | CHANGES | 1 | 24,771 |
| 51 | `absorb_trace` the accepting return | CHANGES | 1 | 4,030 |
| 52 | `gate_violations` shape guard | **BYTE-IDENTICAL** | 0 | 23,684 |
| 53 | `gate_violations` the violation set | CHANGES | 1 | 7,681 |
| 54 | `diagonal_moves` shape guard | **BYTE-IDENTICAL** | 0 | 23,684 |
| 55 | `diagonal_moves` the routing quantity | CHANGES | 1 | 26,468 |
| 56 | `absorbable_by_diagonal_twist` | CHANGES | 1 | 4,030 |

Baseline 23,684 bytes, exit 0, regenerating the committed artifact byte-identically. Row 47
is worth a second look: the artifact *changes* at the *same length* — the trace labels move
and nothing else does, which is what `AFTER-1` says and what a length comparison would have
missed.

**`absorb_trace` is covered at the granularity of a return: 6 of 6.** mg-e7bc's finding does
not survive on that function. Across the whole file 18 of the 56 are byte-identical under
individual deletion; the other 16 are outside the four functions and are printed in the
transcript as context, not as a finding — no claim of mg-9220's says the file is
deletion-covered.

### 1b. "All nine" is not nine returns

`h2`, section 1. The nine are mg-d0e2's `e1_deletion.py`, and that file **cannot run on this
tree** — mg-9220 deleted the text its first mutation anchors on, so it aborts before running
any of them. They are re-derived here from the live source through the syntax tree and run
on the live tree, each reported with **the unit it actually removes**, measured by parsing
both trees:

| tag | mutation | artifact | exit | unit actually removed |
|---|---|---|---|---|
| N1 | delete gate `shape` | CHANGES | 1 | 1 return, 1 stmt |
| N2 | delete gate `diagonal` | CHANGES | 0 | 1 return, 1 stmt |
| N3 | delete gate `magnitude` | CHANGES | 1 | 1 return, 1 stmt |
| N4 | delete gate `parity` | CHANGES | 1 | 1 return, 1 stmt |
| N5 | stop counting `signs_read` | CHANGES | 0 | 0 return, 1 stmt |
| N6 | swap the two forced gates' order | CHANGES | 0 | nothing |
| N7 | delete `diagonal` from `gate_violations` | CHANGES | 0 | nothing |
| N8 | delete `magnitude` from `gate_violations` | CHANGES | 0 | nothing |
| N9 | invert `diagonal_moves` (the routing) | CHANGES | 1 | nothing |

**All nine still bite on the live tree — 9 of 9 move the artifact.** But *per return on all
nine* is not a property nine mutations can have: **four remove exactly one `return`, one
removes a statement that is not a return, two replace a CONDITION with a constant and remove
nothing, and two are a reordering and an inversion.** The question has an answer of five
parts and the transcript prints five parts.

---

## 2. The negative control — re-run, not assumed

`h3`, section 1. `checkrun.py` as a **process**, exit status reported. mg-9220 both
restructured a gate and regenerated the broken artifact, which is exactly the pair of edits
that could stop a control firing while leaving it in the tree.

| artifact | exit |
|---|---|
| the committed artifact, untouched | **0** |
| `positive_control_all_fail.txt` — the committed broken one | **1 — THE CONTROL STILL FIRES** |
| MINE: one `[PASS]` row LINE duplicated | 0 |
| MINE: one `[PASS]` row RENAMED, marker untouched | 0 |
| MINE: two scored rows EXCHANGED in position | 0 |
| MINE: one `[CANNOT FAIL]` row promoted to `[FAIL]` | **1** |

6 of 6 predictions matched. The committed control is still byte-equal to this audit's own
all-`[FAIL]` retagging of the current 23,684-byte artifact, and mg-e7bc's `pc_all_pass.txt`
— regenerated by mg-9220 inside another audit's directory — is still the all-`[PASS]` one.
**And the landing's summary agrees with the rows that produce it.** mg-9220 reports "72
claims, 0 BROKEN, exit 0 (d1 17, d2 33, d3 6, d4 16)". All four scripts were re-run as
processes here: d1 **17**, d2 **33**, d3 **6**, d4 **16**, total **72**, every one exiting 0
with 0 BROKEN. mg-e7bc's `g1_positive_control.py` also exits 0 (8 claims, 1 finding — its
own, unchanged).

---

## 3. The state-of-granularity claims — the declaration checked against the patch

`h4`, section 1, and this is the item pm-onethird added mid-audit: a declared unit is a
claim, and it is the claim the deletion evidence rests on. Each of the eleven patches is
applied to the tree its own `run_case` uses, **both trees are parsed**, and the units
removed are counted from the syntax — returns, other statements, boolean clauses — then
compared with a reading of the declaration written out beside it.

| tag | declared (r/s/c) | measured (r/s/c) | verdict |
|---|---|---|---|
| BEFORE-1 | 0/0/1 | 0/0/1 | EXACT |
| BEFORE-2 | 1/0/0 | 1/1/0 | understates |
| AFTER-1 | 1/0/0 | 1/1/0 | understates |
| AFTER-2 | 1/0/0 | 1/1/0 | understates |
| AFTER-3 | 0/0/0 | 0/0/0 | EXACT |
| AFTER-4 | 0/1/0 | 0/1/0 | EXACT |
| **AFTER-5** | **1/0/0** | **1/1/1** | **understates** |
| AFTER-6 | 1/0/0 | 1/1/0 | understates |
| R1 | 1/0/0 | 1/1/0 | understates |
| R2 | 1/0/0 | 1/1/0 | understates |
| R3 | 2/0/0 | 2/2/0 | understates |

11 of 11 predictions matched. `returns_removed` — the subject's line heuristic — agrees with
the AST count on 11 of 11, so the *number* it prints is right. The landing document's `ret`
column names all eleven mutations and every figure in it equals the returns its patch
removes.

---

## Findings

### F1 — THE GRANULARITY ERROR RECURS AT THE THIRD LEVEL, in the statement the repair wrote

mg-9220 did not cut the inert return; it **merged** it, into

```python
if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
    return Trace(False, "shape", 0)
```

Deleting the **return** moves the artifact (h1 #46; `AFTER-5`). **Deleting the first CLAUSE
of its condition alone leaves the artifact BYTE-IDENTICAL at 23,684 bytes, exit 0, every row
green.** That is mg-e7bc's own sentence with `return` replaced by `clause`: the deletion
proves the *condition* is load-bearing and proves nothing about either clause. The unit moved
from a pair of returns to a pair of clauses; the pair is still what the test bites on.

Population, read from the tree rather than chosen: **11 clauses in 5 deciding conditions**;
all 11 deleted alone, 11 of 11 predictions matched. Only `absorb_trace`'s second clause moves
the artifact.

**The repair's own text predicts this and does not measure it.** `AFTER-5`'s WOULD DIFFER
UNDER already says "…and under this line being read at a granularity finer than the 1
`return` statement the patch takes out". The exposure is named; the measurement is not made.

**What the clause does, measured on the LIVE tree.** The subject answers *remove it or show
what it does* by loading the **pinned** two-return implementation with its first **return**
cut — a measurement about `c7f9673`. The live clause is cut nowhere in the repository. Cut
here, on the live merged condition, over **28,900 pairs across 85 shape profiles** built in
this instrument: the clause moves the **decision on 1,608** pairs and the (decision, gate) on
1,824. So it is inert as a *battery input* and not inert as a *predicate* — which is what
makes F1 a granularity finding and not a demand to delete the clause.

**To close it:** run the deletion test at clause granularity for the conditions that decide a
return, and declare the clause count the way `returns_removed` declares the return count. A
`UNITS` entry that says "one `return` statement" for a patch that removes a two-clause
condition is the same reading one level down (see F2).

### F2 — The DECLARED UNIT is finer than the patch on 8 of 11, and on `AFTER-5` the difference *is* the third-level unit

Each of `BEFORE-2`, `AFTER-1`, `AFTER-2`, `AFTER-5`, `AFTER-6`, `R1`, `R2`, `R3` declares
"one `return` statement" (`R3`: two) and its patch removes the `return` **together with the
`if` that guards it**. `AFTER-5` removes, in addition, **a boolean condition with two
clauses**. So the line a reader consults says the unit is one return, and the unit is a
return plus a two-clause condition.

This is not unavoidable: h1 ran the strictly-return-only version of `AFTER-1`, `-2`, `-5`
and `-6` — returns #47, #48, #46, #50, each replaced by `pass` with its `if` left standing —
and **every artifact verdict and exit code agreed**. So the *results* are unaffected and this
is a defect of the **declaration**, which is now the thing the evidence rests on.

**To close it:** either declare what the patch removes ("one `return` and the `if` that
guards it, whose condition has N clauses"), or make the patch remove only the return, by
substituting `pass` for it. The second is preferable, because it makes the mutation and the
declaration the same size by construction rather than by proofreading.

### F3 — Two more inert returns at the same granularity, in the same repair's blast radius

`gate_violations`'s shape guard (line 889) and `diagonal_moves`'s shape guard (line 912) are
each a `return` whose **individual deletion moves not one byte** of the artifact — the exact
condition mg-e7bc named for `absorb_trace`'s first `shape` return. Both functions are the
companions `absorb_trace`'s own docstring cites, and both were named in the merge's
justification as already using the merged form. **No mutation in `d2_deletion.py` deletes
either of them.**

They are unreachable for the same reason the `shape` gate was: `controls.py` calls both only
after its own shape guard has `continue`d, so no pair with a shape mismatch reaches either.
mg-9220 fixed the one return its ticket named and did not sweep the two next to it.

**To close it:** run the deletion test over the enumerated returns of the predicate layer
rather than over a hand-written table, and dispose of what it finds — removal, or a
measurement of what the statement does.

### F4 — Three of the nine are run by nothing in the tree

`N7`, `N8` and `N9` target `gate_violations` and `diagonal_moves`. `d2_deletion.py`'s eleven
mutations touch neither function; mg-d0e2's `e1_deletion.py` — the only instrument that ever
ran them — aborts on this tree at its first mutation because mg-9220 deleted the text it
anchors on. `d4_auditor_rerun.py` preserves them by re-running `e1` **against the pinned
commit**, which is a measurement about `c7f9673`. On the live tree the standing evidence for
those three is this audit's `h2`.

mg-9220 discloses the general shape of this ("after this commit no independently written
deletion instrument applies to the live tree") and it is stated in the landing. What is not
stated is that three of the nine mutations the "9 of 9" sentence is about now have no live
instrument at all.

**To close it:** re-anchor three mutations into `d2_deletion.py`'s AFTER table, or say in the
landing which of the nine survive on the live tree and which are preserved only at the pin.

### F5 — The merge is not outcome-preserving, and the population that shows it is one the subject's cannot reach

On **2,064 of 28,900** pairs the pinned two-return `absorb_trace` **raises `IndexError`** and
the merged one returns `(False, "shape")` — every one of them a matrix with a **row shorter
than the matrix's own order**, where the old form indexed `A[i][i]` before it had checked row
`i`'s width. (194 pairs raise in both; none raise only in the merged form.) Where both forms
terminate the merge is decision-preserving on **26,642 of 26,642**, with 1,512 gate
relabellings — the behaviour change mg-9220 does disclose.

mg-9220's docstring and landing say the merged gate gives "the SAME DECISION on 7,921 of
7,921". That is true of *its* population — every ragged member of which has rows at least as
long as its order — and it is read as a statement about the merge. The change is an
**improvement**: a total function replacing a partial one. It is undisclosed.

**To close it:** state it. One sentence in `absorb_trace`'s docstring beside the 126
relabellings, and a population in the instrument that contains a row shorter than the order.

### F6 — The guard is over labels and not over the row set, in three more directions

mg-e7bc found that **deleting** a scored row line leaves the repaired check green. Its dual
and its two neighbours do the same: **duplicating** a row, **renaming** one while keeping its
marker, and **exchanging** two rows' positions all exit 0. The check derives an expectation
for each row *present* from that row's own name, so a row that is duplicated, renamed or
moved carries its expectation with it. A `[CANNOT FAIL]` row promoted to `[FAIL]` exits 1, so
this is the extent of the guard and not a failure of these corruptions to be corruptions.

mg-04a8's sentence — "an artifact whose rows have been edited — by a corruption, a bad merge,
or a hand — disagrees with its own summary, and the check below is what notices" — remains
wider than what the code does, one audit later and now in four measured ways.

**To close it:** compare the row *multiset* against a set derived from `controls.py`'s own
row registrations, or narrow the sentence to labels.

---

## What was checked and held

- **The inert return is GONE rather than annotated.** One `shape` return at HEAD (line 837),
  two at `c7f9673` (lines 808, 811), counted from the tree — so a return re-added inside an
  `if False:` or behind a flag would still be counted. And **nothing was added to
  `controls.py` to watch it instead**: 18 constructed-pair entries at HEAD and 18 at the pin.
  The "removal, not detection" half of the ticket is done as stated.
- **The floor item, chosen by this audit because no list in the brief names it: the
  provenance of the two pinned commits.** `R1`, `R2` and `R3` are the whole reproduction of
  mg-e7bc's finding and they are measurements about whatever tree `TWO_RETURN_REF` names.
  Six commits have touched `face_complex.py`; **two** of them have two `shape` returns in
  `absorb_trace`; the **newest** of those is `c7f967394cf7`, which is what `c7f9673`
  resolves to. The docstring's "the last commit in which the `shape` gate had TWO `return`
  statements" is true. `PRE_REPAIR_REF` (`5cae82c^` → `61de12133f74`) contains no
  `absorb_trace` and no `Trace` at all, so the BEFORE half really is contrasting with a
  pre-instrumentation tree.
- **The landing table against the code it describes** — all eleven `ret` figures equal the
  returns their patches remove, measured from the trees.
- **`returns_removed` is honest** — the line heuristic agrees with the AST count 11 of 11.

## This audit's own slip, kept as written

`h2`'s first run declared "invert `diagonal_moves`'s routing return" and inverted its **shape
guard** instead: `ast.walk` is breadth-first, so `[-1]` of the walk is not the last return in
source order. The registered prediction caught it — `N9` predicted CHANGES/1, observed
IDENTICAL/0. The selector now sorts by source position; the accidental mutation is kept as
row `N9x` with a prediction of its own (IDENTICAL/0, registered after the slip and labelled
as such), and it confirms F3 from a second direction: inverting `diagonal_moves`'s shape
return is as invisible as deleting it. **It is the same defect this audit exists to look
for — a mutation whose declaration and whose patch name different things — committed by the
auditor.**

## Prediction score

Every exit code predicted before its run; misses kept as written.

| section | matched |
|---|---|
| h1 — 56 returns | 43 of 56 |
| h2 — the nine (10 rows incl. `N9x`) | 10 of 10 |
| h2 — 11 clauses | 11 of 11 |
| h3 — 6 artifacts | 6 of 6 |
| h4 — 11 declarations | 11 of 11 |

h1's thirteen misses are all in the 45 returns outside the predicate layer, and all in the
same two directions of ignorance: **eight** functions this audit expected the battery to reach
are not reached by it (`Poset.comparable`, `Poset.automorphisms`, `Poset.is_connected`,
`Poset.is_chain`, `_ambient_coxeter_laplacian`, `twist`, `rank_mod_p`, `trace`), and the
remaining **five** are the early exits of `not_isospectral` and `det_shift_mod_p`, whose
load-bearingness the reading here got backwards in both directions. None of them bears on any claim above; they are the
price of naming a population larger than the one the subject claims.
