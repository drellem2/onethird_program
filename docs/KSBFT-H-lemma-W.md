# KSBFT-H: Missing Lemma W is true with a linear loss — and Theorem 1.3 becomes δ > 0.2764 for every range D ≤ 3471 (mg-f218)

Subject: Aires–Chan–Pak–Panova, *Breaking the Infinite Barrier in the 1/3–2/3 Conjecture*, KSBFT_v7 (2026-09-25), read from `/Users/daniel/files/KSBFT_v7.pdf` with `pdftotext -layout`. Page, lemma and equation numbers are the paper's printed ones. This file builds on mg-d707 (`docs/KSBFT-B-case-c-attack.md`, "KSBFT-B") and on its audit mg-3a14 (`docs/AUDIT-mg-d707.md`). Instruments are in `code/ksbft_h_lemma_w_f218/`, and `sh code/ksbft_h_lemma_w_f218/run_all.sh` regenerates every transcript quoted here. It is deterministic, takes about 5 min, and runs at most 3 processes.

Labels:
- **PROVEN**: the proof is in this file.
- **PROVEN-mod-paper**: the proof is here but consumes named lemmas of the paper or of KSBFT-B, each marked *re-derived* or *read only*.
- **EMPIRICAL**: comes with its instrument and range.
- **CONJECTURED**: a guess.

---

## 0. Verdict

1. **Lemma W is TRUE with a linear-in-D loss (PROVEN).** Take any finite poset, any x ∥ y, and let N(x,y) := {w ∉ {x,y} : w ⊀ y and x ⊀ w}. Then:
   - **either** N(x,y) = ∅, and P[f(x) − f(y) ≥ 2] = 0;
   - **or** P[f(x) − f(y) ≥ 2] ≥ P[f(y) < f(x)] / (π_N + 1), where π_N = max over w ∈ N(x,y) of π(w), which is ≤ π(P).

   The proof is a one-page injection (§2). It needs no BFT hypothesis at all. The BFT-triple structure enters only to bound the numerator: inside the paper's window p = P[f(y) < f(x)] ≥ C_BFT − θ (§3.1). So in the setting of Lemma 3.2(iii), **P[f(x) − f(y) ≥ 2] ≥ (C_BFT − θ)/(D+1)** replaces q₃ = (D+1)^(−3(D+1)).
2. **The constant 1/(π_N + 1) is sharp (PROVEN for every D ≥ 3; upgraded from EMPIRICAL by audit mg-e60e §3).** The exhaustive census of every poset on n ≤ 8 elements (2 800 472 at n = 8) finds that the minimum of P[gap ≥ 2]/p equals 1/(π+1) exactly, for every π = 2..7. It is attained by pairs that are the first two elements of a Case-D BFT triple. The audit's explicit family P_k = (({x ≺ z} ⊔ {y}) ⊕ chain of k) ⊔ {w}, w isolated, has π = D = k+3, (x, y, z) a Case-D BFT triple, N(x,y) = {w}, and ratio exactly 1/(D+1), for every k ≥ 0 (see §2.1). So no version of Lemma W that uses only "Case-D BFT triple + range ≤ D" can beat 1/(D+1), for any D ≥ 3. This does **not** show the loss is intrinsic inside the paper's window, which is empty (item 3).
3. **Theorem 1.3″ (PROVEN-mod-paper).** Let P be a finite non-chain poset with π(P) ≤ D (D ≥ 2). Then

   > δ(P) ≥ C_BFT + min(θ₀, θ_W(D)),  θ₀ := 0.2764 − C_BFT ≈ 6.7978·10⁻⁶,  θ_W(D) := C_BFT/((5+3√5)(D+1) + 1).

   The inequality is strict when θ₀ < θ_W(D). **For every D ≤ D₀ = 3471 the bound is δ(P) > 0.2764**, uniform in D. Beyond D₀ it is ≈ 0.0236/(D+1), i.e. C_BFT + Θ(1/D). Comparison: mg-d707 had (D+1)^(−3(D+1))/12 and the paper had (D+1)^(−4(D+1))/4096 (≈ 10^(−18.8) and 10^(−27.3) at D = 6).
