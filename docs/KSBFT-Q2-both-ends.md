# KSBFT-Q2: the ends of a counterexample, second order. The ladder DOES run past the Y-gadget, pivoting on the gadget's twins instead of on x. It is Zaguia's good-pair ladder made local (Swap Ladder Thm 1.4, PROVEN). It certifies every balanced pair of every witness, and fires on all 146 468 indecomposable 9-element posets and all 2 534 mg-2912 records (EMPIRICAL). The two ends do NOT interact once n ≥ 8D−1 (PROVEN), and P_9's "straddling" balance is a one-end phenomenon (exact ablation). No contradiction is reached: the precise gap is an (L3)-type input for the Swap Ladder (mg-ce69)

Instrument: `code/ksbft_q2_both_ends_ce69/` (Python, exact integers/Fractions). `sh code/ksbft_q2_both_ends_ce69/run_all.sh` regenerates every transcript, takes about 2.5 min wall at 3 processes, and exits 1 on a failed check or a control that did not fire. Census files come from mg-eedd's generator (`pcert onept gen`), with OEIS A000112 as its control (`out_gen.txt`).

Built on mg-5f14 (`docs/KSBFT-Q-local-width2.md`, "Q" below), **read through its audit mg-3345** (`docs/AUDIT-mg-3345.md`). Nothing here uses the claims that audit breaks:
- the §3.2 inclusion is not used;
- the threshold event past the branch is used only through the corrected identity `∩_{u∈U}{x<u} = {f(x) ≤ k+1}`;
- "touching" is not used.

Thm 3.1 of Q is used with the audit's added hypotheses: not a chain, indecomposable.

Labels:
- **PROVEN**: the proof is in this file, or is cited and was re-derived here.
- **KNOWN**: the proof is in the literature and I re-derived it.
- **EMPIRICAL**: exact arithmetic over a stated finite population.
- **CONJECTURED**: a guess.

Computation was used only to probe candidate lemmas. No case search was extended. The two small census runs at range ≤ 3 and ≤ 4 (§4) re-use the populations of Q §4 and add no new `n`.

Conventions:
- `↑b`, `↓b` are the closed up-set and down-set; `up(b) = ↑b ∖ {b}`, `down(b) = ↓b ∖ {b}`; `Inc(x)` is the set of elements incomparable to `x`.
- A pair `(x, b)` is **nested** if `x ∥ b` and `down(x) ⊆ down(b)`. Every pair `(x, b)` with `x` minimal and `b ∈ Inc(x)` is nested.

---

## 0. Verdict

**Item 1: second-order ladder at the Y-gadget. YES, it runs, but on the twins, not on x.**

- (a) **The Y-gadget is O1 in disguise (Lemma 1.1, PROVEN, exact).** On the event `{x after c_k}`, every extension begins with exactly `c_1 … c_k`. So `P[x < b] = s + (1−s)·P_R[x < b]` for `b ∈ Inc(x) ∖ C`, where `R = P ∖ C`, `s = S_{k−1}`, and `min(R) = {x} ∪ U`. The branch reduces the O2 case to the O1 case (≥ 3 minimal elements) in `R`, with the balance window for x-pairs shifted to `[(1/3−s)/(1−s), (2/3−s)/(1−s)] ⊇ [1/3, 1/2]`.
- (b) **Past a branch, no threshold event of x's ladder is a pair event unless `Inc(x)` re-merges (Pinch Lemma 1.2, PROVEN).** `{f(x) ≤ t+1}` is a pair event `{x < w}` iff `Inc(x) = L ⊕ {w} ⊕ M` (ordinal sum) with `|L| = t`. So a second-order ladder pivoting on `x` needs a singleton ordinal summand of `Inc(x)` at the crossing, which is a strong structural extra fact.
- (c) **Pivot on the twins instead (Swap Ladder, Thm 1.4, PROVEN).** Let `x ∥ b` with `down(x) ⊆ down(b)`, and let `b = b_0 < b_1 < … < b_m` be the chain bottom of `↑b ∖ ↑x`. Then the steps `P[b_{i−1} < x < b_i]` are non-increasing. So if `P[x<b_0] ≤ 2/3` and `P[x<b_m] ≥ 1/3`, some `(x, b_i)` is balanced.
  - The full-chain case is **Zaguia's good-pair theorem** (KNOWN: Zaguia, *Order* 2019, arXiv 1610.00809, Thm 2; the step lemma is credited to his 2012 N-free paper).
  - What is new here is the chain-bottom / 2/3 form. It stands to Zaguia's theorem as Q's Local Linial stands to Linial's.
  - Linial's theorem and Q's Local Linial Thm 2.1 are the special case `x` minimal, `b_0 = c_1`.
