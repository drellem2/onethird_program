# What does PER-SLOT adjacency symmetry buy?

**Work item.** `mg-200d` (repo `onethird_program`), filed by `pm-onethird` as the one live lever
left after `mg-6bc2` closed the pair-marginals route in both directions.
**Instrument.** `code/perslot_symmetry_200d/` · **Predictions** committed at `b5784ee`, before
any script of this instrument existed, with eight hand measurements disclosed and two
most-likely errors filed in advance (`P12`, `P13`).
**Method.** Hand derivation, plus exact-rational LPs over measures on `S_n`, on an independently
written two-phase simplex sharing no code with `mg-6bc2`'s. **No poset enumeration** — §7 says
why the disjunctive program is not one in disguise.
**Parent.** `mg-6bc2` **landed on `main` as `e1f7bb2` at 2026-08-07 18:21**, while this ticket
was in the merge queue. It was read out of branch `polecat-a6bc2` (`90d19e7`) throughout; the
rebase changed the hash and **not the content** — `lp6bc2.py`, `v2_optimiser.py`,
`out_v2_optimiser.txt` and its document are byte-identical between the two, checked by `git diff`
after it landed. **So §8's two corrections apply to what is on `main`, not only to what was on a
branch.**

---

## 0. Verdict

> ## **PER-SLOT ADJACENCY SYMMETRY BUYS A FACTOR THAT GROWS WITH `n`, NOT A CONSTANT — AND THE TICKET'S OWN SIZING PARAGRAPH IS WRONG BECAUSE OF IT.**
>
> Imposed **soundly**, per-slot adjacency symmetry takes the relaxation value from
> `C(n,2)/3` down to **`(n−1)/3`** — from `Θ(n²)` to `Θ(n)`:
>
> | | `n = 3` | `n = 4` | `n = 5` | as `n → ∞` |
> |---|---|---|---|---|
> | **baseline** `M_n` alone (`mg-6bc2`) | `1` | `2` | `10/3` | `ε_spec = n/(n+1) → 1` |
> | **+ per-slot adjacency symmetry** | **`2/3`** | **`1`** | **`4/3`** | **`ε_spec = 2/(n+1) → 0`** |
> | ratio | `2/3` | `1/2` | `2/5` | `→ 0` |
>
> **The gain is not a constant factor.** The ticket sized this ticket in advance as *"a
> milestone, not a wall-breaker, and the writeup must say which"*, on the assumption that a
> result here would move `d·q̄` by a constant. **It does not, and that instruction cannot be
> obeyed as written:** at `ε_spec = 2/(n+1)`, Daniel's `1/6` is reached at `n ≥ 11` and the
> wall's `≈ 2×10⁻²` at `n ≥ 99`. §6 states both sizings and the condition they hang on.
>
> ### The condition, stated at the same volume as the result
>
> **`(n−1)/3` is EXACT only at `n ∈ {3, 4, 5}` — a finite population, three points.** The
> `≥` direction is a **theorem for every `n`** (an explicit 3-atom construction, §4.2). The
> `≤` direction is a **CONJECTURE and is not proven here.** It must be read with the
> suspicion due to something that strong: **a proof of it at all `n` would be a proof of the
> `LIB` face** (`E[inv_e] = O(n)`) for the class `M_n` — which `STATE.md:179` records as the
> open residual and which obstruction 4 says is hard. If a three-point extrapolation is
> going to break, this is where.

### Three findings the ticket did not ask for and which change what it asked

1. **The literal reading of this ticket is UNSOUND, and provably so.** Per-slot symmetry
   `J_k(x,y) = J_k(y,x)` imposed on **every** pair holds for `uniform L(P)` **iff `P` is an
   antichain** — any cover `x ⋖ y` breaks it. So does the aggregate form. Imposing it as
   written excludes **every realisable measure in the relaxation**, and the LP duly returns
   **INFEASIBLE at `n = 3, 4, 5`**. A number obtained that way would have been an upper bound
   for nothing. §2.

2. **The sound BRANCH-FREE form buys exactly NOTHING.** The sharpest linear consequence of
   realisability that needs no case split is `J_k(y,x) ≤ J_k(x,y)`, and the value under it is
   `C(n,2)/3` — unchanged — at `n = 3, 4, 5, 6`. **All of the information is in the
   non-convexity**, i.e. in the fact that "comparable *or* symmetric" is a disjunction. §3.

