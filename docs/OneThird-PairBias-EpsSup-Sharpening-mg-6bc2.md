# What does pair bias actually give for `ε_sup`, and is it `1/6`?

**Work item.** `mg-6bc2` (repo `onethird_program`). Daniel, 2026-08-06: *"We should get 1/6 or
something via pair bias alone!"* Unblocked 2026-08-07 by `mg-345e` on this ticket's own second
disjunct; `L4` remains open and is untouched here.
**Instrument.** `code/pairbias_sharpening_6bc2/` · **Predictions** committed at `384c595`, before
any script of this instrument existed, with six hand measurements disclosed and two most-likely
errors filed in advance.
**Method.** Hand derivation, plus one exact-rational LP over measures on `S_n`. **No poset
enumeration** — `mg-345e`'s refusal is kept and §8 says why.

> ## ⚠️ §5 AND P6 WERE REPAIRED BY `mg-ba78` — AND THE REPAIR IS A STRENGTHENING
>
> `mg-200d` found **two defects, both downstream of the optimum, and neither touching the
> theorem** — which it reproduced exactly at `n = 3,4,5,6` on an independent two-phase solver.
> Repaired in place by `mg-ba78`; instrument [`code/pairbias_repair_ba78/`](../code/pairbias_repair_ba78/),
> and `code/pairbias_sharpening_6bc2/` is patched so it cannot reprint the wrong figures.
>
> 1. **The optimisers this document diagnosed were SUB-PROBABILITY MEASURES.** The LP normalises
>    with `sum μ ≤ 1`; both objectives vanish at the identity, so the simplex left the remainder
>    unplaced and the `n = 3` optimiser carried **total mass `2/3`**. Completing it changes no
>    objective value — **which is why §3's and §4's numbers, and the theorem, are untouched** —
>    but the adjacency diagnostics are equality tests between masses, not linear functionals.
>    **§5's `0` at `n = 3` becomes `2`, and the headline it carried is gone.**
> 2. **§5's two columns were in DIFFERENT UNITS** — aggregate over *ordered* adjacency keys,
>    per-slot over `x < y` crossed with slots. `6 vs 8` at `n = 4` was not a comparison. Both are
>    now per **unordered pair**, the unit is stated at the table, and the `(pair, slot)` count is
>    kept beside them as the strictly finer thing it is.
>
> **What replaces the struck headline is sharper than it was** (§5.1): the aggregate form is
> violated by *every* optimiser at *every* `n` here, so **P6 as written HELD** — this document
> scored its own prediction `REFUTED` off a measurement on an incomplete measure. And the
> aggregate/per-slot distinction survives, relocated from `n = 3` to the asymptotics: `mg-200d`
> finds the two **agree at `n = 3` and separate from `n = 4`**, with the per-slot form buying
> ~~`ε_spec = 2/(n+1)`~~ **[REFUTED at `n = 6` — `mg-131e` §0, §4; see the banner below]** and
> the aggregate form buying no decay at all.
>
> **Unchanged:** §0's verdict, §2, §2.1, §3, §4, §6, §7. Nothing in the `1/6`-vs-`1` answer moves.

> ## ⚠️ `ε_spec = 2/(n+1)` IS REFUTED, AND THIS DOCUMENT PRINTED IT AS LIVE AT FIVE SITES (`mg-372e`)
>
> `mg-131e` refuted it **at `n = 6`** by an explicit hard-coded feasible witness that touches no
> LP — `E[inv] = 11/6 > 5/3`, i.e. `ε_spec = 11/35 > 2/7` — and the excess **grows linearly in
> `n`**. It is **FALSE, not conjectural**. The refutation is at
> [`OneThird-DualCertificate-mg-131e.md`](OneThird-DualCertificate-mg-131e.md) §0 and §4; it is
> not restated here. The ledger carries it at `STATE.md:167(a)`.
>
> **This is a staleness repair, not a new result.** `mg-131e` flagged that this document was
> uncorrected and deliberately did not correct it; `mg-b488` landed the refutation into `STATE.md`
> and scoped itself to `STATE.md`, saying so in as many words at `:168`. `mg-372e` is that landing.
>
> **Struck in place at `:35`, `:85`, §5.1's *"what it buys"* table, §5.1's route ordering, and
> §9's closing note.** `:320` is **NOT** struck: *"`6E/(n²−1) = 2/(n+1)` exactly at `n = 3,4,5`"*
> is scoped to three values of `n`, is **TRUE**, and is the `n`-labelling check `mg-94c3` re-ran
> and confirmed 3/3. A blanket edit on the string would have broken it.
>
> **What is NOT touched.** §5's figures (`mg-ba78`'s repair, landed and correct); the theorem —
> Claim 3.1, Claim 4.1, §0's `1/6`-vs-`1` answer — which never depended on `2/(n+1)`; and
> `PREDICTIONS.md`, a pre-registration artefact.

---

## 0. Verdict

