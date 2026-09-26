# AUDIT of mg-d707 (KSBFT-B, `docs/KSBFT-B-case-c-attack.md`) — mg-3a14

Auditor: an independent polecat with fresh context, not the author. The subject is `docs/KSBFT-B-case-c-attack.md` as of `d1583e7`, together with its commit message `1333884` and its instruments in `code/ksbft_case_c_d707/`. The paper is `/Users/daniel/files/KSBFT_v7.pdf`, read with `pdftotext -layout`; page and equation numbers below are the printed ones.

Verdict scale: **HOLDS** (re-derived here or re-computed independently), **BROKEN** (false as stated), **OVERSTATED** (the true content is weaker than the words), **UNVERIFIABLE** (not checkable with what I had).

Independent instruments are in `code/audit_ksbft_3a14/`, and `sh run_all.sh` regenerates them in about 5 min on one process. They share **no code** with `census.c`:

- `indep.py`: exact `Fraction`/integer arithmetic, its own poset generator and its own ideal DP.
- `relax.py`: its own sampler of the Lemma 4.2 relaxation.

---

## 0. Summary

| # | claim (doc §) | label in doc | verdict |
|---|---|---|---|
| 1 | Prop A: M ≤ max(p,p′) ≤ 1/2 under Lemma 3.2's structure (§1.3) | PROVEN-mod-paper | **HOLDS** |
| 2 | "Route as printed cannot reach 1/3 at any M"; 5.01 is 18× the cap (§0.1, §1.3a) | PROVEN-mod-paper | **HOLDS** (trivially: Lemma 4.2 itself forces M ≤ 21√ε) |
| 3 | Price of 1/3 is M ≥ 1/3, threshold μ*(1/3) = 1/3 (§0.2, §1.4) | EMPIRICAL | **HOLDS, and it is actually PROVEN** (2 lines, §2.3 below). **OVERSTATED** as "the price of 1/3": it is a price *inside Lemma 3.2's structure*, which is only available for δ ≤ C_BFT + θ |
| 4 | M ≥ 1/3 is false: 6-element poset with M = 4/13, δ = 5/13 (§0.3, §1.5) | EMPIRICAL (exact) | **HOLDS**. Re-computed exactly; it is a proof by exhibit |
| 5 | Exhaustive minima of M, n ≤ 8 (table §1.5) | EMPIRICAL | **HOLDS for n ≤ 7** (independent exact enumeration). n = 8 is *reproduced only by the author's instrument*, though its witness 37/123 is verified exactly |
| 6 | Annealing minima 0.2995 / 0.2869 / 0.2866 (§1.5) | EMPIRICAL | **HOLDS** as a transcript quote. These are upper bounds only, correctly labelled |
| 7 | CONJECTURED inf M ≈ 0.28–0.30 (§1.5) | CONJECTURED | correctly labelled; no verdict |
| 8 | M(F_m) = F_{2m}/F_{2m+2} → 0.382; F is not the obstruction (§1.5) | EMPIRICAL + paper | **HOLDS** (exact for m = 1..6) |
| 9 | "π = 2 rows reproduce exactly these values" (§1.5) | EMPIRICAL | **OVERSTATED (minor)**. Even-n rows give F_{n−1}/F_{n+1} (2/5, 5/13, 13/34), which are the even-length Fibonacci truncations, not F_m values |
| 10 | Erratum: paper's d formula has no sign, and the true d alternate (§1.5) | EMPIRICAL | **HOLDS**, and is provable (antisymmetry, §2.5) |
| 11 | Prop B: d₁ ≥ 1/(D+1), tight (§2.1) | PROVEN | **HOLDS** |
| 12 | Why q₂; parallel chains give 1/C(2k,k); "Lemma 3.1's shape is right for arbitrary events" (§2.1, §0.5) | EMPIRICAL | 1/C(2k,k) **HOLDS** (provable). "Shape is right" is **OVERSTATED**: 4^{−D} shows *exponential*, not (D+1)^{−2(D+1)} |
| 13 | Prop C: a ≥ C_BFT + M/24.5 (§2.2) | PROVEN-mod-paper | **HOLDS** (every step re-derived) |
| 14 | Thm 1.3′: δ > C_BFT + (D+1)^{−3(D+1)}/12 (§2.3) | PROVEN-mod-paper | **HOLDS**. But the credit is **OVERSTATED**: Prop B alone gives it, and the linear conversion (Prop C) is not load-bearing (§2.7) |
| 15 | "Only D-exponential loss left is Lemma 3.2(iii)" (§0.5, §3) | — | **HOLDS** as bookkeeping of this proof |
| 16 | "…That is the precise obstruction to a range-uniform bound along this route" (§0.5) | — | **OVERSTATED**. The witness 1/(24.5(D+1)) is a second, polynomial obstruction to range-uniformity |
| 17 | "With Lemma W at constant c, Thm 1.3′ becomes a D-uniform improvement C_BFT + c′" (§3) | (unlabelled) | **BROKEN** (§2.8) |
| 18 | Generic Lemma W false with polynomial c (§3) | EMPIRICAL | **HOLDS** (provable from parallel chains) |
| 19 | Prop D: golden-ratio lemma and depth bound for BFT triples (§4.1) | PROVEN / PROVEN-mod-paper | **HOLDS, but VACUOUS**: its hypothesis δ ≤ C_BFT + θ is exactly the regime Thm 1.3′ proves empty |
| 20 | "What would close case (c) this way" (§4.1) | CONJECTURED shape | **OVERSTATED**. The proposed lemma would yield nothing beyond Thm 1.3′ (§2.9) |
| 21 | B_K numbers (§4.2, §0.6) | EMPIRICAL | **HOLDS for n ≤ 7** (exact). The search quotes have **minor misquotes** (§2.10) |
| 22 | "B_{K(D)} ≥ 1/3 … is equivalent to the conjecture itself for range ≤ D" (§4.2) | CONJECTURED | **BROKEN**: only one direction (⇒ conjecture) holds |
| 23 | §5 compactness and transfer matrix | heuristic / CONJECTURED | correctly labelled; no verdict |
| 24 | "Lemma 3.2 read line by line, no gap found" (§1.1) | read only | **HOLDS**: I read it too and found no gap (§3) |

