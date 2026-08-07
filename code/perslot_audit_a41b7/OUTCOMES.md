# `mg-41b7` — outcomes against `PREDICTIONS.md`

Predictions committed at **`3c5ed10`**, before one byte of `code/perslot_symmetry_200d/`, the
`mg-200d` document, or `STATE.md` was read. Nothing below edits a prediction; refuted ones are
scored and kept as written. Full reasoning:
[`docs/OneThird-PerSlot-AdjacencySymmetry-mg-41b7-IndependentAudit.md`](../../docs/OneThird-PerSlot-AdjacencySymmetry-mg-41b7-IndependentAudit.md).

## Hand measurements (§0 of `PREDICTIONS.md`)

| # | claim | outcome |
|---|---|---|
| H9 | the LITERAL per-slot system forces the uniform measure at `n=3`, so it is infeasible against the `1/3` cap | **HELD, and generalises.** Infeasible at `n = 3,4,5`, phase-1 residual `1/3` at each. `a1_forms.py` |
| H10 | the AGGREGATE form is also infeasible at `n=3` once `E[inv]=1` is demanded — so my brief's "excludes NOTHING" is false | **HELD, and UNDERSTATED.** The aggregate polytope is **entirely empty** at `n = 3,4,5` (residuals `1/3`, `1/5`, `1/6`), not merely unable to reach the optimum |
| H11 | `mg-200d`'s number in the parent's currency is `(n−1)/3` against `C(n,2)/3`, a ratio of exactly `2/n` | **HELD** — arithmetic, and confirmed against the reproduced LP values |

## Predictions

| # | outcome | note |
|---|---|---|
| P1 | **HELD**, with a note | exact `Fraction` on every decision path; one **latent** `eps_spec(n, int) -> float` that is shown not to bite at any live call site |
| P2 | **HELD** | the reported value is not from the literal form — that polytope is empty |
| P3 | **HELD** | `mg-200d` reports the infeasibility itself (§2), and its own pre-filed `H4` predicted it |
| P4 | **HELD** | the weakening is disjunctive: a maximum over `2^C(n,2)` comparable/incomparable branches |
| P5 | **[REPRO] HELD** | `E[inv] = 2/3, 1, 4/3` at `n = 3,4,5` reproduced exhaustively on my own solver, each with a verified **dual certificate**. A reproduction, not a hit — the numbers were in my dispatch prompt (H2) |
| P6 | **HELD** | no poset is enumerated on the path to any number |
| P7 | **HELD on existence, MISSED on direction** | the sizing sentence exists in the ticket's own currency and names its condition. I predicted the correction runs **pessimistic**; it runs **optimistic** — a smaller `ε_spec` is a *nearer* threshold. I had the inequality backwards |
| P8 | **HELD** | `(n−1)/3` is marked a **conjecture at the claim**, with the `≥`/`≤` split stated at the same volume as the result. `mg-200d` does **not** commit this lineage's most repeated error |
| P9 | **HELD** | my brief's item-2 premise is false, and traces to `mg-6bc2`'s pre-`mg-ba78` figure of `0` aggregate violations measured on a sub-probability measure — already struck to `2 of 3`, and already corrected by `mg-200d` at its §8.1 |
| P10 | **REFUTED, AND IT IS THE FINDING** | I predicted I would **fail** to beat the bound. `E[inv] = 11/6 > 5/3` at `n = 6` on a six-atom measure verified by substitution and dual-certified, and a **family** beating `(n−1)/3` by `1/6` at every `n` from 6 to 12 |
| P11 | **HELD** | every optimum is exhibited by an explicit measure and re-checked by substitution, never left as a solver value |
| P12 | **did not fire** | there is no defect of `mg-200d` to classify: the statement refuted at §6 is one it had itself marked unproven |
| P13 | **guard bound, and it FIRED — against my own code** | see defect 3 |
| P14 | **guard bound, and LOAD-BEARING** | `NC1` distinguishes infeasible / optimum-0 / nonzero in all four arms, and caught defect 1, which was a **false infeasibility** in my own solver |

**Score: 10 held, 1 refuted (and the refutation is the finding), 1 half-missed, 1 did not fire.
Both pre-filed errors fired, and both fired against me rather than against `mg-200d`.**

## Defects of this instrument, kept in the source

Four of the five were caught by my own controls **firing against correct code**.

1. **The simplex entered on the wrong sign of the reduced cost** — the maximisation rule inside
   a minimisation routine. The textbook LP returned `0` instead of `36`, and an
   equality-constrained LP returned **`infeasible`, phase-1 residual `1`**. A sign slip
   producing a *false infeasibility* is exactly `P14`'s hazard, committed in my own solver and
   caught by `selftesta41b7.py` before any audit number existed.
2. **A selftest expected `20` where the answer is `17`** (`max x+2y` s.t. `x+y ≤ 10`, `x ≥ 3`).
   My negative control failed against a **correct** solver, whose dual then verified at `17`.
   Corrected at the call site with the reason, not quietly retuned.
3. **My row builders emitted vacuous `0 = 0` rows**, so `a4_rowcheck.py` reported **214 of 219**
   branches as DIFFER against a row system that was in fact **identical**. The guard fired
   against my own code; `mg-200d`'s rows were right. Trusting the guard's first verdict would
   have produced a false finding about the single most load-bearing check in my brief.
4. **`a6_instrument.py`'s M4 asserted the `slot_le` surrogate for the two-atom law** — a measure
   outside the hypothesis the surrogate is claimed on — and failed against correct code. That is
   the same shape of error this arc keeps recording, committed by the auditor sent to check for
   it. Re-pointed at `uniform L(P)`, with the wrong version documented where it was made.
5. **`a5_construction.py` first called `L.perms(20)`**, i.e. tried to materialise `S_20`. It
   produced **no output at all** for forty minutes rather than raising — indistinguishable from
   a slow correct run. Replaced by a sparse reporter that never materialises `S_n`.