> ## **DANIEL'S CONJECTURE IS RIGHT, AND IT IS ALREADY PROVEN. `1/6` AND `1` ARE THE SAME THEOREM IN TWO NORMALISATIONS.**
>
> Pair bias alone gives `E[inv_e] < n²/6` — **the constant is exactly `1/6`, in the units
> `E[inv_e] ≤ ε·n²`.** The corpus already records it in those words:
> *"Freezing unconditionally gives only `ε < 1/6 ≈ 0.167`"*
> ([`OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415`](OneThird-LIBweak-mg-c4f5-IndependentAudit.md),
> with `ε` defined by `E[inv_e] ≤ εn²` at [`OneThird-LIBweak-mg-c3ca.md:172`](OneThird-LIBweak-mg-c3ca.md)).
>
> **It is the same statement as `ε_sup < 1`.** The architecture's `ε_spec` is defined by
> `E[inv_e] ≤ (ε_spec/6)(n²−1)` — it carries an explicit `/6`. That `/6` is the entire difference:
>
> | | definition | what pair bias gives | limit |
> |---|---|---|---|
> | `ε_c3ca` | `E[inv_e] ≤ ε·n²` | `(n−1)/(6n)` | **`1/6`** |
> | `ε_spec` | `E[inv_e] ≤ (ε/6)(n²−1)` | `n/(n+1)` | **`1`** |
>
> Same `E[inv_e] < m/3 ≤ n(n−1)/6`. Two divisors. **`ε_spec/ε_c3ca = 6n²/(n²−1) → 6`.**
>
> ### So the ticket's two readings have two different answers, and both are settled here.
>
> **Reading A — "pair bias should give `1/6`."** **TRUE, PROVEN, ALREADY IN THE CORPUS, NOTHING TO
> DO.** `Op-Form` Claim 6.1 is that theorem; `mg-c4f5:415` is that constant. §2.
>
> **Reading B — "sharpen `ε_spec` from `1` to `1/6`."** **PROVABLY UNAVAILABLE from pair bias
> alone** — and *not* "not yet". §3 computes the exact value of the pair-bias information set: it
> is `n/(n+1)`, **attained**, so `Op-Form` Claim 6.1 is **not a lossy step that a cleverer argument
> could tighten.** It is the whole of what per-pair marginals contain. Reading B asks for a factor
> of **6** that the normalisation has already eaten; anyone pursuing it would be trying to prove a
> statement 6× stronger than Daniel's while believing they were confirming it.
>
> ### Where it stops, exactly
>
> **At `n/(n+1)`, in BOTH renderings of the master bound** — the footrule form buys **nothing**
> (§4). I built this instrument to test the one lever that looked free, and **it is not free; my
> own lead is dead and the machine killed it.** Every route below `1` needs a *realizability* fact,
> and the first already-proven one that bites is **`mg-92e6`'s per-slot adjacency symmetry**
> `J_k(x,y) = J_k(y,x)` — which every optimiser here violates, and which the corpus already names
> as "the extra juice" (`STATE.md:156`). §5.
>
> **Repaired at §5 (`mg-ba78`), and it comes out stronger.** Both forms of the lemma are violated
> by every optimiser here — the aggregate form too, once the measure is completed — so the
> *witness* test does not separate them. What separates them is the **value**: `mg-200d` computes
> that the per-slot form buys ~~`ε_spec = 2/(n+1)`, i.e. `Θ(n²) → Θ(n)`~~ **[the constant is
> REFUTED at `n = 6` — `mg-131e` §0, §4. What survives is the separation at `n = 4,5`, which is
> exact; the ASYMPTOTIC rendering rests on the same three points and no proof]**, and the
> aggregate form buys **no decay at all**. Same conclusion, better reason, and it now lives at
> the asymptotics rather than at `n = 3`.
>
> ### Two corrections and one routing
>
> 1. **`mg-345e:292` is wrong on both counts.** *"`1/6` occurs twice in this corpus and neither
>    occurrence is a supply-side derivation."* Re-counted (§7): **three** distinct
>    programme-relevant meanings, and **one of them is exactly the supply-side derivation** — the
>    one that answers this ticket. I inherited that sentence and it cost me an hour; it is the
>    only load-bearing claim in `mg-345e` I found wrong.
> 2. **`1/6` in `ε_spec` units would not clear the wall anyway** (§6). `ε_dem ≤ 1/50`, and that
>    figure is already the optimistic `C₃ = 1` value. `1/6` is `8.3×` short of a demand constant
>    that is itself an over-estimate.
> 3. **Which `1/6` Daniel meant is Daniel's to say, and I have routed it to him.** The
>    mathematics is the same either way; what changes is whether this ticket is *closed* or
>    *reopened at 6× the difficulty*.

---

## 1. Why "the constant we can prove" needs an information set before it means anything

`ε_sup` is defined (`mg-345e:59`) as *"the smallest `c` for which we can prove
`E[inv_e] ≤ (c/6)(n²−1)` for every frozen `P`"*. Read as a supremum over a population, **that
quantity is `0`**: if the 1/3–2/3 conjecture is true there are no frozen posets, the supremum is
over the empty set, and every `c` "works" vacuously. The corpus states the emptiness itself —
1/3–2/3 is verified to `n = 14` (`mg-33f5`), so the class is empty at every `n` anyone can reach.

So `ε_sup` is **not a fact about posets. It is a fact about a proof.** It only becomes well-posed
once you say *what the proof is allowed to know*. That is why "pair bias **alone**" is the load-
bearing word in Daniel's sentence, and it is what makes the question answerable:

> **Definition (the pair-bias information set).** `M_n(η) = ` all probability measures `μ` on `S_n`
> such that for some linear order `e`, every pair is flipped against `e` with probability
> `≤ 1/3 − η`.

A derivation that uses only the per-pair flip probabilities and linearity of expectation is valid
for **every** member of `M_n(η)` — including the ones no poset realises. Hence its constant is
**at least** the maximum over `M_n(η)`. That maximum is computable, and §3 computes it.

