# OneThird — COMPRESSION W5: **the bar IS `k`-independent, and so is the ceiling, and it is the same fact that makes both true.** `alpha_k ≤ 1` at every poset and every `k`, attained at every `k`. **CLASS CLOSED BY CEILING, AT EVERY `k`.**

**Work item.** `mg-8d66` (repo `onethird_program`), filed by `pm-onethird` on Daniel's
suggestion after `mg-409a` closed the `k = 2` route; dispatched by the mayor with the
instruction to **attack** the derivation rather than confirm it.
**Subject.** `pm-onethird`'s generalisation of `docs/imports/compression.tex` §§4–5 to `k`
foliations, quoted in full in §1 below, and the two questions it turns on: is the **bar**
`k`-independent, and what is the **ceiling** on `alpha_k`.
**Depends on.** W4 `mg-409a` (`188c959`) — the bar and the `k = 2` ceiling, read in full, not
re-derived and not attacked. W2 `mg-8bc7` (`fa29801`) — the operator inequality and its
equality case, which is the object generalised here.
**Instrument.** [`code/compression_kfoliation_8d66/`](../code/compression_kfoliation_8d66/),
`run_all.sh`, ~170 s.

---

## 0. VERDICT

> ### **1. IS THE BAR `k`-INDEPENDENT?  YES — and `pm-onethird`'s premise is right for exactly the reason he gives.**
>
> The constant `2/(n−1)` is a per-position constant. It does not carry a class size. Verified
> in the strong form: the operator inequality `((n−1)/2)(I − P_BK) ⪰ Q_S` holds with that one
> constant at **1 728 of 1 728 (poset, partition) pairs**, by exact rational PSD, over **every**
> admissible partition. The bar `alpha_k > (n−1)/(γn)` therefore contains no `k`.
>
> ### **2. WHAT IS THE CEILING?  `alpha_k ≤ 1`. AT EVERY `k`. ATTAINED AT EVERY `k`.**
>
> Not `k − 1`, which is all `mg-409a`'s own proof generalises to — and `k − 1` clears a bar of
> 3 from `k = 4`, so **the ticket's suspicion about that proof is correct** (`k4.5`: `mg-409a`'s
> witness family really does reach `2.18` at `k = 5`). The ceiling of `1` survives because a
> **different** witness does, and that witness is *blind to `k`*:
>
> ```
>     alpha_S  ≤  R_{Q_S}(f_xy)  =  P(x,y adjacent) / (4 p(1−p))  ≤  1/(2 max(p,1−p))  ≤  1
> ```
>
> the same rational number at **every** admissible partition `S`, because `f_xy` sees exactly
> one swap position in the whole word and is therefore affine on every fiber of every class.
> Exact rationals, exhibited vector, no eigensolver: **0 failures at 18 373 (poset, pair)
> instances exhaustively over every labeled poset at `n = 3, 4, 5`**, and `alpha_S(Z_n) = 1`
> **exactly at all 4 360 (`Z_n`, partition) pairs** for `n = 4, 6, 8, 10`, both directions exact.
>
> ### **3. THEREFORE: `class-closed-by-ceiling`, at every `k`.**
>
> `1 < 2 ≤ (n−1)/(γn) < 3`. The shortfall is a factor of 2 at `n = 3` rising to 3, **identical
> to `mg-409a`'s at `k = 2`**, and it does not improve at any `k`.
>
> ### And the structural reason, which is the part worth carrying forward:
>
> **`sup_k alpha_k = ((n−1)/2)·gap_BK`, attained at `k = n−1`.** Refining a class raises `Q`
> (exact PSD, 2 032 refinement instances), and the finest admissible partition is
> `Q_finest = ((n−1)/2)(I − P_BK)` **as an exact matrix identity** — the BK generator itself,
> rescaled. So the `k`-family is squeezed between *strictly weaker than the truth* (every
> `k < n−1`) and *exactly the truth* (`k = n−1`), where the bound reads `gap_BK ≥ gap_BK`.
>
> **The compression cannot overshoot the spectral gap. It can only walk back toward it.** The
> `k` at which the ceiling is highest is the `k` at which the compression compresses nothing:
> each fiber is a **one-dimensional** cube, i.e. a single swap.
>
> ### `class-closed-by-counting`: **NO, and it was checked first.**
>
> `k` reaches `n−1` (all singletons; `k1`). The minimum is 2 and **the `k = 2` partition is
> unique** — a path has one proper 2-colouring — so `mg-409a`'s odd/even was not a choice. The
> cheap answer the ticket hoped for is **not available**; the class had to be closed on the
> operator.

