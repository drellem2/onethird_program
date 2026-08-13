# `mg-9b6b` — the density route's last named survivor, and the shape of the dial it sits on

**Successor to `mg-3da1`, which was the successor to `mg-c776`.** Four arms, standard library only,
exact rationals on every verdict path, `sh run_all.sh`, ~3 min, worst arm exit 0. Predictions with
the exposure disclosed per line: [`PREDICTIONS.md`](PREDICTIONS.md). The document is
[`docs/OneThird-LeverShape-mg-9b6b.md`](../../docs/OneThird-LeverShape-mg-9b6b.md).

---

## §1. The question, and why it is this one

`mg-3da1` closed the image line and named its remainder as *"what remains as a lever at all"*.
`mg-0b96` had already closed the density lever — `(1_D)` is the conjecture on `{d > D}` at every
`D` — and then, in its §6, named **the one thing that would change that verdict**:

> *"A result of the form `δ(P) ≥ f(d)` with `f` increasing and `f(2×10⁻²) ≥ 1/3` — a
> DENSITY-TO-BALANCE bound rather than a structure-to-balance one. … **It is not ruled out here.**"*

That is the last named survivor of the whole density route, and it is the only object on the board
whose population is not empty. This directory asks what it is.

## §2. The verdict

**Every reading of it lands on the dial `mg-0b96` closed, and one reading is refuted outright.**

| reading of §6's `f` | status | where |
|---|---|---|
| **flat** — `f = (1/3)·1[d ≥ D]` | **it IS `(2_D)`, hence `(1_D)`** — the closed statement in unconditional clothing | `e1` m2 |
| **strictly increasing at `D`**, or any `f` with `f(D) > 1/3` | **FALSE at 63 orders** — `n = 3…66` except 65 — refuted by an explicit ordinal-sum family with `δ = 1/3` exactly and `d` above `D_needed` | `e1` m3 |
| **restricted to primitive posets** | `e1` m3 lapses above `n = 3`; `e1` m2 does not. Same statement, and **`mg-0b96`'s price already ran through primitivity** | `e1` m4 |

**And the reason it keeps looking open is measured rather than guessed.** The frontier is REAL:
`G(s) = max{d : δ ≤ s}` is a genuine rising function with no conjecture anywhere in it, computable
to the last member — **and it is EMPTY at every `s < 1/3`.** An instrument computing residual (R)
therefore returns a healthy, exactly-computed answer at every hypothesis **except the one row 8
consumes** (`e2` m1). The route reads as open from the instrument side however many times it is
closed from the logic side.

**The dial, priced end to end** (`e3`) — `mg-0b96` priced one point of it:

