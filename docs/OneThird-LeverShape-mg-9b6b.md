# What remains as a lever, once the image is exact and the density ceiling is the target? — **NOTHING ON THE DENSITY ROUTE, AND ITS LAST NAMED SURVIVOR IS RULED OUT IN BOTH OF ITS READINGS**

`mg-9b6b`, 2026-08-13, `mg-3da1`'s named successor and the fourth arc to arrive at residual `(R)`.
Instrument: [`code/lever_shape_9b6b/`](../code/lever_shape_9b6b/) — four arms, standard library only,
exact rationals on every verdict path, ~3 min, two consecutive runs byte-identical. Predictions
with the exposure disclosed per line:
[`code/lever_shape_9b6b/PREDICTIONS.md`](../code/lever_shape_9b6b/PREDICTIONS.md).

---

> ## THE VERDICT
>
> **`mg-0b96` §6 named the one thing that would change its NO — a density-to-balance bound
> `δ(P) ≥ f(d)` with `f` increasing and `f(2×10⁻²) ≥ 1/3` — and said in as many words that it is
> NOT RULED OUT THERE. It is ruled out here, in both of its readings, by two different mechanisms.**
>
> **FLAT READING** (`f` a step at `D`): `S_f ⟹ (2_D) ⟹ (1_D)`, and back through the step. It **is**
> the statement `mg-0b96` §2 closed — the escape hatch is the closed door in unconditional clothing.
> The `>` / `≥` gap between §6's wording and `(2_D)`'s is exactly one density quantum `1/C(n,2)`,
> measured rather than waved at: it is non-empty in 1 of 60 instantiated cells.
>
> **STRICT READING** (`f` strictly increasing at `D`, or any `f` with `f(D) > 1/3`): **FALSE**, at
> **63 orders** — every `n` from 3 to 66 except 65 — refuted by an **explicit** family, `⌊n/3⌋`
> copies of `{a<b, c}` in ordinal sum, which has `δ = 1/3` **exactly** at every `n` by the
> ordinal-sum lemma and density above `D_needed`. So `f` is **pinned flat at `1/3`** across the
> whole range where the boundary class lives, and the flat reading is the only survivor.
>
> **AND THE DIAL IS NOW PRICED END TO END, WHICH IS THE HALF `mg-0b96` DID NOT DO.** It priced
> `(1_D)` at one value of `D`. The family's two other ends are where the shape is:
>
> | `D` | what it is | forbids a frozen primitive up to | unreached orders |
> |---|---|---|---|
> | `1 − ⌈(n−1)/2⌉/C(n,2)` | **PROVEN** — F26, kind `U` | nothing | **0** |
> | `ε_dem·(n+1)/n ≈ 2×10⁻²` | what row 8 needs | `n = 98` | **84** |
> | `4⌊n/3⌋/(n(n−1))` | what the **data** exhibits — F23 | **every `n ≥ 4`** | **all of them** |
>
> **Value and price are the same quantity here**, because what a ceiling delivers is measured in
> orders of the conjecture — so a ceiling that delivers more **is** a stronger statement, and the
> dial says it hardest at the end the evidence points to. In orders rather than in `ε`: any `D`
> buying even ONE unreached order must be **under `2/15`**, against a proven ceiling of
> `1 − Θ(1/n)` — **7.0× at `n = 15`, widening to 7.5× at `n = 300`**, which is `mg-0b96`'s `49×`
> in a second currency.
>
> **WHY IT KEEPS LOOKING OPEN, MEASURED RATHER THAN GUESSED — AND THIS IS THE HALF WORTH READING.**
> The frontier is **real**: `G(s) = max{d : δ(P) ≤ s}` is a genuine, rising, exactly-computed
> function with no conjecture anywhere in it — and it is **EMPTY at every `s < 1/3`**. An
> instrument computing residual `(R)` therefore returns a healthy answer at every hypothesis
> **except the one row 8 consumes**, where it returns nothing at all — and *nothing at all* is what
> a ceiling of *`d ≤ anything`* looks like from inside the tool. **The route reads as open from the
> instrument side however many times it is closed from the logic side.**
>
> **ZERO SLACK, AND THE WITNESS IS ALREADY ON THE RECORD.** `F(D_needed) = 1/3` **exactly** at every
> `n = 3…8` — so the `f` §6 asks for cannot have any margin at its own threshold, and the equality
> witnesses are F23's boundary class, which the explicit family carries to 63 orders.
>
> ⚠️ **NOTHING HERE IS A MEASUREMENT ON THE FROZEN CLASS.** It is empty at every `n ≤ 8` — 16 998
> non-chain isomorphism classes at `n = 8` — re-established on this instrument's own population.
> That emptiness is this document's **subject**, not a caveat on its numbers.