4. **The correction's arithmetic is confirmed, with a sharper reading.** "Lemma W alone gives only C_BFT + Θ(1/D)" is right for large D. But three constraints bind, in this order:
   - (a) **θ₀, a D-uniform cap that no strength of Lemma W removes.** It comes from Lemma 3.2(i): Case C is excluded only below 0.2764 (Lemma 2.3).
   - (b) **Lemma W's own 1/(D+1)**, for D > 3471.
   - (c) **The witness 1/(24.5(D+1))**, which is *never* binding once Lemma W is linear, because 24.5·C_BFT < 5+3√5.

   So a D-uniform lower bound on M (target (b) of the ticket) buys **nothing** on top of the proven Lemma W. It would matter only after a D-free Lemma W, and even then only for D ≥ 6004. The best possible D-uniform result along this route is C_BFT + θ₀ = 0.2764, unless Lemma 2.3 itself is improved (§4).
5. **Target (b), a D-uniform lower bound on M, was neither proved nor refuted.** §5 explains why it is now off the critical path.
6. **Nothing new at 1/3 (item 4 of the ticket).** Lemma W plus any finite check settles the 1/3–2/3 conjecture for **no** new D. The smallest D newly settled is: none. The reason is structural, not about the size of n (§6). What *is* newly settled is the weaker δ > 0.2764 for 7 ≤ D ≤ 3471. For D ≤ 6, 1/3 was already known (Peczarski).

---

## 1. Lemma W as mg-d707 needs it, and what each strength buys

### 1.1 Where it is consumed

In Lemma 3.2(iii) (paper p.11) the hypothesis δ(P) ≤ C_BFT + η gives R ≤ (5+3√5)η by (2.4). The proof must then rule out any extension g with g(y) < g(w) < g(x). The paper does this with Lemma 3.1 on S = {x, y, w} and (2.5):

    q₃ ≤ P[f(y) < f(w) < f(x)] ≤ P[f(x) − f(y) ≥ 2] ≤ R.

Symmetrically for the pair (y, z). Everything else in Lemma 3.2 is exact. So the statement needed is:

> **Lemma W (as needed).** Let (x, y, z) be a Case-D BFT triple (x ≺ z, x ∥ y, y ∥ z, h(x) ≤ h(y) ≤ h(z) ≤ h(x) + 2) in a poset with π ≤ D and δ(P) ≤ C_BFT + θ. If some extension has f(y) < f(w) < f(x), then P[f(x) − f(y) ≥ 2] ≥ c(D, θ). The mirror statement holds for (z, y).

The window then closes exactly when (5+3√5)θ < c(D, θ), subject to θ ≤ θ₀ so that Lemma 3.2(i) applies.

### 1.2 What each strength buys (with the M-witness m(D) of Prop B, m(D) = 1/(D+1), and Prop C's 24.5)

After Lemma 3.2 the contradiction also needs θ < m(D)/24.5, where m(D) is a lower bound on M (KSBFT-B §2.3). So the theorem obtained is

    δ(P) > C_BFT + min( θ₀ , c(D)/(5+3√5) [approx.] , m(D)/24.5 ).

| strength of Lemma W | resulting bound, witness m(D) = 1/(D+1) (Prop B, PROVEN) | with a D-uniform witness m(D) ≥ μ (open) |
|---|---|---|
| c = q₃ (paper, Lemma 3.1) | (D+1)^(−3(D+1))/12 (KSBFT-B Thm 1.3′) | same: window-bound |
| c = D^(−k), k ≥ 1 | min(θ₀, ~D^(−k)/11.7) = θ₀ for D^k ≤ 1/((5+3√5)θ₀) ≈ 1.26·10⁴, i.e. D up to ~(1.26·10⁴)^(1/k), then Θ(D^(−k)) (errata mg-9694: was (8.6·10³)^(1/k)) | same |
| **c = (C_BFT − θ)/(D+1) (PROVEN here)** | **min(θ₀, θ_W(D)) = θ₀ for D ≤ 3471, then ≈ 0.0236/(D+1)** | same, because θ_W < 1/(24.5(D+1)) at every D |
| c = absolute constant c₀ | min(θ₀, c₀/11.7, 1/(24.5(D+1))) = θ₀ for D ≤ 6003 (if c₀ ≥ 11.7θ₀), then 1/(24.5(D+1)) | min(θ₀, c₀/11.7, μ/24.5): **D-uniform**, but ≤ θ₀ ≈ 6.8·10⁻⁶ |

