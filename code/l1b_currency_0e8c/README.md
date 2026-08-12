# `code/l1b_currency_0e8c/` — mg-0e8c's instrument for Daniel's challenge to row 8

**THE QUESTION.** `STATE.md` row 8 states the wall as *frozen ⟹ `1 − λ_std ≤ ε_spec` for an
explicit absolute constant, uniform in `n`* and marks it `OPEN`, while the **same cell** records
`ε_sup < 1` as **PROVEN**. Daniel: *"we already have a constant bound so this is the critical
gap, NOT the vague L1B as currently stated."* This instrument decides whether he is right, and
whether the stated form is not merely already-satisfied but **vacuous**.

**THE VERDICT IS IN [`docs/OneThird-L1b-Restatement-mg-0e8c.md`](../../docs/OneThird-L1b-Restatement-mg-0e8c.md).**
This file records what the arms are and what they can and cannot support.

| arm | what it decides | kind of its output |
|---|---|---|
| `a1_selftest.py` | conventions — poset enumeration, `λ_std`, `E[inv_e]`, master-bound direction, both PSD oracles | gate; nothing below is readable if it is red |
| `a2_vacuity.py` | is `1 − λ_std ≤ 1` true with **no hypothesis**? | `FP` exhaustive `n ≤ 6`, plus one **all-`n`** algebraic reduction |
| `a3_currency.py` | the unit map (three normalisations), Claim 6.1 on the frozen class, whether row 8's two halves agree, the gap, the **density** reading | `FP` `n ≤ 6` for the censuses; **algebra** for the unit map and the density threshold |
| `a4_remedy.py` | the frozen boundary at small `n`, and whether the **restatement** reproduces the defect it repairs | `FP` `n ≤ 6`; the remedy check is arithmetic |

Run with `./run_all.sh` (≈20 s on this host). No third-party libraries; there is no numpy on
this machine, which is why the Jacobi solver is hand-written — and why every **verdict** is taken
from exact rational arithmetic instead, with floats used only where a number is being *reported*.

---

## THE DEFECT THIS INSTRUMENT FOUND IN ITSELF, RECORDED RATHER THAN QUIETLY FIXED

The first draft of `a2` tested `1 − λ_std ≤ 1` by asking whether **`S_P` is positive
semidefinite**, reasoning that `S_P·1 = 1` puts the `+1` eigenvector outside `H = 1⊥`. That is
backwards. `λ_std = max spec(S_P|_H)` — the **largest** eigenvalue on `H` — so `λ_std ≥ 0` says
**one** eigenvalue is non-negative, while PSD says **all** of them are. PSD is strictly stronger
and it is false almost everywhere: **4759 of the 4824 posets at `n = 6`** have a non-PSD `S_P`,
while `1 − λ_std ≤ 1` holds at **every one of them**.

The wrong oracle failed *safely* — it would have reported a vacuity failure that is not there,
so the finding would have been under-claimed rather than over-claimed. It was still a test of a
different statement, and "wrong in the safe direction" is how a measurement gets trusted for a
year. `is_psd_exact` is **kept** and `a2` still prints the PSD census, because deleting it would
leave this correction unsupported; `a1/T6d` asserts the separation as a **check**, so the
correction cannot decay into prose.

**This is the enumeration the polecat protocol asks for — a remedy is an artifact of the same
kind as the defect, so it is subject to it.** The defect under investigation is *a statement
made in the wrong currency*. The ways this instrument could exhibit it, and what was done:

| how the remedy could exhibit the defect | check |
|---|---|
| `λ_std` computed under a different convention from the corpus's | `a1/T2` — cross-implementation agreement against `libA94`, no shared code, every poset to `n = 5` |
| `E[inv_e]` counting comparable pairs, or the wrong reference order | `a1/T3`–`T4` — antichain and chain against **hand** arithmetic |
| the master bound assumed to run the direction convenient to the argument | `a1/T5` — tested, 0 violations, `n ≤ 6` |
| `ε_sup` quoted in the wrong normalisation (the ledger's own two-currency trap) | `a3/C1`, `a3/C5` — **three** normalisations shown to be one theorem, exact rationals |
| the vacuity verdict resting on a floating-point tolerance | every verdict is exact rational; floats report numbers only, and `a1/T6c` checks the two agree |
| **the oracle testing a different statement than the one claimed** | **this is the one that fired** — see above |
| the restatement itself being discharged by `ε_sup`, i.e. the repair reproducing the defect | `a4/D2` — checked, and it is not: `ε_sup = 1` misses `ε_dem = 1/50` by 50× |

---

## SCOPE LINES — no figure here may be quoted away from these

* Every census is over the **labelled** posets on `{0..n−1}` admitting `e = 0 < 1 < … < n−1` as a
  linear extension, **exhaustive to `n = 6`** (2, 7, 40, 357, 4824 posets). Nothing is measured
  above `n = 6`. Restricting to this labelling is not a restriction — `e` is a frame, not a
  choice — but it is the population, and it is `FP`.
* **The frozen class at `n ≤ 6` is exactly the chains** (`a3/C2`, `a4/D1`): 1 poset per `n`, none
  with an incomparable pair. So every "0 violations on the frozen class" figure here is a
  measurement over the **chains** and is evidence about nothing else. The nearest miss sits at
  `δ = 1/3` **exactly** — on the boundary, excluded by strictness.
* `ε_sup < 1` and `ε_dem ≈ 2×10⁻²` are **READ** from the corpus (`Op-Form` Claim 6.1 via
  `mg-345e`; `STATE.md:21`'s repaired calibration). Neither is re-derived here. What is computed
  is the conversion between them and its consequences.
* `mg-210d`'s master bound and `Op-Form` Claim 6.1 are **INHERITED**. `a1/T5` and `a3/C2` test
  that our quantities sit on the sides of them the corpus says they do; they are not proofs.
* The all-`n` half of `a2` is the **reduction** `1 − λ_std ≤ (n − trace T_P)/(n−1)`, which is
  algebra. Its premise `trace T_P ≥ 1` is `FP` at `n ≤ 6`. **"The spectral form is vacuous at
  every `n`" is NOT proven here** — and does not need to be, because on the *frozen* class the
  same inequality is a theorem at every `n` by Claim 6.1 plus the master bound.
