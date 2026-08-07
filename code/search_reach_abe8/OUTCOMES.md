# `mg-abe8` — outcomes, scored against `PREDICTIONS.md`

Scored after `run_all.sh`. Predictions were committed at `b6e17e8`, before any script of this
instrument existed. Sources: `out_s1_census.txt`, `out_s2_percandidate.txt`,
`out_s3_largen.txt`, `out_s4_reach.txt`, `out_selftestabe8.txt`.

**Score: 10 HELD, 3 MISSED, 2 process-predictions HELD.** The three misses are all in the same
direction and all *against* the constraints: I predicted rigidity and primitivity would prune
even less than they do at `n = 9`, and they prune slightly more. Neither changes anything —
the joint figure is `2.59` bits at `n = 9` and `0.00` bits at `n = 36`.

| # | claim | verdict | measured |
|---|---|---|---|
| **P1** | all four constraints prune LESS at `n = 9` than at `n = 6` | **HELD** | s1/C: rigid `1.640 → 1.131`, width≥3 `0.388 → 0.018`, not-6-thin `∞ → 1.327`, primitive `0.789 → 0.323`. Four of four WEAKER. |
| **P2** | joint surviving fraction at `n = 9` above 5 % | **HELD** | `16.60 %` — `2.591` bits, `0.755` elements of reach |
| **P3** | rigidity prunes `< 1.0` bit at `n = 9`, and decreasing | **MISSED (half)** | `1.131` bits — above my `1.0`. The *decreasing* half held (`1.640 → 1.131`, and `0.00` by `n = 36` in the KR model). |
| **P4** | primitivity `< 1.0` bit at `n = 9`; decomposable fraction in `[3 %, 12 %]` | **HELD / MISSED** | `0.323` bits ✓. Decomposable fraction `20.06 %` ✗ — outside my band, in the direction of MORE pruning. |
| **P5** | width ≥ 3 prunes `< 0.1` bit at `n = 9` | **HELD** | `0.018` bits |
| **P6** | 6-thinness hardest of the four where non-vacuous; `< 2.0` bits at `n = 9` | **HELD** | `3.055` bits at `n = 8` (vs rigid `1.310`), `1.327` at `n = 9` (vs rigid `1.131`). Hardest at both, and `1.327 < 2.0`. |
| **P7** | pruned candidate count at `n = 34` in `[2^215, 2^235]` | **HELD** | `log₂ N(34) − prune = 223.06`. (Total *work* incl. per-candidate cost is `2^245`.) |
| **P8** | reach `13/14` at `10¹³`, `17/18` at `10¹⁹`, `18/19` at `10²¹` | **HELD** | s4/D: `n = 13` at `2^49.6`, `n = 17` at `2^74.7`, `n = 19` at `2^93`. All three inside the predicted pairs. |
| **P9** | shortfall from `10²¹` visits to `n = 34` in `[140, 180]` bits | **HELD** | `245.4 − 93.0 = 152.4` bits |
| **P10** | **pre-committed verdict: the constraints do not prune enough** | **HELD** | joint pruning `0.07` bits at `n = 20`, `0.00` at `n = 36`; reach `n ≈ 19` at a planetary ceiling |
| **P11** | I will recommend a SAT/CP *refutation* hunt as the only actionable positive | **HELD** | §6 of the report does exactly that, and says why it cannot substitute for the absence proof |
| **P12** | `#ideals` at `n = 34` exceeds `2^17`; including it costs ≥ 1 element of reach | **HELD / PARTIAL** | `log₂ #ideals(34) = 0.4564·34 + 1.749 = 17.3` ✓. The reach cost is `log₂ c(34) = 22.35` bits ≈ **1.8 elements** at `g(34) = 12.6`, so ≥ 1 ✓ — but at the *smaller* budgets it costs closer to 2. |
| **P13** | `mg-5998` still unlanded at submit time | **HELD** | `mg show mg-5998` → `Status: available` at run time |
| **P14** | *my likely error*: pruning computed off the EXCLUDED fraction | **AVOIDED** | `prune_bits` is the only formula in `libabe8`; selftest NC1 exhibits the inverted version disagreeing by `19.93` bits vs `1.4e-06` |
| **P15** | *my likely error*: scoring "search infeasible" as "the bound programme is worthless" | **AVOIDED, and overtaken** | The report's §7 says the finding is about the *checking step*. `mg-00a1` has since refuted the bound on that route entirely (pm-onethird, 20:12), so the framing question P15 guarded against is moot — but the guard is why §1 is written as reach-vs-target rather than reach-vs-window. |