The rows are PROVEN arithmetic (`window.py`, asserts included), given Lemma 3.2's other steps. The only strength actually established is the bold row.

*Errata (mg-9694, per audit mg-e60e item 6a).* The D^(−k) row previously read (8.6·10³)^(1/k), and was not in fact asserted in `window.py`. The correct threshold is D^k ≤ 1/((5+3√5)θ₀) = 1.2564·10⁴; it is now printed and asserted in `window.py`. If instead c multiplies p, as Lemma W's does, the threshold is ≈ 1.2564·10⁴·(C_BFT − θ₀) ≈ 3.47·10³ (the audit's second reading). The row is hypothetical and nothing downstream uses it.

**Verification of the ticket's claim** ("proving Lemma W upgrades Thm 1.3′ from exponential to C_BFT + Θ(1/D)"): **HOLDS for D > 3471. It is an understatement for D ≤ 3471**, where the bound is the D-uniform constant θ₀. The audit's "constant Lemma W ⇒ Θ(1/D)" (mg-3a14 §2.8) is right in form, but it missed the θ₀ cap. Its hypothetical "constant window θ_c" can never exceed 6.8·10⁻⁶, so the witness 1/(24.5(D+1)) starts to bind only at D ≥ 6004.

---

## 2. Lemma W — statement and proof (PROVEN)

**Notation.** f is a uniformly random linear extension. For x ∥ y let

- E₁ = {g : g(x) = g(y) + 1}, E₂ = {g : g(x) = g(y) + 2};
- p = P[f(y) < f(x)];
- N = N(x,y) = {w ∈ X ∖ {x, y} : w ⊀ y and x ⊀ w};
- π_N = max over w ∈ N of π(w), where π(w) = #{u : u ∥ w}.

**Lemma W.** (a) Some extension has f(y) < f(w) < f(x) iff w ∈ N. In particular P[f(x) − f(y) ≥ 2] > 0 iff N ≠ ∅.
(b) If N ≠ ∅, then |E₁| ≤ π_N · |E₂|, and hence

    P[f(x) − f(y) ≥ 2] ≥ P[E₂] ≥ p / (π_N + 1) ≥ p / (π(P) + 1).

*Proof of (a).* If g(y) < g(w) < g(x), then w ⊀ y and x ⊀ w, so w ∈ N. Conversely, for w ∈ N, adding y < w < x to ≺ creates a cycle only if w ≼ y, x ≼ w or x ≼ y, and none of these holds. The transitive closure is then a partial order, and any linear extension of it will do. ∎

*Proof of (b).* We define Φ : E₁ → E₂. Fix g ∈ E₁, with y at position i and x at position i+1. Every element of N sits either before y or after x. Write A = N ∩ {after x} and B = N ∩ {before y}. Then A ∪ B = N ≠ ∅.

- **Case A ≠ ∅.** Let w be the first element of A in g, and let x = t₀, t₁, …, t_{j−1} be the elements from x up to w (exclusive), so w is at position i+1+j. Each t_k is **incomparable to w**:
  - w ⊀ t_k, since t_k precedes w in g.
  - Suppose t_k ≺ w. First, t_k ≠ x, because x ⊀ w as w ∈ N. Next, t_k ⊀ y, because t_k comes after y in g. Next, x ⊀ t_k, else x ≺ t_k ≺ w. So t_k ∈ N, and it lies after x and before w, contradicting the choice of w.

  So moving w from position i+1+j to position i+1 changes only the relative order of w with t₀, …, t_{j−1}, all incomparable to w. It is a linear extension, and it has y, w, x at positions i, i+1, i+2. Set Φ(g) to be it.
