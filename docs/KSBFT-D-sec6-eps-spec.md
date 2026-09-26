# KSBFT-D — does KSBFT §6 give a *derivation* of `ε_spec`?

`mg-c929`, 2026-09-26. Paper: Aires, Chan, Pak, Panova, *Breaking the Infinite Barrier in the
1/3–2/3 Conjecture* (`/Users/daniel/files/KSBFT_v7.pdf`, 2026-09-25, **not in this repository**).
Page and equation numbers are the printed ones. The two preprints were read from arXiv:
AK25a = arXiv:2509.11549v1 (Aires–Kahn, *Balancing extensions in posets of large width*), and
AK25b = arXiv:2510.26134v1 (fetched, not needed below). Haq26 (arXiv:2608.12678) was **not** read;
its one statement is consumed through KSBFT Lemma 5.5.
Instrument: [`code/ksbft_sec6_c929/`](../code/ksbft_sec6_c929/). **`STATE.md` was not edited, and
no ticket was closed. Every verdict is a recommendation to pm-onethird.**

Marks:

- **PROVEN** — the proof is in this document.
- **PROVEN (cond. §6)** — proven here *from* KSBFT's §6 gap bound (Step 4 below). That bound rests
  on AK25a Cor. 5.1(a), AK25a Thm 2.9 and Haq26 Thm 4.1. That is exactly the set of preprints
  Thm 1.4 needs. **AK25b is not used.**
- **CITED** — a statement read in a paper and not re-derived.
- **EMPIRICAL** — the instrument and range are named. Nothing marked this way is a proof.
- **CONJECTURED** — a belief, not established.

---

## 0. Verdict

> **PARTIAL ROUTE. §6 derives an `ε_spec` bound, but not from pair bias, not at `1/6`, and not at
> any `n` anyone can compute.**
>
> 1. **The route exists (PROVEN cond. §6, Prop. B).** Every poset with `δ(P) ≤ 1/3` has
>    `E[inv_h] ≤ C·n`, where `inv_h` counts inversions against the height order and
>    `C = 2√3·e·G(ε₀)/ε₀³ ≈ 3.0×10¹⁷` is explicit. So
>    **`ε_spec ≤ 6Cn/(n²−1) = O(1/n)`**. This is stronger than L1b, which asks only for a
>    constant. It is a derivation, not a calibration. It drops AK25b, and it replaces KSBFT-C's
>    unknown `L*` with a number. **It bites only at `n ≳ 8.9×10¹⁹`** for `ε_dem ≈ 2×10⁻²`
>    (s3).
> 2. **Where `1/e` enters (PROVEN by reading, §1).** It enters in exactly one place: Lemma 5.2,
>    eq. (5.1), a one-dimensional Grünbaum bound for log-concave laws. That bound is consumed once,
>    in Lemma 6.1. Every other constant in §6 is a power of the **deficit**
>    `ε = 1/e − δ(P)`. For the 1/3–2/3 class the deficit is
>    `ε₀ = 1/e − 1/3 ≈ 0.0345 ≈ 1/29`. That tiny deficit is why every constant is astronomical.
>    AK25a Example 11.2 (CITED) makes `1/e` **sharp for this per-pair form of the input**. So
>    "1/e is an artifact" means an artifact of using a per-pair input at all. It does not mean a
>    weak inequality that could be sharpened.
> 3. **A pair-bias-only version gives nothing (PROVEN, Prop. A).** Of §6's quantities, only
>    `δ`, `h`, `Δ` and `gap` are functions of the pair marginals. Every inequality that links them
>    is a realizability fact: log-concavity, XYZ, the window bound, or Haqi–Kahn. The two-atom
>    law `(1−t)δ_e + tδ_{rev e}` has every pair incomparable and `δ = t → 0`. So the pair-bias
>    version of Thm 1.4 has constant **`0`**. The pair-bias version of the `ε_spec` bound stays
>    at `n/(n+1)`, which is mg-6bc2 Claim 3.1, unchanged.
> 4. **`1/6` is not natural in §6.** The only `1/6` near this argument is a **δ-deficit**:
>    `1/2 − 1/3`, the margin KSBFT uses when it applies Thm 1.5 (p.5). If a `1/2`-type input
>    replaced Grünbaum's `1/e`, §6 would run at deficit `1/6` instead of `1/29`. Even then,
>    `ε_spec ≤ 1/6` would arrive only at `n ≳ 5×10¹⁴` (s3, illustrative). **That is a third
>    `1/6`, unrelated to Daniel's**, which is `E[inv_e] ≤ n²/6`, i.e. `ε_spec = 1`. See mg-6bc2 §2.1.
> 5. **Windows (§3).** Thm 2.10 has an explicit form (PROVEN cond., Prop. C). A set `X` with no
>    `(1/e−ε)`-balanced pair has `Σ_{x∈X} win(x) ≤ 4√3·H(X)/ε`. The window sum is exactly an
>    expected count of incomparable pairs that sit in a window (PROVEN, Prop. D). **It does not
>    convert to `E[inv_e]` in general.** Two parallel chains have `Σ(a_x−1) = 2m²/(m+1) < n`
>    (PROVEN) but `E[inv] ≈ 0.158·n^{1.5}` (EMPIRICAL, `m ≤ 11`). Under the no-balanced-pair
>    hypothesis both quantities are `O(n)`. The inversion bound goes through the **gap**
>    (Prop. B), not through windows directly.
>
> **The precise stopping point.** Pair bias stops at `ε_spec = n/(n+1)` (mg-6bc2). §6's
> realizability inputs carry it down to `O(1/n)`, with a constant set by `ε₀⁻⁶` times the
> Haqi–Kahn/§6.4 loss. Nothing in §6 gives an `n`-free constant **below `1` at computable `n`**.
> The loss has three sources: `ε₀ = 1/e − 1/3` is small, `1/e` is sharp for the per-pair input,
> and §6.4's `gap ≤ A log² gap` step.

