# `subset_consumability_99f4` — is any separator in the arbitrary-subset class CONSUMABLE?

`mg-99f4`. The ticket's requirement, verbatim: **"Deliver a separator that is CONSUMABLE, or
establish that separators in this class are not."**

This directory establishes the second, and the reason is one line that is not about any
particular separator.

---

## 1. The answer

> A construction `Φ : 2^{S_n} → V` can be **consumed** only at the inputs where an `e(P)`
> exists, and those are exactly `LL_n = {L(P) : P}`. It can **separate** only by what it does
> elsewhere. A function's value at one point does not constrain its value at another.

So separation and consumability are **independent coordinates of the same function**. The
ticket's demonstrated asset — the BK graph on `supp(μ)`, 12 edges against 0 — is a statement
about `Φ` **off** `LL_n`, and every bound is a statement about `Φ` **on** it. It is worth
exactly zero toward the requirement. **Not "not yet": provably zero.**

`s1.3` makes that constructive rather than rhetorical. Three constructions — `phi_bk`,
`phi_sep`, `phi_blind` — agree at all 19 consumable inputs at `n = 3`, hence support *literally
the same bounds*, and on one marginal-equivalent witness `phi_sep` separates while `phi_blind`
does not. Separation was moved from `YES` to `no` without changing a single bound.

**And the class does not survive its own enlargement.** `LL_n ↔ posets` is a bijection
(`s1.1`, against A001035 at `n = 2…5`), so `Φ` restricted to the consumable inputs **is a
function of `P`** — `mg-8b32`'s C1 reached by a road that never mentions `π`. Daniel's class
survives C1 only because `S` ranges wider than `LL_n`, and `s1.2` prices the extra width: at
`n = 5` the class hands a construction `2^120` inputs of which **4231** carry an `e(P)`.

## 2. And every on-record candidate fails, for two reasons rather than one

`s1.4`–`s1.7` run the four TIER-2 separators `mg-8b32` b2.3 put on record through a screen:

- **Q1 RESOLUTION** — is `Φ` non-constant on `LL_n`? One pass over the posets.
- **Q2 COST** — is `Φ(L(P))` obtainable without enumerating `L(P)`?

| separator | Q1 `res > 1` | Q2 cheap | consumable |
|---|---|---|---|
| `L* ∈ S` | no (`res = 1`) | — | **NO** |
| `\|S\| = e(P(π(S)))` | no (`res = 1`) | — | **NO** |
| `S` is a weak-order ideal under `L*` | no (`res = 1`) | — | **NO** |
| the BK edge count on `S` | **YES** (`res = 4, 10, 29`) | no | **NO** |

Three are **constant on every consumable input** — `s1.5` measures their sharpest bound at
**zero bits** against the free bound, at every `n`. Each is a predicate whose whole content is
*the realizable inputs are realizable*: perfect separation, no resolution. That is
`gap(μ) = log₂ e(P) − H(μ)`'s defect wearing different clothes — there the constant is `0`, here
it is `True`.

The fourth is the survivor and it fails on **cost**: `|E|` is a sum over `L(P)`, and
`e(P) − 1 ≤ |E|` by BK-graph connectivity, so `e(P) ≤ |E| + 1` bounds the thing we cannot
compute by a larger thing we can compute only by computing it.

**Separation is not among the questions and cannot be**, by §1.

## 3. The acceptance condition for the prefix-code branch, stated BEFORE anything is built

The ticket asked for the crossover first. `s2` answers it for the **family**, because the answer
turns out not to depend on the mechanism.

A bound of **shape A**, `log₂ e(P) ≤ c · n log₂ n`, beats the free bound `log₂ n!` exactly when
`log₂ n > log₂(e)/(1−c)`, i.e.

> **`n*(c) = 2^(1.442695 / (1 − c))`** — doubly exponential in `1/(1−c)`.

`s0.6` reproduces `mg-0fc6` a1.6's published `16,777,063` **to the unit** on code that shares
nothing with it, which is what licenses the rest of the table:

| target `n*` | required `c` | required saving | against `compression2`'s 6.01% |
|---|---|---|---|
| `10^7` | 0.9380 | 6.20% | 1.0× |
| `10^3` | 0.8559 | 14.41% | 2.4× |
| **`10^2`** | **0.7899** | **21.01%** | **3.5×** |
| `20` | 0.7066 | 29.34% | 4.9× |

**The frontier that matters is `n ~ 10^2`, not `10^7`** — `mg-0b96` priced the `d`-lever at
`n = 99`. So the ticket's own bar is the weak form of the question.

