# OneThird — THE DEMAND SIDE HAS BEEN ATTACKED, IT IS PRICED, AND THE PRICE IS `10×` AT ITS CEILING AND `6.8×` AT THE ONLY IN-REGIME MEASUREMENT — SO "1 IN 150" BECOMES "1 IN 15" AT BEST AND "1 IN 22" AT MEASURED, AND **NEITHER CLOSES THE WALL, WHICH IS STILL `5×`**. AND THE ENUMERATION NO LONGER HAS TO BE TRUSTED: THE CHEEGER SANDWICH'S **EASY** HALF CAPS **EVERY** DERIVATION OF STEP 5's CONCLUSION AS IT IS WRITTEN — FIFTH CHAIN INCLUDED — AT `ε_dem ≤ 2·ε_leak = 2/5`, SO THE DEMAND SIDE IS WORTH **AT MOST `20×`** AGAINST THE `50×` NEEDED AND THE RESIDUAL WALL IS **`≥ 2.5×`**. ⚠️ **THE CAP'S TWO CONDITIONS TRAVEL WITH IT AND ARE HERE RATHER THAN ONE LINE AWAY: it is CONDITIONAL ON NON-VACUITY — the alternative branch is `L1b` at `2/5`, i.e. the open lemma, so that branch cannot be assumed either — and it is quoted at `ε_leak = 1/5`, which ERRS OPTIMISTIC, so the cap is itself optimistic (`2/7` at the required-scope `n ≤ 7` ceiling, `0` at the uniform value).** The three documents that establish the pricing — `mg-9461`, `mg-81ff`, `mg-00b3` — HAVE NO ROW IN `STATE.md`, `FACTS.md` OR `CONCEPTS.md`, WHICH IS WHY THE HALF LOOKS UNPUSHED. And the number itself carries no combinatorial hint: `150 = 3 · 2 · (1/ε_leak)²`, three of whose four factors are bookkeeping and whose only contentful input is L4's threshold

**Work item.** `mg-7564` (repo `onethird_program`), filed by `pm-onethird` on Daniel's
2026-08-12 question:

> *"did we ever make progress on seeing whether the 1/150 constant can be improved
> downstream so we don't need something so tight? and if we did find the right constant the
> value itself might give a combinatorial hint as to the solution"*

**Instrument.** [`code/demand_relaxation_7564/`](../code/demand_relaxation_7564/) —
predictions committed at `84b1a3a` before one line of it existed, **with the exposure
disclosed**: I had read `mg-9461`, `mg-81ff` and `mg-00b3` in full first, so `R1`–`R5` of
that file are REPORTS at zero credit and only the two-currency join is a live bet.

> ### ⛔ FOUR THINGS THIS DOCUMENT REFUSES TO DO
>
> 1. **NO WINDOW FIGURE.** `mg-131e` refuted the supply `ε_spec = 2/(n+1)` at `n = 6`; every
>    `n ≥ N` table in this lineage rests on it and the replacement is unknown.
> 2. **NO POSET IS ENUMERATED.** Every measured input below — `C₃^gap`, `c`, `gap`,
>    `min_k Q_k`, `ε_leak` — is **cited from the document that measured it, with its status
>    attached**. Agreement with those documents is arithmetic reproduction and is **not**
>    corroboration of the measurement.
> 3. **NOTHING IS WRITTEN INTO `STATE.md`.** §8 is a **proposal**, in the form `mg-9461` §7
>    and `mg-76b2` §10 use. That file is `pm-onethird`'s.
> 4. **NO NUMBER BELOW IS PRESENTED AS A BOUND.** The relaxed targets are what *would*
>    suffice **if** the lemma each is gated on were proved. §6 states the gate at each row.

---

## 0. Verdict

