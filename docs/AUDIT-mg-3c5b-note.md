# AUDIT (mg-7d8e): referee report on `notes/lemma-W-polynomial-range-bound.tex` (mg-3c5b)

Auditor: polecat a7d8e, fresh context. I read the note first, then only the sources it cites:
- KSBFT_v7 (`/Users/daniel/files/KSBFT_v7.pdf`, via `pdftotext -layout`): §§1–4 and Appendix A in full.
- BFT95 as the authors' preprint of 30 May 1995 (`https://page.math.tu-berlin.de/~felsner/Paper/newbft.pdf`, 18 pp, which I fetched myself). I read §§1–6 in full and skimmed §7. I did not see the Order version.
- For question 5 only, I read the scope lines of `docs/KSBFT-K-writeup-novelty.md`. I read that file after I had formed every verdict on the mathematics.

Instrument: `code/audit_ksbft_7d8e/audit_7d8e.py` (run it with `run_all.sh`, about 3 s). The transcript is `out_audit_7d8e.txt`. It imports nothing from the author's code. It contains:
1. an exhaustive census of all 4472 labelled posets on 2–5 elements. The count matches A001035 (3+19+219+4231), which is the positive control on the enumerator.
2. a negative control that fires: the census finds 2568 violations of the note's displayed middle inequality (see B1).
3. exact computation of the sharpness families.
4. random-sample checks of the algebra in Lemma 2.4(a) and Proposition C.
5. every numerical constant in the note.

Labels: **PROVEN** = I re-derived it by hand in this report. **EMPIRICAL** = checked by the instrument over the stated range. **UNVERIFIABLE** = depends on a source I did not read.

---

## 0. Summary