- **Case A = ∅.** Let w be the last element of B = N in g, and let s₁, …, s_{j−1}, s_j = y be the elements from just after w up to y (inclusive). Each s_k is incomparable to w:
  - s_k ⊀ w, by position.
  - For s_j = y: w ⊀ y, because w ∈ N.
  - For k < j, suppose w ≺ s_k. Then s_k ⊀ y (else w ≺ y), x ⊀ s_k (s_k precedes x), and s_k ≠ x, y. So s_k ∈ N lies after w and before y, contradicting the choice of w.

  Moving w to just after y is therefore a linear extension with y, w, x consecutive. Set Φ(g) to be it.

**Counting preimages.** Fix g′ ∈ E₂ and let w be its middle element (position g′(y) + 1).
- A preimage in Case A is determined by its shift j. It requires the j elements immediately to the right of w in g′ to be incomparable to w. So these j's lie in {1, …, a_R}, where a_R is the length of the maximal run of w-incomparable elements immediately right of w.
- A Case-B preimage similarly has j ∈ {1, …, a_L}, with a_L the run to the left.

The two runs are **disjoint** sets of elements incomparable to w, so a_R + a_L ≤ π(w) ≤ π_N. Hence |Φ⁻¹(g′)| ≤ π_N, and |E₁| ≤ π_N|E₂|. Finally,

    p = P[E₁] + P[f(x) − f(y) ≥ 2] ≤ π_N·P[E₂] + P[f(x) − f(y) ≥ 2] ≤ (π_N + 1)·P[f(x) − f(y) ≥ 2]. ∎

**Remarks.**
- The run bound is the "window of π+1 slots" phenomenon of mg-1911 F1: an element can only be moved across elements it is incomparable to. That is why the hop length is at most π(w) and not n.
- The injection is the same kind as mg-d707's Prop B. The difference from Lemma 3.1 is that we lower-bound the *ratio* P[gap ≥ 2]/P[y before x], not the probability of an event. The ratio is polynomial even when both probabilities are exponentially small. mg-d707's generic counterexample (P[u<v] = 1/70) is a small *denominator*, not a small ratio.
- For (y, z) apply the lemma to the ordered pair (z, y): P[f(y) − f(z) ≥ 2] ≥ p′/(π_{N′} + 1) when N′ = {w : w ⊀ z, y ⊀ w} ≠ ∅.

### 2.1 Machine check and sharpness (census EMPIRICAL, exact integer counts; sharpness PROVEN for every D ≥ 3 by audit mg-e60e §3)

`lemw.c` enumerates every naturally labelled poset on N elements. Control: the counts equal OEIS A006455, i.e. 7, 40, 357, 4824, 96428, 2800472 for N = 3..8. For each poset it enumerates every linear extension and, for every ordered incomparable pair, counts |E₁|, |E₂|, #{y before x} and #{gap ≥ 2} as integers.

The transcripts are `out_lemw_3to7.txt` and `out_lemw_8.txt`. At N = 8 there are 91 740 332 ordered pairs.

| check | claim | violations, N = 3..8 |
|---|---|---|
| K0 | P[gap≥2] > 0 ⇔ N(x,y) ≠ ∅ | 0 |
| K1 | \|E₁\| ≤ π_N·\|E₂\| | 0 |
| K2 | p ≤ (π+1)·P[gap≥2] when N ≠ ∅ | 0 |
| **K1m (negative control)** | the FALSE \|E₁\| ≤ (π_N − 1)\|E₂\| | **5 025 852 at N = 8** (fires at every N) |

**Sharpness.** For every π = 2..7 (N = 8), max |E₁|/|E₂| = π exactly and min P[gap≥2]/p = 1/(π+1) exactly. The minimum is attained *on pairs that are the first two members of a Case-D BFT triple* (column "BFT-D"). For example, at π = 4 the witness is down-sets [0,0,0,0,3,13,31,127] with (x,y,z) = (4,5,6), p = 3/11, p′ = 4/11. Witnesses for every π are printed in the transcript.

