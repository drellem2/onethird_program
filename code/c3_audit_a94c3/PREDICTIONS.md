# `mg-94c3` — predictions for the INDEPENDENT AUDIT of `mg-76b2`

**Committed before any script of this instrument exists.** Scoring in this directory's
`README` §3 and in [`docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md`](../../docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md).

I am `mg-76b2`'s **adversary**, not its reviewer. The ticket's instruction is to
**re-derive** rather than step-check, so §1 below records what I derived **by hand, from
`Op-Form`**, before opening `mg-76b2`'s deliverable's derivations — and it is disclosed as
**hand measurement**, not laundered into a prediction. A prediction I have already made is
not a prediction.

---

## 0. What I had read before writing this file

`docs/OneThird-lambda-std-Operative-Form.md` §§4.1–4.3, §6.3, §6.4, §7.1; `STATE.md`
row 8 and the L1b blockquote; `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`
§§2.1, 5.1; `code/pairbias_repair_ba78/README.md`; and `mg-76b2`'s deliverable §§0–11
(verdict, theorem, ledger, scope). I had **not** run any code and had **not** read
`lib76b2.py` or any of `mg-76b2`'s scripts.

---

## 1. Hand measurements — disclosed, NOT predictions

| # | measurement | how |
|---|---|---|
| **H1** | The ticket's algebra is **right as stated**: `2/(n+1) ≤ ε_leak²/(2C₃)` ⟺ `n+1 ≥ 4C₃/ε_leak²` ⟺ `n ≥ 4C₃/ε_leak² − 1`. One cross-multiplication; no factor of 6 anywhere in it. | by hand, from the ticket's own two inputs |
| **H2** | `2/(n+1)` is stated in the **`ε_spec`** normalisation. `mg-6bc2` §5.1 records the per-slot LP optima as `E[inv] = 2/3, 1, 4/3` at `n = 3,4,5`; `6E/(n²−1) = 1/2, 2/5, 1/3 = 2/(n+1)` exactly. In `ε_c3ca = E/n²` the same three numbers are `2/27, 1/16, 4/75` — not `2/(n+1)` at any `n`. | by hand, arithmetic on `mg-6bc2:320` |
| **H3** | `ε_dem = ε_leak²/(2C₃)` is **also** in the `ε_spec` normalisation: `Op-Form §4.2` derives it from `1−λ_std ≤ ε_spec` through the Cheeger sandwich, and `ε_spec` is defined at `:437` by `E[inv_e] ≤ (ε_spec/6)(n²−1)`, i.e. `ε_spec = 6E[inv_e]/(n²−1)`. **Both sides of the ticket's inequality are `ε_spec`.** |  by hand |
| **H4** | The threshold is **normalisation-invariant under consistent conversion.** Multiply both sides by `(n²−1)/(6n²)`: supply `→ (n−1)/(3n²)`, demand `→ ε_leak²(n²−1)/(12C₃n²)`; the `(n−1)` and `n²` cancel and `n+1 = 4C₃/ε_leak²` comes back **identically**. So the factor of 6 is *not* a hazard when both sides move together. | by hand |
| **H5** | The hazard is **mixing**. Supply in `ε_c3ca` against demand in `ε_spec` gives `(n−1)/(3n²) ≤ ε_leak²/(2C₃)`, i.e. `n ≳ 2C₃/(3ε_leak²)` — **`≈ 16.7` at `C₃ = 1`, `ε_leak = 0.20`, against `99`.** A factor of ~6 in the threshold, in the *optimistic* direction. This is the shape of the error the ticket says has already fired once in 24h. | by hand |
| **H6** | `Op-Form §4.3` names **two** repairs and `mg-76b2` names **four chains**, and `C₃` is a *different number* in each. §4.3's gap-form writes `1−ρ_prefix ≤ C₃(1−λ_std)`; the ticket's relation `ε_dem = ε_leak²/(2C₃)` is `mg-76b2`'s chain (III), `Φ ≤ √(2C₃ε_spec)`. `mg-76b2`'s headline `C₃ = 1` is a chain-(III) statement. | read, `Op-Form:297–303` + `mg-76b2 §6` |
| **H7** | `C₃^gap ≥ 1` **identically**, for every poset, because `1−λ_std` is the *minimum* of `1−ρ(f)` over `f ∈ H` and a centred prefix indicator is one such `f`. So `C₃^gap = 1` can only hold where the optimum is attained at a prefix. | by hand |
| **H8** | `mg-76b2`'s own §7 reports `max C₃^gap = 1.500, 1.473, 1.990, 2.386` at `n = 3,4,5,6` — **above 1 and rising** — while its title says `C₃ ... IS 1`. The two are compatible only if the currencies differ, which is H6. | read, `mg-76b2 §7` |
| **H9** | `mg-ba78` (`72a6e33`) repaired `mg-6bc2` §5's adjacency *diagnostics* and explicitly did **not** touch the LP optimum or the per-slot `2/(n+1)`. So the supply side of the ticket's relation is not stale. | read, `pairbias_repair_ba78/README.md` |
| **H10** | `ε_leak = 0.20` is calibrated off `mg-3ce3`'s `survives` envelope, which is the **repaired (iii)** of L4 — and `Op-Form:444` records that under the repaired (iii) **the modulus `F` does not appear in the statement at all**. So a dependence of `ε_leak` on L4 is a dependence on L4's *threshold*, which `mg-345e` permits, not on its *modulus*, which it does not. | read, `Op-Form:434, 444, 490–507` |

