# `mg-131e` — outcomes against `PREDICTIONS.md`

Predictions committed at `7dc374c`, before any script of this instrument existed. Nothing
below edits a prediction; refuted ones are scored and kept as written.

## Hand measurements (§0 of `PREDICTIONS.md`)

| # | claim | outcome |
|---|---|---|
| H1 | the object is a max over branches, so the certificate is a *family* | **HELD** — `d1` covers all `8 + 64 + 1024` branches |
| H2 | the trivial dual is feasible in **every** branch at **every** `n`, bound `\|I_active\|/3` | **HELD** — proved in `lib131e`'s docstring, machine-checked on every branch at `n = 3,4,5` (`S3`, and `d1` asserts it on all 1096) |
| H3 | hence only branches with `\|I\| ≥ n` carry content; counts `1 / 22 / 638` | **HELD on the reduction, REFUTED on the counts.** The right statistic is `\|I_active\|`, not `\|I\|`: the branches actually needing more than the trivial dual are `1 / 18 / 388`, not `1 / 22 / 638`. My counts were of the wrong set — `\|I\| ≥ n` over-counts, because an incomparable pair no column flips carries no cap row. Kept as written. |
| H4 | the trivial dual certifies the attaining branch at `n = 3,4` and **fails** at `n = 5` | **HELD, and sharpened by the machine.** It fails on the two attaining branches `mg-200d` reports — and there are **four** attaining branches at `n = 5`, and on the other two (`I_active` = exactly the 4 consecutive pairs) the trivial dual is **tight at `4/3`**. `mg-200d` reports the first in enumeration order, which is a smallest-`\|C\|` one, so this was invisible in its transcript. |
| H5 | `(0,4)` is inactive in that branch, so the refined trivial dual gives `5/3`, still `> 4/3` | **HELD, exactly** — `active_pairs` returns the 5 pairs predicted, bound `5/3` |
| H6 | `E[inv] = E[des] = 4/3` on the `n = 5` witness; the slot identity alone is not the certificate | **HELD** |
| H7 | the `n = 5` witness puts `1/3` on each of the `n−1` consecutive pairs and `0` elsewhere | **HELD** — and it holds at **every** value-positive branch at `n = 5`: `0` of `52` optima flip a non-consecutive pair. That is what made the `n = 6` refutation, where a non-consecutive pair carries `1/6`, worth looking for. |

## Predictions

| # | outcome | note |
|---|---|---|
| P1 | **HELD** | `2/3, 1, 4/3` reproduced (`S2`) |
| P2 | **HELD** | trivial dual verifies on 100% of branches at `n = 3,4,5` |
| P3 | **HELD** | every branch certified, `0` failures, at all three `n` |
| P4 | **REFUTED** | I predicted the trivial dual would be *insufficient* on the single `\|I\| = 3` branch at `n = 3`. It is: that branch needs tier 2. But I framed it as "`n = 3` needs the infeasibility or a real dual", implying content — the branch is infeasible, so its certificate is **vacuous** and `n = 3` has **zero** informative hard branches. The prediction was right on the mechanics and wrong on the significance. |
| P5 | **REFUTED on the number** | `638` was `\|I\| ≥ n`; the real count is `388` (H3). The qualitative half — "still in the hundreds" — holds. |
| P6 | **HELD, and it is the load-bearing caveat** | `386` of the `388` are primal-infeasible: **99.5% of the hard certificates are vacuous** |
| P7 | **HELD** | `0` informative hard branches at `n = 4`, `2` at `n = 5` (I predicted `0` and `≤ 20`) |
| P8 | **HELD** | the pre-committed verdict — that the honest answer is **neither** of the ticket's two offered answers, because the informative sequence is `0, 0, 2` and one point is not a pattern |
| P9 | **HELD** | the structural uniform statement exists and is stronger than I predicted: it is a **theorem at every `n`** (`d2` PART A), and it does **not** cover the branches with `\|I_active\| > n−1`, exactly as predicted |
| P10 | **HELD** | max certified bound over branches is exactly `(n−1)/3` at all three `n` |
| P11 | **REFUTED, and this is the finding** | I predicted `n = 6` would not be attempted. Exhaustive `n = 6` still is not — but a **targeted, declared, non-exhaustive** probe of the one family the certificate analysis identified as load-bearing was run, and it **refuted the conjecture at `n = 6`**. Predicting that I would not look was the wrong call; the ticket forbids more brute force, not more thought. |
| P12 | **fired, and was caught by the design it was filed against** | vacuity is 99.5% of the hard certificates. Every count in `d1`/`d2` is split by primal class because of this pre-filing. |
| P13 | did not fire | the sign conventions are right; `P2` (100% on the trivial dual) and `S9` (cap-row labelling) are the controls that would have caught it |

**Score: 6 held of 7 hand measurements (one refuted on its counts, one sharpened against me);
8 held and 3 refuted of 11 predictions; 1 of 2 pre-filed errors fired and was contained.**

The refutations that mattered are `H3`/`P5` (I counted the wrong set), `H4` (the machine found
two attaining branches I had not seen, and they make the `n = 5` certificate *look* better than
it is), and `P11` (I pre-committed to not attempting `n = 6`, and attempting it in a targeted
way is what produced the result).

## Defects of this instrument, kept in the source

1. **The consecutive-pairs dual (tier 1) buys exactly nothing, at every `n` tested.** It was my
   first structural guess — `t` = indicator of the pairs `(i,i+1)`, which gives exactly the
   right objective `(n−1)/3` — and it is dominated by the trivial dual on every branch where
   the trivial dual already works, and *provably unavailable* on the two branches where one
   would want it (`d2` PART C: `λ ≤ −1` across the whole optimal face). It is kept in `lib131e`
   and reported as `tier1 = 0` at every `n` rather than deleted, because "the obvious
   `n`-indexed shape is not merely unfound but excluded" is the sharpest single fact in the
   pattern analysis.
2. **`d1` and `d2` re-solve the same branch LPs.** `d2` PART B recomputes the trivial-dual
   coverage that `d1` already computed. They are separate runs on purpose — `d2`'s counts are
   not read out of `d1`'s transcript — but it costs `n = 5` twice and should be said.
3. **`PART A` stops at `n = 8`, not because the statement does.** `branch_columns` filters all
   of `S_n`, so `n = 9` enumerates `9!`. The statement is a proof at every `n`; the loop is its
   illustration, and the limit is mine, not the theorem's.
4. **The growth law `(5n−8)/12` is checked at `n = 6, 8, 10` only, on one sub-family**, and is
   reported as such. No general construction for all `n` was written; see "what was not done".
