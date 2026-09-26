# KSBFT-M: margin-carrying induction on bounded range. The deletion induction cannot sustain a fixed margin (PROVEN for Lemma R alone, EMPIRICAL with decay). An exact ideal-mixture "prefix certificate" replaces it and re-proves D = 3 (base n ≤ 11) and D = 4 (base n ≤ 15). Its cost rules out D ≥ 5, so D = 7 is not reached (mg-6b81)

Builds on mg-eedd (`docs/KSBFT-J-one-pt.md`: Lemma R, the decomposable reduction, the (ONE-PT) census and its margins) and on mg-2912's margin observation. Instruments are in `code/ksbft_m_margin_6b81/`. `sh code/ksbft_m_margin_6b81/run_all.sh` regenerates every transcript quoted here. It runs serially (one process), takes ~15 min, and needs ~2 GB of RAM.

Labels, as in KSBFT-J:
- **PROVEN**: the proof is in this file.
- **PROVEN (computer)**: an exhaustive, exact-integer computation over a finite class, with its instrument and its firing controls. It is a proof about that class only; the theorems below state exactly which finite class each one consumes.
- **EMPIRICAL**: comes with its instrument and range.
- **CONJECTURED**: a guess.

Conventions are those of KSBFT-J. `π(v)` is the number of elements incomparable to `v`, `π(P) = max π(v)`, and `Π_D` is the class of posets of range `≤ D`. A pair `{x,y}` is *balanced* if `x ∥ y` and `p = P[x before y] ∈ [1/3, 2/3]` (closed interval). `dist(p) = min(p − 1/3, 2/3 − p)` (≥ 0 iff balanced). `δ(P) = max over incomparable pairs of min(p, 1−p)`, so the *margin* of `P` is `δ(P) − 1/3 = max dist`. `P` is *indecomposable* if its incomparability graph `G(P)` is connected. An *ideal* is a down-set.

---

## 0. Verdict

1. **Is D = 3 known? Yes.** "k-thin" in Brightwell–Wright (SIAM J. Discrete Math. 5 (1992) 467–474, *The 1/3–2/3 conjecture for 5-thin posets*) and in Peczarski (Order 25 (2008) 91–103, *The gold partition conjecture for 6-thin posets*) means "every element is incomparable to at most k others", i.e. `π(P) ≤ k`. So `D ≤ 6` is known, and Peczarski's proof uses computers heavily. Everything below at `D = 3, 4` is therefore a **test of the method**, as the ticket instructs. I have **not** read either proof, so I cannot say whether the method of §2 is theirs (§6).

2. **Exceptional list (item 1, EMPIRICAL).** Among the indecomposable non-chains of every class computed (all `n ≤ 8`; `Π_3` and `Π_4` for `n ≤ 15`), exactly one has `δ = 1/3`: `2+1` (`A₁ + C₂`, `n = 3`). The other members of "the (2+1) family" that sit at exactly 1/3 are ordinal sums, so they are decomposable and are disposed of by the decomposable reduction. **So the exceptional list for H(D, μ) is `{2+1}`.** The largest μ consistent with the data is:
   - `μ_2 = 1/24` (`F_5`, exact; `inf` over `F_m` is attained at `m = 5`);
   - `μ_3 = μ_4 = 5/318 ≈ 0.01572` (one `n = 10`, `π = 3` poset). For `n = 11..15` the per-`n` minima are 0.0161–0.0175, with no trend (§1).

