# AUDIT of mg-5f14 (KSBFT-Q): every PROVEN claim re-derived, and every witness recomputed

`mg-3345`, 2026-09-26. The subject is `docs/KSBFT-Q-local-width2.md` (commit `c187aa6`), together with `code/ksbft_q_local_width2_5f14/`. I am not its author. I re-derived every proof by hand before reading the author's code.

**Instrument.** `code/audit_ksbft_3345/`. The runner is `sh run_all.sh`: exact `Fraction`s, at most 2 processes, about 25 s wall.

| file | what it does | independence |
|---|---|---|
| `indep.py`, `extra.py`, `remark26.py` | witnesses | Builds the order by transitive closure of the input masks, and **enumerates the linear extensions explicitly**: no ideal DP, no shared code. |
| `rec44.py` | mg-2912's records with δ < 0.35 | My own ideal DP. |
| `wincount.py` | the WIN / BR / minimal-pair census columns at `n = 9`, range ≤ 5 and ≤ 6 | My own DP and my own definitions, written from the doc's prose. The census files come from mg-eedd's generator (`pcert onept gen`); its A000112 control is reproduced in `out_gen.txt`. |
| `negative_control.py` | five planted or false statements | Each must print `CAUGHT`, and all five do (`out_negative_control.txt`). The runner asserts every figure this audit relies on. |

Verdicts:
- **HOLDS**: re-derived.
- **BROKEN**: false as stated.
- **OVERSTATED**: true only in a weaker form.
- **UNVERIFIABLE**: cannot be checked from here.

---

## 0. Summary

> **The flashiest claim holds.** The Local Linial Theorem (Thm 2.1), its certificate form under bounded range (Prop 2.5), and the structural reduction (Thm 3.1: a counterexample has a low 3-antichain at both ends) all re-derive. Their quantifiers and their D-dependence are correct. The bounded-range facts are quoted within their hypotheses.
>
> **One BROKEN statement in a proof-bearing section (§3.2), and it is harmless.** "Beyond the branch rank `k`, `{f(x) ≤ j+1} ⊆ ∩_{u∈U}{x before u}`" is false for every `j > k`. The inclusion runs the **other** way: `∩_U{x before u} = {f(x) ≤ k+1} ⊆ {f(x) ≤ j+1}`. So verdict item 5's "the threshold event `{f(x) ≤ j*+1}` is an intersection of pair events" holds **only when `j* = k`**. The doc's witnesses happen to have `j* = k`. In the doc's own 8-element witness the bottom has `k = 0` and `j* = 2`. Lemma 3.3 and the witness `6 0 0 2 2 3 f` do not depend on the false line, so the obstruction stands.
>
> **One BROKEN sentence in the verdict, plus an OVERSTATED headline, both about the range-5 witness `P_9`.**
> - Item 6(a) says "every pair **touching** `{x} ∪ Inc(x)` for an extreme `x` is outside `[1/3, 2/3]`". That is false: all three balanced pairs of `P_9` touch an end window. The true statement is "no balanced pair lies **inside** such a window", and that is what the doc's instrument tests.
> - The headline and §3.4 say `P_9` has "its only balanced pairs in the middle", with "balance forced off both ends into the middle". That is OVERSTATED. `P_9` has essentially no middle: the two end windows `{0,1,2,3}` and `{4,6,7,8}` plus the element `5` are all of `P_9`. Its balanced pairs `(2,4)`, `(2,5)` and `(4,5)` **straddle the two gadgets**; `(2,4)` joins the bottom gadget's `u` to the top gadget's `u`.
> - The `n = 11` range-6 record **does** have interior balanced pairs, `(4,5)` and `(4,7)`, touching no end window. The refutation of WIN and BR itself HOLDS.
>
> **One numeric misquote (BROKEN).** Item 6(a) and §3.4 give "4 / 29 at range ≤ 6 for n = 9 / 10" as WIN-failure counts. Those are the **BR** counts. The WIN counts are **2 / 18**, in the doc's own table and transcript, and I re-derived the 2 independently. No conclusion changes.
>
> **Minor OVERSTATED:**
> - Remark 2.6's labelling `(v_1, v_2) = (y, x)` is not implied. The value claim holds.
> - "among all posets with `n = 9`" and "34% of all posets" should read "indecomposable".
> - "5–15 points" is really 4.1–14.9.
> - Thm 3.1 omits "not a chain".
> - "as it must" (width 2, 528/528) needs a non-chain end. The diamond is a width-2 poset on which LL fires at neither end.
>
> **Regime caveat (not a defect; the doc flags it as OPEN).** Every refuting witness is short: `n ≤ 2D`, namely `P_9` (n = 9, D = 5), the record (n = 11, D = 6) and `W8` (n = 8, D = 6). No witness lies in the regime `n ≫ D` where bounded range bites, or where Prop 2.5's `|Q| ≥ 3D` applies. So "FALSE at range 5" is literally true, but it says nothing yet about long posets at fixed D.
>
> EMPIRICAL is nowhere presented as proof. The labels are correct throughout.

