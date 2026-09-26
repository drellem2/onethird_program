# KSBFT-I: the finite-state route — "no counterexample of range ≤ D" IS a finite computation, and it settles D = 7 (mg-e8b4)

Subject: the bounded-range case of the 1/3–2/3 conjecture, as isolated by Aires–Chan–Pak–Panova, *Breaking the Infinite Barrier in the 1/3–2/3 Conjecture*, KSBFT_v7 (2026-09-25; `/Users/daniel/files/KSBFT_v7.pdf`, not in this repo). This file builds on mg-1911 (`docs/KSBFT-C-programme-repricing.md` §1 F1/F2/F6 and §3.2) and mg-d707 (`docs/KSBFT-B-case-c-attack.md` §4.2 and §5). The instruments are in `code/ksbft_finite_state/`. `sh code/ksbft_finite_state/run_all.sh` regenerates every transcript except D = 7 in about 2 minutes on 3 cores. `RUN_D7=1 sh …/run_all.sh` also re-runs D = 7, which takes about 2 hours on 3 cores.

Labels:
- **PROVEN**: the proof is in this file.
- **PROVEN (by computation)**: a mathematical proof whose final step is a finite, terminating computation. It is only as good as the code. The code has four controls (§5) and must get the independent audit the rules require.
- **EMPIRICAL**: comes with its instrument and range.
- **CONJECTURED**: a guess.

Nothing here consumes KSBFT Lemma 4.2, its constant 441, or eq. (1.5). The only things used from the paper are the definitions of range and δ, and the BW92/Pec08 citations on p.3 (range ≤ 5 and ≤ 6), which serve only as the targets of the positive controls.

**Errata (mg-171a, per audit mg-9268, `docs/AUDIT-mg-e8b4.md`).** No result changes: the audit finds Thm 7 (D ≤ 7) **HOLDS**, re-run clean by an independent implementation (`aud.c`: 2 181 471 415 nodes, deepest 20). Corrected:
- **Control 3 (`check` mode) assumes the cut lemma; it does not test it.** It builds each random continuation by stepping the node's own cut-k layer forward, so it cannot see a size-k down-set that is missing from the prefix. It tests Lemma 3's arithmetic, but it assumes Proposition 1 and Lemma 2b. The audit's from-scratch probes close this gap: every one of 5.6 M exhaustive labelled indecomposable posets (n ≤ 8–10, D = 2..7) plus 18 000 random ones up to n = 45 was walked through the generator, with V_k and the certificate re-verified in Python. There were 0 failures, and the one-cut-too-deep mutant is caught (AUDIT §3.1–3.3). §5 item 3 is annotated.
- (†) **89 834 748 is the count at depths > 8, not the total.** The total D = 6 no-LP count is **89 903 224**, now reproduced node for node by both implementations (§4.2).
- **`badcert` fires at N = 4** (`[0,0,2,6]`, `out_controls.txt`), not N = 7. `badlp` fires at N = 7 as stated (§5 item 4).
- **N_D depends on the instrument.** It is the deepest node of *this* tree, so it is an upper bound, not an invariant of posets: `aud` gets N_7 = 20, not 21 (§0 item 4, §4.3).
- **Novelty.** The novelty check is `docs/KSBFT-O-novelty-7thin.md` (mg-00c0): NOT FOUND, every source stops at Pec08. Two wording caveats apply to "the first range not covered by BW92/Pec08" (§0 item 2). First, Pec08 proves the **Gold Partition Conjecture** at D ≤ 6, which is stronger than 1/3–2/3. So the D ≤ 6 positive control reproduces only its 1/3–2/3 consequence, and GPC at D = 7 stays open. Second, Gupta 2026 already covers all posets with **n ≤ 14**. What is new here is range ≤ 7 for every n.

---

## 0. Verdict