**Sharpness for every D (PROVEN, audit mg-e60e §3; errata mg-9694).** For k ≥ 0 let Q_k = ({x ≺ z} ⊔ {y}) ⊕ (c₁ ≺ ⋯ ≺ c_k) and P_k = Q_k ⊔ {w}, w incomparable to everything; put D = k+3. Then π(P_k) = π(w) = D, (x, y, z) is a Case-D BFT triple, N(x,y) = {w}, and P[f(x) − f(y) ≥ 2]/P[f(y) < f(x)] = 1/(D+1) exactly: in Q_k, y before x forces y immediately before x, and of the |Q_k| + 1 = D + 1 slots for w exactly one (between y and x) gives gap 2. The audit's `code/audit_ksbft_e60e/family_e60e.py` checks it exactly for D = 3..13, with a negative control (delete w). The census sharpness above is the n ≤ 8 instance; the family makes it unconditional in D. The examples have p = 1/3, outside the paper's window, so this still does **not** show the loss is intrinsic inside the window.

**Near-balanced triples (weak).** Restricted to Case-D BFT triples with max(p, p′) ≤ 0.30, the census finds:
- π = 3: min ratio 1/4 = 1/(π+1), still tight. Witness at n = 8: [0,0,1,3,5,15,63,63], (x,y,z) = (1,2,3), p = p′ = 2/7.
- π = 4: min ratio 1/4 > 1/5.
- π ≥ 5: no such triple with N ≠ ∅ exists at n ≤ 8.

This is too little data to say whether local near-balance improves the constant.

---

## 3. Theorem 1.3″ (PROVEN-mod-paper)

### 3.1 Two facts about the window

Assume δ(P) ≤ C_BFT + θ with 0 ≤ θ ≤ θ₀, so δ(P) ≤ 0.2764. Let (x, y, z) be a Case-D BFT triple.

- **(F-a)** p, p′ ≤ 0.2764 < 1/2. This is Corollary 2.2 (*read only*; it rests on Lemma 2.1 = Kahn–Linial). Hence δ(P;x,y) = p and δ(P;y,z) = p′, so p, p′ ≤ δ(P) ≤ C_BFT + θ.
- **(F-b)** S = p + p′ ≥ 2C_BFT + 2R/(5+3√5) ≥ 2C_BFT. This is the displayed inequality S/2 ≥ C_BFT + R/(5+3√5) inside the proof of Lemma 2.4. *Re-derived from (2.1)–(2.2)*: the Claim 2.5 chain was checked, and so was the chord bound F(s) ≤ c − (c − 3/2)(1−s), where the chord is valid because F is convex. The BFT95 inputs (2.1)–(2.2) are *read only*.

Hence **p ≥ 2C_BFT − p′ ≥ C_BFT − θ**, and likewise p′ ≥ C_BFT − θ. The mechanism: near C_BFT both pairs of the triple are *forced* to be nearly balanced, so the denominator in Lemma W is a constant.

### 3.2 The theorem

**Theorem 1.3″.** Let P be finite, non-chain, with π(P) ≤ D and D ≥ 2. Let θ satisfy 0 ≤ θ ≤ θ₀ and θ < θ_W(D) = C_BFT/((5+3√5)(D+1) + 1). Then δ(P) > C_BFT + θ. Consequently δ(P) ≥ C_BFT + min(θ₀, θ_W(D)), with strict inequality when θ₀ < θ_W(D), i.e. for D ≤ 3471.

*Proof.*

1. **Setup.** Pass to a connected component of G(P) with n ≥ 3, as the paper does (§4, p.12). Suppose δ(P) ≤ C_BFT + θ.
2. **Lemma 3.2 (i), (ii)** hold verbatim. (i) uses only δ(P) ≤ 0.2764: Cases A and B give 1/3, and Case C gives > 0.2764 by Lemma 2.3 (*read only*; Appendix A not checked). (ii) uses no δ hypothesis.
3. **Lemma 3.2 (iii), repaired.** By (2.4), R ≤ (5+3√5)θ. Suppose some extension has g(y) < g(w) < g(x). Then w ∈ N(x,y), and Lemma W with (2.5) and §3.1 gives

       R ≥ P[f(x) − f(y) ≥ 2] ≥ p/(D+1) ≥ (C_BFT − θ)/(D+1).

   Hence θ((5+3√5)(D+1) + 1) ≥ C_BFT, i.e. θ ≥ θ_W(D), which is a contradiction. The pair (y, z) is handled the same way, using p′ ≥ C_BFT − θ. This yields (3.7). The rest of (iii), and all of (iv) and (v), follow exactly as printed (p.12), using no further hypothesis.