---

## §1. The question, and why it is this one

`mg-3da1` closed the image line and declared its remainder in one sentence: *what remains as a
lever at all, given that the image is exact, the density conjecture on `{d > D}` is answered NO,
and `(1_D)` and `(2_D)` collapse to one statement?*

Three arcs had already converged on `d` under freezing — `mg-8b32` at the fiber level, `mg-6ff4` at
the boundary, `mg-c776`/`mg-3da1` at the image — and `mg-0b96` closed the lever itself. But
`mg-0b96` §6 left exactly one object standing, and named it precisely enough to be attacked:

> *"A result of the form `δ(P) ≥ f(d)` with `f` increasing and `f(2×10⁻²) ≥ 1/3` — a
> DENSITY-TO-BALANCE bound rather than a structure-to-balance one. Nothing of that shape appears in
> `mg-33f5`'s survey or in this corpus. **It is not ruled out here**, and it is a different object
> from everything §4 measured: every known exclusion is a statement about *structure*, and this
> would be a statement about *count*."*

**That is the whole remainder of the density route, and it is the only object in the area whose
population is not empty** — `δ ≥ f(d)` quantifies over all posets, where every other statement in
this neighbourhood quantifies over the frozen class. So it is the one that can be measured, and
this document measures it.

## §2. The flat reading is the closed door (`e1` m2)

Write `S_f` for *"every finite poset has `δ(P) ≥ f(d(P))`"*, `f` non-decreasing with `f(D) ≥ 1/3`.

**THEOREM.** `S_f ⟹ (2_D) ⟹ (1_D)`, and `(2_D) ⟹ S_f` for the step `f = (1/3)·1[d ≥ D]`.
*Proof: for `d(P) > D`, monotonicity gives `f(d(P)) ≥ f(D) ≥ 1/3`; the converse is the step read
back, and `(1_D) ⟺ (2_D)` is `mg-0b96` §2.* **Kind `U-id`.**

Two things around it are not one word:

1. **The `>` / `≥` gap is one density quantum and is measured.** §6 writes `f(2e-2) ≥ 1/3`, closing
   the threshold; `(2_D)` opens it. The two differ exactly on posets with `d = D`, i.e. by
   `1/C(n,2) → 0`. Over 60 `(n, β, D)` cells the extra counterexample set is non-empty in 1.
2. **The three predicates are computed through different comparisons and agree in all 60 cells.**
   A tautology's warrant cannot be improved by a run. What a run catches is `frozen` and `δ ≥ 1/3`
   failing to be complements in code, which every number here rests on.

**The asymmetry a run does show is in the POPULATIONS, not the verdicts.** At `β = 1/3` the `(1_D)`
hypothesis class is `0` at every `n` and every `D`; the `(2_D)` class is the entire non-chain
population — 2 044 at `n = 7`. Same statement, same counterexample set, and only one of the two
readings is something a sweep can look at. That is the shape of the trap, not a defect in either.

## §3. The strict reading is not open — it is false (`e1` m3, m4)

If `f` is strictly increasing at `D` — or if `f(D) > 1/3` at all — then `S_f` demands `δ > 1/3`
**strictly** on every poset denser than `D`. The boundary class sits at `δ = 1/3` **exactly**.

**THE WITNESS IS A CONSTRUCTION, NOT A CENSUS.** `⌊n/3⌋` copies of `{a<b, c}` in ordinal sum, chain-
padded. In an ordinal sum `L(P) = L(P₁) × L(P₂) × …` and no incomparable pair straddles a summand,
so `δ(P₁ ⊕ P₂) = max(δ(P₁), δ(P₂))`: the family has `δ = 1/3` at **every** `n`, and
`d = 4⌊n/3⌋/(n(n−1))`, which is F23's maximum. Checked against `delta_exact` at `n = 3…9` anyway,
because a lemma about posets is not a lemma about the code.

