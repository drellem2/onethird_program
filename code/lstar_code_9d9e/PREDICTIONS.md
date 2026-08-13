# PREDICTIONS — `mg-9d9e`, written and committed BEFORE any arm exists

Pre-registration, in this corpus's standing convention (`mg-ba78`, `mg-6bc2`): **never edited
after the fact.** A refuted prediction stays as written, with the refutation beside it.

The ticket's instruction is one line — *build the `L*` code and measure its expected length
against `⌈log₂ n!⌉` at `n = 6…12`* — and the whole point of it is that a code answers by
construction. So these predictions are about what the run will say, not about what a proof
might.

---

**P1 — The exact-index reading of `compression2`'s merge tape is the free code, exactly.**
Encoding each node's merge word by its index among the `C(a+b, a)` words of that shape gives a
total codelength of **exactly `log₂ n!`** at every permutation, every poset and every `n`,
because the tape is a bijection `S_n → ∏(words)` and the binomials telescope. So it **ties**
`⌈log₂ n!⌉` and can never beat it. *Expected: CONFIRMED.*

**P2 — The fixed-width reading of the same tape LOSES at every `n ≥ 3`.** One bit per element
per level is `T(n) = T(⌈n/2⌉) + T(⌊n/2⌋) + n` bits, and `T(n) > ⌈log₂ n!⌉` at every `n ≥ 3`.
*Expected: CONFIRMED.*

**P3 — The `P`-conditioned merge code beats `⌈log₂ n!⌉` at every non-antichain poset and ties
exactly at the antichain.** Restricting each node's word to those consistent with `P` is still
a prefix code (Kraft `= 1` exactly) and is `O(n²)` to compute, so it reads `P` without
enumerating `L(P)`. *Expected: CONFIRMED.*

**P4 — On the `δ = 1/3` boundary family the test is passed by a margin that GROWS with `n`.**
The family is `⌊n/3⌋` ordinal-summed copies of `{a < b, c}`, `δ = 1/3` exactly. Its
`log₂ e(P) = ⌊n/3⌋·log₂ 3 ≈ 0.528·n` against a free bound of `n log₂ n − 1.443n`, so **every**
code that reads `P` at all wins, and its shape-A constant `E[len]/(n log₂ n)` tends to `0`.
*Expected: CONFIRMED — and if so, passing the test carries no information on this population.*

**P5 — The `L*`-free minimal-element code BEATS the `L*` merge code on the boundary family.**
Predicted per-block figures: `MINIMALS` `5/3 = 1.6667` bits, `MERGE-P` `2` bits, truth
`log₂ 3 = 1.5850`. If so, `L*` is not what is doing the work. *Expected: CONFIRMED.*

**P6 — No code beats the free bound at the antichain, and that is a theorem rather than a
search.** `e(antichain) = n!`, so `E[len] ≥ log₂ n!` for **every** code by Gibbs. Hence
`max_P E[len] ≥ log₂ n!` for every family of codes, and a shape-B constant `c < 1` valid at all
`P` is **impossible**. *Expected: CONFIRMED exhaustively at `n ≤ 5`.*

**P7 — The class the bound is about is EMPTY at every `n` the test can be run at.** Frozen
(`δ < 1/3`, non-chain) is empty at `n ≤ 5` on this directory's own enumerator, and the corpus
has it empty to `n = 8` and the conjecture verified to `n = 14`. So the ticket's *"at the `n`
you claim it"* names an `n` at which the population is empty. *Expected: CONFIRMED.*

**P8 — `0.9399·n log₂ n` starts to BITE and starts to NEED ITS HYPOTHESIS at the same `n`, and
it is the same number.** Below `mg-0fc6`'s `16,777,063` the bound is implied by the free bound;
above it the bound is FALSE at the antichain, so it is carried entirely by hypothesis (1)
there. There is no `n` at which the theorem is both non-vacuous and hypothesis-free.
*Expected: CONFIRMED.*

**P9 — The F24 multiplier passes Q1 and fails Q2.** Its scale-variance profile
`(‖D_l f‖²)_l` is non-constant on the realizable measures at `n = 4, 5` (resolution > 1 value,
so > 0 bits), and is not obtainable without the measure — hence without `L(P)`.
*Expected: CONFIRMED both halves.*

**P10 — The per-node conditional entropies on the boundary family are ZERO at every node whose
split falls on a block boundary.** So `compression2`'s per-node ceiling of `0.9399·(a+b)` bits
overpays by the whole node there. *Expected: CONFIRMED.*

---

**What would make this ticket's answer NO in the ticket's own sense** (recorded in advance so
it cannot be recognised after the fact): a code that reads `P` only through `L*` — i.e. only
through the pair marginals, the object `mg-0fc6` §2 showed the poset-dependence washes out to —
and still beats `⌈log₂ n!⌉` by a margin that does not vanish. P1 predicts the one such code on
record does not beat it at all.
