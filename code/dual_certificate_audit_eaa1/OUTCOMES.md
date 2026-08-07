# `mg-eaa1` — outcomes, scored against `PREDICTIONS.md` (`61f7f5b`)

Predictions were committed **before any script of this audit existed** and before one byte of
`code/dual_certificate_131e/`, of `docs/OneThird-DualCertificate-mg-131e.md`, or of `STATE.md`
was read. Seven prior exposures were disclosed there as `H1`–`H7` rather than laundered into
predictions; the ones that make a "hit" below cheap are re-flagged at the line.

**14 held, 2 missed, 3 error-predictions did not fire.** The two misses are `P8a` and `P12`,
and `P12` is the one that mattered: I bet near-even that the parent had conflated the
relaxation with the truth, and it had not.

| | prediction | conf. | outcome |
|---|---|---|---|
| **P1** | the instrument has the house shape (`PREDICTIONS`/`README`/`out_*`) | 85% | **HELD** |
| **P2** | every published certificate verifies under my substitution | 80% | **HELD in substance, with `F1`** — every count reproduces exactly, but the tier-2 *vectors* are not committed, so "verify theirs" was not literally available; I built my own family instead. See §2.1 of the audit document. |
| **P3** | tier 0 (trivial) certifies the attaining branch at `n = 3` and `n = 4` | 70% *(informed by `H2`, not blind)* | **HELD** — `d1` reports `tier=0` on the attaining branch at both, and my run agrees. |
| **P4** | at `n = 5` the trivial dual does not attain; the certificate there is non-trivial | 60% *(informed by `H2`)* | **HELD** — both informative hard branches have trivial bound `5/3` against `val = 4/3`, and `λ = 0` is *provably* unavailable there (§4.1). |
| **P5** | the certified program is the DISJUNCTIVE one: non-empty `C`, feasible, attaining | 90% | **HELD** — checked four ways in `a1_program.py`. |
| **P5a** | a certificate on a `C = ∅` branch at `n ≥ 3` scores check 2 **FAIL** | 95% | **HELD, and the rule needed the refinement I wrote into it.** `d1` *does* certify the `C = ∅` branch — it is one of the `2^C(n,2)` — but classes it `infeasible` and counts it as **vacuous** on its own `tier × primal class` line. Nothing in the result rests on it. The rule as I wrote it ("if I find any certificate whose branch has `C = ∅`") would have mis-fired had I applied it to the *presence* of the branch rather than to what the *result rests on*; recording that so the pre-commitment is not read as cleaner than it was. |
| **P6** | the verdict is NEITHER of the ticket's two offered answers | 75% *(a **REPRODUCTION**: `H1`/`H2`/`H3` told me twice before I began)* | **HELD** — recorded only to date-stamp that I could not have discovered it. |
| **P7** | the `n = 6` refutation is a primal witness, not an exhaustive sweep | 65% | **HELD** — five hard-coded measures, `d3` touches no LP. |
| **P8** | I independently construct a legal `n = 6` branch with `E[inv] > 5/3` | 70% | **HELD** — `56`-branch declared probe, `4` branches beat `5/3`. |
| **P8a** | the `n = 6` value is `≥ 2` | 40% | **MISSED, kept as written.** Every branch I probed tops out at `11/6` — `8` branches beat `5/3` over the `386` of the `\|S\| ≤ 4` family and **all `8` are at exactly `11/6`**. I was predicting a magnitude and the magnitude is smaller than I guessed. |
| **P8b** | my witness has the same value as theirs | 30% | **HELD, and stronger than predicted** — not merely the same value: my solver's optimum on the `S = {(1,4)}` branch is `mg-131e`'s published 6-atom measure **atom for atom and mass for mass**, found without reading it. I had this at 30% precisely because I expected to find *a* violating branch rather than *theirs*. |
| **P9** | the normalisation is EQUALITY `Σ μ = 1`, checked in code not in prose | 80% | **HELD** — `lp200d.build` emits `("==", 1)`; `mg-131e` uses `build` verbatim; my independent builder emits `"=="` too and the two row sets are identical in content and order. `mg-ba78`'s sub-probability trap is not present. |
| **P10** | no tightness claim crept in | 70% | **HELD** — and the numbers under it re-derived: `1/3` at `n = 3` (in `M_3`, attains); `2/5`, `4/11`, `5/14` at `n = 4, 5, 6` (none in `M_n`). |
| **P11** | the `≥` / `≤` split survives | 70% | **HELD** — split typographically in the parent's §0 table and by kind in `STATE.md` row 167. |
| **P12** | **some user-facing sentence conflates "the relaxation's value exceeds `(n−1)/3`" with "`ε_spec ≤ 2/(n+1)` is false"** | 45% — *"I am betting near-even that this is where the defect is, and I am pre-committing to raise it even if every rational number checks out"* | **MISSED. The conflation is not there.** `d3`'s docstring, the document's §5.1 and `STATE.md` row 167 all carry the distinction explicitly and in the same words I would have used: the disjunctive value is an **upper bound**, and a larger upper bound weakens the bound without touching the statement underneath. I was wrong, the parent is cleaner than I bet, and this is the prediction I most wanted to be wrong about. |
| **P13** | no poset enumeration, no transitivity imposed | 85% | **HELD** — transitivity appears once, as a checked property of the *answer*. |
| **P14** | `STATE.md` at `491d42c` carries the refutation **at** the claim | 60% | **HELD** — row 167's own headline says `REFUTED … AND IT IS FALSE, NOT CONJECTURAL`; all four `2/(n+1)` occurrences and every retired threshold are inside sentences that retire them. |
| **P15** | *my most likely error*: I score a sign convention as mathematics | 35% | **DID NOT FIRE, and the guards are the reason it could not.** Guard (i) fixed my conventions in `lib_eaa1`'s docstring before the parent's format was opened; guard (ii) then showed my rows are `lp200d.build`'s rows **in content and in order**, so no transformation was ever needed and guard (iii) had nothing to do; guard (iv)'s mutation control (shave, sign-flip, wrong length, and a *negative on a free row that must NOT be a violation*) fires correctly. |
| **P16** | *second error*: I score a verified trivial dual as vacuous | 30% | **DID NOT FIRE.** Scored `PASS with a note` per the pre-commitment, and the separate question was asked: the trivial dual **does** cover the attaining branch at `n = 3, 4` and **does not** at `n = 5`. |
| **P17** | *third error*: I audit a branch by its label, not by its columns | 25% | **DID NOT FIRE.** `check_measure` asserts no comparable pair carries flip mass, and selftest mutation 3 confirms it rejects a measure that puts mass on a comparable flip. |

