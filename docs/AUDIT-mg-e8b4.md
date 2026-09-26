# AUDIT of mg-e8b4 (KSBFT-I, finite-state route; "range D = 7 settled") — mg-9268

Under audit: `docs/KSBFT-I-finite-state.md` (hereafter **I**) and `code/ksbft_finite_state/` (merged as 7c390ab, `tree.c` sha256 `3e1b9424…41827`, matching I §4.1). I am not the author and read I with fresh context. The ticket treats "every non-chain poset of range ≤ 7 has δ ≥ 1/3" (I Thm 7) as a new theorem to be broken. My instruments are in `code/audit_ksbft_9268/`; `sh code/audit_ksbft_9268/run_all.sh` regenerates every transcript here except the D = 7 run, which is `run_d7.sh`.

Labels: **PROVEN** means the proof is in this file (or in I, re-derived here). **PROVEN (by computation)** means a proof whose last step is a terminating program. **EMPIRICAL** comes with its instrument and range. **CONJECTURED** is a guess.

---

## 0. Verdict

**I Thm 7 (D = 7) HOLDS.** I tried to break it and could not. Every non-chain finite poset with π(P) ≤ 7 has an incomparable pair with 1/3 ≤ P[x<y] ≤ 2/3, so a counterexample to the 1/3–2/3 conjecture has range ≥ 8.

- **What it rests on.** It is a proof by computation. It uses **no imported result**: not BW92, not Pec08, not any KSBFT lemma, not AK25a/b, not Haq26. It uses only the definitions of range and of the uniform linear-extension measure, four elementary lemmas that I re-derived in full (§1), and the correctness of the search program.
- **Why I trust the program.** It was re-run by my own implementation, `aud.c`, written from the lemmas with different mechanics (§2). That run gives ****CLEAN**: 2 181 471 415 nodes, deepest 20, all 30 slices clean, 0 violations, 1 h 58 min on 3 cores**.
- **How the two programs agree.** Without the LP, the two implementations agree **node for node at every depth** for D = 2..6, down to 89 903 224 nodes at D = 6. With the LP, they agree exactly for D ≤ 5; at D = 6 they differ by 88 nodes out of 1.8·10⁷, which traces to floating-point LP rounding (§2.2).
- **BW92 and Pec08** (D ≤ 5, D ≤ 6) enter only as positive controls, and both are reproduced.

| # | claim in I | verdict |
|---|---|---|
| 1 | Completeness: every indecomposable P of range ≤ D is a path in the tree (Lemma 2a, Thm 5) | **HOLDS** (proof re-derived; exhaustive probe to n ≤ 8–10, random to n ≤ 45, 0 misses) |
| 2 | Safe cut k = max(N−D, d(e_N)) (Prop 1 + Lemma 2b) | **HOLDS**, and it is **tight**: k+1 is unsound, with an explicit 6-element example (§1.2) |
| 3 | Early ordinal cut (Lemma 2c) and permanent cut | **HOLDS** |
| 4 | Joint Gordan/LP certificate (Lemma 4), integer-exact | **HOLDS**: the direction is right, the integer check is exact, and sampled certificates were re-verified from scratch in Fractions |
| 5 | Positive controls D ≤ 5, D ≤ 6 reproduced; firing controls | **HOLDS**, reproduced. The wrong target [0.34, 0.66] fires on exactly the 2+1 family. **Gap:** the author's `check` mode cannot detect a wrong cut (§3.3). I closed that gap with my own probes. |
| 6 | D = 7: 2 181 780 336 nodes, deepest 21, 120 slices TERMINATED-CLEAN | **HOLDS**. All 120 committed transcripts are clean and complete, and the aggregate is reproduced byte-for-byte. My independent re-run: **CLEAN**, 2 181 471 415 nodes, deepest 20. Rows are identical through depth 9; deeper, they differ by < 0.02 % per depth (LP rounding). |
| 7 | Thm 7 / "counterexample has range ≥ 8" | **HOLDS** (PROVEN by computation, two implementations) |
| 8 | Prop 1 state bound C(2D, D); transfer-operator encoding | **HOLDS** |
| 9 | Observed max layer = C(D+1, ⌊(D+1)/2⌋); CONJECTURED maximal | EMPIRICAL claim **HOLDS**. The conjecture survives my probe: exhaustive to n ≤ 8 (D = 2), n ≤ 7 (D = 3, 4), and random to n = 26, D ≤ 7. |
| 10 | Lemma 6 (Dobrushin decay 1 − (D+1)^(−m) per m ≥ 2D cuts) | **HOLDS** (re-derived) |
| 11 | One-sided window N_D = 2, 5, 9, 13, 15, 18, 21 | **HOLDS** as an upper bound. N_D is a property of the instrument, not of posets (§4): my implementation gets N_7 = 20. |
| 12 | Same lemma as mg-6b81 Thm 2.4 | **HOLDS**: Prop 1 = Lemma 2.2, Lemma 3 = Lemma 2.3, and the consequence = Thm 2.4 |
| 13 | D = 6 without LP "≈ 9.0·10⁷ (†), 89 834 748 nodes below depth 8" | **OVERSTATED (wording)**. The true total is **89 903 224**. 89 834 748 is the count at depths > 8 only. Now reproduced by both implementations. |
| 14 | §5.4 "`badcert` … CHECK FAILED at N = 7" | **BROKEN (typo-level)**. The transcript `out_controls.txt` says N = 4 (`[0,0,2,6]`). The control does fire. |
| 15 | "the first range not covered by BW92/Pec08" (novelty) | **UNVERIFIABLE** by me. I did not survey the literature beyond I's citations and Gup26 (n ≤ 14, which does not cover it). |
| 16 | D = 8 projection ~4·10¹¹ nodes; decay rates 0.2–0.7/cut; φ⁻² on Fibonacci | EMPIRICAL as labelled. Not re-measured (§6). |

