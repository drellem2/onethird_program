# OneThird — THE DOWNSTREAM OF L1b, ENUMERATED AND PINNED: 25 ROWS, **8 PROVED UNCONDITIONALLY**, AND THE WHOLE THING COLLAPSES ONTO **ONE INEQUALITY WITH TWO OPEN SIDES — `ε_spec ≤ 2·ε₀`**. THE VERDICT IS **UNDETERMINED**, AND THE ABSENT STEP IS **STEP 6's THRESHOLD `ε₀`** — NOT COARSE, NOT UNMEASURED, **UNMEASURABLE**: no positive value can be bounded above without refuting the conjecture nor below without proving it, and its only refutable surrogate is **`0`** in the scope Step 6 must survive. ⚠️ **EVERY OTHER CONSTANT ON THE CHAIN NOW HAS A NUMBER** — the Cheeger `2`, `C₃^(III) = 1` (on an `FP✗` condition), `C₃^gap ≥ 10.1654` in regime, `C₃^cut ≤ 15/8`, `c = 0.9258259` worst in regime, `ε_leak = 1/5` (EMPIRICAL, optimistic), the cap `2ε₀`, and the `Φ = Δ₁` identity at loss exactly `1` — **so the chain has exactly TWO gating holes and I name both.** AND A COARSE PIN THAT MAKES THE CHAIN ABSURD, TAKEN ANYWAY AS INSTRUCTED: L2's second-disjunct constant, at its only PROVED universal value `Δ₁ ≤ 1`, licenses the chain **only at `ε₀ ≥ 1`** — the vacuous end. AND THE NEW ARITHMETIC: **chain (I)≡(III) does not close against the proved pair-bias supply at ANY `ε₀ ∈ (0,1]`** — smallest residual wall `2n/(n+1)`, attained at the vacuous end `ε₀ = 1`, i.e. **`→ 2×` and already `≥ 1.875` at the `n ≥ 15` a minimal counterexample must have** — and **ANY chain whatsoever, including one nobody has written, needs `ε₀ ≥ n/(2(n+1)) → 1/2`**, which is `2.29×` above the restricted-scope proved ceiling `17/78`, `3.5×` above the required-scope `n ≤ 7` ceiling `1/7`, and infinitely above the required-scope uniform value `0`

**Work item.** `mg-ac0c` (repo `onethird_program`), filed by `pm-onethird` 2026-08-13 on
Daniel's direct instruction:

> *"what i am most worried about is that the downstream of L1B is not actually complete, with
> heuristic constants etc. and we keep circling that without doing anything about it. I would
> rather close it off with real but coarse constants now than waste more time circling"*

**Instrument.** [`code/downstream_constants_ac0c/`](../code/downstream_constants_ac0c/) —
predictions committed at `6a6232d` before one line of it existed, **with the exposure
disclosed**: the ticket instructs *read `mg-7564` first*, and I read seven more documents with
it, so `R1`–`R5` of `PREDICTIONS.md` are REPORTS at zero credit. Only the closure arithmetic,
the novelty greps and the census counts were live. Scorecard at §7 — **one prediction survives
only on a reading, and it is scored as a loss on the raw count.**

> ### ⛔ FIVE THINGS THIS DOCUMENT REFUSES TO DO
>
> 1. **NO POSET IS ENUMERATED AND NOTHING IS MEASURED.** Every empirical input — `ε_leak`,
>    `C₃^gap`, `C₃^cut`, `c`, `17/78`, `1/7`, `mg-d3c7`'s family — is **cited from the
>    document that measured it, with its status attached**. Agreement is arithmetic
>    reproduction, **never** corroboration.
> 2. **NO CONSTANT IS IMPROVED.** The ticket forbids it in as many words. Where a proved-but-
>    terrible value exists, that value is the deliverable.
> 3. **NO HOLE IS FIXED.** Finding and naming them is this ticket; fixing is separate work.
> 4. **NOTHING IS WRITTEN INTO `STATE.md`, `FACTS.md` OR `CONCEPTS.md`.** §8 is a
>    **proposal**, in the form `mg-7564` §8 and `mg-9461` §7 use. Those files are
>    `pm-onethird`'s.
> 5. **`mg-7564` IS NOT REDONE.** Its `ε_dem ≤ 2·ε_leak` cap is an **input** here, cited and
>    used, not re-derived. What is new is sweeping `ε₀` — which that cap leaves free — over
>    its whole admissible range, and solving the closure condition **for `ε₀`**.

---

## 0. VERDICT — the three answers the ticket asks for

