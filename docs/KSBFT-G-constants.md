# KSBFT-G — the constants: `K`, `L* = L(K+1, 1/6)`, `L(4, 1/6)`

`mg-b852`, 2026-09-26. Paper: Aires, Chan, Pak, Panova, *Breaking the Infinite Barrier in the
1/3–2/3 Conjecture* (`/Users/daniel/files/KSBFT_v7.pdf`, 2026-09-25, **not in this repository**).
AK25b = arXiv:2510.26134v1 (Aires–Kahn, *Variance vs. range for linear extensions, and balancing
extensions in posets of bounded width*, 11 pp.), **read in full from arXiv**. AK25a
(arXiv:2509.11549) and Haq26 (arXiv:2608.12678) were fetched and **not needed**: `K` is arithmetic
on KSBFT's own printed §6.4 display, and `L` comes from AK25b alone.
Instrument: [`code/ksbft_g_constants_b852/`](../code/ksbft_g_constants_b852/) (`./run_all.sh`,
about 2 s, `decimal` arithmetic because `L*` has about 10²⁹ digits). **`STATE.md` was not edited and
no ticket was closed. Every verdict is a recommendation to pm-onethird.**

Marks:

- **EXPLICIT** — a number with its derivation in this document.
- **ORDER-OF-MAGNITUDE** — a bound on the exponent's shape, with the argument.
- **PROVEN** — the proof is in this document. **CITED** — read in a paper and not re-derived.
- **EMPIRICAL** — the instrument and range are named. **CONJECTURED** — a belief.

---

## 0. Verdict

> **Every constant is now a number. `L*` is tower-free but doubly astronomical:
> `log₁₀ L* ≈ 1.05×10²⁹`. The width-3 window runs to `≈ 10¹¹⁹`. Nothing here is within reach of
> computation, and the `L*`-route consequences are all dominated by mg-c929's `C ≈ 3×10¹⁷`.**

