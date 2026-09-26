# KSBFT-T: 1/3–2/3 for interval orders. Status: NOT FOUND in the literature (Chan–Pak's 2023 list stops at semiorders). Brightwell's semiorder proof generalises to ALL posets except one counting step (PROVEN), and that step is the only place unit length enters. In interval orders it fails for the first time at n = 9, on two posets (exact). The failures survive the Swap-Ladder constraints. No proof; the gap is now a single, explicit, purely combinatorial statement (mg-afa4)

Ticket mg-afa4, following mg-cfba (`docs/KSBFT-S-nested-balance.md`).
- The audit mg-ebbe of mg-cfba was still running at dispatch. pm-onethird's mid-run mail relays two of its findings (`docs/AUDIT-mg-cfba.md`):
  - "all hand-built witnesses are interval orders" is OVERSTATED: hub, W8 and the B7 tails contain 2+2;
  - "not found in the literature" HOLDS, while "open" is UNVERIFIABLE.
- I use nothing from mg-cfba except its Lemma 1.1 (non-nested ⟺ doubly 2+2-trapped). I re-derived it (§1).
- From mg-ce69 I use only the Swap Ladder Thm 1.4 and the Doubling Lemma 1.5. Audit mg-6e7c says both HOLD.

**Instrument.** `code/ksbft_t_interval_orders_afa4/` (Python, exact `Fraction`s). `sh run_all.sh` regenerates every transcript.
- It takes about 3 min at 3 processes.
- The population is **all unlabelled interval orders** with n ≤ 10, generated as canonical interval multisets.
- The generator is certified against OEIS A022493: 1, 2, 5, 15, 53, 217, 1014, 5335, 31240, 201608 (`iolib.gen_fast`). It agrees with a naive generator on n ≤ 7.
- Pair laws are cross-checked against brute-force enumeration of linear extensions: 195 posets, 0 mismatches. A planted perturbation is caught (`out_xcheck.txt`).

Ticket rule: computation was used only as an instrument, to probe candidate lemmas and to search for counterexamples to them. The n ≤ 9 and n ≤ 10 interval-order enumerations are 31 240 and 201 608 posets, the populations on which each candidate lemma was tested. They are not an extension of the 1/3–2/3 case census; that is known through n = 14 anyway (Gupta 2026).

**Labels.**
- **PROVEN**: proof in this file.
- **KNOWN**: in the literature, with the source read (as stated).
- **EMPIRICAL**: exact arithmetic over a stated finite population.
- **CONJECTURED**: a guess.

**Conventions.**
- Interval orders use the **canonical representation** (Fishburn): `x ↦ [l(x), r(x)]` with integer endpoints in `1..h`.
  - Every point is the left end of some element and the right end of some element.
  - `x < y ⟺ r(x) < l(y)`.
  - `down(x) = {w : r(w) < l(x)}` and `up(x) = {w : l(w) > r(x)}`.
  - The multiset of canonical intervals is a complete isomorphism invariant.
- `α(p) = #{x : l(x) = p} ≥ 1` and `β(q) = #{x : r(x) = q} ≥ 1`.
- `x` **dominates** `y` if `l(x) ≤ l(y)` and `r(x) ≤ r(y)`. `x` **contains** `y` if `l(x) < l(y) ≤ r(y) < r(x)`, or with one of the two inequalities weak.
- Every incomparable pair is a dominance pair or a containment pair. Semiorders are exactly the interval orders with no strict containment.

---

## 0. Verdict

1. **STATUS: NOT FOUND, so open as far as can be verified (§1).**
   - A literature sub-agent read the following in full: Chan–Pak's survey (arXiv:2311.02743, Thm 13.2 lists 11 known classes), the Wikipedia list, Trotter's 1997 interval-order survey (§11), Brightwell's research page, Zaguia's three papers and their citers. It also saw every title citing Brightwell 1989 (24) and Brightwell 1999 (33), via OpenAlex.
   - Every list names **semiorders** (Brightwell 1989). None names interval orders.
   - No source says the case is open.
   - The one unread place a remark could hide is Brightwell's 1999 survey (paywalled).
   - Partial coverage that does exist: height ≤ 2 (TGF), semiorders, N-free interval orders (Zaguia 2012), and n ≤ 14 (Gupta 2026).
