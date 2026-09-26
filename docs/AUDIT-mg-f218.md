# AUDIT of mg-f218 (KSBFT-H, `docs/KSBFT-H-lemma-W.md`): mg-e60e

Auditor: an independent polecat with fresh context. I am not the author. The subject is `docs/KSBFT-H-lemma-W.md` as of `033c242`/`def5443`, with its instrument `code/ksbft_h_lemma_w_f218/`. The paper is `/Users/daniel/files/KSBFT_v7.pdf`, read with `pdftotext -layout`. Page, lemma and equation numbers are the paper's printed ones.

Verdict scale:
- **HOLDS**: re-derived here, or re-computed independently.
- **BROKEN**: false as stated.
- **OVERSTATED**: the true content is weaker than the words, or the sourcing is weaker than the words claim.
- **UNVERIFIABLE**: not checkable with what I had.

Instrument: `code/audit_ksbft_e60e/`. Run it with `sh run_all.sh`. It takes about 10 s, runs one process at a time, and is deterministic. `FULL=1 sh run_all.sh` adds N = 8 (about 5 min on one core). It shares **no code** with `lemw.c`. I wrote it before reading `lemw.c` beyond its `pi` variable and its output format.

- **`indep_e60e.c`**
  - Different generator: every transitive upper-triangular relation mask on N labels. The A006455 counts 7, 40, 357, 4824, 96428 are the positive control.
  - Different counting: all extension counts come from a down-set DP (forward × backward). Extensions are never listed.
  - Lemma W is checked in its **stated** form, with π_N. `lemw.c`'s K2 uses π(P), which is weaker.
  - For every Case-D BFT triple it computes S, a₁, a₂ and R exactly. It checks the two paper inequalities the doc consumes: (F-b) S/2 ≥ C_BFT + R/(5+3√5), and (2.5).
  - Negative control: the false bound c₁ ≤ (π_N − 1)c₂ must FIRE, and it does.
- **`family_e60e.py`**: exact `Fraction`s. It checks the audit's own infinite family (§3), which proves the sharpness claim for **every** D ≥ 3. Negative control: the same checker, run with w deleted, must fail on every row. It does, 6/6.
- **`run_all.sh`**: fails if any check count is nonzero or any control is silent. I confirmed that the gate catches three hand-mutated verdict lines.

---

## 0. Headline

