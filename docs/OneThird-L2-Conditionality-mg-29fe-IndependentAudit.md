# OneThird — mg-29fe's INDEPENDENT AUDIT of mg-28ff's L2-free routes to `C₃^(III) = 1`

## **THE AFFIRMATIVE HALF HOLDS AND I TRIED FOUR WAYS TO BREAK IT. THE NEGATIVE HALF'S DIAGNOSIS IS THE DEFECT: `c♯ = ρ·Δ_P − ρ²(1−λ_std)/2` is an IDENTITY, `Δ_P ≤ 1` is a triviality, and together they say THE SWEEP ALONE CANNOT REACH `1` AT ANY `n` — so the thing that can break route (M♯) is the MONOTONE-CONE PRICE `ρ`, which §4.5 never names. And "both extra steps are load-bearing" is HALF TRUE: the cited counterfactual establishes ONE of the two, and the untested cell shows the other is NOT load-bearing at the `n` the claim is made at.**

**Work item:** `mg-29fe` — the independent audit of `mg-28ff`, filed late by `pm-onethird`'s
own account.
**Instrument:** `code/l2_audit_29fe/` — `lib29fe.py` written from the corpus's definitions,
with `lib28ff.py` **not opened until every number here had been produced**.
**Predictions:** committed at `d7ccc1f`, before the parent's document or code were opened.

---

## §0. VERDICT

| | verdict |
|---|---|
| **The affirmative half** (`C₃^(III) = 1` without L2, 4377/4377 primitive `n ≤ 6`) | **CONFIRMED.** Reproduced on an instrument sharing no line of code with the parent's, and it survived four arms designed to falsify it (§5). |
| **Item 1 — the rising-constants table** | **CONFIRMED, and the ticket's suspicion is REFUTED.** All five `c_true` values re-derive exactly; the increments **are** strictly decreasing. The apparent slip is in the **ticket's own compression**, not in mg-28ff. |
| **Item 2 — "it is the Cheeger sweep that degrades"** | **HALF RIGHT, AND THE MISSING HALF IS THE DECISIVE ONE.** True as a measurement of the *gap*; false as an account of what can make the route *fail*. See §3 — this is the finding. |
| **Item 3 — the `n = 6` boundary** | **THE BLANKET SCOPE HOLDS AND WAS RIGHT BY A WIDE MARGIN; THREE LABELLING DEFECTS, ONE OF THEM NOW DEMONSTRATED RATHER THAN FEARED.** Nothing has propagated to `STATE.md` or `roadmap.md`. But the exhaustive `n = 7` landed during this audit: mg-28ff's 106-poset sample reads `c_true = 0.176`, the truth is **`0.341`**, and **both route constants exceed `1` at `n = 7`** — so §4.3's *"100 % at every **enumerated** `n`"* is a sample read as an enumeration and is **false of the truth**. §4.1. |
| **Item 4 — the two added steps** | **OVER-CLAIMED AT EXACTLY ONE JOINT, and UNDER-CLAIMED at another.** §6. |
| **Item 5 — the quantifier move** | **VALID AT EVERY USE SITE.** Lemma 3.3 has exactly one use site in each document, and both branches of the median split were checked, not read. §5. |

**What may not be quoted out of this document.** Every number here is a maximum over an
**exhaustively enumerated** population of naturally labelled posets with `n ≤ 6`. My `n = 7`
work is a **deterministic sample** and is labelled as such at each appearance. Nothing here
reaches the `n ≥ 99` the architecture consumes, and nothing here is a bound in `n`.

---

## §1. WHAT I REPRODUCED, AND WHAT THAT IS WORTH

`PREDICTIONS.md` H1 discloses a **very large** exposure: my dispatch printed mg-28ff's
entire commit subject, including both route sequences, `c_true` and its four increments,
the `6 of 275` counterfactual, and the diagnosis sentence. **Every figure in this section is
therefore a REPRODUCTION, not a discovery**, and is tagged `[REPRO]`.

| | mine | mg-28ff | |
|---|---|---|---|
| naturally labelled posets `n ≤ 6` | **5230** | 5230 | `[REPRO]` |
| primitive | **4377** | 4377 | `[REPRO]` |
| per `n` (2..6) | **1, 4, 27, 275, 4070** | same | `[REPRO]` |
| `c_true` | **0.125000, 0.222222, 0.271353, 0.308339, 0.327508** | same | `[REPRO]` |
| `Σ_k leak(A_k) = ½·E[D_F]` | **5230 / 5230 exact, 0 exceptions** | same | `[REPRO]` |
| `Φ*_pref ≤ E[D_F]/(2⌊n²/4⌋)` | **5230 / 5230 exact** | same | `[REPRO]` |
| L2's first disjunct fails at, `n ≤ 5` primitive | **176** (0, 0, 10, 166) | — | new grain |

The L2 census is one place I am **strictly stronger** than the parent: mg-28ff computes it
in **float at tolerance `1e-9`** (`out_b5_trend.txt`). Here `L2's first disjunct fails ⟺
ρ = μ_pref/(1−λ_std) > 1`, and `μ_pref` is bracketed by bisection on an **exact copositivity
test** of `Q − tN` over the monotone cone, so the census is exact.

---

## §2. ITEM 1 — THE RISING-CONSTANTS TABLE IS RIGHT, AND THE TICKET'S OWN RESTATEMENT IS WHAT LOOKS WRONG

The ticket asks whether `.049 → .037 → .019` depends on an arithmetic slip, and warns that a
wrong convergence "inverts the ticket's entire diagnosis". **It does not, and here is why the
suspicion arose.**

