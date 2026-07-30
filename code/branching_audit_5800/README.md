# `code/branching_audit_5800/` — mg-5800's instrument

Independent audit of **mg-41aa / `504ab6c`** (the repair of mg-af28 under
mg-6ad0's audit). Reasoning and verdict: `docs/OneThird-Audit-mg-41aa-Repair.md`.

`./run_all.sh` — pure Python 3, no dependencies, ~4 minutes.
`a6_quotes.py` downloads `arXiv:math/0612170`; if that fails it prints
`NOT RUN` and the audit reports X3 as **unverified**, not as verified.

## What is here

| file | what it does |
|---|---|
| `kern5800.py` | posets as up-set bitmasks; canonical form by individualisation-refinement; unlabelled enumeration by **adding a maximal element**; ideal lattices; skew shapes as row intervals; **intervals of Young's lattice built directly from partitions**; the Young–Fibonacci lattice from its down-cover rule |
| `selftest5800.py` | 38 assertions against facts taken from **outside** this arc: A000112, A000041, the hook length formula, `Σ (f^λ)² = n!`, Fibonacci rank sizes, `DU − UD = I`, M3 and N5, Birkhoff on hand cases, and canon-invariance under random relabelling |
| `a1_counts.py` | the corrected fractions re-enumerated to `n = 8`; the straight column; the `n ≤ 3` claim; box-growth control at **every** `n` |
| `a2_exactly.py` | the "exactly", both directions, **without Birkhoff**, to `n = 6` |
| `a3_grid.py` | X2's grid from three separate definitions, plus the negatives that survive around it |
| `a4_yf.py` | Young–Fibonacci 33 / 5 / 28, the witness, the 28 reconstructions, and the **new claim** the repair derives |
| `a5_b1b5.py` | B1 as a **lattice** isomorphism; B5 with **no trace form and no cited theorem** |
| `a6_quotes.py` | the four Bergeron–Li strings, on a **fourth** PDF extractor |
| `a7_doc.py` | both documents read off disk; the struck sentences; the beyond-brief diff |

## Independence

`kern5800.py` imports nothing from `branching_af28/`, `branching_audit_6ad0/`
or `branching_repair_41aa/`, and none of them imports anything from here.
Every object is rebuilt from its definition. Two places where that matters:

* **the converse of X1.** mg-41aa's own §7 names this as its weakest link: its
  lattice-level converse stops at `n ≤ 5` and `n = 6` is carried by Birkhoff.
  Here the interval `[μ, λ]` is built as *the set of partitions `ν` with
  `μ ⊆ ν ⊆ λ` under containment* — no cell poset, no `J`, no join-irreducible
  anywhere — and compared with `J(P)` **as a lattice**. So `n = 6` is a
  measurement here, not a theorem applied.
* **the box bound.** Run at every `n` to 8, and cross-checked at `n ≤ 5`
  against a sweep over every raw `(μ, λ)` pair in an `(n+2) × (n+2)` box with
  no row- or column-trimming at all (102 060 pairs at `n = 5`).

## Two controls that FIRED, and are recorded because they fired

1. **`canon` had a label-dependent tie-break.** It chose its target colour
   class by dict-insertion order, which is a function of the labelling, so the
   minimum over the search tree was not a canonical form: two isomorphic
   20-element distributive lattices came out with different codes. **A000112
   to `n = 8` passed while that bug was live** — 1, 2, 5, 16, 63, 318, 2045,
   16999 exactly. Counting sequences are not a control on canonicity;
   random relabelling is, and it is now assertion 10 of the self-test.
2. **The Young–Fibonacci cover rule was wrong on the first coding** — "prepend
   a 1, or change the leftmost 1 to a 2" — and it reproduced the **Fibonacci
   rank sizes** `1,1,2,3,5,8,13,21` exactly. What caught it was `DU − UD = I`
   as an operator identity. Rank sizes are not a control on the neighbour
   rule. The published rule is: `u` is covered by `w` iff `u` is `w` with the
   leftmost 1 deleted, or with a 2 **strictly left of the leftmost 1** replaced
   by a 1.

Both are this instrument's own bugs, not mg-41aa's. They are here because the
same two controls are cited in this arc as evidence, and neither would have
caught what it appears to certify.