---

## 1. What was asked, and what `pm-onethird` wrote

The ticket's derivation, quoted verbatim:

```
    E_BK(f) = (1/(n-1)) * (1/2) * sum over ALL positions p of E[(f - f.tau_p)^2]
            = sum over classes of (2/(n-1)) * E[Var(f | C_i)]                        (A)
            = (2/(n-1)) * <f, (kI - sum_i Pi_i) f>                                   (B)

  THE CONSTANT 2/(n-1) IS THE SAME FOR EVERY CLASS REGARDLESS OF CLASS SIZE
```

**(B) is an identity and it is right.** `<f, (kI − ΣΠ_i) f> = Σ_i E Var(f | C_i)` is the
definition of a conditional expectation, one class at a time.

**The claim about the constant is right, and right for the stated reason.** §2.

**(A) is a `≥`, not an `=`.** §3. It is the same `≥` `mg-8bc7` found at `k = 2`, read one class
at a time, and it is where the derivation's conclusion comes apart — though not in the way that
sentence makes it sound, because the inequality points the *useful* way. What kills the
conclusion is not that (A) is lossy; it is **where the loss goes to zero**. §5.

---

## 2. THE BAR IS `k`-INDEPENDENT — the premise, confirmed exactly

A **class** is a set of pairwise non-adjacent swap positions; an **admissible partition** is a
partition of the `n−1` swap positions into classes. Within a class the swaps act on disjoint
pairs of word positions, so they commute, and — verified at `k0.3`, **0 violations at 548
(poset, class) instances** — each fiber is a genuine **cube**: its size is exactly
`2^(#free positions)`, and the free-position set is constant on the fiber, which is what makes
"cube" true rather than approximately true.

**The anchor (`k2.1`), an exact matrix identity, no test function involved:**

```
    Q_finest  =  (n−1)I − Σ_{p=0}^{n−2} Π_p  =  ((n−1)/2)·(I − P_BK)
```

because `Π_p = (I + T_p)/2` on legal swaps and `I` on illegal ones, so `Σ_p Π_p =
((n−1)/2)I + (1/2)Σ_p T_p` while `(n−1)P_BK = Σ_p T_p`. Checked **entrywise in exact
rationals at 373 posets** (`n = 3, 4` exhaustive; `n = 5` sample(120); `n = 6` sample(60); 8
posets with `|L(P)| > 130` skipped and counted).

**The premise (`k2.2`):** if the constant carried a class size, the operator inequality would
hold at some partitions and fail at others. It does not.

```
    ((n−1)/2)(I − P_BK) − Q_S   is PSD   at 1 728 of 1 728 (poset, S) pairs, EXACTLY
```

— over **every** admissible partition at each poset, by exact rational elimination. Hence
`E_BK(f) ≥ (2/(n−1))·<f, Q_S f>` for every `f` and every `S`, with **one** constant.

> **THE BAR IS `k`-INDEPENDENT.** `alpha_k` must exceed `(n−1)/(γn)`, `γ ≤ 1/3` — a constant in
> `[2, 3)`, containing no `k`.

This is not "the constant happens not to move". The sum is over **positions**; a class
contributes once per position it contains, and the chain's uniform choice among `n−1` positions
is what supplies the `1/(n−1)`. `pm-onethird` identified the mechanism correctly.

---

## 3. …and his second `=` is a `≥`

Within one class the swaps are disjoint, but a class is **not one coordinate**: its fiber is a
cube of dimension `d = #free positions`. On that cube, with `fhat` the Fourier–Walsh
coefficients,

```
    Σ_{p ∈ S} E Var_p(f)  =  Σ_B |B|·fhat(B)²   ≥   Σ_{B ≠ ∅} fhat(B)²  =  E Var(f | C_S)
```

with equality **iff `f` carries no Fourier weight above degree 1 on the fiber**. That is
exactly `mg-8bc7`'s equality case ("(*) is an equality on linear statistics and an inequality in
general"), read one class at a time.

Measured (`k2.3`): the inequality is **strict at 2 789 of 5 184 (f, S) instances** and never
runs the wrong way. Exhibited both ways at `k2.4` — a pair indicator sits in the equality case;
a degree-2 parity planted inside a 2-dimensional fiber loses, `7/60 < 1/5`.

---

