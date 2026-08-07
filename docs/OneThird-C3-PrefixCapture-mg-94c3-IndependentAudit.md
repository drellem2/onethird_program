# OneThird — INDEPENDENT AUDIT of `mg-76b2`: **CONFIRMED WITH CORRECTIONS.** The threshold relation is right, it is right in `ε_spec`, and it is right in `ε_c3ca` too — but `C₃ = 1` is true in ONE of the three currencies `Op-Form §4.3` uses, and the deliverable's title, verdict block and commit subject are the places that do not say which

**Work item.** `mg-94c3` (repo `onethird_program`). Pre-filed in the SAME ACTION as `mg-76b2`,
per the standing rule that a result of this class gets an independent audit rather than a
self-check. I am `mg-76b2`'s adversary, not its reviewer.
**Instrument.** [`code/c3_audit_a94c3/`](../code/c3_audit_a94c3/) — predictions committed at
`e200f18` before any script of it existed; scoring in that directory's `README` §3.
Shares **no code** with `lib76b2.py`; the library is written from
`spectral_near_ordinal_sum_program.tex` directly.
**Calibration used, per the ticket's instruction to say which.** `ε_leak = 0.20`
(`mg-e35c` F5's repaired value; **EMPIRICAL**, resting on `mg-3ce3`'s envelope). Every number
derived from it inherits that status, and the symbolic form is kept beside every number.

---

## 0. Verdict

