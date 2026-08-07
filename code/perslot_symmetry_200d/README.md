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
| `selftest200d.py` | 60+ controls incl. real-poset checks (`S3`,`S5`,`S6`), a mutation (`S7`), solver-invariance (`S8`) and `eps_spec` exactness (`S9`). **Exits 1 on any failure.** |
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

## `eps_spec` exactness — a HARDENING, not a defect repair (`mg-a1fe`)

`mg-41b7`'s differential audit of `measure_report` passed it 111 of 113 and classified the
remaining 2 as a **hardening note, not a defect**: `eps_spec` computed `6*e_inv/(n^2-1)`
with no conversion, so **a plain Python `int` for `e_inv` returned a `float`**. It did not
bite — `measure_report` accumulates `E_inv` from `F(0)`, so it is a `Fraction` on integer
weights, zero weights and the empty measure, and all three live call sites
(`v1_forms`/`v2_disjunctive` here, `dual_certificate_131e`, `dual_certificate_audit_eaa1`)
pass a `Fraction`. That made the guard a **convention held by every caller, not a property
of the function** — and in a corpus whose results are exact rationals compared for
**equality**, a float does not announce itself.

Repaired with one `F()` on the argument, and guarded by **`S9`** in `selftest200d.py`.
`S9` is a real control, verified in both directions: it **fails 5 of its 9 checks against
the pre-repair `lp200d.py`** (the three int-type checks, plus `eps_spec(4, 1) == 2/5`,
where the float path is a genuinely *different number* because `2/5` is not dyadic) and
passes all 9 after. `S9d` is a mutation that runs the pre-repair expression inline, so the
control cannot go vacuous. `S9g` records what the `F()` does **not** buy: it makes the
return *type* a property of the function; it does not launder a float **argument** back
into the rational the caller meant.

Scope, stated so it is not over-read: `mg-200d`'s conclusions are **unchanged and remain
refuted** (`mg-00a1`, `mg-131e`) — this touches the instrument only, and no published
figure moves. `mg-41b7`'s two checks in `a6_instrument.py` now pass **for the right
reason** (its full run: 113 PASS / 0 FAIL against the repaired file), rather than by being
tuned away. One neighbour checked and found **clean**, reported rather than swept: the
only other arithmetic in `lp200d.py` that could import a float is the simplex, and
`solve_max` already coerces every coefficient (`F(v)`), every rhs (`F(rhs)`) and every
objective entry (`-F(v)`) before they reach the tableau — `eps_spec` was the single
unconverted boundary in the file.

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