> ### 1. HAS THE DEMAND SIDE BEEN PUSHED? — **YES, FOUR TIMES, AND IT IS THE BEST-PRICED HALF OF THE GAP. THE READING THAT IT IS THIN IS A READING OF THE LEDGER, AND THE LEDGER IS WHERE THE WORK IS MISSING.**
>
> | ticket | landed | what it did to the demand |
> |---|---|---|
> | `mg-345e` | 2026-08-07 | separated `ε_spec` into `ε_sup` (what we can prove) and `ε_dem` (what suffices), and established the supply side is **L4-independent** |
> | `mg-76b2` / `mg-94c3` | 2026-08-10 | **enumerated four inequivalent `ε_dem` chains** (§6) and proved `C₃^(III) = 1` on L2's first disjunct; measured `C₃^gap` at `1.500 → 2.386`, RISING |
> | `mg-9461` / `mg-39bf` | 2026-08-10 | **priced the whole chain question at `10×` and no more**, and established at source that **Step 6 consumes none of the four chains** |
> | `mg-81ff` / `mg-00b3` | 2026-08-10 | **chain (IV) IS chain (II)** — one unknown in two currencies; and measured `C₃^gap` **IN REGIME**, where it reaches `10.17` at `n = 25` |
>
> **AND HERE IS WHY IT LOOKS UNPUSHED.** `mg-9461`, `mg-81ff` and `mg-00b3` occur **`0`
> times in `STATE.md`, `0` times in `docs/FACTS.md` and `0` times in `docs/CONCEPTS.md`**
> (counted by grep; §7). Three landed documents — one of them the deliverable Daniel
> personally asked for on 2026-08-08 — with **no row in the canonical file**. `STATE.md`'s
> demand-side text is the **pre-`mg-9461` state**: it carries `mg-76b2`/`mg-94c3` and stops
> there. **This is `mg-03cf`'s finding recurring on a different arc** — the compression arc
> had no `STATE.md` row either, so every fact it produced was homeless at once.
>
> ### 2. THE TWO `C₃` STATEMENTS, RECONCILED — **THERE ARE THREE `C₃`s, NOT TWO, AND THE ONE IN `ε_dem` IS ALREADY AT ITS BEST VALUE. THAT LEVER IS CLOSED.**
>
> | name | the relation it lives in | value | status |
> |---|---|---|---|
> | **`C₃^(III)`** | `Φ_pref ≤ √(2 C₃ ε_spec)` — `Op-Form §4.3`'s **displayed** relation | **`1`, uniformly in `n`** | **PROVEN on L2's FIRST DISJUNCT** (`mg-76b2` §3; audited `mg-94c3`, `1032/1032`) |
> | **`C₃^gap`** | `1 − ρ_pref ≤ C₃(1 − λ_std)` — `§4.3`'s gap-form repair, named in the same sentence | `1.500, 1.473, 1.990, 2.386` at `n = 3..6`, **RISING**; `≥ 1` unconditionally, exceeded at **1023 of 1032** | **MEASURED, out of regime** (`mg-94c3` §3) |
> | **`C₃^cut`** | `Φ*_pref / Φ*` — L3's own wording | up to `10/9`, exceeds `1` at `10 of 1032` | **MEASURED** |
>
> **THE `C₃` IN `ε_dem = ε_leak²/(2C₃)` IS `C₃^(III)`.** The two `STATE.md` sentences the
> ticket asks about are **about different numbers and both are true**:
>
> - *"`C₃` is unquantified and not an L4 question"* — `STATE.md`'s `mg-345e` row, whose
>   rider *"the live `ε_spec ≲ 2×10⁻²` is the `C₃ = 1` value and `C₃ ≥ 1`"* is, in
>   `mg-76b2` §10's own words, **"unconditionally true of the gap-form `C₃`"**. It is a
>   statement about `C₃^gap`.
> - *`C₃ = 1` attained* — `mg-76b2`'s theorem, and it is about `C₃^(III)`.
>
> **AND THE CONSEQUENCE FOR DANIEL'S QUESTION IS THE ONE THAT MATTERS: `C₃` CANNOT LOOSEN
> THE DEMAND, IN EITHER CURRENCY.** `C₃^(III)` enters the denominator, so `C₃ ≥ 1` makes
> `1/50` an **over-estimate of the budget**, never an under-estimate (`mg-6bc2` §6,
> `mg-345e` §5.3) — `C₃ = 1` is already the **best case** and it is already the value the
> corpus quotes. Every move `C₃^(III)` can make is a move that makes the demand **tighter**.
> **There is no `C₃` lever. It is closed, and it was closed before this ticket was filed.**
>
> ### 3. `ε_leak = 0.20` — **THE HIGHEST-LEVERAGE NUMBER ON THE DEMAND SIDE, AND IT MOVES THE WRONG WAY. IT IS NOT A CONSTANT WE HAVE FAILED TO COMPUTE; IT IS L4's THRESHOLD WEARING A DECIMAL POINT.**
>
> `ε_leak` **is** L4's threshold `ε₀`: Step 5's conclusion is `Δ₁ ≤ ε_leak` and L4's
> hypothesis is `Δ₁(A,B) ≤ ε`, the same object (`mg-9461` §4.1, `mg-3969`). `0.20` is
> **none of** the three objects that have worn the name — it is the largest `ε` at which
> `mg-3ce3`'s `survives` predicate produced 0 RED over 6681 posets: an **EMPIRICAL `FP`
> calibration**, which in `STATE.md`'s own taxonomy says **nothing** above the largest `n`
> checked.
>
> **Its error direction is known and it is optimistic.** Against the required scope's `n ≤ 7`
> ceiling `1/7` it is **40 % too large**, and that `40 %` is a **floor**, not a margin —
> `mg-d3c7`'s refuting family is *proved*, so the ceiling is available in closed form at
> every `n`: `44 %` at `n = 9`, `282 %` at `n = 21`, `1880 %` at `n = 101`. The uniform
> surrogate in the required scope is **`0` — refuted, not capped**.
>
> **So the quadratic runs against us.** `ε_dem` is increasing in `ε_leak`; overstating
> `ε_leak` overstates the budget, which **understates** how hard L1b must work. **Every
> quotation of `ε_spec ≲ 2×10⁻²` in this corpus is an upper estimate of our own headroom**
> (`mg-9461` §4.3). And **there is no experiment that improves `0.20`**: sweeping further can
> only lower a ceiling on a surrogate already refuted at `0`; pinning the consumed threshold
> at *any* positive value **proves the conjecture on the thin-interface class** (`mg-3969`
> §5.3). Only a proof moves it.
>
> ### 4. THE ANSWER TO DANIEL, AS A NUMBER — **DEMAND-CAN-BE-RELAXED-TO-X, AND `X` IS `1 IN 15` AS A CEILING AND `1 IN 22` AS THE ONLY IN-REGIME MEASUREMENT. IT IS ALSO THE THIRD ANSWER: IT DOES NOT MATTER, BECAUSE THE WALL IS STILL `5×`.**
>
> The join below is this document's own — the corpus states `1/150` against `ε_spec = 1/50`
> and states **no other row in that currency** (grep, `d1` §B, every raw hit adjudicated by
> reading it). Identity: `ε_spec = 3·d·q̄·n/(n+1)` (`mg-6bc2` §3.1, EXACT; rows are the
> `n → ∞` limit, which is the **loosest** reading — at finite `n` the demand is `(n+1)/n`
> tighter).
>
> | row | `ε_dem` | `d·q̄ ≤` | **as** | wall | status |
> |---|---|---|---|---|---|
> | frozen product today (the two-atom law) | `1` | `1/3` | **1 in 3** | `1×` | the SUPPLY side |
> | chain (IV), `c → 1` — the enumeration's **ceiling** | `1/5` | `1/15` | **1 in 15** | **`5×`** | gated on the **Prefix-capture CONJECTURE** |
> | chain (IV), worst `c` **measured in regime** (`S_12`) | `0.13591` | `0.045302` | **1 in 22.1** | `7.36×` | 3 families, **not a bound** |
> | chain (II), `C₃^gap = 1` — the extreme point | `1/5` | `1/15` | 1 in 15 | `5×` | **MEASURED FALSE at 1023/1032** |
> | chain (II), `C₃^gap = 10.1654` in regime (`S_25`) | `0.01967` | `0.006558` | 1 in 152.5 | `50.83×` | **WORSE than the baseline** |
> | **chain (I) = (III) at `C₃ = 1` — AS WRITTEN** | `1/50` | `1/150` | **1 in 150** | `50×` | PROVEN on L2's first disjunct |
>
> **Read as a density, which is the form with combinatorial content.** `q̄ = 1/3` **exactly**
> at every boundary maximiser at every `n ≤ 7` (`mg-6bc2` §3.1, finite population, marked as
> such), so the whole demand collapses onto `d = m/C(n,2)`, the incomparability density:
>
> > **as written: at most `2 %` of pairs incomparable. Loosest of the four: at most `20 %`.
> > The frozen witness that saturates the supply has `100 %`.**
>
> ### 5. AND THE VALUE CARRIES NO COMBINATORIAL HINT, WHICH IS ITSELF THE FINDING.
>
> `150 = 3 · 2 · (1/ε_leak)² = 3 · 2 · 25`. Every factor is named:
>
> | factor | value | where it comes from | status |
> |---|---|---|---|
> | `3` | 3 | the `d·q̄ → ε_spec` conversion | **exact identity** |
> | `2` | 2 | Cheeger's hard direction, `(Φ*)²/2 ≤ 1−λ_std` | **PROVEN** |
> | `C₃` | 1 | the prefix restriction's loss | PROVEN on L2's 1st disjunct |
> | `1/ε_leak²` | 25 | `ε_leak = 1/5`, **squared by the Cheeger square** | **EMPIRICAL — L4's threshold** |
>
> **Three of the four factors are bookkeeping.** The only input with content is `ε_leak`,
> and §3 says what that is. So the number to think with is not `150` — it is **`1/5`**, and
> the honest sentence is that *the entire demand is L4's threshold, squared, times a
> conversion constant.* Dropping the Cheeger square (chains II/IV) removes the `2` **and one
> power of `ε_leak`**: `3/ε_leak = 15`. **The whole `10×` is the Cheeger square**, it is
> exactly `2/ε_leak`, and `d0` §E verifies it is independent of `C₃` at five values because
> `C₃` cancels in the ratio.
>
> ### 6. AND THE ENUMERATION NO LONGER HAS TO BE TRUSTED — **`ε_dem ≤ 2·ε_leak` CAPS EVERY CHAIN, INCLUDING ONE NOBODY HAS WRITTEN. THE DEMAND SIDE IS WORTH AT MOST `20×`, AND THE RESIDUAL WALL IS `≥ 2.5×` BY PROOF.**
>
> Every price above is an **enumeration** statement, and `mg-76b2` §6 explicitly leaves the
> table open: *"If a reader holds a fifth reading, the table is where it should be added."*
> **That hole closes, from an input this corpus already holds.** §4 below gives the argument
> in four lines; the statement is:
>
> > **CEILING.** `Φ* ≥ (1 − λ_std)/2` — the **easy** half of the Cheeger sandwich. `Φ*` is
> > the minimum of `Δ₁` over **all** cuts, so **every** cut, prefix or not, has
> > `Δ₁ ≥ (1−λ_std)/2`. Step 5's conclusion `Δ₁(A_k, A_kᶜ) ≤ ε_leak` is therefore **FALSE at
> > every poset with `1 − λ_std > 2·ε_leak`** — whatever route derives it, whatever constants
> > it carries, and whether or not it pays a Cheeger square.
>
> At `ε_leak = 1/5` that is **`ε_dem ≤ 2/5`**, i.e. **`d·q̄ ≤ 2/15` = 1 in 7.5**, i.e. **at
> most `40 %` of pairs incomparable**, and a residual wall of **`≥ 2.5×`**. So:
>
> | | relaxation vs `1/50` | residual wall |
> |---|---|---|
> | chain (IV) at its ceiling — the best any *enumerated* chain gives | `10×` | `5×` |
> | **any chain whatsoever — PROVED CAP** | **`≤ 20×`** | **`≥ 2.5×`** |
> | what closing the wall would need | `50×` | `1×` |
>
> **A fifth chain is worth at most `2×` more than chain (IV)'s ceiling.** That is the price
> of the one genuinely untried direction on this side, stated before anyone spends on it.
>
> ⚠️ **The cap has a non-vacuity caveat and it is stated at the claim, not buried** (§4.1).
> The demand is an *implication over the frozen class*, so it could hold vacuously above
> `2·ε_leak` if the frozen class were empty in `(2·ε_leak, ε_spec]`. **But that branch is
> L1b itself** — `frozen ⟹ 1−λ_std ≤ 2/5` — which is the open lemma, not a relaxation of it.
> Either the cap binds, or the wall is already proved at `2/5` and the demand question is
> moot. **Neither branch is a closure.**

