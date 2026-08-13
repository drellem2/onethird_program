# mg-8748 — WHICH CONVEX COMBINATIONS OF COMPRESSIONS ARE CANONICAL

**What this directory is.** `mg-0fc6`'s scope document scored `compression2.tex` **`SCOPE: low`**
and recommended, in so many words, that **one part not be filed with the rest**:

> *"Keep `a4.3b` separately from the verdict. The filtration/multiplier distinction is a small,
> true, reusable fact about which convex combinations are canonical, and it is orthogonal to
> whether this note's route works."*

This is that keeping. **It builds nothing for the programme, closes nothing, and supplies no
realizability fact** — `STATE.md:21` is untouched by everything below. What it does is hold a
**selection criterion** where the next compression design will hit it, and measure it at a scope
`a4.3b` did not reach: `a4.3b` is **one poset** (the `n = 4` antichain, 3 levels, 5 random `f`).

**Run it:** `sh run_all.sh` — **~50 s measured** on this host. Exact rationals throughout; no
float on any verdict path. Not a gate, and see `run_all.sh`'s header for why it must not become
one.

---

## 1. THE CRITERION, in the form it should be quoted

> **Combining the COMPRESSIONS convexly is never a compression** — on any family, nested or
> transverse. `tA + (1−t)B` is idempotent **iff `A = B`** (Theorem A, `c1`).
>
> **What a NESTED family buys is the INCREMENTS.** `D_l = Π_l − Π_{l−1}` is a projection **iff**
> the family is nested (Theorem C, `c2.5`). Given increments, they are mutually orthogonal, they
> sum to `I − Π_0`, `Var(f) = Σ_l ‖D_l f‖²` exactly, and `M = Σ_l λ_l D_l` commutes with every
> `Π_k` with `M D_l = λ_l D_l` — a **Littlewood–Paley multiplier**, diagonal in the scale
> decomposition (Theorem B, `c2`).
>
> **Nestedness is checkable in one pass over the partitions**, with no matrix formed (`c0.5`,
> exhaustive over all set partitions of a 4- and 5-point space, 0 disagreements with the
> operator route).

**So Daniel's instinct — *"we can combine them in convex combinations to get one that mixes what
we want the right amount"* (2026-08-13T00:40Z) — is right about `compression2`'s scales and wrong
about `compression.tex`'s pair, and the object it is right about is the increments, not the
compressions.**

⚠️ **THE HONEST SCOPING, CARRIED VERBATIM FROM `mg-0fc6` §4 RATHER THAN IMPROVED:**

> *the variance identity is Pythagoras and holds for **any** filtration. The content is the
> **nestedness**, which is by construction of the dyadic tree. It is still a real structural
> difference from the transverse pair, and it is the one place Daniel's stated design is
> strictly better than the objects the closed arc used.*

The claim is **not** "`compression2`'s scales are special". It is "nested beats transverse for
this purpose, and nestedness is cheap to check". The value is as a **selection criterion**, not
as a result.

---

## 2. What this instrument found that `mg-0fc6` did not

Three things, and the first two constrain how the fact may be quoted.

### (a) `a4.3a`'s `40 of 40` is a measurement of DISTINCTNESS, not of transversality

`mg-0fc6` `a4.3a` measures `(Π_o + Π_e)/2` non-idempotent at **40 of 40** posets where the two
differ, and that row is what the verdict offers for *"`compression.tex`'s **transverse** pair"*.
**By Theorem A the non-idempotence follows from `Π_o ≠ Π_e` alone** — and `a4.3a`'s own
population is *posets where the two differ*. `c1.3` runs the identical measurement on
`compression2`'s **nested** scales and it comes out the same way, which is the direct
demonstration that the row cannot separate the two cases. The row is **true and correctly
reported at source**; it does not carry the weight it is quoted for.

### (b) TRANSVERSALITY IS NOT UNIFORM — the number nobody had taken

`c3.1`, over **every labelled poset at `n = 3, 4, 5` with `|L(P)| ≥ 2`** (4 319 of them):

| | transverse | nested **and distinct** | equal |
|---|---|---|---|
| `n = 3` | 7 | 6 | 0 |
| `n = 4` | 153 | 42 | 0 |
| `n = 5` | 3 811 | 300 | 0 |
| **total** | **3 971** | **348** | **0** |

