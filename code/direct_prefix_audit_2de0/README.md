# `direct_prefix_audit_2de0` — the instrument for mg-2de0

Independent audit of the mg-00b9 direct-prefix route (Lemma A / Lemma B). The **report** is
`docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md`; this file documents the instrument.

**Predictions were committed at `e9702ee`, before any file in this directory except
`PREDICTIONS.md` existed.** Scoring is in §3 below.

## Running it

    ./run_all.sh          # ~3.5 min, A5 is the slow section (98442 posets)

Exit codes are **pre-registered** in the runner and re-checked against it. Note `a2` is
expected to exit **1**: its headline finding is that Lemma B's second inequality is false, so an
exit 0 there would mean the detector stopped detecting.

| file | what it audits | expected exit |
|---|---|---|
| `selftest2de0.py` | 64 two-sided red-drills over every verdict in the audit | 0 |
| `a1_lemma_a.py` | Lemma A, derived from the definitions | 0 |
| `a2_lemma_b.py` | Lemma B's **three** inequalities, scored separately | **1** |
| `a3_nonvacuity.py` | Priority 2: `2/3` vs `1/2` vs `√2`, and like-for-likeness | 0 |
| `a4_requirements.py` | Priority 3: the `3/ε_leak` comparison | 0 |
| `a5_linial.py` | item (e): width ≤ 2 ⟹ `δ ≥ 1/3`, as used | 0 |
| `lib2de0.py` | posets, `Kₖ`, footrule, `inv_e`, `Δ₁`, `Φ_P`, `δ`, the `β`-range | — |

## Design commitments

- **Exact arithmetic.** `Fraction` throughout. Floats appear only in display columns, never in
  a comparison that produces a verdict. (This was violated once and fixed — §4.5 of the report.)
- **Every count names its POPULATION and its GRAIN** at the print site, and the label is
  generated from the loop's own counter (`f"{tot}"`), not typed in. Two labels that were typed
  in were wrong; see §4.2 of the report.
- **Three inequalities, three verdicts.** Lemma B is scored as I1/I2/I3 separately, and the
  *proof gap* in I2 is reported separately from whether it produces a *false bound*. Collapsing
  those two is how a false inequality survives an audit that concludes "the algebra checks out".
- **Two-sided closure.** Every check is drilled going red on a constructed input. An audit that
  can only print OK is indistinguishable from one that checks nothing.
- **No truncation anywhere on an output path.** No `head`/`tail`/`sed` in `run_all.sh`, and a
  section that writes fewer than 10 lines is a hard failure regardless of its exit code —
  because "returned 0" and "examined nothing" must be different outcomes.
- **`λ_std` is never computed.** Only the corpus's master *bound* on `1 − λ_std`, named as a
  bound at every use. Everything here is the **transport** axis; the one appearance of `δ` is in
  `a5_linial.py`, where it belongs.

## 3. Prediction scoring — 15 filed, 12 hit, 2 missed, 1 partly wrong

Scored against `PREDICTIONS.md` at `e9702ee`. Misses are kept **as written**.

| # | prediction | outcome |
|---|---|---|
| P1 | Lemma A: 0 exceptions | **HIT** (0 / 5912 permutations, 0 / 13815 pairs) |
| P2 | `STATE.md:28` off by 2 under the pinned reading; 1 site, no normalisation stated | **HIT** |
| P3 | I1: 0 exceptions | **HIT** (0 / 3443 cells) |
| P4 | I2 fails; at β=0 exactly the odd `n` | **HIT** (62 / 183; odd `n` exactly) |
| P5 | I2 composite is false on a real poset, with a further witness at `n ≥ 5` | **HIT** (17 / 3443; `n=5` at β=0, three posets) |
| P6 | I3 outer **survives at β=0** and fails at some β>0 | **HALF WRONG.** The β>0 half hit (8 falsifications). The β=0 half is **REFUTED**: 2 witnesses at β=0. I predicted DG's slack would absorb the deficit; at the witness DG's slack is **exactly 0**, which is why it does not. This is the audit's headline and I predicted against it |
| P7 | the repair holds with 0 exceptions and gives exactly `2/3` at every antichain | **HIT** |
| P8 | master bound `= 1` at the antichain ⟹ spectral vacuous *before* Cheeger | **HIT** (0 / 13) |
| P9 | `Φ_P ≤ 1` always; `Φ* ≤` prefix minimum always | **HIT** (0 / 12702; 0 / 431) — and a stronger positive not predicted: `Φ* =` prefix minimum **at the antichain**. ⚠️ **BOTH HALVES SURVIVED A REPAIR OF THE INSTRUMENT THAT SCORED THEM (mg-8311)**: `E_leak` read the first `|A|` **positions** instead of the positions **indexed by** `A`, so every `Φ` in this audit was computed by the wrong convention. Both halves re-verified at `0 / 12702` and `0 / 431` under the repaired reading — and they were never at risk, for reasons provable by hand (the convention's leak is `\|A∖P\| = \|P∖A\| ≤ \|Aᶜ\|`; and `Φ*` minimises over a family containing the prefixes, where the two readings agree). **What DID move is the figure inside A3.4: `strictly smaller on 65 of 431` is now `16 of 431`.** See `code/eleak_repair_8311/` and `docs/OneThird-Eleak-Repair-mg-8311.md`. |
| P10 | ratio is `3(1−4β²)/ε_leak`; headline is β=0-only; 11.25× not 15× at β=1/4 | **HIT**, with an exception I did not predict: at `n = 3, 4` the β=1/4 window is vacuous and `M ≥ 3` survives |
| P11 | (b) holds at β=0, degrades to `0.919/√μ` at β=1/4, no crossover | **HIT** |
| P12 | `n²` vs `(n²−1)`: corpus form stricter, so mg-00b9 understates its own advantage | **HIT** |
| P13 | five limit-form sites (`:13,:21,:57,:62,:86`); brief's `:56` is node B | **HIT** |
| P14 | C→D arrow is `:63` not `:65`; substance confirmed | **HIT** |
| P15 | Linial-as-used: 0 exceptions on width ≤ 2 with an incomparable pair; needs a non-chain rider | **HIT** (0 / 3210; 12 chains skipped as malformed) |

**Two figures I got wrong and am not laundering:**

- **P6** predicted the opposite of the audit's central finding. The prediction was filed before
  any script existed and it is wrong; it is kept verbatim in `PREDICTIONS.md`. The reason it was
  wrong is worth more than the prediction: I assumed Diaconis–Graham always has slack to spend,
  and at the falsifying witness `2E[inv] − E[D] = 0`.
- **`PREDICTIONS.md` P1 says "5913 permutations"**; `2+6+24+120+720+5040 = 5912`. Arithmetic
  slip in my own predictions file. The predictions commit is **not** amended; the selftest now
  drills the correct value (`S9`).

## 4. Defects of this instrument

Seven, recorded in §8 of the report. The one worth repeating here: **`run_all.sh` v1 returned
exit 0 having executed no section at all** (`declare -A` does not exist in macOS bash 3.2; under
`set -u` it died on line 21 and the caller still saw 0). That is the exact
returned-0-vs-examined-nothing defect this arc has been repairing, committed by this instrument
in its own runner on its first execution. The fix is an examined-nothing guard that does not
trust exit codes, and the history is kept in the runner's header rather than erased.
