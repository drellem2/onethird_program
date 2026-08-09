# OneThird — **THE SWEEP'S LOSS IS UNBOUNDED AND THAT IS NOT THE PROBLEM.** `(M♯)` carries an exact **floor** `c♯(P) ≥ Δ_P − (1−λ_std)/2` that no test vector can beat; `(F)` carries no floor at all and loses through the **mediant**; and **BOTH ROUTES ARE FALSE AT `n = 7`, EXHAUSTIVELY AND EXACTLY** — `(F)` at 168 of 86278 primitive posets, `(M♯)` at exactly 4 — **at DISJOINT sets of posets**, so the object the theorem actually consumes, the **disjunction** `min(c♯, f*)`, survives at **86278 of 86278** with `c_or(7) = 0.894472`

**Work item:** `mg-51f4` — successor to `mg-28ff`, filed on its own recommendation.
**Scope taken:** the ticket's one load-bearing instruction — *file against the pair, not
against either route.* That instruction is why this document has a `c_or` column, and `c_or`
is the only thing in it that is still alive.

---

## §0. THE STATE AFTER THIS TICKET

| | status |
|---|---|
| **`(M♯)`** | **REFUTED.** False at exactly **4 of the 86278 primitive posets on `[7]`**, by exact copositivity brackets on `μ_pref`, and false at every member of a named family from `n = 13` on. |
| **`(F)`** | **REFUTED.** False at **168 of the 86278**, and at every member of a named family from `n = 7` on. Max `f*(7) = 1.297074`. |
| **The disjunction `min(c♯, f*)`** | **ALIVE, and it is the only survivor.** `c_or(7) = 0.894472`, exhaustive; **0 of 86278** posets kill both routes at once. Its increments are `+0.056, +0.245, +0.203, +0.141` — still rising, now decelerating. **Not extrapolated.** |
| **`C₃^(III) = 1` at `n ≤ 7`** | **STILL TRUE, and now on a fully enumerated `n = 7`.** `c_true(7) = 0.340719`, so the target holds with a factor of `2.94` to spare. |
| **`C₃^(III) = 1` uniformly in `n`** | **STILL OPEN, and now conditional on the DISJUNCTION rather than on either route.** L2 untouched. |
| **The `n` the architecture consumes** | `n ≥ 99`. **Nothing here reaches it.** Exhaustive to `n = 7`; ten named families to `n = 14`; every family number is labelled FAMILY. |

**The one-sentence version.** The ticket asked whether the sweep's loss can be bounded
uniformly; the answer is that it cannot and does not need to be — the loss `Λ_M = c♯/c_true`
reaches **1159** at a `14`-element poset while `c♯` there is `0.857` — and the two things that
actually decide the routes are a **floor** on one and a **mediant** on the other, which is why
they die at disjoint posets and why their disjunction is the object worth tracking.

**What may not be quoted without its scope.** `c_true = 0.340719`, `c♯ = 1.018707`,
`f* = 1.297074` and `c_or = 0.894472` are **maxima over the exhaustively enumerated primitive
posets on at most 7 elements**. They are not bounds in `n`. Every number attributed to a named
family carries the word **FAMILY** and is **not** a maximum over its `n`.

---

## §1. THE QUESTION WAS MALFORMED, AND THE MALFORMATION IS THE FIRST FINDING

The ticket says: *"WHAT DOES THE CHEEGER SWEEP LOSE, AS A FUNCTION OF `n`, AND CAN THAT LOSS
BE BOUNDED UNIFORMLY? A bound on the sweep's loss serves BOTH hypotheses at once."*