---

## 1. Claim-by-claim

### §1: Linial's proof and its three facts

| # | claim | verdict | re-derivation |
|---|---|---|---|
| 1.1 | Lemma 1.1: for minimal `x`, `q_0 ≥ q_1 ≥ …` | **HOLDS** | Let `u` be the predecessor of `x` at position `j+2`. Then `u ∥ x`: `u` is not below `x` because `x` is minimal, and not above it because it comes earlier. Swapping keeps every relation, because `u`'s down-set stays before `u` and `x`'s up-set stays after `x`. The inverse swaps `x` with its successor, so the map is injective. The direction is right: `q_{j+1} ≤ q_j`. |
| 1.2 | `Inc(x)` is an ideal; `J` (the elements before `x`) is an ideal of `Inc(x)` with `\|J\| = f(x) − 1` | **HOLDS** | Let `w < z ∈ Inc(x)`. `w > x` would give `x < z`, and `w = x` would too; `w < x` is impossible. |
| 1.3 | Linial's width-2 argument as written | **HOLDS** | Deleting global minima preserves pair probabilities, and it ends with exactly 2 minima because the poset is not a chain. `Inc(x)` contains no 2-antichain, since width is 2. `S_{m−1} = 1 − q_m ≥ 1 − q_0 > 2/3`, so the crossing index `j* ≤ m − 1` and `c_{j*+1}` exists. The doc leaves this step implicit. |
| 1.4 | Table (L1)/(L2)/(L3): width enters only through (L2), up to rank `j*` | **HOLDS** | This is a correct reading. (L3) needs only ≥ 2 minima, as stated. |

### §2: the local version

