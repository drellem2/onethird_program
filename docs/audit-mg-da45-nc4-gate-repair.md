# INDEPENDENT AUDIT of mg-da45 (commit `f024985`) — the repair of row I4's printed reason

**Auditor:** mg-1c80 (pre-filed in the same action as its parent; no coordination with mg-da45)
**Target:** `f024985` — *"control+docs: THE CONDITION IS RIGHT AND THE PRINTED REASON WAS FALSE —
row I4's absorbability answer is FORCED at the ABSOLUTE-VALUE gate on all 61, with ZERO sign-only
mismatches, and the cited witness is absorbable 82/82 by construction (mg-da45)"*
**Files audited:** `code/face_geometry/controls.py`, `code/face_geometry/controls_output.txt`,
`code/face_geometry/face_complex.py`, `code/face_geometry_landing_da45/verify_landing.py` and its
committed output, plus the commit's own description of its method.
**Audit code:** `code/face_geometry_audit_1c80/` (`kern1c80.py`, `a1_gates.py`, `a2_antichain.py`,
`a3_n6_population.py`, `a4_witness.py`, `a5_claims.py`, `a6_mutations.py`; outputs `out_gates.txt`,
`out_antichain.txt`, `out_n6.txt`, `out_witness.txt`, `out_claims.txt`, `out_mutations.txt`;
`run_all.sh` regenerates all six, 27 s).

`kern1c80.py` is a **second implementation**. It shares `posets.all_posets` and the `Poset` type
with the object under audit and nothing else: facets, ridges, the simplicial boundary, the relative
top Laplacian, the twist, the target `D − A` and the parity gauge are all rebuilt from the
definitions, and absorbability is decided by **BFS 2-colouring** and, where `|L(P)| ≤ 8`, by
**brute force over all 2^m sign vectors** — never by `face_complex`'s union-find. No script here
imports `controls.py`, and **none re-runs mg-da45's own verifier**; its committed output is read as
text only where this document quotes it.

Part 1 first checks the rebuild against `face_complex` matrix-for-matrix — 516 twisted `L^rel`s
across six incidence modes, 86 targets, 86 parity gauges, **0 disagreements**; and the three
absorbability routes agree 516/516 and 306/306. Everything below is measured on the rebuild.

---

## VERDICT: **the substance is CONFIRMED; the mechanism is OVERSTATED**

**0 BROKEN mathematics.** mg-f1b2's F1 is right and mg-da45 lands it correctly. Every headline
number reproduces: `61` biting, `3` diagonal-preserved, `3` settled at `|s_i s_j| = 1`, `300`
off-diagonal magnitude mismatches, `0` sign-only, `0` of `297` reaching the parity system, `0`
absorbable, NC3 absorbable `82/82`. `controls_output.txt` regenerates **byte-identically** (17964
bytes, exit 0). `nmax = 2` is unchanged at HEAD and HEAD~1 (both exit 1, both `CONTROLS FAILED: 3`).
The claim was pushed **two sizes further** here — 10080 and 80640 magnitude mismatches at n = 7 and
n = 8, exactly 2 per row, 0 sign-only — and it holds.

**The condition did not move, and the witness was withdrawn rather than replaced.** Both are the
things the ticket asked to protect, and both are verified mechanically rather than read (§WHAT
STANDS). The brief's named failure mode — *a replacement witness that is also absorbable by
construction* — **was not committed**: mg-da45 removes the witness claim for row I4 and names
NC3's gauge only as a witness that the *predicate* can return `True`.

**And the new reason is, in one respect, again a reason it does not have.** `deciding_gate` is
presented as a measurement of `absorbable_by_diagonal_twist` — *"WHICH gate of
`absorbable_by_diagonal_twist` settles the pair"*, *"the gate is measured here rather than argued
for anywhere"*, *"Nothing here routes on a gate it has not measured"*. It is not a measurement of
the predicate. It is a **priority relabelling** of the predicate's tests, and on **57 of the 297**
biting pairs it names a gate the predicate never reaches. The two gates it separates rows by are
not even separable on this population: **deleting the `s_i² = 1` gate from the predicate outright
changes not one byte of the artifact and the battery still exits 0** (mutation M2).