| # | Claim in the note | Verdict |
|---|---|---|
| 1 | Lemma W(a): a linear extension has y<w<x ⇔ w ∈ N(x,y) | **HOLDS** (PROVEN) |
| 2 | Lemma W(b): \|E₁\| ≤ π_N\|E₂\|, and P[f(x)−f(y)≥2] ≥ P[y<x]/(π_N+1) | **HOLDS** (PROVEN; census n≤5 finds 0 violations) |
| 3 | Lemma W(b), displayed middle step: P[f(x)=f(y)+2] ≥ P[y<x]/(π_N+1) | **BROKEN**. Counterexample: c₁<c₂<x with y isolated, where P[E₂]/p = 1/3 < 1/2. The proof never claims this step and nothing downstream uses it. |
| 4 | Lemma W(c): sharp for every D≥2, and on Case-D BFT triples for every D≥3 | **HOLDS** (PROVEN, and exact for D=2..7) |
| 5 | Abstract: "sharp for every value of π_N" | **HOLDS**, but π_N=1 is not exhibited in the note. Example: y≺w with x isolated gives ratio exactly 1/2. |
| 6 | Imports I1–I4 quoted correctly and used within hypotheses | **HOLDS**. I2 and I4 were checked against the BFT95 preprint. I1 holds as KSBFT Lemma 2.1; KL91 is UNVERIFIABLE because unread. |
| 7 | Lemma 3.1 (= KSBFT Cor 2.2), Lemma 3.2 (= KSBFT Lemma 2.4) incl. "(a) needs no δ hypothesis" | **HOLDS** (PROVEN) |
| 8 | Lemma 3.3 (window), Lemma 4.1 (structure, weaker hypothesis, new (iii)) | **HOLDS** (PROVEN) |
| 9 | Remark after Lemma 4.1: "This is the only point where the exponential loss entered" | **BROKEN** as stated: (4.11), M ≥ q₂, is a second entry point |
| 10 | Abstract: "We use this [Lemma W] to replace the only exponentially small quantity" | **OVERSTATED**: Lemma W alone leaves KSBFT's bound at order q₂² (exponential) |
| 11 | Lemma 5.1 (= KSBFT Lemma 4.1), Prop B (d₁ ≥ 1/(D+1)), Prop C (ε ≥ M/(20+2√5)) | **HOLDS** (PROVEN; census 0 violations for Prop B; Prop C sampled, max M/ε = 5.80 < 24.47). "Sharp" in Prop B is true for d₁, not for M. |
| 12 | Theorem 1.3″ and its numbers (θ₀, D₀=3471, the gains, 0.02361, 0.04086) | **HOLDS** mod I1–I4 (PROVEN; numbers recomputed) |
| 13 | "Which constraint binds" remark, including "M²/441 would end at D=17" | **HOLDS** |
| 14 | "Where finiteness enters": "Lemma W and Lemma 4.1 pass to such limits" | **UNVERIFIABLE**. Nothing proves it; it should be labelled heuristic. |
| 15 | Corollary: ε = min(θ₀, θ_W(L)) | **HOLDS**, given the combination. That the combination is how KSBFT get Thm 1.2 at D = L is our reconstruction and is **OVERSTATED** as "is obtained by". |
| 16 | Corollary: "The double exponential in L disappears" | **BROKEN wording**: η_L = (L+1)^(−4(L+1))/4096 is exp(−Θ(L log L)), which is single-exponential in L |
| 17 | §7: KSBFT App. A imports exactly KL + BFT95 Lemmas 2.2, 2.3, 6.2 | **OVERSTATED (incomplete)**. It also needs BFT95 Lemma 2.1 (the Kahn–Saks inequalities (2.1)–(2.6), including Alexandrov–Fenchel), because Lemma 2.2 assumes them, and Lemma 6.1. The four statements that are listed are quoted correctly (HOLDS against the preprint). |
| 18 | §7: "App. A derives 3/5<v_q<1 from q∈(1/5,3/10), which is false near 3/10" | Numerics **HOLD** (v₀.₃ = 0.5650). The attribution is **OVERSTATED**: App. A says only "the bounds on q", which can be read as the sharper [6/11−0.2764, 0.2764] it has just proved, and on that range the claim is true. |
| 19 | §7: 67/242 holds as a non-strict bound; θ₀′ = 4.663e−4; δ ≥ 67/242 for D ≤ 49 | **HOLDS** (PROVEN mod App. A's imports). This improvement imports more than the "exactly four", and the note should say so. |
| 20 | The note does NOT claim KSBFT eq. (1.5) is wrong | **HOLDS**. It says only that (1.5)'s derivation is omitted and gives no value. It never uses the words "does not follow from the printed ingredients", and it does not need to. |
| 21 | Novelty: "We have not found Lemma W in the literature (see the accompanying search log)" | **OVERSTATED (unscoped)**. The note never says that KS84, KL91, BW92, Pec08 and Brightwell's 1999 survey were unread. It also never says that BW92/Pec08 already give δ ≥ 1/3 (stronger than Thm 1.3″) for D ≤ 6. |
| 22 | Self-contained? | **NO**, in presentation only. See §3. The mathematics has no hidden import beyond I1–I4 for Theorem 1.3″. |

Net: the mathematics of Lemma W(b)'s real content and of Theorem 1.3″ HOLDS. None of the defects touches a step that Theorem 1.3″ uses. The note should **not** go out until the required edits in §4 are made. R1–R4 are the must-fix items, because each of them misstates what is proved.

---

## 1. Line-by-line referee notes

### 1.1 Lemma W(a): HOLDS
Forward: g(y)<g(w) gives w⊀y, and g(w)<g(x) gives x⊀w. Converse: adding y<w<x creates a directed cycle only through w⪯y, x⪯w, or (using both new edges) x⪯y, and w∈N together with x∥y excludes all three. "f(x)−f(y) ≥ 2 ⇒ some element lies strictly between, and it is in N" follows from the forward direction.

### 1.2 Lemma W(b): the inequality HOLDS; the displayed chain is BROKEN at one link
Proof of |E₁| ≤ π_N|E₂|, checked step by step:
- *Case A≠∅.* Take w, the first element of A. For each t_k between x and w: w⊀t_k by position. If t_k≺w then k≠0 (because x⊀w), t_k⊀y (by position), and x⊀t_k (else x≺w). So t_k ∈ N, it lies before w and after x, and this contradicts the choice of w. Moving w left past incomparable elements gives a linear extension. ✓
- *Case A=∅.* Take w, the last N-element (before y). For each s_k: s_k⊀w by position. If w≺s_k (k<j) then s_k⊀y (else w≺y), x⊀s_k (by position), and s_k∈N lies after w, a contradiction. For s_j = y we have w⊀y because w∈N. ✓
- *Multiplicity.* A preimage of g′ ∈ E₂ is fixed by (side, j). The j elements passed are incomparable to w, so they lie in the maximal incomparable run on that side. The two runs are disjoint subsets of the elements incomparable to w, so the number of preimages is ≤ a_R + a_L ≤ π(w) ≤ π_N. ✓
- The final display, P[y<x] ≤ (π_N+1)·P[f(x)−f(y)≥2], uses P[E₂] ≤ P[≥2]. ✓

**BROKEN:** the theorem statement displays
P[f(x)−f(y)≥2] ≥ **P[f(x)=f(y)+2] ≥ P[f(y)<f(x)]/(π_N+1)** ≥ …
The bold step is false. Take the chain c₁ ≺ c₂ ≺ x with y incomparable to all three. Then N(x,y) = {c₁, c₂}, π_N = 1, P[y<x] = 3/4 and P[f(x)=f(y)+2] = 1/4 < 3/8. More generally, with a k-chain below x, P[E₂]/p = 1/(k+1). The census finds 2568 violations among the 28722 qualifying ordered pairs on n ≤ 5, while (b)'s actual inequalities have 0 violations (EMPIRICAL, `out_audit_7d8e.txt` §1–2). The proof proves only the bound on P[≥2], and Lemma 4.1(iii) uses only P[≥2]. So nothing downstream is affected. The fix is to delete the middle term.

The remark "π_N ≥ 1" is correct: if w∈N were comparable to both x and y, then y≺w≺x. It is not needed anywhere.

### 1.3 Lemma W(c) and Example 2.1: HOLDS
- Generic family, D ≥ 2 (for D=2 it is the 3-antichain): π(y) = π(w) = D, N = {w}, and the ratio is exactly 1/(D+1). Computed exactly for D = 2..7.
- Case-D family P_k, D = k+3: in Q_k, (h(x), h(y), h(z)) = (4/3, 2, 8/3). Inserting w scales heights by (D+2)/(D+1) ≤ 5/4, so h(z)−h(x) ≤ 5/3 and the triple is a Case-D BFT triple. N = {w}, and the ratio is exactly 1/(D+1). Computed exactly for k = 0..4, where h(z)−h(x) = 5/3, 8/5, …
- The equality in (b) is between P[≥2] and p/(π_N+1). In these examples P[E₂] = P[≥2], so the false middle link happens to be tight there too.

### 1.4 Remark "relation to known inequalities": HOLDS against BFT95 Lemma 2.1
The BFT95 preprint (p.4) states a₁ = b₁ = b and (2.4) a₂+b₂ ≥ a₁+b₁, credited to [13] = KS84. Its notation (a_i, b_i, B, ε = b/B) matches the note's. "ε ≤ π_N/(π_N+1)" follows from E₁ ≤ π_N(p − E₁). KS84 itself is unread (UNVERIFIABLE at source; the note already says "as restated in").

### 1.5 §3 (Case D near C_BFT): HOLDS
- **Lemma 3.1 (Cor 2.2).** Correct. It needs x ≠ y. I1 as stated in the note omits "distinct", while KSBFT Lemma 2.1 has it (nit).
- **Lemma 3.2(a).** Re-derived. Both expressions in the minimum are equal at u₀ = (√(1+4s²)−1)/4 ≤ s/2. The value there is (7/2)√(s²+¼)−¼. On [u₀, s/2] the bound is convex, and its value at s/2 is 7s/2. F is convex, F(0) = 3/2 and F(1) = (7√5−1)/4. The constants are 7/(2(9+c)) = 0.276393202250 = C_BFT and (c−3/2)/(2(9+c)) = 0.085410196625 = 1/(5+3√5). Sampling (2×10⁵ points) finds no violation. Unlike KSBFT, the note's version does not contain the "If b₁ = 0 … When b₁ = 0" typo.
  **"Needs no hypothesis on δ(P)" HOLDS.** In the BFT95 preprint, (5.2) comes from the swap identities, (5.5) from Thm 3.2 plus AM–GM, (5.7) = 2·(5.1)+(5.6), and (5.8) = 4·(5.6)+(5.1) with x₅ ≥ 0. Here (5.1) uses only h(z)−h(x) ≤ 2, and (5.3)/(5.4) are unconditional. No bound on B or B′ enters. (KSBFT quotes (2.1)–(2.2) under its standing assumption δ ≤ C_BFT+η_D, but BFT95 does not need that assumption.)
- **Lemma 3.2(b).** The swap identities hold for j ≥ 2. Since x≺z, the event {f(x) = f(y)+1} forces f(z)−f(y) ≥ 2, and symmetrically for the other pair. Unconditional. ✓
- **Lemma 3.2(c) and Lemma 3.3.** ✓ S ≥ 2C_BFT, and p′ = δ(P;y,z) ≤ δ(P).

### 1.6 §4 (structure): HOLDS
- (i) Checked against BFT95 §4: its case list is taken "taking advantage of duality", and Thms 4.1/4.2 are stated for triples with h(x) ≤ h(y) ≤ h(z) ≤ h(x)+2. The note applies I2 to the *duals* of Cases A and B. This is valid because dualising and reversing the triple preserves δ, π and the BFT-triple conditions, but the note does not say so (§3, S3).
  BFT95's Thm 4.2 proof ends "it may be verified that B ≥ 0.335". That is a sketch in the source, so the note inherits it.
- (ii) ✓. The event x<y<z has positive probability, and on it w ≠ y (w is comparable to x, y is not).
- (iii) ✓. The chain is (C−θ)/(D+1) ≤ p/(π_N+1) ≤ P[≥2] ≤ R ≤ (5+3√5)θ ⇔ θ ≥ θ_W(D). The (y,z) instance uses p′ and the second summand of (b).
- (iv) ✓. This is KSBFT's **(v)**. KSBFT's (iv), the bridges, is dropped and the note does not say so (S7).
- "Under a weaker hypothesis" ✓: η_D < min(θ₀, θ_W(D)) for every D ≥ 2.

### 1.7 Remark after Lemma 4.1 and the abstract: BROKEN / OVERSTATED
In KSBFT, q_m = (D+1)^(−m(D+1)) (Lemma 3.1) enters twice:
- at Lemma 3.2(iii), through (3.6) R < q₃;
- at (4.11), through M ≥ q₂. This second entry sets η_D = q₂²/4096 via Lemma 4.2.

Lemma W removes only the first. With Lemma W alone, KSBFT's argument still gives an improvement of order q₂²/441, which is exponential. The note itself replaces (4.11) by Prop B (§1, "the lower bound (4.11) on M by Proposition 5.2"), so the remark contradicts the note's own import paragraph. The abstract sentence has the same problem, and so does the remark's "This is the only point where the exponential loss entered".

### 1.8 §5 (displacement argument): HOLDS
- **Lemma 5.1.** The case analysis "d_i = M for some i ≤ n−2, or d_j = −M for some j ≥ 3" is complete: I checked the four boundary cases i ∈ {n−1, n} and j ∈ {1, 2}. The no-chain argument is ✓. "g(z)−g(x) = 2 for every g" uses h(z)−h(x) ≤ 2 implicitly.
- **Prop B.** v₁ is minimal. Moving the first incomparable c to the front is valid, and preimages are indexed by t with t−1 ≤ π(c) ≤ D. So P[f(a)=1] ≤ D/(D+1) and d₁ ≥ 1/(D+1). ✓ Census n ≤ 5 (connected G(P)): 0 violations. "Sharp for a D-chain plus one isolated point" is true for **d₁**. For that poset **M ≈ ½**: for D=6, d at the chain element just below the isolated point is 3/7. So "M ≥ d₁ ≥ 1/(D+1). This is sharp" should say "the bound on d₁ is sharp" (S8).
- **Prop C.** Re-derived every identity:
  - The block structure, e(P) = e(L′)e(U′)Z, p = r/Z, α = (1+s)t/Z, h(x) = m+p−α and h(z) = m+2+β−p′.
  - g = √5(X+Y)+2XY.
  - A = (1+ρ)X−ρY, with A+B = X+Y and A−B = √5(X−Y).
  - X+Y ≥ 0, including the case where both are negative: 2|X||Y| ≤ 2ρW < √5W.
  - max(A,B) ≥ W/2.
  - F = (2+ρ)X−(1−ρ)Y+XY and G = (1−ρ)X−(2+ρ)Y−XY.
  - |F|, |G| ≤ (2+ρ)W and g ≤ (√5+ρ)W, so |d| ≤ (1+2√5)W/Z ≤ (20+2√5)ε.

  All correct. Sampling 152 214 admissible (r, s, α*, β*) gives a maximum M/ε of 5.80, against the proved 24.47. The constant is valid but loose (EMPIRICAL).
  Nit: the letter g denotes both a linear extension and v+2rs−2.

### 1.9 Proof of Theorem 1.3″ and numbers: HOLDS
- The components of G(P) are totally ordered. The propagation step is terse but correct: from a≺b we get K_a ≺ b, and then K_a ≺ K_b.
- The contradiction chain is ✓: θ < θ_W < 0.023607/(D+1) < 0.040863/(D+1).
- Endgame ✓: take θ = θ₀ when θ_W > θ₀, otherwise let θ ↑ θ_W.
- Recomputed: θ₀ = 6.797749979e−6, θ_W(3471) = 6.799025646e−6, θ_W(3472) = 6.797068014e−6, D₀ = 3471. The gains are 2.3604e−6 at D=10⁴ and 2.3607e−8 at D=10⁶. The note's values all match.
- Remark: "M²/441 instead ⇒ D-uniform range ends at D=17" ✓. (1/(441(D+1)²) > θ₀ ⇔ D ≤ 17.) This remark uses Lemma 4.2 outside its stated hypothesis, but it is explicitly counterfactual.

### 1.10 "Where finiteness enters": partly UNVERIFIABLE
- The BFT95 citation is fine. Thm 1.4 is δ₀′ = C_BFT over thin posets, and the example Q (range 2, width 2) is on p.3. Better: cite "§1, the poset Q and Thm 1.4".
- The statement about F_m is ✓. In F_m, N(x_i, x_{i+1}) = ∅, and y is incomparable only to x and z.
- "Lemma W and Lemma 4.1 pass to such limits" is asserted, not proved. Linear extensions of an infinite thin poset are defined only through BFT/Brightwell limits. Label this as heuristic or remove it.

### 1.11 Corollary: HOLDS with two wording defects
- ε = min(θ₀, θ_W(L)) is correct *given* the obvious combination. The other two terms, e⁻¹−10⁻¹⁰⁰−C_BFT and ½−ϵ−C_BFT, are larger. But KSBFT p.5 only says "Theorem 1.2 now follows from combining Theorem 1.3, Theorem 1.4, and Theorem 1.5". "Is obtained by combining Thm 1.3 at D = L" is our reconstruction. There is also a width off-by-one: Thm 1.5 needs w < K′, so it must be applied with K′ = K+1.
- "The double exponential in L disappears" is wrong as worded. η_L = (L+1)^(−4(L+1))/4096 = exp(−Θ(L log L)). The double exponential in (1.5) is in the *parameter* 16·10¹⁸, not in L.
- "The conditionality of Thm 1.4 on AK25a and Haqi's preprint is unchanged": true, but [Haq26] is missing from the bibliography. The corollary should also say that Thm 1.5 is imported from the preprint AK25b.
- (1.5): the note says only that the paper omits the derivation and gives no value. It does **not** claim (1.5) is wrong (question 4: HOLDS).

### 1.12 §7, Appendix A and 67/242
- **Import statements, checked against the BFT95 preprint:**
  - Lemma 2.2 (packing): p.4 ✓.
  - Lemma 2.3 (monotonicity): the exception is case (ii) with k=1 and ε ≤ 1/√2, which "only occurs when B ≥ 1−1/√2 ≈ .293". p.5 ✓.
  - Lemma 6.2: pp.13–14. Its proof uses only x, y, z pairwise incomparable, the 1/3-swap and Lemma 6.1 on (x,z), which needs h(z) ≤ h(x)+2. So "needs no bound on p or p′" is ✓.
  - Formulas (A.2) match BFT95 (2.9)/(2.10) ✓.
- **Incomplete list (item 17).** Lemma 2.2 applies to sequences satisfying BFT95 (2.1)–(2.6), which are the Kahn–Saks inequalities (BFT95 Lemma 2.1). (2.6) is the Alexandrov–Fenchel log-concavity. Lemma 6.2 needs Lemma 6.1. Both must be listed as App. A imports. So must the standard fact that t > 0 (some linear extension has y immediately before x), which App. A uses when it takes t ∈ (0,1].
- **v_q (item 18).** I recomputed v₀.₃ = 0.5650, v₀.₂₇₆₄ = 0.6180 and v at 6/11−0.2764 = 0.6360. The note's numbers are right. App. A's sentence is "The bounds on q imply 3/5 < v_q < 1", which is ambiguous between the two ranges it has just established. Rephrase: "if 'the bounds on q' means (1/5, 3/10), the implication fails near 3/10; on the range [6/11−0.2764, 0.2764] also established there, it holds."
- **67/242 (question 3): HOLDS as a non-strict bound (PROVEN, modulo App. A's imports).**
  - Final line: 5−(11/2)(p+p′)+1/22 > 2 ⇔ p+p′ < 67/121. So assuming both balances are < T = 67/242 gives a contradiction, and max ≥ 67/242 follows. At equality the chain gives h(z)−h(x) ≥ 2, which is no contradiction, so the bound is not strict.
  - The other thresholds all hold at T = 67/242:
    - first branch: T < 37/132 = 0.28030;
    - Claim A.1: T < 1−1/√2;
    - Claim A.2, first case: 29/9 < 1/T, which gives t > 2/3;
    - Claim A.2, second case: 32/9 = 3.5556 < 1/T = 3.6119;
    - v_q ∈ [0.6169, 0.6371] ⊂ (3/5, 1) for q ∈ [65/242, 67/242].
  - θ₀′ = 67/242 − C_BFT = 4.6630e−4 ✓, and θ_W(D) ≥ θ₀′ ⇔ D ≤ 49 ✓.
  - Downstream at the new threshold: Lemma 3.1 holds because 67/242 < e⁻¹, Lemma 3.2(c) because 67/242 < ½, and Lemma 4.1(i) holds for θ < θ₀′, strictly, which is needed because the Case-C bound is now non-strict.
  - This improved theorem rests on App. A's *proof*, not on KSBFT's printed Lemma 2.3. So it imports BFT95 Lemmas 2.1–2.3, 6.1 and 6.2 in addition to "exactly four". The note should say this where it states the improvement (R6).

## 2. Imports: quoted correctly and used within hypotheses?

| Import | Source check | Used within hypotheses? |
|---|---|---|
| I1 Kahn–Linial | Matches KSBFT Lemma 2.1 verbatim except that "distinct" is omitted. KL91 p.365 and AK25a Cor 5.1(b) are unread (UNVERIFIABLE at source). | Yes (Lemma 3.1, Lemma 4.1(i)) |
| I2 BFT95 Thms 4.1/4.2 | Preprint p.10: stated as Prob(x<y) ≤ 2/3 for BFT triples in Cases A and B. Same content. The 4.2 proof is a sketch. | Yes, including the duals (the duality is implicit in the note) |
| I3 KSBFT Lemma 2.3 / App. A | KSBFT p.7 verbatim | Yes |
| I4 BFT95 (5.2), (5.5), (5.7), (5.8) | Preprint pp.11–12 verbatim (X = S, x_i = a_i). No p, p′ hypothesis. | Yes, including Lemma 3.2(a) without any δ hypothesis |

"Theorem 1.3″ uses exactly these four and nothing else": **HOLDS**. I found no other non-trivial input. KSBFT Lemma 3.1 and Lemma 4.2 are not used, except in the counterfactual remark.

## 3. Self-containedness: steps that rely on something unstated or uncited

- **S1 Internal references an outside reader cannot follow:**
  - the author line ("internal note, work items mg-f218, mg-e60e, mg-3c5b");
  - "mg-d707, Prop. B/C";
  - "from the audit mg-e60e";
  - "Numbers (from `code/ksbft_k_3c5b/appA_check.py`)";
  - "see the accompanying search log".
- **S2** [Haq26] is cited in prose ("Haqi's preprint") but missing from the bibliography. KSBFT has no arXiv number or URL.
- **S3** Duality is used implicitly in the case list and Lemma 4.1(i): dualising and reversing preserves δ, π and the BFT-triple conditions, and I2 is applied in the dual poset. Add one sentence.
- **S4** I1 omits "distinct".
- **S5** App. A's import list omits BFT95 Lemma 2.1 (Kahn–Saks (2.1)–(2.6), including Alexandrov–Fenchel), Lemma 6.1 and the fact t > 0.
- **S6** Lemma 5.1's "g(z)−g(x) = 2 for every g" uses h(z)−h(x) ≤ 2 without saying so (trivial).
- **S7** The note's Lemma 4.1(iv) is KSBFT's (v); KSBFT's (iv) (bridges) is dropped silently.
- **S8** Prop B: "sharp" applies to d₁, not to M.
- **S9** The letter g is overloaded in Prop C.
- **S10** "Lemma W and Lemma 4.1 pass to such limits" is asserted without proof.

None of S1–S10 hides a mathematical gap in Theorem 1.3″.

## 4. Required edits (ordered; R1–R4 must be fixed before the note leaves)

- **R1 (BROKEN statement).** Thm 2.1(b): delete the middle term "≥ P[f(x)=f(y)+2]", or replace it with a separate true statement P[f(x)−f(y)≥2] ≥ P[f(x)=f(y)+2]. Counterexample: c₁≺c₂≺x with y isolated.
- **R2 (BROKEN remark).** Replace "This is the only point where the exponential loss entered" with something like: "This removes the first of the two places where Lemma 3.1's exponential bound enters KSBFT; the second, (4.11), is replaced by Proposition 5.2, and Lemma 4.2's square by Proposition 5.3."
- **R3 (OVERSTATED abstract).** Change "We use this to replace the only exponentially small quantity" to: "Together with a linear lower bound on the displacement and a linear replacement of their Lemma 4.2, this removes every exponentially small quantity from the proof of Theorem 1.3 of …"
- **R4 (novelty scope).** Replace "We have not found Lemma W in the literature (see the accompanying search log)" with an explicit scope: what was searched, and that KS84, KL91, Brightwell–Wright 1992, Peczarski 2008 and Brightwell's 1999 survey were **not read** (paywalled). Also state that δ ≥ 1/3 is already known for D ≤ 6 [BW92, Pec08], so Theorem 1.3″ is new only for D ≥ 7. KSBFT p.3 says this itself.
- **R5.** Corollary: change "the double exponential in L disappears" to "the factor (L+1)^(−4(L+1)) becomes ≍ 1/L". Change "is obtained by combining Thm 1.3 at D=L" to "the natural combination (not written out in [KSBFT]) applies Thm 1.3 at D = L(K+1, ·)". Mention that Thm 1.5 is imported from the preprint AK25b, and add [Haq26] to the bibliography.
- **R6.** §7: add BFT95 Lemma 2.1 (Kahn–Saks (2.1)–(2.6)), Lemma 6.1 and t > 0 to App. A's import list. State that the 67/242 improvement of Theorem 1.3″ rests on App. A's proof, and hence on these BFT95 lemmas, beyond I1–I4.
- **R7.** §7, v_q: soften the attribution as in §1.12.
- **R8.** Remove the internal work-item IDs, code paths and "accompanying search log" (S1). Give an author/affiliation line suitable for sending.
- **R9.** Add the duality sentence (S3), "distinct" to I1 (S4), "sharp for d₁" to Prop B (S8), the note that (iv) is KSBFT (v) with bridges omitted (S7), and rename g in Prop C (S9).
- **R10.** "Where finiteness enters": mark "Lemma W and Lemma 4.1 pass to such limits" as heuristic, or delete it. Cite BFT95 as "§1 (the poset Q) and Thm 1.4".
- **R11 (optional).** Give a π_N = 1 sharpness example (y≺w with x isolated; ratio ½) so that "sharp for every value of π_N" in the abstract is exhibited, or change the abstract to "every π_N ≥ 2".

## 5. What I did not do

- I did not read KS84, KL91, AK25a, AK25b, Haq26, BW92, Pec08, Brightwell 1999, or the Order version of BFT95.
- I did not re-derive BFT95 Lemmas 2.2 and 2.3, Thm 3.2 (cross-product), or the Thm 4.2 computation, which BFT95 itself only sketches. I read their statements and the short proofs of 6.1 and 6.2.
- I did not run a literature search of my own for Lemma W. Question 5 is answered by comparing the note's wording with the recorded scope.
- The census is n ≤ 5 only (4472 labelled posets). Prior audits (mg-e60e) went to n = 8; I did not repeat that.
- I did not recompile the PDF or check that it matches the .tex.

Negatives, with what was tried:
- (a) I looked for a counterexample to |E₁| ≤ π_N|E₂| and to P[≥2] ≥ p/(π_N+1) by exhaustive search over n ≤ 5: none. The control fired: the same loop finds 2568 violations of the false middle link.
- (b) I looked for violations of Prop B over all connected-G posets with n ≤ 5: none.
- (c) I looked for M/ε > 20+2√5 in Prop C's admissible region over 152 214 samples, half of them concentrated near (ρ, ρ): none (maximum 5.80). This is sampling, not proof; the proof is §1.8.