| # | claim | verdict | re-derivation |
|---|---|---|---|
| 2.1 | **Thm 2.1 (Local Linial)** | **HOLDS** | For `j ≤ k` the only size-`j` ideal of `Z` is `C_j`. By induction, a nonempty ideal of `Z ∖ C_{i−1}` contains its unique minimal element `c_i`, and a unique minimal element of a finite poset is its minimum. So for `j ≤ k − 1`, `{x before c_{j+1}} = {\|J\| ≤ j}`. The doc writes "J contains an ideal of size j+1"; the correct and intended reading is "`J ⊇ C_{j+1}` by the same induction". Hence `P[x before c_{j+1}] = S_j`. If `q_0 < 1/3` then `1 ≤ j* ≤ k − 1` by hypothesis, and `S_{j*} < 1/3 + q_0 < 2/3`. The case `k = 0` is excluded by hypothesis. `q_0 ≤ 2/3 < 1` forces `Inc(x) ≠ ∅`. |
| 2.2 | Cor 2.2: `S_{k−1} ≥ k/(m+1)`; `3k ≥ π(x) + 1` ⇒ hypothesis | **HOLDS** | `q_0..q_m` are non-increasing and sum to 1. Since `k ≤ m`, the first `k` of them average at least the mean. |
| 2.3 | Cor 2.3, both forms | **HOLDS** | With exactly 2 minima, `Inc(x)` has the unique minimal element `y`, so `k ≥ 1`. In the second form, `\|Inc(y)\| ≤ 2` ⇒ `q_0(y) ≥ 1/3` ⇒ `q_0(x) ≤ 2/3`. |
| 2.4 | Cor 2.4, Linial recovered | **HOLDS** | See 1.3. |
| 2.5 | **Prop 2.5 (certificate under range ≤ D)** | **HOLDS** | See §2 below. |
| 2.6 | §2.4 F1/F2 bookkeeping | **HOLDS** | `{x} ∪ Inc(x)` is an ideal of size `≤ D + 1`. `j* ≤ k − 1 < m ≤ D`. The partner is within `2D − 1` of `x` (mg-6b81 Lemma 2.1). |
| 2.7 | §2.5: no margin; `2+1` has `q_0 = 1/3` | **HOLDS** | Recomputed exactly (`out_indep.txt`). |
| 2.8 | Remark 2.6: if `y` is minimal with `Inc(y) = {x}`, then `x` is minimal and `P[x before y] = h(y) − 1` | **HOLDS** | Everything except `x` is above `y`, so `f(y) ∈ {1, 2}` and `x` before `y` ⇔ `x` first. This is **not new**: KSBFT-A §6 already proves `δ(v_1, w) = d_1` as the special case `W = {w}`. |
| 2.9 | Remark 2.6: "if `y = v_1`, the end pair `(v_1, v_2) = (y, x)`" | **OVERSTATED** | `x` need not be `v_2`. Take `y < a < b < c` plus an isolated `x`: `Inc(y) = {x}`, but the height order is `y, a, x, …` (`out_remark26.txt`; control 4). On mg-2912's 44 records with δ < 0.35 it does hold (44/44, `out_rec44.txt`, EMPIRICAL). The value statement is what matters, and it holds. |
| 2.10 | EMPIRICAL on the 44 δ < 0.35 records: LL fires, `j* = 0`, the pair attains δ, 41 at the bottom and 3 at the top; all width 2 | **HOLDS** | Re-derived independently with my own DP: 44 / 44 / 44, 41 + 3, width 2 in 44 of 44, `n ≤ 24`. It is correctly labelled EMPIRICAL. |
| 2.11 | By width, over 2 534 records: 528/528, 661/940, 410/662, 0/10 | **HOLDS as reproduced** | The transcript matches the doc. I did not recount by width independently. "As it must" for width 2 needs ≥ 2 minima or ≥ 2 maxima: LL is applied to `P`, not to its components, and fires at neither end of the width-2 diamond. |

### §3: the obstruction