| constant | value | mark | depends on |
|---|---|---|---|
| `K` (Thm 1.4 as stated, `ε = 10⁻¹⁰⁰`) | **`2.17×10⁴¹¹`** (`log₁₀ = 411.337`) | EXPLICIT (arithmetic on KSBFT's printed §6.4 formula) | KSBFT §6 (AK25a, Haq26) |
| `K₀` (counterexample width, deficit `1/e − 1/3`) | **`1.301×10¹⁴`**, recomputed and equal to mg-c929 | EXPLICIT | same, plus mg-c929 (audited HOLDS, mg-e015) |
| `K₁₂` (the best deficit usable for Thm 1.2, `1/e − C_BFT`) | `1.944×10¹²` | EXPLICIT | same |
| `L(4, 1/6)` (width ≤ 3) | **`≤ 10^119.1`** | EXPLICIT upper bound, cond. on AK25b being correct as written (§3) | AK25b only |
| `L(3, 1/6)` (width ≤ 2) | `≤ 10^87.9` | EXPLICIT, same conditions | AK25b only |
| `L* = L(K₀+1, 1/6)` | **`≤ 10^(1.050×10²⁹)`** | EXPLICIT, same conditions | AK25b + mg-c929's `K₀` |
| `L*` with the paper's `K` | `≤ 10^(10^823.47)` | EXPLICIT, same conditions | AK25b + KSBFT §6 |
| shape of the route's `L(w, ε)` | `2·w²·log₁₀(1/2ε) ≤ log₁₀ L ≤ 13·w²·log₁₀(1/2ε) + O(log w)` | ORDER-OF-MAGNITUDE (PROVEN for this route, §3.8) | AK25b |

**The five findings.**

1. **`L` is single-exponential in `K²`, not a tower (PROVEN by trace, §3).** AK25b's proof has two
   halves. Thm 1.5, via Thm 2.6, gives every element `q(x) ≥ q₀ = (2ε)^{w²}`. This is the only place
   `ε` and `w` enter. Thm 1.3 (`π ⇝ σ`) is **polynomial** in `1/q₀`. Its degree is about 13, from
   Lemma 4.4 (`η⁻²`), the window (17) (`η⁻¹·⁵`), the ratio chain (`η⁻²`), and one more `η⁻¹`, with
   the whole thing squared. So `log₁₀ L ≈ 6.2·w²` at `ε = 1/6`.
2. **Fixing `ε = 1/6` buys nothing structural (PROVEN, §4).** `ε` enters only through the base `2ε`
   of `(2ε)^{w²}`. The whole Thm 1.3 half is `ε`-free. The cost is the **`w²` in the exponent of
   Thm 2.6**, and the proof has no other `w`. A polynomial version of Thm 2.6 would make
   `L* = poly(K₀)`. I could not prove one, nor refute it (§4, negatives).
3. **Width 3: `7 ≤ π ≤ 10¹¹⁹`, and not by any computation (§5.3).** A poset of range `10¹¹⁹` has
   more than `10¹¹⁹` elements. The window is also not a finite check at any range, because `n` is
   unbounded (KSBFT-C §2.9).
4. **`n₀ = 50L* + 1 ≈ 10^(1.05×10²⁹)`, and it is obsolete (§5.1).** On the height order `h`, which is
   a linear extension, both bounds apply. mg-c929's `E[inv_h] ≤ C·n` with `C = 2.964×10¹⁷` beats
   `n·L*/2` by a factor of `10^(1.05×10²⁹)`, and it needs one preprint fewer (no AK25b).
5. **KSBFT eq. (1.5) is NOT REPRODUCED and looks inconsistent with the route as printed (§6).**
   `ε = 3^{−3^{1.6×10¹⁹}}` implies a range cutoff `L` with `log₃ L ≈ 1.6×10¹⁹`. The best route
   through AK25b, at the smallest width bound §6 can supply (`K₁₂ = 1.94×10¹²`), has an
   **unavoidable floor** of `log₃ L ≥ 2·0.732·K₁₂² ≈ 5.5×10²⁴`. That floor would need a width bound
   of about `3×10⁹` to fit. Using mg-f218 instead (if its audit holds), Thm 1.2's constant becomes
   `ε ≈ 10^(−1.7×10²⁵)`: single-exponential, and far larger than (1.5).

---

## 1. `K` — EXPLICIT

KSBFT p.25, last display of §6.4: `w(P) ≤ (2√3/ε)·gap(P) ≤ (442368/ε⁴)·log²(18432√3/ε³)`, natural
log. The instrument evaluates both the printed closed form and mg-c929's `G = max(G₁, 4A log² A)`
form, and they agree:

| deficit `ε` | width bound | use |
|---|---|---|
| `10⁻¹⁰⁰` | `2.17×10⁴¹¹` | Thm 1.4 as stated (`δ > 1/e − 10⁻¹⁰⁰`). |
| `1/e − 1/3 = 0.03455` | `1.301×10¹⁴` | counterexample width (mg-c929). **Use this for `L*`.** |
| `1/e − C_BFT = 0.09149` | `1.944×10¹²` | Thm 1.2's case (a) needs only `δ > C_BFT + ε`, so strictly a hair less than this deficit. |

At `ε = 10⁻¹⁰⁰`: `442368·10⁴⁰⁰ = 4.42×10⁴⁰⁵` and `ln(31925·10³⁰⁰) = 700.6`. The square is
`4.91×10⁵`, and the product is `2.17×10⁴¹¹`. The "`≳ 10⁴⁰⁰`" in the shared context is right as
stated and is the wrong `K` for the conjecture.

**Dependency.** Every number in this document except `L(4,1/6)` and `L(3,1/6)` uses `K₀`, and so
depends on mg-c929 (audited, Prop B HOLDS, mg-e015). The paper-`K` figures are printed alongside for
readers who do not want that dependency.

---

## 2. What KSBFT Thm 1.5 actually imports

AK25b Thm 1.6 is: "For fixed `w` and `P` of width at most `w`, if `π(P) → ∞` then `δ(P) → 1/2`."
KSBFT Thm 1.5 restates it with `w(P) < K`. So **`L(K, ε) = L_AK(w = K − 1, ε)`**. `L* = L(K₀+1, 1/6)`
is the width-`≤ K₀` case. `L(4, 1/6)` is width `≤ 3`.

AK25b proves Thm 1.6 as **Thm 1.5 + Thm 1.3**:

- **Thm 1.5 / 2.5 / 2.6 (easy half).** At bounded width, an element unbalanced against everything
  has a position distribution with a heavy atom: `q(x) := max_k P(f(x) = k)` is bounded below.
  Stanley log-concavity (Thm 2.2) plus Prop 2.3 turns that into bounded `σ(x)`.
- **Thm 1.3, `π ⇝ σ` (hard half, §§3–4).** Large range forces some `σ(x)` to be large. It is proved
  via Thm 3.1 (maximal incomparable pair `(A, B)`), reduced to Thm 3.2 on width-2 unidirectional
  posets, which is proved in §4 with Graham–Yao–Yao (Thm 4.1) and lattice-path counting.

The paper states everything with `O(·)`, `Ω(·)`, "large enough", and "pretend large numbers are
integers". **§3 below assigns every constant.** Where AK25b writes `≈` or leaves a step "routine", I
say so and state the choice I made.

**The contrapositive being quantified.** Suppose `w(P) ≤ w` and `δ(P) ≤ 1/2 − ε`. Show
`π(P) < L_AK(w, ε)`.

---

## 3. The trace — `L_AK(w, ε)` explicitly

### 3.1 Heavy atom: `q(x) ≥ q₀ := (2ε)^{w²}` for every `x` — PROVEN (re-derived from AK25b Thm 2.6)

`δ(P) ≤ 1/2 − ε` gives `δ_x ≤ 1/2 − ε` for every `x`. So each `y ≠ x` has one of `P(y ≺ x)`,
`P(x ≺ y)` at least `1/2 + ε`. Let `D = {y : P(y ≺ x) ≥ 1/2+ε}` and `U = {y : P(x ≺ y) ≥ 1/2+ε}`.

- `P = {x} ⊔ D ⊔ U`.
- `D` is an ideal: `z < y ∈ D` gives `P(z ≺ x) ≥ P(y ≺ x)`. Dually, `U` is a filter.
- `A = max D` and `B = min U` are antichains, so `|A|, |B| ≤ w`.
- For `a ∈ A` and `b ∈ B`, `P(a ≺ x ≺ b) ≥ 1 − (1/2−ε) − (1/2−ε) = 2ε`.

AK25b Thm 2.6 has two XYZ applications (Shepp). First, `P(x ≺ B | a ≺ x) ≥ ∏_b P(x ≺ b | a ≺ x)`,
where the conditioned measure is uniform on `E(P + {a<x})`. So
`P(a ≺ x ≺ B) ≥ (2ε)^{|B|}·P(a≺x)^{1−|B|} ≥ (2ε)^{|B|}`. Second, the same step over `a ∈ A`
conditioned on `x ≺ B` gives `P(A ≺ x ≺ B) ≥ (2ε)^{|A||B|} ≥ (2ε)^{w²}`. Every element of `D` lies
below some element of `A`, and every element of `U` lies above some element of `B`. So
`{A ≺ x ≺ B} = {f(x) = |D|+1}`, and `q(x) ≥ (2ε)^{w²}`. □

At `ε = 1/6`: `q₀ = 3^{−w²}`.

### 3.2 Prop 2.3 with a constant: `Var X ≤ 294/q²` for integer log-concave `X` — PROVEN

AK25b says only `O(q⁻²)`, and "we unfortunately don't know a reference". Here is a constant.
`X` is integer-valued with log-concave, no-internal-zero mass `p` (the support of `f(x)` is an
interval), mode `k₀`, and `p_{k₀} = q`.

- **Right side.** Let `j` be the first `k > k₀` with `p_k < q/2`, and put `a = j − k₀`. The masses
  `p_{k₀}, …, p_{j−1}` are each `≥ q/2`, so `a ≤ 2/q`. The ratios `r_k = p_{k+1}/p_k` are
  nonincreasing. Their product over `k₀ ≤ k < j` is `p_j/q < 1/2`, so
  `r_{j−1} < 2^{−1/a} =: ρ`. Hence `p_{j+t} < (q/2)ρ^t`.
- **The bound.**
  `Σ_{k≥k₀}(k−k₀)²p_k ≤ q·a³/3 + (q/2)Σ_t (a+t)²ρ^t`. Use `(a+t)² ≤ 2a²+2t²`,
  `Σ t²ρ^t ≤ 2/(1−ρ)³`, and `1 − 2^{−1/a} ≥ 1/(2a)` (by concavity of `1 − 2^{−x}` on `[0,1]`).
  The sum is then `≤ 36a³`. So the right side is `≤ 8/(3q²) + 18qa³ ≤ 8/(3q²) + 144/q² < 147/q²`.
  If no `j` exists, only the first term appears.
- **Left side.** Symmetric. So `Var X ≤ E(X−k₀)² < 294/q²`. □

The instrument uses `300`. EMPIRICAL sanity check: the largest `Var·q²` over geometric, binomial,
uniform and triangular test laws is `0.999`. A non-log-concave negative control gives `2.5×10⁹`
(FIRES).

**Easy direction (PROVEN).** For any integer `X` with `max p ≤ q ≤ 1/4`, put `t = 1/(4q)`. Then
`P(|X−μ| < t) ≤ q(2t+1) ≤ 3/4`, so `Var X ≥ t²/4 = 1/(64q²)`. EMPIRICAL: the minimum of `Var·q²` is
`0.083 ≥ 1/64`.

So under the hypothesis, **`σ²(x) ≤ S := 300/q₀²` for all `x`**.

### 3.3 From Thm 3.1 to a range bound — PROVEN

Choose an incomparable pair `(A, B)` with `|A||B|` maximum and `|B| ≥ |A|`. It is a maximal 1-pair,
and `|A||B| ≥ 1·π(P)` (take `A = {x}` and `B = Π(x)`). AK25b Thm 3.1 at `(µ, L) = (1, S+1)` says:
if `|B| ≥ K₃.₁` then `Σ_{x∈A} σ² ≥ (S+1)|A|`, so some `σ²(x) > S`. That is a contradiction. Hence
`|B| < K₃.₁` and **`π(P) ≤ |A||B| ≤ |B|² < K₃.₁²`**. So `L_AK = K₃.₁(1, S+1)²`.

The proof of Thm 3.1 from 3.2 (AK25b p.5–6) applies Thm 3.2 to `(A′, B′)`, with
`|A′| ≥ |A|/2` and `|B′| ≥ |B|/2`, at `(µ/4, 2L)`. So `K₃.₁ = 2K₃.₂(1/4, 2(S+1)) + 2`, where the
`+2` covers parity.

Inside Thm 3.2 (`µ = 1/4`, `L′ = 2(S+1)`), AK25b chooses `η` with `q(x) ≤ η ⟹ σ²(x) ≥ 2L′`. By the
easy direction, **`η = 1/(16√(S+1)) ≈ q₀/277`**.

### 3.4 Thm 3.2's internal constants — PROVEN given AK25b's steps as written

Notation: `N = |{y ≤ max B}|` and `M = |{x ≥ min A}|` (AK25b p.8).

| AK25b step | what it needs | constant chosen | why it suffices |
|---|---|---|---|
| (17) | `P(Ψ_{i,j}) > η ⟹ P(|g(x_i) − j| < D) > 1 − η/4` | **`D = 3·√300/η^{1.5}`** | `q(x_i) > η` gives `σ ≤ √300/η` (§3.2). If `|j − Eg| ≥ σ/√η`, Chebyshev gives `P(g=j) ≤ η`, a contradiction. And `P(|g−Eg| ≥ 2σ/√η) ≤ η/4`. |
| (22) | `E[g(x_{i_{k+1}}) − g(x_{i_k})] ≥ γ·Δi` | **`γ = 3µ³/160`** | Case `j_{k+1} ≥ N/2`: `(j′−j)/(i_{k+1}−ℓ) ≥ (N/8)/(5M/µ) ≥ µ³/40`, using `N ≥ µ²M` and `N ≥ 8D`. Weight `P(g = j_{k+1}±D) ≥ 3/4` by (17), and `g` is monotone on `X`, so dropping the rest is valid. Case `j_{k+1} ≤ N/2`: `(N−j)/(m−i_k+1) ≥ (N/4)/M ≥ µ²/4`, times `3/4`. Minimum is `3µ³/160`. AK25b says "roughly `µ³`". |
| (19) | `r_k ≥ γ′` | `γ′ = γ/2`, with `C ≥ 4D/γ` | `j_k = Eg(x_{i_k}) ± D`, so `r_k ≥ γ − 2D/C`. |
| Lemma 4.4 | `j, n−j > K₄.₄` and `(n−j)/(m−i) < (1+1/K₄.₄)·j/i ⟹ P(Ψ_{i,j}) < ε′` | **`B = ⌈e/ε′⌉`, `K₄.₄ = (3B+1)(B+1)`** | §3.5 |
| (20) | `T/D > 4K₄.₄(η/2)` and `T > 5D` | **`T/D = 4K₄.₄(η/2) + 1`**, `T = γ′C`, so **`C = 2(4K₄.₄+1)D/γ`** | AK25b p.9. The local chain sizes are `≥ T − D > K₄.₄`. |
| (21) | `r_k < 3/η` | — | AK25b p.10. Needs `C > 3D`, which holds. |
| (18) | `t = O(1)` | **`t ≤ 2 + 2(T/D)·ln(6/(γη))`** | `γ′(1+D/T)^{t−2} < 3/η`, and `ln(1+x) ≥ x/2` for `x ≤ 1`. |
| (13) | `|A| ≥ 2|I|`, with `|I| ≤ 2Ct` | **`K₃.₂ = 80·C·t/(ηµ²)`** | Case 2 has `N < 20M/(ηµ)`. So `|A| ≥ µM > ηµ²N/20 ≥ ηµ²K₃.₂/20 ≥ 4Ct`. Case 1 (`N ≥ 20M/(ηµ)`) needs no lower bound on `K`. |

### 3.5 Lemma 4.4 with a constant — PROVEN

After AK25b's reduction to `P = X + Y` with the single relation `x_i < y_{j+1}`, (12) gives the
ratio `R(ℓ) = P(Ψ_{i,ℓ−1})/P(Ψ_{i,ℓ}) = (1 + (m−i)/(n−ℓ+1)) / (1 + (i−1)/ℓ)`.

Put `a = (m−i)/(n−j)` and `b = i/j`. The hypothesis says `a > b/(1+1/K) ≥ b(1−1/K)`. For
`ℓ ∈ (j−B, j]`, with `j, n−j > K` and `B/K ≤ 1/2`:

- `(m−i)/(n−ℓ+1) ≥ a(1 − B/K)`
- `(i−1)/ℓ ≤ b(1 + 2B/K)`

So `R ≥ [1 + b − b(B+1)/K] / [1 + b + 2bB/K] ≥ 1 − (3B+1)/K ≥ 1 − 1/(B+1)` when
`K ≥ (3B+1)(B+1)`. Then `Ψ_{i,j}, …, Ψ_{i,j−B}` are `B+1` disjoint events, each with probability
`≥ (1 − 1/(B+1))^B·P(Ψ_{i,j}) > P(Ψ_{i,j})/e`. So `P(Ψ_{i,j}) < e/(B+1) ≤ ε′`. □

EMPIRICAL:

- (12) matches exact binomial path counts for every `m < 40` and `n < 60` (0 mismatches). A
  deliberately wrong (12) mismatches (FIRES).
- The bound `R ≥ 1 − 1/(B+1)` holds on 59,992 random near-boundary instances at `B ∈ {2, 5, 20}`.
- With `K = B+1` in place of `(3B+1)(B+1)`, there are 122,986 violations (FIRES).

### 3.6 The numbers — EXPLICIT (cond. on AK25b), from `out_constants.txt`

| case | `log₁₀(1/q₀)` | `log₁₀(1/η)` | `C` | `t` | `K₃.₂` | **`log₁₀ L`** |
|---|---|---|---|---|---|---|
| width ≤ 2, `ε = 1/6` | 1.91 | 4.35 | `2.1×10²³` | `7.1×10¹²` | `4.4×10⁴³` | **87.9** |
| **width ≤ 3, `ε = 1/6`** (`L(4,1/6)`) | 4.29 | 6.74 | `4.8×10³¹` | `5.4×10¹⁷` | `1.8×10⁵⁹` | **119.1** |
| **width ≤ `K₀` = 1.301×10¹⁴** (`L*`) | `8.08×10²⁷` | `8.08×10²⁷` | `10^(2.83×10²⁸)` | `10^(1.62×10²⁸)` | `10^(5.25×10²⁸)` | **`1.050×10²⁹`** |
| width ≤ `2.17×10⁴¹¹` (paper `K`) | `10^822.35` | same | — | — | `10^(10^823.17)` | **`10^823.47`** |
| width ≤ `K₁₂`, `ε = 1/2 − C_BFT` (Thm 1.2) | `1.32×10²⁴` | same | — | — | — | **`1.717×10²⁵`** |

For width 2, AK25b's own Remark (p.4) gives the sharper `q(x) ≥ ε`, not `(2ε)⁴`. That would shrink
the width-2 row. I did not redo it, since the conjecture is known at width 2 (Linial).

### 3.7 Caveats on "EXPLICIT" — stated so an auditor can attack them

1. **Conditional on AK25b being correct.** I traced constants through its reductions, but I did
   **not** re-prove its structural steps. That means the Thm 4.1 monotonicity reductions in Lemmas
   4.3 and 4.4, the dualisation in Thm 3.1's proof, Observation 4.2, and (7). I re-derived Thm 2.6
   (§3.1), (12), and Lemma 4.4's calculation (§3.5).
2. **AK25b's approximations.** AK25b writes `T ≈ µ³C`, `N/4 − D ≈ N/4`, and "pretend large numbers
   are integers". I replaced each with an explicit inequality: `N ≥ 8D`, and factors of 2 for
   halving and parity. Each such fix changes `L` by at most a constant factor in `K₃.₂`, which is a
   few units in `log₁₀ L(4,1/6)` and invisible in `log₁₀ L*`.
3. **Loose choices.** Chebyshev in (17) could use log-concave exponential tails. That gives
   `D = O(log(1/η)/η)` instead of `η^{−1.5}`, and the degree 13 becomes about 12 (`log₁₀ L* ≈
   9.7×10²⁸`). Prop 2.3's `294` is surely far from sharp: the test families give `≤ 1`.

### 3.8 ORDER-OF-MAGNITUDE: the shape is forced for this route — PROVEN

- **Lower bound.** `K₃.₂ ≥ 80Ct/(ηµ²) > 1/η` and `η < q₀`, so the route's `L = K₃.₁² > q₀⁻²`.
  That is `log₁₀ L > 2w²·log₁₀(1/2ε)`, which at `ε = 1/6` is `0.954·w²`.
- **Upper bound.** §3.4 gives degree `≤ 13` in `1/η`, plus logs.
- **So for any honest bookkeeping of this route, `log₁₀ L* ∈ [1.6×10²⁸, 1.05×10²⁹]`, and
  `log₁₀ L(4,1/6) ∈ [8.6, 119]`.** At width 3 the *floor* is small, so the bookkeeping matters a
  lot there. At width `K₀` the `K₀²` dominates everything.

---

## 4. Q3 — a better dependence at fixed `ε = 1/6`? A cheaper route in case (b)?

**Fixing `ε` does not help (PROVEN, from §3).** `ε` appears only in `q₀ = (2ε)^{w²}`. Everything
after §3.1 is a function of `q₀` alone. "`1/2 − ε`" versus "`1/3`" changes only the base: `1/3` at
`ε = 1/6`, and `0.447` at Thm 1.2's `ε = 1/2 − C_BFT`. The damage is the **`w²` exponent**, and
`w = K₀ ≈ 10¹⁴`. Aiming at `1/3` rather than `1/2 − ε` is already the cheapest version of AK25b.

**What would help, stated precisely (CONJECTURED as a route).** A bound of the form
`q(x) ≥ (ε/w)^{O(1)}` whenever `δ_x ≤ 1/2 − ε` at width `≤ w` would make, by §3,
`L* = K₀^{O(1)} ≈ 10^{O(14)}`. For width 2 exactly this holds, with `q(x) ≥ ε` (AK25b Remark, p.4).

**Negatives — candidates tried for a better heavy-atom bound, none of which worked:**

1. **Restrict Thm 2.6's product to `A ∩ Π(x)` and `B ∩ Π(x)`.** This is valid, since comparable
   pairs contribute factor 1. But both are still antichains, so the exponent stays `≤ w²`.
2. **Chain decomposition, as in the width-2 Remark.** In each of `w` Dilworth chains, `x` sits in one
   gap with probability `≥ 2ε`. The joint event is exactly `{f(x) = |D|+1}`. Getting a
   *product* of the `w` gap probabilities (`(2ε)^w`, already much better) needs positive
   correlation of two-sided gap events. XYZ gives that only for one-sided events, which is why
   AK25b pays `w²`. I found neither a correlation inequality nor a counterexample. **Whether
   `exp(−Θ(w))` decay of `q` is real is OPEN.** I have no example with `q` exponentially small at
   `δ_x ≤ 1/3`.
3. **Use KSBFT §6's structure (`δ ≤ 1/e − ε₀` ⟹ heights `ε₀/√3`-separated, `d ≤ Δ/ε₀`, bounded
   gap) to bound `σ(x)` directly.** This fails. All §6 inputs are pairwise, and bounding
   `sd(Z_x − Z_y)` says nothing about `Var Z_x` (a floating block moves together). The tail
   (5.2) at `t = Δ/d ≥ ε₀` gives `P ≤ e^{1−ε₀} > 1`, which is vacuous.
