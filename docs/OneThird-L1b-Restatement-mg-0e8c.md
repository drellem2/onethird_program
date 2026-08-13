# OneThird — DANIEL IS RIGHT: ROW 8 AS STATED IS DISCHARGED, AND ITS SPECTRAL HALF IS VACUOUS

*mg-0e8c, 2026-08-13. Filed on `pm-onethird`'s ticket carrying Daniel's challenge. Instrument:
[`code/l1b_currency_0e8c/`](../code/l1b_currency_0e8c/), predictions committed at `71ec9e0`
before one line of it existed.*

> Daniel's words, as `pm-onethird` recorded them:
> *"we really need to get **some** real constant or this whole l1b thing is useless. we already
> have a constant bound so this is the critical gap, NOT the vague L1B as currently stated"*

---

## 0. THE VERDICT, IN FOUR LINES

1. **HE IS RIGHT.** `ε_sup < 1` **does** discharge `STATE.md` row 8 **as stated**. The row asks
   for *an explicit absolute constant, uniform in `n`*; `Op-Form` Claim 6.1 plus `mg-210d`'s
   master bound **is** such a constant, **proven for all `n`**, and **L4-independent**. There is
   no currency defence: `ε_sup` is already quoted in row 8's own `ε_spec` units.
2. **AND IT IS WORSE THAN HE SAID, IN THE DIRECTION THE TICKET SUSPECTED.** Row 8's **spectral**
   half, read at that constant, is **VACUOUS** — `1 − λ_std ≤ 1` holds at **every** poset with
   **no hypothesis at all** (`λ_std ≥ 0`, 0 exceptions in exact arithmetic over all 5,230 posets
   to `n = 6`), and `1` is **exactly** the smallest constant for which that is so, attained at
   the antichain at every `n`.
3. **BUT NOT UNIFORMLY WORSE — THE ROW'S TWO HALVES ARE NOT THE SAME STATEMENT.** The
   **inversion** half at the same constant, `E[inv_e] ≤ (1/6)(n²−1)`, is a **real theorem**: it
   **fails** at the antichain from `n = 3` on, and 82 of the 4,824 posets at `n = 6` satisfy the
   spectral half and fail the inversion half. `CONCEPTS.md` §4's word ***"equivalently"*** is not
   licensed; the master bound runs **inversions ⟹ spectrum, one way**.
4. **THE RESTATEMENT NAMES THE BAR INSTEAD OF ASSERTING A CONSTANT** — §3 — and is checked
   against the defect it repairs: `ε_sup` **misses** it by 50×.

**AND ONE THING THE CHALLENGE DID NOT ASK FOR, WHICH IS THE MOST USEFUL LINE IN THIS FILE.** The
proven supply is not a flat `1`. It is **`ε_sup = d · n/(n+1)`, linear in the incomparability
density `d = m/C(n,2)`**. So the wall is **already down** for every frozen poset with
`d ≲ 2×10⁻²`, proven, all `n`, L4-free — and what is open is the **dense** regime. *"How small a
constant"* and *"how dense a poset"* are the same question, and the second one is the one you
can point an instrument at (§4).

---

## 1. IS THE READING CORRECT? — settle the currency, then the logic

The ticket instructs, correctly, that the currency be settled first: the ledger warns repeatedly
that `ε_spec` and `ε_c3ca` are one theorem in two normalisations and that `1/6` and `1` do not
compare. **The warning is real and it does not apply here.** There are in fact **three**
normalisations in the corpus, not two, and all three are the same theorem:

| normalisation | defining relation | the constant Claim 6.1 reaches | where it is written |
|---|---|---|---|
| `ε_spec` — **row 8's own** | `E[inv_e] ≤ (ε/6)(n²−1)` | `d·n/(n+1) → 1` | `STATE.md:21`, `:125` |
| `ε_c3ca` | `E[inv_e] ≤ ε·n²` | `(n−1)/(6n) → 1/6` | [`mg-c3ca:172`](OneThird-LIBweak-mg-c3ca.md), [`mg-c4f5:415`](OneThird-LIBweak-mg-c4f5-IndependentAudit.md) |
| fraction-of-uniform — **not carried by the ledger at all** | `E[inv_e] ≤ ε·E_unif[inv]` | **`2/3`** | [`Op-Form` §6.3](OneThird-lambda-std-Operative-Form.md) |

