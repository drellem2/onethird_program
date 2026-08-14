# Pre-registered predictions — `mg-872c`

**Committed before one line of `k0`, `k1` or `k2` existed.** The ticket asks for a scoping
recommendation on the one object `mg-9d9e` left standing: *a bound on a code's expected length
PROVED FROM hypothesis (1)*. It also says, in as many words, to check `mg-9b6b` and `mg-0b96`
**before building anything**, because *"the same dial may already have a number on it."*

It has two numbers on it already. §0 says which, and says which of the figures below were taken by
hand during scoping — **a prediction of something already run is a record of nothing** (`mg-365a`,
`mg-3c92`, `mg-68ef`).

---

## §0. WHAT WAS ALREADY RUN OR READ DURING SCOPING, AND IS THEREFORE NOT PREDICTED

**Read from the record, not measured here:**

- **`mg-6ff4` `c1` `m4`** publishes the STRUCTURE of the boundary class in closed form: *a boundary
  poset on `n` elements is `k ≥ 1` copies of `V` ordinally summed with `n − 3k` singletons*, with
  counts `Σ_k C(n−2k, k)` — **exhaustive to `n = 9`**, and `c2` carries it width-restricted to
  `n = 10` (`w ≤ 3`) and `n = 12` (`w ≤ 2`). Every arithmetic consequence below is a corollary of
  that sentence and **is not a new census**.
- **`docs/FACTS.md` F19** banks the width-2 half: *"at `δ(P) = 1/3` … the class has width 2 at
  every member and contains no 3-element antichain"*, `FP` at `n ≤ 8`, 31 members.
