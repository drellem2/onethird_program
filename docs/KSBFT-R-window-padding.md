# KSBFT-R — the window [8, L*]: do the thin witnesses of the δ-direct routes survive padding? Almost all do, into the minimal-counterexample class itself. The one that does not is W*, and it revives the Step-6 transfer in its existential form, which reduces to "balance is created only at the cut"

`mg-7bfc`, 2026-09-26. This follows mg-0b78 (`docs/KSBFT-P1-walled-routes-under-bounded-range.md`,
audit mg-af00 pending). P1 listed "padding finite witnesses into the window" as NOT DONE. This note
does it. **Nothing in `STATE.md` was edited, and no ticket was closed or re-opened. The verdicts are
recommendations to pm-onethird.**

**Errata (mg-ef5b, per audit mg-244e, `docs/AUDIT-mg-7bfc.md`).** Every exhibit was reproduced
exactly by independent code, so no exhibit changes. Corrected:
- **BROKEN: "mg-b447 Thm 4.1 refutes only the continuity form" (§4.2, Rec 2).** mg-b447's (T) is
  **existential** ("some balanced pair of `P[A]` or `P[B]` stays balanced", KSBFT-F §1). `W*`
  refutes that existential form, because `{x,y}` is the only incomparable pair of either side.
  The correct statement: Thm 4.1 refutes the existential (T) **on decomposable posets only**, and
  the refutation does not reach `𝒦_min`.
- **BROKEN at an edge case, harmless: Lemma 1.3(2) needs `U ⊊ W`.** At `U = W` the element `c_k` is
  comparable to everything, so it is isolated in `G`. Every use here has `U ≠ W`.
- **OVERSTATED: "padding kills every δ-direct route inside the minimal-counterexample shape".** The
  hosts satisfy (M1)+(M2) (and O1 at both ends), but not (M3): they have δ ≥ 0.45. So each
  "dead" verdict kills the route's lemma **as a class lemma on (M1)+(M2)**. A route that uses
  counterexample-only hypotheses (no balanced pair, `n`-minimality) is not touched. §4's preamble
  already said this; the headline, verdict 3 and Rec 1 now say it too. A24 stays undecided.
- **OVERSTATED: "exactly three exact paddings" and "inside `𝒦_min` the witness can only appear
  reweighted".** A prime, both-connected 5-poset `{z1<u, z2<v, z1<w, z2<w}` keeps the law of the
  2-antichain `{u,v}` exactly (`P[u<v] = 1/2`, by the automorphism `(z1 z2)(u v)`), although
  `{u,v}` is not a module. What is true, and all that is used: a **module** padding of a non-chain
  witness is never `𝒦_min`-shaped. For `2+2` no such prime host was found (EMPIRICAL, 4000
  random hosts, `n ≤ 8`).
- **(T_cont): the labels were swapped.** `Δ₁ → 0` is **PROVEN** (KSBFT-F Lemma 2.1). That `p_xy`
  stays away from 1/2 is **EMPIRICAL**: the audit's `(M,6,M)` family, `M = 16, 20, 24, 30`
  (range 9), has `p_xy = 0.1457` at every size while `Δ₁` falls 0.044 → 0.024. Primality was
  checked at `M ≤ 16` only.
- **(T∃)'s survival on insulated `W*` is an exact computation, not insulation.** Thm 2.3's
  guarantee needs depth `h(5, 0.05) ≈ 1.8·10⁹`; `M = 8, 16` are nowhere near it.
- **Cor 5.3 is vacuous for `n < h(D,μ)`** (`≳ 10¹⁶` at `D = 8`), so "a least counterexample is
  *exactly* a poset in which this happens at every cut" characterises nothing at feasible sizes.
- **Cor 5.4 is off by one and cites the wrong theorem.** Its proof needs `n ≥ 2h(D,μ)+2D+1`. It
  must use Thm 2.3's symmetric bound (`P → P−v`), not Thm 5.2 (`P[A] → P`). It presupposes a
  robust balanced pair in `P`, so it is vacuous on a counterexample.
- **(T∃^any) must read "ideal or filter".** In the ideal-only form it fails on any poset whose
  only balanced pair is two maximal elements; the V poset is the control, and it fires. mg-b447
  used "`P[A]` or `P[B]`". Prop 5.1 holds for the corrected form (CONDITIONAL on [H]+[D≤7]).
- **UPGRADE: `attach_low(F_N,R)` is PROVEN prime for every `R ≥ 4`, `N ≥ R+2`** (audit §2; `R = 3`
  is sharp, the module `{x_2, z}`). So the A5 exhibit is prime for every `R ∈ [8, L*]`.
- **[D≤7] HOLDS** (audit mg-9268, `docs/AUDIT-mg-e8b4.md`). "audit mg-9268 pending" is stale.

**Conditionality.** Two different hypotheses are used, and each result says which one it needs.

- **[H]** A counterexample has range `π(P) ≤ L*`. This is conditional on AK25a/AK25b/Haq26
  (KSBFT-C §1.1; audited).
- **[D≤7]** Every poset of range `≤ 7` satisfies 1/3–2/3. This is mg-e8b4's computer proof
  (`docs/KSBFT-I-finite-state.md`; audit mg-9268 **HOLDS**, `docs/AUDIT-mg-e8b4.md`). Still
  marked conditional here.

The window is `𝒲 := {P : 8 ≤ π(P) ≤ L*}`. "A counterexample lies in 𝒲" needs **both** [H] and
[D≤7], and every sentence below that says "in the window" inherits that. **The padding
constructions and the transfer theorems are unconditional**: they are statements about explicit
posets, or about `Π_D` with `D` free. Only their *relevance* is conditional.

Marks:

- **PROVEN**: the proof is here.
- **PROVEN (exact computation)**: a finite exact computation on a named poset. That is a proof
  about that poset, and it is only as good as the code. Instrument:
  `code/ksbft_r_window_padding_7bfc/` (`sh run_all.sh`, about 1 s, exact integers).
- **PROVEN (cited)**: proven in the cited document, and I re-read the step I use.
- **EMPIRICAL**: comes with its instrument and range.
- **CONJECTURED**: a guess.

**Computation is used only as an instrument** (ticket rule). Every poset computed is a named witness
or an explicit padding of one. No census and no search were run or extended.

---

## 0. Verdict

