# AUDIT of mg-c929 (KSBFT-D, `docs/KSBFT-D-sec6-eps-spec.md`) — mg-e015

Auditor: an independent polecat with fresh context. I am not the author. The subject is
`docs/KSBFT-D-sec6-eps-spec.md` as of `66c68dc`, with its instrument `code/ksbft_sec6_c929/`. The
paper is `/Users/daniel/files/KSBFT_v7.pdf`, pp. 17–25 (§5–§6). I read it with `pdftotext -layout`,
and I rendered p. 24 to an image to settle one exponent that the text extraction garbles.
Page and equation numbers below are the printed ones.

Verdict scale:
- **HOLDS**: re-derived here, or re-computed independently.
- **BROKEN**: false as stated.
- **OVERSTATED**: the true content is weaker than the words, or the sourcing is weaker than the
  words claim.
- **UNVERIFIABLE**: not checkable with what I had.

Instrument: `code/audit_ksbft_e015/indep_e015.py`. Run it with `sh run_all.sh`, about 15 s, one
process, deterministic. It shares **no code** with `code/ksbft_sec6_c929/`:
- It has its own poset generator (each element gets an order ideal of the earlier elements as its
  down-set). The A006455 counts 2, 7, 40, 357, 4824 are its positive control.
- It computes pair probabilities as exact `Fraction`s.
- It evaluates the constants from KSBFT's printed formulas, not from c929's `s3`.
- It has its own parallel-chain computation, an exact hypergeometric formula cross-checked by
  brute force for `m ≤ 7`.
- It has a negative control: the separation check with its hypothesis removed must FIRE, and it
  does, at slack `−ε₀/√3` on the 2-antichain.

---

## 0. Headline

**The flashiest claim, Prop B, HOLDS.** For every finite `P` with `δ(P) ≤ 1/e − ε`,
`E[inv_h] ≤ C(ε)·n`, conditional on exactly the inputs KSBFT §6 uses:
- AK25a Cor 5.1(a), for log-concavity;
- AK25a Thm 2.9, through (5.3c) and (6.7);
- Haq26 Thm 4.1, through Lemma 5.5;
- LV07 Lemmas 5.4, 5.5(a) and 5.7, which are published.

§5–§6 never cite AK25b, and never use a width hypothesis. §6 proves the contrapositive, "(6.1)
⟹ gap bounded", for **every** finite `P`, so nothing fails at `δ ≤ 1/3`. I re-derived every step
of §6.2–§6.4 myself (§2 below). The constant `C(ε₀) = 2.964×10¹⁷` and the width bound
`1.301×10¹⁴` recompute exactly from the paper's own formulas.

**The defects are small:**
- **BROKEN (minor remark):** the claim that (6.12)'s `/ε³` "is loose, `/ε²` would do". The paper's
  integral step gives `5/ε²` (p. 24, checked on the rendered page), so `/ε³` is necessary.
- **OVERSTATED (sourcing):** "no inequality `E[inv] ≤ C·Σ win` holds for all posets" rested on
  EMPIRICAL data up to `m = 11` plus a CONJECTURED `Θ(n^1.5)` growth. **The statement is true.**
  §4 below gives a proof (`I* ≥ m^{1.5}/28`).
- **OVERSTATED (wording, three places)**, listed in the table.
- **UNVERIFIABLE:** everything cited to AK25a beyond KSBFT's quotation of it (Ex 11.2, and the
  attribution "Thm 2.10"). I did not read AK25a, Haq26 or Air26.

---

## 1. Every PROVEN claim, with verdict

The first column is the section of the c929 document.

