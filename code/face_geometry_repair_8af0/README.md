# mg-8af0 — the repair of mg-fcb2's F1, F2 and F3

**Target:** `code/face_geometry/controls.py`'s `NEGATIVE CONTROL 4` and its verifier
`code/face_geometry_repair_e35b/verify_e35b.py`, as audited by mg-fcb2 against the merged mg-e35b
repair (`5f542f0`).

**In one sentence.** *The row that was supposed to catch a count nobody can move was itself a count
nobody can move; it is replaced by coverage of a population read out of the section's source, every
verdict it makes is flipped on a constructed input, and it found a second forced count and refuted
its own author twice before it went green.*

Run it with `sh run_all.sh` (about 76 s, pure Python 3, exit 0).

---

## The order, and why it is the whole point

**F2 was repaired first, in its own commit, with F1 deliberately left in place.** At that commit
`verify_e35b.py` **exits 1** with exactly one refuted row, naming `controls.py:1927` printing
`N/N`. The transcript is committed at `out_verify_e35b_F2COMMIT_exit1.txt`.

That transcript is the only evidence that will ever exist that this mechanism can fail on a real
defect rather than on a construction. Repairing F1 first would have produced a green verifier and no
such evidence, and would have left the mechanism that hid F1 — a completeness row scoring
`forced == 3 and len(table) == 11` — fully intact for the next count to land behind.

| commit | | `verify_e35b.py` |
|---|---|---|
| `0c39f34` | F2: V6 rewritten, V7 added, F1 untouched | **exit 1**, 1 refuted |
| `fb158c5` | F1: the coverage numerator measured | exit 0 |
| `a82acb3` | F3: all four zeros forced; grain named | exit 0 |

---

## F2 — what was wrong, and what "fixed" has to mean

`verify_e35b.py:402` scored `forced == 3 and len(table) == 11`, where `table` was the list of string
literals defined twenty lines above it. Both operands were functions of that literal alone. Nothing
in the condition — and nothing anywhere in the file — opened `controls.py`.

**A row that scores a literal is not a weak control. It is not a control.** It reports the same
verdict whatever the input and had never been shown capable of reporting anything else. So the
repair is *not* "replace the literal with a computation". What is scored now is **coverage of a
population the verifier did not write**:

> **POPULATION** — every `%`-formatting expression carrying at least one `%d`, lexically inside
> `negative_control_incidence` in `controls.py`, read out by `ast`. **32 sites.** Wider than "the
> lines mg-e35b touched", because the next count will not land only where the last one did.
>
> **GRAIN** — one row per **site**, not per figure; **173** `%d` conversions across the 32. Each
> row's key carries its site's figure count, so adding a figure to an **existing** sentence breaks
> the match too.

Three scored rows, each with a constructed input that flips it (`V7`; all three are AST rewrites, so
none depends on the text of a line a later repair may move):

| scored row | the input that refutes it | result |
|---|---|---|
| every site claimed by exactly one row | a **twelfth count injected** into the section, verifier untouched — mg-fcb2's own F2 demonstration, pointed back at the repair | 33 sites, **1 unclaimed, REFUTES**. Under the old condition it stayed **green** |
| every row claims exactly one site | the ridge sentence **deleted** | 30 sites, **2 rows claim nothing, REFUTES the other way** |
| no site fills an `X/Y` from the **same expression** twice | the coverage numerator **rewritten to its denominator** (F1, reconstructed) | **1 site flagged**, and it is that one |

and a fourth for F1's repaired figure:

| | shipped `n ∈ 2..5` | `n = 1` admitted | corruption made a no-op |
|---|---|---|---|
| repaired numerator | **86/86** | **86/87** | **0/86** |
| the `(N, N)` it replaced | 86/86 | 87/87 *(truth 86 of 87)* | 86/86 *(truth 0)* |

Three values against one. That is the difference between a count and a sentence.

---

## What the repaired mechanism found that nobody asked for

**A second forced count, in a species the structural scan cannot see.** `controls.py:1531` prints
*"All %d vacuous posets are ones where the mutation DID NOT APPLY … (%d of %d)"*. The sentence is
printed only under `if blind == 0`, and the parenthetical is filled `(vac - blind, vac)` — inside
that branch the two are equal by arithmetic, so it can **only ever print `(k of k)`**. The scanner
does not flag it: the two *expressions* differ, and only their *values* are forced. It is not in
mg-e35b's eleven-row table at all, and it was found by deriving the population rather than by reading
the artifact. Classified **FORCED BY THE BRANCH GUARD** and recorded — see OPEN 1.