1. **Yes, at every fixed D, "no counterexample of range ≤ D" can be *proved* by a finite computation, and n-uniformity costs nothing (PROVEN).** The computation searches the finite tree of bottom configurations. It is sound because of an exact convexity identity (Lemma 3): P_P[a<b] is a convex combination of P_J[a<b] over the size-k down-sets J. Those down-sets are all visible in a bounded bottom window, whatever the rest of the poset is, and however long it is. **No decay-of-correlations rate is needed for soundness.** Decay (Lemma 6) is only part of *why* the tree can terminate: it also needs strict margins, and no a-priori argument supplies those (§3.5). The certificate covers every continuation at once, including infinitely many of arbitrary length.
2. **The computation terminates for D = 1, …, 7 (PROVEN by computation).** Every finite non-chain poset of range π(P) ≤ 7 has a pair x ∥ y with 1/3 ≤ P[x<y] ≤ 2/3. **The 1/3–2/3 conjecture holds for 7-thin posets.** That is the first range not covered by Brightwell–Wright (D ≤ 5) and Peczarski (D ≤ 6; Pec08 proves the stronger GPC there, and Gupta 2026 covers n ≤ 14; novelty check `docs/KSBFT-O-novelty-7thin.md`). D = 7 took 2 181 780 336 tree nodes (deepest 21) and 1 h 49 min on 3 cores, split into 120 slices, all clean. The positive controls reproduce D ≤ 5 in 0.75 s and D ≤ 6 in 46 s. *Independently audited: HOLDS (mg-9268, `docs/AUDIT-mg-e8b4.md`).* Consequence: **a counterexample to the 1/3–2/3 conjecture has range ≥ 8.**
3. **Q1, the state space (PROVEN).** For range ≤ D, the uniform linear extension is a non-homogeneous Markov chain on the down-sets of size k, k = 0..n. Each state is determined by a D-subset of a 2D-slot window, so there are at most C(2D, D) states per cut (3432 at D = 7). The transfer matrix at cut k depends only on the comparabilities inside a window of 2D+1 consecutive elements. **The observed maximum is far smaller: exactly C(D+1, ⌊(D+1)/2⌋) = 3, 6, 10, 20, 35, 70 for D = 2..7** (EMPIRICAL over every node of every search). I CONJECTURE that this is the true maximum, attained by the (D+1)-antichain.
4. **Q2, local data (PROVEN by computation, D ≤ 7).** δ(P) is *not* determined by local data: the Fibonacci middle pairs are the counterexample to that. But **"δ(P) ≥ 1/3" is always witnessed by local data at the bottom.** For D ≤ 7, every ordinal-indecomposable poset of range ≤ D has a 1/3-balanced pair among the first N_D elements of its canonical order, with N_D = 2, 5, 9, 13, 15, 18, 21 for D = 1..7 (§4.3). N_D is the deepest node of this instrument, so it is an upper bound: the audit's implementation gets N_7 = 20. This is **one-sided**, and it is proved uniformly in n by the finite check. Compare mg-d707's two-sided h-order boundary windows B_K, which were EMPIRICAL (K = 4, 5, 6 for D ≤ 4, 6, 9). The two windows are not directly comparable (§4.3).
5. **Q3, decay (PROVEN, with a useless constant, and EMPIRICAL, with a good one).** The width of the certification hull shrinks by a factor ≤ 1 − (D+1)^(−2D) every 2D cuts, uniformly over all posets of range ≤ D (Lemma 6, a Dobrushin bound). That is 1 − 2.3·10⁻¹³ per block at D = 7, which is useless as an a-priori depth bound. Measured, it is 0.2–0.7 per *single* cut, and exactly φ⁻² = 0.382 per cut on the Fibonacci poset (`out_decay.txt`). **The Fibonacci C_BFT limit is harmless to this route.** It lives in the two-sided *middle* of the poset, and the route never looks there. For D ≤ 7 the computation shows every bottom is certified by pairs robustly inside [1/3, 2/3]. Example: Fibonacci's bottom pair has P → 1/φ ≈ 0.618, i.e. balance 1/φ² ≈ 0.382.
6. **Relation to mg-6b81 (KSBFT-M, merged while this ran; pm-onethird asked for a comparison; §4.4).**
   - **The certificate lemma is the same.** My Lemma 3 with Proposition 1 is mg-6b81's Lemma 2.3 with Lemmas 2.2/2.4 (the "prefix certificate"), found independently. mg-6b81 is first on main.
   - **The route is much cheaper.** mg-6b81 certifies *every* non-CUT isomorphism class of a fixed size t, costing t(D) = 4D−1 and ~10¹¹ classes at D = 5. This route closes each branch as soon as it certifies (an adaptive tree), and adds three things: a deeper complete cut, from the canonical order (Lemma 2b); an early ordinal-cut prune (Lemma 2c); and a joint Gordan/LP certificate (Lemma 4).
   - **Measured at D = 4:** 4 758 tree nodes, deepest 13, against mg-6b81's 14 298 595 classes at t = 15. At D = 5: 235 851 nodes, against "infeasible (~10¹¹)".
   - **The state space beats t(D) = 4D−1.** The deepest node is ≈ 3D rather than 4D−1, and the number of nodes per depth is far below the number of classes of that size.
7. **Q4, D = 8 (EMPIRICAL projection).** Node counts grow ×49.6, ×77.0, ×120.1 from D = 4→5→6→7. The projected D = 8 cost is ~4·10¹¹ nodes, about 1 000–1 500 core-hours: ~2–3 weeks on this host's 3-core budget, or 1–2 hours on a 1000-core cluster. **Feasible, but not here; not attempted.** §6 lists pruning ideas that could bring it down.

---

## 1. The objects