`a3/C1` and `a3/C5` verify on exact rationals over `n = 3..12` that
`ε_spec/ε_c3ca = 6n²/(n²−1)` and that `(2/3)·E_unif[inv]` in `ε_spec` units is `n/(n+1)`
identically — **0 mismatches**. So:

> **`ε_sup < 1` is already in row 8's currency.** It is not `1/6` misread, and it is not `2/3`
> misread. The two-currency trap the ledger guards against is not what is holding row 8 up.

And the third normalisation is the sharpest evidence for Daniel available anywhere in the corpus,
because it is the **source document for L1b's operative form** saying it in so many words:

> **`Op-Form` §6.3, verbatim:** *"…freezing alone delivers `E[inv_e] < ⅔ E_unif[inv]` — a
> constant-factor improvement on random, unconditionally, i.e. **(LIB-const) already holds, with
> constant 2/3**."* **[PROVEN]**

`(LIB-const)` is the label row 8 uses for its own inversion form. The document that defines the
wall records that the wall's stated conclusion **already holds**. That sentence has been in the
corpus since `mg-88bd` and nothing has ever drawn it up into row 8's `Status` column.

**The logic, then, in one chain a non-specialist can check:**

```
frozen  δ(P) < 1/3                                              [hypothesis]
  ⟹  every incomparable pair flipped w.p. < 1/3                 [definition]
  ⟹  E[inv_e] = Σ_pairs Pr[flipped] < m/3                       [linearity — Op-Form Claim 6.1, PROVEN]
  ⟹  E[inv_e] < (ε/6)(n²−1)  with ε = 2m/(n²−1) = d·n/(n+1) < 1 [arithmetic]
  ⟹  1 − λ_std < d·n/(n+1) < 1                                  [mg-210d master bound, PROVEN]
```

Every step is proven, for every `n`, and **L4 appears nowhere** — `mg-345e` Claim 2.1 exhibits
the complete 5-item dependency list and L4 is not on it. The conclusion is precisely *"frozen ⟹
`1 − λ_std ≤ ε_spec` for an explicit absolute constant uniform in `n`"*.

**Row 8's stated form is a theorem.** It is marked `OPEN`.

### 1.1 The trap the ticket named: it IS vacuous, and the vacuity is sharp

The ticket asks whether `1 − λ_std ≤ 1` might be vacuously true since `λ_std ≥ 0` — a stronger
version of Daniel's point. **It is.** `a2` decides it in **exact rational arithmetic** (no
tolerance appears in any verdict), over every poset to `n = 6`:

| `n` | posets | `λ_std < 0` | `max(1 − λ_std)` | `min trace T_P` |
|---|---|---|---|---|
| 2 | 2 | **0** | 1.000000000000 | 1 |
| 3 | 7 | **0** | 1.000000000000 | 1 |
| 4 | 40 | **0** | 1.000000000000 | 1 |
| 5 | 357 | **0** | 1.000000000000 | 1 |
| 6 | 4824 | **0** | 1.000000000000 | 1 |

Both extrema are attained **at the antichain**, at every `n`, where `T = J/n` and
`spec(I − J/n) = {0} ∪ {1}^(n−1)` — hand-checkable, and checked by hand in `a1/T3`.

**So the vacuity is SHARP.** `1` is not merely *a* constant that makes the spectral form true
without hypothesis; it is **the smallest** one. Any `ε < 1` would have left row 8's spectral form
a genuine statement. The row is standing on exactly the boundary between vacuous and not.

**KIND, marked so this green is not over-read.** One half is algebra and one half is a
population, and they are not the same:

* **ALGEBRA, all `n`.** `M = I − S_P` is the Laplacian of the weighted graph with edge weights
  `S_P[i][j] ≥ 0`, so its eigenvalues are `0 = μ₁ ≤ μ₂ ≤ … ≤ μₙ` and `1 − λ_std = μ₂` is the
  **smallest** of the `n−1` upper ones, hence at most their average:
  `1 − λ_std ≤ trace(M)/(n−1) = (n − trace T_P)/(n−1)`.