## 4. THE CEILING IS 1, AT EVERY `k` — and it needs a witness `mg-409a` did not use

### 4.1 Why `mg-409a`'s proof does not generalise (the ticket is right about this)

`mg-409a` takes `f ∈ Ran(Π_o)`, `f ⊥ 1`, and reads
`<f, (2I − Π_o − Π_e)f> = 2‖f‖² − ‖f‖² − ‖Π_e f‖² ≤ ‖f‖²`. The same move at `k` classes gives
`<f, Q_S f> ≤ (k−1)‖f‖²` and **nothing better** — it discards `k−2` of the `k` terms. A ceiling
of `k−1` clears a bar of 3 from `k = 4`.

And it is not merely that the *bound* degrades — the witness family genuinely goes above 1
(`k4.5`, measured maxima):

| `n` | `k = 2` | `k = 3` | `k = 4` | `k = 5` |
|---|---|---|---|---|
| 4 | 1.000000 | **1.500000** | — | — |
| 5 | 1.000000 | **1.562500** | **1.875000** | — |
| 6 | 1.000000 | **1.636364** | **1.909091** | **2.181818** |

**So `pm-onethird`'s suspicion — that the ceiling of 1 is an artefact of the `k = 2` proof — is
correct about that proof.** It is not correct about the ceiling.

### 4.2 The witness that is blind to `k`

Take an incomparable pair `(x, y)` and `f_xy = 1{x before y}` — Theorem E's own test function,
and the one `mg-409a` uses at its L1/L2.

**Step 1 — `f_xy` is affine on every fiber of every class.** Inside a class the free positions
are disjoint, non-adjacent pairs of word positions. Either `x` and `y` are the two elements of
one such pair — then `f_xy` *is* that coordinate — or they are not, and since the pairs occupy
disjoint consecutive position-ranges, no swap in the class can move `x` across `y`, so `f_xy` is
**constant** on the fiber. Degree ≤ 1 either way. Hence `f_xy` sits in the equality case of §3
for **every** admissible partition, and

```
    <f_xy, Q_S f_xy>  =  ((n−1)/2)·E_BK(f_xy)  =  P(x,y adjacent)/4       for EVERY S.
```

**Verified: one value across all admissible `S`, equal to `((n−1)/2)E_BK`, at 1 447 (poset,
pair) instances** (`k4.1`, exact) — and the control `k4.2` shows a *generic* `f` does depend on
`S`, so this is a property of the witness and not of the quantity.

**Step 2 — the swap is a bijection.** Swapping an adjacent incomparable `x, y` is an involution
of `L(P)` carrying `{x,y adjacent, x first}` onto `{x,y adjacent, y first}`. So each has
probability `P(adj)/2`, and `P(adj)/2 ≤ min(p, 1−p)` where `p = P(x before y)`.

**Step 3 — arithmetic.** `Var(f_xy) = p(1−p)`, so for **every** admissible `S`

```
    alpha_S  ≤  R_{Q_S}(f_xy)  =  P(adj)/(4p(1−p))  ≤  2min(p,1−p)/(4p(1−p))
             =  1/(2 max(p, 1−p))  ≤  1.                                             ∎
```

Every link checked exactly, **exhaustively over every labeled poset at `n = 3, 4, 5`** —
18 373 incomparable pairs, **0 failures on all four links**, largest best-pair value `= 1`. The
witness is also checked to be **non-vacuous**: `P(adj) > 0` at every pair, since a zero would
"prove" `alpha ≤ 0` and contradict `mg-409a`'s positivity theorem — that is what a broken
witness would look like, so it is tested for rather than assumed.

`k4.4` re-derives the cap **directly at every admissible `S`** rather than routing through
Step 1, at 1 548 (poset, `S`) pairs: 0 failures.

### 4.3 And it is ATTAINED at every `k`

`Z_n` (ordinal sum of `n/2` two-element antichains) has `alpha_S(Z_n) = 1` **exactly** at
**every** admissible partition, `n = 4, 6, 8, 10` — **4 360 (`Z_n`, `S`) pairs, both directions
exact**: `Q_S − (I − P_1)` is PSD by exact elimination (`alpha_S ≥ 1`), and the pair witness
gives exactly 1 (`alpha_S ≤ 1`).

> So the ceiling does not merely fail to rise with `k` — **it is the same number, and the same
> attained number, at every `k`.** `mg-409a`'s ceiling was not an artefact of `k = 2`.

---

## 5. The structural reading: the route's best case is the original problem restated