Throughout, P is a finite poset on n elements, π(x) = #{y : y ∥ x}, π(P) = max π(x) (the *range*; "D-thin" in BW92/Pec08), d(x) = #{y : y < x} (down-degree), and L(P) is the set of linear extensions with the uniform measure. The *balance* of an incomparable pair is min(P[x<y], P[y<x]). δ(P) ≥ 1/3 means some incomparable pair has 1/3 ≤ P[x<y] ≤ 2/3. For a linear extension g, I_k(g) is its prefix of size k. Every down-set of size k is I_k(g) for some g.

**F1 (window; PROVEN in mg-1911 §1.2, re-stated).** For every linear extension g and every reference linear extension e, |g(x) − e(x)| ≤ π(x). The reason: d(x)+1 ≤ g(x) ≤ d(x)+1+π(x) for every g.

**F2 (bandwidth; PROVEN in mg-1911 §1.2).** If x ∥ y then |e(x) − e(y)| ≤ π(x)+π(y)−1 ≤ 2D−1 for every linear extension e.

**F6 (entropy; PROVEN in mg-1911 §1.2).** e(Q) ≤ ∏_x (π_Q(x)+1) ≤ (D+1)^|Q| for every poset Q of range ≤ D.

---

## 2. Q1: the finite-state (transfer-operator) encoding — PROVEN

**Proposition 1 (state space).** Let π(P) ≤ D and let e be any linear extension, with positions 1..n. Every down-set J of size k satisfies

  {x : e(x) ≤ k − D} ⊆ J ⊆ {x : e(x) ≤ k + D}.

So J = {e ≤ k−D} ∪ S, with S a set of exactly D elements of the 2D positions k−D+1 .. k+D (fewer near the ends). **The number of states at cut k is at most C(2D, D).**

*Proof.* J = I_k(g) for some g. If e(x) ≤ k−D then g(x) ≤ e(x)+D ≤ k by F1, so x ∈ J. If x ∈ J then g(x) ≤ k, so e(x) ≤ g(x)+D ≤ k+D. Since |J| = k, S has exactly k − (k−D) = D elements. ∎

**Transfer operator.** Let V_k be the set of size-k down-sets, and let (T_k)_{I,J} = 1 when I ∈ V_{k−1}, J ∈ V_k, I ⊂ J. Then e(P) = 𝟙ᵀ T_1 T_2 ⋯ T_n 𝟙. The uniform measure on L(P) is the Markov chain I_0 ⊂ I_1 ⊂ … ⊂ I_n with P[I_k = J] = e(J)·e(P∖J)/e(P). Pair events use a "marked" product in which the entry adding b to a set already containing a carries the event. By Proposition 1, T_k is determined by the comparabilities among the ≤ 2D+1 elements at positions k−D .. k+D. **So a range-≤D poset is a word over a finite alphabet of local windows, and L(P) is a product of finitely many 0/1 matrices of size ≤ C(2D,D).** mg-1911 §3.2 conjectured this, and it is now PROVEN.

**Sizes.**

| D | C(2D, D) (PROVEN bound) | max states observed in the search | C(D+1, ⌊(D+1)/2⌋) |
|---|---|---|---|
| 2 | 6 | 3 | 3 |
| 3 | 20 | 6 | 6 |
| 4 | 70 | 10 | 10 |
| 5 | 252 | 20 | 20 |
| 6 | 924 | 35 | 35 |
| 7 | 3432 | 70 | 70 |

The observed column is the largest layer met at any node of the full searches in §4 (EMPIRICAL, `out_d1to5.txt`, `out_d6.txt`, `out_d7.txt`). The (D+1)-antichain has range D and C(D+1, j) down-sets of size j, so the right-hand column is a lower bound on the true maximum. **CONJECTURED: it is the maximum.** Not proved: my attempt got only as far as the observation that two down-sets of equal size differ by sets that are mutually incomparable.

**The alphabet is not the right measure of cost.** The number of distinct local windows grows like the number of range-≤D posets on 2D+1 elements. What the computation actually pays is the number of tree nodes (§4), which is much smaller because certification closes most branches within about 2D+5 elements.

---

## 3. Q2 and Q3: why a finite check is n-uniform — PROVEN

### 3.1 Lemma 3 (cut decomposition; convexity)

For any finite poset P, any k, and any incomparable a, b:

  P_P[a<b] = Σ_{J ∈ V_k} w_J · ρ_J,  w_J = e(J) e(P∖J)/e(P) > 0,  Σ w_J = 1,

where ρ_J = P_J[a<b] if a, b ∈ J; ρ_J = 1 if only a ∈ J; ρ_J = 0 if only b ∈ J; and ρ_J ∈ [0,1] (unknown) if neither is in J.

*Proof.* Condition on I_k = J. Linear extensions of P with prefix J are pairs (linear extension of J, linear extension of P∖J), and they are uniformly distributed. So given I_k = J, the order inside J is uniform on L(J) and independent of the order on P∖J. If exactly one of a, b is in J, it comes first. w_J > 0 because every down-set is a prefix. ∎

