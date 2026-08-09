# OneThird — INDEPENDENT AUDIT of `mg-81ff`. **THE REVERSAL SURVIVES EVERY ATTACK I COULD BUILD ON IT — and the word `monotonically` does not.** The **two in-regime families are ONE POSET under two labellings**, verified by explicit isomorphism; and a **THIRD family, found by searching the exhaustive population rather than constructed**, sits inside the budget from `n = 12` with `C₃^gap` rising through **`10.17` at `n = 25`**, where `mg-81ff`'s family sits at `1.03` — so `THE TICKET'S PREMISE SURVIVES ON THE ONLY POSETS ANYONE HAS EXHIBITED INSIDE THE REGIME` was true when written and is not true now

**Work item.** `mg-00b3` (repo `onethird_program`), filed by `pm-onethird`.
**Audits.** `mg-81ff` — [`docs/OneThird-ChainIV-CaptureFraction-mg-81ff.md`](OneThird-ChainIV-CaptureFraction-mg-81ff.md), instrument [`code/chain_iv_c_81ff/`](../code/chain_iv_c_81ff/), landed at `767c5a1`.
**Instrument.** [`code/chain_iv_audit_00b3/`](../code/chain_iv_audit_00b3/) — shares no line
with `lib81ff`, `lib76b2`, `lib9461` or `lib_d3c7`. Different enumeration, different
transport, different quadratic form, two different eigenroutines. The README tabulates
each difference; `a0`'s twenty controls, each with a live negative arm, are what make the
agreements below results rather than inheritance.

> ### ⛔ WHAT THIS DOCUMENT DOES NOT DO
>
> - **It does not re-attack the refutation.** The ticket is explicit that `min c` falling
>   and `c > 0.80` being false on the full population is `mg-76b2`'s result extended, and
>   that my effort goes to the **self-caught correction** instead. `§1` reproduces the
>   refutation only far enough to establish that I am measuring the same object.
> - **It does not touch `ε₀`, `L2`, `C₃ = 1`, or `STATE.md`**, and **`17/78` does not
>   occur in it**, with or without its scope.
> - **It prints no window figure** (`mg-131e` voided the supply that table rests on).

---

## 0. Verdict

