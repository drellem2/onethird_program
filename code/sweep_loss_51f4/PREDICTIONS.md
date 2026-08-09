# `mg-51f4` — PREDICTIONS

**Committed before one line of `lib51f4.py` exists.** The ticket asks what the Cheeger
sweep *loses* as a function of `n`, and whether that loss can be bounded uniformly. It
forbids attacking `(M♯)` alone or `(F)` alone. Everything below is written against the pair.

---

## H — EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

This is large and I am not going to pretend otherwise.

* **H1.** My ticket body prints `mg-28ff`'s entire finding: the two route formulae verbatim,
  the four-row table `c_true / c♯ / f*` at `n = 3..6` to three decimals, the increments, the
  "6 % and 19 % headroom", and the diagnosis sentence *"what degrades is the Cheeger sweep"*.
  **Every reproduction of any of those numbers is a `[FORMALITY]`, not a bet**, and is tagged
  as such wherever it appears.
* **H2.** I read `docs/OneThird-L2-Conditionality-mg-28ff.md` **in full** (all 507 lines) and
  `code/l2_conditionality_28ff/lib28ff.py` **in full** (541 lines) before writing this file.
  So I know `Φ*_pref`, `Δ_P`, `μ_pref`, `λ_std`, the `ψ` basis, the pencil closed forms, the
  `sweep_bound_sq` convention, and the exact-PSD device. Nothing about the *definitions* is a
  discovery, and my instrument is not "clean-room" in the sense of not having read the parent
  — it is clean-room only in the sense of sharing no source line and computing the transport
  by a **different algorithm** (down-set DP, not permutation enumeration), which is what makes
  the cross-checks in §C non-vacuous.
* **H3.** I have **not** read `lib76b2.py`, `libA94.py`, `mg-94c3`'s or `mg-9461`'s documents,
  and I did not open any `out_*.txt` of `mg-28ff`.
* **H4.** The one thing below that is genuinely mine and predates any computation is the
  **floor** in P1. I derived it on paper while reading the parent, before creating this
  directory. It is tagged `[DERIVED PRE-RUN]`, which is weaker than "predicted" and stronger
  than "found by the instrument", and I want the distinction on the record.

---

## THE OBJECTS I AM ABOUT TO DEFINE (fixed here so I cannot redefine them to win)

For a poset `P` on `{0..n-1}` with the identity a linear extension, write
`γ = 1 − λ_std`, `m_k = min(k, n−k)`, `A_k = {0..k−1}`, and

