# KSBFT-F — L4, the Step-6 hole, L3, L2 and row 3b under bounded range

`mg-b447`, 2026-09-26. Follows mg-1911 (`docs/KSBFT-C-programme-repricing.md`) and its audit mg-2ec1
(`docs/AUDIT-mg-1911.md`). **Nothing in `STATE.md` was edited. Every verdict below is a
recommendation to pm-onethird.** An independent audit is pre-filed.

Marks, as in KSBFT-C:

- **PROVEN** — the proof is written out here and is elementary. **PROVEN (cond.)** means proven
  *from* **H**, which is conditional on the three preprints (AK25a, Haq26, AK25b; see KSBFT-C §1.1).
  A statement proven for the class `Π_D := {P : π(P) ≤ D}` with `D` a free parameter is
  **unconditional**. It becomes a statement about counterexamples only through H.
- **EMPIRICAL** — instrument and range named. `code/ksbft_f_b447/check.py 6`, transcript
  `out_check.txt`. It shows the arithmetic is right. It proves nothing at unbounded `n`.
- **CONJECTURED** — a belief or a proposed statement.

`π(x)` is the number of elements incomparable to `x`, and `π(P) = max_x π(x)` is the **range**
(KSBFT p.3). **H**: a counterexample has `π(P) ≤ L*` (KSBFT-C §1.1; audited HOLDS, mg-2ec1).

---

## 0. Verdict

> **The first check comes back positive: every witness that obstructs these links already has
> bounded range, and small range.** `W*` has range **3**. mg-63e3's `W` has range 3. The N-poset
> (`2+2`, and the `n = 4` N) has range 2. mg-f5be's fence is the Fibonacci poset, which has range 2.
> The generalisation `W*_t` has range `t+1` for every `t ≥ 2` (EMPIRICAL checks in §3; the ranges
> are also immediate by hand). **So H buys nothing against any of them.**
>
> **What H does do is sharper than "nothing", and it goes the wrong way for the architecture:**
>
> 1. **L4 restricted to `Π_D` is PROVEN, for every `D`, unconditionally, with an explicit linear
>    modulus** `F_D(ε) = (2D−1)(1+f(D))·ε/2` (Theorem 3.1). **Every instance is discharged
>    through branch (ii).** Branches (i) and (iii) are never used. Under H, L4 therefore holds for
>    every poset that could be a counterexample. **It is true and empty**, like L1b past
>    `N₁` (KSBFT-C §2.1).
> 2. **The Step-6 hole does not close.** Its witness `W*` has range 3. `W*_t` puts the same
>    obstruction in every range window `[r, D]` with `3 ≤ r ≤ D`. That includes `[7, L*]`, the only
>    window where a counterexample can live. **Under H it gets worse, not better.** By item 1,
>    *every* prefix cut of a range-`≤ D` poset is in branch (ii), so Step 6 must consume branch (ii)
>    at every cut, and branch (ii) is exactly the branch whose transfer `W*` refutes.
> 3. **The one live repair, (IB), becomes the conjecture itself.** Restricted to `Π_D` with any
>    positive budget, (IB) is **equivalent** to "every non-chain in `Π_D` on at least `N(D,ε)`
>    elements has a balanced pair" (Prop 4.2, PROVEN). The architecture contributes **no reduction**
>    of it.
> 4. **L3 (row 10), L2's second disjunct (row 9) and F-bal drop out.** What the chain consumes
>    from them, a thin balanced prefix, is **automatic** on `Π_D` for `n ≥ 2D/ε + 2` (Prop 5.1,
>    PROVEN). Their literal statements are untouched, because their refuting or excepting instances
>    live at `n ≤ 7`, where every poset has range `≤ 6`.
> 5. **Row 3b drops off the route and is not decided.** Its unconditional form is refuted at
>    `n = 7`, where every poset has range `≤ 6`. Its conditional form feeds node `B`, which no live
>    route consumes (mg-05ec). Node `C` is automatic past `N₁` (mg-1911).
> 6. **Range plus frozen**, the combination the audit left unexamined, gives `(EQ)` with the
>    constant **`< π(x)/3`**, pointwise (Prop 7.1, PROVEN). That is a factor-3 improvement on
>    range alone, and it is still useless at mg-5987's `C < 0.30`. The combination gives nothing
>    for L4 or Step 6 beyond what mg-3af9 §4.1 already priced: restricting to frozen `P` renames
>    the problem.
>
> **Net (§8).** Under H, past `N₁`, the programme's links L1b, L2, L3 and L4 all hold or have lost
> their meaning. Row 3b is off the route. The remaining content is exactly **"there is no minimal
> counterexample of range `≤ D`"**, with `D` a free parameter, since `L*` has no value. That is the
> 1/3–2/3 conjecture restricted to `Π_D`. **The spectral / near-ordinal-sum architecture does not
> reduce it.** The one Step-6-shaped strengthening worth starting on is **(ONE-PT_D)**, §8. Its
> "for every `v`" form is **false** at range 3. Its "exists `v`" form has **0 failures at `n ≤ 6`**
> (EMPIRICAL).