> ## **CONFIRMED WITH CORRECTIONS.**
>
> ### 0.1 The one thing the ticket asked first — and the normalisation it was checked in
>
> **THE TICKET'S ALGEBRA IS CORRECT AS WRITTEN, AND I VERIFIED IT IN THE `ε_spec`
> NORMALISATION — `ε_spec = 6·E[inv_e]/(n²−1)`, `Op-Form:437` / `STATE.md:15`.**
> Both sides of the inequality live there and I checked that they do rather than assuming it:
>
> - **Demand.** `ε_dem = ε_leak²/(2C₃)` is derived at `Op-Form §4.2` from `1 − λ_std ≤ ε_spec`
>   through the Cheeger sandwich, then divided by `C₃` at `§4.3`. There is one `ε_spec` in
>   `Op-Form` and this is it.
> - **Supply.** `2/(n+1)` is `mg-200d`'s per-slot value as recorded at `mg-6bc2:320`, where the
>   optimisers are `E[inv] = 2/3, 1, 4/3` at `n = 3,4,5` and **`6E/(n²−1) = 1/2, 2/5, 1/3 =
>   2/(n+1)` exactly**. In `ε_c3ca = E/n²` those same three optimisers read `2/27, 1/16, 4/75`
>   — not `2/(n+1)` at any `n`, and not even the same *shape*. **Checked, 3/3 and 0/3.**
>
> Then, cross-multiplying: `2/(n+1) ≤ ε_leak²/(2C₃)` ⟺ `n+1 ≥ 4C₃/ε_leak²` ⟺
> **`n ≥ 4C₃/ε_leak² − 1`**. Solved by brute-force search against the closed form at **30/30**
> `(ε_leak, C₃)` grid points, exact rationals, no float anywhere on this path.
>
> **AND THE FACTOR OF 6 IS NOT WHERE THE TICKET FEARED IT WAS — WHICH IS A STRONGER RESULT
> THAN "I CHECKED".** Convert **both** sides to `ε_c3ca` by multiplying by `(n²−1)/(6n²)`:
> supply `→ (n−1)/(3n²)`, demand `→ ε_leak²(n²−1)/(12C₃n²)`, and the `(n−1)` and `n²` cancel
> to give `n+1 = 4C₃/ε_leak²` **identically**. Re-solved by search: **30/30 identical
> thresholds.** *The relation is normalisation-INVARIANT under a CONSISTENT conversion.*
>
> **THE HAZARD IS MIXING, AND IT IS WORTH EXACTLY THE ~6× THE TICKET FEARED, IN THE
> OPTIMISTIC DIRECTION.** Read the supply in `ε_c3ca` against a demand in `ε_spec` and the
> answer at `ε_leak = 0.20, C₃ = 1` is **`n ≥ 16` instead of `n ≥ 99`** — a window six times
> too short, i.e. an error that makes a programme report a win it has not got. Exhibited at all
> 30 grid points, ratios `6.00`–`6.33`. **That error is real, it is the shape this lineage has
> already committed, and IT IS NOT PRESENT IN THE TICKET'S RELATION NOR IN `mg-76b2`'s.**
>
> So `pm-onethird`'s ticket body is right, and **the mail to Daniel does not need correcting on
> this point.** At `C₃ = 1, ε_leak = 0.20` the threshold is `n ≥ 99` and the window still owed
> is `n ≤ 98`.
>
> ### 0.2 The corrections — three, and the first is load-bearing
>
> **C1. `C₃ = 1` IS A STATEMENT IN ONE CURRENCY OF THREE, AND THE SENTENCES A READER CARRIES
> AWAY ARE THE ONES THAT DO NOT SAY WHICH.** `Op-Form §4.3` names two readings of
> prefix-capture and `mg-76b2 §6` correctly resolves them into four chains. Its `C₃ = 1` is a
> **chain-(III)** statement: *there is a prefix `A_k` with `Φ_P(A_k) ≤ √(2(1−λ_std))`*, i.e.
> the Cheeger sweep bound is **delivered at a prefix**. That is exactly the `C₃` the ticket's
> relation carries, and **in that currency the constant is 1 and I confirm it** — 1032 of 1032
> primitive posets exhibiting L2's first disjunct satisfy it, worst ratio `0.2603`.
>
> **It is NOT 1 in the other two, and not even where L2 holds.** Restricting to the **1032
> primitive posets that EXHIBIT L2's first disjunct** (a non-degenerate top standard eigenspace
> whose eigenvector is monotone along `e`):
>
> | currency | `Op-Form §4.3`'s name for it | value under L2, `n ≤ 6` | exceeds 1 at |
> |---|---|---|---|
> | `C₃^(III)` — `Φ_pref ≤ √(2C₃ε_spec)` | the displayed relation | **`= 1`** | 0 of 1032 |
> | `C₃^gap` — `1−ρ_pref ≤ C₃(1−λ_std)` | the **gap-form repair**, named in the same sentence | `1.500, 1.473, 1.990, 2.386` — **rising** | **1023 of 1032** |
> | `C₃^cut` — `Φ*_pref/Φ*` | L3's **own wording** | up to `10/9` | 10 of 1032 |
>
> **WHY THIS IS LOAD-BEARING AND NOT PEDANTRY.** `mg-76b2 §6`'s own headline result is that
> chains (II) and (III) are **not** the same relation and differ by `2/ε_leak = 10` at every
> `C₃` — chain (II) being the gap-form, which never pays the Cheeger square. A reader who takes
> the title's unqualified *"`C₃` … IS `1`"* and substitutes it into chain (II) gets
> `ε_dem = ε_leak = 0.20` and a window of **`n ≤ 8`** instead of `n ≤ 98`. **That is a 10×
> overclaim, of exactly the shape this lineage has already produced twice, and the document's
> own §6 is what forbids it — while its title, its §0 verdict, its claim 6 and its commit
> subject are all silent on the currency.** The measurement above is what closes the door: the
> gap-form `C₃` is *not* 1 under L2, so the substitution is not merely unlicensed, it is false.
>
> This is a **FRAMING** correction in the ticket's own words. The theorem is right. §6 and §7
> are right. What is wrong is that the reading a grepper takes away is wider than the theorem.
>
> **C2. TWO THRESHOLDS ON `c`, NO RECONCILING SENTENCE.** `§5`'s boxed result and headline say
> the literal reading closes for every `c > 1 − ε_leak = 0.80`. `mg-76b2`'s own `s3_c3.py`
> uses the tighter, self-consistent `c ≥ (1−ε_leak)/(1−ε_spec) = 40/49 = 0.8163`, and §7's
> `c below the 0.816 threshold` column is computed against **that** one. Both are defensible;
> the document prints only the first in prose and only the second in its transcript. Verdict
> unaffected — `0.8163` is still an ordinary reading of "a constant fraction" and still far
> from `0.98`.
>
> **C3. §7's `C₃^cut` MUST BE SQUARED TO MEET §6's `C₃`, AND ONLY THE SCRIPT SAYS SO.**
> `s3_c3.py`'s docstring states it — *"`Φ*_pref ≤ √(2 (C₃^cut)² (1−λ_std))`, so `Op-Form`'s
> `C₃` is its SQUARE"* — and the **document does not**. A reader comparing §7's `max C₃^cut =
> 15/8` against §6's chain-(III) `C₃` is off by a square (`15/8 → 225/64 ≈ 3.52`).
>
> ### 0.3 The three "did it smuggle" checks
>
> **UNIFORMITY IN `n` — EXHIBITED, NOT ASSERTED. CONFIRMED.** The ticket asks whether the
> deliverable *shows* `C₃` is uniform rather than claiming it. It does, and I re-derived each
> ingredient from the source rather than checking its steps: **Lemma 3.1**'s constant is `2`
> from Cheeger and contains no `n` (conclusion measured: 0 failures over 4377 positive-gap
> posets, worst `Φ²/(2(1−λ_std)) = 0.2813`); **Lemma 3.2** is a finite-set identity (0
> exceptions over 48616 (permutation, cut) pairs); **Lemma 3.3** is a statement about orderings
> (0 exceptions over 6132 level sets of monotone eigenvectors, with a red drill showing 3340 of
> 3340 non-monotone posets **do** leave the prefix family). **So `4C₃/ε_leak² − 1` is a genuine
> bound and not an implicit inequality** — conditional on L2, which is labelled OPEN at claim 6
> and not claimed otherwise.
>
> **L4 — DID NOT OCCUR, AND VERIFIED AT THE SOURCE RATHER THAN AGAINST THE SCOPE STATEMENT.**
> Every derived number of `mg-76b2` routes its entire L4 dependence through the single
> constant `ε_leak`. That constant's repaired value comes from `mg-3ce3`'s `survives` predicate
> — a file **in another repo that neither `mg-76b2` nor I wrote** — and I opened it: `survives
> = len([pairs balanced in the side that are still balanced in the full poset]) > 0`, with
> `balanced_full` being `1/3 ≤ p^P_xy ≤ 2/3`. **Membership of a fixed window. It consults
> neither `F`, nor the deviation `D`, nor the fitted envelope**, all of which the probe computes
> as *reported outputs* downstream of the RED event. So the dependence is on L4's **threshold**
> `ε₀`, which `mg-345e` permits, and not on its **modulus**, which `mg-345e`'s ruling is about.
> **The third occurrence the ticket warned of did not happen.**
>
> **THE `mg-200d` CONJECTURE — NOT ASSUMED. CONFIRMED.** Strike it entirely and exactly **1 of
> `mg-76b2`'s 24 claims falls** — claim 17, the window `n ≤ 98`, whose own label already reads
> *"CONDITIONAL on 9 **and on the mg-200d conjecture**"*, and whose verdict-block statement is
> preceded by *"**if** the mg-200d route survives mg-131e"*. Claims 1–16 and 18–24 all stand;
> none states a supply-side value of `ε_spec` at all. **One caveat, and it is about how this
> corpus is actually read:** the conditional appears in the document and **not in the commit
> subject**, and commit subjects are what the next agent greps.
>
> ### 0.4 What I could not fault, and one correction *in `mg-76b2`'s favour*
>
> **16/16 of §7's tabulated figures reproduce EXACTLY** on code that shares nothing with
> `lib76b2` — `max C₃^cut` `1, 3/2, 6/5, 15/8`; `max C₃^gap` `1.500, 1.473, 1.990, 2.386`;
> `min c` `0.750, 0.618, 0.536, 0.453`; `c below threshold` `1/3, 5/26, 39/274, 523/4069`. So
> does the population (`5230` / `4377` primitive), `310404` (poset, cut) pairs, `25684`
> (poset, prefix) pairs, `872`/`48616` for Lemma 3.2, claim 18's three-predicate agreement
> (`0` disagreements), claim 19 (`0` posets inside the budget, smallest gap `0.0562`), claim 14
> (`Op-Form`'s supersession banner lists `§§6.4–7.4` and `§10`, does **not** mention `§4.3`, and
> ledger claim 15 still reads `PROVEN` unamended), and claim 22 (`8178` of `11316`).
>
> **THE CORRECTION IN ITS FAVOUR.** My monotonicity census reads **1727 YES / 3340 NO / 163
> UNDECIDED** where `mg-76b2` reports **1890 / 3340 / 0**. `1727 + 163 = 1890` exactly: the 163
> are the degenerate top eigenspaces where *"the* dominant eigenvector" is not well defined, my
> test declines them by declared policy (`B3`), and `mg-76b2`'s existential search over the
> eigenspace resolved every one of them as YES. **Its number is the right one and mine is the
> conservative one.**
>
> ### 0.5 What this audit says `mg-76b2` should NOT be read as having
>
> **The population supplies no evidence FOR the theorem, in either direction.** I ran the red
> drill `mg-76b2` did not: `Φ*_pref ≤ √(2(1−λ_std))` holds at **all 3340 non-monotone primitive
> posets too**. At `1−λ_std ≈ 0.3`, which is where this whole population lives and where `0` of
> `4376` posets are inside the budget, `√(2ε)` is a weak bound and the hypothesis is not
> separating. **§7's monotonicity-concentrates-at-small-gap table is a correlation and nothing
> more** — `mg-76b2` labels it `HEURISTIC` and is right to; a reader taking it as corroboration
> of the theorem would be reading it wrongly. **The theorem's support is its proof**, and this
> audit's contribution is that the proof was re-derived from the source rather than step-checked.
>
> ### 0.6 Not a refutation, and not softened into a correction
>
> The ticket forbids both directions and I have tried to obey both. Nothing in `mg-76b2`'s
> mathematics is wrong. `C1` is not a refutation dressed down: the theorem is true, `§6` states
> the currency, and I verified the constant is `1` where the ticket's relation uses it. Nor is
> it a nicety dressed up: the same document proves chains (II) and (III) differ by `10×`, so an
> unqualified `C₃ = 1` welded onto (II) is a `10×` error the document itself makes available,
> and my measurement shows that welding is **false** and not merely unlicensed.

---

## 1. Method, and why it is a re-derivation and not a step-check

The ticket's instruction is explicit: *"re-derive it from the source rather than checking its
steps. A step-check inherits a wrong framing; an independent derivation does not."*

Concretely, this audit:

1. **Wrote its library from `spectral_near_ordinal_sum_program.tex`**, not from `Op-Form` and
   not from `lib76b2.py`. The convention `σ : position → element` is taken from `tex:130–146`
   (`R(σ)e_a = e_{σ(a)}`, `(T_P)_{xa} = Pr[x` occupies position `a]`) and `tex:56`
   (one-line notation), which is the exact point at which `mg-76b2 §8` reports a live bug in a
   sibling instrument. `libA94.py` and `lib76b2.py` share no line.
2. **Derived Lemma 2.1 rather than checking it.** `(I−S_P)1 = 0` gives
   `⟨f,(I−S_P)f⟩ = ⟨1_A,(I−S_P)1_A⟩ = E|A∖σ(A)|`; `‖f‖² = k(1−k/n)² + (n−k)(k/n)² = k(n−k)/n`;
   divide. Then checked **two ways** — once from the matrix `T_P` and once by counting over
   `L(P)` — because a single path can be wrong the same way twice.
3. **Has no numpy on this machine**, so the eigen path is a hand-written cyclic Jacobi solver.
   That is an accident of the environment and it happens to be the right accident: there is no
   shared linear-algebra dependency between the two instruments either.
4. **Wrote predictions before any script existed** (`e200f18`), with ten hand measurements
   disclosed as hand measurements and two errors of my own filed in advance.

---

## 2. The threshold relation, re-derived

### 2.1 The inputs, and the normalisation of each

| side | statement | source | normalisation |
|---|---|---|---|
| demand | `ε_spec ≤ ½ε_leak²` | `Op-Form §4.2`, `:264–271`, **PROVEN** given the Cheeger sandwich | `ε_spec`, because it is derived from `1−λ_std ≤ ε_spec` |
| demand | `ε_spec ≤ ε_leak²/(2C₃)` | `Op-Form §4.3`, `:299–303`, `C₃` **UNQUANTIFIED** | same |
| definition | `E[inv_e] ≤ (ε_spec/6)(n²−1)` | `Op-Form :437`, `STATE.md:15` | *is* the definition of `ε_spec` |
| supply | `ε_spec = 2/(n+1)` under per-slot adjacency symmetry | `mg-200d`, recorded `mg-6bc2 §5.1` / `:320`, **CONJECTURE for all `n`** | checked below |

### 2.2 The supply side's normalisation, checked and not assumed

`mg-6bc2:320` records the per-slot optimisers as `E[inv] = 2/3, 1, 4/3` at `n = 3,4,5`.

| `n` | `E[inv]` | `6E/(n²−1)` | `2/(n+1)` | match | `E/n²` (`ε_c3ca`) | `= 2/(n+1)`? |
|---|---|---|---|---|---|---|
| 3 | `2/3` | `1/2` | `1/2` | ✓ | `2/27` | ✗ |
| 4 | `1` | `2/5` | `2/5` | ✓ | `1/16` | ✗ |
| 5 | `4/3` | `1/3` | `1/3` | ✓ | `4/75` | ✗ |

**`2/(n+1)` is the `ε_spec` normalisation, 3/3, and is not the `ε_c3ca` one, 0/3.**

### 2.3 The solve

`2/(n+1) ≤ ε_leak²/(2C₃)` ⟺ `n ≥ 4C₃/ε_leak² − 1`. Brute-force search vs closed form,
**30/30** over `ε_leak ∈ {1/5, 1/50, 1/10, 3/20, 1/4}` and `C₃ ∈ {1, 3/2, 2, 5/2, 3, 10}`.
At `ε_leak = 1/5, C₃ = 1`: **`n ≥ 99`**, window owed **`n ≤ 98`**.

### 2.4 Invariance, and where the factor of 6 actually bites

| arm | supply | demand | `n` at `ε_leak=1/5, C₃=1` |
|---|---|---|---|
| both in `ε_spec` | `2/(n+1)` | `ε_leak²/(2C₃)` | **99** |
| both in `ε_c3ca` (consistent) | `(n−1)/(3n²)` | `ε_leak²(n²−1)/(12C₃n²)` | **99** — identical, 30/30 |
| **mixed** | `(n−1)/(3n²)` | `ε_leak²/(2C₃)` | **16** — a factor `6.19` |

The mixed arm is wrong in the **optimistic** direction at all 30 grid points, ratios
`6.00`–`6.33`. The negative control `NC1` feeds three deliberately-wrong closed forms
(`−1` dropped → 100; the `4` halved → 49; a `6` wrongly inserted → 16) and the comparison
rejects all three, so §2.3's agreement is not vacuous.

### 2.5 The other three chains, re-derived

From Lemma 2.1's dictionary (`Φ ≤ 1−ρ ≤ 2Φ`) and Step 5's `Φ ≤ ε_leak`:

| | bound | `ε_dem` | window `n ≥` | reproduced |
|---|---|---|---|---|
| (I) monotone sweep | `Φ ≤ √(2ε_spec)` | `ε_leak²/2` | `4/ε_leak² − 1 = 99` | ✓ |
| (II) gap-form | `Φ ≤ 1−ρ ≤ C₃ε_spec` | `ε_leak/C₃` | `2C₃/ε_leak − 1 = 10C₃−1` | ✓ |
| (III) degraded prefix Cheeger | `Φ ≤ √(2C₃ε_spec)` | `ε_leak²/(2C₃)` | `4C₃/ε_leak² − 1 = 100C₃−1` | ✓ |
| (IV) literal | `1−ρ ≤ (1−c)+cε_spec` | `1−(1−ε_leak)/c` | `2/ε_dem − 1` | ✓ |

Chain (IV)'s windows come out at `80, 32, 16, 11, 9, 8` for
`c = 0.82, 0.85, 0.90, 0.95, 0.99, 1.00` at `ε_leak = 0.20`, and `196, 98` for `c = 0.99, 1.00`
at the superseded `0.02` — `mg-76b2 §5`'s table, exactly, on code that never read it. Chains
(II) and (III) differ by `2/ε_leak = 10` at every `C₃`, as claim 16 says.

---

## 3. The currency measurement — §0.2's `C1`, in full

### 3.1 What was measured

Restrict to **primitive** posets (the decomposable ones have `1−λ_std = 0` and every `C₃`
ratio there is `0/0` — claim 18, reproduced at 0 disagreements over three predicates that
share no code) with a **non-degenerate** top standard eigenspace whose eigenvector **is
monotone along `e`**. That is `1032` posets at `n ≤ 6` and it is L2's first disjunct,
exhibited rather than assumed.

| `n` | primitive ∧ L2 | `max C₃^cut` | `max C₃^gap` | `C₃^cut > 1` | `C₃^gap > 1` |
|---|---|---|---|---|---|
| 3 | 3 | `1` | `1.500` | 0 | 1 |
| 4 | 16 | `1` | `1.473` | 0 | 13 |
| 5 | 108 | `13/12` | `1.990` | 1 | 106 |
| 6 | 905 | `10/9` | `2.386` | 9 | 903 |

and, in the currency the ticket's relation uses, `Φ*_pref ≤ √(2(1−λ_std))` at **1032 of 1032**,
worst ratio `0.2603`.

### 3.2 What it does and does not show

**It does not refute the theorem, and saying it did would be the exact error I filed against
myself as `P9` before running anything.** `mg-76b2`'s theorem does not claim the best prefix is
the best cut, and does not claim the gap-form constant is `1`. It claims the *Cheeger sweep
bound is delivered at a prefix*. `C₃^cut > 1` and `C₃^gap > 1` are both compatible with that,
and `mg-76b2 §3` says so in its own words (*"468 of 5230 posets have `Φ*_prefix > Φ*` strictly
… what rescues it is that the sweep of a monotone eigenvector never proposes the offending
cut"*).

**It does show** that the constant is `1` in exactly one of the three currencies `Op-Form §4.3`
puts on the table, and that the other two are `> 1` **even under L2's own hypothesis** — which
is what forbids the (II)-substitution described in §0.2.

**A hand claim, checked rather than asserted.** `C₃^gap ≥ 1` identically, because `1−λ_std` is
the *minimum* of `1−ρ(f)` over all of `H` and a centred prefix indicator lives in `H`. Machine:
`0` violations over `4376` positive-gap posets, and `1` **is** attained, so the bound is tight
and not slack (`NC6`). This matters in both directions: it is why `STATE.md:164`'s
*"`C₃ ≥ 1`, so the omission runs optimistic"* is **unconditionally true** as a statement about
the gap-form `C₃`, while `mg-76b2`'s correction of it is true **conditional on L2** and in
chain (III)'s currency. Both sentences are correct; they are about different numbers.

---

## 4. Scored predictions

| # | prediction | outcome |
|---|---|---|
| P1 | Lemma 2.1 reproduces at 0 exceptions on disjoint code | **HELD** — 0/25684, factor 2 attained 4812 times |
| P2 | the Cheeger sweep conclusion holds at 0 exceptions | **HELD** — 0/4377, worst `0.2813` |
| P3 | monotone ⟹ level sets are prefixes/suffixes, 0 exceptions | **HELD** — 0/6132, red drill 3340/3340 |
| P4 | `C₃^gap > 1` somewhere **under L2** (bet 70%) | **HELD** — 1023 of 1032, worst `2.386`. This is `C1`. |
| P5 | at least one of §7's 12 figures fails to reproduce (bet 45%) | **MISSED** — 16/16 reproduce, once **my** defect is removed (§5) |
| P6 | 0 load-bearing uses of L4's modulus | **HELD**, and verified at `mg-3ce3`'s source rather than against the scope statement |
| P7 | `2/(n+1)` only at labelled sites; 0 headline claims change | **HELD** — 1 of 24 claims falls, labelled at the claim; 6 machine-bare sites all read as labelled by hand (§5) |
| P8 | the chain-(III) constant comes out at `1` (bet 65%) | **HELD** — 1032/1032 |
| P9 | *my* likely error: reading `Φ*_pref/Φ*` as what the theorem is about | **AVOIDED, and it was live** — §3.2 is the sentence that avoids it, and P4's result is precisely the material that would have produced it |
| P10 | *my* likely error: a framing correction reported as a refutation | **AVOIDED** — `C1` is reported as FRAMING, in the ticket's own words, and §0.6 says why it is neither softened nor inflated |

---

## 5. Defects of this instrument, kept in the source

Four, three of them caught by my own negative controls firing against correct code.

1. **`c = ρ_max/λ_std` divided by zero and printed `0.000` as if it were a capture fraction.**
   The antichain has `S_P|_H = 0`, hence `λ_std = 0` and `ρ_max = 0`, so `c` is `0/0` there.
   My first `C2/C3` table read `min c = 0.000` at every `n` and my primitive counts were larger
   than `mg-76b2`'s by exactly `1` at every `n`. **`mg-76b2`'s exclusion is the correct one**;
   `P5` scored `HELD` on this artefact before it was fixed and scores `MISSED` after.
2. **A negative control that dropped its own hypothesis.** `NC2` asserted Lemma 3.3's
   conclusion about whatever vector Jacobi returned for the antichain — `[0.707,−0.707,0,0]`,
   which is **not monotone**. It duly "failed" against correct code. Fixed by using the
   source's own tied vector `(a,a,a,−3a)`, whose negation is monotone and which is what makes
   the order-slice defect visible at all.
3. **A census population that stopped one `n` short.** `NC3` ran `n = 3,4,5` and reported
   `8177/11312` against `mg-76b2`'s `8178/11316`. Its `n ≤ 5` **includes `n = 2`**, and the
   single missing disagreement is the 2-chain witness the document itself names. Fixed;
   reproduces exactly.
4. **A conditional-marker classifier that counted the word `window`** — the noun a conditional
   qualifies, not the qualifier. `NC5` caught it. Removed; changes no verdict in `a4`. The
   remaining 6 machine-bare sites are reported and then **read by hand** rather than tuned
   away: all 6 are inside `mg-76b2`'s instrument, none in its deliverable, and each carries its
   conditional in wording the regex does not cover (`"No assumption of…"`, `"ASSUMES the
   mg-200d conjecture"`, the column header `n >= (mg-200d)`). **Tuning the regex until it
   returned `0` would have made the census unfalsifiable.**

