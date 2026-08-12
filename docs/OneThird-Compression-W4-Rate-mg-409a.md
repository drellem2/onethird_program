# OneThird — COMPRESSION W4: **the note's `alpha_n` has a CEILING OF 1 and the (1/3)–(2/3) route needs it ABOVE 2.** The bar is not a rate, it is a constant, and it sits above the largest value the quantity can take at any poset

**Work item.** `mg-409a` (repo `onethird_program`), scoped by `pm-onethird` off Daniel's drop
`mg-2ffd`; re-scoped by `pm-onethird` at 14:05 local on 2026-08-12, and this document works the
re-scoped target (full-space spectrum of `2I − Π_o − Π_e`, **not** the linear-statistic
subspace).
**Subject.** [`docs/imports/compression.tex`](imports/compression.tex) §5 (`:229–270`) — the
inequality `E Var(f|C_o) + E Var(f|C_e) ≳ alpha_n Var(f)`, and the `alpha_n` it never defines.
**Depends on.** W2 `mg-8bc7` (`fa29801`) — read in full, its repair is the object priced here.
W1 `mg-bb60` (`7058fbd`) and W3 `mg-623a` (`9b692d7`) — read, cited, not re-measured.
**Instrument.** [`code/compression_rate_409a/`](../code/compression_rate_409a/), `run_all.sh`.

---

## 0. VERDICT