So *"`compression.tex`'s transverse pair"* is a statement about the **typical poset**, not about
the family: at **348** posets one parity foliation genuinely refines the other. And a prediction
of this arm's own was refuted by its own run — the two foliations **never coincide**, at any of
the 4 319.

### (c) THE OPERATIVE PROPERTY IS ORTHOGONALITY OF INCREMENTS, AND NESTEDNESS IS ONE ROUTE TO IT

`c3.3` set out to show that a transverse pair's increments overlap, i.e. `(Π_o − E)(Π_e − E) ≠ 0`.
It holds at **3 640 of 3 670** — and **fails at 30**, where `Π_o Π_e = P_0` exactly: the two
σ-algebras are **independent** under the measure, and there the variance splits despite the pair
being transverse. **The row is kept rather than quietly rewritten**, on `mg-0fc6` `a5`'s own
precedent, because the mistake it made is the mistake the criterion is at risk of. Nestedness is
the **constructive** route to orthogonality — it yields a whole *ordered* family of orthogonal
increments at once, canonically, and it is the route that is cheap to check — but it is **not the
only way orthogonality can occur**, and the criterion must be stated that way.

---

## 3. The arms

| arm | what it does | measured |
|---|---|---|
| `c0` | controls: cross-check against `lib0fc6` (4 469 posets, 0 disagreements); the projection machinery; **six planted worlds** with hand-known answers, two of them transverse; a **wrong-direction world** where a nested family is handed to the detector claimed transverse; and the cheap/expensive route agreement | 1 s |
| `c1` | **Theorem A**, exhaustive over all partition pairs of a 4- and 5-point space × 5 values of `t`; `a4.3a` reproduced independently at 4 018 posets; **and the same measurement on the nested family, where it comes out identically** | 17 s |
| `c2` | **Theorems B and C**: the scale family is a filtration at 7 posets `n = 4…8`; increments are mutually orthogonal projections; `Var(f) = Σ‖D_l f‖²` exact at 11 statistics each including `inv_e`, `pos_x`, `disp²`; the multiplier; and the `iff` exhaustively over all set partitions of a 4- and 5-point space | 7 s |
| `c3` | the transverse side: the classification above; `Π_o − Π_e` neither a projection nor PSD at 3 670 of 3 670 with an explicit negative witness at each; the independence exception; a non-vacuity control inverting every failure on a nested pair; and `k·I − ΣΠ_i = k(I − avg)` exactly | 25 s |
| `c4` | **THE FAST FILTER** — `classify_family(parts)` and `marginal_blind(f, n, mu1, mu2)`, both taking callables so the next proposal needs no edit to this file; the `a2.3` exhibit **re-derived** and landing on the same witness `n = 6`, `e(P) = 9`, max flip `1/3`; four worked families and a planted non-blind construction | 1 s |

**Two defects this instrument made and kept**, because a suite that only records its successes
is evidence of nothing: `c3.2` first swept the indicators of single extensions for a PSD witness
— a family of the right size and the wrong direction, finding one at only 3 136 of 3 670 (D1);
`c4.1`'s two-atom control first used two extensions that differ by one adjacent transposition and
therefore **are** a poset's linear extensions, so the oracle correctly accepted them and the row
went red against a wrong control (D2). Both are named at the site.

**And `mg-0fc6`'s own D4 is carried over rather than rediscovered**: the two-measure exhibit is
built on a poset satisfying `δ(P) ≤ 1/3`, because a filter run outside the hypothesis it filters
is worth nothing. That is why `c4.1` lands at `n = 6` and not on the antichain.

---

## 4. Where the criterion lives, and what it is not

- [`docs/OneThird-ConvexCombination-Criterion-mg-8748.md`](../../docs/OneThird-ConvexCombination-Criterion-mg-8748.md) — the criterion, in two questions.
- [`docs/FACTS.md`](../../docs/FACTS.md) **F24** — the registry entry, with its kind and its exact scope.
- [`PREDICTIONS.md`](PREDICTIONS.md) — filed at `f901435`, before one line of the instrument existed, with `R1`/`R2` disclosed as **reports of a paper derivation at zero credit**.

⚠️ **IT IS NOT A RESULT.** It licenses one step and nothing else. `compression2` is **NESTED and
REALIZABILITY-BLIND** (`mg-0fc6` §2, cited and not re-derived): passing `Q1` told nobody anything
about whether the route worked, and the route does not work. A criterion that gets read as
progress is worse than no criterion.
