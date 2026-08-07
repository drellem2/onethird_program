# `code/perslot_symmetry_200d/` — what per-slot adjacency symmetry buys (`mg-200d`)

Document: [`docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md`](../../docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md)
Predictions: [`PREDICTIONS.md`](PREDICTIONS.md), committed at `b5784ee` **before any script here
existed**. Outcomes: [`OUTCOMES.md`](OUTCOMES.md).

Parent: `mg-6bc2`, read out of branch `polecat-a6bc2` (`90d19e7`) while it was unmerged; it
**landed on `main` as `e1f7bb2`** at 2026-08-07 18:21, content-identical (rebase only). **No code is shared with it** — the
simplex here is two-phase (it has to be: `Σ μ = 1` and the symmetry equalities cannot be
expressed in a form where the origin is feasible), and reproducing `mg-6bc2`'s theorem on it is
one of the controls (`S1`).

## Files

| file | what it is |
|---|---|
| `lp200d.py` | exact-rational two-phase simplex (Bland), the five constraint forms, diagnostics |
| `selftest200d.py` | 60+ controls incl. real-poset checks (`S3`,`S5`,`S6`), a mutation (`S7`) and solver-invariance (`S8`). **Exits 1 on any failure.** |
| `v1_forms.py` | the branch-free forms: baseline, both literal, both surrogate |
| `v2_disjunctive.py` | the disjunctive value: exhaustive over `2^C(n,2)` branches, plus the no-symmetry control |
| `v3_families.py` | lower-bound search past the brute-force horizon, and the `(n−1)/3` construction checked directly at `n = 3..20` |

## Running

```
python3 selftest200d.py                # controls; exit 1 on failure
python3 v1_forms.py 3 4 5              # branch-free forms  (n=6 is slow: 720 cols, 75 eq rows)
python3 v2_disjunctive.py 3 4 5        # exhaustive disjunctive value (n=5 is 1024 branches x3)
python3 v3_families.py 4 5 6           # lower-bound search + the construction
```

Committed transcripts: `out_selftest200d.txt`, `out_v1_n5.txt`, `out_v1_n6.txt`,
`out_v2_n34.txt`, `out_v2_n5.txt`, `out_v3_families.txt`.

## The one thing to read before using any number here

There are **five** symmetry forms and they are not interchangeable:

* **LITERAL** (`slot_eq`, `agg_eq`) — symmetry on *every* pair. **UNSOUND**: it holds for
  `uniform L(P)` only when `P` is an antichain, and no antichain is in `M_n`. Every value it
  produces is an upper bound for **nothing**. Computed only to be reported as empty.
* **SURROGATE** (`slot_le`, `agg_le`) — `J_k(y,x) ≤ J_k(x,y)`. Sound, branch-free, **buys zero**.
* **DISJUNCTIVE** — per pair, `q = 0` **or** symmetry. Sound, and the whole finding.

`build(n, form, comparable=…)` applies the form only to pairs **not** declared comparable, which
is what makes the disjunctive branches sound; passing `comparable=∅` recovers the literal form.

**Every value printed by `v3_families.py` is a LOWER bound on the disjunctive optimum.** It can
refute the `(n−1)/3` conjecture and can never confirm it, and each line says so.
