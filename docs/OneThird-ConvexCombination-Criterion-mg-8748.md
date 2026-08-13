# OneThird — **WHICH CONVEX COMBINATIONS OF COMPRESSIONS ARE CANONICAL.** A selection criterion, not a result. `criterion`

**Work item.** `mg-8748` (repo `onethird_program`), filed by `pm-onethird` on the explicit
recommendation of `mg-0fc6`'s scope document, §6 item 3.
**Why it is its own document.** `mg-0fc6`'s recommendation is **`SCOPE: low`**. `a4.3b` is the one
part of Daniel's stated design that measured out *better* than the objects the closed arc used,
and filed inside that verdict it would be archived with the route it happened to arrive in. **A
live fact does not survive inside a dead verdict's body.**
**Instrument.** [`code/convex_criterion_8748/`](../code/convex_criterion_8748/), `run_all.sh`,
**~50 s measured**, exact rationals. Pre-registered at `f901435` before one line of it existed.
**Cited, not re-measured.** `mg-0fc6`'s verdict, `mg-8d66`'s ceiling, `FACTS.md` F6.

---

## 0. THE CRITERION

> ### `Q1` **Is the family NESTED?** — and ask it about the **increments**, not the compressions.
>
> **Combining the COMPRESSIONS convexly is never a compression.** For orthogonal projections
> `A`, `B` and `t ∈ (0,1)`, `tA + (1−t)B` is idempotent **iff `A = B`**. This is true on a
> filtration too, so nestedness does not rescue it and never did.
>
> **What a nested family buys is that the INCREMENTS EXIST.** `D_l = Π_l − Π_{l−1}` is a
> projection **iff** `Ran Π_{l−1} ⊆ Ran Π_l`, i.e. iff the two levels are nested — an `iff`, not
> a heuristic. Given increments: they are mutually orthogonal, they sum to `I − Π_0`,
> `Var(f) = Σ_l ‖D_l f‖²` **exactly**, and `M = Σ_l λ_l D_l` commutes with every `Π_k` with
> `M D_l = λ_l D_l`. That operator is a **Littlewood–Paley multiplier**: diagonal in the scale
> decomposition, spectrum exactly the weights, mixing the scales in whatever proportion is asked
> for. **That is what Daniel's convex combination should be, and on a filtration it is
> canonical.**
>
> **The check is one pass over the partitions.** `refines(C_a, C_b)` — no matrix, no
> eigenvalue. Measured to agree with the operator route `Π_a Π_b = Π_b Π_a = Π_a` at **every
> ordered pair of set partitions of a 4- and 5-point space** (225 and 2 704 pairs, 0
> disagreements, `c0.5`).

> ### `Q2` **Can the construction SEE realizability?** — the `a2.3` two-measure exhibit.
>
> Two measures with **identical pair marginals**, one a linear-extension measure and one not,
> both inside hypothesis (1). Feed both to the construction. **If it returns the same answer, it
> reads the poset only through its pair marginals and cannot supply a realizability fact** —
> and `STATE.md:21` says every route below `1` must add one. Re-derived here on an
> implementation sharing no code with `mg-0fc6`'s and landing on the same witness: `n = 6`,
> `e(P) = 9`, max flip `1/3` (`c4.1`).

**Together they are a fast filter on compression proposals**, and both answers are cheap.
Neither is a verdict. `Q1 = NESTED` licenses **one step** and says nothing about whether the
construction is going anywhere: **`compression2` is NESTED and REALIZABILITY-BLIND**, which is
exactly why the criterion is worth keeping and the route it arrived in is not.

---

## 1. Daniel's instinct, and the exact sense in which it is right

His words, 2026-08-13T00:40Z: *"we can combine them in convex combinations to get one that mixes
what we want the right amount."*

**Right on `compression2`'s scales.** They are a filtration by construction of the dyadic tree,
so the increments exist and their convex combination is the multiplier above — *"mixes what we
want the right amount"* is precisely what `Σ λ_l D_l` does, and the weights are the mixing.

**Wrong on `compression.tex`'s pair,** at the typical poset: there the increments are not
projections, `Π_o − Π_e` is not even PSD, and there is no σ-algebra the combination is the
conditional expectation of.

**And in both cases, wrong about the compressions themselves.** That half is Theorem A and it has
no family in it.

⚠️ **THE HONEST SCOPING, CARRIED VERBATIM FROM `mg-0fc6` §4 AND NOT IMPROVED:**

> *the variance identity is Pythagoras and holds for **any** filtration. The content is the
> **nestedness**, which is by construction of the dyadic tree. It is still a real structural
> difference from the transverse pair, and it is the one place Daniel's stated design is
> strictly better than the objects the closed arc used.*

The claim is **not** that `compression2`'s scales are special. It is that **nested beats
transverse for this purpose, and nestedness is cheap to check**.

---

## 2. Three things this measurement found that the source verdict did not

### 2.1 `a4.3a`'s `40 of 40` measures DISTINCTNESS, not transversality

`mg-0fc6` `a4.3a` reports `(Π_o + Π_e)/2` non-idempotent at **40 of 40** posets where the two
foliations differ, and that is the row offered for *"`compression.tex`'s **transverse** pair"*.
By Theorem A the non-idempotence follows from `Π_o ≠ Π_e` **alone**, and the row's own population
is *posets where the two differ*. `c1.3` runs the identical measurement on `compression2`'s
**nested** scales at `n = 4, 6, 8` and it comes out the same way. **The row is true, is correctly
reported at source, and cannot separate the two cases** — so it must not be quoted as though it
established transversality.

