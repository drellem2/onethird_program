# THE CONSUMED CONSTANT, WITH ITS PROVENANCE — `ε_spec ≤ 2×10⁻²`, AND STEP 6 CONSUMES **NONE** OF THE FOUR CHAINS

**Work item.** `mg-9461` (repo `onethird_program`), filed by `pm-onethird` on Daniel's
2026-08-08 00:22 request: *"let's fix this quickly and get an actual constant with clarity on
what it means."*
**Instrument.** [`code/chain_selection_9461/`](../code/chain_selection_9461/) — predictions
committed at `3cd39f1` before one line of it existed; scoring in that directory's `README`.
**Source read at source**, not through any restatement:
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
(603 lines by `wc -l`, md5 `db095fbe12ba19f0a8107f962c0d1c8f` — the same file and the same
md5 `mg-d3c7` reports).

> ### ⛔ TWO THINGS THIS DOCUMENT REFUSES TO PRINT, AND THE REASONS ARE DIFFERENT
>
> 1. **NO WINDOW FIGURE.** `mg-76b2`'s window table (`80, 32, 16, 11, 9, 8`) and the `n ≤ 98`
>    rest on the supply `ε_spec = 2/(n+1)`, **REFUTED at `n = 6`** (`mg-131e`). The
>    replacement is unknown and is `mg-00a1`'s, not this ticket's. The instrument computes no
>    window column at all and says so in its own transcript.
> 2. **`17/78` IS NOT USED AS A LIVE CEILING.** It is correct **only** in the restricted scope
>    that skips every cut where either side is a chain. In the architecturally required scope
>    the uniform threshold is **`0`** — refuted, not capped (`mg-d3c7`, re-verified here on an
>    independent path to `k = 50`). `mg-3969`'s document is live on `main` carrying `17/78`
>    without that qualifier in four places and is under repair by `mg-5214` as this lands;
>    its §§0, 7 and 10 are text under repair, not a reference.

> ### 🔧 THREE EDITS APPLIED BY `mg-fd7c`, 2026-08-09, AFTER `mg-39bf`'s INDEPENDENT AUDIT
>
> `mg-39bf` (`f39ccce`, `docs/OneThird-ChainSelection-mg-39bf-IndependentAudit.md`)
> **CONFIRMED this document's central claim** — Step 6 consumes none of the four chains — and
> named three places where the text overstates what the derivation supports. All three are
> applied here; **the ruling is unchanged and nothing is withdrawn.** The corrections make the
> sentences one clause longer; they do **not** collapse the entitlement back to the tie §3
> corrected *from*, and `mg-39bf` §2.3 checked that explicitly.
>
> 1. **§0(i) and §3's table — the asymmetry is real on L2's FIRST disjunct and not unconditional.**
>    `mg-76b2` proves `C₃^(III) = 1` under L2's *monotone* disjunct. Under L2's *second*
>    disjunct — the source's *"or at least yields a low-conductance prefix"* (`:560–562`), under
>    a preamble reading *"established **with adequate constants**"* (`:553–554`) — `mg-76b2`
>    establishes there is **no conversion to charge for**; it does **not** establish that the
>    delivered prefix meets `Φ ≤ √(2ε_spec)` rather than `K√(ε_spec)`. The constant is not
>    eliminated on that disjunct, it is **relocated** into the lemma's own unnamed
>    *"low-conductance"* — the same shape of debt this document charges Prefix-capture with
>    (`mg-39bf` §2.2/§2.4).
> 2. **§0(i) and §3's table — `40/49` is the PARITY threshold, not the CLOSING threshold.**
>    Chain (IV) closes for every `c > 1 − ε_leak = 4/5`; `40/49 = 0.8163` is where its budget
>    *equals* chain (III)'s. At `c = 4/5 + 1/1000`, strictly below `40/49`, chain (IV) gives
>    `ε_dem = 1/801 > 0` — it closes, **worse** than (III) (`mg-39bf` §3, re-derived from chain
>    (IV)'s own bound). **§5.3 already says this correctly and is the text copied from**; this
>    was a wording slip in §0(i) and §3, not a derivation error, and it changes nothing about
>    the ruling on chain (IV), whose measured `min c` is below **`4/5`** at every `n = 3..6`.
> 3. **§0 item 4 and §4.3 — the universal negative gains the scope §4.3's own table already
>    carried, and `40 %` is labelled as the mildest reading available.** *"There is no reading
>    in which `0.20` is conservative"* is **false as written** and is contradicted by this
>    document's **own** §4.3 table, whose third row prints `0.20` as `8.235 %` **below** `17/78`
>    in the restricted both-sides-non-chain scope. **The table was right and qualified inline;
>    the verdict box was not** — and the verdict box is what gets quoted. It now says *"in the
>    required scope"*. §4.3's `40 %` is exactly right (`0.20/(1/7) = 7/5`, excess `2/5` in exact
>    rationals) and is a **floor**: it is the `n ≤ 7` reading and the mildest available, with
>    `44 %` at `n = 9` from `mg-d3c7`'s **proved** family beside it.
>
> **PLUS FOUR SITES NO TICKET NAMED**, found by sweeping this document for the same two defects
> rather than by following the audit's list: §0(ii)'s *"under either disjunct of L2"*, §5.2's
> `C₃^(III)` and `ε_leak` status rows, claim-ledger rows 4/8/11/16, and §11's re-scope question
> for `mg-81ff` (whose *"chain (IV) is dead"* inference needs the `4/5` level, not `40/49`).
> §5.3, §2.3, §6 and §7's *"chain (IV)'s own `40/49` threshold"* were checked and are **already
> correct** — untouched.
>
> **ERRATUM ON THIS DOCUMENT'S OWN COMMIT MESSAGE, WHICH CANNOT BE EDITED.** The landing commit
> `cf1d7ef` says `ε_leak` *"ERRS OPTIMISTIC IN EVERY READING WHERE A COMPARISON EXISTS"* and
> lists only two of the three comparison readings — it **drops the `17/78` row entirely**, so it
> is the unqualified form without even the table beside it. It also carries *"chain (IV) does
> not close at all unless that number clears 40/49"*. Both are corrected **here**, in the
> document the commit points at; the commit subject is immutable and is recorded as wrong rather
> than left to be quoted. This is the **third** instance on this lineage in one day of a claim
> travelling without its scope — `17/78` published unqualified and struck from `roadmap.md` at
> `7cd8ae7`, `mg-3969` §10 nearly landing the same into `STATE.md` (repaired by `mg-5214` at
> `cf4672e`), and now a correct table summarised by an incorrect box, running in the **opposite**
> direction. See `docs/repair-mg-fd7c-the-verdict-box-and-its-table.md`.