| `D` | what it is | forbids a frozen primitive up to | unreached orders it delivers |
|---|---|---|---|
| `1 − ⌈(n−1)/2⌉/C(n,2)` | **PROVEN** (F26, `U`) | nothing | **0** |
| `ε_dem·(n+1)/n ≈ 2e-2` | what row 8 needs | `n = 98` | **84** (`mg-0b96` d2's figure, reproduced) |
| `4⌊n/3⌋/(n(n−1))` | what the **data** exhibits (F23) | **every `n ≥ 4`** | **all of them** |

**Value and price are the same quantity**, so the dial has no setting that is both provable and
worth anything — and it says so hardest at the end the evidence points to. In orders rather than in
`ε`: any `D` delivering even one unreached order must be **under `2/15`**, against a proven ceiling
of `1 − Θ(1/n)` — a factor of **7.0× at `n = 15`, widening to 7.5× at `n = 300`** (`e3` m5), which
is `mg-0b96`'s `49×` in a second currency.

## §3. The two things that are new here rather than re-derived

1. **`e1` m3 — the strict reading is refuted, not open.** `mg-0b96` §6 says *"it is not ruled out
   here"*, which was true of that instrument. It is ruled out here, by a construction: `⌊n/3⌋`
   copies of `{a<b, c}` in ordinal sum has `δ = 1/3` **exactly** at every `n` (the ordinal-sum
   lemma, not a census) and density above `D_needed` at 63 orders.
2. **`e3` m4 — the data end delivers the whole conjecture, not 84 orders of it.** Nobody had asked
   what the family does away from `D_needed`. The answer is that the ceiling the boundary class
   actually exhibits is **strictly worse to buy** than the constant one, because it exempts less.

## §4. What is NOT new, and is here because a later arc will need it in one place

`e1` m2 (the collapse) is `mg-0b96` §2 with the `>`/`≥` quantum measured. `e2` m3 (`G(1/3)`) is
F23. `e3` m2's 84 is `mg-0b96` d2's, recomputed from the exemption side as a control on **this**
arm. `e0` T6 (the frozen class is empty at `n ≤ 8`) is `mg-0b96` d0 T6, re-established rather than
cited because an import whose controls live elsewhere is unchecked from here.

## §5. Controls

- **`e0` T1–T5**: the enumerator against **A000112**; F26's ceiling against two spellings and
  against `mg-0b96`'s own published `ε_sup` table; `δ` against **brute-force enumeration of
  `L(P)`** over all 399 non-chain classes at `n ≤ 6`; a five-poset hand table; **two planted
  defects**, both live (281 and 286 of 317 classes at `n = 6`).
- **`e0` T6 — wrong direction 1.** The frozen class is empty at every `n ≤ 8` (16 998 non-chain
  classes at `n = 8`), established **before** any arm prints a zero over it.
- **`e0` T7 — wrong direction 2, the must-FIRE control.** At `β = 2/5` the class is *not* empty:
  the same `one_D`/`ceiling_at` return real ceilings (`2/3, 1/3, 1/2, 2/5, 4/7` at `n = 3…7`) and
  **FIRE** on explicit counterexamples when the ceiling is set one density quantum too low. Without
  this, every *"empty"* and every *"no lever"* here could be a property of the tool.
- **`e1` m2** cross-checks three predicates computed through **different comparisons** over 60
  `(n, β, D)` cells — a tautology's warrant cannot be improved by a run, but an implementation in
  which `frozen` and `δ ≥ 1/3` are not complements is exactly what a run catches.
- **`e3` m4 re-measures** the six `G(1/3)` values rather than copying them from `e2`'s transcript.

## §6. Where this could be wrong

- **`e2` m3's agreement with F23 is computed through `lib6ff4`, the library F23 was measured
  with.** It is a consistency check on this arm, **not** an independent corroboration, and a
  disagreement would impeach this directory first. Said at the table as well as here.
- **Every use of F23's closed form above `n = 9` is an extrapolation of an `FP` result.** `e3` m4
  is therefore reported twice — once on the measured maxima at `n ≤ 8` alone, where it is a fact,
  and once on the closed form, where it is a conditional. **The first is the one to quote.**
- **`e1` m3's refutation above `n = 9` rests on the family's own `δ` and `d`**, which the
  ordinal-sum lemma gives, and **not** on F23's maximality, which it does not need. The `n ≤ 66`
  bound *is* arithmetic on F23's closed form, and the hole at `n = 65` is real: `65 = 3·21+2`, so
  `⌊n/3⌋` sticks while `D_needed` keeps falling. **A claim of *"every `n ≤ 66`"* would have been
  false at exactly one value**, and only computing the set says so.
- **Nothing here shows any `(1_D)` is FALSE.** Every one of them is true if the conjecture is. The
  finding is about what proving one would deliver.
- **`e2`'s staircase above `1/3` is unconditional information about 20 000 posets, not about all
  posets.** Kind `FP`. Per `STATE.md`'s standing rule, any sentence aggregating this directory's
  results must say **`FP`**.
- **`e3`'s census frontier of 14** is read from `mg-0b96` d2 (Gupta, preprint; refereed 11) and is
  not re-verified here. Move it and the 84 moves with it.

## §7. What was NOT done

- **The boundary was not re-measured** — `e2` m3 reads F23 and does not re-derive it.
- **No arc was opened on `(B-cov)` or `(EQ)`.** *"What remains as a lever"* is answered **for the
  density route only**; the other two residuals are not priced here and this directory says nothing
  about them.
- **`docs/FACTS.md` gets no entry.** Every measurement here is consumed by this landing, which
  fails the registry's own homelessness test (`mg-3da1`'s reason, applied to this branch).
- **No ledger row was edited.** `STATE.md`'s residual list gets the `(R)` bullet corrected — it
  still read as live — and nothing else moves.
