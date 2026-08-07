# `mg-76b2` — predictions for the ATTACK ON `C₃`

**Committed before any other file in this directory exists.** Nothing here has been run. The
population, the arithmetic and the verdicts below are what I expect *before* the machine gets a
vote; misses are to be kept as written and scored in the instrument's `README`.

The ticket asks for one of three things: a usable upper bound on `C₃`; a proof that no bound of the
needed strength follows from the source conjecture as worded; or a demonstration that `ε_dem` is
reachable **without** `C₃` at all. I am going for the third, and the first two fall out on the way.

---

## 0. Hand measurements — DISCLOSED, NOT PREDICTED

These are things I already know by hand, from reading the source and the corpus, before any script
exists. They are **not** predictions and must not be scored as hits. They are recorded here so that
a later reader can tell what the instrument confirmed from what it merely re-printed.

| # | hand measurement | where it came from |
|---|---|---|
| **H1** | For `f = 1_{A_k} − (k/n)·1`, the energy is `‖f‖² = k(n−k)/n` and `⟨f,(I−S_P)f⟩ = k·Φ_P(A_k)`, so the prefix Rayleigh quotient satisfies **`1 − ρ(A_k) = n·Φ_P(A_k)/(n−k)`**, hence `Φ ≤ 1−ρ ≤ 2Φ` for `k ≤ n/2`. Derived by hand. | pencil, from the source's own definitions `:229–237`, `:270–278`, `:299–303` |
| **H2** | The hard half of Cheeger is *proved by sweeping*: median-shift `v`, split into `g₊/g₋`, Cauchy–Schwarz + coarea on `h²` gives a **threshold set** `S` of `v` with `|S| ≤ n/2` and `Φ(S) ≤ √(2(1−λ_std))`. Written out by hand. | standard; the source quotes only the inequality `:317–324`, not the sweep |
| **H3** | Under the LITERAL prefix-capture reading `ρ ≥ c·λ_std`, the chain closes **iff** `c ≥ (1−ε_leak)/(1−ε_spec)`. At the repaired calibration `ε_leak ≈ 0.20`, `ε_spec ≈ 2×10⁻²` this is `0.80/0.98 = 0.816326…`. | arithmetic, by hand |
| **H4** | At the SUPERSEDED calibration `ε_leak ≈ 0.02`, `ε_spec ≈ 2×10⁻⁴` the same threshold is `0.98/0.9998 = 0.980196…`. | arithmetic, by hand |
| **H5** | `STATE.md:164` (mg-345e's row) already says *"the live `ε_spec ≲ 2×10⁻²` is the `C₃ = 1` value and `C₃ ≥ 1`, so the omission runs **optimistic**"*. So the corpus's live headline constant is already the `C₃ = 1` number. | read, by hand |
| **H6** | The source's own remark `:328–332` reads: *"Cheeger theory does not by itself imply that the cut is a prefix. That requires monotonicity of the dominant standard eigenvector in the distinguished order, or a direct prefix theorem."* — the source names monotonicity as what supplies the prefix, and attaches **no loss** to it. | read, by hand |
| **H7** | `lib2de0.E_leak(A)` computes `|A| − |A ∩ set(p[:|A|])|`, i.e. it uses the first `|A|` **positions** rather than the positions indexed by `A`. That is the right quantity when `A` is a prefix and looks wrong otherwise; `phi_star()` calls it on every subset. Read, not run. | read, by hand |
| **H8** | Antichain: `T_P = (1/n)J`, so `S_P|_H = 0`, `1−λ_std = 1`, and `Φ_P(A) = (n−|A|)/n` for every `A`. | pencil; also `Op-Form §4.2` |
| **H9** | `ε_leak = 0.20 ⟹ ε_dem = ε_leak²/2 = 2×10⁻²`, and `2/(n+1) ≤ 2×10⁻² ⟺ n ≥ 99`. | arithmetic, by hand |
| **H10** | Under the GAP-form repair the Cheeger square is not spent, so the relation is `ε_spec ≤ ε_leak/C₃`, giving `n ≥ 2C₃/ε_leak − 1 = 10C₃ − 1` — a factor `2/ε_leak = 10` below the ticket's `100C₃ − 1`. | arithmetic, by hand |

**`ε_leak = 0.20` is the value used everywhere below**, per the ticket's instruction to say which. It
is `mg-e35c F5`'s repaired figure and it is **empirical** (mg-3ce3's envelope), so every number
derived from it inherits HEURISTIC status. The symbolic forms are kept beside the numbers.

---

## 1. Population

`P76B2` := every poset on `{0,…,n−1}` for which the identity is a linear extension (so `e` = the
distinguished order is fixed by the labelling), `n = 2…6`, enumerated exhaustively; plus named
families to `n = 7`. This is the same population shape `lib2de0.all_posets` uses, but the library
is **written from scratch for this ticket and shares no code with `lib2de0`** — H7 is one reason.

I expect `|P76B2(6)| = 4824` (mg-c4f5 reports `4,824 at n=6` for what I believe is the same
population). **P0: that count reproduces.** *(60% — I may be misreading which population that
figure counts.)*

---

## 2. Predictions

Each carries a confidence. Anything below 50% is a bet against myself.

