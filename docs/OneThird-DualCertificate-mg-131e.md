# Dual certificates for `mg-200d`'s `≤` direction — and the answer to whether they are `n`-indexed

`mg-131e` · instrument [`code/dual_certificate_131e/`](../code/dual_certificate_131e/) ·
parent `mg-200d` (`762921d`, `731a9ab`)

---

## 0. The result, first

> **`mg-200d`'s `≤` direction is certified at `n = 3, 4, 5`, and it is FALSE at `n = 6`.**

The certificates asked for exist and are in `d1`. The question they existed to answer —
are the multipliers `n`-indexed (a proof sketch for all `n`) or ad hoc (a small-n
coincidence)? — is answered not by fitting the multipliers but by killing the conjecture they
would have certified:

| `n` | 3 | 4 | 5 | **6** | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| `(n−1)/3` | `2/3` | `1` | `4/3` | `5/3` | `2` | `7/3` | `8/3` | `3` |
| disjunctive per-slot value | `= 2/3` | `= 1` | `= 4/3` | **`≥ 11/6`** | `≥ 20/9` | `≥ 8/3` | `≥ 28/9` | `≥ 7/2` |
| | exact | exact | exact | **refutes** | refutes | refutes | refutes | refutes |

At `n = 3, 4, 5` those are exact values (`mg-200d`, exhaustive) with matching dual certificates
here. From `n = 6` they are lower bounds from explicit feasible measures, and a lower bound
above `(n−1)/3` refutes.

**So: the equality is a small-n coincidence.** That is one of the two answers the ticket asked
for, and it is the one that stops the route being pursued as a wall-breaker.

---

## 1. What a certificate of the `≤` direction has to be

`mg-200d`'s value is a **maximum over `2^C(n,2)` branches**. For each subset `C` of pairs
declared comparable, the branch LP over the permutations flipping no pair of `C` is

```
max  Σ_p μ_p inv(p)
s.t. Σ_p μ_p = 1                                            free multiplier  λ
     q_ij(μ) ≤ 1/3          for ij ∈ I that some column flips      t_ij ≥ 0
     (bwd − fwd)_{ij,k}(μ) = 0   for ij ∈ I, slot k             free  s_{ij,k}
     μ ≥ 0
```

so the `≤` direction is `val(C) ≤ (n−1)/3` **for every branch `C`**, and a certificate is a
*family*, one per branch, covering the infeasible branches too. `verify_dual` checks a
candidate by direct `Fraction` arithmetic — sign conditions plus `Σᵢ yᵢ A_ij ≥ c_j` on every
column — with no simplex in the path, and returns the bound `y·b`.

**All `8 + 64 + 1024` branches are certified**, `0` failures, max certified bound exactly
`(n−1)/3` at each `n` (`out_d1_certificates.txt`). As a control, the dual optimum computed by a
separate LP run equals `mg-200d`'s primal optimum on **every** feasible branch — `3`, `13` and
`116` of them — which is strong duality across two independently written solves.

---

## 2. The piece that IS `n`-indexed, and it is a theorem

**The trivial dual.** Put `λ = 0`, `t ≡ 1` on every cap row, `s ≡ 0`. Every column of a branch
satisfies `flips(p) ⊆ I`, so `Σ_{ij ∈ flips(p)} t_ij = |flips(p)| = inv(p)` and the dual
constraint holds **with equality on every column**. It is feasible in every branch at every
`n`, with bound `|I_active|/3`. This is a proof, not a computation.

**Theorem.** *On the branch `I = {(i,i+1)}` — all consecutive pairs incomparable, everything
else comparable — the disjunctive per-slot value is exactly `(n−1)/3`, for every `n`.*

*Proof.* Every column flips only pairs of `I`, and each `(i,i+1)` is flipped by the adjacent
transposition, which is a column; so there are exactly `n−1` cap rows and the trivial dual gives
`≤ (n−1)/3`. `mg-200d`'s 3-atom fence — identity plus the even- and odd-index matchings, mass
`1/3` each — is feasible on that branch and attains `(n−1)/3`. ∎

No solver appears on either side. `d2` PART A runs it at `n = 3..8`.

This is real and it is `n`-indexed. It is also **one branch out of `2^C(n,2)`**, and it is the
*only* uniform certificate this instrument found.

---