| # | claim | verdict | re-derivation |
|---|---|---|---|
| 3.1 | **Thm 3.1** (i)–(iii), dual, and the O1/O2 dichotomy | **HOLDS** | See the notes below this table. |
| 3.2 | Consequence under range: `k < (D+1)/3`; `u, v` of rank `≤ k + 1 < (D+4)/3` | **HOLDS** | The down-set of `u` is exactly `C`, so `u` has rank exactly `k + 1`. |
| 3.3 | Lemma 3.2: a balanced position event exists at the bottom | **HOLDS** | This is the ladder without (L2). The "≥ 2 minima" hypothesis is not used beyond `q_0 ≤ 1/2`. |
| 3.4 | "Beyond the branch rank `k`, `{f(x) ≤ j+1} ⊆ ∩_{u∈U}{x before u}`" | **BROKEN** for `j > k` | `∩_U{x before u} = {\|J\| ≤ k}`: when `U` is all of `min(Inc(x) ∖ C)`, `J ∩ (Inc(x) ∖ C)` must be empty. So the event is contained in `{f(x) ≤ j+1}` for `j ≥ k`, with equality only at `j = k`. The inclusion as written fails at `j = k + 1`, e.g. on the Y-gadget plus an isolated `x` (`out_extra.txt`; control 1). |
| 3.5 | Verdict 5: "the threshold event `{f(x) ≤ j*+1}` is an intersection `{x before u} ∩ {x before v}`" | **OVERSTATED** | It is true iff `j* = k`. In a counterexample `j* ≥ k`. For `W8`'s bottom `x = 0`, `k = 0`, `S = 15/98, 30/98, 45/98`, so `j* = 2 > k`. The obstruction's substance does not depend on this line: Lemma 3.3 plus the witness is what shows the pair events can both exceed 2/3. |
| 3.6 | Lemma 3.3: `P[x<u], P[x<v] ≥ S_k`; `P[x<u] + P[x<v] ≤ 1 + S_k` | **HOLDS** | `\|J\| ≥ k + 1` ⇒ `J ⊇ C` and `J` meets `U`. "The only constraints the ladder gives" is informal and was not proved. |
| 3.7 | Witness `6 0 0 2 2 3 f`: `S_0 = 4/13`, `S_1 = 8/13`, `P[0<2] = P[0<3] = 19/26`, only balanced pair `(2,3)` at 1/2 | **HOLDS** | By explicit enumeration: `e = 26`, range 3. |
| 3.8 | `5 0 0 2 2 b`: LL fails at both ends; balanced pairs `(0,3)` = 7/11 and `(2,3)` = 4/11 | **HOLDS** | `e = 11`, range 3. It is also self-dual (`0→2, 1→4, 3→3`), which the doc does not state. |
| 3.9 | `P_9`: range 5, width 3, `e = 197`, self-dual, the covers listed, `P[0 first] = 62/197`, `S_1 = 124/197`, `P[0<2] = 161/197`, `P[0<3] = 138/197`, `P[2<3] = 59/197`, balanced pairs exactly `(2,4)` 130/197, `(2,5)` 118/197, `(4,5)` 79/197 | **HOLDS** | Every number was recomputed by enumerating the 197 extensions. Self-duality was checked over 9! maps (map `(7,8,4,6,2,5,3,0,1)`). |
| 3.10 | WIN and BR fail on `P_9` (no balanced pair **inside** `{x} ∪ Inc(x)` for any extreme `x`) | **HOLDS** | |
| 3.11 | Verdict 6(a): "every pair **touching** `{x} ∪ Inc(x)` … is outside `[1/3, 2/3]`" | **BROKEN** | `2 ∈ Inc(0)` and `4 ∈ Inc(7)`. All three balanced pairs touch an end window (control 2). |
| 3.12 | Headline and §3.4: "only balanced pairs in the middle", "balance forced off both ends into the middle" | **OVERSTATED** | The windows `{0,1,2,3}` and `{4,6,7,8}` plus `{5}` are all of `P_9`. `(2,4)` joins the two gadgets' `u`s, `(2,5)` touches the bottom window, and `(4,5)` touches the top. |
| 3.13 | The range-6 record `11 0 0 2 2 3 b 2b 2f af bf 1ff`: δ = 134/375; balanced pairs `(2,5), (4,5), (4,7), (6,7)`; WIN and BR fail | **HOLDS** | Recomputed: `e = 750`, range 6, width 3. `(4,5)` and `(4,7)` touch no end window, so this record, **not** `P_9`, is the genuine "interior" example. "The range-≤6 census limit of mg-2912" is UNVERIFIABLE; not checked. |
| 3.14 | Census of WIN failures: "1/4/0 at range ≤ 5 (n = 9/10/11), and 4/29 at range ≤ 6 (n = 9/10)" | **1/4/0 HOLDS; 4/29 BROKEN** (it should be 2/18) | The doc's own table and `out_d6.txt` give WIN 2/18 and BR 4/29. Independent recount at `n = 9`: WIN fails in 1 poset at range ≤ 5 and 2 at range ≤ 6 (`P_9` and `9 0 0 2 2 3 b 2b 3b 7f`); BR fails in 1 and 4 (`out_wincount_d*_9.txt`). `n = 10, 11` were only read from the transcripts. |
| 3.15 | "≥ 3 minima ⇒ balanced minimal pair" is FALSE; witness `8 0 0 0 4 4 6 16 2f` | **HOLDS** | Range 6, width 4, `e = 392`, no isolated element. Minima `0, 1, 2`: `P[0<1] = 9/28`, `P[0<2] = 10/49`, `P[1<2] = 65/196 < 1/3`. |
| 3.16 | Counts 8/155/2 622 (`n = 7/8/9`), range ≥ 6, 142/155 and 1 762/2 622 with an isolated element | **HOLDS as reproduced; wording OVERSTATED** | The histogram sums match. The population is **indecomposable** posets with ≥ 3 minima, not "all posets" (`min3.py` skips disconnected `G(P)`). Independent recount at range ≤ 6, `n = 9`: 46, which matches the table. |
| 3.17 | EMPIRICAL: the minimal-pair lemma holds at range ≤ 5 on the census | **HOLDS as labelled** | Independently, `n = 9` at range ≤ 5 gives 0. The doc explicitly declines to conjecture it. |

