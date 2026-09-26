# AUDIT of mg-eedd (KSBFT-J, `docs/KSBFT-J-one-pt.md`): mg-95d3

Auditor: an independent polecat with fresh context. I am not the author. The subject is
`docs/KSBFT-J-one-pt.md` and `code/ksbft_one_pt/` as of `fada736`/`7a1866d`. The KSBFT PDF was
**not** consulted. None of the audited claims consumes it: the note uses no KSBFT lemma, and I checked that.

Verdict scale: **HOLDS** (re-derived here, or re-computed independently), **BROKEN** (false as
stated), **OVERSTATED** (the true content is weaker than the words), **UNVERIFIABLE**.
Labels on my own statements: **PROVEN** (proof in this file), **PROVEN (computer)**, **EMPIRICAL**,
**CONJECTURED**.

Instrument: `code/audit_ksbft_95d3/`. Run `sh run_all.sh`. It takes ~4 min, runs at most 3 processes,
and ends with `check_95d3.py`, which exits non-zero on any failed expectation or silent control.
It prints `RESULT: GREEN` (`out_check_95d3.txt`, 35 checks). I wrote it from the *statements* in
the note. I read `onept.c` only for its header comment (modes and file format), after mine was
written. The design is deliberately different:

| | mg-eedd `onept.c` | this audit `indep_95d3.c` |
|---|---|---|
| augmentation | add a new **maximal** element (down-set = any ideal) | add a new **minimal** element (up-set = any filter) |
| dedup | canonical form: least relation matrix over an individualisation–refinement tree | **no canonical form**: bucket by a 64-bit refinement-hash invariant, then an exact backtracking isomorphism test inside the bucket |
| pair count | accumulated when the earlier element `x` is placed | accumulated when the later element `y` is placed |
| arithmetic | `unsigned __int128` | `unsigned __int128`; the Lemma R sharpness family uses Python `Fraction` with its own DP |

Controls, each of which fires:
- **Class counts.** The counts equal OEIS A000112 for n ≤ 10.
- **Counter.** The counter equals brute-force permutation counts on 1 970 posets (random P and every P − v, n = 6, 7, 8). Its control runs brute force on a modified poset and must mismatch. It does: 470/480, `FIRES`.
- **Lemma R.** The window with `r = π(v)` in place of `π(v)+1` is violated millions of times.
- **Narrow interval.** With the interval narrowed to `[2/5, 3/5]`, exists-v fails, and Prop 1.2's equivalence breaks on indecomposable posets but not on decomposable ones.
- **Π₂ classification.** The classifier finds "other" posets in range ≤ 3.
- **Checker.** `check_95d3.py` goes RED when one census `exists_v_fail=0` is mutated to 1. I did this by hand and it is not in `run_all.sh`.

---

## 0. Headline