> ### 1. THE ENUMERATION — **25 ROWS. 8 ARE `PROVED` UNCONDITIONALLY (32 %). THE WEAKEST KIND IN THE SET IS `ABSENT`, AND ANY PROSE AGGREGATING THESE ROWS MUST SAY SO.**
>
> | status | rows | count |
> |---|---|---|
> | `PROVED` — a theorem, unconditionally, at every `n` | 01 04 11 14 17 20 21 22 | **8** |
> | `PROVED*` — a theorem CONDITIONAL on an open lemma | 06 23 24 | **3** |
> | `EMPIRICAL` — an `FP` calibration; says nothing above the largest `n` checked | 07 08 09 10 12 | **5** |
> | `ASSUMED` — asserted, no warrant on the board | 02 | **1** |
> | `REFUTED` — a witness kills it (`FP✗`) | 03 15 18 19 | **4** |
> | `ABSENT` — no value and no derivation route to one | 00 05 13 16 | **4** |
>
> The full table is §1 and it is **the deliverable even if nothing else here is read**.
> `a1` §B prints the census; `libac0c.Const` cannot construct a row without its scope, its
> source and — for every non-`PROVED` row — an explicit pin-or-hole clause.
>
> ### 2. EVERY NON-`PROVED` ENTRY IS PINNED OR DECLARED A HOLE — **AND AFTER THE PINNING THE CHAIN HAS EXACTLY TWO GATING HOLES.**
>
> Of the four `ABSENT` rows, **two do not gate the chain and I say why**: row **00** is L1b's
> own conclusion, i.e. **the wall itself**, which everything below prices rather than
> supplies; row **16** is L4's modulus `F`, which **Step 6 does not consume** (`mg-345e`), so
> its absence costs nothing. The two that gate are:
>
> | hole | what it is | why it is a hole and not a coarse constant |
> |---|---|---|
> | **row 13 — `ε₀^cons`**, L4's threshold as Step 6 consumes it | ⭐ **THE HOLE** | On minimal counterexamples disjunct (i) is **false by hypothesis**; on every poset anyone can exhibit (i) is **true at `ε = 1`**, and it fired at **all 604 230** swept prefix cuts. So no positive value can be bounded **above** without refuting the conjecture, nor **below** without proving it (`mg-3969` Claims 5.1, 5.2). Its refutable surrogate `U_either` is capped at `17/78` in the **restricted** scope and **refuted at `0`** in the **architecturally required** one (`mg-d3c7`). |
> | **row 05 — `K`**, the prefix's conductance constant on **L2's SECOND disjunct** | **PINNED, and the pin is absurd — taken anyway** | *low-conductance* occurs **5×** in the 603-line source and is **unquantified at every one** (`mg-fa70` §12, at source). Its **only PROVED universal** value is the trivial `Δ₁ ≤ 1`, which delivers `Φ_pref ≤ 1` and therefore meets Step 5's `Φ_pref ≤ ε₀` **only at `ε₀ ≥ 1`** — the vacuous end. In `C₃` units the same pin is `C₃ ≤ 1/(2ε_spec)`, at which the demand reads `ε_spec ≤ ε_leak²·ε_spec`, i.e. `ε_leak ≥ 1`. **Same conclusion by two routes.** |
>
> **And the `EMPIRICAL` rows are pinned at their published values with their direction of
> error attached**, not silently carried: `ε_leak = 1/5` **errs optimistic** in the required
> scope (§2); `C₃^gap ≥ 10.1654` **in regime** is where chain (II) stops being a relaxation;
> `C₃^cut ≤ 15/8` at `n ≤ 6` and **must be squared** to meet chain (III)'s `C₃`; `c` is
> `0.9258259` at the worst in-regime family and **below its own threshold `4/5` at every `n`
> on the full population**.
>
> ### 3. DOES THE CHAIN CLOSE? — **UNDETERMINED, AND THE ABSENT STEP IS STEP 6's THRESHOLD `ε₀`.** That is the ticket's third answer, and per its own words it is **the single most important open item in the programme**.
>
> **Why it is `undetermined` and not `does-not-close`, stated first because the arithmetic
> below reads like the latter.** The whole downstream collapses, coarsely and provably, onto
> **one necessary inequality with two open sides**:
>
> > **`ε_spec ≤ ε_dem ≤ 2·ε₀`** — the middle bound is `mg-7564` §4's chain-free cap, so the
> > outer inequality **`ε_spec ≤ 2·ε₀` is NECESSARY for the chain to close by any route,
> > including a chain nobody has written.**
>
> The left side is **L1b** (row 8, `OPEN`) and the right side is **`ε₀`** (row 13, `ABSENT`).
> Neither has a value. A product of two unknowns cannot be evaluated, and no amount of
> *coarsening* helps, because `ε₀` is not coarse — **it is unmeasurable**, and pinning it at
> any positive value **is** the 1/3–2/3 conjecture on the thin-interface class.
>
> **What CAN be settled coarsely, and both halves are new arithmetic (§3, §4):**
>
> - **CHAIN (I) ≡ (III) — the route the source's own Steps 3–4 write — DOES NOT CLOSE AGAINST
>   THE PROVED PAIR-BIAS SUPPLY AT ANY `ε₀ ∈ (0,1]`.** Its demand is `ε₀²/2 ≤ 1/2`; the
>   supply is `ε_sup(n) = n/(n+1) ≥ 2/3` at every `n ≥ 2`. **Smallest residual wall
>   `2n/(n+1)`, attained at `ε₀ = 1`, which is the vacuous end** — `4/3` at `n = 2`, **`≥ 1.875`
>   at the `n ≥ 15` a minimal counterexample must have** (Peczarski/Gupta, `mg-33f5`), and
>   `→ 2×`. So the `50×` the corpus quotes is not a contingent calibration — **a factor
>   approaching `2×` survives every possible value of `ε₀`.**
> - **ANY CHAIN WHATSOEVER NEEDS `ε₀ ≥ n/(2(n+1))`, i.e. `ε₀ ≳ 1/2`**, to close on the
>   pair-bias supply. **Every proved ceiling on the `(i)`-free surrogate is below it**:
>   `17/78 = 0.2179` short by `2.294×` (and that scope is not the required one), `1/7` short
>   by `3.5×`, `51/5050` short by `49.5×`, and the required-scope uniform value `0` short by
>   everything.
>
> ⚠️ **AND THE ONE THING THAT MUST NOT BE READ OFF THAT.** Those ceilings bound the
> **`(i)`-free surrogate `U_either`**, not `ε₀^cons`. They do **not** say `ε₀` is small —
> `ε₀^cons` is unmeasurable and *"L4 as literally stated has threshold `ε₀ = 1`, `n`-free"* is
> a **true** sentence (`mg-3969` `:157`). What they say is sharper and narrower:
> **no `(i)`-free UNIVERSAL argument can ever deliver the threshold the closure needs.** Only
> a **frozen-conditional** transfer theorem can — which is `mg-dcae`'s rule arriving here from
> a new direction: *any usable statement must consume the frozen hypothesis directly.*
>
> ### 4. AND THE ARCHITECTURE HAS A DIAL WITH NO GOOD SETTING — **the two open lemmas move OPPOSITE ways in `ε₀`, and they do not overlap.**
>
> | `ε₀` | L1b must then deliver | how much better than pair bias | what L4 must then be |
> |---|---|---|---|
> | `1/50` | `ε_spec ≤ 2×10⁻⁴` | `5000×` | the superseded calibration |
> | `1/7` | `ε_spec ≤ 1/98` | `98×` | **at** the required-scope `n ≤ 7` ceiling |
> | `1/5` | `ε_spec ≤ 1/50` | `50×` | **40 % above** that ceiling — the live calibration |
> | `17/78` | `ε_spec ≤ 289/12168` | `42.1×` | above the **restricted**-scope ceiling too |
> | `1/2` | `ε_spec ≤ 1/8` | `8×` | the value the **cap** needs for closure at pair bias |
> | `1` | `ε_spec ≤ 1/2` | `2×` | **L4 at `Δ₁ ≤ 1`, i.e. every cut, i.e. the conjecture** |
>
> *Every factor in the third column is quoted at `n → ∞` (`a2` §E evaluates it at `n = 10⁶`); at finite `n` each is `n/(n+1)` of the printed value, so the column is the **loosest** reading and the demand is tighter at every real `n`.*
>
> **Raising `ε₀` relaxes L1b and strengthens L4, and L4 passes the point where its own
> `(i)`-free surrogate is already refuted BEFORE L1b's demand becomes anything pair bias can
> meet.** There is no setting at which both halves are cheap, and the bottom row is the
> circularity in numeric form.