**This framing is not in the corpus** and I believe it is the reason the question has felt
slippery: `STATE.md:17`'s *"it is false for abstract frozen distributions"* and `STATE.md:135`'s
two-atom law are exactly the statement that `M_n` is strictly bigger than the realisable set — but
nobody has asked **how much the bound costs**, which is a number.

---

## 2. Reading A — the `1/6`, and it is already proven

**Claim 2.1.** *Under the frozen hypothesis, `E[inv_e] < n²/6`; equivalently `ε_c3ca < (n−1)/(6n)`,
with supremum `1/6`.* **[PROVEN — this is `Op-Form` Claim 6.1 restated; not re-derived, read]**

*Proof.* `inv_e(σ)` counts incomparable pairs flipped against `e`. Frozen gives `Pr[flip] < 1/3`
per incomparable pair, so by linearity `E[inv_e] = Σ_{i∥j} Pr[flip] < m/3` where `m = #`incomparable
pairs. `m ≤ C(n,2)`, so `E[inv_e] < n(n−1)/6 < n²/6`. □

Three lines, no `L4`, no `Δ₁`, no `C₃`, no Step 6 — the dependency list `mg-345e` exhibited.

**And the corpus already writes the constant as `1/6`.** `mg-c4f5`'s audit, checking whether
`mg-c3ca`'s entropy price bites at the frozen value, records verbatim:

> *"**Prop. 4.1 is VACUOUS for `ε ≥ 1/(2e²) ≈ 0.0677`** … **Freezing unconditionally gives only
> `ε < 1/6 ≈ 0.167`.** So at the unconditional frozen value the entropy price says nothing."*
> — [`OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415`](OneThird-LIBweak-mg-c4f5-IndependentAudit.md)

and `mg-c3ca:172` fixes that `ε` as `E[inv_e] ≤ εn²`. **That is Daniel's `1/6`, written down, in
this repository, before he asked for it.**

### 2.1 The unit map, stated once so it cannot be re-welded wrongly

```
E[inv_e] < m/3 ≤ n(n−1)/6                     <- the one theorem
   |                                    |
   | divide by n²                       | divide by (n²−1)/6
   v                                    v
ε_c3ca < (n−1)/(6n)  ->  1/6            ε_spec < n/(n+1)  ->  1
```

**⚠️ The trap this document exists to prevent.** `ε_spec` and `ε_c3ca` are both called `ε` in this
corpus, differ by a factor of `6n²/(n²−1)`, and both have a live `1/6` attached — `ε_c3ca`'s is the
*value pair bias proves*, `ε_spec`'s is *Daniel's conjectured target*. A reader who meets the
number in one place and the threshold in the other will weld them and conclude the programme is a
factor of 6 from a bound it already has. This is the same shape `mg-33f5`/`mg-d1a2` guarded against
for `N₀`, and it is why this is a document rather than a one-line reply.

---

## 3. Reading B — the exact value of the pair-bias information set

**Claim 3.1.** *`max{ 6E_μ[inv_e]/(n²−1) : μ ∈ M_n(η) } = (1−3η)·n/(n+1)`, attained.*
**[PROVEN, all `n`, by hand; machine-confirmed exactly at `n = 3,4,5,6`]**

*Proof.* **`≤`:** `E[inv_e] = Σ_{pairs} q_{ij} ≤ m(1/3−η) ≤ C(n,2)(1/3−η)`, then divide.
**`≥`:** the **two-atom law** `μ = (2/3+η)δ_e + (1/3−η)δ_{rev e}` puts every pair at flip
probability exactly `1/3−η` and has `E[inv_e] = C(n,2)(1/3−η)`. □

> **So `Op-Form` Claim 6.1 is not a bound waiting to be sharpened. It is an equality for the
> information it consumes.** No rearrangement, no cleverer inequality, no third elementary identity
> can move it, because there is an explicit feasible measure sitting on it.

The witness is not new — it is `STATE.md:135`'s **two-atom law**, the corpus's own named
obstruction ("*a two-atom law has every pair frozen yet `Θ(n²)` inversions*"). What is new is that
it is **exactly tight for this constant**, which turns a qualitative obstruction into a number:
**the price of dropping realizability is precisely the whole gap from `1` down to anything.**

### 3.1 The two levers, and what `1/6` would cost in each

Writing `d = m/C(n,2)` (incomparability density) and `q̄` (mean flip probability over incomparable
pairs), the identity is exact:

```
ε_spec  =  3 · d · q̄ · n/(n+1)
```

| target | what it requires | factor below the frozen product `d·q̄ = 1/3` |
|---|---|---|
| `ε_spec = 1` (have) | `d = 1`, `q̄ = 1/3` | — |
| `ε_spec = 1/6` (Daniel, reading B) | `d·q̄ ≤ 1/18` | **6×** |
| `ε_spec = 1/50` (what `ε_dem` needs) | `d·q̄ ≤ 1/150` | **50×** |

Either lever alone: `1/6` needs `d ≤ 1/6` (five sixths of all pairs comparable) **or** `q̄ ≤ 1/18`
(mean bias six times below the frozen threshold). Both are **realizability** statements about real
posets — §5 — and `mg-345e`'s P5 grep found the corpus's density facts all run the *wrong way*
(`m ≥ n−1` from primitivity, co-degree `≥ 2` from `mg-e2de`: **lower** bounds, which push `d` up).
I re-ran that grep; see §7.