| # | claim (mg-eedd) | verdict |
|---|---|---|
| 1 | Prop 1.2: for decomposable `P`, (ONE-PT)(P) ⟺ δ(P) ≥ 1/3 (and Lemma 1.1) | **HOLDS.** Re-derived (§1). Exact check: 0 mismatches on all 431 816 decomposable non-chains with n ≤ 10, at `[1/3,2/3]` and at `[2/5,3/5]`. |
| 2a | Lemma R: reweighting by `w_v ∈ [1, π(v)+1]`, window, `\|p−p'\| ≤ (√r−1)/(√r+1)` | **HOLDS.** Re-derived (§2). 0 violations in 675.7 M distinct exact checks (all non-chains n ≤ 10, range ≤ 4 n = 11..13, range ≤ 3 n = 14..16). |
| 2b | "sharp at π(v) = 1" | **HOLDS, but it was EMPIRICAL in the source.** The note infers the supremum from census values ("Pell-type approximants, so the bound is the supremum"), which is not a proof. The commit subject files it under PROVEN. **I prove it here** with an explicit family (§2.2) that reproduces the census's values 6/35, 35/204, …, 40391/235416 exactly. |
| 3 | Lemma 4.2: indecomposable `Π₂` = {A₃, 2+2, F_n}; Lemma 4.4 `e(F_m) = f(m+1)`; Thms 4.1, 4.3 (canonical form) | **HOLDS.** Every step was re-derived (§3), and **the classification is complete**. Independently, the exhaustive range ≤ 2 classes to n = 14 are exactly {A₃, F₃}, {2+2, F₄}, and {F_n} for n = 5..14. The classifier's control fires on range 3. |
| 4a | generation is complete (indecomposable, up to isomorphism) | **HOLDS.** The argument re-derives (§4.1). My generator uses a different augmentation and a different dedup, and reproduces **every** class count: A000112 to n = 10, range ≤ 3 to n = 16 (…, 1 525 168, 4 320 980), range ≤ 4 to n = 13 (178 811, 666 778, 2 490 595). |
| 4b | exists-v: 0 failures on all non-chains n ≤ 10 (2 769 953), on indec range ≤ 3 n = 11..16 (129 683), and on indec range ≤ 4 n = 11..13 (839 679) | **HOLDS.** Re-computed on the same populations with identical sizes: 0 failures. I went past the requested n ≤ 13 and covered everything the note claims. |
| 4c | Thm 4.5: (ONE-PT₃) for n ≤ 16, (ONE-PT₄) for n ≤ 13, PROVEN (computer). The n ≥ 11 restriction to indecomposable classes matches Prop 1.2. | **HOLDS** (§4.2). |
| 4d | "every min-range v works" fails only on `A₁ + C₃` | **HOLDS.** It fails on exactly one class, `4 6 4 0 0`, in all n ≤ 10 and in every range-restricted class. |
| 5a | obstruction numbers: crude transport 0.1716 vs margins ≈ 0.016 at range 3 (n = 11..16), a factor of ~10 | **HOLDS.** Every worst margin and canonical margin at n = 11..16 re-computes to the same fraction (§5). §2.2 strengthens it: Lemma R cannot be improved in the worst case at π(v) = 1. |
| 5b | "a proof **needs** covariance decay plus a margin hypothesis" | **OVERSTATED.** This is an analysis of one route (canonical `v`, transport a pair of `P − v`), not a necessity. The note concedes this in §7 but not in §0 item 5. |
| 5c | "margin bounded away from 0 in every class computed: ≥ 1/51 for all n ≤ 10"; "canonical margin down to 1/159" | **BROKEN**, by the note's own transcripts (§5.2). The margin is **0** at indecomposable n = 3, 4 (F₃, 2+2) and at every n for decomposable posets. It is **5/318 < 1/51** at indecomposable n = 10. The canonical margin is **0** at indecomposable n = 5, 6, 8, including range ≤ 3 at n = 6. |
| 5d | "`F_m` satisfies [the margin route] with `μ₂ = 1/φ² − 1/3`" | **BROKEN as a bound.** It holds only as a limit. `F₅` has margin 1/24 = 0.0417, and every odd `m` is below 0.04863. `F₃` has margin 0 (§5.3). |

Net: every **proof** in the note holds. The **computer proofs** hold and were independently
regenerated in full. The one "PROVEN" item that had no proof, the sharpness of Lemma R, is now
proven. What is wrong is the **margin headline**, which is contradicted by the note's own data,
and a stated `μ₂` that is a limit, not a lower bound. This weakens the evidence behind §5's
"margin exists" in exactly one way: any margin hypothesis for an induction has to exclude small
base cases, because margins are exactly 0 there.

---

## 1. Decomposable reduction (claim 1): HOLDS

**Lemma 1.1, re-derived.** Take `x' ∉ C` and `x ∥ y` in `C`. If `x < x'` and `x' < y`, then
`x < y`, a contradiction. So `x < x'` implies `y < x'`, since `x'` and `y` lie in different
components and are therefore comparable. By connectivity of `C`, `C < x'`. For `y'` adjacent to
`x'` in `G`, and `c ∈ C`: `y' < c < x'` would contradict `x' ∥ y'`, so `c < y'`. By connectivity
of `C'`, `C < C'`. The component order is total and transitive (it is the order on
representatives). A linear extension of `A ⊕ B` is one of `A` followed by one of `B`, so
within-summand probabilities are those of the summand. ✔

**Prop 1.2, re-derived.**
- (⟹) ONE-PT gives a pair balanced in `P`, and "balanced" is exactly the closed-interval event, so δ(P) ≥ 1/3.
- (⟸) The balanced pair lies in a summand `S`. Decomposable means some other summand `S'` exists. Deleting `v ∈ S'` leaves an ordinal sum still containing `S` unchanged, so the pair's probability is unchanged. The proof never uses the value 1/3, so the equivalence holds for **any** interval `[λ, 1−λ]`. ✔

**Corollary.** (ONE-PT_D) ⟺ [conjecture on Π_D] ∧ [ONE-PT on indecomposable Π_D]. This holds
because every summand of `P ∈ Π_D` is in `Π_D`: an incomparable pair lies within one summand,
so `π` computed in the summand equals `π` in `P`. ✔

