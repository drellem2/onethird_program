# `code/l2_audit_29fe/` — mg-29fe's instrument for the INDEPENDENT AUDIT of mg-28ff

**Written from the corpus's definitions, not from the parent's code.** `lib29fe.py` was
written against the definitions in `docs/OneThird-C3-PrefixCapture-mg-76b2.md` (Lemma 2.1,
Lemma 3.1, §4). `code/l2_conditionality_28ff/lib28ff.py` was **not opened until every
number below had already been produced** — `PREDICTIONS.md` E5 named that as the guard I
was most likely to break, and the only thing that kept it was writing the lib first.

## Run

```sh
python3.11 selftest29fe.py            # 26 arms, all FORCED
python3.11 s1_truth_and_sweep.py      # items 1 and 2
python3.11 s2_footrule.py             # route (F), and the f* precision question
python3.11 s3_counterfactual.py       # item 4 — the 2x2 on the two added steps
python3.11 s4_theorem_and_quantifier.py  # item 5, and the falsification arms
```

`python3.11` specifically: it is the interpreter on this machine with `numpy`, which only
`selftest29fe.py` A8 needs. Nothing on a verdict path uses it.

## What is exact here that was not exact in the parent

| quantity | mg-28ff | mg-29fe |
|---|---|---|
| `1 − λ_std` | exact PSD bisection, 60 steps | exact PSD bisection, 34 steps |
| `Φ*_pref`, `E[D_F]`, `leak` | exact | exact |
| `c_true` | exact bracket, 24 steps over `[0,2]` | exact, reproduces to 6 d.p. |
| `f*` | exact bracket, **20 steps over `[0,4]`** (width `3.8e-6`) | exact, width `1.8e-12` |
| **`μ_pref`** | **FLOAT** support enumeration + float generalized eigenproblem; extremal direction labelled a MEASUREMENT (§6, §10) | **EXACT** — bisection on an exact **copositivity** test of `Q − tN` over the monotone cone |
| **the L2 census** | **FLOAT, tol `1e-9`** (`out_b5_trend.txt`) | **EXACT** — `L2's first disjunct fails ⟺ ρ > 1` |
| PSD decision | Faddeev–LeVerrier | brute-force **principal minors**, plus an `O(n³)` symmetric-elimination fast path asserted equal to it on every matrix the sweep tests (A3j) |

The PSD algorithm is deliberately different. mg-28ff's E3 records a **sign error** in its
Faddeev–LeVerrier; an auditor who reuses that algorithm inherits its failure mode, so this
instrument decides PSD by summing principal minors, where there is no sign convention to
get wrong.

`μ_pref` being exact is the one place this instrument is strictly stronger than its parent,
and it is what makes §4's counterfactual a **theorem about the population** rather than a
float measurement.

## Defects of my own, caught by controls, kept rather than deleted

**D1 — a negative control that could never have fired.** `selftest` A6c was first written
as *"add a constant to `ψ` and `Q_kk = leak(A_k)` must break"*. It does not break, and it
**cannot**: the energy form is shift-invariant, so a constant shift changes `Q` by exactly
nothing. I had built a mutation test whose mutation is in the kernel of the thing it
mutates. It is replaced by a **single-coordinate** perturbation, which does fire, and the
dead form is **kept as arm A6c0** asserting the non-effect — so the reason the first control
was worthless is now itself a live assertion and cannot be re-introduced silently.
This is the third instrument in this lineage to file the same shape of defect
(mg-28ff E4, mg-81ff s0 C, mg-9461 s0 C).

**D2 — a finding I nearly published that was my own misreading.** I had `§4.2`'s `n = 7`
row (`40`) scored as contradicting `§0`/`§10`'s *"a deterministic sample of 90–200 posets"*,
i.e. a sample size outside its own stated range. It is **not** a defect: that column is the
**primitive count**, and `40` is the number of primitive members of a 90-poset sample
(`b2_census.py:138` uses `sample_posets(7, 90)`, while `b1`/`b5` use `sample_posets(7, 200)`
and get `106`). My own `PREDICTIONS.md` guard — *"I must quote the sentence and the sample
size from the same document before scoring"* — is the only reason this did not ship. What
survives is a much smaller note: `§4.2`'s `n = 7` population is a **different** sample from
`§4.1`'s and `§4.3`'s, and the document does not say so.

**D3 — the `f*` discrepancy was mine to explain, not the parent's to answer.** My `f*` came
out `5e-6` below the document's at `n = 5, 6` and I flagged it to `pm-onethird` as unresolved
rather than as a finding. Cause, found afterwards: the parent's `f*` bisection is `20` steps
over `[0,4]`, a bracket `3.8e-6` wide, and the document prints **six** decimals from an
instrument that printed **five**. The document's figures are the **upper** bracket ends —
i.e. conservative, erring toward over-stating the route's constant. Nothing is wrong with
the conclusion; the sixth decimal is simply not supported by the measurement.

**D4 — I shipped the very defect I was auditing.** `s3` implemented the hypothesis (M♯)
exactly as mg-28ff's §2 and §4.2 *state* it — the single expression
`μ_pref(2Δ_P − μ_pref)/(2(1−λ_std))` — and therefore dropped the **second branch** that
mg-28ff's own §2 *theorem* carries (`Δ_P²` when `R(g) > Δ_P`). It surfaced because my
`c♯(2) = 0.000000` disagreed with the parent's published `0.125000`, and the parent is right:
at `n = 2`, `μ_pref = 1 > Δ_P = 1/2`, so the second case applies. Fixed in `s5_branch.py`,
which re-runs the whole sweep branched.

The reason this is worth keeping rather than quietly fixing: **the remedy carried the defect
it remedies.** I was auditing a mismatch between a theorem and the hypothesis derived from
it, and I reproduced that mismatch in my own code by reading the hypothesis instead of the
theorem — which is precisely how it got into the document. It also means the finding in
§6.1 of the audit is one I could only have found by being wrong in the same way first, and
that the parent's *instrument* was correct throughout: only its *prose* drops the branch.

## Not done

* No `n = 8`. No exhaustive `n = 7` — my `n = 7` work is a **deterministic sample** and every
  figure from it says so at its own use site.
* I did not re-derive L2, `ε₀`, L4, or any chain constant, and I did not open `libA94.py`,
  `lib76b2.py`, or `lib3969.py`.
* The `1032` vs `1037` discrepancy mg-28ff §5 records is left exactly where it left it.
* I edited no document but my own; `docs/OneThird-L2-Conditionality-mg-29fe-IndependentAudit.md`
  proposes text for mg-28ff's document and does not land it.
