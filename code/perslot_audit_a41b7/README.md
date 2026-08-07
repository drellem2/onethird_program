# `code/perslot_audit_a41b7/` — `mg-41b7`'s independent audit of `mg-200d`

Deliverable doc:
[`docs/OneThird-PerSlot-AdjacencySymmetry-mg-41b7-IndependentAudit.md`](../../docs/OneThird-PerSlot-AdjacencySymmetry-mg-41b7-IndependentAudit.md).
Predictions: [`PREDICTIONS.md`](PREDICTIONS.md), committed at `3c5ed10` **before one byte of
`code/perslot_symmetry_200d/`, the `mg-200d` document, or `STATE.md` was read**.
Outcomes: [`OUTCOMES.md`](OUTCOMES.md).

## What is audited, and at which commit

`mg-200d`, landed on `main` at **`762921d`** (finding+instrument+docs), `ffc5501` (evidence)
and `731a9ab` (post-landing re-check). Read at `main = dafe759`, by which time `mg-372e`
(`dafe759`) had already struck the `2/(n+1)` cells in the document **in place** — so the
document as read carries strike-through that the landing did not. Both readings are scored.

## Independence

**No code is shared with `code/pairbias_sharpening_6bc2/` or `code/perslot_symmetry_200d/`.**
`liba41b7.py` is written from the definitions: its own permutation generator (by insertion,
not `itertools`), its own inversion count, its own row builders, its own exact two-phase
simplex with Bland's rule, and its own **arithmetic dual verifier**, so every `≤` direction
here is a certificate rather than a solver claim.

The **only** contact with `mg-200d`'s code is `a4_rowcheck.py`, which imports `lp200d.build`
in order to **assert that my rows are its rows**. That is an assertion, not a dependency: no
number reported anywhere else in this audit passes through it.

Exact rationals throughout. There is no floating-point number on any decision path.

## Files

| file | what |
|---|---|
| `liba41b7.py` | combinatorics, the five row families, exact two-phase simplex, primal **and dual** verifiers, sparse reporter |
| `selftesta41b7.py` | 62 checks; **NC1** is the load-bearing one — infeasible / feasible-with-optimum-0 / feasible-nonzero must come back as three distinct answers |
| `a1_forms.py` | baseline, literal per-slot, literal aggregate; and what each symmetry family alone *pins* |
| `a2_disjunctive.py` | the disjunctive value, exhaustive over every branch, `n = 3,4,5` |
| `a3_n6.py` | the complete `n = 6` determination, with the two reductions and their controls |
| `a3b_level.py` | one `\|I\|` level of the same scan, so the levels run in parallel |
| `a4_rowcheck.py` | **P13's guard** — my rows vs `lp200d.build`, plus two negative controls |
| `a5_construction.py` | the `≥` direction at `n = 3..20` by substitution; the surrogate; the disjunctive aggregate |
| `a6_instrument.py` | **differential audit of `lp200d.measure_report`**, the load-bearing part per `pm-onethird` |
| `a7_family.py` | brief item 3's deliverable: a family of measures that **beats** `(n−1)/3` |
| `a8_downstream.py` | **pm-onethird's disjoint re-check** of `mg-131e`'s and `mg-00a1's witnesses |

## Running

```
python3 selftesta41b7.py           # 62 checks, exit 1 on any failure
python3 a1_forms.py 3 4 5
python3 a2_disjunctive.py 3 4 5    # n=5 is 1024 branches
python3 a3b_level.py 6 K           # K = 6..15, run in parallel
python3 a4_rowcheck.py             # exit 1 if my rows are not its rows
python3 a5_construction.py
python3 a6_instrument.py           # exits 1 on the LATENT eps_spec float path (see below)
python3 a7_family.py 6 7 8 9 10 11 12
```

`a6_instrument.py` **exits 1 by design**: its two failing checks are the latent
`eps_spec(n, <python int>)` float path in `lp200d.py`. That path is shown in the same script
**not to bite at any live call site**, because `measure_report`'s `E_inv` is a `Fraction` on
every input tested. It is left failing rather than tuned away, because a check tuned until it
returns 0 is unfalsifiable.

## The one thing to read before using any number here

`(n−1)/3` is **not** the disjunctive per-slot value. It is exact at `n = 3, 4, 5` — reproduced
here independently, with dual certificates — and **`a7_family.py` beats it at every `n` from 6
to 12** with an explicit measure whose feasibility is checked by substitution. Its `≥`
direction is sound at every `n` tested (`a5`, `n = 3..20`); its `≤` direction is false from
`n = 6`, which `mg-200d` itself declared unproven at the claim.