**Exact check (EMPIRICAL, instrument above).** On all 431 816 decomposable non-chains with
n ≤ 10, `exists-v ⟺ (∃ balanced pair)` has 0 mismatches. Under `[2/5,3/5]` it still has 0
mismatches on decomposable posets (n ≤ 8). On indecomposable posets the equivalence **does**
break (2 at n = 4, 4 at n = 8), which shows the test can fire (`out_control_narrow_95d3.txt`).

## 2. Lemma R (claim 2)

### 2.1 The bound: HOLDS

Re-derived independently:
- **Slot count.** For `L' ∈ L(P−v)`, `v` can be inserted exactly in the slots after the last element of `down(v)` and before the first element of `up(v)`. Every `down(v)` element precedes every `up(v)` element (`d < v < u`), so `b > a` and there are `b − a ≥ 1` slots.
- **Upper bound on `w_v`.** The `b − a − 1` elements strictly inside are in neither `down(v)` nor `up(v)`, so they are incomparable to `v`. Hence `w_v ≤ π(v)+1`.
- **Reweighting.** The map `L(P) → L(P−v)` has fibre size `w_v(L')`, so `P_P[E] = E'[w 1_E]/E'[w]` for `E` measurable in the order of `P − v`.
- **Window.** The extremal ratio has weight `r` on `E` and 1 off it, which gives `rp'/(rp'+1−p')` and the mirror bound.
- **Maximising the gap.** `g(p') = p'(1−p')(r−1)/(1+(r−1)p')`, and `g' = 0 ⟺ (r−1)p'² + 2p' − 1 = 0`, whose root is `p' = 1/(1+√r)`. There `g = (√r−1)/(√r+1)`. I checked the algebra: `1+(r−1)/(1+s) = s` for `s = √r`. ✔

**Exact check.** Every `(P, v, pair)` in every population of §4 was tested: 462 393 584 checks
at n = 10 (all non-chains), 123 660 152 at range ≤ 4 with n = 13, and more. There are 0 violations.
The `r = π(v)` control fires in every block.
- Nit: the note's "408 million checks at n = 10" is the *indecomposable* count (407 890 520, reproduced exactly). The all-non-chain count is 462 393 584, which also equals the author's `out_census_all.txt`.

### 2.2 Sharpness at π(v) = 1: HOLDS, with the proof the note lacks (PROVEN here)

**Proposition S.** Let `Q(a,b)` be the disjoint union of a chain `A` of `a` elements with top `x`
and a chain `B` of `b` elements with top `z`. Let `P(a,b) = Q(a,b) ∪ {v}` with `v > q` for every
`q ≠ z`, and `v ∥ z`. Then `π(v) = 1`, `P − v = Q(a,b)`, and

`p' := P_Q[x before z] = b/(a+b)`,  `p := P_P[x before z] = 2p'/(1+p')`,  `p − p' = p'(1−p')/(1+p')`.

Choosing `b/(a+b) → √2 − 1` gives `p − p' → 3 − 2√2`. So the Lemma R bound at `r = 2` is the
supremum. It is not attained, because `√2 − 1` is irrational.

*Proof.* `v` is comparable to everything except `z`, so `π(v) = 1`. In `L' ∈ L(Q)` the last
element is maximal, so it is `x` or `z`.
- `down(v) = Q ∖ {z}` and `up(v) = ∅`. So `w_v(L') = 2` if `z` is last, i.e. `v` may go before or after `z`, and `w_v = 1` otherwise.
- `z` is last iff `x` precedes `z`. If `x` precedes `z`, then every element of `A` precedes `x`, and every element of `B` precedes `z`. Conversely, if `z` is last, `x` precedes it.
- So `w_v = 1 + 1{x before z}` exactly.
- By Lemma R(2), `p = 2p'/(2p' + 1 − p') = 2p'/(1+p')`.
- The last element of a uniform interleaving of two chains comes from `B` with probability `b/(a+b)`, so `p' = b/(a+b)`.
- Then `p − p' = p'(1−p')/(1+p') = g(p')` at `r = 2`, and `g(√2−1) = 3 − 2√2`. Rationals `b/(a+b)` are dense in (0,1). □

Check (`out_sharp_95d3.txt`, exact Fractions with an independent DP): the closed form matches for
10 pairs `(a,b)` up to n = 30. The control, making `v > z` too, gives `p = p'` every time.

