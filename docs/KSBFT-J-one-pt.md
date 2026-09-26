# KSBFT-J: (ONE-PT) — no failure on 2.77 million non-chains; a canonical v (every element of minimal range) fails once, at n = 4; PROVEN for range ≤ 2; range 3 verified to n = 16 and open past that, for a reason that can be stated (mg-eedd)

Builds on mg-b447 (`docs/KSBFT-F-L4-step6-under-bounded-range.md`, §8, which names (ONE-PT_D)) and its audit mg-de37, and on mg-1911 (`docs/KSBFT-C-programme-repricing.md`, F1/F2). Instruments are in `code/ksbft_one_pt/`. `sh code/ksbft_one_pt/run_all.sh` regenerates every transcript quoted here. It is deterministic (two consecutive runs are byte-identical on every census file), takes ~11 min, and runs at most 3 processes.

Labels:
- **PROVEN**: the proof is in this file.
- **PROVEN (computer)**: an exhaustive, exact-integer computation over a finite class, with its instrument and its positive controls. It is a proof about that class only.
- **EMPIRICAL**: comes with its instrument and range.
- **CONJECTURED**: a guess.

Conventions. `P` is a finite poset. A pair `{x,y}` is *balanced* if `x ∥ y` and `p = P[x before y]` lies in the **closed** interval `[1/3, 2/3]` (uniform linear extension). `π(v)` is the number of elements incomparable to `v`, and `π(P) = max_v π(v)` is the range. `Π_D` is the class of posets of range `≤ D`. `P` is *indecomposable* if its incomparability graph `G(P)` is connected. The statement studied is:

> **(ONE-PT)(P)**: there exist `v ∈ P` and a pair `{x,y} ∌ v` that is balanced in both `P` and `P − v`.
> **(ONE-PT_D)**: (ONE-PT)(P) for every non-chain `P ∈ Π_D` with `n ≥ 3`.

"`v` works" means that some pair `{x,y} ∌ v` is balanced in both `P` and `P − v`.

---

## 0. Verdict