4. **Contradiction.** With the structure in hand, KSBFT-B Prop C (*re-derived* there and in audit §2.6) and Prop B (*re-derived*, audit §2.4) at Lemma 4.1's triple give

       δ(P) ≥ a ≥ C_BFT + M/24.5 ≥ C_BFT + 1/(24.5(D+1)).

   But θ < θ_W(D) < 1/(24.5(D+1)), because 24.5·C_BFT ≈ 6.77 < 5+3√5 ≈ 11.71. This contradicts δ(P) ≤ C_BFT + θ. ∎

**Numbers** (`out_window.txt`, where every inequality above is an `assert`):
- θ₀ = 0.2764 − C_BFT = 6.797750·10⁻⁶.
- D₀ = 3471 is the largest D with θ_W(D) > θ₀: θ_W(3471) = 6.79903·10⁻⁶ and θ_W(3472) = 6.79707·10⁻⁶.
- At D = 10⁴ the bound is 2.36·10⁻⁶; at D = 10⁶ it is 2.36·10⁻⁸.

**Prop C is now load-bearing.** This reverses audit mg-3a14 item 14, which is correct *for the exponential window*. With the printed Lemma 4.2 (M²/441) the witness term is 1/(441(D+1)²). That is below θ_W(D) at every D, and at or below θ₀ from **D = 18** onward. So with 441 alone, the D-uniform range would stop at D = 17, and the bound would decay as 1/D² after that. Prop C's linear conversion is what carries θ₀ to D = 3471.

**Consumed and not re-derived:**
- Lemma 2.1 / Cor 2.2 (Kahn–Linial);
- Lemma 2.3 (BFT95 Case C; Appendix A);
- BFT95 (2.1)–(2.2);
- Lemma 3.2 (iii)'s tail and (iv)–(v): read line by line here, as in mg-d707 and mg-3a14, with no gap found. They use only (3.7) and (ii).

---

## 4. The cap θ₀, and what raises it (CONJECTURED/conditional)

θ₀ comes solely from Lemma 3.2(i). It is the gap between C_BFT and the Case-C constant 0.2764 of Lemma 2.3. Corollary 2.2's proof works for any threshold up to 1/e, and Lemma 2.4 uses δ ≤ 0.2764 only through Cor 2.2 (to get p, p′ < 1/2). So:

- **If the Appendix's stronger claim holds**, "the proof in fact yields the stronger lower bound 67/242 ≈ 0.27686 for Lemma 2.3" (Appendix A, p.28, *not checked*), then θ₀ can be replaced by 67/242 − C_BFT ≈ 4.663·10⁻⁴. The bound becomes C_BFT + min(4.66·10⁻⁴, θ_W(D)), with the constant regime ending near D ≈ 49. This is **conditional on an unchecked appendix claim**, and I have not re-derived it.
- Any D-uniform improvement along this route is at most (Case-C constant) − C_BFT. A route to 1/3 would have to replace Case C entirely (§6).

---

## 5. Target (b): a D-uniform lower bound on M — not done, and now off the critical path

- **Not proved, not refuted.** mg-d707's census evidence stands: min M = 4/13 at n = 6, 37/123 at n = 8, and ≈ 0.2866 by annealing at n = 18. I added no search.
- **Why it no longer matters.** With the PROVEN Lemma W, the binding constraints are θ₀ (D ≤ 3471) and then θ_W(D) ≈ 0.0236/(D+1). The M-witness 1/(24.5(D+1)) ≈ 0.0408/(D+1) is strictly weaker at every D. A D-uniform M bound would help only in combination with a D-free Lemma W (last row of the §1.2 table), and even then only for D ≥ 6004.
- **What would be needed for the last row.** A D-free Lemma W *inside the window* needs to beat the tight examples of §2.1. Those examples are Case-D BFT triples, so the proof would have to use the global hypothesis δ(P) ≤ C_BFT + θ, not just local triple data.

  One observation (EMPIRICAL, small; `out_fibw.txt`): in the family G(m,a,b) = F_m plus one element w ∈ N(x₀,x₁), adding w destroys every central BFT triple. The Case-D BFT triples that survive all have N = ∅ (m = 6, every 1 ≤ a ≤ 5, 2 ≤ b ≤ 5). Near-C_BFT structure seems to *repel* N-elements. I did not turn this into a proof. The positive control is that plain F_m has P[gap≥2] = 0 at the centre and p = F_{m+1}F_m/F_{2m+2}, matching the paper's formula for m = 2, 4, 6.