| # | link | witness range | does H help? | status under H | mark |
|---|---|---|---|---|---|
| 1 | L4 (row 11) | N-poset 2, fence = `Z_n` 2, `W`/`W*` 3 | the witnesses never refuted L4. H **proves** L4, via (ii) only | **PROVEN on `Π_D`, every `D`, and empty** | PROVEN (Thm 3.1) |
| 2 | Step-6 transfer `(T)` (mg-3af9) | `W*`: 3; `W*_t`: `t+1`, every `t ≥ 2` | **no.** Stop. | **still refuted**, in every range window `[r,D]`, `3 ≤ r ≤ D` | PROVEN (Thm 4.1) |
| 2′ | (IB), repaired form (mg-63e3 §7, mg-f825 §5) | — | turns it into the target | **⟺ conjecture on `Π_D`, `n ≥ N(D,ε)`** | PROVEN (Prop 4.2) |
| 3 | L3 (row 10), consumed content | exception at `n ≤ 6`, so range `≤ 5` | literal: no. Consumed content: **automatic** | drops out | PROVEN (cond.) (Prop 5.1) |
| 4 | L2 (row 9), both disjuncts | first-disjunct refuters at `n = 6`, range `≤ 5` | first disjunct: no. Second's product: **automatic** | drops out | PROVEN (cond.) for the product; literal reading of the second disjunct NOT EXAMINED |
| 5 | row 3b | refuters at `n = 7`, range `≤ 6` | no, for the unconditional form | off the route. Truth under H NOT EXAMINED | — |
| 6 | `(EQ)` under range + frozen | 2-antichain (range alone, mg-2ec1) | factor 3 only | `\|h(x) − e(x)\| < π(x)/3` | PROVEN (Prop 7.1) |

---

## 1. Statements used, and where they were read

The canonical architecture `spectral_near_ordinal_sum_program.tex` is **not readable from this
machine**. Its iCloud copy returns `Resource deadlock avoided`, which means the file is evicted.
Every statement of it below is taken from the verbatim quotes in mg-63e3 §2
(`docs/OneThird-L4-Branch-ii-Consumability.md:86–90`) and mg-3af9 §§1–2
(`docs/OneThird-L4-Branch-ii-Sublinear-Modulus.md`). **I did not re-verify them at the source.**

**L4** (`:464–474`, as quoted). There is `F(ε) → 0` such that, for every finite `P` and every prefix
cut `(A, B)` of a linear extension `e` with `Δ₁(A,B) ≤ ε`, at least one of these holds:

- **(i)** `P` has a `1/3`-balanced pair;
- **(ii)** after removing or modifying at most `F(ε)·n` interface elements, `P` becomes `P[A] ⊕ P[B]`;
- **(iii)** a balanced pair of `P[A]` or `P[B]` stays balanced in `P`, up to error `F(ε)`.

Here `Δ₁(A,B) = E|A ∖ σ(A)| / min(|A|,|B|)` and `K(σ) := |A ∖ σ(A)|`. There are two readings of
`ε`: **(E1)**, any `ε ≥ Δ₁`, and **(E2)**, `ε = Δ₁` (mg-3af9 §1.1). Everything below holds under
**both**.

**Step 6** (`:513–515`). *"Use near-ordinal-sum stability to transfer a balanced pair from `P[A_k]`
or `P[A_k^c]` to `P`, contradicting minimality."* On branch (ii) it needs mg-63e3's **(T)**: if
`Δ₁ ≤ ε` and `P` is within `F(ε)n` interface modifications of `P[A] ⊕ P[B]`, then some balanced pair
of `P[A]` or `P[B]` is still balanced in `P`.

**Fact 2.1 (source `:254–256`, via mg-3af9).** For a prefix cut there is no relation `b < a` with
`a ∈ A`, `b ∈ B`.

**mg-3af9 Theorem A (re-checked, not re-proved).** For every `σ ∈ L(P)`, put
`X_σ = A ∖ σ(A)` and `Y_σ = σ(A) ∖ A`. Then every pair in `X_σ × Y_σ` is incomparable (∗), and any
branch-(ii) certificate `S` has `|S| ≥ max_σ K(σ)`. X2 re-checks this exhaustively on 25 669
prefix cuts, with 0 violations (EMPIRICAL, `n ≤ 6`).

---

## 2. Three elementary lemmas about range

Throughout, `P ∈ Π_D`, `e` is a linear extension, and `(A, B) = (e⁻¹[1..k], e⁻¹[k+1..n])`.

**Lemma 2.0 (bandwidth: KSBFT-C F2, re-derived here) — PROVEN.** If `a ∥ b`, then in every linear
extension `g`, `|g(a) − g(b)| ≤ π(a) + π(b) − 1 ≤ 2D − 1`.

