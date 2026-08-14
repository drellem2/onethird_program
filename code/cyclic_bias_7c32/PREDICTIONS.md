# PREDICTIONS — mg-7c32, the cyclic-orientation bias

## §0 What was ALREADY MEASURED before any prediction was written, and is therefore not one

A prediction of something already run is a record of nothing. These were settled during
scoping, by hand or by grep, before the arms existed:

- **The dedup search itself.** `grep` over the whole tree for `cochain`, `coboundar`,
  `cyclic`, `telescop`, `3-cycle`, `linear ordering polytope`, `XYZ`, `FKG`, `Shepp`,
  `Kahn`. The result is P8 below and it is recorded as a **refutation of the ticket's own
  standing assumption**, not as a prediction of mine.
- **Steps 1–3 were re-derived on paper** before any code was written, and all three came
  out correct. So P1–P3 are predictions that a correct derivation would survive an
  exhaustive machine check — which is worth running and is not a hard prediction.
- **`db = 1/2` on a chain triple** was noticed on paper (all three marginals are 1) and is
  the origin of P4.

## §1 The predictions, with what happened

| # | Prediction | Outcome |
|---|---|---|
| P1 | Step 1's identity `db = Pr[cyclic] − 1/2` holds exactly at every ordered triple of every poset `n ≤ 7`, by two routes sharing no line | **CONFIRMED** — c1 §2, 471 804 triples, 0 disagreements |
| P2 | `N = #{x<y, y<z, z<x}` takes only the values 1 and 2, over every word of every `L(P)` | **CONFIRMED** — c1 §1, values observed exactly `[1, 2]` |
| P3 | The step-3 telescope is an exact identity at every base point and for every chain, including chains that are not linear extensions | **CONFIRMED** — c2 §1 (152 609 telescopes) and c2 §4 (39 426, every permutation at `n ≤ 5`) |
| P4 | `db = 1/2` is attained, on chain triples, so step 4's target is **false unconditionally** and must be a statement about the counterexample class | **CONFIRMED, and sharper than predicted** — c1 §3: on this population `db = 1/2` holds at the chain triples and **nowhere else** (43 644 ordered triples = 3 × 14 548 chains) |
| P5 | The bracketing freedom the ticket names as an unspent resource moves the defect total `D`, so a good bracketing could reduce it | **REFUTED** — c2 §2. `D` is bracketing-**invariant**: 19 441 of 19 441 posets reach the same `D` under the star and under the balanced tree, while 19 392 of them visit a *different* multiset of `db` values. Rebracketing redistributes the defect and cannot change its total, because `D` is defined as a difference of two quantities neither of which mentions the bracketing. One of the ticket's two free resources buys nothing. |
| P6 | On the extremal class (`δ(P) = 1/3`) the measured average `db` sits within `1/(n−2)` of step 3's own floor `(n−4)/(6(n−2))`, because §2 says the average is the mean consecutive bias to that precision | **REFUTED** — c3 §4. At `n = 8` the smallest average over the 12 extremal posets is `5/18 ≈ 0.2778` (`7/30 ≈ 0.2333` with the base point spent well) against a floor of `1/9 ≈ 0.1111`: slack `11/90`, an order larger than predicted. The prose in c3 §4 was rewritten to what ran. The refutation is in the **direction that hurts step 4 more**, not less — 0 of 12 reach the target at any base point. |
| P7 | The invariant cut in `Poset.canonical_key` leaves the key string unchanged, so a string comparison against the unrestricted key is a valid control | **REFUTED, on this directory's own first run** — the strings differ on 82 labelled posets at `n ≤ 5` and c1 §0 went red on its own arm. The cut is a valid *canonical form* (constant on isomorphism classes and separating them) but not the lex-least one. The control was replaced by the claim that was actually being made — the two keys induce the same **partition** — which passes. A control asserting the wrong invariant is the failure this table exists to keep visible. |
| P8 | The corpus search returns nothing, as the ticket states (`a dedup search on "cyclic order", "triple bias", "3-cycle probability", "linear ordering polytope" returned nothing here`) | **REFUTED** — `docs/BASIC-FACTS.md`, landed at `73af2f3` the **same night** as this ticket was filed, carries the ticket's step 1 triangle-inequality half as **fact 1**, its step 2 verbatim as **fact 2**, and its step 3 with `D = 0` as **fact 3**. The ticket's own vocabulary is why the grep missed it: that file says *coboundary* once and *cyclic* never. |
| P9 | No poset at `n ≤ 8` has `δ(P) < 1/3`, so every measurement here is off the counterexample class and none of it is evidence about that class | **CONFIRMED** — c3 §1, the minimum `δ` is exactly `1/3` at every `n = 3..8`. Both directions of this are stated where they matter: c3 §3 warns against reading the 95.4% below `1/6` as support, and c3 §4 warns against reading its own contrary result as refutation. |
| P10 | Relaxing the majority threshold from `2/3` to `1/2` will be **invisible** on this population, so c3 §1's `0 cyclic` does not test the band | **CONFIRMED** — c0 D6, the required-inert plant. The instance the population cannot supply is `mg-24a3`'s `n = 11` majority cycle. |

## §2 What this table does not do

It does not make the arms right. Five of ten were settled or half-settled on paper before
being run, and the two that carry the weight of the write-up — P5 and P6 — are both
**refutations of my own expectation**, which is the only reason they are worth the space.
Nothing here checks that the table was filled in honestly.