---

## 6. Proposal for `pm-onethird` — stated as a proposal, not an edit

**Nothing here has been written into `STATE.md` or into `Op-Form`.** `mg-76b2 §10` already
carries three proposals of its own and I do not duplicate them; these are additions to that
list, and they follow from `C1`.

> **Proposed to `mg-76b2 §0` and to any `STATE.md` landing of it.** State the currency where
> the result is stated, not only where it is derived. Suggested: *"`C₃ = 1` in the currency
> `Op-Form §4.3`'s displayed relation uses — the loss inside the Cheeger square,
> `Φ_pref ≤ √(2C₃ε_spec)`. **It is NOT 1 in the gap-form `1−ρ_pref ≤ C₃(1−λ_std)` that §4.3
> names in the same sentence**, where it is measured at `1.473 → 2.386` over `n = 4..6` even
> restricted to posets exhibiting L2 (mg-94c3 §3). Chain (II) therefore does not inherit this
> result, and substituting `C₃ = 1` into it would overstate the window by `10×`."*
>
> **Proposed to `mg-76b2 §7`.** Add the one sentence its own script's docstring carries and its
> document does not: `Op-Form`'s chain-(III) `C₃` is the **square** of `C₃^cut`.
>
> **Proposed to `mg-76b2 §5`.** Reconcile the prose threshold `c > 1 − ε_leak = 0.80` with the
> instrument's `c ≥ (1−ε_leak)/(1−ε_spec) = 40/49 = 0.8163`, which is what §7's own column is
> computed against.
>
> **Not proposed, deliberately.** No change to the ticket's relation `n ≥ 4C₃/ε_leak² − 1`,
> which is correct; no change to `STATE.md:164`, which is `mg-345e`'s row and whose
> *"`C₃ ≥ 1`, so the omission runs optimistic"* is true of the gap-form `C₃` unconditionally
> (§3.2) — `mg-76b2`'s proposed replacement is also true, conditionally, and the two should be
> merged by whoever owns the row rather than one struck by an auditor.