> ### 🔧 SEVEN MORE SCOPE CLAUSES REPAIRED BY `mg-be0b`, 2026-08-10 — AND `mg-fd7c`'s OWN "§2.3 … CHECKED AND ALREADY CORRECT" IS FALSE AT ONE OF ITS FOUR ENTRIES
>
> **Same defect as item 1 above, at seven sites the block above did not reach.** `mg-3329`
> (`641ef42`), landing `mg-fa70`'s finding into `STATE.md`, flagged **two** of them —
> `:102` and `:328` as they then stood — and deliberately left them as this document's property.
> Sweeping this document for the **CLAIM** rather than the phrase found **five more**:
>
> | § | what it read | what it reads now |
> |---|---|---|
> | §2.1 | *"a constant `mg-76b2`'s theorem sets to **1** under L2, which is Step 3"* | **on L2's FIRST DISJUNCT**, L2 being Step 3 |
> | §0 item 5 (the provenance box) | *"**PROVEN CONDITIONAL ON L2**"* | **CONDITIONAL ON L2's FIRST DISJUNCT, WHICH IS STRICTLY STRONGER** |
> | §2.3 table | *"flat — and PROVEN flat, under L2"* | **on L2's FIRST DISJUNCT** |
> | §3 opening | *"The figure `2×10⁻²` is conditional on L2"* | conditional on **L2's FIRST DISJUNCT**, with the reason (`C₃ = 1` is a first-disjunct statement) |
> | §3 closing | *"a row that prints `2×10⁻²` without `under L2` …"* | without **`under L2's first disjunct`** |
> | §7 (the text offered for `STATE.md:164`) | *"**PROVEN CONDITIONAL ON L2** and L2 IS OPEN"* | **CONDITIONAL ON L2's FIRST DISJUNCT — STRICTLY STRONGER THAN L2** |
> | §11 | *"everything else is either **proven** (`C₃^(III)`)"* | **proven-conditionally**, on L2's first disjunct — §5.2 |
>
> **NOTHING IS WITHDRAWN AND NO NUMBER MOVES.** Not one figure, count, threshold or table entry
> in this document changes. The ruling — Step 6 consumes none of the four chains — is untouched,
> and so is the entitlement argument: **`REDUCES C₃ TO L2` and `L3 IS NOT AN INDEPENDENT LEMMA`
> both survive on BOTH disjuncts** (`mg-76b2` §9 row 8) and neither is qualified here. **The
> second disjunct is UNQUANTIFIED, which is weaker than and different from REFUTED, and it is
> not struck anywhere.** Over-correcting in that direction was `mg-fa70`'s own recorded error and
> is the more expensive one.
>
> **THE PART WORTH MORE THAN THE SEVEN EDITS.** The block above records *"§5.3, §2.3, §6 and
> §7's «chain (IV)'s own `40/49` threshold» were checked and are **already correct** — untouched."*
> **§2.3 carried this defect at the time that was written**, in the `C₃^(III)` row of its own
> four-row table. `mg-be0b` re-ran the check rather than inheriting it: §5.3 and §6 are **clean**
> of it and the record is right about those two; §7 was never claimed as checked and simply
> carried it. So the entry is **false for defect (1) and may well have been true for defect (2)**
> — which is the trap, because the record does not say which defect it was checked against, and a
> reader gets a clean bill for both. This is the **second** time in this lineage that the thing
> that was wrong was a **CLEAN CHECK**: `mg-fa70` §2.1 recorded *"`code/c3_prefix_capture_76b2/`
> (greps clean)"* in the very amendment whose headline finding was *sweep for the CLAIM, not the
> PHRASE* — and that directory held **six** occurrences of the claim (`mg-3329`, re-verified by
> `mg-be0b`). **Do not inherit a CHECKED-AND-LEFT list in this lineage. Re-run it.**
>
> See `docs/repair-mg-be0b-the-either-disjunct-claim-outside-STATE.md`.

---

## 0. Verdict