3. **H(D, μ) ⇒ H(D, μ) by deletion does not close (item 2).**
   - (a) **PROVEN (Prop 3.1).** Lemma R alone transports *no* margin at all. For every `μ > 0` and every `v` with `π(v) ≥ 1`, which is every `v` of an indecomposable `P` with `n ≥ 2`, Lemma R's window around any `p' ∈ [1/3+μ, 2/3−μ]` leaves `[1/3+μ, 2/3−μ]`. So with Lemma R alone, **no μ > 0 is self-sustaining**, for any D.
   - (b) **Structural.** Any transport bound ε > 0 degrades a fixed margin μ to μ − ε. A deletion induction can therefore only spend a finite budget `Σ ε_k`, never sustain a fixed μ.
   - (c) **EMPIRICAL, where it breaks at D = 3.** Deleting a minimal-range `v` moves `p` of a pair at `G`-distance `d` from `v` by up to 0.17, 0.073, 0.029, 0.011, 0.0041, 0.0016, … for `d = 1, 2, 3, …` (ratio ≈ 0.38–0.41 per step, §4). The pairs that are balanced in both `P` and `P − v` have worst margin 0.0145 (`n = 10`) to 0.0155 (`n = 13`) at `d ≥ 1, 2`, and 0.0128–0.0155 at `d ≥ 3`. At `d ≥ 4`, some posets have **no** pair balanced in both at all (worst margin −0.027). So at every `d` the uniform error exceeds the available margin. The deletion scheme with minimal-range `v` and graph-distance decay fails quantitatively at `D = 3`.

4. **What works instead: the prefix certificate (§2, PROVEN).** Condition a linear extension on its first `s` elements. The set of those elements is an ideal `J` of size `s`, so `p_P(x<y) = Σ_J w_J p_J(x<y)` **exactly**, with positive weights, for any pair lying in every size-`s` ideal (Lemma 2.3). In `Π_D` all size-`s` ideals lie inside any ideal `Q` with `|Q| = s + D` (Lemma 2.2). So a pair balanced in **every** size-`s` ideal of `Q` is balanced in **every** `P ∈ Π_D` having `Q` as an ideal, however large `P` is. This is the margin-carrying step made exact: zero transport error, with the margin being the robustness over the ideal family. It needs no induction on `n` and no decay estimate.

5. **Theorem 5.1 (D = 3, PROVEN (computer)).** Every non-chain `P ∈ Π_3` has `δ(P) ≥ 1/3`. It consumes two finite checks:
   - (i) `δ ≥ 1/3` on the indecomposable members of `Π_3` with `n ≤ 11` (2 + 7 + 15 + 32 + 59 + 131 + 289 + 643 + 1 404 = 2 582 posets at `n = 3..11`; per-`n` counts in §1's table, columns π = 2, 3);
   - (ii) every one of the **4 224** non-CUT isomorphism classes of size `t = 11` in `Π_3` has a certificate at `s = 8`.

   The worst robust margin is `1/96 ≈ 0.0104`, and 0 classes fail. Posets with `n ≥ 12` are handled by (ii) alone, so the ticket's "base case `n ≤ 16`" is not needed: the base is `n ≤ 11`.

6. **Theorem 5.2 (D = 4, PROVEN (computer)).** The same holds on `Π_4`. It consumes base `n ≤ 15` (7 238 840 indecomposable posets at `n = 15`) and **14 298 595** non-CUT classes at `t = 15`, each with a certificate (worst robust margin `1/150`, 0 failures). At `t = 14` there are still 14 failures.

7. **D = 5 and D = 7 are not reached (EMPIRICAL cost).** The needed prefix length grows by 4 per unit of `D`: `t(3) = 11`, `t(4) = 15`. At `D = 5`, `t = 12` and `t = 13` still leave 127 288 of 3 740 359 and 141 882 of 17 890 772 classes uncertified. The non-CUT class count grows ×3.4 per step at `D = 4` and ×4.7 at `D = 5`. By extrapolation (CONJECTURED), `D = 5` needs `t ≈ 19` and ~10¹¹ classes, and `D = 7` needs `t ≈ 27`, far beyond exhaustive class enumeration. The method is **sound and D-uniform, but its verification cost is not**. §7 lists what would have to change.

8. **Covariance decay (item 4, EMPIRICAL).** The worst `|Cov_{P−v}(w_v, 1{x<y})| / E[w_v] = |p_P − p_{P−v}|` decays geometrically in the `G(P)`-distance `d` between `v` and the pair. The rate is ≈ 0.38–0.41 per step, which is close to `1/φ² ≈ 0.382` (the Fibonacci rate). The rate is flat in `n` (`n = 10` and `n = 13` agree to 2–3 significant digits wherever both are defined) and roughly flat in `π(v)` (§4).

---

## 1. The exceptional list and the empirical μ (item 1)

EMPIRICAL, exact. Instrument: `pcert delta` (exact `__int128` counts via mg-eedd's `lecount`; `dist` is compared by integer cross-multiplication). Populations:
- every isomorphism class for `n = 3..8`;
- the indecomposable members of the non-CUT lists `c3_n` (`n ≤ 11`) and `c4_n` (`n ≤ 15`), which contain **every** indecomposable member of `Π_D` of that size (Lemma 2.5(c));
- the full range-`≤ 3` census for `n = 12, 13`.

Transcript: `out_base.txt`. The indecomposable counts reproduce mg-eedd's independently generated census wherever they overlap: `Π_3` gives 1 404 / 6 736 / 14 792 / 32 455 at `n = 11, 13, 14, 15`, and `Π_4` gives 50 910 + 176 766 + 612 003 = 839 679 for `n = 11..13`.

Minimum of `δ(P) − 1/3` over indecomposable non-chains, by `n` and `π(P)` (exact):

Generated by `code/ksbft_m_margin_6b81/table_base.py` from `out_base.txt` (the `## D=4 n=…` sections; entries are exact reduced fractions; columns are the exact range `π(P)` of the poset, so the `π=2` column is `F_n` and, at `n = 3`, `2+1 = F_3`; #indec counts indecomposable non-chains of that exact range):