**Sizing, immediately, because the finding must not be read as bigger than it is.** Nothing above
touches the conclusion. Both gates are forced; `0 of 297` reach the parity system under *either*
reading; row I4's own `58 / 3 / 0` split is **identical** under both. mg-f1b2's F1 stands entirely,
and so does the substance of the repair.

**LEDGER: 23 claims scored — 17 HOLDS, 4 SCOPE, 2 BROKEN** (`out_claims.txt`). A `SCOPE` is a claim
that is **true** but computed over a smaller population than the sentence says it covers — the
shape `controls.py` itself calls *"a printed claim wider than the code verifies"*.

---

## FINDINGS

### F1 (headline). The gate table is not a measurement of the predicate, and 57 of 297 pairs are attributed to a gate the predicate never reaches

`absorbable_by_diagonal_twist` (`face_complex.py:770-775`) does **not** run three stages. It runs
one loop:

```python
for i in range(m):
    if len(A[i]) != len(B[i]) or A[i][i] != B[i][i]:   # gate 1, row i
        return False
    for j in range(m):
        if abs(A[i][j]) != abs(B[i][j]):               # gate 2, row i
            return False
```

Gates 1 and 2 are **interleaved by row**. A pair whose diagonal moves in row 4 and whose magnitudes
move in row 0 exits at the *magnitude* comparison. `deciding_gate` (`controls.py:661-668`) tests
**all** diagonals, then **all** magnitudes, and reports the first that fires. Measured over the four
scored rows (`out_gates.txt`):

| row | corruption | bites | `deciding_gate` diag/mag/par | the predicate's own order | differ |
|-----|-----------|------:|------------------------------|---------------------------|-------:|
| I1 | `ridge_facets` | 72 | **72 / 0 / 0** | **15 / 57 / 0** | **57** |
| I2 | `split_free_as_interior` | 82 | 82 / 0 / 0 | 82 / 0 / 0 | 0 |
| I3 | `ridge_drop` | 82 | 82 / 0 / 0 | 82 / 0 / 0 | 0 |
| I4 | `facet_offbyone` | 61 | 58 / 3 / 0 | 58 / 3 / 0 | 0 |

The artifact prints *"WHICH GATE of absorbable\_by\_diagonal\_twist settles each answer, per row —
**I1 72 biting = 72 diagonal + 0 magnitude + 0 parity**"*. On the predicate's own execution it is
15 + 57 + 0. `deciding_gate`'s docstring states the premise that makes the table read as a trace:
*"The predicate answers … in **three stages**"* (`controls.py:641-642`). It does not.

**And the two gates are not alternatives here at all.** Every one of the **294** `diagonal`
attributions is *also* an absolute-value violation — 294 of 294, and provably so, not measured so:
`L^rel = dᵀd` has a non-negative diagonal and `D − A` has a non-negative diagonal, so two unequal
diagonal entries have unequal absolute values, and the magnitude loop runs over `j == i` too. The
absolute-value gate **subsumes** the diagonal gate on this population.

Mutation **M2** makes that operational and it is the sharpest evidence in this audit: **delete
`A[i][i] != B[i][i]` from the predicate and `controls_output.txt` regenerates byte-identically,
exit 0.** The gate the repair calls *"the FIRST of the predicate's two forced gates"* can be removed
from the predicate without the battery noticing. So the sentence *"three at the diagonal gate and I4
at the absolute-value gate"* is a statement about the order of two tests inside a function mg-da45
wrote, not about `absorbable_by_diagonal_twist`.

**What this is and is not.** It is the arc's defect class at one more remove: a control asserting a
reason it does not have — here, that a printed split is the predicate's. It is **not** a defect in
the conclusion. Both gates are forced whatever the order; the parity total is 0 either way; row I4,
the row the whole repair is about, is attributed identically by both readings. The correction owed
is to the framing (`deciding_gate` classifies which forced gates a pair violates, in a stated
priority; it does not trace the predicate), not to any number.

