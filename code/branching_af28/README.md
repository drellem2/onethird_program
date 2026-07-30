# `code/branching_af28` — does this construction meet the branching-graph programme?

Instruments for **mg-af28**, supporting
`docs/OneThird-Branching-Graphs-Where-This-Lives.md`.

Run: `./run_all.sh` — pure Python 3, no dependencies, about 6 minutes.
`scan_brown.py` is the only step that needs network (it downloads
`arXiv:math/0006145`); if the download fails it says so and exits 0, and nothing
else depends on it.

Shares no code with `code/landscape_ebd8/`, `code/landscape_repair_1953/`,
`code/landscape_audit_d673/`, `code/semigroup_note/`, `code/unified_gate_8fd1/`
or any other instrument in the repo. Posets are carried as tuples of up-set
bitmasks, moves as tuples of block bitmasks; every object is rebuilt from its
definition and the enumeration is certified against A000112, A000110, A000670
and the hook length formula in `selftest.py`.

| file | what it does |
|---|---|
| `core_af28.py` | posets, order ideals, linear extensions, moves (both definitions), the product, `AC(P)`, cell posets `D_λ`, sub-shapes, hook length formula, the Young–Fibonacci lattice, exact rank over ℚ |
| `t_young.py` | **T0** moves = chains in `J(P)`; **T1** `J(D_λ) = [∅,λ]` and maximal chains = SYT(λ); **T2** how many posets are shape posets — **straight** (`J(P) = [∅,λ]`) *and* **skew** (`J(P) = [μ,λ]`), corrected by mg-41aa; **T6** no non-identity invertible move |
| `t_branching.py` | **T3** Stanley's differential condition, with Young's lattice and Young–Fibonacci as positive controls; **T7** Bergeron–Li's tower axiom (2); **T8** which branching graphs are distributive lattices |
| `t_lrb_reps.py` | **T5** `dim kF(P)/rad = |AC(P)|` from the trace form |
| `scan_brown.py` | keyword census of Brown (2000), with present-word controls |
| `selftest.py` | 31 assertions covering every number in the document |

**Three design points worth knowing before reading the outputs.**

*The controls are load-bearing and two of them fired.* T3 runs Young's lattice
and the Young–Fibonacci lattice through the same code path as `J(P)`; the first
version of the Young–Fibonacci cover rule **failed** the control, which is how
the wrong cover rule was found and replaced with the published one. `scan_brown`
scored its own control `left regular band` as 0 occurrences on the first run,
because Brown hyphenates it — the control caught the scanner, not the paper.

*Nothing is capped silently.* `t_lrb_reps.py` has a size cap on `|F(P)|` (exact
rank over ℚ of a `|F| × |F|` matrix); every class over the cap is listed
individually in the output with its size. T2's skew column is enumerated here for
`n ≤ 6` only and its `n = 7, 8` entries are marked `*` and attributed to the two
instruments that computed them — this file's canonical form is a min over all `n!`
relabellings, which cannot afford that enumeration.

*One test in this directory was CORRECTED rather than added to.* T2 used to assert
that the posets `P` with `J(P)` an interval of Young's lattice are *exactly* the
cell posets, and measured only the cell posets. mg-6ad0's audit refuted the
"exactly" by construction (the 2-element antichain), and mg-41aa fixed it here:
T2 now names both classes, measures both, prints the witness, and the corrected
numbers are 62/318, 149/2 045, 360/16 999 against the straight 6, 8, 12, which are
reproduced unchanged. See `docs/OneThird-Branching-Graphs-Repair.md` and
`code/branching_repair_41aa/`.
