# `mg-00a1` — predictions for **THE TRUE GROWTH OF THE DISJUNCTIVE PER-SLOT VALUE**

**Committed before any script of this instrument exists.** Nothing in
`code/growth_rate_00a1/` has been written yet.

Parent: `mg-131e` (`b7b6941` on `main`), which refuted `ε_spec = 2/(n+1)` at `n = 6` and named
this question as its own successor, deliberately unanswered. Grandparent: `mg-200d`
(`762921d`), whose formulation and row builder `lp200d.build` are **used, not re-derived** —
a growth rate for a re-derived row set would be a growth rate for a different question.

§0 below is **long on purpose.** I did a great deal of scratch exploration before writing this
file, and every number I already have is disclosed here as a **measurement**, not laundered into
a prediction. The ticket's warning 1 is that `2/(n+1)` matched at `n = 3,4,5` and died at the
first untested value; the honest defence is to say exactly which points I have, and to make the
predictions about points I do **not** have.

---

## 0. Measurements already made, disclosed (scratch code, outside this instrument)

**H1 — THE TRANSITIVE-CLOSURE REDUCTION IS A THEOREM AND I HAVE ITS PROOF ON PAPER.** Let `C` be
a branch (a set of pairs declared comparable) and `tc(C)` its transitive closure inside the
natural order. Then

> `columns(C) = columns(tc(C))` and `feasible(C) ⊆ feasible(tc(C))`, so `val(C) ≤ val(tc(C))`.