> **1. WHICH CHAIN DOES STEP 6 CONSUME? — NONE OF THEM, AND THIS IS A FACT ABOUT THE SOURCE,
> NOT A PREFERENCE.**
>
> Step 6's hypothesis is Step 5's conclusion, and Step 5's conclusion is
> `E K_k ≪ min(k, n−k)`, i.e. `Δ₁(A_k, A_kᶜ) ≤ ε_leak`. **No chain's constant occurs in it.**
> Checked byte-wise at source (`s3`): `C_3` occurs **0 times in the whole 603-line file**, and
> `Rayleigh`, `prefix capture`, `Cheeger`, `\sqrt` and `\std` occur **0 times in Steps 5 and
> 6**. The four chains are four **supply routes** for one and the same hypothesis; Step 6
> cannot tell which one delivered it, and nothing downstream of Step 5 can either.
>
> This is `mg-345e`'s method applied to `C₃` instead of `F`, exactly as the ticket instructs,
> and it lands the same way: *the demand's dependency is on the statement Step 6 consumes, not
> on the machinery that produced it.*
>
> **2. WHERE THE CHAIN IS ACTUALLY SELECTED — Step 3 and Step 4, and the selector is which
> open lemma gets proved.** Step 4 **is** `Apply Cheeger sweeping`, and it writes
> `Φ_P(A_k) ≲ √ε` with **no constant attached**. So the architecture as written is chain
> **(I)**, and chain **(III)** is that same chain with a bookkeeping constant inserted for
> L3's loss — a constant `mg-76b2`'s theorem sets to **1** on **L2's FIRST DISJUNCT**, L2 being
> Step 3, which the architecture already assumes. *(`mg-be0b`: this read "under L2". `L2` is a
> DISJUNCTION, so "under L2" is "under EITHER disjunct" with the words removed — see §0's
> `mg-fd7c` block item 1 and §0(i). On L2's second disjunct the constant is RELOCATED into the
> lemma's own unnamed "low-conductance", not eliminated. **The architecture assuming Step 3 is
> not the same as the architecture assuming Step 3's FIRST CLAUSE**, and that gap is what the
> unqualified sentence hid.)* **Chains (II) and (IV) are not readings of Steps 3–4.
> They are replacements for them**, routing through the Prefix-capture conjecture at `:360–364`
> — a statement inside a `\begin{conjecture}` environment that is **not one of the six steps
> and not one of the source's four main open lemmas.**
>
> **3. IS THE PROGRAMME ENTITLED TO CHAIN (III)'s CURRENCY WITH L2 UNPROVED? — YES, ON FIVE
> TERMS, AND THE FIRST IS THE ONE THAT DECIDES IT.**
>
> **(i) CHAIN (III) NEEDS A LEMMA, AND A CONSTANT ONLY IF THAT LEMMA IS PROVED IN ITS SECOND
> DISJUNCT. CHAINS (II) AND (IV) NEED A LEMMA *AND* A CONSTANT UNDER EVERY READING, AND (IV)
> ADDITIONALLY NEEDS ITS CONSTANT TO CLEAR A THRESHOLD IT IS MEASURED BELOW AT EVERY
> `n = 3..6`.** *(This sentence is `mg-39bf` §2.4's, applied by `mg-fd7c`; the paragraph below
> is the original argument with the disjunct made explicit.)* Each of the three routes rests on
> exactly **one** open statement — that is a real symmetry and I nearly mis-stated it as a count
> in chain (III)'s favour, which it is not. The asymmetry is in **what proving it delivers**.
> **On L2's first disjunct** — a monotone dominant standard eigenvector, which is where
> `mg-76b2`'s theorem is actually proved — chain (III) needs only that **L2 be true**: the
> theorem then supplies the conversion constant, `C₃^(III) = 1`, uniformly in `n`, with nothing
> left to quantify. **On L2's second disjunct** the source asks only for *"or at least yields a
> low-conductance prefix"* (`:560–562`), under a preamble reading *"established **with adequate
> constants**"* (`:553–554`): `mg-76b2` establishes there is **no conversion to charge for**, and
> that is not the same as establishing that the delivered prefix meets `Φ ≤ √(2ε_spec)` rather
> than `K√(ε_spec)`. On that branch the constant is **relocated**, not eliminated — it moves out
> of the conversion and into the lemma's own unnamed *"low-conductance"*, which is the same shape
> of debt this section charges Prefix-capture with (`mg-39bf` §2.2). Chains (II) and (IV) need
> the **Prefix-capture conjecture** to be true *and* need its constant to take a particular value
> **on every reading** — proving it qualitatively delivers *"a constant fraction"* and no number,
> and chain (IV) is strictly worse than chain (III) below `c = 40/49` and does not close at all
> below `c = 4/5`. **A route whose lemma comes with its constant attached is entitled in a way a
> route whose lemma leaves the constant open is not**, and that difference does not depend on
> either lemma being proved — but on L2's second disjunct chain (III) is on the *other* side of
> that line, and the disjunct carrying the clean version is the one `STATE.md` row 9 records as
> `FP✗`-false as stated. On top of which: L2 is on the source's **own list of four main open
> lemmas**, and Prefix-capture is not on that list at all.
>
> **(ii) IT IS THE ONLY ONE OF THE FOUR WHOSE CONVERSION CONSTANT IS PROVEN RATHER THAN
> MEASURED** — `C₃^(III) = 1`, uniformly in `n`, **on L2's first disjunct** (`mg-76b2`, audited
> `mg-94c3`, `1032/1032`). *(`mg-fd7c`: this read "under either disjunct of L2". Under the
> second disjunct what is proven is that there is **no conversion to charge for**, which is not
> the same as a proven `C₃` — see (i). The other three constants are measured under every
> reading, so the "only one of the four" holds either way; what does not hold unconditionally is
> the word **proven**.)*
>
> **(iii) AND — THE PART THAT IS NOT ALREADY IN THE CORPUS — IT IS THE ONLY ONE FOR WHICH THE
> `n`-FREENESS OF THE CONVERSION IS PROVEN RATHER THAN ASSUMED.** `Op-Form §4.3`'s whole
> purpose is the sentence *"there is no reading of the source under which `n` enters at L3"*,
> and that sentence is **conditional on `C₃` being a constant** — it says *"under either repair
> the loss is a constant `C₃`"*. In chain (III) the constant is proven and is `1`. In the other
> three it is **assumed**, and all three of their constants have been measured moving the wrong
> way with `n` (§2.3). So the conclusion §4.3 exists to establish holds for exactly one of the
> four chains it puts on the table.
>
> **(iv) THE CORROBORATING POPULATION IS NON-SEPARATING AND MUST NOT BE QUOTED AS SUPPORT.**
> `mg-94c3`'s red drill: `Φ*_pref ≤ √(2(1−λ_std))` holds at **all 3340 non-monotone primitive
> posets too**. At the `1−λ_std ≈ 0.3` where that population lives, `√(2ε)` is a weak bound and
> the hypothesis does not discriminate. **The entitlement rests on the proof alone.**
>
> **(v) IT DOES NOT DEGRADE GRACEFULLY.** If L2 fails in *both* disjuncts, `C₃^(III)` becomes
> unquantified and there is **no fallback figure**, because the other three chains' constants
> are the ones measured trending against. The conditioning is therefore load-bearing and must
> be printed at the figure, not one line away.
>
> **4. WHAT IS `ε_leak`, EXACTLY? — IT IS NOT A MEASUREMENT AND IT IS NOT A BOUND. IT IS A
> NON-REFUTATION OVER A FINITE POPULATION, AND IT ERRS OPTIMISTIC IN EVERY READING *IN THE
> REQUIRED SCOPE*.**
>
> `ε_leak` **is** L4's threshold: Step 5's `≪` is `Δ₁ ≤ ε_leak` and L4's hypothesis is
> `Δ₁(A,B) ≤ ε`. Three objects have worn that name (`mg-3969`), and `0.20` is none of them:
>
> | object | what it is | value | status |
> |---|---|---|---|
> | `ε₀^cons` | the threshold below which Step 6's consumable *"(i) ∨ (iii-exact)"* holds **on the class where it is consumed** | — | **STRUCTURALLY UNMEASURABLE.** On minimal counterexamples (i) is false by hypothesis; on everything exhibitable (i) is true at `ε = 1`. Proving it positive **is** the conjecture (`mg-3969` §5.3) |
> | `ε₀^unif` | the `F`-free, (i)-free uniform surrogate, **at least one side non-chain** | **`0`** | **REFUTED, not capped** (`mg-d3c7`; re-verified here to `k = 50`) |
> | `0.20` | the largest `ε` at which `mg-3ce3`'s `survives` predicate produced 0 RED over 6681 posets | `1/5` | **EMPIRICAL CALIBRATION**, `FP` in `STATE.md`'s own taxonomy — and the standing rule says `FP` says **nothing** above the largest `n` checked |
>
> **Direction of error: optimistic, in both readings in the required scope in which a
> comparison exists.** Against the required scope's `n ≤ 7` ceiling `1/7` it is **40 % too
> large** — and that `40 %` is the **mildest** of the required-scope readings, not the margin:
> `mg-d3c7`'s family is *proved*, so the ceiling is available in closed form at every `n` and
> `0.20` is `44 %` above the `n = 9` ceiling `5/36`, `282 %` above `n = 21`'s `11/210`, and so
> on without bound (§4.3). Against the uniform value `0` it is too large by everything.
> Overstating `ε_leak` overstates `ε_dem`, which understates how small `ε_spec` must be, which
> **understates the difficulty**. **There is no reading *in the required scope* in which `0.20`
> is conservative.**
>
> > *(`mg-fd7c`, per `mg-39bf` §4: this read* **"There is no reading in which `0.20` is
> > conservative"**, *and that is false — it is contradicted by §4.3's own third row, which
> > prints `0.20` as `8.235 %* ***below*** *`17/78` in the* ***restricted*** *both-sides-non-chain
> > scope. The table qualified it inline and the verdict box did not, and the verdict box is what
> > gets quoted. The restricted scope is not the one Step 6 must survive — which is why the row
> > does not disturb the ruling — but it is a reading, and a comparison does exist there.)*
>
> **Derivable? No — and not because nobody has done the work.** `mg-3969` §4 finds no `F`-free
> derivation route for the value, and §5.3 shows that pinning the consumed object at *any*
> positive value proves the conjecture on the thin-interface class. **`ε_leak` is not a
> constant we have failed to compute. It is the last lemma wearing a number's clothes** — which
> is what the roadmap's own sweep line already says, and this is the argument for it.
>
> **5. THE CONSTANT, WITH ITS PROVENANCE — the deliverable Daniel asked for.**
>
> > **`ε_spec ≤ ε_leak²/(2C₃) = (1/5)²/2 = 1/50 = 2×10⁻²`**, being the demand of **chain (III)
> > at `C₃ = 1`, which is chain (I)** — the route the source's own Steps 3–4 write.
> > **Inputs, each with its status:** the Cheeger sandwich `(Φ*)²/2 ≤ 1−λ_std ≤ 2Φ*`
> > (`:318–324`) — **PROVEN**; the `Φ ↔ 1−ρ` dictionary — **PROVEN** (`mg-76b2` Lemma 2.1,
> > 25 684 pairs, exact); `C₃^(III) = 1` uniformly in `n` — **PROVEN CONDITIONAL ON L2's FIRST
> > DISJUNCT, WHICH IS STRICTLY STRONGER THAN L2** (`mg-be0b`: this read "CONDITIONAL ON L2";
> > on L2's second disjunct the constant is relocated, not eliminated — §0(i)) — and L2 is
> > **OPEN** while that first disjunct is **`FP✗`-false as stated** (`STATE.md` row 9,
> > `2/126` at `n = 6`); `ε_leak = 0.20` — **EMPIRICAL**, a finite-population non-refutation of
> > a surrogate whose uniform form is refuted at `0`, erring **optimistic in the required
> > scope**; and the Cheeger
> > square itself — **PROVEN as the price of Step 4, ROUTE-DEPENDENT, not architecture-forced.**
> > **Sensitivity: `ε_leak` enters SQUARED, so a factor-2 error in it is a factor-4 error in the
> > target; `C₃` enters linearly; the chain choice is worth `2/ε_leak = 10×` and no more.**
>
> **6. TARGET, OR ARTEFACT OF A LOSSY DERIVATION? — NEITHER, AND THE THIRD ANSWER IS THE
> USEFUL ONE.** `1/50` is a **sufficient** demand of **one** route and has never been shown
> necessary for anything. The square is **not** a derivation error — it is Cheeger's genuine
> price along the route Step 4 actually writes; the factor that *was* an artefact is `C₃`, and
> `mg-76b2` already removed it. And the most permissive route in the enumeration, chain (IV) at
> `c → 1`, demands `1/5` — exactly `10×` weaker, exactly `2/ε_leak`.
>
> **BUT THE NUMBER THAT SETTLES WHETHER ANY OF THIS MATTERS IS NOT `1/50`. IT IS `5`.** Pair
> bias proves `1−λ_std ≤ ε_sup` with `ε_sup = 1` and that is an **equality** for the
> information it consumes — no rearrangement moves it (`mg-6bc2` Claim 3.1). So the distance to
> the wall is `ε_sup/ε_dem = 50×` at the architecture's own chain and **still `5×` at the most
> permissive of the four**. **No choice among the four chains closes the wall.** *"We have been
> aiming at the wrong number all day"* is at most `10×` right and `5×` short of mattering.

---

## 1. Question 1, answered from the source: Step 6 consumes none of the four

### 1.1 The six steps, quoted (`:486–516`, `s3` §A)

```
Step 1  Assume P is a minimal counterexample and label it by its distinguished order e=12…n.
Step 2  Port the known bad-mixing argument … to obtain  λ_std(P) ≥ 1 − ε   with sufficiently small ε.
Step 3  Prove that the dominant standard eigenvector is monotone in e, or directly produce a
        low-conductance prefix.
Step 4  Apply Cheeger sweeping to obtain  A_k = {1,…,k},  Φ_P(A_k) ≲ √ε.
Step 5  Interpret this as an L¹ near ordinal sum:  E K_k ≪ min(k, n−k).
Step 6  Use near-ordinal-sum stability to transfer a balanced pair from P[A_k] or P[A_kᶜ] to P,
        contradicting minimality.
```

### 1.2 The measurement (`s3` §B)

| token | in Step 5 | in Step 6 | in the whole 603-line file |
|---|---|---|---|
| `C_3` (chains II, III) | 0 | 0 | **0** |
| `constant fraction` / `captures` (chain IV) | 0 | 0 | 2 |
| `Rayleigh` (chain IV's currency) | 0 | 0 | 3 |
| `prefix capture` | 0 | 0 | 2 |
| `Cheeger` | 0 | 0 | 9 |
| `\std` (the spectral side) | 0 | 0 | 12 |
| `\sqrt` (the Cheeger square) | 0 | 0 | 1 |

**Step 6's whole hypothesis is Step 5's whole conclusion**, and Step 5's conclusion is a
statement about `E K_k` against `min(k, n−k)` — by `Op-Form` Corollary 2.2 exactly
`Δ₁(A_k, A_kᶜ) ≤ ε_leak`. **The four chains differ entirely above that line.** They agree on
what they deliver and disagree only on what they charge for it. **[PROVEN — it is a byte-wise
fact about the source plus one reading of two sentences.]**

### 1.3 Why this is the same finding `mg-345e` made, and why that matters

`mg-345e` asked *"does L4's modulus `F` appear in anything Step 6 can consume?"* and answered
no, concluding that the demand's dependency on L4 is a dependency on its **threshold**, not its
modulus. The identical move here gives: **the demand's dependency on the chain is a dependency
on `ε_leak`, not on the chain.** The chain fixes the *exchange rate* between `ε_spec` and
`ε_leak`; Step 6 consumes only the latter.

**The consequence is the one worth carrying.** *"Which chain does Step 6 consume"* has no
answer because it is not a Step 6 question. The question with an answer is **"which chain does
the programme's Step 3 proof commit it to"**, and that is §2.

---

## 2. Question 1, part two: where the chain *is* selected, and what selects it

### 2.1 The architecture as written is chain (I) ≡ chain (III) at `C₃ = 1`

Step 4 **is** `Apply Cheeger sweeping`, and it displays `Φ_P(A_k) ≲ √ε` with **no constant**.
The square root is Cheeger's hard direction and it is in the source's own text. So the
architecture pays the Cheeger square and charges nothing for the prefix restriction. That is
chain (I) exactly.

`Op-Form §4.3` then inserts `C₃` at the prefix restriction, on the ground that L3 quantifies
its loss only as *"quantitatively controlled"*. That gives chain (III). **`mg-76b2`'s theorem
sets that constant to `1`** — under L2's first disjunct every set the Cheeger sweep visits is
already a prefix, so restricting the sweep to prefixes costs a factor of exactly `1`; under
L2's second disjunct the prefix is the output and there is nothing to charge. `mg-94c3`
confirms it at `1032/1032` primitive posets exhibiting the first disjunct, worst ratio `0.2603`.

**So (III) collapses onto (I) under precisely the hypothesis Step 3 already is.** The two rows
of `mg-76b2` §6's table are one row.

### 2.2 Chains (II) and (IV) are replacements for Steps 3–4, not readings of them

Both route through the Prefix-capture conjecture, `:360–364`:

> A threshold cut of the dominant standard eigenvector gives a prefix `A_k` whose Rayleigh
> quotient captures a constant fraction, or possibly `1−o(1)`, of the dominant standard
> eigenvalue.

`s3` §C locates it: it sits inside a `\begin{conjecture}` environment, **not** in the
architecture section, and **not** in the source's list of four main open lemmas (`:556–570`).
Taking chain (II) or (IV) therefore does not choose differently *within* the architecture — it
**substitutes a statement that is not on the source's list of four main open lemmas** for the
one that is, displacing L3 (chain II) or both L3 and the Cheeger step (chain IV). It is a
*swap*, not an addition — §3 states the count honestly as a tie and rests the argument
somewhere else.

- **Chain (II)** — the gap-form repair, `1−ρ_pref ≤ C₃(1−λ_std)` — supplies the prefix
  directly, so the Cheeger square is never paid: `Φ ≤ 1−ρ ≤ C₃·ε_spec`, giving
  `ε_dem = ε_leak/C₃`.
- **Chain (IV)** — the literal reading, `ρ ≥ c·λ_std` — gives
  `1−ρ ≤ (1−c) + c·ε_spec`, hence `ε_dem = 1 − (1−ε_leak)/c`, usable for every
  `c > 1−ε_leak = 0.80` (`mg-76b2` §5; the self-consistent threshold at this chain's own budget
  is the tighter `40/49 = 0.8163`).

### 2.3 All three of the constants that are not chain (III)'s are measured moving the wrong way

Read from `mg-76b2` §7 and `mg-94c3` §3, **not re-measured here**:

| constant | chain | `n=3` | `n=4` | `n=5` | `n=6` | direction |
|---|---|---|---|---|---|---|
| `C₃^(III)` — `Φ_pref ≤ √(2C₃ε_spec)` | (III) | `1` | `1` | `1` | `1` | **flat — and PROVEN flat, on L2's FIRST DISJUNCT** (`mg-be0b`: read "under L2"; §0(i)) |
| `C₃^gap` — `1−ρ_pref ≤ C₃(1−λ_std)` | (II) | `1.500` | `1.473` | `1.990` | `2.386` | **up** |
| `C₃^cut` — `Φ*_pref/Φ*` (L3's own wording; **must be squared to meet chain (III)'s `C₃`**) | — | `1` | `3/2` | `6/5` | `15/8` | **up** |
| `min c` — the literal capture fraction | (IV) | `0.750` | `0.618` | `0.536` | `0.453` | **down** |

**Two readings of that table, and only the first is a finding.**

1. **Chain (IV)'s own threshold is `c ≥ 40/49 = 0.8163`, and the measured `min c` is below it
   at every one of `n = 3, 4, 5, 6`, falling.** So chain (IV) as a statement uniform over
   primitive posets is not merely unproven — it is **false on the measured population**, and
   the population is one where `1−λ_std ≥ 0.0562` throughout, i.e. **outside the regime the
   conjecture is about**. That is exactly the caveat `mg-76b2` attaches to every figure in its
   §7 and it is attached here too: this is a **direction**, at `n ≤ 6`, not a refutation of the
   conjecture as intended.
2. `C₃^gap` rising is the same shape for chain (II), and the same caveat applies. Within the
   L2 population specifically, `mg-94c3` finds `C₃^gap > 1` at **1023 of 1032** and
   `C₃^cut > 1` at **10 of 1032** (up to `10/9`), against `C₃^(III) > 1` at **0 of 1032**.

**What this buys, stated at its true strength.** It is not a proof that (II) and (IV) are
unavailable. It is that **the corpus has measured three constants and one theorem**, and the
theorem is chain (III)'s. A `FP` direction cannot establish a bound; but a programme choosing
between a proven constant and three measured-adverse ones is not making a coin-flip.

---

## 3. The entitlement question, which is the live remainder

`pm-onethird`'s narrowing: *is the programme entitled to work in chain (III)'s currency given
that L2 is unproved?*

**The question is well posed and the answer is yes, but "entitled" has to be given a meaning
first.** The figure `2×10⁻²` is conditional on **L2's FIRST DISJUNCT** — it is `ε_leak²/(2C₃)`
at `C₃ = 1`, and `C₃ = 1` is a first-disjunct statement (`mg-be0b`: this read "conditional on
L2", which is weaker than the truth and therefore understates what is being assumed; §0(i)).
The only thing that can make quoting it
illegitimate is if the conditioning **costs more than the alternatives'** conditioning does.

**THE COUNT IS A TIE, AND I SAY SO BEFORE THE ARGUMENT THAT IS NOT A TIE.** The prefix has to
come from somewhere, and the source offers exactly two producers — L2 (Step 3, `:499–500` and
the Remark at `:328–332`) and the Prefix-capture conjecture (`:360–364`). Each route rests on
**one** of them, not on both:

| route | producer of the prefix | open statement | on the source's list of four main open lemmas? | does proving it give the constant? |
|---|---|---|---|---|
| **(I) ≡ (III) at `C₃ = 1`**, L2's **first** disjunct (monotone `v`) | L2 | **L2** (and L3 comes free — `mg-76b2` makes it a *consequence* of L2 in this currency) | **yes** | **YES — `C₃^(III) = 1`, uniform in `n`, nothing left over** |
| **(I) ≡ (III)**, L2's **second** disjunct (*"or at least yields a low-conductance prefix"*, `:560–562`) | L2 | **L2** | **yes** | **NO** — there is no *conversion* to charge for, but the lemma's own unnamed *"low-conductance"* must still be established *"with adequate constants"* (`:553–554`): a prefix at `Φ ≤ K√(ε_spec)` gives an effective `C₃ = K²/2` (`mg-39bf` §2.2) |
| (II) gap-form | Prefix-capture, gap form | **Prefix-capture** | **no** | **no** — delivers *"a constant"*, not a number; `C₃^gap` stays open |
| (IV) literal | Prefix-capture, literal form | **Prefix-capture** | **no** | **no** — and it is strictly worse than chain (III) below `c = 40/49` and does not close at all below `c = 4/5` |

So *"chain (III) borrows less"* is **false as a count** and I am not resting anything on it.
What is true is the last column: **chain (III) needs a lemma, and a constant only if that lemma
is proved in its second disjunct; chains (II) and (IV) need a lemma and a constant under every
reading, and (IV) additionally needs its constant to clear a threshold it is measured below at
every `n = 3..6`.** Proving Prefix-capture tomorrow, in either form, would leave `ε_dem` exactly
as unpinned as `Op-Form §8.1` records it today — which is precisely the failure mode `mg-345e`
§5.2 already identified for a different gate. **Chain (III) on L2's first disjunct is the only
route on which one open statement closing is sufficient to produce a number** — and that is the
disjunct `STATE.md` row 9 records as `FP✗`-false as stated, which is a cost this section already
prints two paragraphs below and which the unqualified version of this sentence hid.

*(`mg-fd7c`, per `mg-39bf` §2.4 and §3: the row for (IV) read* **"does not close at all unless
`c ≥ 40/49`"**, *which names the wrong threshold — `40/49` is where chain (IV)'s budget* equals
*chain (III)'s, while closure needs only `c > 1 − ε_leak = 4/5`; at `c = 4/5 + 1/1000` chain (IV)
gives `ε_dem = 1/801 > 0`. §5.3 already had it right and is the text copied from. Neither the
split row nor the threshold correction changes the ruling: the measured `min c` is
`0.750, 0.618, 0.536, 0.453` at `n = 3..6`, below `4/5` at every one, so chain (IV) fails under*
both *readings.)*

Second, weaker, but not nothing: L2 is a lemma the programme has **already committed to
attempting** — it is on the source's own list — while Prefix-capture is a conjecture the
source's architecture routes around.

**The two costs that are real, and both must be printed at the figure:**

- **L2's first disjunct is false as stated.** `STATE.md` row 9 records the monotonicity clause
  as `FP✗` — `2/126` at `n = 6`. `mg-76b2`'s theorem is stated under *either* disjunct and so
  survives, but the `1032/1032` census is over posets **exhibiting the first disjunct**, i.e.
  the empirical corroboration is for the clause that is refuted as written.
- **That census is non-separating anyway.** `mg-94c3`'s red drill found the same bound holds at
  **all 3340 non-monotone primitive posets**. At `1−λ_std ≈ 0.3`, `√(2ε)` is weak. **So the
  census is not evidence for the conditioning and must not be quoted as if it were.** The
  theorem's support is its proof — which is why `mg-94c3` re-derived the proof rather than
  step-checking it.

**And the failure mode, said plainly: chain (III) does not degrade, it disappears.** If L2
fails in both disjuncts there is no `C₃^(III) = 2` to fall back on — the constant simply
becomes unquantified, and the three alternatives are the ones with adverse measurements. The
conditional is therefore **load-bearing**, not a formality, and a row that prints `2×10⁻²`
without **`under L2's first disjunct`** is not a rounding of the truth but a different claim.
*(`mg-be0b`: this sentence read "without `under L2`". It is the sentence that tells the next
agent what label to carry, so getting the label one clause short here propagates further than
any other site in this document — and `STATE.md` row `:169` now carries the longer form, landed
`mg-3329`. **The paragraph above is unchanged and is right as it stands:** "fails in both
disjuncts" is exactly the condition under which chain (III) disappears.)*

---

## 4. Question 2: what `ε_leak` is, exactly

### 4.1 The identification

Step 5's `E K_k ≪ min(k,n−k)` **is** `Δ₁(A_k,A_kᶜ) ≤ ε_leak` (`Op-Form` Corollary 2.2), and
L4's hypothesis is `Δ₁(A,B) ≤ ε`. They are the same `ε`. `mg-345e` §4 names it *"the threshold
at which L4 fires"*. So **`ε_leak` is L4's threshold `ε₀`**, and every statement `mg-3969` and
`mg-d3c7` make about `ε₀` is a statement about the number this corpus writes as `0.20`.

### 4.2 The three objects, and which one `0.20` is

Set out in §0.4 above. The essential point for a reader deciding what to do next:

- **`ε₀^cons` cannot be measured, and that is structural, not a gap in the work.** On the class
  where Step 6 consumes it — minimal counterexamples — disjunct (i) is false by hypothesis. On
  every poset anyone can exhibit, (i) is true at `ε = 1`, so the statement is satisfied
  vacuously (`mg-3969`: (i) fired at all 604 230 prefix cuts swept). Proving any positive value
  **is** the 1/3–2/3 conjecture on the thin-interface class.
- **`ε₀^unif`, the honest refutable replacement `mg-3969` offered, is refuted at `0`.**
  `mg-d3c7`'s family — the chain `c₁<⋯<c_{n−1}` plus one isolated `z`, `A = {z,c₁..c_{k−1}}`,
  `n = 2k+1` — has `Δ₁ = (k+1)/((2k+1)k) → 0` with **every** balanced-in-side pair evicted.
  **Re-verified here on a path sharing no line with `mg-d3c7`'s or `mg-3969`'s** (`s2`):
  `Δ₁` agrees with the hand formula at `k = 3,4,5,6,8,10,15,20,30,50`, agrees with a brute-force
  `n!` enumeration wherever `n ≤ 8`, `survives = False` at every member, and at `k = 50`
  `Δ₁ = 51/5050 = 0.0101`.
- **`0.20` is a calibration**, and in `STATE.md`'s own taxonomy an `FP` one. The standing rule
  above the ledger: *`FP` says **nothing** above the largest `n` checked* and is **not** usable
  against a minimal counterexample, whose `n` is unknown and unbounded.

### 4.3 Measurement or bound? — neither; and the error direction

**Neither.** A non-refutation over a finite population is not a measurement of the object
(the object is unmeasurable) and not a bound on it (a finite population can refute a universal
and can never establish one — `STATE.md`'s `FP`/`FP✗` asymmetry).

**Where a comparison exists at all *in the required scope*, `0.20` is on the generous side —
and there is exactly one reading, in a scope Step 6 does not have to survive, where it is not:**

| reading | its value | `0.20` against it | direction |
|---|---|---|---|
| uniform surrogate, **required** scope, uniform in `n` | `0` | **above it by everything** | **optimistic** |
| uniform surrogate, **required** scope, `n ≤ 7` | `1/7 = 0.1429` | **40 % above it** — `0.20/(1/7) = 7/5`, excess `2/5`, exact | **optimistic** |
| uniform surrogate, **restricted** scope (skips chain-sided cuts), `n ≤ 7` | `17/78 = 0.2179` | **8.235 % below it** (`7/85`, exact) — **but this scope is not the one Step 6 must survive** | **conservative** |
| `ε₀^cons` — what Step 6 actually consumes | unmeasurable | no comparison exists | — |

> **THE THIRD ROW RUNS THE OTHER WAY AND IT IS NOT AN EXCEPTION TO BE FILED AWAY.** It is why
> §0 item 4 now says *"in the required scope"* rather than *"in every reading"*: without that
> qualifier the verdict box **contradicts this table**. The restricted scope — cuts at which
> **both** sides are non-chain — is `mg-3969`'s sweep population, not the architecture's; on the
> architecturally required population (**at least one** side non-chain) `mg-d3c7` shows the same
> threshold is `0`, refuted rather than capped. The row is retained rather than deleted, with
> its scope, because a number with a scope is worth more than a number withdrawn (`mg-5214`).

**`40 %` IS THE `n ≤ 7` READING AND THE MILDEST AVAILABLE — IT IS A FLOOR, NOT A MARGIN.**
`mg-d3c7`'s refuting family is **proved**, so its members are witnesses at every `n` and the
required-scope ceiling is available in **closed form with no sweep**. The `n ≤ 7` row above is
therefore the *smallest* excess this comparison ever shows (`mg-39bf` §4):

| `n` | required-scope ceiling `≤` | `0.20` is above it by |
|---|---|---|
| `7` | `1/7` (a different witness; the family's own `n = 7` member is `4/21`, above `1/7`) | **40 %** |
| `9` | `5/36` | **44 %** |
| `21` | `11/210` | 282 % |
| `101` | `51/5050` | 1 880 % |
| `401` | `201/80200` | 7 880 % |

**And this cuts *for* §4.4, not against it:** the movement needs no experiment — it is already
fixed by a proved family, which is exactly what *"only a proof moves it"* predicts.

**And the direction propagates the wrong way for us.** `ε_dem` is increasing in `ε_leak`, so
overstating `ε_leak` overstates the spectral budget, which understates how hard L1b has to
work. **Every quotation of `ε_spec ≲ 2×10⁻²` in this corpus is therefore an upper estimate of
our own headroom.**

### 4.4 Derivable at all?

**No, and the reason is the useful part.** `mg-3969` §4 finds no `F`-free derivation route for
the *value*; §5.3 shows that pinning the consumed threshold at any positive value proves the
conjecture on the thin-interface class. So `ε_leak` is **not a constant we have not yet
computed** — computing it is not a smaller task than the theorem. It is the last lemma with a
decimal point where a proof should be.

**A constant we cannot bound is a different object from one we have simply not computed**, as
the ticket puts it — and the answer is that this is the first kind. What follows from that, and
it is a change of research direction rather than a caveat: **there is no experiment that
improves `0.20`.** Sweeping further can only lower a ceiling on a surrogate that is already
refuted at `0`. The only thing that moves this number is a proof.

---

## 5. Question 3: the constant, with full provenance

### 5.1 The line

> **`ε_spec ≤ ε_leak²/(2C₃) = (1/5)²/(2·1) = 1/50 = 2×10⁻²`**
> — the demand of **chain (III) at `C₃ = 1`**, which is **chain (I)**, which is the route the
> source's own **Steps 3–4** write. **Step 6 consumes no chain**; it consumes `Δ₁ ≤ ε_leak`,
> and this line is the price Steps 3–4 charge to deliver that.

### 5.2 Every input, and its status

| input | value | status | if it is wrong |
|---|---|---|---|
| Cheeger sandwich `(Φ*)²/2 ≤ 1−λ_std ≤ 2Φ*` (`:318–324`) | — | **PROVEN** (in the source) | the whole chain goes |
| dictionary `Φ ≤ 1−ρ ≤ 2Φ` (`mg-76b2` Lemma 2.1) | — | **PROVEN**; 0 exceptions / 25 684 pairs, exact | chains become incomparable again |
| **the chain is (I) ≡ (III)** | — | **DERIVED from the source's Step 4** (§2.1), plus the entitlement ledger (§3) | see §6 — the answer moves by at most `10×` |
| `C₃^(III)` | `1`, uniform in `n` | **PROVEN CONDITIONAL ON L2's FIRST DISJUNCT**; L2 **OPEN**, and that disjunct **`FP✗`-false as stated**. On L2's second disjunct there is no *conversion* to charge for but the lemma's own *"low-conductance"* is unquantified — §0(i) | linear: `C₃ = 2` halves the budget |
| `ε_leak` | `1/5` | **EMPIRICAL**; `FP` calibration of a surrogate whose uniform form is **refuted at 0** in the required scope; errs **optimistic in that scope** (and `8.235 %` conservative in the restricted one — §4.3) | **quadratic** — see §5.3 |
| the Cheeger square | — | **PROVEN as the price of Step 4**; **ROUTE-dependent** | droppable only by swapping L2 for Prefix-capture — a lemma that does not carry its constant |
| `ε_sup = 1` (the comparison, not an input) | `sup_{η>0}(1−3η)n/(n+1)` | **PROVEN**, and an **equality** for the information pair bias consumes; **approached, not attained** in the frozen class | the `50×` moves |

### 5.3 Sensitivity, stated rather than left derivable — which is what the ticket asked for

**`ε_leak` enters chains (I)/(III) SQUARED and chain (IV) LINEARLY** (`s1` §E, exact rationals):

| `ε_leak` | `ε_dem` on (I)/(III) at `C₃=1` | `ε_dem` on (IV) at `c=1` | what this value is |
|---|---|---|---|
| `1/5 = 0.20` | **`1/50`** | `1/5` | the live calibration — EMPIRICAL |
| `17/78 = 0.2179` | `289/12168` | `17/78` | restricted-scope ceiling — **not the required scope** |
| `1/7 = 0.1429` | `1/98` | `1/7` | required-scope ceiling at `n ≤ 7` |
| `1/10 = 0.10` | `1/200` | `1/10` | a **factor-2** error in `ε_leak` |
| `1/50 = 0.02` | `1/5000` | `1/50` | the superseded pre-`mg-e35c` value |

> **A factor-2 error in `ε_leak` is a factor-4 error in the target on the squared chains, and a
> factor-2 error on chain (IV).**
>
> **And the corpus's own history is this sensitivity firing.** `mg-e35c` F5 moved `ε_leak`
> `0.02 → 0.20`, a `10×`; `ε_dem` moved `2×10⁻⁴ → 2×10⁻²`, a **`100×`**. The *"100× too
> pessimistic"* banner **is** the square. Anyone who reads that banner as *"the estimate was
> loose"* has mis-read it: the estimate was exactly as loose as its input, squared.

**`C₃` enters linearly** — `C₃ = 2` gives `1/100`.

**`c` (chain IV) has a threshold, not just a scale** (`s1` §F). Below `c = 1−ε_leak = 4/5` the
chain does not close **at all**, and that threshold **moves with `ε_leak`**: at `ε_leak = 1/7`
it becomes `6/7 = 0.857`, at `ε_leak = 1/50` it becomes `49/50 = 0.98`. So an error in `ε_leak`
does not merely rescale chain (IV) — it relocates the point at which chain (IV) exists.

**The chain choice itself is worth exactly `2/ε_leak = 10`, and not more.** Chains (II) and
(III) differ by `(ε_leak/C₃)/(ε_leak²/(2C₃)) = 2/ε_leak` — **`C₃` cancels**, so the factor is
`10` at *every* `C₃` (`mg-94c3`'s figure; verified here as an identity at `C₃ = 1, 3/2, 7/3, 10`).
Chain (IV) at `c → 1` reaches the same `ε_leak = 1/5`, for the same reason: neither spends the
Cheeger square.

### 5.4 The distance to the supply side — the number that decides whether the chain question matters

| chain | `ε_dem` | `ε_sup/ε_dem` |
|---|---|---|
| **(I) ≡ (III) at `C₃ = 1` — the architecture's own** | `1/50` | **50** |
| (III) at `C₃ = 2` | `1/100` | 100 |
| (II) at the measured `C₃^gap = 3/2` (`n=3`) | `2/15` | 15/2 |
| (II) at the measured `C₃^gap = 2.386` (`n=6`) | `100/1193` | ≈ 11.9 |
| (IV) at `c = 40/49` | `1/50` | 50 |
| (IV) at `c = 9/10` | `1/9` | 9 |
| **(IV) at `c = 1` — the most permissive of the four** | `1/5` | **5** |

**The chain question is worth `10×` of a `50×` gap. Even the most permissive route leaves `5×`,
and the supply side cannot be improved — `ε_sup = 1` is an *equality* for the information pair
bias consumes, and every route below it must add a realizability fact.** *(`mg-92e6`'s
adjacency symmetry is the first that bites; not attempted here.)*

---

## 6. Target, or artefact? — the third answer

The ticket asks it as a dichotomy. **Both horns are wrong and the correct answer is more
useful than either.**

- **Not a target we must hit.** Nothing shows Step 6 *requires* `ε_spec ≤ 1/50`. What is shown
  is that `1/50` **suffices** along the route the source writes. Sufficiency is not necessity
  and the corpus has been quoting one as the other.
- **Not an artefact of a lossy derivation.** The square is Cheeger's real price for turning an
  eigen*value* into a *set*, along a Step 4 that says `Apply Cheeger sweeping` in the source's
  own words. The factor that genuinely *was* an artefact is `C₃` — `Op-Form §4.3` charged for a
  conversion the architecture gets free — and `mg-76b2` already removed it. **The lossy factor
  has been found and it has been paid back; the square is not the same kind of thing.**
- **What it actually is: the demand of the only route whose conversion constant is proven.**
  The `10×` separating it from chain (IV) is not slack recoverable by better bookkeeping. It is
  the **price of holding a lemma that comes with its constant attached** instead of one that
  does not — and whose own threshold `c ≥ 40/49` the measured `min c` violates at every `n`
  from 3 to 6, falling.

**And the honest closing arithmetic.** *"If Step 6 does not actually require the square then
1/50 was never the requirement and we have been aiming at the wrong number all day"* — the aim
was off by at most `10×`, only if a route nobody has proven were taken, and the wall is `50×`
away. **Correcting the aim would leave `5×`.** The chain question was worth answering because
an unstated ambiguity in a headline is a defect regardless of size; it was never going to be
the thing that closes the gap.

---

## 7. Proposal for `pm-onethird` — stated as a proposal, not an edit

I have **not** edited `STATE.md` and have not touched `mg-3969`'s document (`mg-5214` is
repairing it as this lands). The provenance line the ticket asks for, in a form that could sit
at `STATE.md:164`:

> **`ε_dem = ε_leak²/(2C₃) = 2×10⁻²` at `C₃ = 1` — THE DEMAND OF CHAIN (III), WHICH IS THE
> ARCHITECTURE'S OWN STEPS 3–4, AND STEP 6 CONSUMES NO CHAIN AT ALL.** Step 6's hypothesis is
> Step 5's `Δ₁ ≤ ε_leak`; `C_3` occurs **0 times in the source** and no chain constant occurs
> in Steps 5–6, so the four chains are supply routes for one hypothesis and the choice is made
> at **Step 3–4**, not at Step 6 (`mg-9461`). **The choice is entitled and costs nothing:**
> chain (III) at `C₃ = 1` consumes only **L2, which is Step 3** — **on L2's FIRST disjunct,
> which is where `mg-76b2`'s theorem is proved; on L2's second disjunct there is no conversion
> to charge for but the lemma's own *"low-conductance"* is itself unquantified** (`mg-39bf`
> §2.2, applied `mg-fd7c`); chains (II) and (IV) each add
> the Prefix-capture conjecture, which is **not** on the source's list of four main open lemmas
> and, unlike L2, **does not deliver the constant when proved** — and all three of their
> constants are measured moving the wrong way
> (`C₃^gap` `1.500→2.386` up; `C₃^cut` `1→15/8` up; `min c` `0.750→0.453` **down, already below
> chain (IV)'s own `40/49` threshold at every `n = 3..6`**; `mg-76b2` §7 / `mg-94c3` §3,
> `n ≤ 6`, outside the regime — a **direction**, not a refutation). **`C₃^(III) = 1` is PROVEN
> CONDITIONAL ON L2's FIRST DISJUNCT — STRICTLY STRONGER THAN L2, WHICH IS A DISJUNCTION — and
> L2 IS OPEN with that first disjunct `FP✗`-false as stated (row 9); the
> `1032/1032` census is NON-SEPARATING (`mg-94c3`'s red drill: the same bound holds at all 3340
> non-monotone posets) and is not support — the theorem's support is its proof.** **`ε_leak =
> 0.20` is EMPIRICAL and is neither a measurement nor a bound:** it is a finite-population
> non-refutation (`FP`) of a surrogate whose uniform form is **refuted at `0`** in the required
> scope (`mg-d3c7`), it sits **40 % above** that scope's `n ≤ 7` ceiling `1/7` — **the mildest
> reading available, `44 %` at `n = 9` and unbounded thereafter off `mg-d3c7`'s proved family** —
> and it errs **optimistic in the required scope** (it is `8.235 %` conservative against the
> **restricted** both-sides-non-chain ceiling `17/78`, which is not the scope Step 6 must
> survive) — so this budget is an upper estimate of our own headroom. **It enters
> SQUARED: a factor-2 error in `ε_leak` is a factor-4 error here, and `mg-e35c` F5's `10×`
> repair is exactly why this figure moved `100×`.** **The chain choice is worth `2/ε_leak = 10×`
> and no more** — chains (II) and (III) differ by that factor at **every** `C₃`, which cancels
> — **and against `ε_sup = 1` the gap is `50×` here and still `5×` at the most permissive of the
> four, so no chain choice closes the wall.** **NO WINDOW FIGURE: the old ones rest on
> `2/(n+1)`, refuted (`mg-131e`); the replacement is `mg-00a1`'s.**

---

## 8. Claim ledger

| # | claim | status |
|---|---|---|
| 1 | Step 5's conclusion is `Δ₁(A_k,A_kᶜ) ≤ ε_leak`, and it is Step 6's whole hypothesis | **PROVEN** (source `:509–516` + `Op-Form` Cor 2.2) |
| 2 | `C_3` occurs 0 times in the source; no chain constant occurs in Steps 5–6 | **PROVEN** — byte-wise, `s3` §B |
| 3 | Step 6 consumes none of the four chains | **PROVEN** given 1 and 2 |
| 4 | the architecture's own Steps 3–4 are chain (I); (III) at `C₃=1` is the same relation | **PROVEN** (source `:499–507`) + **CONDITIONAL on L2's FIRST DISJUNCT** for the `C₃=1` (`mg-fd7c`, per `mg-39bf` §2.2) |
| 5 | chains (II), (IV) each SUBSTITUTE the Prefix-capture conjecture, which is outside the source's four main open lemmas, for L2 | **PROVEN** — `s3` §C/§D locate it inside `\begin{conjecture}` at `:362` and the four lemmas at `:556–570` |
| 6 | chain (III) is the only one of the four whose conversion constant, **and hence the `n`-freeness `Op-Form §4.3` concludes**, is proven rather than assumed | **PROVEN as a reading of §4.3 + `mg-76b2`'s theorem**; new here |
| 7 | all three non-(III) constants are measured moving adversely | **FP / DIRECTION only**, `n ≤ 6`, outside the regime — read from `mg-76b2` §7, `mg-94c3` §3, **not re-measured** |
| 8 | chain (IV)'s measured `min c` is below its own `40/49` parity threshold at `n = 3..6` — **and below its `4/5` closing threshold at every one of them too**, so chain (IV) fails under both readings | **FP**, same caveat — and the sharpest single fact against chain (IV) |
| 9 | `ε_leak` is L4's threshold `ε₀`; `0.20` is an `FP` calibration, not a measurement or a bound | **PROVEN** (identification) + **cited** (`mg-3969`, `mg-345e`) |
| 10 | the uniform surrogate is `0` in the required scope | **PROVEN — cited `mg-d3c7`, re-verified independently here to `k = 50`** (`s2`) |
| 11 | `0.20` errs optimistic in every reading **in the required scope** in which a comparison exists — and is `8.235 %` **conservative** against the **restricted** both-sides-non-chain ceiling `17/78`, which is not the required scope | **PROVEN** given 10 and monotonicity of `ε_dem` in `ε_leak`. *(`mg-fd7c`: this row read "in every reading in which a comparison exists", which §4.3's own third row contradicts — `mg-39bf` §4)* |
| 12 | a factor-2 error in `ε_leak` is a factor-4 error in `ε_dem` on (I)/(III), factor-2 on (IV) | **PROVEN** — exact rationals, `s1` §E |
| 13 | chains (II) and (III) differ by `2/ε_leak = 10` at **every** `C₃` | **PROVEN** — the `C₃` cancels; `mg-94c3`'s figure, verified as an identity |
| 14 | `ε_sup/ε_dem` is `50` at the architecture's chain and `5` at the most permissive of the four | **PROVEN as arithmetic**, **CONDITIONAL** on `ε_sup = 1`, which is a supremum **approached, not attained** in the frozen class |
| 15 | `1/50` is sufficient for one route and has never been shown necessary | **PROVEN** given 3 |
| 16 | the entitlement: each route rests on **one** open statement (a tie), but only chain (III)'s **delivers the constant when proved — on L2's first disjunct**; on L2's second disjunct chain (III) needs a constant too, and (II)/(IV) need one under every reading | **PROVEN** given 4 and 5 — this is the ticket's live question; the count-based version of it is FALSE (§3), and the *unconditional* version of the asymmetry is over-stated (`mg-39bf` §2.2, applied `mg-fd7c` — it does **not** collapse back to the tie, `mg-39bf` §2.3) |

---

## 9. Where this ruling is a judgement rather than a derivation — guard E5, discharged

`PREDICTIONS.md` E5 bound me to name every place the ruling is not derivable from source plus
landed results. There are two, and they are both in §3, not in §1:

1. **"Chain (III) is the one the programme should quote."** What is *derived* is that Step 4 as
   written is Cheeger sweeping (source) and that (III) at `C₃=1` is the only route whose one
   open statement delivers the constant when proved (§3). What is *judged* is that adding no open statement is the right criterion. A
   programme that valued a larger `ε_dem` above a shorter dependency list would rationally
   prefer chain (IV) and go and prove `c`. **I say which criterion I used rather than pretending
   there is only one.**
2. **"The adverse measurements argue against (II) and (IV)."** They are `FP` at `n ≤ 6` on a
   population containing no poset in the regime. They cannot refute the conjecture and I do not
   claim they do. The judgement is that a direction over four points is worth *something* when
   the alternative on offer is a theorem — not that it is evidence at unbounded `n`.

Everything in §§1, 2.1, 2.2, 4 and 5 is source text, exact arithmetic, or a citation.

---

## 10. What I did NOT do

- **L2 not attempted. `C₃` not bounded. The growth bound and the realizability question not
  touched.** Per the ticket.
- **`c` not resolved** — that is `mg-81ff`. §11 says what this ruling implies for it.
- **`ε_sup` not re-derived.** I took `ε_sup = 1` from `STATE.md:15` / `mg-6bc2` Claim 3.1 by
  reading, and carried the `η` because `mg-832f` Correction 2 says to.
- **`mg-76b2` §7's four measured columns not re-measured.** Read, cited, and marked `FP`.
- **`mg-3969`'s 604 230-cut sweep and `mg-d3c7`'s `n = 7` exhaustive sweeps not re-run.** I
  re-verified only the *family*, which is the part this deliverable leans on.
- **No poset above `n = 101` and no exhaustive population at all.** My `s2` is a family check,
  not a sweep, and it establishes a limit, not a census.
- **`STATE.md` NOT EDITED. `mg-3969`'s document NOT EDITED** (under repair by `mg-5214`).
  §7 is a proposal for `pm-onethird`.
- **No window figure computed or printed anywhere**, per the ticket and guard E1.

---

## 11. Sequencing — what this implies for `mg-81ff`

The ticket says: *if this rules chain (IV) live, `mg-81ff` becomes top priority; if it rules
chain (III), `mg-81ff` should be re-scoped or shelved.*

**It rules chain (III) — but "shelve `mg-81ff`" is not quite the right consequence, and the
reason is §5.4.** `c` is an input to chain (IV) only, and chain (IV) is not the route the
programme holds, so **`c` is not on the critical path and resolving it pins nothing that is
currently quoted.** That is the re-scope.

But `c` is not worthless either, and it is worth saying which question it would answer:
**`c` is the only measurable quantity in this whole ruling that could still move the demand by
`10×`** — everything else is either proven-conditionally (`C₃^(III)`, **on L2's first disjunct**
— §5.2), unmeasurable (`ε_leak`), or an equality
(`ε_sup`). *(`mg-be0b`: this read "either proven (`C₃^(III)`)", which drops the conditional
altogether and not merely the disjunct — the most compressed form of the defect in this
document and the one most likely to be quoted out of §11. §5.2's own row has carried the
conditional since the document landed.)* And `mg-76b2` §7 has already produced the first data point against it: `min c` runs
`0.750, 0.618, 0.536, 0.453` at `n = 3..6`, **below chain (IV)'s own `40/49` threshold at every
one**, falling. So the honest re-scope for `mg-81ff` is:

> **Not** *"establish `c`"* — that is the Prefix-capture conjecture, which is not on the
> source's list of four main open lemmas and does not hand over a number when proved.
> **Instead:** *"is `min c` over the small-gap stratum bounded below by `40/49`, or does it fall
> the way the whole-population `min c` falls?"* — and the question has **two** answer levels,
> because `40/49` is the **parity** threshold (chain (IV) matches chain (III)'s budget) while
> `4/5 = 1 − ε_leak` is the **closing** threshold (chain (IV) exists at all): falling below
> `40/49` costs chain (IV) its advantage, falling below `4/5` kills it (`mg-fd7c`, per
> `mg-39bf` §3). If it falls below `4/5` in the stratum too, chain (IV) is
> dead and the `10×` is not available at any price, which **retires the last ambiguity in the
> headline permanently**. That is a cheap, decisive, `FP✗`-shaped question, and it is worth more
> than a value for `c`.

*(This is a recommendation to `pm-onethird`, not a re-scope I have applied.)*

---

## 12. A note on this ticket's framing and timing, recorded because `pm-onethird` asked for it

`pm-onethird`'s mid-flight correction arrived ~40 minutes after dispatch, after I had read the
sources and committed predictions. **Nothing had to be discarded**, and specifically:

- I never used `17/78` as a live ceiling. It appears in this document only inside a
  sensitivity row and a scope table, both of which name the restricted scope in the same line.
- I did **not** re-derive `mg-94c3`'s `10×`. I cited it, and separately checked in one line
  that it is an **identity** (`C₃` cancels), which is what licensed me to state it at *every*
  `C₃` rather than at the one value `mg-94c3` evaluated.
- I **did** re-verify `mg-d3c7`'s family independently (`s2`), which the correction did not ask
  for. That was deliberate: it is the single imported fact the `ε_leak` half of this deliverable
  rests on, and it merged 22 minutes before I was dispatched. I would make the same call again.
- The re-verification cost is where my own defect surfaced — see the instrument `README`. The
  first DP was numerically correct and exponentially slow, and only the family's large `k`
  exposed it. **A check that compares only numbers cannot see a defect that changes only cost**,
  and in this corpus cost decides which `n` a sweep reaches, which decides every `n`-freeness
  claim built on one.

The framing error cost nothing here. Recorded so the count is honest either way.
