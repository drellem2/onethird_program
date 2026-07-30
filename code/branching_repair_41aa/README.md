# `code/branching_repair_41aa` — the repair of mg-af28 under mg-6ad0's audit

Instruments for **mg-41aa**, landing four findings of
`docs/OneThird-Audit-mg-af28-Branching-Graphs.md` into
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` and into
`code/branching_af28/`. The reasoning is in
`docs/OneThird-Branching-Graphs-Repair.md`.

Run: `./run_all.sh` — pure Python 3, no dependencies, about 4 minutes, of which
`r1b_skew8.py` is 3. `r3_rescope.py` is the only step needing network (it
downloads `arXiv:math/0612170`); if the download fails it says so and exits 0,
and nothing else depends on it.

Shares no code with `code/branching_af28/`, `code/branching_audit_6ad0/`, or any
other instrument in the repo. Posets are carried as tuples of **down**-set
bitmasks (af28 uses up-sets, 6ad0 uses frozensets) and enumerated by **deciding
each pair** — for every `i < j`, one of *i below j* / *j below i* /
*incomparable*, with transitivity pruned at each step and **no induction on `n`**
(af28 adjoins a maximal element, 6ad0 enumerates natural labellings). The
canonical form is necessarily the same *idea* in all three — minimise an encoding
over relabellings — but this one refines colours first, which it must, because
this repair canonicalises objects the other two never touch. Certified against
A000112, A000041, the hook length formula, `Σ_λ (f^λ)² = n!`, the Fibonacci rank
sizes, `DU − UD = I`, Birkhoff's representation theorem as an equality, and M3
and N5, in `selftest41aa.py` (36 assertions).

| file | what it does |
|---|---|
| `kern41aa.py` | posets, order ideals, `J(P)`, canonical form, explicit isomorphism search, partitions, straight and skew cell posets, intervals of Young's lattice from containment, the grid as a product of chains, lattice/distributivity, join-irreducibles, Young–Fibonacci |
| `r1_exactly.py` | **X1.** The test ledger B2's *"exactly"* never got: for all 405 poset classes to `n ≤ 6`, is `J(P)` an interval? — decided by **constructing** the isomorphism and checking it on every pair; the converse tested exhaustively to `n ≤ 5`; the corrected fractions; a box-growth control on the enumeration |
| `r1b_skew8.py` | the `n = 8` entry, on its own because it takes ~3 min |
| `r2_grid.py` | **X2.** Brown's `§4.3` example lattice, built as a product of chains, **is** the interval `[(q), (q+p, q)]` — 25 pairs, each map verified; plus what af28's stated reason does and does not establish |
| `r3_rescope.py` | **X3** Bergeron–Li §3.1 and §3.6 re-read on a third PDF extractor, ligature-aware. **X4** Young–Fibonacci rebuilt, T8's 33/5 reproduced, and the 28 distributive intervals each rebuilt as a `J(P)` |
| `check_doc.py` | reads the repaired document off disk and checks, per finding, that the correction is present **and** that the struck sentence survives only inside the block quote that strikes it |
| `selftest41aa.py` | 36 assertions |

**Three design points worth knowing before reading the outputs.**

*The negative half of `check_doc.py` is the load-bearing half.* A repair that
adds a correction beside a false sentence and leaves the false sentence in force
has not repaired anything. Every struck string is required to occur **exactly
once** and on lines that all begin with `>`.

*Nothing is capped silently.* `r1_exactly.py` decides the "exactly" exhaustively
to `n ≤ 6` in the forward direction and to `n ≤ 5` in the converse; `n = 7` and
`n = 8` are counts only, and the reason the converse stops at 5 is printed with
the sizes involved. `code/branching_af28/t_young.py`'s T2 prints its `n = 7, 8`
skew counts marked `*` with the two instruments that produced them.

*The `n = 8` number is computed, not copied.* `run_all.sh` reads it out of
`out_r1b_skew8.txt` and feeds it to `r1_exactly.py`; no file in this directory
hard-codes 360. `code/branching_af28/t_young.py` does cite it, marked and
attributed, because that file's `n!` canonical form cannot afford to compute it.