| n | #indec (pi=2/3/4) | pi=2 | pi=3 | pi=4 |
|---|---|---|---|---|
| 3 | 2/0/0 | 0 = 0.00000 | – | – |
| 4 | 2/5/0 | 1/15 = 0.06667 | 1/6 = 0.16667 | – |
| 5 | 1/14/16 | 1/24 = 0.04167 | 1/33 = 0.03030 | 1/15 = 0.06667 |
| 6 | 1/31/89 | 2/39 = 0.05128 | 1/42 = 0.02381 | 1/15 = 0.06667 |
| 7 | 1/58/358 | 1/21 = 0.04762 | 2/75 = 0.02667 | 1/39 = 0.02564 |
| 8 | 1/130/1212 | 5/102 = 0.04902 | 1/45 = 0.02222 | 5/138 = 0.03623 |
| 9 | 1/288/4038 | 8/165 = 0.04848 | 1/22 = 0.04545 | 1/51 = 0.01961 |
| 10 | 1/642/14076 | 13/267 = 0.04869 | 5/318 = 0.01572 | 5/219 = 0.02283 |
| 11 | 1/1403/49506 | 7/144 = 0.04861 | 1/57 = 0.01754 | 19/789 = 0.02408 |
| 12 | 1/3075/173690 | 34/699 = 0.04864 | 14/831 = 0.01685 | 19/906 = 0.02097 |
| 13 | 1/6735/605267 | 55/1131 = 0.04863 | 23/1344 = 0.01711 | 16/807 = 0.01983 |
| 14 | 1/14791/2091885 | 89/1830 = 0.04863 | 37/2175 = 0.01701 | 17/876 = 0.01941 |
| 15 | 1/32454/7206385 | 16/329 = 0.04863 | 23/1425 = 0.01614 | 83/4242 = 0.01957 |

`table_base.py` also prints: zero entries `[(3, 2)]` (only `2+1`), negative entries `[]`, minimum positive entry `5/318` at `(n, π) = (10, 3)`. The all-classes sections (`n ≤ 8`, every range up to 7) print exactly one `LOW` line below `1/50`: `2+1`.

**Two different margins, and the mg-95d3 correction.** This file's margin is the **δ-margin** `δ(P) − 1/3`. The margin in KSBFT-J §2.3 is the **ONE-PT margin**: the distance to the boundary of a pair that is balanced in both `P` and `P − v`. The audit mg-95d3 (`docs/AUDIT-mg-eedd.md`) found KSBFT-J's ONE-PT margin claims BROKEN. That margin is 0 at small indecomposable posets (`F_3 = 2+1`, `2+2`), its canonical version is 0 at `n = 5, 6, 8`, and its minimum at `n = 10` is `5/318 < 1/51`. **Nothing here consumes 1/51, 1/159, or any ONE-PT margin.** For the δ-margin, the table above is the census the audit asks for. The only zero is `2+1` (`2+2` has `δ = 1/2`). So H(D, μ) for the δ-margin needs exactly one exception, `2+1`, which is equivalent to a base cut-off `n₀ = 4`. The two margins satisfy `ONE-PT margin ≤ δ-margin` (the ONE-PT pair is balanced in `P`). They coincide in value at the `n = 10` minimiser, where both are `5/318`, but they are different quantities. mg-2912's 0.3489 floor is a δ-statement.

Reading:
- `δ = 1/3` exactly occurs **only** for `2+1`. No other indecomposable poset in these classes is within `5/318` of 1/3.
- The minimisers at `π = 3` from `n = 10` on are the single family `0 0 2 6 3 17 1f …` that mg-eedd found for the ONE-PT margin. That fits the elementary inequality `ONE-PT margin ≤ δ − 1/3`, which holds because the ONE-PT pair is balanced in `P`.
- The margin is flat in `n` (0.0157–0.0175 for `n = 10..15`). This matches mg-2912's "flat in `n`". **I did not recompute mg-2912's 0.3489 at `n = 21`.**

**Formulation (H(D, μ)).** Every indecomposable non-chain `P ∈ Π_D` other than `2+1` has `δ(P) ≥ 1/3 + μ`. The data fit `μ = 5/318` for `D = 3, 4` (EMPIRICAL, `n ≤ 15`). Theorems 5.1 and 5.2 prove only `δ ≥ 1/3` (μ = 0); §2.4 explains why the certificate also yields a positive μ **for all sufficiently long P**, but not for all `P`.

---

## 2. The prefix certificate (PROVEN)

### 2.1 Two windows

