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

> **RED · UNCONDITIONAL · witness `W*` fully CONFIRMED · DISCHARGES row 11's condition (mg-3af9, no computation; audited mg-c8c6 — OVERSTATED, but the headline is CONFIRMED and it is the strongest correct result this arc has produced: 30 CONFIRMED · 4 CONFIRMED-conditionally · 1 BROKEN as scoped, 4 dependents demoted · 1 BROKEN as labelled · 0 arithmetic errors anywhere)**

### Attempt column, verbatim

> does a **sub-linear modulus** rescue Step 6's consumption of branch (ii)? (doc: `OneThird-L4-Branch-ii-Sublinear-Modulus.md`; audit: `OneThird-L4-Branch-ii-Sublinear-Modulus-IndependentAudit.md`)

### Result column, verbatim

**⭐ THE RED, AT FULL STRENGTH AND UNCONDITIONAL — this is the item that changes program state. No strictly positive modulus rescues Step 6's stated transfer on branch (ii)** — `F(ε) = ε/4` and **every** `F(ε) = o(ε)` included. **Row 11's `Ω(ε)` condition is DISCHARGED and the conditional form is gone.** The architecture as written has a hole here, **independent of L1b**. **The witness `W*`, fully rebuilt from the poset axioms by the auditor and CONFIRMED with its parameters:** family `W` with its `B`-side chain **lengthened and decoupled from `a`** — `A = C_{a−2} ⊕ AC_2` (`a` elements), `B = C_b` (`b ≥ max(a,3)`), all `A < B` except `x<b_1`, `x<b_2` deleted; four linear extensions; `EK = 1/2` and **`Δ₁ = 1/(2a)` independently of `b`**, so `n = a+b` is free at fixed `ε` and **`Δ₁·n = (a+b)/(2a)` is UNBOUNDED** — genuinely escaping the `Δ₁·n < 2` regime mg-f825 showed `W` could never leave. Since `F(ε)·n ≥ 1` once `n ≥ 1/F(ε)`, every strictly positive modulus admits it. **The degenerate-escape clause:** the only `F` excluding `W*` is `F ≡ 0`, which reads (ii) as *"`P` is exactly `P[A] ⊕ P[B]`"* — transport then holds trivially, but **L4 is thereby a strictly stronger conjecture**, with the burden on `(i) ∨ (iii)`. Not a repair. **`(ii) ⟹ (iii)` is REFUTED at every modulus**, so the "drop (ii), keep (i)∨(iii)" repair stays unavailable. **State the limits plainly, they matter: `W*` refutes implications, not theorems — L4 itself is NOT refuted** (branch (i) holds: `p^P_{x,b_1} = 1/2`, `δ(W*) = 1/2`) **and the 1/3–2/3 conjecture is untouched.** **No `n`-dependence clause, and this is now settled in the safe direction — say it explicitly, it was the live risk two rounds ago:** an `n`-dependent budget `F(ε,n)` excludes `W*` only if it falls below **one element**, so no `n`-dependence requirement arises and **the mg-88bd row at `:132` does NOT flip** (audit claims 26–27, both CONFIRMED). **`ε_spec` untouched** — it prices Step 2's input, upstream of the failure, and no value of `ε` changes the conclusion. **C3 (*no argument can consume (ii)*) remains DECLINED** — correctly; Theorem B refutes the *stated transfer*, not every argument, and the repaired **(IB)** is still live with `W*` as a third supporting instance (not a chain, one modification from an ordinal sum, has a balanced pair). **The normalisation diagnosis, recorded *as a description of `W*`* and not as a law:** branch (ii)'s budget is `~ n` while the hypothesis `Δ₁` is normalised by `~ min(\|A\|,\|B\|)` (`:273`), and `W*` spends the ratio. **⚠️ NOW THE PART THAT DID NOT LAND AS WRITTEN. The over-reach moved: it is no longer in the headline, it is in the new general theorem introduced to explain the headline.** **(1) Theorem A, the Budget–Leakage inequality `\|S\| ≥ Δ₁·min(\|A\|,\|B\|)`, is BROKEN AS SCOPED and is recorded ONLY WITH ITS HYPOTHESIS.** **The proof defect, the counterexamples `U*` and `V*`, and the general mechanism behind all three** — [row history H1](docs/state-history/attempt-mg-3af9.md). **Recorded form: the inequality holds *for certificates that do not propagate* — i.e. under the removal reading, or under a modification reading in which the modified poset agrees with `P` off `S`.** **Do NOT call it elementary and do not reproduce the proof sketch** — an inequality recorded as elementary is an inequality that gets reused without its hypothesis, and that is the single most damaging thing this deliverable could have put into canonical state. **(2) The promotion clause — *"no balanced-cut witness can refute `F(ε) < ε/2`"* — carries the same condition, and under the transitive-closure reading it is REFUTED: there IS such a witness.** **(3) The vacuity clause** (any `o(ε)` modulus empties (ii) given a balance hypothesis or a re-normalised budget) is **CONDITIONAL on the same reading** — if certificates may propagate, a balance hypothesis does *not* empty branch (ii). **(4) `F-bal` lands as an OPEN ITEM and nothing more:** *can L3 (prefix Cheeger lemma, `:565`) be strengthened to deliver a prefix cut with `min(k,n−k) ≥ β₀n` for an absolute `β₀ > 0`, at controlled loss in `Φ`?* **(5) The §4.1 table row *"(ii) + minimality ⟹ balanced pair in `P` — REFUTED"* is BROKEN AS LABELLED and is recorded as a *route* refutation only:** `W*` **satisfies** that conclusion (`p^P_{x,b_1} = 1/2`) and is not a minimal counterexample, so it neither satisfies the hypothesis nor violates the conclusion. **⭐ (6) NEW OPEN ITEM — (RD): which reading does branch (ii) carry?** `:469–470` does **not** say whether a modification at `S` may **propagate**, and the two disambiguations are **not equivalent**: under one, **every prefix cut whose `A`-side has a unique maximal element is in branch (ii) at `\|S\| = 1` regardless of `Δ₁`** — making branch (ii) far more inclusive and (T) correspondingly *easier* to refute; under the other, `\|S\|` is bounded below by `Δ₁·min(\|A\|,\|B\|)`. **Every threshold statement in this arc depends on the answer** — mg-f825's `ε/2`, mg-3af9's Theorem A, and any future budget calibration. **Recommend the source be tightened**, alongside the (E1)/(E2) drafting flag mg-3af9 already raises (`:461–463` states `Δ₁ = ε` while `:466` states `Δ₁ ≤ ε`; mg-3af9's headline holds under **both**, so nothing above depends on that resolution). **State the direction of the risk, because it is reassuring and belongs on the record: the permissive reading STRENGTHENS mg-3af9's RED and WEAKENS its Theorem A. Nothing in the headline is at stake — only the generalisation.** **One further under-argued rider, noted not landed:** §5.4's *"`F(ε) ≤ ε`, which any useful modulus satisfies for small `ε`"* is asserted, not shown, and is **false for `F(ε) = √ε`**, a legitimate L4 modulus. **Honest net (the audit's): real progress, and more of it than the last two deliverables produced — a genuine construction reaching a regime the previous witness provably could not, converting a conditional row into an unconditional one the auditor could not break; against that, one broken universal, in the newly-general theorem rather than the headline.** *(Full per-row record — every passage relocated from this cell, verbatim: [`docs/state-history/attempt-mg-3af9.md`](docs/state-history/attempt-mg-3af9.md).)*