* **FINITE POPULATION, `n ≤ 6`.** `trace T_P ≥ 1` — i.e. a random linear extension leaves at
  least one element, in expectation, in its `e` position. Minimum measured is exactly `1`, at the
  antichain.

**"The spectral form is vacuous at every `n`" is therefore NOT proven here**, and a general-`n`
proof needs exactly one missing piece: `trace T_P ≥ 1`. It **does not need to be proven** for the
verdict: on the **frozen** class the same inequality is a theorem at every `n` by the §1 chain.
Vacuity is the sharper reading of Daniel's point; it is not the load-bearing one.

### 1.2 The two halves of row 8 are not the same statement

Row 8 joins its spectral and inversion forms with *"in inversion terms"*; `CONCEPTS.md` §4 joins
them with ***"equivalently"***. At `ε = 1` they land on **opposite sides of vacuity** (`a3/C3`):

| `n` | posets | spectral **only** | inversion **only** | both | neither |
|---|---|---|---|---|---|
| 3 | 7 | **1** | 0 | 6 | 0 |
| 4 | 40 | **1** | 0 | 39 | 0 |
| 5 | 357 | **8** | 0 | 349 | 0 |
| 6 | 4824 | **82** | 0 | 4742 | 0 |

The `inversion only` column is empty at every `n` — as it must be, since the master bound gives
**inversion ⟹ spectral**. The `spectral only` column is not. So:

> The master bound is **one-way**. The inversion form is **strictly stronger**, and it is the one
> the architecture consumes. Stating the wall spectrally states **less** than is needed, and at
> the proven constant it states **nothing**.

⚠️ **WHAT THIS DOES AND DOES NOT LICENCE.** It refutes *"equivalently"* as a claim about the two
**quantities**, which is how `CONCEPTS.md` §4 reads it — a reader holding one poset can check
both sides and find them different. It does **not** by itself refute the weaker reading
*"frozen ⟹ A" iff "frozen ⟹ B"*, because the 82 separating posets at `n = 6` are **not frozen**.
That reading is unrefuted here **and unproven**; the honest word for the join is the implication
that **is** proven, with its direction named.

---

## 2. WHY THE CURRENT PHRASING FAILS THE READER — the one paragraph for a non-specialist

Row 8 says the programme cannot yet show that a frozen poset's random linear extension stays
near `e` *"by any fixed amount that does not degrade as `n` grows."* A reader checks whether the
programme has such a fixed amount. **It has one**: freezing every pair below `1/3` makes the
expected number of inverted pairs less than a third of the pairs available, at every `n`, by one
line of linearity — and the ledger records that as `PROVEN` in the same cell. The reader
concludes the wall is nearly down. It is not: the architecture does not need *a* fixed amount, it
needs one about **fifty times smaller** than the one that is proven, and no argument reaches it.
The sentence is not false — it is **satisfied**, and a satisfied sentence marked `OPEN` sends
every reader to the wrong question. Worse, the *spectral* half of that sentence, at the constant
that is proven, is true of **every poset whatsoever, frozen or not** — so a reader who checks the
form the row leads with is checking something that carries no information at all.

**`docs/OneThird-ProofShape-mg-3af8.md` exhibits the failure twice, inside one screen each time.**
At `:39` it says every pair-marginal bound *"is capped at `ε_sup < 1` … against a demand near
`2×10⁻²`"*, and **seven lines later** at `:46` states the wall as *"for an explicit absolute
constant, uniform in `n`."* And at `:276` it states the existence form again, with **nineteen
lines** to `:295`'s *"the supply — `ε_sup < 1`, **proven**."* The document states the open problem
and then, on the same screen, states that it is solved — twice. Nothing is wrong with either
sentence; what is missing is the one that says *"and that is why the row is about the SIZE."*

---

## 3. THE RESTATEMENT

The open content must be the **bar**, not the **existence**. Row 8's headline becomes:

> **L1b — the wall.** frozen ⟹ **`E[inv_e] ≤ (ε/6)(n²−1)` for a constant `ε ≤ ε_dem ≈ 2×10⁻²`,
> uniform in `n`** — equivalently `1 − λ_std ≤ ε` at that same `ε`, which is **strictly weaker**
> (the master bound runs inversions ⟹ spectrum, one way).
> ⚠️ **A CONSTANT UNIFORM IN `n` IS NOT WHAT IS OPEN — ONE IS PROVEN.** `ε_sup < 1` (pair-bias,
> `Op-Form` Claim 6.1, all `n`, L4-independent) already discharges the *existence* form, and
> `Op-Form` §6.3 states it outright: *"(LIB-const) already holds, with constant 2/3."* At that
> constant the **spectral** rendering is **vacuous** — `1 − λ_std ≤ 1` holds at every poset with
> no hypothesis, sharply, with equality at the antichain (`mg-0e8c`). **THE OPEN CONTENT IS THE
> FACTOR OF ~50 BETWEEN `ε_sup` AND `ε_dem`, AND NOTHING ELSE.**

Three properties this phrasing has and the old one did not:

1. **It cannot be discharged by `ε_sup`** — checked, not assumed (`a4/D2`): `ε_sup = 1` fails the
   bar `ε ≤ 1/50` by 50×. *The remedy is an artifact of the same kind as the defect, so it is
   subject to that defect; this is the check that it is not.*
2. **It leads with the inversion form**, which is the one the architecture consumes and the
   strictly stronger of the two (§1.2), instead of the one that is vacuous at the proven constant.
3. **It names the number a proof must beat.** *"An explicit absolute constant"* is a target
   nobody can aim at, because it is already hit. `2×10⁻²` is a target.

**What does NOT change.** The status stays `OPEN` — nothing here proves or disproves the wall.
The kind stays as it was. No other row moves. `ε_dem`'s own dependencies (`C₃` unquantified,
L4-as-stated for the threshold `ε₀`) are untouched, and the `~50` inherits their uncertainty —
which is an argument for naming the bar in the row, where the qualifications already live, rather
than hiding it inside a symbol.

---

## 4. THE READING THE CHALLENGE DID NOT ASK FOR, AND THE ONE MOST WORTH HAVING

`ε_sup` is not a flat `1`. Claim 6.1's bound is

```
    ε_sup(P)  =  d · n/(n+1)         d = m/C(n,2), the incomparability density
```

so the proven supply **already clears the demand** whenever `d ≲ 2×10⁻²`. In other words:

> **The wall is already DOWN — proven, all `n`, L4-free — for every frozen poset of
> incomparability density below about 2%. What is open is the DENSE regime.**

This is not a new number. `a3/C5` cross-checks it against one the ledger already carries:
primitivity forces `m ≥ n−1`, i.e. `d ≥ 2/n`, so a **primitive** poset can have `d ≲ 2×10⁻²` only
when `n ≳ 100` — **exactly** the `n ≥ 100 (primitive)` threshold row 8 already records from
`mg-e35c` A1. The density reading and the ledger's own threshold are one fact reached from
opposite ends. (`Op-Form` §6.3 records the same threshold at the **superseded** `ε_spec = 2×10⁻⁴`,
printing `d ≲ 2×10⁻⁴`; the 100× is `mg-e35c`'s repair, not a new result.)

**Why this is worth more than the phrasing fix.** *"Make the constant 50× smaller"* is not a
statement anyone can attack directly. *"Handle frozen posets of incomparability density above
2%"* is a statement with a population, an instrument, and a boundary — and it recasts tonight's
other threads as attacks on one axis rather than three: `mg-7564` (relax the demand) moves the
threshold up, `mg-6ff4` (measure the boundary) measures where the surviving class lives, and
`mg-6bc2`'s realizability route (`mg-92e6`'s adjacency symmetry is the first fact that bites)
attacks the supply inside the dense regime. All three are attacks on **the size**, which on this
reading is the whole problem rather than a refinement of it.

⚠️ **AND THE LIMIT OF IT, STATED HERE SO IT IS NOT QUOTED BARE.** `d ≲ 2×10⁻²` describes a
**sparse-incomparability** poset. A minimal counterexample is not known to be one, and nothing
here says the surviving dense class is small, non-empty, or tractable. What is established is
that the open region has a **boundary with a number on it**, where before it had a symbol.

