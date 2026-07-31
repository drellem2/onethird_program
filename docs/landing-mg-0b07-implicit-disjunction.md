# Landing mg-0b07: the disjunction is spelled with an operator, and the instrument's bound is a number

**Item:** mg-f7e1. **Closes:** mg-0b07's OPEN item (`clause` is not the floor / finding B1).
**Code:** `code/face_geometry/face_complex.py`, `code/face_geometry/controls.py`,
instrument in `code/face_geometry_instr_5f9a/`.

mg-0b07 booked the mg-64b6 repair as real and this commit does not re-open any of it: the
declaration is still **derived** and is still shown following a patch changed in two
directions, the 8-of-11 re-measure stands, `absorb_trace`'s six returns are still visible 6
of 6 under individual deletion, the inert return is still removed rather than annotated, and
the control still exits 1.

> **What it left open: `clause` was not the floor. `[len(row) for row in A] != [len(row) for
> row in B]` is a disjunction that Python spells with no operator, and its ORDER half —
> `len(A) != len(B)` — could be taken out with the width half standing for BYTE-IDENTICAL,
> exit 0, every row green. Merging had removed the HANDLE, not the rung.**
>
> **This commit takes the move mg-0b07 named as preferred, and takes the other one too because
> the first one's result requires it. The `or` is back — subtraction applied to the
> IMPLICITNESS, not to the condition — so both halves are operands the clause sweep that
> already existed deletes one at a time. It measures the width half CHANGES/exit 1 and the
> order half BYTE-IDENTICAL/exit 0, and prints the second as `NOT COVERED — deletion
> establishes nothing about it` on the row that carries it. And the bound is stated as a
> count: DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO FURTHER, with
> 11 compounds in `face_complex.py`'s deciding conditions that have no operand to delete.**

