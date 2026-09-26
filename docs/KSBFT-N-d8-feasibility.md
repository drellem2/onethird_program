# KSBFT-N: can a state-based DP make range D = 8 feasible on this box? — No (mg-c493)

Subject: the finite check of mg-e8b4 (`docs/KSBFT-I-finite-state.md`, "KSBFT-I"), which settles range π(P) ≤ 7 of the 1/3–2/3 conjecture with an adaptive prefix-certificate tree (2.18·10⁹ nodes). This ticket asked for a state-based algorithm (DP / memoisation) that is sound for the same Theorem 5, validated on D ≤ 7 and projected to D = 8. **D = 8 was not launched.** The instruments are in `code/ksbft_d8/`. `bash code/ksbft_d8/run_all.sh` regenerates every transcript cited here in about 11 minutes on 3 cores.

Labels: **PROVEN** means the proof is in this file. **PROVEN (by computation)** means a finite computation with controls. **EMPIRICAL** comes with its instrument and range. **CONJECTURED** is a guess.

Everything here is relative to KSBFT-I's definitions and lemmas: Prop 1, Lemmas 2–4 and Theorem 5. Their audit (mg-9268) is pending. Nothing here depends on KSBFT Lemma 4.2, its constant 441, or eq. (1.5).

---

## 0. Verdict

1. **The lever is misidentified (PROVEN, plus EMPIRICAL sizes).** The tree does not enumerate paths through the small down-set chain. It enumerates *posets*, meaning canonical prefixes, which are words over the window alphabet. The ≤ C(D+1, ⌊(D+1)/2⌋) states per cut are the layer that *each node already carries*: that is the DP over states, run inside every node. So they bound the per-node cost, not the number of nodes. (Also a correction to the ticket: that count is 70 at **D = 7** and C(9,4) = **126 at D = 8**.)
2. **A sound state-merging DP exists, and its soundness is PROVEN (§2, Theorem 2).** It memoises the full *future key* of a node: the relative 2D-window structure, pic, the relative cut, the live layer counts up to a common scalar, and the live pairs' counts. Two nodes with equal keys have subtrees that decide the same thing (Lemmas A–D). The merge is safe because every certificate found under one node is, word for word, a certificate for the other (§2.3).
3. **Validated (PROVEN by computation, D ≤ 6).** The memo DP reproduces the tree's per-depth node / certified / LP / cut counts **identically** at D = 2, 3, 4, 5, 6, with the same TERMINATED-CLEAN verdicts. It **fails** on the threshold-0.39 control identically to the tree: FOUND-VIOLATION, 140 counterexamples-to-threshold, the same per-depth rows. A self-check re-explores every memo hit and compares the subtree: **0 mismatches over 9 929 hits at D = 6**. A deliberately unsound key (structure only, no counts) is caught: 2 mismatches at D = 4, 15 at D = 5, and changed certified/LP counts at D = 5.
4. **It saves almost nothing (EMPIRICAL).** At D = 6 the memo DP skips 69 902 of 18 169 307 nodes (0.38 %), and its wall time equals the tree's (96 s vs 95 s, one process). Counting every distinct future key in the full trees, the best any merge with this key could do is ×1.003, ×1.012, ×1.022 at D = 4, 5, 6.
5. **No window-keyed DP can do much better (PROVEN floor + EMPIRICAL).**
   - At depth N ≤ 2D − 1, the window that the generation rule reads *is the whole prefix*. So distinct tree nodes there are distinct states for **any** DP keyed on that window. Those nodes are 30.2 %, 30.5 %, 33.5 %, 38.1 % of the tree at D = 4, 5, 6, 7 (measured shares). That makes the maximum speed-up ×3.3, ×3.3, ×3.0, ×2.6.
   - A deliberately too-coarse structural key M (no counts, capped pic, no cut) still leaves 70–76 % of nodes distinct at D = 4..6, i.e. ≤ ×1.42.
   - Merging only by structure, the "certificate-hull" idea, cannot beat that even with a perfect data abstraction.