---

## 1. Which downstream step is being asked to accept less — the ticket's own caution, answered

The ticket is right that a relaxation must be paid for by whatever consumes it, and right
to name Step 6. **The answer is that Step 6 is not the consumer, and this is a fact about
the source rather than a preference** (`mg-9461` §1, byte-checked at
`spectral_near_ordinal_sum_program.tex`, md5 `db095fbe12ba19f0a8107f962c0d1c8f`):

- Step 6's hypothesis is Step 5's conclusion, `Δ₁(A_k, A_kᶜ) ≤ ε_leak`. **No chain's
  constant occurs in it.** `C_3` occurs **0 times in the whole 603-line file**; `Rayleigh`,
  `prefix capture`, `Cheeger`, `\sqrt` and `\std` occur **0 times in Steps 5 and 6**.
- The four chains are four **supply routes for one and the same hypothesis**. Step 6 cannot
  tell which one delivered it, and nothing downstream of Step 5 can either.

**So the step being asked to accept less is Steps 3–4, and the price is not paid downstream
at all — it is paid in a different open lemma.** Step 4 *is* `Apply Cheeger sweeping` and
writes `Φ_P(A_k) ≲ √ε` with no constant, which is chain (I). Chains (II) and (IV) are **not
readings of Steps 3–4; they are replacements for them**, routing through the **Prefix-capture
conjecture** at `:360–364` — a statement inside a `\begin{conjecture}` environment that is
**not one of the six steps and not one of the source's four main open lemmas**.