> **CORRECTED BY mg-69d1 (mg-eaef's E5 and E4), and the sentence above is left as written so the
> correction can be read against it.** That bound is **wider than the sweep**. Read as a
> guarantee about *every* explicit boolean operand it is false: of the **17** in the two files
> this census covers, **6 are not on the reached side** — 4 nested below the top level of their
> own condition in `face_complex.py`, where the sweep cannot reach, and 2 in `posets.py`, which
> the sweep does not visit. All 6 were in **neither** census column. The sentence now reads
> **DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS OF THE DECIDING CONDITIONS IN THE FILES THE
> SWEEP VISITS, AND NOTHING ELSE**, and §5 below classifies all 17.
>
> **No sixth technique was added. Two rows joined a table that was already enumerated from the
> tree, and one new section counts.**

---

## 1. What the finding was, and what it was not

Four generations, each one the previous sentence with a smaller noun:

| rung | the unit | deleting one alone |
|---|---|---|
| **gate** (mg-e7bc) | two `return`s deleted together | the pair was load-bearing, neither member shown to be |
| **return** (mg-c4c8) | two clauses of one condition | first clause alone: **byte-identical**, exit 0 |
| **clause** (mg-0b07) | one comparison of two lists | order half alone: **byte-identical**, exit 0 |

Each answer was a merge, and the merge worked twice. The third time it did not, and the
reason is worth stating precisely, because it is the only new thing here:

**A merge removes a rung only if it removes a decision. `[..] != [..]` still decides both
things — different lengths, or a differing common index — so what the merge removed was the
*handle*, not the *rung*.** mg-64b6's claim ("no boolean operator, so the smallest deletable
unit inside this gate IS the `return`") was **exact**; mg-0b07 checked it against the tree and
found `absorb_trace` contained 0 boolean operators of any kind, not merely 0 deciding ones.
The claim was true and it was about **deletion**; the question this lineage is about is what
can be **perturbed** unseen, and at that site the two came apart.

**And an uncovered thing that cannot be named is worse than one that can**, because the green
above it is read as reaching further than it does. That is the whole argument for the move
below.

## 2. The move: spell it with an operator

```python
    m = len(A)
    shape_A = [len(row) for row in A]
    shape_B = [len(row) for row in B]
    if len(shape_A) != len(shape_B) or any(
            a != b for a, b in zip(shape_A, shape_B)):
        return Trace(False, "shape", 0)
```

That is what a list comparison means, written out. The two previous rewrites merged; this one
un-merges, and it is still the subtraction move — **what is subtracted is the implicitness**.
It converts a level the instrument could not see into one it can, which is mg-0b07's option 1,
stated there as preferred.

## 3. What the sweep now measures — including where it measures nothing

`d2_deletion.py`, section **PER CLAUSE**. The population is read out of the syntax tree, so the
two new clauses are swept without anyone adding them to a list; a clause with no registered
prediction is BROKEN rather than skipped. **11 of 11 predictions matched.**

| function | clause | artifact | exit | what the result establishes |
|---|---|---|---|---|
| `absorb_trace` guard | 1 — `len(shape_A) != len(shape_B)` | **BYTE-IDENTICAL** | 0 | **NOT COVERED** |
| `absorb_trace` guard | 2 — `any(a != b for a, b in zip(...))` | CHANGES | 1 | the battery covers this clause |
| `gate_violations` guard | 1, 2 | BYTE-IDENTICAL | 0 | NOT COVERED |
| `diagonal_moves` guard | 1, 2 | BYTE-IDENTICAL | 0 | NOT COVERED |
| `Poset.leq` value | 1, 2 | BYTE-IDENTICAL | 0 | NOT COVERED |
| `Poset.comparable` value | 1, 2, 3 | BYTE-IDENTICAL | 0 | NOT COVERED |

The last column is new and it is the point. A sweep that prints only `IDENTICAL`/`CHANGES` is
read as coverage in both directions and is coverage in one: a clause whose deletion moves
nothing has been **reached** by the test and not **covered** by it.

**The order clause is UNCOVERED AND NOT INERT, and the two have different remedies.** An inert
clause should be deleted — that is what mg-9220 did with the inert `return`. This one decides
pairs the battery does not contain: cut it and the predicate answers ABSORBABLE for a 2x2
against a three-row B whose first two rows are 2 wide, against a brute force that enumerates
every sign vector and finds none. `zip` stops at the shorter profile, so the width half does
not subsume it. The distinction is claimed in the transcript, not left to a reader.

**No row was added to `controls.py` to cover it, and the reason is on the record** rather than
left as an absence. One pair — `[[0,1],[1,0]]` against `[[0,1],[1,0],[0,0]]` — would cover it
in one line, and the note at `UNREACHED_GATE_PAIRS` says so. The question this lineage keeps
failing is not "is this branch watched" but "does the evidence say what it is read as saying".
The uncovered half is now named on the line its result is read on; whoever wants it covered can
add the pair and watch that line turn, and d2's registered prediction for that clause will MISS
and say so.

**And `AFTER-5`'s site is stated where `AFTER-5` is read** (mg-0b07's B1, second remedy). The
`FINEST UNIT` line states the finest unit of the **patch** and is exact; the site is smaller,
and the run now prints, beneath that line, the guard's clause count and where each is swept.

## 4. The respelling moved nothing, measured twice

A rewrite in this lineage is measured, not asserted — `zip` truncates where `!=` compares
lengths, so this rewrite runs exactly the risk of losing the thing it exists to expose.

- **The artifact.** `RESPELL_BACK` turns the live condition back into mg-64b6's text (an anchor
  required to occur exactly once) and the battery is run on the result: **23,695 bytes, exit 0
  — byte-identical to the live run.**
- **The predicate.** Both forms are asked decision, gate label **and raised exception** over
  **28,900 pairs across 85 shape profiles** — indexed by shape, because shape is what the
  condition reads: **28,900 of 28,900 agree.** The merged two-clause form and the pinned
  two-return form are in the same section, unchanged.

The "before" text is a computed patch in this tree rather than a new pin: a pin would be a
third artifact with a provenance of its own to check, and the anchor is checked on every run.

## 5. The bound, as a count rather than a promise

`d2_deletion.py`, section **THE BOUND OF THIS INSTRUMENT**. Respelling does not terminate:
`any(a != b for ...)` is a disjunction over rows with no operator either, and stopping there is
a choice that has to be stated or it will be read as a floor for the fifth time.

| file | deciding conditions | boolean | top-level operands | compounds it cannot reach | expression nodes |
|---|---|---|---|---|---|
| `face_complex.py` | 73 | 5 | 11 | 11 | 1,002 |
| `posets.py` | 6 | 1 | 2 | 1 | 55 |