**Consequence (the certificate).** If every J ∈ V_k has both a, b ∈ J and ρ_J ∈ [1/3, 2/3], then P_P[a<b] ∈ [1/3, 2/3]. The hypothesis mentions only V_k and the subposets J ∈ V_k. By Proposition 1 these live in the first k+D positions of e. **So the certificate is a property of a bounded bottom window, and it holds for every poset having that window as its bottom, of any length n.**

**Monotonicity.** For k < k′, each ρ_{J′} (J′ ∈ V_{k′}) is itself a convex combination of the ρ_J (J ∈ V_k): apply Lemma 3 to the poset J′. So the hull [min ρ, max ρ] can only shrink as the cut rises. This is used to drop hopeless pairs (hull entirely outside [1/3, 2/3]) for good.

### 3.2 Lemma 4 (joint certificate; Gordan)

All pairs share the same weights w_J. Suppose pair q can leave [1/3, 2/3] on one side only: say every ρ_{qJ} is determined and ≤ 2/3 (resp. ≥ 1/3). Then being unbalanced forces Σ_J w_J a_{qJ} < 0, with a_{qJ} = ρ_{qJ} − 1/3 (resp. 2/3 − ρ_{qJ}). **If integers λ_q ≥ 0, not all zero, satisfy Σ_q λ_q a_{qJ} ≥ 0 for every J ∈ V_k, then some q with λ_q > 0 is balanced in every completion.**

*Proof.* If all Σ_J w_J a_{qJ} < 0, then 0 ≤ Σ_J w_J Σ_q λ_q a_{qJ} = Σ_q λ_q Σ_J w_J a_{qJ} < 0, which is absurd. ∎

λ is found by a floating-point simplex. **Only the exact integer check of Σ_q λ_q a_{qJ} ≥ 0 is trusted.** Every a_{qJ} is multiplied by the positive integer 3·e(J), so the check is in exact 128-bit integers.

### 3.3 Lemma 2 (canonical order; what the tree enumerates)

(a) *Ordering the elements by non-decreasing d(x) gives a linear extension*: x < y implies d(x) < d(y). Break ties inside each equal-d block (which is an antichain) by the down-set bitmask over earlier positions, in non-decreasing order. **Every poset has at least one such canonical order.** The masks of a block depend only on earlier blocks, so the blocks can be fixed one at a time.

(b) *A deeper safe cut.* In a canonical order, every element after position N has d ≥ d(e_N). An element with d(x) ≥ k lies in no down-set of size ≤ k. So **every down-set of size k ≤ d(e_N) lies inside the first N elements.** Together with Proposition 1, the cut k = max(N−D, d(e_N)) is *complete* for a node with N known elements: V_k of every completion equals V_k of the known prefix.

(c) *Early ordinal cut.* If the element at position c+1 has down-set = all c earlier elements (c ≥ 1), then every later element is above all of the first c. By induction on position: a later x has d(x) ≥ c, so either down(x) ⊆ first c elements and equals it, or down(x) contains a later y whose down-set already contains the first c. **So P = (first c) ⊕ (rest) is ordinally decomposable.**

(d) *Minimal counterexamples are ordinal-indecomposable.* If P = A ⊕ B with A, B ≠ ∅, pair probabilities inside A (resp. B) are those of A (resp. B). So a non-chain counterexample P gives a smaller non-chain counterexample A or B. Both inherit range ≤ D.

### 3.4 Theorem 5 (the finite check) — PROVEN, modulo the code implementing it

Fix D. The tree's nodes are the prefixes (first N elements, with their comparabilities) of canonical orders of ordinal-indecomposable posets of range ≤ D. A node's children are all ways to add element N+1. Its incomparable set U among earlier elements must satisfy all of the following:

- it is an up-set of the prefix;
- |U| ≤ D;
- every u ∈ U has current π(u) < D;
- U lies in the last 2D−1 positions (F2);
- d is non-decreasing, and ties are broken by mask (Lemma 2a).

A node is **closed** in any of three cases:

- (cert) Lemma 3 certifies a pair at the complete cut k = max(N−D, d(e_N)) (Lemma 2b);
- (lp) Lemma 4 certifies a set of pairs there;
- (cut) Lemma 2c or a permanent ordinal cut appears. A cut after c is permanent once N ≥ c+2D−1, by F2.

Every node also counts as a *complete* poset (the poset may end there), and its exact δ is computed.

> **If the tree is finite (every branch closes) and no complete node has δ < 1/3, then every finite non-chain poset of range ≤ D has δ ≥ 1/3.**