Three facts compose.

1. **Refinement raises `Q`** (`k3.1`). If `S'` refines `S`, then `Q_{S'} − Q_S` is PSD —
   **2 032 (poset, refinement) instances, 0 failures**, exact. So `alpha_S ≤ alpha_{S'}`.
   *This is `pm-onethird`'s intuition and it is correct.* The control `k3.2` shows the reversed
   comparison is refused at 38 of 61 instances, so the direction is measured, not assumed.
2. **The refinement order has a top**, and it is admissible at every `n`: all singletons,
   `k = n−1` (`k1`).
3. **At the top, `Q` is the chain** (`k2.1`): `Q_finest = ((n−1)/2)(I − P_BK)`, so
   `alpha_finest = ((n−1)/2)·gap_BK` (read back numerically at `k3.3`, worst float difference
   `1.19e-13`).

Therefore `sup_k alpha_k = ((n−1)/2)·gap_BK`, **attained**, and substituting into the route's
own bound at `S = finest`:

```
    gap_BK  ≥  (2/(n−1))·alpha_finest  =  gap_BK.
```

**The `k`-family is a family of *weakenings* of the spectral gap, indexed by how coarse the
foliation is.** Raising `k` recovers the loss; it cannot exceed the gap. And the `k` where the
ceiling is highest is the `k` where each fiber is a **1-dimensional** cube — a single swap —
i.e. where "compression to a cube" has compressed nothing at all.

This is why the ceiling of `1` is not a coincidence of `k = 2`: `alpha_k ≤ 1` **is**
`gap_BK ≤ 2/(n−1)`, which §4.2 proves at every poset with an incomparable pair, via a witness
that no amount of refining can see.

---

## 6. Item 3, measured

`alpha_k` by Jacobi over the poset population (`k5.1`; `n = 3, 4` exhaustive, `n = 5, 6, 7`
sampled 200/120/60, all restricted to `|L(P)| ≤ 34` because Jacobi is `O(N³)`). **3 504
(poset, partition) measurements; maximum over the whole set = 1.000000000.**

| `n` | `k` | posets | max `alpha_k` | mean `alpha_k` | bar (`γ=1/3`) |
|---|---|---|---|---|---|
| 7 | 2 | 23 | 1.000000 | 0.364018 | 2.571429 |
| 7 | 3 | 345 | 1.000000 | 0.366117 | 2.571429 |
| 7 | 4 | 575 | 1.000000 | 0.367046 | 2.571429 |
| 7 | 5 | 230 | 1.000000 | 0.367632 | 2.571429 |
| 7 | 6 | 23 | 1.000000 | 0.368059 | 2.571429 |

**Does `alpha_k` rise with `k`?** At a fixed poset, sometimes: `alpha_finest > alpha_{k=2}` at
**92 of 434** posets measured (`k5.2`). The effect `pm-onethird` predicts is real. It is also
small — the mean moves from `0.364` to `0.368` across the whole range of `k` at `n = 7` — and
it is capped.

> **`alpha_k` rising at a fixed poset and the CEILING rising are two different statements**, and
> only the first is true. That is the step at which the derivation slides, and it is filed as
> `E1` in `PREDICTIONS.md` because it is the error I most expected to make myself.

**The constraint carried forward** (`k5.3`): `mg-8bc7` measured that the two foliations are not
interchangeable. At `k ≥ 3` the asymmetry is worse — worst within-partition rank ratio measured
**5.333**. Nothing in §§2–5 averages over the classes: the identity is a per-position sum, the
Efron–Stein step is applied inside each class separately and then added, and the witness is
checked against each class's own fiber. The asymmetry is priced by never being used.

---

## 7. What this does NOT close, and what would overturn it

**Does not close.** (a) `λ_std`. `STATE.md:78` records that `λ_std` and `λ₂^BK` are
INCOMPARABLE; nothing here reaches the wall, exactly as `mg-409a` §1(c) says of its own result.
(b) **Foliations that are not position-classes.** Everything here is about σ-algebras generated
by *sets of adjacent-transposition positions* — `pm-onethird`'s construction, and the note's.
A compression whose fibers are not orbits of position swaps is outside this argument, and the
`Q_finest = ((n−1)/2)(I − P_BK)` anchor is exactly what such a scheme would have to break.
(c) A different chain. Everything is normalised to `E_BK` at `compression.tex:106`.

**What would overturn this finding** (filed in `PREDICTIONS.md` before the instrument existed):