> ### **THE REQUIRED RATE IS NOT A RATE.**
>
> `alpha_n` must **exceed `(n−1)/(γ·n)`**, where `γ = δ(P) ≤ 1/3` is the balance constant of
> the putative counterexample. At the most generous admissible `γ = 1/3` that is
> **`3(n−1)/n`: `2` at `n = 3`, rising to `3`.** It does **not** decay with `n` at all.
>
> ### **AND THE QUANTITY IS CAPPED AT 1.**
>
> `alpha(P) ≤ 1` for **every** poset with `|L(P)| ≥ 2` — a five-line proof, exhibited-witness
> verified at 4 468 posets, and **attained** (the ordinal sum of 2-element antichains has
> `alpha = 1` exactly, checked to `n = 12`).
>
> **The bar is above the ceiling by a factor of at least 2, rising to 3. No theorem about
> `2I − Π_o − Π_e` can close that, because the shortfall is a fact about the operator and not
> about our arguments.**
>
> ### Attackability, as the ticket requires one of three:
>
> **`attackable-with-a-named-route` — and the route is already published, already exact, and
> already known to be insufficient.**
>
> - **Not `the-original-problem-restated`.** A restatement has the same difficulty. This one
>   has strictly *less*: `alpha(P) > 0` falls out of connectivity of the fiber graph in one
>   line (verified at every poset tested), and `alpha(P) = 1 − cos θ_min` is a **closed form**
>   from Halmos's 1969 two-projection theory, verified here to `1e-14`. The reformulation is
>   real and it genuinely reduces the object.
> - **Not `plausibly-attackable-but-no-route-yet`.** The route is named: Halmos 1969 →
>   Qian [arXiv:2201.12500](https://arxiv.org/abs/2201.12500), the reference W3 supplied.
> - **The reason none of that helps is arithmetic, not mathematical taste:** `1 − cos θ ≤ 1`,
>   and the bar is `≥ 2`.
>
> ### And the mayor's first task, answered before the rate work:
>
> **W2's repair restores §4's OPERATOR and the useful DIRECTION, unconditionally — but it
> moves the QUANTIFIER, and §5's target as written is the wrong side of that move.** The
> repair consumes `alpha_full` (minimum over all of `L²`); §5 states `alpha_lin` (minimum over
> pair-orientation linear statistics). `alpha_full ≤ alpha_lin` always, and they differ
> **strictly at 61 of 195 posets at `n = 4`**, by up to 11 %. Attacking §5 *exactly as
> written* would not have fed the repair. **This is not the "different object, stop" branch:
> the repaired §4 does deliver the operator §5 reduces to. It is the rate that kills it, and
> the rate question was worth doing regardless — which is what the mayor said.**

---

## 1. The mayor's first question: does W2's repair restore the object §5 reduces to?

Three answers, and they are not the same answer.

**(a) THE OPERATOR: YES.** W2's repair is

```
    <f, (I − P_BK) f>  ≥  (2/(n−1)) <f, (2I − Π_o − Π_e) f>        for every f ∈ L²
```

with equality exactly when `f` is affine on every fiber of both foliations. That is the same
`M = 2I − Π_o − Π_e` §4 introduces and §5 reduces to. Re-derived on this instrument at 73
(poset, function) pairs with **0 violations**, alongside the equality case on linear
statistics (`r0.5`). §5's `:217` linearity assumption — the one W1 found is not ours — is
**not needed** for this direction. That is W2's contribution and it stands.

**(b) THE QUANTIFIER: NO, AND IT MOVES AGAINST YOU.** Write

- `alpha_full(P) = min { R_M(f) : f ⊥ 1 }` — what the repair consumes;
- `alpha_lin(P)  = min { R_M(f) : f ⊥ 1, f a pair-orientation linear statistic }` — what §5
  states ("for the relevant `f`").

`alpha_full ≤ alpha_lin` always. Measured (`r4.1`):

| `n` | population | posets | `alpha_full < alpha_lin` strictly | worst ratio |
|---|---|---|---|---|
| 3 | exhaustive | 13 | 0 | 1.000000 |
| 4 | exhaustive | 195 | **61** | 0.893957 |
| 5 | sampled(45) | 44 | **30** | 0.893957 |

So a proof of §5 *as written* does not feed the repair at roughly a third of posets. This is
the measured form of the point `pm-onethird`'s re-scope makes structurally: a bound on a
subspace bounds the gap from **above**, because the gap is a minimum over all of `L²`.

**(c) THE WALL'S OBJECT: NO, AND THE REPAIR DOES NOT CHANGE THAT.** Both `alpha_full` and
`alpha_lin` bound `λ₂^BK`. [`STATE.md:78`](../STATE.md) records that `λ_std` and `λ₂^BK` are
**INCOMPARABLE** — no universal inequality in either direction, exact rationals, `mg-d1be` —
so *"Theorem E's bound on `λ₂^BK` gives nothing for `λ_std`"*, and neither does this one.
Nothing here reaches the wall directly. §2 below prices the one consumer that does not need
to.

---

## 2. THE BAR — what the (1/3)–(2/3) route actually requires of `alpha_n`

The note never says. It is derivable, and there is exactly one place in the programme that can
consume a **lower** bound on the BK gap.

**Why only one.** The architecture's demand is `L1b`: `δ(P) < 1/3 ⟹ 1 − λ_std ≤ ε_spec`, i.e.
`λ_std` **near 1**. Nothing about `λ₂^BK` transfers to `λ_std` (§1(c)). So a lower bound on
the BK gap cannot serve `L1b` at all. What it *can* do is **contradict** a proven upper bound
on the same quantity, emptying the counterexample class — and the corpus has exactly such an
upper bound: **Theorem E, `STATE.md` row 6, `U`/proven**, at
`one_third_width_three/step8.tex` §§G1.1–G1.3.

**Theorem E, quantitatively** (Lemma `frozen-pair-existence`, `step8.tex:195–270`): a
`γ`-counterexample on `n ≥ 2` elements, `γ ∈ (0, 1/3]`, contains an incomparable pair with

```
    E_BK(f_xy) / Var(f_xy)  ≤  λ(γ, n)  =  2/(γ n).
```

**The chain, every link verified exactly on this instrument** (`r2`):

| link | statement | how checked | result |
|---|---|---|---|
| **L1** | `R_M(f_xy) = ((n−1)/2)·E_BK(f_xy)/Var(f_xy)` — (*) at a pair indicator | exact rationals, every incomparable pair of every poset in the population | **0 failures / 19 328 instances** |
| **L2** | `alpha(P) ≤ R_M(f_xy)` — Rayleigh at a test vector | measured `alpha` vs exact bound | **0 violations / 253 posets**; the pair witness is **tight at 51 of them** |
| **L3** | `Σ_{x∥y} E_BK(f_xy) ≤ 1/2` — `step8.tex` Step 1 | exact, re-derived on an implementation that has never seen it | **max = 1/2, 0 failures / 4 449 posets** |
| **L4** | Theorem E as stated | **read from `step8.tex`, not re-proved here** | — |

Therefore, for every `γ`-counterexample, `alpha(P) ≤ (n−1)/(γn)`. **A contradiction requires
that cap violated:**

```
    THE BAR:   alpha_n  >  (n−1)/(γ n),      γ ≤ 1/3  (strict, by the hypothesis δ(P) < 1/3)
```

| `n` | bar at `γ=1/3` | at `γ=1/4` | at `γ=1/6` | **ceiling (§3)** |
|---|---|---|---|---|
| 3 | 2.000000 | 2.666667 | 4.000000 | **1** |
| 4 | 2.250000 | 3.000000 | 4.500000 | **1** |
| 6 | 2.500000 | 3.333333 | 5.000000 | **1** |
| 20 | 2.850000 | 3.800000 | 5.700000 | **1** |
| 1000 | 2.997000 | 3.996000 | 5.994000 | **1** |

**Read the first column before anything else: it does not decay.** The ticket asked for a
rate and the answer is that there is no rate to hit — the demand is a constant in `[2, 3)`.
Every previous discussion of this note has implicitly assumed the bar was something like
`Ω(n^{-1})` or `Ω(n^{-2})` that a good enough angle bound might reach. It is not.

---

## 3. THE CEILING — what `alpha_n` can be

**Theorem (proved here, `r1`).** For every poset `P` with `|L(P)| ≥ 2`, `0 < alpha(P) ≤ 1`,
and `1` is attained.

*Proof of the upper bound, in full, because it is five lines.* Let `Q_o = Π_o − P_1`,
`Q_e = Π_e − P_1`.
**Case 1: `Ran Q_o ≠ 0`.** Take `f ≠ 0` with `Π_o f = f`, `f ⊥ 1`. Then
`<f, Mf> = 2‖f‖² − ‖f‖² − ‖Π_e f‖² = ‖f‖² − ‖Π_e f‖² ≤ ‖f‖²`, so `alpha ≤ R_M(f) ≤ 1`.
**Case 2: `Ran Q_o = 0`,** i.e. `C_o` is constant on `L(P)`: every 2-block `{x_{2j−1}, x_{2j}}`
is a fixed set. Then `C_e` determines `L` completely — `I_1` fixes the order in block 1, and
`I_{2j+1}` together with `I_{2j}` fixes block `j+1` inductively — so `Π_e = I`, `Π_o = P_1`,
and `M|_{1⊥} = 2I − 0 − I = I`, giving `alpha = 1` **exactly**. ∎

*Proof of positivity.* `Mf = 0` iff `Π_o f = Π_e f = f` iff `f` is constant on every odd fiber
and on every even fiber, i.e. invariant under all `τ_odd` and all `τ_even`, i.e. constant on
each component of `G_BK`. `G_BK` is connected (Karzanov–Khachiyan), so `f` is constant. ∎

**Verification, not assertion.**

- `r1.1` — the fiber graph is connected at **4 468 / 4 468** posets (`n ≤ 5` exhaustive plus
  `n = 6` sampled); pure union–find, no eigenvalue, no float.
- `r1.2` — every one of the 4 468 posets is covered by an **exhibited rational witness**:
  4 277 by an odd-fiber indicator, 191 by the `C_o`-trivial case. **Max exhibited `R_M` = 1.**
- `r1.3` — `Z_n` (ordinal sum of `n/2` two-element antichains) has `C_o` constant and `C_e`
  separating at `n = 4, 6, 8, 10, 12`, hence `alpha(Z_n) = 1` exactly; Jacobi agrees to `1e-10`.
- `r1.4` — measured `alpha ≤` the exhibited bound at all 208 posets with `n ≤ 4`.

**`1 < 2`. That is the whole finding.** The constraint Theorem E places on `alpha` for a
counterexample (`≤ (n−1)/(γn) ≈ 3`) is *weaker* than the constraint `alpha` satisfies at every
poset unconditionally (`≤ 1`), so **the compression's output and Theorem E can never
collide.** No lower bound provable about `2I − Π_o − Π_e` can empty the counterexample class.

---

## 4. The other reading of `alpha_n`, and it is worse: `Θ(n^{-2})`

The note writes `alpha_n` with a subscript `n` and no poset, which reads as *one constant valid
at every poset on `n` elements*. Under that reading there is a closed form, provable by hand.

**Theorem (`r3.1`).** On the antichain `A_n`, every centred position statistic
`f_w(L) = Σ_x w_x·pos_L(x)` — a pair-orientation linear statistic with `c_xy = w_y − w_x` —
satisfies, **independently of `w`**,

```
    E_BK(f_w)/Var(f_w) = 12/(n³ − n),        R_M(f_w) = 6/(n(n+1)).
```

*Because* `E_BK(f_w) = Σw²/(n−1)` and `Var(f_w) = n(n+1)Σw²/12` under uniform `S_n`. Hence
**`alpha_n ≤ alpha(A_n) ≤ 6/(n(n+1)) = Θ(n^{-2})`.**

Verified exactly at `n = 3…7` against three or four independent weight vectors each, all
agreeing on the nose. Measured `alpha(A_n)`: `0.500000` / `0.292893` / `0.190983` at
`n = 3,4,5` against the bound `0.5 / 0.3 / 0.2` — and matching `1 − cos(π/n)` to nine digits,
which is what Aldous' spectral gap theorem predicts for this chain (**read from the
literature; no verdict here depends on it**). The antichain is **not** the unique minimiser —
a large tie class shares the value — which makes the closed form more useful, not less.