Re-derived independently, exactly, `c_true(n) = max Φ*_pref²/(2(1−λ_std))` over primitive
posets, by PSD bisection with a bracket `5.8e-11` wide:

| `n` | primitive | `c_true` | Δ |
|---|---|---|---|
| 2 | 1 | `0.125000` | — |
| 3 | 4 | `0.222222` | `+0.097222` |
| 4 | 27 | `0.271353` | `+0.049130` |
| 5 | 275 | `0.308339` | `+0.036987` |
| 6 | 4070 | `0.327508` | `+0.019169` |

**Strictly decreasing.** `0.0972 > 0.0491 > 0.0370 > 0.0192`.

**Where the ticket's `.019`-vs-`.020` worry comes from.** The ticket body quotes `c_true` to
**three** decimals (`0.222, 0.271, 0.308, 0.328`) and then quotes increments
`.097, .049, .037, .019`. Differencing the **rounded** values gives `.020`, not `.019` — so
the ticket's own restatement is internally inconsistent while mg-28ff's six-decimal table is
not. `0.327508 − 0.308339 = 0.019169`, which rounds to `.019`. **The defect is in the
ticket's compression of the parent, not in the parent.** This is worth recording because
compressing a table to three decimals and then differencing it is a reproducible way to
manufacture a phantom arithmetic error.

**One thing the parent's §9 says that is inexact.** P7 is scored on the claim that `c_true`'s
argmax at `n = 4, 5, 6` is *"a disjoint pair of equal chains"*. At `n = 4` it is
`[(0,1),(2,3)]` and at `n = 6` it is two disjoint 3-chains — both correct. At `n = 5` it is
`[(0,1),(3,4)]`, which is **two 2-chains plus an isolated element**, not a disjoint pair of
equal chains (`n = 5` admits none). The `|Aut| = 2` claim survives; the description does not.

---

## §3. ITEM 2 — THE FINDING. "THE SWEEP DEGRADES" IS A TRUE MEASUREMENT AND A WRONG DIAGNOSIS

§4.5's third bullet is the sentence `mg-51f4` is scoped against:

> *"It is in the **Cheeger sweep as an instrument** — the square root and the Cauchy–Schwarz
> throw away a factor that grows with `n`. Anyone attacking this next should attack the
> sweep, not the poset."*

### 3.1 The decomposition, which is algebra and not measurement

Route (M♯)'s constant is `c♯(P) = μ_pref(2Δ_P − μ_pref)/(2(1−λ_std))`. Write

> **`ρ = μ_pref/(1−λ_std) ≥ 1`** — the price of the **quantifier move**: how far the best
> *monotone* vector is from the true optimum. `ρ = 1` is **exactly** L2's first disjunct.

Substituting `μ_pref = ρ(1−λ_std)` and cancelling:

> $$c^{\sharp} \;=\; \rho\,\Delta_P \;-\; \frac{\rho^{2}(1-\lambda_{\mathrm{std}})}{2}
> \qquad\text{and since }\Delta_P\le 1,\qquad c^{\sharp}\;\le\;\rho\,\Delta_P\;\le\;\rho .$$

`Δ_P = max_i(1 − (S_P)_ii) = max_i Pr[pos(i) ≠ i] ≤ 1` is a probability complement, so the
bound is unconditional. Two consequences follow with no computation at all:

> **(A) If `ρ = 1` then `c♯ = Δ_P − (1−λ_std)/2 < 1` at every poset and every `n`.**
> The sharpened sweep, fed an optimal vector, **cannot reach `1`**. Not at `n = 7`, not at
> `n = 99`, not ever.
>
> **(B) Therefore `c♯ > 1` requires `ρ > 1/Δ_P > 1`.** The **only** channel through which
> route (M♯) can fail is the **monotone-cone relaxation**.

### 3.2 The measurement that separates them

`c_sweepL2 := Δ_P − (1−λ_std)/2` is route (M♯)'s constant **with the cone price switched
off**. It is fully exact — it needs no cone minimisation at all. Maxima over primitive
posets:

| `n` | `c_true` (truth) | **`c_sweepL2`** (THE SWEEP ALONE) | `max Δ_P` | mg-28ff's `c♯` |
|---|---|---|---|---|
| 3 | `0.222222` | `0.500000` | `0.666667` | `0.500000` |
| 4 | `0.271353` | `0.636846` | `0.833333` | `0.636846` |
| 5 | `0.308339` | `0.752421` | `0.900000` | `0.803289` |
| 6 | `0.327508` | **`0.825114`** | `0.950000` | **`0.943151`** |

**Read column-wise, not row-wise:**

* At `n = 3` and `n = 4` the sweep-alone column **equals `c♯` to six decimals**. There the
  whole route constant *is* the sweep, and mg-28ff's diagnosis is exactly right.
* At `n = 5` and `n = 6` they **separate**, and the separation is the cone price.
* The sweep column is **bounded by `Δ_P < 1` forever**. The cone column is bounded by
  nothing. §4.5's own urgency argument — *"simple extrapolation of either puts it through
  `1`"* — is an extrapolation of the term the sentence does not name.

> **CORRECTION TO MY OWN FIRST STATEMENT OF THIS, OWED TO `mg-51f4`.** My early mail put the
> cone price at *"13 % of `c♯` at `n = 6`"* by differencing the two **maxima** in the table
> above. Those maxima are **attained at different posets**, so the difference is not a
> per-poset quantity. `q51f4` supplied the right instrument: the floor evaluated at
> **`c♯`'s own argmax**, which is `1.0000, 1.0000, 0.9129, 0.8593` at `n = 3..6` — so the
> cone price at `n = 6` is **14.1 %**, not `12.5 %`. It moves in my direction and the
> correction is `mg-51f4`'s. (`c♯`'s argmax at `n = 6`:
> `[(0,1),(0,2),(0,4),(0,5),(1,2),(1,5),(3,4),(3,5),(4,5)]`, `1−λ_std = 0.236288`,
> `Δ_P = 0.928571`, floor `0.810428`.)

