# `code/growth_rate_00a1/` — the true growth of the disjunctive per-slot value (`mg-00a1`)

Document: [`docs/OneThird-GrowthRate-mg-00a1.md`](../../docs/OneThird-GrowthRate-mg-00a1.md)
Predictions: [`PREDICTIONS.md`](PREDICTIONS.md), committed at `f4d50a2` **before any script here
existed**. Outcomes: [`OUTCOMES.md`](OUTCOMES.md).

Parent: `mg-131e` (`b7b6941`), which refuted `ε_spec = 2/(n+1)` at `n = 6` and named this
question as its own successor, deliberately unanswered. Grandparent: `mg-200d` (`762921d`).
`mg-200d`'s formulation and its row builder `lp200d.build` are **used, not re-derived** — a
growth rate for a re-derived row set would be a growth rate for a different question.

## The one-line result

**The disjunctive per-slot value is `Θ(n²)`, not `c·n + O(1)`. Daniel's route is DEAD, not
re-based** — there is no constant `c` to put in place of `1/3`, because the value does not have
that shape. Secondarily: **`mg-200d`'s `Θ(n²) → Θ(n)` headline is REFUTED**; per-slot adjacency
symmetry buys a constant factor of at most `6`, not an order.

```
n(n+5)/36   ≤   max over branches   ≤   n(n−1)/6
```

Left side: an explicit measure, in closed form, at every `n` (`s1`). Right side: `mg-131e`'s
trivial dual, a theorem at every `n`. Both quadratic.

## Files

| file | what it is |
|---|---|
| `lib00a1.py` | the branch/poset bookkeeping, direct column generation, **the explicit witness**, and `verify_measure` — the arithmetic verifier with no simplex in its path |
| `selftest00a1.py` | 9 control groups, **5 of them mutations**. **Exits 1 on any failure.** |
| `s1_witness.py` | **THE VERDICT.** The witness at `n = 4..24`, every property re-derived by direct `Fraction` arithmetic. **No LP anywhere in this script.** |
| `s2_optimality.py` | exact LP: the controls (`mg-200d` and `mg-131e` both reproduce here), and the witness is **optimal on its branch** at `n = 6,8,10,12` |
| `s3_deadends.py` | the transitive-closure reduction checked on all `64` branches at `n=4` and all `1024` at `n=5`; the two natural quadratic families (two chains, bands) shown **INFEASIBLE** |
| `s4_search.py` | provenance: the greedy hill-climb that found the family, in exact rationals, plus a local-maximality check |

## Running

```
python3 selftest00a1.py             # controls; exit 1 on failure.  ~1 min
python3 s1_witness.py 24            # THE VERDICT.  Seconds.  Uses NO LP at all.
python3 s2_optimality.py 12         # controls + optimality.  ~1 min (n=14 is much longer)
python3 s3_deadends.py              # the reduction and the dead ends.  ~15 min
python3 s4_search.py 10             # provenance.  ~15 min (the n=10 hill-climb dominates)
```

Committed transcripts: `out_selftest00a1.txt`, `out_s1_witness.txt`, `out_s2_optimality.txt`,
`out_s3_deadends.txt`, `out_s4_search.txt`.

## The one thing to read before using any number here

There are **two** kinds of object in this directory and they are not interchangeable.

* **The witness** (`s1`) is a **LOWER** bound. It is an explicit measure whose mass, flip
  probabilities, per-slot symmetry and comparable-pair behaviour are all recomputed from the
  measure by direct `Fraction` arithmetic through `mg-200d`'s own `measure_report`. **No
  simplex appears in that path**, so no bug in any solver — mine or `mg-200d`'s — can make it
  wrong. Each row is a lower bound **on a NAMED branch**, so the true maximum at that `n` may be
  larger (`mg-131e`'s warning 2, kept). *A larger maximum leaves a superlinear verdict standing
  and would destroy a linear one*, which is why the verdict is stated from below.

* **The LP values** (`s2`, `s3`, `s4`) are **branch values** computed by `mg-200d`'s exact
  simplex. They are used for controls, for showing the witness is optimal on its branch, and
  for the infeasibility results. They are not what the verdict rests on.

`s1`'s numbers do **not** depend on `s2` being right. `s2` existing does not make `s1`'s numbers
upper bounds. The exhaustive `n = 6` value is not computed and is not claimed.

## What this does NOT show

The disjunctive value is an **upper bound** on the frozen-poset object. Showing that upper
bound is **larger** than believed *weakens the bound* and says nothing whatever about the
statement underneath. **The frozen-poset conjecture and `(LIB)` are exactly where `mg-131e` left
them.** What is dead is this route as a wall-breaker, not the wall. See the document's §5.2,
which lists five things that must not be read as killed.
