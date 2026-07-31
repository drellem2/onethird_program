# mg-eaef — independent audit of the mg-0b07 repair (`bfd7948`, item mg-f7e1)

> **BOTH MOVES WERE TAKEN AND BOTH CLAIMS ARE PART TRUE.** The `or` is really
> back and both halves are really deletable — and one of the two comes back
> byte-identical, which the subject prints on the row that carries it. The bound
> is really a count — and it is **stated wider than the sweep on one of its two
> census rows**, and it names `explicit boolean operands` as the level deletion
> reaches while **4 of the 15 explicit boolean operands** in the file it counts
> are reached by neither of its two columns. All 4 change the artifact when
> deleted here.
>
> **AND THE SUBJECT'S OWN INSTRUMENT EXITS 1 AT HEAD.** `d2_deletion.py`, re-run
> in place with nothing edited, scores **1 BROKEN of 49** against a landing
> document that says *92 claims, 0 BROKEN*. The claim that broke is the
> two-clause pin, and the commit that broke it is **the repair itself**: it
> respelled the guard into a two-clause condition, so `b6bc2ef` is no longer the
> newest commit that has one. The commit discloses a smaller consequence — one
> transcript line about a commit count — not this one.
>
> **WHAT IS CONFIRMED, MEASURED HERE AND NOT QUOTED.** The declaration is still
> DERIVED after the restructuring (patch changed in two directions, 1 of 11 rows
> moved each way, and it is the row that was edited). The re-measure re-derives
> at **8 UNDERSTATE / 3 AGREE / 0 OVERSTATE over a population of 11**, and the
> three that agree are named.

Run everything:

    ./run_all.sh            # ~6 min, 31 claims, 0 BROKEN, exit 0, 9 findings

Run the primary measurement on its own — **each side of the respelled `or`,
deleted alone, and the two rungs below it**:

    python3 e1_operand.py
    echo $?                 # 0

Run the floor item — **the subject's own instrument's exit code at HEAD, and
the one-line remedy the subject names and does not run**:

    python3 e5_floor.py
    echo $?                 # 0

| file | what it measures |
|---|---|
| `kern_eaef.py` | the harness: an AST enumerator that WALKS for boolean operators, a census, an operand splicer, a patch differ, a tree builder, the battery runner, and a runnable copy of the subject's own instrument |
| `e1_operand.py` | **THE PRIMARY MEASUREMENT**: delete each half of the respelled guard alone; then rung 6 (a nested explicit boolean operand) and rung 7 (a decision hoisted into an assignment), both run rather than named |
| `e2_bound.py` | the stated bound against the operands deletion actually reaches, per census column and per file |
| `e3_derived.py` | mg-0b07's derived-declaration test, re-run after the restructuring with this audit's own two directions |
| `e4_remeasure.py` | the 8 of 11, re-derived from `b6bc2ef`'s own table with this audit's own differ |
| `e5_floor.py` | **the floor item**, chosen here: the exit code of the instrument that raised the findings, and the counterfactual the subject asserts without running |
| `selftest_eaef.py` | this audit's own primitives on inputs counted by hand |
| `out_*.txt` | committed transcripts |
| `PREDICTIONS.md` | every prediction, registered before its run, **with the two misses kept as written** |

**CLAIMS vs FINDINGS.** A `[BROKEN]` claim means **this instrument** is wrong
and sets the exit status. A `[FINDING]` means **mg-f7e1** is; it is counted and
printed and does not. Conflating the two makes an audit unrunnable in CI by
anyone who does not already know the answer.

**Independence.** `kern5f9a.py` — the subject's kernel, and the thing that
computes both the declaration and the census under audit — is **not imported
anywhere**, and neither is `d2_deletion.py`. The enumerators, the census, the
splicer, the differ and the battery runner are re-derived here from `ast`. The
subject's `d2_deletion.py` is **run**, as a subprocess, and every number printed
about it is read out of its own stdout.

**Reading source code is not the test.** Every rung below is a patch that was
applied and a battery that was run: 4 nested operands deleted individually, an
assignment perturbed and the predicate then asked about the pair that separates
the two halves, and the subject's named remedy spliced into `controls.py` and
run at two commits.

---

## The findings

