# OneThird — CHAIN (IV) IS CHAIN (II). Its `c` and chain (II)'s `C₃^gap` are **ONE unknown in two currencies**, their demands are **algebraically equal**, and the `ε_dem = 0.20` that the 5×-not-50× reframing rests on is the **`C₃^gap = 1` extreme point** — the very value `mg-94c3` measured false at `1023/1032`. Separately: `mg-76b2`'s falling `min c` is **CONFIRMED, EXTENDED TO `n = 7`, AND UPGRADED TO AN EXPLICIT INFINITE FAMILY** — and **every poset in it is 23×–33× OUTSIDE the regime**, so it refutes `c > 0.80` on the full population and **settles nothing about the class chain (IV) is invoked on**, where the two families that reach it have `c = 0.9999`

**Work item.** `mg-81ff` (repo `onethird_program`), filed by `pm-onethird`.
**Instrument.** [`code/chain_iv_c_81ff/`](../code/chain_iv_c_81ff/) — shares no line of code
with `lib76b2`, `lib9461` or `lib_d3c7`; a different enumeration, a different transport
computation and a different eigenroutine.
**Source read at source:**
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
(603 lines, md5 `db095fbe12ba19f0a8107f962c0d1c8f` — the same file and md5 `mg-d3c7` and
`mg-9461` report).

> ### ⛔ TWO THINGS THIS DOCUMENT REFUSES TO PRINT
>
> 1. **NO WINDOW FIGURE.** `mg-76b2`'s window table (`80, 32, 16, 11, 9, 8`) rests on the
>    supply `ε_spec = 2/(n+1)`, **REFUTED at `n = 6`** (`mg-131e`). This ticket was told not
>    to carry it and does not: no `n ≤ N` column appears anywhere below or in the
>    instrument's transcripts.
> 2. **NO UNSCOPED `17/78`.** It does not arise here, and where the shape recurs — a
>    figure whose scope is the whole finding — the scope is printed **at** the figure.

---

## 0. Verdict

