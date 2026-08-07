# `pairbias_repair_ba78` — mg-6bc2's section 5, repaired

**Work item.** `mg-ba78`. **Repairs.** [`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`](../../docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md)
§5 and its P6 row, and `code/pairbias_sharpening_6bc2/` in place.
**Defects found by.** `mg-200d`, against mg-6bc2 as merged (`e1f7bb2`).

## What is NOT repaired, because it is not broken

mg-6bc2's theorem — `max{ 6E_μ[inv_e]/(n²−1) : μ ∈ M_n } = n/(n+1)`, attained —
**stands untouched.** `mg-200d` reproduced it exactly at `n = 3,4,5,6` on an
independent two-phase solver. Both defects below sit *downstream* of the LP
optimum, in the adjacency diagnostics that §5 reports.

## The two defects

**Defect 1 — the optimisers were sub-probability measures.** `lp6bc2.relaxation_lp`
normalises with `sum mu <= 1`, an *inequality*, because its simplex requires the
origin to be feasible (`Ax <= b`, `x >= 0`, `b >= 0`) so that phase 1 can be
skipped. Both objectives vanish at the identity, so the simplex had no reason to
place the leftover mass, and the returned measure at `n = 3` carried **total mass
2/3**. The optimum value is unaffected: the identity adds `0` to `E[inv]`, `0` to
`E[F]` and `0` to every pair's flip probability, so completing on it is feasible
at the same objective — which is exactly why the theorem survives, and it is
**checked** here rather than asserted (`T2`, 32 checks). The adjacency
diagnostics, though, are *equality tests between masses*, not linear functionals,
and a missing third changes their answers.

**Defect 2 — the two columns were in different units.** `measure_stats` filtered
the **ordered** keys of the adjacency dict; `per_slot_violations` iterated
`x < y`, i.e. **unordered** pairs, crossed with slots. So "6 vs 8" at `n = 4` was
not a comparison.

## The repair

Complete every measure to a probability measure before diagnosing, and put both
columns on **unordered pairs**, keeping the `(pair, slot)` count as a separately
labelled finer unit. On the common unit the two diagnostics **nest** —
aggregate-violated ⊆ per-slot-violated, since `Σ_k J_k(x,y) ≠ Σ_k J_k(y,x)`
forces some slot to differ — and the inclusion is checked, and checked to be
*strict* somewhere, so the columns are not one number under two names (`T6`).

| `n` | aggregate, published | aggregate, repaired | per-slot, repaired |
|---|---|---|---|
| 3 | **0** ordered keys, mass 2/3 | **2** / 3 unordered pairs | **3** / 3 |
| 4 | 6 ordered keys | **5** / 6 | **6** / 6 |
| 5 | 8 ordered keys | **6** / 10 | **7** / 10 |
| 6 | 10 ordered keys | **7** / 15 | **8** / 15 |

(inversion optimiser; the footrule optimiser's figures are in `out_r1_repair.txt`.)

## Which defect moved which number

`r2_isolate.py` crosses `{uncompleted, completed} × {ordered, unordered}`, four
cells per `(n, objective)`, because two defects reported together do not say
which one moved a figure. The split is clean:

- **Only defect 1 can move the `n = 3` number off zero.** The unordered predicate
  on the *uncompleted* measure still reads `0`, so the unit fix alone would have
  left *"the aggregate form excludes nothing at `n = 3`"* standing. Completion is
  what turns `0` into a violation; the unit then decides `3` or `2`.
- **At `n > 3` the measure was already at mass 1**, so the whole change is
  defect 2 — which bites at every `n`, `8` cells of `8`.

## Files

| file | what it is |
|---|---|
| `lib_ba78.py` | completion, both diagnostics on one declared unit, and mg-6bc2's own predicate kept so the published figures can be *reproduced* rather than asserted |
| `r1_repair.py` | published vs repaired, per `(n, objective)`, plus the repaired §5 table |
| `r2_isolate.py` | the 2×2 that says which defect moved which figure |
| `selftest_ba78.py` | 10 blocks, 5 of them negative controls or mutations; hand values written in the docstring before the code ran |
| `run_all.sh` | regenerates all three transcripts; aggregate exit 0 |

```sh
sh run_all.sh
```

**The LP is assembled here rather than imported.** mg-ba78 also repairs
`lp6bc2.relaxation_lp` *in place*, so importing it would make the "as published"
arm depend on whether that repair is present — and showing the difference between
the two arms is this directory's whole job. What *is* imported from `lp6bc2` is
the part that was never in doubt: the exact-rational simplex and the
combinatorial primitives.

## Bounds

- **`n ≤ 6`.** `S_n` is enumerated. Every figure here is finite-population and
  none is evidence at unbounded `n`.
- **Nothing here computes what the per-slot lemma buys.** That value is
  `mg-200d`'s, is cited in the repaired §5, and is **not re-derived here** — the
  completion argument that rescues the *unconstrained* theorem does **not**
  transplant to the constrained LP, because the identity itself violates per-slot
  symmetry (`J_0(0,1) = 1`, `J_0(1,0) = 0`) and so is not available as the place
  to put leftover mass.
- **No poset enumeration.** `mg-345e`'s and `mg-6bc2`'s refusal is kept.
