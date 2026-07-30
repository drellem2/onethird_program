# `code/species_7d75` — the instrument for mg-7d75

Supports `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`.

```
./run_all.sh        # ~46 s, pure Python 3, no dependencies, NO NETWORK
```

Committed outputs: `out_selftest.txt` (759 assertions), `out_t1_grading.txt`,
`out_t2_operation.txt`, `out_t3_bidigare.txt`, `out_t4_one_operation.txt`,
`out_t5_hopf_monoid.txt`, `out_t6_fock_and_record.txt`.

Every `t*` script ends with a `TOTAL BAD` line. All six are `0`.

## What each file does

| file | what it decides |
|---|---|
| `kern7d75.py` | posets, set partitions, set compositions, the Tits product, `F(P)`, `AC(P)` by two routes, orbits, exact linear algebra |
| `hopf7d75.py` | the Hopf-monoid layer: Aguiar–Mahajan's poset / set-composition / set-partition (co)products on an arbitrary finite ground set, and the two candidate subspecies |
| `t1_grading.py` | **the grading falsifier, run first.** `|Π[n]| = Bell(n)`; `Π[n]/S_n` = integer partitions, `p(n)` of them; `p(n)` = #conjugacy classes of `S_n`; `AC(antichain) = Π[n]` **as sets** |
| `t2_operation.py` | `Φ : kF(P) → k^{AC(P)}` is a surjective algebra map with nilpotent kernel, so `kF(P)/rad = k^{AC(P)}` — a fresh re-anchor of mg-af28 B5 / mg-6ad0 A4a, with no trace form and no citation |
| `t3_bidigare.py` | **Bidigare's theorem built from both definitions and compared structure constant by structure constant.** Four candidate identifications are run; two hold, two fail |
| `t4_one_operation.py` | `(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}` on every poset class to `n ≤ 5`, and both of Daniel's instances read off that one table |
| `t5_hopf_monoid.py` | the bimonoid axioms of Aguiar–Mahajan, checked exhaustively on the ground set `[4]` for both candidate subspecies, with four controls |
| `t6_fock_and_record.py` | the two Fock functors; the Bell(n)/p(n) resolution; the correction to mg-af28's Bergeron–Li negative; the failed candidate map to `Sym` |

## Independence

Written fresh for this ticket. It shares no code with `core_af28.py`,
`kern6ad0.py` or `core1953.py`. Where it recomputes an object those files also
build, it builds it from the geometric definition and cross-checks two routes
against each other inside `selftest.py`.

## Conventions that have bitten this repo before

* `AC(P)` here is the **support semilattice of `F(P)`** = the set partitions of
  `[n]` whose quotient digraph is **acyclic**. It is **not** the set of flats
  meeting the **open** cone; that smaller set additionally requires every block
  to be an antichain, and conflating the two is the error mg-1953 repaired
  (R1). Nothing in this directory uses the smaller set.
* Faces multiply by the **Tits product** (refine the first by the second). The
  Hopf monoid of set compositions multiplies by **concatenation**. These are
  different maps and `t5` control (ii) measures how differently: 1 442 closure
  failures, 252 associativity failures, 11 020 compatibility failures.

## Size exemptions, each listed in the output it belongs to

* `t2` caps `|F(P)| ≤ 80`; 24 of 63 classes at `n = 5` are skipped.
* `t4` caps `dim (kF(P))^{Aut(P)} ≤ 90` for the nilpotency step only; 4 of 63
  classes at `n = 5` are skipped there and tested for everything else.
* `t3` runs to `n ≤ 5`. `n = 6` needs `4683² ≈ 21.9 M` face products and was not
  run.
* `t5` is exhaustive on the ground set `[4]` (4 399 basis elements of `F`,
  2 685 of `AC`) and not beyond.