**Nothing is BROKEN in the mathematics.** The two defects are a transcript-citation typo (row 14) and a mislabelled count (row 13). The substantive audit finding is a **control gap** (§3.3). The author's `check` mode steps the node's own cut-k layer forward into every continuation, so it *assumes* the safe-cut lemma it should be testing. That is not a bug, because the lemma is proved (§1.2) and my from-scratch probes confirm it. But I's claim that control 3 "tests soundness" covers the arithmetic of Lemma 3, not the cut.

---

## 1. The mathematics, re-derived

Notation follows I. P is a poset of range π(P) ≤ D. e is a linear extension, with positions 1..n. V_k is the set of down-sets of size k. ρ_J = P_J[a<b].

### 1.1 Completeness (I Lemma 2a, 2d, Thm 5) — HOLDS

- **(2d) Minimal counterexamples are indecomposable.** If P = A ⊕ B, every incomparable pair of P lies inside A or inside B, with the same probability as there. A non-chain P has a non-chain summand, whose range is ≤ D. ✓
- **(2a) A canonical order exists.** x < y implies d(x) < d(y), so each equal-d block is an antichain. The down-sets of a block's elements lie in earlier blocks, so once earlier blocks are placed, each element's mask is fixed and the block can be sorted by the integer mask. The result is a linear extension in which the key (d, mask) is non-decreasing. This is exactly the test at `tree.c:196-197`: reject if d < d_prev, or if d = d_prev and mask < mask_prev. ✓
  - Uniqueness is **not** needed and does not hold. Equal-mask non-twins give two labelled forms: x, y minimal, z > x only, gives [0,0,1] and [0,0,2]. The tree may therefore visit a class more than once. That costs time, not soundness.
- **Generation constraints are all necessary.** The incomparable set U of the new element (position N+1) must satisfy four things. It must be an up-set of the prefix, because its complement is down(new). It must have |U| ≤ D, because π(new) ≥ |U|. Each u ∈ U must have current π(u) < D, because π only grows. And U must lie in positions ≥ N+1−(2D−1), by F2: if x ∥ y then every element strictly between them in e is incomparable to x or to y, so |e(x) − e(y)| ≤ π(x) + π(y) − 1 ≤ 2D − 1. Every constraint is a consequence of π(P) ≤ D and of the canonical order. So **every prefix of P's canonical order is generated** unless an ancestor was closed. ✓
- **Thm 5.** Closure by (cut) is impossible on P's path because P is indecomposable (§1.3). Closure by (cert) or (lp) gives P a balanced pair (§1.2, §1.4). If the path reaches P itself, the complete check at that node computes δ(P) exactly. The complete check uses only non-hopeless pairs, and a hopeless pair's hull lies outside [1/3, 2/3], so by Lemma 3 its value in P does too. ✓