No PROVEN claim is BROKEN. The two BROKEN items (17 and 22) are unlabelled or CONJECTURED side-sentences, and both point the reader in the optimistic direction. The headline results are Prop B, Prop C and Thm 1.3′, and all three survive.

---

## 1. What I did

1. I enumerated every claim marked PROVEN, PROVEN-mod-paper or EMPIRICAL in the doc, in its §0 verdict and in commit `1333884`'s message. I also covered the unlabelled sentences that assert implications (items 16, 17, 20 and 22 came from there).
2. I re-derived Props A, B and C, the golden-ratio lemma, Prop D, Thm 1.3′ and the §1.4 threshold by hand (§2 below).
3. I read the paper's §2.2 (Lemma 2.4 and Claim 2.5), §3 (Lemmas 3.1 and 3.2), §4.1 (Lemma 4.1), §4.2 (Lemma 4.2) and §4.3 (eq 4.11), and checked every use d707 makes of them (§3 below).
4. I re-computed the empirical claims with an independent exact instrument (§4 below).

---

## 2. Re-derivations

### 2.1 Height identities (consumed by A, C, D)

Under Lemma 3.2(iii)/(v) with x = v_m, y = v_{m+1}, z = v_{m+2}:

- f(x) = m − #{L after x} + 1[y<x], so **h(x) = m + p − α**.
- f(z) = 1 + (m−1) + 1 + 1[y<z] + #{U before z}, so **h(z) = m + 2 − p′ + β**.
- e(P) = e(L′)e(U′)(1 + r + s). There are 3 = 1 + 1 + 1 placements of y when x is last and z is first, since L′ ≺ U′ by (3.5) and x ≺ z.

The α = (1+s)t/Z computation (p.15) was checked. All of this matches the paper's (4.2)–(4.7).

### 2.2 Prop A — HOLDS

We have d_m = p − α and d_{m+2} = β − p′, with α, β ≥ 0 and α + β ≤ p + p′. The four one-line bounds in the doc are each correct:

- d_m ≤ p
- −d_m ≤ p′ − β ≤ p′
- d_{m+2} ≤ p − α ≤ p
- −d_{m+2} ≤ p′

Lemma 4.1 makes M = max(|d_m|, |d_{m+2}|). Note that p ≤ 1/2 already follows from (4.3), p = r/(1+r+s), so Corollary 2.2 is not needed.

`relax.py` found 1.03M feasible points and a worst value of |d| − a of −6.7e−12.

### 2.3 Threshold μ*(1/3) = 1/3 — HOLDS and is PROVEN (the doc says EMPIRICAL)