*Proof.* Let `d(x) = #{v : v < x}`. In any `g`, `d(x) + 1 ≤ g(x) ≤ d(x) + 1 + π(x)`: all
predecessors of `x` come before it and all successors after it. Take `v < b`. Then `v > a` is
impossible, since it would give `a < b`. So `v < a` or `v ∥ a`, and `v ≠ a`. The `v ∥ a` with
`v < b` are incomparables of `a` other than `b`, so there are at most `π(a) − 1` of them. Hence
`d(b) ≤ d(a) + π(a) − 1`, and
`g(b) − g(a) ≤ d(b) + 1 + π(b) − d(a) − 1 ≤ π(a) + π(b) − 1`. By symmetry the same bound holds
for `g(a) − g(b)`. □

**Lemma 2.1 (leakage is at most the range) — PROVEN.** For every `σ`, `K(σ) ≤ D`. Hence
`E K ≤ D` and `Δ₁(A,B) ≤ D / min(k, n−k)`.

*Proof.* If `K(σ) = 0` there is nothing to prove. Otherwise pick `x₀ ∈ X_σ`. By (∗), `x₀` is
incomparable to all `|Y_σ| = K(σ)` elements of `Y_σ`. So `K(σ) ≤ π(x₀) ≤ D`. □
(X3: 0 violations in 25 669 cuts. Control "`K ≤ D−1`" FIRES 47 times.)

**Proposition 2.2 (every prefix cut is `2D−1` elements from an ordinal sum) — PROVEN.** Let
`G_cut` be the bipartite graph on `A ⊔ B` whose edges are the incomparable cross pairs. Write `τ` for
its vertex-cover number.

(a) Under the modification reading, the minimum branch-(ii) certificate has size **exactly `τ`**.
Under the removal reading it is at most `τ`.

(b) Let `I_A = {a ∈ A : a ∥ b for some b ∈ B}`. Then `I_A ⊆ e⁻¹[k−2D+2 .. k]`, so
**`τ ≤ |I_A| ≤ 2D − 1`**. The same holds for `I_B`.

*Proof.* (a) A certificate must meet every edge of `G_cut`: an unmodified, unremoved incomparable
cross pair survives into the result, and the result would not be an ordinal sum with `A` below
`B`. Conversely, let `S` be a vertex cover. Add every relation `a < b` (`a ∈ A`, `b ∈ B`) to `P`.
By Fact 2.1 the result is the relation of `P[A] ⊕ P[B]`, which is a poset. The only pairs whose
status changed are edges of `G_cut`, and each has an endpoint in `S`. So only relations incident to
`S` were modified. Under the removal reading, delete `S`. Every surviving cross pair is comparable,
hence `a < b` by Fact 2.1, and the result is `P[A∖S] ⊕ P[B∖S]`.

(b) Take `a ∈ I_A` with `a ∥ b`, `b ∈ B`. Lemma 2.0 at `g = e` gives
`e(b) − e(a) ≤ 2D − 1`, and `e(b) ≥ k + 1`. So `e(a) ≥ k + 2 − 2D`. `I_A` is a vertex cover. □

(X1: `τ ≤ 2π(P) − 1` holds on all 25 669 cuts, and the ratio `τ/(2D−1)` reaches **1**, so the
bound is attained at `n ≤ 6`. Control "`τ ≤ D−1`" FIRES 137 times.)

**Lemma 2.3 (no flip is negligible, self-contained) — PROVEN.** If `a ∥ b`, then
`P_σ[b before a] ≥ c(D) := 1/(1 + f(D))`, where
`f(D) = Σ_{j=1}^{D} Σ_{r=0}^{2D−1−j} C(j−1+r, r) < 2^{2D−1}`. In particular **`c(D) ≥ 2^{1−2D}`**.

*Proof.* Take `σ` with `a` before `b`. Let `Z` be the set of elements `z` with
`σ(a) < σ(z) ≤ σ(b)` and `z ≤ b` (so `b ∈ Z`). Let `R` be the other elements strictly between `a`
and `b`. Let `σ'` be `σ` with the block `Z`, in its `σ`-order, moved to just before `a`. So `σ'`
reads `… Z a R …`.

`σ'` is a linear extension. First, `z ∈ Z ∖ {b}` comes after `a`, so `z ≮ a`. And `a < z ≤ b` would
give `a < b`. So `Z ⊆ inc(a)`, and `a` may follow `Z`. Second, if `r ∈ R` and `r < z` for some
`z ∈ Z`, then `r ≤ b`, so `r ∈ Z`, which is a contradiction. So `R` may follow `Z`. All other
relative orders are unchanged.