4. **Avoid Thm 1.3 by bounding range through width.** Impossible. Two parallel chains have width 2
   and range `n/2` (KSBFT-C §1.1). Range needs AK25b's variance half, and that half is already
   polynomial.

**A cheaper route to 1/3 in case (b): none found.** The only cost-bearing step is §3.1, and all
four attempts above failed to improve it.

---

## 5. Consequences

### 5.1 `n₀ ≈ 50L*`, and the comparison with mg-c929

- **(EXPLICIT, cond.)** With `K₀`: `log₁₀ n₀ = log₁₀(50L* + 1) ≈ 1.050×10²⁹`. With the paper's `K`:
  `log₁₀ n₀ ≈ 10^823.47`.
- **Which `E[inv]` bound is smaller? (PROVEN given both inputs.)** The height order `h` (sort by
  `h(x) = E f(x)`) is a linear extension, because `x ≺ y ⟹ h(x) < h(y)`. So KSBFT-C's F4
  (`inv_e ≤ nL*/2` for **any** reference extension `e`) applies to `inv_h`, and so does mg-c929
  Prop B (`E[inv_h] ≤ C·n`, `C = 2.964×10¹⁷`).
  `(L*/2)/C = 10^(1.05×10²⁹)`. **mg-c929's bound wins by that factor, and it needs AK25a + Haq26
  only, not AK25b.**