- **Upper bound.** By Prop A, a < 1/3 implies |d| ≤ a < 1/3, so μ* ≤ 1/3.
- **Lower bound.** Take r = s = 1 − η and t = u = η. This point is feasible because 2(2−η)η ≤ 2 − 2η for small η. Then a = (1−η)/(3−2η) ↑ 1/3 and d_m = (1 − η − (2−η)η)/(3−2η) → 1/3.

So the sup is 1/3 and it is not attained. The label can be upgraded.

**OVERSTATED as a "price of 1/3".** The conversion "balance ≥ M" exists only at a triple with Lemma 3.2's structure, and the paper derives that structure only under δ ≤ C_BFT + η_D (d707 gets θ = q₃/12). At δ just under 1/3 there is no structure. Case C triples are ruled out only below 0.2764, via Lemma 2.3. So "M ≥ 1/3 would give 1/3" is a statement about a hypothetical Lemma 3.2 valid up to 1/3. The doc concedes this in the last paragraph of §1.5, but the §0.2 headline does not.

### 2.4 Prop B (d₁ ≥ 1/(D+1)) — HOLDS

I checked each step.

- v₁ is minimal, because w ≺ v₁ would force h(w) < h(v₁).
- In g ∈ E₁ (so f(a) = 1), let c be the first element incomparable to a. Every u strictly between a and c satisfies u ≻ a, so u ⊀ c (else a ≺ c) and u ⊁ c (u precedes c). Hence u ∥ c.
- Moving c to the front therefore gives a valid extension with a in position 2.
- g is recovered from φ(g) and t, and t − 1 ≤ #incomparables of c ≤ D, so φ is at most D-to-1.
- |E₁| ≤ D(e − |E₁|).

The bound is tight: exact values for the D-chain plus a point are d₁ = 1/(D+1) for D = 1..6 (`out_indep_witness.txt`). The exhaustive minimum of d₁(π+1) is exactly 1 in the rows (n, π) = (3,2), (4,3), (5,4), (6,5), (7,6), and ≥ 1 everywhere for n ≤ 7.

### 2.5 Erratum on the Fibonacci displacement sign — HOLDS (provable)

F_m is self-dual under x_i ↦ x_{−i}, so h(x_{−i}) = n + 1 − h(x_i), which gives d(x_{−i}) = −d(x_i). The paper's unsigned F_{2|i|}/F_{2m+2} is positive at both ±i, so it cannot be right as printed.

Exact values at m = 3: 8/21, −1/7, 1/21, 0, −1/21, 1/7, −8/21. They alternate, and the magnitudes match the paper's formula. Exact M(F_m) = F_{2m}/F_{2m+2} was confirmed for m = 1..6.

### 2.6 Prop C (a ≥ C_BFT + M/24.5) — HOLDS

Every identity was re-expanded by hand:

- r/Z − C_BFT = ((1+ρ)X − ρY)/(Z√5), using √5 − ρ = 1 + ρ.
- g = √5(X+Y) + 2XY, using ρ² + ρ − 1 = 0.
- X + Y ≥ 0: in the both-negative case, 2|X||Y| ≤ 2ρ|Y| < √5(|X|+|Y|).
- max(A, B) = (X+Y)/2 + √5|X−Y|/2 ≥ max(X, Y) ≥ W/2. The last step uses X + Y ≥ 0.
- F = (2+ρ)X − (1−ρ)Y + XY and G = (1−ρ)X − (2+ρ)Y − XY. Both constant terms vanish by ρ² + ρ = 1.
- |F|, |G| ≤ (2+ρ)|X| + (1−ρ)|Y| + ρ|Y| ≤ (2+ρ)W.
- g ≤ √5W + ρW, because 2|X||Y| ≤ ρ(|X|+|Y|).
- Hence |d| ≤ (2 + 2ρ + √5)W/Z = (1+2√5)W/Z ≤ (20 + 2√5)ε ≈ 24.47ε.

Also, ε ≥ W/(2√5Z) ≥ 0 comes out automatically. `relax.py` gives an independent sup of |d|/ε equal to 5.854, attained at (r,s,t,u) = (1,1,0,0). This agrees with the doc's C4 value of 5.8541.

### 2.7 Thm 1.3′ — HOLDS, but the linear conversion is not what buys it

**Window.** In Lemma 3.2's proof (pp.11–12), the hypothesis δ ≤ C_BFT + η_D is used only at two points:

- (i), needing δ < 0.2764: C_BFT + q₃/12 ≤ 0.276393 + 4.24e−6 < 0.2764, where the slack is 6.8e−6.
- (iii), needing R ≤ (5+3√5)(δ − C_BFT) < q₃: (5+3√5)/12 = 0.9757 < 1, so this holds.

Lemma 2.4 needs δ ≤ 0.2764, which is satisfied. Lemma 4.1 has no δ hypothesis. The component reduction is the paper's own WLOG. So Lemma 3.2 holds under δ ≤ C_BFT + q₃/12, and the contradiction C_BFT + 1/(24.5(D+1)) > C_BFT + θ is valid.

**Attribution — OVERSTATED.** The commit subject says "d1 >= 1/(D+1) and a LINEAR conversion move Thm 1.3 to (D+1)^(-3(D+1))/12", and §0.5 says "after the two repairs". But the **printed** Lemma 4.2 (M²/441) combined with Prop B gives C_BFT + 1/(441(D+1)²), which is still far larger than θ. Lemma 4.2's proof uses its δ-hypothesis only to get a ≤ 0.2764 and ε < 10⁻⁵, and both still hold under θ. So Prop B **alone** moves η_D to q₃/12. The paper's own bottleneck was the witness: q₂²/441 = q₄/441 is smaller than the window q₃/11.7.

Prop C is still valuable, because it removes the dependence on the AI-assisted 441. But it is a redundancy, not a requirement. This is good news for assurance: Thm 1.3′ now has **two** independent conversions under it, and either one suffices.

The numerics check out: 7^{−21}/12 ≈ 10^{−18.83} and 7^{−28}/4096 ≈ 10^{−27.27}.

### 2.8 Item 17 — BROKEN

§3 says: "With c constant, it [Thm 1.3′] becomes a D-uniform improvement C_BFT + c′."

Suppose Lemma W gave a constant window θ_c. The contradiction argument then reads: assume δ ≤ C_BFT + θ_c; the structure holds; so δ ≥ C_BFT + d₁/24.5 ≥ C_BFT + 1/(24.5(D+1)). This contradicts the assumption only when 1/(24.5(D+1)) > θ_c, which **fails for D > 1/(24.5θ_c)**.

The best conclusion is therefore δ > C_BFT + min(θ_c, 1/(24.5(D+1))) = C_BFT + Θ(1/D). That is polynomial, not D-uniform. Prop B is tight for d₁, so a D-uniform result also needs a **D-uniform lower bound on M** (not d₁) for posets in the window. The doc's only evidence for such a bound is the §1.5 CONJECTURE (inf M ≈ 0.28), which is not proved.

The doc's own §6 bullet (i′), "would not change Theorem 1.3′, which is window-bound", is true only while the window is exponential. It becomes false the moment Lemma W lands.

**Consequence for item 16.** "Lemma 3.2(iii) is the precise obstruction to a range-uniform bound" is OVERSTATED. It is the only *exponential* obstruction; the witness is a second, polynomial one.

### 2.9 Prop D and the §4.1 programme — HOLDS but VACUOUS; programme OVERSTATED

**The golden-ratio lemma holds.** (qρ − p)(qρ′ − p) = p² + pq − q² is a non-zero integer because ρ, ρ′ are the roots of t² + t − 1. Also |qρ′ − p| ≤ δ₀ + √5q. The case δ₀ ≤ 1 ≤ q gives δ₀ ≥ 1/((1+√5)q).

**The rest of Prop D holds.**

- r = e(L)/e(L′), because x is maximal in L′.
- |r − ρ| ≤ W ≤ 2√5Zε ≤ 6√5ε.
- 6√5(1+√5) = 43.42 ≤ 43.5.
- Minimal elements form an antichain of size ≤ D+1, so e(Q) ≤ (D+1)^{|Q|}.
- (v₁, v₂, v₃) would give r = 1 and a ≥ 1/3.

**But it is vacuous.** Prop D assumes δ ≤ C_BFT + θ with θ = q₃/12, and Thm 1.3′ (same document) proves that **no finite poset satisfies this**. So Prop D is a true statement about an empty class. The doc does not say so.

**The §4.1 programme would buy nothing.** It asks for "a BFT triple within the first or last K elements … Combined with Prop D, that contradicts the regime." The regime is already contradicted by Thm 1.3′, so the proposed lemma yields nothing new. It certainly would not "close case (c)", i.e. reach 1/3. It could only matter together with a larger window (Lemma W), and then Prop D's depth bound shrinks with it. The doc's own caveat ("improves the witness side and not the window") understates this: the witness side is not binding (§2.7).