**Side result (PROVEN cond. §6; arithmetic on KSBFT's own final display).** KSBFT evaluates its width
bound at `ε = 10⁻¹⁰⁰` because it wants the statement `δ > 1/e − 10⁻¹⁰⁰`. For the 1/3–2/3
conjecture, `ε = ε₀` suffices. That gives **a counterexample has width `≤ 1.30×10¹⁴`**, far below
`K ≳ 10⁴⁰⁰`. The shared context and KSBFT-C carry the `10⁴⁰⁰`, which is the right number for
Thm 1.4 as stated and the wrong number for the conjecture. `L* = L(K+1, 1/6)` can use this `K`.

---

## 1. Q1 — §6 as a chain of lemmas, and the constant each one consumes

Notation (KSBFT §5.1). `f` is a uniform linear extension. `F` is uniform on the order polytope,
coupled so that `F_x < F_y ⟺ f(x) < f(y)`. `Z = (n+1)F`. `h(x) = E f(x)`,
`Δ(x,y) = |h(x)−h(y)|`, and `d(x,y) = sd(Z_x − Z_y)`.
`a_x = E[f(x) − max_{y≺x} f(y)] = win(x)/2`.
`gap(P)` is the largest consecutive difference of sorted heights, including the two ends.
Hypothesis (6.1): `δ(P) ≤ 1/e − ε`.

| step | statement | input consumed | constant in / out | pair-bias? |
|---|---|---|---|---|
| L5.1 | `Z_x − Z_y` has a log-concave density | Brunn–Minkowski on `O(P)` (AK25a Cor 5.1(a)) | — | **no** (realizability) |
| L5.2 (5.1) | `min(P[V<0],P[V>0]) ≥ 1/e − |μ|/σ` | LV07 Lem 5.4 (**Grünbaum, 1-dim**) + density `≤ 1` (LV07 5.5a) | **`1/e` enters HERE, and only here** | no |
| L5.2 (5.2) | `P[|V−μ| > tσ] ≤ e^{1−t}` | LV07 Lem 5.7 | `e` (tail constant, harmless) | no |
| L5.3 | `a_x ≥ 1`; `d(x,y) ≥ a_x/√3`; `Σ_{B} a_x ≥ |B|²/2` on antichains | trivial; total variance + Jensen (`√3` = sd of a uniform); **AK25a Thm 2.9** | `√3`, `1/2` | no |
| L5.4 | `d(x,z)² ≤ d(x,y)² + d(y,z)²` | Shepp XYZ (continuous) | `1` | no (3-point correlation) |
| L5.5 | `min_J h − max_I h ≤ |max I| + |min J| − 1` | **Haq26** (Haqi–Kahn ideal inequality) | integer | no (poset structure) |
| L6.1 | `d ≤ Δ/ε`; `1 ≤ a_x ≤ √3Δ/ε`; heights `ε/√3`-separated | (5.1) + (6.1) + L5.3 | **`1/e` is converted into `ε`** | inputs `δ, Δ` are pair-bias; `d, a_x` are not |
| L6.2 | `w ≤ 2√3·gap/ε`; `d² ≤ gap·Δ/ε²`; `|B|² ≤ 4√3·H(B)/ε` | L6.1 + L5.3 + L5.4 | `ε⁻¹`, `ε⁻²` | no |
| L6.3 | the added relations fail with probability `≤ gap⁻⁴` | (5.2) + (6.6) + separation | `R = 288/ε²` | no |
| L6.4 | `gap ≤ 2(min_J h_Q − max_I h_Q)` | Cauchy–Schwarz + L6.3 | `ε⁻¹` | no |
| §6.4 | `gap ≤ 4A(log A)²`, `A = 18432√3/ε³`; hence `w ≤ (442368/ε⁴)·log²(18432√3/ε³)` | L5.5 applied in `Q` + (6.7) | `ε⁻³ log²` | no |

**Where `1/e` enters (PROVEN by reading).** It enters in exactly one inequality, (5.1), and that
inequality is used once, in Lemma 6.1. Everything after (6.3) depends on `P` only through the
deficit `ε`. So §6 is really a theorem about the map `ε ↦ (gap bound, width bound)`. The `1/e` in
Thm 1.4 is the point where that map stops being defined.

**Is `1/e` sharp for that input? Yes, for its form (CITED + EMPIRICAL).** Any per-pair input of the
shape `δ_xy ≥ c − g(Δ/d)` with `g(0) = 0` must have `c ≤ 1/e`. AK25a Example 11.2 constructs, for
every `ε, k`, a poset with `k` elements of equal average height, so `Δ = 0`, and all pairwise
`δ_xy ≤ 1/e + ε`. Its proof "skips a few routine verifications", so it is CITED and not
re-derived. At small `n` the opposite happens, and it is only a small-`n` artefact. Over all 5230
naturally labelled posets with `n ≤ 6`, the largest `c` with `min(p,1−p) ≥ c − Δ/d` for every pair
is exactly **`c* = 1/2`** (s1, EMPIRICAL). So `1/e` cannot be seen failing at any `n` we can
enumerate. The authors' remark that "`1/e` is an artifact of the Grünbaum input" is consistent
with this. Beating `1/e` needs a **selection** step that chooses which pair to use, as in Komlós
selection and Air26. It cannot come from a better per-pair inequality. (That last sentence is my
reading of p.4 and AK25a §5, and it is CONJECTURED as a statement about Air26, which I did not read.)

**Re-checked, not just read (EMPIRICAL, s1, all posets `n ≤ 6`).** (5.1), (5.2), all three parts of
(5.3), (5.4), (5.5), (6.4) and (6.11) hold, with worst slacks printed in `out_s1_sec6_checks.txt`.
Two negative controls fire: (5.1) with `0.51` in place of `1/e`, and (5.3b) with the continuous term
dropped from `d`. **This is weak evidence for §6 specifically.** Only 86 posets at `n ≤ 6` satisfy
`δ < 1/e`, with `δ ∈ {1/3, 0.357, 0.364}`, and their gaps are tiny. So Lemmas 6.3, 6.4 and §6.4 are
**not** exercised in any interesting regime. I read those three proofs line by line and recomputed
their algebra, including the `g ≤ A log² g ⟹ g ≤ 4A log² A` step (s3). I found no error. One
inequality chain is loose but valid: (6.12)'s `/ε³` where `/ε²` would do.

---

## 2. Q2 — which steps are pair-bias statements, and what a pair-bias-only version gives

**Pair-bias quantities (PROVEN).** Write `p(x,y) = P[f(x) < f(y)]`. Then
- `δ(P;x,y) = min(p(x,y), p(y,x))` — by definition.
- `h(x) = 1 + Σ_{y≠x} p(y,x)`, because `f(x) = 1 + #{y : f(y) < f(x)}` and expectation is linear.
  So `Δ` and `gap` are pair-bias.
- `d(x,y)` is **not**. From the coupling (`F_x = U_{(f(x))}`, with order statistics independent of
  `f`), `d² = Var(f(x)−f(y)) + E[|k|(n+1−|k|)]/(n+2)` with `k = f(x) − f(y)`. The positive
  control is the 2-antichain, where `d² = 3/2` by hand (s1 PC). `Var(f(x) − f(y))` needs
  **three-element** marginals.
- `a_x` is **not**. It needs the law of `max_{y≺x} f(y)`, a joint statistic of all predecessors.

So the pair-bias quantities are `δ, h, Δ, gap`. **Every inequality in the table that relates them to
each other goes through `d` or `a_x`, or through the poset's ideal structure.** None of the steps is
a pair-bias statement.

**Prop. A (PROVEN). A pair-bias-only version of Thm 1.4 has constant `0`, and a pair-bias-only
version of Prop. B is false.** Call an argument pair-bias-only when it is valid for every probability
measure on `S_n` with the given pair marginals. That is mg-6bc2's information set `M_n`. Take
`μ_t = (1−t)δ_e + tδ_{rev e}` with `0 < t < 1/2`.
*Every* pair has `p ∈ {t, 1−t}` ⊂ `(0,1)`, so every pair is "incomparable" and the width is `n`.
Every pair has `δ = t`, so `δ(μ_t) = t`. As `t → 0`, a pair-bias statement of the form
"width `> K` ⟹ `δ ≥ c`" forces `c ≤ inf_t t = 0`. Likewise
`E_{μ_t}[inv_e] = t·C(n,2)`, which is quadratic, while every pair is `(1/e−ε)`-unbalanced for
`t < 1/e − ε`. So no pair-bias argument can give Prop. B's `O(n)`. The same witness kills the
Kahn–Saks principle "`Δ < 1` ⟹ `δ ≥ c`" in pair-bias form: adjacent pairs have
`Δ = 1 − 2t < 1` and `δ = t`. □

This is mg-6bc2 Claim 3.1's witness, now aimed at §6. **A pair-bias-only §6 gives `0` for the
width theorem and `n/(n+1)` for `ε_spec`.** The latter is no improvement on what pair bias already
proves.

**Is `1/6` natural there? No (PROVEN by reading).** §6's constants are `1/e`, `e`, `√3`, `1/2`,
`288`, `18432`, and powers of `ε`. The only `1/6` in KSBFT is p.5's `ϵ = 1/6` in Thm 1.5, which is
the δ-margin `1/2 − 1/3`. **It would be natural if the Grünbaum input were replaced by a `1/2`-type
input**, because then §6 would run at deficit `1/2 − 1/3 = 1/6` instead of `ε₀ ≈ 1/29`. s3 evaluates
§6's own constants at `ε = 1/6`. This is **illustrative only**: no such per-pair input exists (§1),
and Air26's constants are not §6's. The result is `C ≈ 1.4×10¹³`, and `ε_spec ≤ 1/6` holds from
`n ≳ 5×10¹⁴`. ⚠️ **Do not weld these three `1/6`'s together:**

| `1/6` | what it is | units |
|---|---|---|
| Daniel's (mg-6bc2 §2) | `E[inv_e] < n²/6` from pair bias | `ε_c3ca`; equals `ε_spec = 1` |
| Daniel's target, reading B (mg-6bc2 §3) | `ε_spec = 1/6` | `ε_spec`; provably unreachable by pair bias |
| KSBFT p.5 / this §2 | `1/2 − 1/3`, a margin **in `δ`** | a pair-balance deficit, not an inversion count |

---

## 3. Q3 — windows versus `E[inv_e]` and the footrule

**Prop. D (PROVEN). The window sum is an expected count of incomparable pairs.** Let
`q(x) = max_{y≺x} f(y)`, with `0` if `x` has no predecessor. Every `z` placed strictly between
positions `q(x)` and `f(x)` is incomparable to `x`. It is not `≻ x`, because it comes before `x`. It
is not `≺ x`, because it comes after the last predecessor. So
`Σ_x (a_x − 1) = E[W]`, where `W = #{(z,x) : z ∥ x, q(x) < f(z) < f(x)}`. In particular
`Σ_x (a_x − 1) ≤ m`, the number of incomparable pairs, since each pair is counted at most once, for
whichever element comes later. (s1 check CW is the identity, which holds to `10⁻¹⁵`.)

**Prop. C (PROVEN cond. on L5.1 only). Thm 2.10 with explicit constants.** AK25a's Thm 2.10 reads:
"`Σ_{x∈X} win(x) ≫ n` ⟹ some `x,y ∈ X` have `δ_xy > 1/e − o(1)`". In the contrapositive, under
`δ_xy ≤ 1/e − ε` for all `x, y ∈ X` with `|X| ≥ 2`,
`Σ_{x∈X} a_x ≤ (2√3/ε)·H(X)`, where `H(X)` is the span of heights in `X`. Hence
`Σ_{x∈X} win(x) ≤ 4√3·(n+1)/ε`.
*Proof.* List `X` by height. Apply Lemma 6.1's `a_x ≤ √3Δ(x,y)/ε` to each element and its successor
in `X`, and to the last element and its predecessor. Only the pairs inside `X` need the hypothesis.
Summing gives at most `(√3/ε)(H + last gap) ≤ 2√3H/ε`. This is the middle line of KSBFT's proof of
(6.7). □ For the frozen class this gives `E[W] ≤ (2√3/ε₀)(n+1) ≈ 100(n+1)`.

**No general conversion (PROVEN + EMPIRICAL).** Take two disjoint chains of length `m`, so `n = 2m`.
The window of `a_i` holds only `b`'s. So `Σ(a_x−1) = 2·E[#b before a_m] = 2m²/(m+1) < n`
(PROVEN; checked exactly in s2). *Proof:* the windows of `a_1,…,a_m` telescope, so their
occupancy is the number of `b`'s before `a_m`. That number is `m − T`, where `T` is the number of
trailing `b`'s. `P[T ≥ k] = C(2m−k, m)/C(2m, m)`, and the hockey-stick identity gives
`E[T] = C(2m, m+1)/C(2m, m) = m/(m+1)`. The `b` chain gives the same by symmetry. □ Yet `Σ_{x∥y} min(p,1−p)`, the smallest `E[inv]` that any
reference order can have, equals `16.35` at `m = 11`, and the ratio `I*/n^{1.5}` is
`0.1768 → 0.1585` for `m = 1…11` (s2, EMPIRICAL, exact enumeration). So
`I*/Σ(a_x−1)` climbs from `0.50` to `0.81` and shows no sign of levelling off. **No inequality
`E[inv] ≤ C·Σ win` holds for all posets.** That the growth is `Θ(n^{1.5})` for all `m` is the
standard lattice-path CLT picture: pairs `(a_i, b_j)` with `|i−j| ≲ √m` are balanced. This is
CONJECTURED here, not proven. The witness has balanced pairs (`p(a_i,b_i) = 1/2`), so it says
nothing about the no-balanced-pair class.

**Under no balanced pair: what converts, and how (PROVEN cond. §6).** Thm 2.10 does not convert to
`E[inv_e]` by itself. What converts is §6's *other* output, the **gap bound**. A bounded gap turns
the log-concave tail (5.2) into a tail that decays in the rank difference (Step 5 below). That is
Prop. B. Windows enter only upstream, inside the gap bound, through (6.7).

**Footrule (PROVEN, one line; nothing more done).** Diaconis–Graham gives `F ≤ 2I`, so Prop. B also
gives `E[footrule_h] ≤ 2Cn`. I found no route from windows to the footrule that avoids the gap.
Windows lower-bound `d`, since `d ≥ a_x/√3`. That is spread, and a spread lower bound cannot upper
bound displacement.

---

## 4. Prop. B — `E[inv] = O(n)` for every poset with `δ(P) ≤ 1/e − ε`

**Statement (PROVEN cond. §6).** Let `0 < ε < 1/e`, and let `P` be a finite poset with
`δ(P) ≤ 1/e − ε`. Let `inv_h` count the pairs of `P` that a linear extension orders against the
height order (heights are distinct by Step 1). Then

> `E[inv_h] ≤ C(ε)·n`, where `C(ε) = 2√3·e·G(ε)/ε³`, `G(ε) = max(10e(1+√3)/ε³, 4A(log A)²)`, `A = 18432√3/ε³`.

Consequently `Σ_{x∥y} min(p,1−p) ≤ C(ε)n`. The weak-majority order `e` of F21 therefore has
`E[inv_e] ≤ C(ε)n` wherever F21 applies, and `ε_spec ≤ 6C(ε)n/(n²−1)`. For `δ(P) ≤ 1/3` (frozen or
boundary), take `ε = ε₀ = 1/e − 1/3`. Then `C ≈ 2.96×10¹⁷` (s3).

*Proof.*
**Step 0.** Adjoin a bottom `0̂` and a top `1̂` to get `P̂`, with `n̂ = n+2`. Every new pair is
comparable, so `δ(P̂) = δ(P)`, and every pair of `P` keeps its probability. Heights shift by `1`.
Work in `P̂`.

**Step 1 (height separation; KSBFT (6.4), re-derived).** `a_x ≥ 1`, because `f(x)` exceeds each
predecessor's position by an integer. Condition on every coordinate except `F_x`. Then `F_x` is
uniform on `[Q_x, R_x]`. By total variance and Jensen,
`d(x,y)² ≥ (n̂+1)²E[(R_x−Q_x)²]/12 ≥ a_x²/3`, using `E[R_x − Q_x] = 2a_x/(n̂+1)`. By L5.1,
`V = Z_x − Z_y` is log-concave, so (5.1) gives `1/e − Δ/d ≤ δ(P;x,y) ≤ 1/e − ε`, i.e.
`d ≤ Δ/ε`. Therefore `1 ≤ a_x ≤ √3·d ≤ √3Δ/ε`, and **`Δ(x,y) ≥ ε/√3` for all distinct `x,y`**.

**Step 2 (KSBFT (6.6)).** List `P̂` by height as `v_1 < … < v_{n̂}`. XYZ (L5.4) applied repeatedly,
together with `d ≤ Δ/ε` on consecutive pairs, gives
`d(v_i,v_j)² ≤ Σ_k Δ_k²/ε² ≤ gap·Δ(v_i,v_j)/ε²`.

**Step 3 (KSBFT (6.11)).** For `h(y) > h(x)`, (5.2) with `t = Δ/d` and Step 2 give
`P[f(y) < f(x)] ≤ exp(1 − Δ/d) ≤ exp(1 − ε√(Δ/gap))`.

**Step 4 (KSBFT §6.3–6.4; CONSUMED).** `gap(P̂) ≤ G(ε)`. If (6.8) fails, `gap < 10e(1+√3)/ε³`
directly. Otherwise §6.4 gives `gap ≤ A(log gap)²`, which forces `gap ≤ 4A(log A)²`, because
`g/(log g)²` increases for `g > e²` and `g₀ = 4A(log A)²` satisfies `g₀ > A(log g₀)²` (checked in s3
at both `ε` values used). **This is the step that uses AK25a Thm 2.9 (through (6.7)) and Haq26
(through L5.5).** I read it and recomputed its algebra. I did not re-derive either preprint.

**Step 5 (summation; new here).** For `i < j`, Step 1 gives `Δ(v_i,v_j) ≥ (j−i)ε/√3`. So Step 3
gives `P[v_j before v_i] ≤ e·exp(−c√(j−i))` with `c² = ε³/(√3·gap)`. For fixed `i`, since
`e^{−c√t}` decreases in `t`,
`Σ_{k≥1} e^{−c√k} ≤ ∫_0^∞ e^{−c√t}dt = 2/c² = 2√3·gap/ε³`.
Sum over the `n` elements `v_i` that lie in `P`. `0̂` and `1̂` are comparable to everything, so they
contribute no inversions. That gives `E[inv_h] ≤ n·2√3·e·gap/ε³ ≤ C(ε)n`.

**Step 6.** For each incomparable pair, `min(p, 1−p) ≤ P[against height order]`. Comparable pairs
are never against the height order, because `x ≺ y ⟹ h(x) < h(y)`. Sum over pairs. □

**What Prop. B adds to KSBFT-C (PROVEN cond.).** KSBFT-C §1 F4 gets `E[inv_e] < nL*/6` from H,
which needs AK25a, Haq26 **and AK25b**, with `L*` existential. Prop. B needs only Thm 1.4's two
preprints, and its constant is a number: `ε_spec ≤ ε_dem` for `n ≥ 8.9×10¹⁹` (s3). Both results
make L1b automatic for large `n`. Neither buys anything at computable `n`. Prop. B also has content
on a **nonempty** class. The boundary class `δ = 1/3` is inhabited: the 3-element poset `{a<b} ∪ {c}`
and ordinal sums of copies of it. 39 of the 5230 posets with `n ≤ 6` are in it, and s1 checks
Steps 1, 3 and 5 on all of them (CINV1, CINV2). On those examples the bound is loose by five orders
of magnitude.

---

## 5. Q4 — verdict, and where it stops

**PARTIAL.** §6 **does** give a derivation route for an `ε_spec` bound, and a strong one in form:
`ε_spec = O(1/n)` for the whole class `δ ≤ 1/3`, conditional on AK25a and Haq26 (Prop. B). That
answers the ticket's complaint that `ε_spec` was only a calibration: a derivation now exists. **It
does not deliver what Daniel asked for.**

| what was hoped | what §6 gives | stopping point |
|---|---|---|
| from pair bias alone | **nothing** (Prop. A) | the two-atom law; the pair-bias ceiling `n/(n+1)` (mg-6bc2 Cl. 3.1) is untouched |
| a constant near `1/6` | `ε_spec ≤ 6Cn/(n²−1)`, `C ≈ 3×10¹⁷` | no `n`-free constant below `1` at any `n < 1.8×10¹⁸` |
| a mechanism that explains `1/6` | the δ-deficit `ε₀ = 1/e − 1/3 ≈ 1/29` drives everything; `1/6` would be the deficit under a `1/2` input | `1/e` is sharp for per-pair inputs (AK25a Ex 11.2); §6.4's `ε⁻³ log²` loss |

**For pm-onethird.** (CONJECTURED, a routing suggestion.) If anyone pursues this, the lever is the
deficit rather than the pair bias. A per-pair input cannot beat `1/e`, so the only way to make `ε`
large is a selection argument (Air26), which I did not read. That is the one document that could
change this verdict. Reading Air26 for its analogue of Lemma 6.1 is the next step, if there is
one.

---

## 6. Instrument

[`code/ksbft_sec6_c929/`](../code/ksbft_sec6_c929/). Run it with `sh run_all.sh` (about 50 s). It
uses no randomness and floats with tolerance `1e−9`. No decision in this document rests on a float
near a threshold.

- `s1_sec6_checks.py 6` → `out_s1_sec6_checks.txt`. Every naturally labelled poset with `n ≤ 6`,
  5230 of them with isomorphic duplicates, harmlessly. It checks (5.1)–(5.5), (6.4), (6.11), Prop. D
  and Prop. B's Steps 3–5. It includes a positive control (the `d` formula at the 2-antichain) and
  two negative controls that must fire (N1, N2). It also measures `c* = 1/2` (§1).
- `s2_parallel_chains.py 11` → `out_s2_parallel_chains.txt`. Exact over all `C(2m,m)` extensions,
  `m ≤ 11`.
- `s3_constants.py` → `out_s3_constants.txt`. Evaluates `G`, `C`, the thresholds, and the
  `g ≤ A log² g` step, at `ε₀` and at the illustrative `1/6`.

---

## 7. What I did not do, and negatives

**Not done.**
- I did **not** read Haq26, Air26 or AK25b beyond fetching AK25b. Haq26 enters only through
  KSBFT Lemma 5.5, and Air26 is the one source that could move §5's verdict.
- I did **not** re-derive AK25a Thm 2.9 (it rests on AK25a Thm 5.6, `e(P) ≥ Σ_{x∈A} e(P−x)`) or
  Example 11.2 (its proof skips "routine verifications"). The LV07 lemmas behind (5.1) and (5.2)
  are also taken as cited.
- KSBFT §6.3–6.4 are **read and algebra-checked, not independently re-proved**. The authors report
  heavy AI use on technical lemmas. Step 4 of Prop. B inherits whatever is wrong there.
- I did **not** try to tighten §6's constants: `R = 288/ε²`, the `gap⁻⁴` target, and the
  `4A log²A` step. Doing so would move `C` by powers of ten, not change the verdict.
- I did **not** prove the `Θ(n^{1.5})` growth for parallel chains (CONJECTURED, standard).
- I did **not** decide whether `E[inv] ≤ C'·E[W]` holds on the no-balanced-pair class with a better
  `C'`. It is open, and it would give a much smaller constant than Prop. B, about `100/ε₀`.
- I did **not** check that the architecture's distinguished order is F21's weak-majority order at
  every use site. Prop. B bounds the height-order count and `Σ min(p,1−p)`. It transfers only
  where `E[inv_e]` equals, or is at most, that sum.

**Negatives, with the candidates tried.**
1. A pair-bias-only version of Thm 1.4, Lemma 6.1, the Kahn–Saks `Δ<1` principle, or Prop. B:
   **all killed by the two-atom law** (Prop. A).
2. Replacing `1/e` in (5.1) by a larger per-pair constant: **impossible in general** (AK25a Ex 11.2,
   CITED). It holds with `1/2` at `n ≤ 6` (EMPIRICAL), and that is a small-`n` artefact.
3. Converting windows to inversions directly (`E[inv] ≤ C·Σ win`): **false in general**
   (parallel chains).
4. Windows ⟹ footrule without the gap: **no route found.** Windows lower-bound the spread `d` and
   cannot upper-bound displacement.
5. A `1/6` anywhere in §6's mechanism: **none**. The nearest is the δ-margin `1/2 − 1/3`, which is
   the wrong units.