*Proof.* Let P be a minimal counterexample of range ≤ D. By Lemma 2d it is ordinal-indecomposable. Take a canonical order (Lemma 2a). Its prefixes form a path from the root. At each step, the added element's U satisfies every generation constraint, by range ≤ D, F2 and Lemma 2a. So each prefix is a node, unless some ancestor was closed. It cannot have been closed by (cut), because P is indecomposable (Lemma 2c; a permanent cut is an actual ordinal cut). It cannot have been closed by (cert) or (lp): by Lemma 3/4 and Lemma 2b, P would then have a balanced pair. The tree is finite and P's path is never closed, so the path must end at P itself, i.e. P is a node. But then its complete check found a balanced pair. Contradiction. ∎

The complete check only needs the pairs not already dropped as hopeless. A hopeless pair's hull lies outside [1/3, 2/3], so by Lemma 3 its value in every completion (P included) does too.

### 3.5 Lemma 6 (decay of correlations along the cut) — PROVEN; the rate is useless

Let π(P) ≤ D and let a, b be in every J ∈ V_k. Write W_k := max_{V_k} ρ_J − min_{V_k} ρ_J for the hull width. Then for every m ≥ 2D:

  W_{k+m} ≤ (1 − (D+1)^(−m)) · W_k.

*Proof.* Every J ∈ V_k is contained in every J′ ∈ V_{k+m}: J ⊆ {e ≤ k+D} ⊆ {e ≤ k+m−D} ⊆ J′ (Proposition 1, twice). By Lemma 3 applied to J′, ρ_{J′} = Σ_{J ∈ V_k} W(J′,J) ρ_J with W(J′,J) = e(J) e(J′∖J)/e(J′). The convex set J′∖J has m elements and range ≤ D, so 1 ≤ e(J′∖J) ≤ (D+1)^m (F6). Hence W(J′,J) ≥ e(J)/((D+1)^m Σ_{J″} e(J″)), and Σ_J min(W(J′₁,J), W(J′₂,J)) ≥ (D+1)^(−m). The standard Dobrushin bound gives ρ_{J′₁} − ρ_{J′₂} ≤ (1 − Σ_J min(…)) W_k. ∎

**What this does and does not buy.**

- It is the precise "decay-of-correlations lemma" asked for in Q3. The dependence of a bottom pair's probability on everything beyond the cut contracts geometrically, **uniformly in n and in the poset**, at rate 1 − (D+1)^(−2D) per 2D cuts.
- **It is not needed for soundness** (Lemma 3 is exact) **and not sufficient for termination.** Termination also needs every bottom to carry a pair whose limit is *strictly* inside (1/3, 2/3). Nothing proves that in advance. The computation proves it for D ≤ 7, by terminating.
- The worst-case rate is useless as an a-priori depth bound: 1 − 2.3·10⁻¹³ per 14 cuts at D = 7. The measured rates are 0.2–0.7 per single cut on random range-D posets, and exactly φ⁻² ≈ 0.382 per cut on the Fibonacci poset (EMPIRICAL, `decay.py`, `out_decay.txt`). The bound loses by treating e(J′∖J) as arbitrary in [1, (D+1)^m].

**Long-range correlation, the ticket's "danger".** The Fibonacci infinite limit reaches C_BFT only for pairs in the *two-sided* middle (KSBFT p.4). What decays in a *finite* poset is the influence of the far side of a cut on the near side (Lemma 6). The bottom end is a genuine boundary: its pair limits are those of a one-sided infinite poset, e.g. Fibonacci's (x₀, x₁) → 1/φ ≈ 0.618, i.e. balance 0.382. The computation shows that every bottom of range ≤ 7 carries such a pair, robustly enough to be certified at finite depth.

---

## 4. Q4: the computation

### 4.1 Instrument

`code/ksbft_finite_state/tree.c` is a depth-first search over the tree of Theorem 5.

- For each node it keeps the layer V_k at the complete cut. For every tracked pair and every J it stores the exact counts e(J) and #{L(J) : a before b}, as unsigned 128-bit integers, and aborts if a count gets near overflow.
- A child's layer is computed from the parent's by stepping the cut forward. Layers below the parent's cut are unchanged, because no down-set of size ≤ k_parent contains the new element (Lemma 2b / Proposition 1).
- Closure is decided in this order: (cert) exact rational comparisons; (lp) Lemma 4 with exact verification; (cut) Lemma 2c or a permanent cut.
- The complete check runs the layers forward to the full set.
- `split:I/M@S` deterministically hands out the children of depth-S nodes round-robin to M slices. That the slices partition the tree exactly was checked at D = 5: 580,356 nodes below depth 8 either way. This was a development check, not in the transcripts; `aggregate.py` also refuses a verdict unless every slice index 0..M−1 is present exactly once.

