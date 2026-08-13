# PREDICTIONS — `mg-99f4`, filed before the runs

Filed so that what would have changed the verdict is on record rather than reconstructed. Two
of the five were **wrong**, and both are kept as written with the outcome beside them.

| | prediction | outcome |
|---|---|---|
| **P1** | `LL_n = {L(P)}` is in bijection with the posets, so the consumable restriction of any subset-construction is a function of `P`. | **CONFIRMED** — `s1.1`, injective at `n = 2…5` against A001035. |
| **P2** | All four of `mg-8b32` b2.3's TIER-2 separators have `res = 1` on `LL_n` — constant on every consumable input. | **REFUTED, 3 of 4.** `s1.4`: the BK edge count has `res = 4, 10, 29` at `n = 3, 4, 5`. The prediction was right about T2a/T2b/T2c and wrong about T2d, and the failure is why `s1.6` exists at all — the survivor needed a second, different reason. |
| **P3** | The BK edge count fails to determine `e(P)`, so even its bound is weak. | **REFUTED at `n = 3, 4`.** `s1.6`: it determines `e(P)` *exactly* there; the first ambiguity is one value at `n = 5` (`|E| = 4 → e(P) ∈ {4,5}`). The survivor is **stronger** than predicted and still unconsumable, on cost alone. |
| **P4** | Some construction in the class will pass the two-question screen. | **CONFIRMED-NEGATIVE** — `s1.7`: 0 of 4. Filed as a prediction because a screen that nothing can pass is a screen worth suspecting, and `s1.5`'s T2d row is the vacuity guard on it (`res > 1` is *reachable*, so Q1 is not a tautology). |
| **P5** | `compression2`'s crossover is driven by its constant, so a better constant is the route to non-vacuity. | **REFUTED** — `s2.4`. It is driven by the **reference scale**. Shape `c·n log₂ n` is vacuous below `2^(log₂e/(1−c))` at *every* `c < 1`; shape `c·log₂ n!` bites at every `n` for every `c < 1`. The constant is the wrong dial. |

## What would have refuted the headline

The finding is `s1.3`: separation and consumability are supported on disjoint parts of the
domain. It would have lost if **any** of these had come back the other way, and each was run:

1. `phi_sep` and `phi_blind` failing to agree on all 19 consumable inputs at `n = 3` — they
   agree, so they support literally the same bounds while disagreeing about separation.
2. A construction whose *separating* behaviour changed a bound. None can: `s1.5` computes the
   sharpest bound `B_Φ` from `Φ|_LL` alone, and `Φ|_LL` is what the two variants share.
3. `LL_n → posets` failing to be injective. Then `Φ|_LL` would carry more than `P` does and the
   `mg-8b32` closure would genuinely not reach it. It is injective (`s1.1`, `s0.3`).

## Two things this directory does NOT establish

- **That no consumable construction exists.** The dichotomy says separation cannot *help*; it
  does not say `Φ|_LL` cannot bound `e(P)`. Prefix codes on `L(P)` are exactly such a `Φ|_LL`,
  they are consumable-native, and **neither of today's closures touches them** — both are about
  separation, and a code neither separates nor needs to.
- **That a shape-B bound is achievable.** `s2.5` cites `mg-0fc6` a3.1's five measured points
  (`0.907 … 0.883`, decreasing) as an **existence** statement about the sharpest constant, on a
  population capped at `n = 7`. Five points do not settle a limit and no code achieving them is
  exhibited here.
