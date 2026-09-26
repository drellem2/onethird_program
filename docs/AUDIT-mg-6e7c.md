# AUDIT of mg-ce69 (KSBFT-Q2): the theorems hold, the SL-conjecture is just "a nested balanced pair exists", and "survives any tail" is false

`mg-6e7c`, 2026-09-26. The subject is `docs/KSBFT-Q2-both-ends.md` (commit `c6ddf6c`), together with `code/ksbft_q2_both_ends_ce69/`. I am not its author. I re-derived every PROVEN claim by hand before I ran any code. I also re-derived the beyond-brief material: the Swap Ladder, Doubling, Pinch, release time, Cor 1.6 and Prop 3.2.

**Instrument.** `code/audit_ksbft_6e7c/`. The runner is `sh run_all.sh`: exact integers and `Fraction`s, at most 3 processes, about 3 min wall, exit 1 on any failure. It shares no code with the author's instrument.

| file | what it does | how independent it is |
|---|---|---|
| `aud.py` | three probability engines | An ideal DP (forward × backward counts), an **added-relation count** `e(P + {a<b}) / e(P)`, and explicit enumeration. All three agree on every pair of every witness with `e ≤ 750`. |
| `gencheck.py` | certifies the census files | The files come from mg-eedd's generator, the same one the author used. I certify them without trusting that generator: `Σ n!/\|Aut P\| = A001035` (the labelled posets) for every `n ≤ 9`, using my own automorphism counter. The check fails on a planted drop and on a planted duplicate. |
| `witnesses.py` | every witness number the doc cites | `Q_m` is rebuilt **from the doc's prose** and then compared with the author's printed `Q_4`. |
| `census.py` | theorem checks and coverage counts | All `n ≤ 9` posets, range ≤ 4 at `n = 9`, and mg-2912's 2 534 records. It has 5 firing controls. |
| `pinch.py`, `release.py`, `reduction.py` | Lemma 1.2, Lemma 1.3, and the "one question" reading | |
| `check.py` | the gate | Asserts every figure this audit relies on (`out_check.txt`). |

Verdicts:
- **HOLDS**: re-derived.
- **BROKEN**: false as stated.
- **OVERSTATED**: true only in a weaker form.
- **UNVERIFIABLE**: cannot be checked from here.

---

## 0. Summary

