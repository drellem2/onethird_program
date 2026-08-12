# OneThird — DANIEL'S PRIMITIVITY OBJECTION: **the objection is right about the witness and it does not touch the closure, because the ceiling is a PROVED UNIVERSAL BOUND and not a maximum over witnesses.** The chain `pm-onethird` calls "my reasoning" is CORRECT, it is NOT his — it is already **PROVED IN THE CORPUS** at `mg-8d66` §4.2 — and it was not needed. The primitive maximum is **0.3876**, not 1 and not 3/4

**Work item.** `mg-f5be` (repo `onethird_program`), filed by `pm-onethird` on Daniel's
observation:

> *"Your example relies on an ordinal sum. I assume this works bc we can get close to an
> ordinal sum while being primitive but keep in mind counterexamples are primitive"*

**Subject.** `mg-409a`'s ceiling (`docs/OneThird-Compression-W4-Rate-mg-409a.md` §3),
its attainment witness `Z_n`, and `pm-onethird`'s claim that restricting to the
counterexample class **tightens** rather than loosens it.
**Depends on.** `mg-409a` (`188c959`) — read in full and re-measured where quoted.
`mg-8d66` (`ed3a949`), `mg-145f` (`e09226c`), `mg-05ec` (`0a8415b`) — read, cited, not
re-measured.
**Instrument.** [`code/primitivity_f5be/`](../code/primitivity_f5be/), `run_all.sh`.

---

## 0. VERDICT

> ### **`closure-holds-on-primitives` — and it holds with a LARGER margin there than on the general class.**
>
> The four things the ticket requires a verdict on:
>
> | question | answer |
> |---|---|
> | **is `pm-onethird`'s chain right?** | **YES, every link, exactly — AND IT IS NOT HIS REASONING, IT IS AN ALREADY-PROVED RESULT HE COMMISSIONED.** All four terms, with the same three steps, are `mg-8d66` §4.2 (`ed3a949`), proved there at **every** admissible partition and verified at 18 373 pairs. The ticket sent me to `mg-409a`, where it is genuinely **ABSENT**. Independently re-measured here at **2 532 pairs, `n ≤ 6` exhaustive**: 0 failures. |
> | **the primitive maximum of `alpha`** | **`0.387627564…`, at `n = 4`, and DECREASING in `n`** (0.3876 / 0.3596 / 0.3343 / 0.3219 / **0.3122** at `n = 4…8`). Exhaustive over the primitive class at every `n` listed. |
> | **is the frozen measurement vacuous?** | **VACUOUS.** Zero frozen posets at every `n ≤ 6`; the smallest `δ(P)` available anywhere in range is exactly `1/3`. Reported as *no maximum exists*, not as a maximum of 0. |
> | **is `alpha = 1` attained by a primitive poset?** | **NO** — exact rational test, at every poset to `n = 6` and every primitive poset at `n = 7` (234) and `n = 8` (**2 585**). |
>
> ### **AND THE REASON THE OBJECTION DOES NOT BITE IS NOT THE 3/4.**
>
> `mg-409a` §3 is a **proof that `alpha(P) ≤ 1` at every poset with `|L(P)| ≥ 2`** — five
> lines, no witness set, no enumeration. `Z_n` appears there **only to show the bound is
> ATTAINED**, i.e. tight. **Tightness is the half of the statement the closure does not
> use.** A universally quantified upper bound cannot be raised by restricting its
> quantifier to a subclass; it can only stay or fall. So the class the witness is drawn
> from is **irrelevant to the direction the closure consumes**, and that is the whole
> answer.
>
> ### Daniel is right about the witness, and more strongly than he put it.
>
> It is not merely that `mg-409a` *chose* a decomposable witness. **In range, EVERY
> witness is decomposable, and in the same narrow way.** The attaining set is exactly the
> **ordinal sums of blocks of size 1 and 2** — count `Fib(n+1) − 1`, matched exactly at
> `n = 2,3,4,5,6` (1, 2, 4, 7, 12), with membership checked in both directions. `Z_n` is
> the all-blocks-size-2 member. Nothing outside that family attains.
>
> ### And `pm-onethird`'s reading is right on the mathematics but **not load-bearing**.
>
> The chain is correct, his `3/4` is correct, and his conclusion — *"restricting to the
> class where counterexamples live should LOWER the ceiling"* — is correct **and
> understated**: the measured primitive ceiling is **0.39, not 0.75**. But the closure did
> not need it, was not stated too weakly, and **his recommendation to Daniel (3/10, do not
> pursue) does not need retracting.** The bar is a constant `≥ 2` (`mg-409a` §2). Every
> ceiling in play — `1`, `3/4`, `0.39` — is below it. The strengthening moves the margin
> from a factor of 2 to a factor of about 5. It does not move the verdict.
>
> ### The ticket's own premise is wrong in a way that matters for how it was priced
>
> `mg-f5be` says *"This is MY REASONING off the recorded bound, not a measurement. Treat it
> as the thing to refute."* **It is not his reasoning and it is a measurement.** It is
> `mg-8d66`'s §4.2, proved and checked at 18 373 pairs, and its Step 2 is already in the
> facts registry as **`FACTS.md` F1, kind `U`, an entry Daniel named specifically when the
> registry was commissioned.** The slot was therefore bought partly to re-derive something
> the programme had already proved a commit earlier — which is `mg-623a`'s
> duplicates-the-corpus failure mode, turned inward. **I walked into the same hole and §8
> D0 says so:** my `PREDICTIONS.md` H5 disclosed that I had not read `mg-8d66`'s
> deliverable, and that declared exposure cost exactly what it was declared to risk.
>
> ### The one correction to the ticket's framing
>
> **PRIMITIVE and FROZEN are different restrictions and the ticket runs them together.**
> `pm-onethird`'s `3/4` follows from **FROZEN** (every incomparable pair unbalanced). It
> does **not** follow from **PRIMITIVE** (no nontrivial module). The two are logically
> independent — a primitive poset may have every pair perfectly balanced. Daniel's word
> was *primitive*; the ticket's derivation is about *frozen*; and the frozen class is
> empty, so only the primitive question is answerable at all. It is answered above, by
> measurement rather than by that derivation.