> **1. The class a δ-direct lemma must hold on (§3, PROVEN).** A counterexample of least size
> (least `n`) has four properties:
> - its incomparability graph `G(P)` is connected (ordinal-indecomposable);
> - its comparability graph is connected (it is not a disjoint union);
> - **every proper module (autonomous set) is a chain**;
> - `π(P) ≥ 8` [D≤7] and `π(P) ≤ L*` [H].
>
> Call this shape `𝒦_min`. The first three follow from one exact lemma: a module's internal law is
> exactly its own (Lemma 1.1). They also use n-minimality and Linial's width-2 theorem.
>
> **2. The padding dichotomy (§1, PROVEN).** There are three *module* paddings, which leave
> every internal law of the witness `W` unchanged: `W ⊕ Q`, `W + Q` and substitution `Q[q ← W]`.
> In all three `W` is a proper non-chain module, so **module padding never produces `𝒦_min`**.
> *(Erratum: these are not the only exact paddings. A prime 5-poset keeps a 2-antichain's law
> exactly without it being a module; see the errata above.)* Inside `𝒦_min` the witness generically
> appears **reweighted**, with law ∝ `ext_P(τ)`. So the real question is whether the violation
> survives that reweighting. Two tools answer it:
> - **Insulation (Thm 2.1, Thm 2.3):** in bounded range, the influence of a far modification on a
>   pair's law decays geometrically. For `F_N` this is proved in closed form, at rate `φ⁻²`.
> - **Hub padding (Lemma 1.3):** attach a long chain through one hub element. The reweighting's
>   relative spread is `≤ m/(m+k)`.
>
> **3. Per-route verdicts (§4, the table).** Every walled δ-direct route whose killer is thin or
> finite was examined. *"Survives into `𝒦_min`" below means into the (M1)+(M2) shape: the hosts
> have δ ≥ 0.45, so they violate (M3), and each "dead" is dead as a **class lemma on (M1)+(M2)**
> (erratum, audit mg-244e).*
> - **Structural (every `P`), confirmed dead and excluded:** A13 (probe A), A15 (probe C), B1–B5
>   (F-series, Čech-bias), C1-blindness, C5/f5be (α ≤ 1), 5987's Step 2, 8748/8b32/7c32/7c78/9461.
> - **Thin witness survives INTO `𝒦_min ∩ 𝒲` (PROVEN):**
>   - **A5 (Kahn–Saks/KL):** the Fibonacci centre pair stays within `4φ^{−2a}/((1−φ^{−2a})²R)`
>     of `F_N`'s value, inside a comparability- and incomparability-connected poset of range
>     **exactly `R`** for every `R ≥ 3` (Thm 2.1, closed form). It is prime for every `R ≥ 4`,
>     `N ≥ R+2` (PROVEN by audit mg-244e §2; first recorded here as EMPIRICAL for `N ≤ 30`). So
>     realised centre pairs tend to `C_BFT` inside `𝒲`.
>   - **A14 (probe B, diagonal capacity):** `attach_both(F_20, 8)` is prime, has range 8 and
>     δ = 0.456, and **no pair certifies**: the maximum is 13627/46282 ≈ 0.294 < 1/3 (exact).
>   - **A16 (probe D, co-degree):** a double-hub padding of `2+2` has only chain modules, is
>     connected both ways, and has range 18. The pair keeps its separating number 2 and has balance
>     5336/27441 ≈ 0.194 < 1/3 (exact). *Caveat:* the source never defines "co-degree"; I read it as
>     "the number of elements comparable to exactly one of the two".
>   - **Continuity form of Step 6 (T) (A20/A21):** on an indecomposable, prime, insulated `W*`,
>     `p_xy` falls from 1/2 to 0.146 while `Δ₁ = 0.044` (exact). A single point cannot refute a
>     modulus statement. The `(M,6,M)` family to `M = 30` keeps `p_xy = 0.1457` while `Δ₁ → 0`
>     (0.024 at `M = 30`). So (T_cont) fails on (M1)+(M2)-shape posets, EMPIRICAL (erratum).
> - **Not decided:** A24 (Hodge Thm G). There is no transfer lemma for link spectra, and the data
>   stop at `n ≤ 8`. It targets `λ₂(Δ_AT)`, not δ.
> - **Finite killers (A8, A9, A25, A27, A28):** all on moot/auto routes. The (L*) refuters at
>   `n = 9` and `n = 11` **already lie in 𝒲** (ranges 8, 8, 9; `G`-connected). A8's violation
>   survives exactly into `𝒲` under `+`. See §4.3.
>
> **4. The one killer that does NOT survive (§4.2, §5): `W*` and `W*_t` are ordinal-decomposable**
> (PROVEN: `W*_t = C_{a−2} ⊕ (C_1 + C_{t+1}) ⊕ C_{b−t}`). So they refute nothing on `𝒦_min`. The
> natural indecomposable padding, which replaces both chains by Fibonacci runs, **satisfies** the
> existential Step-6 transfer:
> > **(T∃)** some balanced pair of `P[A]` is balanced in `P`.
>
> It does so at every size computed, with `Δ₁` down to 0.044: a base pair far from the cut
> survives (exact computation; the sizes are far below Thm 2.3's depth, so this is not insulation
> at work). **Best candidate (CONJECTURED): (T∃) on `𝒦_min`, with "ideal or filter".** By minimality it implies the conjecture at
> *any* proper ideal `A` with `P[A]` a non-chain, so the `Δ₁`-hypothesis is not even needed (§5.1).
>
> **5. Deep dive (§5).**
> - **Insulation transfer (Thm 5.2, PROVEN, `Π_D` with `D` free).** Let `(a,b)` be balanced with
>   margin `μ` in `P[A]` and lie at depth `≥ h(D,μ) = 2D+1 + 2D⌈ln μ / ln θ_D⌉` below the cut, where
>   `θ_D = 1−(D+1)^{−2D}`. Then `(a,b)` is balanced in `P`.
> - **Corollary 5.3 (PROVEN, relevant under [H]+[D≤7]).** In a least counterexample, for **every**
>   proper non-chain ideal `A`, every `μ`-robust balanced pair of `P[A]` lies within `h(D,μ)` of
>   the cut; dually for filters. **Balance in every truncation is created at the truncation.** `W*`
>   is the decomposable toy model of exactly this. *(Vacuous for `n < h(D,μ)`, which is `≳ 10¹⁶`
>   at `D = 8`.)*
> - **Corollary 5.4 (PROVEN, repaired).** "Some extreme `v` works" (KSBFT-J's ONE-PT at an extreme
>   element) holds for every `P ∈ Π_D` with `n ≥ 2h(D,μ)+2D+1` that has a `μ`-robust balanced
>   pair. It presupposes that pair, so it is vacuous on a counterexample.
> - **The precise obstruction (§5.4):**
>   1. **Margin.** Nothing bounds `μ` below. `p − 1/3` is a *signed* quantity, which is P1 §5.5's
>      wall again, and closed-interval ties at 1/3 do occur.
>   2. **Constant.** `h(D,μ)` is `(D+1)^{2D}`-large, so at `D ≥ 8` it is useless for any finite
>      check (KSBFT-N).
>   3. **Mechanism.** The one missing mechanism is a lemma that *some* truncation of a least
>      counterexample carries a robust balanced pair away from its cut. No such lemma is on the
>      record. KSBFT-Q (balance forced off the ends into the middle, `P_9`) is the only evidence on
>      where truncation balance sits, and it is compatible with the obstruction.
>
> **Net.** Padding kills, as a class lemma on (M1)+(M2), every δ-direct route examined except the
> existential Step-6 transfer (A24 undecided). The hosts are connected both ways, have only chain
> modules and lie in the window, but they are not counterexample-shaped (M3), so a route using
> counterexample-only hypotheses is untouched. The survivor is
> reduced to a two-ended statement about truncation boundaries, modulo margin. No proof is given,
> and the obstruction is stated.