> **All the PROVEN mathematics holds.** I re-derived each of these by hand:
> - Lemma 1.1 (C-prefix), Lemma 1.2 (Pinch), Lemma 1.3 (release time);
> - **Thm 1.4 (Swap Ladder)**, Lemma 1.5 (Doubling), Cor 1.6;
> - Lemma 2.1 (dominance), the (L1) consequences, Prop 2.3 (gadget dichotomy);
> - Prop 3.1 (separation), Prop 3.2 (Birkhoff–Hopf decoupling), Thm 4.1.
>
> Every exact witness number recomputes. That covers `P_9`, `B7`, `rec11`, `W8`, `Y8`, and `Q_m` up to `n = 46` with `e = 40 440 798 401`. Every census count also reproduces with independent code:
> - 146 468 posets at `n = 9`;
> - Zaguia misses 5 / 114 / 21;
> - Cor 1.6 misses 5 / 138, which by range is 46 / 86 / 5 / 1;
> - range ≤ 4 at `n = 9` has 0 misses.
>
> The structure the doc imports from mg-5f14 is Thm 3.1 as audited, with the audit's hypotheses. The doc uses only the corrected identity `∩_U{x<u} = {|J| ≤ k}`. I checked this.
>
> **The flashiest claim is sound, but it is framed more strongly than it is.**
> - **The SL-conjecture is exactly "every non-chain poset has a nested balanced pair", with nested meaning primal or dual.** Thm 1.4's ladder adds nothing to it. If a nested pair is balanced, it is rung 0 of its own ladder. Conversely, a ladder that fires yields a balanced `(x, b_i)`, and that pair is nested because `down(x) ⊆ down(b) ⊆ down(b_i)`.
> - So these statements are the same census fact:
>   - "SL fires on all 160 567 / 2 534";
>   - "every poset has a nested balanced pair";
>   - "Thm 1.4 certifies every balanced pair of every witness", where most of the certificates are rung 0, i.e. the pair certifying itself.
>
>   I checked per poset that the equivalence holds (`EQV = 0` everywhere).
> - It follows that "the chain-bottom extension is load-bearing" (because Zaguia's form misses 5 / 114 / 21) is **BROKEN** as a statement about the conjecture. What is load-bearing is dropping "full" and allowing any rung 0 in `[1/3, 2/3]`. The chain bottom never matters for whether SL fires.
> - The "(L3)-analogue" that the doc names as the precise gap is **a strengthening of 1/3–2/3** (to nested pairs). It is not a reduction of it.
>
> **BROKEN: §3.3 "the triangle survives any tail".** Take `B7` with a width-2 tail that skips 3 (`r = 3`): `(2,5)` moves to 0.7206 and WIN holds at the bottom. On 13 random range-≤6 tops, the whole triangle survives on 7. It does survive the author's tail (`r = 1`) and the `r = 2` tail.
>
> **OVERSTATED:**
> - Headline: "the two ends do NOT interact once `n ≥ 8D−1` (PROVEN)". Prop 3.1 proves only that the **windows** are separated. Prop 3.2 proves coupling that is exponentially weak, not zero. The "cannot contradict each other unless one already is" reading is a heuristic, not a theorem.
> - Commit subject: "refutes Q §5 candidate". That candidate is a "for `n ≥ n_0(D)`" statement, and no finite family refutes it. What `Q_m` proves is `n_0(5) > 46`. The doc body says this correctly.
> - §1.1: "items 1 and 3 are one question". The reduction to `R` is exact only for x-pairs. For the twin pair `(u, v)`, the law in `P` is a mixture, and on 95 gadget twin pairs (`n ≤ 8`) balance in `R` and in `P` differ.
> - Wording: "11 330 gadgets" counts minimal `x` with `k ≥ 1`, not Y-gadgets.

---

## 1. Claim by claim

### §1: the second-order ladder

| # | claim | verdict | re-derivation / evidence |
|---|---|---|---|
| 1.1 | **Lemma 1.1 (C-prefix)**, parts 1–4 | **HOLDS** | See the notes after this table. |
| 1.1r | Reading: window `W_s ⊇ [1/3, 1/2]` for `s ∈ [0, 1/3)`, length `1/(3(1−s))` | **HOLDS** | `(2/3−s)/(1−s) ≥ 1/2 ⟺ s ≤ 1/3`. `s = S_{k−1} < 1/3` is Q Thm 3.1(i), as audited. |
| 1.1q | "items 1 and 3 of the ticket are **one question**: the O1 configuration" | **OVERSTATED** | Exact for x-pairs only. By part 4, `#_P{u<v} = #_R{u<v} + Σ_{i<k} #_{P∖(C_i∪x)}{u<v}`, which is a mixture of different posets. `R` is also not constrained to be balance-free. On 95 twin pairs of Y-gadgets with `n ≤ 8`, the balanced status in `P` and in `R` differs. First example: `7 0 0 2 2 1 1b 1b`, where `P[2<3] = 5/16` in `P` and `1/3` in `R` (`out_reduction.txt`). |
| 1.2 | **Pinch Lemma**: `{\|J\| ≤ t} = {x<w}` iff `Inc(x) = L ⊕ {w} ⊕ M` with `\|L\| = t` | **HOLDS** | Every ideal of `Z` occurs as the prefix with positive probability (`J, x, rest`), so the event identity is the ideal statement. A size-`(t+1)` ideal containing `w` has `w` as its unique maximum, so it is `↓_Z w`. The size-`t` ideals are then `↓_Z w ∖ w`, and the minimal elements of `Z ∖ L` are `{w}`, so `Z ∖ L ⊆ ↑w`. The converse is clear. The edge case `\|Z\| ≤ t` is consistent (both sides fail). **Tested:** event identity vs the structural condition for every minimal `x` and every `t`, `n ≤ 8`: 0 mismatches. The control (drop "M above w") fires on 32 779. `P_9`'s only pinch is at level 0, confirmed. |
| 1.3 | **Lemma 1.3** (release time) | **HOLDS** | Condition on the length-`ρ(u)` prefix `σ`. `σ` is an ideal and `u` is minimal in `P ∖ σ`, whose extensions are uniform. Q's Lemma 1.1 then applies, and non-increasing laws are closed under mixing. **Tested** by explicit enumeration: 10 750 elements, 0 violations; the min-control has 4 072. Both figures equal the doc's. |
| 1.4 | **Thm 1.4 (Swap Ladder)**, (a)–(c) | **HOLDS** | See the notes after this table. |
| 1.4s | Special cases: Linial and Local Linial | **HOLDS** | If `c_1` is the unique minimum of `Z`, then `W = ↑c_1 ∖ ↑x = Z` and its chain bottom is `C`. The hypotheses are identical to Thm 2.1's. The steps are `q_i`. |
| 1.4z | Full-chain case = **Zaguia's good-pair theorem** (KNOWN), step lemma credited to his 2012 paper, `P[x<b_0] ≤ 1/2` = his Lemma 7 | **HOLDS** | I fetched arXiv 1610.00809 (Zaguia) and read Def. 1 (good pair: `D(a) ⊆ D(b)`, `U(b)∖U(a)` a chain, `P(a≺b) ≤ 1/2`, in `P` or its dual), Thm 2, Lemma 7 (critical pair ⇒ `≥ 1/2`) and the Thm 2 proof via step bounds `q_j`. The doc cites these accurately. **Also**, Zaguia already remarks that "every ordered set of width two has a very good pair", so placing Linial under the good-pair umbrella is also his. That is minor. Novelty of the chain-bottom / 2/3 form beyond Zaguia 2012 is **UNVERIFIABLE** (2012 paper not read, by the author or by me). |
| 1.5 | **Lemma 1.5 (Doubling)**: `down(x) = down(b_0)`, `up(x) ⊆ up(b_0)` ⇒ `t_1 = t_0`, and `P[x<b_0] ≤ 1/2` | **HOLDS** | The inverse swap from `{x<b_0}`: `b_0` moves earlier, and anything between below `b_0` would lie in `down(x)`, which is before `x`. `x` moves later, and anything between above `x` would lie in `up(b_0)`, which is after `b_0`. The image has `b_0 < x < b_1`. So there are injections both ways. `t_0 + t_1 ≤ 1` gives `≤ 1/2`, which is also Zaguia's Lemma 7 applied to the critical pair `(b_0, x)`. **Tested:** 0 violations on `n ≤ 9` and the records. The control (drop `up ⊆`) makes `t_1 ≠ t_0` on 267 238 ladders at `n = 9`. The table values (`P_9` 59/197 → 118/197, `B7`, `rec11`, `Q_4`) recompute exactly. |
| 1.4w | Twin ladder at the Y-gadget; `W ⊆ Inc(u)`, `\|W\| ≤ D` | **HOLDS** | `w ≥ v` and `w < u` would give `v < u`. |
| 1.4e | "Every balanced pair of every witness is a certified rung" | **HOLDS, but near-tautological (OVERSTATED as evidence)** | All balanced pairs of `W6`, `P_9`, `B7`, `rec11`, `W8`, `Y8` and `Q_4` are nested (`out_witnesses.txt` §4). A nested balanced pair is rung 0 of its own ladder, so only the rung ≥ 1 certificates carry content. Examples are `(2,5)` via Doubling and `Y8`'s `(2;4<6)` with first rung 6/11, which I confirmed. |

**Notes on 1.1 (Lemma 1.1).**
- `Z = Inc(x)` is an ideal (mg-3345 1.2). `C` is an ideal of `Z`, because `↓c_i ∩ Z ⊆ C_i`.
- **(1)** On `f(x) > k`, the prefix before `x` is an ideal `J` of `Z` of size `≥ k`, so `J ⊇ C` by the uniqueness of small ideals.
  - Let `w` precede `c_k`. Then `w ∈ Z`.
  - If `w ∈ Z ∖ C`, then `w ≥ u > c_k` for some `u ∈ U`. Here `u > c_k` holds because `Z ∖ C_{k−1} ⊆ ↑c_k`.
  - So the first `k` positions are exactly `C`, and prepending `C` is a bijection onto `E`.
- **(2)** On `|J| = i < k`, `J = C_i`.
- **(3)** is immediate.
- **(4)** Partition by `|J|`. For `b ∈ Z ∖ C`, `x` precedes `b` on `{|J| < k}`, and `1 − s = e(R)/e(P)`.
- **Tested:** the identity `P[x<b] = s + (1−s)P_R[x<b]` on every Y-gadget (`|U| ≥ 2`) with `n ≤ 8`, 4 047 gadgets: 0 mismatches. The control (`s` one rung short) fires on 13 605.
- *Wording:* the doc's "11 330 gadgets" is the author's count of minimal `x` with `k ≥ 1`, cumulative over `n ≤ 8`. It includes full chains and `|U| = 1`. Minor.

**Notes on 1.4 (Thm 1.4).**
- **Chain.** `W ∖ {b_0..b_{i−1}}` has a unique minimal element, so it lies in `↑b_i` (finite poset). Hence `b_0 < b_1 < …`.
- **(b)** `b_i < x` would give `b ≤ b_i < x`, and `b_i ∉ ↑x` by construction.
- **(a)** Take the swap of `x` and `b_{i−1}` on `{b_{i−1} < x < b_i}`.
  - `x` moving earlier is legal: an element between the two slots that lies below `x` would be in `down(x) ⊆ down(b) ⊆ down(b_{i−1})`, so it would precede `b_{i−1}`.
  - `b_{i−1}` moving later is legal: an element between that lies above `b_{i−1}` is in `↑b ⊆ W ∪ ↑x`. If it is in `↑x`, it comes after `x`. If it is in `W ∖ {b_0..b_{i−1}} ⊆ ↑b_i`, it comes after `b_i`, which follows `x`. In the full case `i = m+1`, `up(b_m) ⊆ ↑x`.
  - The map is an involution on position pairs, so it is injective. The image lies in `{b_{i−2} < x < b_{i−1}}`.
- **(c)** `{x<b_{i−1}} ⊆ {x<b_i}` gives the sum identity. From there it is the standard first-crossing argument. When the chain is full, `P[x<b_m] = 1 − t_{m+1} ≥ 1 − t_0 > 2/3`.
- **Tested:** every nested ladder (primal and dual) of every `n ≤ 9` poset (146 468 at `n = 9`), of range ≤ 4 at `n = 9`, and of the 2 534 records: 0 step violations and 0 conclusion violations. The controls fire:
  - dropping H1 gives step increases on 831 478 + 592 597 ladders at `n = 9`;
  - narrowing the window to `[0.34, 0.66]` gives violations on 81 949 + 68 297.

### §2: the 3-antichain

| # | claim | verdict | re-derivation |
|---|---|---|---|
| 2.1 | **Lemma 2.1**: with no balanced pair, `⇒` is a strict linear order on every antichain | **HOLDS** | The relation is a tournament. A 3-cycle would have cyclic sum `> 2`, but each linear order satisfies at most 2 of the 3 cyclic relations. A tournament with no 3-cycle is transitive. |
| 2.2 | (L1) at `r` minima: `P[m_r first] < 1/3`; `P[m_1 first] > 1 − (r−1)/3`; at `r = 3`, `P[m_1 < w] > 2/3` for all `w ∈ Inc(m_1)` | **HOLDS** | The first element is minimal, so `P[m_i first] ≤ P[m_i < m_1] < 1/3`, and the union bound gives the second. At `r = 3`, `P[m_1 < w] ≥ P[m_1 first] > 1/3`, and unbalanced forces `> 2/3`. |
| 2.3 | For `a ⇒ b` (minimal), `↑a ∖ ↑b` must branch below its crossing | **HOLDS** | Thm 1.4 applied to `(b; a, …)`. This holds for every dominance pair, not only adjacent ones. |
| 2.4 | **Prop 2.3 (G1/G2)** | **HOLDS** | See the notes after this table. |
| 2.5 | `P_9`, `B7`, `rec11`, `Q_m` are G1 | **HOLDS** | `P_9`: 161/197 and 138/197, `S_1 = 124/197`, product 0.5725. `rec11`: 119/150 and 173/250, `S_1 = 46/75`. Both are recomputed. None of these posets is a counterexample, so "G1" here only labels the inequality pattern. |
| 2.6 | `W8`: `2 ⇒ 1 ⇒ 0`, `P[1<2] = 65/196 = 1/3 − 1/588`; balanced pairs all rungs, none between two minima | **HOLDS** | Recomputed. The balanced pairs are `(0,3)`, `(0,4)`, `(3,4)`, `(3,5)`, `(6,7)`, all nested. |
| 2.7 | XYZ (Shepp 1982) quoted as `P[x<y, x<z] ≥ P[x<y]P[x<z]` | **HOLDS** (KNOWN) | That is the correct statement of the XYZ inequality. Not re-proved. |
| 2.8 | Kahn–Saks 3/11, BFT `(5−√5)/10` "do not localise" | **UNVERIFIABLE** (recalled; the doc says so) | The constants are correct as recalled. |

**Notes on 2.4 (Prop 2.3).**
- Exhaustive and exclusive: each `P[x<u]` is `> 2/3` or `< 1/3`.
- The audited identity `{x<u} ∩ {x<v} = {|J| ≤ k}` holds because `U = {u, v}` is all of `min(Z ∖ C)`.
- **G1:** XYZ gives `S_k > 4/9 > 1/3`. `S_{k−1} < 1/3` holds because otherwise Local Linial would fire, since `q_0 = P[x<c_1] ≤ 2/3`. So `j* = k`. `S_k < 2/3` because `q_k ≤ q_0`, and `q_0 < 1/3` since `q_0` is unbalanced and `≤ 2/3`.
- **G2:** `S_k ≤ P[x<u] < 1/3`.

### §3: both ends

| # | claim | verdict | re-derivation |
|---|---|---|---|
| 3.1 | **Prop 3.1 (separation)**, `n ≥ 8D−1` | **HOLDS** | See the notes after this table. |
| 3.1h | Headline / (e)–(f): "the two ends do NOT interact once `n ≥ 8D−1` (PROVEN)"; §3.2 Reading "they cannot contradict each other unless one of them is already contradictory on its own" | **OVERSTATED** | Prop 3.1 separates only the `(D+1)`-windows. The doc itself locates the balance at depth `≈ 1.6D` (`Q_m`: labels ≤ 7 from an end), outside those windows. Prop 3.2 gives coupling that is exponentially small, not zero. The "cannot contradict" reading would need a **gluing lemma**: robust bottom-balance-free + robust top-balance-free + a balance-free middle ⇒ balance-free glued poset. That is neither stated nor proved. The `Q_m` family, plus my own `B7`-based glued family (§7 of `out_witnesses.txt`: range 5, WIN fails at both ends, `n = 18, 30`), is **consistent** with it. |
| 3.2 | **Prop 3.2 (decoupling)** | **HOLDS**, with two implicit hypotheses | See the notes after this table. |
| 3.3 | §3.3 ablation table (`P_9` prefixes + tail(20)) | **HOLDS** (values) | The `B7` + tail row recomputes: 0.5844, 0.5900, 0.4974. `(2,4)` in the long family is 0.6707, per the author's transcript. |
| 3.3a | "the triangle **survives any tail**" | **BROKEN** | `B7` + a width-2 tail with `r = 3` (each new element above all but the last 3; range 6, connected): `(2,5) = 0.7206`, unbalanced, and WIN **holds** at the bottom. With `r = 2`, all three survive. On random range-≤6 connected tops of 8 elements, the triangle survives in 7 of 13. The true statement is: it survives the doc's tail (`r = 1`), and more generally it depends on the tail. |
| 3.3b | `(2,5)` is rung 1 of the twin ladder `(2; 3<5<6)`; `(2,4)` balanced "only while `up(4) ⊆ up(2)`" | **HOLDS** / the second is plausible, not checked | `(2;4)` is a full ladder in `P_9`: `up(4) = {8} ⊆ up(2)`. |
| 3.4 | `Q_m` table: indecomposable, range 5, `n = 18…46`, WIN fails at both ends, margin +0.0198 / +0.0197, balanced pairs as listed, `e(Q_14) = 40 440 798 401` | **HOLDS** | See the notes after this table. |
| 3.4a | "refutes, on every tested length, Q §5's candidate" / commit "refutes Q sec.5 candidate on tested n" | **OVERSTATED** | The candidate is "∃ `n_0(D)`: WIN at some end for `n ≥ n_0`". A finite family cannot refute it. What is established is `n_0(5) > 46`, and for the bottom-only form `> 69` (the author's transcript; one-ended, not recomputed by me). "For all `m`" is correctly labelled CONJECTURED. |
| 3.4b | Balanced pairs at depth ≤ 8 from an end, none in the middle | **HOLDS** | The maximum depth is 7 for every tested `m`. |

**Notes on 3.1 (Prop 3.1).**
- `f(x) ≤ |Inc(x)| + 1 ≤ D + 1` (mg-6b81 Lemma 2.2 with `s = 1`, audited).
- F2 gives `|f(z) − f(x)| ≤ 2D − 1`, so bottom-window elements sit at positions `≤ 3D`, and top-window elements at `≥ n − 3D + 1`.
- The gap is `≥ n − 6D + 1 ≥ 2D`, which exceeds `2D − 1`, so the pairs are comparable, with the bottom one smaller.
- **Tested:** on `Q_14` (`n = 46 ≥ 39`), every bottom-window element is below every top-window element.

**Notes on 3.2 (Prop 3.2).**
- Transfer: `e(P∖J) = Σ_{J'} e(J'∖J)·e(P∖J')`, because each extension of `P ∖ J` determines `J'`.
- The entries lie in `[1, D!]`, because every size-`k` ideal lies in every size-`(k+D)` ideal (mg-6b81 Lemma 2.2).
- Birkhoff–Hopf: `τ = tanh(Δ/4)` with `Δ ≤ log max(T_ik T_jl / T_il T_jk) ≤ 2 log D!`, so `τ ≤ (D!−1)/(D!+1)`.
- A Hilbert distance `d` gives a law error `≤ e^d − 1`.
- **Implicit hypotheses:**
  - (i) *both* posets lie in `Π_D`, which is needed for their level sets below `t` to coincide;
  - (ii) the depth formula for R's transfer half has an off-by-ceiling in `⌊(t−s)/D⌋`.
- Neither changes the content. KSBFT-R itself is unaudited.

**Notes on 3.4 (the `Q_m` table).**
- I rebuilt `Q_m` from the prose ("each new element above all but the previous one"; the dual glued on top, whose first element is not above the last one below). It equals the author's printed `Q_4`.
- All figures recompute with my DP, and `e(Q_4)` also by plain recursion: margin +0.01977 (m = 0) and +0.01969 (m ≥ 2).
- Every balanced pair of every `Q_m` is nested.

### §4: the proposition, the census, the conjectures

| # | claim | verdict | evidence |
|---|---|---|---|
| 4.1 | **Thm 4.1** items 1–5 | **HOLDS** | See the notes after this table. |
| 4.2 | **Cor 1.6** (opposite full-chain ladders ⇒ balanced pair), mixed primal/dual case | **HOLDS** | The ladder asserting the order of probability `≤ 1/2` is full with `t_0 ≤ 2/3`, so it fires. The prose says "a primal ladder … and a full-chain ladder", but the proof needs **both** full, and item 3 says "two full-chain ladders". That is minor wording. |
| 4.3 | Census table: SL 12 524 / 146 468 / 2 534; Zaguia misses 5 / 114 / 21; Cor 1.6 misses 5 / 138 (by range 46 / 86 / 5 / 1); range ≤ 3 5 412 and range ≤ 4 69 956 with no misses | **HOLDS** (EMPIRICAL) | **Independently recounted.** `n ≤ 9` in full, range ≤ 4 at `n = 9` (4 327, 0 misses) and the 2 534 records. The 5 `n = 8` failures are the same 5 posets for the Zaguia and Cor 1.6 columns, with ranges 4, 5, 5, 5, 5. The census files are certified complete and duplicate-free by A001035. I did **not** recount range ≤ 3 `n = 10–12` or range ≤ 4 `n = 10, 11`. |
| 4.4 | **SL-conjecture** ⇒ 1/3–2/3 | **HOLDS, but trivially** | See the notes after this table. |
| 4.5 | "Zaguia's good-pair form fails on 5 / 114 / 21 … so the chain-bottom extension is load-bearing" (§0) | **BROKEN** (as reasoning) | The chain bottom is irrelevant to whether SL fires, since rung 0 suffices. What separates SL from Zaguia is dropping "full" (and `≤ 1/2 → ≤ 2/3`). The counts themselves hold. |
| 4.6 | "The obstruction … is an (L3)-type input" | **OVERSTATED** | Equivalently: prove that a nested balanced pair exists. That is **stronger** than 1/3–2/3, so the "gap" is not smaller than the original problem. It is a different, stronger target. That may still be the right target, since nested pairs are exactly the ones swap arguments can reach, but it should be stated as a strengthening. |
| 4.7 | Weak conjecture: Cor 1.6 covers every indecomposable range-≤3 poset | **CONJECTURED, correctly labelled** | Range ≤ 3 was not rechecked beyond `n ≤ 9` (0 misses at range ≤ 4, `n = 9`). |
| 4.8 | KSBFT-R remarks | **UNVERIFIABLE here** (R unaudited) | The twin argument is right: `down(u) = down(v)` and `up(u) = up(v)` make `{u, v}` a module. |

**Notes on 4.1 (Thm 4.1).**
- **Item 1** is Q Thm 3.1 with the audited hypotheses (not a chain, indecomposable).
- **Item 2:** "`≤ 2/3` hence `< 1/3`" uses no-balance. After that it is Thm 1.4(c).
- **Item 4:** under `up(u) ⊆ up(v)`, Lemma 1.5 gives `P[u<v] ≤ 1/2`, hence `< 1/3`. `2P[u<v] ∉ [1/3, 2/3]` and `< 2/3` then give `< 1/6`. The pivot is automatically the weaker twin.
- **Item 5:** `b_i ∈ Inc(x)` by 1.4(b).

**Notes on 4.4 (the SL-conjecture).**
- **SL-conjecture ⟺ Nested Balance:** every non-chain poset has an incomparable pair with `down(a) ⊆ down(b)` or `up(a) ⊆ up(b)` that is balanced.
  - (⇐) The pair is rung 0.
  - (⇒) The fired rung is nested.
- The census confirms this per poset (`EQV = 0` on all 160 567 + 4 327 + 2 534), and "SL fires" = "NESTBAL" on every population.
- So the doc's "necessary condition … and it holds" is in fact **necessary and sufficient**, and the SL-conjecture is a **strengthening** of 1/3–2/3 whose statement needs no ladder.

---

## 2. Did the imported structure really come from mg-5f14 Thm 3.1 *as audited*?

Yes. The doc uses these pieces of mg-5f14, and nothing else:
- (iii) `u > c_k` and `|U| ≥ 2`, re-proved in audit 3.1;
- (i) `S_{k−1} < 1/3`;
- Thm 2.1 for G1's `S_{k−1} < 1/3`;
- the corrected identity `∩_U{x<u} = {|J| ≤ k}`, in Prop 2.3 and Lemma 1.1(1).

The BROKEN §3.2 inclusion, the "touching" wording and the 4/29 counts are not used. The added hypotheses (not a chain, indecomposable) are stated in Thm 4.1.

## 3. Extremal configurations for the "both ends" argument (built myself)

- **`Q_m`, rebuilt from the prose.** This is the author's family, re-derived: range 5 and WIN fails at both ends up to `n = 46`. At `n = 46 ≥ 8D−1`, the separation is verified.
- **`B7`-glued (mine).** `B7 + tail(m)` with its dual glued on top by the same seam. At `n = 18` and `n = 30` it has range 5, is connected, and WIN fails at both ends, with margin +0.0103. The balanced pairs are the bottom triangle `(2,4), (2,5), (4,5)` and its mirror. This is a second, independent both-ends family, so the doc's negative "the ends do not contradict each other" does not rest on one construction.
- **Tail sensitivity (mine).** `B7` with the `r = 2` and `r = 3` tails, and 13 random tops. The triangle is **not** tail-independent (§3.3a).

## 4. Candidates ruled out, checked against the candidate space

| # | candidate | verdict |
|---|---|---|
| (i) | x's own ladder continuing past a branch | **HOLDS.** Ruled out exactly, by the Pinch Lemma. |
| (ii) | "The two ends contradict for long posets" | **HOLDS as "not by any argument of this form, up to `n = 46`"**: two families at range 5. It is not a proof that no long-range contradiction exists. |
| (iii) | "`P_9`'s balance is a two-end interaction" | **HOLDS** for the pairs `(2,5)`, `(4,5)`: `B7` + tail keeps them. |
| (iv) | Q §5 WIN-for-large-`n` | **OVERSTATED.** It is `n_0(5) > 46`, not a refutation. |
| (v), (vi) | Zaguia good pairs always exist; structural Cor 1.6 always applies | **HOLD.** Both are refuted from `n = 8`, and the 5 witnesses were recomputed. |

**Not considered by the doc, and worth recording.** Nested Balance itself is the stronger conjecture the SL-conjecture reduces to. I did not search for counterexamples to it beyond the census (`n ≤ 9` and the records, all clean).

## 5. What I did NOT do

- I did not recount range ≤ 3 (`n = 10–12`) or range ≤ 4 (`n = 10, 11`) for Cor 1.6. I did not re-run the one-ended `n = 54, 69` members, `rec11` + tail, or the `P_9` ablation rows other than `B7`.
- I did not read Zaguia 2012 (N-free), Linial 1984, Shepp, Kahn–Saks or BFT. I read Zaguia 1610.00809 only for Def. 1, Thm 2, Lemma 7 and Def. 5.
- I did not prove persistence of `Q_m` for all `m`.
- I did not check the novelty of Nested Balance as a conjecture.
- The census files come from mg-eedd's generator. Their completeness is certified independently (A001035), not their generation.
- No case search was extended. Computation was used only for recomputation, controls and the counterexamples above.

## 6. Suggested errata (I edited nothing in the subject doc)

1. §0(c)/§4: state that the SL-conjecture ⟺ "every non-chain poset has a nested (primal or dual) balanced pair". Replace "necessary condition" with "equivalent". Drop "the chain-bottom extension is load-bearing". Rephrase the (L3)-gap as "prove Nested Balance, a strengthening of 1/3–2/3".
2. §3.3: "survives any tail" → "survives the tail `r = 1` (and `r = 2`); with `r = 3`, `(2,5)` leaves the window (0.7206)".
3. Headline, §0(e)/(f) and §3.2 Reading: "do NOT interact" → "their windows are disjoint and comparable (Prop 3.1), and they couple only through an exponentially weak boundary vector (Prop 3.2)". Mark "cannot contradict unless …" as heuristic, or CONJECTURED as a gluing lemma.
4. §1.1: "one question" → "one question for x-pairs". Twin-pair laws in `P` are mixtures (95 disagreements at `n ≤ 8`).
5. Commit wording "refutes Q §5 candidate" → "`n_0(5) > 46`".
6. Minor: say "11 330 gadgets" counts minimal `x` with `k ≥ 1`. Cor 1.6's prose should say both ladders are full. Prop 3.2 should say "both in `Π_D`". Credit "width 2 ⇒ very good pair" to Zaguia as well.