---

## 1. THE ENUMERATION — every step and every constant between L1b's conclusion and the contradiction

**The deliverable.** Ordered as the argument runs. `a1` §A prints it with each row's full
scope; the `SOURCE` column is where it can be re-read rather than trusted here.

| # | step | quantity | status | value / bound | scope, in one line | source |
|---|---|---|---|---|---|---|
| **00** | L1b out | `1 − λ_std ≤ ε_spec`, i.e. `E[inv_e] ≤ (ε_spec/6)(n²−1)` — **the chain's INPUT** | **ABSENT** | — | row 8 is `OPEN`; `ε_spec` is whatever a proof would deliver | `STATE.md` row 8 |
| **01** | supply | `ε_sup` — the best `ε_spec` **proved today** | **PROVED** | `sup = 1`; `n/(n+1)` at each `n` | supremum over the frozen class, **approached not attained**; an **equality** for the information pair bias consumes | `mg-6bc2` Cl. 3.1, scope `mg-832f` C2 |
| **02** | Step 3 | **L2** as a disjunction | **ASSUMED** | — | `OPEN`; no constant of its own | `STATE.md` row 9 |
| **03** | Step 3 | L2's **first** disjunct — the eigenvector clause | **REFUTED** | `2/126` fail | `n = 6` data; refutes the **first disjunct only**, not L2 | `STATE.md` row 9, scope `mg-3329` |
| **04** | Step 4 | the **Cheeger square** `(Φ*)²/2 ≤ 1 − λ_std` | **PROVED** | `2` | the hard half of the sandwich, every poset | Op-Form §4.2; source `:318–324` |
| **05** | Step 3 | `K` — the prefix constant on L2's **second** disjunct; effective `C₃ = K²/2` | **ABSENT** | — | *low-conductance* occurs `5×` at source, **unquantified at every one** | `mg-fa70` §12; `STATE.md:179` |
| **06** | L3/Step 4 | `C₃^(III)` in `Φ_pref ≤ √(2C₃ε_spec)` | **PROVED\*** | `1`, uniform in `n` | **conditional on L2's FIRST disjunct — which row 03 records `FP✗`**; `1032/1032` | `mg-76b2` §3, audited `mg-94c3` |
| **07** | L3 | `C₃^gap` in `1−ρ_pref ≤ C₃(1−λ_std)` | **EMPIRICAL** | **`≥ 10.1654` in regime** | `1.500…2.386` at `n=3..6` (out of regime); `10.1654` at `S_25`, **in** regime; `≥1` unconditionally | `mg-94c3` §3; `mg-00b3` §0.4 |
| **08** | L3 | `C₃^cut = Φ*_pref/Φ*` — L3's own wording | **EMPIRICAL** | `≤ 15/8` | `n ≤ 6`; **must be SQUARED** to meet chain (III)'s `C₃` | `mg-9461` §2.3 |
| **09** | L3 (row 10) | best-cut-is-a-prefix | **EMPIRICAL** | `125/126` | `n ≤ 6`, **and the population is not unanimous** | `STATE.md` row 10 |
| **10** | chain IV | `c` — the literal capture fraction | **EMPIRICAL** | `0.9258259` worst in regime | three families, **not a bound**; on the full population `min c` falls to `0.413` at `n = 7`, below its own threshold `4/5` at every `n` | `mg-00b3` §0.4; `mg-81ff` §5 |
| **11** | Step 5 | `Φ_P(A) = Δ₁(A,B)` — the Step 4 → 5 conversion | **PROVED** | loss exactly `1` | an **identity** for `0 < \|A\| ≤ n/2`, not a bound | Op-Form Lemma 2.1 |
| **12** | Step 5 out | `ε_leak` in `Δ₁(A_k,A_kᶜ) ≤ ε_leak` | **EMPIRICAL** | `1/5` | an `FP` **non-refutation** (0 RED / 6681 posets); says **nothing** above the largest `n` checked; **errs optimistic** in the required scope | `mg-e35c` F5; `mg-3ce3` |
| **13** | Step 6/L4 | ⭐ **`ε₀^cons`** — L4's threshold **as Step 6 consumes it** | **ABSENT** | — | (i) is **false by hypothesis** at a counterexample and **true at `ε=1`** on every exhibitable poset; fired at **all 604 230** cuts | `mg-3969` Cl. 5.1, 5.2 |
| **14** | Step 6/L4 | `ε₀^unif(U_either)` — the refutable surrogate, **restricted** scope | **PROVED** | `≤ 17/78` | an **upper** bound over cuts with **both** sides non-chain — **not the population Step 6 must survive** | `mg-3969` §6, reproduced `mg-d3c7` |
| **15** | Step 6/L4 | the same surrogate, **architecturally required** scope | **REFUTED** | **`0`** | at least one side non-chain; **refuted at every positive `ε`** by an explicit `n`-free family, not capped | `mg-d3c7` §4 |
| **16** | Step 6/L4 | `F` — L4's modulus | **ABSENT** | — | **UNCONSUMED**: Step 6 consumes no branch in which `F` appears, so its absence does not gate | `mg-345e`; `mg-3969` Cl. 4.1 |
| **17** | Step 6/L4 | branch **(i)** — `P` has a `1/3`-balanced pair | **PROVED** | — | true at `ε=1` on every poset satisfying the conjecture; **false by hypothesis** at a counterexample | `mg-3969` §5.1 |
| **18** | Step 6/L4 | branch **(ii)** — modify `≤ F(ε)n` interface elements | **REFUTED** | `0` | **unconsumable for EVERY strictly positive modulus**, unconditional, via `W*`; the only escape `F ≡ 0` makes L4 **strictly stronger** | `mg-3af9`, audited `mg-c8c6` |
| **19** | Step 6/L4 | branch **(iii)** **as literally stated** | **REFUTED** | `0` | cannot produce the contradiction for **any** `F > 0`; and minimality cannot supply interior slack — `P₀` attains `δ = 1/3` with **zero** slack | Op-Form Cl. 3.2, 3.3 |
| **20** | minimality | `δ(P[A]), δ(P[B]) ≥ 1/3` | **PROVED** | `1/3` | at every `n`, **unless a side is a chain** | `mg-3969` §5.1 |
| **21** | minimality | the both-sides-chain escape | **PROVED** | width `≤ 2` | closed by **Linial**, in the literature, not by L4 | `mg-3969` Rem. 5.0 |
| **22** | contradiction | a balanced pair contradicts `δ(P) < 1/3` | **PROVED** | window width `1/3` | `n`-free: **the whole downstream of Step 5 is dimensionless** | Op-Form §3.2 |
| **23** | demand | `ε_dem` on chain (I) ≡ (III) `= ε_leak²/(2C₃)` | **PROVED\*** | `1/50` | the **relation** is proven; the **number** inherits row 06 (conditional) and row 12 (empirical) | `mg-9461` §5.1 |
| **24** | demand | **`ε_dem ≤ 2·ε_leak`** — the chain-free **cap** | **PROVED\*** | `2/5` | caps **every** derivation of Step 5's conclusion, one nobody has written included; **conditional on non-vacuity**, whose other branch is L1b at `2/5` | `mg-7564` §4, §4.1 |

