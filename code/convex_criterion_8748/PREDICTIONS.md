# mg-8748 — PREDICTIONS, filed before one line of the instrument exists

**What this ticket is.** `mg-0fc6`'s scope document recommended, in so many words, that `a4.3b`
be kept **out of** its own `SCOPE: low` verdict: *"The filtration/multiplier distinction is a
small, true, reusable fact about which convex combinations are canonical, and it is orthogonal
to whether this note's route works."* This ticket is that keeping. It builds nothing new for the
programme; it makes a **selection criterion** findable, and it measures the criterion at a scope
`a4.3b` did not reach (`a4.3b` is **one poset**: the `n = 4` antichain, 3 levels, 5 random `f`).

**THE EXPOSURE, DISCLOSED RATHER THAN LAUNDERED.** Before writing this file I did the operator
algebra on paper, because the ticket's own statement of the fact needed checking before it could
be filed. Two of the statements below are therefore **REPORTS of a paper derivation at zero
credit**, marked `R`, and they are the two that matter most. Filing them as predictions would be
the laundering this corpus's pre-registration convention exists to stop. The **live** bets are
`P3`–`P8`, and two of them (`P4`, `P5`) are bets **against the way the fact is currently
written down**, including in this ticket's own body.

---

## R1 · REPORT, zero credit — a convex combination of two projections is a projection iff they are EQUAL

For orthogonal projections `A`, `B` and `t ∈ (0,1)`, `M = tA + (1−t)B` satisfies `M² = M` iff
`AB + BA = A + B`. Compressing that by `A·(−)·A` gives `ABA = A`, hence for unit `x ∈ Ran A`,
`‖BAx‖ = ‖Ax‖`, hence `Ran A ⊆ Ran B`; symmetrically `Ran B ⊆ Ran A`; so `A = B`.

**Why it is filed at zero credit and filed anyway.** It says something the ticket body does not:
**nestedness is NOT what makes "combine them in convex combinations" work, because that step
fails on the nested family too.** What nestedness buys is a *different* object — the increments.
The criterion has to be stated on increments or it is false in Daniel's own words.

## R2 · REPORT, zero credit — the increment `B − A` is a projection iff `Ran A ⊆ Ran B`

`(B−A)² = B + A − AB − BA`, so `(B−A)² = B − A` iff `AB + BA = 2A`; compress by `A` to get
`ABA = A`, i.e. `Ran A ⊆ Ran B`. The converse is immediate. **So nestedness is exactly — an
`iff`, not an implication — the property that makes increments exist.** That is the criterion,
and it is sharper than the `FP` measurement `a4.3b` recorded for it.

---

## The live bets

| | claim | `p` |
|---|---|---|
| **P3** | The **cheap** route and the **expensive** route to nestedness agree everywhere tested: `partition_a refines partition_b` ⟺ `Π_a Π_b = Π_b Π_a = Π_a`, 0 disagreements. The criterion is checkable **without building a matrix**, which is the whole claim that it is cheap. | 0.85 |
| **P4** | **`a4.3a`'s measurement does not establish what it is quoted for.** `(Π_o+Π_e)/2` non-idempotent at 40 of 40 posets is implied by `Π_o ≠ Π_e` **alone** (R1) and is therefore evidence of *distinctness*, not of *transversality*. Nothing in `mg-0fc6` measured transversality. I predict the pair **is** transverse at a large majority of posets — but that the number has never been taken. | 0.75 |
| **P5** | **And "transverse" is not a uniform property of `(C_o, C_e)`.** At `n ≤ 5` there exist posets where the two foliations are **nested and distinct** — one genuinely refines the other — so the criterion has to be applied per poset and the phrase *"`compression.tex`'s transverse pair"* is a statement about the typical case, not about the family. | 0.60 |
| **P6** | The `iff` of R2 holds with **0 exceptions** over **all ordered pairs of set partitions of a 5-element space** (`52² = 2704` pairs), and the non-vacuity count — pairs where the increment is *not* a projection — is a **majority** of them. | 0.80 |
| **P7** | On `compression2`'s scales the variance identity `Var(f) = Σ_l ‖D_l f‖²` holds **exactly, in rationals, at every poset measured at `n = 4, 6, 8`** and not only at the `n = 4` antichain `a4.3b` used — and it holds for **structured** `f` (`inv_e`, position statistics), not only random `f`. | 0.90 |
| **P8** | The **second** half of the fast filter separates: the `a2.3` two-measure exhibit, re-derived on an implementation that shares no code with `mg-0fc6`'s, calls `compression2`'s own input **blind** and calls a planted support-reading construction **not blind**. A filter that returned "blind" for everything would be worthless and this is the control that says it does not. | 0.80 |

**What would make me withdraw the criterion rather than file it.** Stated in advance: if the
partition route and the operator route disagree anywhere (`P3` fails), the "cheap check" claim is
gone and only the expensive one survives; if the variance identity needs a hypothesis beyond
nestedness (`P7` fails), the fact is smaller than advertised and the entry must say so.

---

## Errors this remedy could exhibit, being an artifact of the same kind as the defect

The defect being repaired is **a true fact archived inside a dead verdict, quotable away from its
scope**. A registry entry is exactly such an artifact, so:

- **E1 — writing the criterion in Daniel's words rather than in the true ones.** *"Convex
  combinations of nested compressions are canonical"* is FALSE as stated (R1). The entry must say
  **increments**, and it must say so in the STATEMENT and not only in a caveat.
- **E2 — dropping `mg-0fc6`'s honest scoping in retelling.** The ticket names this explicitly.
  The variance identity is **Pythagoras and holds for any filtration**; the content is
  **nestedness**, which for `compression2` is by construction of the dyadic tree. That sentence
  travels verbatim or the entry is a promotion.
- **E3 — quoting `a4.3b`'s scope as though it were the scope of the general fact.** `a4.3b` is one
  poset. The general fact is proved; the measurements are corroboration and must be reported with
  their own populations.
- **E4 — claiming the criterion is a result.** It is a **selection criterion for future
  constructions**. It closes nothing, consumes nothing, and supplies **no realizability fact** —
  `STATE.md:21` is untouched by it. An entry that reads as progress is a worse defect than no
  entry, because this corpus's whole discipline is that a fact carries its own weight and no more.
- **E5 — a `FACTS.md` entry whose SCOPE line is unwritable.** If I cannot say which populations,
  exhaustive or sampled, to which `n`, with the caps, the entry is not ready
  (`docs/FACTS.md` Housekeeping) and the fix is to measure, not to soften.
- **E6 — re-measuring `mg-0fc6` instead of citing it.** `a4.1`, `a4.2`, `a2.1`–`a2.2`, and the
  whole `SCOPE: low` verdict are **cited, not re-derived**. What is re-derived here is only what
  is being *extended*: the nestedness, the increments, and the two-measure exhibit.