6. **D = 8 projection (EMPIRICAL, fit on D = 4..7).** The tree needs **4.1·10¹¹ nodes, ≈ 1 000 core-hours** at the D = 7 per-node cost (9.0 µs, used here as a floor).
   - The exact-memo DP gives ≈ 1 000 core-hours.
   - An ideal structural merge gives ≈ 940.
   - The M-floor gives ≈ 780.
   - The PROVEN window floor gives ≥ 435.
   - **All are ≥ 20× over the 20 core-hour bar** (8·10⁹ nodes). **Not feasible here. Not launched. Nothing for pm-onethird to decide on this route.**

---

## 1. What the tree enumerates, and where the states are

A node of KSBFT-I's tree is a canonical prefix: the first N elements of a canonical order of a range-≤D, ordinal-indecomposable poset. It carries the layer V_k at its complete cut k = max(N−D, d(e_N)): at most C(2D, D) down-sets, observed at most C(D+1, ⌊(D+1)/2⌋). For every tracked pair it also carries the exact counts (e(J), c_q(J)) over J ∈ V_k. The children are all admissible next elements.

**Observation 1 (PROVEN).** The per-node computation of KSBFT-I (`step()`, `classify()`, `lp_certify()`) is already a dynamic program over the down-set states. The transfer from cut k to cut k+1 sums over the at most C(2D,D) states and never over paths. So the "small state graph" is exploited *inside* each node. The quantity that grows is the number of nodes, i.e. the number of distinct poset prefixes that are not yet certified. The states-per-cut bound says nothing about it.