In `σ'`, `b` is before `a`. Given `σ'`, the preimage `σ` is determined by three things: `j = |Z|`,
`r = |R|`, and the interleaving of `Z ∖ {b}` with `R`. `b` is last, so there are
`C(j−1+r, r)` interleavings. Here `1 ≤ j ≤ π(a) ≤ D` because `Z ⊆ inc(a)`. And
`j − 1 + r ≤ 2D − 2` by Lemma 2.0. So the map is at most `f(D)`-to-one, and
`P[a before b] ≤ f(D)·P[b before a]`. Since the two probabilities sum to 1, the claim follows.
For the bound on `f`: grouping by `m = j−1+r`, the inner sum over `j` is at most `2^m`, and
`Σ_{m=0}^{2D−2} 2^m < 2^{2D−1}`. □

(X4: 0 violations over 86 340 ordered incomparable pairs. Control "`≥ 1/2`" FIRES 37 588 times.
`c(1) = 1/2` is attained by the 2-antichain. `c(D) ≥ 2^{1−2D}` holds for `D ≤ 20`.)

*Aside, not consumed.* This beats KSBFT Lemma 3.1 at `|S| = 2`, `q₂ = (D+1)^{−2(D+1)}`, by a
margin that grows with `D`: `1/26` against `1/65 536` at `D = 3`. KSBFT's Thm 1.3 loses `q₂²`. mg-d707
already routes around `q₂` (`d₁ ≥ 1/(D+1)`), so **I do not claim this improves Thm 1.3**, and I
did not check whether it does.

---

## 3. Item 1 — L4 under bounded range

### 3.1 The first check: the witnesses' ranges (EMPIRICAL, `out_check.txt` §W; also by hand)

| witness | where | range `π(P)` | by hand |
|---|---|---|---|
| N-poset `2+2 = {x₁<y₁, x₂<y₂}` | KillShot probe (sibling repo, `:101`, `:241–273`) | **2** | each element is incomparable to the other chain's two |
| N-poset `{0<2, 0<3, 1<3}`, `n = 4` | mg-f5be | **2** | `1 ∥ 0, 2` and `2 ∥ 1, 3` |
| fence argmax at `n = 8` | mg-f5be `:331` | **2** | its transitive closure **is** the Fibonacci poset `Z_8` (`i < j ⟺ j − i ≥ 2`), checked exhaustively; `Z_m` has range 2 for all `m` |
| `W` (`t = 2`) | mg-63e3 | **3** | `x ∥ y, b₁, b₂` |
| `W*(a, b)` | mg-3af9 | **3** | the same, for every `b` |
| `W*_t` (`t` crosses deleted) | §4 below | **`t + 1`** | `x ∥ y, b₁ … b_t` |
| `C_a ⊕ C_a` minus `t` crosses | mg-63e3 §7 | **`t`** | `c_a ∥ b₁ … b_t` |

**So every obstruction on record has range `≤ 3` (and `W*_t` supplies any range `≥ 3`). H buys
nothing against any of them.** The N-poset was never a counterexample to L4. `δ(2+2) = 1/2`, and
the `n = 4` N-poset has `δ = 2/5`, so both satisfy (i). It was an obstruction to a proof
*mechanism*: the best prefix has maximally fat interface, `Δ₁ = 1/2`. That mechanism is moot
under Theorem 3.1.

### 3.2 L4 on `Π_D` is a theorem, discharged through branch (ii) alone

> **Theorem 3.1 — PROVEN (unconditional, every `D ≥ 1`).** Put
> `F_D(ε) := (2D−1)·ε / (2c(D)) = (2D−1)(1+f(D))·ε/2`, which is `≤ (2D−1)·4^D·ε/2`. Let `P ∈ Π_D`,
> let `(A,B)` be a prefix cut of a linear extension `e`, and let `Δ₁(A,B) ≤ ε`. Then **branch (ii)
> holds with budget `F_D(ε)·n`**. So L4 holds on `Π_D` with modulus `F_D`, and `F_D(ε) → 0`. This
> is true under (E1) and (E2), and under both the removal and the modification readings.

*Proof.* If `G_cut` has no edge, then `P = P[A] ⊕ P[B]` and branch (ii) holds with `S = ∅`.
Otherwise fix an edge `a ∥ b`. If `b` precedes `a` in `σ`, then `σ(A) ≠ A`, so `K(σ) ≥ 1`. So by
Lemma 2.3, `E K ≥ P[b before a] ≥ c(D)`. Then
`ε ≥ Δ₁ = E K / min(k, n−k) ≥ c(D)/(n/2)`, so `n ≥ 2c(D)/ε`. Hence
`F_D(ε)·n ≥ (2D−1)ε/(2c(D)) · 2c(D)/ε = 2D − 1 ≥ τ` by Prop 2.2(b). By Prop 2.2(a), a certificate
of size `τ` exists. □

**Consistency with mg-3af9 Cor. A2** (branch (ii) at balance `β` under (E2) needs `F(ε) ≥ βε`):
`F_D(ε)/ε = (2D−1)/(2c(D)) ≥ 1/2 ≥ β`. ✔