---

## 2. Predictions — blind, scored in the `README`

| # | prediction | bet | why it is worth betting on |
|---|---|---|---|
| **P1** | Lemma 2.1 (`1−ρ(A_k) = n·Φ_P(A_k)/max(k,n−k)`, hence `Φ ≤ 1−ρ ≤ 2Φ`) reproduces on code sharing **nothing** with `lib76b2`, at **0 exceptions**, `n = 2..6`. | 90% | It is two lines of linear algebra and `mg-76b2` machine-checked it. If it fails, the failure is mine. |
| **P2** | Some threshold set of a minimiser `v` satisfies `Φ_P(S) ≤ √(2(1−λ_std))` at **0 exceptions** over my population. | 85% | Standard Cheeger. Included as a control on my own sweep code. |
| **P3** | Where a **monotone** dominant standard eigenvector exists, **every** threshold set of it is a prefix or a suffix — 0 exceptions. | 95% | Lemma 3.3 is a tautology about orderings. The risk is my *implementation* of "threshold set" (`mg-76b2` records a real defect here: an order-slice is not a level set). |
| **P4** | **The adversarial one.** Even restricted to posets that *satisfy* `L2`'s first disjunct (a monotone dominant standard eigenvector exists) and are primitive, `C₃^gap = min_k(1−ρ(A_k))/(1−λ_std)` **exceeds 1** at some poset with `n ≤ 6`. | 70% | If it does, `mg-76b2`'s `C₃ = 1` is **currency-specific** and its title is wider than its theorem. If it does not, the two currencies agree under `L2` and the framing objection dies. This is the single measurement that decides my verdict's shape. |
| **P5** | At least one of `mg-76b2` §7's twelve tabulated figures (`max C₃^cut`, `max C₃^gap`, `min c` at `n = 3,4,5,6`) fails to reproduce **exactly** on my independent code. | 45% | Not an accusation: population choice (all 5230 vs 4377 primitive) and float-vs-exact are enough to move a max. A mismatch would be a *definition* finding, not an arithmetic one. |
| **P6** | An L4 census of `mg-76b2`'s deliverable + instrument finds **0** load-bearing uses of L4's modulus `F` — i.e. no derived number of `mg-76b2` changes if `F` is left entirely unquantified. | 80% | `mg-76b2` §11 asserts this. Assertion is what I am here to distrust; but `ε_leak`'s repaired calibration is `F`-free (H10), so the likely answer is that the assertion is true. |
| **P7** | A census of `2/(n+1)` across `mg-76b2`'s deliverable + instrument finds it **only** in sites carrying an explicit conditional label, and **0** headline claims change if the `mg-200d` conjecture is withdrawn. | 75% | `mg-76b2` §11 asserts this too. The place it could be false is §0's verdict block, which states `n ≥ 99` in bold before the conditional appears. |
| **P8** | `mg-76b2`'s `C₃ = 1` theorem, re-derived by me from `Op-Form` and the source's L2 wording **without reading its proof**, comes out at the same constant — **1** — in the chain-(III) currency. | 65% | I expect the theorem to be right. I am predicting the *verdict*, and I want it on the record before I run anything. |

---

## 3. My two most likely errors, filed in advance

| # | error | why I am at risk of exactly this |
|---|---|---|
| **P9** | **I re-commit the currency conflation I am auditing for.** Specifically: I read `Φ*_pref/Φ*` (best prefix cut vs best cut) as the thing `mg-76b2`'s theorem is about, when the theorem is about *the Cheeger sweep bound being delivered at a prefix* — a strictly weaker and strictly more useful statement. `Φ*_pref > Φ*` at 468 posets does **not** refute it. If I write "the measurements contradict the theorem", I have made this error. | It is the *same* shape as the `1/6`-vs-`1` and the `F`-vs-`ε₀` conflations this lineage has committed twice, and the auditor is not immune to the disease he was sent to diagnose. |
| **P10** | **I mistake a framing correction for a refutation, or soften one into the other.** The ticket forbids both directions explicitly. The risk is real because P4, if it fires, gives me a true statement (`C₃^gap > 1` under L2) that does **not** touch the ticket's relation — the relation uses chain (III), where `mg-76b2`'s constant is the right one. Reporting P4 as REFUTED would be wrong; reporting it as nothing would also be wrong. | I have a strong prior that a document whose title omits its currency is overclaiming, and a strong prior is how a correction becomes a refutation. |

---

## 4. Declared limits of this instrument, before it exists

- **B1.** `n ≤ 6` throughout. Every `n`-growth statement I make is a *direction*, never a bound, and a finite population can refute a uniform-in-`n` claim but never establish one. This is the same limit `mg-76b2` declares and I inherit it honestly rather than pretending my population is different.
- **B2.** I do not attempt `L2`, `L4`, or the `mg-200d` conjecture. This audit is about whether `mg-76b2`'s conclusions follow from its stated hypotheses, in the stated currencies.
- **B3.** Degenerate top eigenvalue (`mg-76b2` reports 163 of 5230 posets) makes "*the* dominant eigenvector" ill-defined. My monotonicity test, like `mg-76b2`'s, is **existential** over an eigenbasis of the top eigenspace and is therefore a *sufficient* test only — a `NO` from it is not a proof that no monotone dominant eigenvector exists.
- **B4.** Exact rational arithmetic for the algebra (§1 checks) and for `Φ`; floating-point for eigenvalues. Where a comparison could be decided by float noise I say so rather than reporting a clean count.