3. **`mg-6bc2`'s aggregate/per-slot distinction SURVIVES being made sound, and is now a
   number.** Its finding was that the aggregate form excludes nothing at `n = 3` while the
   per-slot form kills every optimiser. Made sound, the aggregate form gives `2/3, 5/3, 7/3`
   against the per-slot `2/3, 1, 4/3` — **strictly weaker from `n = 4` on, and with no decay
   in `ε_spec` at all**. §5.

### Two corrections to `mg-6bc2`

Both are about its `§5` measurement table, not about its theorem, which reproduces exactly here.

1. **Its optimisers are SUB-PROBABILITY measures and its adjacency diagnostics are computed on
   them.** Its LP carries `Σ μ ≤ 1`; its published `n = 3` support has total mass `2/3`.
   Completing it to a measure (the `1/3` goes on the identity, which changes no objective
   value) turns its headline *"the aggregate form excludes nothing at `n = 3`"* from `0`
   violations to `2`. §8.1.
2. **The two columns of its `§5` table are in different units.** Its aggregate predicate
   iterates **ordered** adjacency keys; its per-slot predicate iterates `x < y`. `6` vs `8` at
   `n = 4` is not a comparison. §8.2.

---

## 1. The object, and the one premise it inherits

`mg-6bc2`'s relaxation, unchanged:

> `M_n` := every probability measure `μ` on `S_n` with `Pr_μ[j precedes i] ≤ 1/3` for every
> pair `i < j`, the reference order `e` being the identity.

**THEOREM (`mg-6bc2`, `90d19e7`).** `max_{μ ∈ M_n} E[inv_e] = C(n,2)/3`, attained;
equivalently `ε_spec = 6E/(n²−1) = n/(n+1)`. Reproduced here on an independent solver at
`n = 3, 4, 5, 6` (`selftest200d.py` S1, `out_v1_n6.txt`, `out_v1b_n6_surrogates.txt`).

**The single inherited premise is that the target posets lie in `M_n` at all** — that a frozen
poset has a coherent reference order. That is `mg-6bc2`'s premise, and `mg-61bb`'s result that
coherence follows from frozenness; **I did not re-derive it.** Everything this document adds is
sound *relative to membership in `M_n`* and needs nothing further, because:

**LEMMA 1.1 (no extra hypothesis is smuggled in).** If `μ = uniform(L(P)) ∈ M_n` then the
identity `e` is a linear extension of `P`. *Proof.* If `x < y` as integers but `y <_P x`, then
`y` precedes `x` in every linear extension, so that pair's flip probability is `1 > 1/3`. ∎

So the comparability structure used below is *forced* by membership in `M_n`; **this document
rests on exactly the premise `mg-6bc2`'s own theorem rests on, no more.**

---

## 2. The literal reading is unsound, and the LP says so

`mg-92e6`'s lemma, as `mg-6bc2` states it at its `§5`, is about **incomparable** pairs: for
`x,y` incomparable the swap map is a bijection of `L(P)`, so `J_k(x,y) = J_k(y,x)` at every
slot `k`. `mg-6bc2`'s scripts then test **all** pairs.

**THEOREM 2.1 (all `n ≥ 2`).** For a poset `P`, `uniform(L(P))` satisfies
`J_k(x,y) = J_k(y,x)` for **all** pairs and all `k` **iff `P` is an antichain**. The same
holds for the aggregate form `J(x,y) = J(y,x)`.

*Proof.* (⇐) All of `S_n`, uniform, is symmetric under every adjacent transposition. (⇒) If
`P` is not an antichain it has a cover `x ⋖ y`; some `L ∈ L(P)` places `y` immediately after
`x`, at some slot `k`, so `J_k(x,y) > 0`, while `x <_P y` gives `J_k(y,x) = 0` for every `k`.
Summing over `k` gives the aggregate form. ∎

**COROLLARY 2.2.** `M_n ∩ {all-pairs adjacency symmetry} ∩ {realisable} = ∅` for `n ≥ 2`: the
only realisable measures satisfying the literal form are antichains, and an antichain's uniform
measure has every pair flipped with probability `1/2 > 1/3`. **A value computed under the
literal reading is not an upper bound for any poset whatsoever.**