> ### 0.1 THE REVERSAL IS REAL. `chain IV dies` IS **NOT** THE VERSION THAT SHOULD HAVE BEEN PUBLISHED.
>
> This is the finding the ticket says is at risk, and it survives four attacks:
>
> | attack | what it removes | result |
> |---|---|---|
> | re-derive the seven bands | shared code | **all fourteen `min c` values reproduce exactly** |
> | ten uniform re-binnings | the chosen boundaries | direction survives; *monotonicity does not* — see `0.2` |
> | equal-count bands | **the population confound `mg-81ff` itself names** | monotone at 4/6/8 bands at **both** `n`, and at 10 bands at `n = 7`; one violation of 0.006 at `n = 6` |
> | **no bins at all** — every threshold `t`, is `min c` below `t` at least `min c` above it? | every boundary anybody chose | **holds at every one of 69 944 thresholds below `0.596` at `n = 7`** (`0.559` at `n = 6`); the 161 that fail all sit above the global minimiser's own gap, where the test is trivially false |
>
> The third row is the one that matters most, because `mg-81ff §3(b)` names exactly one
> confound against its own reading — *"a min over more posets falls for free"* — applies
> it to the `n`-comparison, and does not apply it to the band comparison, where the
> lowest band holds **14** posets at `n = 6` and the `[0.10,0.20)` band holds **1350**.
> Held exactly equal, the confound does not explain the reversal.
>
> ### 0.2 BUT `MONOTONICALLY` IS CARRIED BY THE SIX BANDS, NOT BY THE POPULATION.
>
> Re-bin the same posets at uniform width `0.01` and **32 of 63 adjacent pairs violate
> monotonicity at `n = 6`, and 32 of 73 at `n = 7`**. They are **not** confined to the
> near-antichain tail `mg-81ff` discloses: **10 (`n=6`) and 7 (`n=7`) have both bands
> below gap `0.30`**, inside the low-gap region the reading rests on. Largest such rise:
> `n = 6`, `[0.130,0.140)` `min c` `0.824256` → `[0.140,0.150)` `0.874508`.
>
> **The claim that survives is DIRECTIONAL, not monotone**, and the honest form of it is
> bin-free and is one number per `n`:
>
> | `n` | smallest gap reached | `min c ≥ 40/49` for gap ≤ | chain (IV) **closes** (`max min_k Q_k ≤ 1/5`) for gap ≤ |
> |---|---|---|---|
> | 4 | 0.152786 | 0.400000 | 0.226308 |
> | 5 | 0.095674 | 0.171839 | 0.104715 |
> | 6 | 0.056245 | 0.160030 | 0.095353 |
> | 7 | 0.038999 | **0.132265** | **0.090472** |
>
> against a budget of `ε_spec = 0.020`. Both columns **fall at every `n`**. This is
> `mg-81ff §3(b)`'s own caveat in a form that is not confounded with population size — it
> is a threshold crossing, not a minimum over a band — and it is sharper than the two- and
> three-point version the deliverable prints. It is still only four points and it is
> decelerating; `mg-81ff`'s *"three points decide nothing here either"* is the right
> posture and I do not improve on it.
>
> ### 0.3 THE TWO IN-REGIME FAMILIES ARE **ONE POSET**.
>
> `N(n)` deletes `(a−1, a)` and `N'(n)` deletes `(0, n−1)` from the **same** complete
> bipartite order `K_{a,a}` (checked at every `n = 6..16`: `|rel|` is one short of `a²`
> with nothing outside the bipartite block). `Aut(K_{a,a})` is transitive on its `a²`
> relations, so **any** two single-relation deletions are isomorphic. Exhibited
> explicitly: `n = 6` under `(1,2,0,5,3,4)`, `n = 8` under `(1,2,3,0,7,4,5,6)`.
>
> **The tell is already in `mg-81ff`'s own numbers.** `min_k Q_k` is *identical* for the
> two at every `n` — `1/15, 1/34, 1/65, 1/111, 1/175, 1/260` — and `min_k Q_k` is the
> quantity that decides whether chain (IV) closes (`mg-81ff §1.2`). It is invisible only
> because the `N'` table omits that column and prints `gap` and `c` alone. The two differ
> only in the eigenvalue, at the third decimal, because `M` mixes the element index with
> the **position** index and so is not relabelling-invariant.
>
> So *"A SECOND FAMILY, so the answer is not one construction's artefact"* **is one
> construction.** `mg-81ff`'s hedge *"two families are not a class"* is, if anything, too
> generous to itself.
>
> ### 0.4 A THIRD FAMILY — AND IT ARRIVED BY SEARCH, NOT BY CONSTRUCTION.
>
> Ask the exhaustive population which poset **maximises `C₃^gap = min_k Q_k / gap`** and
> the answer at `n = 5, 6, 7` is one shape: **`i < j` iff `j ≥ i+2`**, the *staircase*
> `S_n`. It is `mg-81ff`'s own `max C₃^gap` row (`1.990, 2.386, 3.075`) — that row's
> maximisers are a family, and `s3` prints the row without saying so. `S_n` is primitive
> at every `n`, has a `2n`-element down-set lattice, and `e(S_n)` is Fibonacci, so it is
> affordable far past the sweep. In exact rationals:
>
> | `n` | `min_k Q_k` | gap (exact) | inside `1/50`? | `C₃^gap` | `c` (exact) |
> |---|---|---|---|---|---|
> | 7 | `1/6` | 0.0541957607 | no | 3.0753 | 0.8810844 |
> | 12 | `64/699` | 0.0187781484 | **YES** | 4.8758 | 0.9258259 |
> | 16 | `441/6388` | 0.0106071789 | **YES** | 6.5084 | 0.9409451 |
> | 20 | `605/10946` | 0.0068008493 | **YES** | 8.1271 | 0.9511976 |
> | 25 | `300/6773` | 0.0043572625 | **YES** | **10.1654** | 0.9598890 |
> | 28 | `142129/3599603` | 0.0034748779 | **YES** | 11.3629 | 0.9638647 |
>
> **Four consequences, and they do not all point the same way.**
>
> 1. **`c → 1` in the regime SURVIVES.** `c(S_n)` *rises* — 0.8811, 0.9258, 0.9410,
>    0.9512, 0.9639 — and is consistent with `→ 1`. **I did not find an in-regime family
>    with `c` bounded away from 1**, I say so rather than leaving the ticket's hedge
>    quietly upgraded, and `§3.3` records the four other constructions I tried.
> 2. **The quantitative reading does not survive.** `mg-81ff §I3`: *"On the two families
>    that DO reach the regime, `c = 0.99990` and `0.99996` … essentially the full `0.20`
>    … **THE TICKET'S PREMISE SURVIVES ON THE ONLY POSETS ANYONE HAS EXHIBITED INSIDE THE
>    REGIME**."* `S_12` is inside the regime and primitive, and gives `c = 0.9258259`,
>    i.e. `ε_dem^(IV) = 0.135882`, **not** `0.199918`. The *"factor of 52 of slack"* on
>    `min_k Q_k` is a factor of **2.2** on `S_12`.
> 3. **`mg-81ff`'s one in-regime family sits at the extreme point its own `§5` names.**
>    `C₃^gap` is `1.0650` on `N(10)` and `1.0275` on `N(16)` — essentially the `C₃^gap = 1`
>    row that `§5` correctly calls *"the best case of the one unknown, not a property of
>    chain (IV)"*. On the staircase, in the **same** regime, it is `4.88` and rising. By
>    `mg-81ff`'s own pricing `wall = 5·C₃^gap`, that is **24×** at `n = 12` against the
>    **5.2×** its family gives.
> 4. **AND IT CROSSES `10` INSIDE THE REGIME, FIRST AT `n = 25`.** `§5`'s table names `10`
>    as *"where chain (IV) stops closing"*. **`S_25` is primitive, has gap
>    `0.0043572625 ≤ 1/50`, and has `C₃^gap = 10.1654`** — exact rationals, one witness, the same shape of refutation as
>    `mg-81ff`'s own `D_k`. `§4`'s hedge that the rising `C₃^gap` *"is measured on the SAME
>    out-of-regime population, so it is a direction in both currencies and a verdict in
>    neither"* no longer covers it.
>
> ### 0.5 `CHAIN (IV) IS CHAIN (II)`: TRUE OF THE UNKNOWN, FALSE OF THE HYPOTHESIS.
>
> The identity `c = (1 − C₃^gap·gap)/(1 − gap)` is an **algebraic rearrangement of two
> definitions** — `C₃^gap·gap` *is* `min_k Q_k` — so verifying it at 90 654 posets checks
> arithmetic, not mathematics. `mg-81ff` says as much (*"the identity is FORMAL"*) and is
> right; the useful half of its `§4` is the reading that `c` and `C₃^gap` are two
> normalisations of **one** measured quantity, which is correct and which I confirm.
>
> The demand algebra `ε_dem^(IV) = ε_leak/C₃^gap = ε_dem^(II)` I **re-derived from
> `mg-76b2 §6`'s formulae rather than from `mg-81ff`'s two lines**, and I get the same
> thing, at all nine grid values, with a negative control (a chain (IV) mis-derived to pay
> a Cheeger square) that fires at every point.
>
> **The joint is the quantifier.** That algebra fixes **one value** of the one unknown.
> Neither chain is invoked at a value; each is invoked over the class `{gap ≤ ε_spec}`, and
> the step *"the worst `c` is `(1 − g·ε)/(1 − ε)`"* needs the worst `C₃^gap` to be attained
> **at** `gap = ε`. **It is not** — at `n = 7` it is attained at `gap = 0.054196` (the
> staircase) for every cap from `0.20` down to `0.06`. So over a class the relation is an
> **inequality**, and on this population it is strict: evaluated self-consistently, chain
> (IV) tolerates `1.23×` (`n=6`) and `1.42×` (`n=7`) the `ε_spec` that chain (II) does.
> **The direction is the safe one** — `mg-81ff`'s conclusion is *conservative* against
> chain (IV) — so this is a qualification and not a defect.
>
> **And the staircase makes the same point with no limit argument at all.** On the class
> Step 2 supplies: chain (II) needs a universal `g` with `min_k Q_k ≤ g·gap`, and closing
> needs `g ≤ ε_leak/ε_spec = 10`; `S_25` forces `g ≥ 10.1654`, exactly, so chain (II)'s
> route does not close there. Chain (IV) needs `c ≥ 40/49 = 0.816327`; `S_25` gives
> `0.9598890`, and its per-poset condition `min_k Q_k = 300/6773 ≤ 1/5` holds with `4.5×`
> to spare. **One exact in-regime witness on which one chain closes and the other does
> not.** `mg-81ff` names the mechanism correctly — chain (II)'s bound is *relative*, chain
> (IV)'s *absolute* — and then files it as *"an advantage in PROVABILITY, not in the
> constant"*. On this witness it is an advantage in what closes.
>
> ### 0.6 THE THINGS THE TICKET ASKED ME TO CONFIRM, CONFIRMED.
>
> - **Item 3, the `D_k` arithmetic.** All eight rows reproduce exactly, in exact rational
>   brackets: `c = 0.6180340 … 0.1957034`, gaps `0.4607 … 0.6593`, every one primitive,
>   `1 − min_k Q_k = 1/(n−1)` **asserted** (not eyeballed) at every `k`, argmin at `A₁`.
>   **And nothing downstream upgrades `refuted at eight k` to `c(D_k) → 0`**: the
>   disclaimer occurs three times in `mg-81ff`'s artefacts, including in its commit
>   subject's last clause, and every other `→ 0` in the corpus is about `min_k Q_k` or
>   `ε_spec` and is correctly attributed.
> - **Item 4, the control.** `mg-76b2`'s own transcript
>   `code/c3_prefix_capture_76b2/out_s3_c3.txt:89` carries `6 4070 2.386087 0.452934 523 of
>   4069`, so the `n ≤ 6` row *is* `mg-76b2`'s and reproducing it is a control —
>   `mg-81ff` uses it as one, marks those rows `= mg-76b2`, marks `n = 7` `NEW`, files
>   `s0 (H)` as a control, and discloses in advance that the ticket body printed the four
>   figures. `0.412700` over 86 277 informative posets occurs nowhere in `mg-76b2`'s
>   artefacts. **Both halves confirmed.**
>
> ### 0.7 VERDICT
>
> **CONFIRMED ON THE CENTRAL CORRECTION.** `mg-81ff` was right not to publish *"chain IV
> dies"*, right that the refuting posets are out of regime, right that the direction
> reverses, right about the identity, and right in every figure I could recompute — and it
> caught the scope-invisibility defect itself, which is the thing this corpus has failed at
> five times. **THREE JOINTS ARE OVER-STATED, ALL THREE IN THE SAME DIRECTION** — each is
> a claim about a *class* resting on evidence about a *choice*: `monotonically` on the
> choice of six bands, `a second family` on the choice of two labellings of one poset, and
> `the ticket's premise survives on the only posets anyone has exhibited` on the choice of
> the one family that happens to sit at the extreme point. **None of them inverts the
> verdict**; `§0.6`'s answer to *is `c > 0.80` establishable* remains `(c)`, not bounded
> away either way.