The source used for the D = 7 run is exactly the committed `tree.c`, sha256 `3e1b9424a352b86bc50257cb10eeef82b3a1ac1689b26e9dedb9a0ade2a41827`. Its header comment says the certifying cut is "k = N−D". The code uses `cut_of()` = max(N−D, d(e_N)), which is Lemma 2b and has its own comment. The header was left unedited so that the audited source is byte-identical to the one that ran.

### 4.2 Results (PROVEN by computation; transcripts `out_d1to5.txt`, `out_d6.txt`, `out_d7.txt`)

| D | nodes (with LP) | deepest node | wall (3 cores) | verdict | nodes without LP | nodes without LP and without d(e_N)-cut |
|---|---|---|---|---|---|---|
| 1 | 3 | 2 | 0 s | TERMINATED-CLEAN | | |
| 2 | 11 | 5 | 0 s | TERMINATED-CLEAN | | |
| 3 | 152 | 9 | 0 s | TERMINATED-CLEAN | | |
| 4 | 4 758 | 13 | 0.01 s | TERMINATED-CLEAN | 7 101 | 29 107 |
| 5 | 235 851 | 15 | 0.75 s | TERMINATED-CLEAN (= BW92) | 603 659 | 6 871 716 |
| 6 | 18 169 307 | 18 | 46 s | TERMINATED-CLEAN (= Pec08) | 89 903 224 (†) | |
| 7 | **2 181 780 336** | **21** | **1 h 49 min** | **TERMINATED-CLEAN (new)** | — | — |

D = 1..5 come from `out_d1to5.txt`, D = 6 from `out_d6.txt` (30 slices), and D = 7 from `out_d7.txt` (120 slices; the per-slice transcripts are in `out_d7/`). Wall times are on this host.

(†) As first written this was "≈ 9.0·10⁷", from a pre-LP build with otherwise identical rules, run once at 30 slices while developing: 89 834 748 nodes, all slices clean. That figure is the count at depths > 8, not the total. The total is **89 903 224**, and audit mg-9268 reproduced it node for node with `tree.c nolp` and with its own `aud.c` (AUDIT-mg-e8b4 §2). The no-LP D = 4/5 rows are reproducible (`tree D 58 1 3 nolp`).

The last two columns measure the two prunings. The LP (Lemma 4) saves ×1.5 at D = 4, ×2.6 at D = 5 and ≈ ×5 at D = 6. The d(e_N)-cut (Lemma 2b) saves ×4.1 at D = 4 and ×11.4 at D = 5.

"TERMINATED-CLEAN" means three things: the tree is finite (no node reached the depth cap of 58); no complete node has δ < 1/3; and for split runs, all M slices are present and clean (`aggregate.py` refuses otherwise).

**Theorem 7 (PROVEN by computation).** Every finite poset P that is not a chain and has π(P) ≤ 7 has two incomparable elements x, y with 1/3 ≤ P[x<y] ≤ 2/3.

**Corollary.** Combined with nothing else: a counterexample to the 1/3–2/3 conjecture has range ≥ 8. Under the programme's inference from KSBFT Thms 1.4 and 1.5 (conditional on three preprints), the open region is 8 ≤ π(P) ≤ L*.

### 4.3 The one-sided window (answers Q2's "boundary-window balance")

On the path of any indecomposable P of range ≤ D, closure happens at depth ≤ the deepest node. The certified pair (or LP set) lies among the first *depth* elements of P's canonical order. **So: every ordinal-indecomposable poset of range ≤ D has a 1/3-balanced pair among its first N_D elements in canonical order, where N_D is the deepest node** (PROVEN by computation; N_1..N_7 = 2, 5, 9, 13, 15, 18, 21). **N_D is a property of this instrument, not of posets.** A stronger certificate closes branches earlier, and audit mg-9268's `aud`, with slightly different LP rounding, gets N_7 = 20. So read N_D as an upper bound. mg-d707's B_K used the h-order and both ends, and was EMPIRICAL (annealing, n ≤ 20). The statement here uses the canonical order and the bottom end only, and it holds for all n. The two windows are not comparable element-for-element, because canonical order ≠ h-order. That the bottom alone suffices is the new fact.

### 4.4 Relation to mg-6b81 (KSBFT-M prefix certificate)

`docs/KSBFT-M-margin-induction.md` (mg-6b81, merged on main at 2026-09-26 while this ran; unaudited) proves the same exact reduction. Its Lemma 2.2 (ideal window) is my Proposition 1, and its Lemma 2.3 / Theorem 2.4 (ideal mixture and prefix certificate) are my Lemma 3 and its consequence. I found them independently and did not read mg-6b81 before §3 was written. **Priority on main is mg-6b81's.** Its Lemma 2.5 (CUT) plays the role of my Lemma 2c/2d plus the permanent-cut rule.

Where the two differ, and what each difference costs:

| | mg-6b81 | this file |
|---|---|---|
| what is checked | every non-CUT isomorphism class of size t, at one fixed t | the prefixes of canonical orders, closed adaptively as soon as certified |
| certifying cut for a prefix of size t | s ≤ t − D | k = max(t − D, d(e_t)) in canonical order (Lemma 2b): typically D/2 deeper |
| certificate | one pair, robust over all size-s ideals | one pair (Lemma 3), **or** a Gordan/LP combination of pairs sharing the unknown weights (Lemma 4) |
| decomposable prefixes | CUT: strong cut with \|I\| ≤ t − 2D + 1 | plus Lemma 2c: an element above everything earlier kills the branch at once |
| D = 3 | t = 11, 4 224 classes | 152 nodes, deepest 9 |
| D = 4 | t = 15, 14 298 595 classes | 4 758 nodes, deepest 13 |
| D = 5 | not reached (t = 13 leaves 141 882 of 17 890 772 uncertified; ~10¹¹ classes projected) | 235 851 nodes, 0.75 s |
| D = 6, 7 | not reached (t(7) ≈ 27 projected) | 1.8·10⁷ and 2.18·10⁹ nodes, deepest 18 and 21 |
| margin | yes: robust margin rm (1/96 at D = 3, 1/150 at D = 4) | not computed; the certificate is qualitative (≥ 1/3) |

**Answers to pm-onethird's three questions:**

1. **Same, weaker, or cheaper? Same reduction, much cheaper verification.** Neither is weaker: both prove "no counterexample of range ≤ D" outright from a terminating finite check.
2. **Does the state space beat t(D) = 4D−1? Yes, on both axes.**
   - Depth: the deepest node is 5, 9, 13, 15, 18, 21 for D = 2..7. That is about 3D, not 4D−1 (7, 11, 15, 19, 23, 27). The reasons are the d(e_t) cut and the fact that most branches close long before the worst one.
   - Count: the tree visits only prefixes not already certified, not all classes of the final size. At D = 4 that is a factor of ≈ 3 000 (4 758 against 14.3 M).
3. **mg-6b81 did not have** Lemma 2b (the canonical-order cut), Lemma 4 (the joint certificate), or the adaptive closure. Those three are what move D from 4 to 7.

The two routes also agree on the decay rate: mg-6b81 §4 measures ≈ 0.38–0.41 per G-distance step, and this file measures exactly φ⁻² per cut on Fibonacci. A proof of decay is suggested there via Birkhoff contraction and not attempted. Lemma 6 here is that proof, as a Dobrushin bound, with the useless constant stated.

### 4.5 D = 8 (EMPIRICAL projection; not run)

The growth factors in nodes are ×49.6 (4→5), ×77.0 (5→6) and ×120.1 (6→7). Each factor is about 1.55× the previous one, which gives about ×185 for 7→8, i.e. roughly 4·10¹¹ nodes. The per-node cost was 9.0 µs at D = 7 (1 h 49 min × 3 cores over 2.18·10⁹ nodes) and rises slowly with D. So D = 8 is about 1 000–1 500 core-hours. **Feasible on a cluster (the split is embarrassingly parallel), infeasible within one polecat's 3-core budget (~2–3 weeks).** Memory is not a constraint: under 100 MB per process. The deepest node would be ≈ 24.

---

## 5. Controls (all in `run_all.sh`)

1. **Generation control (`gen_control.py`, `out_gen_control.txt`).** With certification switched off (`nocert dump`), the complete posets the tree visits are compared up to isomorphism with a brute-force list. The list contains every naturally labelled poset (counts checked against OEIS A006455: 1, 2, 7, 40, 357, 4824, 96428 for n = 1..7), filtered to ordinal-indecomposable and range ≤ D. **EQUAL for every D = 1..6 and n = 2..7.** At D = 5, n = 7 there are 1033 classes, and at D = 6, n = 7 there are 1351. Brute force over all n! permutations also confirms min δ = 1/3 over all 1576 indecomposable classes with n ≤ 7.
2. **Independent re-implementation (`indep_tree.py`, `out_indep_tree.txt`).** A Python implementation of the same rules, without the LP and with a different design: no incremental layers, Fraction arithmetic, every pair re-evaluated from scratch at every node. Per-depth node, certified and cut-pruned counts are **identical** to `tree.c nolp` for D = 2, 3, 4 (11, 170 and 7101 nodes).
3. **Soundness checks (`check` mode, `out_controls.txt`).** At every certified or LP-certified node, the certified pair (or pair set) is re-tested exactly on the node's *own* completion and on 4 random *canonical* continuations of 0..2D+1 more elements. Clean for D = 2..5: 192 191 certificates at D = 5. **Caveat (audit mg-9268 §3.3):** the continuations are built by stepping the node's own cut-k layer forward, so this check assumes Proposition 1 and Lemma 2b rather than testing them. It cannot see a size-k down-set of a continuation that is missing from the prefix. The audit closed the gap with from-scratch probes. It walked 5.6 M exhaustive labelled posets (D = 2..7, n ≤ 8–10) and 18 000 random ones (n ≤ 45) through the generator, and re-verified V_k and each certificate in Python. It found 0 failures, and its one-cut-too-deep mutant fires.
4. **Firing controls (`out_controls.txt`).** Each must fail, and each does.
   - `badcert` certifies a pair from one down-set only (unsound): check mode prints `CHECK FAILED` at N = 4 (`[0,0,2,6]`; corrected from N = 7 per audit mg-9268).
   - `badlp` accepts an unverified LP value > −0.02 (unsound): `CHECK FAILED` at N = 7.
   - Threshold 0.39 instead of 1/3 prints `COUNTEREXAMPLE-TO-THRESHOLD` lines, the first being the 3-element 2+1 (δ = 1/3 < 0.39). It also does not terminate, because Fibonacci-type bottoms converge to 0.382 < 0.39.

   So the instrument can say "no", both for an unsound certificate and for a real violation of a threshold.