**WEAKEST KIND IN THIS SET: `ABSENT`.** `STATE.md:107`'s standing rule binds this table:
any sentence aggregating these rows must say so. *"The downstream of L1b is proved"* is
**false** over this set however true each of the eight `PROVED` rows is on its own — which is
the exact worry the ticket was filed on.

---

## 2. THE PINS — every non-`PROVED` row, taken at a real value

The ticket's rule: *pinning may be ugly — a crude bound, a worst case, a value that makes the
chain absurd. Take it anyway and write the number down.* Both absurd pins below are taken.

### 2.1 The two pins that make the chain absurd, and are the deliverable for it

**PIN A — row 05, L2's second-disjunct constant, at its only PROVED universal value.**
The source never names it. The one universal statement available about any delivered prefix is
the trivial `Δ₁(A,B) ≤ 1` for `0 < |A| ≤ n/2` — since `|A ∖ σ(A)| ≤ |A| = min(|A|,|B|)`, a
bound the corpus already holds (`mg-3969` `:154`, where it is derived; and `mg-d3c7`'s control
`C8`). Pinned there, the second disjunct delivers `Φ_pref ≤ 1`, and Step 5 needs
`Φ_pref ≤ ε₀`. **The pin licenses the chain only at `ε₀ ≥ 1`.** `a2` §C runs it at
`ε₀ = 1/5, 1/7, 1/2, 1` and it is `NO, NO, NO, YES`.

*Read in `C₃` units the same pin is `C₃ ≤ 1/(2ε_spec)`, at which
`ε_dem = ε_leak²/(2C₃) = ε_leak²·ε_spec`, so the demand reads `ε_spec ≤ ε_leak²·ε_spec`, i.e.
`ε_leak ≥ 1`. **Two routes, same conclusion** — which is the check that the pin is a property
of the constant and not of the currency it is written in.*

**PIN B — row 13, `ε₀`, at the largest value it can take.** `ε₀ = 1` is the top of the
admissible range: above it Step 5's conclusion is vacuous, because `Δ₁ ≤ 1` always. It is also
exactly where `mg-3969` Claim 5.1 finds the consumable statement trivially true on every
exhibitable poset, and where `mg-3969` `:157` records *"L4 as literally stated has threshold
`ε₀ = 1`, `n`-free"* as **a true sentence and a useless one**. **Pinned there, chain (I)≡(III)
demands `ε_spec ≤ 1/2` and STILL does not close against the proved supply** — §3.

### 2.2 The rest, pinned at their published values with the direction of error attached