That is the honest form of the trade: *relaxing the demand does not weaken the contradiction;
it re-routes the proof through a conjecture the source does not list among its open lemmas,
and whose constant it does not name.*

---

## 2. Chain (II) is not a relaxation, and one exact in-regime witness is why

Chain (II)'s demand is `ε_dem = ε_leak/C₃^gap`, so its wall is `ε_sup/ε_dem = 5·C₃^gap`
(`mg-81ff` §5). It beats the baseline **iff `C₃^gap < 10`**, and meets it exactly at `10` —
verified in `d0` §F.

`mg-9461` priced the chain question against `C₃^gap ≤ 2.386`, the largest value then
measured. **Every one of those values is out of regime**: `0` of `4376` primitive posets at
`n ≤ 6` has `1 − λ_std ≤ 2×10⁻²`, smallest gap `0.0562` (`mg-76b2` §7). `mg-00b3` §0.4 then
measured the same constant **inside** the budget, on the staircase `S_n` (`i < j` iff
`j ≥ i+2`), found by asking the exhaustive population which poset maximises `C₃^gap`:

| `n` | gap (exact) | in regime | `C₃^gap` | chain (II) `ε_dem` | `d·q̄ ≤` | wall |
|---|---|---|---|---|---|---|
| 7 | `0.0541957607` | no | 3.0753 | 0.065034 | 1 in 46 | 15.4× |
| 12 | `64/699` | **YES** | 4.8758 | 0.041019 | 1 in 73 | 24.4× |
| 20 | `605/10946` | **YES** | 8.1271 | 0.024609 | 1 in 122 | 40.6× |
| **25** | `300/6773` | **YES** | **10.1654** | **0.019675** | **1 in 152.5** | **50.8×** |
| 28 | `142129/3599603` | **YES** | 11.3629 | 0.017601 | 1 in 170 | 56.8× |

**`S_25` is primitive, sits inside the chain-(III) budget, and forces `C₃^gap ≥ 10.1654`
exactly.** Chain (II) needs a **universal** `C₃^gap` over the class `{gap ≤ ε_spec}` — its
bound is *relative* (`mg-00b3` §0.5) — so one in-regime witness above the crossing point is
enough. **Chain (II)'s `10×` is the `C₃^gap = 1` extreme point and nothing else, and that is
the value `mg-94c3` measured false at 1023 of 1032.**

⚠️ **This table is the join, not a new measurement.** The `C₃^gap` column is `mg-00b3`'s;
the three columns right of it are arithmetic on it, performed here for the first time.

---

## 3. Chain (IV) is the one surviving lever, and it is worth `6.8×`, not `10×`