---

## 1. Padding: exact, insulated and hub

Notation: `ext_P(τ) = #{σ ∈ L(P) : σ|_W = τ}` for `τ ∈ L(W)`, with `W ⊆ P` induced. The **law of
`W` in `P`** is `μ_{P,W}(τ) ∝ ext_P(τ)`. Every event about the relative order of `W`'s elements
has `P`-probability `μ_{P,W}(E)`.

**Lemma 1.1 (module transfer) — PROVEN.** If `M ⊆ P` is a module (every `z ∉ M` is above all of
`M`, below all of `M`, or incomparable to all of `M`), then `μ_{P,M}` is uniform on `L(M)`.

*Proof.* Fix `σ ∈ L(P)` and let `S` be the set of positions `M` occupies. Refill `S` in the order of
any `τ ∈ L(M)`. The result is still a linear extension. Constraints inside `M` hold by `τ`. A
constraint `z < m` with `z ∉ M` holds because `z < m'` for every `m' ∈ M`, so `z` precedes all of
`S`; dually for `z > m`. Incomparable `z` carry no constraint. So `L(P)` is in bijection with
`{σ restricted off M, with the set S} × L(M)`, and the restriction map has fibres of equal size. □

**Corollary 1.2 (the three module paddings) — PROVEN.** *(Erratum: they are exact, but they are
not the only exact paddings; audit mg-244e §3.)* In `W ⊕ Q`, `Q ⊕ W`, `W + Q` (disjoint union)
and `Q[q ← W]` (lexicographic substitution), `W` is a module. So every relative-order event of `W`
keeps **exactly** its `W`-probability. The ranges are:

- `π_{W⊕Q}(w) = π_W(w)`, so `π(W ⊕ Q) = max(π(W), π(Q))`;
- `π_{W+Q}(w) = π_W(w) + |Q|` and `π_{W+Q}(q) = π_Q(q) + |W|`;
- `π_{Q[q←W]}(w) = π_W(w) + π_Q(q)`.

`W + Q` has connected `G`, and `Q[q ← W]` has connected `G` and comparability graph when `Q` is
prime. **In each case `W` is a proper module, and it is a non-chain whenever the witness has an
incomparable pair.** Positions shift: exactly (by `|Q|`) under `⊕`, and by a random amount under
`+`. So slot laws are exact under `⊕` only.

*(EMPIRICAL control, `out_pad.txt` §1: `F_7`, `P_9`, `2+2` padded by `+C_8`, `⊕A_9`, `F_9[x_4←W]`
keep every pair law exactly. The non-module embedding `attach_low(F_7,3)` changes 6 of 6 pair
laws: that is the NEGATIVE CONTROL, and it is CAUGHT.)*

**Lemma 1.3 (hub padding) — PROVEN.** Let `|W| = m`, `U ⊊ W` a non-empty proper down-set
(erratum: at `U = W`, `c_k` is isolated in `G` and (2) fails), and let
`H_k(W,U)` be `W + (c_1 < … < c_k)` with `c_k > u` for every `u ∈ U`. Then:

1. For `τ ∈ L(W)`, `ext(τ) = C(m+k, k) − C(p_τ − 1 + k, k)`, where `p_τ` is the position in `τ` of
   the last element of `U`. Hence `μ_{H,W}(E) ∈ [P_W(E)·k/(m+k), P_W(E)·(m+k)/k]`.
2. `G(H_k)` is connected, since `c_1` is incomparable to all of `W` and `c_k` is incomparable to
   `W ∖ U ≠ ∅`. The comparability graph is
   connected, since `c_k` touches `U` and the chain.
3. `π(c_j) = m` for `j < k`, `π(c_k) = m − |U|`, and `π(w) = π_W(w) + k − [w ∈ U]`.
4. `{c_1, …, c_{k−1}}` is a module and is a chain. That is allowed in `𝒦_min` (§3).

*Proof.* (1) Shuffle the chain into `τ`. The only constraint is that `c_k` comes after every
element of `U`, i.e. after position `p_τ` of `τ`. The shuffles that violate it put the whole chain
before that element: `C(p_τ − 1 + k, k)` of them out of `C(m+k,k)`. Since `|U| ≤ p_τ ≤ m`,
`ext(τ) ∈ [C(m+k,k) − C(m−1+k,k), C(m+k,k)]`, and `C(m−1+k,k)/C(m+k,k) = m/(m+k)`. So
`max ext / min ext ≤ (m+k)/k`, which gives the stated bound on `μ_{H,W}(E)`. Parts (2)–(4) are read
off the construction. □

Hub padding makes `W`'s elements **wide** (`+k`). That is harmless for lemmas that do not mention the
pair's range. Other modules of `W` may survive, and are removed case by case (§4.1, A16).

## 2. Insulation: bounded range localises a pair's law

### 2.1 The Fibonacci witness, exactly

`F_N` (x_i < x_j iff j−i ≥ 2) is the "fence", "Z_n" (mg-5987) and "Fibonacci poset" of the
record. It is the witness of A5, A24 (fence), E3/5987 and KSBFT-A §5.

**Lemma 2.0 — PROVEN.** `L(F_N)` is in bijection with the tilings of `[1,N]` by monominoes and
dominoes, a domino `{i,i+1}` meaning `x_{i+1}` precedes `x_i`. Hence `e(F_N) = F_{N+1}`, and
`P[x_{i+1} before x_i] = F_i F_{N−i} / F_{N+1}`.

*Proof.* `x_j < x_i` for all `j ≤ i−2`, and `x_i < x_j` for all `j ≥ i+2`. So `pos(x_i) ∈
{i−1, i, i+1}`, and a permutation with every displacement `≤ 1` is a product of disjoint adjacent
transpositions. Conversely, every such product respects `j − i ≥ 2 ⟹ pos(x_i) ≤ i+1 ≤ j−1 ≤
pos(x_j)`, with equality impossible. A domino at `{i,i+1}` leaves tilings of `[1,i−1]` and
`[i+2,N]`: `F_i · F_{N−i}`. □

As `i, N−i → ∞`, Binet gives `F_iF_{N−i}/F_{N+1} → (φ^i/√5)(φ^{N−i}/√5)/(φ^{N+1}/√5) = 1/(√5 φ) = (5−√5)/10 = C_BFT`. That is
KSBFT-A's "centre adjacent pair → C_BFT", now with a closed form.