1. **"Exists v" never fails (EMPIRICAL, exact).** There are 0 failures on **every** non-chain isomorphism class with `3 ≤ n ≤ 10`. That is 2 769 953 posets, of which 2 567 283 have `n = 10` (§2). There are also 0 failures on every indecomposable class of range `≤ 3` for `n = 11..16` (129 683 posets), and of range `≤ 4` for `n = 11..13` (839 679 posets). mg-b447's census reached `n ≤ 6` (5 224 naturally labelled posets, i.e. 398 classes). Since (ONE-PT) is an isomorphism invariant, this census covers every labelled poset in its range.
2. **A canonical v exists in the data: every element of minimal range works (EMPIRICAL).** Over all 2 769 953 non-chains with `n ≤ 10`, the rule "**every** `v` with `π(v) = min_u π(u)` works" fails on exactly one poset: `A₁ + C₃` (a point beside a 3-chain, `n = 4`, with `v` the middle of the chain). It has 0 failures in every range-restricted class. The weaker "some minimal element works" and "some maximal element works" also have 0 failures on indecomposable posets. The h-order endpoint rule ("some h-first element works") fails once (`n = 9`, §3). **"Every v"** is FALSE and stays false (287 failures at `n = 10`). But among **indecomposable** posets of range `≤ 3` it fails only for `n ≤ 8` and at one `n = 12` poset. For `n = 13..16` it has 0 failures (§3).
3. **Margin.** Define `margin(P)` = max over `(v, pair)` of min(distance of `p_P`, distance of `p_{P−v}`) to the boundary of `[1/3, 2/3]`. It stays bounded away from 0 in every class computed: **≥ 1/51 ≈ 0.0196** for all `n ≤ 10`, and **0.0161–0.0175** at range 3 for `n = 11..16`, with no downward trend (§2.3). The canonical rule (worst over the minimal-range `v`) has a smaller margin, down to 1/159 ≈ 0.0063 (`n = 9`). The Fibonacci poset's margin converges to `1/φ² − 1/3 ≈ 0.04863`.
4. **PROVEN.**
   - (a) **Decomposable reduction** (Prop 1.2): for decomposable `P`, (ONE-PT)(P) ⟺ δ(P) ≥ 1/3. So (ONE-PT_D) ⟺ [the conjecture on `Π_D`] ∧ [(ONE-PT) on indecomposable members of `Π_D`], and only the indecomposable case has content.
   - (b) **Reweighting lemma R** (Lemma 1.3): the uniform measure on `L(P)` is the uniform measure on `L(P−v)` reweighted by the slot count `w_v ∈ [1, π(v)+1]` (mg-1911's F1 window, read as a density). Consequently `|p_P − p_{P−v}| ≤ (√(π(v)+1) − 1)/(√(π(v)+1) + 1)`. This is sharp at `π(v) = 1`: the census reaches 0.1715729 against the bound `3 − 2√2 = 0.1715729`, and 0 of 408 million exact checks violate it.
   - (c) **(ONE-PT_1) and (ONE-PT_2), in the canonical form** (Thms 4.1, 4.3): for every non-chain `P ∈ Π_2` with `n ≥ 3`, **every** element of minimal range works. The proof classifies the indecomposable members of `Π_2` (Lemma 4.2: `A₃`, `2+2`, and the Fibonacci posets `F_m`) and computes `F_m` exactly.
5. **Range 3: PROVEN (computer) for `n ≤ 16`, open for `n ≥ 17`.** The obstruction is quantitative and measured (§5). The only exact transport available, Lemma R, moves `p` by up to 0.1716 even when `π(v) = 1`. The pairs that actually transport have margins of about 0.016. So a proof needs the covariance `Cov_{P−v}(w_v, 1{x<y})` to be about 10× smaller than its worst case, for some pair located away from `v`. That is correlation decay along the window (mg-1911 §3.2, CONJECTURED there), and it has to be **exact enough to beat a 0.016 margin**, not asymptotic. The interface bound `τ ≤ 2D − 1` (sharpened to `τ ≤ D` by mg-de37) was **not** used and does not bear on this obstruction (§5.2).
6. **Item 4 (ε-transport) is moot.** "Exists v" never failed, so the fallback was not needed. The maximum over `P` of the ε such that some pair balanced in `P − v` lies within ε of `[1/3,2/3]` in `P` is exactly 0 in every class computed. Lemma R is the PROVEN universal ε-transport, with `ε(π(v))` as in 4(b).

---

## 1. PROVEN structure

### 1.1 Ordinal sums

**Lemma 1.1 (PROVEN, standard).** Let `C₁, …, C_k` be the vertex sets of the components of `G(P)`. After reordering, `P = P[C₁] ⊕ … ⊕ P[C_k]` (every element of `C_i` is below every element of `C_j` for `i < j`). Every linear extension of `A ⊕ B` is one of `A` followed by one of `B`. Hence for `x, y` in one summand, `P[x before y]` is the same in `P` as in that summand alone. Every incomparable pair lies inside one summand.

*Proof.* Elements in different components are comparable. Let `C ≠ C'` be components, `x ∥ y` in `C` adjacent in `G(P)`, and `x' ∈ C'`. If `x < x'` then `y < x'`: otherwise `x' < y`, and `x < x' < y` contradicts `x ∥ y`. By connectivity of `C`, `x < x'` for one `x ∈ C` forces `C < x'`. Symmetrically, connectivity of `C'` forces `C < C'`. The relation "`C < C'`" is a restriction of the order to representatives, hence a linear order on components. The statement about linear extensions follows because nothing of `B` can precede anything of `A`. □

**Prop 1.2 (decomposable reduction, PROVEN).** Let `P` be a decomposable non-chain with `n ≥ 3`. Then (ONE-PT)(P) ⟺ δ(P) ≥ 1/3.

*Proof.* (⟹) is trivial. (⟸): a balanced pair lies in one summand `S` (Lemma 1.1). Since `P` is decomposable there is another summand `S'`. Delete any `v ∈ S'`. Then `P − v` is the ordinal sum with `S'` replaced by `S' − v` (or `S'` dropped), so the pair's probability is unchanged (Lemma 1.1). □

So on decomposable posets (ONE-PT) *is* the conjecture. A minimal counterexample is indecomposable, since `δ(A ⊕ B) = max(δ(A), δ(B))` by Lemma 1.1. Every statement below about a "canonical v" is about indecomposable `P`.

### 1.2 The reweighting lemma

**Lemma 1.3 (R, PROVEN).** Fix `v`. For a linear extension `L'` of `P − v`, let `a(L')` be the position of the last element of `down(v)` (0 if none) and `b(L')` the position of the first element of `up(v)` (`n` if none). Set `w_v(L') := b − a`. Then:
1. `1 ≤ w_v(L') ≤ π(v) + 1`;
2. for every event `E` that depends only on the relative order of elements of `P − v`, `P_P[E] = E'[w_v·1_E] / E'[w_v]`, where `E'` is uniform on `L(P − v)`;
3. hence, with `r = π(v) + 1`, `p' = p_{P−v}(x<y)` and `p = p_P(x<y)`:

   `p'/(p' + r(1−p')) ≤ p ≤ r p'/(r p' + 1 − p')`,  and  `|p − p'| ≤ (√r − 1)/(√r + 1)`.

*Proof.* (2) Deleting `v` maps `L(P)` onto `L(P−v)` and preserves the relative order of the other elements. The preimage of `L'` is the set of ways to insert `v` after every element of `down(v)` and before every element of `up(v)`, which is `b − a` slots. (1) The elements strictly between positions `a` and `b` are in neither `down(v)` nor `up(v)`, so they are incomparable to `v`. There are `b − a − 1 ≤ π(v)` of them, and `b > a` because `down(v) < up(v)`. (3) The ratio `Σ w·1_E / Σ w` with `w ∈ [1, r]` is maximised by weight `r` on `E` and 1 off it, which gives the upper bound. The lower bound is the mirror. `g(p') = r p'/(r p'+1−p') − p' = p'(1−p')(r−1)/(1+(r−1)p')`. Put `s = √r` and `p' = 1/(1+s)`: then `1 − p' = s/(1+s)` and `1 + (r−1)p' = s`, so `g = (s−1)/(s+1)`. That this is the maximum is a one-variable calculus check: `g' = 0` reduces to `(r−1)p'² + 2p' − 1 = 0`, whose root in `(0,1)` is `1/(1+√r)`. □

This is F1 (mg-1911: `v` sits in a window of `π(v)+1` slots) read as a density rather than as a support bound.

*Checks (EMPIRICAL, exact).* Every `(P, v, pair)` in every scanned class is tested against the two-sided window in item 3, by integer cross-multiplication: 408 million checks at `n = 10` and 124 million at range `≤ 4`, `n = 13`. There are 0 violations. The **control**, the same window with `r = π(v)` in place of `π(v)+1`, is violated millions of times (`FIRES`), so the `+1` is needed. The worst `|p − p'|` at `π(v) = 1` is `6930/40391 = 0.17157288` (`n = 10`) and `40391/235416 = 0.17157288` (range 3, `n = 16`), against `3 − 2√2 = 0.17157288`. These are Pell-type approximants, so the bound is the supremum. For `π(v) ≥ 2` the observed maximum stays well below the bound (0.2107 vs 0.2679 at `π(v) = 2`, `n = 10`).

**Corollary 1.4 (PROVEN).** If `π(v) ≤ 1` and `p_{P−v}(x<y) = 1/2`, then `{x,y}` is balanced in `P`. (`r = 2`, `p' = 1/2` gives `p ∈ [1/3, 2/3]` exactly.) For `r ≥ 3`, or for `p' ≠ 1/2`, Lemma R alone certifies nothing on the closed interval.

---

## 2. The census (EMPIRICAL, exact)

### 2.1 Instrument

`code/ksbft_one_pt/onept.c`:
- **Generator.** Every isomorphism class on `n` elements is obtained from a class on `n − 1` by adding a new maximal element whose down-set is any order ideal. (Delete a maximal element of any poset to see that this is exhaustive.) Classes are then canonicalised and deduplicated. The canonical form is the least relation matrix over all leaves of an individualisation–refinement tree (1-WL colour refinement on down/up neighbourhoods). No automorphism pruning is used, so the form is exact. **Positive control:** the class counts are `1 2 5 16 63 318 2045 16999 183231 2567284` for `n = 1..10`, equal to OEIS A000112 (`out_gen_all.txt`). The range-restricted generator keeps only range `≤ D` at each step. This is exhaustive for `Π_D` because `Π_D` is closed under deleting elements. Its counts at `n = 9, 10` (2 942, 8 362 for `D = 3`) equal the range-`≤ 3` subtotals of the unrestricted census plus the chain.
- **Counter.** DP over order ideals, in `unsigned __int128`. `N_P(x,y) = Σ_I N(I)·S(I ∪ x)` over ideals `I` avoiding `x, y` with `x` addable. `P` and all `n` deletions `P − v` are computed separately. **Positive controls** (`out_controls.txt`): brute-force permutation counts agree on 420 random posets and all their deletions (`n = 6, 7, 8`). The Fibonacci poset gives `e(F_M) = f(M+1)` and `#(x₂ before x₁) = f(M−1)` for every `M ≤ 20` (Lemma 4.4).
- **Decisions are integer.** "Balanced" is `3N ≥ e ∧ 3N ≤ 2e`. Margins are fractions `min(3N−e, 2e−3N)/(3e)` compared by cross-multiplication. No floating point enters any count or comparison.
- **Firing controls.** (i) The "every v" row must be nonzero, and it is in every exhaustive range. (ii) mg-3af9/mg-b447's `W*(4,4,2)` must fail "every v", and it does. The failing `v` are exactly `x` and `b₁` (`W = eb`). mg-b447 named `b₁`; `x` also fails. (iii) With the interval narrowed to `[2/5, 3/5]`, "exists v" **must** fail somewhere, and it does at every `n = 3..8`: 1, 2, 2, 3, 10, 46 indecomposable failures (`out_control_narrow.txt`). One example is the Fibonacci `F_m`, whose balanced pairs sit near `0.382`. (iv) Lemma R's `r → r−1` control (§1.2).

### 2.2 Results

"all" means every non-chain isomorphism class. "indec" means those with `G(P)` connected. Each cell counts failures (posets where the rule fails).

| class | #posets | exists v | every v (control) | some minimal v | some maximal v | some h-endpoint | some min-range v | **every min-range v** |
|---|---|---|---|---|---|---|---|---|
| all, n = 3..8 | 19 440 | **0** | 160 | 6 | 6 | 0 | 0 | 1 (`n=4`) |
| all, n = 9 | 183 230 | **0** | 153 | 1 | 1 | 0 | 0 | 0 |
| all, n = 10 | 2 567 283 | **0** | 287 | 1 | 1 | 0 | 0 | 0 |
| indec, n = 3..10 | 2 338 137 | **0** | 133 | **0** | **0** | 0 | 0 | 1 (`n=4`) |
| indec, range ≤ 3, n = 11..16 | 129 683 | **0** | 1 (`n=12`) | 0 | 0 | 0 | 0 | 0 |
| indec, range ≤ 4, n = 11..13 | 839 679 | **0** | 2 | 0 | 0 | 0 | 0 | 0 |

The two range blocks overlap: range `≤ 4` contains range `≤ 3`. The per-`n`, per-`π` breakdown, 18 rules in all, is in `out_census_all.txt`, `out_census_indec.txt` and `out_census_range.txt`.

The "some minimal v" failures in the "all" rows are one decomposable poset per `n`: `A₂ ⊕ C_{n−2}` (e.g. `9 0 0 3 7 f 1f 3f 7f ff`). Its minimal elements are the two elements of the `A₂`, and deleting either destroys the only incomparable pair, while every other `v` works. The "some maximal v" failures are the duals, `C_{n−2} ⊕ A₂`. Prop 1.2 disposes of all of these.

The number of working `v` is almost always all of them. At `n = 10`, 2 566 996 of 2 567 283 non-chains have **every** `v` working. For indecomposable range `≤ 3` at `n = 13..16`, every `v` works in every poset.

### 2.3 Margin

`margin(P)` = max over `v` and pairs `{x,y} ∌ v` of min(`d_P`, `d_{P−v}`), where `d` = min(`p − 1/3`, `2/3 − p`). The canonical margin is the min over minimal-range `v` of that `v`'s best pair. Both are exact rationals, with minima taken over the class:

| class | worst margin | at | worst canonical margin |
|---|---|---|---|
| indec n=8 | 1/45 (π=3) | `8 0 0 2 6 3 13 f 3f` | 1/69 |
| indec n=9 | 1/51 (π=4) | `9 0 0 2 6 3 e 13 53 7f` | 1/159 (π=5) |
| indec n=10 | 5/318 (π=3) | `10 0 0 2 6 3 17 1f 5f 3f 17f` | 1/81 (π=8) |
| range ≤3, n=11..16 | 1/57, 14/831, 23/1344, 37/2175, 23/1425, 97/5694 | family `0 0 2 6 3 17 1f …` | 8/525, 1/84, 2/129, 11/687, 7/435, 4/249 |
| range ≤4, n=11..13 | 19/789, 19/906, 16/807 (π=4) | | 5/318, 2/129, 29/1893 |
| Fibonacci `F_m` (π=2) | → `1/φ² − 1/3 = 0.048633` | `F_n` | same |

(Posets are printed as `n` followed by the strict down-sets in hex, in canonical labelling.) At range 3 the worst margin oscillates in `[0.0161, 0.0175]` for `n = 11..16`, with no trend towards 0. The minimisers are a single family: a fixed gadget `0 0 2 6 3 17` followed by a Fibonacci-like tail. That is consistent with a limit margin near 0.016 **(CONJECTURED)**.

---

## 3. Which v works (item 2)

EMPIRICAL, same instrument and classes.

- **Every element of minimal range works** (`π(v) = min_u π(u)`). Among all non-chains with `n ≤ 10` this fails once: `A₁ + C₃` (`4 0 0 2 6`). There the minimal-range elements are the three chain elements (`π = 1`). The top and bottom work. The middle one `c₂` fails: `P − c₂ = A₁ + C₂` has pair probabilities `1/3, 2/3`, but in `P` those pairs have `1/4, 3/4`. Zero failures in every range-restricted class. For decomposable `P` with a singleton summand, the minimal-range elements are the `π = 0` ones. Deleting them changes no probability, so there the rule is exactly δ ≥ 1/3.
- **Some minimal element works** and **some maximal element works**: 0 failures on indecomposable posets in every class. On decomposable posets they fail exactly as described in §2.2.
- **h-endpoints.** "Some element of least `h = E f(x)`" fails on one indecomposable poset (`9 0 0 2 1 6 9 16 2b bf`, π = 5). "Some element of greatest `h`" fails on its dual. "Some h-endpoint" (first or last) has 0 failures.
- **Every v with P − v indecomposable**: this fails, and in fact nearly all "every v" failures have `P − v` indecomposable. So the failing deletions are *not* the ones that split `P`.
- **Every v** fails, with the obstruction dying out with `n` at bounded range. Among indecomposable posets of range `≤ 3` it fails at `n = 3..8` (1, 1, 2, 2, 3, 1 posets) and at one poset at `n = 12` (`12 0 0 2 6 3 17 f 5f 3f 17f ff 5ff`, `v` = element 6). It fails nowhere at `n = 9, 10, 11, 13, 14, 15, 16`. mg-b447's `W*` is **decomposable** (`c₁, c₂` are comparable to everything), so it is not an indecomposable counterexample to "every v".
- **Pair-first**: "some `v` together with a δ-attaining pair of `P`" has 0 failures everywhere. **Strong transport** ("some `v` all of whose balanced pairs in `P − v` stay balanced in `P`") fails often: 181 153 times at `n = 10`. An induction therefore cannot take an *arbitrary* balanced pair of `P − v`. It must choose the pair.

**CONJECTURED (ONE-PT-min).** For every non-chain `P` with `n ≥ 5`, every element of minimal range works. This is proved for `Π_2` (Thm 4.3), holds for all `n ≤ 10` and for range `≤ 3` to `n = 16` (EMPIRICAL), and is the canonical form a proof would use. Its mechanism would be Lemma R: small `π(v)` means a small weight spread `r = π(v)+1`.

---

## 4. Proofs at small D (item 3)

### 4.1 D = 1

**Theorem 4.1 (PROVEN).** (ONE-PT_1) holds, and every element of minimal range works.

*Proof.* `π ≤ 1` means `G(P)` has maximum degree `≤ 1`, so every component of `G(P)` is `A₁` or `A₂`. With `n ≥ 3` and `P` not a chain, Lemma 1.1 gives `P = S₁ ⊕ … ⊕ S_k` with `k ≥ 2` and some `S_i = A₂`, whose pair has `p = 1/2`. Let `v` have minimal range. If some summand is a singleton, `π(v) = 0`, and deleting `v` changes no probability (Lemma 1.1). The `A₂` pair works. Otherwise every summand is `A₂`, so `k ≥ 2`, and the `A₂` not containing `v` keeps `p = 1/2`. □

### 4.2 D = 2

**Lemma 4.2 (PROVEN).** If `P` is indecomposable with `π(P) ≤ 2` and `n ≥ 3`, then `P` is `A₃`, `2+2` (two disjoint 2-chains), or the Fibonacci poset `F_n` (`x_i < x_j` iff `j − i ≥ 2`).

*Proof.* `G(P)` is connected with maximum degree `≤ 2`, so it is a path `u₁ − u₂ − … − u_n` or a cycle. All non-adjacent pairs are comparable.

*Propagation step.* Suppose `u_i < u_{i+2}`, and `u_{i+3}` is comparable to both `u_i` and `u_{i+1}`. Then `u_{i+1} < u_{i+3}` and `u_i < u_{i+3}`. Indeed, suppose `u_{i+3} < u_{i+1}`. If `u_{i+3} < u_i`, then `u_{i+3} < u_i < u_{i+2}`, contradicting `u_{i+3} ∥ u_{i+2}`. If `u_i < u_{i+3}`, then `u_i < u_{i+3} < u_{i+1}`, contradicting `u_i ∥ u_{i+1}`. So `u_{i+1} < u_{i+3}`. Now if `u_{i+3} < u_i`, then `u_{i+1} < u_{i+3} < u_i`, a contradiction, so `u_i < u_{i+3}`.

*Path.* Replacing `P` by its dual if needed, `u₁ < u₃`. The step applies for every `i ≤ n − 3`, so `u_i < u_{i+2}` for all `i ≤ n − 2` and `u_i < u_{i+3}` for all `i ≤ n − 3`. Every `j ≥ i + 2` is reached from `i` by steps of 2 and 3, so `u_i < u_j` by transitivity. Hence `P ≅ F_n`. `F_n` is self-dual via `x_i ↦ x_{n+1−i}`, so the dual case gives `F_n` too.

*Cycle, n ≥ 5.* `u₁, u₃` are non-adjacent, so WLOG `u₁ < u₃`. The step at `i` needs `{i, i+3}` and `{i+1, i+3}` to be non-edges. In a cycle the only extra edge is `{1, n}`, and `{i, i+3} = {1, n}` forces `n = 4`. So all steps `i = 1..n−3` apply, and as for the path, `u₁ < u_n`. But `u₁ ∥ u_n`, a contradiction.

*Cycle, n = 4.* The comparable pairs are exactly `{u₁,u₃}` and `{u₂,u₄}`, so `P` is two 2-chains with all cross pairs incomparable, i.e. `2+2`.

*Cycle, n = 3.* This is `A₃`. □

**Lemma 4.4 (PROVEN).** With `f(0)=0, f(1)=f(2)=1, f(k+1)=f(k)+f(k−1)`: `e(F_m) = f(m+1)`, and for `m ≥ 2`, `P_{F_m}[x₂ before x₁] = f(m−1)/f(m+1) ∈ [1/3, 1/2]`.

*Proof.* The first element of a linear extension is minimal, so it is `x₁` or `x₂`, since `x_j > x₁` for `j ≥ 3`. If it is `x₁`, the rest is a linear extension of `F_{m−1}` on `x₂..x_m`. If it is `x₂`, the next must be `x₁`, the only minimal element left (`x_j > x₁` for `j ≥ 3`), and the rest is a linear extension of `F_{m−2}`. So `e(F_m) = e(F_{m−1}) + e(F_{m−2})` with `e(F₀) = e(F₁) = 1`, and `#(x₂ before x₁) = e(F_{m−2}) = f(m−1)`. For `k = m ≥ 2`: `f(k+1) = f(k) + f(k−1) ≥ 2f(k−1)`, so the ratio is `≤ 1/2`. Also `f(k+1) = 2f(k−1) + f(k−2) ≤ 3f(k−1)`, so it is `≥ 1/3`. □

(`out_controls.txt` checks both formulas for `M ≤ 20`.)

**Theorem 4.3 (PROVEN).** (ONE-PT_2) holds. Moreover, for every non-chain `P ∈ Π_2` with `n ≥ 3`, **every** element of minimal range works.

*Proof.* **Indecomposable `P`** (Lemma 4.2):
- `A₃`: every `v` has `π = 2`. `P − v = A₂`, and its pair has `p = 1/2` in both `P` and `P − v`, by the transposition symmetry.
- `2+2` (`a < b`, `c < d`): every `v` has `π = 2`. There is an automorphism swapping the chains (`a ↔ c`, `b ↔ d`), so `P[a before c] = P[b before d] = 1/2`.
  - `v = b`: `P − b = {a} ∥ {c < d}` has extensions `acd, cad, cda`, so `P[a before c] = 1/3`. Balanced in both.
  - `v = a`: `P − a = {b} ∥ {c < d}`, so `P[b before d] = 2/3`. Balanced in both.
  - `v = c, d`: the same, by the automorphism.
- `F_n` (`n ≥ 3`): the minimal-range elements are `x₁` and `x_n` (`π = 1`; every interior element has `π = 2`). `F_n − x_n = F_{n−1}`, and `{x₁, x₂}` has `P[x₂ before x₁] = f(n−1)/f(n+1)` in `F_n` and `f(n−2)/f(n)` in `F_{n−1}`. Both lie in `[1/3, 1/2]` by Lemma 4.4, since `n − 1 ≥ 2`. For `v = x₁`, apply the anti-automorphism `x_i ↦ x_{n+1−i}`: the pair `{x_{n−1}, x_n}` has the complementary probabilities, which are also in `[1/2, 2/3]`.

**Decomposable `P`**, `P = S₁ ⊕ … ⊕ S_k`, `k ≥ 2`. Every nontrivial summand is `A₂`, `A₃`, `2+2` or `F_m`, and each has a balanced pair with `p ∈ [1/3, 1/2]` (Lemma 4.4 and the symmetries above). Let `v` have minimal range and lie in summand `S`.
- If some summand is a singleton, `π(v) = 0`, so `v` is a singleton summand. Deleting it changes no probability, and any nontrivial summand's balanced pair works.
- Otherwise every summand is nontrivial, and a summand `S' ≠ S` exists. Its balanced pair is unchanged by deleting `v` (Lemma 1.1). □

### 4.3 D = 3

**Theorem 4.5 (PROVEN (computer)).** (ONE-PT_3) holds for every non-chain `P ∈ Π_3` with `n ≤ 16`. Every element of minimal range works for all of these except `A₁ + C₃`.

*Proof.* A decomposable poset reduces to δ ≥ 1/3 of some summand (Prop 1.2). Every nontrivial summand is either `A₂` (`p = 1/2`) or an indecomposable member of `Π_3` with `3 ≤ size ≤ 15`, and for those the verified (ONE-PT) implies δ ≥ 1/3. No literature is needed. Indecomposable ones: `out_census_indec.txt` covers `n ≤ 10` (all ranges) and `out_census_range.txt` covers `Π_3` for `n = 11..16`. The generator is complete for `Π_3` (§2.1), and its counts are cross-checked at `n = 9, 10` against the unrestricted census. The exact counter is controlled (§2.1). □

Likewise **(ONE-PT_4) holds for `n ≤ 13`** (PROVEN (computer), same argument, `out_census_range.txt`).

**What a hand proof at D = 3 would need, and why it is not here.** Lemma 4.2 fails at `D = 3`. Indecomposable members of `Π_3` are not a finite list of families: they number 1 404, 3 076, 6 736, 14 792, 32 455, 71 220 at `n = 11..16`, growing by about ×2.2 per step. So a proof must be structural, not a classification. §5 says exactly what is missing.

---

## 5. The obstruction beyond the finite check (item 3, continued)

### 5.1 What the natural argument needs, quantitatively

The natural argument is:
1. pick the canonical `v` (minimal range);
2. find a pair `{x,y}` balanced in `P − v`;
3. show it stays balanced in `P`.

Step 2 is the induction hypothesis. Step 3 is exact transport. Lemma R gives step 3 **only if** `p_{P−v}` is at distance `≥ (√r−1)/(√r+1)` from the boundary: `0.1716` for `π(v) = 1`, `0.268` for `π(v) = 2`, `0.333` for `π(v) = 3`. At `π(v) ≥ 3` this is impossible, since the interval has half-width `1/6`. At `π(v) = 1` the window of Lemma R stays inside `[1/3, 2/3]` only for `p' = 1/2` exactly: `p'/(p'+2(1−p')) ≥ 1/3` needs `p' ≥ 1/2`, and the upper bound needs `p' ≤ 1/2` (Cor 1.4). The pairs that actually transport in the census have `margin ≈ 0.016` at range 3 (§2.3). **So the crude transport is off by a factor of about 10 even in the best case.**

The gap is exactly the covariance term. By Lemma R, `p − p' = Cov_{P−v}(w_v, 1{x<y}) / E'[w_v]`. The worst case (0.1716) is when `w_v` is a function of `1{x<y}`, i.e. the pair sits in `v`'s window. A proof must instead choose the pair **away from `v`** and show `|Cov(w_v, 1{x<y})| ≤ 0.016·E'[w_v]`. `w_v` depends only on the order of the `≤ π(v)` elements of `v`'s window relative to `down(v)` and `up(v)`, which is F1/F2 locality. So what is needed is a decay-of-correlations statement along the window (mg-1911 §3.2, CONJECTURED there). It must be

- (a) **explicit** at a distance of a few windows, not merely `→ 0`;
- (b) combined with a **margin statement**: a pair of `P − v` balanced with margin `μ(D) > 0`, which the induction hypothesis (δ ≥ 1/3) does not supply.

Point (b) is the real wall. The induction hypothesis gives `δ(P − v) ≥ 1/3`, **with no margin**. So step 3 must be exact at the boundary, and no decay estimate delivers exactness. This is mg-b447 §8's last bullet, made quantitative. The census says that the margin *exists* (≥ 0.016 at range 3, EMPIRICAL). But proving it means proving `δ ≥ 1/3 + μ` on `Π_3`, which the known `π ≤ 5` result (BW92) does not imply, so the induction does not reduce the problem.

**CONJECTURED (route).** An induction would have to carry the stronger hypothesis "every non-chain in `Π_D` of size `< n` has a pair with margin `≥ μ_D` located near each end of the h-order". Lemma R plus decay would then transport a pair from the *far* end. `F_m` satisfies this with `μ₂ = 1/φ² − 1/3`, and it is how Thm 4.3's `F_m` case works (`v = x_m`, pair at `x₁x₂`). This was not attempted beyond `D = 2`.

### 5.2 The interface bound

mg-b447's `τ ≤ 2D − 1` (sharpened by mg-de37 to `τ ≤ D`) bounds the branch-(ii) certificate at a cut. ONE-PT deletes a point and does not cut, so `τ` does not enter. The relevant local quantity is the slot count `w_v ≤ π(v) + 1` of Lemma R. I did not find a way to use `τ` here, and I am not claiming that none exists.

---

## 6. Item 4

"Exists v" never failed, so the weaker transport was not needed. Measured: the maximum over `P` of [the minimum over `(v, pair balanced in P−v)` of the distance of `p_P` outside `[1/3,2/3]`] is **exactly 0** in every class (EMPIRICAL). The universal ε-transport that holds for **every** pair and every `v` is Lemma R, `ε = (√(π(v)+1) − 1)/(√(π(v)+1) + 1)`. It is sharp at `π(v) = 1` (PROVEN bound, sup attained in the limit, EMPIRICAL). So "within ε of balanced" holds with `ε = 3 − 2√2` whenever `v` has `π(v) = 1`, which every indecomposable `F_m`-like end supplies.

---

## 7. What I did not do, and the negatives

**Not done:**
- `n = 11` exhaustively (all 46 749 427 classes). The generator stores every class in memory (~2 GB at `n = 11`), and I did not write the canonical-augmentation (orderly) version that would avoid storing them.
- Range `≤ 3` past `n = 16`, range `≤ 4` past `n = 13`, range `≥ 5` past `n = 10`.
- A proof at `D = 3` for `n ≥ 17`. §5 is an obstruction analysis, not a proof that no proof exists.
- The decay/margin route of §5.1 was **not** attempted beyond `D = 2`.
- BW92, Peczarski and Gup26 were cited, not re-verified. Nothing proven here depends on them.
- `mg-1911`'s F1/F2 were consumed only through Lemma R, which is re-proved here from scratch. `τ` was not used.
- Nothing consumes KSBFT Lemma 4.2, the constant 441 or eq. (1.5).

**Negatives (candidate canonical choices of `v` that FAIL, with witnesses):**
1. *Every v.* FALSE: 287 failures at `n = 10`, including indecomposable ones such as `8 0 0 2 6 3 17 f 5f` and `12 0 0 2 6 3 17 f 5f 3f 17f ff 5ff`.
2. *Every extremal (minimal or maximal) v.* FALSE: 27 failures at `n = 10`, e.g. `F₃` with `v = x₂`, where `P − v` is a chain.
3. *Every minimal v.* FALSE: 3 indecomposable failures at `n = 10`.
4. *Some minimal v*, *some maximal v*, on decomposable `P`. FALSE: `A₂ ⊕ C₇` and its dual. On indecomposable `P`: no failure found.
5. *Some h-first v.* FALSE on one indecomposable poset at `n = 9` (`9 0 0 2 1 6 9 16 2b bf`); "some h-last v" fails on its dual.
6. *Some v of maximal range.* FALSE: 105 failures at `n = 10`.
7. *Every v whose deletion keeps P indecomposable.* FALSE: 55 failures at `n = 10`.
8. *Some v with a pair comparable to v on both sides.* FALSE: 41 failures at `n = 10`, mostly `π = n − 1`, e.g. the antichain.
9. *Strong transport* (every balanced pair of `P − v` stays balanced). FALSE: 181 153 failures at `n = 10`.
10. *Crude transport via Lemma R alone* (§5.1). Insufficient by a factor of about 10 at range 3.

**Survivors (0 failures in every class computed):** exists v; some minimal-range v; every minimal-range v (except `A₁ + C₃`); some h-endpoint v; some v with a δ-attaining pair of `P`; and, on indecomposable `P`, some minimal v and some maximal v.