### 3.2a PRIORITY, AND WHY IT MAKES THIS FINDING STRONGER RATHER THAN WEAKER

**Consequence (A) is `mg-51f4`'s, and it was committed before my mail was sent.** Its
`code/sweep_loss_51f4/PREDICTIONS.md` (commit `01c206f`, author date `2026-08-09T20:24:09Z`)
files as its P1, pre-run: *"THE FLOOR. For every poset, `c♯(P) ≥ Δ_P − γ/2`"*, with the same
proof and — as §6.1 below matters for — **both branches**. My mail is stamped `20:57:23Z`.
I did not know, and I record the order rather than the coincidence.

**Why this is the strongest form the finding could take.** Two instruments with no contact
until after both had committed — mine by `n!` enumeration with PSD by principal minors, its
by down-set DP with definiteness by Sylvester/Bareiss minors on the `(n−1)×(n−1)` pencil —
produce `0.500000, 0.636846, 0.752421, 0.825114` for the sweep-alone column **to six
decimals**, and agree on `5230 / 4377 / 1,4,27,275,4070`, on `c_true(6) = 0.327508`, on
`c♯(6) = 0.943151`, and on `f*(6) = 0.811649`. The re-diagnosis in §3 is therefore not one
auditor's reading of one document.

**And it is confirmed in the direction that matters most.** `mg-51f4` reports exhibited
posets at which each route **fails**: route (F) at `n = 7` (two antichains `{0,1,2}`,
`{3,4,5,6}`, all `a<b` except `(2,3)`; `f* = 1.2266`) and route (M♯) at `n = 13` (a 12-chain
plus one isolated element; `c♯ = 1.0133`, `μ_pref` bracketed by the same exact copositivity
test used here). **I have NOT verified either and do not claim them as audited** — they are
outside this ticket, which audits mg-28ff's `n ≤ 6` claims. What I will say is that the
`n = 13` witness is exactly the shape consequence **(B)** requires: `ρ > 1/Δ_P`. A route that
died through the sweep alone would contradict §3.1.

### 3.3 The candidate causes, enumerated, and what the evidence separates

The ticket asks for this explicitly.

| candidate | does the evidence separate it? |
|---|---|
| **the Cheeger sweep** (Cauchy–Schwarz, `√`, co-area, median split) | **YES.** `c_sweepL2` isolates it exactly: `0.500 → 0.825`. It **does** degrade, and mg-28ff is right about that. |
| **`Δ_P`** | **YES, and it is not an independent cause** — it is the sweep's own parameter. `max Δ_P` rises `0.667 → 0.950`, which is most of `c_sweepL2`'s rise, and it rises for a reason that has nothing to do with the instrument: `Δ_P = max_i Pr[pos(i) ≠ i] → 1` for almost every poset as `n` grows. **This is a property of the population, not a loss.** |
| **the monotone-cone relaxation `ρ`** | **YES, and §4.5 does not name it.** It is zero at `n ≤ 4` and worth `0.118` at `n = 6`, and by (B) it is the *only* term that can carry `c♯` past `1`. |

**So the diagnosis should read:** the sweep's loss grows but is **provably capped below `1`**;
what decides whether route (M♯) survives at large `n` is `ρ`, the price of the quantifier
move — which is precisely the quantity L2 sets to `1`. That is a sharper and less
comfortable statement than §4.5's, because it says the new route's failure channel is the
**same quantity** the old hypothesis controlled — the move buys a *relaxation* of L2
(`ρ ≲ 1/Δ_P` rather than `ρ = 1`), not an escape from it.

### 3.4 Route (F) contains no Cheeger sweep at all