**MEASURED.** The literal LPs are not merely unsound, they are **empty**:

| `n` | literal per-slot | literal aggregate |
|---|---|---|
| 3 | INFEASIBLE (phase-1 residual `1/3`) | INFEASIBLE (`1/3`) |
| 4 | INFEASIBLE (`1/3`) | INFEASIBLE (`1/5`) |
| 5 | INFEASIBLE (`1/3`) | INFEASIBLE (`1/6`) |

At `n = 3` the reason is visible by hand and was filed as `H4` before any script ran: the six
equations `J_k(x,y) = J_k(y,x)` (3 pairs × 2 slots) force the **uniform** measure on `S₃`, whose
pair flips are `1/2`. Checked at `S4b`/`S4c`.

> **This is what makes the ticket's framing of the lever a trap rather than a lever.** *"The
> per-slot form is VIOLATED BY EVERY OPTIMISER at every `n` tested"* is true, and it is also true
> of every non-antichain poset. A constraint that excludes the optimisers **and** the intended
> conclusions excludes nothing useful; the work is entirely in imposing it only where
> realisability actually forces it.

---

## 3. The sound branch-free form, and why it buys nothing

**LEMMA 3.1 (sound, branch-free, all `n`).** For every poset `P` with `uniform(L(P)) ∈ M_n`
and every pair `x < y` and slot `k`: **`J_k(y,x) ≤ J_k(x,y)`**. Likewise `J(y,x) ≤ J(x,y)`.

*Proof.* By Lemma 1.1, `e` is a linear extension. If `x, y` are comparable then `x <_P y`, so
`J_k(y,x) = 0`. If incomparable, `mg-92e6` gives equality. ∎

This is the tightest *single linear inequality* implied by the disjunction "comparable **or**
symmetric" — it is satisfied in both branches, so it is valid for their convex hull.

**MEASURED — it buys nothing:**

| `n` | baseline | surrogate per-slot | surrogate aggregate |
|---|---|---|---|
| 3 | `1` | `1` | `1` |
| 4 | `2` | `2` | `2` |
| 5 | `10/3` | `10/3` | `10/3` |
| 6 | `5` | `5` | `5` |