Notes on 3.1 (Thm 3.1):
- The reduction to a component of `G(P)` is valid, since components are intervals of the linear-sum decomposition and pair laws are unchanged. It needs `P` not a chain, which the doc omits (minor).
- (i) and (ii) are the contrapositives of Thm 2.1 and Cor 2.2, and both are trivially true at `k = 0`.
- (iii) `Inc(x) = C` ⇒ `k = m ≥ 1` ⇒ `3m ≥ m + 1`, a contradiction.
- `u > c_k`: take the largest `i` with `u > c_i`. Then `u` is minimal in `Inc(x) ∖ C_i`, because everything below `u` lies in the ideal `Inc(x)`. That contradicts the uniqueness of `c_{i+1}` whenever `i < k`.
- The two-minima case gives `c_1 = y` (the minima of the ideal `Inc(x)` are minima of `P`). The ≥ 3 case gives `k = 0`.

### §4: census (EMPIRICAL)

| # | claim | verdict | note |
|---|---|---|---|
| 4.1 | Table values | **HOLDS as reproduced** | `summary.py` over the committed transcripts. I independently re-derived the WIN, BR and minimal-pair columns for `d5_9` and `d6_9` (1/1/0 and 2/4/46). I did not re-run the full census (~1 h). |
| 4.2 | 0 violations of Thm 2.1 and Lemma 1.1; the controls fire (1, 4, 16, 46 at `n = 3, 5, 6, 7`; MONO 1 and 30) | **HOLDS** | `out_negctrl.txt`. Those are theorems, so zero is the expected value. The controls show the checker can fail. |
| 4.3 | "At D ≥ 4 the quantitative form adds 5–15 points" | **OVERSTATED (minor)** | From the table: 4.1–5.0 at D = 4, 8.1–8.9 at D = 5, 13.9–14.9 at D = 6. So the range is 4.1–14.9. |
| 4.4 | Coverage 87/73/63/49% and "34% of all posets at `n = 9`" | **HOLDS; wording** | The 34% is of the **indecomposable** posets at `n = 9`. |
| 4.5 | "Everything Linial does not cover is O1 or O2" | **HOLDS** | The proof of Thm 3.1 (ii)–(iii) uses only "LL does not fire at that end". It is not specific to counterexamples. |

### §5: negatives, checked against the candidate space

- (i) WIN from range 5 **HOLDS**.
- (ii) BR from range 5 **HOLDS**.
- (iii) The minimal-pair lemma from range 6 **HOLDS**.
- (iv) "No balanced pair touching an extreme element" **HOLDS**: `6 0 0 2 2 3 f` has minima `{0,1}`, maxima `{4,5}`, and only `(2,3)` balanced.
- (v) The ladder as a pair argument past the branch **HOLDS**, via Lemma 3.3 and the witness, not via the BROKEN inclusion.

All five refute the stated local forms. None of them refutes a "for `n ≥ n_0(D)`" form: every witness has `n ≤ 2D`. The doc states this itself and leaves the long-poset question OPEN. That is correct scoping.

---

