# Attempt index — OVERSTATED · core CONFIRMED-conditionally · RE-SHAPES (R) (mg-88bd): the operative λ_std form

Per-row history for `STATE.md` § *Attempt index*, the **OVERSTATED · core CONFIRMED-conditionally · RE-SHAPES (R) (mg-88bd)** row.
Split out of the ledger cell by mg-34bf, 2026-07-30.

Every passage below was **moved verbatim** out of that cell. Nothing was rewritten,
condensed, summarised or dropped, and no citation was changed. The row now asserts current
state and points here; `code/state_restructure_34bf/verify_relocation.py` checks, clause by
clause against the pre-restructure `STATE.md`, that every clause of the old cell is still
present in the row or in this file. See [`README.md`](README.md) for the convention.

## Corrections, retractions, supersessions and mechanism notes

*Why this section exists: a ledger row must not be able to contain a claim and its own
retraction. The row states what is true now; what it used to say, what was struck, and why,
is here. Sections are numbered `H1`, `H2`, … and the row cites them by number.*

### H1 — audit F1's steelman, and F4's "the source's THIRD form, not a fourth"

(Audit F1: §3.3 refutes a steelman for `n`-dependence, but not the strongest one — the leakage-*count* objection `εk = O(1)` lives inside branch (iii), the branch Step 6 actually consumes, and §3.3's "the only route … is branch (ii)" is a false universal.)

**It is the source's THIRD form, not a fourth** (audit F4): Step 2's own form, applied to the single hypothetical minimal counterexample, where there is no quantifier over `n` to be missing.

### H2 — branch (iii) — arithmetic CONFIRMED, framing OVERSTATED (audit F2)

**Branch (iii) — arithmetic CONFIRMED, framing OVERSTATED** (audit F2).

But the source's own L4 in the open-lemma list (`:567–569`, "**preserving** a balanced pair from one side") and its own prose (`:476–479`, "the thin interface **cannot destroy** all such pairs") already read as the repaired form — so this is an **internal drafting inconsistency in the source, not a defect in the architecture's intent**; the repair (restate (iii) as exact preservation in `[1/3,2/3]`, already the predicate mg-3ce3 tested green) is worth landing, "newly-found architectural defect" is not.

### H3 — F3's struck second half, "and there is no repair available"

**F3's second half — *"and there is no repair available"* — is now OVERSTATED and is STRUCK (mg-63e3, audited mg-f825 — see that row):** it named a property of the *branch* on evidence about the branch's *statement* only, and it never ran the ordinal-sum route; a candidate repair **(IB)** exists (repaired form — see that row).

### H4 — why §7.2 did not settle satisfiability; THE FALSE LOSS (audit F8/F9)

**Why the deliverable's own §7.2 did not settle this:** it shows every antichain prefix has `Δ₁ ≥ 1/2`, which excludes vacuity-**by-universality**; the open question was vacuity-**by-emptiness**, and §7.2 does not touch that.

**THE FALSE LOSS — "the weakening buys the mg-210d route nothing" is OVERSTATED** (audit F8), and the consequence is landed at the mg-210d row above and in *Second clean residual* below: the weakening converts Residual **(R)** from **categorically** insufficient to **quantitatively** insufficient, because under this document's own verdict **a constant `λ_std` IS the currency the downstream consumes** — *a door recorded as the wrong shape is now the right shape with the wrong size*.

The route's *conclusion* survives and more robustly than argued (F9: the unconditional output is `ε_spec < 1`, useless at any constant target — no numeric budget needed).

### H5 — the two BROKEN label/attribution derivations, F5 and F6

**Two BROKEN derivations of labels/attributions; neither changes a mathematical statement.**

**F5** — §6.4's "L4 usable" budget row is BROKEN as labelled and it is the numeric spine of §7: under the *repaired* (iii) the modulus `F` does not appear in the statement at all, so there is no `F(ε_leak) < slack` to calibrate; under the *stated* (iii) the document's own `P_0` proves the slack can be `0`, so no `F > 0` satisfies it; and the row's `1/6` is a *centred* pair's **maximum** used as a guarantee.

Two tools merged into one — exactly the Appendix A step-5 object check.

## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

The source writes `ε` for the spectral `λ_std ≥ 1−ε` and for the leakage `Δ₁ = ε` three lines apart in the architecture; Cheeger relates them by `ε_spec ≤ ε_leak²/2`.

The arithmetic: (iii) as worded gives `p^P_{xy} ∈ [1/3 − F, 2/3 + F]`, consistent with `δ(P) < 1/3`, so no contradiction for **any** `F > 0`; and `P_0 = {a<b} ⊔ {c}` has `δ = 1/3` with **zero slack**, so minimality cannot be strengthened to supply it.

L4's conclusion is a disjunction; (ii) delivers a structural statement and no balanced pair, so if (ii) is the branch that holds for some `P` in the hypothesis class, Step 6 has nothing to consume — unlike (iii).

Implied by the deliverable's own §3.3 sentence and never drawn.

`W_n = C_n ⊔ C_1` — a chain plus one free point, the corpus's own `W_m`: **primitive** (incomparability graph is the star `K_{1,n}`, connected, so `λ_std < 1` strictly, not the degenerate case), and **every** prefix is thin at the same rate — `z` lands uniformly in `n+1` slots, so `E\|A∖σ(A)\| = k/(n+1)` and `Φ = Δ₁ = 1/(n+1)` **independent of `k`**, giving `1 − λ_std ≤ 2/(n+1)`.

So `W_n` satisfies `1 − λ_std ≤ ε_spec` once `n+1 ≥ 2/ε_spec`, while carrying genuinely non-trivial LE geometry (`E[inv_e] = Θ(n)`).

Corroborated independently by mg-3ce3's `8AC ⊕ 8AC`-minus-one-cross witness (`n=16`, `Δ₁ = 0.0019`, `λ_std = 0.996`).

mg-210d Thm 2.4 builds it from the **unconditional** Buser cut bound with **indicator** vectors `1_A − a·1` (a different vector per cut) over all `n−1` prefix cuts, relaxed by a mediant inequality; `ũ` (`tex:400–424`) is a separate tool that *does* consume `Pr[j≺i] < 1/3` once and yields `λ_std > 1/3`.

**Free audit by-products, recorded not acted on:** primitivity (`d ≥ 2/n`) sharpens "the master bound cannot deliver the target for any non-chain poset on `n ≤ 100`" to **`n ≤ 2/ε_spec`** — `10⁴` at the deliverable's budget, `10²` at the repaired one — which is the relevant class since minimal counterexamples are primitive; and the source's own `ũ`, priced for the first time, sharpens "given (B), the master bound yields `1 − λ_std = O(1/n)`" to **`O(1/n²)`** (both bounds still antichain-sharp, so no redirect changes).

---

## Full cell text before the mg-ea0e relocation (2026-08-06)

Appended by **mg-ea0e**, 2026-08-06, on pm-onethird's relocation spec, which finishes here
the convention mg-34bf started: **relocation, not deletion**.  The `STATE.md` row now
carries its status label, its own opening sentence verbatim, and a link to this file.

**Everything below is that ledger cell's ENTIRE text as it stood immediately before that
edit** — all three columns, character for character, from `STATE.md` at `78ae4d9`.  Nothing
was rewritten, condensed, summarised or dropped.  Passages mg-34bf had already relocated
appear above under `H1`…; they recur below only because this is the whole cell, and the
sentence the row retained appears below as well, in its place.

### Status-label column, verbatim

> **OVERSTATED · core CONFIRMED-conditionally · RE-SHAPES (R) (mg-88bd, no computation; audited mg-e35c — 0 BROKEN mathematics, 2 BROKEN label/attribution derivations)**

### Attempt column, verbatim

> the **operative `λ_std` form**, by backward derivation from L4 (doc: `OneThird-lambda-std-Operative-Form.md`; audit: `OneThird-lambda-std-Operative-Form-IndependentAudit.md`)

### Result column, verbatim

**The form, and it is CONDITIONAL — record the condition, not just the form.** The architecture consumes `1 − λ_std ≤ ε_spec` for an **explicit absolute constant, uniform in `n`** (in inversion terms **(LIB-const)** `E[inv_e] ≤ (ε_spec/6)(n²−1)`, equivalently `E[footrule] ≤ ε_spec·E_unif[footrule]` — a constant-factor improvement on the uniform-random value). **CONFIRMED — but conditionally, and the condition is heavier than the deliverable conveys:** this is what the *stated* architecture consumes, and **L4-as-stated (row 11, OPEN/AMBER) is itself the thing whose provability at an `n`-free modulus is in doubt.** The form is *not* settled with the only open question downstream; if L4 needs an `n`-dependent modulus the answer flips. **Two audit corrections to the deliverable's own framing** — [row history H1](docs/state-history/attempt-mg-88bd.md). **The genuine news is about the corpus's two asymptotic renderings** — this document's limit (`λ_std → 1`) and mg-7ae7's rate (`1 − λ_std ≤ C/(γn)`) are **both genuinely stronger than the architecture needs**, and mg-7ae7's `1/(γn)` is inherited from Theorem E's *output shape*, not demanded by any consumer. **The durable wins — this is the substance:** (1) **the `ε_spec` / `ε_leak` notation collision, and the square between them.** Real, verified, and it is what actually **dissolves the limit-vs-rate confusion**. (2) **§4.3: prefix-capture as literally worded is too weak to use** — it yields a constant *floor*, not a small gap, which makes L3's *statement* an open item and not merely its constant. (3) **The `Φ → Δ₁` conversion is the identity, not a bound — CONFIRMED and STRONGER than stated** (audit F7): the source defines `Φ_P` *only* on `0 < \|A\| ≤ n/2`, so `\|A\| ≤ n/2` is not a hypothesis restricting the identity, it is `Φ`'s whole domain — the two symbols are the same function everywhere both are defined. Hence **Steps 4 and 5 state the same inequality about the same number: Step 5 adds no bound, it re-reads Step 4.** **Branch (iii): arithmetic CONFIRMED, framing OVERSTATED (audit F2); the current status of (iii) is at ledger row 11 and at the mg-63e3 row below** — [row history H2](docs/state-history/attempt-mg-88bd.md). **The larger Step-6 gap, which the deliverable missed and which was written down nowhere (audit F3): branch (ii) is unconsumed.** **F3's second half — *"and there is no repair available"* — is STRUCK (mg-63e3, audited mg-f825; see that row)** — [row history H3](docs/state-history/attempt-mg-88bd.md). **The *reason* clause is CONFIRMED and now proven far more strongly** — the transfer's failure is quantitative and survives `ε → 0`, **for every strictly positive modulus** (mg-63e3/mg-f825 proved this at `F(ε) = Ω(ε)`; mg-3af9, audited mg-c8c6, **discharged the condition** — sub-linear moduli included). **So as literally stated, L4 closes Step 6 only via the trivial branch (i)**, which *is* the conclusion. This is the more consequential of the two. **Satisfiability: CONFIRMED non-trivially, with a hand witness the deliverable does not have** (audit §4). **THE FALSE LOSS — *"the weakening buys the mg-210d route nothing"* is OVERSTATED (audit F8/F9); its live consequence is carried at the mg-210d row above and in *Second clean residual* below** — [row history H4](docs/state-history/attempt-mg-88bd.md). **Two BROKEN derivations of labels/attributions — F5 (§6.4's budget row) and F6 (the master bound's attribution); neither changes a mathematical statement. Their live consequences:** — [row history H5](docs/state-history/attempt-mg-88bd.md). The consequence is one-directional: the right calibration under the repair is mg-3ce3's first RED, and the probe reports **0 RED / 6681 up to `ε = 0.20`**, supporting `ε_leak ≈ 0.20` hence `ε_spec ≲ 2×10⁻²` — **100× larger than the deliverable's `2×10⁻⁴`, i.e. the error inflates the pessimism.** So **do not carry `2×10⁻⁴` or the `n ≈ 10⁵` crossover as flat text**: the budget is unpinned by ~2 orders of magnitude, the pessimistic reading is the smaller one, and under the repair the crossover falls to `n ≈ 900` — inside the range an unknown minimal counterexample could live. **F6** — the master bound is **misattributed**: it is *not* the source's single test vector `ũ` and it does *not* consume freezing. Substance CONFIRMED (antichain-sharpness is a limit of the tool, not of the problem — true of the correct tool too), attribution BROKEN, the `PROVEN` label unearned. **Constraint compliance CLEAN** on both documents: one `.md` each, no scripts, no data, no enumeration. **Honest net (the audit's): a genuine notation catch plus a re-pricing — not new mathematics.** *(Full per-row record — every passage relocated from this cell, verbatim: [`docs/state-history/attempt-mg-88bd.md`](docs/state-history/attempt-mg-88bd.md).)*