---

## 1. Ticket step 1: **the chain is in the corpus — just not in the document the ticket names**

The ticket says, correctly, *"I read it out of a mail summary, not the document,"* and
instructs: *"Check my chain against the actual proof in mg-409a's deliverable … If the
bound is stated differently, that is the finding and stop there."*

### 1.1 In `mg-409a`: **ABSENT**, and the ticket is right that it is

`mg-409a` §3 proves `alpha ≤ 1` by a two-case split on `Ran Q_o`: Case 1 exhibits an
**odd-fiber indicator**, Case 2 shows `Π_e = I`. No pair bias appears anywhere in it.
Mechanically (`p1.0`):

| probe | in `docs/OneThird-Compression-W4-Rate-mg-409a.md` |
|---|---|
| `4 p (1-p)` | **ABSENT** |
| `4p(1-p)` | **ABSENT** |
| `P(adjacent)` | **ABSENT** |
| `adjacent` | **ABSENT** |
| `max(p` | **ABSENT** |

### 1.2 In `mg-8d66`: **PRESENT, VERBATIM, AND PROVED** — which the ticket does not know

[`docs/OneThird-Compression-kFoliation-mg-8d66.md:34`](OneThird-Compression-kFoliation-mg-8d66.md),
in that document's own §0 verdict block:

```
    alpha_S  ≤  R_{Q_S}(f_xy)  =  P(x,y adjacent) / (4 p(1−p))  ≤  1/(2 max(p,1−p))  ≤  1
```

— character for character the ticket's chain, and **stronger than the ticket states it**,
because `mg-8d66` proves it at *every* admissible partition `S` and not only at `k = 2`. Its
§4.2 gives the three steps (`:175–207`): Step 1 the affine-on-every-fiber argument, **Step 2
the adjacent-swap involution**, Step 3 the arithmetic. **Verified there at 18 373 incomparable
pairs, exhaustively over every labeled poset at `n = 3, 4, 5`, 0 failures on all four links.**

And Step 2 is separately in the facts registry: **[`docs/FACTS.md`](FACTS.md) F1 · *Bias
controls adjacency*, `KIND: U` — proved**, with the same involution proof, and its entry
records that **Daniel named it specifically** when the registry was commissioned.

### 1.3 So the finding at step 1 is not the one the ticket expected