*Proof.* A column is a permutation placing `i` before `j` for every `(i,j) ∈ C`, `i<j` — i.e. a
linear extension of the relation `C`, hence of `tc(C)`; so the column sets are equal. For a pair
`(i,j) ∈ tc(C) \ C`, branch `C` calls it incomparable and therefore imposes
`J_k(i,j) = J_k(j,i)` at every slot; but no column flips it, so `J_k(j,i) = 0` and the row reads
`J_k(i,j) = 0` — an extra constraint that `tc(C)` does not impose. Cap rows are unaffected
(`lp200d.build` writes a cap row only `if col:`, and that pair's column set is empty). ∎

**So `max over the 2^C(n,2) branches = max over TRANSITIVELY CLOSED branches = max over posets
`P` on `[n]` having the identity as a linear extension.** This is one of the three answers the
ticket names as real ("a proof that the maximum over branches is attained on a structured
family"). It is an *argument*, not an enumeration: no poset is constructed anywhere.

It also explains, rather than merely records, `mg-131e`'s 99.5%-vacuous count: the
non-transitively-closed branches carry strictly more constraints and are the first to go
infeasible.

**H2 — the per-slot symmetry constraint is exactly the ADJACENT-TRANSPOSITION symmetry of
`uniform L(P)`.** For `x, y` incomparable in `P` and adjacent at slots `k, k+1`, swapping them
maps `L(P)` to `L(P)` bijectively between the two orders, so `uniform L(P)` satisfies every
per-slot row. Two consequences I will use: the symmetry-feasible set is **never empty** on a
transitively closed branch (it contains `uniform L(P)`), so *all* infeasibility on such branches
comes from the `1/3` caps; and the disjunctive relaxation is exactly "`M_n` ∩ {measures with the
adjacent-swap symmetry}", which is the natural relaxation of the frozen-poset object itself.

**H3 — E[des] ≤ (n−1)/2 for every feasible measure in every branch.** This is `mg-131e`'s H6,
re-derived, not new: every descent sits on an incomparable pair, per-slot symmetry gives
`E[des] = E[asc_I]`, and `E[des] + E[asc_I] ≤ n−1`. **It cannot by itself give a linear upper
bound**, because `inv ≥ des` pointwise runs the wrong way. `mg-131e` said this too. I record it
because if the answer turns out to be superlinear, this identity is the reason the obvious
linear-looking bound was never a bound.

**H4 — the TWO-CHAIN posets are INFEASIBLE for every `(a,b)` I tried.** `P` = two disjoint
chains on `{0..a−1}` and `{a..a+b−1}`. Exact rationals through `lp200d.relaxation`, all
`INFEASIBLE`: `(1,1) (1,2) (2,2) (1,3) (2,3) (3,3) (2,4) (3,4) (4,4) (1,4) (1,5) (2,5)`, i.e.
every `a+b ≤ 8`. The phase-1 residual **rises** with `n` (`1/3, 1/2, 5/9, …, 13/21`), so this
is not a near miss. **The obvious quadratic-|I| family is dead**, and that is a measurement,
not a guess.

**H5 — the BAND posets are INFEASIBLE for every span `s ≥ 2`.** `I = {(i,j) : j−i ≤ s}`.
`s = 1` is `mg-131e`'s consecutive branch and gives `(n−1)/3` exactly; `s = 2` is infeasible at
`n = 4..14`, `s = 3` at `n = 5..9` (float LP; the `s=1` row is exact). So a feasible branch's
incomparability graph cannot be locally dense either.

**H6 — a GREEDY search from the consecutive branch finds a chord family whose chord count grows
QUADRATICALLY, and its first three values fit a quadratic exactly.** Greedy: start from
`I = {(i,i+1)}`, repeatedly add the single pair that most increases the value. It selects

> `I(n) = {(i,i+1)} ∪ {(i,j) : i odd, j even, j ≥ i+3, j ≤ n−2}`,

which has `m(m+1)/2` incomparable pairs at `n = 2m` — **quadratic**. Values, **exact rationals**
at `n = 6, 8` and float at `n = 10`:

| `n` | 6 | 8 | 10 |
|---|---|---|---|
| value | `11/6` **exact** | `26/9` **exact** | `25/6` float |
| `(n−1)/3` | `5/3` | `7/3` | `3` |
| `n(n+5)/36` | `11/6` | `26/9` | `25/6` |

All three sit **exactly** on `n(n+5)/36`. Second differences in `m = n/2` are constant at `2/9`.

**I am putting this on the record as three points and a fit, which is precisely the shape of the
thing that killed `2/(n+1)`.** `n = 6` and `n = 8` are exact; `n = 10` is float. Three points do
not decide a growth rate and I am not claiming they do — see P2, P3, P4.

**H7 — the branch of H6 is a genuine comparability pattern (transitively closed), and I know
which poset it is.** `C` = evens a chain, odds a chain, and `2k < 2l+1` iff `l ≥ k+1`; no odd is
below any even. Linear extensions are the lattice paths `(0,0) → (m,m)` with `j ≤ i+1` — the
ballot paths, `Catalan(m+1)` of them (`429` at `n=12`, `1430` at `n=14`, `4862` at `n=16`). So
this family is computable far past the range where a general branch is.

**H8 — my float simplex was WRONG on first writing and I caught it against the exact solver.**
It reported `13/9` where `lp200d.relaxation` reports `4/3`, on the `n = 5` branch
`consecutive ∪ {(1,3)}` — it left artificial variables basic after phase 1 and used a Dantzig
rule that cycles under this problem's heavy degeneracy. Fixed (artificials driven out, Bland's
rule) and then cross-checked: **364/364 agreement** with `lp200d.relaxation` on *all* `64`
branches at `n = 4` and `300` random branches at `n = 5`. Every float number in this instrument
is search-only and is re-derived exactly or by direct arithmetic before it is reported.

**H9 — `mg-200d`'s baseline for comparison is `n(n−1)/6`.** Caps alone (`form='none'`) give
`1, 2, 10/3` at `n = 3,4,5`, i.e. `n(n−1)/6`. So if H6's family is real, per-slot symmetry buys
a **constant** (`1/6 → 1/36`), not an order — and `mg-200d`'s `Θ(n²) → Θ(n)` headline, which
`mg-131e` explicitly declined to refute, would be refuted.

---

## 1. Predictions

Scored `HELD` / `REFUTED` in `OUTCOMES.md`, kept as written either way.

| # | prediction | conf | why |
|---|---|---|---|
| **P1** | Controls reproduce: `lp200d`'s `2/3, 1, 4/3` at `n = 3,4,5`, and `(n−1)/3` on the consecutive branch at `n = 3..10` in exact rationals. | 97% | If the parent does not reproduce in my worktree nothing here is readable. |
| **P2** | The H6 family's value at `n = 12` is **exactly `17/3`**, the value `n(n+5)/36` predicts. | **50%** | It is a three-point fit and this lineage has been killed by a three-point fit tonight. I give it a coin flip *on purpose*: I believe the *shape* far more than the *formula*. |
| **P3** | Whatever the value at `n = 12` is, it is **`≥ 5.5`** — i.e. strictly above `25/6 + 23/18 = 49/9 ≈ 5.444`, the value a *linear* continuation of the last increment would give. | 85% | This is the prediction that decides linear vs superlinear at the first untested point, and it is stated so that it can fail cleanly. |
| **P4** | **THE ANSWER IS SUPERLINEAR: the disjunctive per-slot value is `Θ(n²)`, so Daniel's route is DEAD rather than re-based.** | 80% | H6's family has quadratically many incomparable pairs at a constant fraction of the cap, and H4/H5 show the constraint that kills *other* quadratic families does not bite here. But 20% is real: the family may saturate. |
| **P5** | `mg-200d`'s `Θ(n²) → Θ(n)` headline is **REFUTED**, and what per-slot symmetry actually buys is a constant factor of about `6` (`n²/6 → n²/36`). | 75% | Direct corollary of P4 and H9. Filed separately because it is a *second* result and it should be scored on its own. |
| **P6** | The transitive-closure reduction (H1) verifies by machine on **all `64` branches at `n = 4`** and on a sample at `n = 5`: `val(C) ≤ val(tc(C))` with **0** exceptions, and the max over all branches is attained at a transitively closed one. | 95% | It is a proof (H1). What is being tested is whether I have `build`'s row conventions right. |
| **P7** | Every two-chain poset `(a,b)` with `a+b ≤ 10` is infeasible, in exact rationals — extending H4 by two more `n`. | 90% | The residual is rising, not falling. |
| **P8** | I will produce an **explicit measure family, checked by direct `Fraction` arithmetic with NO LP anywhere in the path**, feasible on the H6 branch at `n = 6, 8, …, 16` with `E[inv]` growing quadratically. | 60% | This is the only artefact that would make the answer independent of my simplex. `mg-131e` did exactly this at `n = 6..10` and it is why its refutation stuck. 60% because I do not yet know the pattern of the optimal measures — the `n=8` optimum is not uniform (one atom carries `2/9`). |
| **P9** | The greedy at `n = 12`, re-run from scratch, selects the **same** family H6 names (all `(odd, even)` chords with `j ≥ i+3`, `j ≤ n−2`) and finds nothing better. | 55% | Greedy is greedy. A better branch at `n = 12` would not hurt the verdict — it would strengthen it — but it would refute this prediction. |
| **P10** | No **linear** upper bound over all branches exists, so the ticket's first offered answer (`cn + O(1)` with explicit `c`) is **not** what I return. | 80% | Consequence of P4. Stated separately so that "I failed to find an upper bound" cannot later be dressed up as "there is none". |
| **P11** | `E[des] ≤ (n−1)/2` holds on every optimum I compute (a theorem, H3), **and** `E[inv]/E[des] → ∞` on the H6 family — so the descent identity is not merely insufficient, it is off by an unbounded factor. | 85% | `E[inv] ~ n²/36` against `E[des] ≤ n/2`. |
| **P12** | The value of the H6 family at `n = 14` is computable by me and is **≥ 7.0**. | 70% | `1430` columns; `n(n+5)/36 = 133/18 ≈ 7.39`. If I cannot compute it I will say so rather than interpolate. |

---

## 2. My two most likely errors, filed in advance

**P13 — THE ERROR I AM MOST LIKELY TO MAKE: fitting `n(n+5)/36` on three points and reporting
the FORMULA as the answer.** This is `mg-131e`'s warning 1 aimed directly at me, and I have
already written the formula down in H6, which is how it starts. The formula is *not* the
deliverable; the *growth class* is. I commit in advance: if `n = 12` misses `17/3` I will report
the raw value, score P2 REFUTED, and re-ask whether the *class* survives — I will **not**
silently re-fit a new quadratic through four points and present that instead. And I will state
how many points are exact and how many are float at every table.

**P14 — THE SECOND ERROR: reading "the relaxation is quadratic" as "the frozen-poset conjecture
is refuted", or as "(LIB) is false".** It is neither. The disjunctive value is an **upper
bound** on the object of interest; showing an upper bound is larger than believed *weakens the
bound* and says nothing whatever about the statement underneath. `mg-131e` filed this same
caveat as its §5.2 and I expect to be tempted by it harder, because a superlinear answer is a
more dramatic sentence than a linear one. What a superlinear answer kills is **this route as a
wall-breaker**, not the wall.

**P15 — the third, smaller one: treating a named-branch value as the maximum.** The ticket's
warning 2. Every `n ≥ 6` number here is a **lower** bound found on a **named** branch, so the
true maximum at each `n` may exceed it. That direction is harmless for a superlinear verdict
(a larger maximum is still superlinear) and fatal for a linear one, so it must be stated
wherever a linear reading is offered.

---

## 3. Bounds I am keeping

* **No exhaustive `n = 6`.** The ticket forbids it and H1 does not license it: the reduction
  cuts `32768` branches to the transitively closed ones, which is a large cut, but "cheaper
  brute force" is still brute force and the ticket says to mail `pm-onethird` rather than start
  it. I am not starting it and I am not asking.
* **No poset enumeration.** H1 is a *theorem about the branch family*, proved on paper. No
  poset is enumerated anywhere in this instrument; every object computed is a set of measures
  on `S_n`, and the families are **named by hand**. `mg-345e`'s and `mg-6bc2`'s refusal stands.
* **`M_n` membership** is inherited from `mg-200d` and `mg-131e` and kept.
* **Tightness is open beyond `n = 3`** — `mg-200d`'s caveat, untouched.
* **This is not an `N₀` argument** and nothing here is discharged by citing `mg-c4f5 §5.3`.
  The question is an explicit rate, which `STATE.md` row 8 permits.