> **Theorem 2.1 (Fibonacci insulation) — PROVEN.** Let `3 ≤ R ≤ N−2`, and let
> `P = F_N ∪ {z}` with `z ∥ x_1..x_R` and `z < x_{R+1}, …, x_N` (`attach_low(F_N, R)`). Then:
> 1. `π(P) = max(R, 3)`. **Both** `G(P)` and the comparability graph are connected.
> 2. For a centre pair `B = {x_i, x_{i+1}}` with `a := i − R − 1 ≥ 1`, write `A` for the domino
>    `{R, R+1}`. Then
>    `P_P(B) = P(B) + (P(A)P(B) − P(A∩B)) / (R + 1 − P(A))`,
>    where `P(·)` is the tiling measure of `F_N`, `P(A) = F_R F_{N−R}/F_{N+1}` and
>    `P(A∩B) = F_R F_{a} F_{N−i}/F_{N+1}`.
> 3. `|P_P(B) − P(B)| ≤ 4u^a / ((1−u^a)² R)` with `u = φ^{−2} ≈ 0.382`.
>
> So for every `R ∈ [8, L*]` and every `ε > 0`, `𝒲` contains a poset of range **exactly `R`**,
> connected both ways, with a pair whose balance is within `ε` of `C_BFT`.

*Proof.* (1) `π(z) = R`. `π(x_j) ≤ 2 + [j ≤ R] ≤ 3`. `G(F_N)` is the path `x_1 − x_2 − … − x_N`,
plus the edge `z − x_1`. And `z < x_N`.

(2) `z`'s constraints are: before every `x_j` with `j ≥ R+1`, free with respect to `x_1..x_R`. In the
extension given by a tiling `T`, the first element of index `≥ R+1` sits at position `R+1`, unless
`T` has the domino `{R,R+1}`, in which case it sits at `R`. So `z` has
`w(T) = R + 1 − 1_A(T)` slots, and
`P_P(B) = E[w 1_B]/E[w] = ((R+1)P(B) − P(A∩B)) / (R+1 − P(A))`, which rearranges to (2). The
dominoes `A` and `B` are disjoint and non-adjacent (`a ≥ 1`), so
`P(A∩B) = F_R · F_{a} · F_{N−i} / F_{N+1}` by Lemma 2.0.

(3) `P(A∩B)/(P(A)P(B)) = F_a F_{N+1} / (F_{N−R} F_i)`. By Binet, `F_k = φ^k(1−q^k)/√5` with
`q = −φ^{−2}`. The powers of `φ` cancel (`a + N + 1 = (N−R) + i`), leaving
`(1−q^a)(1−q^{N+1}) / ((1−q^{N−R})(1−q^i))`. Every exponent is `≥ a`, so with `u = |q|`:
`|ratio − 1| ≤ (1+u^a)²/(1−u^a)² − 1 = 4u^a/(1−u^a)²`. Finally
`|P_P(B) − P(B)| = P(A)P(B)|ratio−1| / (R+1−P(A)) ≤ |ratio − 1|/R`. □

*Exact check (`out_pad.txt` §2):* the closed form (2) matches the DP **exactly** at every tested
`(N,R) ∈ {(14,5), (20,8), (30,8), (41,8), (41,12), (61,8), (81,8), (81,20)}`. The bound (3) holds with
room. At `(81, 8)`, the padded centre pair is `C_BFT + O(10⁻¹⁵)` in a range-8 poset.
**Primality (EMPIRICAL here; PROVEN by audit mg-244e §2):** `attach_low(F_N,R)` is prime for
`N ∈ {8,12,20,30}` and `5 ≤ R < min(N−2,12)`. The CONTROL `attach_low(F_12,3)` has the module
`{x_2, z}`, and the test CAUGHT it. The audit proves primality for every `R ≥ 4`, `N ≥ R+2` (a
module containing `z` meets `F_N` in one `x_j`, which cannot be incomparable to all of
`x_1..x_R` for `R ≥ 4`), with `R = 3` sharp. The theorem needs only the two connectivities.

### 2.2 The general insulation lemma (bounded range, any witness)

**Lemma 2.2 (cited, re-derived).** These are KSBFT-I Proposition 1, Lemma 3 and Lemma 6
(`docs/KSBFT-I-finite-state.md` §2–§3.5; audit mg-9268 HOLDS, Lemma 6 re-derived in
`docs/AUDIT-mg-e8b4.md` row 10). Let `π(P) ≤ D` and let `e` be a
linear extension.

- **(i)** Every ideal `J` of size `k` satisfies `{e ≤ k−D} ⊆ J ⊆ {e ≤ k+D}`.
  *Re-derived:* `e(x) > k+D` gives `d(x) ≥ e(x) − 1 − π(x) ≥ k`, so `x ∉ J`; dually.
- **(ii)** `P_P[a<b] = Σ_{J∈V_k} w_J ρ_J` with `w_J = e(J)e(P∖J)/e(P)`, and `ρ_J` depends on `J`
  only.
- **(iii)** If `a, b` lie in every `J ∈ V_{k₀}`, the hull width satisfies
  `W_{k₀+2Dj} ≤ θ_D^j`, where `θ_D = 1 − (D+1)^{−2D}`.

> **Theorem 2.3 (bottom insulation) — PROVEN (from Lemma 2.2).** Let `π(P) ≤ D`, let `A` be an ideal
> of `P` with `|A| = K`, and let `a, b ∈ A` with `max(e(a), e(b)) ≤ K − 2D − 1 − 2Dj` for some linear
> extension `e` of `P` that lists `A` first. Then `|P_P[a<b] − P_{P[A]}[a<b]| ≤ θ_D^j`.

*Proof.* Put `k₀ = max(e(a),e(b)) + D`, so `a, b ∈ J` for every `J ∈ V_{k₀}` by (i). Put
`k = k₀ + 2Dj ≤ K − D − 1`. By (i) applied to `e`, every size-`k` ideal of `P` lies in
`{e ≤ k+D} ⊆ A`. So `V_k(P) = V_k(P[A])`: ideals of `P[A]` are ideals of `P`, because `A` is an
ideal. By (ii), both probabilities are convex combinations of the **same** numbers `ρ_J`,
`J ∈ V_k`, so they differ by at most the hull width, which is `≤ θ_D^j` by (iii). □

The same holds dually for filters. The rate `θ_D` is useless numerically (KSBFT-I §3.5). What matters
here is that it is **independent of `n` and of everything above the cut**. Measured rates are much
better: `φ⁻²` per cut on `F_N`.

## 3. What a minimal counterexample in the window must satisfy

> **Proposition 3.1 — PROVEN (Lemma 1.1 + n-minimality + Linial 1984).** Let `P` be a
> counterexample (no balanced pair, not a chain) of least `n`. Then **every module `M` with
> `2 ≤ |M| < n` is a chain.** Hence `P` is neither an ordinal sum nor a disjoint union: both `G(P)`
> and the comparability graph are connected.

*Proof.* If `M` is a non-chain proper module, it is smaller than `P`, so it is not a counterexample.
So it has a balanced pair, and by Lemma 1.1 that pair has the same probability in `P`,
contradicting that `P` is a counterexample. If `P = A ⊕ B`, then `A` and `B` are modules, hence
chains, hence `P` is a chain. If `P = A + B`, then `A` and `B` are chains, so `P` has width 2, and
Linial's theorem gives a balanced pair. □