| # | finding |
|---|---|
| **E1** | **The move bought a HANDLE and not a second covered half.** Of the 2 operands the respelling created, 1 changes the artifact and 1 does not. The subject states this on the row that carries it, and this audit reproduces it independently — booked as a **disclosed limit**, not a false claim. |
| **E2** | **RUNG SIX IS REAL AND IT IS LOAD-BEARING.** 4 explicit boolean operands in `face_complex.py`'s deciding conditions are NESTED — under a comprehension in `proper_ideals`, under a quantifier in `mat_eq` — so the sweep never deletes one. Deleted here, **4 of 4 CHANGE the artifact**. Deletion reaches 11 of the 15 explicit boolean operands there are, and the 4 it misses are the ones the battery would have seen. |
| **E3** | **RUNG SEVEN: a decision hoisted out of the condition is outside every number the subject prints.** A one-token change to `shape_B = [len(row) for row in B]` reinstates exactly mg-0b07's defect and leaves the artifact **BYTE-IDENTICAL at exit 0**, removing 0 returns, 0 statements and 0 boolean operands. The `1002 expression nodes` column is offered as the total that depends on no classification; it depends on the classification *deciding condition*, and this patch is outside it. |
| **E4** | **The bound is stated wider than the sweep on one of its two rows.** The census prints `2` under `operands` for `posets.py` — a column the kernel documents as *operands the sweep can delete* and the landing document heads *operands the sweep deletes* — and the sweep deletes **0** there. The same transcript says so twenty lines above; the qualifier that travels with the claim covers only the `compounds` column. |
| **E5** | **The bound names a floor it does not reach.** `DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO FURTHER` is read as *every explicit boolean operand is on the reached side*, and 4 of 15 are on neither side of the census. They are excluded **by name**: the compound filter skips the forms `or` and `and`, on the assumption that anything spelled with an operator is deletable. |
| **E6** | **CONFIRMED.** The declaration survives the restructuring as a DERIVED value — two patches changed in two directions, in a copy where no declaration was touched, and the printed unit followed both times, on exactly the row that was edited and on no other. |
| **E7** | **CONFIRMED.** 8 UNDERSTATE / 3 AGREE / 0 OVERSTATE, population still 11, re-derived from `b6bc2ef`'s own table with this audit's own differ. The three that agree are `BEFORE-1`, `AFTER-3`, `AFTER-4`. |
| **E8** | **The instrument does not regenerate at HEAD, and the disclosure is narrower than the consequence.** `d2_deletion.py` exits **1** with **1 BROKEN of 49**, and 3 transcript lines differ. The landing document discloses only that one line — the commit count — will drift. What actually fails is the pin claim's truth condition: the repair reintroduced a two-clause `shape` guard, so `b6bc2ef` is not the newest commit that has one. The claim's own `WOULD DIFFER UNDER` names the event exactly. `d1`, `d3` and `d4` regenerate byte-identically and exit 0. |
| **E9** | **The remedy is one line, it works, and nothing runs it.** The subject names the covering pair and asserts what adding it would do. Run here: at HEAD the ORDER clause goes BYTE-IDENTICAL → **CHANGES**, exit 1; and at **`b6bc2ef`, where the same defect is still present**, the same row turns mg-c4c8's byte-identical result into CHANGES at exit 1. |

## The ladder, as it stands after this audit

| rung | the unit | who | deleting one alone |
|---|---|---|---|
| 1 | two `return`s together | mg-e7bc | the pair was load-bearing, neither member shown to be |
| 2 | one `return` of two | mg-c4c8 | first alone: **byte-identical** |
| 3 | one clause of two | mg-0b07 | first alone: **byte-identical** |
| 4 | one half of a list comparison, with no operator | mg-0b07 | order half alone: **byte-identical** |
| 5 | one operand of a restored `or` | mg-f7e1 | order half alone: **byte-identical**, and printed as NOT COVERED |
| **6** | **one operand of a `or`/`and` NESTED inside a condition** | **mg-eaef** | **4 of 4 CHANGE — and the sweep never deletes one** |
| **7** | **a decision in an assignment the condition reads** | **mg-eaef** | **byte-identical, and outside every census column** |

Rung 7 is named to show the chasing does not terminate, and it is **run** for
the same reason: an unrun rung is a sentence, and this lineage's whole subject
is the difference between the two. The next one after it is not hard to name
either — `zip` truncating at the shorter profile is a decision with no operand,
no operator and no statement of its own — which is the point.