### F2. *"0 entries anywhere differ in sign alone"* is computed over 3 of the 297 pairs — and the landing's own verifier has the same `continue`

`controls.py:1001-1005` accumulates `sign_entries` **inside the `diag_preserved` branch**:

```python
if gate == "diagonal":
    diag_moved += 1
else:
    diag_preserved += 1
    dm, ds = entry_mismatches(L_mut, target)
    mag_entries += dm
    sign_entries += ds
```

`tot_sign` is therefore a sum over the pairs whose diagonal survived — **3 of 297, 1.0% of the
population**. The routing row prints it as *"measured over all four rows, … 0 entries **anywhere**
differ in sign alone"* (`controls.py:1130`), and the gate table as a *"Section total"*.

**The number is right.** Measured over all 297 pairs it really is 0 (`out_gates.txt`), and over all
1201 biting pairs at n = 6 it is also 0 (`out_n6.txt`). This is a warrant finding, not a
correctness one — and it is not pedantic:

- **M7** — widen the census from 3 pairs to 297 and the artifact is **byte-identical**. Nothing
  changes today. That is precisely why the narrow scope is invisible.
- **M8** — inject a genuine sign-only mismatch on I4's *diagonal-moved* pairs (55 pairs, 110
  entries). The battery **still exits 0**, row I4 still passes, and the routing row **still prints
  "0 entries anywhere differ in sign alone"**. The sentence is then false and nothing reports it.

**The landing's own verifier repeats it.** `verify_landing.py:127-135` does `if g == "diagonal":
dia += 1; continue` *before* counting sign-only entries, then checks *"not one entry **anywhere** in
those rows differs in SIGN ALONE"*. So the *"25 claims scored, 0 BROKEN"* verification does not
cover this sentence either. Its `gate()` is also the same four-line priority function as
`deciding_gate`, written — its docstring says — *"from the predicate's DOCSTRING, not from
controls.py's copy of the same idea"*. That is true about provenance and is exactly the mechanism of
F1: **the independence is in the numbers, not in the definition, and the definition is what the
defect was about.**

### F3. *"forced at every n"* is argued for antichains only; the other half is neither argued nor measured — and this audit measures it

The section docstring's argument is checked here in full and every step holds (`out_antichain.txt`):
`le_to_facet_offbyone(w) == le_to_facet(rot(w))` on 46232 words at n = 2..8; rot-conjugation keeps
`n−2` of the `n−1` adjacent transpositions adjacent at every n = 3..8; exactly one neighbour of every
vertex changes, giving **2 per row** and `2|L(P)|` in total — **12 / 48 / 240 / 1440 / 10080 /
80640** at n = 3..8, with **0** sign-only mismatches and the diagonal preserved at every size. The
n = 7 and n = 8 figures are new; mg-f1b2 and mg-da45 both stop at n = 6.

But `rot` maps `L(P)` onto `L(P)` **only when `L(P)` is all of `S_n`**, so the argument is about
antichains. *"Forced at every n"* also needs the other half — that at larger n **no other poset** has
row I4's diagonal preserved, since such a poset is exactly what would reach the parity system and
make the absorbability answer a decision after all. That half is argued nowhere and measured
nowhere in the chain: mg-f1b2's `out_gates.txt` runs the four-mutation split at n ≤ 5 and the
antichain alone at n = 6; `verify_landing.py` does the same.

**Measured here** (`a3_n6_population.py`, all 318 posets on 6 elements, all four scored mutations):

```
I1 312 biting = 312 diagonal + 0 magnitude + 0 parity
I2 317 biting = 317 diagonal + 0 magnitude + 0 parity
I3 317 biting = 317 diagonal + 0 magnitude + 0 parity
I4 255 biting = 254 diagonal + 1 magnitude + 0 parity
totals: 1201 biting pairs, 0 reaching the parity system, 0 absorbable,
        0 entries differing in sign alone over ALL 1201 pairs,
        and the ONLY diagonal-preserved pair in the whole population is the antichain.
