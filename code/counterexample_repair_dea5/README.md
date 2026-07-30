# `counterexample_repair_dea5` — the instrument for the mg-dea5 repair

Produces every number in `docs/OneThird-Counterexample-Under-The-Action-Repair.md` and every figure the
repair writes into `docs/OneThird-Counterexample-Under-The-Action.md`.

```
./run_all.sh          # ~7 minutes, pure Python 3, no dependencies
```

**Independence.** Imports nothing from `code/counterexample_probe_24a3/` (the target) or
`code/counterexample_audit_a7b4/` (the audit) and shares no code with either. Every object is rebuilt from its
definition in exact integer / rational arithmetic; no floats are used anywhere a comparison depends on one.

**Routes deliberately not the target's.**

* `e(P|_S)` for *every* subset in one `O(2ⁿ n)` pass, from `e(S) = Σ_{x minimal in P|_S} e(S − x)`.
* `p(x,y) = e(P ∪ {x<y}) / e(P)` on the transitively closed augmentation.
* Isomorph rejection by an explicit canonical labelling (colour refinement, then branch-and-bound over the
  colour-compatible relabellings of an incrementally comparable encoding), checked against brute force over
  all `n!` relabellings at `n ≤ 5` and against A000112 **and** A001035.
* Multiplicities by the factorisation `m_X = Π_{B ∈ X} M(P|_B)` rather than by inverting the level lattice.
  This is what brings `n = 8` — 16,999 isomorphism classes — into range; the Lemma and its proof are at the
  top of `levels.py`, and control C7 checks it against the lattice inversion on every level at `n ≤ 5`.
* The spectrum via `trace(Mᵏ) = Σ_X m_X λ_Xᵏ` on the actual transition matrix, in exact rationals — no
  eigensolver.

**Randomness.** Seeded and reported: `SEED = 20260730` for the permutation tests, `SEED = 4242` (the target's
own seed) for the cycle search. Every output file reproduces byte-identically.

## Files

| file | what |
|---|---|
| `poset.py` | posets, exhaustive enumeration up to isomorphism, `e`, `p(x,y)`, `δ`, tie-freeness, `L*`, cycle detection |
| `levels.py` | levels, the multiplicativity Lemma, `qmass`, `qfrac` |
| `walk.py` | moves, the action, the transition matrix, `λ_X`, `s(x,y)`, `m_X`, power sums |
| `records.py` | per-poset records for `n = 3…8` and the §4 population |
| `section4.py` | **the re-measurement** → `out_section4.txt` |
| `theorem4.py` | Theorem 4 for every weight → `out_theorem4.txt` |
| `cycles.py` | majority cycles: exhaustive to `n = 8`, witnesses above → `out_cycles.txt` |
| `controls.py` | 12 positive controls and 4 negative controls that fire → `out_controls.txt` |

## Reading the output

`out_section4.txt` is the primary deliverable. Its §3 is the pre-specified test, its §4 is the
multiple-comparison position, its §5 is the powered test on the whole population, and its §5b is the
deflation — the separation inside those groups does not need `L*`. `out_controls.txt` should be read first:
if the four negative controls do not fire, nothing else in the directory is evidence of anything.
