# KSBFT-K: write-up of Lemma W and Thm 1.3″, literature novelty check, and a check of KSBFT Lemma 2.3 / Appendix A (mg-3c5b)

Deliverables:
- `notes/lemma-W-polynomial-range-bound.tex` and its PDF: a 7-page self-contained note that compiles with pdflatex (TeX Live 2019).
- This file.
- `code/ksbft_k_3c5b/`: `appA_check.py`, `run_all.sh` and the transcript `out_appA_check.txt`. `sh code/ksbft_k_3c5b/run_all.sh` takes under 2 s, runs one process, is deterministic, and fails loudly.

Sources:
- The paper is KSBFT_v7 (`/Users/daniel/files/KSBFT_v7.pdf`, read with `pdftotext -layout`); page numbers are the printed ones.
- BFT95 is the authors' preprint of 30 May 1995, https://page.math.tu-berlin.de/~felsner/Paper/newbft.pdf, retrieved by a sub-agent. Pages 4–5 and 10–15 were checked as rendered images. Page numbers are the preprint's, and I did not see the Order version.

Labels: PROVEN (proof in the note), EMPIRICAL (instrument and range given), CONJECTURED.

---

## 0. Verdict

1. **The note is written and compiles (PROVEN content).**
   - It proves Lemma W, with its sharpness for every D ≥ 2 generically and for every D ≥ 3 on Case-D BFT triples.
   - It proves Thm 1.3″: δ(P) ≥ C_BFT + min(θ₀, C_BFT/((5+3√5)(D+1)+1)), strict for D ≤ 3471.
   - Its only imports are four external facts, listed below as I1–I4.
   - Everything else it consumes from KSBFT is reproved in the note: Cor 2.2, Lemma 2.4, Lemma 3.2 under the weaker hypothesis with the new (iii), Lemma 4.1, (4.2)–(4.7), and Props B/C from mg-d707.
   - KSBFT Lemma 3.1 and Lemma 4.2 are not used.
2. **Novelty: PARTIAL, and NOT FOUND for the exact statement.** The nearest known result is Kahn–Saks' two-sided inequality a₂ + b₂ ≥ a₁ + b₁ with a₁ = b₁ (KS84, as restated in BFT95 Lemma 2.1 (2.1), (2.4)). Lemma W is one-sided and carries a range factor, which the sharpness family shows is necessary. The consequence "δ ≥ C_BFT + c/(D+1) for range ≤ D" was not found anywhere (§2).
3. **KSBFT Lemma 2.3 / Appendix A: HOLDS modulo BFT95 Lemmas 2.2, 2.3, 6.2 (with 6.1) and Kahn–Linial.**
   - All of the appendix's own algebra is re-derived by hand, and checked numerically where marked (§3).
   - One justification is too weak, though its conclusion holds: "p, p′ ∈ (1/5, 3/10) ⇒ 3/5 < v_q < 1" is false near 3/10. It holds on the range the proof actually has.
4. **67/242: HOLDS as a non-strict bound, max(δ(x,y), δ(y,z)) ≥ 67/242 ≈ 0.276860.** At T = 67/242 the last line gives exactly h(z) − h(x) ≥ 2, so the argument closes for every T < 67/242 and not at T itself. Consequences:
   - θ₀ → θ₀′ = 67/242 − C_BFT = 4.663·10⁻⁴.
   - Thm 1.3″ becomes δ ≥ C_BFT + min(θ₀′, θ_W(D)), which is ≥ 67/242 for D ≤ 49.
   - This is PROVEN-mod-(the same BFT95 imports as Lemma 2.3 itself).
5. **New point surfaced by the literature search: where finiteness enters (PROVEN, in the note as a remark).**
   - BFT95 Thm 1.4 has thin infinite posets of range 2 with balance exactly C_BFT. So any bounded-range improvement must use finiteness.
   - Lemma W and the structure lemma survive the limit: the Fibonacci central triples have N = ∅ and the bridged 2+1 structure.
   - Finiteness enters only through Lemma 4.1's boundary relations (d₁ ≥ 0, d₁ + d₂ ≥ 0, …) and Prop B's bottom element (d₁ ≥ 1/(D+1)).
   - This matches the shared context's remark that "any case-(c) argument must use FINITENESS quantitatively". The finiteness is used polynomially, not exponentially.