## 3. Why three points could never have answered the question

A branch needs more than the trivial dual exactly when `|I_active| > n−1`. Splitting those by
whether the branch has any measures at all:

| `n` | branches | need more than trivial | of which **infeasible** (vacuous) | of which **feasible** (informative) |
|---|---|---|---|---|
| 3 | 8 | 1 | 1 | **0** |
| 4 | 64 | 18 | 18 | **0** |
| 5 | 1024 | 388 | 386 | **2** |

**99.5% of the hard certificates are vacuous** — a dual on a branch with no feasible measures
bounds a maximum over the empty set and says nothing about the conjecture. Pre-filed as the
error `P12` before any script existed, and it fired.

Which leaves the informative sequence `0, 0, 2`. **The phenomenon the ticket asks about does
not occur at `n = 3` or `n = 4` at all.** There is no `n = 3` or `n = 4` instance of the object
whose multipliers one would compare. Three points was one point.

That is why the certificates at `n = 3` and `n = 4` are almost content-free, which was hand-
measured and disclosed in `PREDICTIONS.md §0 H4` before anything was run.

### 3.1 And at that one point the natural `n`-indexed shape is excluded outright

The obvious guess is `t` = indicator of the `n−1` consecutive pairs with `λ = 0`, because its
objective is exactly `(n−1)/3` for every `n`. On both informative hard branches at `n = 5`, LP
over the **whole dual optimal face** gives

```
λ ∈ [−1995/2, −1]        ← λ < 0 across the entire face
t_(1,3) ∈ [0, 0]         ← forced to zero
```

So no certificate at those branches has `λ = 0`, and none has `t` an indicator vector. This is
not "I did not find one": the shape is unavailable. Correspondingly the consecutive-pairs dual
discharges `0` branches at every `n` tested that the trivial dual had not already discharged.

---

## 4. The refutation at `n = 6`

Take `I = {(0,1),(1,2),(2,3),(3,4),(4,5)} ∪ {(1,4)}`, everything else comparable. The measure

| atom | mass | `inv` |
|---|---|---|
| `(0,1,2,3,5,4)` | `1/6` | 1 |
| `(0,1,3,2,5,4)` | `1/6` | 2 |
| `(0,2,1,4,3,5)` | `1/6` | 2 |
| `(0,2,4,1,3,5)` | `1/6` | 3 |
| `(1,0,2,3,4,5)` | `1/6` | 1 |
| `(1,0,3,2,4,5)` | `1/6` | 2 |

has, checked by direct arithmetic through `mg-200d`'s own `measure_report` and not by any
solver: mass `1`; every flip probability `≤ 1/3` (the five consecutive pairs at `1/3`, the pair
`(1,4)` at `1/6`); **no comparable pair ever flipped**; **zero per-slot symmetry violations on
any incomparable pair**; and

```
E[inv] = 11/6 > 5/3 = (n−1)/3          ε_spec = 11/35 > 2/7 = 2/(n+1)
```

The conjecture is false at `n = 6`. The whole of `d3` runs without touching the LP.

**Three things that make this hard to explain away.**

* **The refuting branch is a genuine comparability pattern.** `mg-200d` imposes no transitivity
  — that is what keeps its value an upper bound — so a refutation on a non-transitive branch
  would have been much weaker. This branch's comparable set **is** transitive, and `d3` checks
  that rather than asserting it.
* **The excess grows.** On the periodic sub-family `chords = {(2j+1, 2j+4)}` the value is
  `(5n−8)/12`, checked at `n = 6, 8, 10`, against `(n−1)/3 = (4n−4)/12`. The gap `(n−4)/12` is
  **linear in `n`** — not a boundary wobble a nearby constant would absorb.
* **The mechanism is visible and is exactly what `n ≤ 5` could not show.** At every one of the
  `52` value-positive branches at `n = 5`, the optimum flips **only consecutive pairs**. At
  `n = 6` a non-consecutive pair carries flip mass for the first time (`q_(1,4) = 1/6`), and
  that is the whole excess. `n ≤ 5` is too small to hold the gadget.

---

## 5. What this does and does not kill

**Killed.** `ε_spec = 2/(n+1)` as a theorem, and with it "proving the `≤` direction at all `n`
would be the (LIB) residual". There is nothing at all `n` to prove: the statement is false from
`n = 6`. Daniel's *"if we could decisively prove the conjecture above some reasonable bound"* —
this conjecture cannot be proved above any bound, because it fails immediately above the range
where it was measured.

