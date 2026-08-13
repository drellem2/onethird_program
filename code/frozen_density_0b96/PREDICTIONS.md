# `mg-0b96` — predictions, with the exposure disclosed per line

**Filed after `lib0b96.py` existed and after an `n ≤ 8` residue census had been run in a scratch
directory, and NOT before.** That is the honest order and it is stated here rather than implied by
a filename, because a prediction filed after the run it predicts is a description wearing a
prediction's clothes. Each line below carries what it was exposed to when it was written.

The ticket's own expectation is on the record and is the headline prediction: **"a NO-hunt, not a
construction — the expected and most useful outcome is a cheap NO."**

| # | prediction | exposure when written | outcome |
|---|---|---|---|
| P1 | A frozen-class ceiling `(1_D)` is equivalent to the conjecture on `{d > D}`, for every `D`. | **NONE** — this is contraposition and was written before any code. | **HELD** (`d1`) |
| P2 | The equivalence is a tautology, so a run can only check the implementation, not the statement. | NONE | **HELD** — `d1 m1` says so at the table |
| P3 | `{d > D}` is non-empty at every `D < 1`, so the weakening never empties its own hypothesis. | NONE | **HELD** (`d1 m2`) |
| P4 | The crossing where primitivity's `d ≥ 2/n` first meets `D_needed` lands at `n ≈ 100`, reproducing `mg-33f5`'s T2 from the density side. | **PARTIAL** — I had read T2 = 100 in `mg-33f5` §3 before predicting. The prediction was that the density route reproduces it, not the value. | **HELD at 99**, one unit off T2, and the unit is the `n/(n+1)` factor T2 drops (`d2 m3`) |
| P5 | No class exclusion on the record delivers an upper bound on `d` below `1 − Θ(1/n)`. | **NONE for the joint statement**; I had seen `mg-33f5` §2's table and expected `k`-thin to be the only density-shaped row. | **HELD** — 5 of 7 deliver any bound at all, the strongest `5/6` at `n = 9` (`d3 m2`) |
| P6 | The joint residue is non-empty and its maximum density rises with `n`. | **EXPOSED** — the `n ≤ 8` scratch run had already returned `452` posets at `max d = 3/4`. | **HELD** (`d3 m3`), and the `n = 9` value `7/9` was NOT exposed |
| P7 | The residue is empty below `n = 8` because every poset on `≤ 7` elements is 6-thin. | **EXPOSED** — the scratch run returned empty at `n ≤ 7` and I worked out the reason from it. Recorded as an explanation, not a prediction. | **HELD** (`d3 m4`) |
| P8 | An explicit family, outside every class at every `n ≥ 15`, exists with `d = 1 − Θ(1/n)`. | **NONE at the time of writing the design**; the first two attempts at such a family FAILED the rigidity predicate and are not in the shipped code. | **HELD** (`d3 m5`), third construction |
| P9 | The elementary "two interchangeable elements ⟹ `δ ≥ 1/2`" bound exists and is worth `1 − Θ(1/n)`. | NONE | **HELD** (`d4 m1`, `m2`) |
| P10 | That bound is NOT sharp on its own class. | NONE | **REFUTED — it is attained at every `n` swept.** The arm reads sharpness off the measurement now; the prose that asserted the opposite was written first and was wrong. |
| P11 | The must-say-YES control returns a ceiling strictly below 1 on the pseudo-frozen class `δ < 1/2`. | NONE | **HELD** (`d0` T7) — and the ceiling RISES with `n` (`2/3, 1/2, 7/10, 11/15, 17/21`), which was not predicted |

**P10 is the one that matters and it is kept as written.** It was refuted by this directory's own
run, in the direction that makes the elementary bound *better* than I expected and the verdict
unchanged — the bound is sharp on the class it is proved for and still worth `1 − Θ(1/n)`. The
sentence asserting non-sharpness sat beside a table showing attainment at all six `n`; that is a
prose figure not regenerated from its measurement, which is `mg-2959`'s defect one directory over,
and it was repaired by making the verdict a function of the table rather than by deleting the
prediction.