2. **Item 2, why the semiorder proof needs unit intervals (PROVEN, §2).** I read Brightwell's proof through Trotter's verbatim reproduction.
   - **Every step but one holds for every poset.** In a counterexample, the relation "`P[x<y] > 2/3`" is a linear extension `L`. Every `L`-consecutive incomparable pair then has **≥ 2 separators** (Thm 2.1, the Generalised Brightwell Lemma).
   - The semiorder hypothesis is used **only** in the count "each element separates at most one pair from above". That count is equivalent to "every down-set `down(z)` is an `L`-prefix".
   - In an interval order that prefix property is broken exactly by the containment pairs (Prop 2.4).
   - The agent's reading (Trotter's LEM-cycle remark as the obstruction) is **wrong**. LEM cycles are about majority 1/2. The 2/3-relation is always transitive.
3. **The repair attempt, and its exact failure (§3).** The interval form of the separator count is exact (Prop 3.1):
   `|S| = Σ_{p ∈ up-gap} α(p) + Σ_{q ∈ down-gap} β(q)`.
   So a consecutive pair in strict dominance order always has ≥ 2 separators, and only containment steps can be "good". I tested **Claim K**: every linear extension of a non-chain interval order has an `L`-consecutive incomparable pair with ≤ 1 separator. K would **prove 1/3–2/3 for interval orders** via Thm 2.1.
   - **EMPIRICAL:** K holds on **all** interval orders with n ≤ 8, for every linear extension, even without the dominance restriction. It holds on 1 560 random interval orders with n = 10–30.
   - **K is FALSE at n = 9:** exactly 2 of 31 239 non-chain interval orders have a bad `L` (§3.3). At n = 10 it fails on 26 of 201 607 (24 with dominance-respecting `L`).
   - Both n = 9 obstructions **survive** the extra constraints the audited Swap Ladder imposes on a counterexample's `L`. At n = 10, 16 of the 24 survive.
   - **Control:** K fails already at n = 7 on a general poset containing 2+2, so K is genuinely a 2+2-free phenomenon.
   - The random sample missed every obstruction, so random negatives are worthless here.
4. **Item 1, the Swap Ladder in interval terms (PROVEN, §4).**
   - Every incomparable pair starts a ladder: H1 is `l(x) ≤ l(b)`.
   - For a **dominance** pair the ladder is trivial (`W = {b}`, `P ≥ 1/2`).
   - All the content sits on **containment** pairs `x ⊃ b`. There the primal and the dual ladder share the pivot `x`, and run right and left of `b` *inside x's interval* (Cor 4.2).
   - "Full chain" means "the intervals are pairwise disjoint".