## Four defects of my own, kept in the source rather than tidied away

1. **Three selftest assertions were WRONG and the CODE caught them.** I asserted `δ(V) = 1/3`,
   `δ(N) = 1/3` and "V is primitive" for `V` = two minimal elements under one top. All three are
   false: `δ(V) = 1/2`, `δ(N) = 2/5`, and `V` is the ordinal sum `antichain₂ ⊕ point`, hence not
   primitive. The `1/3` anchor `mg-5998` actually names is `E` = 2-chain plus an isolated point
   (extensions `cab/acb/abc`), and that one reproduces exactly. The corrected assertions are in
   `selftestabe8.py` with the error recorded at the site.
2. **The canonical-key docstring I inherited was wrong** and my selftest asserted the wrong
   property because of it. The refined-invariant key is **not** the global lexicographic minimum
   over `S_n` — it differs on `58 of 63` posets at `n = 5`. What it is, and what the enumeration
   needs, is a **complete isomorphism invariant**; the selftest now checks that instead
   (constant under all `n!` relabellings, separates all classes to `n = 6`). Noted, not fixed
   elsewhere: `code/counterexample_probe_24a3/core.py` carries the same overstated docstring,
   though *its own* selftest (`control_canonical_key`) already states the correct property — so
   that is a stale comment, not a defect, and it is out of this ticket's scope.
3. **`prune_at` in `s4` is non-monotone** (`0.46` at `n = 12`, `0.67` at `n = 14`) because the
   KR-model figures are 400-sample estimates and rigidity's density is noisy at small `n`. Left
   in rather than smoothed: smoothing would hide the sample size.
4. **The KR rigidity test is the LAYER-PRESERVING one.** A layer-swapping automorphism would be
   missed, which would make the test report *more* rigid posets and hence *less* pruning — the
   direction that flatters my own conclusion. Disclosed at the function and measured: the
   necessary condition for such an automorphism held on `78 of 4000` samples, so the residual is
   bounded by `2 %` and cannot move a `0.00`-bit figure.

## What this instrument did NOT do

- **No large search was run.** The largest computation is `s1`'s exhaustive `n ≤ 9`
  (183,231 posets, 174 s, one core). Total instrument wall-clock across all four scripts and the
  selftest: **under 7 minutes, single process, one core.** No fan-out, per the mayor's load note.
- **`n = 10` was not enumerated exhaustively.** 2.5 M posets is ~12 min and several GB in this
  implementation and adds one row to a trend already established over four.
- **None of `mg-5998`'s four attributions was verified.** They are used as given and marked
  UNVERIFIED at every site, including inside `libabe8.CONSTRAINTS`.
- **The KR model is not the uniform measure on posets.** Every figure derived from it is labelled
  KR-model. Its agreement with the exhaustive census where they overlap (`n = 10..14`, same
  direction, same order of magnitude) is the only cross-check it has.
- **`δ` was not computed exhaustively above `n = 8`**, and the KR-model `δ` samples above `n = 20`
  are 30 per size. The frozen-census claim is therefore `FP` at `n ≤ 8` and *sampled* above.
- **`mg-00a1` was not touched.** Its result arrived as mail mid-run and changed the framing of §1
  and §7; nothing in the measurement depends on it.