### 1.2 The safe cut k = max(N−D, d(e_N)) — HOLDS, and it is tight

Let Q be the prefix (first N positions) of the canonical order of some P of range ≤ D.

- **(Prop 1)** Take J ∈ V_k(P). Then J = I_k(g) for some linear extension g. Since d(x) + 1 ≤ g(x) ≤ d(x) + 1 + π(x) and the same holds for e, we have |g(x) − e(x)| ≤ π(x) ≤ D. So x ∈ J gives e(x) ≤ k + D. If k ≤ N − D, then J ⊆ Q. ✓
- **(2b)** In canonical order every later element x has d(x) ≥ d(e_N). A down-set containing x contains down(x) ∪ {x}, so it has size ≥ d(x) + 1. So if k ≤ d(e_N), no size-k down-set contains a later element, and J ⊆ Q. ✓ This step genuinely needs the canonical order. It is false for an arbitrary linear extension.
- A size-k down-set of P inside Q is a down-set of Q. Conversely, Q is a down-set of P, so down-sets of Q are down-sets of P. So **V_k(P) = V_k(Q), with the same subposets J**. That is all Lemma 3 needs. ✓
- **Lemma 3 (the mixture).** Conditioned on I_k = J, the extension is a uniform pair (L(J), L(P∖J)), so P_P[a<b] = Σ_J w_J ρ_J with w_J > 0 and Σ w_J = 1. ✓

**Tightness (answers "find a counterexample if it is too aggressive").** The rule cannot be pushed one cut deeper. Take D = 3 and P = [0,0,1,1,7,11]: elements 0 and 1 minimal, 2 > 0, 3 > 0, 4 > {0,1,2}, 5 > {0,1,3}. This is P's canonical form.

- At the node N = 5 the safe cut is max(2, d(e_5) = 3) = 3.
- At k = 4 the prefix's V_4 misses {0,1,3,5}, a size-4 down-set of P.
- On the prefix's V_4 the pair (1,2) looks certified, but in P, P[1<2] = **15/22 > 2/3**.

My mutant `aud … badcut` makes exactly this one-cut-too-deep decision. The end-to-end probes flag it on 26–46 % of random posets: 259 of 1000 at D = 3 (with 20 "certified" pairs unbalanced in P), 457 at D = 5, and 438 at D = 7 (`out_controls.txt`). The same mutation applied to `tree.c` (cut_of + 1) makes it report FOUND-VIOLATION at D = 3, 4, 5, including the 2-antichain. So both instruments can see a cut error, by different routes.

### 1.3 The ordinal-cut prunes — HOLDS

- **(2c)** Suppose e_{c+1} has down-set = {e_1..e_c}, with c ≥ 1. Every later x has d(x) ≥ c. Either down(x) ⊆ {e_1..e_c}, in which case it equals that set by size, or down(x) contains some later y ⪰ e_{c+1}, whose down-set contains {e_1..e_c} by induction. So P = {e_1..e_c} ⊕ rest, with both parts non-empty, and P is decomposable. In the code this is `sz == 0 && N >= 1`: U empty means Dn = all earlier elements. ✓
- **(Permanent cut)** The code tests at Nc = N+1 whether positions c..Nc−1, with c = Nc − 2D + 1, all lie above positions 0..c−1. Every future element has its U inside positions ≥ (its position) − 2D + 1 ≥ c. So future elements lie above positions 0..c−1 as well, the cut is an actual ordinal cut of every completion, and all completions are decomposable. ✓

### 1.4 The joint Gordan/LP certificate (I Lemma 4) — HOLDS, right direction

A pair enters the LP only if it is **one-sided**, i.e. every J determines ρ_J and all ρ_J lie on one side.