**Consequence, and it is the "true and useless" outcome the ticket asked to be tested for.**
Through W2's repair a uniform `alpha_n = Θ(n^{-2})` yields `gap_BK = Ω(n^{-3})` — the order
this chain is *already* known to have at every poset (Bubley–Dyer `n³ log n`, cited in this
repo at [`docs/audit-stage-process.md:211`](audit-stage-process.md)). It reproduces a known
result and is `Θ(n²)` below the bar.

---

## 5. Does the two-projection literature settle it?  (the re-scope's explicit ask)

**It settles the FORM completely and supplies NO NUMBER that helps.**

**Settles.** Specialising Halmos (1969) to `M` on `1⊥`: on the generic part the pair
`(Q_o, Q_e)` is unitarily `2×2` blocks with `M`-spectrum `1 ∓ cos θ_k`; on
`Ran Q_o ∩ Ker Q_e` and `Ker Q_o ∩ Ran Q_e` it is `1`; on `Ker Q_o ∩ Ker Q_e` it is `2`; and on
`Ran Q_o ∩ Ran Q_e` it is `0` — **a part `r1.1` shows is empty at every poset**. Hence exactly

```
    alpha(P) = 1 − cos θ_min,        cos θ_min = √( λ_max(Q_o Q_e Q_o) ),
```