---

## F1 — the count

`controls.py:1927` supplied `(N, N)`. The numerator is now `site_corrupted`, a sum over the
population. The **committed artifact is byte-identical** after that repair: the repaired expression
prints the same characters the tautology printed, which is exactly why F1 needed an instrument and
not an eye.

The sentence now names what it is counting: **population** the 86 posets; **grain** the poset,
counted corrupted when the ORDERED facet list built by `le_to_facet` differs. **At the facet-SET
grain the answer is 82, not 86** — four posets differ only in the order of the same facets.

**mg-fcb2's OPEN 4 is decided, not deferred.** The population is **not** widened to admit `n = 1`.
Widening moves every other count in the section and every figure in the artifact, to fix a defect
that is not about the range. The widened population is worth more as the input that flips the figure,
and that is what it is used as.

---

## F3 — the label

mg-e35b: *"I4 rebuilds the facet enumeration outright, so a ridge there CAN lie in >= 3 facets; its
zero is the only one of the four that is a result."* **Withdrawn.** All four are forced.

Both `le_to_facet` and `le_to_facet_offbyone` return a chain of masks of sizes `1, 2, …, n−1`. A
ridge omits the level-`k` mask; the two masks bracketing it differ in exactly two elements; exactly
two candidates to re-insert. **It is a property of the maps, not of the mutation** — which is why
"rebuilds the enumeration outright" did not save it.

Premise and conclusion are measured **separately**, over a wider population than the section runs on
(810 `(poset, facet map)` families, every poset up to isomorphism with `n ≤ 6`, grain: the ridge):
premise **810/810**, largest multiplicity **2**, families with a ridge in `≥ 3` facets **0**.

**And the bound is shown capable of failing** — without that, "no ridge in ≥ 3 facets" is the output
of a routine never seen to say anything else. A constructed family with profile `[1, 3]` has a ridge
in **three** facets under the *same* routine. Swept over all 11 level-size profiles on a 5-element
ground set, **exactly one** has multiplicity `≤ 2` — the full profile `1..n−1`, the one both maps
produce. The bound is tight.

---

## Predictions, scored

`PREDICTIONS.md` was committed at `cdc7d6f` **before a line of this repair's code existed**. Nothing
in it has been edited. Four figures in it are disclosed there as **measurements already taken** and
are excluded from this table.

| | prediction | outcome |
|---|---|---|
| **P-1** | population derived from source; `len(table) == 11` gone | **ON** — the string survives only inside prose quoting the old condition |
| **P-2** | F2 commit exits **1**, exactly one refuted row, the tautology row | **ON**, exactly |
| **P-3** | F1 commit exits 0 | **ON** |
| **P-4** | injected count → exactly 1 unclaimed, refutes | **ON** |
| **P-5** | deletion refutes the other way; *"I expect the first form of my check to get exactly one of these two directions and not both"* | substance **ON**; **the hedge is REFUTED** — the first form got **both** directions |
| **P-6** *(risky)* | ≥ 1 FORCED count absent from mg-e35b's table | **ON** — `controls.py:1531`, the branch-guard tautology |
| **P-7** | artifact **byte-identical** after F1 | **ON** |
| **P-8** | widened population prints 86/87 | **ON** |
| **P-9** | no-op corruption prints 0/86 | **ON** |
| **P-10** | 810 families, largest multiplicity 2, 0 over the bound | **ON**, exactly |
| **P-11** | *"any facet family whose members are chains of masks of sizes 1, 2, …, n−1 has ridge multiplicity at most 2"* | **ON** — and see the miss below, which is **not** a miss of P-11 |
| **P-12** | my own completeness check fires on **me** first time — *"an anchor matching two sites, or a site I failed to claim"* | outcome **ON**, **mechanism MISSED**, and it fired **three** times, not once |
| **P-13** | `face_geometry/run_all.sh` exits 0, `probe_output_n6.txt` byte-identical | **ON** |

**Exit codes.** Every one landed as predicted, with one row of the table **void**:

| script | predicted | actual |
|---|---|---|
| `verify_e35b.py` at the F2 commit | 1 | **1** |
| `verify_e35b.py` at the F1 commit and after | 0 | **0** |
| `flips_8af0.py` | 0 | **VOID — THAT SCRIPT DOES NOT EXIST.** The flips went into `verify_e35b.py`'s V7 instead, where the thing they flip is defined. Not scored as a pass |
| `forcing_8af0.py` | 0 | **0** |
| `run_all.sh` (this directory) | 0 | **0** |
| `face_geometry/run_all.sh` | 0 | **0** |