- `canlt && !cangt`: every ρ_J ≤ 2/3. Undetermined J set both flags, so such a pair never enters (`tree.c:355`). Then P_P ≤ 2/3 by convexity, so "unbalanced" means P_P < 1/3, i.e. Σ_J w_J (ρ_J − 1/3) < 0.
- The other side is symmetric, with a = 2/3 − ρ.
- Given λ ≥ 0, not all zero, with Σ_q λ_q a_qJ ≥ 0 for every J: if every λ-supported pair were unbalanced, then 0 ≤ Σ_J w_J Σ_q λ_q a_qJ = Σ_q λ_q (Σ_J w_J a_qJ) < 0. So some λ-supported pair is balanced, for **every** weight vector w, hence for every completion. ✓
- This is the easy ("certificate ⇒ infeasible") direction of Gordan's alternative. Only that direction is used, and it is the right one.
- **Exactness.** Row J is scaled by 3·e(J) > 0, which preserves the sign of Σ_q λ_q a_qJ. The entries are |A| ≤ 3·e(J) < 3·2^85 (guarded at `tree.c:350`). λ is floored to a 2^30 grid. With m ≤ 96 pairs, |Σ| < 96 · 2^30 · 3 · 2^85 < 2^124, inside the i128 range. The float solution is used only as a candidate, and only the integer check is trusted. ✓
- **Re-verified from scratch.** For every LP certificate met by the end-to-end probes, and for every sampled search certificate, I rebuilt the certificate (**5 236** LP certificates in total; §3):
  - V_k by brute-force enumeration;
  - ρ_J by brute-force linear-extension DP;
  - the side conditions and Σ λ a ≥ 0 in Python `Fraction`s;
  - a check that a λ-supported pair is actually balanced in the completion.

  0 failures.

### 1.5 Other PROVEN items

- **Prop 1's bound C(2D, D)** follows from J = {e ≤ k−D} ∪ S with S a D-subset of 2D slots. ✓ The claim that the transfer matrices depend only on (2D+1)-windows follows from the same description. ✓
- **Lemma 6.** For m ≥ 2D, J ⊆ {e ≤ k+D} ⊆ {e ≤ k+m−D} ⊆ J′, so every J ∈ V_k lies in every J′ ∈ V_{k+m}. Then W(J′, J) = e(J)·e(J′∖J)/e(J′) with 1 ≤ e(J′∖J) ≤ (D+1)^m by F6, so Σ_J min(W(J′₁,J), W(J′₂,J)) ≥ (D+1)^(−m), and Dobrushin's bound gives the stated contraction. ✓ The constant (D+1)^(−2D) = 2.27·10⁻¹³ at D = 7 is as stated.
- **Lemma 3 against KSBFT-M Thm 2.4, compared exactly (pm-onethird asked for this).**
  - Thm 2.4 assumes x, y ∈ K = ∩𝒥 (both in every size-s ideal), s ≤ t − D, and p_J ∈ [1/3, 2/3] for all J. I's "Consequence (the certificate)" assumes the same (a, b ∈ every J ∈ V_k, ρ_J ∈ [1/3, 2/3]) at k ≤ N − D. **For that cut they are identical.**
  - I goes further in two ways that Thm 2.4 and its audit mg-f889 do **not** cover:
    - (i) the deeper cut k = d(e_N) > N − D, via Lemma 2b (§1.2 above);
    - (ii) Lemma 3's version for J containing only one of a, b (ρ_J = 1 or 0). That version is what the hopeless-pair drop and Lemma 4 use.
  - (ii) is immediate from the same conditioning argument. If exactly one of a, b is in the prefix I_k = J, it precedes the other in every extension with that prefix. ✓ Both extensions were re-derived here and not taken from f889.
- **The mg-6b81 comparison.** KSBFT-M Lemma 2.2 = Prop 1, Lemma 2.3 = Lemma 3, and Thm 2.4 = I §3.1's consequence. KSBFT-M's "s = t−D+1" firing control is the same experiment as my `badcut`. ✓ The "~3000×" figure compares tree nodes with isomorphism classes: a count of objects examined, not of CPU time.

---

## 2. The computation, re-done independently

### 2.1 `aud.c` — an independent search

I wrote `code/audit_ksbft_9268/aud.c` from I's lemmas. I had read `tree.c` first, so it is not clean-room, but every mechanism differs:

| | `tree.c` | `aud.c` |
|---|---|---|
| child generation | builds the up-set U, descending | builds down(new), ascending, with a down-closure test |
| π counts | incremental counter | recomputed from up/down masks at every node |
| layer step | push into a hash table | pull over the maximal elements of each new state, sorted array + binary search; **aborts if a predecessor state is missing** (an internal completeness assertion) |
| complete-poset check | steps the tracked layer to the full set; tracked pairs only | forward/backward DP over **all** down-sets of the whole poset, from scratch, for **every** incomparable pair |
| LP | Bland simplex, λ floored on a 2^30 grid | own Bland simplex (different formulation: t shifted and bounded), λ rounded to nearest on a 2^28 grid, own exact i128 check |
| split | round-robin over children created at depth S | round-robin over DFS index of depth-S nodes, validated (split = unsplit, D = 5) |

### 2.2 Agreement (`out_compare.txt`)

The comparison key is the per-depth row (nodes, certified, LP-certified, cut-pruned, frontier) at every depth.

| D | mode | nodes | per-depth rows |
|---|---|---|---|
| 2, 3, 4, 5 | no LP | 11, 170, 7 101, 603 659 | **IDENTICAL** |
| 2, 3, 4, 5 | with LP | 11, 152, 4 758, 235 851 | **IDENTICAL** |
| 5 | no LP, no d-cut | 6 871 716 | **IDENTICAL** |
| 4 | LP, no d-cut | 17 864 | **IDENTICAL** |
| 6 | no LP | **89 903 224** | **IDENTICAL** (8.4 min each, single process) |
| 6 | with LP | 18 169 219 vs 18 169 307 | identical through depth 9; from depth 10, aud's LP certifies 6 more nodes, a cascade of ±40 nodes/depth follows; both CLEAN, deepest 18 |

The D = 6 LP difference is expected. The LP is decided by a floating-point simplex, then an exact check, and the two programs round λ differently. A node certified by only one of them is still certified soundly, since both verify exactly. The **deterministic** part of the search (generation, cuts, single-pair certificates, complete checks) is identical node-for-node up to 9·10⁷ nodes.

### 2.3 D = 7

- **The author's run.** All 120 committed slice transcripts `out_d7/part_*.txt` were checked:
  - each has header `D=7 MAXDEPTH=58 threshold=[1/3, 1-1/3]` and `RESULT TERMINATED-CLEAN D=7`;
  - the slice indices are exactly 0..119, once each;
  - no depth row has a non-zero frontier, and each slice reports 0 counterexamples;
  - `aggregate.py 9 out_d7/part_*.txt` reproduces the committed `out_d7.txt` byte-for-byte.

  (The transcripts do not record the mode flags. An accidental `badcert`/`badlp`/`nolp` run would change the node counts, and the counts are corroborated by the independent run below.)
- **My independent run** (`run_d7.sh`, `aud.c` sha256 `dd0cf145…cc53`, 30 slices split at depth 9, 3 processes): **VERDICT D=7: CLEAN** (`out_aud_d7.txt`, per-slice transcripts `out_d7/aud_part_*.txt`).
  - 2 181 471 415 nodes, deepest node 20; 0 violations and 0 frontier.
  - 1 h 58 min wall on 3 cores (17 991 s user).
  - Per-depth rows are **identical to the author's through depth 9**, which is 1 188 641 nodes and the entire split-independent top of the tree.
  - From depth 10 on, the LP decisions differ at a handful of nodes; aud certifies 8 more at depth 10. The rows drift by at most 0.02 % per depth: 2 181 471 415 vs 2 181 780 336 nodes in total, and aud's deepest node is 20 against the author's 21. Every other rule is deterministic and was shown identical at D ≤ 6. So this difference is the floating-point LP and nothing else.
  - Two programs written separately, with different LP rounding, both terminate clean at D = 7.
- **A sample of the author's own slices re-run** with the committed `tree.c`: slices 9, 41, 45, 53, 71, 73, 95, 97, 100 (`random.Random(9268).sample(range(120), 9)`). **All 9 are byte-identical** to the committed `part_*.txt` (`out_tree_sample.txt`; 8 min 18 s on 3 cores). This establishes that the committed transcripts are what the committed source produces.