| row | pinned at | direction it moves, and why that is the load-bearing half |
|---|---|---|
| 03 | `2/126` fail at `n = 6` | `FP✗` — **refutes the first disjunct only.** The live route is the second, which is row 05, which is ABSENT. |
| 06 | `C₃^(III) = 1` | **the best case, and already the value the corpus quotes.** `C₃` is in the denominator and `C₃ ≥ 1`, so every move it can make makes the demand **tighter**. There is no `C₃` lever — `mg-7564` §0.2 closed it and this ticket does not reopen it. |
| 07 | `C₃^gap ≥ 10.1654` in regime | **RISING** in `n`, and past `10` chain (II) is **worse** than the baseline. One exact in-regime witness (`S_25`) is enough because chain (II) needs a **universal** constant. |
| 08 | `C₃^cut ≤ 15/8`, `n ≤ 6` | up; and it must be **squared** to meet chain (III)'s `C₃`, so `15/8` there is `225/64 ≈ 3.5`. |
| 09 | `125/126`, `n ≤ 6` | `FP` — **not usable against a minimal counterexample at all**, whose `n` is unknown and unbounded. |
| 10 | `c = 0.9258259` at `S_12` | the class `{gap ≤ 1/50}` is **non-empty but unenumerable**, so `c` over it is **UNMEASURED, not unmeasurable**; on the full population `min c` falls below chain (IV)'s own threshold `4/5` at every `n = 3..7`. |
| 12 | `ε_leak = 1/5` | **OPTIMISTIC**, and by a floor rather than a margin: `40 %` above the required-scope `n ≤ 7` ceiling `1/7`, rising without bound off a **proved** family (`44 %` at `n = 9`, `1880 %` at `n = 101`). It enters **squared**. **No experiment moves it** — only a proof. |
| 15 | `0` | **PROVED, and it is the coarse real value the ticket asks for.** At it, no positive `ε_dem` exists on any chain. |
| 18, 19 | `0` | branches (ii) and (iii)-as-stated deliver nothing at any modulus. The live reading is the `F`-free repaired (iii) = rows 13–15. |
| 23, 24 | `1/50`, `2/5` | the **relations** are proved; the **numbers** move with row 12 and are quoted at its optimistic value, so both are optimistic (`2/7` at the `n ≤ 7` ceiling; `0` at the uniform value). |

---

## 3. DOES IT CLOSE? — the sweep the corpus does not perform