## 1. The note: what it contains, and what it imports

The four external inputs, stated in the note exactly as used:

| # | statement | source |
|---|---|---|
| I1 | h(x) ≤ h(y) ⇒ P[f(y) < f(x)] ≤ 1 − 1/e | Kahn–Linial 1991 p.365; AK25a Cor 5.1(b); KSBFT Lemma 2.1 |
| I2 | Cases A, B ⇒ P[f(y) < f(x)] ≥ 1/3 | BFT95 Thms 4.1, 4.2. The preprint states them as "Prob(x<y) ≤ 2/3", which is the same thing. |
| I3 | Case C ⇒ max(δ(x,y), δ(y,z)) > 0.2764 | KSBFT Lemma 2.3 / App. A, from BFT95 §6. Checked in §3 below. |
| I4 | Case D: 2a₁+a₂ ≤ S, 2a₂+2a₃ ≤ S, 4a₁a₃ ≤ a₂², 7 ≤ 9S + 7a₁ + 3a₂ + 3a₃ | BFT95 (5.2), (5.5), (5.7), (5.8) = KSBFT (2.1)–(2.2). The preprint's (5.5) is x₁x₃ ≤ x₂²/4 from Thm 3.2 and AM–GM. (5.7) is 2·(5.1) + (5.6); (5.8) is 4·(5.6) + (5.1) with x₅ ≥ 0. |

Proofs are reproduced in the note, re-derived by me line by line in this session. They match mg-f218, mg-d707 and the audits mg-e60e and mg-3a14.
- Cor 2.2.
- Lemma 2.4:
  - the Claim 2.5 case split, with u₀ = (√(1+4s²) − 1)/4 ≤ s/2;
  - the convexity chord;
  - 7/(2(9+c)) = C_BFT and (c − 3/2)/(2(9+c)) = 1/(5+3√5), both checked exactly;
  - (2.5) via p(−1, j) = p(1, j−1), using that x ≺ z forces f(z) − f(y) ≥ 2 on {f(x) = f(y)+1}.
- The window lemma: p, p′ ≥ C_BFT − θ.
- The structure lemma, with (iii) proved via Lemma W. The audit's §4.1a is merged as a remark: it is the same middle term, pair, orientation and event as (2.5).
- Lemma 4.1.
- Prop B (injection; t − 1 ≤ π(c)).
- Prop C:
  - the constant is 20 + 2√5 ≈ 24.47, rather than the rounded 24.5;
  - every identity was re-expanded: F = (2+ρ)X − (1−ρ)Y + XY, g = √5(X+Y) + 2XY, and so on;
  - it also covers the height identities (4.2)–(4.7) under the structure lemma, including |L′| = m (w ≺ y ⇒ h(w) < h(y) strictly, so tie-breaking does not matter).
- Component reduction. The incomparability-graph components are totally ordered, and the note includes the proof.

**Merged from the audit (mg-e60e):**
- the Case-B well-definedness remark: move only when A = ∅;
- preimages determined by (side, j), with disjoint runs, so a_R + a_L ≤ π(w);
- a_L = 0 if y ≺ w;
- §4.1a;
- the P_k sharpness family.

Added here:
- a generic sharpness family for every D ≥ 2: a (D−1)-chain from x, plus isolated y and w;
- π_N ≥ 1;
- the finiteness remark;
- the Kahn–Saks comparison remark;
- the 67/242 section.

**Not in the note, deliberately:** the census numbers of mg-f218/mg-e60e (EMPIRICAL). The note's claims are all proofs, so the census is not needed to check it. It remains in the repo as corroboration.

## 2. Novelty check

