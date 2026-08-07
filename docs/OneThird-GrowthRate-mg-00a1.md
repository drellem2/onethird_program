# The true growth of the disjunctive per-slot value — it is `Θ(n²)`, and the route is dead

`mg-00a1` · instrument [`code/growth_rate_00a1/`](../code/growth_rate_00a1/) ·
parent `mg-131e` (`b7b6941`) · grandparent `mg-200d` (`762921d`, `731a9ab`)

---

## 0. The result, first

> **The disjunctive per-slot value is `Θ(n²)`, not `c·n + O(1)`.**
> There is no constant `c` to put in place of `1/3`, because the value does not have that
> shape at all. **Daniel's route is dead, not re-based.**

`mg-131e` refuted `ε_spec = 2/(n+1)` at `n = 6` and named this question as its own successor,
deliberately unanswered: *if the value is `c·n + O(1)` the route survives with `c` in place of
`1/3`; if it is superlinear the route is genuinely dead.* It is superlinear.

The answer is a **construction**, not a fit. For every even `n = 2m ≥ 4` there is an explicit
measure — written down in closed form, feasible on an explicit **transitively closed** branch,
checked by direct `Fraction` arithmetic with **no simplex anywhere in the verification path** —
with

```
E[inv]  =  n(n+5)/36 .
```

Against `mg-131e`'s trivial dual (`val ≤ |I_active|/3 ≤ n(n−1)/6`, a theorem at every `n`) this
pins the growth from both sides:

```
n(n+5)/36   ≤   max over branches   ≤   n(n−1)/6 .
```

Both ends are quadratic. The class is settled.

| `n` | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|
| **witness `E[inv]`** | `11/6` | `26/9` | `25/6` | `17/3` | `133/18` | `28/3` | `23/2` | `125/9` | `33/2` | `58/3` |
| `mg-200d`'s `(n−1)/3` | `5/3` | `7/3` | `3` | `11/3` | `13/3` | `5` | `17/3` | `19/3` | `7` | `23/3` |
| exact branch value (LP) | `11/6` | `26/9` | `25/6` | `17/3` | — | — | — | — | — | — |

Every row of the witness line is verified by arithmetic at that `n`, and at the four `n` where
an exact LP is affordable the witness is **optimal on its branch** — so `n(n+5)/36` is that
branch's *value*, not a slack point inside it.

**A second result, which `mg-131e` explicitly declined to touch.** `mg-200d`'s headline —
per-slot adjacency symmetry buys `Θ(n²) → Θ(n)` — is **REFUTED**. What it buys is a **constant
factor of at most 6** (`n²/6` down to at least `n²/36`), not an order. `mg-131e` wrote *"`mg-200d`'s
`Θ(n²) → Θ(n)` headline is not refuted; every value here is still linear in `n`"* and correctly
noted that the rate then rested on three points and no proof. Those three points were `n ≤ 5`,
and `n ≤ 5` is too small to hold the gadget.

---

## 1. What is being measured, in one paragraph

`mg-200d`'s disjunctive formulation: for each subset `C` of pairs declared comparable, take the
measures `μ` on the permutations that flip no pair of `C`, impose `q_ij ≤ 1/3` on the
incomparable pairs and per-slot symmetry `J_k(x,y) = J_k(y,x)` on them at every slot, and
maximise `E[inv]`. The **disjunctive per-slot value** is the maximum over the `2^C(n,2)`
branches. It is an **upper bound** for every frozen poset, which is the whole reason it was
worth computing.

Nothing in that is re-derived here. `lp200d.build` writes the rows, and a growth rate for a
re-derived row set would be a growth rate for a different question.

---

## 2. The reduction: the maximum lives on a genuine poset

**Theorem 1.** *For every branch `C`, `val(C) ≤ val(tc(C))`, where `tc(C)` is the transitive
closure of `C` inside the natural order. Hence the maximum over the `2^C(n,2)` branches is
attained at a **transitively closed** branch — i.e. at a poset on `[n]` having the identity as a
linear extension.*