**Positive controls against the literature.** D ≤ 5 (BW92) and D ≤ 6 (Pec08) are reproduced, and D ≤ 6 is reproduced twice: without the LP (89.9 M nodes) and with it (18.2 M).

---

## 6. Where the cost goes, and pruning not tried

The tree peaks at depth ≈ 2D − 1 to 2D + 1. A pair can be certified only once both of its elements lie in every size-k down-set, which needs N ≳ 2D. Ideas **not tried** that would matter for D = 8:

- (i) **Isomorphism reduction** beyond the canonical order. Twins and equal-mask blocks still produce duplicates.
- (ii) **LP with branching** on pairs that can leave on either side. These are currently just dropped from the LP.
- (iii) **Merging nodes with identical future behaviour**, i.e. identical last-2D window plus identical projective layer data. This is the automaton view of §2 made literal.
- (iv) **Using the top end too.** Currently only complete nodes see their top.

---

## 7. What I did not do (negatives)

- **I did not read BW92 or Pec08.** (Novelty is checked in `docs/KSBFT-O-novelty-7thin.md`.) So I cannot say whether their proofs are of this finite-check form. The KSBFT paper says their methods "break down for larger D" (p.3). The method here did not.
- **The D = 7 result was, when written, not independently audited.** (Since done: audit mg-9268, `docs/AUDIT-mg-e8b4.md`, HOLDS. It includes an independent D = 7 re-run.) Controls 1–4 test the code, but none of them re-runs D = 7 with a different implementation. **An audit should at least:**
  - re-derive Lemmas 2–4 and Theorem 5;
  - re-run `indep_tree.py` against `tree.c` at D = 5 (the Python is slow but feasible, ~10⁶ nodes);
  - re-run D = 7 from source with `RUN_D7=1`.
- **The state-count conjecture C(D+1, ⌊(D+1)/2⌋) is not proved.** Candidate tried: the symmetric-difference structure of equal-size down-sets (mutually incomparable across). It did not close.
- **No a-priori bound on the tree depth.** Lemma 6's rate is too weak, and there is no proof that the tree terminates for every D. It might fail at some D, if a one-sided infinite range-D poset has all bottom pairs with limits outside (1/3, 2/3) or exactly at 1/3. CONJECTURED: it terminates for every D, since a one-sided counterexample would be a one-sided analogue of the conjecture failing.
- **D = 8 was not run.** §4.5 gives the projection only.
- **Nothing here touches the regime 8 ≤ π ≤ L*** beyond the corollary. Nothing here is uniform in D.
- **Lemma 4's LP drops two-sided pairs.** That is sound (fewer constraints) but weaker than possible (§6 ii).

## 8. Reproduce

```
sh code/ksbft_finite_state/run_all.sh            # controls + D <= 6, ~2 min, 3 procs
RUN_D7=1 sh code/ksbft_finite_state/run_all.sh   # + D = 7, ~2 h on 3 procs
```

| file | contents |
|---|---|
| `tree.c` | the search (§4.1); modes `nocert`, `dump`, `check`, `badcert`, `badlp`, `nolp`, `nodcut`, `noearlycut`, `split:I/M@S` |
| `indep_tree.py` | independent re-implementation (control 2) |
| `gen_control.py` | generation control (control 1) |
| `aggregate.py` | sums the split transcripts; refuses a verdict unless every slice is present and clean |
| `decay.py` | hull-width decay (Q3, EMPIRICAL) |
| `out_d1to5.txt`, `out_d6.txt`, `out_d7.txt`, `out_d7/part_*.txt` | the searches |
| `out_gen_control.txt`, `out_indep_tree.txt`, `out_controls.txt`, `out_decay.txt` | controls and measurements |
