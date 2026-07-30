# Attempt index — RED · UNCONDITIONAL · witness W* fully CONFIRMED (mg-3af9): does a sub-linear modulus rescue branch (ii)?

Per-row history for `STATE.md` § *Attempt index*, the **RED · UNCONDITIONAL · witness `W*` fully CONFIRMED · DISCHARGES row 11's condition (mg-3af9)** row.
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

### H1 — the arguments under Theorem A, the promotion clause and the §4.1 row — the counterexamples `U*` and `V*`, and the general mechanism

Its proof silently assumes a certificate's modifications **cannot propagate** — and **transitivity propagates them**.

It is false **by an unbounded factor**: `U*` = two `N`-chains with no cross relations (`Δ₁ = 1/2`, `Δ₁·m = N/2`) becomes an exact ordinal sum by modifying the **single** element `a_N`, so `\|S\| = 1`; already a counterexample at `N = 3`, on six elements.

General mechanism, one line: **if `P[A]` has a unique maximal element `z`, then `S = {z}` is a one-element branch-(ii) certificate for *any* `Δ₁` whatsoever.**

`W`/`W*` are immune only because their `A`-side has **two** maximal elements — which is exactly why the incidental locality of their certificates was invisible.

(Remark 3.1's relation-counting variant `\|S\| ≥ (max_σ K)²` inherits the same defect — `U*(3)` needs **one** added relation against a claimed `≥ 9`.)

The auditor built it: **`V*(N)`**, `A = {u,v} ∪ C_{N−2}` with `u,v < z_1` and `u ∥ v`, `B = C_N`, the single cross `v < b_1`; `β = 1/2` **exactly**, its only side pair balanced at `1/2` in `P[A]` and at `p^P_{uv} = (N−1)/(3N−2) < 1/3` in `P`, one-element certificate at the unique maximum `z_{N−2}`, `Δ₁ = (3N−4)/(2(3N−2)) → 1/2` — admitted by moduli far below `ε/2` (e.g. `F(ε) = ε/100` admits `V*(100)`).

**Hand-verified at `N = 3` by enumerating all 14 linear extensions** (`EK = 15/14`, `Δ₁ = 5/14`, `p_{uv} = 2/7`), matching the closed form at general `N`.

**The deliverable's claim that better-balanced witnesses cannot exist is struck in every form.**

So the two readings give **different mathematics**, and the document picked neither.

The deliverable's billing of it as *the single question on which the value of a sub-linear modulus now turns* is **dropped** — it is conditional on the broken reading, and it is about a route that terminates in an already-refuted disjunct (run forward: `F-bal` ⟹ `o(ε)` empties (ii) ⟹ burden on `(i) ∨ (iii)` ⟹ (iii)-standalone is already refuted at every `ε`, modulus-free).

What it refutes is the route — *"the pair minimality supplies is a side pair, and side pairs need not transport"* — which is (T) again.

The document violated its own motto two rows above the motto.

## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

(Exactly quantified, per the audit: the universal is over every `F` **strictly positive on the sequence `{1/(2a) : a ≥ 3}`**; `ε` ranges over that discrete sequence accumulating at `0`, which for any monotone `F` is no restriction.

The inference runs `ε` **first**, then `n` free — the reverse of mg-63e3's, and valid.)

**One** modified element (`S = {x}`, confirmed under *both* the modification and the removal reading); the sides' **only** incomparable pair balanced at exactly `1/2` in `P[A]` and at **`1/4`** in `P`; the `a = 4, b = 28` instance (`n = 32`, `Δ₁ = 1/8`, `Δ₁·n = 4`) verified element by element.

**The escape is constructed, not asserted** — the auditor attacked it four ways (`Δ₁` secretly `b`-dependent · the element-vs-relation counting unit · `δ(W*) = 1/2` so out of scope · the cut is degenerate `β → 0`) and **all four fail**.

**CREDIT, and it is load-bearing for how the next deliverable is read: §5.1–5.2's self-audit is the first time in this arc a deliverable correctly diagnosed and avoided its predecessor's quantifier defect** — the auditor tried to break it and could not.

Its restraint on the `n`-dependence clause and on C3 was right, and it **declined to claim the vacuity route as a repair** when that would have been easy.

**Its two honest halves are sound and stay: *"this is a change to L4, not a reading of it"* and *"Steps 2–5 do not deliver it"*** (no step constrains `k`; `Φ_P^* = min_{0<\|A\|≤n/2} Φ_P(A)` at `:235–237` is *defined* by minimisation over all cut sizes, so conductance permits unbalanced cuts; L3 says nothing about balance — audit claim 31 CONFIRMED).

**Constraint compliance CLEAN on both documents** (verified at the commit: `e2ccee6` adds exactly one `.md`): zero scripts, zero datasets, zero enumerations; the audit is likewise computation-free, every count a hand count on posets with at most 20 linear extensions.
