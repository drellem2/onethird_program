# Attempt index — RED-for-lever · AMBER-redirect (mg-a58f): the (B-bias) O(1) locality lemma

Per-row history for `STATE.md` § *Attempt index*, the **RED-for-lever · AMBER-redirect · CORRECTS MERGED WORK (mg-a58f)** row.
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

### H1 — the first three of the four corrections (this document's § The single lemma to prove, ledger row 8, mg-dbd1 §2.1, the (A)+(B) route's advertised advantage)

**Four corrections:** (1) **this document's § *The single lemma to prove* line — "the two faces are logically independent" — is false in one direction**; (B) is the *stronger* face.

**Ledger row 8's `⟺ LIB ⟺ (B)` was the same error, and the two contradicted each other**; both are reconciled in this pass to the one-way implication, with the reverse marked UNPROVEN (mg-d112 §6.1: annotating one and leaving the other standing would have left the inconsistency in place).

(2) mg-dbd1 §2.1's "(B) is weaker than LIB" is **REFUTED**.

(3) The (A)+(B) route's advertised advantage — "tolerating quadratic `E[inv_e]`" (mg-dbd1 §0/§5, mg-8201 §2) — is **vacuous**: (B) is unsatisfiable when `E[inv_e] = ω(n)`, so the stated reason for abandoning LIB does not hold.

### H2 — the limit-vs-rate scoping question, and its answer

**Scoping question flagged, not picked — since ANSWERED (mg-88bd, audited mg-e35c; see that row):** this document states the conclusion as a limit, mg-7ae7 states the operative target as the rate `1−λ_std ≤ C/(γn)`; those differ by a factor `n` in the inversion requirement and pm-onethird owned pinning which one L4 consumes (extract mailed under mg-1fdb).

**Answer: neither.**

Backward derivation from L4 fixes the operative requirement as `1 − λ_std ≤ ε_spec` for an absolute constant uniform in `n` — the source's own Step-2 form — so **both of the corpus's asymptotic renderings, the limit here and mg-7ae7's rate, are genuinely stronger than the architecture needs** (conditionally on L4-as-stated, which is itself OPEN/AMBER).

All three arcs that recommended it (mg-dbd1 §5.1, mg-dcae §7.2, mg-0ed7 §7.5) mis-priced it.

## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

`Σ_x m_x = 2E[inv_e]` identically, so `max_x m_x ≤ C` ⟹ `E[inv_e] ≤ Cn/2` = **LIB** (γ-free) ⟹ (mg-210d master bound) `1 − λ_std ≤ 3Cn/(n²−1) → 0` = L1b's conclusion.

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

> **RED-for-lever · AMBER-redirect · CORRECTS MERGED WORK (mg-a58f; audited mg-d112 — CONFIRMED, 40 ledger rows re-derived, 0 BROKEN)**

### Attempt column, verbatim

> (B-bias) `O(1)` locality lemma (doc: `OneThird-Bbias-Locality-Lemma.md`; audit: `OneThird-Bbias-Locality-Lemma-IndependentAudit.md`)

### Result column, verbatim

**⚠️ Largest item first — (B) IMPLIES LIB (Thm 3.3, elementary, unconditional):** `E[inv_e] ≤ E[Σ\|disp\|] ≤ √(n·E[Σdisp²])` by the lower half of Diaconis–Graham + Cauchy–Schwarz, so (B) with constant `C` forces `E[inv_e] ≤ Cn`. (The audit verified this holds under **either** statement of (B) — the inversion form used in mg-dbd1/mg-8201 *and* the footrule form this document uses.) **Four corrections landed against prior text; the fourth is current state and stays here** — [row history H1](docs/state-history/attempt-mg-a58f.md). (4) Given (B), the mg-210d master bound alone yields `1−λ_std = O(1/n)`, so **(A) SPREAD and `Λ = O(1)` are off the critical path** (both still true; (F2) simply postdates the certificate). **Net: LIB is the weakest of the *three* sufficient conditions on the table** — the set being `{locality, (B), LIB}` — **and alone suffices; both objects the (A)+(B) route has attacked since mg-8201 — (B) and the locality lemma — are strictly-at-least-as-strong surrogates for it.** *(Restricted per mg-d112 §4.1: this does **not** extend to everything the program has attacked since mg-8201 — mg-4a86's standard-dominance/Wilson comparison route, mg-210d's (R), and the entropy probes are **not** LIB surrogates. The unrestricted universal was false and is not recorded.)* And `λ_std → 1` as stated here needs only **(LIB-weak)** `E[inv_e] = o(n²)` — never attacked by any arc. **The limit-vs-rate scoping question this row raised is ANSWERED (mg-88bd, audited mg-e35c) at the mg-88bd row below** — [row history H2](docs/state-history/attempt-mg-a58f.md). **On the ticket's own target: the lemma implies the wall.** So it is **not** an elementary reserve route below the crux; it is at least as strong as the crux, and it silently re-imposes the `E[inv_e] = O(n)` requirement mg-8201 retired as "structurally unnecessary". **The lossy step is located exactly:** both derivations bound the per-element **bias** `b_x = \|E[pos_σ x] − rank_e x\|` by the per-element **inversion mass** `m_x` *before* taking the max, discarding the cancellation between `e`-above and `e`-below inversion mass — worth a factor `n` (witness `C_m ⊔ C_1`: `max b_x ≤ 1`, `max m_x = Θ(n)`, `E[inv_e] = Θ(n)`, all exact by hand). **Redirect — (EQ):** `max_x \|E[pos_σ(x)] − rank_e(x)\| = O(1)`. Proven here: (EQ) ⟹ (B-bias) (unconditionally); (EQ) ⟹ mg-dbd1 §3.4's auxiliary `Λ = O(1)`; (EQ) is exactly the negation *at every element* of mg-dbd1 §3.1's named (B)-falsifier (which was stated only at the `e`-min, where `b_x = m_x`); (EQ) is strictly weaker than the locality lemma. Leaves **(B-cov)** as the sole residual on the certificate route — the same edge this document already names, reached without over-shooting. Also new: `m_x = E\|σ_{<x} Δ D_x\|` (per-element leak identity); conditional-uniformity window bound `locality ⟹ E[W_x] = O(1)`; the 3-element system is provably inert (satisfied by the two-atom law with `m ≡ ε`). Kills none of the three routes to (B-cov); withdraws the side-door three arcs recommended. Zero computation. **Audit additions (mg-d112, free):** (EQ) ⟹ `E[L_j] ≤ C₀·min(j, n−j)` per prefix cut — a genuine consequence the deliverable did not record, and it shows (EQ) does **not** deliver LIB by the natural analogue of Thms 3.2/3.3 (it gives only the trivial `Θ(n²)`), so the AMBER redirect survives the deliverable's own re-pricing check. §7.3's insufficiency claim downgraded PROVEN → **PLAUSIBLE** (rests on the `Θ(√m)` HEURISTIC rate); nil consequence. *(Full per-row record — every passage relocated from this cell, verbatim: [`docs/state-history/attempt-mg-a58f.md`](docs/state-history/attempt-mg-a58f.md).)*