Independent of everything above. §4.5 offers one cause for the rise of **both** columns. But
route (F)'s bound is the **linear co-area/footrule inequality** of §3 — `min_k a_k/b_k ≤
Σa/Σb` — with **no Cauchy–Schwarz, no square root of a Rayleigh quotient, and no
eigenvector**, as §3 itself says twice. Whatever makes `f*` climb `0.125 → 0.812` therefore
**cannot** be the Cheeger sweep, because route (F) does not contain one. The common-cause
reading of §4.5 does not survive contact with the document's own two routes.

`mg-51f4` independently confirms this and puts a floor on the asymmetry: from
`leak(A_k) ≥ γ·k(n−k)/n`, route (F) obeys `f* ≥ ρ_n²γ/2` with
`ρ_n = (n²−1)/(6⌊n²/4⌋) → 2/3` — **a floor that vanishes with `γ` instead of rising toward
`1`**. So (M♯) carries a floor climbing toward `Δ_P` and (F) carries none: **the two routes
do not share a degrading factor at all**, which is the sharpest available statement of why
§4.5's single cause cannot cover both columns.

### 3.5 THE OBJECT THE ARCHITECTURE ACTUALLY CONSUMES IS `min(c♯, f*)`, NOT EITHER COLUMN

Recorded because it bears directly on how §4.5's negative should be read, and because I can
check it on my own instrument. (M♯) and (F) are each **separately sufficient** for
`C₃ = 1` at a poset, so what matters is `c_or(n) = max over primitive of min(c♯, f*)`. My
exact values — **`0.125000, 0.250000, 0.306250, 0.550747, 0.753639`** at `n = 2..6` —
reproduce `mg-51f4`'s independently computed `0.250, 0.306, 0.551, 0.754` and sit
**strictly below both published columns** (`0.943151` and `0.811649` at `n = 6`). §4.5's *"both of my routes are climbing
fast toward the `1` they must stay under"* is true of each column separately and
**overstates the danger to the disjunction**, which is the thing `§8`'s dependency diagram
actually places under `C₃ = 1`. §8 gets this right (*"three independent sufficient
hypotheses"*); §4.5's presentation does not carry it.

---

## §4. ITEM 3 — THE `n = 6` BOUNDARY

**The blanket statements are sound.** §0 and §10 both say, unprompted and before any table,
that exhaustive evidence stops at `n = 6` and that no `n = 7` number is a maximum. Every
`n = 7` table row carries `(sample)`. **Nothing has propagated**: `mg-28ff`, `0.943`,
`0.811`, `0.327508` and `c_true` appear **nowhere** in `STATE.md`, `roadmap.md`, or
`docs/state-of-the-wall.html`, so the `17/78` failure mode — an unscoped figure reaching a
consumer — has **not** occurred here.

**Three defects, all small, all at the same joint.**

1. **§4.3's summary sentence promotes a sample to an enumeration.** Directly under the table
   whose `n = 7` row is a sample: *"**100 % at every enumerated `n`**"*. `n = 7` is
   **sampled, not enumerated**. The commit subject does it unqualified in the permanent git
   record: *"(F) certifies at 100% of primitive posets at **EVERY n = 2..7**"*.
   Suggested repair: *"100 % at every exhaustively enumerated `n` (`n ≤ 6`), and at all 106
   primitive members of the `n = 7` sample."*

2. **§8.1's own scope self-audit is false as written.** It claims *"every `n = 7` row is
   labelled *sample, not a maximum* at each appearance."* Only §4.1's row carries
   *"NOT a maximum"*; §4.2's and §4.3's carry `(sample)` alone. The **self-check written to
   prevent the `17/78` defect is itself inaccurate about its own document** — which is the
   §8.1 pattern applied to §8.1.

3. **§4.2's `n = 7` population is a different sample from §4.1's and §4.3's**, and the
   document does not say so: `b2_census.py:138` draws `sample_posets(7, 90)` (40 primitive)
   while `b1`/`b5` draw `sample_posets(7, 200)` (106 primitive). Both are labelled
   `(sample)`; they are simply not the same sample.

**One thing that is a credit rather than a defect, and I record it because it is the test
that matters:** the `n = 7` sample rows point the *other way* — `c_true` drops to `0.176`
and `c♯` to `0.850` — so if the document had leaned on them they would have **contradicted**
its own "rising" thesis. It does not lean on them. The `n = 7` numbers are carried and not
used, which is the correct handling.

### 4.1 THE `n = 7` SAMPLE HAS NOW BEEN MEASURED AGAINST THE EXHAUSTIVE TRUTH, AND IT WAS WRONG BY A FACTOR OF ~2

While this audit was running, `mg-51f4` enumerated **all 96428 naturally labelled posets on
`[7]`** (86278 primitive) — the first genuine `n = 7` maximum in this lineage. Against
mg-28ff's 106-poset sample:

| `n = 7` | mg-28ff (SAMPLE of 106) | `mg-51f4` (EXHAUSTIVE, 86278 primitive) |
|---|---|---|
| `c_true` | `0.176145` | **`0.340719`** |
| `c♯` | `0.850074` *(40-poset sample)* | **`1.018707`** — over `1` |
| `f*` | `0.832530` | **`1.297074`** — over `1` |

**The sample understated `c_true` by 1.93×, and it understated both route constants across
the `1` boundary.** This does three things to §4 above:

1. **It vindicates mg-28ff's blanket labelling.** §0 and §10 insist, unprompted, that no
   `n = 7` number is a maximum. **They were right, and by a wide margin.** Whatever else is
   true, the document's central scope discipline did its job.
2. **It makes the three labelling defects materially worse, not cosmetic.** A reader who
   took §4.3's *"100 % at every **enumerated** `n`"* at face value would have concluded
   route (F) certifies at every `n ≤ 7`. It **does not** — it fails at 168 of 86278
   primitive posets at `n = 7`. That is exactly the `17/78` failure mode, one population
   over, and it is now demonstrated rather than feared.
3. **It leaves mg-28ff's own thesis intact.** `c_true(7) = 0.340719` gives increment
   `+0.013211` after `+0.019169` — **still strictly decreasing**. So the *"differences are
   shrinking"* claim of §4.1, which §4.5's whole diagnosis rests on, **survives its first
   test at an `n` beyond the evidence that produced it.** Item 1 is confirmed twice over.

**I verified both of `mg-51f4`'s counterexamples on my own exact instrument** rather than
taking them on report (`out_s6_verify_q51f4.txt`), and they reproduce to every digit:

| witness | mine | |
|---|---|---|
| **(M♯) fails**, `rel = [(0,1),(0,2),(0,3),(0,5),(0,6),(1,2),(1,3),(1,5),(1,6),(2,3),(2,6),(4,5),(4,6),(5,6)]` | 19 linear extensions, `Δ_P = 18/19`, `1−λ_std = 0.185485078`, `μ_pref = 0.226537524` (exact copositivity bracket), **`c♯ = 1.018707`** | ✔ |
| **(F) fails**, two antichains `{0,1,2}`, `{3,4,5,6}`, all `a<b` except `(2,3)` | 156 linear extensions, `E[D_F] = 293/39`, `M = 293/936`, **`f* = 1.226627`** | ✔ |

**And the (M♯) witness instantiates consequence (B) exactly as §3.1 requires:** there
`ρ = 1.221325` and `1/Δ_P = 1.055556`, so **`ρ > 1/Δ_P`** — the route dies through the cone
price, as the algebra says it must. At the **(F)** witness `ρ = 1.000000` **exactly** (L2's
first disjunct holds there), so (M♯) is comfortably safe at `c♯ = 0.749259`. The two
failure sets are disjoint **for the reason §3 gives**, checked at the witnesses themselves.

**A further independent confirmation of §6's reading 4.** `mg-51f4` measures `max ρ` over
primitive posets as `1.0000, 1.0854, 1.1412, 1.2176, 1.2762` at `n = 3..7`. My **V00**
column — computed as an exact copositivity bracket, and equal to `ρ` by the algebra of §6 —
reads `1.000000, 1.085410, 1.141242, 1.217605` at `n = 3..6`. **Two instruments, six
decimals, no shared code.** That `V00 = ρ` is confirmed as a measurement and not only as an
identity I derived.

**A precision note on §4.3, in the conservative direction.** `f*` is printed to six decimals
(`0.550750`, `0.811654`), but `b1_footrule.py:77` brackets it with **20 bisection steps over
`[0,4]`** — a bracket `3.8e-6` wide — and the instrument itself printed **five**
(`0.55075`, `0.81165`). The exact values, bracketed here to `1.8e-12`, are **`0.550747`** and
**`0.811649`**. The document quotes the **upper** bracket ends, so it errs toward
over-stating the route's constant, i.e. toward over-stating the danger. Nothing in the
conclusion moves — `19 %` of headroom is `19 %` either way. But the column header says
`EXACT`, and `c_true`'s neighbouring column really is tight to six decimals while this one
is not, so the two read as equally resolved when they are not.

---

## §5. ITEM 5 — THE QUANTIFIER MOVE, AND THE FOUR ARMS THAT COULD HAVE FALSIFIED THE AFFIRMATIVE HALF

The ticket asks: *"If you conclude the affirmative half holds, say what you did that COULD
have falsified it."* Four arms, on my own instrument, each of which prints a counterexample
if the claim is false.

| | arm | result |
|---|---|---|
| **T1** | added step **S2** is an **identity**, not a bound: `Σa_ij(h_i+h_j)² = 2Σd_i h_i² − E(h)` | **48318 / 48318 exact, 0 exceptions.** NC: the discarded `−E(h)` is **strictly positive** at 5906 pairs, so S2 is not decorative. |
| **T2** | **the quantifier move at its only load-bearing joint** — every level set of `h` really is a prefix or a suffix | **65396 / 65396, 0 exceptions**, over both median branches and every candidate median |
| **T3** | **the theorem itself vs brute force**, `Φ*_pref` by exhaustive minimisation over prefixes | **21120 / 21120 (poset, monotone vector) pairs, 0 exceptions.** NC: the **mutated** theorem (`Δ_P → Δ_P/2`) **fails at 260 pairs**, so T3 is not a tautology. |
| **T4** | dropping mg-76b2's `|S| ≤ n/2` clause is free | **36116 / 36116** cuts have `leak(A) = leak(Aᶜ)` |

**The one-use-site claim is TRUE, and I checked it rather than reading it.** In `mg-76b2` §3,
Lemma 3.1's proof uses the minimality of `v` at exactly one place (`R(g) ≤ R(v) = 1−λ_std`)
and is otherwise indifferent to the vector's provenance; Lemma 3.2 is a set identity; L2 is
spent at Lemma 3.3 and the theorem uses Lemma 3.3 once. mg-28ff's §2 uses it once. **There
is no subsidiary use site for the substitution to fail at.**

**The one place mg-28ff's §2 is loose, and it does not bite.** §2 writes *"Every `{h² > t}`
is a level set of `h`, hence of `g`"*. For the `h = (g−m)₋` branch that is inexact: `h` is
**anti**-monotone there, and `{h > s} = {g < m−s}` is a **co**-threshold set of `g`, not a
threshold set. mg-76b2's Lemma 3.3 states **both** directions (*"every threshold set is a
suffix and every co-threshold set is a prefix"*) and its own Lemma 3.1 says so carefully
(*"upward for `g₊`, downward for `g₋`"*), so the conclusion is right. T2 exercises that
branch at **32698** level sets specifically, because a loose sentence at the load-bearing
joint is exactly this programme's recurring bug and reading it was not enough.

---

## §6. ITEM 4 — THE TWO ADDED STEPS: OVER-CLAIMED AT ONE JOINT, UNDER-CLAIMED AT ANOTHER

§2 states:

> *"**Both extra steps are free and both are load-bearing.** Without them the route below
> fails: with the un-sharpened `2Δ_P R(g)` form the constant already exceeds 1 at `n = 5`
> (6 of 275 primitive posets — `b4` R5)."*

Two steps, so **four** bounds — and each of the four has a closed form in `ρ`, `Δ_P` and the
gap, so the 2×2 is exactly computable:

| | S1 (`d_i ≤ Δ_P`) | S2 (evaluate `−E(h)`) | bound on `Φ*²` | constant |
|---|---|---|---|---|
| **V11** | ✔ | ✔ | `R(2Δ_P−R)` | `ρΔ_P − ρ²(1−λ)/2` |
| **V10** | ✔ | ✖ | `2Δ_P R` | `ρΔ_P` ← **the cell R5 tests** |
| **V01** | ✖ | ✔ | `R(2−R)` | `ρ − ρ²(1−λ)/2` ← **untested** |
| **V00** | ✖ | ✖ | `2R` | `ρ` ← mg-76b2's own form |

Measured **exactly** (`μ_pref` by copositivity bisection; a poset is scored FAIL only when
the *lower* bracket end already exceeds `1`, so every count is a lower bound and no failure
is bracket slack):

| `n` | primitive | V11 both | **V10 (S1 only)** | **V01 (S2 only)** | **V00 (neither)** | L2 fails |
|---|---|---|---|---|---|---|
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 4 | 0 | 0 | 0 | 0 | 0 |
| 4 | 27 | 0 | 0 | 0 | **10** | **10** |
| 5 | 275 | 0 | **6** | **0** | **166** | **166** |
| 6 | 4070 | **0** | **192** | **1** | **3164** | **3164** |

maxima at `n = 6`: V11 **`0.943151`**, V10 `1.156724`, V01 `1.028754`, V00 `1.217605`.

**Four readings, and they do not all favour the parent.**

1. **R5 reproduces exactly.** `6 of 275` at `n = 5`, and V10's maximum `1.027118` is
   precisely the `1.027` §9's P4 scores itself against. `[REPRO]` — my dispatch printed both.

2. **V11's maximum reproduces `c♯` exactly at every `n ≥ 3`** — `0.500000, 0.636846,
   0.803289, 0.943151` — on an exact instrument where mg-28ff's is float. And the **L2
   census reproduces exactly**: `0 + 0 + 10 + 166 + 3164 = 3340`, the parent's own number,
   here as an exact consequence of `ρ > 1` rather than a `1e-9` float tolerance.

3. **THE OVER-CLAIM.** R5 tests **V10**, in which `Δ_P` is **kept** and only `−E(h)` is
   discarded. So it establishes that **S2 is load-bearing** and says nothing whatever about
   **S1**. The cell nobody ran, **V01** — keep `−E(h)`, discard `Δ_P` — has **0 failures at
   `n ≤ 5`** and first fails at **`n = 6`, at 1 poset of 4070**.
   So the sentence *"both are load-bearing"* is **true**, but:
   * at the `n` where §2 makes its claim (`n = 5`), **S1 is not load-bearing at all**;
   * the two steps are **wildly unequal** — dropping S2 costs `6` then `192` posets;
     dropping S1 costs `0` then `1`;
   * and the evidence cited (`b4` R5) **cannot** support the S1 half, because R5 keeps S1.

   *"Both are free"* is right, *"both are load-bearing"* is right at `n = 6`, and
   *"**and I measured it**"* is right for one of the two. The repair is one clause, not a
   retraction — see §4's suggested text.

4. **THE UNDER-CLAIM, and it is larger than the over-claim.** **`V00 = ρ` exactly.** So
   mg-76b2's own un-sharpened sweep, applied to a monotone vector, certifies `C₃ = 1` at a
   poset **if and only if `ρ ≤ 1`, i.e. if and only if L2's first disjunct holds there.**
   The measurement confirms it exactly: V00's failure count **equals the L2-failure count at
   every `n`** (`0, 0, 10, 166, 3164`). **Without the two steps the quantifier move buys
   literally nothing — the L2-free route collapses back onto L2 itself.** That is a far
   stronger justification for the two steps than *"the constant exceeds 1 at `n = 5`"*, and
   it moves the first failure from `n = 5` to **`n = 4`**. mg-28ff **understates its own
   result**, and this is the one place where correcting it makes the parent stronger.

### 6.1 A SECOND DEFECT AT THE SAME JOINT: **(M♯) AS STATED DROPS THE THEOREM'S SECOND BRANCH**

§2's **theorem** has two cases — `R(g)(2Δ_P − R(g))` when `R(g) ≤ Δ_P`, and `Δ_P²`
otherwise. §2's **hypothesis (M♯)** and §4.2's **`c♯` formula** have one:

> **(M♯)** `μ_pref (2Δ_P − μ_pref) ≤ 2(1 − λ_std)`  •  `c♯(P) = μ_pref(2Δ_P − μ_pref)/(2(1−λ_std))`

Since `t ↦ t(2Δ−t)` is **decreasing** for `t > Δ`, the one-case form **understates** what
the theorem delivers when `μ_pref > Δ_P`: the truth there is `Δ_P²`, and
`μ(2Δ−μ) < Δ_P²`. **So (M♯) as written can hold at a poset where the theorem does not
deliver `C₃ = 1`.** As a *stated sufficient condition* it is unsound in that regime.

**It does not bite on this population, and the instrument was never wrong.** Re-running the
whole `n ≤ 6` sweep with the branch restored (`out_s5_branch.txt`): `μ_pref > Δ_P` at
exactly **one poset per `n`**, and the branched maximum differs from the one-case maximum
**only at `n = 2`** (`0.125000` branched vs `0.000000` one-case). At `n = 3..6` both give
`0.500000, 0.636846, 0.803289, 0.943151` — mg-28ff's published column exactly. And
mg-28ff's `c♯(2)` **is** `0.125000`, i.e. **its code implements the branch its document
omits**. So: a real unsoundness in the *stated* hypothesis, **zero effect on any published
number above `n = 2`**, and no effect at all on the instrument. It should be repaired as
prose (R3 in §6.5), not treated as a result being withdrawn.

**This is a documentation defect, and I found it by shipping it myself.** My own `s3`
implemented (M♯) exactly as §2 and §4.2 state it, one case, and produced `c♯(2) = 0.000000`
against the parent's `0.125000`. Chasing my own disagreement with the parent is what
surfaced the branch — I audited a formula-versus-theorem mismatch and committed the same one.
It is recorded in `code/l2_audit_29fe/README.md` as D4.

---

## §6.5. SUGGESTED REPAIRS — five clauses, no figure withdrawn

Per the standing scope guard (*"do not delete contested figures — qualify them"*), every
repair below **adds** scope or a clause. Nothing is struck. These are **proposals for
whoever owns `docs/OneThird-L2-Conditionality-mg-28ff.md`**; I have landed none of them.

| # | site | current | suggested |
|---|---|---|---|
| **R1** | §4.5 bullet 3 | *"It is in the **Cheeger sweep as an instrument** … Anyone attacking this next should attack the sweep, not the poset."* | *"It is in **two** places, and they behave differently. The sweep's own loss — isolated as `Δ_P − (1−λ_std)/2`, the constant this route yields when the cone price is off — climbs `0.500 → 0.825`, but is **bounded by `Δ_P < 1` at every `n`**, so the sweep alone can never carry the route past `1`. What can is `ρ = μ_pref/(1−λ_std)`, the price of the quantifier move, which is `1` at `n ≤ 4` and `14 %` of `c♯` at `n = 6`. **A successor must measure `ρ`; attacking the sweep lowers the constant but cannot save the route.**"* |
| **R2** | §4.5, and §3's framing | uses the rise of **both** columns as joint evidence for one cause | add: *"Route (F) contains no Cheeger sweep — no Cauchy–Schwarz, no square root of a Rayleigh quotient — so its rise has a different cause and is not evidence for this one."* |
| **R3** | §2 and §4.2 | **(M♯)** and `c♯` stated in one case | add the theorem's second branch: *"…and `Δ_P² ≤ 2(1−λ_std)` when `μ_pref > Δ_P`."* The instrument already does this; only the prose omits it. |
| **R4** | §2 | *"Both extra steps are free and both are load-bearing. Without them … `2Δ_P R(g)` … exceeds 1 at `n = 5` (6 of 275)."* | *"Both are free. **They are load-bearing very unequally, and R5 measures only one of them**: R5 discards `−E(h)` while keeping `Δ_P`, so it shows **S2** is load-bearing (`6 of 275` at `n = 5`, `192 of 4070` at `n = 6`). Discarding `Δ_P` while keeping `−E(h)` first fails at **`n = 6`, at 1 poset of 4070**. And **discarding both** leaves `c = ρ`, which is `≤ 1` **exactly** at the L2-exhibiting posets — so without the two steps the quantifier move buys nothing at all, failing from `n = 4` at `10, 166, 3164`, the L2-failure counts themselves."* |
| **R5** | §4.3 summary; commit subject | *"100 % at every **enumerated** `n`"* / *"EVERY n = 2..7"* | *"100 % at every exhaustively enumerated `n` (`n ≤ 6`), and at all 106 primitive members of the `n = 7` **sample**."* |
| **R6** | §8.1 item 3 | *"every `n = 7` row is labelled *sample, not a maximum* at each appearance"* | true only of §4.1's row; either label §4.2's and §4.3's the same way, or weaken the sentence to *"every `n = 7` row is labelled `(sample)`, and §4.1's additionally as not-a-maximum."* |
| **R7** | §4.3 | `f*` printed to 6 d.p. under a column headed `EXACT` | the bracket is `3.8e-6` wide (`b1_footrule.py:77`, 20 steps over `[0,4]`) and the instrument printed 5 d.p. Either print 5, or re-run at more steps: the exact values are **`0.550747`** and **`0.811649`** (confirmed independently by `mg-51f4`). |

---

## §7. WHAT WOULD CHANGE MY VERDICT

* **Resolved while this was written:** V01 *does* exceed `1` at `n = 6`, at **1 poset of
  4070**. So S1 is load-bearing from `n = 6`, mg-28ff's sentence is **true**, and my finding
  narrows to what it should be — **R5 is not evidence for the S1 half, and the two halves
  are unequal by two orders of magnitude** (`192` vs `1` at `n = 6`). It does not touch §3.
* If someone exhibits a poset with `Δ_P > 1`, §3 collapses. `Δ_P = max_i Pr[pos(i) ≠ i]`, so
  this cannot happen; I state it because §3 rests on it entirely.
* If the exhaustive `n = 7` figures I quote from `mg-51f4` in §4.1 are wrong, §4.1's
  upgrade falls (though §4's three labelling defects stand regardless — they are textual).
  I verified its two **counterexamples** exactly on my own instrument; I did **not**
  re-enumerate its 86278-poset population, and I say so rather than implying I did.
* If `μ_pref` were *not* the right cone minimum — e.g. if the monotone cone were **not**
  the nonneg span of `ψ_k` — then `ρ` is not what I say it is. Arm A7 checks both directions
  of that on my own basis, and A6a/A6b check `Q`, `N` and `Q_kk = leak(A_k)` against their
  definitions at 5230 posets.

---

## §8. PREDICTIONS SCORED

`PREDICTIONS.md` at `d7ccc1f`, before the parent's document or code were opened.

| | bet | outcome |
|---|---|---|
| P1 (0.30) | the increment sequence has an arithmetic slip | **LOST** — and rightly. §2. |
| **P1b (0.55)** | the last increment is `.020`, not `.019` | **LOST.** `0.019169` rounds to `.019`. What I got right for the wrong reason: the `.020` reading *is* what you get from the ticket's own 3-d.p. restatement, which is where the ticket's suspicion came from — but mg-28ff's table is not what is wrong. |
| P2 (0.45) | "four points is not a trend" is a fair hit but not the dispatch's version | **HELD in part.** The deltas *are* decreasing, so the inversion scenario does not fire, as predicted. My named alternative (the columns coincide at the left end) is real but trivial. |
| **P3 (0.60) — principal live bet** | the diagnosis is **under-separated**; `Δ_P` rises and supplies part of the divergence for free | **HELD, and for the reason given.** `max Δ_P` rises `0.667 → 0.950` and is most of `c_sweepL2`'s climb. My pre-registered falsifier — *"score P3 LOST if max `Δ_P` is flat within 0.02"* — did not fire. But the **important** half of §3 is one I did **not** predict: that `Δ_P ≤ 1` caps the sweep below `1` forever and hands the whole failure channel to `ρ`. I found that after measuring, not before. |
| P4 (0.35) | an `n = 7` figure is used as if exhaustive | **HELD, narrowly** — §4.3's *"every enumerated `n`"* and the commit subject's *"EVERY n = 2..7"*. §4. |
| **P5 (0.50)** | only **one** of the two steps is load-bearing at `n = 5`, and the commit sells both off a single joint counterfactual | **HELD, exactly as filed.** §6. This is the prediction I am most pleased with, because the guard I bound to it in advance ("I must run the 2×2") is the only reason I ran the cell nobody had run. |
| P6 (0.35) | the quantifier move has a second, unchecked use site | **LOST.** There is exactly one use site and mg-28ff's claim is right. It rests on a *reading*, and I converted it to a machine check (T2, 65396 level sets) rather than leaving it as one. |
| P7 (0.70) | the affirmative half holds | **HELD**, against four falsification arms (§5), with the falsifiers named in advance. |
| P8 (0.20) | I find a defect that invalidates `mg-51f4`'s scoping | **HALF-HELD, and I score it conservatively.** §3 does not void mg-51f4 — it under-scopes it, exactly as I predicted at 0.20 ("more likely to REFINE than to void"). Mailed to `q51f4` and `pm-onethird` ~35 minutes in, before this document existed. |

**Errors of my own — E1–E8 as filed.** **E5 held** (`lib28ff.py` was not opened until every
number here existed, and opening it afterwards is what explained the `f*` gap). **D1 and D2
in `code/l2_audit_29fe/README.md` are two defects the guards caught**: a negative control
that could never have fired, and a finding about §4.2's `n = 7` sample size that was **my
misreading and would have been a false accusation** had my own "quote it from the document
first" guard not stopped it. **E7 honoured**: every maximum here is labelled a maximum over
an enumerated finite population. **E8 honoured**: I qualified figures and withdrew none.

---

## §8.5. WHAT IS `mg-51f4`'s AND NOT MINE

Filed explicitly, because this audit ran concurrently with the successor it is partly about
and the two exchanged mail four times.

* **Consequence (A) — the floor `c♯ ≥ Δ_P − γ/2` — is `mg-51f4`'s**, committed pre-run at
  `01c206f`, `20:24:09Z`, 33 minutes before my mail. Mine is the same object written with
  the quantifier price `ρ` left in.
* **The pointwise-argmax correction in §3.2 is `mg-51f4`'s**, and it corrects an error in
  my first statement of the finding.
* **The exhaustive `n = 7` population, `c_or`, the `γ`-binned table and both
  counterexamples are `mg-51f4`'s.** I verified the two counterexamples exactly (§4.1); I
  did **not** re-enumerate 86278 posets and do not claim that population as audited.
* **Mine are:** the `ρ`-identity and consequence **(B)** in the form *"`c♯ > 1` requires
  `ρ > 1/Δ_P`, so the sweep alone can never break the route"*; the 2×2 counterfactual and
  the `V00 = ρ` reading (§6); the second-branch defect in (M♯) (§6.1); the four
  falsification arms (§5); and the three `n = 7` labelling defects plus the `f*` precision
  cause (§4).
* **`mg-51f4`'s own conclusion, which I record because it bears on why this audit was
  filed:** its scoping instruction — *file against the pair, not against either route* —
  was **right**, and it is why `c_or` exists at all, even though the sentence attached to
  it (§4.5's single cause) was wrong. **The mis-diagnosis I found did not waste the
  successor's effort.** That is worth saying plainly: my §3 corrects a sentence, not a
  ticket.

---

## §9. NOT DONE

* **The affirmative half was confirmed, not re-certified poset-by-poset.** I did not
  re-exhibit 4377 rational witness vectors; I re-derived `c_true` exactly (which bounds the
  truth route-independently) and attacked the **theorem** they are certificates for (§5).
  A defect in an individual witness would not show up here.
* **No `n = 8`, no exhaustive `n = 7`.**
* **L2, `ε₀`, L4, and every chain constant untouched**, as the ticket instructs.
* **The `1032` vs `1037` discrepancy is left exactly where mg-28ff left it.**
* **`μ_pref`'s *lower* use is now exact** where mg-28ff's was float — but only to `n ≤ 5`
  in the counterfactual table; the `n = 6` cone row is §6.1.
* **I edited no other document.** §4's three suggested repairs to
  `docs/OneThird-L2-Conditionality-mg-28ff.md` and §3's re-diagnosis are **proposals for
  whoever owns that document**, not landings.

---

*`mg-29fe`. Instrument: `code/l2_audit_29fe/` — `lib29fe.py` written from the corpus's
definitions with `lib28ff.py` unopened until every number above existed; `selftest29fe.py`
**26/26 arms**, including a PSD path deliberately different from the parent's (whose
Faddeev–LeVerrier sign error its own E3 records) and one negative control rebuilt after it
proved incapable of firing.*
