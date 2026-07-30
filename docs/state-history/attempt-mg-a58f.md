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
