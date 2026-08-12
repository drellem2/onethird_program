# `compression_kfoliation_8d66` — W5's instrument: **is the ceiling a `k = 2` artefact?**

Work item `mg-8d66`. Subject: `pm-onethird`'s generalisation of
[`docs/imports/compression.tex`](../../docs/imports/compression.tex) §§4–5 to `k` foliations.
Full write-up:
[`docs/OneThird-Compression-kFoliation-mg-8d66.md`](../../docs/OneThird-Compression-kFoliation-mg-8d66.md).

```
./run_all.sh          # k0 gates; k1..k5 only run if it passes.  ~170 s.
```

## The finding in three lines

```
  THE BAR      k-INDEPENDENT.  pm-onethird's premise is RIGHT and right for his reason:
               2/(n-1) is a PER-POSITION constant.  Exact PSD at 1728/1728 (poset, S) pairs.

  THE CEILING  ALSO k-INDEPENDENT.  alpha_S <= 1 at every poset and EVERY admissible S, by an
               exhibited rational witness that is BLIND to S, and ATTAINED at every S at Z_n.

  WHY         sup_k alpha_k = ((n-1)/2) gap_BK, attained at k = n-1 where Q IS the BK
              generator rescaled.  The route cannot overshoot the gap; its best case is the
              original problem restated.        =>  CLASS CLOSED BY CEILING, AT EVERY k.
```

`1 < 2`, at every `k`, exactly as at `k = 2`.

## Arms

| file | what it establishes | exact? |
|---|---|---|
| `k0_selftest.py` | **gate.** Hand-known LE counts; my backwards LE enumeration and orbit fibers cross-checked against `lib409a` **and** `lib8bc7` (two prior, independently written libraries); every fiber verified to be a **cube**; my `Q` at `k=2` is `lib409a`'s `M` entrywise; my exact PSD test cross-checked and shown to refuse planted indefinites; **four planted defects that must go red** (adjacent-position class, dropped position, repeated position, class-size-weighted constant) | yes |
| `k1_counting.py` | **item 4, checked first.** Admissible partitions = partitions of the path `P_{n-1}` into independent sets. `k_min = 2` and **unique**; `k_max = n−1`. Counting does **not** close the class — reported as a NEGATIVE result | yes |
| `k2_premise.py` | **item 1.** `Q_finest = ((n−1)/2)(I − P_BK)` entrywise; `((n−1)/2)(I − P_BK) ⪰ Q_S` at every admissible `S` — the same constant at every `k`, so **the bar is `k`-independent**. And the second `=` of the derivation is a `≥`, strict at 2 789 of 5 184 instances, with the equality case exhibited both ways | yes |
| `k3_monotone.py` | refinement monotonicity as an operator statement (`Q_fine − Q_coarse` PSD), **with the reversed comparison shown to be refused** so the direction is measured; the top of the order is `((n−1)/2)·gap_BK` | yes (`k3.3` float, labelled) |
| `k4_ceiling.py` | **item 2, the deciding arm.** The witness is blind to `k`; the closed form `P(adj)/(4p(1−p)) ≤ 1/(2 max(p,1−p)) ≤ 1` at **18 373 pairs exhaustively over `n = 3,4,5`**; `alpha_S ≤ 1` directly at every `S`; **why `mg-409a`'s own proof gives only `k−1`**; attainment at every `S` at `Z_n` both directions | yes |
| `k5_measure.py` | **item 3.** `alpha_k` measured by `k`; does it rise (92 of 434, and the mean barely moves); the `mg-8bc7` asymmetry constraint at `k ≥ 3`; the shortfall table against the bar | measurement |

## Independence, stated rather than implied

`lib8d66.py` builds everything on a verdict path from scratch, and **two constructions
deliberately take a different route** from both priors: linear extensions are enumerated by
choosing the **last** element (both priors choose the first), and fibers are computed as
**orbits** under the class's legal swaps (both priors use position-group content keys).
`lib409a` and `lib8bc7` are imported by **`k0` only**, as second and third implementations to
check this one against. **`k1`–`k5` share one library, mine, and are therefore not independent
witnesses of each other** — same shape as `mg-409a`'s D5 and `mg-8bc7`'s D6.

## Float discipline

Every `PASS` in `k0`, `k1`, `k2`, `k4` and `k3.1`/`k3.2` is an exact rational comparison, an
exact PSD elimination, or an exhibited rational witness. Jacobi appears in `k3.3` and all of
`k5`, which are labelled measurement. **No verdict rests on a float.**

## Populations, named

- `k2`, `k3` — `n = 3, 4` exhaustive; `n = 5` sample(120, seed 3); `n = 6` sample(60/40, seed 5).
  Posets with `|L(P)| > 130` are **skipped and counted** (8 of them); exact PSD is `O(N³)` in
  rationals.
- `k4.1`, `k4.4` — `n = 3, 4` exhaustive; `n = 5` sample(120); `n = 6` sample(40).
- **`k4.3` — `n = 3, 4, 5` EXHAUSTIVE over labeled posets (18 373 incomparable pairs).** This is
  the arm that carries the ceiling.
- `k4.6` — `Z_n` at `n = 4, 6, 8, 10`, **every** admissible partition (4 360 pairs).
- `k5` — `n = 3, 4` exhaustive; `n = 5, 6, 7` sample(200/120/60); all capped at `|L(P)| ≤ 34`.

## Defects of my own, kept

- **D1** — my first `k1_counting.py` recomputed `max(ks)` inside a generator over 115 975
  partitions. Quadratic; it hung for three minutes before I killed it — **in the arm whose
  subject is counting.** Caught by timing, not by a check.
- **D2** — my first `k0.7` control read `verdict(lhs != wrong or True, ...)`: **a row that
  cannot fail, inside the gate**. Caught by re-reading my own diff, not by any arm.
- **D3** — **P8 lost**: I predicted `alpha_k` rises strictly at a majority of posets; it is 92
  of 434.
- **D4** — populations above; `n = 5` is exhaustive only in `k4.3`.
- **D5** — see *Independence*.
- **D6** — see *Float discipline*.
- **D7** — the witness `f_xy` is **not new**: it is Theorem E's test function and `mg-409a`
  already uses it. What is mine is why it is blind to `k`. Disclosed as H2 of `PREDICTIONS.md`
  before the instrument existed.

## Not done here

`docs/imports/compression.tex` is not edited. `STATE.md` is not touched. `mg-409a`'s and
`mg-8bc7`'s directories are not modified. Theorem E is not re-proved. `lambda_std` is not
computed anywhere in this directory. The `k = 2` route is not re-opened.