| # | claim (doc §) | label in doc | verdict |
|---|---|---|---|
| 1 | Lemma W: P[f(x)−f(y) ≥ 2] ≥ P[y<x]/(π_N+1) when N(x,y) ≠ ∅; no BFT hypothesis (§2) | PROVEN | **HOLDS**. I checked the injection line by line: it is well-defined, lands in E₂, and each image has at most a_R + a_L ≤ π(w) ≤ π_N preimages. I re-computed it with exact counts: 0 violations for N ≤ 8 (2 800 472 posets and 91 740 332 ordered pairs at N = 8). |
| 1′ | Lemma W (a): gap ≥ 2 possible ⇔ N ≠ ∅ | PROVEN | **HOLDS** |
| 1″ | "the earlier generic counterexample (1/70) is a small denominator, not a small ratio" | remark | **HOLDS**. The 1/70 and the "generic Lemma W is false" line in KSBFT-B §3 are both about the *absolute* probability. Lemma W is about the *ratio*. The two are consistent (§1.4). KSBFT-B's "it has to use the BFT-triple hypotheses" is superseded: the ratio lemma is generic, and the BFT structure enters only through the denominator. |
| 2 | Thm 1.3″: δ ≥ C_BFT + min(θ₀, C_BFT/((5+3√5)(D+1)+1)); δ > 0.2764 for every D ≤ 3471 (§3) | PROVEN-mod-paper | **HOLDS** (§4). Every step was re-derived against the PDF. The consumed paper facts are Cor 2.2, Lemma 2.3, (2.1)–(2.2), and Lemma 3.2(i)–(v) with the hypothesis weakened. Prop C was re-derived here in full (§4.4). |
| 2′ | window chain p ≥ 2C_BFT − p′ ≥ C_BFT − θ (§3.1) | PROVEN-mod-paper | **HOLDS**. S/2 ≥ C_BFT + R/(5+3√5) is re-derived, and I checked it exactly on all 97 199 Case-D BFT triples with N ≤ 7 (0 violations). |
| 2″ | θ₀ = 0.2764 − C_BFT = 6.7978·10⁻⁶ comes from Case C / Lemma 3.2(i) | PROVEN | **HOLDS**. It is (√5 − 2.236)/10. Lemma 2.3 is the only place 0.2764 is irreducible (§4.2). |
| 2‴ | D₀ = 3471; 10⁴ → 2.36·10⁻⁶; 10⁶ → 2.36·10⁻⁸ | arithmetic | **HOLDS**. Recomputed: θ_W(3471) = 6.79903·10⁻⁶ > θ₀ > θ_W(3472) = 6.79707·10⁻⁶. |
| 3a | "the M-witness 1/(24.5(D+1)) never binds once Lemma W is linear" | PROVEN | **HOLDS**. θ_W(D) < C_BFT/((5+3√5)(D+1)) = 0.02361/(D+1) < 0.04082/(D+1). |
| 3b | "Prop C is load-bearing again: with the printed 441 the D-uniform range stops at D = 17" | PROVEN | **HOLDS**. 1/(441·18²) = 6.9987·10⁻⁶ > θ₀ > 1/(441·19²) = 6.2814·10⁻⁶. Prop A (a ≥ M) cannot substitute, since it helps only for D ≤ 2. This correctly reverses audit mg-3a14 item 14, which was right only for the exponential window. |
| 4 | 1/(π+1) is sharp at every π = 2..7 on Case-D BFT triples (EMPIRICAL, n ≤ 8) | EMPIRICAL | **HOLDS**, reproduced for π = 2..7 at N ≤ 8 with my own generator, with the minimum attained on the (x,y) side of a Case-D triple. **Strengthened**: I prove it for every D ≥ 3 with an explicit family (§3). The doc's §0.2 sentence "no version of Lemma W that uses only 'Case-D BFT triple + range ≤ D' can beat 1/(D+1)" had support only for D ≤ 7 in the doc. It is now PROVEN for all D (§3). |
| 5 | "no new D at 1/3; the route is capped below 0.2764 by Case C" (§4, §6) | PROVEN-mod-paper | **HOLDS** as a statement about this route (§5). |
| 6a | §1.2 table row "c = D^(−k): θ₀ for D up to ~(8.6·10³)^(1/k)" | "PROVEN arithmetic (window.py, asserts included)" | **BROKEN (minor number)**. The row is not in `window.py`. The correct threshold is D^k ≤ 1/((5+3√5)θ₀) = 1.256·10⁴, or 3.47·10³ if c multiplies p as in Lemma W. Neither value is 8.6·10³. Nothing downstream uses it. |
| 6b | 67/242 conditional: θ₀′ = 4.663·10⁻⁴, constant regime to D = 49 (§4) | conditional | **HOLDS** as arithmetic. The appendix claim itself is UNVERIFIABLE (not checked by the doc or by me). Cor 2.2 still works at 0.27686 < 1/e, and Lemma 2.4 uses δ only through Cor 2.2. |
| 6c | Fibonacci control p(F_m; x₀,x₁) = F_{m+1}F_m/F_{2m+2} for m = 2, 4, 6 (§5) | EMPIRICAL | **HOLDS**: 2/8, 15/55 = 3/11, 104/377 = 8/29. |
| 6d | "near-C_BFT structure repels N-elements" (§5, G(m,a,b)) | EMPIRICAL, weak | Not re-run. It is correctly labelled as an observation, and nothing consumes it. |
| 6e | "What it newly settles: δ > 0.2764 for 7 ≤ D ≤ 3471" (§6) | PROVEN-mod-paper | **HOLDS** relative to the repo and the paper's printed Thm 1.3. I have no literature search beyond the shared context. |

