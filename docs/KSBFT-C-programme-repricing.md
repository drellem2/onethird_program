# KSBFT-C — repricing the programme under *"a counterexample has bounded range"*

`mg-1911`, 2026-09-26. Daniel: *"investigating how to use it to make progress"*.
Paper: Aires, Chan, Pak, Panova, *Breaking the Infinite Barrier in the 1/3–2/3 Conjecture*
(`/Users/daniel/files/KSBFT_v7.pdf`, dated 2026-09-25, **not in this repository**). Page numbers are
the printed ones. **Nothing in `STATE.md` was edited and no ticket was closed. Every verdict below is
a recommendation to pm-onethird.**

Every claim carries a mark:

- **PROVEN** — the proof is in this document, and it is elementary enough to check line by line.
  **PROVEN (cond.)** means proven *from* the hypothesis **H** below, which is itself conditional on
  preprints.
- **EMPIRICAL** — the instrument and range are named. That tells you the arithmetic is right. It
  does not prove anything.
- **CONJECTURED** — a belief or a proposed route, not established here.

---

## 0. Verdict

> **Under H, the wall is not where the difficulty lives any more.** For large `n`, every
> Axis-1 object this repository has priced as open is either automatic or has lost its
> meaning. That covers L1b/`(LIB-const)`, the single lemma's two faces `(B)` and `(LIB)`,
> `(EQ)`, and `(R)`. The reason is one elementary fact. Bounded range forces every element's
> position into a window of `π(x)+1` slots in **every** linear extension (§1, F1).
>
> **That buys nothing at any `n` anyone can compute.** The thresholds are `n ≥ L*/ε_dem + 1 ≈
> 50·L* + 1`, and `L*` has no published value. The only explicit constant in the chain is
> `K ≳ 10^400`. **Bounded range is not small `n`.** The Fibonacci family `Z_n` (`π = 2`,
> primitive, width 2) exists at every order. So H delivers **zero whole orders** in mg-5987's
> currency, and H plus "a finite check at small range" does **not** settle width 3 (§2.9).
>
> **What H changes structurally, and why it matters for where to push:**
>
> 1. **(PROVEN cond.)** For `n ≥ N₁ := ⌈L*/ε_dem⌉ + 1`, L1b's *conclusion* holds for every
>    counterexample. So L1b is equivalent to a statement about posets on fewer than `N₁` elements.
> 2. **(PROVEN cond.)** For `n ≥ 3L*/ε + 1` that conclusion holds for **every** poset of range
>    `≤ L*`, frozen or not, measured against any reference linear extension. **So L1b carries no
>    information that separates counterexamples from non-counterexamples in the regime where
>    counterexamples live.** Past `N₁`, the programme's whole remaining content is the downstream
>    links L3 (row 10), L4 (row 11) and the Step-6 hole, restricted to range `≤ L*`.
> 3. **(PROVEN cond.)** The programme's standing premise is *"the open region is the DENSE one"*
>    (row 8, mg-0e8c), with the corollary *"dense means wide"* (mg-9d9e §5.3). **H inverts it.**
>    A counterexample has `d ≤ L*/(n−1) → 0` and width `≤ K` (Thm 1.4 alone). So the programme's
>    open region contains no counterexample once `n > 50L* + 1`. KSBFT's residual region is
>    exactly the region where the programme's wall is already down. The two attacks are
>    complementary, and the overlap where both are open is `{π ≤ L*, n ≤ 50L*}`.
> 4. **(CONJECTURED — the one route this document proposes.)** Bounded range makes the uniform
>    measure on `L(P)` a **finite-state transfer-matrix object** (§1 F2, which is PROVEN: bandwidth
>    `≤ 2L*−1` in every linear extension). If correlations decay along the window (§3.2), then
>    "no counterexample of range `≤ D`" becomes a finite computation for each fixed `D`. That
>    would turn H into a proof at whatever `L*` turns out to be.

| # | object | verdict under H | mark |
|---|---|---|---|
| 1 | `(LIB-const)` / L1b, row 8 (mg-6bc2) | **AUTOMATIC** for `n ≥ L*/ε + 1`. Daniel's `3L*/ε` is also right; it drops the frozen factor `1/3`. | PROVEN (cond.) |
| 1′ | same, at computable `n` | **buys nothing.** `N₁` is not computable-size. | PROVEN (cond.) that it is `≥ 50L*`; size of `L*` unknown |
| 2 | "open content is the ~50× between `ε_sup` and `ε_dem`"; "open region is DENSE" | **REPRICED, inverted.** Closed for counterexamples at `n ≥ 50L*+1`; open only at `n ≤ 50L*`. | PROVEN (cond.) |
| 3 | pair-bias ceiling, mg-6bc2 Claim 3.1 (`(1−3η)n/(n+1)`, attained) | **UNCHANGED as stated.** Its witness (the two-atom law) has density 1. **H is exactly a realizability fact**, and it gives `ε_spec ≤ L*·n/(n²−1)`. | PROVEN (cond.) |
| 4 | single lemma, face `(B)` | **AUTOMATIC** with constant `L*`. | PROVEN (cond.) |
| 5 | single lemma, face `(LIB)` `E[inv_e] = O(n/γ)` | **AUTOMATIC** with constant `L*/6`, independent of `γ`. | PROVEN (cond.) |
| 6 | `(LIB-weak) ⟹ (LIB-const)`, "no `N₀` works" (mg-c4f5 §5.3) | **UNCHANGED as logic, MOOT as a direction.** H supplies `O(n)`, not `o(n²)`, and `N₀ = ⌈L*/ε⌉+1`. | PROVEN (cond.) |
| 7 | `(EQ)` `max_x \|E pos − rank_e\| = O(1)` | **AUTOMATIC in existence form** (constant `L*`). **UNCHANGED at the constant that delivers orders** (`C < 0.30`, mg-5987). | PROVEN (cond.) |
| 8 | `(B-cov)` | **MOOT as a route to `(B)`'s existence form. UNCHANGED at a useful constant** (`C < 0.32`, mg-5987). | PROVEN (cond.) for the moot half |
| 9 | `(R)` density ceiling, `(1_D)` (mg-0b96, mg-9b6b) | **AUTOMATIC for `n ≥ L*/D + 1`.** "No `D` both provable and worth an unreached order" **still holds at computable `n`**. | PROVEN (cond.) |
| 10 | code-length line: mg-872c's one object; mg-cace (PARKED) | **REPRICED.** `log₂ e(P) ≤ n·log₂ min(K, L*+1)` is `Θ(n)` from H. The existence question is answered. Only a *useful constant* is open. **Recommend: leave mg-cace parked, and re-scope it on unpark** (§2.8). | PROVEN (cond.) |
| 11 | "dense means wide", so `n log₂ w` is vacuous where needed (mg-9d9e §5.3) | **REFUTED under H.** Counterexamples have `w ≤ K`. | PROVEN (cond.) |
| 12 | width-3 (milestone-1; the sibling repo) | **REPRICED, not settled.** Modulo **AK25b alone**, a width-≤3 counterexample has `7 ≤ π ≤ L₃ := L(4, 1/6)`. That is **not finite**: `n` is unbounded. What remains is stated in §2.9. | PROVEN (cond. on AK25b) |
| 13 | Theorem E (row 6), L3 (row 10), Step-6 hole (mg-3af9), literature `n`-bounds | **UNCHANGED.** | — |
| 13′ | the absent Step `(T)` (mg-7ae5) | **UNCHANGED as far as I can tell.** H's density scaling `Θ(L*/n)` is the one mg-7ae5 §4 already priced as *not* filling the hole (§4). | CONJECTURED |
| 13″ | per-slot LP value `Θ(n²)`, *"Daniel's route is dead"* (mg-00a1) | **REPRICED.** On range `≤ L*` the value is `≤ nL*/6`: re-based at a useless constant (§4). | PROVEN (cond.) |
| 13‴ | bounded-width machinery *"off-route / width-3 baggage"* (`STATE.md:3`, attempt-index DROP of mg-c47a) | **REPRICED.** Under H_w every counterexample has width `≤ K`, so it is on-route. Whether to re-open is pm-onethird's call. | PROVEN (cond.) |
| 14 | L4 (row 11) | **REPRICED in scope only.** It now needs to hold only on `π ≤ L*`. Still **OPEN**. | PROVEN (cond.) that the scope suffices |
| 15 | obstruction 4 ("false for abstract frozen distributions") | **REPRICED.** H is the realizability input the executive summary says is needed, and it breaks the two-atom witness. | PROVEN (cond.) |