1. Any admissible partition at any poset with `alpha_S > 1`.
2. Any counterexample to `Q_finest = ((n−1)/2)(I − P_BK)` — the finest foliation not being the
   chain would cost the ceiling argument its anchor.
3. Any `f` and `S` with `<f, Q_S f> > ((n−1)/2)E_BK(f)` — the inequality running the wrong way.
4. An incomparable pair with `P(adj) > 2·min(p, 1−p)`, breaking the swap bijection.

Each is checked here and each returns 0 at the populations named. **None of them is checked
beyond `n = 6`,** and §4.2's Steps 1–3 are a proof rather than an induction on `n`, so the
`n`-uniform claim rests on that proof and not on the enumeration.

---

## 8. Predictions scoreboard, and defects of my own

`PREDICTIONS.md` was committed at `8b07335`, before the instrument existed, **with the exposure
disclosed**: I derived the answer on paper first and ran a scratch probe at `n = 4, 5`
exhaustive, so **P1–P4 are reports at zero credit** and only P5–P9 were live.

| # | claim | p | outcome |
|---|---|---|---|
| P5 | ceiling attained at every `k` at `Z_n`, both directions exact | 0.85 | **HIT** (4 360 pairs) |
| P6 | `mg-409a`'s proof generalises only to `k−1`, above the bar from `k = 4` | 0.80 | **HIT** (2.18 at `k = 5`) |
| P7 | `k_max = n−1`, `k_min = 2`, `k = 2` partition unique | 0.90 | **HIT** (`n = 3..12`) |
| P8 | `alpha_k` rises strictly at a **majority** of posets | 0.70 | **LOSS — 92 of 434 (21 %)** |
| P9 | the operator inequality is strict somewhere | 0.85 | **HIT** (2 789 of 5 184) |

**P8 is the one worth having.** I over-estimated how often refinement actually moves `alpha`;
it usually does not move it at all. That makes the derivation's mechanism *weaker* than I
expected while making its conclusion no more wrong, and it is the only place my priors were
tested rather than reported.

**Defects of my own, kept.**

- **D1** — my first `k1_counting.py` recomputed `max(ks)` inside a generator over 115 975
  partitions: quadratic, and it hung for over three minutes before I killed it — **inside the
  arm whose entire subject is counting.** Caught by timing, not by any check.
- **D2** — my first `k0.7` control was written `verdict(lhs != wrong or True, ...)`: a row that
  **cannot fail**, planted inside the gate whose job is to catch exactly that. Caught by
  re-reading my own diff before committing, not by any arm. Same shape as `mg-06d1`'s D2 and
  `mg-17aa`'s whole subject, committed by someone who had read both.
- **D3** — **P8 lost.** See above.
- **D4** — populations. `k2`/`k3`'s exact PSD arms skip posets with `|L(P)| > 130` (8 skipped,
  counted and printed); `k5` caps at `|L(P)| ≤ 34`. Every table names its population. `n = 5`
  is exhaustive **only** in `k4.3`, which is the arm that carries the ceiling.
- **D5** — `k1`–`k5` share one library, mine, and are therefore **not independent witnesses of
  each other**. `lib409a` and `lib8bc7` are imported by `k0` only. Same shape as `mg-409a`'s D5
  and `mg-8bc7`'s D6, recorded because it applies here too.
- **D6** — floats. `k3.3` and all of `k5` are Jacobi. No verdict rests on them; the exact
  statements are `k2.1`, `k2.2`, `k3.1`, `k4.1`, `k4.3`, `k4.4`, `k4.6`.
- **D7** — **my witness is not new.** `f_xy` is Theorem E's test function and `mg-409a` already
  uses it at L1/L2 to cap `alpha` at `k = 2`. What is mine is Step 1 — *why it is blind to `k`*
  — and the composition with monotonicity. Disclosed as H2 in `PREDICTIONS.md` before the
  instrument existed.

---

## 9. Not done here

`docs/imports/compression.tex` is not edited (its README reserves that directory for verbatim
copies). **`STATE.md` is not touched.** `mg-409a`'s and `mg-8bc7`'s instruments are not
modified — they are imported read-only by `k0` as cross-checks. Theorem E is not re-proved; its
statement is read from `mg-409a` §2. `λ_std` is not computed anywhere in this directory. The
`k = 2` route is not re-opened and no claim here contradicts `mg-409a`: this document
**generalises** its ceiling and reproduces its number.
