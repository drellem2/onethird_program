# `mg-6ff4` — predictions for MEASURE THE BOUNDARY (`ε_spec` at `δ(P) = 1/3` exactly)

Filed before one line of `lib6ff4.py` or any arm exists. **But not before I had thought**, and this
repository's standard (`mg-b417`, `mg-a0d6`, `mg-7c78`) is that a prediction filed after the fact is
a report, and that saying so is worth more than the appearance of a bet. So the exposure first, in
full, because on this ticket the exposure is unusually large and hiding it would make a derivation
look like a measurement.

## Exposure — what I already knew when this file was written

- **H1 — I HAD ALREADY READ `mg-7c78`'s `a5` CENSUS IN FULL**, including the boundary counts
  `1, 2, 3, 5, 8, 12` at `n = 3…8`, `0` frozen posets, the width-`2` collapse, and the sentence
  *"30 of the 31 ARE ORDINAL SUMS. Exactly one is primitive."* Every prediction below that concerns
  the **shape** of the boundary class is therefore a **REPORT at zero credit**, not a bet.
- **H2 — I DERIVED THE CLOSED FORM ON PAPER BEFORE WRITING ANY CODE, AND IT ALREADY MATCHES THE
  PUBLISHED CENSUS.** Three steps, all elementary:
  1. `L(A ⊕ B) = L(A) × L(B)` and every incomparable pair lies inside one summand, so
     `δ(A ⊕ B) = max(δ(A), δ(B))` and `E[inv_e]` is **additive** over ordinal summands.
  2. Hence the whole boundary class is the ordinal sums whose non-chain summands are exactly the
     **primitive** posets with `δ ≤ 1/3`, and `mg-7c78` reports there is exactly **one** of those at
     `n ≤ 8`. It must be the 3-element `V` (`a < b`, `c` free), which is primitive and has
     `δ = 1/3`.
  3. So a boundary poset on `n` elements is `k ≥ 1` copies of `V` interleaved with `n − 3k`
     singletons, `C(n − 2k, k)` classes for each `k`. `Σ_k C(n−2k, k)` at `n = 3…8` is
     `1, 2, 3, 5, 8, 12` — **`a5`'s census exactly**.
  I also hand-computed the `V`: `L = {acb, abc, cab}`, `e = (a, c, b)`, `E[inv_e] = 2/3`,
  `ε_obs = 6·(2/3)/8 = 1/2`. **P1–P5 below are consequences of that derivation and are reports.**
- **H3 — I have read `mg-6bc2` §3** and therefore know `max{ 6E_μ[inv_e]/(n²−1) : μ ∈ M_n(0) } =
  n/(n+1)`, attained by the two-atom law, before predicting anything about the realizability gap.
  `P7` is scored at low credit for that reason.
- **H4 — the arithmetic of the crossing point is mine and was done on paper**, not measured: if the
  closed form is right the max at `n` is `4⌊n/3⌋/(n²−1) ≈ 4/(3n)`, which meets `ε_dem ≈ 2·10⁻²`
  near `n ≈ 67`. That is not a prediction about the world, it is division; what is live is whether
  the closed form survives an exhaustive `n = 9` and a width-restricted sweep above it.

**What is genuinely live**, and where I can actually be wrong: `P6`, `P8`, `P9`, `P10`, `P11`, `P12`,
`P13`. Everything else is bookkeeping on a derivation and is marked as such.

## Predictions

| # | claim | p | status when filed |
|---|---|---|---|
| **P1** | the boundary class is EXACTLY the ordinal sums of singletons and copies of the 3-element `V`, with `≥ 1` copy — `Σ_{k≥1} C(n−2k, k)` classes at each `n` | 0.95 | **report** (H2; matches `a5` at `n ≤ 8`) |
| **P2** | `ε_obs` on a boundary poset with `k` copies of `V` is **exactly** `4k/(n²−1)`, for every such poset, with **no dependence on where the copies sit** | 0.95 | **report** (H2, additivity) |
| **P3** | so the distribution at each `n` is supported on `⌊n/3⌋` values only, and `min = 4/(n²−1)`, `max = 4⌊n/3⌋/(n²−1)` | 0.93 | **report** (H2) |
| **P4** | the trend in `n` is **FALLING**, like `Θ(1/n)` at the max and `Θ(1/n²)` at the min | 0.93 | **report** (H2) |
| **P5** | `ε_obs = 1/2` at `n = 3`, the largest value anywhere in the class, and it EXCEEDS `ε_dem ≈ 2·10⁻²` by a factor `25` | 0.95 | **report** (hand-computed, H2) |
| **P6** | an **EXHAUSTIVE `n = 9`** sweep finds **no new primitive** boundary poset — the count is `Σ_k C(9−2k,k) = C(7,1) + C(5,2) = 7 + 10 = 17` | 0.80 | **live** — this is the one measurement the whole extrapolation rests on |
| **P7** | the realizability gap `n/(n+1) − max_P ε_obs(P)` is **increasing in `n` and tends to `1`**, and the **ratio** `(n/(n+1)) / max_P ε_obs` grows **linearly**, `≈ 3(n−1)/4` | 0.85 | half report (H3 gives the `n/(n+1)`), the ratio's growth live |
| **P8** | the weak-majority (`≥ 2/3`) tournament is **acyclic at every boundary poset**, so `e` is **unique and canonical**, and no tie-break is ever exercised — even though the *strict* `> 2/3` tournament is **NOT** total (the `V` has a pair at exactly `2/3`) | 0.85 | **live** (the second half is the interesting one and `a5` did not report it) |
| **P9** | over ALL `n!` reference orders, `ε` at a boundary poset spans a range **at least `6·(m/2)/(n²−1)`** wide — i.e. the choice of `e` moves the measurement by MORE than the whole measured value, so `P8` is load-bearing and not a formality | 0.75 | **live** |
| **P10** | at every boundary poset the mean flip probability over incomparable pairs is `q̄ = 1/3` **exactly** (both pairs of a `V` are at `1/3`… no: one is at `1/3` and one at `1/3`) — I predict `q̄ = 1/3` exactly at **every** member | 0.70 | **live** |
| **P11** | the incomparability density is `d = 2k/C(n,2) = Θ(1/n²)` and it, not `q̄`, is where the entire fall lives — the `mg-6bc2` identity `ε_spec = 3·d·q̄·n/(n+1)` reproduces every measured `ε_obs` exactly | 0.85 | live (the identity is H3; that `d` carries the fall is the bet) |
| **P12** | a width-`≤2`-restricted exhaustive sweep to `n ≥ 12` finds **no new primitive** boundary poset either | 0.80 | **live** |
| **P13** | **exactly one** boundary poset at each `n` is primitive… no — I predict **zero** primitive boundary posets at every `n ≥ 4`, the `n = 3` `V` being the only one in the entire class at any `n` reached | 0.80 | **live** |

## What would falsify the headline

A **new primitive poset with `δ ≤ 1/3`** at `n = 9` or above. That single object would break P1–P4,
P6, P12 and P13 at once, and it is the only thing that could — every other number here is a
consequence of the ordinal-sum algebra, which is proven. **If one appears, the closed form dies and
the trend argument dies with it**, and that is the correct outcome, because the trend argument is
exactly the claim that no such object exists.

## What no arm here can do

Measure the frozen class. `δ < 1/3` is the counterexample condition; the population is **empty at
every `n` any enumerator reaches**. Nothing below is a frozen-class number and nothing below may be
quoted as one — that is `STATE.md` row 3b's `0/132` error, and this programme has paid for it once.