`S_25` does **not** kill chain (IV), and the asymmetry is real: chain (IV)'s condition is
**absolute and per-poset** (`min_k Q_k ≤ 1 − c(1−gap)`), so on `S_25` it holds with `4.5×` to
spare at `c = 0.9598890 > 40/49`. What governs chain (IV) is the **worst `c` over the class**:

| source | `n` | in regime | `c` | `ε_dem` | `d·q̄ ≤` | wall |
|---|---|---|---|---|---|---|
| `mg-81ff` §5, `N(16)` | 16 | YES | 0.9999000 | 0.199920 | 1 in 15.0 | 5.00× |
| `mg-00b3` §0.4, `S_12` | 12 | **YES** | **0.9258259** | **0.135907** | **1 in 22.1** | **7.36×** |
| `mg-00b3` §0.4, `S_25` | 25 | YES | 0.9598890 | 0.166570 | 1 in 18.0 | 6.00× |
| ceiling, `c → 1` | — | — | 1 | 0.200000 | 1 in 15 | 5.00× |

**So the honest relaxed target is `1 in 22`, not `1 in 15`** — a `6.80×` relaxation of the
demand, not the `10×` the ceiling advertises. `mg-81ff`'s own in-regime family sits at the
extreme point its §5 correctly calls *"the best case of the one unknown, not a property of
chain (IV)"*; the staircase, in the same regime, is worse and the worst row governs.

**Three limits on that number, stated at it:**

1. **It is a measurement over three families, not a bound.** The class `{gap ≤ 1/50}` is
   **non-empty but unenumerable** — `0` of `86 277` at `n = 7`, first reached at `n = 10`
   (`mg-81ff` §6) — so `c` over the class is **UNMEASURED, not unmeasurable**. The next
   in-regime family found could be worse than `S_12`, exactly as `S_12` was worse than
   `N(16)`.
2. **On the FULL population `min c` falls** — `0.750, 0.618, 0.536, 0.453, 0.413` at
   `n = 3..7` — and is below `4/5` at every one, **where chain (IV) does not close at all**.
   Those posets are `23×`–`33×` outside the regime and the refutation does not transfer
   (`mg-81ff` §3), but the direction is not encouraging and it is not this document's to
   dismiss.
3. **It is gated on the Prefix-capture conjecture** (§1), and proving that conjecture
   *qualitatively* delivers *"a constant fraction"* and no number — which is the debt, not
   the payment.

---

## 4. The ceiling on **every** chain — including one nobody has written

The four-chain enumeration is the corpus's, and it is honest about being an enumeration.
This section replaces it, on the demand side only, with a cap.

**The input, and why it does not rest on the unread `.tex`.** The Cheeger sandwich
`(Φ*)²/2 ≤ 1 − λ_std ≤ 2Φ*` is recorded as **PROVEN** at the source (`:318–324`,
`mg-9461` §5.2 row 1). Its **right** half — the easy direction, and the only half used here
— also follows from two things this corpus holds *directly*:

- **(a)** `mg-76b2` **Lemma 2.1**, `Φ ≤ 1 − ρ ≤ 2Φ` for every `k` — **PROVEN**, and
  verified at **25 684** pairs, **exact**, `0` exceptions (`mg-76b2` §9 row 2);
- **(b)** the variational characterisation of `λ_std` as the **maximum** of the Rayleigh
  quotient on `1⊥`, so `ρ(v) ≤ λ_std` for every test vector `v`.

Take `v` = the centred indicator of a cut `A*` attaining `Φ*`. Then
`1 − λ_std ≤ 1 − ρ(1_{A*}) ≤ 2Φ(A*) = 2Φ*`.

**The argument, in four lines.**

1. `Φ* ≥ (1 − λ_std)/2`, by the above.
2. `Φ*` is the minimum of `Δ₁` over **all** cuts, so every cut — prefix or not — has
   `Δ₁ ≥ (1 − λ_std)/2`.
3. Step 5's conclusion is `Δ₁(A_k, A_kᶜ) ≤ ε_leak` at some prefix `A_k`. By (2) that
   conclusion is **false** at every poset with `1 − λ_std > 2·ε_leak`.
4. Therefore **no** derivation of Step 5's conclusion from `1 − λ_std ≤ ε_spec` is sound
   for `ε_spec > 2·ε_leak`. **This mentions no chain**, so a fifth chain does not escape it.

| | value at `ε_leak = 1/5` |
|---|---|
| `ε_dem` cap | **`2/5 = 0.40`** |
| in the `d·q̄` currency | **`2/15`, i.e. `1 in 7.5`** |
| as a density (`q̄ = 1/3`) | **`d ≤ 40 %` of pairs incomparable** |
| relaxation available vs `1/50` | **at most `20×`** |
| residual wall, `ε_sup < 1` | **at least `2.5×`** |

The four enumerated chains all sit **inside** it, none tightly: chain (IV) at `c → 1` and
chain (II) at `C₃^gap = 1` both land at `ε_leak`, exactly **`2×`** below the cap. **So a
fifth chain is worth at most `2×` more than the best enumerated one, and would leave the
wall at `2.5×`.** That is the price of searching for one, stated in advance. A negative
control in `d3` §B confirms the cap test refuses a hypothetical `ε_dem = 3·ε_leak` rather
than accepting everything.

### 4.1 The non-vacuity caveat, at the claim

