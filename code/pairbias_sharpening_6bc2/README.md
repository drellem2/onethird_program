# `pairbias_sharpening_6bc2` — the marginal-relaxation LP

**Work item.** `mg-6bc2`. **Deliverable doc.**
[`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`](../../docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md).

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
python3 selftest6bc2.py          # 7 constructions, 3 negative controls; exits 0
python3 v1_relaxation.py 3 4 5   # ~1 s      | n=6 takes ~15 min (720 vars, Fractions)
python3 v2_optimiser.py  3 4 5   # the optimisers themselves + adjacency-symmetry tests
```

Exact rationals throughout (`fractions.Fraction`); no floating point in any decision. The simplex
uses Bland's rule, so it terminates.

## Committed transcripts

| file | what |
|---|---|
| `out_selftest.txt` | selftest, exit 0 |
| `out_v1_n345.txt`, `out_v1_n6.txt` | the optima at `n = 3,4,5,6` |
| `out_v2_optimiser.txt` | the optimising measures and their adjacency-symmetry violations |

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
