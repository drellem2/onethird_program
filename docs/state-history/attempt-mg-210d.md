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

> **SOUND negative · actionable (mg-210d)**

### Attempt column, verbatim

> best *constant* lower bound on `λ_std`, primitive/frozen — ISOLATED elementary probe (doc: `probe-lambda-constant-bound.md`)

### Result column, verbatim

**Best constant this route proves = `0`.** Master bound (re-derived from scratch, sharp): `1−λ_std ≤ 3·E[footrule]/(n²−1) ≤ 6·E[inv]/(n²−1)`, equality at the antichain. Frozen ⟹ `λ_std > 1 − d·n/(n+1)` (`d = m/C(n,2)` = incomparability density), but `d ≤ 1` degenerates it to `1/(n+1)` — positive, **not constant**. **Connectivity is wrong-signed:** primitivity gives `m ≥ n−1` — a *lower* bound on the pair count — which *degrades* the bound `O(1/n)`; a non-degeneracy hypothesis, not a quantitative lever. **Sole missing ingredient = Residual (R): is there a constant `D < 1` with density `d(P) ≤ D` on every *frozen* poset?** ⟹ `λ_std > 1 − D` immediately. (R) open: entropy + inversion-counting attacks both fail; pinning-cost heuristic supports; antichain (`d=1`) is *not* frozen, so freezing does spend density. **Free by-product (= our 3-cycle anchor, independently re-derived): frozen ⟹ the majority relation is automatically a linear extension**, and `1/3` is exactly the threshold — the distinguished order is *canonical*, not chosen. **The "honest caveat" this row used to carry is RETIRED (mg-88bd, audited mg-e35c — F8; see that row), and the verdict *"best constant this route proves = 0"* is untouched by the retirement** — [row history H1](docs/state-history/attempt-mg-210d.md). **Do not over-correct: (R) is not thereby sufficient.** Its insufficiency moves from **categorical** ("even if proven, it is the wrong kind of object") to **quantitative** ("it is the right kind of object, and the open question is whether the constant it delivers is good enough") — `D ≤ ε_spec`, which for a *primitive* poset (`d ≥ 2/n`) additionally forces `n ≥ 2/ε_spec`. **A door recorded as the wrong shape is now the right shape with the wrong size:** (R) is reopened as a live quantitative question, not closed. All four load-bearing claims hand-verified; scripts benign (n≤7, no dataset). *(Full per-row record — every passage relocated from this cell, verbatim: [`docs/state-history/attempt-mg-210d.md`](docs/state-history/attempt-mg-210d.md).)*
