# What does pair bias actually give for `ε_sup`, and is it `1/6`?

**Work item.** `mg-6bc2` (repo `onethird_program`). Daniel, 2026-08-06: *"We should get 1/6 or
something via pair bias alone!"* Unblocked 2026-08-07 by `mg-345e` on this ticket's own second
disjunct; `L4` remains open and is untouched here.
**Instrument.** `code/pairbias_sharpening_6bc2/` · **Predictions** committed at `384c595`, before
any script of this instrument existed, with six hand measurements disclosed and two most-likely
errors filed in advance.
**Method.** Hand derivation, plus one exact-rational LP over measures on `S_n`. **No poset
enumeration** — `mg-345e`'s refusal is kept and §8 says why.

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

**Measured (`out_v2_optimiser.txt`):**

| `n` | inv-optimiser, aggregate | inv-optimiser, per-slot | `F`-optimiser, aggregate | `F`-optimiser, per-slot |
|---|---|---|---|---|
| 3 | **0** | 4 | **0** | 4 |
| 4 | 6 | 8 | 6 | 8 |
| 5 | 8 | 9 | 8 | 10 |
| 6 | 10 | — | 17 | — |

> **The distinction is the finding, and it refutes my own P6.** I predicted the optimisers would
> violate adjacency symmetry in its **aggregate** form. At `n = 3` they do **not** — the aggregate
> form is satisfied by an optimiser and therefore excludes nothing. The **per-slot** form — which
> is the form `mg-92e6` actually proved — is violated by every optimiser at every `n` tested. **Had
> I not measured both, I would have recommended the weaker lemma, which is inert here.**

So the ordering of the route is:

1. **pair marginals alone → exactly `1`** (`= 1/6` in `ε_c3ca` units). Closed, both directions.
2. **+ per-slot adjacency symmetry → unknown.** It kills every optimiser found here. **What it
   buys is not computed in this document** and is the natural next question — elementary,
   `L4`-free, and a well-posed LP.
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
| **P6** | every optimiser violates adjacency symmetry (**aggregate** form, as I wrote it) | **REFUTED.** At `n = 3` the aggregate form is **satisfied** by an optimiser — 0 violations. The **per-slot** form (`mg-92e6`'s actual statement) is violated at every `n`. Kept as written: I named the wrong form of the lemma, and only measuring both caught it. §5. |
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
3.1's `≤` and Claim 4.1's `≤` are theorems for all `n`; **every attainment statement is finite
population** and is marked as such. Nothing here is evidence at unbounded `n` about attainment.

**Defect 3 — the adjudication in §7 is by hand.** The grep is mechanical; the assignment of 39
lines to five meanings is my reading, and a different reader could split the Hodge weights or the
modulus domain differently. The *load-bearing* row — `mg-c4f5:415` being supply-side — rests on
`mg-c3ca:172`'s definition, which I quote.

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
  `1/6` or anything else. That is the next ticket.
- **No re-derivation** of `mg-210d`'s master bound (inherited; hand-re-derived by `mg-c4f5`), of
  `mg-92e6`'s adjacency symmetry (read from `STATE.md:156`; the probe's own document not opened),
  or of Diaconis–Graham.
- **The source `.tex` was not opened**, and neither was the sibling repo.
- **I cannot tell you which `1/6` Daniel meant.** §0 answers both. The disambiguation is routed to
  him, not decided here.