- **`mg-c47a` Obs 3.1(a)/(b), audit-CONFIRMED** (`docs/state-history/attempt-mg-c47a-drop.md` H1):
  *"low `δ` forces width ≤ 2"* is **logically equivalent to the conjecture** modulo Sah. ⚠️ The
  same record REJECTS the inference the deliverable drew from it (*"a programme pursuing it goes in
  a circle"* — *equivalence of statements says nothing about difficulty of proofs*), and nothing
  here re-runs that inference.
- **`mg-9d9e` §3.1**: `MERGE-P` and `MINIMALS` are equal on the boundary family, both at `5/3` bits
  per block against a truth of `log₂ 3`. `mg-9d9e`'s own **P5 predicted a separation here and was
  REFUTED**.

**Measured by hand during scoping (four figures, all reproductions of the above):**

| figure | value | already on record as |
|---|---|---|
| `|{δ(P) ≤ 1/3, non-chain}|`, `n = 3…8` | `1, 2, 3, 5, 8, 12` | `mg-6ff4` `c1`; sums to F19's **31** |
| `max e(P)` over that class, `n = 3…8` | `3, 3, 3, 9, 9, 9` | new as a figure, corollary of `c1` `m4` |
| `max w(P)` over that class, `n = 3…8` | `2` at every `n` | **F19**, already banked |
| the argmax at `n = 8` | `V ⊕ V ⊕ chain(2)` | `mg-9b6b` §3's family, chain-padded |

**So `P1`–`P10` are about what has NOT been run.**

---

## The predictions

**P1 — the identity every number downstream is arithmetic on.** `e(P) = 3^k` at every member of
`{δ ≤ 1/3}`, `n ≤ 8`, with `k` the number of `V` summands, re-derived through a decomposition
written here rather than through `lib6ff4.ordinal_summands`. ⚠️ **Expected CONFIRMED and it is
corroboration of `mg-6ff4` `c1` `m4`, not news** — recorded because if it fails, every figure in
`k2` is about something else.

**P2 — the code the ticket asks for, priced.** `MINIMALS` (imported verbatim from `lib9d9e`, not
re-spelled) has `E[len] = 5k/3` **exactly** at every member of the class, hence exactly
`(5/3)/log₂ 3 = 1.05155×` the entropy **at every member, independent of `n` and of `k`**.

**P3 — ⚠️ EXPOSED, and exposed where its predecessor was refuted.** `MERGE-P` **ties** `MINIMALS`
at every member of the class. `mg-9d9e`'s P5 predicted a separation in this exact area and came
back a tie; this predicts the tie and can be refuted by a separation in either direction.

**P4 — `MINIMALS` is optimal at `k = 1` and NOT at `k ≥ 2`.** The optimal prefix code on `3^k`
equiprobable words has `E[len] = L + 1 − a/m` with `m = 3^k`, `L = ⌊log₂ m⌋`, `a = 2^{L+1} − m`:
`5/3` at `k = 1` (tie) and `29/9 < 10/3` at `k = 2` (strict). So `MINIMALS`'s `5.155 %` is **not**
all prefix-integrality, and the gap opens from the second `V` on.

**P5 — the benchmark's looseness on this class is UNBOUNDED, not `1.893×`.** `w(P) = 2` on the
whole class, so `n log₂ w(P) = n` bits, and the ratio to the truth is `n/(k log₂ 3)`: **maximal at
`k = 1`, where it grows like `n`**, and minimal `n/(⌊n/3⌋ log₂ 3) → 1.893` at `k = ⌊n/3⌋`.
`mg-9d9e` §5.3's benchmark is order-optimal only at the top of the class.

**P6 — no shape-A bound can be contradicted here.** With `compression2`'s
`c = 1 − 1/(24 ln 2)`, `c·n log₂ n > log₂ E(n) = ⌊n/3⌋ log₂ 3` at **every** `n ≥ 3`, by a ratio
that grows without bound and is already `≥ 4` at `n = 12`. Hypothesis (1) moves `e(P)` in the
direction that makes a shape-A target **easier**, so satisfying it costs nothing and refuting it is
unavailable.

**P7 — `Q1′` has no bite on the object it was written for.** `MINIMALS` at the antichain has
`E[len] = log₂ n!` exactly at `n ≤ 8` (it passes `Q1′`), and `δ(antichain) = 1/2` at every
`n ≥ 2`, so the antichain is **outside** hypothesis (1). A bound *proved from hypothesis (1)* is
never asked about the antichain, so `Q2′` is the whole surviving test.

**P8 — the machinery is not returning a degenerate answer.** The `δ ≤ 2/5` class is non-empty at
`n = 4…8`, contains members of **width ≥ 3**, and its `max e(P)` is **strictly above** `3^{⌊n/3⌋}`
at every `n ≥ 5`. Without this the headline is indistinguishable from a sweep that silently
narrowed to nothing (`mg-9b6b`'s must-FIRE control, one subject along).

**P9 — `EMPTY` is printed and `0` is not.** The frozen class `δ < 1/3` is empty at every `n ≤ 8`
and every arm says `EMPTY`, never `0` (`mg-9b6b`'s carry-forward; `mg-3c92` measured that this
estate already does it at 9 sites in 10).

**P10 — the strongest form of "there is nothing left to bound".** On this class even the
**OPTIMAL** code passes `Q2′`: its expected length is a closed-form function of `P`, needing only
`e(P) = 3^k`, and `k` is read off the decomposition in polynomial time. Where the optimal code is
consumable, a *bound* on a code's length is not an object anyone needs.

---

## What would make this directory wrong

- **Everything above is `FP` and inherits `mg-6ff4`'s reach**, not more: exhaustive `n ≤ 9`,
  width-restricted to `n = 12`. A boundary poset of width `≥ 3` at some `n ≥ 13` breaks `P1`,
  `P2`, `P5` and `P10` at once — and finding one would be far bigger news than this ticket.
- **The frozen class is empty at every `n` reached.** ⚠️ Nothing here is a measurement on it. That
  emptiness is the subject, not a caveat on the numbers (`mg-9b6b` §0's wording, deliberately).
- **`P3` imports another directory's code.** If `lib9d9e`'s `rel` ↔ `lib6ff4`'s `down` conversion
  is wrong, `P2` and `P3` are about a different poset than `P1` is. `k0` asserts the conversion
  both ways before any arm uses it.