---

## 3. Probes that could have failed

The task asked for a checker that can fail. Every probe below has a firing control in the same transcript. `check_controls.py` asserts that each firing control actually fired, printing `NEGATIVE CONTROL CAUGHT` (`out_check_controls.txt`). It prints `FAILED TO FIRE` on a planted silent control: replacing FOUND-VIOLATION with TERMINATED-CLEAN in the transcript was tested.

### 3.1 End-to-end completeness and soundness on real posets (`follow_check.py`, `exhaustive_follow.py`)

A poset P is put into canonical order **in Python**. Then `aud … follow` walks P's path through the real generator: MISSED means a generation bug, and CUT on an indecomposable P means a prune bug. The outcome is then verified from scratch:

- V_k(prefix) = V_k(P), by brute force;
- the certificate itself;
- the certified pair (or some LP pair) is balanced in P, computed exactly;
- δ(P) ≥ 1/3.

- **Exhaustive:** every naturally labelled indecomposable poset of range ≤ D, 0 failures in every row:

  | D | n ≤ | labelled posets | canonical forms | CERT / LP / ENDED |
  |---|---|---|---|---|
  | 2 | 10 | 233 | 19 | 12 / 0 / 7 |
  | 3 | 9 | 26 318 | 1 450 | 1 333 / 40 / 77 |
  | 4 | 8 | 108 537 | 6 785 | 5 414 / 203 / 1 168 |
  | 5 | 8 | 722 204 | 33 151 | 20 350 / 904 / 11 897 |
  | 6 | 8 | 2 037 137 | 82 878 | 36 962 / 1 683 / 44 233 |
  | 7 | 8 | 2 691 024 | 114 927 | 44 965 / 1 869 / 68 093 |

  **0 MISSED and 0 CUT.** At D ≥ 5 these sizes are below the permanent-cut depth (N ≥ 2D). The random runs below reach it.
- **Random** (range exactly D, n from 2D to 40–45): 3 000 posets for each D = 3..7 at n ≤ 45 (range exactly D), plus 1 000 for each D = 3, 5, 7 at any range, n ≤ 30. **0 failures, 0 MISSED, 0 CUT.** 301 + 10 of these closed by LP. The minimum δ over the range-exactly-D sets is 0.357 (D = 3) and 0.420 (D = 7).
- **Firing:** `badcut` is flagged on 259/1000 (D = 3), 457/1000 (D = 5) and 438/1000 (D = 7) random posets.

### 3.2 Search certificates re-verified, with random continuations (`sample_check.py`)

Every R-th closed node of a real search is dumped with its certificate. Python rebuilds V_k and ρ_J, re-checks the certificate exactly, then appends 0..3D random elements, keeping range ≤ D and the canonical order (generated in Python). It then checks two things: V_k(completion) = V_k(prefix), and that the certified pair or LP set has a balanced pair in the completion. Sampling rates were every 10th closed node at D = 4, every 200th at D = 5 and every 20 000th at D = 6; at D = 7 it was every 100 000th within slice 0/30.

| D | CERT | LP | continuations | failures |
|---|---|---|---|---|
| 4 | 303 | 30 | 1 665 | 0 |
| 5 | 879 | 82 | 2 883 | 0 |
| 6 | 726 | 76 | 1 604 | 0 |
| 7 | 608 | 38 | 1 292 | 0 |

(`out_sample.txt`)

- **Firing:** with `badcut`, the same probe reports `SAFE CUT FAILS` (14 of 34 sampled nodes at D = 4).

### 3.3 The gap in I's control 3

`tree.c`'s `check` mode (`rand_check`, `tree.c:263-293`) builds each random continuation by **stepping the node's own cut-k layer forward** (`complete_balanced(&cur, n, …)` starting from `cur = sub`). So it can never see a size-k down-set of the continuation that is missing from the prefix. It tests the arithmetic of Lemma 3 on continuations, but it assumes Prop 1 and Lemma 2b. I §5.3 presents it as a soundness check without that caveat. The cut is sound (§1.2), and my probes above test it without the assumption, so this is a gap in evidence, not in the result.

### 3.4 Wrong targets (`out_controls.txt`)