---

## 1. The hypothesis, what it rests on, and seven elementary consequences

### 1.1 H, and exactly what it depends on

Notation, all from the paper (p.3):

- `π(x)` is the number of elements incomparable to `x`, and `π(P) = max_x π(x)` is the **range**.
- `w(P)` is the width.
- `d(x) := #{v : v ≺ x}` is the down-degree.
- `m` is the number of incomparable pairs, and `d = m/C(n,2)` is the incomparability density.
  The repo's `d`, not the paper's `d_i`.

**The three theorem statements this document uses** were checked against the PDF by me (p.3–5):

| | statement | conditional on |
|---|---|---|
| Thm 1.4 | `w(P) > K ⟹ δ(P) > 1/e − 10⁻¹⁰⁰` | AK25a (arXiv:2509.11549, Lemmas 5.1 and 5.3) and Haq26 (arXiv:2608.12678, Lemma 5.5) |
| Thm 1.5 | `∀K, ε ∃L(K,ε)`: `w(P) < K` and `π(P) > L ⟹ δ(P) > 1/2 − ε` | AK25b (arXiv:2510.26134v1), imported whole. `L` is existential in the statement. |
| Lemma 3.1 | `π(P) ≤ D` and `E` an `S`-dependent event with `P[E] > 0` ⟹ `P[E] ≥ (D+1)^{−|S|(D+1)}` | **nothing.** Elementary, and re-read line by line here (p.9–10). EMPIRICAL check at `m = 2` in App. A. |

**H_w (PROVEN cond. on AK25a and Haq26).** A counterexample `P`, meaning a non-chain with
`δ(P) < 1/3`, has `w(P) ≤ K`.
*Proof.* `1/3 < 1/e − 10⁻¹⁰⁰`, so `w(P) > K` would give `δ(P) > 1/3`. □

**H (PROVEN cond. on AK25a, Haq26 and AK25b).** A counterexample has `π(P) ≤ L* := L(K+1, 1/6)`,
and therefore `w(P) ≤ L* + 1`.
*Proof.* By H_w, `w(P) < K+1`. Apply Thm 1.5 at `(K+1, 1/6)`: `π(P) > L*` would give
`δ(P) > 1/3`. For the width bound, take an antichain of size `w`. Each of its elements is
incomparable to the other `w−1`, so `w − 1 ≤ π(P)`. □

⚠️ **Which consequences need which half.** The width bound `w ≤ K` needs **only Thm 1.4**. Every
density, window or displacement consequence needs **Thm 1.5 as well**. Bounded width alone does
not bound density: two incomparable chains of length `n/2` have width 2 and `d → 1/2`. The table
in §0 uses `min(K, L*+1)` wherever the width alone suffices.

**e is well defined for a counterexample (PROVEN, and not new).** Orient each incomparable pair
in its `> 2/3` direction, and keep `≺` on comparable pairs. This gives a tournament. A 3-cycle
would have three cyclic probabilities summing to `> 2`. But in any linear order at most two of the
three cyclic events hold, so that sum is `≤ 2`. A 3-cycle-free tournament is transitive. So `e` is
a linear order containing `≺`, i.e. a linear extension. This is the standard argument; FACTS.md F22
notes it needs the *strict* `< 1/3`, which a counterexample has.

### 1.2 Consequences F1–F7

Throughout, `P` is any finite poset, `D := π(P)`, `g` is any linear extension, and `e` is any
reference linear extension. Frozenness is used only in F4.