**THE WITNESS SET IS COMPUTED, AND IT IS RAGGED.** The family beats `D_needed` at 63 orders:
`n = 3…66` **except 65**. The hole is the floor's doing — `65 = 3·21+2`, so `⌊n/3⌋` sticks at 21
while `D_needed` keeps falling — and it is not an artefact of choosing this family, since F23's
form is the maximum over the whole boundary class. ⚠️ **The first draft asserted *"every `n ≤ 66`"*
and it would have been false at exactly one value.** Only computing the set says so.

**THE PRIMITIVITY OBJECTION IS REAL AND IS CONCEDED.** A minimal counterexample is primitive, so a
primitive-restricted `S_f` would serve row 8 — and every refuter above is an ordinal sum. Measured:
over every isomorphism class at `n ≤ 8` there is **exactly one** primitive member of the boundary
class, at `n = 3`. So §3 lapses under the restriction above `n = 3`. **§2 does not**: restricted to
primitives, `S_f` is `(2_D)` restricted to primitives, and `mg-0b96`'s price already ran through
primitivity. The restriction changes the class, not the price. (F23's own *"48 of the 49 are ordinal
sums"* is this observation from the other side; here it is 30 of 31 at `n ≤ 8`.)

## §4. The frontier is real, and it rises in the wrong place (`e2`)

One exhaustive table over every isomorphism class at `n ≤ 8`, read both ways.

**`G(s) = max{d : δ ≤ s}`** — the `(R)`-shaped reading — is non-decreasing and non-empty for
`s ≥ 1/3` (at `n = 8`: `1/7` at the boundary, `15/28` at `2/5`, `3/4` at `9/20`, `1` at `1/2`) and
**EMPTY in all 15 cells below `1/3`**. `G(1/3)` reproduces F23's closed form at every `n = 3…8`.
⚠️ **Through `lib6ff4`, which is the library F23 was measured with — a consistency check on this
arm, not a corroboration of F23.**

**`F(t) = min{δ : d ≥ t}`** — §6's `f`, at its largest possible — is a **10-step staircase at both
`n = 7` and `n = 8`**, running from `1/3` to `1/2`. So a density-to-balance
relation genuinely exists as unconditional information. **It is just that every value of it row 8
could consume sits at, or on the far side of, the one place where the population goes to zero.**

**The `(R)`-shaped instrument therefore has a pole exactly at the hypothesis row 8 needs**, and it
does not announce the difference: `EMPTY` and `0` are printed as different answers here for that
reason.

## §5. The dial, priced end to end (`e3`)

`(1_D)` forbids a frozen **primitive** poset at exactly the `n` with `2/n > D`, so the family maps
`D` to an initial segment of the conjecture. Read as a table, `D` from the useless end to the
useful one:

| `D` | forbids up to | orders | unreached (`n > 14`) |
|---|---|---|---|
| `1/2` | `n = 3` | 1 | 0 |
| `2/15` | `n = 14` | 12 | 0 |
| `1/10` | `n = 19` | 17 | 5 |
| `ε_dem·(n+1)/n` — **row 8** | `n = 98` | 96 | **84** |
| `1/100` | `n = 199` | 197 | 185 |
| F26's `1 − ⌈(n−1)/2⌉/C(n,2)` — **PROVEN** | **nothing** | **0** | **0** |
| F23's `4⌊n/3⌋/(n(n−1))` — **DATA** | every `n ≥ 4` | all | all |

The `84` reproduces `mg-0b96` d2's figure from the exemption side and is a control on this arm.

**WHAT THE CEILING EXEMPTS is the same question and not the same answer.** `{d ≤ D}` is the class
`(1_D)` lets off. At `D_needed` it contains **no non-chain poset below `n = 11`** and **no
primitive poset below `n = 99`** — so at every `n ≤ 10` the ceiling row 8 needs is the conjecture
verbatim, with no restriction at all.

**THE DATA END IS THE FINDING.** Feed the dial the ceiling the boundary class actually exhibits and
it forbids a frozen primitive at every `n ≥ 4` — the whole conjecture in one step, not 84 orders of
it. Reported twice: on the **measured** maxima at `n ≤ 8` alone, where it is a fact (`2/n` beats
`G(1/3)` at every `n = 4…8`; `n = 3` is the lone exception and is the boundary poset itself, where
`d = 2/3 = 2/n` exactly), and on F23's closed form, ⚠️ **where it is an extrapolation of an `FP`
result above `n = 9`**. The first is the one to quote.

## §6. Recommendation to `pm-onethird`

**Mark `(R)` closed as a lever in the residual list, which this branch does in one clause**, and
carry the reason in the form that stops a fifth arc: **not** *"a density ceiling is hard"* but
*"value and price are the same quantity on this dial, so no setting is both provable and worth an
unreached order."* `mg-0b96` §6's escape hatch is closed with it.

**What the record should carry, and it is one clause.** `STATE.md`'s `(R)` bullet still read as
live — *"reopened quantitatively by mg-88bd"* — with the pricing only in the rider 25 lines below.
That bullet is where a reader picks a route. It is corrected here and **paid for out of its own
prose**: `mg-88bd`'s *"a door recorded as the wrong shape is now the right shape with the wrong
size"* leaves this file for `docs/state-history/threads-chronology.md`, which already carries it
verbatim in two places. `CEILING.json` is banked **down** 5048 → 5047 in this commit.

**`docs/FACTS.md` deliberately gets no entry.** Every measurement here is consumed by this landing,
which fails the registry's own homelessness test — `mg-3da1`'s reason, applied to this branch.

**The one thing that would change THIS verdict, named so it can be looked for.** §3's refutation is
of `S_f` **unrestricted**, and it lapses on the primitive class above `n = 3`. A *primitive*
density-to-balance bound with strictly positive slack is therefore not refuted by anything here —
it is merely, by §2, the same statement at the same price. **The object that would escape is one
whose hypothesis is not `frozen` and whose conclusion is not a restriction of the target**, and
this document did not find one on the density route. Where else to look is `(B-cov)` and `(EQ)`,
and **neither is priced here.**

## §7. Where this could be wrong

- **`e2` m3's agreement with F23 is computed through F23's own library.** Consistency, not
  corroboration; a disagreement would impeach this directory first.
- **Every use of F23's closed form above `n = 9` is an extrapolation** of an `FP` result. §5 is
  reported both with and without it. §3's refutation above `n = 9` does **not** need it — it needs
  the family's own `δ` and `d`, which the ordinal-sum lemma gives — but §3's `n ≤ 66` boundary
  **is** arithmetic on that form.
- **Nothing here shows any `(1_D)` is FALSE.** Every one of them is true if the conjecture is.
- **The census frontier of 14** is read from `mg-0b96` d2 (Gupta, preprint; refereed 11) and is not
  re-verified. Move it and the 84 moves with it.
- **`e2`'s staircase is `FP` at `n ≤ 8`** — unconditional information about 20 000 posets, not
  about all posets. Per `STATE.md`'s standing rule, any sentence aggregating this document's
  results must say **`FP`**; only §2's collapse is `U-id` and only §3's refutation is `FP✗`-shaped.
- **§6's *"nothing on the density route"* is a claim about the route, not about row 8.** Two
  residuals stand untouched.

## §8. What was NOT done, per the ticket's own scope discipline

- **No arc was opened on `(B-cov)` or `(EQ)`** — the ticket's *"what remains as a lever"* is
  answered for the density route only.
- **The boundary was not re-measured.** F23 stands; `e2` m3 reads it.
- **No ledger row was edited**, and the twin's per-row digests do not move — `(R)` is a residual in
  *Where the threads converge*, not a ledger row, so no re-pin is owed.
- **`docs/CONCEPTS.md` gets no row.** The concepts gate is green on this branch and the conceptual
  content here — *a sub-case of the target looks exactly like a lemma until somebody prices it* —
  is `mg-0b96` §2's, already cited there.

## §9. Provenance

Instrument [`code/lever_shape_9b6b/`](../code/lever_shape_9b6b/), four arms, `sh run_all.sh`, worst
exit 0, two consecutive runs byte-identical. `lib6ff4` is imported for enumeration and `δ` and
`lib0b96` for `ε_dem`, `density` and `d_needed` — controlled primitives, re-checked here against
OEIS A000112, against brute-force enumeration of `L(P)` over all 399 non-chain classes at `n ≤ 6`,
against a five-poset hand table, and against `mg-0b96`'s own published `ε_sup` figures, because an
import whose controls live elsewhere is unchecked from here. Two planted defects, both live. Two
wrong-direction controls: the population warning (frozen class empty, `n ≤ 8`), and a **must-FIRE**
control at `β = 2/5` where the class is *not* empty — the same machinery returns real ceilings
(`2/3, 1/3, 1/2, 2/5, 4/7` at `n = 3…7`) and fires on explicit counterexamples one density quantum
below them. ⚠️ Those ceilings are **not monotone in `n`**, which was not predicted and is reported
rather than smoothed.