Step (3) shows the *conclusion* fails pointwise above `2·ε_leak`. The **demand** is an
implication over the **frozen class**, so it could still hold vacuously at a larger
`ε_spec` if the frozen class contained no poset with `1 − λ_std ∈ (2·ε_leak, ε_spec]`.
Both branches of that disjunction point the same way:

- **If the class IS empty there**, then `frozen ⟹ 1 − λ_std ≤ 2/5` is **true** — and that
  is **L1b itself**, at `ε_spec = 2/5`. That is the wall *proved*, not the demand
  *relaxed*, and it is strictly harder than anything on the ladder. It cannot be assumed,
  because assuming it assumes the open lemma.
- **If it is NOT empty**, the cap **binds**.

**Either way the demand side is capped at `2·ε_leak` and the residual wall is `≥ 2.5×`.
The disjunction is the result; neither branch is a closure.**

⚠️ **And the cap moves with `ε_leak`, which errs optimistic (§3 of the verdict).** At
`mg-d3c7`'s required-scope `n ≤ 7` ceiling `ε_leak ≤ 1/7` the cap is `2/7 ≈ 0.286` and the
wall is `≥ 3.5×`; at the uniform value `0` the cap is `0`. **The cap is quoted at the
corpus's own optimistic calibration and is therefore itself optimistic.**

---

## 5. Is `2×10⁻²` itself soft? — **YES, BY ABOUT TWO ORDERS OF MAGNITUDE, AND THE BRACKET IS NOT SYMMETRIC**

The ticket asks whether the target is less precise than the phrasing suggests. It is, and
the corpus says so: `ε_dem ≈ 2×10⁻²` is *"the **repaired** calibration and is **unpinned by
~2 orders of magnitude**"* (`mg-3af8`, three times). That is not a bracket someone drew —
it is **this sensitivity having already fired once**: `mg-e35c` F5 moved `ε_leak` from
`0.02` to `0.20`, a `10×`, and `ε_dem` moved `100×`, because `ε_leak` enters squared.

**But it does not follow that `1/150` might be `1/1.5`.** The direction of the *next*
correction is known (§3 of the verdict): `0.20` errs **optimistic** in the required scope,
by a factor that a *proved* family makes available in closed form and that **grows without
bound in `n`**. So:

> **The `~2 orders` is volatility, not headroom.** The known-direction correction makes the
> demand **tighter**, not looser. Quoting `1/150` as a soft number that might turn out
> generous is the one reading the corpus rules out.

Both halves belong in any answer to Daniel: the number is soft, and it is soft in the
direction that costs us.

---

## 6. What each row of the ladder is gated on — so no row can be quoted without its gate

| row | gate | kind of gate |
|---|---|---|
| `1 in 150` (chains I / III at `C₃ = 1`) | **L2**, and `C₃^(III) = 1` needs L2's **FIRST** disjunct, which `STATE.md` row 9 records `FP✗` — *false as stated*, `2/126` at `n = 6` | one of the source's **four main open lemmas** |
| `1 in 15` (chain II at `C₃^gap = 1`) | **REFUSED** — measured false at 1023/1032 on L2's first disjunct; **UNLICENSED** on the second, where it is unmeasured | not available |
| `1 in 15` (chain IV, `c → 1`) | the **Prefix-capture conjecture**, *and* `c → 1` over an unenumerable class | a conjecture **not on the source's list** |
| `1 in 22` (chain IV, worst in-regime `c`) | the same conjecture, *and* the assumption that `S_12` is the worst case | conjecture + an **unbounded** empirical assumption |
| **`1 in 7.5` (the cap, §4)** | **none — it is a cap, not a route.** No chain reaches it and none can pass it | **PROVED**, from the sandwich's easy half |

**And the row that decides whether any of this matters is none of them.** Pair bias proves
`1 − λ_std ≤ ε_sup` with `ε_sup < 1` — ceiling `n/(n+1)`, **approached, not attained** in the
frozen class — and that is an **equality for the information it consumes**, so no
rearrangement moves it (`mg-6bc2` Claim 3.1; scope `mg-832f` Correction 2). Against it:

> **`50×` at the architecture's own chain. `7.4×` at the best in-regime measurement. `5×` at
> the enumeration's ceiling. `2.5×` at the cap on every chain that could ever be written.
> NO ROW ON THE LADDER CLOSES THE WALL, AND NOW NO ROW CAN.**

Daniel's instinct — that the demand is the unexplored half — is right about *where nobody
was looking* and wrong about *what is there*. The demand side is the **better-priced** half:
it has a proven constant, an exhaustive enumeration of its routes, a `10×` ceiling on that
enumeration and — as of §4 — a `20×` cap that does not depend on the enumeration being
complete. What it does not have, and provably cannot have, is `50×`.

---

## 7. The ledger finding — three landed documents with no row anywhere

Counted by grep at this branch's base commit:

| ticket | `STATE.md` | `docs/FACTS.md` | `docs/CONCEPTS.md` |
|---|---|---|---|
| `mg-9461` — the chain-selection ruling | **0** | **0** | **0** |
| `mg-81ff` — chain (IV) is chain (II) | **0** | **0** | **0** |
| `mg-00b3` — the in-regime `C₃^gap` | **0** | **0** | **0** |
| `mg-76b2` / `mg-94c3` | 3 / 2 | 0 | 0 |
| `mg-345e` / `mg-6bc2` | 5 / 5 | 0 | 1 |

