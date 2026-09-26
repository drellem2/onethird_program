# KSBFT-Q: localizing Linial's width-2 proof. It localizes exactly: a counterexample must be locally width ≥ 3 at BOTH ends, below the Linial crossing (PROVEN). The complementary "end balanced for another reason" fails for the local configurations {x} ∪ Inc(x) at both ends: an exact range-5 poset on 9 elements has no balanced pair inside either end window; its balanced pairs straddle the two end gadgets (mg-5f14)

Instrument: `code/ksbft_q_local_width2_5f14/` (Python, exact integers/Fractions). `sh code/ksbft_q_local_width2_5f14/run_all.sh` regenerates every transcript (~1 h wall at 3 processes). The census files come from mg-eedd's generator (`code/ksbft_one_pt/onept.c`, reached through `code/ksbft_m_margin_6b81/pcert.c onept gen`). Its positive control is OEIS A000112 (1, 2, 5, 16, 63, 318, 2045, 16999, 183231 for n = 1..9, reproduced in `out_gen.txt`). The indecomposable counts also match earlier censuses: Π_3 gives 289 / 6 736 at n = 9 / 13 (mg-6b81 §1), and Π_4 gives 50 910 / 176 766 at n = 11 / 12 (mg-eedd).

**Errata (mg-a468, per audit mg-3345, `docs/AUDIT-mg-3345.md` §4).** No theorem changes. Thm 2.1, Cors 2.2–2.4, Prop 2.5, Thm 3.1 and Lemmas 1.1/3.2/3.3 HOLD. Corrected: the §3.2 inclusion (it runs the other way; equality only at `j = k`), so verdict 5's "intersection" holds only at `j* = k`; verdict 6(a) "touching" → "inside"; the WIN-failure counts at range ≤ 6 are 2 / 18, not 4 / 29 (those are the BR counts); `P_9` has no middle — its balanced pairs straddle the two end gadgets, and the `n = 11` record is the genuinely interior example; Remark 2.6's labelling `(v_1, v_2) = (y, x)` is EMPIRICAL, not implied; "all posets" → "indecomposable posets"; Thm 3.1 needs "not a chain"; "5–15 points" → 4.1–14.9; "as it must" qualified.

Labels, as in the other KSBFT files:
- **PROVEN**: the proof is in this file.
- **EMPIRICAL**: exact arithmetic over a stated finite population, with the instrument named.
- **CONJECTURED**: a guess.

Computation is used only as a probe. It tests candidate lemmas on the census and looks for counterexamples. No case search was extended.

Conventions: `Inc(x)` is the set of elements incomparable to `x`, so `π(x) = |Inc(x)|`. `f(x)` is the position of `x` in a uniform random linear extension. A pair is *balanced* if `x ∥ y` and `P[x before y] ∈ [1/3, 2/3]`.

---

## 0. Verdict

1. **Linial's proof, read carefully, uses three facts, and only one of them is about width (§1, PROVEN).**
   - (L1) The position law of a *minimal* element is non-increasing. This holds in every finite poset, by a one-swap injection.
   - (L2) For the chosen minimal `x`, the prefix before `x` is determined by its size. This holds when `Inc(x)` is a chain, and it is needed only up to the crossing index `j*`.
   - (L3) Some minimal `x` has `P[x first] ≤ 2/3`. This holds whenever there are at least 2 minimal elements.

   Width 2 enters only through (L2), for one element, up to rank `j* ≤ π(x)`. Nothing above the `(j*+1)`-th element of `Inc(x)` is used. The top of `P` is never used. The second chain is used only through its minimal element.

2. **Local Linial Theorem (Thm 2.1, PROVEN).** Let `x` be minimal with `P[x first] ≤ 2/3`. Let `c_1 < … < c_k` be the chain bottom of `Inc(x)`, i.e. the longest chain such that `c_{j+1}` is the unique minimal element of `Inc(x) ∖ {c_1..c_j}`. If `P[f(x) ≤ k] ≥ 1/3`, then some `(x, c_j)`, `j ≤ k`, is balanced.

   Structural sufficient condition (Cor 2.2): `3k ≥ |Inc(x)| + 1`.

   Linial's theorem is the special case in which `Inc(x)` is a whole chain (Cor 2.4). Under range `≤ D`, all the data the theorem needs sits in a bottom ideal of size `≥ 3D`. Its two hypotheses are linear in the law of the prefix, so they pass through the prefix-certificate mixture (Prop 2.5). That makes it an **n-uniform, pair-agnostic certificate**: different bottom ideals may cross at different `j`, yet `P` is still certified.