Done by a sub-agent (web search plus full-text reads and greps). I then checked its key citation, BFT95 Lemma 2.1, myself against the rendered page.

**Verdict: PARTIAL.** Nothing I found states Lemma W or anything that implies it. The nearest items:

| source | what it has | relation to Lemma W |
|---|---|---|
| Kahn–Saks 1984, via BFT95 Lemma 2.1 (preprint p.4) | a₁ = b₁ (adjacent in either order equally likely); a₂ + b₂ ≥ a₁ + b₁; log-concavity for i ≥ 2 | Two-sided with constant 1. Lemma W is one-sided: b₁ ≤ π_N·b₂. It **cannot** have a universal constant (sharp family), so the two statements are different in kind. In BFT's parametrisation Lemma W reads ε = b₁/B ≤ π_N/(π_N+1). KS84/BFT95 never bound ε away from 1. |
| BFT95 Lemma 5.1: p(2,3) ≤ p(1,3) + p(1,4) | a swap injection similar in spirit | a different inequality, with no multiplicity/range factor |
| AK25a (arXiv:2509.11549) Lemma 5.2(b): h(y) − h(x) ≤ 1/P(f(y) − f(x) = 1) | involves the adjacency probability | bounds a height gap, not N₁ vs N₂. The authors call it "surely not new". |
| van Handel–Yan–Zeng (arXiv:2309.13434), Kahn–Saks for x ≱ y | N_k² ≥ N_{k−1}N_{k+1} for k = 2..n−2 | N₁ appears only in N₂² ≥ N₁N₃. No bound on N₁/N₂ alone. |

**Searched with no match (full text unless noted):**
- Chan–Pak survey arXiv:2311.02743 (§4, §9.2, §13);
- Chan–Pak–Panova arXiv:2106.07133, 2104.09009, 2205.02798;
- Chan–Pak arXiv:2211.16637;
- AK25b arXiv:2510.26134;
- Gupta arXiv:2607.23926;
- arXiv 1706.04985, 1709.05753, 2410.12494, 1811.01500 (title only), 2608.12678 (Haqi);
- the Wikipedia 1/3–2/3 page.

Queries included: adjacency probability for incomparable elements in a random linear extension; Kahn–Saks N_k for incomparable pairs; "consecutive"/"adjacent"/"gap" with "linear extension" and "number of incomparable elements"; bounded range / thin posets and BFT improvements; Aires–Kahn; Aires–Chan–Pak–Panova.