- For KSBFT-C's `inv_e` against the majority order `e`, I did **not** check whether mg-c929's `C`
  transfers. So for `inv_e` the `L*` bound is still the only one this document certifies.

### 5.2 Thm 1.2's `ε` under the unaudited improvements — EXPLICIT, conditional

The best route for Thm 1.2 takes case (a) at deficit just under `1/e − C_BFT` (`K₁₂ = 1.94×10¹²`),
case (b) at `ε′ = 1/2 − C_BFT` (`L₁₂ = 10^(1.72×10²⁵)`), and case (c) at `D = L₁₂`.

| case-(c) theorem used | `ε` of Thm 1.2 | status |
|---|---|---|
| paper Thm 1.3, `(D+1)^{−4(D+1)}/4096` | `10^(−10^(1.72×10²⁵))` | cond. AK25a, Haq26, AK25b |
| mg-d707 Thm 1.3′, `(D+1)^{−3(D+1)}/12` | `10^(−10^(1.72×10²⁵))` (same to the shown digits) | + mg-d707 (audit mg-3a14: HOLDS) |
| **mg-f218 Thm 1.3″, `min(6.8e−6, 0.0236/(L+1))`** | **`≈ 10^(−1.72×10²⁵)`** | + mg-f218 (**UNAUDITED**, audit filed) |
| same, for the 1/3 statement at `L*` (`K₀`) | `0.0236/(L*+1) ≈ 10^(−1.05×10²⁹)` | same |