- **[0.34, 0.66]** (lo = 34/100). Both implementations terminate at D = 3, 4, 5 with exactly **two violations: [0,0,1] and [0,0,2]**, the two labelled forms of 2+1 (δ = 1/3). Nothing else.
  - As a side result, EMPIRICAL / PROVEN by the same computation: for D ≤ 5, every ordinal-indecomposable non-chain poset of range ≤ D other than 2+1 has a pair in [0.34, 0.66]. This agrees with mg-6b81's "exceptional list = {2+1}". I did not run it at D = 6 or 7.
- **[0.39, 0.61]**, D = 3, depth cap 20: 4 201 violations and 12 564 frontier nodes. It does not terminate, as I §5.4 says: the Fibonacci-type bottoms tend to 0.382 < 0.39.

---

## 4. Remarks on scope (not defects)

- **N_D (I §4.3).** N_D is the deepest node of *this* tree. My `aud`, with slightly different LP rounding, closes every branch by depth 20 at D = 7, where `tree.c` needs 21. The true statement is "some pair among the first N_D elements in canonical order is balanced". A stronger certificate would lower N_D, so N_D is an upper bound from one instrument, not an invariant. I §4.3 reads correctly if taken that way.
- **"Max layer" (I §2 table).** `tree.c`'s `max layer` counts the intermediate layers of complete-poset checks as well as certification layers. My `aud` reports only certification-cut layers, which are smaller (14 vs 20 at D = 5). The EMPIRICAL claim is about any layer met, and it reproduces.
- **Termination for general D** is CONJECTURED in I and remains so. Nothing here bears on D ≥ 8.

## 5. What rests on what

Thm 7 (D = 7) rests on:

1. F1/F2/F6 (elementary; re-derived in §1);
2. Lemma 2 (a–d), Prop 1, Lemma 3 and Lemma 4 (re-derived in §1);
3. the correctness of the search program.

Item 3 is corroborated by two implementations that agree node-for-node on the deterministic part up to D = 6 without the LP, and that both terminate clean at D = 7. **No imported theorem is used.** In particular, no part of KSBFT_v7 beyond the definitions is used (not Lemma 4.2, not the constant 441, not eq. 1.5), nor BW92, Pec08, AK25a, AK25b or Haq26. The corollary "open region 8 ≤ π ≤ L*" is conditional on KSBFT Thms 1.4/1.5 and hence on AK25a, AK25b and Haq26, as I says.

## 6. What I did not do (negatives)

- **I did not prove the programs correct.** The evidence is two implementations plus probes.
- **The LP code of the two programs was not compared certificate-by-certificate.** Their decisions differ on a handful of nodes at D = 6, which is expected from floating point.
- **I did not re-run D = 7 with LP disabled** (projected ~10¹⁰ nodes). So the D = 7 agreement between the two programs is at the level of "both clean, rows equal to depth 9, within 0.02 % beyond", not node-for-node.
- **I did not re-run** `decay.py` (Q3 rates), the D = 8 projection, or `indep_tree.py` at D = 5. `aud.c` is a faster independent implementation and was run to D = 7 instead.
- **Isomorphism-class completeness** was not re-done beyond I's `gen_control` (n ≤ 7). My exhaustive probe works on labelled posets instead: every labelled indecomposable poset maps to a canonical form that must be generated, so no iso machinery is needed.
- **Literature.** I did not read BW92, Pec08 or Gup26, so the novelty claim (row 15) is UNVERIFIABLE here.
- **Candidates I tried to break things with,** all of which failed to break them:
  - generation: exhaustive labelled posets (§3.1) and random posets up to n = 45;
  - cut: the +1 mutant, both programs;
  - LP: a from-scratch Fraction re-check;
  - layer conjecture: exhaustive to n = 8/7 and random to n = 26;
  - targets: [0.34, 0.66] and [0.39, 0.61].

## 7. Reproduce

```
sh code/audit_ksbft_9268/run_all.sh     # comparisons D<=6, probes, controls (28 min on 3 cores)
sh code/audit_ksbft_9268/run_d7.sh      # independent D=7 (~2 h on 3 cores)
sh code/audit_ksbft_9268/tree_sample.sh  # 9 random author slices, byte-for-byte (8 min)
```