**Under H.** Take `D = L*`. **L4 holds for every poset that can be a counterexample, and for every
prefix cut of it, through branch (ii) alone. PROVEN (cond.)** The modulus is explicit in `L*`,
which itself has no value.

**What this means (PROVEN (cond.) as logic).** An L4 that is always satisfied through (ii) gives
Step 6 nothing to work with except (ii). L4's disjunction was supposed to push the proof into (i),
which contradicts minimality directly, or into a branch Step 6 can consume. On `Π_D` it pushes
every instance into the one branch Step 6 cannot consume (§4). **So under H, L4 is proven and
empty, exactly as L1b is past `N₁`.**

**If one instead picks a sub-linear `F`, to keep balanced cuts out of (ii)** (mg-3af9 Cor. A3), the
burden returns to (iii) on balanced cuts. (iii) as a standalone universal is refuted at every `ε`
by `W`, which is balanced (`a = b`) and has range 3 (mg-f825 F4). So in L4-as-a-disjunction, a
minimal counterexample would need (iii) to hold for *it specifically*. That is a statement about
counterexamples only, i.e. the target again (CONJECTURED as a reading; I did not formalise it).

---

## 4. Item 2 — the Step-6 transfer hole under bounded range

### 4.1 The witness has range 3, so stop

**Theorem 4.1 — PROVEN.** For every `D ≥ 3` and every `3 ≤ r ≤ D`, `(T)` is false on
`{P : r ≤ π(P) ≤ D}` at every strictly positive modulus.

*Proof.* Take `t = r − 1 ≥ 2` and `W*_t(a, b)`: `A = C_{a−2} ⊕ AC_2 = {c₁<…<c_{a−2}} < {x, y}`,
`B = b₁ < … < b_b`, all of `A` below all of `B` except `x < b₁, …, x < b_t`, with `b ≥ max(a, t+1)`.
This is mg-3af9's `W*` with `2` replaced by `t`, and mg-3af9 Lemmas 4.1–4.2 go through verbatim.
Everything except `x` is a chain, and `x` has `t+2` insertion slots, between `c_{a−2}` and
`b_{t+1}`, among `y, b₁, …, b_t`. So:

- `π(x) = t+1 = r`, and every other element has range `≤ 1`;
- `p^P_{xy} = 1/(t+2) ≤ 1/4`, while `p^{P[A]}_{xy} = 1/2`, and `{x,y}` is the sides' only
  incomparable pair;
- `E K = t/(t+2)` and `Δ₁ = t/((t+2)a)`, independent of `b`;
- `S = {x}`, `τ = 1`.