The premise is that the two routes share a degrading factor. **They do not, and the ticket's
filer has since said so unprompted** (`pm-onethird`, 2026-08-09T21:02Z: *"Route (F) has NO
Cheeger sweep in it at all … So the common factor I asserted was never established"*), as did
the independent audit of the parent (`mg-29fe`, 20:57Z). I reached the same conclusion from
the other end and had committed the algebra before either mail arrived — `PREDICTIONS.md` P1
and P3, commit `01c206f`, author date **20:24:09Z**, 33 minutes earlier. Three routes to the
same place is worth more than any of them alone, so the record is: **this was found
concurrently and independently, not handed to me.**

Define the loss precisely, so that "the sweep loses" stops being a slogan. With
`γ = 1 − λ_std`, `m_k = min(k, n−k)`, and the **prefix-conductance profile**
`φ_k = leak(A_k)/m_k`:

$$\Lambda_M(P)\;=\;\frac{c^{\sharp}(P)}{c_{\mathrm{true}}(P)}\;=\;\frac{\mu_{\mathrm{pref}}(2\Delta_P-\mu_{\mathrm{pref}})}{\Phi^{*2}_{\mathrm{pref}}},\qquad \Lambda_F(P)\;=\;\frac{M}{\Phi^{*}_{\mathrm{pref}}},\quad M=\frac{\sum_k \mathrm{leak}(A_k)}{\sum_k m_k},$$

so that `c♯ = Λ_M·c_true` and `f* = Λ_F²·c_true` **pointwise, by definition**. `Λ_M` is the
Cheeger sweep's loss — Cauchy–Schwarz, the degree rounding, and the cone price. `Λ_F` is the
**mediant** loss: the `m`-weighted *mean* of the profile over its *minimum*. There is no
Cauchy–Schwarz and no square root anywhere in route (F).

**Both are unbounded, and it does not matter.** Exhaustive maxima:

| `n` | primitive | `max Λ_M` | `max Λ_F` | `max φ_max/φ_min` |
|---|---|---|---|---|
| 3 | 4 | 3.750 | 1.500 | 2 |
| 4 | 27 | 20.000 | 3.500 | 6 |
| 5 | 275 | 30.372 | 5.000 | 10 |
| 6 | 4070 | 79.309 | 9.667 | 21 |
| 7 | **86278** | **110.967** | **13.083** | — |

and along the near-ordinal family `Λ_M` reaches **1159.3** at `n = 14` *while `c♯` there is
`0.8572`, comfortably under 1*. **A bound on the loss was never the thing to want**: the loss
grows exactly where `c_true` collapses, and only the product is consumed. What follows
replaces the question with the two that can be answered.

---

## §2. ROUTE `(M♯)` HAS A FLOOR, AND IT IS ONE LINE

> **THEOREM (the floor).** *For every poset `P` with `γ = 1−λ_std > 0`,*
> $$c^{\sharp}(P)\;\ge\;\Delta_P-\tfrac{\gamma}{2}.$$

**Proof.** `μ_pref ≥ γ`, because the monotone cone sits inside `1^⊥` and `γ` is the minimum of
the Rayleigh quotient over all of `1^⊥`. Write `q(t) = t² − 2Δ_P t + \mathrm{sweep}(μ_{pref},Δ_P)`.
In the branch `μ_pref ≤ Δ_P` the sweep is `μ(2Δ−μ)` and `q(t) = (t−μ)(t−(2Δ−μ))`, which is
`≥ 0` for every `t ≤ μ`, hence at `t = γ`. In the other branch the sweep is `Δ²` and
`q(t) = (t−Δ)² ≥ 0` outright. Either way `q(γ) ≥ 0`, and
`c♯ − (Δ_P − γ/2) = q(γ)/(2γ)`. ∎

**Machine check.** The theorem's *entire* content is `γ ≤ μ_pref`, so the check is **one exact
decision per poset** with no bracket and no float: `γ > μ_pref` must be FALSE.
**0 of 4377 primitive posets `n ≤ 6`** (`s1` S1.2). The mutation control — the floor with the
sign flipped, `Δ_P + γ/2` — is violated at **4377 of 4377**, so the check discriminates.

### 2.1 What the floor costs, quantitatively — and this is the part that kills the repairs

`Δ_P ≤ 1` always and `γ > 0`, so the floor never reaches `1` and the theorem never refutes
`(M♯)` by itself. What it does is **remove the repair everyone would try next**:

| `n` | `max c♯` | `max (Δ_P − γ/2)` | the floor **at `c♯`'s own argmax** | floor/`c♯` there | **median** floor/`c♯` |
|---|---|---|---|---|---|
| 3 | 0.500000 | 0.500000 | 0.500000 | 1.0000 | 1.0000 |
| 4 | 0.636846 | 0.636846 | 0.636846 | 1.0000 | 1.0000 |
| 5 | 0.803289 | 0.752421 | 0.733351 | 0.9129 | 0.9978 |
| 6 | 0.943151 | 0.825114 | 0.810428 | 0.8593 | 0.9937 |
| 7 | **1.018707** | **0.880249** | **0.854626** | **0.8389** | — |

At the *typical* poset the floor is **99.4 %** of `c♯` (`n = 6` median). At `c♯`'s own extremal
poset it is **83.9 %** at `n = 7`. So:

> **A better monotone test vector cannot save `(M♯)`.** Even a *perfect* one — attaining
> `μ_pref = γ`, which is exactly L2's first disjunct — leaves `c♯ = 0.854626` at the `n = 7`
> extremal poset. `g_sort`, `g_cone`, and every successor to them are competing for the
> remaining 16 %.

The complementary half is `mg-29fe`'s, derived concurrently: writing `ρ = μ_pref/γ ≥ 1`,
`c♯ = ρΔ_P − ρ²γ/2` identically, so `ρ = 1` forces `c♯ < 1` at every poset and every `n`, and
**the cone price `ρ` is the only channel through which `(M♯)` can fail.** `ρ` is *measured*
here, not inferred: `max ρ = 1.0000 / 1.0854 / 1.1412 / 1.2176 / 1.2762` at `n = 3..7`. At the
`n = 7` witness in §5, `ρ = 1.2213` and `1/Δ_P = 1.0556`, so `ρ > 1/Δ_P` exactly as the
algebra requires.

---

## §3. ROUTE `(F)` HAS NO FLOOR — ITS LOSS IS THE MEDIANT, AND THAT IS A DIFFERENT OBJECT

The centred indicator of `A_k` is a test vector, so `leak(A_k) ≥ γ·k(n−k)/n`, and summing,

$$M\;\ge\;\rho_n\gamma,\qquad \rho_n=\frac{n^2-1}{6\lfloor n^2/4\rfloor}\;\longrightarrow\;\tfrac23,
\qquad\text{hence}\qquad f^{*}\;\ge\;\tfrac12\rho_n^{2}\gamma .$$

That floor **vanishes with `γ`** instead of climbing toward 1. Exhaustively, `max` over
primitive posets of `(F)`'s floor is `0.222 / 0.195 / 0.222 / 0.210` at `n = 3..6` — flat, and
nowhere near the `0.5 → 0.880` of `(M♯)`'s.

**So the two routes do not share a degrading factor.** `(M♯)` is pinned from below by a
quantity that rises with `Δ_P`; `(F)` is not pinned at all, and everything it loses it loses
through `Λ_F = M/Φ*_pref` — how far the *average* prefix conductance sits above the *minimum*.

---

## §4. THE MEASUREMENT — EXHAUSTIVE TO `n = 7`

Population: **every** poset on `{0,…,n−1}` for which the identity is a linear extension.
`2 / 7 / 40 / 357 / 4824 / 96428` at `n = 2..7`; primitive `1 / 4 / 27 / 275 / 4070 / 86278`.
The `n ≤ 6` totals are `mg-28ff`'s `5230` and `4377` exactly, on an instrument that computes
the transport by a **down-set dynamic program** rather than by filtering `n!` permutations.

**`n = 7` IS ENUMERATED HERE, NOT SAMPLED.** `mg-28ff`'s `n = 7` figures are deterministic
samples of 40–200 posets, correctly labelled as such at every appearance in its document, and
**I do not quote any of them.** The size of the gap justifies the caution: its `n = 7` sample
reads `c_true = 0.176145`; the maximum over the enumerated population is **`0.340719`**, and
the sample was low by a factor of `1.93`.

| `n` | primitive | `c_true` (the truth) | `c♯` (route M♯) | `f*` (route F) | **`c_or` = max min** |
|---|---|---|---|---|---|
| 3 | 4 | 0.222222 | 0.500000 | 0.250000 | 0.250000 |
| 4 | 27 | 0.271353 | 0.636846 | 0.306250 | 0.306250 |
| 5 | 275 | 0.308339 | 0.803289 | 0.550747 | 0.550747 |
| 6 | 4070 | 0.327508 | 0.943151 | 0.811649 | 0.753639 |
| **7** | **86278** | **0.340719** | **1.018707** | **1.297074** | **0.894472** |

`c_true`'s increments are `+0.049, +0.037, +0.019, +0.013` — still shrinking at the new point,
so the phenomenon `mg-28ff` identified as stable is stable on a `21×` larger population.

*(One small disagreement recorded rather than smoothed: `mg-28ff` prints `f*(6) = 0.811654`;
I get `0.8116489` at the same poset, `M = 88/243`. Five significant figures agree and the
sixth does not. Too small to matter here, and not mine to adjudicate.)*

---

## §5. BOTH ROUTES ARE FALSE AT `n = 7` — EXACTLY, EXHAUSTIVELY, AT DISJOINT POSETS

> **`(F)` FAILS AT 168 OF 86278 PRIMITIVE POSETS ON `[7]`.**
> `(F)` reads `M² ≤ 2γ`, so it fails at `P` iff `γ < M²/2` — **one exact decision**, the
> negation of `γ ≥ M²/2`, settled by the signs of the principal minors of `Q − (M²/2)N`.
> No float appears in the verdict.
>
> **The extremal witness.** `A = {0,1,2}`, `B = {3,4,5,6}`, both antichains, every `a < b`
> present **except** `(2,3)` and `(0,6)`:
> `[(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(1,6),(2,3),(2,4),(2,5),(2,6)]`.
> 156 linear extensions, `Φ*_pref = 1/39`, `M = 157/468`, `M²/2 = 24649/438048 > γ`, so
> **`f* = 1.297074 > 1`**, with `c_true = 0.007578` — the truth is 130× under the target while
> the route is over it.

> **`(M♯)` FAILS AT EXACTLY 4 OF 86278.**
> Refuting `(M♯)` needs a **lower** bound on `μ_pref` — the direction `mg-28ff` §10 records as
> a float measurement, which is why the parent could report the trend and not the refutation.
> Here `μ_pref ≥ t` is decided as **copositivity of `Q − tN` over the monotone cone**, by exact
> KKT enumeration of the `2^{n−1}−1` faces of the simplex.
>
> **The count is exact in both directions.** The exhibited-vector `c♯` is an *upper* bound, so
> every poset with `c♯_upper ≤ 1` provably satisfies `(M♯)`; and at all 4 posets with
> `c♯_upper > 1` the exact bracket confirms genuine failure.
>
> **The extremal witness.**
> `[(0,1),(0,2),(0,3),(0,5),(0,6),(1,2),(1,3),(1,5),(1,6),(2,3),(2,6),(4,5),(4,6),(5,6)]`.
> 19 linear extensions, `Δ_P = 18/19`, profile `(5/19, 5/19, 5/19, 8/19, 7/19, 7/19)`,
> `μ_pref ∈ [0.226537524, 0.226537524]`, `sweep/2 = 0.188954871 > γ = 0.185485078`, so
> **`c♯ = 1.018707 > 1`**, with `ρ = 1.2213 > 1/Δ_P = 1.0556`.

> ### **AND BOTH FAIL AT 0 OF 86278.**

The two failure sets are disjoint, and not narrowly. This is `mg-28ff` §4.5's own
extrapolation — *"simple extrapolation of either puts it through 1 within a step or two of
`n = 7`"* — landing exactly where it said, for **both** routes, and now proved on the
population rather than projected from a trend.

---

## §6. THE DISJUNCTION IS THE OBJECT THE ARCHITECTURE CONSUMES

`(M♯)` and `(F)` are each **separately sufficient** for `C₃^(III) = 1` at a poset (`mg-28ff`
§2, §3). The theorem needs **one** route to fire there, not both. So the constant the
architecture actually consumes is

$$c_{\mathrm{or}}(n)\;=\;\max_{P\ \mathrm{primitive}}\ \min\bigl(c^{\sharp}(P),\,f^{*}(P)\bigr),$$

which had never been computed before this ticket. `0.250, 0.306, 0.551, 0.754, **0.894**` at
`n = 3..7`, exhaustive, primitive. At `n = 6` it is strictly below **both** published
constants; at `n = 7` it is below both by `0.12` and `0.40`.

**And the disjunction genuinely bites** — it is not a relabelling of one route. At `n ≤ 5`,
`f*` is the smaller at all 275 primitive posets and `c♯` at none, so there `min()` *is*
route (F); from `n = 6` on both arguments occur. (That fact came out of a control of mine that
**failed** — see §9.)

**The honest reading, and I am not going to dress it up.** `c_or` is rising: `+0.056, +0.245,
+0.203, +0.141`. The increments have turned over, which is the first encouraging thing in this
column, and **four points after a turnover is not a trend.** `c_or(7) = 0.894` leaves 10.6 %
of headroom, and the architecture consumes `n ≥ 99`. **I do not extrapolate it and neither
should anyone quoting it.**

---

## §7. WHY THE INTERSECTION IS EMPTY — A MECHANISM, NOT AN ACCIDENT OF `n = 7`

Binned by `γ` over all 86278 primitive posets at `n = 7`, **exhaustive**:

| `γ` bin | count | `max ρ = μ_pref/γ` | `max M/Φ*_pref` | `max c♯` | `max f*` | `max min` |
|---|---|---|---|---|---|---|
| `[0.00, 0.05)` | 354 | 1.0265 | **13.083** | 0.8418 | **1.2971** | 0.8418 |
| `[0.05, 0.10)` | 4451 | 1.0540 | 8.667 | 0.9010 | **1.2708** | 0.8945 |
| `[0.10, 0.20)` | 30936 | 1.2316 | 5.969 | **1.0187** | 0.8338 | 0.8041 |
| `[0.20, 0.30)` | 27405 | 1.2461 | 3.331 | 0.9990 | 0.5266 | 0.5266 |
| `[0.30, 0.50)` | 21532 | **1.2762** | 2.498 | 0.9499 | 0.4730 | 0.4730 |
| `[0.50, 1]` | 1600 | 1.2547 | 1.820 | 0.8234 | 0.3410 | 0.3410 |

**`(F)` exceeds 1 only at `γ < 0.1`. `(M♯)` exceeds 1 only at `γ ∈ [0.1, 0.3)`.** The cone
price `ρ` — the sole channel that can break `(M♯)` — **collapses toward 1 exactly in the
small-`γ` bins where `(F)`'s mediant loss explodes.** The same shape appears at `n = 6`
(`s1` S1.7), on a population `21×` smaller and computed independently.

The mechanism this suggests, **stated as a conjecture and not as a result**: a poset with a
very thin bottleneck has a Fiedler vector that *is* monotone — L2's first disjunct holds
there — which pins `c♯` to its floor `Δ_P − γ/2 < 1`; and a poset whose Fiedler vector is badly
non-monotone has a *fat* profile, which keeps `M/Φ*_pref` small. **Neither half is proved
here.** A proof of either would be the first uniform-in-`n` statement anyone in this lineage
has had, and it is the successor this ticket wants.

---

## §8. THE FAMILIES — THE FAILURES ARE NOT AN `n = 7` ARTEFACT

Every row below is a **FAMILY MEMBER**, never a maximum over its `n`.

| FAMILY | what it shows |
|---|---|
| **near-ordinal antichains** (two antichains, all `a<b` but one) | `f*` = `0.725, **1.227**, 1.764, 2.595, 3.476, 4.719, 6.026, 7.762, **9.577**` at `n = 6..14`. `(F)` fails **exactly** at every `n ≥ 7`. Here `μ_pref = γ` exactly, so `c♯ = Δ_P − γ/2` sits **on** its floor and rises to `0.857`. |
| **chain(`n−1`) + one isolated point** | `c♯` = `0.794, 0.850, 0.893, 0.928, 0.955, 0.978, 0.997, **1.013**, **1.027**` at `n = 6..14`. `(M♯)` fails, with an **exact** copositivity bracket, from `n = 13`. `f*` there is `0.17`, falling — route (F) covers it easily. |
| **bipartite ladder**, **near-ordinal (2 missing)** | same shape as the near-ordinal family; `(F)` fails from `n = 11` and `n = 8`. |
| **antichain**, **two interleaved chains** | both routes comfortable at every `n ≤ 14`; `min ≈ 0.20`. |
| **near-ordinal antichains + isolated point** (`s4`) | the one construction on which **both** constants rise together. `min(c♯,f*)` = `0.393, 0.415, 0.481, 0.497, 0.563, 0.576, 0.642` at `n = 8..14`, rising steadily, with **both** `c♯` (`0.841 → 0.979`) and `f*` (`0.393 → 0.642`) climbing together — the only construction where that happens. **It does not kill the disjunction at any `n` where I can certify: `(M♯)` provably HOLDS there at every `n ≤ 14`, by exact copositivity bracket.** Past `n = 15` I cannot certify `(M♯)`'s failure at all — see §9. |

Largest `min(c♯, f*)` at any family member tested: `0.858` (bipartite ladder, `n = 14`).
**Every one is under 1.** The disjunction has not died on anything tested.

---

## §9. TWO EPISTEMIC STATUSES, AND A CONTROL OF MINE THAT FAILED

**The direction that is a theorem at each poset.** `γ` brackets, `Φ*_pref`, `M`, `Δ_P`,
`c_true`, `f*` and every `(F)` verdict are exact rationals with every comparison decided
exactly. `(M♯)` verdicts are exact wherever the copositivity bracket was run: the `n = 7`
population and families to `n = 15`.

**The direction that is a MEASUREMENT, and where.** Elsewhere `c♯` is computed from an
**exhibited** monotone vector, so it bounds `μ_pref` — and hence `c♯` — from **above**. That
direction can certify that `(M♯)` *holds* and **can never certify that it fails**. Every table
that carries such a `c♯` says so at the top, and `s4`'s uncertifiable rows are printed as `n/a`
rather than `FAILS` for exactly this reason. Where both were run they agree to `10⁻⁹`.

**A control of mine that failed, and the failure is a finding.** `C4` asserts that
`min(c♯, f*)` is attained by *both* arguments somewhere, or the disjunction is a relabelling
of one route. Its first version asserted this at `n = 5` and **FAILED**: at all 275 primitive
posets on 5 elements `f*` is the smaller and `c♯` never is. That is a fact about the
population, not about the code — `(M♯)` does not begin to bind anywhere until `n = 6` — and the
arm now asserts both halves. Had I not filed E7's guard in advance I would have deleted it.

**Two more defects caught by arms filed in advance.** `A8`'s copositivity test **refuses** the
Horn matrix rather than guessing at it, which is the designed behaviour and is asserted.
And my first attempt at reproducing `mg-28ff`'s L2 census asked whether a *rationalised*
`μ_pref` landed inside a `2⁻⁴⁹`-wide bracket; it answered **53** where the established number
is **1037**. I did not publish a repair — the census is not this ticket's and is established
on two instruments already — I deleted the number and said so in `s1` S1.1. The quantitative
form of the same question, the cone price `ρ`, is measured throughout.

---

## §10. PREDICTIONS SCORED

`PREDICTIONS.md` was committed at `01c206f`, before one line of `lib51f4.py` existed.

| | bet | outcome |
|---|---|---|
| **P1** (0.90) | `[DERIVED PRE-RUN]` the floor `c♯ ≥ Δ_P − γ/2` | **HELD**, 0 exceptions at 4377 primitive posets, and it is §2. Derived and committed 33 min before `mg-29fe`'s independently derived `ρ = 1` column arrived; the two agree to six decimals. |
| **P2** (0.55) | **PRINCIPAL LIVE BET** — the floor is `≥ 0.90` at `n = 6`, i.e. `≥ 95 %` of `c♯` | **LOST on the number it named.** `max(Δ_P − γ/2) = 0.825114`, and at `c♯`'s own argmax the floor is `85.9 %` of `c♯`, not `95 %`. **The qualitative content held and then some**: the *median* ratio is `0.9937`, so at a typical poset the floor is essentially all of `c♯`, and the "better vector" repair is dead anyway. I put the guard in (`report the floor at c♯'s own argmax`) precisely so I could not move the goalposts, and it is what scores this a loss. |
| **P3** (0.65) | `(F)` has no comparable floor; the ticket's common-cause premise is wrong | **HELD**, §3. Independently confirmed by `mg-29fe` and conceded by the filer. |
| **P4** (0.50) | the two routes fail in **opposite regimes**; different argmaxes at `n = 6` | **HELD, and far more strongly than I bet.** Not merely different argmaxes: at `n = 6`, **0 of 4070** posets have both `c♯ > 0.8` and `f* > 0.8`; at `n = 7`, `(F)` exceeds 1 only at `γ < 0.1` and `(M♯)` only at `γ ∈ [0.1,0.3)`. |
| **P5** (0.45) | `c_or(6) < 0.80` | **HELD**: `0.753639`, below both published constants. |
| **P6** (0.60) | `c_or(n)` still rising at every step (the one I wanted to lose) | **HELD** — `0.250, 0.306, 0.551, 0.754, 0.894`. It is rising and I lost the thing I wanted. The increments have turned over, which is not the same as convergence and I do not claim it is. |
| **P7** (0.60) | an explicit infinite family kills `(F)`: near-ordinal antichains, `f* → ∞` | **HELD** exactly as constructed, `f*` reaching `9.58` at `n = 14`; and superseded by the stronger `n = 7` exhaustive result. |
| **P8** (0.30) | the same family also kills `(M♯)` | **LOST**, and instructively: on the near-ordinal family `μ_pref = γ` exactly, so `c♯` sits **on** its floor and can never reach 1. `(M♯)` needed a different family (chain+point) and a different regime. This is the sharpest single piece of evidence for P4. |
| **P9** (0.40) | no family I test kills the **disjunction** | **HELD** to `n = 14` on ten families and on the combined construction to every `n` where `(M♯)` can be certified, and confirmed exhaustively at `n = 7` (0 of 86278). |
| **P10** (0.75) | the ticket's question is malformed; the loss is unbounded and need not be bounded | **HELD**, §1: `Λ_M = 1159.3` at an `n = 14` family member with `c♯ = 0.857` there. |
| **P11** (0.50) | `n = 7` exhaustive is reachable inside this ticket | **HELD** — 96428 posets, ~28 min, streamed. |
| **P12** | `[FORMALITY]` reproduce `mg-28ff`'s constants and populations | reproduced: `5230 / 4377`, `1,4,27,275,4070`, `c_true(6) = 0.327508`, `c♯(6) = 0.943151`. `f*(6)` differs in the sixth figure (§4). |

**My principal live bet lost, and the two I would most have liked to lose — P6 and P8 — one
held and one lost.**

---

## §11. THE REPAIR SITES IN `mg-28ff`, NAMED — FILE, LINE, CURRENT WORDING, REPLACEMENT

`pm-onethird` asked for these explicitly, because `mg-28ff` is **landed**, so a superseded
`n = 7` figure is wrong on `main` right now. **I have edited nothing** — these are proposals
for whoever owns that document. All seven are in
`docs/OneThird-L2-Conditionality-mg-28ff.md`.

**Every one of `mg-28ff`'s `n = 7` figures was correctly labelled a sample at each
appearance.** None of these is a labelling failure. What the enumeration shows is that the
samples were *badly unrepresentative* — and at site 4 unrepresentative enough to invert a
universal claim.

| # | line | current | replacement | why |
|---|---|---|---|---|
| **1** | **247** | *"**100 % at every enumerated `n`, with no eigenvector on the left.**"* | *"100 % at every **exhaustively enumerated** `n ≤ 6`. **At `n = 7`, exhaustively, route (F) is FALSE at 168 of 86278 primitive posets** (`mg-51f4` §5); the `n = 7` row below is a 106-poset sample and does not support this sentence."* | **The most serious of the seven, and the only one that is a claim rather than a number.** The word *enumerated* sat over a table whose `n = 7` row was a sample, so the sentence reads as covering `n = 7` and is false there. |
| **2** | **245** | `\| 7 \| 106 *(sample)* \| 106 / 106 \| 0.832530 \|` | `\| 7 \| **86278 (EXHAUSTIVE)** \| **86110 / 86278** \| **1.297074** \|` | the sample certified 100 %; the population certifies 99.81 %, and the maximum is over 1 |
| **3** | **200** | `\| 7 \| 106 *(sample — NOT a maximum)* \| 0.176145 \| — \|` | `\| 7 \| **86278 (EXHAUSTIVE)** \| **0.340719** \| **+0.0132** \|` | the sample is low by a factor of **1.93**. The replacement *strengthens* `mg-28ff`'s own thesis: the increment `+0.0132` continues the shrinking sequence `.049, .037, .019`, so `c_true`'s convergence now has a fifth point |
| **4** | **217** | `\| 7 \| 40 *(sample)* \| 0.850074 \|` | `\| 7 \| **86278 (EXHAUSTIVE)** \| **1.018707** \|` | the 40-poset sample reads under 1; the population maximum is **over** 1, so `(M♯)` is refuted at `n = 7`, not "approaching failure" |
| **5** | **15–16, §0** | *"`C₃^(III) = 1` uniformly in `n` … **conditional on either of two scalar hypotheses**, (M♯) or (F)"* | *"… conditional on **the disjunction** of (M♯) and (F). **Both are individually FALSE from `n = 7`** (`mg-51f4` §5); their disjunction survives at 86278 of 86278 with `c_or(7) = 0.894472`."* | the two hypotheses are no longer open; what is open is `min(c♯, f*) ≤ 1` |
| **6** | **487–489, §10** | *"**(M♯) and (F) are both OPEN.** Verifying a hypothesis exhaustively on a finite population is not proving it"* | *"**(M♯) and (F) are both CLOSED — refuted** at `n = 7` (`mg-51f4` §5). The open hypothesis is their disjunction."* | |
| **7** | **377–383, §8** | the dependency diagram listing `(M♯)` and `(F)` as two independent sufficient conditions under `C₃ = 1` | keep both lines — they remain **pointwise** sufficient and that is what the diagram asserts — and add a third: `<= min(c#,f*) <= 1  [the disjunction; the only one still open]`, with a note that neither of the first two holds at every poset | |

**One further item, found by `mg-29fe` and recorded here because it belongs with the list.**
`mg-28ff` §2 and §4.2 state the hypothesis `(M♯)` in its **one-case** form `μ_pref(2Δ_P −
μ_pref) ≤ 2(1−λ_std)`, while the theorem above it carries **two** cases. Since `t(2Δ−t)`
decreases past `t = Δ`, the one-case form is the *weaker* requirement, so `(M♯)` as written
can hold where the theorem does not deliver `C₃ = 1`. **I measured how far it bites: exactly
5 of the 4377 primitive posets `n ≤ 6` have `μ_pref > Δ_P`, and they are the ANTICHAINS, one
per `n`.** Their `c♯` is `0.13–0.35`, nowhere near extremal, so **no constant in either
document moves** — but the statement should carry the branch. My instrument uses the branched
form throughout, so every `c♯` and `c_or` here is on the theorem's reading.

*Not in this list, and deliberately:* `f*(6) = 0.811654` versus the exact `0.811648852`.
`mg-29fe` found the cause (`b1_footrule.py:77` brackets `f*` in 20 bisection steps over
`[0,4]` and the sixth decimal printed is the upper bracket end, not a measurement). It is
**conservative, not wrong** — it over-states the route's own constant — and it is `mg-29fe`'s
finding to file, not mine.

---

## §12. NOT DONE

* **L2 is not proved, not refuted, not touched.** Neither is `mg-28ff`'s L2-free theorem, which
  I take as read and re-derive nowhere; `sweep_bound_sq` is its statement, not a re-proof.
* **Nothing here reaches `n ≥ 99`.** Exhaustive to `n = 7`; ten named families to `n = 14`; the combined construction of §8 to `n = 14`. **No family number is a maximum over its `n`** and none is labelled as one.
* **`c_or` is not bounded, only measured.** §7's mechanism is a conjecture with exhaustive
  evidence at `n ≤ 7` and no proof. **A proof of it would be the first uniform-in-`n` statement
  in this lineage, and it is the successor this ticket wants filed** — against the anti-
  correlation, not against either route and not against the loss.
* **`(M♯)`'s failure past `n = 15` is a measurement**, because exact copositivity enumerates
  `2^{n−1}−1` faces. Past that I can certify `(M♯)` holds and never that it fails.
* **`ε₀` is out of scope** and appears nowhere. **`17/78` appears nowhere in this document.**
* **`mg-28ff`'s `n = 7` sample figures are not quoted anywhere**, by design (`PREDICTIONS.md`
  E2). The one place I mention one — its `c_true(7) = 0.176145` in §4 — is to record that the
  enumerated maximum is `1.93×` larger, and it carries the word *sample* in the same sentence.
* **The 1032-vs-1037 L2 discrepancy is left exactly where `mg-28ff` left it**, and my own
  attempt at that census was wrong and is deleted rather than repaired (§9).
* **I edited no other document.** `STATE.md`, `roadmap.md`, and the `mg-28ff` / `mg-76b2` /
  `mg-94c3` documents are untouched. §6's `c_or` and §7's conjecture are proposals for whoever
  owns those files, not landings.

---

*`mg-51f4`. Instrument: `code/sweep_loss_51f4/` — `lib51f4.py` written from scratch, sharing no
source line with `lib28ff`, `lib76b2`, `libA94`, `lib_d3c7`, `lib3969` or `lib9461`, and
computing the transport by a **down-set dynamic program** rather than by filtering `n!`
permutations, which is what makes A2's agreement a cross-check and what makes families past `n = 10`
reachable at all. `s0_selftest.py` **16/16 forced arms**, including A6 (two independent exact
definiteness devices, 3902 decisions), A8 (the copositivity test refuses what it cannot
decide), and four negative controls, one of which failed and became §9.*