with `alpha = 1` when the generic part is empty. **Verified on this instrument at 233 posets, worst
disagreement `7.8e-15`** (`r6.1`). And the angle has a clean closed form on the antichain:
`θ_min(A_n) = π/n` exactly at `n = 3, 4, 5` (45.00° at `A_4`, 36.00° at `A_5`), while `Z_n` is
the **degenerate** case — `Ran Q_o = {0}`, every angle `π/2`, `alpha = 1`, the largest a
principal-angle bound can ever return. Qian, [arXiv:2201.12500](https://arxiv.org/abs/2201.12500), applies precisely this
theory to two-component Gibbs samplers and — per its abstract — reduces the previously
intractable questions to matrix algebra. `(Π_o + Π_e)/2` **is** such a sampler; W3 established
that.

**Cannot settle.**

- **Any value above 1.** `1 − cos θ ≤ 1` is an identity. No principal-angle theorem, published
  or future, puts `alpha` over the bar. *This is why the literature question, which looked like
  the expensive one, is cheap: the ceiling is a property of the object.*
- **A constant.** [arXiv:2304.02109](https://arxiv.org/abs/2304.02109) (AAP 2025) proves
  **solidarity** — if one scan order has a gap then all do, and polynomial scaling is preserved
  — a positivity/scaling transfer, not a constant. For us positivity is already free (`r1.1`,
  one line from connectivity). And Wilson (`arXiv:math/0102193` §7, quoted by W3) already
  priced the sweep decomposition at *about a factor of two, on the upper bound only*.

**Caveat, stated plainly:** the two arXiv items were read at **abstract level only**
(`WebFetch`, 2026-08-12). Nothing above depends on their contents — the ceiling is proved in
§3 and the bar in §2, both on this machine.

---

## 6. The note's own checkable ask: "expressed purely in terms of a pair bias"

`compression.tex:270`. **The answer splits, and the split is worth more than either half.**

**(a) THE SCALAR `δ` DOES NOT CONTROL `alpha` — refuted, at every even `n`.** Take

- `A_n`, the antichain: **every** incomparable pair has `p_xy = 1/2` exactly, `δ = 1/2`;
- `Z_n`, the ordinal sum of 2-antichains: **every** incomparable pair has `p_xy = 1/2` exactly,
  `δ = 1/2`.

Verified exactly at `n = 4, 6, 8` (`r5.1`). Identical, maximal balance — and
`alpha(A_n) ≤ 6/(n(n+1)) → 0` while `alpha(Z_n) = 1`. A factor `Θ(n²)` apart at the same `δ`.
Since **`δ(P) < 1/3` *is* the (1/3)–(2/3) counterexample condition**, the connection the note
hoped for cannot run through it. This is the direction the corpus already predicted:
[`docs/audit-stage-process.md:211`](audit-stage-process.md) records that the `δ` obstruction is
**provably not a mixing obstruction**, and `alpha` is a mixing quantity.

**(b) THE FULL BIAS MULTISET IS NOT REFUTED — and it goes the note's way.** Keyed on the
isomorphism-invariant multiset `{min(p_xy, 1−p_xy)}`:

| `n` | population | buckets | buckets merging **>1** iso class | buckets with `alpha` spread |
|---|---|---|---|---|
| 4 | exhaustive | 10 | 4 | **0** |
| 5 | exhaustive | 33 | 22 | **0** |
| 6 | sampled(60) | 39 | 5 | **0** |

The vacuity control is the third column: the buckets genuinely merge non-isomorphic posets, so
"0 spread" is not the tautology "isomorphic posets agree". **On every population tested the
pair-bias multiset determines `alpha` outright.** That is an `n ≤ 5`-exhaustive observation and
not a theorem, and **it changes nothing about the verdict** — §2 is a statement about `alpha`'s
*value*, and no representation of a quantity raises it. It is reported because it runs against
this ticket's direction of travel and against my own expectation (see D3).

---

## 7. What would have to be true for this verdict to be wrong

Filed as named conditions so that a reversal cannot be assembled after the fact.

1. **Theorem E is wrong or `λ(γ,n) = 2/(γn)` is misread.** The bar is read off `step8.tex:195–270`
   and `:325–375`. I re-derived its Step 1 (`Σ E ≤ 1/2`) exactly and independently; I did **not**
   re-derive Steps 2–4 or `I(P) ≥ n/2`. If `λ(γ,n)` is actually `o(1/n)`, the bar falls below 1
   and the route reopens. **It would have to fall by a factor of `n`.**
2. **Some consumer of a BK-gap *lower* bound exists that I did not find.** I claim the only one
   is contradiction with Theorem E, on the strength of `STATE.md:78`'s incomparability of
   `λ_std` and `λ₂^BK`. A route from `λ₂^BK` to `λ_std` would be `L1b` itself (row 8, OPEN), so
   this is not a gap in my search so much as the wall.
3. **`alpha ≤ 1` is wrong.** It is proved in §3 in five lines and witnessed at 4 468 posets. If
   it is wrong, the witness at some poset is wrong, which is checkable in one command.
4. **The re-scoped target is not the full-space `alpha`.** The re-scope is explicit that
   `alpha_full` is the target, so this is a hypothetical — but it is worth pricing, because
   `alpha_lin ≥ alpha_full` means §3's ceiling does **not** transfer to `alpha_lin` for free.
   It is **measured** rather than proved: `max alpha_lin = 1.0` over `n ≤ 4` exhaustive plus
   `n = 5` sampled(45), attained at the 3-element poset `{0<2, 1<2}`. So the bar is above that
   ceiling too, on the populations tested — but **`alpha_lin ≤ 1` is asserted here as a
   measurement, not a theorem**, and Case 1 of §3's proof does not obviously supply a *linear*
   witness (a linear statistic is `Π_o`-measurable only when its coefficients vanish on every
   incomparable 2-block, which is a real condition and not automatic).

---

## 8. Defects of my own, all kept

**D1 — my first control could not fire, and I would not have noticed if it had passed.**
`r0.7`'s original C1 corrupted `blocks_e` by dropping the trailing singleton for even `n`. The
identity `(*)` still held **exactly**, because the last position of a linear extension is
determined by the other `n−1`, so the coarser group list induces the *same* partition of
`L(P)`. A control that cannot fail is not a control (W2's own D2 is the same shape). Replaced
with two that do fire, and the reason the first could not is now itself an arm (`r0.7`, D1
block) rather than a sentence.

**D2 — I keyed an isomorphism-invariant question on a non-invariant key, and got a clean
answer.** `r5.2`'s first version bucketed posets by the multiset of `p_xy` over label-ordered
pairs. That is **not** an isomorphism invariant — an isomorphism can flip `p ↦ 1−p` on any
pair — so it split isomorphism classes apart and reported "30 distinct multisets, 0 with
`alpha` spread" over `n = 4`, where there are only 16 isomorphism classes. The number 30 > 16
is what caught it, and only because I ran a class count I had not planned to run. Corrected to
`{min(p, 1−p)}`, which gives 10 buckets at `n = 4`, and **the corrected answer is the same
"0 spread"** — so the defect did not change the finding, which is exactly the case in which it
would normally go unrecorded.

**D3 — a prediction of mine that lost, and it is §6(b).** I expected the pair-bias multiset to
fail to determine `alpha`, and built `r5.2` as a refutation search. It found **0 collisions on
every population**, including `n = 5` exhaustive with 22 of 33 buckets merging distinct
isomorphism classes. The note's instinct is supported there and mine was wrong.

**D4 — no `PREDICTIONS.md` was filed before the instrument existed.** Several tickets in this
repo do file one and this did not; the honest reason is that the load-bearing content here is
an inequality between two derived numbers rather than a search, so there was little to bet on
— but that is a judgement I made, not a rule I followed, and D3 is the one place a prior
existed and it lost.

**D5 — `r0` imports `lib8bc7` and `r1…r6` do not.** The cross-check in `r0.2–r0.5` is
therefore a genuine second implementation, but everything downstream shares **one** library
(mine), so the arms are not independent witnesses of each other. Same shape as W2's D6, stated
because it applies to me too.

**D6 — the eigenvalue path is float.** `alpha_measured` is a Jacobi sweep. Every **verdict**
here is either an exact rational comparison (`r0.4`, `r0.5`, `r1.2`, `r2.1`, `r2.2`, `r3.1`,
`r5.1`) or an exhibited rational witness (`r1.2`, `r1.3`). The float values are measurements
and appear in tables, never under a `PASS`. The one place a float carries weight is `r6.1`'s
`1e-14` agreement, and §5 does not depend on it.

**D7 — `n = 6` and `n = 7` are SAMPLES, and the samples are small.** `r1.1` (150), `r2` (120 /
40), `r3.3` (60), `r5.2` (60), `r6.1` (25). Every table says so in its population column. The
ceiling and the bar are **proved**, not sampled; the sampled rows are consistency, not warrant.

---

## 9. What this document does not do

- **`docs/imports/compression.tex` is NOT edited.** Its README reserves that directory for
  verbatim copies; W1 and W2 left it alone and so does this.
- **`STATE.md` is NOT touched.** Nothing here is a ledger movement — the finding is about a
  document that is not on the ledger, and `mg-e331`'s ratchet is not exercised.
- **Theorem E is not re-proved**, only its Step 1 and its statement are used; row 6's kind is
  unchanged.
- **`λ_std` is not computed anywhere in this directory**, and no claim is made about it beyond
  quoting `STATE.md:78`'s incomparability.
- **No claim is made that the compression is worthless as mathematics.** §1(a) is a real
  unconditional theorem of W2's and §5's closed form is real. The claim is narrower and is the
  one the ticket asked for: **against the (1/3)–(2/3) bar, `alpha_n` has nowhere left to go.**