---

## 1. What I am measuring, and that it is the same object

`c(P) = max_k ρ(A_k)/λ_std`, `ρ(A) = ⟨f_A, M f_A⟩/‖f_A‖²`, `f_A = 1_A − (|A|/n)1`, taken
from `Op-Form §4.3` and `mg-76b2` and **not** from `mg-81ff`'s prose. Writing
`gap = λ₂(L) = 1 − λ_std` and `Q_k = 1 − ρ(A_k)`:

```
c = (1 - min_k Q_k) / (1 - gap)          C3gap = min_k Q_k / gap
```

`a0 (C)`'s negative arm shows the centring is a real choice — the **un**centred reading
disagrees at 1422 of 1548 `(poset, k)` pairs. `a0 (E)` asserts `min_k Q_k ≥ gap` exactly at
all 4376 primitive posets `n ≤ 6`, which is why `C₃^gap ≥ 1` and `c ≤ 1` identically;
neither is assumed anywhere.

**The population lands where `mg-81ff`'s does**, on a mask-and-transitivity enumeration
rather than an extension: `4 / 27 / 275 / 4070 / 86278` primitive, one fewer informative at
each `n` (`a0 (F)` names the exclusion: the antichain, where `λ_std = 0`), and `96 428`
naturally labelled posets at `n = 7`, which is `mg-d3c7`'s figure.