---

## 6. Item 4: does Lemma W plus a finite check close any new D at 1/3? No (PROVEN-mod-paper reasoning)

The M-witness failure mg-d707 found (M = 4/13 < 1/3 at n = 6) concerns the conversion "balance ≥ M". That conversion exists **only at a triple with Lemma 3.2's structure** (Prop A). That structure is derived only under δ(P) ≤ 0.2764, because Case C triples are excluded only below Lemma 2.3's constant. So the route runs as follows:

- Lemma W enlarges the window from exponential to θ₀. It cannot enlarge it past θ₀, since Lemma 3.2(i) caps it, whatever the strength of Lemma W.
- Inside any window below 0.2764, Prop A gives M ≤ max(p, p′) ≤ δ < 0.2764. So the price "M ≥ 1/3" is never payable there. A small-n finite check cannot supply it, because the posets it would need to control are exactly those where the structure is unavailable.
- To reach 1/3 at a fixed D, the posets with 0.2764 < δ < 1/3 must be handled. Neither Lemma W nor the displacement route says anything about them.

**Smallest D newly settled at 1/3: none.** Beyond Peczarski's D ≤ 6 (and Gup26's n ≤ 14) this route adds no range at 1/3. What it does newly settle is the statement **δ(P) > 0.2764 for all finite non-chain posets of range 7 ≤ D ≤ 3471** (Thm 1.3″). Previously the best for those ranges was mg-d707's C_BFT + (D+1)^(−3(D+1))/12. It is *not* new for D ≤ 6, where 1/3 is known.

---

## 7. What I did not do, and negatives

- **Lemma W with a D-free constant**: not proved. It is refuted for any proof using only "Case-D BFT triple + range ≤ D" (tight examples at every π ≤ 7, §2.1). It is untested under the global window hypothesis, which is by Thm 1.3″ **empty for D ≤ 3471**, so no finite search can test it there.
- **A D-uniform M bound**: not attempted beyond the argument in §5 that it is off the critical path. Candidate tried in thought only: M ≥ (1/k)·E[#inversions across the h-prefix cut V_k]. This fails because the cut probabilities can be exponentially small, which is the same phenomenon as Lemma 3.1.
- **Not checked**: Lemma 2.3 / Appendix A (including the 67/242 claim), BFT95 (2.1)–(2.2), Lemma 2.1, eq (1.5), Thms 1.4/1.5, the preprints. Brightwell–Wright 1992 and Peczarski 2008 were not read.
- **Census range**: exhaustive n ≤ 8 only. Heights in `lemw.c` are compared exactly (integer position sums); the printed ratios are doubles of exact integer quotients.
- **Candidates for the injection that I rejected**: the 2D-to-1 version (first draft: bounded the two sides separately by D each). It is superseded by the disjoint-run count, which the census shows is sharp.

## 8. Reproduce

```
sh code/ksbft_h_lemma_w_f218/run_all.sh    # ~5 min, <= 3 procs, deterministic; fails loudly if K0/K1/K2 != 0 or the negative control is silent
```

| file | contents |
|---|---|
| `lemw.c` | exhaustive census; checks K0, K1, K2, negative control K1m; sharpness and witnesses |
| `window.py` | θ₀, θ_W, D₀ = 3471, the D = 18 crossover for 441, the table in §1.2/§3 (all asserted) |
| `fibw.py` | F_m positive control; the G(m,a,b) family of §5 |
| `out_lemw_3to7.txt`, `out_lemw_8.txt`, `out_window.txt`, `out_fibw.txt` | transcripts |