### 2.10 Minor misquotes in §4.2 and §0.6 (from `out_search_summary.txt`)

- **"B₄ … 0.309 at D = 5, 6" and "K = 4 fails at D = 5 (0.309)":** the D = 5 minimum is 0.3131 (n=18); 0.3093 is D = 6. D = 7 (0.300 at n=10) is omitted. The conclusion (B₄ < 1/3 from D = 5) is unaffected.
- **B₅ undercount:** B₅ < 1/3 also at n = 14, D = 8 (0.3287) and D = 9 (0.3234), not only at n=18, D=7. This is consistent with "5 for D ≤ 6".

### 2.11 Item 22 — BROKEN

The doc says the existence of K(D) with B_{K(D)} ≥ 1/3 for all range-≤D posets "is equivalent to the conjecture itself for range ≤ D".

- B_K ≥ 1/3 ⇒ δ ≥ 1/3: this direction is true.
- The converse would require every balanced pair to be locatable within a window independent of n. That does not follow from the conjecture.

So the K(D) statement is **strictly stronger a priori**, not equivalent. The practical danger is that a refutation of K(D) would be misread as a refutation of the conjecture.

### 2.12 Item 12 — OVERSTATED (minor)

Parallel k-chains give P = 1/C(2k,k) ≈ 4^{−k} with range k. I verified this exactly for k = 2..5, and it is provable: there is a single interleaving. This shows Lemma 3.1-type bounds must be exponential in D. It does **not** show that (D+1)^{−2(D+1)} = e^{−2(D+1)ln(D+1)} is the right order. The claim "Lemma 3.1's shape is right" should read "exponential decay is necessary".

The §6 negative (i), "Summation cannot beat the generic exponential", is true for a simpler reason than the one given: d₁ is a sum of at most D terms, each lower-bounded by Lemma 3.1 only by q₂.

---

## 3. Uses of KSBFT_v7

| paper item | used by d707 as | audit |
|---|---|---|
| Lemma 3.1 (p.9) | window cost, §3 | Re-read. Proof correct: (3.2) e(Q) ≥ e(P[U]), (3.3) e(P) ≤ e(P[U])(D+1)^{\|T\|} |
| Lemma 3.2 (pp.10–12) | structure, read only | Re-read line by line. (ii): the event x<y<z is consistent (no cycle) and forces a gap ≥ 3. (3.8): adding y<w<x is consistent unless w≺y or x≺w. (iv)/(v) follow. **No gap found.** Only two δ-uses (§2.7) |
| Lemma 2.4 / Claim 2.5 (pp.7–9) | inside Lemma 3.2 | Constants checked: 7/(2(9+c)) = C_BFT and (c−3/2)/(2(9+c)) = 1/(5+3√5) with c = (7√5−1)/4. (2.5): the events f(x)>f(y) and f(y)>f(z) are disjoint since x≺z. Cosmetic: Claim 2.5's proof states the b₁ = 0 case twice ("If b₁ = 0 …" then "When b₁ = 0 …"); the case split itself is correct. BFT95 (2.1)–(2.2) inputs **not checked** (not in hand) |
| Lemma 2.3 (Case C) | inside Lemma 3.2(i) | **not checked** (Appendix A not audited) |
| Lemma 4.1 (p.13) | triple choice | Re-read: correct. d₁ ≥ 0, d₁ + d₂ ≥ 0 etc.; the chain case contradicts connectivity |
| (4.2)–(4.7) | Props A, C, D | Re-derived (§2.1) |
| Lemma 4.2 / 441 (pp.14–17) | replaced by Prop C | **Checked anyway: HOLDS.** (r−s)² ≤ (v−2ρ)(v+2ρ+2) ≤ 11ε·4.48 ≤ 50ε; V′ ≤ 2/(1−0.5528)² = 10.0 < 11; V(0.2764) = 691/559. **Typo in (4.9):** it prints "(11ε + 50ε)/2 ≤ 5√ε"; it should read (11ε + √(50ε))/2 ≤ 5√ε, which holds for ε ≤ 0.07. Then \|d\| ≤ 20√ε + 11ε ≤ 21√ε for ε ≤ 1/121 |
| (4.11) | replaced by Prop B | Correct but lossy, as the doc says |
| eq 1.5, Thms 1.4 and 1.5 | not used by d707 | not audited (d707 does not consume them) |

---