3. **The structural reduction (Thm 3.1, PROVEN).** In any poset with no balanced pair, **every** minimal `x` with `P[x first] ≤ 2/3` (at least one exists) has these properties:
   - `Inc(x)` branches before the Linial crossing: `P[f(x) ≤ k] < 1/3`;
   - hence `3k < π(x) + 1 ≤ D + 1`;
   - there are `u ∥ v` in `Inc(x)` lying above all of `c_1..c_k`.

   So `{x, u, v}` is a 3-antichain of rank `≤ k + 2 < (D+1)/3 + 2` in `{x} ∪ Inc(x)`. The same holds at the top, dually. **A counterexample is locally width ≥ 3 at both ends, low down.** There are two shapes:
   - **(O1)** `≥ 3` minimal elements (`k = 0`);
   - **(O2)** exactly 2 minimal elements `x, y` whose poorer element `x` carries a **Y-gadget**: `x ∥ y = c_1 < … < c_k < {u, v}`, with `u ∥ v`.

4. **The data is explained (§2.6, PROVEN + EMPIRICAL).**
   - On every one of mg-2912's 44 distinct δ < 0.35 records (`n` up to 24), Local Linial fires at one end, the crossing is at `j* = 0`, and the Linial pair attains δ. It fires at the bottom for 41 records and at the top for 3. The pair is the two minimal (resp. maximal) elements, with value `P[x first]`.
   - PROVEN: if a minimal `y` has `Inc(y) = {x}`, then `P[x before y] = h(y) − 1` (the special case `W = {w}` of KSBFT-A §6's `δ(v_1, w) = d_1`; not new). With `y = v_1` this gives mg-2912's "δ = M = d_1, extreme element with one incomparable"; that the pair is then `(v_1, v_2)` is EMPIRICAL (44/44 records), not implied.
   - Near-extremal posets are the ones where Linial's ladder stops at its first rung.

5. **The obstruction: Linial does not extend past a local 3-antichain (§3, PROVEN by exact witnesses).**
   - At the branch, the threshold event `{f(x) ≤ j*+1}` is still balanced (Lemma 3.2, PROVEN, every poset). When `j* = k` it is an *intersection* `{x before u} ∩ {x before v}` of pair events, and nothing forces any one pair to be balanced. (For `j* > k` it is not an intersection: `∩_U {x before u} = {f(x) ≤ k+1}` is strictly smaller. In a counterexample `j* ≥ k`; e.g. `W8`'s bottom has `k = 0`, `j* = 2`.)
   - The only constraints are `P[x<u], P[x<v] ≥ S_k` and `P[x<u] + P[x<v] ≤ 1 + S_k` (Lemma 3.3).
   - Witness `6 0 0 2 2 3 f`: both `(x,u)` and `(x,v)` are at `19/26`. The balance moves to `(u, v)`, at 1/2.

6. **The step-3 question: every bottom end locally width 2 or balanced for another reason? No, in every bounded-configuration form I could state.**
   - (a) **Balance inside `{x} ∪ Inc(x)` for some extreme `x`, at either end (WIN), is FALSE at range 5.** Exact witness `P_9 = 9 0 0 2 2 3 b 2b 2f 7f` (hex down-masks; range 5, width 3, self-dual, a Y-gadget at each end). Its only balanced pairs are `(2,4), (2,5), (4,5)`. No pair lying **inside** `{x} ∪ Inc(x)` for an extreme `x` is balanced (§3.4). All three balanced pairs do *touch* an end window: `P_9` has no middle (the windows `{0,1,2,3}`, `{4,6,7,8}` and the element `5` are all of it), and its balanced pairs straddle the two gadgets — `(2,4)` joins the bottom gadget's `u` to the top gadget's `u`. The genuinely interior example is the `n = 11` range-6 record below. Census: 1 / 4 / 0 such posets at range ≤ 5 for `n = 9 / 10 / 11`, and 2 / 18 at range ≤ 6 for `n = 9 / 10` (the BR counts there are 4 / 29), plus the `n = 11` record below. Whether they persist for large `n` at fixed D is OPEN (§5).
   - (b) The narrower "branch lemma" BR (some pair in `{x} ∪ C ∪ U` is balanced) fails there too. It also fails at range 6, `n = 11`: this is mg-2912's own `min δ` record at π = 6, δ = 134/375, whose balanced pairs `(4,5)` and `(4,7)` touch no end window.
   - (c) **A local 3-antichain gives balance by no known argument, and by no true one in the naive form.** "`≥ 3` minimal elements ⇒ some pair of minimal elements balanced" is FALSE: exact range-6 witness on 8 elements with no isolated element; 2 622 counterexamples among the indecomposable posets with `n = 9` (1 762 of them have an element comparable to nothing). EMPIRICAL: it holds for range `≤ 5` in the whole census here (`n ≤ 11` at D=5, `n ≤ 12` at D=4, `n ≤ 13` at D=3).
   - What survives is mg-e8b4's **computer-proven** bottom window of N_D canonical elements (D ≤ 7; `N_5 = 15 ≥ 9`, so no conflict). It is a finite check, not a mechanism.

7. **Coverage (EMPIRICAL, §4).** Local Linial at either end (quantitative form) fires on:
   - 87% of indecomposable range-≤3 posets (`n = 13`);
   - 73% at range ≤ 4 (`n = 12`);
   - 63% at range ≤ 5 (`n = 11`);
   - 49% at range ≤ 6 (`n = 10`);
   - 34% of the indecomposable posets at `n = 9` (any range).

   Zero violations of Thm 2.1 or Lemma 1.1 anywhere; both checks fire under their controls. Everything Linial does not cover is O1 or O2: the proof of Thm 3.1 (ii)–(iii) uses only "LL does not fire at that end".

**Bottom line.** The localization works, and it gives a clean necessary condition on counterexamples: a low 3-antichain at both ends. That condition is not closed by any local argument at the ends. The range-5 witness shows that no end window need contain a balanced pair even at `n = 9`: its balanced pairs straddle the two end gadgets (it has no middle). The `n = 11` range-6 record has genuinely interior balanced pairs. Whether that persists for long posets at fixed D is open: at range 5 the census has such posets at `n = 9, 10` and none at `n = 11`. The next conceptual object is the Y-gadget/3-antichain transfer, i.e. how balance propagates inward. That is the 1/3–2/3 problem proper, not a width-2 problem.

---

## 1. Linial's proof, and exactly what it uses

**Source note.** I did not obtain the 1984 SIAM J. Comput. text; it is paywalled, and no request was made. What follows is the standard proof as it is usually expounded, written out in full, so correctness here does not depend on the source. It recovers Linial's theorem (Cor 2.4).

**Lemma 1.1 (monotone position law of a minimal element, PROVEN; any finite poset).** Let `x` be minimal and `q_j = P[f(x) = j+1]`, i.e. exactly `j` elements precede `x`. Then `q_0 ≥ q_1 ≥ q_2 ≥ …`.

*Proof.* Take an extension `L` with `x` at position `j+2`, and let `u` be its predecessor. `u ∥ x`: it is not below `x`, since `x` is minimal, and not above `x`, since it comes earlier. Swap `u` and `x`. The result is a linear extension, because every element below `u` still precedes `u`, and nothing is below `x`. The map is injective, since its inverse swaps `x` with its successor. So `#{f(x)=j+2} ≤ #{f(x)=j+1}`. □

**The prefix before a minimal element.** Let `Z = Inc(x)`. Then `Z` is an ideal: if `z ∈ Z` and `w < z`, then `w ∉ ↑x` (else `x < w < z`) and `w ≠ x`. The set `J` of elements before `x` is an ideal of `P` that avoids `↑x ∪ {x}`, so `J` is an ideal of `Z`, and `|J| = f(x) − 1`. For `a ∈ Z`, `{x before a} = {a ∉ J}`.

**Linial's argument (width 2).** Let `P` be covered by chains `A, B` and not be a chain. An element below everything is first in every extension, and deleting it changes no pair probability. Delete such elements until there are exactly 2 minimal elements `x ∈ A`, `y ∈ B` (width 2 allows at most 2). Then `Inc(x) ⊆ B` is a chain `y = c_1 < c_2 < … < c_m`. So `J = {c_1..c_{|J|}}` and `P[x before c_{j+1}] = S_j := q_0 + … + q_j`.

Choose `x` to be the one of the two with `P[first] ≤ 1/2`, i.e. `q_0 ≤ 1/2`.
- If `q_0 ≥ 1/3`, the pair `(x, c_1)` is balanced.
- Otherwise the `S_j` climb from `q_0 < 1/3` to 1 in steps `q_j ≤ q_0 < 1/3` (Lemma 1.1). So the first `S_{j*} ≥ 1/3` is `< 2/3`, and `(x, c_{j*+1})` is balanced. □

**What is used:**

| fact | where | global width-2 content |
|---|---|---|
| (L1) Lemma 1.1 | the step bound `q_j ≤ q_0` | none (every poset) |
| (L2) prefix before `x` determined by size | `{x before c_{j+1}} = {|J| ≤ j}` | only "`Inc(x)` is a chain", and only its first `j*+1` elements |
| (L3) `q_0 ≤ 2/3` for the chosen `x` | start of the ladder | "exactly 2 minimal elements" (any `≥ 2` gives some `x` with `q_0 ≤ 1/2`) |

The top of `P`, the rest of chain `A`, and every element of `B` beyond `c_{j*+1}` play no role.

---

## 2. The local version

### 2.1 The theorem

**Theorem 2.1 (Local Linial, PROVEN).** Let `x` be minimal in a finite poset `P`, with `q_0 = P[x first] ≤ 2/3`. Let `C = (c_1 < … < c_k)` be the chain bottom of `Z = Inc(x)` (`k ≥ 1`). Suppose `S_{k−1} = P[f(x) ≤ k] ≥ 1/3`. Then some `(x, c_j)` with `1 ≤ j ≤ k` is balanced. Precisely, `j = j* + 1` with `j* = min{j : S_j ≥ 1/3}`.

*Proof.* For `j ≤ k`, the only ideal of `Z` of size `j` is `C_j = {c_1..c_j}`. This holds by induction, since any nonempty ideal of `Z ∖ C_{j−1}` contains its unique minimal element `c_j`. So for `j ≤ k − 1`:
- if `|J| ≤ j`, then `J = C_{|J|} ∌ c_{j+1}`;
- if `|J| ≥ j+1`, then `J` contains an ideal of size `j+1`, namely `C_{j+1} ∋ c_{j+1}`.

Hence `P[x before c_{j+1}] = S_j`, and `c_{j+1} ∈ Z` is incomparable to `x`.
- If `q_0 ∈ [1/3, 2/3]`, then `(x, c_1)` is balanced.
- Otherwise `q_0 < 1/3`, so `j* ≥ 1`, `j* ≤ k − 1` by hypothesis, and `S_{j*} = S_{j*−1} + q_{j*} < 1/3 + q_0 < 2/3` by Lemma 1.1. □

### 2.2 Structural sufficient conditions

**Corollary 2.2 (PROVEN).** `S_{k−1} ≥ k/(m+1)`, where `m = |Z| = π(x)`. So `3k ≥ π(x) + 1` implies the hypothesis `S_{k−1} ≥ 1/3`.

*Proof.* `|J| ≤ m`, so `q_0 ≥ … ≥ q_m` are `m+1` non-increasing numbers summing to 1. The largest `k` of them sum to at least `k/(m+1)`. □

**Corollary 2.3 (PROVEN; "structural LL").** Suppose `P` has exactly 2 minimal elements, and each satisfies `3k ≥ π + 1`. Then `P` has a balanced pair at its bottom. The same holds if `P` has exactly 2 minimal elements `x, y` with `|Inc(y)| ≤ 2` and `x` satisfying `3k ≥ π(x) + 1`. In that case `P[y first] ≥ 1/(|Inc(y)|+1) ≥ 1/3` (the largest of `|Inc(y)|+1` non-increasing terms), so `P[x first] ≤ 2/3`.

*Proof.* With 2 minimal elements, one has `P[first] ≤ 1/2`. Apply Thm 2.1 with Cor 2.2. □

**Corollary 2.4 (Linial 1984; recovered).** Every width-2 non-chain has a balanced pair. (§1.)

### 2.3 Under bounded range: the certificate form

**Proposition 2.5 (PROVEN).** Let `P ∈ Π_D`, let `Q` be an ideal of `P` with `|Q| ≥ max(3D, 2D+1)`, let `x` be minimal in `Q`, and put `m = |Inc_Q(x)|`. Then:
- (a) `x` is minimal in `P`, and `Inc_P(x) = Inc_Q(x)`. In particular the chain bottom `C` is computed inside `Q`.
- (b) For `s = m + 1`, every ideal `J` of `P` of size `s` contains `x`. For every `t ≤ s`, `P_P[f(x) ≤ t] = Σ_J w_J P_J[f(x) ≤ t]`, with the weights `w_J = e(J)e(P∖J)/e(P)` of mg-6b81's Lemma 2.3. By mg-6b81's Lemma 2.2 these `J` are exactly the size-`s` ideals of `Q`, since `s + D ≤ 2D + 1 ≤ |Q|`.
- (c) Hence, if every size-`s` ideal `J` of `Q` satisfies the two linear inequalities `P_J[x first] ≤ 2/3` and `P_J[f(x) ≤ k] ≥ 1/3`, then **every** `P ∈ Π_D` having `Q` as an ideal has a balanced pair among `(x, c_1), …, (x, c_k)`.

*Proof.*
- (a) Take `L` to begin with a linear extension of `Q`. The ideal `{x}` lies within the first `1 + D` positions (mg-6b81 Lemma 2.2). An element `b ∉ Q` sits at a position `> |Q| ≥ 3D`, at distance `≥ 2D` from `x`, so it is comparable to `x` (mg-6b81 Lemma 2.1), and it is above `x` because it comes later. Likewise no `b ∉ Q` is minimal in `P`: `{b}` would have to lie within the first `D + 1 ≤ |Q|` positions.
- (b) An ideal avoiding `x` avoids `↑x`, so it lies in `Inc(x)` and has size `≤ m < s`. The mixture identity: `L ↔ (J, L|_J, L|_{P∖J})`, and `f_L(x) = f_{L|_J}(x)` because `J` is the first `s` positions and `x ∈ J`. This is the argument of mg-6b81's Lemma 2.3, applied to a position event instead of a pair event.
- (c) Both conditions are preserved by convex combination. Then apply Thm 2.1 in `P`. □

**Why this matters conceptually.** mg-6b81's Theorem 2.4 needs **one** pair balanced in **every** bottom ideal `J`. mg-e8b4's Lemma 4 relaxes this to a Gordan combination over a set of pairs, found by LP. Prop 2.5 is a *structural* joint certificate for the pair set `{(x, c_j)}`. It needs no LP, and the crossing index may differ from `J` to `J`. The mixture still certifies `P`, because Lemma 1.1 holds in `P` itself. So Linial's proof **is** already a local argument: it never needs the pair to be identified in advance. I did not implement Prop 2.5 inside the mg-e8b4 tree, so I do not know how many nodes it would close there (NOT DONE).

### 2.4 F1/F2 bookkeeping

Everything Thm 2.1 touches lies in `{x} ∪ Inc(x)`, which has `≤ D + 1` elements (range). The crossing index satisfies `j* ≤ k − 1 < m ≤ D`. So the Linial pair lies in the ideal `{x} ∪ Inc(x)`, which has `≤ D + 1` elements. In every extension, `x` is within the first `D + 1` positions (mg-6b81 Lemma 2.2), and its partner is within `2D − 1` positions of `x` (F2).

### 2.5 No margin

Thm 2.1 gives no margin above 1/3. `S_{j*}` can sit at exactly 1/3: in `2+1` (`3 0 0 2`), `q_0(x) = 1/3`. This is consistent with the exceptional list `{2+1}` (mg-6b81). Any margin must come from the size of the steps `q_{j*}` relative to `S_{j*−1}`, and Lemma 1.1 alone does not bound that below.

### 2.6 Why near-extremal posets are width 2 with the balance at an end pair

**Remark 2.6 (PROVEN).** Let `y` be minimal with `Inc(y) = {x}`. Then `x` is minimal too: `w < x` would force `w > y`, which is impossible since `x ∥ y`. And `P[x before y] = P[x first] = P[f(y) = 2] = E f(y) − 1 = h(y) − 1`.

So if `y = v_1` in h-order, the pair `(y, x)` has `min(p, 1−p) = d_1` whenever `d_1 ≤ 1/2`. This is Thm 2.1 at `j* = 0`, with `x` the poorer minimal element and `c_1 = y`. The value identity is not new: it is the special case `W = {w}` of `δ(v_1, w) = d_1` in `docs/KSBFT-A-range-probe.md` §6, which is mg-2912's pattern "δ attained at an END pair, δ = M = d_1, the extreme element has exactly one incomparable". That `x = v_2`, i.e. the pair is `(v_1, v_2)`, is **not** implied (`y < a < b < c` plus an isolated `x` has h-order `y, a, x, …`; audit mg-3345 `out_remark26.txt`). It holds on all 44 δ < 0.35 records (EMPIRICAL, audit `out_rec44.txt`).

**EMPIRICAL (`out_records.txt`).** mg-2912 kept 2 534 distinct records with `n ≥ 3` (exhaustive extremes and annealing witnesses, `n` up to 24), deduplicated here by down-mask list. 44 of them have δ < 0.35. For every one of the 44:
- Thm 2.1 fires at one end (the bottom for 41, the top for 3);
- the crossing is at `j* = 0`;
- the Linial pair attains δ.

Over all 2 534 records, Thm 2.1 fires at some end for every width-2 record (528 of 528). That is forced only for width-2 posets with `≥ 2` minimal or `≥ 2` maximal elements: LL is applied to `P`, not to its components, and on the width-2 diamond it fires at neither end. For width 3 it fires on 661 of 940, for width 4 on 410 of 662, and for widths 10 and 11 on 0 of 10.

Reading: small δ occurs exactly when the ladder stops at its first rung with `P[x first]` just above 1/3. The width-2 shape is what makes the first rung a single pair.

---

## 3. The obstruction

### 3.1 Necessary structure of a counterexample

**Theorem 3.1 (PROVEN).** Let `P` be finite, not a chain, with no balanced pair. Pass to a component of `G(P)` that is not a single point, so `P` is indecomposable and `n ≥ 2`; an indecomposable `P` has `≥ 2` minimal elements. Then for **every** minimal `x` with `P[x first] ≤ 2/3`, and there is at least one:
- (i) `S_{k−1} < 1/3`, where `k` is the chain-bottom length of `Inc(x)`;
- (ii) `3k < π(x) + 1`;
- (iii) `Inc(x) ≠ C`, and `U = min(Inc(x) ∖ C)` has `≥ 2` elements. Each `u ∈ U` is above all of `C`, and `{x} ∪ U` is an antichain.

The dual statements hold at the top. If `P` has exactly two minimal elements, the poorer one carries a Y-gadget (`k ≥ 1`, `c_1 = y`). If it has `≥ 3`, then `k = 0`.

*Proof.* (i) is the contrapositive of Thm 2.1, and (ii) is the contrapositive of Cor 2.2. For (iii): if `Inc(x) = C` then `k = m` and `3m ≥ m + 1`, contradicting (ii). So `Inc(x) ∖ C ≠ ∅`, and it has `≥ 2` minimal elements, since one would extend `C`.

Let `u ∈ U`. It is above `c_k`. Otherwise `u` is minimal in `Inc(x) ∖ C_i` for the largest `i < k` with `u > c_i` (or `i = 0`), which contradicts `c_{i+1}` being the unique minimal element there. So `u > c_k > … > c_1`.

For the last two sentences: `y` is minimal and `≠ x`, so `y ∈ Inc(x)`. If there are exactly two minimal elements, `y` is the unique minimal element of `Inc(x)`, since `Inc(x)` is an ideal whose minimal elements are minimal in `P`; so `c_1 = y`. If there are `≥ 3`, `Inc(x)` has `≥ 2` minimal elements. □

**Consequence under range `≤ D`.** In a counterexample, both ends contain a 3-antichain `{x, u, v}` with `u, v` of rank `≤ k + 1 < (D+4)/3` in `Inc(x)`. The Linial ladder runs `k < (D+1)/3` rungs and then branches before reaching 1/3.

### 3.2 What survives at the branch

**Lemma 3.2 (PROVEN, any finite poset with `≥ 2` minimal elements).** For a minimal `x` with `q_0 ≤ 1/2` there is `j` with `P[f(x) ≤ j+1] ∈ [1/3, 2/3]`.

*Proof.* The argument of Thm 2.1 without (L2). □

So a balanced **event** always exists at the bottom. Linial's structure is exactly what makes it a **pair** event. At the branch, with `U = min(Inc(x) ∖ C)`, `∩_{u ∈ U} {x before u} = {|J| ≤ k} = {f(x) ≤ k+1}`, which is strictly smaller than each pair event. For `j > k` the threshold event `{f(x) ≤ j+1}` contains this intersection (strictly, unless `q_{k+1} = … = q_j = 0`) and is not itself an intersection of pair events `{x before u}`, `u ∈ U`. *(Erratum, mg-3345: an earlier version stated the inclusion the other way round for `j > k`; that is false, e.g. on the Y-gadget plus an isolated `x`.)*

**Lemma 3.3 (PROVEN).** At a branch with `U = {u, v}` exactly:
- `P[x before u] ≥ S_k` and `P[x before v] ≥ S_k`;
- `P[x before u] + P[x before v] ≤ 1 + S_k`.

*Proof.* The first line holds because `|J| ≤ k` means `J ⊆ C`. For the second, every ideal of `Inc(x)` of size `≥ k + 1` contains `C` and a minimal element of `Inc(x) ∖ C`. So `P[u ∈ J] + P[v ∈ J] ≥ P[|J| ≥ k+1] = 1 − S_k`. □

These are the only constraints the ladder gives, and they allow both pairs to exceed 2/3. **Witness `6 0 0 2 2 3 f`** (exact, `out_witnesses.txt`):
- `x = 0`, `C = (1)`, `U = {2, 3}`;
- `S_0 = 4/13`, `S_1 = 8/13`;
- `P[0<2] = P[0<3] = 19/26 > 2/3`.

The balance moves to `(u, v) = (2, 3)` at 1/2, by the automorphism swapping them. Without that symmetry it need not be there (§3.4).

### 3.3 The smallest double failure

`5 0 0 2 2 b`: Thm 2.1 fails at both ends. At the bottom, `x = 0` has `k = 1 < (3+1)/3` and `S_0 = 3/11`. At the top, the poorer maximal element has `k = 1`, `m = 3`, and `S_0 = 3/11`. The balanced pairs are `(0,3)` at `7/11` and `(2,3)` at `4/11`. Both still touch the gadget.

### 3.4 No balanced pair inside either end window: the range-5 witness

`P_9 = 9 0 0 2 2 3 b 2b 2f 7f` (hex strict down-masks). It has range 5, width 3, and `e = 197`, and it is self-dual (isomorphic to its dual; checked by brute force over `9!` relabellings). Covers: `1<2, 1<3, 0<4, 1<4, 0<5, 3<5, 5<6, 2<7, 5<7, 2<8, 4<8, 6<8`.

- Bottom Y-gadget: `x = 0 ∥ {1, 2, 3}`, `1 < 2`, `1 < 3`, `2 ∥ 3`. `P[0 first] = 62/197 ≈ 0.315 < 1/3`. The ladder crosses at `j = 1` (`S_1 = 124/197`). The two pair events it is the intersection of are both unbalanced: `P[0<2] = 161/197` and `P[0<3] = 138/197`. Also `P[2<3] = 59/197`.
- Top: the mirror image.
- **Every balanced pair:** `(2,4)` at 130/197, `(2,5)` at 118/197, `(4,5)` at 79/197. None of them lies inside `{x} ∪ Inc(x)` for an extreme element `x` at either end (WIN fails), so none lies in `{x} ∪ C ∪ U` either (BR fails). They are not "in the middle": the end windows `{0,1,2,3}` and `{4,6,7,8}` together with `5` are all of `P_9`, and every balanced pair touches an end window. They **straddle the two gadgets**: `(2,4)` joins the bottom gadget's `u = 2` to the top gadget's `u = 4`, `(2,5)` touches the bottom window, `(4,5)` the top.

It is a proven instance: the numbers are exact, and `show.py` reproduces them. So **the proposition "the bottom end contains a balanced pair directly, or has local width-2 structure to which Linial applies" is FALSE** whenever "bottom end" means the local configuration at a minimal element: `{x} ∪ Inc(x)`, of size `≤ D + 1`, even at both ends together. By the census, the first failures occur at range 5: 1 poset at `n = 9`, 4 at `n = 10`, and **none at `n = 11`**. At range ≤ 6, WIN fails at both ends in 2 posets at `n = 9` and 18 at `n = 10` (BR, the narrower window, fails in 4 and 29). None occurs at range ≤ 4 for `n ≤ 12`, or at range ≤ 3 for `n ≤ 13`. So these witnesses are short posets, with a gadget at each end and a small middle. The census does not show whether the phenomenon persists as `n → ∞` at fixed D; the range-5 count going to 0 at `n = 11` suggests it may not. That question is open (§5). The same gadget closed at `n = 11` is mg-2912's range-6 `min δ` record (`11 0 0 2 2 3 b 2b 2f af bf 1ff`, δ = 134/375). Its balanced pairs are `(2,5), (4,5), (4,7), (6,7)`; `(4,5)` and `(4,7)` touch no end window, so this record, not `P_9`, is the genuinely interior example. WIN and BR fail at both ends of it as well (checked with `probe.window_tests`). So at range 6 the phenomenon reaches at least `n = 11`, which is the range-≤6 census limit of mg-2912 (that limit is not re-checked by audit mg-3345).

### 3.5 Local 3-antichains do not give balance by themselves

The ticket asks whether "a local antichain of size 3 gives balance by a known argument". I know of none: no result in the literature I am aware of derives balance from a 3-antichain. The natural candidate is refuted:

- **FALSE:** "`≥ 3` minimal elements ⇒ some pair of minimal elements is balanced." Exact witness `8 0 0 0 4 4 6 16 2f` (range 6, no element comparable to nothing). Its minimal elements are `0, 1, 2`, with `P[0<1] = 9/28` and the other two pairs outside `[1/3, 2/3]` as well. Counts (`out_min3.txt`): 8 / 155 / 2 622 counterexamples at `n = 7 / 8 / 9` (indecomposable posets with `≥ 3` minimal elements; `min3.py` skips disconnected `G(P)`). They have range `≥ 6`. Most, but not all, have an element comparable to nothing: 142 of 155 at `n = 8`, 1 762 of 2 622 at `n = 9`.
- **EMPIRICAL:** at range `≤ 5` it holds on the whole census (D=3 `n ≤ 13`, D=4 `n ≤ 12`, D=5 `n ≤ 11`; last column of §4). I do not conjecture it for all `n` at `D ≤ 5`: the census reaches only `n ≈ 2D`.

---

## 4. Census (EMPIRICAL)

`probe.py` runs over every indecomposable poset of the population. "LL fires" means some minimal (resp. maximal, dually) `x` meets Thm 2.1's quantitative hypotheses. "Structural LL" is Cor 2.3's first condition at either end. BR, WIN and the minimal-pair test are as in §3. Table from `summary.py` (`out_summary.txt`):

Row names: `pN` = every poset on N elements; `dD_N` = range ≤ D on N elements.

| population | indecomposable | LL fires, either end | LL fires, bottom | structural LL (Cor 2.3), either end | BR fails, both ends | ... of which no isolated element | WIN fails, both ends | >=3 minimal, no balanced minimal pair |
|---|---|---|---|---|---|---|---|---|
| p3 | 2 | 1 (50.0%) | 1 (50.0%) | 1 (50.0%) | 0 | 0 | 0 | 0 |
| p4 | 7 | 3 (42.9%) | 3 (42.9%) | 3 (42.9%) | 0 | 0 | 0 | 0 |
| p5 | 31 | 17 (54.8%) | 12 (38.7%) | 13 (41.9%) | 0 | 0 | 0 | 0 |
| p6 | 184 | 99 (53.8%) | 61 (33.2%) | 74 (40.2%) | 0 | 0 | 0 | 0 |
| p7 | 1351 | 614 (45.4%) | 366 (27.1%) | 451 (33.4%) | 3 | 0 | 0 | 8 |
| p8 | 12524 | 4986 (39.8%) | 2870 (22.9%) | 3309 (26.4%) | 14 | 0 | 0 | 155 |
| p9 | 146468 | 50167 (34.3%) | 28127 (19.2%) | 29439 (20.1%) | 224 | 18 | 2 | 2622 |
| d3_9 | 289 | 249 (86.2%) | 183 (63.3%) | 249 (86.2%) | 0 | 0 | 0 | 0 |
| d3_10 | 643 | 558 (86.8%) | 409 (63.6%) | 558 (86.8%) | 0 | 0 | 0 | 0 |
| d3_11 | 1404 | 1223 (87.1%) | 898 (64.0%) | 1223 (87.1%) | 0 | 0 | 0 | 0 |
| d3_12 | 3076 | 2679 (87.1%) | 1970 (64.0%) | 2679 (87.1%) | 0 | 0 | 0 | 0 |
| d3_13 | 6736 | 5861 (87.0%) | 4310 (64.0%) | 5861 (87.0%) | 0 | 0 | 0 | 0 |
| d4_9 | 4327 | 3241 (74.9%) | 2154 (49.8%) | 3053 (70.6%) | 0 | 0 | 0 | 0 |
| d4_10 | 14719 | 10798 (73.4%) | 7158 (48.6%) | 10199 (69.3%) | 0 | 0 | 0 | 0 |
| d4_11 | 50910 | 37117 (72.9%) | 24492 (48.1%) | 34636 (68.0%) | 0 | 0 | 0 | 0 |
| d4_12 | 176766 | 129228 (73.1%) | 85061 (48.1%) | 120342 (68.1%) | 0 | 0 | 0 | 0 |
| d5_9 | 25540 | 15638 (61.2%) | 9665 (37.8%) | 13353 (52.3%) | 1 | 1 | 1 | 0 |
| d5_10 | 116925 | 73626 (63.0%) | 45510 (38.9%) | 63451 (54.3%) | 4 | 4 | 4 | 0 |
| d5_11 | 535167 | 339323 (63.4%) | 210479 (39.3%) | 295694 (55.3%) | 0 | 0 | 0 | 0 |
| d6_9 | 77537 | 37190 (48.0%) | 21596 (27.9%) | 25682 (33.1%) | 4 | 4 | 2 | 46 |
| d6_10 | 524253 | 258151 (49.2%) | 151086 (28.8%) | 185104 (35.3%) | 29 | 29 | 18 | 227 |

Checks (`summary.py` exits 1 otherwise):
- **Thm 2.1 violations: 0. Lemma 1.1 violations: 0. Posets with no balanced pair: 0.** This covers every population above.
- **Firing controls (`out_negctrl.txt`):**
  - With "balanced" narrowed to `[0.34, 0.66]` in Thm 2.1's conclusion, the check fires, starting with `2+1` at `n = 3` (1, 4, 16, 46 violations at `n = 3, 5, 6, 7`).
  - Lemma 1.1's test applied to non-minimal elements fires (1 and 30 at `n = 3, 5`).

  So both zero counts come from instruments that can fail.

Readings:
- At fixed D the LL share is flat in `n`: 86–87% at D=3, 73–75% at D=4, 61–63% at D=5, 48–49% at D=6.
- It falls with D, and the share at the bottom alone is lower: 64%, 48%, 39%, 28–29%.
- At D = 3, structural LL (Cor 2.3) equals quantitative LL on every row. At D ≥ 4 the quantitative form adds 4.1–14.9 points (4.1–5.0 at D = 4, 8.1–8.9 at D = 5, 13.9–14.9 at D = 6).
- The complement is O1 ∪ O2 (Thm 3.1). So at range 3, about 13% of indecomposable posets have a low 3-antichain at both ends.

---

## 5. What I did NOT do, and the candidates ruled out

**Ruled out (PROVEN by exact witness):**
- (i) balance within `{x} ∪ Inc(x)` of some extreme element (WIN), from range 5;
- (ii) the branch lemma BR, from range 5;
- (iii) "`≥ 3` minimal elements ⇒ balanced minimal pair", from range 6;
- (iv) "no balanced pair touching a minimal/maximal element ⇒ …" as a route: `6 0 0 2 2 3 f` has none, and its balanced pair is `(u, v)`;
- (v) Linial's ladder as a pair argument past the branch (Lemma 3.3 plus `6 0 0 2 2 3 f`).

**Not done:**
- Did not read Linial 1984 or Aigner's equality paper (§1 source note). Did not re-derive mg-2912's records; they were re-analysed by my own code.
- Did not implement Prop 2.5 inside mg-e8b4's tree, so it is not known whether it would shorten D = 8.
- Did not attempt a second-order ladder at the Y-gadget: pivoting on `u` or `v` conditional on `C` being placed. The obstacle is that `C` is not always a prefix, because `x` can precede it. That is the natural next attempt.
- No `n` beyond the table. No annealing.
- Did not settle whether the WIN/BR failures persist for long posets at fixed D. At range 5 they occur at `n = 9, 10` and not at `n = 11`. If they die out, "balance within `{x} ∪ Inc(x)` at some end, for `n ≥ n_0(D)`" becomes a live CONJECTURE, and it would be the precise local form of the ticket's proposition. A search for long witnesses (Y-gadget at both ends plus a long width-2 middle) is the probe to run; I did not run it.

**CONJECTURED (for a successor).** What a proof must handle beyond Linial is the *inward transfer* of balance across a Y-gadget. On the δ side this is reminiscent of mg-6b81's measured covariance decay (≈ 1/φ² per G-step). Nothing here proves a connection.