* **the prefix-conductance profile** `φ_k = Φ_P(A_k) = leak(A_k)/m_k`, `k = 1..n−1`;
* `Φ*_pref = min_k φ_k`, `Φ^max_pref = max_k φ_k`, **spread** `= Φ^max_pref/Φ*_pref`;
* `M = Σ_k leak(A_k) / Σ_k m_k` — the `m`-weighted **mean** of the profile
  (`= E[D_F]/(2⌊n²/4⌋)`, i.e. exactly route (F)'s bound);
* `c_true(P) = Φ*_pref² / (2γ)`, `c♯(P) = sweep(μ_pref, Δ_P)/(2γ)`, `f*(P) = M²/(2γ)`,
  where `sweep(r,Δ) = r(2Δ−r)` if `r ≤ Δ` else `Δ²`;
* **the sweep's loss** `Λ_M(P) = c♯(P)/c_true(P)` and **the mediant loss**
  `Λ_F(P) = M/Φ*_pref`, so `f*(P) = Λ_F(P)²·c_true(P)`;
* **the disjunction constant** `c_or(n) = max_P min(c♯(P), f*(P))` over primitive `P`.
  `min` is legitimate because (M♯) and (F) are each *separately sufficient* for
  `C₃^(III) = 1` at that poset (`mg-28ff` §2, §3) — the theorem needs one route to fire,
  not both. **This is the object the ticket's "do not attack one route" instruction points
  at, and it is the object I will report.**

---

## P — PREDICTIONS

| | bet | p |
|---|---|---|
| **P1** | **`[DERIVED PRE-RUN]` THE FLOOR.** For **every** poset, `c♯(P) ≥ Δ_P − γ/2`. *Proof sketch, fixed here:* `μ_pref ≥ γ` because the monotone cone sits inside `1^⊥`; `t ↦ t(2Δ−t)` increases on `[0,Δ]`; so `sweep(μ_pref,Δ_P) ≥ γ(2Δ_P−γ)` in the first branch, and in the second branch `Δ²/(2γ) ≥ Δ − γ/2 ⟺ (Δ−γ)² ≥ 0`. Divide by `2γ`. **Machine-checked exactly at every poset `n ≤ 6`, 0 exceptions.** | 0.90 |
| **P2** | **PRINCIPAL LIVE BET — THE FLOOR IS WHAT IS RISING.** `max_P (Δ_P − γ/2)` over primitive `P` at `n = 6` is `≥ 0.90`, i.e. it accounts for `≥ 95 %` of `c♯(6) = 0.943`. If it does, **no choice of monotone test vector can lower `c♯`**, the rise is not a defect of the sweep's *analysis*, and every "find a better vector" repair of (M♯) is dead in advance. **Guard bound now:** I must print `max_P(Δ_P − γ/2)` at every `n`, and its value *at `c♯`'s own argmax*, before scoring. | 0.55 |
| **P3** | Route (F) has **no** comparable floor: its structural floor `ρ_n²γ/2` (with `ρ_n = (n²−1)/(6⌊n²/4⌋) → 2/3`, from `leak(A_k) ≥ γk(n−k)/n`) stays `≤ 0.25` at every `n ≤ 7`. So the two routes' degradations are **not** the same object, and the ticket's premise of a single common degrading factor is **wrong** — which I would be filing as a finding, not as a licence to attack one route. | 0.65 |
| **P4** | **The two routes fail in OPPOSITE regimes.** `c♯` degrades as `γ → 0` (P1's floor → `Δ_P`); `f*` degrades as `γ` grows. Concretely: at `n = 6` the argmax of `c♯` and the argmax of `f*` are **different posets**, and the poset maximising each has `min(c♯,f*)` well under both maxima. | 0.50 |
| **P5** | **The disjunction is much better than either route.** `c_or(6) = max_P min(c♯,f*) < 0.80` — strictly below `f*(6) = 0.812`, hence below both published constants. | 0.45 |
| **P6** | …but `c_or(n)` is **still rising** at every step `n = 3..6`. (I want to lose this one.) | 0.60 |
| **P7** | **An explicit infinite family kills (F).** The *near-ordinal sum* — two antichains `A`, `B` of size `n/2` with every relation `a < b` present **except one pair** — has `γ → 0` while `M` stays bounded away from `0`, so `f* = M²/(2γ) → ∞`. Scored only on exact values at `n = 6..16`, and the family is a **FAMILY**, never a maximum. | 0.60 |
| **P8** | The same family also kills (M♯): `c♯ > 1` at some `n ≤ 16`. | 0.30 |
| **P9** | **No family I test kills the disjunction:** `min(c♯,f*) ≤ 1` at every member of every family tested to `n = 16`. Losing this is the strongest negative available to this ticket and I would report it as the headline. | 0.40 |
| **P10** | **The ticket's question is malformed in a specific and fixable way, and I will say so.** "Can the sweep's loss be bounded uniformly?" — **No, and it does not need to be.** `Λ_M = c♯/c_true` is *unbounded* over posets, because `c_true(P) → 0` along families where `Φ*_pref` is linear rather than square-root in `γ`, while `c♯` is floored by P1. The quantity that must be bounded is the **product** `Λ_M·c_true = c♯`, not the loss. Scored by exhibiting a family with `Λ_M ≥ 10` at `n ≤ 16` while `c♯ ≤ 1` there. | 0.75 |
| **P11** | `n = 7` **exhaustive** (all naturally-labelled posets on `[7]`) is reachable inside this ticket for the disjunction certificate, replacing `mg-28ff`'s 40–200-poset sample with a maximum. | 0.50 |
| **P12** | `[FORMALITY]` — my independent instrument reproduces `c_true(6) = 0.327508`, `f*(6) = 0.811654`, `c♯(6) = 0.943151`, `4377` primitive, `3340` L2-failing. Pre-answered by H1; a control on my instrument, not a bet. | — |

---

## E — MY OWN ERRORS, FILED IN ADVANCE, WITH THE GUARD FOR EACH

* **E1 — I publish a maximum over a FAMILY as a maximum over `n`.** This is the exact defect
  the ticket names twice and the one this lineage has now committed three times.
  **Guard:** every number from a named family carries the word **FAMILY** in its own row, and
  every number from a sample carries **SAMPLE — NOT A MAXIMUM**, at each appearance.
* **E2 — I let one of `mg-28ff`'s `n = 7` numbers travel without "sample".**
  **Guard:** I do not quote any `n = 7` number of `mg-28ff`'s at all. If I have an `n = 7`
  number it is my own and exhaustive, or it is not printed.
* **E3 — my floor is vacuous, or true for a reason that makes it uninformative.**
  A floor of `Δ_P − γ/2` is worthless if it is negative, or if it is far below `c♯`
  everywhere. **Guard, both directions:** (a) report the floor's *slack* `c♯ − (Δ_P−γ/2)`
  and its minimum over the population — the claim in P2 is that this is *small at the
  argmax*, and if it is large everywhere P2 loses; (b) a **mutation control**: the floor with
  the sign flipped, `Δ_P + γ/2`, must FAIL somewhere, or my checking code cannot discriminate.
* **E4 — I read "different regimes" off a correlation and not off the mechanism.**
  **Guard:** report `(γ, Δ_P, M, Φ*_pref, c♯, f*)` at both argmaxes explicitly, and exhibit
  a poset where `c♯ > f*` and one where `f* > c♯`, rather than only a correlation coefficient.
* **E5 — my exact definiteness test disagrees with the parent's and I do not notice.**
  I intend a Sylvester/Bareiss leading-minor test on the `(n−1)×(n−1)` pencil, which is a
  different device from `mg-28ff`'s Faddeev–LeVerrier on the `n×n` Laplacian.
  **Guard:** agreement of the two on **every** poset `n ≤ 5` and on `≥ 200` at `n = 6`, at
  several rational thresholds, plus a forced-disagreement negative control.
* **E6 — I treat `min(c♯,f*)` as free when it is not.** (F) is a statement about **primitive**
  posets (`mg-28ff` §3, `1−λ_std = 0` on decomposables). **Guard:** the disjunction is
  reported over primitive posets only, and that scope is in the same sentence as the number.
* **E7 — I attack one route and call it the sweep.** The ticket's central instruction.
  **Guard:** no table in the output may carry `c♯` without `f*` beside it, and the headline
  claim must be a statement about the pair or about the instrument they share.
* **E8 — I re-derive what `mg-28ff` already established** and spend the ticket reproducing it.
  **Guard:** the two routes and the L2-free theorem are taken as read; my `[FORMALITY]`
  reproductions exist only as controls on my own instrument and get one table, not a section.
* **E9 — the down-set DP is wrong in a way no small-`n` check sees.** `mg-9461`'s `s0` records
  exactly this failure mode (a predicate right at every small `n` and wrong in its state
  count). **Guard:** the DP transport is asserted equal to the permutation-enumeration
  transport at **every** poset `n ≤ 5` and a sample at `n = 6,7`, *and* the down-set count is
  asserted `≤ 2^n` with a mutation test that inflates it.

---

*`mg-51f4`. Written before `lib51f4.py` existed; `git log` for this file is the proof.*