**The forced structure `𝒦_min`**, as it applies to a counterexample of least size:

| property | source | status |
|---|---|---|
| (M1) `G(P)` connected, comparability graph connected, every proper module a chain | Prop 3.1 | PROVEN |
| (M2) `8 ≤ π(P) ≤ L*` | [D≤7] + [H] | conditional |
| (M3) no balanced pair; every `P − v` (non-chain) has one | definition, n-minimality | PROVEN |
| (M4) a low 3-antichain at **both** ends (O1: ≥ 3 minimal; O2: a Y-gadget below the Linial crossing, `3k < π(x)+1`) | KSBFT-Q Thm 3.1 (audited, mg-3345) | PROVEN (cited) |
| (M5) `δ ≥ C_BFT + min(θ₀, C_BFT/((5+3√5)(D+1)+1))`; `d₁ ≥ 1/(D+1)` | Lemma W, KSBFT-A §3.1 | PROVEN (cited) |
| (M6) balance in every truncation is created at the cut (Cor 5.3) | §5 | PROVEN (vacuous for `n < h(D,μ)`) |
| (M7) *a wide element (π ≥ 8) within a bounded distance of each end* | would follow from a localised KSBFT-I Thm 5 | **CONJECTURED** (below) |

*(M7), stated precisely as a conjecture.* KSBFT-I certifies every range-≤7 indecomposable poset within
its first `N_7 = 21` canonical elements. The tree's generation constraints are local, since they
read only the ranges of prefix elements. But the complete cut `k = max(N−D, d(e_N))` uses
Prop 2.2(i) with `D = 7` for **all** elements, including those beyond the prefix. The `d(e_N)` part
is range-free, and the `N−D` part is not. A localisation would need the elements beyond position
`N` that could enter a size-`(N−7)` ideal to have range `≤ 7`. I did not check whether the tree's
certificates close at `k ≤ d(e_N)`. **Not examined further.** If (M7) holds, a counterexample must
be wide at both ends, which is where Local Linial (KSBFT-Q) also points.

**Consequence for padding (PROVEN, Cor 1.2 + Prop 3.1).** A module padding of a non-chain witness is
never of shape `𝒦_min`. (Erratum: "exact" was written here; a non-module exact embedding into a
prime host exists, audit mg-244e §3.) A witness refutes a lemma **on the class that matters** only if its
violation survives the reweighting `μ_{P,W}` of some `𝒦_min`-shaped host. §2 and Lemma 1.3 are
the tools for that.

## 4. Per-route analysis

"Survives into `𝒦_min`" means that the lemma's failure is exhibited on a poset that is connected
both ways, has only chain modules, and has range `≥ 8`. That is everything in (M1)–(M2) except
being a counterexample. The hosts are **not** counterexamples: all have δ ≥ 0.45. For a **sound**
certificate (a proven lower bound `δ ≥ B(data)`) that is exactly the right test. On a counterexample
`B < 1/3` automatically, so the route needs *completeness* (`max B ≥ 1/3`) on every
`𝒦_min`-shaped non-chain, and a complete-but-for-one host kills it. **So every "dead" below is dead
as a class lemma on (M1)+(M2)** (and O1 at both ends for A14, A16). A route that also uses (M3)
(no balanced pair, `n`-minimality) is not refuted by these hosts.

### 4.1 δ-direct routes killed by thin witnesses