**Could not access (paywalled; abstracts only):**
- Kahn–Saks 1984 (the original; BFT95's restatement used instead);
- Kahn–Linial 1991;
- Brightwell–Wright 1992 (5-thin);
- Peczarski 2008 (6-thin);
- Brightwell's 1999 survey.

The thin-poset papers are computer-assisted, so a lemma of this shape there is unlikely but **not ruled out**. The KSBFT paper itself was not found on arXiv or the web.

**The consequence δ ≥ C_BFT + c/(D+1):** NOT FOUND. It is new only for D ≥ 7, since 1/3 is known for D ≤ 6 (Peczarski; not re-read).

**Negative-result control:** the same search did find the known neighbours listed above (KS84 (2.4), AK25a Lemma 5.2(b), BFT Lemma 5.1). So the instrument does fire on adjacency-type results.

## 3. KSBFT Lemma 2.3 and Appendix A (pp. 28–31) against BFT95

**Imports, checked against the BFT95 preprint:**
- **Packed sequences.** The definition on p.4 matches App. A's (B ≤ 1/3, 0 < ε ≤ 1, cases (i) and (ii)). BFT prove uniqueness themselves; App. A attributes it to KS84 §3, which is harmless.
- **Lemma 2.2 (packing), p.5.** Any two-way sequence satisfying KS (2.1)–(2.6) has height at least that of the packed sequence with the same B and ε. This gives (A.4), h(z) − h(x) ≥ H(p,t) + H(p′,t′), applied to the pairs (x,y) and (y,z).
- **Lemma 2.3 (monotonicity), p.5.** H(B,ε) is decreasing in ε for B ≤ 1/3, except in case (ii), k = 1, ε ≤ 1/√2, which occurs only when B ≥ 1 − 1/√2 ≈ 0.293. App. A invokes it only for q ≤ 0.2764 < 0.293. ✔
  - *Side note:* BFT's remark after Lemma 2.3 prints "H(B,ε) ≤ H(B,1)". Given the lemma this must read ≥. H(B,ε) = H(B,1/(2ε)) there, and 2ε + 1/ε is convex on [1/2,1], so the minimum is at the endpoints. The numeric check P2 confirms ≥ on q ≤ 0.2764. This does not affect App. A, which uses the lemma itself.
- **Lemma 6.2 (with 6.1), p.13.** P[f(x)−f(y) ≥ 2] + P[f(y)−f(z) ≥ 2] ≥ 1/11. The hypotheses are pairwise incomparability and h(z) ≤ h(x)+2 (through Lemma 6.1: P[x>z] ≥ 3/22). No bound on p or p′ is needed. I re-checked the proof:
  - the three consecutive orders zyx, yzx and zxy are equinumerous by adjacent swaps, so P[zyx consecutive] ≤ P[z<x]/3;
  - if z < x and the three are not consecutive as zyx, then one of the two gaps is ≥ 2;
  - the packed sequence at B = 3/22, ε = 1 is a = (3,6,8,2)/22 with height exactly 2. ✔

  The orientation matches (A.1). Also p(1−t) = p − P[f(x) = f(y)+1] = P[f(x) − f(y) ≥ 2]. ✔

**The appendix's own algebra, re-derived by hand, with numeric checks in `out_appA_check.txt`:**
- (A.2) closed forms. Case (i), k = 2 derived by hand. Case (ii), k = 1 derived by hand; the pdftotext rendering "k + 3 −" is k + 3/2, which is BFT (2.10). The general k was checked numerically against the definition (P1: max error 3.3·10⁻¹³ on a 59×59 grid, a unique packed pair each time).
- Claim A.1:
  - the q ≥ 1/5 branch gives exactly (5 − 11q)/2;
  - the q < 1/5 branch gives 3 − 8q ≥ (5 − 11q)/2. ✔
- The range. p + p′ ≥ 6/11 gives p, p′ ∈ [6/11 − 0.2764, 0.2764] = [0.2690, 0.2764].
  - **Nit (reasoning too weak, conclusion true).** The text says "both p and p′ lie in (1/5, 3/10), so … 3/5 < v_q < 1". But v_{3/10} ≈ 0.565 < 3/5.
  - On the actual range, v_q ∈ [0.618, 0.636] (P3). v_q > 3/5 needs only q < 1/(1.6·2.2) = 0.2841.
- (A.5).
  - The boundary identity H(p,v) − H(p,1) = (−3v²+6v−2)/(2v(1+v)(1+2v)) was re-expanded by hand. It needs p ≥ 1/5, which holds on the range.
  - At (1+v)(1+2v) = 1/p we get a₃ = a₂, so (p,v) is on the case (i)/(ii) boundary with k = 2. ✔
  - The bound ≥ 1/12 holds on [1/2, 1], with equality at both endpoints. ✔
  - The first branch then gives 5 − 11·0.2764 + 1/12 = 2.0429 > 2. ✔
- Claim A.2:
  - **Sub-case (ii), k = 1** (1/p ≤ 1 + 2t + 2t²): the difference is p(1−t)(2 − 1/t), and p ≤ 0.2764 forces t ≥ 0.7486 > 2/3. ✔
  - **Sub-case (i), k = 2** (1 + 2t + 2t² < 1/p < (1+t)(1+2t)):
    - the identity with g(t) = 2/t − 4 + 5t + 2t² ✔;
    - (1 + 2t + 2t²) − g = (1−t)(3t−2)/t ✔;
    - g < 32/9 on (3/5, 2/3) ✔ (since 32/9 = 3.556 < 3.618 = 1/0.2764).
  - The packed-case boundaries agree with BFT (2.7)–(2.8) at k = 1, 2. A grid check (P4) confirms (A.6).
- The final line: 5 − (11/2)(p+p′) + 1/22 ≥ 5 − 11·0.2764 + 1/22 = 2.00505 > 2. ✔ (P5, exact Fraction.)

**Verdict on Lemma 2.3: HOLDS**, modulo I1, BFT95 Lemmas 2.2, 2.3, 6.1 and 6.2, and the Kahn–Saks inequalities (2.1)–(2.6) that Lemma 2.2 assumes. I did not re-derive those four BFT95 lemmas; I read their statements and re-checked the short proof of 6.2 only. One small point: t ∈ (0,1] needs P[f(x) = f(y)+1] > 0 whenever p > 0. This is a standard fact: for incomparable x, y, some linear extension has y immediately before x. I did not write out a proof here; BFT95 take it for granted in defining ε ∈ (0,1].

**The 67/242 claim: HOLDS, as ≥.** Re-run every step with the threshold T = 67/242 = 0.276860:
- Cor 2.2 / Lemma 2.1: T < 1/e ✔
- Claim A.1: T < 1 − 1/√2 ✔
- range [0.2686, 0.2769], v_q ∈ [0.617, 0.637] ✔
- Claim A.2: t ≥ 0.7475, and 32/9 < 242/67 = 3.612 ✔
- first branch: T < 37/132 = 0.2803 ✔
- last line: 5 − 11T + 1/22 = 2 **exactly** (P5, exact).

So the proof shows max(δ(x,y), δ(y,z)) > T for every T < 67/242, i.e. ≥ 67/242. The negative control is T = 0.2770, where the last line fails (FIRES). The threshold 67/242 is exactly where this argument stops. That is not evidence that the true Case-C constant is 67/242.

**Effect on Thm 1.3″** (PROVEN-mod-imports, stated in the note's §7):
- Lemma 3.2(i) now excludes Case C for δ < 67/242.
- Cor 2.2 and Lemma 2.4(c) work verbatim at threshold 67/242.
- Hence δ(P) ≥ C_BFT + min(θ₀′, θ_W(D)) with θ₀′ = 4.663019·10⁻⁴.
- The constant regime runs to D₀′ = 49: θ_W(49) = 4.7133·10⁻⁴ > θ₀′ > θ_W(50) = 4.6210·10⁻⁴.
- This matches mg-f218 §4 and mg-e60e 6b, which labelled the 67/242 claim UNVERIFIABLE; it is now checked.

## 4. What I did not do, and negatives

- **Did not read:** KS84, Kahn–Linial, Brightwell–Wright, Peczarski, or Brightwell's survey (all paywalled). BFT95 was read in its preprint form, not the Order version.
- **Did not re-derive:** BFT95 Lemmas 2.2, 2.3, 6.1, or Thms 4.1/4.2, nor the (5.x) inequalities (I read the statements; for (5.7) and (5.8) I also read the derivations from (5.1) and (5.6)). AK25a Cor 5.1(b) was not re-read.
- **No new census.** The note relies on proofs only. The existing n ≤ 8 censuses (mg-f218, mg-e60e) stand as corroboration.
- **Did not determine the numeric value of Thm 1.2's new ε.** It is min(θ₀, θ_W(L)), but L from AK25b is not printed in KSBFT.
- **Did not claim** that 67/242 is the true Case-C optimum. Did not attempt to improve Case C, which is the only remaining source of the D-uniform cap.
- **Open, unchanged:** whether Lemma W's 1/(D+1) improves under the global window hypothesis. That hypothesis is vacuous for D ≤ 3471 (or D ≤ 49 with θ₀′).
- **No outreach** to the authors or anyone else.

## 5. Reproduce

```
sh code/ksbft_k_3c5b/run_all.sh     # < 2 s; ALL OK + NEG CONTROL FIRES; rebuilds notes/*.pdf if pdflatex present
```