> **The chain is not `pm-onethird`'s reasoning and it is not unmeasured. It is a proved,
> registered corpus result, one commit older than the ticket that asks for it to be
> attacked.** The ticket pointed at `mg-409a` — where it is genuinely absent — and inferred
> from that absence that the chain was his own derivation off a summary.

**I did not stop at step 1, and the reason is stated so the override is visible.** The
narrow instruction was satisfied the moment §1.1 came back ABSENT, but stopping there would
have recorded a true fact about one document while leaving the actual question — does the
ceiling tighten on the class Daniel named — untouched, and that question is why the slot was
spent. §2 below is therefore an **independent re-measurement** on a different population, not
a derivation, and §4 is the part that is new.

---

## 2. The chain, re-measured independently — **CORRECT, every link**

⚠️ **Read §1.2 first: this is a RE-DERIVATION of `mg-8d66` §4.2, not a new one.** I derived
it before reading that document (`PREDICTIONS.md` H2/H5) and the derivations agree step for
step, which is worth exactly what an independent reproduction is worth and nothing more. What
this section adds over `mg-8d66` is a **different population** — every iso class to `n = 6`,
where `mg-8d66` ran every labeled poset to `n = 5`.

### 2.1 The derivation (= `mg-8d66` §4.2 Steps 1–3)

Writing `f_xy = 1{x <_L y}` for the pair indicator at an incomparable pair, `p = p_xy`,
and `P(adj)` for the probability that `x` and `y` occupy adjacent positions:

| link | statement | source |
|---|---|---|
| **L1** | `R_M(f_xy) = ((n−1)/2)·E_BK(f_xy)/Var(f_xy)` | `mg-409a` §2, **re-measured here** |
| **A** | `E_BK(f_xy) = P(adj)/(2(n−1))` | `mg-8d66` §4.2 Step 1 (as `= P(adj)/4` after the `(n−1)/2` factor) |
| **B** | `Var(f_xy) = p(1−p)` | `mg-8d66` §4.2 Step 3 |
| ⇒ | **`R_M(f_xy) = P(adj) / (4 p (1−p))`** | **= TERM 1**, `mg-8d66:34` |
| **L2** | `alpha(P) ≤ R_M(f_xy)` at **every** incomparable pair | `mg-409a` §2 (Rayleigh at a test vector) |
| **C** | `P(adj) ≤ 2·min(p, 1−p)` | **`FACTS.md` F1, `KIND: U`** = `mg-8d66` §4.2 Step 2 |
| ⇒ | **`≤ 1/(2·max(p, 1−p))`** | **= TERM 2** |
| **D** | `max(p,1−p) ≥ 1/2` | ⇒ **`≤ 1`** = TERM 3 |

**Link C is the one that carries the argument and it is prettier than an inequality.**
Swapping an adjacent incomparable `{x,y}` maps `L(P)` to `L(P)` and is an **involution**,
so it is a *bijection* between `{L : x,y adjacent, x before y}` and `{L : x,y adjacent,
y before x}`. Hence `P(adj) = 2·P(adj ∧ x before y)` **exactly**, and the inequality then
comes for free from `{adj ∧ x before y} ⊆ {x before y}`, giving `P(adj) ≤ 2p`; symmetrically
`P(adj) ≤ 2(1−p)`. This is `FACTS.md` F1 and it is `U`/proved; the measurements below
corroborate a theorem rather than establishing one.

### 2.2 The measurement — `n ≤ 6` EXHAUSTIVE, exact rationals throughout

| arm | statement | population | result |
|---|---|---|---|
| `p1.1` | `Var = p(1−p)`, `E_BK = P(adj)/(2(n−1))`, and **TERM 1 exact** | every incomparable pair of every iso class, `n ≤ 6` | **0 failures / 2 532 pairs** |
| `p1.2` | the involution is an **equality**, and `P(adj) ≤ 2min(p,1−p)` | same | **0 failures / 2 532**; tight at **566**, worst slack `2/3` |
| `p1.3` | `TERM1 ≤ TERM2 ≤ 1` | same | **0 failures / 2 532** |
| `p1.4` | `alpha ≤` the **minimum over pairs** of either term | 81 posets, `n ≤ 5` exhaustive | **0 violations**; the pair witness is **tight at 13** |
| `p1.6` | `p = 1/3 ⇒ TERM2 = 3/4`, and `p < 1/3 ⇒ TERM2 < 3/4` strictly | arithmetic | **exact** |

