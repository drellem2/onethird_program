# `pairbias_sharpening_6bc2` — the marginal-relaxation LP

**Work item.** `mg-6bc2`. **Deliverable doc.**
[`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`](../../docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md).

> ## ⚠️ REPAIRED IN PLACE BY `mg-ba78` — the adjacency diagnostics, not the LP
>
> `mg-200d` found two defects downstream of the optimum. **The optima, and the theorem, are
> unaffected and are not changed here.**
>
> 1. `relaxation_lp` normalises with `sum mu <= 1` (the simplex needs the origin feasible so phase 1
>    can be skipped) and both objectives vanish at the identity, so it **returned sub-probability
>    measures** — mass `2/3` at `n = 3` — and `v1`/`v2` diagnosed those. It now completes on the
>    identity, which adds `0` to `E[inv]`, `0` to `E[F]` and `0` to every flip probability.
> 2. `measure_stats` counted **ordered** adjacency keys while `v2.per_slot_violations` counted
>    `x < y`, so the two columns of the doc's §5 table were in different units. Both are now per
>    **unordered pair**, and the `(pair, slot)` count is printed as the separate finer unit it is.
>
> **Every committed transcript here was regenerated**, and `out_v2_optimiser.txt` now covers
> `n = 3,4,5,6`. Superseded figures, the 2×2 that isolates which defect moved which number, and the
> repair's own self-test live in [`code/pairbias_repair_ba78/`](../pairbias_repair_ba78/).

## What it computes, and what it does NOT

It maximises `E[inv_e]` and `E[footrule]` over **every probability measure on `S_n`** subject to one
family of constraints — every pair flipped against the reference order with probability `≤ 1/3`.
That feasible set is the formalisation of **"pair bias alone"**: any derivation that knows only the
per-pair flip probabilities and uses linearity of expectation is valid on all of it, so its
constant is at least this maximum.

**It enumerates no posets.** `mg-345e`'s refusal is kept: the frozen class is empty at every `n`
this corpus can enumerate, so an empirical calibration of `ε_sup` would measure a hypothetical
population. Measures on `S_n` are a different object — the relaxation itself.

## Run

```
python3 selftest6bc2.py            # 7 constructions, 3 negative controls; exits 0
python3 v1_relaxation.py 3 4 5     # n=6 is a separate run, see out_v1_n6.txt
python3 v2_optimiser.py  3 4 5 6   # the optimisers themselves + adjacency-symmetry tests
```

Exact rationals throughout (`fractions.Fraction`); no floating point in any decision. The simplex
uses Bland's rule, so it terminates.

## Committed transcripts

| file | what |
|---|---|
| `out_selftest.txt` | selftest, exit 0 |
| `out_v1_n345.txt`, `out_v1_n6.txt` | the optima at `n = 3,4,5,6` |
| `out_v2_optimiser.txt` | the optimising measures and their adjacency-symmetry violations, `n = 3,4,5,6` |

## Headline

`max E[inv_e] = C(n,2)/3` **exactly** at every `n` tested — so `Op-Form` Claim 6.1 is an **equality**
for the information it consumes, not a bound awaiting a sharpening. `max E[footrule] = 2·C(n,2)/3`,
so both forms of the master bound give `ε = n/(n+1)` and **the footrule form buys nothing** — the
one cheap lever on the board, tested and dead.

## Defect recorded in the code, not only in the doc

The lead this instrument was built to test (`PREDICTIONS.md` H3: the two-atom law scores `1/2` in
the footrule form, so switching forms looks like a free factor of 2) was already refuted by the
author's own hand construction (H4) **before the LP ran**, and the LP then returned `0` gain. H3 is
a witness-specific artefact that was read as a structural fact. It is kept in `PREDICTIONS.md` as
written.

**And a second one, found from outside.** `PREDICTIONS.md` P6 was scored `REFUTED` off `0`
aggregate violations at `n = 3` — a figure measured on a measure missing a third of its mass.
Completed, it is `2` of `3` pairs, so **P6 held**. The prediction is kept as written and the
superseded scoring is struck rather than deleted, in the doc's §8. The general shape is worth
keeping: the LP's optimum is invariant under the missing mass and the adjacency diagnostics are
not, and both were read off the same returned object.