### 2.2 Transversality is not uniform, and here is the number

`c3.1`, over **every labelled poset at `n = 3, 4, 5` with `|L(P)| ≥ 2`** — 4 319 of them:

| | transverse | **nested and distinct** | equal |
|---|---|---|---|
| `n = 3` | 7 | 6 | 0 |
| `n = 4` | 153 | 42 | 0 |
| `n = 5` | 3 811 | 300 | 0 |
| **total** | **3 971 (91.9 %)** | **348 (8.1 %)** | **0** |

At **348** posets one parity foliation genuinely **refines** the other, and there the convex
combination of increments *is* available. So *"`compression.tex`'s transverse pair"* is a
statement about the typical poset, not about the family, and **`Q1` has to be asked per poset**.
A prediction of that arm's own was refuted by its own run: the two foliations **never coincide**,
at any of the 4 319.

### 2.3 The operative property is ORTHOGONALITY, and nestedness is the cheap route to it

`c3.3` asserted that on a transverse pair the increments overlap — `(Π_o − E)(Π_e − E) ≠ 0`. It
holds at **3 640 of 3 670** and **fails at 30**, where `Π_o Π_e = P_0` exactly: the two
σ-algebras are **independent** under the measure, and the variance splits despite transversality.
**The arm's own asserted lemma is refuted by its own run and is kept rather than rewritten**, on
`mg-0fc6` `a5`'s precedent, because the mistake it made is the mistake the criterion is at risk
of.

> **Nestedness is the CONSTRUCTIVE route to orthogonal increments — it supplies a whole ORDERED
> family of them at once, canonically, and it is the route that is cheap to check. It is not the
> only way orthogonality can occur.** The criterion must be stated that way or it over-claims.

---

## 3. What this does NOT do

- **It supplies no realizability fact.** `STATE.md:21` is untouched. `compression2` passes `Q1`
  and is realizability-blind (`mg-0fc6` §2), which is the whole demonstration that `Q1` is not
  evidence of progress.
- **It does not revive either note.** `mg-0fc6`'s `SCOPE: low` stands, unamended, and this
  document takes no position on it — that is what *orthogonal to whether this note's route works*
  means.
- **It is not a new degree of freedom on `compression.tex`'s family.** `k·I − Σ_i Π_i` **is**
  `k·(I − ` the equal-weight convex combination `)` — verified exactly at `c3.5` — so on that
  family "combine them convexly" names the object `mg-8d66` already priced
  ([`FACTS.md`](FACTS.md) F6, `mg-409a`'s bar, cited and not re-measured).
- **It says nothing above the `n` it reaches.** The census is `n ≤ 5`; the filtration rows are
  seven posets at `n = 4…8` under `|L(P)| ≤ 42`. What carries above them is the **proof** —
  Theorems A and C have no poset in them — and the partition sweeps, which are about projections.

---

## 4. How the pre-registration scored

[`PREDICTIONS.md`](../code/convex_criterion_8748/PREDICTIONS.md), committed at `f901435` before
one line of the instrument existed.

| | | outcome |
|---|---|---|
| `R1` | `tA+(1−t)B` idempotent iff `A = B` | **REPORT, zero credit.** Derived on paper before the code, and disclosed as such rather than filed as a bet. It is the statement that made the fact's usual phrasing false. |
| `R2` | `B − A` a projection iff `Ran A ⊆ Ran B` | **REPORT, zero credit**, same derivation. |
| `P3` | cheap route ≡ expensive route, 0 disagreements | **CONFIRMED**, exhaustive at 225 and 2 704 ordered partition pairs. |
| `P4` | `a4.3a`'s row measures distinctness; the pair is transverse at a large majority | **CONFIRMED**, both halves — 3 971 of 4 319. |
| `P5` | *and* nested-and-distinct instances exist, so the word is not uniform | **CONFIRMED** — 348 of 4 319. This was the bet I was least sure of (`p = 0.60`). |
| `P6` | the `iff` holds with 0 exceptions and the failing side is a majority | **CONFIRMED** — 0 exceptions; not a projection at 165/225 and 2 346/2 704. |
| `P7` | `Var = Σ‖D_l f‖²` at every poset measured and for structured `f` | **CONFIRMED** — 7 posets, 11 statistics each, deviation 0. |
| `P8` | the two-measure exhibit separates, and the planted non-blind control does not read blind | **CONFIRMED**, onto `mg-0fc6`'s own witness. |

**Eight of eight live bets confirmed, and that is a weaker result than it looks**, because two of
them (`R1`, `R2`) were paper-derived first and the rest are close to them. **The instrument's own
uncontracted expectations did worse and that is where the information is:** two rows were refuted
by their own run — the foliations never coincide (`c3.1`), and the cross term vanishes at 30
transverse posets (`c3.3`). Both are kept in the arm rather than rewritten, and the second one
changed the criterion's statement.

## 5. Where it is filed

[`docs/FACTS.md`](FACTS.md) **F24**, with its kind and its exact scope. It is registered there
rather than in `STATE.md` for `FACTS.md`'s own three reasons, and the second is the operative one
here: **a fact with no relation to the current argument can only be filed in `STATE.md` by
pretending it has one.** This one has none, deliberately.