mg-3af9 Theorem B's argument then applies unchanged: fix `a`, set `ε = Δ₁`, take `b ≥ 1/F(ε)`. □
(EMPIRICAL §W: `t = 2, 3, 6, 7` give ranges `3, 4, 7, 8`, `p_xy = 1/4, 1/5, 1/8, 1/9`, `τ = 1`,
and all of mg-3af9's six `W*` rationals at `(4, 28, 2)`.)

**`[7, L*]` is the window that matters.** A counterexample has `π ≥ 7` by Brightwell–Wright (`π ≤ 5`)
and Peczarski (`π ≤ 6`). I cite these and did not re-verify them. `W*_6` has range 7. **H buys
nothing for the Step-6 hole.**

### 4.2 Under H it is worse: the only repair on the table becomes the target

By Theorem 3.1, every prefix cut of a `Π_D` poset is in branch (ii). So on `Π_D`, Step 6 must consume
(ii) at every cut. The only candidate consumer is mg-63e3's (IB), in the repaired form of mg-f825 §5
and mg-3af9 §6.3: *if `P` is not a chain and is within `G(ε)n` interface modifications of
`P[A] ⊕ P[B]` across a prefix cut with `Δ₁ ≤ ε`, then `P` has a `1/3`-balanced pair.*

> **Proposition 4.2 — PROVEN.** Fix `D`, `ε > 0` and `G(ε) > 0`. Put
> `N(D,ε) := max(2D/ε + 2, (2D−1)/G(ε))`. Then **(IB) restricted to `Π_D` ⟺ every non-chain
> `P ∈ Π_D` with `n ≥ N(D,ε)` has a `1/3`-balanced pair.** (On `n < N`, (IB) restricted to `Π_D` is
> implied by the conjecture on `Π_D`, which is all ⟸ needs.)

*Proof.* (⟸) The conclusion of (IB) is the conjecture's. (⟹) Let `P ∈ Π_D` be a non-chain with
`n ≥ N`. Take the middle prefix cut `k = ⌊n/2⌋` of any linear extension. By Lemma 2.1,
`Δ₁ ≤ D/⌊n/2⌋ ≤ 2D/(n−1) ≤ ε`, using `n ≥ 2D/ε + 1`. By Prop 2.2, `P` is within
`τ ≤ 2D−1 ≤ G(ε)n` interface modifications of `P[A] ⊕ P[B]`. So (IB)'s hypothesis holds, and (IB)
gives the balanced pair. □

**So under H, (IB) is the 1/3–2/3 conjecture on the counterexample class, and not a reduction of
it.** This sharpens mg-63e3 §7 property 2 ("(IB) is a special case of the conjecture"): on `Π_D`,
and past an explicit `N`, it is the **whole** case. Minimality is spent **zero** times on this
branch. It starts a spectral chain whose every link is now automatic, and it is not used at
Step 6.

### 4.3 One-point transport: the "for every `v`" form is false at range 3

Step 6 is a transfer from a proper subposet. Its smallest form is one deletion: *a balanced pair of
`P − v` that stays balanced in `P`*. A minimal counterexample offers every `v` with `P − v` a
non-chain.

- **"For every `v`" — REFUTED (PROVEN by hand, EMPIRICAL check §T).** In `W*(4,4,2)`, delete
  `v = b₁`. In `P − b₁`, `x` has three slots among `y, b₂`, so `p_{xy} = 1/3` and
  `p_{x b₂} = 2/3`. Both are balanced, and they are the only incomparable pairs. In `P`,
  `p_{xy} = 1/4` and `p_{x b₂} = 3/4`. **No balanced pair of `P − b₁` survives.** Range 3.
- **"There exists `v`" — EMPIRICAL, 0 failures.** Every non-chain on `3 ≤ n ≤ 6` (5 224
  naturally labelled posets, which covers every isomorphism class) has a pair balanced in `P` and
  in some `P − v` (§S). In `W*` itself, `v ∈ {c₁, c₂, y, b₂, b₃, b₄}` all transport `(x, b₁)`.
  **This says nothing above `n = 6`, and at `n ≤ 6` every non-chain has a balanced pair, so it
  cannot see a frozen poset.** §S has no firing control: no false variant of "exists `v`" was
  planted. Its companion §T shows the same code distinguishing surviving pairs from dying ones on
  `W*`.

---

## 5. Item 3 — L3 (row 10), and F-bal

**Witness check.** Row 10 is `FP`, `125/126` at `n ≤ 6`. Its single exception is not identified
(mg-957a), but it is a poset on at most 6 elements, so its range is at most 5. **For the literal
statement "the best cut is a prefix", H buys nothing** (for any `D ≥ 5`, and `L* ≥ 7` whenever a
counterexample exists at all).

**What the chain consumes from L3 is automatic.** Steps 4–5 need a prefix `A_k` with small `Δ₁`,
i.e. `E K_k ≪ min(k, n−k)`. mg-3af9's F-bal additionally asks for balance `min(k,n−k) ≥ β₀ n`.

> **Proposition 5.1 — PROVEN (unconditional on `Π_D`; PROVEN (cond.) for counterexamples at
> `D = L*`).** For `P ∈ Π_D`, every linear extension `e`, and `k = ⌊n/2⌋`: `β ≥ (n−1)/(2n)`,
> `Δ₁(A_k) ≤ 2D/(n−1)`, and, reading row 5's `leak(A) = E|A ∖ σ(A)|` (the transport-energy
> identity), `n·leak(A_k)/(|A_k||A_k^c|) ≤ 4nD/(n²−1)`. So a thin, balanced prefix exists once
> `n ≥ 2D/ε + 1`, and by row 5 (easy/Buser), `1 − λ_std ≤ 4nD/(n²−1)`.

*Proof.* Lemma 2.1 and `⌊n/2⌋⌈n/2⌉ ≥ (n²−1)/4`. □

**F-bal (mg-3af9 §8), therefore, is answered YES on `Π_D`**, and at no cost in `Φ`: the middle
prefix cut is simultaneously balanced and thin. By mg-3af9 Cor. A3, a sub-linear modulus then empties
branch (ii) on that cut under (E2), and the burden moves to (iii). See §3.2's last paragraph.

**Caveat on "row 5's leak".** I read row 5 as `leak(A) = E|A∖σ(A)|`, following the KillShot probe's
setup (`⟨1_A,(I−S_P)1_A⟩ = E_σ|A∖σ(A)|`). If row 5 normalises differently, only the constant in the
`λ_std` clause changes.

---

## 6. Row 9 (L2) and row 3b — the audit's addition

**Row 9, L2.** L2 is a disjunction (mg-3329): *a dominant standard eigenvector is monotone in `e`,
**or** at least yields a low-conductance prefix*.

- **First disjunct.** It is `FP✗` at `n = 6` (`2/126`). Those refuters have range `≤ 5`. **H buys
  nothing.**
