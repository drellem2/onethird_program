# `c3_prefix_capture_76b2` — the instrument for mg-76b2 (ATTACK `C₃`)

The **report** is [`docs/OneThird-C3-PrefixCapture-mg-76b2.md`](../../docs/OneThird-C3-PrefixCapture-mg-76b2.md);
this file documents the instrument and scores the predictions.

**Predictions were committed at `0cfae5f`, before any file in this directory except
`PREDICTIONS.md` existed.** Scoring is in §3.

## Running it

    ./run_all.sh          # ~45 s

Exit codes are **pre-registered** in the runner and re-checked against it. Every section
is expected to exit `0`. A section that exits `0` and writes fewer than 20 lines is a hard
failure — "returned 0" and "examined nothing" must be different outcomes.

| file | what it does | expected exit |
|---|---|---|
| `selftest76b2.py` | 22 two-sided red drills over every verdict below | 0 |
| `s1_dictionary.py` | the `ρ ↔ Φ` dictionary, exactly, over 5230 posets | 0 |
| `s2_sweep.py` | the sweep lemma, `monotone ⟹ prefix`, and the theorem | 0 |
| `s3_c3.py` | `C₃` measured in all three currencies, population stratified | 0 |
| `s4_budget.py` | the four chains, and the finite window | 0 |
| `lib76b2.py` | posets, `T_P`, `M`, `Φ_P`, `ρ(A_k)`, Jacobi, the sweep | — |

## Design commitments

- **Written from scratch.** Shares no code with `lib2de0`, `lib_c4f5`, `lib4d3b` or
  `counterexample_probe_24a3/core.py`. `PREDICTIONS.md` H7 records a suspected defect in
  `lib2de0.E_leak`, and an instrument that inherits the library it is checking cannot find
  that class of defect. (H7 is confirmed — §3, P11.)
- **Exact arithmetic for every verdict.** `Fraction` throughout. Floats appear only in the
  Jacobi eigen-routine and in display columns, and every eigen-derived number is labelled
  `FLOAT` at its print site.
- **Cheeger comparisons are squared, never rooted.** `Φ ≤ √(2R)` is checked as
  `Φ² ≤ 2R` in `Fraction`. No verdict passes through `math.sqrt`.
- **The population is stratified before it is measured.** `s3` (C0) establishes exactly
  where `1 − λ_std = 0` *before* any `C₃` figure is printed, because on that
  sub-population every currency of `C₃` is `0/0`.
- **Every `C₃` figure carries the sentence that it is measured outside the regime it would
  be used in**, at its own print site, not once at the top.
- **`σ(A)` is the image of `A`.** Not `set(p[:|A|])`. The other convention is implemented
  as `leak_naive_prefixstyle` on purpose, so P11 is measured rather than argued.

## 3. Prediction scoring — 15 filed, 10 hit, 3 refuted, 2 half

Scored against `PREDICTIONS.md` at `0cfae5f`. **Misses are kept as written**, in both
files.

| # | prediction | outcome |
|---|---|---|
| P0 | `\|P76B2(6)\| = 4824` | **HIT** — 2 / 7 / 40 / 357 / 4824 |
| P1 | the dictionary identity holds with 0 exceptions | **HIT as to substance, and the FORM I filed was WRONG.** H1's `n·Φ/(n−k)` is the `k ≤ n/2` case only; `Φ_P` normalises by `min(\|A\|,\|Aᶜ\|)` and the normalisation switches sides at the median. The script caught it on **9909** (poset, prefix) pairs before the general form `1−ρ = n·leak/(k(n−k)) = n·Φ/max(k,n−k)` was written. The general form: **0 exceptions / 25684** |
| P2 | `Φ ≤ 1−ρ ≤ 2Φ`, and the factor 2 attained "in the limit only" | **HALF.** The inequality: 0 exceptions / 25684, and it holds for **every** `k`, not only `k ≤ n/2`. The second clause is **REFUTED**: `1−ρ = 2Φ` is attained exactly, at `k = n/2`, in **5866** of 25684 cases — every even `n` |
| P3 | `1−λ_std = 0` exactly on the ordinal-sum-decomposable posets | **HIT, and stronger than filed.** Three independent exact predicates — graph disconnected, has a cut point, `Φ* = 0` — agree on **all 5230** posets, 0 disagreements |
| P4 | primitive fraction at `n=6` under 50% | **REFUTED.** 4070 / 4824 = **84.4%** primitive. I had the direction of the split backwards |
| P5 | some primitive poset at `n ≤ 6` has `C₃^cut > 1` | **HIT** — 468 of 4377; first witness `n=4`, `rel=[(0,1),(2,3)]`, `Φ* = 5/12`, `Φ*_pref = 1/2`, ratio `6/5` |
| P6 | `max C₃^cut` grows with `n` across `n = 4,5,6` | **HALF.** Not weakly monotone — `1, 1, 3/2, 6/5, 15/8` for `n = 2..6`, so it **dips at `n=5`**. But it is strictly larger at `n=6` than at any smaller `n`, so the direction of travel is upward. Reported as the negative result it is |
| P7 | monotone dominant eigenvector for "the overwhelming majority but not all" | **REFUTED, and badly.** 1890 YES / 3340 NO / 0 UNDECIDED — monotonicity is the **minority** (36.1%) over the whole population. It is *not* refuted where it matters: stratified by gap it is 35.5% in `[0, 0.25)`, 11.6% in `[0.25, 0.5)`, 2.7% in `[0.5, 0.75)`, and **28 of the 50 smallest-gap primitive posets** are monotone. Monotonicity concentrates exactly where the conjecture claims it |
| P8 | a degenerate top standard eigenvalue somewhere | **HIT** — 163 of 5230. `monotone_in_span` handles it existentially and returned `UNDECIDED` **0** times, so no verdict here rests on a basis choice |
| P9 | no poset in the population is inside the budget | **HIT** — 0 of 4377 primitive posets have `1 − λ_std ≤ 2×10⁻²`; the smallest is `0.05625` at `n=6` |
| P10 | the literal capture fraction `c` falls below the `0.8163` threshold somewhere | **HIT** — 523 of 4069 at `n=6`; `min c` falls with `n`: `0.750, 0.618, 0.536, 0.453` |
| P11 | `lib2de0.E_leak` diverges from the definition on non-prefix cuts | **HIT** — **8178 of 11316** (poset, cut) pairs at `n ≤ 5`. Smallest witness: the 2-chain `0<1` with `A = {1}`, where the definition gives `0` and the other convention gives `1`. NOTED, NOT REPAIRED — mg-2de0 owns that file |
| P12 | the theorem survives every red drill | **HIT** — 1037 of 1037 sweeps of an exhibited monotone eigenvector landed on a prefix-or-suffix cut, worst `Φ²/(2(1−λ_std)) = 0.347` |
| P13 | *my likely error*: the suffix branch. Bet 15% it breaks | **HIT (the worry is REFUTED)** — `\|A∖σ(A)\| = \|Aᶜ∖σ(Aᶜ)\|` on all 48616 (permutation, cut) pairs to `n=6`. `Φ_P` is a function of the cut, not the side |
| P14 | *my likely error*: dropping a Cheeger square that the chain needs. Bet 25% | **STANDS, and is answered by enumeration rather than assertion.** All four chains are stated separately in `s4` (B0) with the reading each belongs to. Op-Form §4.3's displayed relation belongs to the degraded-prefix-Cheeger reading and **not** to the gap-form repair it names in the same sentence |

