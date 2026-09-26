# KSBFT-K2: revision of the Lemma W / Thm 1.3″ note per the referee audit (mg-e3df)

Revised files: `notes/lemma-W-polynomial-range-bound.tex` and its PDF (8 pp, pdflatex, TeX Live 2019).
Source of the required edits: `docs/AUDIT-mg-3c5b-note.md` §4 (audit mg-7d8e).

The mathematics is unchanged. Every edit either removes a false or overstated sentence, or adds a scope statement, a citation or a one-line justification. Theorem 1.3″, its constants and Lemma W's actual inequality are word-for-word what the audit re-derived. The sentence on eq. (1.5) ("The paper does not print $L$ …, and it omits the derivation of its (1.5), so we give no numerical value.") is kept verbatim. The note still does not claim that (1.5) is wrong.

## Must-fix

| Item | Audit finding | Edit in the note |
|---|---|---|
| **R1** | Thm W(b)'s middle link P[f(x)=f(y)+2] ≥ p/(π_N+1) is false | Deleted from the display in Thm 1.2(b). The display is now P[f(x)−f(y)≥2] ≥ p/(π_N+1) ≥ p/(π(P)+1). A remark after the proof states what the proof gives, says the middle link is false in general, and gives the counterexample c₁≺c₂≺x with y isolated (1/4 < 3/8, while P[≥2] = 1/2 ≥ 3/8). |
| **R2** | "This is the only point where the exponential loss entered" is wrong | Replaced in the remark after Lemma 4.1. It now says this removes the *first* of the two places where KSBFT Lemma 3.1's bound enters. The second is (4.11), M ≥ q₂, which Prop B replaces, and Lemma 4.2's square is replaced by Prop C. With Lemma W alone, the improvement would still be of order q₂². |
| **R3** | The abstract says Lemma W replaces "the only exponentially small quantity" | The abstract now says: "Together with a linear lower bound on the displacement and a linear replacement of Lemma 4.2 of [KSBFT], this removes every exponentially small quantity from the proof of their Theorem 1.3." |
| **R4** | The novelty claim is unscoped | The sentence "(see the accompanying search log)" is replaced by the actual scope: what was searched in full text ([CP23], Chan–Pak–Panova, [vHYZ23], [AK25a], [AK25b], [Haq26], and the statements of [BFT95]), and a statement that [KS84], [KL91], [BW92], [Pec08] and [Bri99] were **not read**, so a prior statement there is not ruled out. The abstract and §1 now say that δ ≥ 1/3 is already known for D ≤ 6 [BW92, Pec08] (as recorded in KSBFT p.3), so Thm 1.3″ is new only for D ≥ 7. |

## The rest

| Item | Edit |
|---|---|
| **R5** | Corollary. "The double exponential in L disappears" → "the factor (L+1)^(−4(L+1)) becomes ≍ 1/L". "Is obtained by combining" → KSBFT p.5 says only that Thm 1.2 follows from Thms 1.3–1.5; the combination written out (Thm 1.5 at K′ = K+1 because it needs w < K′, then Thm 1.3 at D = L(K+1,·)) is flagged as our reconstruction. Thm 1.5 is now stated to be imported from the preprint [AK25b]. [Haq26] is added to the bibliography and cited. |
| **R6** | §7 import list. Added BFT95 Lemma 2.1 (the Kahn–Saks inequalities (2.1)–(2.6), including the Alexandrov–Fenchel log-concavity), Lemma 6.1 as a separate item, and the fact t > 0 with a one-line proof (a down-set construction). Also added the sentence that the 67/242 improvement rests on App. A's *proof*, and so imports BFT95 Lemmas 2.1, 2.2, 2.3, 6.1 and 6.2 and t > 0 beyond I1–I4. |
| **R7** | v_q. The sentence "Appendix A derives 3/5 < v_q < 1 from q ∈ (1/5, 3/10)" is replaced by: App. A's "the bounds on q" is ambiguous. On (1/5, 3/10) the implication fails near 3/10, and on [6/11−0.2764, 0.2764], which App. A also established, it holds. |
| **R8** | Removed: the author line with its work-item IDs (now "Daniel Miller"), "mg-d707, Prop. B/C" (now "displacement floor" / "replaces [KSBFT, Lemma 4.2]"), "from the audit mg-e60e", the code path in "Numbers" (now "computed in double precision"), and "the accompanying search log". `grep 'mg-\|code/\|texttt\|search log'` on the .tex returns nothing. |
| **R9** | Added a duality sentence after the case list (P*, reversed triple, h* = n+1−h, preserves δ, π and the BFT-triple conditions), plus "apply Fact I2 in P*" in Lemma 4.1(i). Added "x ≠ y" to I1. Prop B now says the bound on **d₁** is sharp for a D-chain plus an isolated point; for that poset M is between 3/7 and 1/2 when D ≥ 3 (computed exactly for D = 2..8). Lemma 4.1 now notes that its (iv) is KSBFT's (v), and that KSBFT's (iv) (bridges) is omitted; §1's list of reproved results says so too. The letter g in Prop C is renamed γ. Lemma 5.1 now says where h(z)−h(x) ≤ 2 is used (S6). |
| **R10** | "Where finiteness enters": "Lemma W and Lemma 4.1 pass to such limits" is now labelled a heuristic, with an explicit statement that the passage to infinite posets is not made rigorous. The finite statement about the central triples of F_m (N = ∅, bridged 2+1 structure) is kept, and F_m is defined. BFT95 is cited as "§1 (the poset Q) and Thm 1.4". |
| **R11** | Example 2.2 gains the π_N = 1 case (y ≺ w with x isolated; ratio exactly 1/2). Thm 1.2(c) now lists it, so "sharp for every value of π_N" in the abstract is exhibited. |

Also fixed: two overfull boxes that were already there before this revision. One was the running head, fixed by a short title. The other was the header of Fact I3.

Bibliography added: [BW92], [Pec08], [Bri99], [Haq26], [CP23], [vHYZ23]. I took the bibliographic data for BW92, Pec08 and Bri99 from memory, and did not check it against the journals.

## Checks

- `pdflatex` ×2: 0 errors, 0 undefined references, 0 overfull boxes. 8 pages.
- `sh code/ksbft_k_3c5b/run_all.sh`: ALL OK, negative control fired. This also rebuilds the PDF.
- `sh code/audit_ksbft_7d8e/run_all.sh`: ALL OK, negative control fired. Its transcript still shows the false middle link firing (2568 violations), which is the counterexample now printed in the note.
- The π_N = 1 example (3 linear extensions, ratio 1/2) and the c₁≺c₂≺x counterexample (1/4 vs 3/8) were checked by hand.

## Not done

- The author line "Daniel Miller" was taken from the repository's git identity. The author should confirm the name and add an affiliation before the note is sent.
- I did not re-read BW92, Pec08, Bri99, KS84 or KL91. The note now says so.