**Lemma 2.1 (bandwidth, PROVEN).** Let `P ∈ Π_D` and let `L` be a linear extension. If `x ∥ y` sit at positions `i < j` of `L`, then `j − i ≤ 2D − 1`.

*Proof.* Let `z` sit strictly between them. `z` cannot be below `x` (it comes after `x` in `L`) or above `y`. If `x < z` and `z < y`, then `x < y`, which is false. So `z ∥ x` or `z ∥ y`. Hence `j − i − 1 ≤ (π(x) − 1) + (π(y) − 1) ≤ 2D − 2`. □

**Lemma 2.2 (ideal window, PROVEN).** Let `P ∈ Π_D`, let `L` be a linear extension, and let `J` be an ideal with `|J| = s`. Then `J` lies within the first `s + D` positions of `L`. Consequently, if `Q` is an ideal of `P` with `|Q| ≥ s + D`, then every ideal of `P` of size `s` is contained in `Q`. The ideals of size `s` of `P` are **exactly** the ideals of size `s` of the poset `Q`.

*Proof.* Suppose `x_j ∈ J` sits at position `j > s + D`. At most `s − 1` of the `j − 1` earlier positions hold elements of `J`, so at least `j − s > D` earlier elements `x_i ∉ J`. None of them is below `x_j` (`J` is down-closed), and none is above it (it comes earlier in `L`). So `π(x_j) > D`, a contradiction. For the consequence, choose `L` to begin with a linear extension of `Q`. This is possible because `Q` is down-closed. Then `J ⊆` first `s + D ≤ |Q|` positions `= Q`. An ideal of the poset `Q` is an ideal of `P` because `Q` is down-closed, and conversely an ideal of `P` inside `Q` is an ideal of `Q`. □

### 2.2 The mixture identity

**Lemma 2.3 (ideal mixture, PROVEN).** Let `s ≥ 1`, let `𝒥_s` be the set of ideals of `P` of size `s`, and let `x ∥ y` belong to every `J ∈ 𝒥_s`. Then

  `p_P(x<y) = Σ_{J ∈ 𝒥_s} w_J · p_J(x<y)`,  where `w_J = e(J)·e(P∖J)/e(P) > 0` and `Σ w_J = 1`.

In particular `min_J p_J ≤ p_P ≤ max_J p_J`.

*Proof.* A linear extension `L` of `P` determines `J` = its first `s` elements (an ideal of size `s`), `L|_J ∈ L(J)` and `L|_{P∖J} ∈ L(P∖J)`, and conversely every such triple concatenates to a linear extension. Since `x, y ∈ J`, "`x` before `y` in `L`" is "`x` before `y` in `L|_J`". Summing over `J` gives `e(P) p_P = Σ_J e(P∖J) N_J(x<y)`, with `N_J = e(J) p_J`. □

This is the exact form of the transport. Lemma R reweights by one slot count `w_v ∈ [1, π(v)+1]`, and its error comes from the spread of that weight. Here the weights `w_J` can be anything, but they average quantities `p_J` that are all balanced, so the error is zero.

**Theorem 2.4 (prefix certificate, PROVEN).** Let `P ∈ Π_D`, let `Q` be an ideal of `P` with `|Q| = t`, and let `s ≤ t − D`. Let `𝒥` be the set of ideals of the poset `Q` of size `s`, and `K = ∩𝒥`. Suppose `x, y ∈ K`, `x ∥ y`, and `p_J(x<y) ∈ [1/3, 2/3]` for every `J ∈ 𝒥` (**"`Q` is certified at `s` by `{x,y}`"**). Then `{x, y}` is balanced in `P`. More precisely, `dist(p_P(x<y)) ≥ min_J dist(p_J(x<y)) =: rm`.

*Proof.* By Lemma 2.2, `𝒥` is the set of size-`s` ideals of `P`, and `x, y` lie in each of them. By Lemma 2.3, `p_P` is a convex combination of the `p_J`, all in `[1/3 + rm, 2/3 − rm]`, which is convex. □

Note that `P` can be arbitrarily large. The certificate is a property of the finite poset `Q`.

### 2.3 Which Q must be checked

**Definition.** A poset `Q ∈ Π_D` with `|Q| = t` is **CUT** if it has an ideal `I` with `1 ≤ |I| ≤ t − 2D + 1` and `a < b` for all `a ∈ I`, `b ∈ Q∖I` (a "strong cut" low in `Q`).