**One presentational difference, so a reader does not read it as a disagreement:** the
minimiser is not unique. At `n = 5` I get `[(0,1),(2,4)]` where `mg-81ff` reports
`[(0,2),(3,4)]`; both are *2 disjoint 2-chains + an isolated point*, differently labelled,
and both attain `0.536219`. `a1 (P2)` prints how many labelled posets attain each minimum.

---

## 2. The reversal (ticket item 1) — `a2`

`§0.1` and `§0.2` are the result. Two details belong here.

**(a) One band count differs by one, and the reason is this section's own subject.** I get
`1035 / 1259` at `n = 6` in `[0.20,0.30)` / `[0.30,0.50)` where `mg-81ff` has
`1034 / 1260`; totals agree at `4069`. One poset —
`[(0,2),(0,4),(0,5),(1,2),(1,4),(1,5),(3,4),(3,5)]` — has `λ₂` **exactly** `3/10`, which I
certified rather than inferred (the exact test says `λ₂ > 3/10` is false and
`λ₂ > 3/10 − 10⁻¹²` is true). It sits on a band edge, so which half-open band it lands in
is decided by the last bit of whichever eigenroutine ran. Its `c` is `0.785714`, it is
nobody's minimum, and **nothing in the reading moves** — but a boundary a rounding error
can move is precisely the hazard being tested, so it is reported rather than absorbed.

