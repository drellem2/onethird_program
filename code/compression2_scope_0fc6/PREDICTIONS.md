# `mg-0fc6` — predictions for SCOPING `compression2.tex`, with the exposure disclosed rather than laundered

Filed before `lib0fc6.py` or any arm exists — **but not before I had read the note and worked
through it on paper.** The repo's standard (`mg-b417`, `mg-a0d6`, and every compression-arc
ticket) is that a prediction filed after the fact is a report, and that saying so is worth more
than the appearance of a bet.

## Exposure

- **H1 — I READ `docs/imports/compression2.tex` IN FULL FIRST.** The ticket orders exactly that
  ("Read `docs/imports/compression2.tex` and scope it"), so there is no version of this ticket
  in which the note is unread when predictions are filed. Everything below that is a claim
  *about the note's own text* is a **REPORT at zero credit**.
- **H2 — I RE-DERIVED THE ENTROPY LEMMA (5) BY HAND BEFORE WRITING ANY CODE,** including the
  centre-of-mass step, the Cauchy–Schwarz constant `2m(4m²−1)/12`, and the Pinsker step, and I
  checked `inv(W) = Σ_t d_t` by hand on `CA`, `AC`, `ACCA`. **P1, P2, P3 are REPORTS OF A
  PAPER DERIVATION**, not bets. What the arms add for them is machine confirmation on a real
  population, which is worth having and is not a prediction.
- **H3 — I read `STATE.md:21`, `STATE.md:29`, `STATE.md:158`, `docs/FACTS.md` §F18, and the
  `mg-8d66` / `mg-145f` / `mg-409a` commit bodies before filing.** So P6's *identification* of
  the note's hypothesis with the corpus's `M_n(η)` is a report of a reading. What is live in P6
  is only the numerical pricing.
- **H4 — the ticket's addendum tells me Daniel's stated target is REALIZABILITY and instructs me
  NOT to apply `mg-8d66`/`mg-145f` by analogy.** An agent under that instruction has an
  incentive to manufacture a positive verdict in order to look like it obeyed. The guard I can
  offer is P5: I predict the note is **realizability-blind**, which is a NEGATIVE answer to the
  question the addendum is most hopeful about, reached by a route (`STATE.md:21`, pair-bias
  closure at equality) that is **not** either of the two tickets I was told not to quote.
- **H5 — I derived the `n = 3` maximum-entropy tilt by hand** (`w = (√12−2)/4`, `H = 2.344`
  bits, `H / log₂ 3! = 0.907`) before writing P7. The `n = 3` value is a report; `n ≥ 4` is live,
  and at `n = 3` all three pair constraints coincided by symmetry, which is exactly the
  degeneracy that makes `n = 3` uninformative about the trend.

## Predictions