With `b/(a+b)` = Pell convergents `P_k/P_{k+1}`, the gaps are 6/35, 35/204, 204/1189, 1189/6930,
6930/40391, 40391/235416. **These are exactly the census maxima** reported by mg-eedd and by me.
The census witnesses are bounded-range relatives of the same mechanism: `w_v = 1 + 1_E` with
`P'(E) → √2 − 1`.

Not settled: whether the bound is sharp for `π(v) ≥ 2`. The note does not claim it. Its observed
maxima are 0.21 vs 0.268 at π(v) = 2, which I reproduce: 0.2078 at n = 8, all.

## 3. Π₂ classification and ONE-PT₁/₂ (claim 3): HOLDS, and the classification is complete

**Lemma 4.2**, re-derived step by step:
- `π(P) ≤ 2` with `G(P)` connected means `G` has maximum degree ≤ 2, so it is a path or a cycle. Non-edges are comparable pairs.
- **Propagation.** Assume `u_i < u_{i+2}`, and that `{i,i+3}` and `{i+1,i+3}` are non-edges. Then:
  - `u_{i+3} < u_{i+1}` is impossible. If `u_{i+3} < u_i`, then `u_{i+3} < u_{i+2}`, contradicting `u_{i+2} ∥ u_{i+3}`. If `u_i < u_{i+3}`, then `u_i < u_{i+1}`, contradicting `u_i ∥ u_{i+1}`.
  - So `u_{i+1} < u_{i+3}`.
  - `u_{i+3} < u_i` would give `u_{i+1} < u_i`, so `u_i < u_{i+3}`. ✔
- **Path.** After dualising, `u₁ < u₃`. By induction `u_i < u_{i+2}` for all `i`, and steps of 2 and 3 reach every `j ≥ i+2`. So `P = F_n`. For n = 3 this gives `F₃`, which is `A₁ + C₂`. ✔
- **Cycle.** The only extra edge is `{1,n}`. `{i+1,i+3} = {1,n}` needs n = 3, and `{i,i+3} = {1,n}` needs n = 4.
  - For n ≥ 5 all steps apply, which gives `u₁ < u_n`, contradicting the edge `{1,n}`. ✔
  - n = 4: the comparable pairs are exactly `{1,3}` and `{2,4}`, so `P` is 2+2. ✔
  - n = 3: `A₃`. ✔
- No family is missed. Nothing else has a connected graph of maximum degree ≤ 2.

**Exhaustive confirmation (PROVEN (computer) for n ≤ 14).** Every indecomposable range ≤ 2 class
from my generator is classified in `out_classify_pi2_95d3.txt`. The result is n = 3: {A₃, F₃};
n = 4: {2+2, F₄}; n = 5..14: {F_n} only. There are 0 "other". The control (range ≤ 3, n ≤ 8)
reports 238 "other" classes: `FIRES`.

**Lemma 4.4** (`e(F_m) = f(m+1)`, `P[x₂ before x₁] = f(m−1)/f(m+1) ∈ [1/3, 1/2]`), re-derived:
- The first element is `x₁` or `x₂`. If it is `x₂`, then `x₁` is the only minimal element left.
- The bounds follow from `2f(k−1) ≤ f(k+1) ≤ 3f(k−1)`, which needs `f(k−2) ≤ f(k−1)`. This holds for `k ≥ 2`.
- Spot checks: F₃ gives 1/3, F₂ gives 1/2. ✔

**Thm 4.1** (`D = 1`): holds. The components are A₁ or A₂.

**Thm 4.3** (`D = 2`, every min-range `v` works): holds case by case.
- 2+2: checked by hand. `P − b = {a} ∥ {c<d}` gives `P[a before c] = 1/3`, and `P − a` gives `P[b before d] = 2/3`. Both are balanced, as are the values in `P`.
- `F_n`: `v = x_n` with pair `{x₁,x₂}` gives probabilities `f(n−1)/f(n+1)` and `f(n−2)/f(n)`. Both are in `[1/3,1/2]` for n ≥ 3. By self-duality the same holds at `v = x₁`.
- Decomposable case: holds. A min-range `v` with `π(v) = 0` is a singleton summand. Otherwise, another summand keeps its balanced pair.

## 4. Computer proofs (claim 4): HOLDS

### 4.1 Completeness of generation