mg-f218 removes one exponential. `ε` is then limited by `L`, exactly as the ticket anticipated.

### 5.3 The width-3 window `7 ≤ π ≤ L(4,1/6)`

**(EXPLICIT, cond. on AK25b alone.)** A width-`≤ 3` counterexample has `7 ≤ π(P) ≤ 10^119.1`. The
lower end is Peczarski (`π ≤ 6`). The upper end is the §3.8 floor/ceiling pair:
`8.6 ≤ log₁₀ L(4,1/6) ≤ 119`, depending on how tightly AK25b's `Ω`'s can be done.

**Within reach of computation? No, only in principle.**

- Even the *floor* `10^8.6` is an element count: range `π` forces `n ≥ π + 1`.
- Exhaustive enumeration stops at `n ≤ 14` (Gup26).
- More fundamentally, for every fixed range `≥ 2`, `n` is unbounded (the Fibonacci family `Z_n`),
  so no range window is a finite check (KSBFT-C §2.9). The window makes width 3 a
  **bounded-range** problem, not a finite one.

A computation could become relevant only if both of these happened:

- **(i)** A polynomial Thm 2.6 plus a tight Thm 1.3 bring `L(4,1/6)` near 10.
- **(ii)** KSBFT-C §3.2's transfer-matrix route (CONJECTURED) makes each fixed range a finite
  computation.