The corpus prices the demand **at `ε_leak = 1/5`** (`mg-9461` §5.4's seven rows; `mg-7564`
§0.4's six). **Nobody sweeps `ε₀` over its whole admissible range**, and that sweep is the
ticket's question. `a2` §§A–B is it. Supply benchmark: `ε_sup(n) = n/(n+1)`, what pair bias
**proves**, and an equality for the information it consumes.

| `ε₀` | chain (I)≡(III) `ε₀²/2` | closes? | wall | chain (IV) `c→1` | closes? | cap `2ε₀` | closes? |
|---|---|---|---|---|---|---|---|
| `1` — vacuous end | `1/2` | **no** | **`2n/(n+1)`** | `1` | yes† | `2` | yes† |
| `17/78` — restricted-scope ceiling | `0.023751` | no | `42.1×` | `0.217949` | no | `0.435897` | no |
| `1/5` — the live calibration | `1/50` | no | `50×` | `1/5` | no | `2/5` | no |
| `1/7` — required-scope `n ≤ 7` ceiling | `1/98` | no | `98×` | `1/7` | no | `2/7` | no |
| `51/5050` — the family at `n = 101` | `5.0995×10⁻⁵` | no | `1.961×10⁴` | `0.010099` | no | `0.020198` | no |
| `0` — required-scope uniform | `0` | no | **∞** | — chain absent — | — | `0` | no |

*Every `wall` figure other than the first is quoted at `n → ∞` (`a2` §B evaluates at `n = 10⁶`); at finite `n` each is `n/(n+1)` of the printed value. The column is therefore the **loosest** reading of the wall at every row.*

† **AND THE DAGGER IS THE WHOLE POINT.** Chain (IV) and the cap "close" at `ε₀ = 1` because
`ε₀ = 1` means L4 fires at `Δ₁ ≤ 1`, i.e. **at every cut of every poset** — which by
`mg-3969` Claim 5.2 **is the conjecture**. A closure that appears only where the hypothesis is
the theorem is a circularity, not a closure, and it is reported here rather than quoted as a
positive row.

**THE ONE ROW WITH REAL CONTENT: chain (I)≡(III) — the route the source's own Steps 3–4
write — does not close at ANY `ε₀ ∈ (0,1]`.** `ε₀²/2 ≤ 1/2` for every admissible `ε₀`, while
`ε_sup(n) = n/(n+1) ≥ 2/3` at every `n ≥ 2`. So:

> **A FACTOR `2n/(n+1)` OF THE PUBLISHED `50×` IS NOT A CALIBRATION. It survives every
> possible value of `ε₀` and every value of `C₃ ≥ 1`, and it is a property of the Cheeger
> square, which is `PROVED`.** ⚠️ **CARRY THE `n`:** it is `4/3` at `n = 2`, `1.875` at
> `n = 15`, and `2×` only in the limit. Quoting a bare `2×` overstates it at every finite `n`
> — by `50 %` at `n = 2` (`2` against `4/3`) and by `6.7 %` at the smallest `n` a
> counterexample can have (`2` against `1.875`).

**What that does NOT say, stated because it is the misreading to expect.** It does not say L1b
is impossible. `ε_sup` is what pair bias proves, and pair bias is **closed at an equality**
(`mg-6bc2` Cl. 3.1) — so `ε_sup` is a floor on what *this route's information* can deliver,
not on what L1b can. **The `2n/(n+1)` is a lower bound on how much better than pair-marginal
information any proof of L1b must be, on the architecture's own chain.** Every route below it
must add a realizability fact — which is `STATE.md:21`'s sentence, reached here from the
demand side rather than the supply side.

---

## 4. THE CLOSURE CONDITION, SOLVED FOR `ε₀` RATHER THAN CHECKED AT PINS

`mg-7564`'s cap is chain-free. So closure on the pair-bias supply requires

```
        n/(n+1)   ≤   ε_dem   ≤   2·ε₀           hence           ε₀  ≥  n/(2(n+1)).
```

| `n` | `ε₀` must be `≥` | | ceiling on the `(i)`-free surrogate | value | short of `1/2` by |
|---|---|---|---|---|---|
| `2` | `1/3 = 0.3333` | | `17/78` — restricted scope, `n ≤ 7` | `0.217949` | **`2.294×`** |
| `7` | `7/16 = 0.4375` | | `1/7` — **required** scope, `n ≤ 7` | `0.142857` | **`3.5×`** |
| `15` | `15/32 = 0.4688` | | `51/5050` — required scope, `n = 101` | `0.010099` | `49.51×` |
| `100` | `50/101 = 0.4951` | | `0` — required scope, **uniform** | `0` | **∞** |
| `→ ∞` | **`1/2`** | | | | |

**Every proved ceiling is below the requirement, and the required-scope ones are far below.**

⚠️ **THE SCOPE THAT MUST TRAVEL WITH THAT, AND IT IS THE DIFFERENCE BETWEEN A FINDING AND AN
OVERCLAIM.** Those ceilings bound `U_either` — the deliberately **`(i)`-free** surrogate —
**not** `ε₀^cons`. `ε₀^cons` is unmeasurable and could be `1`. What the table establishes is
therefore not *"`ε₀` is too small"* but:

> **NO `(i)`-FREE UNIVERSAL ARGUMENT CAN DELIVER THE THRESHOLD THE CLOSURE NEEDS.** The
> transfer must be proved **frozen-conditionally**, i.e. by an argument that consumes
> `δ(P) < 1/3` directly — `mg-dcae`'s rule, arriving at Step 6 from the demand side.

That is a **positive** statement about what a proof of the transfer must look like, and it is
the most useful thing in this document after the enumeration itself.

---

## 5. THE DIAL — why there is no good setting of `ε₀`

`a2` §E. Raising `ε₀` relaxes L1b and strengthens L4. The two requirements do not overlap:

- L1b's demand becomes something pair bias could meet only at **`ε₀ ≥ 1/2`** (at the cap) or
  **`ε₀ > 1`** (on chain (I)≡(III), i.e. never).
- L4's `(i)`-free surrogate is already **refuted** in the required scope at `n ≤ 7` above
  **`1/7`**, and **uniformly at `0`**.

`1/7 < 1/2`. **The window is empty**, and it is empty by a factor of `3.5` at the mildest
reading available. At the one setting where the arithmetic does close — `ε₀ = 1` — L4 is the
conjecture. This is `mg-3969` §5.3's circularity, re-derived as a range rather than as a point,
and it is why *"pick a coarse `ε₀` and see"* cannot be made to work.

---

## 6. NOVELTY — what is new here, adjudicated by reading

`a3` runs six **decisive** patterns with **every raw hit printed** and three **non-decisive**
ones reported as establishing nothing in either direction. Corpus at `6a6232d`, 502
`.md`/`.tex`/`.html` files.

| claim | raw hits | adjudication |
|---|---|---|
| the closure requirement `n/(2(n+1))` | **2** | **NEITHER is it.** Both are `3n/(2(n+1))` — the master bound's lossiness factor at the antichain (`mg-6bd1` `:127`, Op-Form audit `:331`), a different object. **NEW.** |
| a threshold on `ε₀`/`ε_leak` at one half | **0** | **NEW.** |
| `ε_dem = 1/2`, i.e. chain (I)/(III) at `ε₀ = 1` | **0** | **NEW.** |
| the dial (raising `ε₀` relaxes L1b, strengthens L4) | **0** | **NEW** as a statement; the two halves exist separately (`mg-9461` §5.3, `mg-3969` §5.3) and nothing joins them. |
| `ε₀ = 1` as a pin | **14** | **12 are `ε_leak = 1/5`** in various tables. **2 are the real thing** and they are `mg-3969` `:59` and `:157` — the vacuity row and *"a true sentence, and a useless one"*. **NOT NEW**, and it is cited as an input at §2.1 rather than claimed. |
| `Δ₁ ≤ 1` as a universal bound | **7** | **NOT NEW.** It is derived at `mg-3969` `:154` and is control `NC3`/`C8` in two instruments. **What is new is applying it as the pin on row 05**, which no hit does. Recorded as a reuse, not a derivation. |

**What a grep can and cannot establish, kept rather than dropped:** it can establish a phrase
is absent; it cannot establish a **statement** is absent — the limit `STATE.md:29` puts on
`mg-145f`'s corpus search, which it marks *"NOT A LEDGER KIND AT ALL"*. Every count above is
**documentary**, at this commit, over this file set.

---

## 7. PREDICTIONS SCORECARD — kept as written, including the one that loses

| # | prediction | outcome |
|---|---|---|
| R1–R5 | the five REPORTS | **zero credit by construction**, as filed |
| **P1** | 18–26 rows, at most 9 `PROVED`-unconditional | **HELD** — 25 rows, 8 `PROVED` (32 %) |
| **P2** | **exactly 2** `ABSENT` entries, named in advance as `ε₀` and L2's second-disjunct constant | ⚠️ **LOST ON THE RAW COUNT — 4 rows are `ABSENT`.** The two I named are right and are the two that **gate**; the other two are L1b's own conclusion (the input) and `F` (unconsumed). **I am scoring this a loss rather than re-reading my own prediction into agreement**, because "on the critical path" was doing work in that sentence that I had not defined before the run. |
| **P3** | chain (I)/(III) never closes on pair bias for any `ε₀ ∈ (0,1]`, minimum wall `2×` | **HELD on the closure half, exactly.** ⚠️ **The `2×` is CORRECTED against myself:** the wall is `2n/(n+1)`, so `2×` is the **limit** and the prediction overstated it at every finite `n` — `4/3` at `n = 2`, `1.875` at `n = 15`. The corrected figure is carried everywhere in this document and the bare `2×` is not. |
| **P4** | the requirement is `ε₀ ≥ n/(2(n+1))`, above every proved ceiling | **HELD**; `17/78` short by `2.294×`, `1/7` by `3.5×` |
| **P5** | `0` hits for both closure statements | **HELD** on both, with the two `3n/(2(n+1))` near-misses adjudicated by reading. **Partial disclosure against myself:** `Δ₁ ≤ 1` and `ε₀ = 1` are both already in the corpus (7 and 2 real hits), so §2.1's two pins **reuse** corpus bounds rather than deriving them. |
| **P6** | the verdict is `undetermined-because-step-X-is-ABSENT`, not `chain-does-not-close` | **HELD** — and it was a bet against the more dramatic reading of my own P3/P4 |
| **P7** | no `ε₀` makes both halves cheap | **HELD**; the window is empty by `3.5×` at the mildest reading |

**Six held, one lost, five at zero credit by construction.** The loss is P2 and it is the one
that would have been easiest to talk my way out of.

---

## 8. PROPOSAL for `pm-onethird` — stated as a proposal, not an edit

**Nothing here has been written into `STATE.md`, `FACTS.md` or `CONCEPTS.md`.** Suggested
attempt-index row, in the form the surrounding rows use:

> **GREEN · THE DOWNSTREAM OF L1b IS ENUMERATED AND PINNED — 25 ROWS, 8 PROVED
> UNCONDITIONALLY, AND IT COLLAPSES ONTO ONE NECESSARY INEQUALITY `ε_spec ≤ 2·ε₀` WITH BOTH
> SIDES OPEN · VERDICT: UNDETERMINED, AND THE ABSENT STEP IS STEP 6's THRESHOLD `ε₀`
> (mg-ac0c; no poset enumeration — deliberately, `mg-345e`'s and `mg-7564`'s refusal kept)** |
> is the downstream of L1b complete, and does the chain close at coarse constants? |
> **THE ENUMERATION IS THE RESULT** — every step and constant between L1b's conclusion and the
> contradiction, each with its kind and scope at the row
> ([`OneThird-DownstreamConstants-mg-ac0c.md`](docs/OneThird-DownstreamConstants-mg-ac0c.md)
> §1): `8` PROVED unconditionally, `3` PROVED-conditional, `5` EMPIRICAL, `1` ASSUMED, `4`
> REFUTED, `4` ABSENT. **WEAKEST KIND IN THE SET: `ABSENT`** — so *"the downstream is proved"*
> is FALSE over it however true the eight are individually. **EXACTLY TWO HOLES GATE THE
> CHAIN, and the other two ABSENT rows are named as non-gating:** row 00 is L1b itself and row
> 16 is `F`, which Step 6 does not consume (mg-345e). **⭐ THE GATING HOLE IS `ε₀`** — not
> coarse, **UNMEASURABLE**: no positive value bounds above without refuting the conjecture nor
> below without proving it (mg-3969 Cl. 5.1/5.2), and its refutable surrogate is `17/78` in
> the **restricted** scope and **`0`** in the **required** one (mg-d3c7). **THE SECOND HOLE IS
> PINNED AND THE PIN IS ABSURD, TAKEN ANYWAY:** L2's second-disjunct constant is unquantified
> at all `5` of its source occurrences (mg-fa70 §12); at its only PROVED universal value
> `Δ₁ ≤ 1` it licenses the chain **only at `ε₀ ≥ 1`**, the vacuous end — and the same pin in
> `C₃` units gives `ε_leak ≥ 1`, two routes to one conclusion. **NEW ARITHMETIC, AND IT IS
> CHAIN-FREE: (a) chain (I)≡(III) — the route the source's own Steps 3–4 write — DOES NOT
> CLOSE against the proved pair-bias supply at ANY `ε₀ ∈ (0,1]`; minimum residual wall
> `2n/(n+1)`, attained at the vacuous end — **carry the `n`: `4/3` at `n = 2`, `1.875` at the
> `n ≥ 15` a minimal counterexample must have, `2×` only in the limit** — so a factor
> approaching `2×` of the published `50×` survives every possible value of `ε₀` and every
> `C₃ ≥ 1`.** **(b) ANY chain, including one nobody has
> written, needs `ε₀ ≥ n/(2(n+1)) → 1/2` to close on that supply** (from mg-7564 §4's
> chain-free cap `ε_dem ≤ 2ε₀`), which is `2.294×` above `17/78`, `3.5×` above `1/7` and
> infinitely above `0`. ⚠️ **THE SCOPE TRAVELS OR THE ROW IS AN OVERCLAIM:** those ceilings
> bound the `(i)`-FREE SURROGATE, **not** `ε₀^cons`, which is unmeasurable and for which
> *"L4 as literally stated has threshold `ε₀ = 1`"* is TRUE (mg-3969 `:157`). What (b)
> establishes is that **no `(i)`-free UNIVERSAL argument can deliver the threshold the closure
> needs — the transfer must consume the frozen hypothesis directly** (mg-dcae's rule, reached
> from the demand side). **(c) THE DIAL HAS NO GOOD SETTING:** raising `ε₀` relaxes L1b and
> strengthens L4, and L4 passes its own refuted surrogate (`1/7`, required scope, `n ≤ 7`)
> **before** L1b's demand becomes anything pair bias can meet (`1/2`). The window is empty by
> `3.5×`. At the one setting where the arithmetic closes, `ε₀ = 1`, L4 **is** the conjecture
> (mg-3969 Cl. 5.2) — the circularity as a range rather than a point. **NOT DONE, AT THE
> CLAIM:** no constant improved (the ticket forbids it), no hole fixed, no poset enumerated,
> nothing re-measured — every empirical input is cited from the document that measured it and
> if mg-d3c7's family is wrong the `ε₀ = 0` row is wrong with it; mg-7564's cap is an INPUT
> and is not re-derived; L2, L4 and the Prefix-capture conjecture are not attempted. |

**Three candidate `FACTS.md` entries**, each with the registry's five fields:

- **STATEMENT** *Chain (I)≡(III)'s demand `ε_dem = ε₀²/(2C₃)` cannot reach the pair-bias
  supply `ε_sup(n) = n/(n+1)` for any `ε₀ ∈ (0,1]` and any `C₃ ≥ 1`; the minimum residual
  factor is `2n/(n+1)` — `4/3` at `n = 2`, `1.875` at `n = 15`, `2×` only in the limit.*
  **KIND** `U` — algebra on two proved inputs. **SCOPE** every
  `n ≥ 2`; `ε₀ ≤ 1` because `Δ₁ ≤ 1` always, so above it Step 5's conclusion is vacuous.
  **FROM** `mg-ac0c`, `a2` §B. **NOT** a statement that L1b is impossible — `ε_sup` is what
  **pair bias** proves and is a floor on that route's information, not on L1b.
- **STATEMENT** *Closure on the pair-bias supply requires `ε₀ ≥ n/(2(n+1))`, for any
  derivation of Step 5's conclusion whatsoever.* **KIND** `U`, given `mg-7564` §4's cap.
  **SCOPE** every `n`; inherits the cap's non-vacuity condition, whose other branch is L1b at
  `2ε₀`. **FROM** `mg-ac0c`, `a2` §D. **NOT** a bound on `ε₀^cons`, which is unmeasurable.
- **STATEMENT** *L2's second disjunct, at the only universal bound the corpus proves about a
  delivered prefix (`Δ₁ ≤ 1`), licenses Step 5's conclusion only at `ε₀ ≥ 1`.* **KIND** `U`.
  **SCOPE** the trivial pin only; a proof of L2's second disjunct **with a named constant**
  would replace it, and none exists — the word *low-conductance* is unquantified at all five
  of its source occurrences. **FROM** `mg-ac0c` §2.1, on `mg-fa70` §12 and `mg-3969` `:154`.
  **NOT** a refutation of L2's second disjunct.

---

## 9. WHAT I DID **NOT** DO, at the claim

1. **I enumerated no posets and re-measured nothing.** `ε_leak`, `C₃^gap`, `C₃^cut`, `c`,
   `17/78`, `1/7`, `125/126`, `2/126`, `604 230` and `mg-d3c7`'s family are all typed in from
   the documents that measured them. **If `mg-d3c7`'s family does not do what it is recorded
   as doing, §3's `ε₀ = 0` row is wrong with it and this instrument would not notice.** `a0`
   §G reproduces that family's **arithmetic** at four published points and explicitly does not
   reproduce its **poset property**.
2. **I did not read the source `.tex`.** It is not in this repository. Steps 1–6, L4's
   verbatim text, the Cheeger sandwich, the Prefix-capture conjecture and `mg-fa70`'s five
   *low-conductance* occurrences are carried **on those documents' record**, as `mg-3af8`,
   `mg-3329` and `mg-7564` carry theirs.
3. **I improved no constant** — forbidden by the ticket, and the temptation was real at row 05,
   where a slightly better pin than `Δ₁ ≤ 1` looks reachable. **It is not taken here.**
4. **I fixed no hole.** L2, L4, the Prefix-capture conjecture and the frozen-conditional
   transfer §4 identifies as the required shape are all **named and not attempted**.
5. **I did not re-derive `mg-7564`'s cap, `ε_sup`, `C₃^(III) = 1`, or the master bound.** Each
   is cited with its status and its condition. The cap in particular is an **input** and its
   non-vacuity caveat is inherited, not re-argued.
6. **I edited no canonical file.** §8 proposes text; landing it is `pm-onethird`'s. `STATE.md`
   is size-ratcheted and a landing is a separate decision.
7. **The `2n/(n+1)` floor is against the PAIR-BIAS supply and nothing else.** It is not a lower
   bound on what L1b can prove. Anyone quoting it as one is quoting a different statement —
   and anyone quoting it as a bare `2×` is quoting its **limit** as though it were its value.

---

## 10. Sources

- [`STATE.md`](../STATE.md) at `87c12d1` — rows 8, 9, 10, 11; the diagram; the standing rule
  at `:107`; § *The single lemma to prove*.
- [`docs/OneThird-DemandRelaxation-mg-7564.md`](OneThird-DemandRelaxation-mg-7564.md) — the
  chain-free cap `ε_dem ≤ 2ε_leak` (§4), the three `C₃`s reconciled (§0.2), `ε_leak` as L4's
  threshold (§0.3). **The template this ticket was told to follow and not to redo.**
- [`docs/OneThird-L4-Threshold-eps0-mg-3969.md`](OneThird-L4-Threshold-eps0-mg-3969.md) —
  Claims 4.1, 5.1, 5.2; §6's ceilings; `Δ₁ ≤ 1` at `:154`; `ε₀ = 1` at `:59` and `:157`.
- [`docs/OneThird-L4-Threshold-eps0-mg-d3c7-IndependentAudit.md`](OneThird-L4-Threshold-eps0-mg-d3c7-IndependentAudit.md)
  — the required-scope refutation at `0`.
- [`docs/OneThird-ChainSelection-mg-9461.md`](OneThird-ChainSelection-mg-9461.md) — the six
  steps (§1.1), the four chains (§2.2), every input's status (§5.2), the sensitivity (§5.3).
- [`docs/OneThird-lambda-std-Operative-Form.md`](OneThird-lambda-std-Operative-Form.md) —
  Lemma 2.1, Claims 3.1–3.3, §4.2's Cheeger square, §6.4's constant budget.
- [`docs/OneThird-ProofShape-mg-3af8.md`](OneThird-ProofShape-mg-3af8.md) — the chain as a
  loop, and the reading of Step 3 this document's rows 02/03/05 follow.
- [`docs/state-history/attempt-mg-3af9.md`](state-history/attempt-mg-3af9.md) — the Step-6
  hole on branch (ii), independent of L1b.
- [`docs/OneThird-C3-PrefixCapture-mg-76b2.md`](OneThird-C3-PrefixCapture-mg-76b2.md) and its
  audit `mg-94c3` — `C₃^(III) = 1`, `C₃^gap`, `C₃^cut`.
- Ticket bodies `mg-ac0c`, `mg-7564`.