- (d) **At the Y-gadget, `u` and `v` are down-twins** (`down(u) = down(v) = C`). The twin ladder `(u; v < b_1 < …)` in `↑v ∖ ↑u` is exactly the second-order ladder the ticket asked for.
  - **Exact extra fact needed:** `↑v ∖ ↑u` (or `↑u ∖ ↑v`) has a chain bottom reaching the crossing. It suffices that it is a chain (with `P[u<v] ≤ 2/3`), or that both private up-sets are chains (Zaguia's "very good pair").
  - When additionally `up(u) ⊆ up(v)`, the first two steps are **equal** (Doubling Lemma 1.5): `P[u < b_1] = 2·P[u < v]` exactly. This identity is visible in `P_9`, `B7`, the n=11 record and every `Q_m` (e.g. `P_9`: 59/197 → 118/197).

**Item 2: both ends. They do not contradict each other. In the long regime they do not even interact.**

- (e) **Separation (Prop 3.1, PROVEN).** For `P ∈ Π_D` with `n ≥ 8D−1`, every element of a bottom window `{x} ∪ Inc(x)` lies below every element of a top window. The straddling pairs that carry `P_9`'s balance cannot exist.
- (f) **Decoupling (Prop 3.2, PROVEN, Birkhoff–Hopf).** Bottom pair laws depend on the part of `P` above level `t` only through a positive vector. Its Hilbert-metric influence contracts by `τ_D = (D!−1)/(D!+1)` every `D` levels. The constant is useless numerically, but the statement is exact.
- (g) **P_9's mechanism is not an interaction (§3.3, exact ablation).**
  - The whole balanced triangle `{2,4,5}` of `P_9` already lives in its first 7 elements `B7 = 7 0 0 2 2 3 b 2b`. It survives when the top is replaced by a long gadget-free tail.
  - Each of its pairs is a Swap-Ladder rung anchored at the **bottom** gadget: `(2,5)` is rung 1 of the twin ladder `(2; 3<5<6)`, and `(4,5)`, `(2,4)` are rung 0 of nested ladders.
  - `P_9` (n = 9 < 8·5−1) is two one-end configurations overlapping. Its "top gadget" `{4,6,7,8}` is built from the bottom configuration's own depth-2 elements.
  - The only genuinely two-sided effect is that `(2,4)` is balanced because `up(4)` is small. In the long family it becomes 0.6707.
- (h) **The long both-ends witnesses `Q_m` (EMPIRICAL, exact per member).** `Q_m` is `P_9` plus a zigzag tail of m elements, with its dual glued on top.
  - It is indecomposable, of range 5, with `n = 18, 22, 26, 30, 38, 46`, and WIN fails at **both** ends. The window margin is frozen at +0.0197.
  - The one-ended version keeps WIN failing up to n = 69 (margin +0.019686 at m = 30, 45, 60).
  - This refutes, on every tested length, Q §5's live candidate "WIN at some end for `n ≥ n_0(D)`" at D = 5.
  - All balanced pairs of `Q_m` sit at depth ≤ 8 from an end, **just outside** `{x} ∪ Inc(x)`; the long middle has none.
  - In the long regime, "both ends" is "one end, twice". The object that carries balance is the bottom ideal of size about 2D (the Swap-Ladder rungs), not the window of size D+1.

**Item 3: the 3-antichain.**

- (i) **Dominance (Lemma 2.1, PROVEN).** With no balanced pair, "a before b with probability > 2/3" is a **linear order** on every antichain, because a cyclic triangle would need a cyclic sum > 2.
- (j) **At three minimal elements `m_1 ⇒ m_2 ⇒ m_3`**, (L1) and the union bound force two things:
  - `P[m_3 first] < 1/3`;
  - `P[m_1 first] > 1 − (r−1)/3`, where `r = |min P|`.
- (k) **Shepp's XYZ inequality** (KNOWN, sanity-checked with 0 violations on n ≤ 7) sharpens Q's Lemma 3.3 at the gadget. It gives the **gadget dichotomy** (Prop 2.3, PROVEN):
  - (G1) `x` beats both `u` and `v` (> 2/3 each), and then `4/9 < P[x<u]P[x<v] ≤ S_k < 2/3`, so the crossing is exactly at the branch;
  - or (G2) some `u` beats `x`, and then the crossing is strictly past the branch.

  `P_9`, B7, rec11 and `Q_m` are all G1.
- (l) All minimal elements are pairwise down-twins. So the Swap Ladder applies to every ordered pair of them. For a dominance-adjacent `a ⇒ b`, the private up-set `↑a ∖ ↑b` must branch below its crossing.
- (m) No known 3-element argument gives a balanced pair locally. Kahn–Saks and BFT compare heights globally and give 3/11 and 0.276, not 1/3 (recalled, not re-read). `W8 = 8 0 0 0 4 4 6 16 2f` (Q §3.5) still stands against the naive form. Its balanced pairs are all Swap-Ladder rungs, but none of them involves two minimal elements.

**The aimed proposition (Thm 4.1, PROVEN).** No balanced pair implies the following explicit structure, at both ends and everywhere:
- every nested ladder with `P[x<b_0] ≤ 2/3` branches before reaching 1/3;
- no incomparable pair carries opposite full-chain ladders;
- every Y-gadget is G1 or G2, and its twin ladder against the dominance branches;
- under range ≤ D, every ladder lives in a window of ≤ D + 1 elements.

**No contradiction is reached.** The obstruction is exact and small:
- The structural corollary (Cor 1.6, which needs no probabilities) fails on 5 of 12 524 indecomposable posets at n = 8 and on 138 of 146 468 at n = 9 (range 4: 1 at n = 8; range 5–8 otherwise). One of them, `8 0 0 2 2 3 b 1b 2f`, is itself a Y-gadget. It fails on none at range ≤ 3 (n ≤ 12) or range ≤ 4 (n = 9–11).
- The quantitative Swap Ladder covers every one of these. What it needs there is an (L3)-type probabilistic input: some nested ladder whose chain bottom reaches 1/3 has first rung ≤ 2/3.
- **CONJECTURED (SL-conjecture):** every finite non-chain poset has such a ladder. It implies 1/3–2/3.
- EMPIRICAL support: all 160 567 indecomposable posets with 3 ≤ n ≤ 9, and all 2 534 records up to n = 24. Zaguia's good-pair form fails on 5 / 114 / 21 of these, so the chain-bottom extension is load-bearing.

**Answer to pm-onethird on KSBFT-R (mg-7bfc, unaudited).** This ticket supplies the **transfer** half of R's missing lemma but not the **existence** half.
- Prop 3.2's decoupling: a pair within depth `O(D)` of the bottom has the same law, up to `Δ_D τ_D^{⌊(t−3D)/D⌋−1}`, in `P` and in every truncation whose cut is at level `≥ t`.
- So a robust balanced pair of a truncation, lying far from its cut, near the bottom, **is** a balanced pair of `P`.
- What is missing is that such a pair exists. The `Q_m` family shows it is where the balance of these long examples actually lives (depth ≤ 8, never at the far cut). But Q_m has range 5, and a minimal counterexample has range ≥ 8 (mg-9268 HOLDS, per pm).
- R's Prop 3.1 (chain modules only) excludes twins with equal up-sets, i.e. the equality case of Zaguia's critical pairs. So in a least counterexample every Y-gadget's twins have `up(u) ≠ up(v)` (§4). It does not otherwise touch Thm 4.1.

---

## 1. Item 1: the second-order ladder

Setting (Q Thm 3.1, O2):
- `x` is minimal with `q_0 = P[x first] ≤ 2/3`;
- `Z = Inc(x)`, with chain bottom `C = (c_1 < … < c_k)`, `k ≥ 1`;
- `U = min(Z ∖ C)`, `|U| ≥ 2`;
- `J` is the set of elements before `x`, an ideal of `Z`;
- `S_j = P[|J| ≤ j]`.

### 1.1 The gadget is O1 in the residual

**Lemma 1.1 (C-prefix decomposition, PROVEN).** In the setting above:
1. On the event `E = {f(x) > k}` (i.e. `x` after `c_k`), every linear extension begins with exactly `c_1, …, c_k` in that order. Hence `#E = e(R)`, where `R = P ∖ C`.
2. For `i < k`: `#{|J| = i} = e(P ∖ (C_i ∪ {x}))`, where `C_i = {c_1..c_i}`. On that event the extension begins `c_1 … c_i, x`.
3. `min(R) = {x} ∪ U`.
4. For every incomparable pair `a, b` of `R`:
   `#_P{a<b} = #_R{a<b} + Σ_{i<k} #_{P∖(C_i∪x)}{a<b}`.
   For a pair `(x, b)` the `i`-th summand is the full `e(P∖(C_i∪x))`, since `x` precedes all of `R ∖ x` there.
   In particular, for `b ∈ Z ∖ C`: `P[x<b] = s + (1−s)·P_R[x<b]`, with `s = S_{k−1}`.

*Proof.*
1. Let `f(x) > k` and let `w` precede `c_k`. Then `w ≠ x`, and `w` is not above `x`, since everything above `x` comes after `x` and `x` comes after `c_k`. `w` is not below `x`, since `x` is minimal. So `w ∈ Z`. Every element of `Z ∖ C` lies above some `u ∈ U`, and `u > c_k` (Q Thm 3.1(iii)); so `w ∉ Z ∖ C`, hence `w ∈ C`. Conversely `C_k` precedes `c_k`. So the first `k` positions are `C`, and `C` is an ideal of `P`, since it is an ideal of the ideal `Z`. Prepending `C` to any extension of `R` gives an extension of `P` in `E`.
2. Given `|J| = i < k`, `J = C_i` (Q Thm 2.1's induction), so the extension begins `C_i, x`. The rest is any extension of `P ∖ (C_i ∪ x)`.
3. A minimal element of `R` is `x`, or lies in `Z ∖ C` and is then in `U`, or lies above `x` and so is not minimal.
4. Partition by `|J|`, using 1 and 2. □

`out_gadget.txt` checks 1–4 exactly on every gadget of every indecomposable poset with n ≤ 8: 11 330 gadgets, 0 mismatches. Both firing controls fire on 11 330 and 11 201 gadgets: `C_{k−1}` in place of `C` in (1), and the last summand dropped in (4).

**Reading.** Past the chain bottom, the Y-gadget is the O1 case of Q's Thm 3.1, in `R`. `x` together with `U` are ≥ 3 minimal elements, and the balance window for x-pairs is shifted and widened to `W_s = [(1/3−s)/(1−s), (2/3−s)/(1−s)]`. Its length is `1/(3(1−s)) > 1/3`, and it contains `[1/3, 1/2]` for every `s ∈ [0, 1/3)`. So items 1 and 3 of the ticket are **one question**: the O1 configuration. In `R`, pivoting on any minimal element branches immediately, whether `x`, `u` or `v`: each has ≥ 2 other minimal elements in its incomparable set.

### 1.2 Why x's ladder cannot continue

**Lemma 1.2 (Pinch Lemma, PROVEN).** Let `x` be minimal and `t ≥ 0`. The threshold event `{f(x) ≤ t+1} = {|J| ≤ t}` equals a pair event `{x < w}` for some `w ∈ Z` iff `Z = L ⊕ {w} ⊕ M` (ordinal sum: everything in `L` is below `w`, and `w` is below everything in `M`) with `|L| = t`.

*Proof.* `{x<w} = {w ∉ J}`. So the two events agree iff every ideal of `Z` of size `≥ t+1` contains `w`, and none of size `≤ t` does. Every ideal of size `≥ t+1` contains one of size `t+1`, and every ideal of size `≤ t` lies in one of size `t`. So the condition is: every size-`(t+1)` ideal contains `w`, and no size-`t` ideal does.

Let `I` be a size-`(t+1)` ideal. If `w` were not its unique maximal element, removing another maximal element would give a size-`t` ideal containing `w`. So `I = ↓_Z w`, which is unique. Every size-`t` ideal extends by a minimal element of its complement to `↓_Z w`, so it equals `L := ↓_Z w ∖ {w}`, which is unique. Hence the only minimal element of `Z ∖ L` is `w`, so `Z ∖ L ⊆ ↑w`.

Conversely, `Z = L ⊕ {w} ⊕ M` makes the ideals of sizes `t` and `t+1` unique, equal to `L` and `L ∪ {w}`. □

So Linial's ladder has a pair at every level (`Z` is a chain). Local Linial has one at levels `< k`. Past the branch, **x's own ladder yields a pair only at a singleton ordinal summand of `Inc(x)`**, i.e. if `Inc(x)` re-merges into a single element above the whole branch. This is the precise form of the audit's correction: at `j* = k` the threshold event is the intersection `∩_U{x<u}` (not a pair event). At `j* > k` it is a pair event iff there is a pinch at `j*`. `P_9`'s `Inc(0) = {1} ⊕ {2,3}` has its only pinch at level 0.

### 1.3 Release time and the swap ladder

**Lemma 1.3 (release-time monotonicity, PROVEN; generalizes Q's Lemma 1.1).** For any element `u`, let `ρ(u) = max_{w<u} f(w)` (0 if `u` is minimal). The law of `f(u) − ρ(u)` is non-increasing.

*Proof.* Condition on the first `ρ(u)` elements, i.e. on the sequence up to the release time. The rest is a uniform extension of the residual poset, in which `u` is minimal. Apply Q's Lemma 1.1 and mix. □

Checked by explicit enumeration on every element of every indecomposable poset with n ≤ 7 (10 750 elements, 0 violations). Its control, the same law measured from `min_{w<u} f(w)`, fires on 4 072 elements.

**Theorem 1.4 (Swap Ladder, PROVEN).** Let `x ∥ b` with `down(x) ⊆ down(b)` (H1). Let `b = b_0 < b_1 < … < b_m` be the chain bottom of `W = ↑b ∖ ↑x`: `b_{i+1}` is the unique minimal element of `W ∖ {b_0..b_i}`, and the construction stops when that element is not unique or does not exist. Put
- `t_0 = P[x < b_0]`;
- `t_i = P[b_{i−1} < x < b_i]` for `1 ≤ i ≤ m`;
- if `W = {b_0..b_m}` ("full"), also `t_{m+1} = P[b_m < x]`.

Then:
- (a) `t_0 ≥ t_1 ≥ … ≥ t_m` (and `≥ t_{m+1}` if full), and `P[x < b_i] = t_0 + … + t_i`;
- (b) every `b_i ∥ x`;
- (c) if `P[x < b_0] ≤ 2/3` and `P[x < b_m] ≥ 1/3`, then some `(x, b_i)` is balanced. The second hypothesis is automatic when `W` is full and `t_0 < 1/3`.

The dual statement, with `up(x) ⊆ up(b)` and the chain top of `↓b ∖ ↓x`, holds by reversing the order.

*Proof.*
- (b) `b_i ∉ ↑x`, and `b_i < x` would give `b ≤ b_i < x`.
- (a) For `1 ≤ i ≤ m+1`, map an extension in which `b_{i−1}` precedes `x` and `x` precedes `b_i` (for `i = m+1`, only the first condition) to the one obtained by swapping `x` with `b_{i−1}`. It is a linear extension:
  - `x` moves earlier, to `b_{i−1}`'s slot, and `down(x) ⊆ down(b) ⊆ down(b_{i−1})` all precede that slot.
  - `b_{i−1}` moves later, to `x`'s slot, and every element of `up(b_{i−1})` lies in `up(x)` (after `x`) or in `↑b_i` (after `b_i`, which follows `x`). For `i = m+1` and full `W`, `up(b_m) ⊆ up(x)`.
  - The image has `b_{i−2} < x < b_{i−1}` (for `i = 1`: `x < b_0`), because `b_{i−2} < b_{i−1}`.
  - The map is injective, since it is its own inverse on its image.
- (c) The sum identity holds because `{x<b_{i−1}} ⊆ {x<b_i}`.
  - If `t_0 ∈ [1/3, 2/3]`, then `(x, b_0)` is balanced.
  - If `t_0 < 1/3`, let `i*` be the first `i` with `P[x<b_i] ≥ 1/3`. It exists by hypothesis, and `P[x<b_{i*}] < 1/3 + t_{i*} ≤ 1/3 + t_0 < 2/3`.
  - When full, `P[x<b_m] = 1 − t_{m+1} ≥ 1 − t_0 > 2/3`. □

Special cases:
- **Linial (1984) and Q's Local Linial Thm 2.1:** `x` minimal, `b_0 = c_1`. Then H1 is `∅ ⊆ ·`, and `↑c_{i+1} ∖ ↑x ⊆ {c_{i+1}} ∪ ↑c_{i+2}` because `Z ∖ C_{i+1}` has unique minimal element `c_{i+2}`.
- **Zaguia's good pair (KNOWN):** full `W` and `P[x<b] ≤ 1/2` (arXiv 1610.00809, Def. 1 and Thm 2, with the step lemma credited to Zaguia, EJC 19(2) 2012). I found this after deriving Thm 1.4. The full-chain core is his, and the proof above is his proof.
- **What is added:**
  - the chain-bottom (local) form;
  - the threshold 2/3 in place of 1/2;
  - the "full ⇒ second hypothesis automatic" remark;
  - the placement of Linial, Local Linial and the Y-gadget twin ladder as instances of one theorem.

  Novelty beyond Zaguia 2012/2019 is UNCHECKED; I read only 1610.00809.

**Census (`out_swapladder_{1,2}.txt`, EMPIRICAL).** Every nested ordered pair, in `P` and its dual, of every indecomposable poset with 3 ≤ n ≤ 9 was checked: 160 567 posets and 6 362 370 ladders. There are 0 step violations of (a) and 0 conclusion violations of (c). Both controls fire:
- dropping H1 makes the steps increase on 1 406 503 + 1 651 227 ladders;
- narrowing the window to `[0.34, 0.66]` produces 83 923 + 81 949 violations (sharp at `2+1`).

**Lemma 1.5 (Doubling, PROVEN).** If, in Thm 1.4, `down(x) = down(b_0)` and `up(x) ⊆ up(b_0)`, then `t_1 = t_0`, i.e. `P[x < b_1] = 2·P[x < b_0]`. Moreover `P[x < b_0] ≤ 1/2`.

*Proof.* The swap of (a) at `i = 1` is invertible:
- starting from `x < b_0`, swapping moves `b_0` earlier, which is valid since `down(b_0) = down(x)`;
- it moves `x` later to `b_0`'s slot, which is valid since `up(x) ⊆ up(b_0)` lies after `b_0`;
- the image satisfies `b_0 < x < b_1`, since `b_1 > b_0`.

`P[x<b_0] ≤ 1/2` is Zaguia's Lemma 7 (critical pair `(b_0, x)`). □

### 1.4 The answer to item 1

At a Y-gadget, `u, v ∈ U` are **down-twins**: `down(u) = down(v) = C`. So Thm 1.4 applies to `(u; v, …)` with `W = ↑v ∖ ↑u`, and to `(v; u, …)` with `↑u ∖ ↑v`. Under range `≤ D`, `W ⊆ Inc(u)`, so `|W| ≤ D`. Every such ladder lives in a window of `≤ D+1` elements. That is the second-order ladder:
- **Pivot:** the dominance-weaker twin, i.e. the one with `P[pivot < other] < 1/3`. (In a counterexample one of `P[u<v]`, `P[v<u]` is `< 1/3`.)
- **Rungs:** the chain bottom of its partner's private up-set.
- **The exact extra fact needed:** that chain bottom reaches the crossing. Equivalently, the private up-set does not branch before 1/3. Sufficient conditions:
  - it is a chain (then the only requirement is `P[u<v] ≤ 2/3`);
  - both private up-sets are chains (Zaguia's very good pair, no probability needed);
  - `up(u) ⊆ up(v)` and `W ∖ {v}` has a unique minimum, and `P[u<v] ≥ 1/6` (Lemma 1.5: the second rung is `2P[u<v]`).

The ladder on `(x, u)`/`(x, v)` is also a Swap Ladder, with `x` minimal and `down(x) = ∅ ⊆ C`, and rungs in `↑u ∖ ↑x`. It is useful only in case G2 (§2), where `P[x<u] < 1/3`.

**Every balanced pair of every witness is a certified rung (`out_explain.txt`).** In `P_9`, `B7`, `rec11` and `Q_4`, the pair `(2,5)` is rung 1 of the twin ladder `(2; 3 < 5 < 6)`, with exactly doubled steps:

| witness | first rung `P[2<3]` | second rung `P[2<5]` |
|---|---|---|
| `P_9` | 59/197 | 118/197 |
| `B7` | 17/62 | 17/31 |
| `rec11` | 247/750 | 247/375 |
| `Q_4` | 809 911/2 673 421 | 1 619 822/2 673 421 |

`(4,5)` is rung 0 of `(4; 5, …)`, since `down(4) = {0,1} ⊆ down(5) = {0,1,3}`. In `rec11`, `(4,7)` and `(6,7)` are rungs of `(4; 7 < 8)` and `(6; 7)`. In `W8` all five balanced pairs are rungs, for example `(0,3)` via the full ladder `(0; 3)`.

---

## 2. Item 3: the 3-antichain

**Lemma 2.1 (dominance, PROVEN).** Let `P` have no balanced pair and `A` be an antichain. Write `a ⇒ b` if `P[a<b] > 2/3`. Then `⇒` is a strict linear order on `A`.

*Proof.* Any two elements of `A` are comparable under `⇒`, since the pair is unbalanced. A cyclic triple `a ⇒ b ⇒ c ⇒ a` has cyclic sum `> 2`, but every linear order of `{a,b,c}` satisfies at most two of `a<b`, `b<c`, `c<a`. □

The cyclic-sum bound `[1,2]` was checked on 721 428 ordered 3-antichains (n ≤ 8), and its control (`≤ 3/2`) fires.

**What (L1) forces at `r ≥ 3` minimal elements `m_1 ⇒ … ⇒ m_r` (PROVEN):**
- `P[m_r first] ≤ P[m_r < m_1] < 1/3`;
- `P[m_1 first] ≥ 1 − Σ_{i≥2} P[m_i < m_1] > 1 − (r−1)/3`. For `r = 3` this is `> 1/3`, and then `P[m_1 < w] ≥ P[m_1 first] > 1/3` forces `P[m_1 < w] > 2/3` for every `w ∈ Inc(m_1)`: the dominant minimal element precedes each of its incomparables with probability `> 2/3`;
- minimal elements are pairwise down-twins, so Thm 1.4 applies to each ordered pair. For `a ⇒ b`, the ladder `(b; a, …)` has first rung `P[b<a] < 1/3`, so `↑a ∖ ↑b` must branch below its crossing. **What lies above the stronger element and not above the weaker one must branch early.**

**Shepp's XYZ inequality** (Shepp, *Ann. Probab.* 10 (1982); KNOWN, recalled, not re-read): `P[x<y, x<z] ≥ P[x<y]·P[x<z]`. It showed 0 violations on every 3-antichain with n ≤ 7 by explicit enumeration (`out_gadget.txt`, column X).

**Proposition 2.3 (gadget dichotomy, PROVEN).** At a Y-gadget with `U = {u, v}` in a poset with no balanced pair, exactly one of the following holds:
- **(G1)** `P[x<u], P[x<v] > 2/3`. Then `S_k = P[x<u, x<v] ≥ P[x<u]P[x<v] > 4/9`, so `j* = k` and `S_k ∈ (4/9, 2/3)`.
- **(G2)** some `P[x<u] < 1/3`. Then `S_k ≤ P[x<u] < 1/3`, so `j* > k`.

*Proof.* By the audit's corrected identity, `{x<u} ∩ {x<v} = {|J| ≤ k}`. For G1 apply XYZ; for `S_k < 2/3` use `q_k ≤ q_0 < 1/3`. □

`P_9` (161/197, 138/197, `S_1` = 124/197 ≥ 0.573), `B7`, `rec11` and `Q_m` are all G1. There the second-order balance comes from the twin ladder, not from `x`.

**Is there a known 3-element argument that applies locally?** Not one that yields a balanced pair.
- Kahn–Saks and Brightwell–Felsner–Trotter work with expected-height differences and global log-concavity. They give 3/11 and `(5−√5)/10`, not 1/3, and they do not localise at an end. (Recalled; BFT's cross-product analysis was not re-read.)
- XYZ and dominance are the local 3-element facts. They constrain but do not balance. `W8` (Q §3.5) has three minimal elements `2 ⇒ 1 ⇒ 0` with `P[1<2] = 65/196`, which is 1/3 − 1/588. Its balance sits on nested ladders one level up.

---

## 3. Item 2: both ends

### 3.1 Separation

**Proposition 3.1 (PROVEN).** Let `P ∈ Π_D` and `n ≥ 8D − 1`. Every element of a bottom window `{x} ∪ Inc(x)` (`x` minimal) is below every element of a top window.

*Proof.*
- `f(x) ≤ D + 1` in every extension (mg-6b81 Lemma 2.2, with `s = 1`).
- `z ∥ x` gives `|f(z) − f(x)| ≤ 2D − 1` (mg-6b81 Lemma 2.1). So bottom-window elements occupy positions `≤ 3D`, and dually top-window elements occupy positions `≥ n − 3D + 1`.
- The gap is `≥ n − 6D + 1 ≥ 2D`, so the elements are comparable (Lemma 2.1), and the bottom one is smaller. □

So `P_9`'s "straddling" pairs (n = 9 < 39) are a short-poset artefact. For n ≥ 8D−1 no pair joins the two gadgets.

### 3.2 Decoupling

**Proposition 3.2 (PROVEN).** Let `P ∈ Π_D` and `s ≥ 3D`. Every pair `(a,b)` inside a bottom window has
`P[a<b] = Σ_{J ∈ V_s} β_J · P_J[a<b]`, with `β_J ∝ e(J)·e(P∖J)` (mg-6b81 Lemma 2.3).

The vector `v_s = (e(P∖J))_{J∈V_s}` equals `T_{s+1} ⋯ T_t · v_t`, where `T_k` are the ideal transfer matrices (KSBFT-I §2). Grouped in blocks of `D` levels, each block is **strictly positive** with entries in `[1, D!]`:
- entry `(I, J')` is `e(J'∖I)`;
- every size-`k` ideal lies in every size-`(k+D)` ideal (mg-6b81 Lemma 2.2).

So by Birkhoff–Hopf each block contracts Hilbert's projective metric by `τ_D ≤ tanh(log(D!)/2) = (D!−1)/(D!+1)`. Two posets sharing an ideal of size `≥ t + D` therefore have bottom vectors within Hilbert distance `2 log(D!) · τ_D^{⌊(t−s)/D⌋ − 1}`, and hence bottom-window laws within `e^{that} − 1`.

*Proof.* Assembled from the cited lemmas and the Birkhoff–Hopf theorem. The diameter bound `Δ ≤ 2 log(D!)` is the entry-ratio bound. Nothing here depends on KSBFT-I's Lemma 6 (whose audit status I did not check). □

**Reading.** In the long regime, the constraints "no balanced pair near the bottom" and "no balanced pair near the top" live on disjoint pairs (Prop 3.1). They see each other only through an exponentially weak boundary vector (Prop 3.2). They cannot contradict each other unless one of them is already contradictory on its own. Self-duality doubles the constraints but adds no interaction.

### 3.3 P_9's mechanism

`ablate.py` keeps an initial ideal of `P_9` and replaces the rest with the zigzag tail. The tail has no gadget and no interior balanced pair (`P[i<i+1] → 0.72`). In the table, `*` marks a balanced value (`out_ablate.txt`):

| kept ideal | WIN at bottom | `P[2<4]` | `P[2<5]` | `P[4<5]` |
|---|---|---|---|---|
| first 5 | holds | 0.695 | — | — |
| first 6 | holds | 0.598* | 0.771 | 0.709 |
| **first 7 (= B7)** | **fails** | 0.584* | 0.590* | 0.497* |
| first 8, 9 (= P_9) | fails | 0.671 | 0.606* | 0.394* |

So the whole balanced triangle of `P_9` is present in the 7-element ideal `B7 = 7 0 0 2 2 3 b 2b`. That ideal is one bottom gadget `{0; 1 < 2, 3}` plus its depth-2 elements `4 > {0,1}`, `5 > {0,1,3}` and `6 > 5`, and the triangle survives any tail. `P_9`'s "top gadget" `{4, 6, 7, 8}` re-uses 4 and 6.

- **Mechanism:** the pairs are Swap-Ladder rungs anchored at the bottom gadget (§1.4). `(2,5)` is the twin ladder of `u=2`, `v=3`, with `2P[2<3]`.
- **The one two-sided effect:** `(2,4)` is balanced only while `up(4) ⊆ up(2)`, which makes `(2;4)` a full ladder. That inclusion needs the top to be close.

`rec11` behaves the same way. Its four balanced pairs survive truncation to 9 elements plus a tail (range 6), so its "interior" pairs are also within depth 9 of the bottom.

### 3.4 The long both-ends family

`Q_m` is `P_9` plus a zigzag tail of `m` elements, with its dual glued on top by a staircase seam (`bothends.py`, `witness.py`). Every member is **indecomposable, range 5**, with WIN failing at both ends:

| m | n | WIN_bot | WIN_top | window margin | balanced pairs |
|---|---|---|---|---|---|
| 0 | 18 | fails | fails | +0.0198 | (2,5),(4,5),(6,7) + mirror |
| 2, 4, 6, 10 | 22–38 | fails | fails | +0.0197 | same, near each end |
| 14 | 46 | fails | fails | +0.0197 | same (`e = 40 440 798 401`) |

The one-ended `P_9 + tail(m)` keeps WIN failing with margin +0.019686 at m = 30, 45 and 60 (n up to 69). `B7 + tail(m)` shows the same, with every value exact in `out_witness.txt`; the small members are cross-checked by explicit enumeration. The control `6 0 0 2 2 3 f + tail`, whose `(u,v)` automorphism pins `(2,3)` at 1/2, keeps WIN at every m, so the WIN test fires.

**Consequences (EMPIRICAL on the family, exact per member).**
- (i) Q §5's candidate "for `n ≥ n_0(D)`, some extreme window contains a balanced pair" is **false at D = 5 for every tested n up to 46** (both ends) or 69 (one end). By Prop 3.2 the margin converges, and the data freezes it to 6 digits. That makes the family persist for all m, but the "all m" statement is CONJECTURED, not proven.
- (ii) The balance in these long posets is **at the ends, just outside the windows**: labels ≤ 8 and ≥ n−9, i.e. within the first/last `≈ 1.6D` positions. The long middle has none. The right local object is the bottom ideal of size `O(D)` (mg-e8b4's certified bottom, and Prop 2.5 of Q), and within it the Swap-Ladder rungs, not `{x} ∪ Inc(x)`.

---

## 4. The proposition, and the precise obstruction

**Theorem 4.1 (PROVEN).** Let `P` be a finite non-chain indecomposable poset with no balanced pair. Then:
1. (Q Thm 3.1, audited) each end is O1 or O2, and every minimal `x` with `P[x first] ≤ 2/3` branches before its Linial crossing.
2. For every nested pair `(x, b)` with `P[x<b] ≤ 2/3` (hence `< 1/3`), the chain bottom `b_0 < … < b_m` of `↑b ∖ ↑x` has `P[x < b_m] < 1/3`, so `↑b ∖ ↑x` is not a chain. The dual holds as well.
3. (Cor 1.6) No incomparable pair `{x, b}` carries two full-chain ladders asserting opposite orders. In particular `P` has no Zaguia good or very good pair, and no nested pair `(x,b)` with `up(x) ⊆ up(b)` whose private up-set `↑b ∖ ↑x` and private down-set `↓b ∖ ↓x` are both chains.
4. At every Y-gadget, G1 or G2 holds (Prop 2.3). For its twins `u, v`, the ladder of the dominance-weaker twin through its partner's private up-set branches before reaching 1/3. If `up(u) ⊆ up(v)` and `↑v ∖ ↑u ∖ {v}` has a unique minimum, then `P[u<v] < 1/6` (Lemma 1.5).
5. If `P ∈ Π_D`: every ladder in 2–4 lies in `Inc(x)`, a window of `≤ D+1` elements. For `n ≥ 8D−1` the constraints at the two ends involve disjoint pairs and interact only through Prop 3.2's boundary vector.

**Corollary 1.6 (PROVEN), used in 3.** Suppose `{x, b}` carries a primal ladder asserting `x` before `b` and a (primal or dual) full-chain ladder asserting `b` before `x`. Then one of the two orders has probability `≤ 1/2`, so its full ladder has `t_0 ≤ 1/2 ≤ 2/3`, and Thm 1.4(c) applies. The twin case is Zaguia's very good pair. The mixed primal/dual case (`down(x) ⊆ down(b)`, `up(x) ⊆ up(b)`, both private sets chains) is not stated in 1610.00809.

**How far Thm 4.1 goes (`out_summary.txt`, EMPIRICAL; indecomposable posets, per population).**

| population | n | Swap Ladder fires (Thm 1.4) | Zaguia good pair | structural Cor 1.6 (no probabilities) | Local Linial (Q) |
|---|---|---|---|---|---|
| all posets | 8 | 12 524 / 12 524 | 12 519 | 12 519 | 4 986 |
| all posets | 9 | 146 468 / 146 468 | 146 354 | 146 330 | 50 167 |
| range ≤ 3 | 9–12 | — | — | 5 412 / 5 412 | — |
| range ≤ 4 | 9–11 | — | — | 69 956 / 69 956 | — |
| mg-2912 records | ≤ 24 | 2 534 / 2 534 | 2 513 | — | — |

Where "fires", a balanced pair is certified by the theorem, and 0 conclusion violations were found. Also EMPIRICAL on every population above: every poset has a **nested** balanced pair. That is the only kind of pair a Swap Ladder can certify, so this is a necessary condition for the SL-conjecture below, and it holds.

**The obstruction.**
- The structural statement (item 3 of Thm 4.1, which needs no probabilities) fails on 5 indecomposable posets at n = 8 (ranges 4, 5, 5, 5, 5) and 138 at n = 9 (46 of range 5, 86 of range 6, 5 of range 7, 1 of range 8). Examples: `8 0 0 0 4 5 6 e 2f`, `8 0 0 2 2 a b 7 5f` (range 4) and `8 0 0 2 2 3 b 1b 2f`. The last one is a Y-gadget `{0; 1<2,3}` whose twins' private up-sets both branch.
- On each of these, only the quantitative Swap Ladder certifies the balance. For `8 0 0 2 2 3 b 1b 2f` it is `(2; 4 < 6)`, a nested but non-twin ladder, with first rung 6/11.
- So what a contradiction needs beyond Thm 4.1 is an **(L3)-analogue for the Swap Ladder**: a reason why *some* nested ladder whose chain bottom reaches 1/3 must start at `≤ 2/3`. In Linial's proof this came from "two minimal elements, one has `P[first] ≤ 1/2`". Cor 1.6 supplies it whenever a pair carries opposite ladders, and the census shows that is not always so.

**CONJECTURED (SL-conjecture).** Every finite non-chain poset has a nested pair (in `P` or its dual) meeting Thm 1.4(c)'s two inequalities. It implies the 1/3–2/3 conjecture. The evidence is the first and last rows above. Zaguia's good-pair form alone is false on 5 / 114 / 21 of them, so the chain-bottom form is needed. I do not know whether the good-pair form was ever conjectured; nothing in 1610.00809 says so.

**CONJECTURED (weak).** Cor 1.6 covers every indecomposable poset of range ≤ 3. Evidence: n ≤ 12, plus all posets n ≤ 9, whose 143 failures all have range ≥ 4. If true, this would give a human-checkable proof of 1/3–2/3 at range 3. It is irrelevant to a minimal counterexample, which has range ≥ 8 (mg-9268, per pm-onethird).

**For KSBFT-R (mg-7bfc, unaudited).**
- R's Prop 3.1 (a least counterexample has only chain modules) forbids `down(u) = down(v)` and `up(u) = up(v)` for `u ∥ v`, since that would make `{u,v}` an antichain module. At a Y-gadget of a least counterexample the twins therefore have `up(u) ≠ up(v)`. With Lemma 1.5 this is the only interaction I found.
- R's missing lemma ("some truncation has a robust balanced pair away from its cut"):
  - **Transfer half: supplied.** By Prop 3.2, a μ-robust balanced pair at depth `O(D)` of a truncation whose cut is at depth `≥ 3D + D(1 + log_{1/τ_D}(2 log D!/log(1+μ)))` is balanced in `P`.
  - **Existence half: not supplied.** It is what the SL-conjecture would give at the bottom of a truncation. `Q_m` shows that in long range-5 posets the balance sits exactly there, but that is range 5, not ≥ 8.

---

## 5. What I did NOT do; candidates ruled out

**Ruled out:**
- (i) "x's own ladder continues past the branch": impossible without a pinch (Lemma 1.2), PROVEN.
- (ii) "The two ends' constraints contradict each other for long posets": no. They are separated (Prop 3.1) and decoupled (Prop 3.2), and the `Q_m` family realises both ends balance-free with a range-5 indecomposable poset up to n = 46 (exact).
- (iii) "P_9's balance is created by the two ends interacting": no, it is a one-end, depth-2 configuration (§3.3, exact ablation).
- (iv) "WIN at some end for `n ≥ n_0(5)`" (Q §5's live conjecture): false for every tested length (§3.4).
- (v) "Zaguia good pairs always exist": false. 5 / 114 / 21 exceptions (n = 8 / n = 9 / records), all covered by the local form.
- (vi) "The structural corollary always applies": false from n = 8 (5 posets).

**Not done:**
- No contradiction: Thm 4.1 is a structure theorem, and the (L3)-analogue is open.
- Did not read Linial 1984, Kahn–Saks, BFT or Shepp. Of Zaguia I read only arXiv 1610.00809 (definitions, Thm 2, Lemma 7, and the step lemma credited to [12]), not the 2012 N-free paper. Novelty of the chain-bottom form and of mixed Cor 1.6 is UNCHECKED beyond that.
- Did not try to prove the SL-conjecture, or Cor 1.6 at range 3. Either would be a case analysis of bottom configurations, which the directive rules out as rote.
- Did not implement Thm 1.4 as a certificate inside mg-e8b4's tree. Its hypotheses are linear in pair laws, so it would pass through Prop 2.5-type mixtures only for pairs lying in every size-`s` ideal.
- Did not prove that the `Q_m` margin stays positive for all m (EMPIRICAL to m = 14 / 60). Did not search for range ≥ 8 analogues of `Q_m`.
- The range-≤3/≤4 structural counts and the n ≤ 9 counts re-use the Q populations. No `n` was extended.
- KSBFT-R is cited from pm-onethird's mail (unaudited). It is not on this branch, and I did not read it.