5. **Item 3, the (L3) existence question: every natural candidate FAILS (EMPIRICAL, §5).** Counts are over the 5 198 indecomposable twin-free interval orders with n = 9.

   | candidate | fails on |
   |---|---|
   | Ladders from pairs of minimal or maximal elements (this includes the two smallest right endpoints) | 539 |
   | Ladders pivoting inside a down-twin or up-twin class (the interval form of Zaguia's `D(a)=D(b)` pairs) | 7 |
   | A balanced pair consecutive in the `(l,r)` or `(r,l)` lexicographic order (the naive Brightwell pair) | 3 |
   | Zaguia's Thm 3 configurations (no probability needed; they exist in every semiorder, by Brightwell) | 1 / 1 / 3 / 13 at n = 5 / 6 / 7 / 8 |

   The full nested-ladder family never fails. By audit mg-6e7c, "some nested ladder fires" is **equivalent** to 1/3–2/3 via rung 0, so that says nothing.
6. **Item 4, the margin (EMPIRICAL, exact).**
   - **T8 is NOT an interval order.** It contains an induced 2+2 (mg-cfba's own `out_io.txt` says so, and I re-checked it). So do T13, T14 and N12.
   - Over all interval orders with n ≤ 9, the only indecomposable twin-free one at `δ = 1/3` is **2+1**. 2+1 is itself an interval order (a semiorder), so a proof must allow equality anyway.
   - Otherwise, over 4 ≤ n ≤ 9, min `δ` is 14/39 = 0.35897, at n = 7, on a semiorder (the zigzag `[1,1][1,2][2,2][2,3][3,3][3,4][4,4]`; at n = 9 the minimum is 50/139 = 0.35971, again a zigzag). Among non-semiorders, min `δ` is 8/21 = 0.38095, at n = 7 (5/13 at n = 8 and 9).
7. **Verdict.**
   - The interval-order case is **still open**, and I did not prove it.
   - The ticket's route, "find one ladder that starts ≤ 2/3 and ends ≥ 1/3", has no natural candidate that survives n = 9.
   - The most promising route is **Brightwell's, not Zaguia's**. It already reduces the whole problem to *one* combinatorial statement about linear extensions, with no probability left. That statement is true through n = 8 and fails on a sparse, highly structured family (§3.3).
   - What is missing is **one more probabilistic input for pairs with exactly two separators** (§6). That is a well-posed, finite-looking target, and the two n = 9 obstructions are its test cases.

---

## 1. Status (Step 0)

**Sources read (by the literature sub-agent, full text unless stated):**
- **Chan–Pak, arXiv:2311.02743, Thm 13.2 (verbatim):** "(1) width two posets [Lin84], (2) posets with a symmetry [GHP87], (3) semiorders [Bri89] … (4) height two posets [TGF92], (5) |min(P)| > Cn [Fri93], (6) … (7) (ε,δ)-dense … (8) 6-thin posets [Pec08] … (9) series-parallel and N-free posets [Zag12], (10) skew Young diagram posets [OS18], (11) posets whose cover graph is a forest [Zag19]."
  - §11.6, "Interval orders and semiorders", covers only the Fishburn–Trotter extremal count.
  - **Interval orders are absent.**
- **Wikipedia, "1/3–2/3 conjecture":** same classes plus "at most 13 elements" and a 2026 preprint to 14. No interval orders.
- **Trotter, "New perspectives on interval orders and interval graphs" (Surveys in Combinatorics 1997), §11, pp. 255–257:** reproduces Brightwell's proof as Thm 11.4, for semiorders only. It then says only that TGF did height 2, and that Brightwell–Fishburn–Winkler found LEM cycles in interval orders.
  - A survey devoted to interval orders claims balance only for semiorders.
- **Zaguia arXiv:1107.5626, 1610.00809 and 2002.11604; Olson–Sagan; Sah; Gaetz–Gao** (Gaetz–Gao generalise Brightwell to "generalised semiorders", which stay (3+1)-free); **Chen; arXiv:2410.12494; Gupta arXiv:2607.23926.** All say "semiorders". None mentions interval orders.
- **Not accessible:**
  - Brightwell 1989 (Order 5), seen only through Trotter's reproduction;
  - Brightwell 1999 (Discrete Math 201), paywalled;
  - TGF 1992 and Peczarski 2008, titles only;
  - an MSU thesis (HTTP 403).

**Verdict:** NOT FOUND. Consistent with audit mg-ebbe: "not found" HOLDS, "open" is unverifiable.

**Lemma 1.1 (mg-cfba Lemma 1.1, re-derived; PROVEN).** In an interval order every incomparable pair is nested (primal and dual).

*Proof.* `down(x) = {w : r(w) < l(x)}` is monotone in `l(x)`, and `up(x)` is antitone in `r(x)`. □

So on interval orders "some nested pair is balanced" is literally 1/3–2/3.

---

## 2. Brightwell's argument, generalised (answers item 2)

The source is Trotter's verbatim reproduction of Brightwell's Thm 11.4.
- Take a minimum counterexample.
- Define `x <_L y ⟺ P[x > y] < 1/3`, and claim `L` is a linear extension ordering `X` by left endpoints.
- `x_j` *separates* `x_i, x_{i+1}` **from above** if `x_j` covers `x_i` and `x_j ∥ x_{i+1}`, and **from below** if `x_{i+1}` covers `x_j` and `x_j ∥ x_i`.
- "Each `x_j` separates at most two pairs, one from above and one from below", so at most `2n − 4` separations in total. Hence some consecutive pair has ≤ 1 separator.
- Swapping gives an injection `Λ₁ → Λ₃`, so `|Λ₂| > t/3`. A unique separator is then balanced against the pair.

**Theorem 2.1 (Generalised Brightwell Lemma, PROVEN, any finite poset).** Let `P` have no balanced pair.

(a) `x ≺ y :⟺ P[x<y] > 2/3` is a linear order `L` extending `P`.

(b) Let `a ≺ a'` be `L`-consecutive with `a ∥ a'`. Let
`S(a,a') = {z : a ⋖ z, z ∥ a'} ∪ {z : z ⋖ a', z ∥ a}`.
Then `P[a < a' and some z ∈ S lies between them] ≥ 2P[a<a'] − 1 > 1/3`. In particular `|S(a,a')| ≥ 2`.

*Proof.*

(a)
- For `x ∥ y`, exactly one of `P[x<y]`, `P[y<x]` exceeds 2/3. For `x < y`, `P = 1`. So `≺` is a tournament extending `P`.
- A 3-cycle `x≺y≺z≺x` would need `P[x<y] + P[y<z] + P[z<x] > 2`. But no linear extension satisfies all three events, so the sum is ≤ 2.
- A tournament with no 3-cycle is transitive.

(Brightwell needed the representation only to *identify* `L`. Its *existence* is free. The LEM cycles of interval orders are cycles of the 1/2-majority relation, not of the 2/3 relation, so they are no obstruction.)

(b) Split the extensions with `a` before `a'` into `Λ₁` (no element of `S` strictly between them) and `Λ₂` (the rest). Let `Λ₃ = {a' before a}`. For `λ ∈ Λ₁`, swap `a` and `a'`. This is a linear extension:
- Suppose some `w` between them had `a < w`. Take a cover `a ⋖ c ≤ w`; `c` lies between them too. `c < a'` would give `a < a'`, and `c > a'` is impossible by position. So `c ∥ a'` and `c ∈ S`, a contradiction.
- Dually, nothing between them is below `a'`.

The swap is an involution, so `|Λ₁| ≤ |Λ₃|`, and `P(Λ₂) = P[a<a'] − P(Λ₁) ≥ 2P[a<a'] − 1 > 1/3`.
- If `S = ∅`, then `Λ₂ = ∅`, a contradiction.
- If `S = {z}` with `a ⋖ z`, then `Λ₂ ⊆ {z before a'}`. So `P[z<a'] > 1/3`, hence `> 2/3`, i.e. `z ≺ a'`. But `a ≺ z` because `a < z`. So `z` lies strictly between the consecutive pair `a ≺ a'`, a contradiction.
- The below case is dual. □

*Check.* The injection (b) is tested exactly for every ordered incomparable pair of every interval order with n ≤ 6: 292 posets, 0 violations. **Control:** with only above-separators in `S`, it fails on 653 pairs (`out_brightwell.txt`).

**Corollary 2.2 (PROVEN).** 1/3–2/3 holds for every poset `P` whose linear extensions all have an `L`-consecutive incomparable pair with ≤ 1 separator ("Brightwell-good"). It suffices to check the `L` that also put `x` before `y` whenever `down(x) ⊆ down(y)` and `up(x) ⊇ up(y)` (the swap gives `P[x<y] ≥ 1/2`, hence `x ≺ y`), and the other constraints of §3.4.

**Where the semiorder hypothesis is used: exactly one place.** Brightwell's `L` restricted to the semiorder is the canonical order. The count "`x_j` separates at most one pair from above" holds because `down(x_j)` is an `L`-prefix: a separation from above is an exit from `down(x_j)` into a non-member.
- (Trotter's text also uses minimality to make all `L`-consecutive pairs incomparable. That fails in interval orders, but it is harmless: comparable consecutive pairs just drop out of the count. See `out_bwstats.txt`, HC.)

**Proposition 2.4 (PROVEN).** Let `P` be an interval order, and let `L` put `x` before `y` for every dominance pair (`l(x) ≤ l(y)`, `r(x) ≤ r(y)`, `x ∥ y`, intervals distinct). A counterexample's `L` is such an `L`: the swap gives `P ≥ 1/2`. Then:
- every down-set `down(z)` is an `L`-prefix iff no containment pair `y ⊃ x` has `y` before `x`;
- every up-set is an `L`-suffix iff no containment pair `y ⊃ x` has `x` before `y`.

So both hold iff `P` has no strict containment, i.e. `P` is a semiorder.

*Proof.* `down(z) = {c : r(c) < l(z)}`. Its prefix property fails iff some `y` with `r(y) ≥ l(z)` precedes some `x` with `r(x) < l(z)`. Such `x`, `y` are incomparable, and since `L` respects dominance we must have `l(y) < l(x)` (strictly: `r(x) < r(y)`, and `l(y) ≥ l(x)` would make `x` dominate `y`). So `y ⊃ x`. Conversely, a containment `y ⊃ x` with `y` first breaks `down(z)` for any `z` with `r(x) < l(z) ≤ r(y)`. Such a `z` exists canonically, because the point `r(x)+1` is a left endpoint. Up-sets are dual. A containment pair must break one side whichever way `L` orders it. □

So Brightwell's argument does not need unit length as such. It needs `L` to respect **both** chains of down-sets and up-sets. Interval orders keep both chains (that is 2+2-freeness) but lose their compatibility (that is 3+1).

---

## 3. The repair attempt: Claim K

### 3.1 The separator count in interval terms (PROVEN)

Write `L = v_1 … v_n` with `v_i = [l_i, r_i]`. Step `i` is incomparable iff `l_{i+1} ≤ r_i` (a linear extension never has `v_{i+1} < v_i`). Put
- `ρ(p) = min{r(c) : l(c) > p}`;
- `λ(q) = max{l(c) : r(c) < q}`.

**Proposition 3.1.** For an incomparable step `i`, `|S(v_i, v_{i+1})| = A_i + B_i`, where
- `A_i = Σ_{p ∈ (r_i, min(r_{i+1}, ρ(r_i))]} α(p)` (above-separators: the minimal elements of `up(v_i) ∖ up(v_{i+1})`);
- `B_i = Σ_{q ∈ [max(l_i, λ(l_{i+1})), l_{i+1})} β(q)` (below-separators: the maximal elements of `down(v_{i+1}) ∖ down(v_i)`).

*Proof.*
- `a ⋖ z ⟺ r(a) < l(z) ≤ ρ(r(a))`: `z` is minimal in `up(a) = {l > r(a)}`.
- For `z ∈ up(a)`, `z ∥ a'` iff `l(z) ≤ r(a')`, since `z` comes after `a'` and is not below it.
- Below-separators are dual. □

This is checked against direct counting on every incomparable step of every linear extension of every interval order with n ≤ 7: 0 mismatches (`gaps.py`).

**Corollary 3.2 (PROVEN).** Since `α, β ≥ 1`, a step with `l_i < l_{i+1}` and `r_i < r_{i+1}` has `|S| ≥ 2`. Hence a step with `|S| ≤ 1` is one of:
- (i) `v_{i+1}` dominates `v_i`, including twins: `|S| = 0`;
- (ii) `v_{i+1} ⊇ v_i` with `l_{i+1} ≤ l_i`, `A_i = 1` (so exactly one element starts at `r_i + 1`, and `r_{i+1} = r_i + 1` or `ρ(r_i) = r_i + 1`);
- (iii) the mirror image, `v_i ⊇ v_{i+1}` with `B_i = 1`.

Under a dominance-respecting `L` without twins, (i) cannot occur. **The good pairs are all containment steps, or steps inside a twin class.** In a semiorder they are steps with equal `l` or equal `r`, which is where Brightwell's count finds them.

### 3.2 Claim K and the evidence for it

> **Claim K.** Let `P` be an interval order that is not a chain. Every linear extension `L` of `P` (it would suffice: every dominance-respecting `L`) has an `L`-consecutive incomparable pair with at most one separator.

By Cor 2.2, K ⟹ **1/3–2/3 for interval orders**. So K was worth attacking directly.
- **EMPIRICAL, n ≤ 8:** K holds for **every** linear extension of **every** interval order with n ≤ 8, with no dominance restriction and including decomposable posets and twins (`out_bwhyp.txt`; `kdfs.py`, an exact prefix-pruned search, `out_kdfs.txt`). Brightwell's cruder count `T ≤ 2m − 2` fails already at n = 7 (`out_bwstats.txt`, HT), but `T ≤ 2m − 1` held throughout n ≤ 7 (`out_bwinc.txt`, `out_onesided.txt`). Here `T` is the total number of separations and `m` the number of incomparable steps.
- **CONTROL (general posets):** the same search finds bad linear extensions for posets **with** 2+2 already at n = 7. The first hit is `{0<1,0<5,0<6,1<6,2<5,3<4,3<6}`, `L = 0 3 2 1 4 5 6` (`out_bwgeneral.txt`). So K is not a triviality, and it really uses 2+2-freeness.
- **Structure:** Brightwell's per-element bound fails in interval orders. Over all linear extensions (twins and non-dominance `L` included), one element can separate up to 3 pairs from above at n = 7 (`out_bwinc.txt`), and the up-gaps of distinct pairs can overlap even under dominance (`out_gaps.txt`). What held through n = 7 is only the global inequality: `T_up ≤ m` and `T_down ≤ m` for dominance-respecting `L`, never with both equal (`out_onesided.txt`). Both one-sided bounds fail for non-dominance `L` (25 cases each at n = 7).
- **Ruled out as proof routes** (`out_bwrefine.txt`, `out_bwrules.txt`, `out_tight.txt`):
  - "the first or last incomparable step is good" fails at n = 5;
  - "≥ 2 good pairs" (Brightwell's "in fact, at least two") fails at n = 7, with 2 (P, L) having exactly one good pair;
  - the one-sided forms "a good pair with `A = 0`" and "a good pair with `B = 0`" fail at n = 6;
  - nine extremal selection rules (max `r(a)`, min `l(a')`, max overlap, …) all fail at n = 4–5.

### 3.3 K is false: the n = 9 obstructions (EMPIRICAL, exact, `out_kdfs.txt`, `out_obstruction.txt`)

The exact search over all 31 239 non-chain interval orders with n = 9 finds **exactly two** with a bad dominance-respecting `L`:
- **O9a** = `[1,1] [1,2] [1,5] [2,3] [2,6] [3,4] [4,5] [5,6] [6,6]`, `L = [1,1] [1,2] [2,3] [1,5] [3,4] [2,6] [4,5] [5,6] [6,6]`;
- **O9b** = `[1,1] [1,2] [2,3] [2,6] [3,4] [4,5] [5,6] [6,7] [7,7]`, `L = [1,1] [1,2] [2,3] [3,4] [2,6] [4,5] [5,6] [6,7] [7,7]`.

Both are a **unit staircase** `[1,1] [1,2] [2,3] …` (the path semiorder, in which each interval overlaps only its neighbours; it attains the interval-order minimum `δ` = 5/13 at n = 6 and 13/34 at n = 8) with one or two **long intervals** inserted. `L` places each long interval in the middle of the staircase it contains. O9a is self-dual, and every one of its steps has exactly 2 separators, e.g. `([2,3], [1,5])` has separators `[4,5], [5,6]`.

At n = 10 there are 26 posets with a bad `L` (24 with a dominance-respecting one). The 2 + 24 posets with a bad dominance-respecting `L` have the same shape: 1–3 intervals of canonical length ≥ 2, every other interval of length ≤ 1, and all contain 3+1 (checked; `out_kladder.txt` lists them). The 1 560 random interval orders with n = 10–30 contained **none**. The obstruction family is sparse, so random search says nothing about it.

These posets are nowhere near counterexamples:
- `δ(O9a) = 228/515 ≈ 0.443` and `δ(O9b) = 22/53 ≈ 0.415`;
- the "bad" `L` disagrees with their true 2/3-relation. For instance `P[[1,1] < [1,2]] = 0.655` is itself balanced.

So the obstruction is an artefact of the *method* (the `L`-sequence is taken as arbitrary), not a near-counterexample.

### 3.4 Adding the audited Swap-Ladder constraints does not kill them (EMPIRICAL, `out_kladder.txt`)

A counterexample's `L` must also satisfy, for every nested `(x; b)` with chain bottom `b_0 < … < b_m` of `↑b ∖ ↑x` (mg-ce69 Thm 1.4, audit mg-6e7c HOLDS):
- **(SL1)** if `b ≺ x` then `b_m ≺ x`. Otherwise the first crossing is balanced, since steps are ≤ `t_0 < 1/3`.
- **(SL2)** if `↑b ∖ ↑x` is a chain, then `x ≺ b`.
- The duals of both.

Results:
- n = 9: both obstructions **survive** (O9a, O9b).
- n = 10: of 24 posets with 29 bad dominance-respecting `L`, **16 posets and 20 `L` survive**.

So "Brightwell + Swap Ladder + dominance", all purely combinatorial constraints on `L`, still does not prove the interval case.

---

## 4. Item 1: the Swap Ladder in interval language (PROVEN; restatement of mg-ce69 Thm 1.4)

Let `x ∥ b` in an interval order, oriented so that `l(x) ≤ l(b)`. This is H1, `down(x) ⊆ down(b)`, and it always holds in one orientation (Lemma 1.1).

- **Dominance case, `r(x) ≤ r(b)`:** `W = ↑b ∖ ↑x = {b}`, which is full. The ladder says only `P[x<b] ≥ 1/2`. **All the content is "`P[x<b] ≤ 2/3`"**, which no ladder supplies.
- **Containment case, `r(b) < r(x)`:** `W = {b} ∪ Z` with `Z = {z : r(b) < l(z) ≤ r(x)}`. These are the elements above `b` that still lie inside `x`'s interval, and all of them are incomparable to `x`. The chain bottom is `b_1 = ` the unique element of `Z` whose left end is ≤ `min_{w∈Z} r(w)` (if unique), and so on recursively.
  - "Full" (Zaguia's good pair) ⟺ the intervals of `Z` are pairwise disjoint.
  - "The chain bottom reaches 1/3" is a statement about the leftmost part of `Z` being a staircase of disjoint intervals.

**Corollary 4.2 (two-sided ladder, PROVEN from Thm 1.4 and its dual).** If `x ⊃ b` (strict containment), the same pivot `x` carries two ladders through `b`:
- the primal one, through `Z_right = {z : r(b) < l(z) ≤ r(x)}`;
- the dual one, through `Z_left = {z : l(x) ≤ r(z) < l(b)}`.

The steps of `x`'s position are non-increasing moving away from `b` in **both** directions. If both `Z_left` and `Z_right` are chains (disjoint intervals), then `(x; b)` or its dual is a Zaguia good pair with probability ≤ 1/2, so **some `(x, ·)` is balanced with no probabilistic hypothesis**. The other orientation has `P[b<x] = 1 − P[x<b]`.
- (This is Zaguia's Thm 2 applied in `P` or its dual; KNOWN-equivalent.)

**Down-twin classes.** `L_p = {x : l(x) = p}` has all members with equal down-sets, and nested up-sets ordered by `r`.
- Doubling (mg-ce69 Lemma 1.5) applies to every pair in `L_p`: for `r(x) < r(y)`, if `{z : r(x) < l(z) ≤ r(y)}` has a unique minimal element `b_1`, then `P[y < b_1] = 2P[y < x]`.
- In a counterexample every such pair has `P[y<x] < 1/6` whenever `b_1` exists (mg-cfba Lemma 2.1).
- Up-twin classes `R_q = {x : r(x) = q}` behave dually.

---

## 5. Item 3: (L3)-type existence, candidate by candidate (EMPIRICAL, `out_probe8.txt`, `out_probe9.txt`, `out_zaguia3.txt`)

Population: all indecomposable twin-free interval orders.
- A ladder "fires" when its first rung is ≤ 2/3 and its chain bottom reaches 1/3, or it is full with `t_0 < 1/3`.
- Counts are failures, at n = 7 / 8 / 9, out of 160 / 866 / 5 198 posets.

| candidate | fails | smallest failure |
|---|---|---|
| C1: a pair of minimal elements, or of maximal elements, is balanced | 31 / 169 / 934 | n = 5 (`[1,1][1,2][2,2][2,3][3,3]`, `δ = 4/11`) |
| **L1: a ladder pivoting on two minimal (or two maximal) elements fires.** This includes the ticket's "two smallest right endpoints" `[1,1]`, `m_2`. | 15 / 92 / 539 | n = 5 |
| C2: a balanced pair with equal `l` or equal `r` | 11 / 41 / 163 | n = 5 |
| **L2: a ladder pivoting inside a down-twin or up-twin class fires** (Zaguia/Doubling pairs, chain-bottom form) | 1 / 1 / 7 | n = 7: `[1,1][1,3][2,2][2,4][3,5][4,4][5,5]` |
| C7: some pair consecutive in `(l,r)` or `(r,l)` lexicographic order is balanced | 1 / 1 / 3 | n = 7: `[1,1][1,6][2,2]…[6,6]` (a 6-chain plus a long interval) |
| Zaguia Thm 3 (i)–(iii) configuration exists (certifies balance with no probability) | 3 / 13 / – | n = 5: `[1,1][1,4][2,2][3,3][4,4]` |
| L3: some nested ladder fires | 0 / 0 / 0 | — (≡ 1/3–2/3, audit mg-6e7c) |

- The Zaguia-Thm-3 count is **0 on semiorders** at every n. That is the positive control: Brightwell's pair is a Thm 3(i) configuration.
- The smallest C7 and Zaguia-3 failures are a chain plus one interval spanning it (width 2, so Linial covers them). The larger ones are not: the n = 9 C7 failure `[1,1][1,4][1,7][2,2][3,3][4,7][5,5][6,6][7,7]` has width 3.

**Reading.**
- The linear order of down-sets makes **every** pair ladder-eligible. But the ladder's *start* condition ("≤ 2/3") is exactly as hard as before on dominance pairs, and those carry the balance in most small interval orders (C8 in `out_probe*.txt`: balanced dominance pairs are missing on only 128/5 198 at n = 9, and balanced containment pairs on 97).
- No single canonical pair works. The failures of L2 at n = 7–9 show that even the twin classes, where Doubling holds, cannot be the whole story.
- Brightwell's approach is different in kind. It never chooses a pair; it uses the *whole* 2/3-order `L` and a count, which is why it gets further (n ≤ 8 with no failure).

---

## 6. What would finish it (CONJECTURED directions)

The gap is now exactly this. In a counterexample interval order, every `L`-consecutive incomparable pair has ≥ 2 separators (Thm 2.1). Those configurations exist (§3.3), so a proof needs **one more probabilistic lemma for pairs with exactly two separators**. In O9a every step has exactly 2. Candidates, in order of plausibility:
1. **Two above-separators `z_1, z_2` (both covering `a`, both `∥ a'`).** In an interval order they have `l(z_k) ∈ (r(a), r(a')]`, so they are comparable in dominance or containment. If `z_1` dominates `z_2`, then `{z_2 between a and a'} ⊆ {z_1 before a'}`, up to an injection. That would give `P(Λ₂) ≤ 2·P[z_1 < a']`, which only yields `P[z_1<a'] > 1/6`. A sharper injection, swapping `a'` with the earlier of the `z`'s, is the natural next step. Not attempted.
2. **One above- and one below-separator `z, w`.** 2+2-freeness forces `w < z` (else `{a<z, w<a'}` is an induced 2+2). So `Λ₂` splits into `w`-between and `z`-between events, which are linked through the chain `w < z`.
3. **Use more than one step.** In O9a, consecutive steps share separators (e.g. `[1,1]`, `[1,2]` appear twice). A count over two adjacent steps may close it.

Any such lemma is testable against O9a, O9b and the 20 n = 10 survivors: it must make every one of their `L` inconsistent.

---

## 7. What I did NOT do

- **Did not prove 1/3–2/3 for interval orders**, nor Claim K (which is false), nor any strengthening of Thm 2.1 for two separators (§6).
- Did not read Brightwell 1989 or 1999 myself. Thm 2.1 follows Trotter's reproduction; the sub-agent transcribed it verbatim and I re-derived every step. The generalisation to arbitrary posets and the remark that part (a) needs no hypothesis are mine. They are elementary, and may well be folklore. **Novelty is not claimed.**
- Did not read Gaetz–Gao's "generalised semiorders" myself. The sub-agent reports that the class stays (3+1)-free; if so, it cannot contain O9a/O9b, which contain 3+1 (checked). Unverified.
- The Brightwell-bad search is exact on the census (n ≤ 10) but **random above**. The random sample provably missed the obstruction family. Nothing is claimed for n ≥ 11 beyond that the obstruction family persists at n = 10.
- `onesided.py`, `bwinc.py`, `gaps.py` and `bwrefine.py` ran on n ≤ 7 only.
- Did not test Claim K or Thm 2.1 on the bounded-range environment (range ≥ 8). Interval orders of large range are exactly the long staircases with long intervals, the obstruction shape.

## 8. Files (`code/ksbft_t_interval_orders_afa4/`)

| file | content |
|---|---|
| `iolib.py` | canonical generator (OEIS-certified), exact pair laws over the ideal lattice |
| `xcheck.py` | laws vs brute force, planted-error control, 2+2 status of T8 / T13 / T14 / N12 / P9 |
| `probe.py` | §5 candidate families (`out_probe8.txt`, `out_probe9.txt`) |
| `brightwell.py` | Thm 2.1(b) injection with control; bad-`L` enumeration n ≤ 8 |
| `bwstats.py`, `bwhyp.py`, `bwinc.py`, `bwrules.py`, `bwrefine.py`, `onesided.py`, `tight.py`, `gaps.py` | §3.2 structure and ruled-out routes |
| `bwgeneral.py` | control: bad `L` on general posets with 2+2 |
| `kdfs.py` | exact bad-`L` search, census n ≤ 10 and random n ≤ 30 (§3.3) |
| `kladder.py` | Swap-Ladder constraints on the bad `L` (§3.4) |
| `obstruction.py` | O9a/O9b, step by step |
| `zaguia3.py` | Zaguia Thm 3 configurations, semiorder control |
| `run_all.sh` | regenerates all `out_*.txt` |