> ### 1. THE SEQUENCING DIRECTIVE, RUN FIRST AND ANSWERED: `min c` KEEPS FALLING, AND IT IS NOT A TREND — IT IS A FAMILY.
>
> `mg-76b2`'s `0.750000, 0.618034, 0.536219, 0.452934` at `n = 3..6` reproduce **exactly**
> on an instrument that shares no code with it (`s0 (H)`), together with its primitive
> counts `4, 27, 275, 4070`. **`n = 7` is new and does not break the trend: `0.412700`**
> over 86 277 informative posets. So the failure mode the ticket warns of — a
> characterisation certified at small `n` and false at the first untested value, which
> killed `2/(n+1)` at `n = 6` and the ordinal-sum characterisation at `n = 7` — **does not
> occur here.**
>
> And the minimisers at `n = 4, 5, 6, 7` are one shape: **`k` disjoint 2-chains** (plus an
> isolated point at odd `n`). That family `D_k` is defined at every `k`, so the question
> stops being an extrapolation. Evaluated in **exact rationals** on a Sylvester bracket, no
> float on the verdict path:
>
> | `k` | `n` | `1 − min_k Q_k` | gap | `c` |
> |---|---|---|---|---|
> | 2 | 4 | `1/3` | 0.4607 | **0.6180340** |
> | 4 | 8 | `1/7` | 0.6012 | **0.3582576** |
> | 6 | 12 | `1/11` | 0.6407 | **0.2530331** |
> | 8 | 16 | `1/15` | 0.6593 | **0.1957034** |
>
> **`c > 0.80` IS REFUTED OVER THE FULL NATURALLY LABELLED POPULATION** — already at
> `n = 4`, exactly, and at every `k` evaluated. No `n₀` rescues it. *(I did **not** prove
> `c(D_k) → 0`; that needs a lower bound on `λ_std(D_k)` uniform in `k`, which a test
> vector does not supply. The refutation needs one `k` and has eight.)*
>
> ### 2. AND IT SETTLES NOTHING, BECAUSE EVERY REFUTING POSET IS OUT OF REGIME. THIS IS THE FINDING.
>
> `c` is invoked at **one** place: after Step 2 has supplied `λ_std ≥ 1 − ε`, i.e. on posets
> with **gap `≤ ε_spec = 2×10⁻²`**. Every `D_k` has **gap `≥ 0.46`** — 23× outside that at
> `k = 2` and 33× at `k = 8`. Stratify the same population by gap and the direction
> **reverses**:
>
> | gap band | `n = 6` `min c` | `n = 7` `min c` |
> |---|---|---|
> | `[0.50, 0.70)` | 0.452934 | 0.412700 |
> | `[0.30, 0.50)` | 0.488010 | 0.514306 |
> | `[0.20, 0.30)` | 0.728438 | 0.687795 |
> | `[0.10, 0.20)` | 0.796735 | 0.787389 |
> | `[0.06, 0.10)` | 0.868532 | 0.858894 |
> | `[0.00, 0.06)` | **0.988958** | **0.881084** |
>
> **`min c` falls because the GAP is large, not because `n` is.** The band nearest the
> regime is the band where `c` is largest, at both `n`. *(The one band omitted above is
> `[0.70, 1.01)`, and it is omitted from this summary table only — it is printed in `s2`,
> it BREAKS the monotonicity at `0.673`/`0.556`, and it holds 14 and 38 posets at the
> near-antichain end where `λ_std ≈ 0` and `c` is a ratio of two small numbers. It is the
> farthest band from the regime; it does not disturb the reading, and it is named here so
> the table is not choosing its rows to fit the sentence.)*
>
> ### 3. THE REGIME IS REACHABLE, AND `c → 1` THERE. `0 of 4377` WAS A STATEMENT ABOUT `n ≤ 6`, NOT AN EMPTINESS THEOREM.
>
> `mg-76b2 (C1)`'s *"0 of 4377 primitive posets inside the budget"* is reproduced and
> extended (**0 of 86 277 at `n = 7`** too; smallest gap `0.038999`). It has been read in
> this corpus as though the regime were structurally empty. **It is not — it is out of
> enumeration range**, and the budget is reached at `n = 10` by an explicit primitive
> family. `N(n)`: antichain `{0..a−1} <` antichain `{a..n−1}`, `a = n/2`, **minus the single
> relation `(a−1, a)`** — exact figures:
>
> | `n` | gap (exact) | inside `ε_spec = 1/50`? | `min_k Q_k` | `c` (exact) |
> |---|---|---|---|---|
> | 8 | 0.026823309 | no | `1/34` | 0.9973402 |
> | 10 | 0.014445971 | **YES** | `1/65` | 0.9990476 |
> | 14 | 0.005520070 | **YES** | `1/175` | 0.9998047 |
> | 16 | 0.003743404 | **YES** | `1/260` | **0.9998969** |
>
> A second family (`(0, n−1)` removed instead) gives `0.9999555` at `n = 16`. **In the
> regime `c` goes to 1, not to 0**, with `min_k Q_k = 1/260` against a requirement of `1/5`
> — a factor of 52 of slack. **The ticket's premise survives on the only posets anyone has
> exhibited inside the regime.**
>
> ### 4. BUT THE PREMISE COSTS MORE THAN IT LOOKS, AND THIS IS THE PART THAT IS NEW: **`c` IS NOT AN INDEPENDENT UNKNOWN. IT IS `C₃^gap`.**
>
> On every poset, exactly:
>
> > **`c = (1 − C₃^gap · gap) / (1 − gap)`**,  `C₃^gap := min_k Q_k / gap`
>
> — verified as an exact rational identity at **all 90 654 primitive posets `n ≤ 7`** (and
separately on the exact Sylvester bracket at the 4376 of `n ≤ 6`). *The count is every
primitive poset because `primitive ⟺ connected` — `s0 (G)`'s `DISC ⟺ CUT`, verified here at
`n = 7` on 96 428 posets, which is why the loop's two filters collapse to one.* The two
> constants are one quantity in two currencies. **And the demands coincide**: evaluated
> self-consistently (the reconciliation `mg-01ea` landed), two lines of algebra give
>
> > **`ε_dem^(IV) = ε_leak / C₃^gap = ε_dem^(II)`.**
>
> **So chain (IV) does not buy a weaker demand than chain (II). It buys exactly chain
> (II)'s demand, with the same unknown written `1/x` instead of `x`.** The `10×` the ticket
> attributes to chain (IV) is the `10×` chain (II) already has, and `mg-9461` already priced
> it: *"the chain choice is worth `2/ε_leak = 10×` and no more."*
>
> **What chain (IV) *does* buy is real and is a different thing: a WEAKER HYPOTHESIS.**
> Chain (II) assumes `min_k Q_k ≤ C₃·gap`, a **relative** bound forcing `min_k Q_k → 0` with
> the gap; chain (IV) assumes `min_k Q_k ≤ 1 − c(1−gap)`, an **absolute** bound that permits
> `min_k Q_k ≈ 1−c` however small the gap gets. On `{gap ≤ ε_spec}` they deliver the same
> conclusion, but (IV)'s is strictly easier to prove. **Chain (IV)'s advantage is in
> PROVABILITY, not in the constant.**
>
> ### 5. AND `ε_dem = 0.20` IS THE `C₃^gap = 1` EXTREME POINT.
>
> `ε_dem^(IV) = 1 − (1−ε_leak)/c = 0.20` requires **`c = 1` exactly**, which by the identity
> is **`C₃^gap = 1` exactly** — a prefix indicator that *is* a minimiser of the Rayleigh
> quotient over `H`. **That is precisely the `C₃ = 1` whose gap-form reading `mg-94c3`
> measured FALSE at 1023 of 1032** (`STATE.md:164`, `:169`). So `0.20` is the value at the
> extreme point, not a value any measurement supports — and the wall, priced in the one
> unknown, is
>
> > **`ε_sup / ε_dem = C₃^gap / ε_leak = 5·C₃^gap`.**
>
> | `C₃^gap` | `ε_dem` | wall |
> |---|---|---|
> | 1 | 0.200000 | **5×** |
> | 2.386 (`n = 6`, out of regime) | 0.083822 | 11.9× |
> | 3.075 (`n = 7`, **new**, out of regime) | 0.065041 | 15.4× |
> | 10 (where chain (IV) stops closing) | 0.020000 | **50×** |
>
> **THE 5× REFRAMING IS THE `C₃^gap = 1` ROW AND ONLY THAT ROW.** It is the best case of the
> one unknown, not a property of chain (IV). **The Cheeger square is not avoided by chain
> (IV); it is refinanced, and `C₃^gap` is the interest rate.**
>
> ### 6. SO: IS `c > 0.80` ESTABLISHABLE? — **(c) OF THE TICKET'S THREE: NOT BOUNDED AWAY EITHER WAY, AND NOW WITH THE REASON.**
>
> Not (a): no proof is offered and the identity shows a proof would have to be a proof
> about `C₃^gap`, which `STATE.md:169` already records as unquantified. Not (b): the
> counterexample family exists and is exact, but it lives 23×–33× outside the class, and a
> refutation there does not transfer — **that is the same scope-invisibility defect this
> corpus has now recorded five times, and it would have been the sixth had this ticket
> stopped at its own sequencing directive.** What is left is (c), sharpened: **the class is
> non-empty but unenumerable** — 0 of 86 277 at `n = 7`, first reached at `n = 10` — so `c`
> in the regime is **UNMEASURED, not unmeasurable**, and the two families that reach it say
> `0.9999`. Two families are not a class.