---

## 7. Scope statement

One deliverable, as budgeted. Not done, and deliberately:

- **L2 is not attempted, and neither is L4 or the `mg-200d` conjecture.** This audit is about
  whether `mg-76b2`'s conclusions follow from its stated hypotheses in the stated currencies.
- **`n ≤ 6` throughout.** Every `n`-growth statement here is a **direction**. A finite
  population can refute a uniform-in-`n` bound and can never establish one, and `0` of `4376`
  primitive posets in it are inside the budget `ε_spec ≤ 2×10⁻²` (smallest gap `0.0562`), so
  **every `C₃` figure in this document is measured outside the regime it would be used in** —
  the same limit `mg-76b2` declares, inherited rather than pretended away.
- **Degenerate top eigenspaces are returned `UNDECIDED`, 163 of them**, not searched. My
  monotonicity test is therefore *sufficient* only, and `mg-76b2`'s existential search is the
  stronger instrument here (§0.4).
- **`mg-76b2`'s §8 finding about `lib2de0` is reproduced (`8178/11316`) and its consequences
  are still NOT ASSESSED.** `code/direct_prefix_audit_2de0/` is `mg-2de0`'s file and this audit
  does not own it either.
- **No `STATE.md` edit, no `Op-Form` edit, no edit to `mg-76b2`'s deliverable.** §6 is a
  proposal.
- **`ε_leak = 0.20` is empirical and is not pinned here.** It is `HEURISTIC`, resting on
  `mg-3ce3`'s envelope, and every headline number that uses it says so.