`STATE.md`'s demand-side text is therefore the **pre-`mg-9461` state**. It carries
`mg-76b2`/`mg-94c3` — including, correctly, the refusal to substitute `C₃ = 1` into chain
(II) — and stops there. It does **not** carry:

- that **Step 6 consumes none of the four chains**, byte-checked at source;
- that **the chain question is worth `2/ε_leak = 10×` and no more**;
- that **the residual wall is `5×` at the most permissive chain**;
- that **chain (IV) is chain (II)**, one unknown in two currencies;
- that **`C₃^gap` reaches `10.17` INSIDE the regime at `n = 25`**, which is where chain (II)
  stops being a relaxation at all.

**This is the mechanism, not a complaint.** `pm-onethird` filed this ticket reading the
demand side as under-explored, and that reading is exactly what a canonical file missing
three documents produces. It is `mg-03cf`'s finding on a second arc — and the remedy is the
same one: a row, with its scope at the claim.

---

## 8. Proposal for `pm-onethird` — stated as a proposal, not an edit

**Nothing here has been written into `STATE.md`.** Suggested addition to the attempt ledger,
in the form the surrounding rows use:

> **GREEN · THE DEMAND SIDE IS PRICED AND CAPPED — `10×` ACROSS THE ENUMERATION, `6.8×` AT
> ITS ONLY IN-REGIME MEASUREMENT, AND `≤ 20×` FOR **ANY** CHAIN BY PROOF, AGAINST THE `50×`
> THAT WOULD CLOSE IT (mg-9461, audited mg-39bf; mg-81ff, audited mg-00b3; joined to the
> `d·q̄` currency and capped by mg-7564)** | can `ε_dem` be
> relaxed downstream instead of proved? | **Step 6 consumes NONE of the four chains** —
> its hypothesis is `Δ₁ ≤ ε_leak` and `C_3` occurs `0` times in the 603-line source
> (mg-9461 §1, byte-checked). So relaxing the demand costs nothing downstream of Step 5 and
> **is instead a replacement of Steps 3–4**, routed through the **Prefix-capture conjecture**,
> which is **not one of the source's four main open lemmas**. **The four chains are
> enumerated and priced: `ε_dem` ranges over `ε_leak²/(2C₃^(III))` = `1/50` (as written) to
> `ε_leak` = `1/5` (chain IV, `c → 1`), a factor of exactly `2/ε_leak = 10` at every `C₃`
> because `C₃` cancels.** **Chain (II) is NOT a relaxation:** `ε_dem^(II) = ε_leak/C₃^gap`
> meets `1/50` at `C₃^gap = 10`, and `S_25` — primitive, gap `300/6773 ≤ 1/50`, **in
> regime** — forces `C₃^gap ≥ 10.1654` (mg-00b3 §0.4). **Chain (IV) survives** because its
> condition is absolute and per-poset, at `ε_dem = 0.1359` from the worst in-regime `c`
> measured (`S_12`, `c = 0.9258259`) — **`6.80×`, not `10×`**, and over a class that is
> **non-empty but unenumerable** (`0` of `86 277` at `n = 7`, first reached at `n = 10`), so
> `c` over the class is **UNMEASURED**. **IN THE `d·q̄` CURRENCY (mg-7564, the join): `1/150`
> as written, `1/15` at the ceiling, `1/22` at the only in-regime measurement — and with
> `q̄ = 1/3` pinned at every boundary maximiser at every `n ≤ 7`, these are DENSITY bounds:
> `d ≤ 2 %`, `20 %`, `13.6 %` of pairs incomparable, against `100 %` at the frozen witness.**
> **AND NONE OF IT CLOSES THE WALL — AND NOW NOTHING CAN:** against `ε_sup < 1` — an
> **equality** for the information pair bias consumes — the gap is `50×` as written and
> **still `5×` at the enumeration's ceiling**. ⭐ **AND THE ENUMERATION NO LONGER HAS TO BE
> TRUSTED (mg-7564 §4): the sandwich's EASY half gives `Φ* ≥ (1−λ_std)/2`, so EVERY cut has
> `Δ₁ ≥ (1−λ_std)/2` and Step 5's conclusion is FALSE at every poset with
> `1 − λ_std > 2·ε_leak` — whatever route derives it. Hence `ε_dem ≤ 2·ε_leak = 2/5`
> (`d·q̄ ≤ 2/15`, `d ≤ 40 %`), the demand side is worth AT MOST `20×`, and the residual wall
> is `≥ 2.5×`. A FIFTH CHAIN IS WORTH AT MOST `2×` MORE THAN CHAIN (IV)'s CEILING.** The cap
> rests on `mg-76b2` Lemma 2.1 (PROVEN, `0/25684` exact) plus the variational
> characterisation of `λ_std`, so it does not depend on the unread `.tex`. **Its
> non-vacuity caveat is at the claim:** the demand is an implication over the frozen class,
> so it could hold vacuously above `2/5` only if the frozen class were empty in
> `(2/5, ε_spec]` — but that is `L1b` itself at `ε_spec = 2/5`, i.e. the wall PROVED, and it
> cannot be assumed. Either the cap binds or the open lemma is already true; **neither branch
> is a closure.** **`C₃` IS NOT A LEVER IN EITHER CURRENCY:** `C₃^(III)` is in the
> denominator and `C₃ ≥ 1`, so `C₃ = 1` is already the loosest value and every move it can
> make tightens the demand. **`ε_leak = 0.20` IS NOT A LEVER EITHER, AND IT IS THE ONE THAT
> LOOKS LIKE ONE:** it enters SQUARED, it **is** L4's threshold `ε₀`, it is an **EMPIRICAL
> `FP`** non-refutation, it errs **optimistic** in the required scope by `≥ 40 %` (a floor,
> rising without bound in `n` off a **proved** family), and **no experiment moves it** —
> pinning it at any positive value proves the conjecture on the thin-interface class
> (mg-3969 §5.3). **So `2×10⁻²`'s "unpinned by ~2 orders of magnitude" is VOLATILITY, NOT
> HEADROOM: the known-direction correction makes the demand TIGHTER.** *Docs:*
> `OneThird-ChainSelection-mg-9461.md`, `OneThird-ChainIV-CaptureFraction-mg-81ff.md`,
> `OneThird-ChainIV-CaptureFraction-mg-00b3-IndependentAudit.md`,
> `OneThird-DemandRelaxation-mg-7564.md`.