| # | claim | p | status when filed |
|---|---|---|---|
| **P1** | the merge-word encoding `L ↔ (W_B)` is a **bijection** on `L(P)` — the note's "compression" **forgets nothing** | 0.99 | **report** (paper) |
| **P2** | `inv_{L*}(L) = Σ_B K_B` **exactly**, and `K_B = Σ_{t=1}^{2m−1} d_t(W_B)` **exactly** — identities (2) and (3) hold as written | 0.98 | **report** (paper) |
| **P3** | the entropy lemma (5) is **correct as stated**, both inequalities, with the elementary constant `1 − 1/(24 ln 2) = 0.93989` | 0.95 | **report** (paper) |
| **P4** | identity (8) holds **exactly**: one BK swap changes **exactly one** `W_B` and changes it by **one adjacent `AC↔CA`** | 0.90 | live |
| **P5** | **the whole argument is REALIZABILITY-BLIND**: every step uses `P` only through the pair marginals `Pr[v_j <_L v_i]`, so it holds verbatim for measures on `S_n` that are **not** any poset's linear-extension measure — i.e. it injects **no** realizability fact and cannot separate a poset from a frozen measure | 0.90 | live |
| **P6** | the note's hypothesis (1) **is** membership in the corpus's pair-bias information set `M_n(0)` (`STATE.md:21`), so the closure that bites is `Op-Form` Claim 6.1 / `mg-6bc2` Claim 3.1 — **not** `mg-8d66` and **not** `mg-145f` | 0.85 | live |
| **P7** | the bound is **true but not sharp** on `M_n`: `max{H(μ) : μ ∈ M_n(0)} / log₂ n!` lands **strictly between 0.60 and 0.94** at `n = 4,5,6,7`, and the explicit mixture `μ = (2/3)·Unif(S_n) + (1/3)·δ_{L*}` is within `0.15` of the optimum | 0.65 | live |
| **P8** | **headline (6) is NUMERICALLY VACUOUS** at every `n` any object in this corpus reaches: `0.9399·n log₂ n ≥ log₂ n!` — i.e. weaker than the free bound `e(P) ≤ n!` — for all `n` below a crossover I predict lies in `[10⁶, 10⁸]` | 0.80 | live |
| **P9** | the scale partition of BK edges is **NOT** an admissible `k`-foliation in `mg-8d66`'s sense — its fibers are **not cubes** — so `mg-8d66`'s ceiling does **not** apply to it verbatim, and saying it does would be the error the ticket warns against | 0.85 | live |
| **P10** | the family the note actually produces is **NESTED** (a filtration `F_0 ⊂ F_1 ⊂ …`), not transverse like `compression.tex`'s `C_o`/`C_e`; so `Var` decomposes **exactly** by scale, and Daniel's convex-combination step is **sound and canonical** on this family (a multiplier) while being **not a projection** on `compression.tex`'s | 0.75 | live |
| **P11** | `compression.tex` and `compression2.tex` contain **two different families**, not one — the first genuinely forgets (a quotient), the second does not (a bijection) — so "combine them in convex combinations" is **not type-correct as stated** without first choosing which object is being combined | 0.70 | live |

## Named conditions under which I would report `engages-realizability`

Filed in advance so a verdict cannot be assembled after the fact.

1. Any step of the note whose validity **fails** for some measure `μ ∈ M_n(0)` that is not a
   linear-extension measure — i.e. any place `P`'s order relation is consumed beyond the
   marginals.
2. Any quantity the note bounds whose value **separates** the linear-extension measures inside
   `M_n(0)` from the rest — measured, not argued.
3. Any dependence of the dyadic tree on `P` that is **not** a dependence on `L*` alone.
4. A conclusion that is **false** for some frozen measure and **true** for every poset in the
   same information set.

If any of these fires, P5 loses and the note is the first realizability lever this programme has
had. I expect none of them to fire.

## Errors I expect to be able to make here

- **E1 — reading "different construction" as "unpriced".** The note is not `compression.tex`'s
  variant, which the ticket is right to insist on; that does **not** mean the corpus is silent
  about it. `STATE.md:21`'s pair-bias closure is indexed by the **information consumed**, not by
  the construction, and it is the citation that survives a change of construction.
- **E2 — the mirror error, quoting `mg-8d66`/`mg-145f` at a target they do not share.** The
  ticket names this one explicitly. The main body of `compression2` lands on `log e(P)`, a
  counting quantity; those two tickets closed a **spectral** route. They are silent about the
  main body and must be cited only against the note's **closing paragraph**, which does aim back
  at the spectral problem.
- **E3 — confusing "the bound is true" with "the bound is useful".** (6) and (7) can be, and I
  predict are, simultaneously correct and numerically empty at every reachable `n`.
- **E4 — treating the merge coordinates as a product.** They are not: `(W_B)` ranges over the
  legal tuples only, and legality is where `P` re-enters. Any multiscale argument that assumes
  independence across scales is wrong for that reason, and it is the reason I would look at
  first if the note is pursued.
- **E5 — over-reading `H(μ) ≤ 0.94 n log₂ n` as progress toward `E[inv_e]`.** The implication
  the note proves runs **inversions ⟹ entropy**; `STATE.md:158`'s untried slot wants
  **entropy ⟹ inversions**. Those are different directions across the same named bridge.