| # | prediction | conf. |
|---|---|---|
| **P1** | The dictionary identity `1 − ρ(A_k) = n·Φ_P(A_k)/(n−k)` (H1) holds with **0 exceptions** over every poset in `P76B2` and every `1 ≤ k ≤ n−1`, in exact arithmetic. | 97% |
| **P2** | `Φ_P(A_k) ≤ 1 − ρ(A_k) ≤ 2·Φ_P(A_k)` for every `k ≤ n/2`, **0 exceptions**; and the upper factor `2` is **attained in the limit only**, i.e. no poset attains `1−ρ = 2Φ` exactly for `n` odd. | 90% / 55% |
| **P3** | `1 − λ_std = 0` happens on a **large** sub-population, not just chains — specifically on **exactly** the ordinal-sum-decomposable posets (those with some `k` where `A_k` is an exact cut). 0 exceptions in both directions. | 85% |
| **P4** | Consequently `C₃` in **every** currency is `0/0` on that sub-population, and the honest population for any `C₃` measurement is the **primitive** (ordinal-sum-indecomposable) posets. I expect the primitive fraction at `n=6` to be **under 50%**. | 70% |
| **P5** | The conductance-currency loss `C₃^cut := Φ*_pref / Φ*` (min over prefixes ÷ min over all cuts) is `= 1` for most primitive posets but **not all**: there is at least one primitive poset at `n ≤ 6` with `C₃^cut > 1`. | 85% |
| **P6** | `max C₃^cut` over primitive posets **grows with `n`** across `n = 4,5,6` (weakly monotone, strictly at least once). If it does, that is a **negative** result for the conductance reading of L3 and I will report it as one. | 60% |
| **P7** | The dominant standard eigenvector is monotone in `e` for the overwhelming majority of primitive posets but **not all** — at least one non-monotone witness at `n ≤ 6`. | 70% |
| **P8** | The top standard eigenvalue is **degenerate** (multiplicity ≥ 2) for at least one primitive poset in `P76B2`, so "*the* dominant standard eigenvector" is not well defined there, and the monotonicity verdict at those posets depends on which eigenvector the routine happens to return. | 65% |
| **P9** | **Every** poset in `P76B2` has `1 − λ_std > 2×10⁻²` or `= 0` exactly — i.e. **no** poset in the population sits inside the regime the budget describes, so every `C₃` number this instrument prints is measured **outside** the regime it would be used in. I will print that sentence next to every `C₃` figure. | 90% |
| **P10** | The literal-reading capture fraction `c(P) := max_k ρ(A_k)/λ_std` falls **below** the `0.8163…` threshold of H3 on at least one primitive poset, so the literal form is not automatically satisfied even where it is not vacuous. | 75% |
| **P11** | H7 is a real defect: I will produce an explicit `A` and poset where `lib2de0.E_leak(A)` differs from `E|A∖σ(A)|`. **Noted, not repaired** — it is mg-2de0's file. | 80% |
| **P12** | The theorem **C₃ = 1 given L2** survives every red drill: on every poset whose dominant standard eigenvector *is* monotone, the sweep produces a prefix-or-suffix cut `S` with `Φ(S)² ≤ 2(1−λ_std)`, 0 exceptions, and the corresponding prefix `A_k` satisfies `Δ₁(A_k, A_kᶜ) = Φ(S)`. | 88% |

---

## 3. My two most likely errors, filed in advance

**P13 — the suffix branch.** The sweep's `g₊` branch produces a **suffix**, not a prefix. I claim
that is harmless because `|A∖σ(A)| = |Aᶜ∖σ(Aᶜ)|` for every `σ`, so `Δ₁` reads the same on both sides
and Step 5's `E K_k ≪ min(k,n−k)` is symmetric under `k ↦ n−k`. **I bet 15% that this is wrong** —
that the identity fails, or that Step 5 wants the prefix specifically for a reason downstream of the
number. If it breaks, the theorem needs the `g₋` branch alone and the median argument has to be
redone. The instrument checks the set identity exhaustively rather than assuming it.

**P14 — the currency conflation, committed by me this time.** `Op-Form §4.3` states
`ε_spec ≤ ε_leak²/(2C₃)`; I claim (H10) that under the **gap-form** repair the Cheeger square is not
spent and the right relation is `ε_spec ≤ ε_leak/C₃`. The risk is that I have talked myself into
dropping a square that the chain really does need — the exact shape of the error this lineage has
already made twice with L4. **I bet 25% that at least one reviewer reads §4.3's composite as
correct under a reading I have not enumerated.** I will enumerate all three chains explicitly and
label which relation belongs to which, rather than asserting one of them is *the* relation.

---

## 4. What I am NOT doing

- **No L4 attempt.** mg-345e settled that Step 6 consumes no branch in which L4's modulus appears;
  an L4 result does not discharge this and I will not produce one.
- **No `ε_sup` derivation.** That is mg-6bc2 and it landed at `e1f7bb2`.
- **No assumption of the mg-200d conjecture.** `2/(n+1)` appears only where I am converting a `C₃`
  value into the finite window the ticket asks to be sized, and it is labelled as that conjecture's
  consequence at every site.
- **No edit to `STATE.md`.** `STATE.md:164` is mg-345e's row and `STATE.md:15` is row 8; both are
  pm-onethird's. The correction to H5's rider is written as a **proposal** and mailed, not landed.
- **No repair to `lib2de0`.** H7/P11 is reported and left where it is.
