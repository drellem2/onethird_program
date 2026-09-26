# KSBFT-L — can AK25b's heavy-atom bound `q₀ = (2ε)^{w²}` be made `poly(ε/w)`?

`mg-5371`, 2026-09-26. AK25b = Aires–Kahn, arXiv:2510.26134v1. I read §2 in full: Thms 2.1, 2.2,
Prop 2.3, Cor 2.4, Thm 2.5, the width-2 Remark, Thm 2.6 and its proof, pp. 4–5. The paper is not in
this repository. Upstream is mg-b852 (`docs/KSBFT-G-constants.md`, audited by mg-5562).
Instrument: [`code/ksbft_l_heavy_atom_5371/`](../code/ksbft_l_heavy_atom_5371/). `./run_all.sh`
runs in about 8 s on one core, in exact `Fraction` arithmetic except the `Decimal` constants. Seeded
randomness appears only in the two log-concavity probes. **`STATE.md` was not edited. Every verdict
is a recommendation to pm-onethird.**

Marks: **PROVEN** (the proof is here), **EMPIRICAL** (instrument and range named), **CONJECTURED**
(a belief), **CITED** (read in a paper, not re-derived).

---

## 0. Verdict

> **As stated, Thm 2.6 cannot be made polynomial, nor even `exp(−o(w))`. But `L*` never needed Thm
> 2.6. It needs the *maximal* atom `q(x) = max_k P(f(x)=k)`, and nothing I found stops that from
> being `poly(ε/w)`. The target is therefore a different statement, and it is OPEN. What I prove:**
>
> 1. **(PROVEN, §2) Thm 2.6's conclusion is exponentially small on an explicit family.** Take `m`
>    disjoint 2-chains plus an isolated `x`. Hypothesis (4) holds with `ε = 1/3` and `|A| = |B| = m`.
>    Yet `P(A≺x≺B) = 2^m m!²/(2m+1)! < 2^{−m}`. More generally, with chains of length `k` and
>    `ε = 1/(k+1)`, `P(A≺x≺B) ≤ (πk/2)^{−m/2}·√(2/(mk))`. So any bound `P(A≺x≺B) ≥ g(w, ε)` has
>    `g(w, 1/3) < 2^{−w}`, and `log(1/g) ≥ (w/2)·log(1/ε)·(1 − o(1))`. **The true exponent of
>    Thm 2.6 lies between `c_ε·w·log(1/ε)` and AK25b's `w²·log(1/ε)`, where the family's
>    coefficient `c_ε ∈ (1/2, 0.631]` (0.631 at `ε = 1/3`) and `c_ε → 1/2` as `ε → 0`.** Scope: the
>    family meets (4) only for `ε ≤ 1/3`, i.e. `ε_δ ≤ 1/6` in the application (audit mg-2198, 1c).
> 2. **(PROVEN, §2.3) On the same family the quantity `L*` actually consumes is polynomial:**
>    `q(x) = 1/(mk+1) = Θ(ε/w)`. The family also shows that **`q₀ ≤ 1/((w−1)(1/(2ε)−1)+1)` is a
>    ceiling** for any lower bound under AK25b's hypotheses (`δ_x ≤ 1/2−ε`, width `≤ w`), exactly at
>    `ε = 1/(2(k+1))` with `k` even, hence for every `ε ≤ 1/6`. It is `Θ(ε/w)` but not `≈ 2ε/w`: it is
>    `≥ 2ε/w` always, and at `ε = 1/6` it is `1/(2w−1)`, `1.5×` larger (audit mg-2198, 2b). So
>    `poly(ε/w)` is the best shape one could hope for, and it is not refuted. For `ε ∈ (1/6, 1/2)`
>    no member exists and no ceiling is proven.
> 3. **(PROVEN, §1) Where `w²` enters, and the two separate exponential losses in AK25b's proof.**
>    - **(L1)** It lower-bounds `q(x)` by the single joint event `{A≺x≺B} ⊊ {f(x)=|D|+1}`. On the
>      family this alone loses a factor `C(2m,m)/2^m ≈ 2^m/√(πm)`.
>    - **(L2)** It then lower-bounds that event with two nested XYZ products. The `|A|·|B|` exponent
>      is exactly the nesting: one factor `ε^{|B|}` for each `a ∈ A`.
>
>    (L1) is unavoidable for any proof that goes through `{A≺x≺B}` (item 1). (L2) is what separates
>    AK25b's `w²` from the true linear exponent of that event.
> 4. **(PROVEN by an exact instance; frequencies EMPIRICAL, §3.3) The natural chain-by-chain route
>    to `poly` has a missing ingredient.** The route is `f(x) − 1 = Σ_i N_i` over a Dilworth
>    partition of `Π(x)`, with Minkowski on `sd(N_i)`. It would need each per-chain count
>    `N_i = #{c ∈ C_i : c ≺ x}` to be log-concave, like Stanley's `f(x)`. It is not: the exact
>    instance with counts `[20,120,114,138]` proves it. Log-concavity fails for 855 of 8,207
>    (x, Dilworth-chain) pairs, and unimodality for 85, at `n ≤ 9`. The Stanley control has 0
>    failures.
> 5. **(PROVEN given mg-b852's chain, §4) What each exponent buys.** Rows marked with `*` below are
>    hypothetical: no such theorem exists.
>
> | heavy-atom shape `q₀` | status | `log₁₀ L*` (width `K₀`) | `log₁₀ L(4,1/6)` | `log₁₀ ε` of Thm 1.2 (via Thm 1.3″) |
> |---|---|---|---|---|
> | `(2ε)^{w²}` (AK25b) | PROVEN (AK25b, re-derived by mg-b852) | `1.050×10²⁹` | 119.1 | `−1.717×10²⁵` |
> | `(2ε)^{0.6309w}` = the best any Thm-2.6-type bound could give (§2) | *; floor, not a theorem | `5.09×10¹⁴` | — | `≈ −5.6×10¹²` (extrapolated) |
> | `(2ε)^{w}` | * | `8.07×10¹⁴` | 81.6 | `−8.83×10¹²` |
> | `(2ε/w)^{w}` (a `w log w` exponent) | * | `2.47×10¹⁶` | 100.4 | `−3.19×10¹⁴` |
> | `(2ε/w)³` | * | 633.7 | 100.4 | `−559.0` |
> | `2ε/w` | *; `1.5×` below the §2.3 ceiling at `ε = 1/6` | 253.5 | 75.4 | `−229.7` |
> | `1/((w−1)(1/(2ε)−1)+1)` = `1/(2w−1)` at `ε = 1/6` (the §2.3 ceiling) | *; best possible for `ε ≤ 1/6` | **251.2** | **72.0** | — (not covered: Thm 1.2's `ε_δ ≈ 0.224 > 1/6`, no ceiling proven) |
>
> **So even a perfect linear-exponent Thm 2.6 leaves `L*` doubly exponential in size
> (`10^{8×10¹⁴}`). Only a `poly` bound on the maximal atom, which cannot come from Thm 2.6, gives
> `L* = poly(K₀)`. At the ceiling `q₀ = 1/(2w−1)` (`ε = 1/6`) that is `L* ≈ 10^{251.2} ≈
> 10^{67.8}·K₀^{13}`.** No ceiling is proven at Thm 1.2's `ε_δ ≈ 0.224`; the hypothetical shape
> `2ε/w` would give Thm 1.2's `ε ≈ 10^{−230}` there, but that is not a best-possible value.

---

## 1. Where `w²` enters — PROVEN (re-derivation of AK25b Thm 2.6)

**Statement (CITED, p.4).** `P = {x} ⊔ D ⊔ U`, with `D` an ideal and `U` a filter. `A = max(D)` and
`B = min(U)`, with `|A|, |B| ≤ w`. (The printed "`max(C)`" is a typo for `max(D)`.) If
`P(a≺x≺b) ≥ ε` for all `a ∈ A`, `b ∈ B` (hypothesis (4)), then `P(A≺x≺B) ≥ ε^{w²}`. It is applied
with `2ε` in place of `ε`, via `δ_x ≤ 1/2−ε ⟹ P(a≺x≺b) ≥ 2ε`. Then
`q(x) ≥ P(f(x) = |D|+1) ≥ P(A≺x≺B)`. The printed "`|A|+1`" on p.5 is a typo for `|D|+1`.

**Proof (AK25b's, restated so the exponent can be seen).**

- **Step 1.** Fix `a`. In the poset `P + {a<x}` the measure is `P(·|a≺x)`, and Shepp's XYZ (Thm 2.1)
  gives `P(x≺B | a≺x) ≥ ∏_{b∈B} P(x≺b | a≺x) ≥ ∏_b ε/P(a≺x)`. So `P(a≺x≺B) ≥ ε^{|B|}`. **One
  factor `ε` for each `b`.**
- **Step 2.** In `P + {x<B}`, XYZ again: `P(A≺x | x≺B) ≥ ∏_{a∈A} P(a≺x≺B)/P(x≺B)`. Each factor is
  `≥ ε^{|B|}` by Step 1. So `P(A≺x≺B) ≥ ε^{|A||B|}`. **A factor `ε^{|B|}` for each `a`.**

`w²` is exactly the nesting. Step 2 re-uses Step 1's `ε^{|B|}` as its per-`a` input. No other `w`
enters the proof, and there is no iteration: two applications of XYZ, `|B|` factors inside, each of
the `|A|` outer factors, `|A|·|B|` in total. □

**The two losses, quantified on the family `F(m,2)` of §2** (`|A| = |B| = m`, hypothesis (4) at
`ε = 1/3`):

| quantity | value | source |
|---|---|---|
| `q(x) = max_k P(f(x)=k)` (what L* uses) | `1/(2m+1)` | §2, (F2) |
| `P(f(x) = |D|+1)` | `1/(2m+1)` | (F2): `f(x)` is uniform |
| `P(A≺x≺B)` (what Thm 2.6 bounds) | `2^m m!²/(2m+1)! < 2^{−m}` | (F1) |
| AK25b's lower bound for it | `3^{−m²}` | Thm 2.6 |

**(L1) PROVEN.** The inclusion `{A≺x≺B} ⊆ {f(x)=|D|+1}` loses the factor
`C(2m,m)/2^m ≥ 2^m/(2√m)`. It is strict because `f(x) = |D|+1` also occurs when `x` has some `d ∈ D`
above it and the same number of `u ∈ U` below it.

**(L2) PROVEN.** From `2^{−m}` down to `3^{−m²}`. The reason is visible in the family.
- Given `x ≺ B`, `x` is pushed to relative height `≈ 1/√m`, so each factor `P(a≺x | x≺B) ≈ 2/√m`
  (heuristic calculation, not used below).
- XYZ's product of these factors, `(2/√m)^m`, is already far below the truth `2^{−m}`, before
  Step 1's `ε^{|B|}` is substituted for each factor.

---

## 2. The family `F(m,k)` — PROVEN

**Definition.** `m` pairwise-incomparable chains `C_i = c_{i,1} < … < c_{i,k}` (`i ≤ m`), plus one
element `x` incomparable to everything. `n = mk+1` and width `m+1`. Fix `1 ≤ j < k`. Put
`a_i = c_{i,j}`, `b_i = c_{i,j+1}`, `D = {c_{i,l} : l ≤ j}` (an ideal) and `U = P − D − x` (a filter).
Then `A = {a_i}` and `B = {b_i}`, so `|A| = |B| = m`.

**Uniform-shuffle fact (U).** For a disjoint union of components, a uniform linear extension is:
independent uniform extensions of each component, interleaved by a uniform multinomial shuffle. The
number of extensions factorises as `n!/∏|P_i|! · ∏ e(P_i)`, and the shuffle is independent of the
component extensions. So the relative order restricted to any sub-collection of components is again
a uniform shuffle of them.

- **(F2)** `f(x)` is uniform on `[n]`. By (U) with components `{x}` and the rest, `x`'s slot among the
  `mk` others is uniform. **Hence `q(x) = 1/(mk+1)`**, and `P(f(x)=|D|+1) = 1/(mk+1)`.
- **(F4)** `P(c_{i,l} ≺ x) = 1 − l/(k+1)`. By (U), `x`'s slot among the `k` elements of `C_i` is
  uniform on `k+1` slots, and `c_{i,l} ≺ x` means the slot is `> l`.
- **(F3)** `P(a_i≺x≺b_i) = 1/(k+1)`, which is one slot by (U). For `i ≠ l`:
  `P(a_i≺x≺b_l) = P(a_i≺x) − P(a_i≺x, b_l≺x) ≥ P(a_i≺x) − P(b_l≺x) = (1−j/(k+1)) − (1−(j+1)/(k+1)) = 1/(k+1)`.
  **So (4) holds with `ε₄ = 1/(k+1)`.** Exact values for `k = 2, 4, 6, 8` are
  `11/30, 17/70, 1129/6006, 6841/43758`, all `≥ 1/(k+1)` (`out_family.txt`).
- **(F1)** `{A≺x≺B}` = "the elements before `x` are exactly `D`". Counting,
  `e(D) = (mj)!/(j!)^m`, `e(U) = (m(k−j))!/((k−j)!)^m` and `e(P) = (mk+1)!/(k!)^m`. So
  **`P(A≺x≺B) = C(k,j)^m / (C(mk,mj)·(mk+1))`**.
- **Bounds.**
  - `k = 2, j = 1`: `P = 2^m/(C(2m,m)(2m+1))`. With `C(2m,m) ≥ 4^m/(2√m)` this is
    `≤ 2^{−m}·2√m/(2m+1) < 2^{−m}` for every `m ≥ 1`.
  - `k` even, `j = k/2`: use `C(k,k/2) ≤ 2^k/√(πk/2)` and `C(mk,mk/2) ≥ 2^{mk}/√(2mk)`. Then
    **`P(A≺x≺B) ≤ (πk/2)^{−m/2}·√(2mk)/(mk+1) ≤ (πk/2)^{−m/2}·√(2/(mk))`**. □

**Consequence for Thm 2.6 (PROVEN).** Let `g(w, ε)` be any function with `P(A≺x≺B) ≥ g(w,ε)`
whenever (4) holds with `|A|, |B| ≤ w`. Then:

- `g(w, 1/3) < 2^{−w} = (1/3)^{0.6309·w}`, from `F(w,2)`.
- For `ε = 1/(k+1)`, `k` even: `g(w, ε) ≤ (π(1−ε)/(2ε))^{−w/2}·√(2/(wk))`.
- `log(1/g) ≥ (w/2)·log(1/ε)·(1 − o(1))` as `ε → 0`.

**No `poly(ε/w)` and no `exp(−o(w))` version of Thm 2.6 exists**, as a statement uniform in `ε`, or
at any fixed `ε ≤ 1/3` in (4) (`ε_δ ≤ 1/6` in the application). **Scope:** `F(m,k)` has no member
with (4) at `ε > 1/3`, so an `ε`-dependent claim "exponent `o(w)` for `ε_δ > 1/6`" is not refuted
here; that range contains Thm 1.2's `ε_δ = 1/2 − C_BFT ≈ 0.224` (audit mg-2198, 1c). The family's
exponent coefficient `log(1/atom)/(m log(k+1)) → (k log 2 − log C(k,k/2))/log(k+1)` is 0.6309 at
`k = 2`, 0.6094 at `k = 4`, 0.5484 at `k = 100`, and tends to `1/2` (audit's `out_audit_2198.txt`
[B]). The `w²` might still be reducible to `Θ(w)` (§3.1).

**The same family in AK25b's application (PROVEN).**
- `F(m,k)` with `k` even satisfies `δ_x = 1/2 − 1/(2(k+1))` by (F4) (the closest level is
  `l = k/2`), so it meets the Thm 2.5/1.5 hypothesis with `ε_δ = 1/(2(k+1))`.
- AK25b's `D` and `U` (`P(y≺x) ≥ 1/2+ε_δ`) are exactly the `D` and `U` above.
- `F(m,2)` has `ε_δ = 1/6`, which is `L*`'s `ε`.

So at the very `ε` used for `L*`, the atom `P(A≺x≺B)` is `< 2^{−(w−1)}`, while `q(x) = 1/(2w−1)`.

### 2.3 The ceiling — PROVEN

`F(m,k)` has width `w = m+1`, `δ_x = 1/2 − ε` with `ε = 1/(2(k+1))`, and `q(x) = 1/(mk+1)`. Hence
**no theorem "`width ≤ w` and `δ_x ≤ 1/2−ε` ⟹ `q(x) ≥ g(w,ε)`" can have
`g(w,ε) > 1/((w−1)(1/(2ε)−1)+1)`** at these `ε`. The hypotheses are monotone in `ε`, so for any
`ε ≤ 1/6` the largest admissible even `k` gives a ceiling that is still `Θ(ε/w)`. For
`ε ∈ (1/6, 1/2)` there is no member (odd `k` gives `δ_x = 1/2`) and no ceiling is proven.

The ceiling is `≥ 2ε/w`, since `(w−1)(1/(2ε)−1)+1 ≤ w/(2ε)`. The ratio to `2ε/w` is 1.8 at `w = 3`
and `→ 1.5` as `w → ∞` at `ε = 1/6`, where the ceiling is `1/(2w−1)`; it tends to 1 as `ε → 0`
(audit mg-2198, 2b). The maximal-atom question has answer between this ceiling and AK25b's
`(2ε)^{w²}`.

**Caveat: this ceiling does not bind the application.** `F(m,k)` has `δ(P) = 1/2`, since two `a_i`
are exactly balanced. `L*` needs the bound only under the global hypothesis `δ(P) ≤ 1/2−ε`, where
the truth could be better still.

---

## 3. Attempts at `poly(ε/w)` and at a better exponent — negatives

### 3.1 A linear or `w log w` exponent for Thm 2.6 — NOT PROVEN

- **Attempt 1.** Keep Step 1. In Step 2, lower-bound `P(a≺x | x≺B)` by `poly(ε/w)` instead of by
  `ε^{|B|}/P(x≺B)`. On `F(m,k)` the true value is `Θ(1/√m)`, a heuristic calculation (§1, L2).
  - If `P(a≺x | x≺B) ≥ (ε/w)^{O(1)}` held in general, Thm 2.6 would give
    `ε^{|B|}·(ε/w)^{O(|A|)} = exp(−O(w log(w/ε)))`.
  - I have **no proof**. The only tools used were XYZ (Thm 2.1), `P(a≺x≺b) ≥ P(a≺x)+P(x≺b)−1`, and
    Stanley log-concavity in `P + {x<U}`. None of them controls a conditional probability under the
    *joint* conditioning `x ≺ B`.
  - **CONJECTURED:** Thm 2.6 holds with exponent `O(w log(w/ε))`. The §4 table gives
    `log₁₀ L* ≈ 2.5×10¹⁶` for that shape.
- **Attempt 2.** Pair-correlation: `P(A≺x≺B) ≥ c·P(A≺x)·P(x≺B)`. **FALSE on `F(m,2)` (PROVEN).**
  There `P(A≺x) ≥ P(x last) = 1/(2m+1)` and `P(x≺B) ≥ P(x first) = 1/(2m+1)` by (F2), so the product
  is `≥ (2m+1)^{−2}`, polynomial, while the joint event is `< 2^{−m}` (audit mg-2198 §4). (The true
  size is `≈ √π/(2√m)` each, by the heuristic integral `∫₀¹(1−s²)^m ds ≈ √(π/4m)`; not needed.)
  The negative correlation between "`x` above all of `D`" and "`x` below all of `U`" is exponentially strong. No
  FKG/XYZ-type product bound can hold for the two-sided event.
- **Attempt 3.** The insertion identity. Removing `x` gives
  `P(A≺x≺B) = e(D)e(U)/e(P) = P_{P−x}(D before U) / E_{P−x}[s]`, where `s = #slots for x`. PROVEN,
  but it is a restatement: on `F(m,2)`, `P_{P−x}(D before U) = 2^m/C(2m,m)` is where the exponent
  lives, and the hypothesis says nothing about `P − x`.

### 3.2 `poly` for the maximal atom via Stanley + quantiles — circular

`Z := f(x) − |D| − 1` is log-concave (Stanley, Thm 2.2). `P(Z ≥ 0) ≥ P(A≺x) ≥ (1/2+ε)^{|A|}` by
XYZ, and dually. A log-concave isoperimetric bound gives `P(Z=0) ≳ min(P(Z≥0), P(Z≤0))/σ(x)`. But
`σ(x) ≍ 1/q(x)`, so this returns `q ≳ (1/2+ε)^w·q`. **No information, and not a proof of anything:**
the whole question is equivalent to `σ(x) ≤ poly(w/ε)`, by Cor 2.4 and Prop 2.3 (mg-b852 §3.2).

### 3.3 The chain route and its missing ingredient — PROVEN by an exact instance; frequencies EMPIRICAL

Partition `Π(x)` into `≤ w−1` chains `C_i` (Dilworth). Then `f(x) − 1 = |{y<x}| + Σ_i N_i`, with
`N_i = #{c ∈ C_i : c ≺ x}`. `D ∩ C_i` is an initial segment of length `k_i`.

**PROVEN:** `P(N_i ≤ k_i) ≥ 1/2+ε`, `P(N_i ≥ k_i) ≥ 1/2+ε`, and `P(N_i = k_i) ≥ 2ε`. Each chain
count has a heavy atom at its median. This is the width-2 Remark applied chain by chain.

If each `N_i` were log-concave, Prop 2.3 would give `sd(N_i) ≤ √294/(2ε)`. Minkowski would then give
`σ(x) ≤ (w−1)·√294/(2ε)`, so **`q(x) ≥ c·ε/w`, the §2.3 ceiling shape**. The chain counts are not
log-concave:

| probe | range | log-concavity failures | unimodality failures | control |
|---|---|---|---|---|
| `lc_chain_probe.py`: every chain `C ⊆ P−x` | 400 random posets, `4 ≤ n ≤ 9`, 37,081 (x,C) pairs, seed 5371 | 3,390 | 465 | Stanley `f(x)`: 0 failures (PASS); antichain count: 8,521 failures (FIRES) |
| `lc_dilworth_probe.py`: `C ⊆ Π(x)` with `w(Π(x)−C) = w(Π(x))−1` | 300 posets, `5 ≤ n ≤ 9`, 8,207 pairs, seed 53712 | 855 | 85 | same machinery as the row above |

Explicit non-unimodal Dilworth-type case: `n = 9`, predecessor masks
`[112,113,272,115,0,0,0,115,0]`, `x = 2`, `C = {1,3,5}` (mask 42). The distribution of `N_C(x)` is
`[20,120,114,138]` out of `e(P) = 392`, exact. It is not unimodal (`120 > 114 < 138`), hence not
log-concave (`114² < 120·138`), so **this instance PROVES** that per-chain counts of Dilworth type
need not be log-concave or even unimodal (re-verified independently by audit mg-2198 §4). Only the
failure frequencies in the table are EMPIRICAL. A trivial non-unimodal case for a non-saturated
chain: `v < c₁ < c₂ < u < c₃` with `x` isolated and `C = {c₁,c₂,c₃}` gives `[2,1,2,1]`.

**What this does and does not show.**
- **Does:** Minkowski-plus-per-chain-log-concavity is dead as stated.
- **Does not:** it does not show `sd(N_i)` can be large. In every example the counts are tiny.
- **Open:** a weaker per-chain statement might suffice: `sd(N_i) ≤ poly(w/ε)` given the median atom
  `2ε`. I found no counterexample and no proof.
  - An `N_i` with atom `2ε` at `k_i` and mass `≈ 1/2−ε` at distance `R` on both sides, with `R` huge,
    is not excluded by any pairwise information.
  - It must be excluded by the bounded width of the whole poset. That is the same thing AK25b's
    joint event exploits, and it is where the exponential loss comes from.

### 3.4 Global hypothesis `δ(P) ≤ 1/2−ε`: semiorders — EMPIRICAL, inconclusive

`F(m,k)` has `δ(P) = 1/2`. I tried the semiorders `S(n,k)` (`x_i < x_j` iff `j − i ≥ k`, width
`k`), which are globally unbalanced (`out_semiorder.txt`, exact):

| `k` (= width) | `n` | `δ(P)` | `P(A≺x≺B)` | `q(x) = P(f(x)=|D|+1)` |
|---|---|---|---|---|
| 2 | 12 | 0.236 | 0.446 | 0.446 |
| 3 | 14 | 0.160 | 0.242 | 0.291 |
| 4 | 16 | 0.124 | 0.134 | 0.207 |
| 5 | 18 | 0.097 | 0.077 | 0.166 |
| 6 | 20 | 0.086 | 0.049 | 0.145 |

The ratio atom/`q` falls with width here too. But `δ(P)` also falls, so `ε` is not fixed and this
says nothing about fixed-`ε` asymptotics. The `n` values are small. **I did not find a globally
unbalanced family (fixed `ε`) with `P(A≺x≺B)` exponentially small, and I did not prove one cannot
exist.**

### 3.5 Summary of negatives

| candidate | outcome |
|---|---|
| `poly(ε/w)` version of Thm 2.6 (atom `P(A≺x≺B)`) | **REFUTED** (§2) |
| `(2ε)^{o(w)}` version of Thm 2.6 | **REFUTED** for `ε_δ ≤ 1/6` (`ε ≤ 1/3` in (4)) (§2); at Thm 1.2's `ε_δ ≈ 0.224` no member of `F(m,k)` applies |
| `(2ε)^{O(w)}` or `exp(−O(w log(w/ε)))` version of Thm 2.6 | open, CONJECTURED true (§3.1) |
| product lower bound `P(A≺x≺B) ≳ P(A≺x)P(x≺B)` | **REFUTED** (§3.1) |
| `q(x) ≥ poly(ε/w)` via Stanley + quantiles | circular (§3.2) |
| `q(x) ≥ cε/w` via per-chain log-concavity + Minkowski | missing ingredient is false (§3.3, PROVEN by an exact instance) |
| `q(x) ≥ poly(ε/w)` under `δ_x ≤ 1/2−ε`, width `≤ w` | **OPEN**; ceiling `1/((w−1)(1/(2ε)−1)+1)` PROVEN for `ε ≤ 1/6` (§2.3) |
| same under global `δ(P) ≤ 1/2−ε` | **OPEN** |

---

## 4. What each exponent gives — PROVEN given mg-b852's chain

`consequences.py` copies mg-b852's `q₀ ↦ L` chain verbatim (AK25b Prop 2.3 → Thm 3.2 → Thm 3.1),
re-parametrised by `log₁₀ q₀`.

- **Control:** at `q₀ = (2ε)^{w²}` it reproduces mg-b852's `log₁₀ L(4,1/6) = 119.107` and
  `log₁₀ L* = 1.0500×10²⁹` (MATCH).
- **Negative control:** exponent `w` in place of `w²` changes `L*` (FIRES).
- **Inputs:**
  - `K₀ = 1.301×10¹⁴` (mg-c929) and `K₁₂ = 1.944×10¹²` (mg-b852), `ε = 1/6` for `L*`.
  - `ε = 1/2 − C_BFT` for Thm 1.2's case (b).
  - Thm 1.2's `ε = min(6.8×10⁻⁶, 0.0236/(L₁₂+1))` via Thm 1.3″ (mg-f218, audited HOLDS by
    mg-e60e).

The numbers are in the §0 table. Additional notes:

- **The Thm 1.3 half costs `L ≈ c·q₀^{−13}` with `c ≈ 10^{63}`.** That is why the `poly` rows still
  show `L(4,1/6) ≈ 10^{72}–10^{75}` and `L* ≈ 10^{251}–10^{253}`. The degree-13 bookkeeping is
  mg-b852's §3.4, not re-derived here. mg-b852 §3.7 lists loosenesses there that are independent of this ticket.
- **The "floor" row** uses the exact `F(m,2)` bound `g(w, 1/3) < 2^{−w}`, which is valid at `ε = 1/6`
  (so for `L*`). Its Thm 1.2 line applies the same exponent `0.6309w` at base
  `2ε = 1 − 2C_BFT ≈ 0.447`, where `F(m,k)` has no member. That line is an extrapolation.
- **The ceiling row** evaluates the exact ceiling `1/(2w−1)` at `ε = 1/6`, at `w = L*` and at
  `w = L(4,1/6)`; the values 251.2479 and 72.0291 are computed in the audit instrument
  (`code/audit_ksbft_2198/out_audit_2198.txt`, [E]), not by `consequences.py`. Its Thm 1.2 entry is
  left blank: `F(m,k)` has no member at `ε_δ ≈ 0.224`, so no best-possible value is proven there.
  The `2ε/w` row's `−229.7` is a hypothetical shape, like the other `*` rows.
- **Answer to the ticket's premise.** "Poly would give `L* = poly(1.3e14)`" is right: at the
  ceiling `1/(2w−1)`, `L* ≈ 10^{63.8}·(2K₀)^{13} ≈ 10^{67.8}·K₀^{13} = 10^{251.2}`. But **that poly
  cannot be obtained by improving Thm 2.6**; only a new heavy-atom statement about `max_k` could give
  it.

---

## 5. What I did not do

- I did **not** prove any improvement of `q₀`. The status of `q(x) ≥ poly(ε/w)` is OPEN, both under
  `δ_x ≤ 1/2−ε` and under global `δ(P) ≤ 1/2−ε`.
- I did **not** re-derive mg-b852's `q₀ ↦ L` chain or AK25b §§3–4; I reused them.
- I did **not** use mg-1911's F1/F2 windows or mg-f218's Lemma W beyond reading their role in the
  ticket. Lemma W bounds `P(f(x) − f(y) ≥ 2)` for a pair with a linear range loss, which is a
  pairwise statement. By §3.3, pairwise information is exactly what cannot see the spread of
  `f(x)`. I did not find a way to make an injection argument control the spread of `f(x)` against
  `w` chains simultaneously. This is a negative about my attempt, not a proof that Lemma W cannot
  help.
- I did **not** use "Lemma 3.1-type flip bounds": they are `range`-dependent, and range is the
  quantity being bounded here.
- I did **not** search the literature beyond AK25b §2. In particular I did not check Chan–Pak–Panova's
  work on Kahn–Saks-type log-concavity for a result on per-chain counts. A known result there could
  change §3.3.
- The two probes use small posets (`n ≤ 9`). They falsify log-concavity and unimodality by explicit
  exact instances, and say nothing about asymptotic spread. The semiorder probe is small and
  inconclusive.
- Audit hooks. Every PROVEN claim in §2 is exact, and `family.py` checks (F1)–(F4) against a
  brute-force downset DP on 9 instances (PASS), with a firing negative control. The bounds in §2
  use only the two standard central-binomial inequalities, stated inline.