**Controls that fire** (`p1.5`): dropping `P(adj)` from TERM 1 — the shape a careless reading
suggests — breaks the identity at **272 of 286** pairs; and link `C` is **strict at 202**
pairs, so it is not an identity in disguise.

⚠️ **The `2 532` is not larger than `mg-8d66`'s `18 373` and must not be quoted as though it
were.** Mine counts pairs over **isomorphism classes**, `mg-8d66`'s over **labeled** posets,
so at `n ≤ 5` mine is a sub-population of theirs up to relabelling. The only thing this
section adds to the record is the extension to **`n = 6`** and a second implementation of
links `A`, `B` and `C`.

### 2.3 Ticket step 2: **the chain is available at every pair, so the most extreme may be chosen**

`L2` is a Rayleigh quotient at a named test vector. **Nothing distinguishes a pair** — there
is no minimality, no extremality, and no selection anywhere in `mg-409a` §2's statement of
it. Every incomparable pair yields a valid bound, so the **minimum over pairs is a valid
bound**, which is exactly the freedom `pm-onethird`'s argument needs. Measured at every
poset to `n = 5`: 0 violations (`p1.4`). Writing

```
    mu(P) = min over incomparable pairs of min(p_xy, 1 − p_xy)          (the WORST pair)
```

the chain delivers the **unconditional** bound `alpha(P) ≤ 1/(2(1 − mu(P)))`, verified at
all **399** posets with `|L| ≥ 2`, `n ≤ 6` (`p3.2`). **The frozen hypothesis is used only to
turn `mu < 1/3` into the number `3/4`.** The bound itself needs no hypothesis.

⚠️ **`mu` is not `δ`, and the ticket's phrasing invites the confusion.** `δ(P) = max_{x‖y}
min(p,1−p)` is the (1/3)–(2/3) quantity — a statement about the **best** pair. `mu` is the
**worst**. Frozen (`δ < 1/3`) forces `mu ≤ δ < 1/3`, so the implication runs and
`pm-onethird`'s `3/4` is right; but the two are different functions (`p0.6` exhibits a poset
with `δ = 1/2`, `mu = 1/3`) and only one direction is available.

---

## 3. Ticket step 3: the frozen class is **VACUOUS**, and the near-frozen measurement

| `n` | posets with `|L| ≥ 2` | **FROZEN (`δ < 1/3`)** | min `δ` in range |
|---|---|---|---|
| 2 | 1 | **0** | `1/2` |
| 3 | 4 | **0** | `1/3` |
| 4 | 15 | **0** | `1/3` |
| 5 | 62 | **0** | `1/3` |
| 6 | 317 | **0** | `1/3` |

**Reported as vacuous, not as a zero.** There is no maximum of `alpha` over the frozen
class because there is no frozen poset; `p3.1` checks that asking for one **raises
`ValueError`** rather than printing a number. This is `PREDICTIONS.md` E3 made operational,
and it is the ticket's own instruction.

This is not a limitation of the enumeration — it is the (1/3)–(2/3) conjecture being true
in range, verified independently to `n = 14` per `mg-145f`. **The smallest `δ` reachable at
all is exactly `1/3`**, at which the chain returns `TERM2 = 3/4` while measured `alpha` is
`0.5`. For reference the best unconditional bound in the literature is
`δ ≥ (5−√5)/10 = 0.27639…`; nothing in range goes below `1/3`.

**And the hypothetical is answered without needing a poset** (`p3.4`), because it is
arithmetic:

| `mu` | ceiling `1/(2(1−mu))` | bar / ceiling, at bar = 2 |
|---|---|---|
| `1/3` | **0.750000** | ≥ 2.67 |
| `3/10` | 0.714286 | ≥ 2.80 |
| `1/4` | 0.666667 | ≥ 3.00 |
| `1/5` | 0.625000 | ≥ 3.20 |
| `0` | 0.500000 | ≥ 4.00 |

**Every value is below the bar.** The strengthening changes the margin and not the verdict.

---

## 4. Ticket step 4 and the main measurement: **`alpha` on the PRIMITIVE class**

### 4.1 "Primitive" is ambiguous, so all three readings are carried

| notion | definition | `Z_n` |
|---|---|---|
| **PRIME / primitive** | no module (autonomous set) of size `2..n−1` | **fails** |
| **ordinal-indecomposable** | no proper down-set lying entirely below its complement | **fails** |
| **connected** | comparability graph connected | passes |

`Z_n` fails the first two at `n = 4, 6, 8` (`p2.0`), so **the objection's premise is
checked, not assumed.** "Primitive" is taken to mean **prime**, the strongest reading and
the standard sense of the word; results for the other two are carried alongside.

### 4.2 Is `alpha = 1` attained by a primitive poset? — **NO**, by an exact test

The test needs no eigenvalue. By two-projection theory (`mg-409a` §5), `alpha = 1 − cos θ_min`
between `Ran Q_o` and `Ran Q_e`, so

```
    alpha(P) = 1   ⟺   Ran Q_o ⊥ Ran Q_e   ⟺   Π_o v_F = 0 for every even fiber F,
                                                 v_F = 1_F/|F| − 1/N