---

## 1. What `c` is, stated before anything is done with it

The ticket's item 1. `Op-Form`'s Prefix-capture conjecture, quoted verbatim from source at
`:360–364`:

> **Conjecture (Prefix capture).** *A threshold cut of the dominant standard eigenvector
> gives a prefix `A_k` whose Rayleigh quotient captures a constant fraction, or possibly
> `1−o(1)`, of the dominant standard eigenvalue.*

So, per poset and then per population:

```
c(P) = max_{1<=k<=n-1} rho(A_k) / lambda_std(P),        c(n) = min over the population
rho(A) = <f_A, M f_A>/||f_A||^2,   f_A = 1_A - (|A|/n)1     (CENTRED: f_A lies in H)
```

The centring is not a convention this document asserts in prose — `s0 (D)` exhibits the
uncentred reading disagreeing on **1432 of 1562** `(poset, k)` pairs, and the centred one is
the only reading landing in `H = 1^⊥`. That it is also **`mg-76b2`'s** object is not assumed
either: `s0 (H)` reproduces its four figures exactly.

**⚠️ SCOPE AT THE DEFINITION, because it is the whole finding.** The conjecture sits in
`§ Empirical structural conjectures` (*"Preliminary small-poset computations suggest the
following"*), and the two conjectures immediately above it — Monotone standard mode and
Order identification — **both say "For a minimal counterexample"**. Prefix capture is stated
**bare**. So the source itself does not settle whether `c` is quantified over all posets or
over the class Step 2 delivers, and **the two readings give opposite answers**: §2 refutes
the bare reading, §3 supports the restricted one. Anyone quoting a `c` figure without saying
which reading is quoting a different number.

### 1.1 Which threshold — `0.80` or `40/49` (`mg-01ea`'s reconciliation, read not re-derived)

`mg-01ea` landed `mg-94c3`'s `C2` into `mg-76b2`'s own §5 and this ticket reads it there:

- **`c > 1 − ε_leak = 0.80`** — the **existence** threshold, exactly `ε_dem > 0`; the
  `ε_spec → 0` limit of the condition; carries no supply-side number.
- **`c ≥ (1−ε_leak)/(1−ε_spec) = 40/49 = 0.8163`** — the **self-consistent** threshold, the
  same condition evaluated at `ε_spec = ε_leak²/2 = 1/50`; necessarily tighter.

**Every verdict in this document is stated against BOTH**, because nothing here turns on
which: §2's figures land far below both and §3's far above both.

### 1.2 The requirement, stripped of every constant

Chain (IV) delivers `Φ_P(A_k) ≤ 1 − ρ(A_k) = min_k Q_k` (`mg-76b2` Lemma 2.1) and Step 5
needs that `≤ ε_leak`. So:

> **Chain (IV) closes on a poset ⟺ `min_k Q_k ≤ ε_leak = 1/5`**,

and `c ≥ 40/49` is exactly this re-parametrised at `gap = ε_spec`. Writing it this way is
what makes §4's identity visible; `c` and `C₃^gap` are two ways of dividing the same
`min_k Q_k`.

---

## 2. The sequencing directive, run first

`s1`. mg-76b2's row extended:

| `n` | primitive | informative | `min c` | source |
|---|---|---|---|---|
| 3 | 4 | 3 | 0.750000 | = `mg-76b2` |
| 4 | 27 | 26 | 0.618034 | = `mg-76b2` |
| 5 | 275 | 274 | 0.536219 | = `mg-76b2` |
| 6 | 4070 | 4069 | 0.452934 | = `mg-76b2` |
| 7 | 86278 | **86277** | **0.412700** | **NEW — first untested value** |

**Informative points, counted as the ticket asks: FIVE values of `n`, four of them
`mg-76b2`'s and one new.** The minimisers:

```
n=4: [(0,1),(2,3)]          n=5: [(0,2),(3,4)]
n=6: [(0,1),(2,3),(4,5)]    n=7: [(0,1),(2,4),(5,6)]
```

— `k` disjoint 2-chains, plus an isolated point at odd `n`. `D_k` is that family; §0.1 has
its exact values. `1 − min_k Q_k = 1/(n−1)` exactly at every `k` evaluated, attained at the
prefix `A₁ = {0}`.

**PROVEN, not extrapolated:** `c > 0.80` and `c ≥ 40/49` are both false on the full
naturally labelled population, at `n = 4` already, in exact rationals.
**NOT PROVEN:** `c(D_k) → 0`. Eight exact falling points are a direction.

---

## 3. The scope, which reverses the reading

`s2`. §0.2's band table, §0.3's in-regime families. Two further things belong here.

**(a) The envelope of the actual requirement.** `max min_k Q_k` over `{gap ≤ ε}`, against
the `0.2` that chain (IV) needs:

| `ε` | `n=4` | `n=5` | `n=6` | `n=7` |
|---|---|---|---|---|
| 1.00 | 0.66667 | 0.75000 | 0.80000 | 0.83333 |
| 0.20 | 0.20000 | 0.34091 | 0.35000 | 0.36842 |
| 0.10 | — | 0.11905 | 0.21429 | 0.22436 |
| 0.06 | — | — | 0.06667 | 0.16667 |
| 0.04 | — | — | — | 0.04487 |

**(b) The one reading that runs against §0.3, stated here rather than left for a reader to
find.** At a **fixed** gap cap, `min c` falls as `n` grows — `0.974 → 0.869 → 0.859` at
`ε = 0.10` for `n = 5,6,7`, and `0.989 → 0.881` at `ε = 0.06` for `n = 6,7`. **That is three
and two informative points**, it is confounded with population size (a minimum over more
posets falls for free), and every value is above both thresholds. It is not evidence that
`c` drops below the threshold in the regime and it is not evidence that it does not. Four
points killed `2/(n+1)`; three decide nothing here either.

---

## 4. The identity, and why chain (IV) is chain (II)

`s3`. The two lines, in full:

```
chain (IV):  eps_dem = 1 - (1-eps_leak)/c            [mg-76b2 sec.5, boxed]
self-consistently the budget IS the gap, eps = eps_dem, and c = (1 - g*eps)/(1 - eps)
with g := C_3^gap, by the identity of sec.0.4.  Substituting:

    1 - eps  =  (1-eps_leak)/c  =  (1-eps_leak)(1-eps)/(1 - g*eps)
    =>  1 - g*eps  =  1 - eps_leak            [divide by (1-eps) != 0]
    =>  eps        =  eps_leak / g            =  chain (II)'s eps_dem.        QED
```

Checked against both chains' own formulae as `mg-76b2` §6 writes them, at
`g = 1, 1.5, 2, 2.386, 3.075, 5, 10, 20` — equal, exactly, at all eight. **And the check is
not vacuous:** a chain (IV) deliberately mis-derived so that it *does* pay a Cheeger square
(`Φ ≤ √(2(1−c(1−ε_spec)))`) **disagrees at all five** grid points tested (`s3 (I4)`).

**`max C₃^gap` by `n`, reproducing `mg-76b2` and extending it:** `1.500, 1.473, 1.990,
2.386` at `n = 3..6` (`mg-76b2`'s, matched) and **`3.075` at `n = 7`** (new). ⚠️ **This is
the SAME measurement as §2's falling `min c`, read in the other currency, on the SAME
out-of-regime population.** It is a direction in both currencies and a verdict in neither,
and quoting one as corroboration of the other would be quoting one number twice.

---

## 5. What I did not do, at the claim

- **No `n = 8` sweep.** The population is ~2.8M and the box was under load-management
  instruction tonight; `n = 7` is the first untested value and is the one the trap concerns.
- **No proof that `c(D_k) → 0`**, and none that `c ≥ 40/49` in the regime. §0.6 is (c).
- **No attempt at L2, L3, L4, `C₃`, `ε_leak` or the growth bound** — the ticket forbids the
  last three and the others are not this item's.
- **`ε_leak = 0.20` is EMPIRICAL** (`mg-e35c` F5, on `mg-3ce3`'s envelope) and every figure
  derived from it inherits that, including both thresholds on `c` and the `0.2` of §1.2.
  `mg-9461` §4 records its direction of error as **optimistic**; nothing here improves it.
- **`STATE.md` NOT TOUCHED** — the ticket forbids it. §0's rows are `pm-onethird`'s to land
  or refuse, and the row that would take them is `:169`, whose closing sentence already
  reserves `Op-Form §4.3`'s four chains as *"`Op-Form`'s ground, not this ledger's."*
- **NO PREDICTIONS FILE.** This corpus's convention is to commit predictions before the
  instrument exists. I did not, and writing one now would be a fabrication rather than a
  record. The exposure that a predictions file would have disclosed is stated instead in the
  instrument's `README`: the ticket body printed `mg-76b2`'s four `min c` figures, the two
  thresholds and chain (IV)'s formula verbatim, so §2's reproduction is a **check**, and only
  §3 and §4 are findings.
- **One defect of my own, caught by a control before publication and kept in the history:**
  this instrument's module docstring wrote the central identity as `c = (1−minQ)/λ₂` where
  the truth is `(1−minQ)/(1−λ₂)`, and `c_bracket` inherited the slip from the prose while
  `float_c` had it right. `s0 (E)` is the control that now pins it, computing `ρ(A_k)` from
  `M` directly against `1 − Q_k` from the Laplacian at 25 682 `(poset, k)` pairs. A second:
  `s0 (C)`'s mutation control was built to assert the broken down-set peel gives **wrong
  numbers**; it gives **right** ones, and the control had to be rebuilt to assert the state
  count instead — independently arriving at the design `mg-9461`'s own `s0 (C)` records.