**Bottom line.** Lemma W is a correct, generic, and sharp theorem. Theorem 1.3″ holds modulo the same paper inputs as KSBFT-B's Theorem 1.3′ (Cor 2.2/Kahn–Linial, Lemma 2.3/Appendix A, BFT95 (2.1)–(2.2)). It **no longer consumes Lemma 3.1 or Lemma 4.2 at all**: the 441 and the AI-assisted Lemma 4.2 inequalities are off the path, replaced by Prop C (re-derived here). No counterexample was found. One minor number in a hypothetical table row is wrong.

---

## 1. Lemma W: the injection in full (claim 1, HOLDS)

Setting: x ∥ y. E₁ = {g : g(x) = g(y)+1}, E₂ = {g : g(x) = g(y)+2}, and N = {w ∉ {x,y} : w ⊀ y, x ⊀ w}.

### 1.1 Φ is well defined and lands in E₂

Take g ∈ E₁, with y at position i and x at position i+1. Every w ∈ N sits outside {i, i+1}, so it is before y or after x.

**Case A (some N-element after x).** Let w be the first one, at position i+1+j, and let t₀ = x, t₁, …, t_{j−1} be the elements strictly between y and w. I must show t_k ∥ w for every k.
- w ⊀ t_k, since t_k precedes w in a linear extension.
- Suppose t_k ≺ w. For k = 0 this contradicts x ⊀ w. For k ≥ 1:
  - t_k ⊀ y, because t_k is after y in g;
  - x ⊀ t_k, else x ≺ t_k ≺ w;
  - t_k ∉ {x, y}.

  So t_k ∈ N, and it lies strictly between x and w, contradicting minimality.

Moving w left across a block of elements that are all incomparable to it preserves every relation. Each pair whose relative order changes is a (w, t_k) pair, and those are incomparable. The result has y, w, x at positions i, i+1, i+2, so it lies in E₂. ✔

**Case B (no N-element after x).** Then N ≠ ∅ lies before y. Let w be the last N-element, and let s₁, …, s_{j−1}, s_j = y be the elements after w up to and including y.
- s_k ⊀ w, by position.
- For y: w ⊀ y, because w ∈ N.
- For k < j, suppose w ≺ s_k. Then:
  - s_k ⊀ y, else w ≺ y;
  - x ⊀ s_k, because s_k precedes x;
  - s_k ∉ {x, y}.

  So s_k ∈ N and lies after w, contradicting maximality.

Moving w right to just after y is again a linear extension, and it has y, w, x consecutive. ✔