```

So the claim gains a size and loses nothing. It remains a claim whose second half the file does not
argue.

### F4 (minor). *"three at the diagonal gate and I4 at the absolute-value gate"* against its own table

The final measured-block sentence assigns one gate per row. The gate table three lines above it
gives I4 as **58 diagonal + 3 magnitude**: on 58 of its 61 biting pairs I4 is settled at the
diagonal gate. The sentence is a fair summary of *what changed* — the three magnitude-gate pairs are
the newly-forced part — and is not a fair summary of the row.

### F5 (minor). Two printed quantities are narrower or wider than the code that computes them

- `entry_mismatches` counts **the whole matrix**, diagonal included, and row I4 prints its value as
  *"%d off-diagonal magnitudes"*. Correct today only because it is summed exclusively over pairs
  whose diagonal is preserved — an invariant nothing in the code asserts. Both counts are computed
  separately in `a1_gates.py`; on the three cited posets they coincide (300 = 300).
- The gate table prints `"%s %d biting = %d diagonal + %d magnitude + %d parity"` with the left side
  `app` and the right side summed over `shape_ok`. Equal here (297 = 297, measured), never checked;
  a shape-mismatched pair would be dropped from the sum while the printed equation still read as an
  identity. `gates[gate] = gates.get(gate, 0) + 1` would likewise silently admit a `"shape"` key
  that no printed slot shows. (The `shape_ok` guard above makes `"shape"` unreachable in practice —
  verified, 297/297 same-shape.)
- **In the commit message only, not in the file:** *"No sign was consulted anywhere in the section"*
  is contradicted by the commit's own next paragraph — NC3's gauge reaches the parity system 82/82
  and is reported inside that same section's measured block. The file's text is correctly scoped
  (*"over all four rows"*, *"anywhere in this row"*); the commit message is one word wider.

---

## WHAT STANDS — verified mechanically, and I tried to break each one

**The condition did not move.** `controls.py` was parsed at HEAD and HEAD~1, every comment and every
string literal deleted, and what is left diffed (`out_witness.txt` §3). Prose is invisible to that
diff; a moved condition is not. The diff is two new functions, four new tallies, the
`diag_preserved`/`diag_moved` branch rewritten, and new arguments to three existing `print`/`check`
calls. The scored conditions themselves, extracted from the AST, are **character-identical** across
the commit:

```
HEAD~1 : forced = diag_preserved == 0 | cond = app > 0 and rej == app and (shape_ok == app)
         | cond = cond and caused == app | cond = cond and absorb == 0
HEAD   : forced = diag_preserved == 0 | cond = app > 0 and rej == app and (shape_ok == app)
         | cond = cond and caused == app | cond = cond and absorb == 0