---

## A defect of THIS instrument, kept in the record

`lib_eaa1.columns` filters `n!` permutations. `a3_n6.py`'s A3.1 loop runs to `n = 12`, so the
first run of that script spent **two and a half minutes enumerating `12! ≈ 4.8×10⁸`
permutations and producing nothing** before I killed it. The repair is
`columns_consecutive_branch`, which generates that branch's columns directly (they are the
matchings of the path on `n` vertices — Fibonacci-many), and it is **cross-checked against
brute-force filtering of `n!` at every `n ≤ 8`** rather than trusted. `active_pairs` had the
same latent cost and now accepts the column list.

Worth naming for what it is: the failure produced **no output at all**, which is the benign
shape. The dangerous version of the same bug is one that returns a *smaller* column set
silently — which is exactly what the `n ≤ 8` cross-check exists to catch, and why it is in the
transcript rather than in a comment.

---

## The four findings, and their direction

| | finding | direction |
|---|---|---|
| `F1` | tier-2 multiplier vectors are regenerated at run time, not committed; the artefact for `1/18/388` branches is a **count**, not a certificate | against — but substance confirmed independently, and my transcript supplies the missing vectors |
| `F2` | `d2`'s "optimum flips only consecutive pairs" caveat is in the **transcript** and dropped in the **document §4** and **`STATE.md` row 167** | **resolves for the parent** — settled here over the whole optimal face of all 52 branches: max non-consecutive flip mass is `0`, so the unqualified sentence is true |
| `F3` | `d2` PART C's `λ ∈ [−1995/2, −1]` is printed on a row not marked `(boxed)`, but `−1995/2` **is** the `±1000` box; unboxed, `λ → −∞` | cosmetic — the conclusion rests on `max λ = −1`, which is exact and genuine |
| `F4` | document §5's *"false from `n = 6`"* reads as all `n ≥ 6`; §7 and `STATE.md` say plainly that it is not established | local, corrected downstream |