(I note that Case B genuinely needs A = ∅. If some N-element sat after x, the last N-element before y could still be moved, but Φ would no longer be a function of g alone. The doc's case split handles this correctly.)

### 1.2 Multiplicity

Fix g′ ∈ E₂, with middle element w (so w ∈ N). A preimage is recovered from g′ by moving w
- right by j (Case A), across x and then j−1 more elements, or
- left by j (Case B), across y and then j−1 more elements.

The preimage is therefore determined by (side, j). A move is a linear extension only if every element w jumps over is incomparable to w. So j ≤ a_R, respectively j ≤ a_L, where these are the lengths of the maximal runs of w-incomparable elements immediately right and left of w in g′.

Those two runs lie on opposite sides of w, so they are **disjoint** sets of elements incomparable to w. Hence a_R + a_L ≤ π(w) ≤ π_N.

If y ≺ w, then a_L = 0 and there is no Case-B preimage. The bound only gets easier. ✔

Not every (side, j) within the runs need be an actual preimage, because Φ's choice rule must also select w. That only helps the upper bound. So |E₁| ≤ π_N|E₂|. Then

p = P[E₁] + P[gap ≥ 2] ≤ π_N P[E₂] + P[gap ≥ 2] ≤ (π_N + 1) P[gap ≥ 2]. ∎

### 1.3 Part (a)

The added relations y < w < x close into a cycle only via w ≼ y, x ≼ w, or x ≼ y. The first two are excluded by w ∈ N and the third by x ∥ y. The converse holds by position. ✔

### 1.4 Reconciliation with "generic versions are FALSE"

KSBFT-B §2.1 (1/70 = P[top of one 4-chain before bottom of the other], n = 8, π = 4) and KSBFT-B §3 ("min P[gap ≥ 2] at n = 8 is 0.235, 0.0556, 0.0143, … by π") are **lower bounds on an absolute probability**. That is Lemma 3.1's shape, and it really is exponential in general.

Lemma W bounds the **ratio** P[gap ≥ 2]/P[y < x]. When P[gap ≥ 2] is tiny, P[y < x] is tiny too: at π = 4 the minimum 1/70 forces p ≤ 5/70. So nothing contradicts. What changed is the realisation that the BFT window supplies the denominator (p ≥ C_BFT − θ, §4.1), so the absolute bound is not needed.

KSBFT-B §3's sentence "What Lemma W must use: … It cannot use generic event bounds" was true of absolute bounds. It is now moot.

### 1.5 Machine check (independent)

`out_indep_3to7.txt`: for N = 3..7, the poset counts equal A006455. The ordered incomparable pairs number 22, 260, 3968, 82088 and 2336072, matching `lemw.c`'s counts from a different generator.

| check | N=3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| K0 gap ≥ 2 possible ⇔ N ≠ ∅ | 0 | 0 | 0 | 0 | 0 |
| K1 c₁ ≤ π_N c₂ | 0 | 0 | 0 | 0 | 0 |
| K2 **p ≤ (π_N+1)·P[gap ≥ 2]** (stated form) | 0 | 0 | 0 | 0 | 0 |
| NEG c₁ ≤ (π_N−1)c₂ (false) | 12 | 135 | 1350 | 15098 | 235491 (FIRES) |

The negative-control counts coincide exactly with `lemw.c`'s K1m. That is two independent generators and two independent counting methods agreeing on 5 numbers.

**N = 8** (`out_indep_8.txt`, 4 min 40 s on one core): there are 2 800 472 posets (A006455) and 91 740 332 ordered pairs, the same as the doc. K0, K1 and K2 have 0 violations. The negative control gives 5 025 852, identical to `lemw.c`.

---

## 2. The window chain (claim 2′, HOLDS)

From the PDF, pp. 7–9: p := P[f(y) < f(x)] and p′ := P[f(z) < f(y)]. This is **the same orientation** as Lemma W's p, which I checked because a flipped orientation would have broken the plug-in.

1. **The S bound.** The inequality S/2 ≥ C_BFT + R/(5+3√5) is the last display of Lemma 2.4's proof before "(2.4)". It uses only (2.1)–(2.2), Claim 2.5 and the chord bound, and it uses no δ-hypothesis. I re-derived all of it:
   - Claim 2.5. With b₂ = s − 2u we get b₂ + b₃ ≤ s²/(4u) − u. On (0, u₀] the right side is 7u + 3/2, and on [u₀, s/2] it is 4u + 3s²/(4u). The endpoint values are (7/2)√(s² + 1/4) − 1/4 and 7s/2.
   - F is convex, being the max of convex functions. F(0) = 3/2 and F(1) = (7√5 − 1)/4 = c.
   - 7/(2(9+c)) = 0.276393 = C_BFT, and (c − 3/2)/(2(9+c)) = 0.085410 = 1/(5+3√5).
2. **The p′ bound.** Cor 2.2 with h(y) ≤ h(z) gives p′ ≤ 0.2764 < 1/2, so δ(P;y,z) = p′ ≤ δ(P) ≤ C_BFT + θ. Cor 2.2 needs δ ≤ 0.2764, which θ ≤ θ₀ gives.
3. **Conclusion.** With R ≥ 0: p ≥ 2C_BFT − p′ ≥ C_BFT − θ, and symmetrically p′ ≥ C_BFT − θ. ✔

**Machine check.** `indep_e60e.c` computes S, a₁ = p(1,1), a₂ = p(1,2) + p(2,1) and R for every Case-D BFT triple, using exact integer counts via consecutive-pattern DP. It checks (F-b) and (2.5). There are 3 + 64 + 554 + 6894 + 97199 triples for N = 3..7, and 2 092 966 at N = 8, with **0 violations** of each. This is a check of the paper's BFT95-derived inequality on small posets, not a proof of it.

---

## 3. Sharpness for every D: an explicit family (claim 4, HOLDS and strengthened)

**Reproduction (EMPIRICAL, exact).** In `out_indep_3to7_xy.txt` I restrict to the (x,y) side of Case-D BFT triples. For N = 7, the minimum of P[gap ≥ 2]/p equals 1/(π+1) exactly for every π(P) = 2, 3, 4, 5, 6: 6/18, 3/12, 2/10, 8/48 and 8/56. The minimum over *all* ordered pairs is also exactly 1/(π+1) at every π. Within max(p, p′) ≤ 0.30, N ≤ 7 has triples only at π = 3, and the minimum there is 1/4. This matches the doc's N ≤ 7 lines.

At **N = 8** (`out_indep_8.txt`), the minimum is again exactly 1/(π+1) for π = 2..7, attained on the (x,y) side of a Case-D triple; π = 7 gives 40/320. Within max(p, p′) ≤ 0.30:
- π = 3: 1/4;
- π = 4: 1/4 > 1/5;
- no qualifying triple at π ≥ 5.

All three match the doc's §2.1. The (F-b) and (2.5) checks have 0 violations on all 2 092 966 Case-D triples at N = 8.

**Proposition (PROVEN here).** For k ≥ 0, let Q_k = ({x ≺ z} ⊔ {y}) ⊕ (c₁ ≺ ⋯ ≺ c_k), with every c_i above x, y, z. Let P_k = Q_k ⊔ {w}, where w is incomparable to everything. Put D := k + 3. Then:
1. π(P_k) = π(w) = D.
2. (x, y, z) is a Case-D BFT triple of P_k.
3. N(x,y) = {w}.
4. P[f(x) − f(y) ≥ 2] / P[f(y) < f(x)] = 1/(D+1) exactly.

*Proof.*
1. π(w) = |Q_k| = k+3. Every other element is incomparable to at most y or x/z, and to w.
2. In Q_k, the heights are those of 2+1: h(x) = 4/3, h(y) = 2, h(z) = 8/3, because the chain sits on top. Inserting the isolated w uniformly into the |Q_k| + 1 slots multiplies every height by (|Q_k|+2)/(|Q_k|+1) ≤ 5/4. So h(x) ≤ h(y) ≤ h(z) ≤ h(x) + (4/3)(5/4) < h(x) + 2. The order relations x ≺ z, x ∥ y, y ∥ z are those of Case D.
3. N(x,y) = {w}, since z and every c_i lie above x.
4. In Q_k, N_{Q_k}(x,y) = ∅, so y before x forces y immediately before x. Let A be the number of such extensions of Q_k. In P_k, w goes into one of |Q_k| + 1 slots:
   - the one slot between y and x gives gap exactly 2;
   - the other |Q_k| slots give gap 1.

   So p = (|Q_k|+1)A/e and P[gap ≥ 2] = A/e, and the ratio is 1/(|Q_k|+1) = 1/(D+1). ∎

`family_e60e.py` checks this exactly for D = 3..13: h = (5/3, 5/2, 10/3), …, (10/7, 15/7, 20/7), p = 1/3, and ratio 1/(D+1). It also checks a generic, non-BFT family: a chain from x plus isolated y and w, with ratio 1/(D+1) for D = 2..11. Negative control: deleting w makes the check fail on all 6 rows tested.

**Consequence.** Lemma W's constant is best possible for every D, both generically and on Case-D BFT triples. The doc's sentence "no version of Lemma W that uses only 'Case-D BFT triple + range ≤ D' can beat 1/(D+1)" is therefore **true for all D**, but the doc supported it only for D ≤ 7. These examples have p = 1/3, far outside the window, which is consistent with the doc's own caveat.

---

## 4. Theorem 1.3″ (claim 2, HOLDS)

### 4.1 The hypothesis δ ≤ C_BFT + θ, θ ≤ θ₀, and where Lemma 3.2 uses it

Every use of the δ-hypothesis in Lemma 3.2's proof (pp. 11–12), read line by line:
- **(i)**
  - Cases A and B give a pair with δ ≥ 1/3 > 0.2764 (BFT95 plus Lemma 2.1).
  - Case C gives max > 0.2764 by Lemma 2.3.

  So δ ≤ 0.2764 suffices. The printed proof writes "< 0.2764" but only needs the non-strict form, because Lemma 2.3's inequality is strict.
- **(ii)** Uses no δ-hypothesis.
- **(iii)** Uses Lemma 2.4, which needs δ ≤ 0.2764, and gets R ≤ (5+3√5)(δ − C_BFT) from (2.4), where max(δ(P;x,y), δ(P;y,z)) ≤ δ(P). The doc replaces "q₃ ≤ P[E]" (Lemma 3.1) with Lemma W. The inequality P[E] ≤ P[f(x) − f(y) ≥ 2] is no longer needed; the doc uses P[f(x) − f(y) ≥ 2] directly with (2.5):

  (C_BFT − θ)/(D+1) ≤ p/(π_N+1) ≤ P[gap ≥ 2] ≤ R ≤ (5+3√5)θ,

  so θ ≥ θ_W(D). The mirror pair (z,y) has N′ = {w : w ⊀ z, y ⊀ w} and denominator p′ ≥ C_BFT − θ, and (2.5) contains both gap terms. ✔

  The existence of w with g(y) < g(w) < g(x) is exactly w ∈ N (Lemma W(a)), so the hypothesis N ≠ ∅ of Lemma W(b) is met. ✔
- **(3.8)–(3.9), (iv), (v)** Use only (3.7) and (ii). ✔

### 4.2 θ₀

θ₀ = 0.2764 − (5 − √5)/10 = (√5 − 2.236)/10 = 6.797750·10⁻⁶. The cap enters from Lemma 2.3, from Cor 2.2 (via Lemma 2.4), and from (F-a):
- Cor 2.2 extends to any threshold ≤ 1/e.
- Lemma 2.3's 0.2764 is a hard numeric input from BFT95 §6 / Appendix A.

So the doc's attribution of θ₀ to Case C is right. ✔

### 4.3 The contradiction

Step 1 is the component reduction (p. 12, "comparison probabilities within a component are unchanged"; the range does not increase). Lemma 4.1 then supplies a triple with max(|d_k|, |d_{k+2}|) = M. Lemma 3.2's structure applies to it. KSBFT-B Prop B gives M ≥ d₁ ≥ 1/(D+1); its injection was re-read here and is fine, and it is tight on a D-chain plus a point. Prop C gives a ≥ C_BFT + M/24.5.

Then δ ≥ C_BFT + 1/(24.5(D+1)) > C_BFT + θ_W > C_BFT + θ, which is a contradiction. Taking θ = θ₀ when θ₀ < θ_W(D), i.e. D ≤ 3471, gives the strict δ > 0.2764. Otherwise the supremum gives δ ≥ C_BFT + θ_W(D). ✔

### 4.4 Prop C re-derived (it is now load-bearing, so I redid it)

Notation: ρ = (√5−1)/2, r = ρ + X, s = ρ + Y, Z = 1 + r + s, a = max(r, s)/Z (from (4.3)–(4.4)), and ε = a − C_BFT. The steps:
- **Step 1.** √5 r − ρZ = (1+ρ)X − ρY, since 1 + 2ρ = √5 and √5 − ρ = 1 + ρ. ✔
- **Step 2.** g := v + 2rs − 2 = √5(X+Y) + 2XY, since 2ρ + 2ρ² − 2 = 0. X + Y ≥ 0 follows from (4.7), using |X| ≤ ρ (as r ∈ [0,1]). ✔
- **Step 3.** max(A, B) ≥ (X+Y)/2 + √5|X−Y|/2 ≥ max(X, Y) ≥ W/2 when X + Y ≥ 0. ✔
- **Step 4.**
  - F = (2+ρ)X − (1−ρ)Y + XY, using 1 − ρ² = ρ ✔.
  - |F| ≤ (2+ρ)|X| + (1−ρ)|Y| + ρ|Y| ≤ (2+ρ)W ✔.
  - 2|X||Y| ≤ ρ(|X| + |Y|) ✔.
  - α* + β* ≤ g/Z, from (4.6) ✔.
  - |d| ≤ (1+2√5)W/Z ≤ (20 + 2√5)ε = 24.47ε ✔.

Prop C needs no smallness of ε. The paper's "ε < 10⁻⁵" (p. 16) is not used by Prop C, and the paper's own proof does not really need it either: (r−s)² ≤ (v − 2ρ)(v + 2ρ + 2) uses only v ≤ 1.237. θ₀ < 10⁻⁵ anyway.

Prop C consumes (4.3), (4.6) and (4.7) (p. 14–15). I re-read those: they follow from the structure (3.4)–(3.5) by the counting argument printed there. So **Thm 1.3″ uses neither Lemma 3.1 nor the AI-assisted Lemma 4.2 inequalities.**

### 4.5 Arithmetic (recomputed independently in Python; one-liners in §8)

| quantity | value |
|---|---|
| θ₀ | 6.797750·10⁻⁶ |
| D₀ | 3471: θ_W(3471) = 6.799026·10⁻⁶, θ_W(3472) = 6.797068·10⁻⁶ |
| 441-witness crossover | D = 18: 1/(441·18²) = 6.9987·10⁻⁶, 1/(441·19²) = 6.2814·10⁻⁶ |
| 24.5-witness crossover | D = 6004 |
| 67/242 variant | θ₀′ = 4.6630·10⁻⁴, D ≤ 49 |
| C/(5+3√5) | 0.023607 |
| 1/24.5 | 0.040816 |

---

## 5. "No new D at 1/3; capped by Case C" (claim 5, HOLDS)

The route has two parts: the contradiction argument (the window) and Lemma 3.2's structure. Both need δ ≤ 0.2764, because of Lemma 2.3. So the best conclusion the route can ever produce is δ > 0.2764, whatever Lemma W and whatever witness is used.

Inside the window, Prop A (M ≤ max(p, p′) ≤ δ) makes "M ≥ 1/3" unpayable. Posets with 0.2764 < δ < 1/3 are untouched. So no D gains 1/3. For D ≤ 6, 1/3 was already known (Peczarski; shared context, not re-read). ✔

The residual gain is δ > 0.2764 on 7 ≤ D ≤ 3471. That is 6.8·10⁻⁶ above C_BFT, and it is D-uniform on that range.

---

## 6. What Thm 1.3″ does to the paper's Theorem 1.2 constant

Theorem 1.2 (p. 2) combines three cases:
- width > K: Thm 1.4, δ > 1/e − 10⁻¹⁰⁰;
- width < K and range > L: Thm 1.5, δ > 1/2 − ϵ;
- range ≤ L: Thm 1.3 with D = L, δ > C_BFT + η_L.

The last is the only one near C_BFT. Substituting Thm 1.3″ gives:

**ε(Thm 1.2) = min(θ₀, C_BFT/((5+3√5)(L+1)+1))**, which is ≈ 0.0236/(L+1) once L > 3471.

Both the double exponential in (D+1)^(−4(D+1)) and the paper's (1.5) layer from it are gone. **The bottleneck is now entirely the size of L = L(K, ϵ) from Thm 1.5 (AK25b)**, which the paper states existentially (p. 5). Its explicit value is not printed ("we omit their values", p. 5), and the derivation of (1.5) is omitted (p. 2).

So I cannot say what the new ε is numerically. That is UNVERIFIABLE from the PDF. **Inference, not checked:** if (1.5) was obtained as η_L, then (L+1)^(4(L+1)) ≈ 3^(3^(1.6·10¹⁹)). That gives L ≈ 3^(1.6·10¹⁹)/(6.4·10¹⁹·log₃L), and the new ε ≈ 0.0236/L ≈ 10^(−7.6·10¹⁸), i.e. one tower level removed.

The conditionality of Thm 1.4 on AK25a and Haq26 is unchanged. In the programme's own terms, for the conjecture the only open region stays range ≤ L*, and Thm 1.3″ leaves it open at 1/3 (§5).

---

## 7. Every other PROVEN claim and paper use, checked

- **§1.1** transcription of Lemma 3.2(iii): matches pp. 11–12, including "q₃ ≤ P[E] ≤ P[f(x) − f(y) ≥ 2] ≤ R". ✔
- **§1.2** table:
  - the bold row ✔;
  - the c = q₃ row reproduces KSBFT-B ✔;
  - the constant-c₀ row ✔ (6003/6004);
  - the D^(−k) row's "(8.6·10³)^(1/k)" is **wrong** (item 6a). It is also mislabelled as asserted in `window.py`, which contains no such row.
- **§1.2** "mg-3a14 §2.8 missed the θ₀ cap": correct. That audit's constant-window hypothetical ignored that Lemma 3.2(i) caps θ at θ₀. ✔
- **§2** remark "the injection is the same kind as Prop B": ✔. Prop B moves the first incomparable element to the front, and has the same run argument with one side.
- **§3.1 (F-a)** "δ(P;x,y) = p": needs p ≤ 1/2, which Cor 2.2 gives since h(x) ≤ h(y). ✔
- **§3.2 step 1**: n ≥ 3 and connected, as on p. 12. ✔
- **Consumed and not re-derived by me**: Lemma 2.1 (Kahn–Linial / AK25a), Lemma 2.3 and Appendix A, BFT95 (5.2), (5.5), (5.7)–(5.8) → (2.1)–(2.2), and BFT95 Thms 4.1/4.2 (Cases A/B). These are the same external inputs the paper's own Thm 1.3 uses. Nothing new is consumed.

---

## 8. What I did not do, and negatives

- **Census range**: my own census is exhaustive for N ≤ 8. N = 8 is run only with `FULL=1`: it is one core, about 5 min, and its transcript is committed.
- **Not re-run**: `lemw.c`, `fibw.py`, and the G(m,a,b) family (§5 of the doc). I recomputed the Fibonacci control values by hand. I did not run the doc's `run_all.sh`.
- **Not checked**: Lemma 2.3 / Appendix A (including 67/242), BFT95, Lemma 2.1, Peczarski and Brightwell–Wright, and eq (1.5)'s derivation (omitted by the paper). Also the literature status of "δ > 0.2764 for 7 ≤ D ≤ 3471 is new": I did no search.
- **Counterexample hunt, negative**:
  - The injection's weak points were candidate failures, and I tried each:
    - (i) Case B when some N-element also lies after x. Excluded by the case split.
    - (ii) y or x comparable to w in g′, which kills a run. This only lowers the count.
    - (iii) The same g′ reached from both sides with the same j. Impossible, since the directions differ.
    - (iv) Orientation mismatch between the doc's p and the paper's p. They are the same.
  - Exhaustive N ≤ 7: 0 violations.
- **Instrument notes**: the (F-b) check compares doubles of exact integer quotients with a 1e−12 tolerance. Everything else is exact integer or `Fraction`.

Recompute the §4.5 numbers:

```
python3 -c "from math import sqrt;C=(5-sqrt(5))/10;K=5+3*sqrt(5);t=0.2764-C;tw=lambda D:C/(K*(D+1)+1);print(t,max(d for d in range(2,10**4) if tw(d)>t),1/(K*t))"
```

## 9. Reproduce

```
sh code/audit_ksbft_e60e/run_all.sh          # ~10 s, N=3..7 + family; fails loudly on any nonzero count or silent control
FULL=1 sh code/audit_ksbft_e60e/run_all.sh   # adds N=8 (single core, long)
```