**Lemma 2.5 (PROVEN).**
- (a) If `P ∈ Π_D` is indecomposable and `Q` is an ideal of `P` with `|Q| = t < |P|`, then `Q` is not CUT.
- (b) If `Q' ∈ Π_D` is not CUT, `|Q'| = t`, and `z` is a maximal element of `Q'`, then `Q' − z` is not CUT (as a poset of size `t − 1`).
- (c) An indecomposable `P` is not CUT. So every indecomposable `P ∈ Π_D` of size `n` appears in the list of non-CUT classes of size `n`, and by (b) the pruned generator (`pcert gencut`: add a new maximal element in every way, keep range `≤ D` and non-CUT, canonicalise) produces **every** non-CUT class of each size.

*Proof.* (a) Let `I` be a strong cut of `Q` with `k = |I| ≤ t − 2D + 1`. Take `L` = a linear extension of `I`, then of `Q∖I`, then of `P∖Q`. This is valid because `I` and `Q` are ideals. For `a ∈ I` (position `≤ k`) and `b ∈ P∖Q` (position `≥ t+1`), the gap is `≥ t + 1 − k ≥ 2D`, so `a` and `b` are comparable by Lemma 2.1, and `a < b` because `a` comes first. With `a < b` for `b ∈ Q∖I` too, `G(P)` has no edge between `I` and `P∖I ≠ ∅`, so it is disconnected. (b) The same argument applies inside `Q'`, with `P := Q'` and `Q := Q' − z` (an ideal of `Q'`, since `z` is maximal) and `t − 1` in place of `t`: a strong cut of `Q' − z` of size `≤ (t−1) − 2D + 1` is a strong cut of `Q'` of size `≤ t − 2D + 1`. (c) A strong cut of `P` disconnects `G(P)`. For the generator: every non-CUT `Q'` of size `t` is `(Q' − z) + z` with `Q' − z` a non-CUT class of size `t − 1` (by (b)) and `z` added as a new maximal element whose down-set is an ideal. By induction on `t`, the list is complete. □

*Check (EMPIRICAL).* The pruned counts equal the full range-`≤ 3` census minus its CUT members at every `t = 9..13` (`out_controls.txt`): 938, 2 001, 4 224, 9 307, 20 459.

### 2.4 Margin, and what "self-sustaining" becomes

With the certificate, the margin that an induction would have to carry is `rm(Q) = max_{s, pair} min_J dist(p_J)`. It depends only on the size-`t` ideal `Q`, and it bounds `δ(P) − 1/3` from below for **every** `P` above `Q`. So:

**Corollary 2.6 (PROVEN, given the computations of §5).** For every indecomposable `P ∈ Π_3` with `n ≥ 12`, `δ(P) ≥ 1/3 + 1/96`. For every indecomposable `P ∈ Π_4` with `n ≥ 16`, `δ(P) ≥ 1/3 + 1/150`.

*Proof.* Theorem 2.4 with the worst `rm` in `out_cert_d3.txt` (`t = 11`) and `out_cert_d4.txt` (`t = 15`). □

This is **H(3, 1/96)** for `n ≥ 12`. Combined with the base table of §1, H(3, μ) holds for every indecomposable non-chain other than `2+1` with `μ = min(1/96, 5/318) = 1/96` (PROVEN (computer)). Likewise H(4, 1/150). It is not the empirical `5/318`: the certificate sees only a bracket, not the true `p_P`.

---

## 3. Why the deletion induction cannot carry a fixed margin (item 2)