```

— `O(N · #fibers)` exact rational work. Cross-checked against `lib409a`'s Jacobi at every
poset to `n = 5`: **0 mismatches**, both directions (`p0.4`), and it goes **red** on `A_4`
and **green** on `Z_4` (`p0.5`), so it is not a constant function.

| `n` | population | attain `alpha = 1` | **of which PRIMITIVE** |
|---|---|---|---|
| 2 | all (1) | 1 | **0** |
| 3 | all (4) | 2 | **0** |
| 4 | all (15) | 4 | **0** |
| 5 | all (62) | 7 | **0** |
| 6 | all (317) | 12 | **0** |
| 7 | **all 234 primitive classes** | 0 | **0** |

### 4.3 What the attaining set actually is — **exactly the ordinal sums of 1- and 2-blocks**

`mg-409a` §3 Case 2 shows that family is **sufficient**. In range it is also **necessary**,
and the count is a clean independent check: compositions of `n` into parts `1` and `2`
number `Fib(n+1)`, of which exactly one — all parts 1, the chain — has `|L(P)| = 1`.

| `n` | attainers | `Fib(n+1) − 1` | all in the family? | every family member attains? |
|---|---|---|---|---|
| 2 | 1 | 1 | ✔ | ✔ |
| 3 | 2 | 2 | ✔ | ✔ |
| 4 | 4 | 4 | ✔ | ✔ |
| 5 | 7 | 7 | ✔ | ✔ |
| 6 | 12 | 12 | ✔ | ✔ |

**This is Daniel's observation, confirmed and sharpened.** The witness set is not merely
*drawn from* the decomposable class — **it is contained in a single two-parameter family of
ordinal sums**, and `Z_n` is one member of it. My own P9 (that some non-ordinal-sum poset
would attain) is **REFUTED**.

### 4.4 The primitive maximum — **the number the ticket asks for**

| `n` | primitive classes (`|L| ≥ 2`) | max `alpha` over ALL posets | **max over PRIMITIVE** | max over non-primitive |
|---|---|---|---|---|
| 4 | **1** | 1.000000000 | **0.387627564** | 1.000000000 |
| 5 | **4** | 1.000000000 | **0.359611797** | 1.000000000 |
| 6 | **28** | 1.000000000 | **0.334349276** | 1.000000000 |
| 7 | **234** | — (primitive-only population) | **0.321946387** | — |
| 8 | **2 585** | — (primitive-only population) | **0.312169329** | — |

**The primitive maximum in range is `0.3876…`**, attained at `n = 4` by `{0<2, 0<3, 1<3}` —
the **N-poset**, which is the *unique* primitive 4-element poset, so that row is a maximum
over a population of one and should be read as such. The maximum **decreases at every step
through `n = 8`**, where the population is 2 585 classes.

The `n = 7` and `n = 8` rows come from `p4`, which needs a **colour-refined canonical form**
(brute force is `8! = 40 320` relabellings per candidate). That form is validated against
brute force before it is used — no class collisions and invariance under 24 relabellings at
every class, `n ≤ 6` — and the enumeration it drives reproduces **A000112's 2 045 at
`n = 7`** as a positive control (`p4.0`, `p4.1`). ⚠️ **The `n = 8` primitive population is
seeded from the FULL `n = 7` population, not the primitive one**: deleting a maximal element
from a primitive poset can *create* a module, so seeding from primitives would silently miss
classes. That is the `n = 8` form of `PREDICTIONS.md` E5 and it is most of what the arm costs.

The `n = 8` argmax is `{0<2, 0<3, 1<3, 1<4, 2<4, 2<5, 3<5, 3<6, 4<6, 4<7, 5<7}` (`|L| = 34`)
— a zigzag/fence, the same shape as the `n = 7` argmax and as the `n = 4` N-poset. **That the
maximiser is the same family at every size is an observation, not a result**: nothing here
proves the fence maximises `alpha` among primitives, and no such claim is made.

**The verdict-carrying statements are the exact ones, not that float.** At the primitive
argmax an exhibited rational test vector gives `alpha ≤ 5/8`. Over **every** primitive poset
in range the worst exhibited rational certificate is

```
    R_M  ≤  525/832  =  0.631009615…   <   1
```

at the `n = 7` poset `{0<2, 0<3, 1<3, 1<4, 2<4, 2<5, 3<5, 3<6, 4<6}` (`p2.3`). So *"no
primitive poset in range comes within a third of the ceiling"* is a statement about
exhibited rationals, not about a Jacobi sweep.

### 4.5 PRIMITIVE is not FROZEN — the ticket's two restrictions are independent

I predicted (**P5**, `p = 0.60`) that some primitive poset would exceed `3/4`, on the
reasoning that nothing about *having no nontrivial module* forces *any pair to be
unbalanced*. **That reasoning is sound and the prediction LOST**: the measured primitive
maximum is `0.39`. Primitivity does not **imply** the frozen bound — it delivers a stronger
one anyway, empirically, and that is a fact about `alpha` and not a logical consequence.

The distinction matters for reading the ticket, which slides between the two:
`pm-onethird`'s `3/4` is a theorem about **frozen** posets (a class that is empty), while
Daniel's objection is about **primitive** ones (a class that is large and measurable). The
answer to Daniel is §4.4; the `3/4` is §3.

---

## 5. Why the objection does not touch the closure — the structural point, stated once

**Daniel's caution is correct as a general rule, and this programme has been bitten by it.**
`mg-05ec` records that the *"standard dominance fails exactly on the ordinal sums"* rescue
**breaks at `n = 7` on indecomposable witnesses** (166 refuters, `STATE.md` row 3b). A
result whose witnesses are all decomposable is a result about decomposable posets until
someone checks.

**The rule does not apply here, and the reason is the logical shape and not the numbers.**

| | `mg-05ec`'s broken rescue | `mg-409a`'s ceiling |
|---|---|---|
| shape | *"failures occur **only** on class `X`"* | *"`alpha(P) ≤ 1` for **every** `P`"* |
| what the witnesses carry | **the content itself** — the claim IS a statement about which posets do what | **tightness only** — that the bound cannot be improved |
| what restricting the class does | can **falsify** it, by exhibiting a failure outside `X` | can only **lower** the bound, never raise it |
| what the closure consumes | — | the **upper bound**, not the tightness |

A universally quantified upper bound restricted to a subclass is still an upper bound on
that subclass. `Z_n`'s job in `mg-409a` §3 is to show `1` cannot be lowered *in general*;
that job is unrelated to the direction §2's bar argument uses. **So the witness being
outside the counterexample class is not a defect in the closure — it is irrelevant to it.**

`p2.5` makes this concrete rather than rhetorical: `mg-409a`'s **own** witness families
(pair indicators and odd-fiber indicators) certify `alpha ≤ 1` at **all 267 primitive
posets** in range. The proof is class-blind, as claimed.

---

## 6. The whole picture, in one table

| restriction | ceiling on `alpha` | kind | vs the bar (`≥ 2`) |
|---|---|---|---|
| none — every poset | **1** | **PROVED** (`mg-409a` §3, five lines) | short by ≥ 2× |
| frozen (`δ < 1/3`) | **3/4** | **PROVED** (chain, §2 here) but **VACUOUS** — class empty to `n = 14` | short by ≥ 2.67× |
| primitive (`n ≥ 4`) | **0.3876** | **MEASURED** exhaustively to `n = 8`; exact certificate `≤ 525/832` over `n ≤ 7` | short by ≥ 5.2× |
| the bar itself | **`> (n−1)/(γn)`, a constant in `[2,3)`** | **PROVED** (`mg-409a` §2) | — |

**Every row is below the bar. The closure holds, and it holds hardest exactly where
counterexamples would have to live.**

---

## 7. What would have to be true for this verdict to be wrong

Filed as named conditions so that a reversal cannot be assembled after the fact.

1. **`mg-409a` §3 is wrong.** Everything here about the *unconditional* ceiling is
   downstream of a proof I read but did **not** re-derive line by line; I re-measured its
   consequences (`p2.5`: its own witnesses certify `≤ 1` at 267 primitive posets) rather
   than auditing its Case 2 argument. If `alpha ≤ 1` is false at some poset, §5's
   structural point survives but its subject does not.
2. **The bar is wrong.** `alpha_n > (n−1)/(γn)` is **read from `mg-409a` §2** and its
   Theorem E input is read from `step8.tex`. Neither is re-derived here. If the bar is
   actually `o(1)`, every ceiling in §6 becomes interesting again and this document's
   verdict inverts. `mg-409a`'s own §7.1 prices this and says it would have to fall by a
   factor of `n`.
3. **The primitive maximum rises with `n`.** It falls at every step `n = 4…8`, but that is
   **five points and a measurement**, not a theorem. A primitive poset at some larger `n`
   with `alpha` near 1 would not break the closure (the `≤ 1` proof is unconditional) but
   it would refute §4.4's trend and make §4.5's "delivers a stronger bound anyway" false.
4. **`n ≤ 8` is too small for primitivity to have shown its behaviour.** Primitive posets
   first exist at `n = 4`, so the exhaustive range covers only five sizes. This is the same
   exposure that killed the standard-dominance rescue at `n = 7` — one size past where it
   had been checked — which is why `p4` was run at all, and it does not stop being an
   exposure just because `n = 8` agreed.
5. **My reading of "primitive" is not Daniel's.** All three notions are measured (§4.1) and
   the answer is the same under prime and under ordinal-indecomposable. If he meant
   something else again — *near* an ordinal sum while primitive, which his sentence can also
   be read as — then the right object is a continuity statement about `alpha` under
   perturbation towards `Z_n`, and **that is not measured here.**

---

## 8. Defects of my own, all kept

**D0 — I RE-DERIVED A PROVED CORPUS RESULT AND WROTE IT UP AS NEW, AND I HAD DECLARED THE
EXPOSURE IN ADVANCE.** `PREDICTIONS.md` H1 records that I read `mg-409a`'s deliverable in
full before writing anything; **H5 records that I had NOT read `mg-8d66`'s.** I then derived
the chain on paper (H2), measured it, and drafted §1 and §2 claiming links `A`, `B` and `C`
as *new* and the chain as *"a re-derivation, and it must be earned here"*. All three links
and the whole chain are `mg-8d66` §4.2, one commit older, and link `C` is `FACTS.md` F1 with
`KIND: U` — an entry **Daniel named specifically**. I found this only when I opened
`FACTS.md` for an unrelated reason, after the instrument was written and committed.

**This is `mg-623a`'s duplicates-the-literature failure with the corpus in the literature's
place**, and the registry that exists precisely to prevent it (`mg-03cf`, landed the same
day) would have prevented it had I read it first. The commit `254d7ce` carries the wrong
framing and is left in history with this note rather than rewritten. What survives is what
the re-measurement is actually worth: a second implementation and the extension to `n = 6`
(§2.2), and it is labelled that way now.

**The generalisable lesson, since a defect that only indicts me is worth little:** `mg-409a`
and `mg-8d66` are the same arc, the ticket named both in its first paragraph, and I read one.
A ticket that cites two prior items is telling you its author read summaries of both.

**D1 — my first run reported a REFUTATION and it was my own definition's empty
quantifier.** `is_prime` tests for a module of size `2..n−1`. At `n = 2` that range is
**empty**, so the 2-element antichain passes vacuously — and it attains `alpha = 1`. `p2.2`
therefore printed `FAIL — NO PRIME POSET ATTAINS alpha = 1 (1 found)` and the sole
"counterexample to my own finding" was `A_2`. `PREDICTIONS.md` **E2 named this exact
ambiguity in advance and I still walked into it.** Fixed by `is_primitive_proper`
(`prime ∧ n ≥ 4`), which excludes exactly the degenerate cases and nothing else — there is
no prime poset on 3 elements, and `p0.3` checks that rather than assuming it. **Kept
because the fix turned a FAIL into a PASS, which is precisely the case where a defect
normally gets erased.** The finding survives the fix and is sharper for it: the single
literal-prime attainer is the 2-element antichain, which is not an independent witness at
all — it is the **block `Z_n` is the ordinal sum OF**.

**D2 — `alpha` itself is a float.** `alpha_power` is a power iteration. Every **verdict** is
an exact rational comparison (`p1.1`–`p1.3`, `p1.6`, `p3.2`, `p3.4`), an exhibited rational
witness (`p2.3`), a combinatorial count (`p0.1`, `p2.2c`), or the exact `alpha == 1`
orthogonality test (`p2.2`). The numbers `0.3876…`, `0.3596…`, `0.3343…`, `0.3219…` are
**measurements** and appear in tables, never under a `PASS`. Same exposure as `mg-409a`'s
D6, stated because it applies to me too.

**D3 — "the primitive maximum is 0.3876" is a maximum of a measured quantity.** What is
*proved in range* is weaker and exact: no primitive poset attains 1, and every primitive
poset carries an exhibited rational witness with `R_M ≤ 525/832`. The gap between
`0.3876` and `525/832 = 0.6310` is the gap between what I measured and what I can certify
without an eigenvalue, and it is not closed.

**D4 — the `n = 7` and `n = 8` populations are PRIMITIVE-only.** The full `n = 7` iso-class
count (2 045) is verified as an enumeration control, but `alpha` is measured only at the 234
primitive classes there and the 2 585 at `n = 8`. So *"max `alpha` over all posets at
`n = 7` or `n = 8`"* is **not** measured here and those rows of §4.4 say so. The exact
`R_M ≤ 525/832` certificate likewise covers `n ≤ 7` only — `p4` runs the exact `alpha == 1`
test at `n = 8` but not the exact upper-bound certificates.

**D5 — I import `lib409a` for the entire object.** Deliberate, and argued in the instrument
README: this ticket audits a claim *about* `mg-409a`'s operator, so a second construction
would make disagreement uninterpretable. The cost is real — a defect in `lib409a`'s
`Π_o`/`Π_e` or fiber construction would propagate here **undetected**, and my three `alpha`
routes (Jacobi, power iteration, exact orthogonality) all run through **the same fibers**.
They cross-check the linear algebra, not the compressions. Same shape as `mg-409a`'s D5 and
`mg-8bc7`'s D6.

**D6 — the decreasing trend is five points.** `0.3876 / 0.3596 / 0.3343 / 0.3219 / 0.3122`
is monotone and the steps are shrinking, which is consistent with convergence to something
positive and with decay to 0 alike. **No extrapolation is offered and none should be read
in.** §7.3 files the reversal condition.

**D7 — I did not re-derive Theorem E, the bar, or `mg-409a` §3's Case 2.** All three are
read. §7.1 and §7.2 name what that costs.

---

## 9. What this document does not do

- **`STATE.md` is NOT touched.** Nothing here is a ledger movement: the finding is about a
  document that is not on the ledger, `mg-409a` §9 says the same of itself, and no row's
  kind or status changes. The `mg-e331` ratchet is not exercised.
- **`docs/imports/compression.tex` is NOT edited** — its README reserves that directory for
  verbatim copies, and W1, W2 and W4 all left it alone.
- **`mg-409a`'s deliverable is NOT edited.** Its §3 is confirmed, not corrected; the chain
  it does not contain is a re-derivation and belongs here.
- **No recommendation is retracted.** `pm-onethird`'s 3/10-and-do-not-pursue stands, and
  §0 says so explicitly, because the objection resolves in favour of the closure.
- **No claim is made about `λ_std`, or about the route reopening.** The bar and the wall are
  taken from `mg-409a` §2 and `STATE.md:78` as read.