| row | route and key lemma (source) | witness, and how it violates | padding decision | verdict |
|---|---|---|---|---|
| **A5** | Kahn–Saks / KL relaxation (mg-a1ec, sib `EntropyDiscontinuity-Mechanism.md:155-170`). **Lemma:** δ ≥ inf δ over `𝓡` (log-concave slot data + pairwise consistency, not realised). The inf is `C_BFT`, at the geometric ray `r = 1/φ`. The route needs the inf over *realised* data ≥ 1/3 | `F_N` centre pair, `F_iF_{N−i}/F_{N+1} → C_BFT` (Lemma 2.0), range 2 | **Survives into `𝒦_min ∩ 𝒲` (PROVEN, Thm 2.1):** range exactly `R` for any `R ∈ [8,L*]`, both connectivities, prime for every `R ≥ 4` (PROVEN, audit mg-244e §2). The window constraint is **global** (some element is wide), and the relaxation is **pair-local**, so it cannot see it | **dead** |
| **A13** | probe A (mg-61bb, attempt-index:30): coherence adds nothing; subadditivity is upper bounds only | none (logical; the "β ≡ 10⁻¹⁰⁰" in P1 is not in the source) | structural: an upper-bound system forces no lower bound on any class | **structural — excluded** |
| **A14** | probe B (mg-92e6, attempt-index:31). **Lemma (sound):** `δ ≥ ½(T[x,k]+T[x,k+1]+T[y,k]+T[y,k+1]−1)⁺`. The route needs some pair and slot to reach 1/3 | the source says only "dies as the pair spreads". **P1's "spread 4 / range 3" is not in the source** | **Survives into `𝒦_min ∩ 𝒲` (PROVEN, exact):** `attach_both(F_20,8)` (bottom `z ∥ x_1..x_8`, top dual `z'`) is prime, range 8, δ = 0.4561, max certificate 13627/46282 = 0.2944 < 1/3. One-sided padding is *certified* at its free end (0.382). So the certificate lives at ends, and capping both ends removes it | **dead** |
| **A15** | probe C (mg-f82f, attempt-index:32). **Lemma (sound):** `δ ≥ (1−1/e(P))/s`, `s` = free slots of the coherent order. It proves the conjecture for `s ≤ 2` | "extremal posets have s ≥ 4" (no poset named; P1's `n=6` witness is not in the source) | structural: every counterexample has `s ≥ 3` (by the probe's own theorem), where the bound is `< 1/s ≤ 1/3`. No poset can revive it | **structural — excluded** |
| **A16** | probe D (mg-e2de, attempt-index:33). **Lemma:** co-degree ≤ 1 ⟹ δ ≥ 1/3, and "frozen ⟹ every edge has co-degree ≥ 2". The route needs a local bound ≥ 1/3 at co-degree 2 | `C_2 + C_2`: pair `(a₁, b₂)`, `P[b₂ before a₁] = 1/6` at co-degree 2 (read as the separating number, see caveat) | **Survives into `𝒦_min ∩ 𝒲` (PROVEN, exact, under that reading):** the double hub `H_8(H_8(2+2,{a₁,a₂,b₂}),{a₂})` is connected both ways, has only chain modules, range 18, separating number still 2, and balance 5336/27441 = 0.194 < 1/3. For `k = 16, 30`: 0.183, 0.176 (→ 1/6, EMPIRICAL). The single hub leaves the non-chain module `{a₂,b₂,c_1..c_{k−1}}`, which the CONTROL catches. G-blindness (δ 4/9 vs 1/2 on isomorphic `G`) survives into `𝒲` under `⊕ attach_low(F_20,8)` (δ 0.456 vs 1/2), but blindness is not a killer at 1/3 (both values are ≥ 1/3) | **dead** (caveat: "co-degree" is undefined in the source) |
| **A24** | Hodge side, Thm G (mg-a3d4, `Hodge-Side-Leverage.md:328-428`). **Lemma:** Alev–Lau, `λ₂(Δ_AT) ≥ 2∏(1−γ_i)`. The route needs `γ_i` small | `γ_i ≥ 1/2` on `A_n` (proven), `γ = 1/2` on `C_a + C_a` (`n ≤ 8`), fence `γ₋₁ ≈ 0.46` (`n ≤ 7`) | **NOT DECIDED.** `γ_i` is a max of link spectra over a level of `F(P)`. I have no transfer lemma for links under `⊕`, `+` or hubs, and I did not compute links at `n ≥ 16`. Note that the target is `λ₂(Δ_AT)`, not δ | not decided (δ-adjacent) |
| **B1–B5** | F-series (Route A chamber-Morse; hybrid; sheaf; Čech-bias F29–F31) | none: `K_chain-loc ⊆ ker Φ_*` for every `P` (F31 Lemma 3.2.1), etc. | structural, true at every `P` | **structural — excluded** |
| **C1** | compression2 realizability-blindness (mg-0fc6) | `μ₁` vs `μ₂`, same pair marginals (the `n=6`, `e=9` poset; "V⊕V" is P1's inference) | structural: every downstream quantity is a function of the pair marginals | **structural — excluded** |
| **C5, f5be** | W4 rate / α (mg-409a, 8d66, f5be): the route needs `α ≥ 2`–3 | `α(P) ≤ 1` for **every** `P` | structural | **structural — excluded** |
| **E3/5987** | lever test: "frozen ⟹ Q ≤ C" | Step 2 is the conjecture restricted to `{Q > C}` (structural). The caps come from `F_N` | structural. The `F_N` caps survive into `𝒦_min` by Thm 2.1 anyway | **structural — excluded** |
| **E3/9b6b** | density lever `δ ≥ f(d)` | `V^{⊕k} ⊕` chain: **decomposable**, and the source itself says the refutation lapses for primitive posets | lapses on `𝒦_min`, but **[H] makes the lever finite**: `d ≤ L*/(n−1)`, so `{d ≥ d₀} ∩ 𝒲` has `n ≤ L*/d₀ + 1`. The "flat" reading is the conjecture on a finite (astronomical) range of `n` | **transformed, not a route** |
| **E4** | 8748, 8b32, 7c32, 7c78, 9461 | blindness, "does not exist", an identity, bipartiteness, architecture | structural | **structural — excluded** |
| **A19–A21, E1** | Step 6 (T) (mg-63e3 → 3af9 → b447) | `W` (range 3), `W*` (range 3), `W*_t` (range `t+1`) | **the witnesses are ordinal-decomposable (§4.2)** | **→ §4.2, §5** |

### 4.2 Step 6: the continuity form dies, the existential form survives

`W*_t(a,b) = C_{a−2} ⊕ S_t ⊕ C_{b−t}`, where `S_t = {x} + {y < b_1 < … < b_t}` is the star
(PROVEN: `c_{a−2}` is below everything else and `b_{t+1}` is above everything else. Checked for
`(t,a,b) = (2,4,4), (3,4,8), (7,9,9), (8,9,10)`: `G`-disconnected, with `p_xy = 1/(t+2)`). So
`W*_t ∉ 𝒦_min`, and mg-b447's Thm 4.1 ("(T) refuted in every range window") is a statement about
decomposable posets. KSBFT-J already noted that `W*` is decomposable. **Erratum (audit mg-244e
§4):** mg-b447's (T) is the *existential* form, and `W*` refutes it, because `{x,y}` is the only
incomparable pair of either side. Thm 4.1 refutes the existential (T) **on decomposable posets
only**; it does not reach `𝒦_min`. The section title's "continuity form dies" is this note's own
separate finding, below.

Two forms of (T) must be separated:

- **(T_cont)** (mg-3af9's modulus form): `Δ₁ ≤ ε ⟹ |p^P − p^{P[A]}| ≤ F(ε)` for pairs of `P[A]`.
- **(T∃)**: `Δ₁ ≤ ε` and `P[A]` a non-chain ⟹ **some** balanced pair of `P[A]` (or, dually, of
  `P[B]`, as mg-b447 states it) is balanced in `P`.

**Insulated `W*` (PROVEN, exact, `out_pad.txt` §3).** Replace the bottom chain by `F_M`, with `x, y`
above `f_1..f_{M−1}` and `∥ f_M`. Replace the top chain by `F_s`, with `x < b_j` iff `j ≥ t+2`. The
cut is `A = F_M ∪ {x,y}`. Every instance is prime and connected both ways:

| (M, t, s) | range | Δ₁ | `p_xy` in `P[A]` → `P` | balanced pairs of `P[A]` | still balanced in `P` |
|---|---|---|---|---|---|
| (8, 2, 8) | 5 | 0.0618 | 1/2 → 0.253 | 4 | `(f_0,f_1)` 0.618, `(f_7, y)` 0.602 |
| (12, 3, 12) | 6 | 0.0479 | 1/2 → 0.213 | 4 | `(f_0,f_1)`, `(f_11, y)` |
| (16, 6, 16) | **9** | 0.0443 | 1/2 → 0.146 | 4 | `(f_0,f_1)` 0.618, `(f_15, y)` 0.609 |

- **(T_cont) fails on (M1)+(M2)-shaped window posets (EMPIRICAL).** At range 9 the interface pair
  moves by 0.354 while `Δ₁ = 0.044`. `Δ₁ → 0` as `M, s → ∞` at fixed `t` is **PROVEN**, by Lemma
  2.1 of KSBFT-F, since `E K ≤ D`. That `p_xy` stays away from 1/2 is **EMPIRICAL** (erratum: the
  labels were swapped). Audit mg-244e computed `(M,6,M)` for `M = 16, 20, 24, 30`: `p_xy = 0.1457`
  at every size (to 4 dp) while `Δ₁` falls 0.044 → 0.024. Primality was checked at `M ≤ 16` only.
- **(T∃) holds on every instance (exact computation).** The bottom pair `(f_0,f_1)` of the base is
  far from the cut and survives. (Erratum: this is **not** Thm 2.3 at work. Its guarantee needs
  depth `h(5, 0.05) ≈ 1.8·10⁹`, and `M = 8, 16` are nowhere near it. The table's `f_0` is
  0-indexed; the text is 1-indexed.) What made `W*` a counterexample to (T∃) was that its base was a **chain**,
  which has no pair to transfer. In an indecomposable host the base must carry incomparabilities,
  and pairs far from the cut are insulated.

So (T∃) is the one δ-direct lemma whose killer does not pad into `𝒦_min`. That makes it **the best
candidate** (a judgement, CONJECTURED). §5 takes it up.

### 4.3 The finite killers

| row | killer | padding | verdict |
|---|---|---|---|
| A8 | log-concavity of `e(P_m)` fails (`[1,2,6]` at `n = 5`; posets not recorded) | **exact under `+`:** `e(P_m + C_8) = C(|P_m|+8, 8)·e(P_m)`, a constant factor, and `P_m` has the same size for every `m`. So any violation survives into `𝒲 ∩ {G connected}` (PROVEN, Cor 1.2). Not tried in `𝒦_min` | moot (B-wall / L1b line, not δ-direct) |
| A9 | "primitive ⟹ good mixer" | **worse in `𝒲`:** `1 − λ_std ≤ 4nD/(n²−1)` on `Π_D` (KSBFT-F Prop 5.1) | dead, structurally in window |
| A25 | LP value `(n−1)/3` false at `n = 6` | an abstract LP (transitivity not imposed); its target `ε_spec` is auto on `Π_D` (P1) | moot; not padded |
| A27 | L2 first disjunct false (2/126 at `n = 6`) | global eigenvector; L2 drops out (KSBFT-F §6) | moot; not padded |
| A28 | (L*), (F)&(M♯) | **(L*) refuters already lie in `𝒲`:** `n=9` #1, #2 have range 8, `n=11` has range 9, all `G`-connected (recomputed, `out_pad.txt` §7; the (L*) inequality itself is cited, not recomputed). The two `n=9` ones are disjoint unions. (F)&(M♯) (ranges 5–7): global spectral quantities, no transfer lemma, not padded | moot (spectral chain) |

## 5. Deep dive: the existential Step-6 transfer on `𝒦_min`

### 5.1 What the route needs

**Proposition 5.1 — PROVEN.** Suppose **(T∃^any)** holds: *for every `P ∈ 𝒦_min ∩ 𝒲` and some
proper ideal **or filter** `A` with `P[A]` a non-chain, some balanced pair of `P[A]` is balanced in
`P`*. Then, conditional on [H] and [D≤7], the conjecture holds.

*(Erratum, audit mg-244e §5: as first written, with ideals only, (T∃^any) fails on any poset whose
only balanced pair is two maximal elements — no proper ideal contains both. The V poset (two
elements over one) is such a case, and the audit's control fires on it. Allowing filters, as
mg-b447's "`P[A]` or `P[B]`" did, repairs this; the proof below is unchanged. On 158 random prime,
both-connected hosts with `n ≤ 8` neither form failed, EMPIRICAL. The hypothesis may be strictly
stronger than the conjecture on `𝒦_min ∩ 𝒲`; see §5.4(3).)*

*Proof.* A least counterexample is in `𝒦_min ∩ 𝒲` (Prop 3.1, [H], [D≤7]). It has width `≥ 3`
(Linial), so it has a 3-antichain. For any maximal `v`, `A = P − v` is a proper ideal containing
at least two elements of that antichain, so `P[A]` is a non-chain. The same holds for every proper
ideal containing two incomparable elements. By minimality `P[A]` has a balanced pair. So if
(T∃^any) holds at `P`, one of those pairs is balanced in `P`, which contradicts `P` being a
counterexample. □

The `Δ₁ ≤ ε` hypothesis of (T) is **not needed**: minimality supplies the side's balanced pair at
any cut. The two extreme choices of `A` are:

- `A = P − v` with `v` maximal: this is KSBFT-J's ONE-PT at a maximal `v` (0 failures on
  indecomposable posets, EMPIRICAL, `n ≤ 10` all, range ≤ 3 to `n = 16`);
- the middle cut: this is mg-63e3's (T) with `Δ₁ ≤ 2D/(n−1)`.

**The candidate's own killer is gone** (§4.2). Its remaining content is the transfer.

### 5.2 The proof attempt: insulation does all the far pairs

> **Theorem 5.2 (insulation transfer) — PROVEN (Thm 2.3).** Let `P ∈ Π_D`, `A` a proper ideal, and
> `(a,b)` a pair of `P[A]` with `P_{P[A]}[a<b] ∈ [1/3+μ, 2/3−μ]`, `μ > 0`. If for some linear
> extension `e` of `P` listing `A` first, `max(e(a),e(b)) ≤ |A| − h(D,μ)`, where
> `h(D,μ) := 2D + 1 + 2D⌈ln μ / ln θ_D⌉`, then `(a,b)` is balanced in `P`.

*Proof.* Thm 2.3 with `j = ⌈ln μ/ln θ_D⌉`, so that `θ_D^j ≤ μ`. □

> **Corollary 5.3 (balance is created at the cut) — PROVEN.** Let `P` be a least counterexample and
> `D = π(P)` (`8 ≤ D ≤ L*` under [H]+[D≤7]). Then for every proper ideal `A` and every `μ > 0`,
> every balanced pair of `P[A]` with margin `≥ μ` has `max(e(a),e(b)) > |A| − h(D,μ)` for every
> `e` listing `A` first. Dually, for every proper filter `B`, every `μ`-robust balanced pair of
> `P[B]` lies within `h(D,μ)` of `B`'s lower boundary.

*Proof.* Otherwise Thm 5.2 gives `P` a balanced pair. □

*(Erratum: Cor 5.3 is vacuous whenever `n < h(D,μ)`, and `h(D,μ) ≳ 10¹⁶` at `D = 8`. So it
constrains nothing at the sizes a counterexample might have.)*

> **Corollary 5.4 (ONE-PT at an extreme, for long posets) — PROVEN (repaired).** If `P ∈ Π_D` has a
> balanced pair of margin `μ > 0` and `n ≥ 2h(D,μ) + 2D + 1`, then some extreme `v` works for
> ONE-PT. More precisely: either every maximal `v`, or every minimal `v`, keeps that pair balanced
> in `P − v`.

*Proof (repaired per audit mg-244e §5).* By the cross-extension window of KSBFT-F Lemma 2.0
(`e₁(b) − e₂(a) ≤ π(a)+π(b)−1 ≤ 2D − 1`, valid across different extensions), the pair cannot lie
within `h(D,μ)` of both the top and the bottom once `n ≥ 2h(D,μ)+2D+1`. If it lies `h(D,μ)` or more
below the top, apply **Thm 2.3** (whose bound is symmetric in `P` and `P[A]`) to `A = P − v`, an
ideal listed first by an `e` that puts `v` last, to transfer the balance from `P` to `P − v`.
Otherwise use the dual (filters, `v` minimal). (As first written, the bound was `2h+2D`, one too
small, and the proof cited Thm 5.2, which transfers `P[A] → P`, the wrong direction.) The corollary
presupposes a robust balanced pair in `P`, so it contributes nothing toward the conjecture and is
vacuous on a counterexample. □

So **everything far from a cut transfers**, uniformly in `n`, at every range. (T∃) can fail only
through pairs within `h(D,μ)` of the cut or with small margin. By Cor 5.3, in a least counterexample
this happens at **every** cut simultaneously. (Erratum: "exactly" was OVERSTATED — for
`n < h(D,μ)` Cor 5.3 is vacuous and characterises nothing.)

### 5.3 What is consistent with the obstruction

- **`W*` is the decomposable toy model.** Its side `C_{a−2} ⊕ {x,y}` has exactly one balanced
  pair, and that pair sits at the cut.
- **Insulated `W*` shows why indecomposability helps.** The base must carry incomparable pairs, and
  one of them is balanced and far from the cut.
- For a least counterexample to exist, every truncation's bottom must have **no robustly balanced
  pair**. The truncation's bottom *is* `P`'s bottom, whose pairs are unbalanced in `P` and hence,
  by insulation, unbalanced in the truncation up to `θ_D^j`. That is exactly (M4): a low
  3-antichain at both ends, and no Local-Linial pair.
- KSBFT-Q's `P_9` (range 5, `n = 9`) shows the end-configurations can push balance into the middle.
  Whether a long indecomposable poset can be balanced **only near one end** (a "one-sided"
  counterexample) is KSBFT-Q §5's open question. A (T∃) refuter would need such sides at every cut.

### 5.4 The precise obstruction

(T∃^any) on `𝒦_min` is proved by Thm 5.2 for every pair at depth `≥ h(D,μ)`. What remains, and
nothing proves it:

1. **(Margin) A lower bound on how far the truncation's balanced pair sits from 1/3.** `p − 1/3` is
   a *signed* quantity. Bounded range quantises positive counts, via injections with bounded
   fibres (P1 §3.3), and it does not quantise differences. That is P1 §5.5's wall again. The only
   a-priori bound is `|p − 1/3| ≥ 1/(3e(P))` when non-zero, which is exponentially small.
   Closed-interval ties at exactly 1/3 do occur (`F_3`, `(2+1)`-type ends). KSBFT-J's empirical
   margins (`≥ 5/318` on indecomposable range ≤ 3, `7 ≤ n ≤ 16`) are the only evidence, and they
   are EMPIRICAL at range ≤ 3, far outside `𝒲`.
2. **(Constant) `h(D,μ) ≈ 2D(D+1)^{2D} ln(1/μ)`.** At `D ≥ 8` that is `≥ 10^{16}` elements. So
   "check the two end-windows" is a finite statement only in principle. KSBFT-N already prices
   `D = 8` whole-poset search as infeasible here.
3. **(Mechanism, the real gap) A lemma of the form:** *in a least counterexample, some truncation
   `P[A]` has a `μ`-robust balanced pair at depth `≥ h` below its cut.* Cor 5.3 says a least
   counterexample is exactly a poset where no truncation does. So this lemma **is** the conjecture
   on `𝒦_min ∩ 𝒲`, rephrased as a statement about where truncation-created balance can sit. It is
   a sharper target than (MC_D), because it localises the question to `h`-windows at the two
   boundaries of each truncation. But it is not a reduction to something known.

**Verdict on the deep dive.** The candidate survives padding, where every other δ-direct route
dies. Its far-field is proven (Thm 5.2, Cor 5.4). Its near-field is precisely the statement that
truncation-created balance can always be pushed away from some cut, modulo margin. No proof is
given.

## 6. What I did NOT do, and the candidates ruled out

**Not done:**

- **A24 (Hodge Thm G):** no link-spectrum transfer lemma, and no computation at `n ≥ 16`.
  Not decided.
- **(M7):** the localisation of KSBFT-I Thm 5 is stated as a conjecture, with the exact step that
  fails (the `N − D` complete cut). I did not re-read `tree.c`.
- **Primality of `attach_low(F_N,R)`** was EMPIRICAL here (`N ≤ 30`). It is now PROVEN for every
  `R ≥ 4`, `N ≥ R+2` by audit mg-244e §2. The theorems use only the connectivities.
- **Probe D's "co-degree"** has no definition in any source: the probes have no documents, and the
  sub-agent confirmed that from the index rows. I use "the number of elements comparable to exactly
  one of the pair", reconstructed from "1/6 at co-degree 2 via `C_p ⊔ C_q`". Under a different
  definition the A16 exhibit may not apply.
- **Several P1 table details are not in any source** (per the sub-agent's reading, which I spot-checked
  at `attempt-index.md:30-33`):
  - A13's "β ≡ 10⁻¹⁰⁰";
  - A14's "≤ 1/spread", "spread 4, range 3";
  - A15's "`n=6`, δ=1/3, `s=4`";
  - A16's "`1/C(p+q,p)`" formula.

  My A14 verdict does not rely on them: it exhibits its own window witness.
- **Rows A25, A27, (F)&(M♯):** not padded (moot routes, global spectral quantities).
- The source lemma statements of rows I did not open myself (B5, C1, C5, E4, A8, A9, A27, A28) are
  from a read-only sub-agent, with file:line citations. Rows A5, A13–A16, P1, KSBFT-A/F/I/J/Q were
  read directly.
- **No census or search.** Every computed poset is named in `out_pad.txt`.
- Nothing about `L*`, `K`, AK25a/b or Haq26 was re-checked.

**Candidates ruled out as the deep-dive target:**

1. A5 (KS/KL), A14 (probe B) and A16 (probe D): each killer survives into `𝒦_min ∩ 𝒲` (§4.1).
2. A13, A15, B1–B5, C1, C5, f5be, 5987, E4: structural.
3. 9b6b (density lever): its witness lapses on `𝒦_min`, but [H] turns the lever into a finite-`n`
   statement, so it is not a route.
4. (T_cont): fails on prime window-range posets (§4.2; the family is EMPIRICAL, `Δ₁ → 0` PROVEN).

**Recommendations to pm-onethird (no edits made):**

1. Record that the thin-witness walls of A5, A14 and A16 hold **as class lemmas on (M1)+(M2)**
   (Thm 2.1, exact exhibits), not merely inside `Π_D`. P1's "survives" becomes "survives on the
   (M1)+(M2) shape". The hosts are not counterexample-shaped (M3), so routes using
   counterexample-only hypotheses are not refuted (erratum).
2. Correct the record on Step 6: mg-b447 Thm 4.1 refutes the existential (T) **on decomposable
   posets only**; the refutation does not reach `𝒦_min` (erratum: "is of the continuity form" was
   BROKEN). The existential form (T∃^any), with "ideal or filter", is **unrefuted** on `𝒦_min`. Its far-field is
   proven here, and its near-field is the §5.4 obstruction. That makes it the natural home for the
   ONE-PT line (KSBFT-J) and the end analysis (KSBFT-Q).
3. Audit targets:
   - Lemma 1.1, Lemma 1.3(1), Lemma 2.0 and Thm 2.1(2)–(3) (closed forms, re-derivable by hand);
   - Thm 2.3 (its use of KSBFT-I Prop 1/Lemma 6; audit mg-9268 HOLDS);
   - Prop 3.1 (uses Linial);
   - the three exact exhibits (`attach_both(F_20,8)`, double hub `k = 8`, insulated `W*` (16,6,16)).