**F1 — the window (PROVEN).** For every `g`: `d(x) + 1 ≤ g(x) ≤ d(x) + 1 + π(x)`. So
`|g(x) − e(x)| ≤ π(x)`: **displacement from any reference linear extension is at most `π(x)`,
pointwise, for every `σ`.** The window is attained whenever `π(x) > 0`.
*Proof.* All `d(x)` predecessors of `x` precede it. All `u(x) = n − 1 − d(x) − π(x)` successors
follow it. So `g(x) ≤ n − u(x) = d(x) + 1 + π(x)`. Now `e` is also a linear extension, so `e(x)`
lies in the same window of `π(x)+1` slots. For attainment, list `x`'s down-set, then all of `x`'s
incomparables together with their down-sets, then `x`. This is a valid prefix: a predecessor of an
element incomparable to `x` cannot lie above `x`, since `x ≺ v ≺ z` would make `z` comparable to
`x`. □ *(Also in KSBFT's own proof of Lemma 3.1, p.10.)*

**F2 — bandwidth (PROVEN).** If `x ∥ y`, then `d(x) − d(y) ≤ π(y) − 1`. Hence, for every `g`,
`|g(x) − g(y)| ≤ π(x) + π(y) − 1 ≤ 2D − 1`. **Incomparable elements are within distance `2D−1`
in every linear extension.**
*Proof.* Take `v ≺ x`. Then `v ≠ y`, and `v ≻ y` is impossible (it would give `y ≺ x`). So each
such `v` is either `≺ y` or `∥ y`. The elements `∥ y` that are `≺ x` exclude `x` itself, and `x`
is one of `y`'s `π(y)` incomparables. So there are at most `π(y) − 1` of them, and
`d(x) ≤ d(y) + π(y) − 1`. By F1, `g(x) − g(y) ≤ d(x) + 1 + π(x) − d(y) − 1 ≤ π(x) + π(y) − 1`. □
*My first draft had `≤ π(y)`. The negative control N2 in Appendix A showed the `−1` was always
available, and the proof above supplies it.*

**F3 — sparsity (PROVEN).** `m = ½·Σ_x π(x) ≤ nD/2`, so `d ≤ D/(n−1)`.

**F4 — inversions (PROVEN).** For any `P` and reference `e`, `inv_e(σ) ≤ m ≤ nD/2` for every `σ`.
If `P` is frozen and `e` is its majority order, then `E[inv_e] = Σ_{x∥y} q_{xy} < m/3 ≤ nD/6`,
since each flip probability `q_{xy} < 1/3`.
In `ε_spec` units (mg-6bc2 §3.1's identity `ε_spec = 3·d·q̄·n/(n+1)`), this gives
`ε_spec < d·n/(n+1) ≤ D·n/(n²−1)`.

**F5 — the displacement face (PROVEN).** `Σ_x disp(x)² ≤ D·Σ_x |disp(x)|` pointwise, by F1. So
`E[Σ disp²] ≤ D·E[Σ|disp|]`.

**F6 — entropy (PROVEN).** `log₂ e(P) ≤ Σ_x log₂(π(x)+1) ≤ n·log₂(D+1)`. By F1, `x` has at most
`π(x)+1` possible positions and the position vector determines `g`. The same inequality is (3.3) of
the paper with `U = ∅`. Independently, mg-9d9e §5.3 gives `log₂ e(P) ≤ n·log₂ w(P)` via `MINIMALS`.

**F7 — no flip is negligible (PROVEN; KSBFT Lemma 3.1 at `|S| = 2`, re-derived).** If `x ∥ y`,
then `P[g(y) < g(x)] ≥ q₂ := (D+1)^{−2(D+1)}`. I re-read the proof on p.9–10 and it is correct as
written. It does **not** depend on Lemma 4.2 or on the constant `441`, which the ticket flags as
low-assurance. Nothing in this document consumes Lemma 4.2 or eq. (1.5).

**Under H, set `D = L*` in F1–F7.** That substitution is the only thing the rest of this document
does.

---

## 2. Item by item

### 2.1 mg-6bc2 / `(LIB-const)` / L1b (row 8) — **AUTOMATIC for `n ≥ L*/ε + 1`; buys nothing at computable `n`**

**Daniel's claim is right, and the threshold can be improved by a factor of 3.** Two readings:

- *Without* frozenness: `E[inv_e] ≤ nL*/2 ≤ (ε/6)(n²−1)` holds once `n(n − 3L*/ε) ≥ 1`. That is
  true for `n ≥ 3L*/ε + 1`. **(PROVEN cond., F3 + F4.)**
- *With* frozenness, which every counterexample has: `E[inv_e] < nL*/6 ≤ (ε/6)(n²−1)` holds once
  `n(n − L*/ε) ≥ 1`. That is true for `n ≥ L*/ε + 1`. **(PROVEN cond., F4.)** At
  `ε = ε_dem ≈ 1/50` this is **`n ≥ 50L* + 1`**. mg-6bc2 §6 says `1/50` over-estimates the budget,
  because `C₃ ≥ 1` is a loss factor. So the honest threshold is `n ≥ 50·C₃·L* + 1`.

**What it closes.** L1b's hypothesis class is the frozen non-chains, which are exactly the
counterexamples. Chains satisfy the conclusion trivially. So under H:

> **L1b ⟺ "every frozen poset on fewer than `N₁ = ⌈L*/ε_dem⌉ + 1` elements satisfies
> `E[inv_e] ≤ (ε_dem/6)(n²−1)`"** — a statement about finitely many posets. **(PROVEN cond.)**

**What it does not buy (answering "does it buy anything at computable `n`?"): nothing.**

1. `L*` has no published value. Thm 1.5's `L` is existential in the statement, and the paper
   (p.5, §1.5) says only that it "can be made explicit".
2. The one explicit constant upstream is `K ≳ 10^400`. Nothing known to me makes `L*` smaller than
   astronomical. I do **not** claim `L* ≥ K`; I found no argument either way.
3. The literature floor on a minimal counterexample (`n ≥ 15`, Gup26) is nowhere near `N₁`.

⚠️ **The structural reading matters more than the threshold (PROVEN cond.).** The first reading
above used no frozenness. So for `n ≥ 3L*/ε + 1`, **every** poset of range `≤ L*` satisfies L1b's
conclusion against **every** reference linear extension. That includes non-counterexamples such as
`Z_n`. In the regime where H says counterexamples live, L1b's conclusion is a consequence of range
alone. It cannot be the step that finds the contradiction. **Past `N₁`, the programme's contradiction
has to come entirely from rows 10 and 11 and the Step-6 hole**, all restricted to `π ≤ L*`. That is
the sense in which "the wall is not where the difficulty lives any more". It is a re-pricing of the
*chain*, not a closure of it.

### 2.2 "The open content is the ~50×"; "the open region is the DENSE one" (row 8, mg-0e8c) — **REPRICED: inverted**

Row 8 says `ε_sup = d·n/(n+1)` is linear in density. So the wall is proven for `d ≲ 2×10⁻²` and
open in the dense regime. **Under H, a counterexample has `d ≤ L*/(n−1)` (F3)**, so the dense
regime contains **no counterexample** once `n > 50L* + 1`. **(PROVEN cond.)**

The ~50× gap therefore survives only at `n ≤ 50L*`. There it is a finite question, and not a
computable one.

### 2.3 mg-6bc2 Claim 3.1 (pair-bias ceiling is an equality) — **UNCHANGED as a theorem; H is the missing realizability fact**

Claim 3.1 is about the marginal class `M_n(η)`, and it stands. Its extremal witness is the two-atom
law, which has **density 1**. H restricts the counterexample class to `M_n(η) ∩ {d ≤ L*/(n−1)}`, and
on that class F4 gives `ε_spec ≤ L*·n/(n²−1) → 0`. The executive summary says: *"closing the gap
needs … a realizability fact"*. **Bounded range is such a fact** (PROVEN cond.). It is supplied by
AK25b, not by anything pair-bias can see. It is priced at `L*`, so it arrives at `n ≈ 50L*`.

### 2.4 The single lemma: `(B)` and `(LIB)` — **AUTOMATIC**

- `(B)`: `E[Σ disp²] ≤ L*·E[Σ|disp|]` (F5). The `O(·)` constant is `L*`. **PROVEN (cond.)**
- `(LIB)`: `E[inv_e] < nL*/6` (F4). The constant is `L*/6` and does not depend on `γ`.
  **PROVEN (cond.)**

These hold at **every** `n`, not only large `n`, but with constant `L*`. STATE.md's single lemma is
stated in `O(·)`, so the lemma *as written* is discharged under H. What the architecture consumes is
the constant (`ε_dem`), and that is §2.1.

### 2.5 `(LIB-weak) ⟹ (LIB-const)` and "no `N₀` works for the class" (mg-c4f5 §5.3) — **UNCHANGED as logic; MOOT as a direction**

§5.3 says an `o(n²)` hypothesis yields no threshold. That remains true. H does not pass through
`o(n²)`: it supplies `O(n)` with an explicit constant, and the resulting threshold is
`N₀ = ⌈L*/ε⌉ + 1` (§2.1). Nothing in §5.3 is contradicted. What §5.3 closed ("go and find `N₀` from
LIB-weak") stays closed, and it no longer matters.

### 2.6 `(EQ)` and `(B-cov)` — **AUTOMATIC / MOOT in existence form; UNCHANGED at the constant that matters**

- `(EQ)`: `max_x |E[pos_σ x] − rank_e x| ≤ max_x π(x) ≤ L*` by F1 averaged. **PROVEN (cond.)**
- mg-5987 priced `(EQ)_C`: it delivers **every order `3…8` only for `C < 37/123 ≈ 0.30`** and
  **nothing for `C ≥ 2/5`**. `C = L*` is on the useless side by an astronomical margin. So `(EQ)` at
  a useful constant is **UNCHANGED**.
- `(B-cov)` was a route *to* `(B)`. `(B)` is now automatic with constant `L*` (§2.4), so
  `(B-cov)`-as-route-to-existence is **MOOT**. `(B-cov)_C` at `C < 8/25` is **UNCHANGED**; I found
  no bounded-range bound on the covariance sum below `L*`-scale.

### 2.7 `(R)` density ceiling and `(1_D)` (mg-0b96, mg-9b6b) — **AUTOMATIC for `n ≥ L*/D + 1`; the "no lever" verdict survives at computable `n`**

`(1_D)` reads "every frozen poset has `d ≤ D`". Under H this holds for all `n ≥ L*/D + 1`, by F3.
**(PROVEN cond.)**

mg-0b96's theorem `(1_D) ⟺ (2_D)` (the conjecture on `{d > D}`) makes this unsurprising. **KSBFT
is, conditionally, a proof of the conjecture on `{d > D, n > L*/D + 1}`.** mg-9b6b's verdict was
that no `D` is both provable and worth an unreached order. That verdict **still holds at every
computable `n`**. H makes `D = 2×10⁻²` provable only from `n ≈ 50L*` on. mg-9b6b's table shows `(1_D)`
at that `D` "forbids a frozen primitive up to `n = 98`". So H would have to meet the primitive floor
`d ≥ 2/n` at `n ≤ 98`, and it cannot: `50L* ≫ 98` unless `L* ≤ 1`, and BW92 already covers `π ≤ 5`.

**mg-5987's step-2 observation, applied to KSBFT itself (PROVEN).** "Frozen ⟹ `π ≤ L*`" is the
conjecture restricted to `{π > L*}`. It covers order `n` exactly when every primitive at order `n`
has `π > L*`. **`Z_n` is primitive with `π(Z_n) = 2` at every `n`**. It is the Fibonacci poset `F`,
which mg-5987 already uses. So `floor_π(n) ≤ 2` for all `n`, and **KSBFT delivers zero whole orders**
in that currency. This is the precise version of "bounded range is not small `n`".

### 2.8 The code-length line: mg-872c's one object and mg-cace — **REPRICED; recommend: leave parked, re-scope on unpark**

mg-872c asked: *"what does hypothesis (1) actually force `e(P)` to be? … If a `Θ(n)` bound is
provable under hypothesis (1), it is a far stronger statement and it is what the evidence points at."*

**Under H, yes (PROVEN cond.):** `log₂ e(P) ≤ n·log₂ min(K, L*+1)` (F6 plus mg-9d9e's `MINIMALS`
bound). `K` alone needs only Thm 1.4. `log₂ e(P)` is a lower bound on the expected length of *every*
prefix code for `L(P)` (Gibbs), and `MINIMALS` attains the upper bound. So the upper side of "the
code-side object" exists: **a code whose length is bounded from hypothesis (1) at `Θ(n)`**, with
constant `log₂ K`. What H gives is a **width/range** bound. It is **not** mg-872c's intended
mechanism ("δ ≤ 1/3 forces the merge words to be predictable"). It arrives at the same place by a
different road.

**Shape-A targets (`c·n log₂ n`) become automatic for `n ≥ min(K, L*+1)^{1/c}` (PROVEN cond.).** For
`compression2`'s `c ≈ 0.9399`, that is `n ≥ K^{1.064}`, astronomically past `16,777,063`. So mg-9d9e
§4.2 still stands at every computable `n`: *"no `n` at which the theorem is both non-vacuous and
hypothesis-free"*. What changes is that at astronomical `n` the "hypothesis-need" half is now supplied
by H.

**mg-9d9e §5.3's "vacuous exactly where the programme needs it — dense means wide" is REFUTED
under H (PROVEN cond.).** mg-9d9e itself flagged that sentence as not measured. Counterexamples have
`w ≤ K`, so `n log₂ w` is **not** vacuous on them.

**On mg-cace (recommendation, not a decision):**

- **Its arm, `k0/k1/k2` scoring P1–P10 on the boundary population at `n ≤ 12`, is UNCHANGED by H.**
  It is a finite-population measurement, and H says nothing at those `n` (§2.1).
- **Its motivation is REPRICED.** P10 was sold as the thing that makes "the object mg-9d9e left
  standing … not an object anyone needs". Under H that object's *existence* question is already
  answered, at constant `log₂ K`. Only a *useful constant* remains open.
- **So: do not close it. KSBFT is conditional on three preprints, and closing work on a conditional
  would bank the condition.** Leave it PARKED (Daniel's pause), and on unpark re-scope its framing
  to: *"P10 as a measurement; the existence of a `Θ(n)` code-length bound under (1) is answered
  conditionally by KSBFT's range bound (docs/KSBFT-C-programme-repricing.md §2.8); the open
  content is only the constant."*
- **If pm-onethird adopts H as a working hypothesis, the code-side line's theoretical object is
  MOOT and mg-cace could be closed.** That is pm-onethird's call.

### 2.9 Width 3 (milestone-1; the sibling repository) — **REPRICED, not settled**

**The ticket's question:** does Thm 1.5 plus a finite check at small range settle width 3?
**No, and the reason is structural (PROVEN).** "Small range" is an infinite family. `Z_n` has
`π = 2` and width 2 at every `n`, and range-`≤ D` posets of width 3 exist at every `n`. A check at
small range is a check over infinitely many posets.

**What KSBFT does give for width 3 (PROVEN cond. on AK25b ALONE).** Thm 1.4 is not needed for width
3, and neither are AK25a and Haq26. Take `K = 4, ε = 1/6` in Thm 1.5: a width-`≤ 3` counterexample
has `π ≤ L₃ := L(4, 1/6)`. With BW92 (`π ≤ 5`) and Peczarski 2008 (`π ≤ 6`), both refereed and cited
on p.3:

> **Width-3 1/3–2/3 ⟸ AK25b + "no width-`≤ 3` poset with `7 ≤ π(P) ≤ L₃` is a counterexample",
> at every `n`.**

**What is left for width 3, in order of cost:**

1. **Extract `L(4, 1/6)` explicitly from AK25b.** This is the single cheapest high-value action in
   this document. The paper says the constant can be made explicit, and §7.2 says the proof "uses
   only elementary probabilistic estimates". Everything below depends on whether `L₃` is `10` or
   `10^{10}`. **Not done here** (I did not read AK25b).
2. **Extend BW92/Pec08 from `π ≤ 6` to `π ≤ L₃`, at width `≤ 3`.** Those papers are hand proofs for
   all `n` at fixed small range, so they are the precedent for the form of argument. The paper says
   their methods "break down for larger `D`" (p.3). That remark is about general width; whether
   width `≤ 3` rescues them is **not examined**.
3. **The transfer-matrix route (§3.2, CONJECTURED).**
4. **The sibling repo's own residuals, restricted to the slice.** The width-3 repository has two
   residuals: the Route-B small-`γ`-tail hole (F25/F27) and the `case3Witness_hasBalancedPair_outOfScope`
   axiom (`lean/OneThird/Step8/Case3Residual.lean:208`). Both now need to hold only for
   `7 ≤ π ≤ L₃`. **Whether either becomes easier on that slice was NOT examined.** One thing I did
   look at: the axiom's regime (`n ≤ 6w+6`, `K ≤ 2w+2`, band interaction width `w`) does **not**
   by itself bound `π` from below. `w` is an upper bound on how far incomparabilities reach, so a
   poset can carry a large `w` with small range. The slice therefore does not obviously discharge
   the axiom. **Negative, not a proof of impossibility.**

Thm 1.3 does **not** help here: `C_BFT + η_D < 1/3`.

### 2.10 Rows 6, 10, 11, the Step-6 hole, literature bounds — **UNCHANGED (L4 repriced in scope)**

- **Row 6, Theorem E** — proven any width. H adds nothing. UNCHANGED.
- **Row 10, L3 (`FP`, 125/126 at `n ≤ 6`)** — still `FP`. Its population is still the one that
  says nothing past `n = 6`. UNCHANGED.
- **Row 11, L4** — still OPEN. Under H it needs to hold only on `{frozen, π ≤ L*}`. **This is now
  where the programme's contradiction must come from past `N₁`** (§2.1). REPRICED in scope only.
- **Step-6 hole (mg-3af9)** — "independent of L1b", so independent of H. UNCHANGED.
- **Literature `n`-bounds** (`n ≥ 12` Pec06, `n ≥ 15` Gup26, `n ≥ 100` primitive, `n ≈ 900C`
  mg-33f5) — each is `≪ N₁`. UNCHANGED, and still not a discharge of anything here.

### 2.11 The repo-wide sweep for "wide"/"dense" premises

The sweep is §4. It was made as a claim sweep, not a phrase sweep.

---

## 3. How to use it to make progress — two proposals, both CONJECTURED

### 3.1 Get a number for `L*` (and `L₃`) before anything else

Every repricing above is "automatic at `n ≈ 50L*`". Whether that is progress depends entirely on
`L*`. Two separate extraction tasks:

- `L₃ = L(4, 1/6)`, from AK25b only. This decides whether width 3 is a bounded-range question
  with small `D`.
- `L* = L(K+1, 1/6)`, which also needs `K` from §6.

**CONJECTURED:** `L*` is at least as astronomical as `K`. That is a guess from the shape of the
arguments, not a derivation.

### 3.2 The transfer-matrix route: bounded range is a finite-state structure

By F2, list the elements in any linear extension. Each element is incomparable only to elements
within distance `2D−1`. So a range-`≤ D` poset is a word over a finite alphabet, the local
comparability pattern in a sliding window, and the set of all such posets is a regular family.
Counting linear extensions is a dynamic program over down-sets. The state is the down-set's frontier
inside the window, which takes finitely many values for fixed `D`. So `e(P)`, and every pair count
`#{g : g(x) < g(y)}`, is a product of transfer matrices. **The finite-state description is PROVEN
(it follows from F1/F2). What follows is not.**

**CONJECTURED lemma (decay of correlations).** For fixed `D`, and for primitive range-`≤ D` posets,
`P[g(x) < g(y)]` for `x, y` in the first `k` windows depends on the rest of the poset only up to an
error `≤ C_D·λ_D^k`, with `λ_D < 1`. This is a Birkhoff-contraction statement for products of the
transfer matrices, and it would need the matrices to be uniformly primitive over bounded blocks.

**If it holds**, then "no counterexample of range `≤ D`" reduces to a finite computation over
bottom-prefixes of bounded length, with certified error. That is exactly how KSBFT's own mechanism
and BW92 find their balanced pairs: at the **ends** of the poset (the Fibonacci endpoint pairs reach
`≈ 0.382`, p.4). Combined with §3.1 this could turn H into a proof, **if `L*` or `L₃` is small enough
to compute at**.

**Why it might fail:** ordinal-sum and near-ordinal-sum structure is exactly where the matrices lose
primitivity. That is plausibly benign, since an ordinal sum decouples. I have not checked it.
**Nothing here is proven beyond the finite-state description.**

---

## 4. Sweep of STATE.md and docs/ for premises about wide or dense `P`

**How the sweep was made.** An `Explore` sub-agent read STATE.md, EXECUTIVE-SUMMARY.md,
docs/CONCEPTS.md, docs/FACTS.md, docs/BASIC-FACTS.md, docs/why-one-third-elementary-anchor.md,
docs/state-history/ and the non-audit docs/OneThird-*.md. It was told to find claims whose premise
or pricing depends on wide, dense, large-range, `Θ(n²)`-inversion or `n log n`-entropy counterexamples.
I read the load-bearing hits myself before classifying them. Anything I did not read is marked
*agent-reported*.

The table has **one row per claim**, not one per phrase. *Read* means I read the passage myself.
*Agent* means the passage was located and quoted by the sub-agent and I rely on its quote.

| site | claim, and its hidden premise | verdict under H | mark | read? |
|---|---|---|---|---|
| `STATE.md:21`, `:72`, `:123`; `EXECUTIVE-SUMMARY.md` "factor of roughly fifty"; mg-0e8c `:33-36` | the open content is the ~50× between `ε_sup` and `ε_dem`, and the open region is the DENSE one. **Premise: a counterexample may have `d = Θ(1)`.** | **REPRICED, inverted** (§2.2). Closed for `n ≥ 50L*+1`. | PROVEN (cond.) | read |
| mg-0e8c `:238-240` | *"a minimal counterexample is not known to be"* sparse | **REPRICED.** Under H it is known: `d ≤ L*/(n−1)`. | PROVEN (cond.) | agent |
| mg-ac0c `:254-256`, `:283-284`; mg-7564 `:117-118` | every demand/supply table is evaluated at `d = 1`; *"in the sparse regime nothing is needed"* | **AUTOMATIC** past `50L*`, by the ledger's own sentence | PROVEN (cond.) | agent |
| `EXECUTIVE-SUMMARY.md` *"we have proved that our current method never will"*; `CONCEPTS.md:146-150` *"pair-by-pair information is exhausted"* | exhaustion is proved at the two-atom law, `d = 1` | **UNCHANGED as a theorem about `M_n(η)`. REPRICED as a verdict about counterexamples:** pair bias plus H gives `ε_spec ≤ L*n/(n²−1)` (§2.3) | PROVEN (cond.) | read |
| `STATE.md:143`, `:23`; `CONCEPTS.md:59-60` (obstruction 4) | both faces are false for abstract frozen distributions, so a proof must use realizability | **REPRICED.** H **is** a realizability fact, and it excludes the witness (`Θ(n²)` inversions needs `Θ(n²)` incomparable pairs, against `≤ nL*/2`) | PROVEN (cond.) | read |
| mg-6bc2 `:238-246` | `d` is the only lever, uncontrolled from above | **REPRICED:** `d ≤ L*/(n−1)` | PROVEN (cond.) | read |
| `STATE.md:158-160`, `:185-187`; mg-0b96 `:12-38`; mg-9b6b dial table; mg-3da1 `:182-197`; `CONCEPTS.md:181`, `:201-203` (BELIEF: density ceiling); `FACTS.md` F23 `:809`, F26 `:1030-1036`, F2 `:168-170` | `(R)`: no provable frozen density ceiling below `1 − Θ(1/n)`; every density fact is a lower bound; CONCEPTS records the ceiling as an unearned **belief** | **AUTOMATIC for `n ≥ L*/D + 1`** (§2.7). The CONCEPTS belief becomes **conditionally proven** at large `n`. "No lever at computable `n`" **still holds.** | PROVEN (cond.) | read (0b96, 9b6b); agent (others) |
| mg-0b96 `:44-47` | a named family at `d ∈ [0.838, 0.947]` that nothing on the record decides | **MOOT for counterexamples at large `n`.** The family is dense, so its range is `Θ(n)` and exceeds `L*` once `n` is large enough. It says nothing at small `n`. | PROVEN (cond.) | agent |
| mg-0b96 `:161-165` | every exclusion on the record cuts the sparse side and pushes `d` up | **REPRICED, inverted.** H cuts the **dense** side. | PROVEN (cond.) | agent |
| mg-7ae5 `:94-105`, `:350-354` (Step `(T)`, the absent step) | *"there is no density at which the hole is filled"* (§4), alongside *"`(T)` closes if a frozen poset's density is bounded"* (candidate 1) | **UNCHANGED, as far as I can tell.** H puts counterexamples at `d = Θ(L*/n)`. That is the `d → 0` scaling where §4 found the refuting family (`d = 2/n`) calibrated to the requirement with margin `→ 1`. So density alone does not fill `(T)` under H. ⚠️ I did not reconcile §4 with candidate 1 and did not re-derive §4's arithmetic. | CONJECTURED | read |
| `STATE.md:160-165`; mg-5987 `:29-35`, `:98-103`; `CONCEPTS.md:198-200` (BELIEF: `(B-cov)` is where the answer is) | `(EQ)` and `(B-cov)` have no unconditional reading. The antichain witnesses this, with `max\|h − rank_e\| = (n−1)/2`. | **AUTOMATIC / MOOT in existence form. UNCHANGED at the useful constants** (§2.6). The CONCEPTS belief about `(B-cov)` loses its reason at large `n`, because `(B)` no longer needs it. | PROVEN (cond.) | read (5987) |
| `STATE.md:136-137` (single lemma); mg-c3ca `:164-172`; `proof-chain-riders.md:43`; `CONCEPTS.md:174`; attempt-mg-a58f `:26`, `:70`; `FACTS.md` F3 `:191`, `:195` (`Var(pos_x)` unbounded) | `(B)` fails via block-crossers of `Θ(n)` mobility, e.g. `C_m ⊔ C_1` | **AUTOMATIC** (§2.4). Every witness named there has range `Θ(n)`. Under H, `Var(pos_x) ≤ (L*+1)²/4` by F1. | PROVEN (cond.) | read (STATE); agent (rest) |
| attempt-index `:24`; threads-chronology `:19` | slot probabilities must decay, *"prove that, and the wall falls"* | **AUTOMATIC.** The slot law of `x` is supported on `π(x)+1 ≤ L*+1` slots (F1). | PROVEN (cond.) | agent |
| `STATE.md:123`; `CONCEPTS.md:173`; ledger-row-8 `:132`, `:156` | no `N₀` works for the class; *"only a rate would give one"* | **UNCHANGED as logic. H supplies the rate**, so `N₀ = ⌈L*/ε⌉+1` (§2.5) | PROVEN (cond.) | read |
| Op-Form `:618-631`, `:634-645` (§7.4) | the master bound cannot deliver below `~100` elements, and above that it needs near-chain density; the `(LIB)` constant `C` is unknown, with crossover at `n ≈ 900C` | **REPRICED:** `C = L*/6`, and the crossover is at `n ≈ 50L*` | PROVEN (cond.) | agent |
| mg-33f5 `:121-125`, `:134-135`; `BASIC-FACTS.md:24`; `why-one-third…:18` | literature thresholds. **Peczarski 2008 proves 6-thin, i.e. range `≤ 6`.** | **UNCHANGED.** Consistent with H and sharpens it: a counterexample has `7 ≤ π ≤ L*`. `n ≥ 15` is still `≪ N₁`. | PROVEN | agent (33f5 quote) + read (KSBFT p.3 cites Pec08) |
| mg-c3ca `:198-209` | `(LIB-weak) ⟹ log(n!/e(P)) = ω(n)`, discharged via `w = o(n)` from the large-width result | **REPRICED:** `w ≤ K` (H_w) | PROVEN (cond.) | agent |
| mg-9d9e `:219-225` (*"dense means wide"*), `:13-24`, `:151`, `:204`, `:252`; mg-0fc6 `:31-33`, `:109-113`; mg-99f4 `:88-92`, `:104-106` | `n log₂ w` is vacuous where needed; the shape-A frontier is at `16,777,063` | **REFUTED / REPRICED** (§2.8) | PROVEN (cond.) | read (9d9e); agent (0fc6, 99f4) |
| mg-00a1 `:10-12`, `:34`; mg-abe8 `:29-31`, `:249-250`; mg-200d `:118` | the per-slot LP value is `Θ(n²)`, witnessed by a staircase between two chains, so *"Daniel's route is dead, not re-based"* | **REPRICED.** On range `≤ L*`, mg-131e's own trivial dual gives `val ≤ \|I\|/3 ≤ nL*/6`, i.e. `c·n` with `c = L*/6`. The route is re-based at a useless constant, and adds nothing beyond F4. The staircase witness has range `Θ(n)`. | PROVEN (cond.), using mg-131e's dual as cited, not re-derived | read (00a1) |
| mg-abe8 (search reach) | the population is `2^{Θ(n²)}`, and a structural result would have to shrink it | **REPRICED.** Range-`≤ D` posets on `n` elements number at most `2^{(2D−1)n}` up to isomorphism. List a poset along one of its linear extensions. By F2 every pair at distance `≥ 2D` in that list is comparable, oriented forwards, and every pair at distance `< 2D` is either forwards-comparable or incomparable. That is at most `(2D−1)n` binary choices. | PROVEN (crude bound) | agent (abe8's quote); count is mine |
| `STATE.md:3` *"width-3 is old-repo baggage"*; mg-957a `:89-93`; attempt-index `:18` (width `≥ 4`, `n ≥ 10` gap **DROPPED for tractability**), `:19` (mg-c47a: low-δ ⟺ bounded-width equivalence, **PROVEN**) | bounded-width machinery is off-route | **REPRICED.** Under H_w every counterexample has bounded width (`≤ K`), so bounded-width machinery is **on**-route. The mg-c47a DROP was on tractability grounds only; H changes the value side of that call, not the tractability side. | PROVEN (cond.) that it is on-route; whether to re-open is pm-onethird's call | read (STATE, attempt-index) |
| Op-Form `:580-582` (antichain prefix `Δ₁ ≥ 1/2`) | calibration at the antichain | **UNCHANGED**, and irrelevant: the antichain is not a counterexample | — | agent |

---

## 5. Recommendations to pm-onethird (no edits made)

1. **Do not edit row 8 yet. Carry this as a CONDITIONAL rider.** Suggested wording: *"Conditional on
   AK25a, AK25b and Haq26 (KSBFT Thms 1.4–1.5), every counterexample has range `≤ L*` and `d ≤
   L*/(n−1)`, so L1b holds for `n ≥ L*/ε_dem + 1` and is equivalent to a finite statement below
   that; `L*` is not explicit."* Kind: `U` *conditional on preprints*. The ledger has no such kind,
   and **whether to add one is your call**. Do not mark it `U` bare.
2. **mg-cace: leave PARKED; re-scope on unpark** (§2.8). Close it only if H is adopted as a working
   hypothesis.
3. **mg-6bc2 (done): no reopening.** Its Claim 3.1 stands. This document is the answer to "is
   Daniel's `3L*/ε` right": yes, and `L*/ε` with frozenness.
4. **Width-3: file an extraction ticket for `L(4, 1/6)` from AK25b** (§3.1). It is the cheapest
   action that can change a verdict here.
5. **The CONCEPTS/EXECUTIVE-SUMMARY sentence "closing the gap needs a realizability fact" now has a
   conditional instance** (§2.3). Worth one clause, conditionally, if you touch that file.
6. **Audit targets for the independent audit polecat:** F1, F2 (including the `−1`), F4's
   frozen factor, §2.1's two thresholds, §2.7's `Z_n` zero-orders argument, and §2.9's claim that
   width 3 needs AK25b only.

---

## 6. What I did NOT do, and the negatives

**Not done:**

- I did **not** read AK25a, AK25b or Haq26, so every "(cond.)" inherits their status unexamined.
- I did **not** verify KSBFT's Lemma 4.2, its constant `441`, eq. (1.5), or anything in §6 (the proof
  of Thm 1.4). None of them is consumed here.
- I did **not** extract `L*`, `L₃` or `K`.
- I did **not** attempt the §3.2 decay lemma.
- I did **not** examine whether the width-3 repo's Route B or its Case-3 axiom simplify on
  `7 ≤ π ≤ L₃`. The one check I made is recorded in §2.9 item 4.
- I did **not** edit STATE.md, EXECUTIVE-SUMMARY.md, CONCEPTS.md or FACTS.md, and closed no ticket.
- I added **no** `code/` directory. The instrument in Appendix A is inlined, not committed as a
  script, so no census or gate transcript in this repository moves.
- I did not re-derive the ticket's "two parallel chains `~ n^1.5`" figure. It is not consumed.

**Negatives, with the candidates tried:**

- *Does bounded range bound `n`?* **No.** Candidate: `Z_n`, with `π = 2` at every `n` (§2.7).
- *Does the width-3 Case-3 axiom's regime force large range, so that AK25b discharges it?*
  **Not by itself.** A large `w` is compatible with small `π` (§2.9).
- *Does H lower `(EQ)` or `(B-cov)` to the constants mg-5987 needs?* **No.** F1 gives `L*`, and I
  found no sub-`L*` bound.
- *Does H give anything at `n ≤ 98`, the primitive-floor regime?* **No** (§2.7).
- *Is `L* ≥ K` forced?* **I found no argument either way**, and I claim neither.

---

## Appendix A — EMPIRICAL sanity check of F1, F2, F4, F5, F6, F7 (not a proof)

This checks every naturally labelled poset on `2 ≤ n ≤ 6`, which is 5 230 labelled posets and
covers every isomorphism class. Each positive check `Ck` is paired with a **negative control** `Nk`:
the same bound tightened by one unit must **fail somewhere**, or the instrument could not have
detected a failure. The script ran in about 2 s. It is standard-library Python with exact rationals
for C6. It is reproduced here verbatim, sha1 `351c990d8cb1cecf62957756f518e8235bbb3342`.

| check | statement | holds | control (tightened) fires on |
|---|---|---|---|
| C1 / N1 | F1 `\|g(x) − e(x)\| ≤ π(x)` / window attained (`max−min pos = π(x)`) | 5230/5230 | 5225 (every non-chain) |
| C2 / N2 | F2 `d(x) − d(y) ≤ π(y) − 1` / with `−2` | 5230/5230 | 3404 |
| C3 / N3 | F2 `\|g(x) − g(y)\| ≤ π(x) + π(y) − 1` / with `−2` | 5230/5230 | 3404 |
| C4 / N4 | F6 `e(P) ≤ Π(π(x)+1)` / with `Π max(1, π(x))` | 5230/5230 | 282 |
| C5 / N5 | F5 `E Σdisp² ≤ D·E Σ\|disp\|` / with `D − 1` | 5230/5230 | 187 |
| C6 | F7 `P[flip] ≥ (D+1)^{−2(D+1)}` | 5230/5230 | (no control; the bound is very loose at these `n`) |

**The control N2 is what found F2's `−1`.** The first draft checked `≤ π(y)` and `≤ π(y) − 1` as its
control. That control never fired at `n ≤ 5`, which is how I learned the sharper bound holds; the
proof in §1.2 was written after. F4 is not checked separately: it is `E[inv_e] ≤ m` (trivial) and
the frozen factor `q < 1/3`, and the frozen class is empty at these `n`.

```python
"""mg-1911: exhaustive check of the elementary bounded-range inequalities used in
docs/KSBFT-C-programme-repricing.md §1, over every naturally labelled poset on n <= NMAX
elements (every isomorphism class has a natural labelling, so this covers all posets).
Each positive check is paired with a NEGATIVE CONTROL: the same bound tightened by one
unit (or by a factor), which must FAIL somewhere, or the instrument is not able to fire."""
import itertools, math, sys
from fractions import Fraction as Fr

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

def posets(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    # choose cover-free relation sets, keep only transitively closed ones
    for mask in range(1 << len(pairs)):
        rel = {pairs[k] for k in range(len(pairs)) if mask >> k & 1}
        ok = True
        for (a, b) in rel:
            for c in range(b + 1, n):
                if (b, c) in rel and (a, c) not in rel:
                    ok = False; break
            if not ok: break
        if ok:
            yield rel

def lin_exts(n, rel):
    below = [[a for a in range(n) if (a, b) in rel] for b in range(n)]
    out = []
    def rec(placed, seq):
        if len(seq) == n:
            out.append(tuple(seq)); return
        for x in range(n):
            if x not in placed and all(a in placed for a in below[x]):
                placed.add(x); seq.append(x); rec(placed, seq); seq.pop(); placed.discard(x)
    rec(set(), [])
    return out

stats = {k: 0 for k in ["posets", "C1", "C2", "C3", "C4", "C5", "C6",
                        "N1", "N2", "N3", "N4", "N5"]}
fail = []
for n in range(2, NMAX + 1):
    for rel in posets(n):
        stats["posets"] += 1
        comp = lambda a, b: (min(a, b), max(a, b)) in rel
        inc = [[y for y in range(n) if y != x and not comp(x, y)] for x in range(n)]
        pi = [len(s) for s in inc]; D = max(pi)
        d = [sum(1 for a in range(n) if (a, b) in rel) for b in range(n)]
        L = lin_exts(n, rel); e = len(L)
        pos = [[0] * n for _ in L]
        for k, s in enumerate(L):
            for i, x in enumerate(s): pos[k][x] = i + 1
        ref = pos[0]                      # any linear extension serves as e
        # C1 |g(x) - e(x)| <= pi(x); N1: <= pi(x)-1 must fail somewhere
        c1 = all(abs(p[x] - ref[x]) <= pi[x] for p in pos for x in range(n))
        # N1: the window is attained: for some x with pi(x)>0, max_g - min_g position = pi(x)
        n1 = all(max(p[x] for p in pos) - min(p[x] for p in pos) <= pi[x] - 1 for x in range(n) if pi[x] > 0)
        # C2 x||y => d(x)-d(y) <= pi(y)-1 (x itself is incomparable to y and not below x);
        # N2: <= pi(y)-2 must fail somewhere
        c2 = all(d[x] - d[y] <= pi[y] - 1 for x in range(n) for y in inc[x])
        n2 = all(d[x] - d[y] <= pi[y] - 2 for x in range(n) for y in inc[x])
        # C3 x||y => |g(x)-g(y)| <= pi(x)+pi(y)-1 ; N3: <= pi(x)+pi(y)-2 must fail somewhere
        c3 = all(abs(p[x] - p[y]) <= pi[x] + pi[y] - 1 for p in pos for x in range(n) for y in inc[x])
        n3 = all(abs(p[x] - p[y]) <= pi[x] + pi[y] - 2 for p in pos for x in range(n) for y in inc[x])
        # C4 log e(P) <= sum log(pi(x)+1) ; N4: e(P) <= prod(pi(x)+1) / 2 when P not a chain
        prod = math.prod(q + 1 for q in pi)
        c4 = e <= prod
        n4 = e <= math.prod(max(1, q) for q in pi)   # drop the +1: must fail somewhere
        # C5 E[sum disp^2] <= D * E[sum |disp|] ; N5: with D-1 (only meaningful if D>=1)
        s2 = sum(sum((p[x] - ref[x]) ** 2 for x in range(n)) for p in pos)
        s1 = sum(sum(abs(p[x] - ref[x]) for x in range(n)) for p in pos)
        c5 = s2 <= D * s1
        n5 = (D <= 1) or (s2 <= (D - 1) * s1) or s1 == 0
        # C6 KSBFT Lemma 3.1, m=2: x||y => P[g(y)<g(x)] >= (D+1)^(-2(D+1))
        c6 = True
        for x in range(n):
            for y in inc[x]:
                cnt = sum(1 for p in pos if p[y] < p[x])
                if Fr(cnt, e) < Fr(1, (D + 1) ** (2 * (D + 1))): c6 = False
        for k, v in [("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4), ("C5", c5), ("C6", c6)]:
            if v: stats[k] += 1
            else: fail.append((k, n, sorted(rel)))
        for k, v in [("N1", n1), ("N2", n2), ("N3", n3), ("N4", n4), ("N5", n5)]:
            if not v: stats[k] += 1   # count posets where the tightened bound FAILS
print("n <= %d, naturally labelled posets checked: %d" % (NMAX, stats["posets"]))
for k in ["C1", "C2", "C3", "C4", "C5", "C6"]:
    print("  %s holds on %d / %d" % (k, stats[k], stats["posets"]))
for k in ["N1", "N2", "N3", "N4", "N5"]:
    print("  %s (tightened bound) FIRES on %d posets  -> %s" % (k, stats[k], "control OK" if stats[k] else "CONTROL DID NOT FIRE"))
print("failures of C-checks:", len(fail), fail[:3])
```

Output (`python3 range_checks_1911.py 6`):

```
n <= 6, naturally labelled posets checked: 5230
  C1 holds on 5230 / 5230
  C2 holds on 5230 / 5230
  C3 holds on 5230 / 5230
  C4 holds on 5230 / 5230
  C5 holds on 5230 / 5230
  C6 holds on 5230 / 5230
  N1 (tightened bound) FIRES on 5225 posets  -> control OK
  N2 (tightened bound) FIRES on 3404 posets  -> control OK
  N3 (tightened bound) FIRES on 3404 posets  -> control OK
  N4 (tightened bound) FIRES on 282 posets  -> control OK
  N5 (tightened bound) FIRES on 187 posets  -> control OK
failures of C-checks: 0 []
```