**Author's argument.** Adding a maximal element whose down-set is any ideal is exhaustive:
delete a maximal element. Min-over-leaves of an equivariant IR tree without pruning is a canonical
form. `Π_D` is closed under deletion, because deleting can only lower `π`, so filtering at every
level is exhaustive. The range-limited runs seed from *all* classes on 8 (D = 3) or 10 (D = 4)
elements and filter from the next level on, which is also exhaustive. ✔

**Independent regeneration.** I added a minimal element (dual augmentation) and deduplicated by
exact isomorphism test instead of a canonical form. It gives the same count at every level
(`out_gen_95d3.txt`, asserted by `check_95d3.py`):
- all classes: 2, 5, 16, 63, 318, 2 045, 16 999, 183 231, 2 567 284 (A000112);
- range ≤ 3, n = 9..16: 2 942, 8 362, 23 701, 67 116, 190 035, 538 329, 1 525 168, 4 320 980;
- range ≤ 4, n = 11..13: 178 811, 666 778, 2 490 595.

Two generators with disjoint designs agreeing on 20 counts is strong evidence that both are right.
A duplicate-producing or class-dropping bug would have to hit both identically.

The indecomposable subtotals also agree:
- range ≤ 3, n = 11..16: 1 404, 3 076, 6 736, 14 792, 32 455, 71 220 = 129 683;
- range ≤ 4, n = 11..13: 50 910, 176 766, 612 003 = 839 679;
- all ranges, n = 3..10: 2 338 137 indecomposable, 2 769 953 non-chains.

### 4.2 Census results (`out_census_95d3.txt`, exact integers)

- **exists-v**: 0 failures in every block (all n = 3..10; indecomposable n = 3..10; indecomposable range ≤ 3 n = 11..16; indecomposable range ≤ 4 n = 11..13).
- **every min-range v**: 1 failure, `4 6 4 0 0` (A₁ + C₃, `v` = middle of the chain), and none elsewhere.
- **every v** (the control): 287 at n = 10 (all), 153 at n = 9, 133 indecomposable n ≤ 10. Range ≤ 3: 1 at n = 12 only. Range ≤ 4: 1, 1, 0. This matches the note.

**Does the n = 11..16 restriction to indecomposable classes match Prop 1.2?** Yes. Take a
decomposable `P ∈ Π₃` with n ≤ 16. It has ≥ 2 summands, each in `Π₃` and of size ≤ 15.
- Singletons are irrelevant, and a size-2 summand is `A₂` with p = 1/2.
- A summand of size ≥ 3 is an indecomposable non-chain of `Π₃`, and it is covered: all ranges for size ≤ 10, the range ≤ 3 census for 11..15. There ONE-PT gives δ ≥ 1/3.
- Prop 1.2 then gives ONE-PT(P).

The same argument gives `Π₄` for n ≤ 13. The label PROVEN (computer) is appropriate. Overflow is
not an issue: `e ≤ 16! < 2.1·10¹³`, and the largest product formed is `< 10²⁸ ≪ 2¹²⁸`.

## 5. The obstruction (claim 5)

### 5.1 The numbers (HOLDS)

The worst margin (max over `(v,pair)`, min over `P`) at indecomposable range ≤ 3, n = 11..16,
re-computes to exactly 1/57, 14/831, 23/1344, 37/2175, 23/1425, 97/5694 (0.0161–0.0175). The
canonical margins re-compute to 8/525, 1/84, 2/129, 11/687, 7/435, 4/249. Lemma R's `r = 2` window
lies inside `[1/3,2/3]` only at `p' = 1/2` (Cor 1.4; re-derived: `p'/(2−p') ≥ 1/3 ⟺ p' ≥ 1/2`). So
"crude transport needs 0.1716, the data offer ≈ 0.016, a factor of ~10" is correct.

§2.2 adds that this worst case is **attained in the limit**. No sharpening of Lemma R alone can
close the gap. Any improvement must come from choosing the pair, i.e. from the covariance term,
as the note says.

### 5.2 "Margin bounded away from 0 in every class computed; ≥ 1/51 for all n ≤ 10": BROKEN