## 2. Bounded-range usage (Prop 2.5): the one "route works under bounded range" claim

Setting: `P ∈ Π_D`, `Q` an ideal with `|Q| ≥ max(3D, 2D+1) = 3D` (for `D ≥ 1`), and `x` minimal in `Q`.

- **(a)** Put a linear extension of `Q` first. Then `f(x) ≤ D + 1` by mg-6b81 **Lemma 2.2**, applied to the size-1 ideal `{x}`; hypotheses `P ∈ Π_D`, `{x}` an ideal. Any `b ∉ Q` is at position `≥ 3D + 1`, a gap of `≥ 2D > 2D − 1`, so `b` is comparable to `x` by **Lemma 2.1** (bandwidth; hypothesis `P ∈ Π_D`), and `b > x`. So `Inc_P(x) = Inc_Q(x)`. Both facts are quoted within their hypotheses. **HOLDS.**
- **(b)** An ideal of size `s = m + 1` avoiding `x` avoids `↑x`, so it lies in `Inc(x)`, which has size `m`. That is impossible, so every such ideal contains `x`. The mixture `L ↔ (J, L|_J, L|_{P∖J})` preserves `f(x)` because `x ∈ J`. It is mg-6b81 Lemma 2.3's bijection applied to a position event, which is legitimate: the lemma's hypothesis `x ∥ y` is not needed for the bijection, only for the pair reading. `s + D ≤ 2D + 1 ≤ |Q|`, so by Lemma 2.2 the size-`s` ideals of `P` are exactly those of `Q`. **HOLDS.**
- **(c)** Both conditions are linear in the law of `f(x)` with `t ∈ {1, k}` and `k ≤ m < s`, so they survive the convex combination. Then Thm 2.1 applies in `P`. The result is n-uniform (`Q` is fixed and `P` arbitrary) and pair-agnostic. **HOLDS.**

The D-dependence is correct: the window is `3D`, and the certificate family is the size-`(π(x)+1)` ideals of `Q`. **Whether Prop 2.5 ever certifies anything that mg-e8b4's tree does not was NOT DONE by the author, and not by me either.**

---

## 3. What I did NOT do

- I did not re-run the author's full census (`n = 10, 11` at range 5, `n = 10` at range 6, range 3 and 4, `p3`–`p9`). I recounted only `d5_9` and `d6_9`, with my own code.
- I did not independently recount the per-width LL rates over all 2 534 records. I rechecked only the 44 records with δ < 0.35.
- I did not read Linial 1984. The doc's proof is self-contained, and I re-derived it.
- I did not check the claim "the range-≤6 census limit of mg-2912".
- I did not search for long (`n ≫ D`) WIN/BR counterexamples. That is the doc's own open question, and a case search is out of scope under the 2026-09-26 directive.
- I relied on mg-eedd's generator for completeness of the `n = 9` census files. My control is its A000112 reproduction (`out_gen.txt`) and the indecomposable counts 25 540 and 77 537, which match the doc's table.

## 4. Suggested errata (for a successor; I edited nothing in the subject doc)

1. §3.2: replace the inclusion with `∩_{u∈U}{x before u} = {f(x) ≤ k+1}`, which holds when `U` is all of `min(Inc(x) ∖ C)`. Scope verdict item 5's "is an intersection" to `j* = k`.
2. Verdict 6(a): change "touching" to "inside", and change "4 / 29 at range ≤ 6" to "2 / 18" (4 / 29 are the BR counts). Make the same change in §3.4.
3. Headline, 6(a), §3.4 and the bottom line: `P_9`'s balanced pairs straddle the two end gadgets; there is no middle. Cite the `n = 11` record for genuinely interior balanced pairs.
4. Remark 2.6: drop "`(v_1, v_2) =`", or state it as EMPIRICAL (44/44). Cite KSBFT-A §6 for the value identity.
5. §3.5 and §4: change "all posets" to "indecomposable posets". Change "5–15 points" to "4–15". In Thm 3.1, add "not a chain". Qualify "as it must" (diamond).