**Prop 3.1 (PROVEN).** Let `r ≥ 2` and `μ > 0`. For no `p' ∈ [1/3 + μ, 2/3 − μ]` is Lemma R's window `W_r(p') = [p'/(p' + r(1−p')), r p'/(r p' + 1 − p')]` contained in `[1/3 + μ, 2/3 − μ]`. Even at `μ = 0`, containment holds only for `r = 2`, `p' = 1/2`.

*Proof.* The lower end `≥ 1/3 + μ > 1/3` requires `3p' > p' + r(1 − p')`, i.e. `p' > r/(r+2) ≥ 1/2`. The upper end `≤ 2/3 − μ < 2/3` requires `3rp' < 2rp' + 2 − 2p'`, i.e. `p' < 2/(r+2) ≤ 1/2`. These contradict each other. At `μ = 0` the inequalities are non-strict and force `r/(r+2) ≤ p' ≤ 2/(r+2)`, so `r ≤ 2`. □

In an indecomposable `P` with `n ≥ 2` every `v` has `π(v) ≥ 1`, i.e. `r ≥ 2`. So from "`P − v` has a pair of margin `μ`" Lemma R certifies nothing about `P`, for every `μ > 0`. The margin cannot be sustained by Lemma R, whatever D.

**The telescoping alternative, and its failure (EMPIRICAL).** Replace Lemma R by a transport bound that decays with distance: `|p_P − p_{P−v}| ≤ ε(d)` for pairs at `G(P)`-distance `≥ d` from `v`. Then margin `μ` in `P − v` gives `μ − ε(d)` in `P`. A fixed `μ` is never self-sustaining. The best possible is a budget: an induction started from a base with margin `μ_0` survives as long as the accumulated `Σ ε` stays below `μ_0`. That requires, at every step, a pair at distance `≥ d` from the deleted `v` whose margin exceeds `ε(d)`. `pcert decay` measures both sides (`out_decay.txt`, `Π_3` indecomposable, `v` of minimal range):

| d | uniform ε(d) = max `|p_P − p_{P−v}|` (π(v)=1 / 2 / 3), n = 13 | worst margin of a pair at distance `≥ d` balanced in P and P−v, n = 10 / n = 13 |
|---|---|---|
| 1 | 0.1716 / 0.1983 / 0.2004 | 0.0145 / 0.0155 |
| 2 | 0.0730 / 0.0769 / 0.0721 | 0.0145 / 0.0155 |
| 3 | 0.0283 / 0.0294 / 0.0254 | 0.0128 / 0.0155 |
| 4 | 0.0107 / 0.0125 / 0.0109 | **−0.0265 / −0.0269** (no such pair in some P) |
| 5 | 0.0041 / 0.0048 / 0.0043 | −0.066 / −0.066 |

At every `d` the uniform error exceeds the worst available margin. For `d ≤ 3` the margin is too small; from `d = 4` on, some posets have no balanced pair that far from `v`. **So the deletion induction breaks at D = 3 already, and it breaks at the step "choose a pair far from v", not at the decay estimate.** Balanced pairs are not spread through `P`: in the extremal family they sit near the ends, as in `F_m`, where only the end pairs are balanced. A deletion at the far end is then the right move, but it needs the pair's `p` to be stable **uniformly in the size of `P`**, which is exactly what Lemma 2.3 supplies without any decay estimate. The certificate is this idea made exact. It conditions on the whole bottom level instead of deleting one point at the top.

(I did not try deletion rules other than "minimal range" with the `G`-distance, for example "`v` = the h-last element and pairs near the h-first end". KSBFT-J §5.1's CONJECTURED route is of that form. §2 makes it unnecessary for `D ≤ 4`.)

---

## 4. Covariance decay (item 4, EMPIRICAL)

Instrument `pcert decay`, over every indecomposable member of `Π_3`, `n = 10..13`, every `v`, and every pair `∌ v`. It records the exact `|p_P − p_{P−v}|`, which by Lemma R(2) equals `|Cov_{P−v}(w_v, 1{x<y})| / E'[w_v]`, bucketed by `π(v)` and by the `G(P)`-distance `d` from `v` to the nearer of `x, y`. Transcript: `out_decay.txt`.

- `ε(1) = 0.17157 = 3 − 2√2` at `π(v) = 1`. This is Lemma R's supremum (mg-eedd), reached by pairs adjacent to `v`.
- Successive ratios `ε(d+1)/ε(d)` for `π(v) = 1`, `n = 13`: 0.425, 0.388, 0.380, 0.386, 0.397, 0.415, 0.35, 0.38, 0.33 (the tail has few pairs). For `π(v) = 2, 3` they are 0.39–0.43. The geometric rate is ≈ `0.38–0.41 ≈ 1/φ² = 0.382` (CONJECTURED: the extremal decay is the Fibonacci transfer rate).
- **Flat in `n`.** `ε(d)` at `n = 10` and `n = 13` agree to 2–3 significant digits wherever both exist (e.g. `d = 4`, `π(v) = 1`: 0.01064 vs 0.01074). The decay is a local property, as F1/F2 locality predicts.

A proof of such decay would presumably come from Birkhoff contraction of the ideal transfer matrices. By Lemma 2.2, blocks of `2D` consecutive levels are strictly positive matrices. **I did not attempt it.** Given §3, it would not rescue the deletion scheme anyway.

---

## 5. The theorems at D = 3 and D = 4

Instrument `pcert cert` computes, for every class `Q` of a non-CUT list of size `t` and every `s = 2..t−D`, the robust margin `rm(Q, s)` of Theorem 2.4. It uses exact `__int128` counts and integer comparisons, and flags CUT. Transcripts: `out_cert_d3.txt`, `out_cert_d4.txt`, `out_cert_d5.txt`. `AGG CT t total CUT fail failCUT` gives the counts. `AGG CS t s #certified-at-s worst-rm-at-s` gives the per-`s` data. `AGG CW` gives the worst `rm` with its poset.

| D | t | non-CUT classes | uncertified | worst rm (max over s) |
|---|---|---|---|---|
| 3 | 9 | 938 | 13 | −1/39 |
| 3 | 10 | 2 001 | 4 | −1/39 |
| 3 | **11** | **4 224** | **0** | **1/96** (at s = 8) |
| 3 | 12 | 9 307 | 0 | 1/96 |
| 3 | 13 | 20 459 | 0 | 4/303 |
| 4 | 10 | 29 491 | 990 | −2/15 |
| 4 | 11 | 103 198 | 943 | −4/57 |
| 4 | 12 | 357 363 | 496 | −2/51 |
| 4 | 13 | 1 224 360 | 192 | −4/183 |
| 4 | 14 | 4 177 332 | 14 | −1/417 |
| 4 | **15** | **14 298 595** | **0** | **1/150** |
| 5 | 12 | 3 740 359 | 127 288 | −1/6 |
| 5 | 13 | 17 890 772 | 141 882 | −4/39 |

At `D = 3`, the single value `s = 8` certifies every class at `t = 11, 12, 13` (`AGG CS 1x 8`). The uncertified classes at `t = 9, 10` (13 + 4; all are printed in `out_cert_d3.txt`) all begin with the gadget `0 0 2 6 3` followed by `13 f`, `17 f` or `f 17`. That is the gadget of the low-δ-margin family of §1.

**Theorem 5.1 (PROVEN (computer)).** Every non-chain `P ∈ Π_3` has a balanced pair.

*Proof.* By strong induction on `n`. If `P` is decomposable, `P = S₁ ⊕ … ⊕ S_k` and some `S_i` is not a singleton (`P` is not a chain). `S_i` is indecomposable, lies in `Π_3` and is smaller, and its balanced pair is balanced in `P` (KSBFT-J Lemma 1.1). If `P` is indecomposable with `n ≤ 11`, it appears in the list `c3_n` (Lemma 2.5(c)), and `out_base.txt` shows every indecomposable non-chain there has `δ − 1/3 ≥ 0`. If `P` is indecomposable with `n ≥ 12`, take any ideal `Q` of size 11. `Q ∈ Π_3` because range does not increase in induced subposets, `Q` is not CUT (Lemma 2.5(a)), and its class is in `c3_11` (Lemma 2.5(c)). There it is certified at `s = 8` (`out_cert_d3.txt`: `AGG CT 11 4224 0 0 0`), so `P` has a balanced pair (Theorem 2.4). □

**Theorem 5.2 (PROVEN (computer)).** The same for `Π_4`, with base `n ≤ 15` (`out_base.txt`, `## D=4`) and certificate `t = 15` (`AGG CT 15 14298595 0 0 0`).

What these theorems consume: Lemmas 2.1–2.5 (proven here), KSBFT-J Lemma 1.1 (standard, proven there), mg-eedd's `lecount` and canonical form (both controlled there and re-controlled here, §5.1), and the transcripts. They consume **nothing** from KSBFT (no Lemma 4.2, no 441, no eq. (1.5)), BW92, Peczarski, or Gup26.

### 5.1 Controls (`out_controls.txt`)

`check_controls.py` asserts every line below. Its transcript is `out_check_controls.txt` (VERDICT: GREEN), and it exits 1 if any negative control stays silent (tested by planting a zeroed firing count, which turns it RED).

- **Counter.** Inherited from mg-eedd and re-run: Fibonacci closed form (MATCH) and brute-force permutation counts on random posets with all their deletions (MATCH).
- **Generator.** Pruned counts equal the filtered full census at `t = 9..13` (§2.3). The full census's own positive control is OEIS A000112 for `n ≤ 8` (`out_gen.txt`).
- **Theorem 2.4 end to end (e2e).** For every indecomposable `P ∈ Π_3` with `n = 12, 13` (3 076 + 6 736), every size-11 ideal `Q` of `P`, and every pair in `K`, the program checks the bracket `min_J p_J ≤ p_P ≤ max_J p_J` against the **directly counted** `p_P`, and checks that the certifying pair is balanced in `P`. Result: **0** bracket violations over 48 840 + 122 280 pair checks, and 0 unbalanced certificates. The same holds for `Π_4` at `t = 11` on 612 003 indecomposable posets (0 of 12 126 488).
- **e2e FIRING control.** Using `s = t − D + 1`, one more than Lemma 2.2 allows, the ideal family misses ideals of `P` and the argument breaks. Measured: 7 178 and 17 877 bracket violations for `Π_3`, with 8 and 28 "certified" pairs that are **unbalanced in `P`**, and 517 886 violations for `Π_4`. So the instrument detects exactly the failure the lemma rules out.
- **cert FIRING control.** Narrowing the interval to `[2/5, 3/5]` and `[7/20, 13/20]` must make certification fail. At `D = 3`, `t = 13` it does: 1 265 and 64 uncertified classes.

---

## 6. Novelty and what the result is worth

- `D ≤ 6` is **known** (BW92 `D ≤ 5`, Peczarski `D ≤ 6`, the latter with extensive computation). Theorems 5.1 and 5.2 are **re-proofs**, and their value is as a **test of the method**, as the ticket specifies.
- I have not read BW92 or Peczarski. The prefix/ideal-mixture argument is elementary. It is plausible that BW92, and certainly a computer search like Peczarski's, uses a bottom-of-the-poset argument of this shape. **Novelty: UNCHECKED.** An auditor with the papers should compare them.
- What the method **does** buy over the KSBFT-J line: exact transport (no Lemma-R loss), no decay estimate, a base case of `n ≤ 11` instead of 16, and a positive margin `1/96` for all long indecomposable `P ∈ Π_3`. That last is a statement of H(3, μ) type that the ticket asked for. (For `D ≤ 6` a positive margin is not implied by `δ ≥ 1/3` results unless they prove one. I did not check whether BW92 or Peczarski do.)

## 7. Where D = 7 stands, and what would have to change

- **Cost (EMPIRICAL).** `t(D) = 4D − 1` for `D = 3, 4` (fitted on two points, so CONJECTURED as a law). Non-CUT class counts at `D = 5` are 46 421 / 178 180 / 798 563 / 3 740 359 / 17 890 772 at `t = 9..13` (`out_gen.txt`), growing ×4.7–4.8 per step; the uncertified fraction falls 10.7% → 3.4% → 0.79% at `t = 11, 12, 13`. `t = 19` would need ~10¹¹ classes, which is not feasible here. `D = 7` at `t ≈ 27` is far beyond reach.
- **Levers, not attempted.**
  1. A sharper bracket. The weights `w_J ∝ e(J)·e(P∖J)`, with `e(J)` known from `Q`, and `e(P∖J)/e(P∖J')` constrained by Lemma-R-type insertion ratios, give an LP bracket strictly inside `[min p_J, max p_J]`. This might lower `t` by a little.
  2. Replacing enumeration of whole prefixes by propagating interval brackets through the finite automaton of `2D`-windows (abstract interpretation of the ratio vectors `a_E/a` over ideal states). This would make the cost polynomial in the number of window types rather than in the number of prefix classes.
  3. Using the dual (suffix) certificate for the prefixes that fail. This requires pairing prefixes with suffixes, and I did not pursue it.
- Neither lever is PROVEN to suffice. **D = 7 is open. This ticket did not settle it.**

## 8. What I did not do, and the negatives

**Not done:**
- Read BW92, Peczarski or Gup26. The novelty of §2 is unchecked (§6).
- Recompute mg-2912's `n = 21` value 0.3489.
- Any proof of covariance decay (§4 is measurement only), or any Birkhoff-contraction bound.
- `D = 5` certification (stopped at `t = 13`: 141 882 uncertified), and `D ≥ 6` at all.
- `Π_3` census past `n = 13` of my own. For `n = 14, 15` the base tables use the `c3`/`c4` lists, which contain every indecomposable poset (Lemma 2.5(c)). mg-eedd's `n = 16` range-3 census was not re-run, because Theorem 5.1 does not need it.
- The margin tables (§1) and §4 are EMPIRICAL. Only Theorems 5.1 and 5.2, Corollary 2.6 and Prop 3.1 are claimed as proofs.

**Negatives (candidates tried that FAIL):**
1. *Fixed-margin induction via Lemma R.* Impossible for every μ > 0 (Prop 3.1).
2. *Deletion of a minimal-range `v` with a pair at `G`-distance `≥ d`, transported by the uniform decay bound.* It fails at every `d` at `D = 3` (§3 table): the margin is too small for `d ≤ 3`, and from `d = 4` there is no balanced pair that far away.
3. *Prefix certificate with short prefixes.* `t ≤ 10` at `D = 3` (4 failures at `t = 10`) and `t ≤ 14` at `D = 4` (14 failures at `t = 14`).
4. *Prefix certificate at `D = 5`, `t = 12`.* 127 288 failures.
5. *Certificate with interval `[2/5, 3/5]` or `[7/20, 13/20]`* (firing controls). Fails at `D = 3`, `t = 13`, as it must, because the Fibonacci-type end pairs sit near 0.38.

## Sources

- [Brightwell–Wright 5-thin (citation via Olson–Sagan, "On the 1/3–2/3 Conjecture", Order)](https://link.springer.com/article/10.1007/s11083-017-9450-3)
- [Peczarski, The Gold Partition Conjecture for 6-Thin Posets, Order 2008](https://link.springer.com/article/10.1007/s11083-008-9081-9)