## 4. Defects of this instrument, kept in the source

Four found by this instrument's own cross-checks, three of them mine and one of them the
class of error the ticket is about.

**D1 — an order-slice is not a level set.** `sweep_sets` originally returned `order[cut:]`
for each cut of the sorted order. Where `f` ties, that **splits the tie** and returns sets
no threshold ever produces. On the antichain at `n = 4` the dominant standard eigenvector
is `(a,a,a,−3a)` — monotone, ties everywhere — and the old routine offered `{1,2}` and
`{2}` as "threshold sets" of it. `s2` (S3) duly reported three monotone sweeps landing
outside the prefix family. **The sets were the artifact; the theorem was not.** The error
direction is stated rather than buried: too many sets makes the sweep lemma (S1) *easier*
and the prefix claim (S3) *harder*, so (S1)'s clean pass under the old routine was
flattered and had to be re-run. Fixed in place, kept in the docstring and in the history.

**D2 — the min/max normalisation slip, made twice in one prediction file.** `Φ_P`
normalises by `min(|A|,|Aᶜ|)`. `PREDICTIONS.md` H1 wrote the dictionary as `n·Φ/(n−k)` and
H8 wrote the antichain conductance as `(n−|A|)/n`; **both are the `≤ n/2` case only**, and
both were caught by the machine — H1 by 9909 failing pairs in `s1`, H8 by a red drill in
`selftest76b2`. Kept as written in `PREDICTIONS.md`, corrected at the check sites. This is
the same slip twice in the same file, which is why it is listed as one defect and not two.

**D3 — five of 22 red drills had their mutation arm written as the mutant claim rather
than as its refutation**, so `drill(...)` received `False` where it needed "the mutation
was caught". The harness caught them because it demands *both* arms; a one-sided harness
would have printed 22 ok. The drills were rewritten, not deleted.

**D4 — `connected()` was defined inside `s3_c3.py` and imported by the selftest**, which
executed the whole of `s3` as a side effect of the import and interleaved its 116 lines
into the selftest transcript. Moved into `lib76b2`. Trivial, and recorded because a
selftest whose transcript is polluted by the thing it is testing is not independent of it.

## 5. Not done

- **`n = 7` is not swept.** The population is ~96k posets with up to 5040 linear
  extensions each; the exhaustive `Φ*` over `2ⁿ` cuts puts it out of budget here. Every
  `n`-growth statement in `s3` (C2) rests on `n = 2..6` and says so. **A finite population
  cannot establish a bound uniform in `n` in any case — only refute one.**
- **No feasibility solver for the degenerate case.** `monotone_in_span` is a one-sided
  positive test (basis vectors, then the projection of the source's own centred
  expected-rank observable). It returned `UNDECIDED` 0 times here, so nothing rests on it,
  but at larger `n` it could.
- **`lib2de0` is not repaired.** P11 is reported where it was found.
- **No `STATE.md` edit.** `STATE.md:15` and `:164` are pm-onethird's rows; the correction
  to `:164`'s rider is a proposal in the report, mailed, not landed.
- **`λ_std` is never certified exactly.** Jacobi is float. Every exact verdict is
  arranged to avoid it: the dictionary, the stratification, `C₃^cut` and the whole of `s4`
  use no eigenvalue at all.