*Proof.* A column of branch `C` is a permutation placing `i` before `j` for every `(i,j) ∈ C`
with `i<j` — a linear extension of the relation `C`, hence of `tc(C)`. So the two branches have
**the same columns**. Now take `(i,j) ∈ tc(C) \ C`. Branch `C` calls that pair incomparable and
therefore imposes `J_k(i,j) = J_k(j,i)` at every slot; but no column flips it, so `J_k(j,i) = 0`
and the row reads `J_k(i,j) = 0` — *`i` and `j` are never adjacent in that order either*. Branch
`tc(C)` imposes nothing there. Cap rows are unaffected: `build` writes a cap row only `if col:`,
and that pair's column set is empty. So `feasible(C) ⊆ feasible(tc(C))`. ∎

This is an *argument about the branch family*. **No poset is enumerated anywhere in this
instrument**; `mg-345e`'s and `mg-6bc2`'s refusal stands. `s3` PART A checks it on all `64`
branches at `n = 4` and all `1024` at `n = 5`, with `0` violations.

It also *explains* rather than merely records `mg-131e`'s finding that 99.5% of the hard
certificates were vacuous: the non-transitively-closed branches carry strictly more constraints
and go infeasible first.

**Theorem 1′ (the same fact, read forwards).** On a transitively closed branch, per-slot
symmetry is **exactly** the adjacent-transposition symmetry of `uniform L(P)`: swapping two
incomparable elements that are adjacent in a linear extension is a bijection of `L(P)` between
the two orders. So the symmetry-feasible set is never empty there — it contains `uniform L(P)` —
and **every infeasibility on such a branch comes from the `1/3` caps**. This is what makes the
search tractable and it is why §3's dead ends die the way they do.

---

## 3. Why the answer is not obvious: the two natural quadratic families are infeasible

To beat `Θ(n)` one needs `ω(n)` incomparable pairs each carrying a constant share of the cap.
The two families anyone would try first both die, and `s3` runs them.

* **Two disjoint chains** (`|I| = ab`, quadratic). **INFEASIBLE at every `(a,b)` with
  `a+b ≤ 10`**, in exact rationals. Not a near miss: the phase-1 residual *rises* with `n`
  (`1/3, 1/2, 5/9, …, 5/8, 17/27`).
* **Bands** `I = {(i,j) : j−i ≤ s}`. `s = 1` is `mg-131e`'s consecutive branch and gives
  `(n−1)/3` exactly. **Every `s ≥ 2` is INFEASIBLE**, at every `n` computed.

So a feasible branch's incomparability graph can be neither a block nor locally dense. The
family in §4 threads between them: quadratically many incomparable pairs, arranged as a
*staircase between two chains*.

---

## 4. The construction

Fix even `n = 2m`, `m ≥ 2`. Write `E = {e_0 < … < e_{m−1}} = {0,2,…,2m−2}` and
`O = {o_0 < … < o_{m−1}} = {1,3,…,2m−1}`.

**The branch.** `E` is a chain, `O` is a chain, and

```
e_k  <_P  o_l    iff   l ≥ k+1 ;        no odd is ever below an even.
```

Equivalently, the incomparable set is the `n−1` consecutive pairs together with every chord
`(odd i, even j)` with `j ≥ i+3` and `j ≤ 2m−2`; equivalently again,
`I = { {e_k, o_l} : l ≤ k }`, so **`|I| = m(m+1)/2` — quadratic in `n`.** The comparable set is
transitively closed (`s1` PART B checks it at every `n`), so this is a genuine comparability
pattern, not an artefact of `mg-200d` imposing no transitivity.

**Lattice-path coordinates.** A linear extension is an interleaving; record it as a path from
`(0,0)` to `(m,m)` with step `R` = "place the next even", `U` = "place the next odd". The
relation says `o_l` may not appear before `e_0,…,e_{l−1}`, i.e. the path stays in `{j ≤ i+1}`.
So `L(P)` is the set of ballot paths, `Catalan(m+1)` of them — which is why this family is
computable far past the range where a general branch is.

Two facts drop out of the coordinates and they are the reason the family works.

* **Each incomparable pair has exactly ONE non-trivial symmetry row.** `e_k` and `o_l` can be
  adjacent only at slots `(k+l, k+l+1)`, because the prefix before them is forced to be exactly
  `e_0..e_{k−1}, o_0..o_{l−1}`. The row says the two two-step routes from `(k,l)` to
  `(k+1,l+1)` carry equal mass:
  ```
  Pr[ at (k,l), then R, then U ]  =  Pr[ at (k,l), then U, then R ] .          CORNER(k,l)
  ```