| # | claim (c929 §) | c929 label | verdict | how checked |
|---|---|---|---|---|
| 1 | **Prop B**: `δ(P) ≤ 1/e−ε ⟹ E[inv_h] ≤ C(ε)n`, `C = 2√3·e·G/ε³`, `G = max(10e(1+√3)/ε³, 4A log²A)`, `A = 18432√3/ε³` (§4) | PROVEN cond. §6 | **HOLDS** | §2, every step re-derived; EMPIRICAL S1/S3/S5/S6 at `n ≤ 6` |
| 2 | Prop B uses AK25a + Haq26 only, **not AK25b** (§0, §4) | PROVEN by reading | **HOLDS** | `grep` of the whole paper: AK25b is cited only at p.3 and p.5 (Thm 1.5) and in §7.2. §5–§6 cite AK25a Cor 5.1(a), (24), Thm 2.9, Haq26 Thm 4.1 and LV07, nothing else |
| 3 | No Thm 1.4 width hypothesis is used (implicit) | — | **HOLDS** | §6 opens with "(6.1)" and nothing else. (6.8) is a case split, not an assumption: when it fails, the gap is `< G1` directly |
| 4 | `C(ε₀) ≈ 2.96×10¹⁷` (§0, §4) | arithmetic | **HOLDS** | `2.964e17`, recomputed; `ε₀ = 0.0345461` |
| 5 | Counterexample width `≤ 1.30×10¹⁴` at `ε₀` (§0 side result) | PROVEN cond. | **HOLDS** | (6.5)·G and the paper's final display `442368/ε⁴·log²(18432√3/ε³)` both give `1.301e14`. A counterexample has `δ < 1/3 < 1/e − ε₀`. When (6.8) fails the bound is `2√3·G1/ε₀ ≈ 1.8e8`, which is smaller |
| 6 | Paper's `K` at `ε = 10⁻¹⁰⁰` is `≳ 10⁴⁰⁰` (§0) | arithmetic | **HOLDS** | `log10 = 411.3` |
| 7 | `L* = L(K+1, 1/6)` may use this `K` (§0) | — | **HOLDS** (cond., now also on AK25b for Thm 1.5) | `w ≤ 1.301e14 < K+1` |
| 8 | `ε_spec ≤ 6Cn/(n²−1)` via F21 (§0, §4) | PROVEN cond. | **HOLDS** | F21: `E[inv_e] = Σ_{x∥y} min(p,1−p)` for `δ ≤ 1/3`, with 0 exact mismatches on my 39-poset population. Step 6 gives `Σ min ≤ E[inv_h]` |
| 9 | Thresholds `n ≥ 1.778e18` (for ≤1), `1.067e19` (for ≤1/6), `8.891e19` (for ≤2e-2) (§0, s3) | arithmetic | **HOLDS** | recomputed |
| 10 | `g ≤ A log²g ⟹ g ≤ 4A log²A` (§1, Step 4) | PROVEN (s3 numeric) | **HOLDS**, and in general form | it holds iff `L > log 4 + 2 log L` with `L = log A`, and `g/log²g` is increasing for `g > e²`. At `ε₀`: `20.47 > 7.42` |
| 11 | "(6.12)'s `/ε³` where `/ε²` would do" (§1) | stated as a reading | **BROKEN** (minor) | p. 24 prints `Σ ≤ (5/ε²)e^{−ε√j₀/2}`. Times `2e(1+√3·gap/ε)`, that is `≈ 10e√3·gap/ε³`. A `/ε²` version is smaller than the true prefactor by a factor of about 18 at `gap = 1e6` (`6.2e10` vs `1.14e12`) |
| 12 | `1/e` enters exactly once, at (5.1), and is consumed once, in Lemma 6.1 (§0, §1) | PROVEN by reading | **HOLDS** | read. The other `e`'s, in (5.2), (6.8) and (6.11), are the tail constant `e^{1−t}` |
| 13 | "Every other constant in §6 is a power of the deficit" (§0.2) | by reading | **OVERSTATED** (wording) | the constants are `poly(1/ε)·log²(1/ε)` times absolute numbers (288, 18432, `√3`, `e`). c929's own table shows this |
| 14 | `1/e` is sharp for per-pair inputs (AK25a Ex 11.2) (§0, §1) | CITED | **UNVERIFIABLE**, but the reduction HOLDS | Given the example (`Δ = 0` pairs with `δ_xy ≤ 1/e + ε`), `c ≤ 1/e` follows. That is consistent with (5.1), which forces `δ_xy ≥ 1/e` when `Δ = 0` |
| 15 | `c* = 1/2` over all `n ≤ 6` (§1) | EMPIRICAL | correctly labelled. `c* ≤ 1/2` is trivial (2-antichain). **OVERSTATED** (wording): "cannot be seen failing at any `n` we can enumerate" when only `n ≤ 6` was enumerated |
| 16 | `h(x) = 1 + Σ_y p(y,x)`; `δ, h, Δ, gap` are pair-bias (§2) | PROVEN | **HOLDS** | `f(x) = 1 + #{y : f(y) < f(x)}` holds for any measure on `S_n` |
| 17 | `d² = Var(f(x)−f(y)) + E[|k|(n+1−|k|)]/(n+2)`, and `d` is not pair-bias (§2) | PROVEN | **HOLDS** | formula re-derived (Beta spacing). **The audit supplies the missing witness** (section D): on `S_3`, the uniform law and `μ₂ = (1/12, 1/6, 1/4, 1/6, 1/4, 1/12)` have identical pair marginals, yet `Var(f(0)−f(2))` is `2` vs `3/2` |
| 18 | `a_x` is not pair-bias (§2) | PROVEN | plausible, **not witnessed** by either document | c929's argument is "needs the law of `max_{y≺x} f(y)`". No explicit pair of measures is given. Nothing downstream consumes it |
| 19 | No §6 step is a pair-bias statement (§2) | by reading | **HOLDS**, with a wording note | Lemma 5.5 relates `h` to the ideal structure, and in the measure setting the ideal structure is itself determined by the pair marginals (`p ∈ {0,1}`). The correct reason it is not "pair-bias-only" is that it is valid only for **realizable** laws. c929's §0.3 says exactly this ("realizability fact") |
| 20 | **Prop A**: the two-atom law gives a pair-bias Thm 1.4 constant of `0` and kills a pair-bias Prop B (§2) | PROVEN | **HOLDS** | §3 below: exact at `n = 5`, `t = 1/10` |
| 21 | Kahn–Saks "`Δ<1 ⟹ δ ≥ c`" in pair-bias form is killed too (§2) | PROVEN | **HOLDS** | adjacent `Δ = 1−2t = 4/5`, `δ = 1/10` |
| 22 | The only `1/6` near §6 is p.5's `ϵ = 1/6`, the margin `1/2 − 1/3` in `δ` (§0.4, §2) | by reading | **HOLDS** | p.5: "by taking `ϵ = 1/6`". §5–§6 contain no `1/6` |
| 23 | Constants at an illustrative `ε = 1/6`: `C ≈ 1.39e13`, and `n ≳ 5.0e14` for `ε_spec ≤ 1/6` (§2) | arithmetic, illustrative | **HOLDS** | recomputed. It is correctly labelled as a hypothetical input |
| 24 | **Prop D**: `Σ_x(a_x−1) = E[W] ≤ m` (§3) | PROVEN | **HOLDS** | re-proved: a `z` strictly between `q(x)` and `f(x)` is neither `≺x` nor `≻x`, and an unordered pair is counted at most once per extension |
| 25 | **Prop C**: `Σ_{x∈X} a_x ≤ 2√3·H(X)/ε` under pairwise `δ_xy ≤ 1/e−ε` in `X` (§3) | PROVEN cond. L5.1 | **HOLDS** as a statement | it is the middle line of (6.7)'s proof. The step `a_x ≤ √3·Δ/ε` needs the hypothesis only for that one pair. **The label "Thm 2.10 with explicit constants" is UNVERIFIABLE** (AK25a not read) |
| 26 | Frozen class: `E[W] ≤ (2√3/ε₀)(n+1) ≈ 100(n+1)` (§3) | PROVEN cond. | **HOLDS** | `2√3/ε₀ = 100.3`, and `H ≤ n−1` |
| 27 | Parallel chains: `Σ(a_x−1) = 2m²/(m+1)` (§3) | PROVEN | **HOLDS** | hockey-stick proof re-checked; brute force exact for `m ≤ 7` |
| 28 | **"No inequality `E[inv] ≤ C·Σ win` holds for all posets"** (§3, bold; negative #3 "false in general") | EMPIRICAL (`m ≤ 11`) + CONJECTURED growth | **OVERSTATED as sourced; TRUE** | §4 below proves `I* ≥ m^{1.5}/28`. The exact computation is extended to `m = 3000`: `I*/n^{1.5} → 0.15667 ≈ √(2π)/16` |
| 29 | Footrule `E[F_h] ≤ 2Cn` (Diaconis–Graham) (§3) | PROVEN | **HOLDS** | `F ≤ 2I` holds pointwise |
| 30 | Step 0: adjoining `0̂, 1̂` preserves `δ` and the pair probabilities (§4) | PROVEN | **HOLDS** | |
| 31 | The boundary class `δ = 1/3` is inhabited; 39 of 5230 naturally labelled posets at `n ≤ 6`; 86 have `δ < 1/e` (§4, s1) | EMPIRICAL (exact) | **HOLDS** | reproduced by my own generator: 39 and 86 |
| 32 | "On those examples the bound is loose by five orders of magnitude" (§4) | EMPIRICAL | **OVERSTATED (imprecise)**, in the harmless direction | measured against the closed form with the **actual** gap, the slack is `≈ 9.1e5`. Measured against `C`, it is **18** orders (`max E[inv_h]/n = 0.222`) |
| 33 | "No `n`-free constant below 1 at any `n < 1.8e18`"; "nothing in §6 gives … below 1 at computable `n`" (§0, §5) | arithmetic | **HOLDS** for §6's printed constants | Even with every absolute constant set to 1, `C ≳ ε₀⁻⁶ ≈ 6e8`, so the threshold stays near `n ~ 10⁹`, not computable. c929 says it did not tighten |
| 34 | (5.1)–(5.5), (6.4), (6.11) re-checked at `n ≤ 6` (§1, s1) | EMPIRICAL | correctly labelled; **not presented as proof** | c929 itself calls it "weak evidence". My S1/S3 reproduce c929's C64/C611 worst slacks, `0.633914` and `2.31935` |

---

## 2. Prop B re-derived end to end

Work in `P̂`, which is `P` with `0̂` and `1̂` adjoined. Then `n̂ = n+2`, and `δ(P̂) = δ(P) ≤ 1/e − ε`,
because every new pair is comparable. All inputs below are KSBFT's. My re-derivation of each is
given.

1. **Lemma 6.1 / (6.4), height separation.**
   - (5.1): for log-concave `V` with mean `μ` and s.d. `σ`,
     `min(P[V<0],P[V>0]) ≥ 1/e − |μ|/σ`. This comes from Grünbaum (LV07 5.4) together with density
     `≤ 1` for an isotropic law (LV07 5.5a). Moving the threshold from `0` to `−μ/σ` costs at most
     `|μ|/σ`.
   - Apply (5.1) to `V = Z_x − Z_y`, which is log-concave by AK25a Cor 5.1(a). This gives
     `1/e − Δ/d ≤ δ(P;x,y) ≤ 1/e − ε`, so `d ≤ Δ/ε`. This holds for **every** distinct pair. For a
     comparable pair, `δ(P;x,y) = 0`, and the inequality still holds.
   - From (5.3): `a_x ≥ 1` (integer positions), and `d ≥ a_x/√3`. The second follows from the
     conditional law `F_x | rest ~ U[Q_x,R_x]`, total variance, Jensen, and
     `E[R_x−Q_x] = 2a_x/(n̂+1)`.
   - Therefore `Δ ≥ ε/√3` for all distinct `x, y`, and the heights are strictly ordered.
   - **Condition used:** only (6.1). **Holds at `δ ≤ 1/3` with `ε = ε₀`.**
2. **(6.6).**
   - XYZ (Shepp, continuous) gives `Cov(Z_x−Z_y, Z_z−Z_y) ≥ 0`, hence
     `d(x,z)² ≤ d(x,y)² + d(y,z)²`.
   - Chain this along consecutive `v_k, v_{k+1}`, with `d_k ≤ Δ_k/ε`. Then
     `Σ Δ_k² ≤ gap·Σ Δ_k = gap·Δ(v_i,v_j)`.
3. **(6.11).**
   - For `h(y) > h(x)`, `P[Z_y < Z_x] ≤ P[|V−Δ| ≥ Δ] ≤ e^{1−Δ/d}`, by (5.2) (LV07 5.7).
   - Then `Δ/d ≥ Δ·ε/√(gap·Δ) = ε√(Δ/gap)`.
4. **Gap bound, §6.3–§6.4.** I re-derived each line.
   - **Case (6.8) fails:** `gap < 10e(1+√3)/ε³`.
   - **Case (6.8) holds:**
     - `u, v` realise the gap in the interior, since the end gaps equal 1.
     - Every added comparison (6.9) has `Δ ≥ ℓ = R·gap·log²gap`, with `R = 288/ε²`.
     - An interval of length `gap` holds at most `1 + √3·gap/ε` elements.
     - `Σ_{j≥j₀} e^{−ε√j} ≤ e^{−ε√j₀}(1 + 2√j₀/ε + 2/ε²) ≤ (5/ε²)e^{−ε√j₀/2}`. With
       `τ = ε√j₀`, this is `(ε² + 2 + 2τ)e^{−τ} ≤ e^{−τ/2}(1 + 2(1+τ)e^{−τ/2}) ≤ 5e^{−τ/2}`.
     - `j₀ = ⌊R log²gap⌋ ≥ R log²gap/2`, so `ε√j₀/2 ≥ 6 log gap`.
     - Hence `q ≤ 10e(1+√3)/ε³ · gap^{−5} ≤ gap^{−4}`, by (6.8).
     - Lemma 6.4: `h_Q = E[Z|E]`, because `O(Q) = O(P) ∩ E`. Cauchy–Schwarz gives
       `|E[V|E]−E[V]| ≤ σ√(q/(1−q))`. Then `σ ≤ √(gap·Δ)/ε ≤ Δ/ε` for `Δ ≥ gap`, and
       `(1/ε)(gap⁴−1)^{−1/2} ≤ 1/2`, by (6.8). So `h_Q(t) − h_Q(s) ≥ gap/2`.
     - `I` remains an ideal of `Q`. A chain from `J` down into `I` would need a `P`-relation from
       `J` to `I`, and the added relations stay within `I` or within `J`.
     - Lemma 5.5 (Haq26) in `Q`: `|B₀| + |B₁| − 1 ≥ gap/2`, so `|B| ≥ gap/4`, and `H_P(B) ≤ ℓ`.
     - (6.7) in `P`, which uses AK25a Thm 2.9 through (5.3c): `gap²/16 ≤ (4√3/ε)·R·gap·log²gap`.
       Hence `gap ≤ A log² gap`, with `A = 64√3R/ε = 18432√3/ε³`.
   - Row 10 then gives `gap ≤ 4A log²A`. **No step here uses AK25b or a width hypothesis.**
5. **Summation (c929's own step).**
   - Consecutive separations add, so `Δ(v_i,v_j) ≥ (j−i)ε/√3`.
   - Therefore `P[v_j before v_i] ≤ e·exp(−c√(j−i))` with `c² = ε³/(√3·gap)`. Check:
     `ε·√((j−i)ε/(√3·gap)) = √(ε³/(√3·gap))·√(j−i)`.
   - `Σ_{k≥1} e^{−c√k} ≤ ∫₀^∞ e^{−c√t}dt = 2/c²`, because the summand is decreasing.
   - Sum over the `n` lower endpoints in `P`. Pairs with lower endpoint `0̂` have probability 0,
     and pairs with upper endpoint `1̂` are only over-counted.
   - Result: `E[inv_h] ≤ 2√3·e·gap·n/ε³ ≤ C(ε)n`.
6. **Step 6.** A comparable pair is never against the height order, because `x≺y ⟹ h(x)<h(y)`.
   For an incomparable pair, `min(p,1−p) ≤ P[against the height order]`.

**Verdict: HOLDS**, conditional on AK25a Cor 5.1(a), AK25a Thm 2.9, Haq26 Thm 4.1 and LV07.

As EMPIRICAL corroboration only, S1, S3, S5 and S6 hold with the slacks printed in
`out_indep_e015.txt`, on both the `δ ≤ 1/3` population (39) and the `δ < 1/e` population (86).
**This is weak, as c929 said:** at `n ≤ 6` every gap is tiny, so §6.3–§6.4 are never exercised.

---

## 3. Prop A: the two-atom law is valid

`μ_t = (1−t)·δ_id + t·δ_rev`, with `0 < t < 1/2`:
- It is a probability measure on `S_n`.
- Every pair marginal is in `{t, 1−t}` ⊂ `(0,1)`, so every pair is "incomparable" in the
  measure setting, and the width is `n`.
- `δ = t`.
- The heights are `h(x_i) = (1−t)i + t(n+1−i)`. They are increasing, with spacing `1−2t < 1`.
- `E[inv_h] = E[inv_id] = t·C(n,2)`.
- For `t ≤ 1/3 − η`, the law lies in mg-6bc2's `M_n(η)`: some order `e` has every pair flipped with
  probability at most `1/3 − η`. So the law is inside the candidate space the claim quantifies over.

Exact at `n = 5`, `t = 1/10` (section A): marginals `{1/10, 9/10}`, `δ = 1/10`, heights
`7/5, 11/5, 3, 19/5, 23/5`, and `E[inv_h] = 1 = t·C(5,2)`.

Taking `n = K+1` and `t → 0` forces the constant in "width `> K` ⟹ `δ ≥ c`" to be `0`, and it makes
any `O(n)` inversion bound false. **HOLDS.**

The claim needs the definition "pair-bias-only = valid on every law with the given pair marginals".
Under a narrower reading, "valid for posets, using only facts about their marginals", the two-atom
law is not a poset law, because its all-incomparable marginal matrix would have to come from the
antichain, which has `p = 1/2`. Under that reading Prop A proves nothing. c929 states the broad
definition explicitly, so this is not a defect.

---

## 4. Windows do not control inversions: a proof (upgrading c929 row 28)

This covers two chains `a₁<…<a_m` and `b₁<…<b_m`, with `n = 2m`.
- `W = Σ(a_x−1) = 2m²/(m+1) < n`.
- Let `S_N` be (#a − #b) among the first `N` positions. It is the sum of a size-`N` sample
  **without replacement** from `m` copies of `+1` and `m` copies of `−1`, and it is symmetric about 0.
- `a_i` comes before `b_j` iff `S_N ≥ s+1`, where `N = i+j−1` and `s = i−j`. So
  `min(p,1−p) = min(P[S_N>s], P[S_N≤s])`.
- For `N ≤ m`, every threshold `s ≡ N+1 (mod 2)` with `|s| ≤ N−1` is realised by a valid pair
  `(i, j)`.
- On a lattice of spacing 2, `Σ_s min(P[S>s], P[S<s]) ≥ E|S|/2`. Each value `k > 0` is counted at
  least `k/2` times, and likewise for `k < 0`.
- Hence `I* ≥ Σ_{N≤m} E|S_N|/2`.
- `Var S_N = N(2m−N)/(2m−1) ≥ N/2` for `N ≤ m`.
- Hoeffding (1963, Thm 4): sampling without replacement is dominated in convex order by sampling
  with replacement. So `E S_N⁴ ≤ 3N² − 2N ≤ 3N²`.
- Hölder, `E S² ≤ (E|S|)^{2/3}(E S⁴)^{1/3}`, gives `E|S_N| ≥ (N/2)^{3/2}/(√3N) = √N/(2√6)`.
- Summing over `m/2 ≤ N ≤ m` gives **`I* ≥ m^{1.5}/(8√12) > m^{1.5}/28`**, so `I*/W ≥ √m/56 → ∞`.
- `E[inv]` against **any** fixed order is at least `I*`, and the footrule is at least `inv`. So
  neither inversions nor footrule are `O(Σ win)` in general. □

The chain `I* ≥ Σ E|S_N|/2 ≥ bound` is checked numerically in section W for `m ≤ 200`. The exact
`I*/n^{1.5}` is `0.15845` at `m = 11` and `0.15667` at `m = 3000`, matching the heuristic constant
`√(2π)/16 = 0.15666`.

As c929 says, the witness has balanced pairs, so this says nothing about the no-balanced-pair class.

---

## 5. Negatives versus the candidate space

| c929 negative | candidates tried | verdict |
|---|---|---|
| 1. Pair-bias-only Thm 1.4 / Lemma 6.1 / Kahn–Saks / Prop B | one witness, the two-atom law, covers all four | **HOLDS**. A single law suffices, because every candidate is a universally quantified pair-bias statement |
| 2. A per-pair constant larger than `1/e` in (5.1) | AK25a Ex 11.2 (cited) | **UNVERIFIABLE** here |
| 3. `E[inv] ≤ C·Σ win` in general | parallel chains | **HOLDS**, now PROVEN (§4). c929 had it only EMPIRICAL + CONJECTURED |
| 4. Windows ⟹ footrule without the gap | "no route found", one idea (a spread lower bound cannot bound displacement) | honestly labelled as a non-finding. In general it is **refuted** by §4, since footrule ≥ inv ≥ I*. On the no-balanced-pair class it is open, as c929 says |
| 5. No `1/6` in §6's mechanism | read §5–§6 | **HOLDS** |

**EMPIRICAL vs proof.** c929 labels s1 and s2 as EMPIRICAL throughout and calls s1 "weak evidence".
The one place where EMPIRICAL was allowed to read as proof is row 28, the bold "No inequality …
holds". It was true anyway (§4).

---

## 6. What I did NOT do

- I did not read AK25a, AK25b, Haq26, Air26 or LV07. Everything they supply is taken as KSBFT quotes
  it: Cor 5.1(a), Thm 2.9's `(n+1)|B|²/(2n)`, Thm 4.1, and LV07 5.4/5.5a/5.7. AK25a Ex 11.2 and the
  "Thm 2.10" attribution are UNVERIFIABLE.
- I did not re-run c929's own `run_all.sh`. I compared my independent figures against its committed
  transcripts, and they agree on: 39 and 86; C64 `0.633914`; C611 `2.31935`; W for `m ≤ 11`;
  I* for `m ≤ 11`; and every constant in s3.
- I did not re-check (5.1)–(5.5) numerically with `d`. My census checks the consequences c929
  consumes (S1, S3, S5, S6, F21). It does not check the `d`-inequalities themselves; c929's s1
  does that.
- I did not attempt to tighten §6's constants, and I did not decide the open question of
  `E[inv] ≤ C'·E[W]` on the no-balanced-pair class.
- I did not witness claim 18 (`a_x` is not pair-bias).
- `STATE.md` was not edited, and no ticket was closed.