---

## 4. The one lever that looked free, and is not — the footrule form

`Op-Form:§6.3` records that the master bound's **inversion** form is *"itself a factor `3/2` lossy
at the antichain, since `D ≤ 2I` is not tight there"*. The master bound has two forms:

```
1 − λ_std  ≤  3E[footrule]/(n²−1)   ≤   6E[inv]/(n²−1)
             ^ sharp at the antichain    ^ the one Claim 6.1 uses
```

The two-atom law scores `1/2` in the footrule form and `1` in the inversion form (hand-computed;
machine-confirmed). **That looked like a free factor of 2 — bound the footrule directly and the
constant halves, with no new mathematics at all.** It is the only cheap sharpening on the board,
so I built the LP to test it.

**Claim 4.1.** *`max{ 3E_μ[footrule]/(n²−1) : μ ∈ M_n } = n/(n+1)` — identical to the inversion
form.* **[`≤` PROVEN all `n` (Diaconis–Graham `F ≤ 2I` plus Claim 3.1); attainment MEASURED at
`n = 3,4,5,6` (LP) and `n = 8` (explicit construction). Not proven for all `n`.]**

| `n` | `max E[inv]` | `= C(n,2)/3`? | `ε_spec` | `max E[F]` | `= 2·C(n,2)/3`? | footrule `ε` | `n/(n+1)` |
|---|---|---|---|---|---|---|---|
| 3 | `1` | ✓ | `3/4` | `2` | ✓ | `3/4` | `3/4` |
| 4 | `2` | ✓ | `4/5` | `4` | ✓ | `4/5` | `4/5` |
| 5 | `10/3` | ✓ | `5/6` | `20/3` | ✓ | `5/6` | `5/6` |
| 6 | `5` | ✓ | `6/7` | `10` | ✓ | `6/7` | `6/7` |

`out_v1_n345.txt`, `out_v1_n6.txt`, exact rationals throughout.

**Why it fails, mechanically.** `F ≤ 2I` is slack at the *reversal*, which is why the two-atom law
scores `1/2` — but the optimiser is not the two-atom law. The LP finds measures supported on
**monotone-displacement** permutations, where no element both overtakes and is overtaken, and those
satisfy `F = 2I` **exactly**. The relaxation is free to choose them, so the `3/2` the antichain
comparison advertises is not available under the frozen cap.

**And it is not merely unproven at large `n`.** By hand, a hierarchical block-rotation family
(levels `ℓ = 0,1,2`, `2^ℓ` blocks each internally half-rotated, mass `1/3` each, pairwise disjoint
flip-sets) is feasible for every `n` and reaches `7/8` of the cap — attaining it exactly at `n = 8`
(`E[F] = 56/3 = 2·C(8,2)/3`, selftest S7). **So the footrule form can buy at most a factor `8/7`,
ever, and buys exactly `1` wherever it has been computed.** Recorded as dead.

---

## 5. Where the route actually stops, and which lemma is next

Every optimiser above is infeasible for a real poset, and the corpus already owns the reason.

**Adjacency symmetry.** For incomparable `x,y`, the swap map is a bijection of `L(P)`, so for the
uniform measure on `L(P)`, `Pr[x` immediately precedes `y` at slot `k]` `=` `Pr[y` immediately
precedes `x` at slot `k]` — `mg-92e6`'s `J(k,k+1) = J(k+1,k)`, `STATE.md:156`, already proven,
already named there as *"the extra juice is one joint fact"*.

**Measured (`out_v2_optimiser.txt`) — REPAIRED BY `mg-ba78`; the superseded table is at §5.2.**

**⚠️ THE UNIT, STATED AT THE TABLE, BECAUSE THE SUPERSEDED VERSION HAD TWO OF THEM.** Every cell
below counts **UNORDERED PAIRS `{x,y}`, `x < y`, of a PROBABILITY measure**, out of `C(n,2)`.
*Aggregate* means `Σ_k J_k(x,y) ≠ Σ_k J_k(y,x)`; *per-slot* means `J_k(x,y) ≠ J_k(y,x)` **for at
least one `k`**. On that unit the two **nest** — aggregate-violated ⊆ per-slot-violated, since a
difference of sums forces some summand to differ — so the columns are comparable, and the
inclusion is checked, and checked to be *strict* somewhere, rather than assumed
(`selftest_ba78.py` T6). The `(pair, slot)` count is a **strictly finer unit** and is carried in
its own bracket so it can never be read against the other two.

| `n` | `C(n,2)` | inv-opt, aggregate | inv-opt, per-slot | `F`-opt, aggregate | `F`-opt, per-slot | *(pair,slot)s, inv / `F`, out of `C(n,2)(n−1)`* |
|---|---|---|---|---|---|---|
| 3 | 3 | **2** | **3** | **2** | **3** | *4 / 4, of 6* |
| 4 | 6 | **5** | **6** | **5** | **6** | *8 / 8, of 18* |
| 5 | 10 | **6** | **7** | **6** | **6** | *9 / 10, of 40* |
| 6 | 15 | **7** | **8** | **13** | **14** | *12 / 25, of 75* |

### 5.1 What the repaired table says, and it is not what the superseded one said