```

The rewritten branch is semantically identical: `deciding_gate(...) == "diagonal"` iff some diagonal
entry differs, which is the old `all(L_mut[i][i] == target[i][i])` negated. The one way it could
differ — a `"shape"` return falling into the `else` — is unreachable behind the `shape_ok` guard,
and 297/297 pairs are same-shape.

**No new scored row.** 26 `check(` call sites before, 26 after.

**The witness was withdrawn, not replaced.** The artifact contains no sentence claiming row I4 is
falsifiable; mg-8a12's phrases *"this is the witness"* and *"row I4 is falsifiable"* are both gone,
and neither is replaced by another candidate — this is false as mg-8a12 stated it, and mg-da45 says
so instead of restating it about something else.

**NC3's gauge is absorbable by construction, and this is stronger than the repair states it.** The
repair says *"D.L.D by construction"* and supports it with the predicate's answer. Here the sign
vector is **exhibited**: `s = ((−1)^j)` satisfies `sᵢ · (E·L^rel(parity)·E)ᵢⱼ · sⱼ == (D−A)ᵢⱼ` on
**86/86** posets, entry by entry, with no predicate consulted. It bites on 82, its magnitudes are
the target's on 82/82, and it is the only corruption anywhere in the section reaching the parity
system (82/82 at n ≤ 5; 317/317 at n = 6). It cannot witness anything about a pair whose magnitudes
differ.

**Row I4 can still fail — but only through one clause.** `app > 0 and rej == app and shape_ok == app
and absorb == 0`. Given claim (1) on the uncorrupted build (86/86, and **proven** for every finite
poset), `L_mut ≠ L_true` iff `L_mut ≠ target`, so `rej == app` is an identity. `|facets| = |L(P)|`
under every incidence mode, so `shape_ok == app` is an identity. `absorb == 0` is forced. What is
left that can fail is `app > 0`. This is the shape mg-f1b2 filed as F2 for the routing row, one row
over; mg-da45 correctly leaves it to its own item and says so.

**The carried-forward list is COMPLETE.** Rather than checking the repair's named list, I swept the
**whole repository** — `code/`, `docs/`, `STATE.md`, every `.py`/`.txt`/`.md`/`.sh` — for five
phrasings of the false premise: **22 occurrences, 20 of them quoted inside a denial or an audit
finding, and exactly 2 still asserting it** — `code/face_geometry_audit_fcf1/audit_nc4.py:98` and
`.../out_nc4.txt:27`. Both are the sites mg-da45 names and declines to touch, and `controls.py`
points at `out_nc4.txt:27` by name. The sweep excludes **its own** directory and says so in its
output rather than silently: `a6_mutations.py:165` carries the sentence as a mutation *payload* (M5
reinstalls it precisely to check that a text sweep would catch it), which is not an assertion of it
— but a sweep that quietly skipped itself would be the shape of the defect under audit.

**Byte-for-byte and edge cases.** `controls_output.txt` regenerates identically, exit 0.
`python3 controls.py 2` exits 1 with `CONTROLS FAILED: 3` at **both** HEAD~1 and HEAD, so mg-f1b2's
F3 is untouched exactly as claimed.

---

## MUTATION BATTERY — exit codes predicted before the run

Eight mutations, each applied to a temporary copy of `code/face_geometry`. Predictions were written
into `a6_mutations.py` before any of them ran and are printed above the results
(`out_mutations.txt`). **8 of 8 correct.**

| id | mutation | exit (pred) | artifact (pred) |
|----|----------|------------|-----------------|
| M1 | delete the `\|sᵢsⱼ\| = 1` gate from the predicate | **1** (1) | CHANGES (CHANGES) |
| M2 | delete the `sᵢ² = 1` gate from the predicate | **0** (0) | **IDENTICAL** (IDENTICAL) |
| M3 | `deciding_gate` returns `"parity"` where it returns `"magnitude"` | 0 (0) | CHANGES (CHANGES) |
| M4 | `entry_mismatches` returns the magnitude count as the sign count | 0 (0) | CHANGES (CHANGES) |
| M5 | row I4's printed reason reverted to mg-8a12's, denial removed | 0 (0) | CHANGES (CHANGES) |
| M6 | `cond = cond and absorb == 0` deleted from row I4 | 0 (0) | **IDENTICAL** (IDENTICAL) |
| M7 | `sign_entries` accumulated over all biting pairs (the F2 repair) | 0 (0) | **IDENTICAL** (IDENTICAL) |
| M8 | a real sign-only mismatch injected on I4's diagonal-moved pairs | 0 (0) | CHANGES (CHANGES) |

M1 reddens the brute-force-agreement instrument row: the absolute-value gate is what forbids row
I4's three antichains, which is F1 of mg-f1b2 confirmed from the other direction. **M2 is silent**
(F1 above). **M6 is silent and byte-identical** — the clause the entire repair is about can be
deleted with zero visible effect; mg-da45 declares that exposure (*"NO NEW SCORED ROW,
deliberately"*) and the declaration is defensible, but this is its size. **M7 is silent** and **M8
is green while printing a false sentence** (F2 above).

---

## MINOR / CARRIED FORWARD (not mg-da45's to fix, recorded so they are not lost)

- mg-f1b2's **F2** (the routing row cannot fail), **F3** (the `[CANNOT FAIL]` row's per-row half at
  `nmax = 2`), **F4**, **F5** — all named as carried forward by mg-da45 and all still open. F3
  reproduced here: `controls.py 2` exits 1 with 3 failures at HEAD, identically to HEAD~1.
- `STATE.md:314` — *"Three of NEGATIVE CONTROL 4's four rows then could not fail … so 'absorbable on
  0 of N' is ARITHMETIC for I1/I2/I3 at every n"*. Read against this commit it is **understated, not
  false**: the sentence is about rows, and what it says about I1/I2/I3 is true; it simply does not
  say the same of I4. mg-da45's characterisation of it is accurate. Not edited here.
- `code/face_geometry_audit_fcf1/audit_nc4.py:98` and `out_nc4.txt:27` — the two surviving unmarked
  assertions of the premise, in another item's committed audit artifact. Named by mg-da45.
- `code/face_geometry/run_all.sh` — stale runtimes and a *"CI-adjacent battery"* with no CI in the
  repository. Named by mg-da45.

---

## MY NEAR-MISSES, and what I audited that no list named

**Recorded because a claim of compliance is cheap and a claim of non-compliance against oneself is
not.**

- **My own mutation was the one thing that failed first.** M5's first draft added a `%d` to a format
  string whose argument tuple it did not touch; the mutated battery died on a `TypeError` and exited
  1 against my predicted 0. **7 of 8, not 8 of 8, on the first run** — and the eighth was my
  arithmetic, not the battery's. The corrected patch is what ships; the first draft is recorded in
  `a6_mutations.py`'s docstring.
- I expected *"0 entries anywhere differ in sign alone"* to be **false**. It is true — on all 297
  pairs at n ≤ 5 and all 1201 at n = 6. F2 is a warrant finding only.
- I expected the `diag_preserved`/`diag_moved` branch swap to be a latent bug through a `"shape"`
  return. It is not: the `shape_ok` guard makes it unreachable, 297/297.
- I expected `absorb == 0` to have been quietly weakened or dropped. It is verbatim, and the
  code-only diff proves nothing else moved either.
- I expected a replacement witness for row I4. There is none; the claim was withdrawn.
- I expected the n = 6 population to contain a non-antichain with a preserved diagonal. It does not
  — 1 of 255.
- I expected NC3's *"spectrum provably moves on 0/82"* to be an artefact. It is right and it is
  forced: the gauge is a conjugation.

**Four things audited that this brief's list does not name** (the brief asked for at least one):

1. **The predicate's execution order against `deciding_gate`'s priority order.** The brief says
   *"read the predicate, not the repair's description of it"*; the repair's description turns out to
   be of a three-stage predicate that does not exist. This is F1.
2. **Whether the two gates are separable at all on this population.** They are not: the
   absolute-value gate subsumes the diagonal gate wherever both matrices have non-negative
   diagonals, which is always. M2 demonstrates it.
3. **The gate split over the whole n = 6 population** (318 posets, 1201 biting pairs) rather than
   the antichain alone. This is the unmeasured half of *"forced at every n"* — F3.
4. **A whole-repository sweep for the false premise**, rather than a check of the repair's named
   carried-forward list. The list turns out to be complete: 2 loose occurrences, both named.

---

## NET

The repair does what mg-f1b2's F1 asked and does not over-correct: the condition is untouched to the
character, no scored row was added, the withdrawn witness was not replaced with another that cannot
bite, and every number in the corrected text reproduces from an instrument that shares no code with
it — plus two sizes of new evidence at n = 7 and n = 8 and a full n = 6 population sweep, all of
which agree with it.

What did not fully land is the repair's account of **why** its answer is forced. `deciding_gate` is
a priority ordering the repair invented, presented as a trace of the predicate; it disagrees with
the predicate on 57 of 297 pairs, and the gate it calls "first" can be deleted from the predicate
without changing a byte of the artifact. And the one number the repair leans on hardest for the
sign question — *"0 entries anywhere"* — is computed over 1% of the population the sentence names,
in the file **and** in the verifier that scored the file 0-BROKEN.

Both are corrections to the printed reason, not to the mathematics, which is what a sixth
generation of this defect looks like. The right repair is one paragraph in two docstrings and one
`continue` moved four lines — and, if anything is to be widened, the sign census, because M8 shows
a green battery printing that sentence falsely.
