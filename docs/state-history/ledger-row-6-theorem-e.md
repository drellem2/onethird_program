# Full ledger row 6 — Theorem E

Per-row history for `STATE.md` § *Full ledger*, row 6.
Split out of the ledger cell by **mg-bdb0, 2026-08-13 — landing A of the two-landing
protocol** (`code/rendered_twin_pin_9bc2/twin_pin.py` section 8, shipped by mg-1344).

Every passage below was **moved verbatim** out of that cell: each is a literal slice of the
cell as it stood at `092a508`, and the row keeps the rest of that cell, also verbatim, with
only the punctuation seams a removal leaves. Nothing was rewritten, condensed, summarised or
dropped, and no citation was changed. Retained text + the passages below reconstruct the old
cell character for character. The row now asserts current state and points here. See
[`README.md`](README.md) for the convention and for which passages relocate.

## Corrections, retractions, supersessions and mechanism notes

*Why this section exists: a ledger row must not be able to contain a claim and its own
retraction. The row states what is true now; what it used to say, what was struck, and why,
is here. Sections are numbered `H1`, `H2`, … and the row cites them by number.*

### H1 — the PROVENANCE REPAIR (mg-957a), and what the defect actually was

*In the row it stood between “…inimal counterexample ⟹ low-conductance BK cut. ” and “The corpus's only proof of this row is [`one_thi…”:*

**PROVENANCE REPAIRED, mg-957a — the "any" was CORRECT MATHEMATICS CARRIED ON AN UNRECORDED GENERALISATION, and the ledger's *warrant* was the defect, not its *claim*.**

### H2 — mg-e35c's F12, ruled out of scope, and how "any" stood for months

*In the row it stood between “…ounterexample on `n ≥ 2` elements…"* (`:57–62`).” and “ **Settled by reading the source rather than by …”:*

mg-e35c's auditor raised the discrepancy as **F12**, it was ruled out of scope, and it never landed — so this cell carried **"any"** against a width-3 source for months.

## Supporting record

*`docs/state-history/README.md`'s clause (c): a derivation, construction, enumeration or
numeric evidence supporting a claim the row still states. The claim stayed in the row; the
working is here.*

### S1 — where the width-3 hypothesis enters, and the four proofs that do not consume it

*In the row it stood between “…: the width-3 hypothesis is PRESENT AND INERT.**” and “ **The general statement, and what proves it: de…”:*

It enters only as the file's blanket Setup hypothesis (`:21` — a file whose *own* main theorem is the **width-3** conjecture, so every statement in it inherits the phrase) and is restated at `:60`, `:158`, `:196`, `:332`. **No step of any of the four proofs consumes it:** Lemma `dirichlet-conductance` (`:122–152`) is a general reversible-chain inequality; Lemma `indec-incompairs` (`:167–195`) uses only indecomposability, via an ordinal-sum split; Lemma `frozen-pair-existence` (`:196–270`) uses only (1) at most `n−1` adjacent positions per `σ`, (2) the `γ`-counterexample hypothesis, (3) `I(P) ≥ n/2` from the previous lemma, (4) min ≤ ratio-of-sums; the theorem's own proof (`:330–370`) adds only `p_xy ≥ γ`.