*(The `n = 6` row is measured in `out_v1b_n6_surrogates.txt`, solved separately: `v1_forms.py 6`
runs the LITERAL forms first, and at `n = 6` those are 720 columns against 75 **equality** rows,
so phase 1 carries 76 artificials and did not finish in this run's budget. The surrogate forms
are inequality-only and solve quickly. **The `n = 6` literal values are therefore NOT measured
here** — §2's infeasibility table stops at `n = 5` and is not extrapolated.)*

Hand-verified at `n = 3` before any script (`H6`): `μ(id) = 1/3` and `1/6` each on `(0,2,1)`,
`(1,0,2)`, `(1,2,0)`, `(2,0,1)` is feasible for the caps, satisfies all six surrogate
inequalities, and has `E[inv] = 1`.

> **So the whole of what adjacency symmetry contributes lives in the NON-CONVEXITY of
> realisability, not in any linear consequence of it.** Convexifying the disjunction destroys
> the information completely. That is worth recording on its own: it says that any future
> attack that relaxes realisability to a linear program *without branching* cannot use this
> lemma at all, however cleverly it is written.

---

## 4. The answer: the disjunctive value

### 4.1 The program

Realisability says, of each pair `x < y` **independently**:

> **either** `x, y` are comparable — and then `q_xy = Pr[y before x] = 0`
> **or** they are incomparable — and then `J_k(x,y) = J_k(y,x)` for every slot `k`

so the feasible set is a union of `2^C(n,2)` polytopes, and the exact value is the maximum over
branches. Each branch is solved in exact rationals; comparability is imposed by deleting the
columns that flip the pair.

**THEOREM 4.1 (soundness, all `n`).** Every `μ = uniform(L(P)) ∈ M_n` is feasible in the branch
indexed by `P`'s own comparability relation. Hence the maximum over branches is an upper bound
on `E[inv_e]` for every such `P`. *(Machine control: `selftest200d.py` `S6`, on nine hand-named
posets.)*

### 4.2 The value

**FINITE POPULATION, `n ∈ {3, 4, 5}` — exact, by exhaustive branch enumeration:**

| `n` | branches | feasible | **max `E[inv]`** | `ε_spec` | `(n−1)/3` | `2/(n+1)` | attaining branch |
|---|---|---|---|---|---|---|---|
| 3 | 8 | 3 | **`2/3`** | **`1/2`** | `2/3` ✓ | `1/2` ✓ | `{0,2}` comparable |
| 4 | 64 | 13 | **`1`** | **`2/5`** | `1` ✓ | `2/5` ✓ | `{0,2},{0,3},{1,3}` |
| 5 | 1024 | 116 | **`4/3`** | **`1/3`** | `4/3` ✓ | `1/3` ✓ | `{0,2},{0,3},{1,4},{2,4}` |

**Attained?** Yes — these are LPs over non-empty compact polytopes, and the witness is explicit.
At every `n` the optimum is attained by a **3-atom** measure at `max flip = 1/3` exactly. At
`n = 5`:

```
mass 1/3  (0,1,2,3,4)   mass 1/3  (0,2,1,4,3)   mass 1/3  (1,0,3,2,4)
```

**Attained by a REAL POSET?** **At `n = 3`, yes.** The optimal branch's poset is `0 < 2` with `1`
free; `L(P) = {012, 021, 102}` and the uniform measure on it **is** the LP's witness, has
`max flip = 1/3` and `E[inv] = 2/3`. So **the relaxation is TIGHT at `n = 3`**, and the tight
example is the classic `δ = 1/3` extremal poset. At `n = 4` and `n = 5` the attaining branch's
own uniform-`L(P)` measure is **not** in `M_n` (`max flip = 2/5`, resp. the branch is not even
transitive), so tightness beyond `n = 3` is **open and is not claimed**.

**THEOREM 4.2 (lower bound, every `n ≥ 3`).** The disjunctive per-slot value is `≥ (n−1)/3`.

*Construction.* Take the branch in which `x, y` are incomparable exactly when `y = x+1`. Put
mass `1/3` on each of: the identity; the product of the transpositions at **even** slot indices;
the product at **odd** slot indices. Each of the `n−1` consecutive pairs is flipped in exactly
one atom, so `q = 1/3` for each and `E[inv] = (n−1)/3`; every non-consecutive pair is never
flipped; and at each slot `k` the identity supplies `J_k(k,k+1) = 1/3` while whichever matching
owns index `k` supplies `J_k(k+1,k) = 1/3`, which is the symmetry — every other adjacency the
atoms create spans distance 3 and so sits on a **comparable** pair, which carries no constraint.
∎ *(Checked directly, without the LP, at every `n` from 3 to 20: `out_v3_families.txt` §V3b.)*

**CONJECTURE 4.3 (NOT PROVEN).** The disjunctive per-slot value is **exactly** `(n−1)/3` for
every `n`, i.e. `ε_spec = 2/(n+1)`.

Evidence and its limits, stated together:
- exact and matching at `n = 3, 4, 5` (exhaustive);
- at `n = 6` the same construction's branch gives exactly `5/3 = (n−1)/3` and `ε_spec = 2/7`, but
  `n = 6` is `32768` branches over `720` columns and **the exhaustive maximum was not computed**;
- a **lower-bound search** at `n = 4, 5, 6` over window families, block families and a
  deterministic random sweep found **nothing above `(n−1)/3`** — and that search can only refute
  the conjecture, never confirm it. Every line of `v3_families.py` prints that asymmetry.

> **Treat 4.3 with suspicion proportional to its strength.** `ε_spec = 2/(n+1) → 0` is
> `E[inv_e] = Θ(n)`, which *is* the `LIB` face. The corpus records that face as open and records
> (obstruction 4, `STATE.md:135`) that it fails for abstract frozen distributions — the two-atom
> law has `Θ(n²)` inversions with every pair frozen. **Adjacency symmetry is exactly what kills
> the two-atom law here** (it has every pair flipped at `1/3`, so every pair must sit in the
> incomparable branch, which is the literal all-pairs form, which §2 shows is empty) — so the
> mechanism is the right one and it is the one `STATE.md:156` named as *"the extra juice"*. That
> makes 4.3 plausible **and** makes a three-point extrapolation to it exactly the kind of claim
> this corpus has been burned by. **The next move is a dual certificate at `n = 3, 4, 5`, not
> more brute force.**

---

## 5. Aggregate vs per-slot, made sound

`mg-6bc2`'s load-bearing distinction, re-measured on the sound program:

| `n` | baseline | **disjunctive per-slot** | disjunctive aggregate | control: branching, no symmetry |
|---|---|---|---|---|
| 3 | `1` (`ε = 3/4`) | **`2/3`** (`ε = 1/2`) | `2/3` (`ε = 1/2`) | `1` (`ε = 3/4`) |
| 4 | `2` (`ε = 4/5`) | **`1`** (`ε = 2/5`) | `5/3` (`ε = 2/3`) | `2` (`ε = 4/5`) |
| 5 | `10/3` (`ε = 5/6`) | **`4/3`** (`ε = 1/3`) | `7/3` (`ε = 7/12`) | `10/3` (`ε = 5/6`) |

**The distinction survives, and it inverts `mg-6bc2`'s reading of where each form bites.** Its
measurement was that the aggregate form *excludes nothing* at `n = 3`; on the sound program the
two forms **agree** at `n = 3` and separate from `n = 4` on, with the per-slot form worth a
further factor of `5/3` and then `7/4`. And the aggregate form's `ε_spec` — `1/2, 2/3, 7/12` —
**shows no decay at all**: whatever the aggregate form buys, it is not the `Θ(n²) → Θ(n)` drop.
`mg-6bc2`'s recommendation to reach for the per-slot form rather than the aggregate one is
**confirmed, for a reason different from the one it gave.**

### The control that decides whether any of this is real

`P13`, filed in advance, was that I would report as "bought by adjacency symmetry" a gain
actually bought by the branch structure. The control is the third column: **the same
`2^C(n,2)` branching with no symmetry constraint at all.** `{q = 0} ∪ {q ≤ 1/3}` *is*
`{q ≤ 1/3}`, so it must return the baseline. **It does, at every `n`: `1`, `2`, `10/3`, on
`8/8`, `64/64` and `1024/1024` feasible branches.** The entire gain is attributable to symmetry.

---

## 6. Sizing — and the ticket's sizing instruction is corrected

The ticket states `ε_spec = 3·d·q̄·n/(n+1)` exactly, with `d·q̄ = 1/3` today (`ε_spec → 1`),
Daniel's `1/6` needing `d·q̄ ≤ 1/18`, and closing the wall needing `d·q̄ ≤ 1/150`. It then
instructs: *"A result here is a milestone, not a wall-breaker, and the writeup must say which."*

**That instruction presupposes a constant-factor gain and cannot be obeyed as written.** The
measured gain replaces the factor `n/(n+1)` by `2/(n+1)` — equivalently `d·q̄ = 2/(3n)`, which
is not a constant:

| target | needs `ε_spec ≤` | reached at |
|---|---|---|
| Daniel's `1/6` | `1/6` | **`n ≥ 11`** |
| closing the wall (`≈ 2×10⁻²`, the optimistic `C₃ = 1` value) | `1/50` | **`n ≥ 99`** |

So, stated at the strength it actually has and no more:

- **At `n ∈ {3,4,5}` — a theorem about the relaxation, finite population.** `ε_spec` is `1/2`,
  `2/5`, `1/3` where the baseline gives `3/4`, `4/5`, `5/6`. On its own that is **a milestone**:
  three small `n`, and `1/3` is nowhere near `1/50`.
- **Under Conjecture 4.3 — which is NOT proven here.** It is **a wall-breaker for `n ≥ 99`**,
  and the master bound is primitive from `n ≥ 100`. That coincidence is not evidence for the
  conjecture; it is a consequence of any bound that tends to `0`.

**Do not carry `ε_spec = 2/(n+1)` as an established figure.** It is exact at three values of `n`
and conjectural elsewhere, and the honest one-line form is: *per-slot adjacency symmetry is
worth `Θ(n²) → Θ(n)` at `n ≤ 5` and the all-`n` statement is open.*

---

## 7. Why the disjunctive program is not the enumeration that was refused

`mg-345e` and `mg-6bc2` both declared and refused poset enumeration, and this ticket repeats the
refusal with its reason: **if `1/3–2/3` holds the frozen class is EMPTY**, so the question is
about measures on `S_n`. `P12` filed in advance that I would either refuse the disjunctive
program on those grounds and lose the finding, or run it while pretending the question did not
arise. Neither: the question is answered.

- **No poset is constructed and none is enumerated.** The index set is subsets of pairs; each
  branch is a set of **measures on `S_n`**, and the objective is over measures.
- **Transitivity is never imposed.** The branch family is a strict **superset** of the
  comparability patterns of real posets — which is exactly what keeps the maximum an **upper
  bound** rather than a search over a possibly-empty class. The `n = 5` optimum lands on a
  branch that **is not transitive** and therefore is not any poset's pattern; a poset-enumerating
  instrument could not have found it and would have reported a smaller number.
- **The emptiness argument does not apply.** An empty class makes a *search* vacuous; it does
  not make an *upper bound over a superset* vacuous.

What imposing transitivity would do is shrink the feasible set further, so `(n−1)/3` would remain
an upper bound. **That was not computed** and is the obvious next lever.

---

## 8. Corrections to `mg-6bc2`

### 8.1 Its optimisers are sub-probability measures, and its adjacency table is computed on them

`lp6bc2.py:relaxation_lp` carries `Σ μ ≤ 1`, which is harmless for the objective (the slack can
go on the identity, `inv = 0`) but **not** for any adjacency statistic. Its published `n = 3`
optimiser is `{(0,2,1): 1/3, (1,2,0): 1/3}` — **total mass `2/3`**. Completing it:

| | mass | `E[inv]` | aggregate violations | per-slot violations |
|---|---|---|---|---|
| as published | `2/3` | `1` | **`0`** | `4` |
| completed with `1/3` on the identity | `1` | `1` | **`2`** (3 in its own ordered unit) | `4` |

So `mg-6bc2`'s headline — *"At `n = 3` the aggregate form is satisfied by an optimiser and
therefore excludes nothing"* — **is an artefact of a measure with a third of its mass missing.**
Its `P6` is scored `REFUTED` in its own document on the strength of that `0`; the refutation
stands (its `P6` predicted violation and the per-slot count is `4`), but the sentence about the
aggregate form does not. §S2 of the selftest drives this.

*(My own hand measurement `H7` predicted the completed count would be `4`. It is `2` in this
document's unit and `3` in `mg-6bc2`'s. **`H7` is REFUTED on the number and kept as written**; its
substance — `0` becomes nonzero — holds.)*

### 8.2 The two columns of its §5 table are in different units

`lp6bc2.py:measure_stats` builds `adj` keyed on **ordered** pairs and reports violations by
iterating those keys; `v2_optimiser.py:per_slot_violations` iterates `x < y` and slots. So
"aggregate 6, per-slot 8" at `n = 4` compares ordered pairs against `(unordered pair, slot)`
incidences. Checked at `S2g`/`S2h`.

**Neither correction touches `mg-6bc2`'s theorem**, which reproduces exactly here at
`n = 3, 4, 5, 6` on an independent two-phase solver (`S1`).

---

## 9. Predictions, scored

Committed at `b5784ee` before any script existed. Kept as written.

| # | prediction | outcome |
|---|---|---|
| P1 | baseline returns `C(n,2)/3` at `n = 3..6` | **HELD** |
| P2 | sound branch-free per-slot surrogate buys nothing | **HELD** |
| P3 | sound aggregate surrogate buys nothing | **HELD** |
| P4 | disjunctive per-slot strictly below `C(n,2)/3` at every `n ≥ 3` | **HELD** at `n = 3,4,5` |
| P5 | disjunctive value at `n = 3` is exactly `2/3` on the branch with `{0,2}` comparable | **HELD, exactly** |
| P6 | sound aggregate strictly larger than sound per-slot at some `n ≤ 5` | **HELD** (`5/3` vs `1` at `n = 4`) |
| P7 | branching with no symmetry returns exactly `C(n,2)/3` | **HELD** at `n = 3,4,5` — the control that makes §5 readable |
| P8 | literal per-slot infeasible at `n = 3`, **feasible at `n = 4,5`** | **REFUTED.** Infeasible at `n = 4` and `n = 5` too. I reasoned from unknowns-vs-equations and the caps bind long before the count does. |
| P9 | literal aggregate feasible at `n = 3` with value in `(2/3, 1)` | **REFUTED.** Infeasible at `n = 3, 4, 5`. |
| P10 | the ratio to baseline does not fall over `n = 3,4,5`; expect a factor near `3/2`; *"a milestone, not a wall-breaker"* | **REFUTED, and this is the finding.** The ratio is `2/3, 1/2, 2/5` — it falls, the gain compounds, and §6 says why the sizing verdict I pre-committed to is the wrong shape. |
| P11 | `n = 6` reached branch-free, not disjunctively | **HELD** |
| P12 | (my likely error) refusing or fudging the enumeration question | did not fire — §7 answers it |
| P13 | (my likely error) mis-attributing the branch structure's gain to symmetry | did not fire — the control in §5 was run and is clean |

## 10. Defects of this instrument, left in the code

1. **My first general construction for Theorem 4.2 was wrong, and it was wrong in the way that
   would have survived a weaker check.** 3-colouring the `n−1` consecutive pairs by index mod 3
   hits `E[inv] = (n−1)/3` **and** the `1/3` cap at every `n`, and **violates per-slot symmetry
   from `n = 4` up.** Had `v3_families.py` checked only the value and the cap — the two things I
   was trying to achieve — it would have passed. The refuted version is kept in the file
   (`v3_families.py`, commented, above `fence_atoms`).
2. **The randomised sweep's first version drew branch membership from an LCG's low bit**, which
   is periodic, and returned `0/60` feasible at `n = 4` — a sweep that had searched nothing while
   printing a verdict line. Fixed to bit 16; the fix is commented at the call site.
3. **`H7`, a hand measurement, was wrong on its number** (§8.1) and is kept as written.

## 11. What I did not do — declared, not discovered later

- **No proof of Conjecture 4.3.** The `≤` direction at general `n` is open. No dual certificate
  was extracted at `n = 3, 4, 5`, and that is the cheapest next step.
- **No exhaustive disjunctive value at `n ≥ 6`.** `n = 6` is `32768` branches over `720`
  columns; only window/block families and a `60`-branch sweep were run there, and those give
  **lower** bounds only.
- **No transitivity closure on the branch family** (§7) — it would only shrink the value further.
- **No computation of what full realizability buys.** Explicitly out of scope per the ticket.
- **No `L4`, no `C₃`, no `ε_dem`, no poset enumeration.**
- **No re-derivation of `mg-92e6`'s symmetry lemma, `mg-210d`'s master bound, `mg-61bb`'s
  frozen ⟹ coherent, or Diaconis–Graham.** `mg-92e6`'s lemma is read from `STATE.md:156` and
  from `mg-6bc2 §5`; that probe's own document was not opened. The `.tex` sources were not opened.
- **`ε_spec` here is `6·E[inv_e]/(n²−1)` throughout**, the architecture's normalisation. The
  `ε_c3ca = 1/6` reading of the same theorem (`mg-6bc2 §2`) is not re-derived.
- **No claim that the frozen class is non-empty.** Every statement is about `M_n` and about
  posets whose linear-extension measure lies in it.
- **`mg-6bc2`'s landing WAS re-checked, so this is no longer an open note.** This document
  originally said "if it lands changed, §8's two corrections should be re-checked against what
  actually merges". It landed (`e1f7bb2`) while this ticket was queued, and the check was done:
  all four files §8 depends on are byte-identical to the branch versions. Nothing in §8 moves.
- **`STATE.md` is NOT touched.** `mg-d1a2` established that `STATE.md` is `pm-onethird`'s file
  and that landings there are approved before they land. The row this document would want is
  **routed to `pm-onethird` with the verdict**, not written unilaterally. *(The original reason
  given here — that a row would reference an unmerged parent — expired when `mg-6bc2` landed at
  `e1f7bb2`. The ownership reason is the one that stands, and it is the one that mattered.)*
- **The `n = 6` LITERAL values and the `n = 6` wide-window branches were not obtained.** The
  all-pairs literal LP at `n = 6` is 720 columns against 75 equality rows (76 artificials in
  phase 1); both runs were stopped after ~25 and ~50 minutes rather than block the merge, and
  each transcript carries a `[RUN HALTED BY mg-200d]` note saying exactly where it stopped. The
  `n = 6` numbers this document DOES claim are the baseline `5`, both surrogates `5`, and the `window w=1` value `5/3` — all printed in the committed transcripts.
