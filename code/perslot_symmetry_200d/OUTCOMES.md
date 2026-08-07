# `mg-200d` — outcomes against `PREDICTIONS.md`

Predictions committed at `b5784ee`, before any script of this instrument existed. Nothing below
edits a prediction; refuted ones are scored and kept as written.

## Hand measurements (§0 of `PREDICTIONS.md`)

| # | claim | outcome |
|---|---|---|
| H1 | `mg-6bc2` states the lemma for *incomparable* pairs and its scripts test all pairs | **HELD** — `v2_optimiser.py:per_slot_violations`, `lp6bc2.py:measure_stats` |
| H2 | all-pairs adjacency symmetry holds for `uniform L(P)` iff `P` is an antichain | **HELD** — proved (Thm 2.1), machine-checked on 9 hand-named posets (`S3`) |
| H3 | hence the literal reading excludes every realisable measure in `M_n` | **HELD** (`S4b`/`S4c`, `S7b`) |
| H4 | literal per-slot is infeasible at `n = 3` | **HELD** — and it is infeasible at `n = 4, 5` too, which `P8` got wrong |
| H5 | the sound branch-free consequence is `J_k(y,x) ≤ J_k(x,y)` | **HELD** — proved (Lem 3.1), 0 violations on all 9 posets (`S5`), reversed form fails (`S7a`) |
| H6 | that surrogate buys nothing at `n = 3`, by the named witness | **HELD** |
| H7 | completing `mg-6bc2`'s `n = 3` optimiser turns 0 aggregate violations into **4** | **REFUTED on the number.** It is **2** in this document's unit and **3** in `mg-6bc2`'s own ordered unit. Substance (0 → nonzero) holds. Kept as written. |
| H8 | under `Σ μ = 1` the aggregate equality form already bites at `n = 3` | **HELD, and understated** — it does not merely bite, it is **infeasible** |

## Predictions

| # | outcome | note |
|---|---|---|
| P1 | **HELD** | baseline `= C(n,2)/3` at `n = 3,4,5,6` on an independent two-phase solver |
| P2 | **HELD** | sound per-slot surrogate: no change at any `n` computed |
| P3 | **HELD** | sound aggregate surrogate: no change |
| P4 | **HELD** at `n = 3,4,5` | disjunctive value strictly below baseline |
| P5 | **HELD, exactly** | `2/3` at `n = 3`, on the predicted branch `{0,2}` comparable |
| P6 | **HELD** | sound aggregate `5/3` > sound per-slot `1` at `n = 4` |
| P7 | **HELD** | the control: branching without symmetry returns the baseline on `8/8`, `64/64`, `1024/1024` branches |
| P8 | **REFUTED** | I predicted the literal per-slot form would be feasible at `n = 4,5`. It is infeasible at both. I counted unknowns against equations; the `1/3` caps bind long before the count does. |
| P9 | **REFUTED** | I predicted the literal aggregate form feasible at `n = 3` with value in `(2/3,1)`. Infeasible at `n = 3,4,5`. |
| P10 | **REFUTED, and this is the finding** | I predicted the ratio to baseline would not fall and that the result would be a milestone rather than a wall-breaker. The ratio is `2/3, 1/2, 2/5`: the gain compounds, `ε_spec = 2/(n+1)` at `n ≤ 5`, and the sizing verdict I pre-committed to is the wrong *shape*. See §6 of the document for what replaces it — including that the all-`n` statement is a **conjecture**, so the wall-breaking reading is conditional. |
| P11 | **HELD** | `n = 6` reached branch-free; the exhaustive disjunctive value at `n = 6` was not computed and is declared |
| P12 | did not fire | the enumeration question is answered in §7 rather than ducked |
| P13 | did not fire | the no-symmetry control was run and is clean at every `n` |

**Score: 8 held, 3 refuted, 2 pre-filed errors did not fire; 1 of 8 hand measurements refuted on
its number.** The three refutations are `P8`, `P9` and `P10`, and `P10` is the one that mattered:
it is the prediction that this result would be small.

## Defects of this instrument

1. My first general construction for the `(n−1)/3` lower bound (3-colour the consecutive pairs
   by index mod 3) hits the value **and** the cap at every `n` and **violates per-slot symmetry
   from `n = 4`**. A check on only the two things I was aiming at would have passed it. Refuted
   version kept, commented, in `v3_families.py`.
2. The randomised sweep first drew branch membership from an LCG's **low bit**, which is
   periodic; it returned `0/60` feasible at `n = 4` — a search that had searched nothing while
   printing a verdict line. Fixed to bit 16, with the reason at the call site.
3. `H7` was wrong on its number (above).