**(b) The band table is in the looser of the two currencies, and it hides one thing.**
`mg-81ff §1.2` establishes that chain (IV) closes on a poset **iff** `min_k Q_k ≤ ε_leak`,
and that `c ≥ 40/49` is that condition re-parametrised **at** `gap = ε_spec`. Away from
that point they are not the same, and the `c`-form is looser: at `gap = 0.10` the closing
condition allows `min_k Q_k ≤ 0.200` while `c ≥ 40/49` allows `0.265`. The consequence is
already in `mg-81ff §3(a)`'s table and is not remarked on there: at `n = 7`,
`max min_k Q_k` over `{gap ≤ 0.10}` is **`0.22436`, above the `0.2` its own column header
names as the closing condition** — a poset only `5×` outside the budget on which chain (IV)
does not close, while the band table's `min c` at the same cap, `0.858894`, reads
comfortably safe.

---

## 3. The regime (ticket item 2) — `a3`

`§0.3` and `§0.4` are the result.

### 3.1 Both of `mg-81ff`'s families are confirmed on every count the ticket asks

Primitive at every `n`; inside `ε_spec = 1/50` from `n = 10`; `min_k Q_k = 1/65 … 1/260`
against a requirement of `1/5`; `c = 0.9990476 / 0.9998969` (`N`) and
`0.9996372 / 0.9999555` (`N'`), each an exact rational bracket. Every figure `mg-81ff`
prints for them reproduces.

### 3.2 The staircase, and what it is evidence of

`§0.4`. Two things I will not let this audit upgrade:

- **`C₃^gap(S_n) → ∞` is NOT proven.** Seventeen exact in-regime points (`n = 12..28`) rising with a clean
  linear fit (`C₃^gap ≈ 0.406·n`, residual under 1% from `n = 12`; `min_k Q_k ≈ 1.105/n`;
  `gap ≈ 2.72/n²` — all three printed as fits in `a3`) is a **direction**. The limit needs
  an asymptotic for `λ₂(S_n)` uniform in `n`, which a test vector does not supply. This is
  the same line `mg-81ff` correctly refuses to cross for `c(D_k) → 0`.
- **The refutation of `C₃^gap ≤ 10` on the regime class does not need the limit.** It needs
  one witness in the class and it has one, exactly: `S_25`.

### 3.3 What else I tried, so that *"I could not"* is a measurement and not a silence

A third family with `c` bounded away from 1 in the regime needs `min_k Q_k` bounded away
from 0 while the gap goes to 0 — `C₃^gap` growing like `1/gap`, not like `n`. Tried, all
primitive, all evaluated exactly at `n = 10, 12, 14, 16` (`a3 (F3)`):