*(§5.1 and §5.2 are written by `mg-ba78`, the repairing item, about `mg-6bc2`. The rest of this
document is `mg-6bc2`'s own voice and is left in it.)*

> **P6 HELD. Both forms are violated by every optimiser at every `n` measured here — including the
> aggregate form at `n = 3`, where this document published `0`.** That `0` was a diagnostic run on
> a measure carrying **two thirds of its mass**: the LP normalises with `sum μ ≤ 1`, `inv` and `F`
> both vanish at the identity, and the simplex therefore never placed the last third. Put it back
> — which changes no objective value and breaks no constraint — and the `n = 3` optimiser violates
> the aggregate form at **2 of its 3 pairs**. **So the witness test does not separate the two forms
> at all**, and this document scored its own prediction `REFUTED` against a figure that was not a
> measurement of what it named.
>
> **The defect ran in the flattering direction, which is the one worth distrusting.** A prediction
> the author refutes himself reads as more careful than a prediction that lands, and it supplied
> the surprise that §5's conclusion was built on. Neither the refutation nor the surprise was
> real. The claim is not taken on the repair's word either: a mutation that withholds the
> completion reproduces the published `0` exactly, and all eight published aggregate figures
> besides (`selftest_ba78.py` T4–T5, `r2_isolate.py`).

**The distinction survives, and it moved to where it is worth more.** What separates the two forms
is not *which measures they exclude* but *what they buy*, and `mg-200d` — this document's own
named next ticket — computed it:

| | `n = 3` | `n = 4` | `n = 5` | what it buys |
|---|---|---|---|---|
| **+ aggregate** symmetry | `2/3` | `5/3` | `7/3` | **`ε_spec` shows no decay at all** |
| **+ per-slot** symmetry | `2/3` | `1` | `4/3` | ~~**`ε_spec = 2/(n+1)`, `Θ(n²) → Θ(n)`**~~ **REFUTED — see below** |

> ⚠️ **The *"what it buys"* cell on the per-slot row is STRUCK (`mg-372e`).** `mg-131e` refuted
> `ε_spec = 2/(n+1)` **at `n = 6`** by explicit witness (§0, §4) and the excess grows linearly in
> `n`; the formula is **FALSE, not conjectural**, and there is **no replacement constant to print
> — do not carry the old one and do not invent a new one** (`STATE.md:167(a)`). The **three
> tabulated values `2/3, 1, 4/3` are `n ≤ 5` exhaustive LP optima and are UNTOUCHED and correct**
> — the strike is on the all-`n` reading of them, not on the numbers. `mg-00a1` is the open
> question that replaces the formula: what *is* the true growth of the disjunctive per-slot value?
> The aggregate row's *"no decay at all"* is unaffected, so **the recommendation to reach for the
> per-slot form still stands** — on the exact separation at `n = 4,5`, not on an asymptotic rate.

— `mg-200d` (`max E[inv_e]` under each constraint set; **its result, cited, not re-derived here**;
see the bound at the end of §9). **The two AGREE at `n = 3` and separate from `n = 4`.** So the
original conclusion holds with a better warrant: recommending the aggregate form would have
recommended a lemma that is **inert asymptotically** — it does not move `E[inv_e]` out of `Θ(n²)`
— rather than one that is inert at `n = 3`, which it is not. **"Excludes nothing at `n = 3`" was
false; "buys no decay, ever" is both true and stronger.**

*The one check `mg-ba78` made on `mg-200d`'s figures, and the only one:* its per-slot triple
satisfies `6E/(n²−1) = 2/(n+1)` **exactly** at `n = 3,4,5` (`2/3 → 1/2`, `1 → 2/5`, `4/3 → 1/3`),
which confirms the `n`-labelling of the row. Neither constrained LP was re-solved — and there is a
reason beyond scope not to attempt it with *this* instrument, given at the end of §9.

### 5.2 The superseded table, kept so the correction is legible

| `n` | inv-opt, aggregate | inv-opt, per-slot | `F`-opt, aggregate | `F`-opt, per-slot |
|---|---|---|---|---|
| 3 | **0** | 4 | **0** | 4 |
| 4 | 6 | 8 | 6 | 8 |
| 5 | 8 | 9 | 8 | 10 |
| 6 | 10 | — | 17 | — |

Both defects are visible in that table at once. The aggregate columns are counts of **ordered**
adjacency keys on **sub-probability** measures; the per-slot columns are counts of **(unordered
pair, slot)** on the same measures. The two are crossed and isolated in `r2_isolate.py`, and the
split is clean: **only the missing mass can move the `n = 3` figure off `0`** (the unordered
predicate on the uncompleted measure still reads `0`), while at `n ≥ 4` the measure was already at
mass `1` and the entire change — `6 → 5`, `8 → 6`, `10 → 7`, `17 → 13` — is the unit.

**This is the second unit-mismatch defect in this lineage in one day.** The first was `ε_spec` vs
`ε_c3ca`, which §2.1 exists to guard against — and this document then shipped a table with two
units in it. The guard was written for the *reader* and not applied to the *author's own columns*.

So the ordering of the route is:

1. **pair marginals alone → exactly `1`** (`= 1/6` in `ε_c3ca` units). Closed, both directions.
2. **+ per-slot adjacency symmetry → ~~`ε_spec = 2/(n+1)` (`mg-200d`)~~ an UNKNOWN rate
   (`mg-200d`, then `mg-131e`).** ~~It was open when this document landed; it is not any more~~
   **It was open when this document landed; `mg-200d` answered it and `mg-131e` then REFUTED that
   answer at `n = 6` (§0, §4), so it is open again — with the `n ≤ 5` values `2/3, 1, 4/3` and
   `Θ(n²) → Θ(n)` on ONE named sub-family as all that is established** (`mg-372e`). The aggregate
   form is still the inert one. `mg-200d`'s landing is where that result was established and
   `mg-131e`'s is where it was killed — this section cites them and restates neither.
3. **+ the rest of realizability →** the open residual `(R)`, `STATE.md:179`.

**A negative worth recording so nobody re-walks it.** The 3-element cyclic identity
(`STATE.md:203`, `Pr[x<y]+Pr[y<z]+Pr[z<x] ≤ 2`) reduces, on a frozen triple, to
`q_xz ≤ q_xy + q_yz` — **subadditivity**, an *upper* bound satisfied with room to spare when every
`q = 1/3`. It cannot exclude the extremal configuration, so it buys nothing here. That is the same
conclusion `mg-61bb` reached from the other side (coherence is a *consequence* of frozen, and its
residual is a system of upper bounds); I re-derived it rather than citing it, and it agrees.

---

## 6. Rider — `1/6` in `ε_spec` units would not clear the wall

Even granting Reading B outright: `ε_dem = ε_leak²/(2C₃) = 1/50` at `C₃ = 1`, and `C₃ ≥ 1` is a
loss factor, so `1/50` is an **over-estimate** of the budget (`mg-345e:§5.3`). `1/6` against `1/50`
is short by `8.3×`. The published gap factor of `~50` is `ε_sup/ε_dem`; reading-B `1/6` takes it to
`~8.3`, which is progress and is **not** a closure. The number that would close it is `1/50` — and
`d·q̄ ≤ 1/150`, i.e. a **50×** improvement on the frozen product. Sizing this is not discouragement:
it is the difference between a milestone and a wall, and the ticket asked for the constant, not for
optimism.

---

## 7. The counts, re-run rather than inherited

**Population, named before counting:** files tracked in *this* repository matching
`*.md`, `*.tex`, `*.html` — **319 files at `550a7f1`** (the base commit), **320 with this
document**. **Boundary, stated so the number is not over-read:** this excludes the sibling repo
`one_third_width_three` (not opened here — the same boundary `mg-345e` declared), git history, and
the literature.

**NOT STATIONARY, and it moved under my hand while I was counting it.** At `550a7f1` the corpus
carries **39** `1/6` lines in **16** files; with this document it carries **43** in **17**. *This
paragraph is part of the delta it reports.* The population grows with every landed item, so it
moves as a function of our own dispatch rate — which is why the base commit is named beside every
figure below rather than left to be inferred.

**`1/6` — `mg-345e:292` says "occurs twice … neither is a supply-side derivation". Both halves are
wrong.** `grep -n '1/6\|\\frac{1}{6}\|\\tfrac16'` over that population **at `550a7f1`** returns
**39 lines in 16 files**. Adjudicated by hand into meanings (≈10 are false positives such as
`61/61` and `1/20030010`):

| meaning | where | supply or demand? |
|---|---|---|
| `E[inv_e] < εn²` at the frozen value → **`ε < 1/6`** | `OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415` | **SUPPLY — this is the one** |
| "slack `≤ 1/6` for a centred pair" | `Op-Form:433,434,446,448` + audit `488,497,499,690` | demand (and `BROKEN as labelled`, `mg-e35c` F5) |
| collapse of the local `δ` bound at co-degree 2 | `STATE.md:158` (`mg-e2de`) | neither — a `δ` lower bound |
| modulus domain `(0,1/6]` | `L4-Branch-ii-Sublinear-Modulus-IndependentAudit.md:132,340` | `L4`, unrelated |
| Hodge weights `{−1: 1/6, …}` | `Hodge-Side-Leverage.md:554,843,845` | unrelated |

**Three programme-relevant meanings, not two; and the supply-side one exists.** `mg-345e` is a
GREEN, audited-adjacent finding whose main verdict I rely on throughout — this is a single wrong
sentence in it, not a reason to doubt the rest, and I am recording it because I inherited it and it
sent me looking for a derivation that was already written down.

**Frozen-conditional *upper* bound on `d` — `mg-345e`'s P5, re-run with my own predicate.**
`grep -niE 'density.*(ceiling|upper bound|at most)|d\(P\) ?[<≤]'` over the same population returns
**5 lines**, and **0** of them is a *proven* frozen-conditional upper bound on `d`:

| hit | what it actually is |
|---|---|
| `STATE.md:177` | residual **(R)**, *"do frozen posets have a density ceiling `d(P) ≤ D < 1`?"* — the open **question** |
| `Op-Form-IndependentAudit.md:428` | the same **(R)**, restated |
| `state-history/attempt-mg-210d.md:54` | `mg-210d`'s own record: *"best constant this route proves = `0`"* |
| `state-history/threads-chronology.md:27` | the same `mg-210d` residual, in prose |
| `Unified-Framework-Gate-IndependentAudit.md:66` | an unrelated F5 about near-empty posets in a sweep |

**P5 reproduces: every density fact on record is a lower bound, and the only upper one is an open
question with `0` as its best proven constant.** (`mg-345e` described its near-hits as
`Op-Form:§7.3`'s *required* density; my predicate finds a different five. Two greps, two predicates
— the conclusion is the same and the hit sets are not, which is worth knowing before either is
quoted as *the* count.)

---

## 8. Predictions, scored — including the refuted ones, kept as written

| # | prediction | outcome |
|---|---|---|
| P1 | LP max `E[inv_e]` is exactly `C(n,2)/3` | **HELD**, `n = 3,4,5,6`, exact |
| P2 | LP max `E[F] < (n²−1)/3`, ratio in `[3/4, 1)` | **HELD AS WRITTEN — AND THE LEAD IT TESTED IS DEAD.** The ratio is `3/4, 4/5, 5/6, 6/7` ∈ `[3/4,1)` ✓, but it equals the *inversion* form's ratio exactly. The interval was right and the reason I chose it was wrong. Scoring this as a hit would be the vacuous pass this arc keeps producing. |
| P3 | two-atom law attains the `E[inv]` optimum | **HELD**, all `n` tested |
| P4 | two-atom law does not attain the `E[F]` optimum | **HELD** (`1/2` vs `n/(n+1)`) |
| P5 | footrule ratio non-decreasing in `n` | **HELD** — `3/4 → 4/5 → 5/6 → 6/7`, i.e. `→ 1` |
| **P6** | every optimiser violates adjacency symmetry (**aggregate** form, as I wrote it) | ~~**REFUTED.** At `n = 3` the aggregate form is **satisfied** by an optimiser — 0 violations.~~ **RESCORED BY `mg-ba78`: HELD.** The `0` was measured on a measure carrying mass `2/3`; completed, the `n = 3` optimiser violates the aggregate form at **2 of 3 pairs**, and so does every other optimiser at every `n` tested. The **per-slot** form (`mg-92e6`'s actual statement) is violated at every `n` too — *both* are, so the violation test never separated them. Kept as written, and the original scoring kept struck rather than deleted: **I marked my own prediction refuted on the strength of a defective measurement, in the direction that made the finding look sharper.** §5.1. |
| P7 | *my most likely error* — reading finite-`n` LP values as the limit | **HELD AS A RISK, and it bit P2.** §4's `≤` is a theorem for all `n`; attainment is `n ∈ {3,4,5,6,8}` only, and §4 says so at the claim rather than in a footnote. |
| P8 | *second most likely error* — reporting `1/6` and `1` as two findings rather than one fact in two normalisations | **HELD AS A RISK, and §0/§2.1 are the guard I built.** Whether it survived contact is `mg-832f`'s to say, not mine. |

---

## 9. Defects of this instrument, and what I did not do

**Defect 1 — my own headline lead was wrong, and I had already refuted it by hand before the
machine ran.** H3 (the two-atom law scores `1/2` in the footrule form) is true and made the
footrule route look like a free factor of 2. H4 (the hierarchical construction, `7/8`) already
showed it could buy at most `1/8`. I built the LP anyway and it returned `0`. The honest reading is
that **H3 was a witness-specific artefact read as a structural fact** — precisely the error §3
exists to name, committed by the author of §3.

**Defect 2 — the LP is `n ≤ 6`.** `S_n` is enumerated, so the tableau is `C(n,2)+1` by `n!`. Claim
3.1's `≤` and Claim 4.1's `≤` are theorems for all `n`; **every attainment statement THIS LP
SUPPLIES is finite population** and is marked as such. Nothing here is evidence at unbounded `n`
about attainment.

> **Scoped to the LP by `mg-8257`; the over-reach was found by `mg-9f91`'s audit, F1.** As first
> written the middle sentence read *"every attainment statement"* and so contradicted Claim 3.1's
> own header at `:175` — *"[PROVEN, all `n`, by hand]"* — inside a section whose heading and closing
> sentence are both about the LP. **Claim 3.1's attainment is all-`n` and does not come from the
> LP:** the `≥` witness is the two-atom law `μ = (2/3+η)δ_e + (1/3−η)δ_{rev e}` — two permutations,
> no tableau — checked `192/192` in exact rationals over
> `n ∈ {2,3,4,5,6,7,8,9,11,20,50,137} × η ∈ {0, 1/100, 1/12, 1/6}`
> ([`code/unitmap_audit_9f91/m3_attainment.py`](../code/unitmap_audit_9f91/m3_attainment.py)),
> seven of those `n` outside `{3,4,5,6,8}`. **A two-permutation construction is not a
> finite-population result.** The finite population `{3,4,5,6,8}` is **Claim 4.1**'s — the
> *footrule* statement — and is marked there at `:228–230`. `mg-9adf` (`21ee93f`) and `STATE.md`
> row 8 resolved this in that direction **deliberately** and did not record that they had resolved
> anything; the silence is a decision already taken, not an oversight to be undone. **A reader
> arriving from `STATE.md` row 8 does not have to re-adjudicate this.**

**Defect 3 — the adjudication in §7 is by hand.** The grep is mechanical; the assignment of 39
lines to five meanings is my reading, and a different reader could split the Hodge weights or the
modulus domain differently. The *load-bearing* row — `mg-c4f5:415` being supply-side — rests on
`mg-c3ca:172`'s definition, which I quote.

**Defect 4 — THE SECTION 5 DIAGNOSTICS RAN ON SUB-PROBABILITY MEASURES.** *(Found by `mg-200d`;
repaired by `mg-ba78`, §5.1–5.2.)* The LP's normalisation is `sum μ ≤ 1` — an inequality, because
the simplex needs the origin feasible so phase 1 can be skipped — and both objectives vanish at the
identity, so the leftover mass was never placed. The `n = 3` optimiser I diagnosed carried mass
`2/3`. **The optimum value and the theorem are unaffected**, because the identity contributes `0`
to `E[inv]`, `0` to `E[F]` and `0` to every flip probability, so the completion is feasible at the
same objective — but the adjacency diagnostics are equality tests between masses, and `0`
violations at `n = 3` became `2`. **The error is not "the LP was wrong"; it is that a quantity that
is invariant under the defect (the optimum) and a quantity that is not (an equality test) were
read off the same object without asking which was which.**

**Defect 5 — THE TWO SECTION 5 COLUMNS WERE IN DIFFERENT UNITS.** *(Found by `mg-200d`; repaired by
`mg-ba78`.)* Aggregate counted **ordered** adjacency keys, per-slot counted **(unordered pair,
slot)**. `6 vs 8` at `n = 4` was not a comparison. **This is the same class of defect as the one
§2.1 exists to prevent, in the same document, one section later** — `ε_spec` vs `ε_c3ca` differ by
a normalisation and I built a guard for the reader; my own table then carried two units without
one. A guard aimed outward is not a check.

### Not done, deliberately

- **No poset enumeration.** The frozen class is empty at every `n` this corpus can enumerate
  (1/3–2/3 verified to `n = 14`, `mg-33f5`), so calibrating `ε_sup` empirically would measure a
  hypothetical population. The LP is over **measures on `S_n`**, which is the relaxation itself —
  a different object, and the reason it is admissible here.
- **No attempt at `L4`.** Row 11 untouched; the modulus question is exactly as open as before.
- **No attempt at `ε_dem`, `ε₀` or `C₃`.** Out of scope by the ticket's own wording. §6 uses
  `ε_dem ≤ 1/50` as an inherited figure and does not re-derive it.
- **I did not compute the relaxation value with adjacency symmetry imposed.** §5 shows it excludes
  every optimiser found here. **It does not show what it buys**, and I am not claiming it reaches
  `1/6` or anything else. That is the next ticket. *(It was `mg-200d`, and it answered:
  ~~`ε_spec = 2/(n+1)` for the per-slot form~~ **`ε_spec = 2/(n+1)` for the per-slot form —
  since REFUTED at `n = 6` by `mg-131e` §0/§4, so that half of the answer is FALSE and the rate
  is unknown (`mg-372e`; the live question is `mg-00a1`)** — no decay for the aggregate form,
  which stands — cited at §5.1 and established in `mg-200d`'s own landing, not here.)*
- **No re-derivation** of `mg-210d`'s master bound (inherited; hand-re-derived by `mg-c4f5`), of
  `mg-92e6`'s adjacency symmetry (read from `STATE.md:156`; the probe's own document not opened),
  or of Diaconis–Graham.
- **The source `.tex` was not opened**, and neither was the sibling repo.
- **I cannot tell you which `1/6` Daniel meant.** §0 answers both. The disambiguation is routed to
  him, not decided here.

### What the `mg-ba78` repair did NOT do

Written by the repairing agent, not by this document's author, and kept separate from the list
above so the two are not read as one voice.

- **The theorem was not touched, and not re-derived either.** Claim 3.1, Claim 4.1, §4's table and
  §0's verdict are unchanged. `mg-200d` reproduced the theorem exactly at `n = 3,4,5,6` on an
  independent two-phase solver; `mg-ba78` did not re-derive it and does not need to — its checks
  establish only that the *completion* moves no objective value and breaks no constraint
  (`selftest_ba78.py` T2, 32 checks), which is what makes the two defects downstream of it.
- **`mg-200d`'s two constrained-LP sequences were NOT re-solved here.** They are cited at §5.1 as
  its result. The single check made on them is the `n`-labelling arithmetic stated there. There is
  a reason not to attempt them with this document's instrument: the completion that rescues the
  *unconstrained* optimiser **does not transplant**, because the identity itself violates per-slot
  symmetry (`J_0(0,1) = 1`, `J_0(1,0) = 0`), so it is not available as the place to put leftover
  mass — a constrained LP needs a solver that normalises with an equality, which is what `mg-200d`
  used and this one does not have.
- **`n ≤ 6` throughout, as before.** The repaired §5 figures are finite-population and are evidence
  about the optimisers found at those `n`, nothing more.
- **No `STATE.md` row.** `STATE.md` is Daniel's file (`mg-d1a2`) and neither `mg-200d` nor
  `mg-ba78` landed a row in it; that is a separate decision and was not taken here.
- **Nothing else in this document was re-checked.** §7's counts, §6's `ε_dem`, §2.1's unit map and
  §4's hierarchical construction were read, not re-run. What *was* swept, because a struck claim
  that has escaped is the failure mode this corpus keeps hitting: `grep -inF` for `"per-slot"` and
  `"inert lemma"` over every tracked `*.md`, `*.tex` and `*.html` **outside this document** returns
  **0** lines each; `"aggregate"` returns **21** and `"excludes nothing"` returns **2**, and
  **0 of those 23 are about adjacency symmetry** — the only two that even mention a slot are the
  Hodge lineage's *prose slots* (`Mg9207Repair.md:189`, `hodge_leverage_repair_ff3e/PREDICTIONS.md:80`),
  a different object with the same word. `STATE.md` carries **no row for `mg-6bc2`** at all. So the
  repair is complete at one document plus its instrument, and that is measured rather than assumed.