**Two candidate `FACTS.md` entries**, each with the KIND and SCOPE the registry requires:

- **`ε_dem` spread across the enumeration.** *The four enumerated chains' demands differ by
  exactly `2/ε_leak`.* KIND: **PROVEN (algebra)**. SCOPE: the four chains of `mg-76b2` §6;
  independent of `C₃` because `C₃` cancels; at `ε_leak = 1/5` the factor is `10`.
- **`ε_dem` CAP, chain-independent.** *`ε_dem ≤ 2·ε_leak`, for any derivation of Step 5's
  conclusion whatsoever.* KIND: **PROVEN**, from `mg-76b2` Lemma 2.1 (`0/25684`, exact) plus
  the variational characterisation of `λ_std`. SCOPE: it caps what any chain can license; it
  is **not** a bound on any poset, and it is **conditional on non-vacuity** — the alternative
  branch is `L1b` at `ε_spec = 2/5`, which is the open lemma and not a weaker statement. At
  `ε_leak = 1/5` the cap is `2/5`; **it moves with `ε_leak`, which errs optimistic**, so the
  cap is itself optimistic (`2/7` at `mg-d3c7`'s `n ≤ 7` ceiling, `0` at the uniform value).
- **`C₃^gap` in regime.** *`C₃^gap ≥ 10.1654` is forced by `S_25`, which is primitive and has
  gap `300/6773 ≤ 1/50`.* KIND: **FP✗ — a single exact witness refuting a universal**.
  SCOPE: the staircase family only; it refutes `C₃^gap < 10` over `{gap ≤ 1/50}` and says
  nothing about the class's other members.

---

## 9. What I did NOT do, at the claim

- **I enumerated no posets and re-measured nothing.** `C₃^gap`, `c`, `gap`, `min_k Q_k` and
  `ε_leak` are all typed in from the documents that measured them. If `mg-00b3`'s
  `C₃^gap(S_25) = 10.1654` is wrong, §2's table is wrong with it and this instrument would
  not notice. That is the control this ticket cannot have, and it is stated rather than left
  to be discovered.
- **I did not read the source `.tex`.** It is not in this repository. `mg-9461`'s Step-5/6
  byte-check, `mg-76b2`'s §4.3 quotations and `mg-3969`'s `ε₀` taxonomy are carried **on
  those documents' record**, as `mg-3329` and `mg-be0b` carry theirs.
- **I did not re-derive `ε_sup`, `C₃^(III) = 1`, or `ε_leak`'s calibration.** Each is cited
  with its status and its condition.
- **I did not attempt the Prefix-capture conjecture, L2, or L4.** §6's gates are named, not
  attacked.
- **I did not construct a FIFTH chain, and §4 is why nobody should bother without pricing it
  first.** `mg-76b2` §6 explicitly invites one — *"If a reader holds a fifth reading, the
  table is where it should be added"* — and nobody has added one. §4 does not close that
  door; it puts a **cap** on what is behind it: `ε_dem ≤ 2·ε_leak`, so at most `2×` more than
  chain (IV)'s ceiling and a residual wall of `≥ 2.5×`. **Constructing one is still untried
  and is now the only untried demand-side direction. It cannot close the wall.**

  **⚠️ AND THE FIRST VERSION OF THIS BULLET WAS WRONG, WHICH IS WHY §4 EXISTS.** It read
  *"bounded by `ε_dem ≤ ε_leak` … because `Φ ≤ 1−ρ` is the dictionary"* — an assertion with
  no argument behind it, off by a factor of `2` from the cap that is actually provable, and
  arrived at by pattern-matching the enumerated chains' ceiling rather than by deriving
  anything. Writing it out is what produced §4's four lines. **It is recorded here rather
  than silently replaced**, because the useful part of this document came out of a sentence
  that would have been quoted as a bound if nobody had checked it.
- **I did not edit `STATE.md`, `FACTS.md` or `CONCEPTS.md`.** §7 reports their state and §8
  proposes text; landing it is `pm-onethird`'s.