| construction | best `C₃^gap` in regime | best `c` in regime |
|---|---|---|
| unbalanced `K_{3,n−3}` minus one relation | 1.0585 | 0.9991091 |
| `K_{a,a}` minus **two** relations | 1.0506 | 0.9991402 |
| three blocks, one relation cut at each joint | 1.6717 | 0.9908505 |
| stride-3 staircase (`j ≥ i+3`) | — | — *(gap `0.0276` at `n = 16`: does not reach the budget)* |

None has `c` bounded away from 1. **A structural reason, offered as an argument and not as
a proof:** a small gap forces a sparse cut of `M` (Cheeger), and a naturally labelled poset
that is nearly an ordinal sum must have its near-cut at a **prefix**, because a natural
labelling of an ordinal sum puts the lower block's labels first. Separating the sparse cut
from every prefix cut is what a counterexample must do, and none of the four does it.
**The hedge stands and I have not upgraded it.** What has changed is that the evidence base
is one shape plus the staircase, and the staircase says the regime is not the benign place
the `0.9999` figures make it look.

---

## 4. The headline (`a4`)

`§0.5` is the result. The three checks in order: the identity is true and true by
substitution; the demand algebra is correct and I re-derived it from `mg-76b2 §6` rather
than reading `mg-81ff`'s, with a negative control that fires at all five grid points; and
the equality is **pointwise in the one unknown** while both chains are quantified over a
class, where it becomes an inequality — strict on this population, and in chain (IV)'s
favour.

`mg-81ff §5`'s wall table had no measured in-regime row. It now has three:

| poset | gap | in regime? | `C₃^gap` | wall `= 5·C₃^gap` |
|---|---|---|---|---|
| `N(16)` | 0.003743 | YES | 1.0275 | **5.1×** |
| `S_12` | 0.018778 | YES | 4.8758 | 24.4× |
| `S_25` | 0.004357 | YES | 10.1654 | **50.8×** |

**The `5×` row is not merely the extreme point — which is `mg-81ff`'s reading and is
right. It is also the row its one in-regime family happens to sit on.**

---

## 5. What I did not do, at the claim

- **No `n = 8` sweep.** The reversal is tested at `n = 6` and `n = 7`, which is **two**
  values of `n`, and `§0.2`'s falling crossings are **four** values. I do not treat either
  as more than that, and `mg-81ff`'s *"three points decide nothing"* applies to my table
  as much as to its own.
- **No proof of `C₃^gap(S_n) → ∞`**, and none of `c(S_n) → 1`; both are fits. `§3.2`.
- **`ε₀`, `L2`, `C₃ = 1` untouched** — the ticket forbids all three. **No `17/78`**, with
  or without scope. **No window figure.** **`STATE.md` untouched**, and I did not edit
  `mg-81ff`'s document: the three over-stated joints of `§0.7` are `pm-onethird`'s to land
  or refuse.
- **`ε_leak = 0.20` is empirical** (`mg-e35c` F5) and every threshold here inherits that,
  including `40/49`, the `1/5` closing condition and the `10` of `§0.5`. `mg-9461 §4`
  records its direction of error as **optimistic**; nothing here improves it, and if
  `ε_leak` moves, `S_25`'s crossing of `10` moves with it.
- **One defect of my own, caught by a control, kept in the history.** `a0 (A)` failed on
  its first run at 3280 of 5230 posets: it compared the two down-set enumerators as
  **lists** when only the **set** and the popcount-ordering are load-bearing. The failure
  was my control's, not my instrument's, and asserting list equality would have made the
  `n = 28` rows unreachable for a reason that does not exist. Rebuilt to assert both
  load-bearing properties, with the negative arm kept.
- **No `PREDICTIONS.md`, and I say why rather than back-dating one.** My dispatch printed
  `mg-81ff`'s band-table endpoints at both `n`, all four `D_k` values, both families' `c`,
  the primitive counts, `0.412700`, `3.075` and the headline — so §1, `a2 (R1)` and
  `a3 (F1)` are **checks**, and only the re-binnings, the bin-free crossings, the
  isomorphism, the staircase and `a4 (I3)` are findings. The instrument's README states
  the split at the file level.