* **The flip probabilities are order statistics.** Let `X_l` be the number of `R` steps before
  the `(l+1)`-th `U`. Then `q(e_k,o_l) = Pr[X_l ≥ k+1]` for `k ≥ l+1`, `q(e_l,o_l) = Pr[X_l = l]`,
  and `inv = Σ_l 1[X_l = l] + Σ_l (X_l − l − 1)⁺`.

**The measure.** Two parts; the split is forced, not tuned.

> **CASCADE** — total mass `1/3`. For `t = 1..m−1`, the path
> `A_t = R^(t+1) (U R)^* U^*`, each with weight `w = 1/(3(m−1))`.
> These carry the quadratically many chord inversions: `inv(A_t) = t(m−t) + t(t−1)/2`.
>
> **FENCE** — total mass `2/3`. `F_S` = the identity with block `k` (the pair `2k, 2k+1`)
> transposed for every `k ∈ S`, distributed as `2/3` times the symmetric two-state Markov
> measure `P` on `{in,out}^m` with `P[x_0 = in] = 1/2` and `P[x_k = x_{k−1}] = p = 1/(m−1)`.

`p = 1/(m−1) ≤ 1` for every `m ≥ 2`, so the measure is nonnegative at every `n`. **The Markov
parameter is not fitted.** `P[in] = 1/2` is what the distance-`0` corner forces; `p` is what the
distance-`1` corner forces against the cascade weight `w`. Both are read off Lemma 2 below.

### 4.1 Lemma 1 — where each atom's corners are

*(a)* `A_t`'s point sequence is `(0,0),…,(t+1,0),(t+1,1),(t+2,1),(t+2,2),…`, i.e. it visits
`(t+1+s, s)` and `(t+1+s, s+1)`. At `(t+1+s, s)` it goes `U` then `R`; at `(t+1+s, s+1)` it goes
`R` then `U`. So **`A_t` supplies the `RU` route at exactly the corners with `k − l = t`, and
the `UR` route at exactly those with `k − l = t+1`** (both for `k ≤ m−1`).

*(b)* `F_S` is a concatenation of blocks: unswapped block `k` is `(k,k)→(k+1,k)→(k+1,k+1)`,
swapped is `(k,k)→(k,k+1)→(k+1,k+1)`. Every visited point has `|i−j| ≤ 1`, so **a fence
contributes at no corner with `k − l ≥ 2`**. At `(k,k)` it supplies `RU` iff `k ∉ S` and `UR`
iff `k ∈ S`. At `(k+1,k)` it supplies `UR` iff blocks `k` **and** `k+1` are both unswapped, and
it can never supply `RU` there (that would need an `R` step out of `(k+1,k)`). ∎

### 4.2 Lemma 2 — `CORNER(k,l)` holds for every incomparable pair

Every incomparable pair is `{e_k, o_l}` with `0 ≤ l ≤ k ≤ m−1`. Write `d = k − l`.

* **`d ≥ 2`.** Fences contribute nothing (Lemma 1b). `RU` mass `= w` from `A_d`
  (`1 ≤ d ≤ m−1` ✓); `UR` mass `= w` from `A_{d−1}` (`1 ≤ d−1 ≤ m−2` ✓). **Equal.** The cascade
  balances symmetry *against itself* at every distance `≥ 2`, one shift apart.
* **`d = 1`.** `RU` mass `= w` from `A_1`. The `UR` route would come from `A_0` — and `A_0` is
  the identity path, which is **excluded**, because including it would push `q` at distance `1`
  over the cap. So the fence must supply it, and it does:
  `(2/3)·P[l ∉ S and l+1 ∉ S] = (2/3)·(1/2)p = 1/(3(m−1)) = w`. **Equal.** *This is the whole
  job of the fence, and it is what fixes `p = 1/(m−1)`.*
* **`d = 0`.** No cascade contributes. Fence: `RU = (2/3)P[k ∉ S] = 1/3`,
  `UR = (2/3)P[k ∈ S] = 1/3`. **Equal.** *This is what fixes `P[in] = 1/2`.* ∎

### 4.3 Lemma 3 — every cap holds, and the largest is exactly `1/3`