**But the finding is `s2.4`, and it moves the dial off the constant entirely.** A bound of
**shape B**, `log₂ e(P) ≤ c · log₂ n!`, bites at **every** `n` for **every** `c < 1`. There is no
crossover to compute. `n log₂ n` exceeds `log₂ n!` by `1.4427·n` — *linear* in `n`, against a
saving that is a constant fraction of `n log₂ n` — so a shape-A saving must first pay back a
linear term. **That is the entire content of `compression2`'s `1.7 × 10⁷`: arithmetic about two
scales, not a fact about the merge tree.**

So the operative question is one line, and it is **not** "what is your constant":

> Does the code's expected length beat `⌈log₂ n!⌉` — the code that indexes `L` into all of
> `S_n` and ignores `P` — **at the `n` you claim it?**

A code answers that at any single `n` by construction, since it *is* a code: run it. No
asymptotic constant needs proving to find out. **The cheap test the ticket asked for is cheaper
than the ticket supposed.**

## 4. What went red, and what was predicted wrong

- **`s0.6` went red on its first run** and is reported rather than quietly fixed. The control
  was calibrated on `0.9399`, the constant as **printed** in `mg-0fc6`'s table header; the code
  computes `1 − 1/(24 ln 2) = 0.9398877`. The two crossovers differ by **57,186**. Not an error
  in `mg-0fc6`'s measurement — its number is right for its own constant and the header is a
  rounding in prose. It is recorded because the **elasticity** `d(ln n*)/dc = 1/(1−c)²` is
  **277** there, so four printed digits of `c` do not pin `n*` to four digits.
- **Two of five predictions were refuted** (`PREDICTIONS.md` P2, P3, P5) and are kept as
  written. P3 is the one worth reading: the survivor determines `e(P)` **exactly** at `n = 3, 4`
  — *stronger* than predicted, and unconsumable anyway.
- **`s1.5`'s first draft credited `T2a` with 2.26 bits it has not got**, by bucketing
  *undefined* as a value. `L*` does not exist at every poset (2040 of 4231 at `n = 5`), and the
  split being scored was `does L* exist` — a TIER-0 function of `π`, not the row. The population
  is now the one the separator is defined on, and the note says so.
- **`s0.9`'s plant came back INERT** and is printed rather than swapped out. A plant has to be a
  defect the domain can express; on an `L(P)` the two readings of the weak-ideal predicate
  coincide, so it discriminates at 0 of 110.

## 5. What this directory does NOT establish

- **Not that no consumable construction exists.** The dichotomy says separation cannot *help*.
  It does not say `Φ|_LL` cannot bound `e(P)` — and **prefix codes on `L(P)` are exactly such a
  `Φ|_LL`.** They are consumable-native (Kraft/Shannon), and **neither of today's closures
  touches them**, because both are about separation and a code neither separates nor needs to.
  Daniel's 20:35Z direction survives; what does not survive is the *subset framing* offered as
  its justification. His §1 — *"a code's output on a set `S` reads `S`, so it is not a function
  of `P`"* — is true and is the wrong half: the reading that bounds `log₂ e(P)` is the one at
  `S = L(P)`, and that one **is** a function of `P`.
- **Not that a shape-B bound is achievable.** `s2.5` cites `mg-0fc6` a3.1 (`0.907 … 0.883`,
  `n = 3…7`, decreasing) as an **existence** statement about the sharpest constant. Five points
  do not settle a limit; no code achieving them is exhibited here. `mg-0fc6` a3.2's caution
  stands in the other direction — the two-atom law has `H = 0.9183` bits at *every* `n` with
  simultaneously maximal `E[inv_e]`, so an entropy bound does not deliver an inversion bound.
- **Nothing above `n = 5`** for the poset sweeps, and nothing about the F24 multiplier's third
  axis. See §6.

## 6. Not done, and it is the successor's

`mg-9d9e` carries both halves. **The prefix-code branch**, with the subset framing stripped off
and the one-line acceptance test above as its gate. And **the F24-multiplier branch** (the
ticket's 20:20Z addendum), which is **not addressed here** at all: its third axis is still
unnamed, and by §1 a multiplier is a `Φ|_LL` object — so the dichotomy **scopes** it rather than
closing it, and it faces the same two-question screen. Pricing it is a separate landing.

## 7. Controls

`s0` runs before any arm that produces a finding: A001035 at `n = 1…5` by a brute-force
enumerator that shares no idea with the estate's recursions; `e(P)` against a down-set DP that
never enumerates a permutation; `P = ⋂L(P)` at every poset; `L* ∈ L(P)` wherever `L*` exists
(2150 posets); `δ` against hand values; `mg-0fc6`'s crossover to the unit; and four planted
defects, of which the fourth is the one that matters — a crossover comparing against the *wrong
scale* would make `s2`'s whole finding true by construction, and `s0.6`'s unit agreement is what
rules it out.

Two consecutive `sh run_all.sh` runs are **byte-identical** on all three transcripts, ~4 s.
No `random`, no clock, no float where a rational decides a verdict.