*Proof.* The node cost is O(|V_k| · D · #pairs) per cut step, read off `step()`. The node count is the number of admissible prefixes. These are different objects. ∎

So "enumerate STATES instead of PATHS" can only mean *merge nodes*: two prefixes with the same future are explored once. §2 does this soundly. §4 measures how much it can buy.

The node-count profile shows why the answer is "little". The tree peaks at depth ≈ 2D (D = 7: 6.2·10⁸ nodes at depth 14 of 2.18·10⁹ total). Up to depth 2D − 1, the prefix is no longer than the window any merge must respect.

---

## 2. The exact-key DP and its soundness — PROVEN

### 2.1 What is memoised

For a node ν with N elements that is **not closed** (no certified pair, no LP certificate, not cut-pruned), let w₀ = max(0, N − 2D). Its key K(ν) consists of:

1. N if w₀ = 0; otherwise a marker (N itself is not in the key);
2. k − N, where k is the node's cut;
3. for each position i ∈ [w₀, N): the down-set of i restricted to [w₀, N), relabelled by i ↦ i − w₀, and pic(i) (the current number of incomparable elements);
4. the live layer: the multiset {(J ∩ [w₀,N) relabelled, e(J)/g)}, sorted by relabelled mask;
5. the live pairs: the multiset {(ā, b̄, (c_q(J)/g)_J in the sorted state order)}, where x̄ = x − w₀ if x ≥ w₀ and x̄ = OLD otherwise;

where g is the gcd of all e(J) and c_q(J). Keys are compared **word for word** (`key_full()`, `memo_find()` in `dp.c`). No hash is trusted. A stored entry holds:

- the full key;
- the subtree's per-relative-depth profile (nodes, certified, LP-certified, cut-pruned);
- its counterexample-to-threshold count;
- its height.

An entry is stored only if its subtree met no depth cap. A later node with the same key *replays* the entry (adds the profile and the counterexample count) instead of exploring. By default this happens only at depth ≥ 2D+1, where hits can occur; `memo:0` memoises everywhere. Memoising fewer nodes is always sound.

### 2.2 Why the key is enough

**Lemma A (every state contains the prefix below the window).** Every J ∈ V_k contains every position < w₀.

*Proof.* By Prop 1 of KSBFT-I, J ⊇ {positions < k − D}. Also k ≥ N − D, so k − D ≥ N − 2D = w₀ (when w₀ > 0). ∎

**Lemma B (the children and the pruning are functions of the key).** The set of admissible child up-sets U (relabelled), each child's cut, and each child's cut-pruning are determined by items 1–3 of K(ν).

*Proof.* Go through the generation rules of KSBFT-I Theorem 5 as `enum_U()` implements them.

- U lies in [N−2D+1, N). It must be an up-set there (successors of a window position are later, hence in the window), with |U| ≤ D and pic < D. These are read from item 3.
- **d non-decreasing.** d(new) = N − |U| and d(e_N) = popcount(down(N−1)). Every position p < N−2D is below N−1: its distance ≥ 2D exceeds the F2 bandwidth 2D−1, so p and N−1 are comparable, and p comes first. So d(e_N) − N is read from item 3.
- **Tie-break.** The masks Dn = [0,N)∖U and down(N−1) are compared as integers. Both contain every position < w₀: Dn because U ⊆ [w₀+1, N), and down(N−1) by the previous point. So their order is decided on [w₀, N).
- **Child's cut.** max(N+1−D, N−|U|) is relative.
- **Early cut (Lemma 2c).** This is U = ∅.
- **"Permanent cut".** This rule of `tree.c` reads further back, but it never fires when the early cut is on. If positions 0..c−1 are below everything from position c on, then the element at position c has down-set exactly {0..c−1}, so it was added with U = ∅ and pruned then. This is EMPIRICALLY confirmed as well: `SHOWCUT=1` prints nothing at D = 4, 5.
- **`decomposable_complete()`.** This is identically false on surviving nodes, for the same reason.

The child's pic on the window is pic + 1_U, and pic(new) = |U|. ∎

**Lemma C (the key propagates).** K(child) = F(K(ν), Ū), for one function F.

*Proof.*

- The child's layer is obtained by `step()`. For each parent state I, `step()` adds positions z ∉ I with down(z) ∖ I = ∅.
- By Lemma A, z ∉ I forces z ≥ w₀, and down(z) ∖ I only involves positions ≥ w₀. Membership of an OLD endpoint in any state is always true.
- New pairs are (j, N) for j ∈ U.
- `step()` is linear in the vector (e, c), so the common factor g passes through, and the child's key re-normalises.
- When the window slides (w₀ → w₀+1), position w₀ leaves. By Lemma A applied to the child, it lies in every child state, so pairs touching it become OLD, and its pic is no longer read (Lemma B).

Hopeless-pair dropping and the live set are determined by the ratios c/e, which item 5 carries. ∎

**Lemma D (the decisions are functions of the key's mathematics).** At a node with key K:

- whether some pair is certified (`classify()`: comparisons of c/e with 1/3, 2/3, and membership);
- which pairs are hopeless;
- the outcome of the complete check (δ over the live pairs of the poset ending here, computed by stepping the layer to the full set);
- the validity of any given Gordan multiplier vector λ (the exact integer test Σ_q λ_q a_{qJ} ≥ 0 of KSBFT-I Lemma 4, where a_{qJ}·3e(J) is linear in (e, c));

are all invariant under the relabelling and scaling in K.

*Proof.* Every one of them is a sign condition on a homogeneous linear form in (e(J), c_q(J)), or a membership test. ∎

**Remark (what is *not* key-invariant).** The *search* for λ (a floating-point simplex whose column order is the code's pair order) and the LP's overflow guard (e ≥ 2⁸⁵ ⇒ skip) may depend on the order and scale of the representation. So an LP *attempt* at two nodes with equal keys may succeed at one and fail at the other. The proof below uses only *successful* certificates, which Lemma D transfers. Empirically the attempts did agree: every hit re-explored at D ≤ 6 matched (§3).

### 2.3 Theorem 2 (soundness of the memo DP) — PROVEN

> Suppose the memo DP (`dp D MAXDEPTH 1 3 memo[:m]`) reports TERMINATED-CLEAN: no frontier and no counterexample-to-threshold, including the counts added by replays. Then every finite non-chain poset of range ≤ D has δ ≥ 1/3.

*Proof.*

1. **Setting up.** Let P be a minimal counterexample. By KSBFT-I Lemma 2d, P is ordinal-indecomposable of range ≤ D. Let ν₀, ν₁, …, ν_n be the prefixes of a canonical order (Lemma 2a).
2. **P's path is never closed.** As in KSBFT-I Theorem 5:
   - no ν_i is closed by a certificate, since P would then have a balanced pair (Lemmas 3/4, 2b);
   - no ν_i is closed by the early cut, since P would then be decomposable (Lemma 2c);
   - ν_n's complete check reports P, since δ(P) < 1/3 over all pairs, the live ones included.
3. **Induction.** Call a stored entry E *good* if no node ν with key K(E) that is a prefix of an indecomposable counterexample exists. We prove every entry that the DP replays is good. We argue by induction on the order in which entries are **stored**. An entry is stored only after its subtree has been completely explored, and during that exploration only earlier-stored entries are replayed.
4. **Following a counterexample below a stored entry.** Take E, stored after exploring node α. Suppose some counterexample Q has a prefix ν with K(ν) = K(α). Let w = (U₁, …, U_m) be the rest of Q's canonical order after ν, written as relabelled up-sets.
   - By Lemmas B and C, w is admissible after α too, and the nodes α·w₁..ⱼ and ν·w₁..ⱼ have equal keys for every j.
   - Follow α·w through the DP's exploration of α's subtree. Each node α·w₁..ⱼ is one of five things:
     - (a) closed by a certified pair: by Lemma D, the same pair is certified at ν·w₁..ⱼ, so Q has a balanced pair. Contradiction.
     - (b) closed by a successful LP certificate λ: by Lemma D, λ is a valid Gordan certificate for ν·w₁..ⱼ, so Q has a balanced pair. Contradiction.
     - (c) cut-pruned (U_j = ∅): then Q is decomposable. Contradiction.
     - (d) replayed from an earlier-stored entry E′: by the induction hypothesis E′ is good, but ν·w₁..ⱼ has its key and is a prefix of Q. Contradiction.
     - (e) explored.
   - Since E was stored, α's subtree met no depth cap, so the path cannot stop at a frontier. If (e) holds all the way to j = m, then α·w is a complete node whose complete check has the same outcome as Q's (Lemma D). That is a counterexample-to-threshold, counted in E's recorded count.
   - If that count is > 0, then every replay of E adds it to the global count, so a TERMINATED-CLEAN run replays only entries with count 0. So E, if replayed, is good.
5. **Conclusion.** Walk P's path in the DP.
   - If some ν_i is replayed, its entry is good by step 4. But ν_i is a prefix of the counterexample P. Contradiction.
   - Otherwise every ν_i is explored, and ν_n reports P. Contradiction. ∎

**What merging two paths assumes, stated once.** Two prefixes with equal keys have the same set of admissible continuations. Every continuation gives both the same exact pair data up to a common positive scalar. That is all Lemma 3 (convexity) ever reads. The past beyond the window enters only through e(J), c_q(J) and pic, and those are in the key.

### 2.4 The "certificate-hull" relaxation (designed, not built; why)

The ticket's alternative merges nodes that are only structurally equal (items 1–3), carrying an *abstraction* of the data, e.g. a box of e-ratios and c/e-values. Certification is then required for every point of the box.

- **Sound in principle.** Each decision in Lemma D is a homogeneous linear sign condition on (e, c). "Pair q is certified at a given future node" is therefore a polyhedral cone condition on the data, and "for all points of a box" is an LP.
- **Two traps for the audit.**
  1. "Some pair is balanced" is a *union* of cones, not convex. So merging two nodes by the *convex hull* of their data is unsound unless one fixed pair or λ works for the whole hull.
  2. OLD pairs of two different histories are different pairs with no correspondence, so only witnesses built from window pairs transfer.
- **Its ceiling.** It cannot merge more than the structural key S does. §4 measures S's ceiling at ×1.08–1.10 (D = 4..6), and the looser M floor at ≤ ×1.42. The cost per abstract node (an LP per decision) is higher than a tree node's. So it was **not built**. The negative rests on the ceiling measurement, not on an implementation.

---

## 3. Validation — PROVEN by computation (D ≤ 6) / controls

All of the following are produced by `run_all.sh`.

| check | transcript | result |
|---|---|---|
| memo DP vs tree, per-depth node / certified / LP / cut / counterexample rows, D = 2..5, `memo` (depth ≥ 2D+1) and `memo:0` (all depths) | `out_memo_d2to5.txt` | **IDENTICAL** (8/8) |
| the same at D = 6 | `out_memo_d6.txt` | **IDENTICAL**; 335 538 lookups, 9 303 hits, 326 235 entries (1.1 GB of key words), 69 902 tree nodes replayed |
| every hit re-explored and compared (`memocheck`), D = 3..6 | `out_memocheck.txt` | **0 mismatches** (0, 1, 113, 9 929 hits) |
| firing control: structure-only key (`badmemo`, unsound on purpose) under `memocheck` | `out_memocheck.txt` | **caught**: 2 mismatches at D = 4, 15 at D = 5 (D = 3: its single hit happens to agree) |
| firing control: `badmemo` without the check, D = 5 | `out_memocheck.txt` | **per-depth rows differ from the tree** (certified/LP at depths 12, 13) |
| threshold 0.39 control, D = 3, cap 12: tree, `memo`, `memo:0` | `out_control039.txt` | all three **FAIL** (FOUND-VIOLATION, 140 counterexamples-to-threshold, first ones 2+1 = [0,0,2] and [0,0,2,3,7], frontier 402); per-depth rows identical |

D = 7 was **not** re-run with the memo. At the measured saving (§4) it would cost the same ~1 h 49 min on 3 cores and add nothing. The memo at D = 7 would also need ≈ 10¹⁰ bytes of keys per slice, extrapolating the 1.1 GB at D = 6.

Per-node cost, from this session's single-process runs of the same binary (EMPIRICAL): 3.2 µs at D = 5 and 5.2 µs at D = 6. KSBFT-I reports 9.0 µs at D = 7 (3 processes). The memo's bookkeeping costs as much as it saves at D = 6 (96 s vs 95 s).

---

## 4. The ceiling: how many distinct futures are there? — EMPIRICAL

Instrument: `dp D 58 1 3 keystat` computes, at every node of the full tree, 128-bit fingerprints of three keys and counts the distinct ones (`out_keystat_d*.txt`).

- **X**: the exact key of §2.1, computed on the node's own layer.
- **S**: items 1–3 only (structure).
- **M**: a deliberately too-coarse structural key: window [N−2D+1, N), pic capped at D, no cut.

A fingerprint collision could only merge keys, i.e. over-state the possible merging. That direction is harmless for a negative.

| D | tree nodes | distinct M | distinct S | distinct X | share at depth ≤ 2D−1 | max speed-up M / S / X / depth-floor |
|---|---|---|---|---|---|---|
| 3 | 152 | 0.737 | 0.934 | 1.000 | — | ×1.36 / ×1.07 / ×1.00 / — |
| 4 | 4 758 | 0.704 | 0.914 | 0.9975 | 0.302 | ×1.42 / ×1.10 / ×1.003 / ×3.3 |
| 5 | 235 851 | 0.728 | 0.911 | 0.988 | 0.305 | ×1.37 / ×1.10 / ×1.012 / ×3.3 |
| 6 | 18 169 307 | 0.764 | 0.924 | 0.978 | 0.335 | ×1.31 / ×1.08 / ×1.022 / ×3.0 |
| 7 | 2 181 780 336 | — | — | — | 0.381 | — / — / — / ×2.6 |

**Proposition 3 (the depth floor, PROVEN given the counts).** Every DP whose state determines the labelled window [N−2D+1, N) (the region `enum_U` reads) has at least Σ_{N ≤ 2D−1} nodes_N states.

*Proof.* For N ≤ 2D−1 the window starts at position 0, so it is the whole prefix. The tree generates each labelled prefix at most once: siblings differ in U, and distinct parents differ in the prefix. ∎

The D = 7 column is only this floor. A full D = 7 keystat needs three fingerprint sets of 2·10⁹ entries (≈ 100 GB), so it was not run. Two D = 7 slices (`out_keystat_d7_slices.txt`; slices 0 and 1 of 120 at depth 9, 1.9·10⁷ nodes each) show *no* merging inside a slice (M 0.9992, X 1.0000). That is uninformative: the D = 6 calibration slices show the same (M 0.994 inside a slice, 0.764 globally), because matching futures sit in different depth-8/9 subtrees. The per-slice numbers are reported and **not used**.

Trend: the mergeable fraction does **not** grow with D. M's share rises 0.704 → 0.728 → 0.764, and X's saving grows only from 0.25 % to 2.2 %.

---

## 5. D = 8 projection — EMPIRICAL (`project.py`, `out_projection.txt`)

- **Tree size.** Fitting log₁₀(nodes) to a quadratic in D over D = 4, 5, 6, 7 (4 points, 3 parameters) gives the residuals below 0.001 in log₁₀. The successive log-growths 1.695, 1.886, 2.080 have second differences 0.191 and 0.193. **D = 8: 4.07·10¹¹ nodes (×187)**. KSBFT-I's ratio-of-ratios rule gives 4.08·10¹¹.
- **Per-node cost.** 9.0 µs, the D = 7 figure, used as a *floor*. It rose 3.2 → 5.2 → 9.0 µs over D = 5 → 7, and the layer bound grows from 70 to 126 states at D = 8.

| method | projected D = 8 nodes / states | core-hours (at 9.0 µs) |
|---|---|---|
| tree (KSBFT-I) | 4.1·10¹¹ | ≈ 1 020 |
| exact-key memo DP (this ticket; D = 6 share 0.978) | 4.0·10¹¹ | ≈ 1 000 |
| ideal structural merge S (D = 6 share 0.924) | 3.8·10¹¹ | ≈ 940 |
| any merge coarser than S down to M (D = 6 share 0.764) | 3.1·10¹¹ | ≈ 780 |
| **any window-keyed DP, PROVEN floor** (depth ≤ 15 share, extrapolated 0.43) | 1.7·10¹¹ | **≥ 435** |
| bar set by the ticket | 8·10⁹ | 20 |

**Conclusion (EMPIRICAL projection, with a PROVEN-shaped floor).** No state-merging DP of the kind asked for comes within a factor 20 of the bar. Even the floor, which assumes free data abstraction and free merging of everything past depth 2D − 1, is ≈ 22× over. D = 8 stays at ≈ 10³ core-hours, as KSBFT-I estimated. That is cluster scale, and on this route the decision is unchanged.

---

## 6. What I did not do; negatives

- **D = 8 was not launched** (per the ticket), and D = 7 was not re-run with the memo (§3).
- **The certificate-hull / box abstraction (§2.4) was designed, not implemented.** It is ruled out by the measured S/M ceilings, not by a run.
- **Candidates tried as merge keys, with the ceiling each gives at D = 6:**

  | key | ceiling at D = 6 |
  |---|---|
  | X (exact) | ×1.022 |
  | S (structure: window, pic, cut) | ×1.083 |
  | M (window of 2D−1 positions, pic capped, no cut) | ×1.31 |
  | whole-window floor | ≤ ×3.0 |

- **Not explored:**
  - *dominance* merges between structurally different windows (e.g. pic pointwise larger ⇒ fewer continuations), which Proposition 3 does not cover;
  - merges up to isomorphism of the window rather than labelled equality (twins; KSBFT-I §6 (i)). Merging isomorphic prefixes is **not obviously sound**, because the canonical-order tie-break depends on labels.

  These fall outside Proposition 3's floor and are open. CONJECTURED: neither gives ×50. The first would at best approach the M column, which already drops the counts. The second is bounded by the number of automorphisms of 2D-element windows seen on tree paths.
- **The levers that might reach ×50 are not state-merging:**
  - LP with branching on two-sided pairs (KSBFT-I §6 ii), which attacks the depth-2D peak directly by certifying earlier;
  - using the top end (§6 iv);
  - isomorphism reduction proved sound for the canonical order.

  None was tried here.
- **The fingerprints in `keystat` are probabilistic.** They are used only for the ceiling measurement, where a collision errs in the harmless direction. The memo itself compares full keys.
- **Theorem 2 inherits KSBFT-I Theorem 5 and Lemmas 2–4 unchanged.** Their audit (mg-9268) is pending. If they fall, so does this.

## 7. Reproduce

```
bash code/ksbft_d8/run_all.sh     # ~11 min, 3 processes; does not run D = 8
```

| file | contents |
|---|---|
| `dp.c` | `tree.c` of mg-e8b4 plus: `memo[:m]` (§2), `memocheck`, `badmemo` (controls), `keystat` (§4). All tree modes are unchanged; without these flags its per-depth output equals `tree.c`'s. |
| `project.py` | §5, reading mg-e8b4's committed transcripts and `out_keystat_*` |
| `out_memo_d2to5.txt`, `out_memo_d6.txt` | memo DP vs tree |
| `out_memocheck.txt` | hit re-exploration + the unsound-key control |
| `out_control039.txt` | threshold 0.39 control |
| `out_keystat_d{3,4,5,6}.txt`, `out_keystat_d{6,7}_slices.txt` | distinct-key counts |
| `out_projection.txt` | D = 8 projection |