* `d = 0`: `q(e_k,o_k) = Pr[X_k = k] =` fence mass with block `k` swapped `= 1/3`. (Cascades
  have `X_k ≥ k+1`, so they contribute nothing.) **At the cap.**
* `d ≥ 1`: fences have `X_l ∈ {l, l+1}` and contribute `0`. `A_t` has `X_l = min(m, l+1+t)`, and
  since `k = l+d ≤ m−1` gives `l+d+1 ≤ m`, `X_l ≥ l+d+1 ⟺ t ≥ d`. So
  `q = w·#{t ∈ [1,m−1] : t ≥ d} = (m−d)/(3(m−1)) ≤ 1/3`, with equality iff `d = 1`. ∎

So `max_flip` is exactly `1/3` at every `n` and never exceeds it — which is what the
`maxflip` column of `s1` PART A reports.

### 4.4 Lemma 4 — the value

`inv(A_t) = Σ_{l} min(m−1−l, t) = t(m−t) + t(t−1)/2`, and `inv(F_S) = |S|`. Then

```
Σ_{t=1}^{m−1} inv(A_t)  =  m(m−1)(2m−1)/6 ,        E_P|S| = m/2 ,

E[inv]  =  w · m(m−1)(2m−1)/6  +  (2/3)(m/2)
        =  m(2m−1)/18  +  m/3
        =  m(2m+5)/18  =  n(n+5)/36 .                                              ∎
```

**Theorem 2.** *For every even `n ≥ 4` the disjunctive per-slot value is at least `n(n+5)/36`.
For odd `n` it is at least `(n−1)(n+4)/36` (append `n−1` as a top element: it is comparable to
everything, so it is never flipped and carries no symmetry row).* ∎

`s1` re-derives every claim of Lemmas 2–4 from the measure itself at `n = 4..24`, by direct
`Fraction` arithmetic through `mg-200d`'s own `measure_report`. **There is no simplex in that
path**, so no bug in any solver — mine or `mg-200d`'s — can make Theorem 2 wrong.

---

## 5. What dies, and what does not

### 5.1 Dead

**Daniel's route, as a wall-breaker.** The ticket's own framing: *"If it is `c·n + O(1)` for
some constant `c`, then Daniel's framing SURVIVES with `c` in place of `1/3`."* It is not. The
wall does **not** close above a larger threshold, because there is no threshold: the per-slot
value grows at the same *order* as the quantity it was supposed to beat.

Read in `mg-200d`'s normalisation, this is the cleanest statement of the death:

```
ε_spec  =  6 E[inv] / (n² − 1)   →   1/6      on this family,
```

whereas the baseline `M_n` value `n(n−1)/6` gives `ε_spec → 1`. **`ε_spec` does not tend to
zero.** `mg-200d`'s `2/(n+1)` did, which is exactly why it looked like a wall-breaker, and
`mg-131e` killed it at `n = 6`. Per-slot adjacency symmetry divides `ε_spec` by at most `6` and
cannot drive it to `0`.

> ⚠️ **The `1/6` above is a NUMERAL COINCIDENCE with `STATE.md` row 8's "pair bias gives `1/6`",
> and I am not claiming they are the same object.** Row 8 records `ε_sup < 1` and "pair bias
> gives `1/6`" as *the same theorem in two normalisations* (`mg-9adf`, on `mg-6bc2`). The `1/6`
> here is a limit of `ε_spec` in `mg-200d`'s normalisation, which in that dictionary is the
> `ε_spec = 1` end, improved sixfold. Whether the two `1/6`s are related is **not established
> here and must not be asserted from this document.** This lineage has committed a currency
> conflation twice (`mg-76b2` filed it in advance as its `P14`); this is the site where a third
> would go.

**`mg-200d`'s `Θ(n²) → Θ(n)` headline.** Refuted — and `mg-200d` had already narrowed it to
exactly the statement this refutes. Its own §7 says *"per-slot adjacency symmetry is worth
`Θ(n²) → Θ(n)` at `n ≤ 5` and the all-`n` statement is open"*; the all-`n` statement is now
closed, in the negative. The gain is a constant factor `≤ 6`.
`mg-131e` was right to leave it standing on its evidence and right to flag that the evidence was
three `n ≤ 5` points; the mechanism it identified — *"at `n ≤ 5` the optimum flips only
consecutive pairs; at `n = 6` a non-consecutive pair carries flip mass for the first time"* — is
exactly what this family scales up. `mg-131e`'s chord sub-family `{(2j+1, 2j+4)}` with value
`(5n−8)/12` is the `d ≤ 3` slice of it; taking chords at **every** distance, not just distance
`3`, is what turns a linear excess into a quadratic one.