**The third column was headed `operands the sweep deletes` and it read 2 for `posets.py`, where
the sweep deletes 0 (mg-eaef's E4; corrected by mg-69d1).** It counts what `deciding_clauses`
*finds* in that file. Whether the sweep *visits* the file is a fact about the sweep, so the two
are now derived from one constant — `SWEEP_FILES` in `d2_deletion.py`, read by the sweep and by
the table that describes it — and the column is headed `top-level`.

**And every explicit boolean operand is now in exactly one named column** (mg-69d1, on E5):

| file | swept | not swept: file | not swept: nested | not determined | all |
|---|---|---|---|---|---|
| `face_complex.py` | 11 | 0 | 4 | 0 | 15 |
| `posets.py` | 0 | 2 | 0 | 0 | 2 |
| **ALL** | **11** | **2** | **4** | **0** | **17** |

`not determined` is a **column, not an omission**: an operand the classifier cannot place is
printed there rather than falling out of the table. An explicit *not determined* is checkable;
an empty cell is the absence of an answer, which is the ambiguity a stated bound exists to
remove. The 6 not-swept operands are named individually in the transcript, because a count of
what is uncovered that cannot be pointed at is the same silence as no count at all. The four
nested ones are `proper_ideals`' `m != 0` and `m != full` and `mat_eq`'s `len(a) == len(b)` and
`all(x == y for x, y in zip(a, b))`; **deleted one at a time, all four CHANGE the artifact**
(measured by mg-eaef's `e1`, re-derived by mg-69d1's `p1`), which is why they cannot be left
implicitly on the covered side.

The compounds are named in the transcript, one line each: 7 quantifiers (`any`/`all`) and 4
memberships (`x in S`) in `face_complex.py`, 1 membership in `posets.py`. Four forms are
recognised — `or`/`and`, chained comparison, sequence comparison, membership, quantifier — and
**the last column depends on none of them**: it counts every expression node in every deciding
condition, so a compound in a form nobody has thought of is inside a printed number rather than
outside every number. That is the treatment `unit_removed` gives its own three chosen units,
one rung up.

**The census is shown separating the two spellings**, so it is not an identity: on mg-64b6's
text `absorb_trace`'s guard reads as an unreachable `sequence` compound, and on this tree as an
`or` with two deletable operands and a `quantifier` left inside the second.

## 6. mg-0b07's own probe, unmodified, against the repair

`d4_auditor_rerun.py` runs `code/face_geometry_audit_0b07/p3_grain.py` as a subprocess — the
same treatment mg-d0e2's and mg-e7bc's deletion tests get. It is the **one independently
written instrument that still applies to the live tree**, because it locates the `shape` gate
by what it returns rather than by an anchor of source text.

- **6 claims scored, 1 BROKEN, and it is named rather than counted**: the claim asserting that
  `absorb_trace` contains **no boolean operator of any kind** — which is precisely what this
  commit put back. A repair whose auditor's every claim still holds has not changed what the
  auditor measured, so that claim is **required** to go red.
- **Its three perturbation rows are unchanged**: S1 (order half alone) CHANGES/exit 1, S2 (width
  half alone) BYTE-IDENTICAL/exit 0, S3 (condition → `False`) CHANGES/exit 1 — 3 of 3. The
  spelling moved; the units did not.
- **Its cross-check against `b6bc2ef` still holds**: the two sub-conditions on this tree answer
  as the two clauses do on the tree that had them.
- **Neither of its findings is withdrawn.** B1 says the order half comes back byte-identical: it
  does, and the sweep now prints that result as NOT COVERED. B2 says the `FINEST UNIT` line
  states the finest unit of the patch where a reader takes it for the site: that line is
  unchanged and still exact, and the site is now printed beneath it.

## 7. This deliverable is an artifact of the same kind as the defect it repairs

**What kind it is: a statement of an instrument's bound** — a claim about what a measurement
does *not* reach, repairing an instrument whose limit was real and unstated. The defect such an
artifact inherits is that **the bound can itself be understated**, and that it can be true and
placed where nobody reads it.

The enumeration lives in `d2_deletion.py` (`SELF_DEFECT_BRANCHES`) and is printed with every
run, so it travels with the transcript. **12 branches, 11 checked by a claim in the file, 1
carrying the reason it cannot be.** The five that are this commit's:

| # | branch | disposition |
|---|---|---|
| 7 | the regress continues below a clause | **CHECKED, on the second attempt.** mg-64b6's answer — "CANNOT ARISE FOR THE DELETION TEST" — is kept verbatim so the correction is visible. mg-0b07 checked the reason and it is TRUE; the conclusion does not follow, because it answers "can anything smaller be DELETED" and the question is "can anything smaller be PERTURBED unseen". Now: the operator makes both halves deletable, the remaining compounds are counted, and mg-0b07's perturbation probe is re-run in d4. |
| 9 | **the bound itself has a bound** — a fifth form nobody named counts 0 exactly as the list comparison did | **CHECKED, AND THE CHECK IS NARROWER THAN THE BRANCH.** The expression-node total depends on no classification, and unlike `unit_removed`'s `nodes` it is an absolute count rather than a difference, so mg-0b07's B4 (a size-preserving substitution hiding in a net) cannot arise for it. **Stated residue: it bounds how much is there and does not name what.** |
| 10 | the bound stated in a document beside the run rather than in it | **CHECKED:** census, named compounds and the NOT COVERED marker are printed in the transcript, and the marker is on the same line as the result it qualifies. |
| 11 | the respelling buys a visible clause with a behaviour change | **CHECKED TWICE:** byte-identical artifact from the reconstructed one-comparison text, and 28,900-pair agreement on decision, gate and exception. |
| 12 | the uncovered clause is really INERT, which has a different remedy | **CHECKED:** separator pairs run against brute force; a clause that turned out inert would be removed here rather than named. |

**The branch that cannot be checked, with its reason:** the `aim` strings beside each mutation
are prose and could acquire a size that contradicts the derived unit. Checking that is a parse
of English — the apparatus this lineage removes rather than adds. It is survivable because
nothing computes from an aim and the derived unit is printed on the same line.

## 8. Disclosures

- **The order half is still uncovered.** This commit makes that visible, named and printed; it
  does not make it covered, and it says so on the row rather than in a paragraph. That is
  mg-0b07's option 2 applied to the residue of option 1, which is what its result required.
- **mg-0b07's B2, B3, B4, A1 and A2 are not closed here.** B3's substance is answered (branch 7
  above is rewritten and the conclusion corrected). B2's remedy is partly taken — the site's
  clause count is printed beneath `AFTER-5`'s line — but the `FINEST UNIT` sentence itself is
  unchanged. **A1** (the transcript's commit-count line cannot be fixed by regenerating) and
  **B4** (`nodes` is a net difference and a size-preserving substitution hides in it) are
  untouched. **A1's drift is inherited again, stated rather than engineered around:** the
  transcript committed here says *"of the 7 commits that ever touched `face_complex.py`"*, and
  this commit is the eighth — so `out_d2_deletion.txt` will differ from a re-run at that one
  line the moment it lands, exactly as mg-0b07 predicted of any commit in this file's history.
  A history-dependent count cannot be pinned by regenerating; the fix A1 names is to stop
  quoting the total, and that is a change to the pin claim which this commit does not make.
- **`gate_violations` and `diagonal_moves` keep the two-clause form.** Their returns are inert
  whole (mg-c4c8 F3) and no commit in this lineage has touched them.
- **`controls_output.txt` does not move**, and neither do the derived artifacts taken from it:
  the rewrite is byte-identical on the battery. `out_d1`–`out_d4` are regenerated.
- **mg-0b07's `p3_grain.py` now exits 1 against this tree**, by design, and `d4` scores exactly
  which claim and why. Its other five scripts are that audit's record of its run against the
  tree it audited and are not rewritten.

---

**Numbers.** Battery 43 rows, 0 failures, exit 0, **23,695 bytes — unchanged**, and
`controls_output.txt` is not touched by this commit. Instrument `run_all.sh` 166 s, **92 claims,
0 BROKEN** (d1 17, d2 49, d3 6, d4 20). `out_d1_trace.txt` and `out_d3_reintroduction.txt`
regenerate byte-identically; `out_d2_deletion.txt` and `out_d4_auditor_rerun.txt` move. No
`| tee` (mg-f922).