## 4. Empirical claims — independent re-computation

`code/audit_ksbft_3a14/indep.py` (exact Fractions).

- **Controls.** The poset counts 7, 40, 357, 4824, 96428 for n = 3..7 equal A006455. The connected counts 4, 27, 275, 4070, 86278 equal census.c's.

- **Per-(n, π) minima for n ≤ 7.** min M, min δ, min d₁(π+1), min B₃ and min B₄ agree with `out_census_all.txt` in every row. Examples:
  - n=6, π=3: min M = **4/13** at [0,0,1,3,5,23], δ = 5/13.
  - n=7, π=4: min M = 4/13 at [0,0,1,1,7,7,31], δ = 14/39.
  - n=7: B₃ = 0.280702, B₄ min = 14/39.

  No row with n ≤ 5 has M < 1/3; the minima are 1/3, 2/5 and 4/11. So "first fails on a 6-element poset" HOLDS.

- **n = 8 witness** [0,0,1,1,3,7,13,63]: M = **37/123** = 0.300813, δ = 49/123. That the minimum over all 2 800 472 posets at n = 8 is this value was **not** independently re-enumerated (see §5).

- **Other exact checks:** parallel chains 1/6, 1/20, 1/70, 1/252; chain plus point d₁ = 1/(D+1); Fibonacci M values.

- **Annealing (`out_search_*.txt`).** Values were quoted correctly, apart from the misquotes in §2.10. I did not re-run the searches. Everything from them is correctly labelled "upper bound" and "weak evidence" in the doc, and nowhere is it presented as a proof.

**Were EMPIRICAL results presented as proofs?** No. The reverse happened once: §1.4 (item 3) is labelled EMPIRICAL but is provable. The exact computations for small posets (items 4 and 5) are genuine proofs by exhibit.

---

## 5. Negatives checked against the candidate space

| negative in d707 | candidate space | audit |
|---|---|---|
| Route as printed cannot reach 1/3 | a single route, fully specified | HOLDS; trivially true |
| Unconditional M ≥ 1/3 witness is false | all finite connected posets; one exact counterexample | HOLDS |
| Generic Lemma-3.1 bound cannot be polynomial | one family (parallel chains), which suffices for a "cannot" | HOLDS |
| Summing Lemma 3.1 over the boundary cannot win | argument, not a search | HOLDS (reason as in §2.12) |
| No D-uniform improvement found; Lemma W unresolved | the brief's (i)–(iv) each tried; (iii) heuristic only | honest; it is a report of non-finding, not an impossibility claim |
| K = 4 fails at D = 5, K = 5 fails at D = 7 | annealing over n ≤ 18, 3 seeds | as a "fails" statement these are **witnessed** (a search that finds B < 1/3 exhibits a poset). HOLDS as existence, modulo float precision (values ≥ 0.02 below 1/3, so safe) |

---

## 6. What I did not do

- I did not re-enumerate n = 8 (2.8M posets; my exact Python instrument would take hours). The n = 8 minima rest on census.c alone. Its witness is exact-verified here.
- I did not re-run the annealing searches.
- I did not check BFT95's inequalities (2.1)–(2.2), Lemma 2.3 or Appendix A, eq 1.5, Thms 1.4/1.5, or the preprints. d707 consumes only the first three, via Lemma 3.2.
- I did not read Brightwell–Wright 1992 or Peczarski 2008.
- I did not attempt Lemma W or a D-uniform bound on M.
- I did not edit the source doc.

## 7. Successor needed

A small doc-fix ticket against `docs/KSBFT-B-case-c-attack.md`:

- (a) §3: replace "D-uniform improvement C_BFT + c′" with "C_BFT + Θ(1/D), unless a D-uniform lower bound on M is also proved".
- (b) §0.5 and §3: "precise obstruction" → "only exponential obstruction; the witness 1/(D+1) is a second, polynomial one".
- (c) §2.3 and the commit claim: say that Prop B alone yields Thm 1.3′, and that Prop C is a redundant, higher-assurance conversion.
- (d) §4.1: note that Prop D is vacuous given Thm 1.3′, and that the "close case (c)" programme adds nothing without Lemma W.
- (e) §4.2: "equivalent" → "implies".
- (f) §1.4: upgrade μ*(1/3) = 1/3 to PROVEN, and qualify "price of 1/3" as conditional on Lemma 3.2's structure.
- (g) Fix the §4.2 B₄/B₅ misquotes, and the "reproduce exactly these values" wording for even n.