### 5.2 NOT dead, and must not be read as dead

1. **The frozen-poset conjecture is untouched.** The disjunctive value is an **upper bound** on
   it. Showing an upper bound is **larger** than believed *weakens the bound* and says nothing
   whatever about the statement underneath. This is `mg-131e` §5.2 verbatim and it applies with
   more force here, because a superlinear answer is a more dramatic sentence than a linear one.
2. **`(LIB)` is untouched.** Nothing here bears on `STATE.md` row 8 except by removing one
   candidate *route* to it.
3. **This is not an `N₀` argument** and is **not** discharged by `mg-c4f5 §5.3`. That result
   closes extracting a threshold from the *qualitative* `o(n²)` hypothesis. This is an
   **explicit rate**, which `STATE.md` row 8 says is the permitted case, and it is settled on
   its own merits by exhibiting a measure.
4. **Tightness is open beyond `n = 3`** — `mg-200d`'s caveat, untouched. Nothing here claims the
   relaxation is attained by a real poset at any `n ≥ 4`, and no such claim is needed: the
   verdict is about the relaxation's own growth.
5. **`M_n` membership** is inherited from `mg-200d` and kept.

---

## 6. The one asymmetry to keep in mind when reading any number here

**Every `n ≥ 6` figure in this document is a LOWER bound found on a NAMED branch.** The true
maximum over branches at that `n` may be larger. `mg-131e` filed this as its warning 2 and it is
kept here.

That direction is **harmless** for a superlinear verdict — a larger maximum is still
superlinear — and would be **fatal** for a linear one. That is why the verdict is stated from
below and why `s4` reports, rather than hides, that its search is a greedy hill-climb: a branch
better than this one would *strengthen* the conclusion, not weaken it.

---

## 7. What was NOT done

* **No exhaustive `n = 6`.** The ticket forbids it and Theorem 1 does not license it. The
  reduction is a large cut (transitively closed branches only), but cheaper brute force is
  still brute force; the ticket says to mail `pm-onethird` and say why rather than start it. I
  did not start it and I did not ask, because the answer did not need it.
* **No proof that this family is the MAXIMUM.** It is proved to be a lower bound at every `n`,
  and computed to be *optimal on its own branch* at `n = 6,8,10,12`, and checked to be locally
  maximal under adding any single further pair at `n = 6,8,10` (`s4`). The maximum over all
  branches is not computed at any `n ≥ 6` and is not claimed.
* **No upper bound better than the trivial dual.** `val ≤ n(n−1)/6` is enough to pin the class,
  so the constant in `Θ(n²)` is bracketed only as `[1/36, 1/6]` and is **not** determined. If
  anyone wants the true constant, that is the next question and it is not answered here.
* **No exact LP at `n ≥ 14` on this family.** `n = 14` is `1430` columns; it was attempted and
  **did not finish**, so `s2` stops at `n = 12` and no `n = 14` branch value is reported or
  interpolated. The *witness's* value at `n ≥ 14` is carried by arithmetic (`s1`), which does
  not depend on any solver; the *branch's* value at those `n` is simply not computed.
* **No edit to any other document, no `L4`, no `C₃`, no `ε_dem`, no `.tex` sources opened.**
  **`STATE.md` does NOT carry this headline** — I checked before writing this line, and it does
  not mention `mg-200d`, `mg-131e`, `per-slot`, or `2/(n+1)` at all, so there is nothing to
  correct there and I am recording that rather than asserting a correction nobody needs. The
  three documents that DO carry it, and now need one, are
  `docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md` (`:25`, `:30`, `:319`),
  `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` (`:85`, `:310`), and
  `docs/OneThird-DualCertificate-mg-131e.md` (`:171`, whose "not refuted" is now refuted).
  Each is another landing's document; correcting them is a separate landing and is named in
  the mail to `pm-onethird`, not performed here.
* **No poset enumeration, and no re-derivation of `mg-200d`'s formulation.** As instructed.