Neither exists.

---

## 6. KSBFT eq. (1.5) — NOT REPRODUCED; inconsistent with the printed route

KSBFT p.2: "Our proof allows us to take `ε := 3^{−3^{16×10¹⁸}}`". The derivation is omitted and was
AI-assisted (p.26).

- **What (1.5) implies.** Case (c) uses Thm 1.3 at `D = L`, with `η_D = (D+1)^{−4(D+1)}/4096`. So
  (1.5) corresponds to `4(L+1)log₃(L+1) ≈ 3^{1.6×10¹⁹}`, i.e. **`log₃ L ≈ 1.6×10¹⁹`**.
- **What the route gives.** With the smallest width bound §6 can supply for Thm 1.2
  (`K₁₂ = 1.94×10¹²`), §3.8's route floor is `log₃ L ≥ 2·log₃(1/0.447)·K₁₂² ≈ 5.5×10²⁴`. My trace
  gives `3.6×10²⁵`. With the paper's own `K = 2.17×10⁴¹¹`, `log₃ L` is about `10^823`.
- **What would reconcile them.** Fitting under `1.6×10¹⁹` needs width `w ≈ 3.3×10⁹` (floor
  coefficient 2) to `4.7×10⁹` (`q₀` alone). **No width bound printed in KSBFT §6 is that small.**
  Coincidentally, `16×10¹⁸ = (4×10⁹)²`, the shape `(width)²` has.