**Not killed, and must not be read as killed.**

1. **The frozen-poset conjecture is untouched.** The disjunctive value is an *upper bound* on
   it. Showing the upper bound is bigger than believed weakens the bound; it says nothing about
   the statement underneath.
2. **`mg-200d`'s `Θ(n²) → Θ(n)` headline is not refuted.** Every value here is still linear in
   `n`. What died is the **constant**, i.e. the exact formula. Note, though, that the exact
   values supporting `Θ(n)` are the same `n ≤ 5` that supported the formula which is now false,
   so the *rate* is now evidenced by three points and no proof, and the correction at `n = 6..10`
   runs **upward** — a smaller gain than `mg-200d`'s formula claims, not a larger one.
3. **Per-slot symmetry is still worth a great deal.** `(5n−8)/12` against the baseline
   `n(n−1)/6` is still `Θ(n²) → Θ(n)` on this sub-family. The finding is that its constant is
   not `1/3` and is not yet known.
4. **Nothing here is an `N₀` argument.** `mg-c4f5 §5.3` — no `N₀` works for the class — is about
   extracting a threshold from the *qualitative* hypothesis `o(n²)`, and this route was about
   proving an *explicit rate*, which `STATE.md` row 8 says is the permitted case. This document
   does **not** discharge the route by citation to §5.3; it refutes the specific rate on its own
   merits, by exhibiting a measure. Anyone reading this as a re-run of §5.3 has the wrong
   result.

**The live question that replaces it.** *What is the true growth of the disjunctive per-slot
value?* If it is `cn + O(1)` for some constant `c`, the route survives with `c` in place of
`1/3` and Daniel's framing is intact — the wall closes above a (larger) threshold. That is now
the thing to measure, and it is a different question from the one this ticket was given, so it
is not answered here.

---

## 6. Inherited premises and standing caveats, kept

* **`M_n` membership.** Everything is sound relative to the premise, named by `mg-200d` and kept
  here, that the target posets lie in `M_n` at all. Nothing further is needed and nothing
  further is claimed.
* **No poset enumeration.** No poset is constructed, transitivity is never imposed, and every
  branch is a set of measures on `S_n`. `mg-345e`'s and `mg-6bc2`'s refusal stands. That the
  `n = 6` refuting branch happens to be transitive is a *checked property of the answer*, not an
  enumeration of the class.
* **Tightness is open beyond `n = 3`.** `mg-200d`'s caveat is untouched. Nothing here claims the
  relaxation is attained by a real poset at any `n ≥ 4`; the `n = 6` witness's own poset has
  `uniform L(P)` with max flip `5/14 > 1/3`, so it is **not** in `M_6`.

---

## 7. What was NOT done

* **No exhaustive `n = 6`.** `32768` branches over `720` columns; the ticket forbids extending
  the brute force and this instrument did not. Every `n ≥ 6` number is a **lower** bound found
  on a **named** branch, so the true `n = 6` maximum may be larger than `11/6`.
* **No general construction for all `n`.** The refuting witnesses are hard-coded at
  `n = 6,7,8,9,10` and directly verified. `(5n−8)/12` is checked at `n = 6, 8, 10` on one
  sub-family and is **not** proved for all `n`. An explicit family, checked at `n = 3..20` the
  way `mg-200d`'s fence is, was not written — so "false at `n = 6`" is a theorem here and "false
  for every `n ≥ 6`" is not.
* **No Farkas certificates for the infeasible branches.** They are discharged by a dual with
  objective `≤ (n−1)/3` (always available) plus the recorded fact that they are infeasible. A
  Farkas certificate would be the cleaner object and was not produced.
* **No search for the true growth constant.** §5's replacement question is stated and not
  answered.
* **No re-derivation of `mg-200d`'s formulation, and no "fix" of the literal form's
  infeasibility.** As instructed.
* **No `L4`, no `C₃`, no `ε_dem`, no `.tex` sources opened, no `STATE.md` edit.** `STATE.md`
  carries `mg-200d`'s conjecture and now needs a correction; that is a separate landing and is
  named in the mail to `pm-onethird`, not performed here.
