# Attempt index — SOUND negative · actionable (mg-210d): best constant lower bound on λ_std

Per-row history for `STATE.md` § *Attempt index*, the **SOUND negative · actionable (mg-210d)** row.
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

### H1 — the retired "honest caveat", and why the row's own verdict is untouched by the retirement

**Honest caveat RETIRED (mg-88bd, audited mg-e35c — F8; see that row).**

This row used to carry *"(R) ⟹ a constant `λ_std`, which does **not** by itself give `δ` (rate ≠ the problem; the `λ_std → δ` conversion stays open)."*

That is **false as stated**: the `λ_std → δ` conversion *is* Steps 3–6 of the architecture, and backward derivation from L4 shows Steps 3–6 consume **a constant** — `1 − λ_std ≤ ε_spec`, absolute and uniform in `n` — not a limit and not a rate.

So a constant `λ_std` **is** the currency the downstream consumes, and (R) with `D ≤ ε_spec` would discharge Step 2, which is the wall.

The row's own verdict is untouched — "best constant this route proves = 0" survives, and robustly, since the route's *unconditional* output is `1 − λ_std < d·n/(n+1)` with `d ≤ 1`, i.e. `ε_spec < 1`, useless against **any** constant target `< 1` whatever its value (audit F9 — a constant-free argument, so it does not ride on the unpinned budget).