- **Verdict.** The route through AK25b as printed does **not** support (1.5). (1.5) needs either a
  polynomial-exponent Thm 2.6, or a width bound about `10³` times smaller than §6's best (about `10⁴⁰²`
  times smaller than the `K` KSBFT actually uses).
- **Mark: NOT REPRODUCED.** This is consistent with the shared context's "treat eq 1.5 as
  low-assurance". It does **not** threaten Thm 1.2's qualitative statement (`ε > 0`), only the
  printed value. The corrected value on the same route is in §5.2.

---

## 7. What I did not do, and negatives

- I did **not** re-prove AK25b's structural lemmas (§3.7 item 1). `L` is EXPLICIT *conditional on
  AK25b as written*.
- I did **not** read AK25a or Haq26 beyond fetching them. `K` is arithmetic on KSBFT's printed
  formula, and the AK25a/Haq26 dependence is inherited from KSBFT §6 and mg-c929.
- I did **not** audit mg-c929, mg-d707 or mg-f218. Dependence on each is marked: `K₀`, `L*`, `n₀`
  and §5.1 use mg-c929 (audited); §5.2 rows use mg-d707 and mg-f218.
- I did **not** optimise the bookkeeping (log-concave tails, a sharp Prop 2.3, the width-2 Remark).
  §3.8 bounds how much that could move things.
- I did **not** determine the *true* least valid `L(4, 1/6)`. Every number here is an upper bound on
  what AK25b's proof certifies. If the conjecture holds, the least valid `L` could be tiny.
- **Negatives, with candidates:** §4 lists four attempts at a better heavy-atom bound, all failed.
  No cheaper case-(b) route was found. No reconstruction of eq. (1.5) was found: I tried width
  bounds at every deficit in `[10⁻¹⁰⁰, 1/e − C_BFT]` (the smallest is `1.94×10¹²`) and both
  targets `1/6` and `1/2 − C_BFT`.
- The Lemma 4.4 sampling check (§3.5) is EMPIRICAL and uses seeded randomness (`seed 852`). The
  proof is the analytic one above it.