The note's own transcripts contradict it, and my census reproduces each value:
- **n = 10, indecomposable:** worst margin **5/318 = 0.0157 < 1/51**, at `10 0 0 2 6 3 17 1f 5f 3f 17f`. The note's own §2.3 table lists this value.
- **n = 3, 4, indecomposable:** margin **0**. `3 0 0 2` = F₃ = A₁ + C₂ has `p = 1/3` exactly. `4 0 0 2 1` = 2+2 has a balanced pair only at 1/3 in `P − v`. See `out_census_indec.txt` lines 23, 56–57.
- **decomposable, every n:** margin 0 (`out_census_all.txt`, π = 2 rows).
- **Canonical margin**, claimed as "down to 1/159": it is **0** at indecomposable n = 5 (`5 2 0 8 0 0`), n = 6 (`6 36 24 0 30 20 0`, range ≤ 3), and n = 8 (`8 76 74 70 70 20 0 0`). The note's transcript shows 0 in the π = 4 row at n = 5, the π = 3 row at n = 6, and the π = 7 row at n = 8. The headline quotes only the positive rows.

The zeros are closed-interval ties at `1/3`, so ONE-PT still holds there. But "margin bounded away
from 0" and "≥ 1/51" are false as stated. The true statement (EMPIRICAL) is narrower. For
indecomposable range ≤ 3 with 7 ≤ n ≤ 16, the worst margin is ≥ 5/318 ≈ 0.0157 and the canonical
margin is ≥ 1/84 ≈ 0.0119. Both are positive, with no downward trend visible at n = 11..16.

### 5.3 "F_m satisfies the route with μ₂ = 1/φ² − 1/3": BROKEN as a lower bound

Here are the F_n margins, computed as the worst margin over indecomposable range ≤ 2, which is
exactly `F_n` for n ≥ 5:

| n | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| margin | 0 | 0* | **1/24** | 2/39 | 1/21 | 5/102 | 8/165 | 13/267 | 7/144 | 34/699 | 55/1131 | 89/1830 |

The n = 4 value is 0 because the n = 4 block includes 2+2; F₄ alone has 1/15.

The limit is `1/φ² − 1/3 = 0.048633`. Odd `n` approach it **from below** (1/24 = 0.0417, and
55/1131 = 0.048629). So `μ₂` as a uniform constant must be ≤ 1/24 on n ≥ 4, and it is 0 at n = 3.
This sits inside a CONJECTURED route, so it does not affect any theorem. It does show the margin
hypothesis has to be stated with a base-case cutoff.

### 5.4 "A proof needs covariance decay plus a margin hypothesis": OVERSTATED

The argument shows that the *natural route* needs both:
1. canonical `v`;
2. a pair from the induction hypothesis on `P − v`;
3. transport by Lemma R.

This is well supported: 5.1 holds, and the need for margin is right because the induction
hypothesis δ(P−v) ≥ 1/3 carries no margin while Lemma R has a non-zero spread. It is not shown that
*every* proof of ONE-PT₃ needs these, and §7 of the note says as much ("§5 is an obstruction
analysis, not a proof that no proof exists"). §0 item 5's "a proof needs" should read "this
route needs". Also, per 5.2, the margin that exists empirically is ~0.016 at range 3 **only for
n ≥ 7**. It is 0 at small n, so the margin-carrying induction would need a finite base checked
separately. The census already provides that base up to n = 16.

---

## 6. What I did not do, and negatives

**Not done:**
- The other 13 rules in the note's census tables, and the h-order and "strong transport" negatives of §3/§7, were not re-checked. These include some minimal/maximal v, h-endpoints, "pair-first", and max-range v. I re-checked exists-v, every-v, every/some min-range v, margins, and Lemma R.
- I did not re-run the author's `run_all.sh`. Their numbers are quoted from the committed transcripts, and each one I quote was matched by my own run.
- I did not go past the note's range: no n = 11 unrestricted, no range ≤ 3 past n = 16.
- The KSBFT PDF, BW92, Peczarski and Gup26 were not read. Nothing audited depends on them.
- I did not settle the sharpness of Lemma R for `π(v) ≥ 2`.
- The checker's own firing control (a mutated `exists_v_fail`) was run by hand, not from `run_all.sh`.

**Negatives, each with the candidates tried:**
- **Missing family in Π₂.** Candidates: cycles of every length (ruled out by proof for n ≥ 5), paths with non-Fibonacci orientation (ruled out by the propagation step), and an exhaustive search to n = 14. None found.
- **Generator discrepancy.** Candidates: all 20 level counts across 3 regimes, and the indecomposable subtotals. None found.
- **Counter discrepancy.** Candidates: 1 970 brute-force comparisons, and every margin/extremal fraction the note prints for n = 11..16. None found.
- **Lemma R violation.** Candidates: 675 726 142 distinct (P, v, pair) checks. None found.
- **Prop 1.2 violation.** Candidates: 431 816 decomposable posets at two intervals. None found.