---

## 5. WHERE THE PHRASING LIVES — every site, and what each needs

Grep for the existence form across the corpus. The sites split three ways, and the split is the
repository's own convention (`STATE.md`'s attempt-index rule and the strike convention).

**CANONICAL — moved by this work item:**

| site | what it says | disposition |
|---|---|---|
| `STATE.md:21` | the L1b blockquote, existence form, spectral-first | **rider added** |
| `STATE.md:31` | Axis 1 bullet, *"a constant uniform in `n`"* | **rider added** |
| `STATE.md:67` | mermaid node `C` | **relabelled** |
| `STATE.md:125` | row 8 itself | **restated per §3** |
| `docs/CONCEPTS.md:126` | §4, existence form + the word ***"equivalently"*** | **restated; `equivalently` replaced** |
| `docs/OneThird-ProofShape-mg-3af8.md:46` | §1 move 3, existence form | **rider added** |
| `docs/OneThird-ProofShape-mg-3af8.md:276` | §4 blockquote, existence form | **rider added** |

**THE RENDERED TWIN — RECONCILED HERE, not deferred:**
`docs/state-of-the-wall.html:263` (the formula block) and `:409` (row 8's cell) both carried the
existence form. It is **hand-maintained and subordinate to `STATE.md`**, with a `STATE-PIN`
checked per-row by `code/rendered_twin_pin_9bc2/twin_pin.py`.

I first intended to flag these and leave re-pinning to `mg-cdd5`'s process. **That was wrong, and
the gate said so:** `code/control_gate_724a` went **RED** on this branch with
`twin.control_exit`, `twin.verdict_grade` and `twin.worklist` all diverged — because moving row 8
in `STATE.md` and not moving the twin *is itself* the defect the twin control exists to catch.
Deferring would have meant landing the restatement while the rendered page kept telling readers
the wall is *"a constant uniform in `n`"* — the exact failure this work item was filed about,
reproduced one document over. **Both cells are edited with the old text struck rather than
deleted, and row 8 is re-pinned.** (`mg-cdd5`'s ruling that a cell need not be edited when *"the
page does not render what moved"* does not apply: this page renders precisely what moved.)

**ARCHIVAL — must NOT be edited**, listed so the next reader knows they were checked and why they
stand: `docs/state-history/attempt-mg-88bd.md:98`, `attempt-mg-a58f.md:34`,
`attempt-mg-210d.md:24`, `threads-chronology.md:47`; and the write-ups that state the form as
their own subject at the time they were written —
[`OneThird-lambda-std-Operative-Form.md:40`, `:707`](OneThird-lambda-std-Operative-Form.md),
[`…-IndependentAudit.md:30`, `:660`](OneThird-lambda-std-Operative-Form-IndependentAudit.md),
[`OneThird-LIBweak-mg-c3ca.md:99`](OneThird-LIBweak-mg-c3ca.md),
[`OneThird-LIBweak-mg-c4f5-IndependentAudit.md:262`](OneThird-LIBweak-mg-c4f5-IndependentAudit.md),
[`OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:332`](OneThird-Direct-Prefix-Route-mg-2de0-Audit.md),
[`OneThird-PairBias-Independence-mg-345e.md:30`, `:64`, `:108`](OneThird-PairBias-Independence-mg-345e.md),
[`OneThird-PairBias-Independence-mg-6bd1-IndependentAudit.md:200`](OneThird-PairBias-Independence-mg-6bd1-IndependentAudit.md).
An attempt file records what was believed when it was written; rewriting it destroys the only
evidence of when the belief changed. **Two of these are worth reading against this file rather
than struck:** `mg-345e:64` already says the pair-bias constant *"is `1` — already proven"*, and
`mg-6bd1`'s audit at `:200` already questions *"the claim that a constant uniform in `n` is the
right thing to want."* The finding in this document was **twice reachable from the corpus's own
words** before Daniel reached it from them a third time. That is the argument for the rider.

---

## 6. WHAT I DID NOT DO, AND WHAT I GOT WRONG

**Not re-derived, inherited:** `Op-Form` Claim 6.1; `mg-210d`'s master bound; `mg-61bb`'s
coherence; `mg-e35c`'s repaired `ε_dem ≈ 2×10⁻²` and the `~50` that follows; `mg-6bc2`'s
Claim 3.1. `a1/T5` and `a3/C2` test that this instrument's quantities sit on the sides of the
first two that the corpus says they do — that is a consistency check, not a proof.

**Not measured above `n = 6`.** Every census here is `FP`. The `n ≤ 6` frozen class is **exactly
the chains**, so every "0 violations on the frozen class" figure in this file is a measurement
over the chains and is **evidence about nothing else**. The nearest miss is `δ = 1/3` **exactly**
— on the boundary, excluded by the strictness of `δ < 1/3`, the same hair that puts `mg-6bc2`'s
`η = 0` witness outside `M_n(η)`.

**Not decided:** whether the surviving dense class is non-empty; whether `ε_dem` can be relaxed
(that is `mg-7564`); whether the true constant is far below the demand; which `1/6` Daniel meant.

**WHAT I GOT WRONG, and it is in the instrument's own record.** My first oracle for §1.1 tested
`S_P` **PSD** instead of `λ_std ≥ 0`. PSD is strictly stronger — it asks every eigenvalue to be
non-negative where `λ_std ≥ 0` asks only for the largest one on `1⊥` — and it is **false at 4759
of the 4824 posets at `n = 6`**, while the statement I was testing holds at all of them. The
wrong oracle failed in the *safe* direction, which is precisely how it would have survived: it
would have under-claimed, and nobody re-checks an under-claim. **A report about a claim stated in
the wrong currency very nearly shipped one.** The census that caught it is kept in `a2`'s output
and asserted as a check in `a1/T6d` rather than removed, and `code/l1b_currency_0e8c/README.md`
carries the full enumeration of ways this remedy could have exhibited the defect it repairs.

**PREDICTIONS SCORED** (`71ec9e0`, committed before the instrument existed):

| | prediction | outcome |
|---|---|---|
| P1 | Daniel is right; `ε_sup` discharges the stated form | **HIT** — but largely a restatement of R1, low credit |
| P2 | spectral half **vacuous**, `λ_std ≥ 0` everywhere | **HIT on the claim, MISS on the mechanism** — I named `S_P` PSD as the reason and that is false almost everywhere; the true reason is `trace T_P ≥ 1` through the Laplacian average |
| P3 | `max(1 − λ_std) = 1` exactly, attained at the antichain | **HIT**, exact, `n ≤ 6` |
| P4 | the two halves come apart at `ε = 1` | **HIT** — 82 separating posets at `n = 6` |
| P5 | frozen class non-empty at `n ≤ 6` and **exactly the chains** | **HIT**, and it settles the disagreement with `mg-7c78`'s *"empty"*: the class is non-empty and carries **zero** posets with an incomparable pair, which is what that prediction meant |
| P6 | four canonical sites, no fifth | **MISS** — there are **seven**: I missed `STATE.md:31` and `:67`, and `ProofShape` carries **two**, not one. The rendered twin's two cells make **nine**, and I predicted the twin would not be in scope; the merge gate disagreed and was right |
| P7 | `ProofShape` §4 contradicts itself within 20 lines | **HIT** — nineteen lines at `:276`→`:295`, and a tighter one I did not predict at `:39`→`:46`, seven lines |

---

## 7. APPLICATION AUDIT — mg-28b6, the successor this document required

*Appended by `mg-28b6`, 2026-08-13. The finding above is not re-litigated here: it is merged, it
is measured over 5,230 posets, and it carries its own pre-correction defect in the record. This
section records only whether it is APPLIED, where the enumeration in §5 lost a site, and what the
ceiling-raise process owes.*

### 7.1 The premise of the successor ticket was false, and that is the first finding

`mg-28b6` was filed on the reading that *"the finding is not yet applied to the documents it is
about."* **It was.** Every one of §5's nine canonical sites was already carrying its rider on
arrival, in the same commit as the finding (`b364767`), with the ceiling raise banked in the
commit that caused it (`CEILING.json`, 20,784 → 21,328). The four documents were read site by
site before a line of `code/l1b_application_28b6/` existed; that table is in that directory's
`README.md` §0.

What the successor ticket did have to do is the **fourth** item of this document's own VERDICT
REQUIRED clause — *the list of other sites carrying the same phrasing* — which §5 delivered least
completely, and which `P6` scored as its only outright **MISS**.

### 7.2 The site §5 missed: `docs/state-of-the-wall.html:385–386`

The twin's **proof-chain** rendering of the very mermaid edge `B → C` and node `C` this work item
moved at `STATE.md:67` and `:72`. It read *"**L1b** — bad mixing ⟹ λ_std → 1"* over a node
labelled *"λ_std → 1 · near-ordinal-sum"* — i.e. the **LIMIT** rendering, which row 8's own cell
calls *"a stronger rendering that happens to be available, not the requirement"*, standing where
`STATE.md` now leads with the constant and names the **size** as the open content. **Restated by
`mg-28b6`, old text struck rather than deleted**, in the convention §5 used at `:263` and `:409`.

**§5's own reasoning predicted this miss and stopped one document short of it.** It argued the
twin had to move *because* *"moving row 8 in `STATE.md` and not moving the twin is itself the
defect the twin control exists to catch"* — and then took the twin's two **ledger** sites, which
are the two the control can see. `code/rendered_twin_pin_9bc2/COVERAGE.md` says in its own words
that proof-chain prose is uncovered and that *"the historically most common form of this defect is
out of scope"*. `mg-957a` had **named this exact lag a fortnight earlier and left it** (`:249`).
So the site was: known, recorded, uncovered, and adjacent to a red gate that could not reach it.

**No re-pin.** `STATE.md` is byte-identical to what the pin already names, so re-pinning would
have been `COVERAGE.md` item 4's *"caller who edits nothing and re-pins anyway"* — performed by
the work item whose subject is that control's blind spot. The pin is green before and after, and
**that green says nothing about `:385`**.

### 7.3 The ceiling raise: none is due, and here is the arithmetic rather than the claim

The successor ticket asked that the ceiling-raise process be documented and not bypassed.
`code/state_ratchet_e331` measures **`STATE.md`** against `words_ceiling = 21328`, and `mg-28b6`
adds **zero words to `STATE.md`** — the restatement is already there and the site it moved is in
the rendered twin, which the ratchet does not measure. So the correct disposition is *no raise*,
and the check is a run of the gate rather than an assertion (`sh build.sh`, exit 0, ratchet arm
green). Raising the ceiling with nothing to bank would have been growth laundered through a
process designed to make growth visible.

### 7.4 What now asks the question, and what it cannot answer

`code/l1b_application_28b6/` — two arms, **0.34 s**, wired into `build.sh`. `c0` checks **12**
anchored sites (§5's nine, with this document's `STATE.md:67` split into the diagram's node and
its edge, plus the two new twin chain sites) and sweeps the four canonical files for the
discharged phrasing appearing in an L1b context without a rider or a strike. `c1` runs eight
planted worlds; **seven fire or refuse, and the eighth stays green on purpose** — the discharged
phrasing restored as row 8's lead with the rider left in place. The gate is on **STRUCTURE, not
on truth**, and that world is the measurement of it.

**Sites checked and deliberately left**, beyond §5's archival list: `docs/OneThird-L4-Threshold-eps0-mg-3969.md:500`
(*"`ε_dem`'s FORM — an absolute constant uniform in `n` — IS reachable without `ε₀`"* — a claim
about the **demand** side's form, correct in its own scope and not a statement of what L1b leaves
open); `STATE.md:179–180` (`C₃^(III)` and `(L*)`, two other statements sharing the phrase — the
reason `c0` requires an L1b token within 240 characters, and the reason `mg-8d63` swept *"for the
CLAIM and not the phrase"*); and the deliverables that state the operative form with the symbol
`ε_spec` rather than the existence claim (`mg-05ec`, `mg-409a`, `mg-7564`, `mg-9461`, `mg-145f`).