- **Second disjunct.** Its downstream product is a low-conductance prefix, handed to L3/L4. Under
  H that product is **automatic** by Prop 5.1, whatever the eigenvector does. **So row 9 drops out
  of the route: nothing downstream needs L2 once Prop 5.1 supplies the prefix. PROVEN (cond.).**
  If the disjunct is read literally, as "*the eigenvector's own sweep* yields a low-conductance
  prefix", its truth under H is **NOT EXAMINED**. Nothing needs it.

**Row 3b, standard dominance.**

- **Unconditional form.** It is refuted by 166 refuters at `n = 7` (mg-8b64, read by STATE, not by
  me). Those have range `≤ 6`. **H buys nothing** for the statement.
- **Conditional form (all-pairs-frozen).** It feeds node `B` of the proof chain, which is
  unconsumed by every live route (mg-05ec). Node `C` (L1b's conclusion) is automatic past `N₁`
  (KSBFT-C §2.1, audited HOLDS). **So 3b drops off the route under H.**
- **Not claimed.** STATE records `L1b ⟺ "all-pairs-frozen ⟹ standard dominance"` from a sibling-repo
  document (`:449`). I did not read it. **I do not claim that standard dominance becomes true under
  H**, because L1b's *inversion* form being automatic need not transfer to a *spectral block*
  statement. NOT EXAMINED.

---

## 7. Range plus frozen — the audit's open combination (mg-2ec1 D6)

**Identity (U-id, PROVEN; EMPIRICAL check X5, 30 894 element-instances, 0 violations).** Let
`h(x) = E_σ[pos_σ x]`. Then, with positions counted the same way as `e`,

`h(x) − e(x) = Σ_{y ∥ x, e(y) > e(x)} P[y before x] − Σ_{y ∥ x, e(y) < e(x)} P[x before y]`.

*Proof.* `pos_σ(x) = d(x) + 1 + #{y ∥ x : y before x}`, and
`e(x) = d(x) + 1 + #{y ∥ x : e(y) < e(x)}`. Subtract and take expectations. □

> **Proposition 7.1 — PROVEN.** If `P` is frozen with majority order `e`, then
> `|h(x) − e(x)| < max(λ(x), ε(x))/3 ≤ π(x)/3`. Here `λ(x)` and `ε(x)` are the numbers of
> incomparables of `x` that come later and earlier in `e`. Under H: `(EQ)` holds with constant `L*/3`.

*Proof.* In the identity every probability is a flip against `e`, so each is `< 1/3`. The first
sum lies in `[0, λ/3)` and the second in `[0, ε/3)`. □

**What this buys: a factor of 3 over range alone** (KSBFT-C §2.6 had `≤ π(x)`). **It is useless at
mg-5987's constants** (`C < 0.30` / `2/5`), since it is below `0.30` only for `max(λ, ε) = 0`.
The audit's 2-antichain (range alone: `1/2 ≥ 2/5`) is not frozen, and the bound above is how
frozenness disposes of it: at `π = 1` the bound is `< 1/3`. **Whether range plus frozen gives a
sub-`0.30` `(EQ)` constant is not decided here.** Proposition 7.1 is the only bound I found, and
I have no frozen witness to test against. None exists at any `n` anyone has enumerated, the
frozen class being empty there.

**`(B-cov)`.** Not examined beyond KSBFT-C F5 (`Σ disp² ≤ D·Σ|disp|` pointwise, and frozenness does
not enter a pointwise bound).

**For L4 / Step 6.** The combination adds nothing. L4 is already proven on `Π_D` (Thm 3.1).
Restricting `(T)` to frozen `P` makes it a statement about an empty-or-not class. That renames the
problem (mg-3af9 §4.1, mg-f825 §2), and Prop 4.2 shows that on `Π_D` the renamed problem is the
conjecture.

---

## 8. Item 4 — the net, and one proposition to start on

**Under H, past `N₁ = ⌈L*/ε_dem⌉ + 1`, link by link:**

| link | status under H | source |
|---|---|---|
| L1b (row 8) | conclusion **automatic** | KSBFT-C §2.1, audited |
| L2 (row 9) | product **automatic**; the literal first disjunct is refuted at range `≤ 5` | §6 |
| row 3b | **off the route** | §6 |
| L3 (row 10) / F-bal | consumed content **automatic** | Prop 5.1 |
| L4 (row 11) | **PROVEN, via branch (ii) only** | Thm 3.1 |
| Step 6 on (ii) | **refuted** at range 3; the only repair **is the conjecture on `Π_{L*}`** | Thm 4.1, Prop 4.2 |

So the whole remaining content, under H, is:

> **(MC_D) — there is no minimal counterexample of range `≤ D`.** *If `π(P) ≤ D`, `P` is not a
> chain, and `δ(P − v) ≥ 1/3` for every `v` such that `P − v` is not a chain, then `δ(P) ≥ 1/3`.*

**Why this is the right object (PROVEN (cond.)).** Deleting an element cannot increase any `π(x)`,
so `Π_D` is closed under induced subposets. A minimal counterexample is therefore a counterexample,
so by H it lies in `Π_{L*}`. (MC_{L*}) then finishes the whole conjecture, at every `n`, not only at
`n ≥ 50L*`, conditional on the three preprints. **`L*` has no value, so in practice `D` must be a
free parameter**, and a proof whose constants depend on `D` is what is wanted. For `n ≥ 50L*` alone
there is **no smaller statement** coming from this architecture. Prop 4.2 shows the Step-6 repair on
`Π_D` is the conjecture on `Π_D` past `N(D,ε)`, and every other link is automatic. (MC_D) for
`D ≤ 6` is the literature (BW92, Pec08, not re-verified). KSBFT's Fibonacci remark says any proof
must use finiteness quantitatively, since `Z_∞` has `π = 2` and `δ = C_BFT` in the limit sense.

**The Step-6-shaped form Daniel could start on — CONJECTURED:**

> **(ONE-PT_D)** For every non-chain `P ∈ Π_D` with `n ≥ 3`, there exist an element `v` and a pair
> `{x, y} ∌ v`, balanced in `P − v`, that is also balanced in `P`.

- (ONE-PT_D) ⟹ (MC_D): trivially, since its conclusion is `δ(P) ≥ 1/3`. It is **strictly
  stronger** than needed, because it names *which* pair.
- Its "for every `v`" strengthening is **FALSE** at range 3 (§4.3, `W*`, `v = b₁`). So any proof
  must **choose** `v`. This is the one-point form of mg-63e3 §7's migration: the balanced pair of
  `P` need not come from an arbitrary subposet.
- The "exists `v`" form has **0 failures on all 5 224 non-chains with `n ≤ 6`** (EMPIRICAL). This is
  weak evidence. At `n ≤ 6` the conclusion's second half (`balanced in P`) is never in danger for
  the conjecture, so the probe tests only that *some* balanced pair of `P` survives *some*
  deletion.
- Under H, `v` can be taken far from `{x,y}` (Lemma 2.0 localises everything to windows of width
  `2D−1`). That is where KSBFT-C's transfer-matrix route (§3.2 there) would bear on it. **An
  approximate locality statement is not enough**: it gives `δ(P) ≥ 1/3 − η`, and a counterexample
  can sit at `δ = 1/3 − η/2`. Any proof via locality needs **exact** transport or a quantitative
  gap. (CONJECTURED, as a remark on method.)

---

## 9. What I did not do, and the negatives

**Not done:**

- The `.tex` source was **not read** (evicted from iCloud: `Resource deadlock avoided`). L4, (T),
  Step 6 and Fact 2.1 are taken from the mg-63e3 / mg-3af9 verbatim quotes.
- The row-5 normalisation of `leak` was **not re-read** at its source; see the caveat in §5.
- Brightwell–Wright (`π ≤ 5`), Peczarski (`π ≤ 6`) and Gup26 were **cited, not verified**.
- The L3 exception at `n ≤ 6` was **not identified**. Its range bound (`≤ 5`) is by size alone.
- L2's second disjunct under the literal "eigenvector sweep" reading: **not examined**.
- Standard dominance under H: **not examined**.
- `(B-cov)` under range plus frozen: **not examined**.
- The absent Step `(T)` of mg-7ae5: **not examined**.
- Whether Lemma 2.3's `c(D)` improves KSBFT Thm 1.3: **not checked**.
- Exhaustive checks stop at **`n = 6`**.
- **Nothing consumes** KSBFT Lemma 4.2, the constant `441` or eq. (1.5).

**Negatives, with the candidates tried (each is a way H might have closed the Step-6 hole):**

1. *Restrict (T) to a range window that excludes `W*`.* Refuted: `W*_t` covers every window
   `[r, D]` with `r ≥ 3` (Thm 4.1). Windows with `D ≤ 2` are covered by the literature, and
   counterexamples need `π ≥ 7`.
2. *Restrict to balanced cuts* (F-bal). This is available on `Π_D` (Prop 5.1), but mg-f825 F4's `W`
   is balanced, has range 3, and still breaks (iii). And (T) at a balanced cut is still refuted by
   `W` (`a = b`, one modified element), under (E1) (mg-3af9 §5.4). Under (E2) balanced cuts
   leave (ii) for a sub-linear `F`, which moves the burden to (iii); see §3.2.
3. *One-point transport for every deleted `v`.* Refuted, `W*`, `v = b₁` (§4.3).
4. *Approximate locality (correlation decay along the window).* It does not give exactness (§8,
   last bullet). The decay itself is unproven (KSBFT-C §3.2, CONJECTURED there).
5. *Frozenness added to (T).* It renames the problem (§7).
6. *A sharper interface bound than `2D − 1`.* Refuted as a universal: `τ/(2D−1) = 1` is attained
   at `n ≤ 6` (X1).