---

## Defects of this repair's own instruments

Recorded rather than quietly corrected. All three were caught by this repair's own checks, and each
failing transcript is committed beside the passing one.

1. **The round-trip check compared a sequence where the population is a multiset.**
   (`out_verify_e35b_FIRSTFORM_exit1.txt`.) `ast.unparse` puts each statement on one line, which
   collapses a nested `%` site onto its parent's and reorders a population it does not change. The
   instrument reported a difference that was not there. This is what actually fired first — **not**
   the mechanism P-12 named.
2. **Naming the grain broke my own key, and the coverage row refuted on my own edit.**
   (`out_verify_e35b_F3GRAIN_exit1.txt`.) Adding population and grain to the coverage sentence took
   it from 12 figures to 15; the `(anchor, figure-count)` key stopped matching and the row went red
   before I updated the table. That is precisely the hole a sentence-only key would have left open,
   demonstrated on a real edit rather than a constructed one — the best evidence in this repair that
   the mechanism works, and I did not build it deliberately.
3. **S4's generalisation was wrong and its own sweep refuted it.**
   (`out_forcing_8af0_FIRSTFORM_exit1.txt`.) I generalised F3's forcing to "consecutive profiles".
   The sweep refuted it on its own output: `[1, 2]` is consecutive and gives 4, `[2, 3]` gives 3. The
   dividing line is being **the full profile `1..n−1`**, not consecutiveness — a ridge omitting the
   first level is bracketed below by the empty set. **P-11 as pre-registered is exactly right**; what
   was loose was a paraphrase I wrote later in code, and the sweep caught it.

---

## STATE WHAT YOU DID NOT DO

* **mg-fcb2's F5 is not repaired.** The gauge standard disqualifies `NEGATIVE CONTROL 2`'s M1 and M3
  and their rows say nothing about it. That is a change to a different section's scored rows
  (mg-fcb2's OPEN 2) and nothing here touches it.
* **mg-fcb2's F6 is not repaired.** `code/face_geometry_audit_fcf1/audit_nc4.py:41` is another tree's
  instrument (mg-fcb2's OPEN 3), left alone deliberately.
* **F4 is repaired in one string only.** It is not in the ticket's *WHAT TO DO*, but its subject is a
  `why` inside the very table F2 made me rewrite and mg-fcb2 showed the sentence false with the
  substitution **reached** (297 calls). Leaving a sentence I had read and knew to be false inside a
  table I was rewriting was the worse option. Nothing else in F4's scope is addressed.
* **No scoring change to row I4.** Its surviving forced clause is deferred by mg-e35b to its own item
  and stays deferred.
* **The population still starts at `n = 2`** — decided, not overlooked; see F1 above.
* **The completeness mechanism covers `negative_control_incidence` only.** The rest of the battery,
  and the rest of the repository, is unscanned by it. mg-fcb2's repo-wide sweep found a second
  tautology site outside this tree and it is still there.
* **The verdicts in V6's table are still judgements.** What is derived is the population they must
  cover and the structural-tautology property; whether a given `COULD MOVE` is right is argued in the
  `why` and not proved. Three of the 32 are shown moving by construction (the coverage site, and the
  two flips); the rest are not.

## OPEN

1. **`controls.py:1531`'s `(k of k)` is classified, not repaired.** It is printed under
   `if blind == 0` and filled `(vac - blind, vac)`. Classifying it FORCED is what V6 exists to do;
   rewriting the sentence is a change to a row's printed text under a different finding's heading and
   is left to its own item. **The structural scan cannot catch this species** — the expressions
   differ and only their values are forced — so a scanner for guard-implied equalities is the general
   remedy and is not written here.
2. **The scanner is scored in the verifier, not in the battery.** mg-fcb2's OPEN 5 asked for it to be
   wired into a runner; it is wired into `verify_e35b.py`, which covers one section. Whether
   `controls.py` should carry it as a row of its own is a change to the battery's own scoring.
3. **`site_corrupted` is computed twice per poset.** `mutation_applied_at_site` and
   `mutated_facet_set_differs` each rebuild both facet lists. It costs a fraction of a second on this
   population and is not optimised.
