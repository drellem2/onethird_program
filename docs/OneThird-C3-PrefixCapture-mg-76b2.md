# OneThird — `C₃` IS NOT AN INDEPENDENT UNKNOWN. It is `1` **IN CHAIN (III)'s CURRENCY — the loss inside the Cheeger square, `Φ_pref ≤ √(2C₃ε_spec)`, which is `Op-Form §4.3`'s displayed relation** — under the lemma the architecture already requires; **CHAIN (II) DOES NOT INHERIT IT — the gap-form `C₃` is NOT 1 under L2, it is measured at `1.500, 1.473, 1.990, 2.386` and RISING**; and the reading Op-Form calls "too weak to use" is usable

**Work item.** `mg-76b2` (repo `onethird_program`). Filed by `pm-onethird` as the item
`mg-845e` reserved and declined to attempt.
**Instrument.** [`code/c3_prefix_capture_76b2/`](../code/c3_prefix_capture_76b2/) —
predictions committed at `0cfae5f` before any script of it existed; scoring in that
directory's `README` §3.
**Calibration used, per the ticket's instruction to say which.** `ε_leak = 0.20`
(mg-e35c F5's repaired value; **EMPIRICAL**, resting on mg-3ce3's envelope: 0 RED events
across 6681 posets up to `ε = 0.20`). Every number derived from it inherits that status,
and the symbolic form is kept beside every number.
**Amended at `mg-01ea`, after the independent audit `mg-94c3` (`c80a4f1`) CONFIRMED it.**
Four changes, all to **how this document is stated** and none to what it says: `C1` names the
**currency** in the title, the §0 verdict, the §3 theorem and ledger claim 6, and says that
**chain (II) does not inherit `C₃ = 1`**; `C2` reconciles §5's prose threshold `c > 0.80`
with the instrument's `c ≥ 40/49 = 0.8163`; `C3` records that §7's `C₃^cut` must be
**SQUARED** to meet §6's `C₃`; and one correction **in this document's favour** records that
its monotonicity census `1890 / 3340 / 0` is the correct one and the auditor's is the
conservative one. **The theorem, §6, §7 and all 16/16 of §7's independently reproduced
figures stand unchanged.**

> **CURRENCY BANNER — READ BEFORE QUOTING ANY `C₃` FROM THIS DOCUMENT (`mg-94c3` `C1`).**
> Every unqualified `C₃ = 1` here means `C₃^(III)`: *there is a prefix `A_k` with
> `Φ_P(A_k) ≤ √(2(1−λ_std))`*. That is the `C₃` the ticket's relation
> `n ≥ 4C₃/ε_leak² − 1` carries, and `mg-94c3` confirms it at **1032 of 1032** primitive
> posets exhibiting L2's first disjunct, worst ratio `0.2603`. **It is not uniformly 1 in
> either of the other two currencies `Op-Form §4.3` puts on the table, and not even where L2
> holds:** over those
> same 1032 posets the **gap-form** `C₃` (`1−ρ_pref ≤ C₃(1−λ_std)`, §4.3's own repair, named
> in the same sentence) exceeds 1 at **1023 of 1032** and runs `1.500, 1.473, 1.990, 2.386`
> — **rising** — and `C₃^cut` (`Φ*_pref/Φ*`, L3's own wording) exceeds 1 at **10 of 1032**.
> **CHAIN (II) THEREFORE DOES NOT INHERIT THIS RESULT.** §6 below proves chains (II) and
> (III) differ by `2/ε_leak = 10` at every `C₃`, so a reader who substitutes an unqualified
> `C₃ = 1` into chain (II) gets `ε_dem = ε_leak = 0.20` and a window of `n ≤ 8` instead of
> `n ≤ 98` — a `10×` overclaim, and the gap-form measurement above makes that substitution
> **false**, not merely unlicensed.

---

## 0. Verdict

> **`C₃ = 1`, uniformly in `n`, under either disjunct of L2 — IN CHAIN (III)'s CURRENCY,
> `Φ_pref ≤ √(2C₃ε_spec)`, WHICH IS `Op-Form §4.3`'s DISPLAYED RELATION AND IS THE ONLY ONE
> OF THE THREE IN WHICH IT IS UNIFORMLY 1 — and L2 is Step 3 of the architecture, already required,
> already on the programme's own list of open lemmas.**
>
> **And that currency qualification is load-bearing, not pedantry.** `C₃ = 1` is a statement
> about the loss spent *inside* the Cheeger square. **It is NOT 1 in the gap-form
> `1−ρ_pref ≤ C₃(1−λ_std)` that `§4.3` names in the same sentence** — `mg-94c3 §3` measures
> that one at `1.500, 1.473, 1.990, 2.386` over `n = 3..6`, exceeding 1 at **1023 of the 1032**
> primitive posets that *exhibit* L2's first disjunct, and rising; nor is
> `C₃^cut = Φ*_pref/Φ*` always 1 there (up to `10/9`, at 10 of 1032). **Chain (II) does not
> inherit this result**, and §6 below is what proves why it cannot: chains (II) and (III)
> differ by `2/ε_leak = 10` at every `C₃`, so substituting `C₃ = 1` into (II) yields
> `ε_dem = ε_leak = 0.20` and a window of `n ≤ 8` in place of `n ≤ 98`. The gap-form
> measurement is what makes that substitution **false** rather than merely unlicensed.
>
> This is the ticket's **third** disjunct — *"a demonstration that `ε_dem` can be reached
> WITHOUT `C₃` at all"* — and `mg-845e` names the same disjunct as its own second unblock
> condition, so it discharges both. It is **not** a bound on the Prefix-capture
> conjecture: it is the observation that the programme was being **billed twice for one
> conversion**.
>
> Cheeger's hard direction is *proved by sweeping*, and the sets it sweeps are threshold
> sets of the dominant standard eigenvector. If that eigenvector is monotone along `e` —
> which is exactly L2's first disjunct and Step 3's first clause — then every set the
> sweep visits **is already a prefix or a suffix**, and `Φ_P` is a function of the cut, not
> of the side. "Restricting the Cheeger sweep to prefixes" therefore costs a factor of
> **exactly 1**. Under L2's *second* disjunct ("or at least yields a low-conductance
> prefix") there is no `C₃` either, because the prefix is the output.
>
> **So `ε_dem = ε_leak²/2` with no `C₃` in it — which is `2×10⁻²`, the figure `STATE.md`
> already carries.** `STATE.md:164`'s rider that *"the live `ε_spec ≲ 2×10⁻²` is the
> `C₃ = 1` value and `C₃ ≥ 1`, so the omission runs **optimistic**"* is the one sentence
> this ticket corrects: the omission is not optimistic, it is **correct**, and it is
> correct for a reason — under the architecture's own Step 3 there is nothing to omit.
>
> **Two further results, both negative-direction and both about `Op-Form §4.3`:**
>
> 1. **"As literally worded, prefix capture is too weak to use" does not survive the
>    mg-e35c calibration repair.** The literal form `ρ ≥ c·λ_std` closes the chain for
>    **every** `c > 1 − ε_leak`, giving `ε_dem = 1 − (1−ε_leak)/c`. At the repaired
>    `ε_leak = 0.20` that threshold is `c > 0.80`; at the superseded `ε_leak = 0.02` it was
>    `c > 0.98`. *(`0.80` is the **existence** threshold, `ε_dem > 0`. Evaluated at the
>    `C₃`-free chain's own budget `ε_spec = ε_leak²/2 = 2×10⁻²`, the **self-consistent**
>    threshold is the tighter `c ≥ (1−ε_leak)/(1−ε_spec) = 40/49 = 0.8163`, and that is the
>    one the instrument and §7's column use. §5 reconciles them; neither moves this
>    verdict.)* §4.3's verdict was reached against the superseded number — the
>    supersession banner at the head of that document lists §§6.4–7.4 and §10, and **§4.3
>    is not among them**, and claim 15 still carries `PROVEN` with the audit's `CONFIRMED`
>    beside it. The correct verdict is **UNQUANTIFIED at a now-explicit threshold**, not
>    *too weak*. And at `c → 1` — the conjecture's *own* alternative wording, `1−o(1)` —
>    the literal reading is the **strongest** of the four chains, not the weakest, because
>    it never spends the Cheeger square.
> 2. **The ticket's relation is the most pessimistic of four inequivalent chains.**
>    `ε_dem = ε_leak²/(2C₃)` belongs to a *degraded-prefix-Cheeger* reading. The
>    **gap-form** repair that §4.3 names in the same sentence gives `ε_dem = ε_leak/C₃`,
>    which is weaker by the factor `2/ε_leak = 10`. §4.3 says *"under **either** repair …
>    giving `ε_spec ≤ ε_leak²/(2C₃)`"*; that relation follows from one of the two repairs
>    and not from the other.
>
> **The finite window, which is the other half of what the ticket asked.** Under the
> `C₃`-free chain and *if* the mg-200d route survives mg-131e, the demand `2/(n+1) ≤ ε_dem`
> is met from **`n ≥ 99`**, so the window still owed is **`n ≤ 98`** — at `ε_leak = 0.20`,
> symbolically `n ≥ 4/ε_leak² − 1`. Not `100·C₃ − 1` with `C₃` unknown.
>
> **What this does NOT do.** It does not prove L2, and it does not bound the Prefix-capture
> conjecture. It shows the two gates are **one gate**, so `mg-845e`'s gate list shrinks
> from `{ε₀, C₃}` to `{ε₀, L2}` — and L2 was already on the programme's list of four main
> open lemmas before this ticket was filed.

---

## 1. What the ticket asked, and what the source actually says

The ticket's facts are `Op-Form §4.3` and `§8.1`: `C₃` is UNQUANTIFIED, `C₃ ≥ 1`, its
source conjecture is OPEN, and as literally worded it is too weak to use.

The source (`spectral_near_ordinal_sum_program.tex`, 603 lines) has four main open lemmas.
Two of them are in play here, verbatim (`:560–566`):

> **L2. Monotonicity/prefix lemma.** A dominant standard eigenvector is monotone in the
> distinguished order, **or at least yields a low-conductance prefix**.
>
> **L3. Prefix Cheeger lemma.** The Cheeger sweep can be restricted to prefixes with
> quantitatively controlled loss.

and Step 3 and Step 4 of the architecture (`:499–507`):

> **Step 3.** Prove that the dominant standard eigenvector is monotone in `e`, or directly
> produce a low-conductance prefix.
>
> **Step 4.** Apply Cheeger sweeping to obtain `A_k = {1,…,k}`, `Φ_P(A_k) ≲ √ε`.

**Step 4 already writes the output as a prefix, and attaches no constant to it.** The
constant `C₃` is not in the source at all; it is `Op-Form §4.3`'s name for L3's
"quantitatively controlled loss", quantified by the empirical **Prefix-capture**
conjecture (`:360–364`, verbatim):

> A threshold cut of the dominant standard eigenvector gives a prefix `A_k` whose Rayleigh
> quotient captures a constant fraction, or possibly `1−o(1)`, of the dominant standard
> eigenvalue.

And 30 lines earlier the source says, in its own voice, what supplies the prefix
(`:328–332`, verbatim):

> **Remark.** Cheeger theory does not by itself imply that the cut is a prefix. That
> requires **monotonicity of the dominant standard eigenvector in the distinguished
> order**, or a direct prefix theorem.

**The source names monotonicity as the mechanism and attaches no loss to it.** `Op-Form
§4.3` routes the same conversion through Prefix-capture instead and charges `C₃` for it.
That is the double-billing this document is about. *(This remark was read by hand and
recorded as `PREDICTIONS.md` H6 before any script existed.)*

---

## 2. The dictionary — without it, nothing about `C₃` is checkable

`Op-Form §4.3` reasons entirely in the currency of the **prefix Rayleigh quotient**
`ρ(A_k)`; the architecture consumes the **conductance** `Φ_P(A_k) = Δ₁(A_k, A_kᶜ)`.
Nothing in the corpus connects them: a grep for `Rayleigh` across `docs/` and `STATE.md`
returns two lines, both inside `§4.3` itself.

**Lemma 2.1 (the dictionary).** *Let `f = 1_{A_k} − (k/n)·1` be the centred prefix
indicator and `ρ(A_k) = ⟨f, S_P f⟩ / ‖f‖²`. Then*

$$1-\rho(A_k)\;=\;\frac{n\,\mathbb E_\sigma|A_k\setminus\sigma(A_k)|}{k(n-k)}\;=\;\frac{n}{\max(k,\,n-k)}\;\Phi_P(A_k),$$

*and consequently, for **every** `k`,*

$$\Phi_P(A_k)\;\le\;1-\rho(A_k)\;\le\;2\,\Phi_P(A_k).$$

*Proof.* `(I − S_P)1 = 0`, so `⟨f,(I−S_P)f⟩ = ⟨1_{A_k},(I−S_P)1_{A_k}⟩ = E|A_k∖σ(A_k)|`
by the source's own identity (`:220–227`). And
`‖f‖² = k(1−k/n)² + (n−k)(k/n)² = k(n−k)/n`. Divide. `Φ_P` normalises by
`min(k, n−k)`, giving the second form; `1 ≤ n/max(k,n−k) ≤ 2` gives the third. ∎
**[PROVEN]**

**Machine check.** 0 exceptions over **25684** (poset, prefix) pairs, exactly, across every
poset on `{0..n−1}` with the identity a linear extension, `n = 2..6` (**5230** posets); and
`⟨1_A,(I−S_P)1_A⟩ = E|A∖σ(A)|` on **310404** (poset, cut) pairs, computed from the matrix
on one side and from the definition on the other. **The upper factor 2 is attained
exactly**, at `k = n/2`, in 5866 of the 25684 cases.

> ⚠ **A slip of mine, kept.** `PREDICTIONS.md` H1 wrote this as `n·Φ/(n−k)` for all `k`.
> That is the `k ≤ n/2` case only — the `min` in `Φ_P`'s normalisation switches sides at
> the median. The machine caught it on **9909** failing pairs before the general form was
> written. H8 carries the identical slip about the antichain (`(n−|A|)/n`, correct only
> below the median; the general form is `max(|A|,n−|A|)/n`) and a red drill caught that
> one. Both are kept as written in `PREDICTIONS.md`.

**Why it matters.** With Lemma 2.1, "a bound on `1−ρ`" and "a bound on `Φ`" are the same
statement up to a factor 2, so `§4.3`'s Rayleigh-quotient arithmetic becomes arithmetic
about the quantity Step 5 actually consumes — and the four chains of §5 become
distinguishable. Without it they are not.

---

## 3. The theorem

**Lemma 3.1 (the sweep is over threshold sets).** *Let `v ∈ H` attain
`1 − λ_std = min_{f∈H} ⟨f,(I−S_P)f⟩/‖f‖²`. Then some **threshold set** `S = {i : v_i > t}`
or `{i : v_i < t}` with `0 < |S| ≤ n/2` satisfies `Φ_P(S) ≤ √(2(1−λ_std))`.*

*Proof.* This is the standard proof of the hard half of the Cheeger sandwich the source
quotes at `:317–324`, written out because the source quotes only the inequality. Let `m` be
a median of `v`, chosen so `|{v>m}| ≤ n/2` and `|{v<m}| ≤ n/2`, and `g = v − m`. Energy is
unchanged by the shift and `‖g‖² = ‖v‖² + nm² ≥ ‖v‖²` because `v ⊥ 1`, so
`R(g) ≤ R(v) = 1−λ_std`. Split `g = g₊ − g₋`. Edgewise
`(g₊(i)−g₊(j))² + (g₋(i)−g₋(j))² ≤ (g_i−g_j)²` and `‖g₊‖² + ‖g₋‖² = ‖g‖²`, so by the
mediant inequality `min(R(g₊), R(g₋)) ≤ R(g)`. Let `h` be the smaller one; it is
non-negative and supported on `≤ n/2` vertices. Write `E(h) = Σ_{\{i,j\}} a_{ij}(h_i−h_j)²`
with `a_{ij}` the source's weights (`:205–216`), and `d_i = Σ_{j≠i} a_{ij} = 1 − (S_P)_{ii} ≤ 1`
since `S_P` is an average of permutation matrices. Then by Cauchy–Schwarz

$$\sum_{\{i,j\}}a_{ij}\bigl|h_i^2-h_j^2\bigr|\;\le\;E(h)^{1/2}\Bigl(2\sum_i d_i h_i^2\Bigr)^{1/2}\;\le\;\sqrt{2\,E(h)\,\|h\|^2},$$

and the coarea formula applied to the level sets of `h²` gives

$$\min_t \Phi_P(\{h^2>t\})\;\le\;\frac{\sum_{\{i,j\}}a_{ij}|h_i^2-h_j^2|}{\|h\|^2}\;\le\;\sqrt{2R(h)}\;\le\;\sqrt{2(1-\lambda_{\mathrm{std}})}.$$

Every `{h² > t}` is a level set of `h`, hence a level set of `v` (upward for `g₊`, downward
for `g₋`), and is contained in `supp(h)`, so has size `≤ n/2`. ∎ **[PROVEN]**

**Lemma 3.2 (`Φ_P` is a function of the cut, not the side).** *`|A∖σ(A)| = |Aᶜ∖σ(Aᶜ)|`
for every permutation `σ` and every `A`.* Immediate from `|A∖σ(A)| = |σ(A)∖A| = |Aᶜ∩σ(A)|`.
**[PROVEN]** — machine-checked on **48616** (permutation, cut) pairs over all 872
permutations to `n = 6`, 0 exceptions. Since `Δ₁` normalises by `min(|A|,|Aᶜ|)`, which is
also symmetric, **a low-conductance suffix of size `≤ n/2` delivers Step 5's own quantity
`Δ₁(A_k, A_kᶜ)` at the complementary prefix, with no loss and no further argument.**

*(This was `PREDICTIONS.md` P13 — the error I bet 15% on. The worry is refuted.)*

**Lemma 3.3 (monotone ⟹ prefix).** *If `v₁ ≤ v₂ ≤ … ≤ v_n` then every threshold set of `v`
is a suffix and every co-threshold set is a prefix.* Immediate. **[PROVEN]** —
machine-checked on 1435 threshold sets over 301 monotone rational functions, `n = 2..7`.

> A defect of this instrument sits precisely here and is kept in the source. The first
> version of the sweep routine returned *slices of the sorted order* rather than level
> sets. Where `v` ties — and the antichain's dominant eigenvector `(a,a,a,−3a)` ties
> everywhere — a slice **splits the tie** and returns sets no threshold produces. That
> produced three spurious "monotone sweeps landing outside the prefix family". **An
> order-slice is not a level set.** The sets were the artifact; the theorem was not.

### THEOREM. Under L2, `C₃^(III) = 1`, uniformly in `n` — in chain (III)'s currency, `Φ_pref ≤ √(2C₃ε_spec)`, and in that one only.

*Assume L2's first disjunct: some dominant standard eigenvector `v` is monotone along `e`.
Then Lemma 3.1 produces a threshold set `S` of `v` with `|S| ≤ n/2` and
`Φ_P(S) ≤ √(2(1−λ_std))`; Lemma 3.3 makes `S` a prefix or a suffix; Lemma 3.2 makes the
suffix case deliver the complementary prefix at the same number. Hence there is a prefix
`A_k` with*

$$\Delta_1(A_k,A_k^c)\;=\;\Phi_P(A_k)\;\le\;\sqrt{2(1-\lambda_{\mathrm{std}})}\;\le\;\sqrt{2\,\varepsilon_{\mathrm{spec}}}.$$

*L3's "quantitatively controlled loss" is a factor of **exactly 1**, and `Step 4`'s
`Φ_P(A_k) ≲ √ε` is recovered verbatim, constant `√2`. Under L2's second disjunct the
prefix is the output and there is no conversion to charge for at all.* **[PROVEN, given L2 —
in chain (III)'s currency. The displayed conclusion is a statement about `Φ_P(A_k)` under a
square root, which is what chain (III) consumes; it says nothing about the gap-form
`1−ρ_pref ≤ C₃(1−λ_std)` of chain (II), whose constant `mg-94c3 §3` measures at `> 1` at
1023 of the 1032 primitive posets that exhibit this theorem's own hypothesis.]**

**Uniform in `n` — the statement the ticket asks for explicitly.** `C₃ = 1` is a constant.
Not a constant that happens to be small at the `n` we can enumerate: **the proof contains
no `n`-dependent step**. Lemma 3.1's constant is `2` from Cheeger, Lemma 3.2 is an identity
of finite sets, Lemma 3.3 is a statement about orderings. So `4C₃/ε_leak² − 1` is a genuine
bound and not an implicit inequality. This is the one place where "is it uniform in `n`?"
has a clean answer in this ticket, and it has it because the answer is `1`.

**Machine corroboration.** At every poset in the 5230-poset population with an exhibited
monotone dominant eigenvector and a positive gap, the sweep of that eigenvector landed on a
prefix-or-suffix cut: **1037 of 1037**, worst `Φ²/(2(1−λ_std)) = 0.347`. Red drills confirm
the hypothesis is doing work — a non-monotone vector's threshold sets *do* leave the prefix
family, and **468 of 5230** posets have `Φ*_prefix > Φ*` strictly, so the prefix
restriction genuinely can cost something. What rescues it is that the sweep of a monotone
eigenvector never proposes the offending cut.

---

## 4. What this does and does not buy `mg-845e`

`mg-845e`'s gate is *"(a) L4's consumable threshold `ε₀` … AND (b) `C₃` quantified at a
usable strength. Both."*

**Clause (b) is discharged in the form `mg-845e` itself names** — its second unblock
disjunct, *"a demonstration that `ε_dem` can be reached WITHOUT `C₃`"*. `ε_dem = ε_leak²/2`
follows from L2 alone.

**And it is not a shell game, for three reasons.**

1. **L2 was already required.** It is Step 3 of the architecture and one of the four main
   open lemmas (`:560–562`). The chain cannot reach a prefix without it under *any*
   reading. Prefix-capture, by contrast, is an additional empirical conjecture from a
   section titled *"Empirical structural conjectures"*.
2. **Both disjuncts of L2 kill `C₃`.** Monotonicity gives `C₃ = 1`; "or directly produce a
   low-conductance prefix" gives no `C₃` at all. There is no branch of L2 under which a
   separate `C₃` has to be quantified.
3. **The route that pays `C₃` is strictly worse.** It proves neither disjunct of L2 and
   invokes an extra open conjecture on top, and — §6 — under the reading `§4.3`'s displayed
   relation belongs to, it charges the prefix loss *and* the Cheeger square.

So the honest bookkeeping is: **`mg-845e`'s gate list shrinks from `{ε₀, C₃}` to
`{ε₀, L2}`, and the number of unquantified constants in the chain drops by one.** L2 is not
proved here and this document does not claim it is.

**L3 is not an independent lemma.** Given L2, L3 holds with loss 1. The programme has four
main open lemmas and **three independent ones**; L3 as stated is a consequence of L2 and
should be recorded as such rather than carried as a separate unquantified constant.

---

## 5. `Op-Form §4.3`'s literal-reading verdict does not survive the calibration repair

`§4.3`'s first rider, and claim 15 of its ledger:

> As literally worded, prefix capture is too weak to use. "Captures a constant fraction
> `c<1` of `λ_std`" gives a prefix Rayleigh quotient `ρ ≥ cλ_std ≈ c`, hence `1−ρ ≈ 1−c` —
> a *constant floor*, not a small gap. **[PROVEN — arithmetic on the stated form]**

The arithmetic is right. **The conclusion does not follow.** Write it out with the
dictionary (§2) attached:

$$1-\rho\;\le\;1-c\,\lambda_{\mathrm{std}}\;\le\;1-c(1-\varepsilon_{\mathrm{spec}})\;=\;(1-c)+c\,\varepsilon_{\mathrm{spec}},$$

and `Φ_P(A_k) ≤ 1−ρ`. The consumer does not need a vanishing quantity: Step 5 needs
`Φ_P(A_k) ≤ ε_leak` for an **absolute constant** `ε_leak` — and it is `Op-Form §3.2`, in
the same document, that establishes `ε_leak` is an absolute constant. **A constant floor
below a constant ceiling is usable.** Solving:

$$\boxed{\;\varepsilon_{\mathrm{dem}}\;=\;1-\frac{1-\varepsilon_{\mathrm{leak}}}{c},\qquad\text{usable for every }c\;>\;1-\varepsilon_{\mathrm{leak}}.\;}$$

**[PROVEN — arithmetic, given Lemma 2.1]**

> **The two thresholds on `c`, reconciled (`mg-94c3` `C2`, landed at `mg-01ea`).** This
> document quotes **two** different thresholds on `c` and they are different numbers, both
> read off the same inequality `(1−c) + c·ε_spec ≤ ε_leak`. They differ in what is held fixed:
>
> - **`c > 1 − ε_leak = 0.80` — the *existence* threshold, and it is the one in the box.**
>   It is exactly the condition `ε_dem > 0`, i.e. that there is **some** positive spectral
>   budget at which the literal reading closes. Equivalently it is the `ε_spec → 0` limit of
>   the condition. It is the right thing to state symbolically, because it carries no
>   supply-side number inside it.
> - **`c ≥ (1−ε_leak)/(1−ε_spec) = 0.80/0.98 = 40/49 = 0.8163` — the *self-consistent*
>   threshold, and it is the one the instrument uses.** It is the same condition evaluated at
>   a specific budget rather than at zero: substitute the `C₃`-free chain's own
>   `ε_spec = ε_leak²/2 = 2×10⁻²` and solve for `c`. It is necessarily the tighter of the two,
>   because a chain that must also absorb a real `ε_spec` has less of `ε_leak` left for the
>   constant floor.
>
> `s3_c3.py` sets `C_THRESH = (1−ε_leak)/(1−ε_spec)` and §7's `c below the 0.816 threshold`
> column is counted against **that** one — which is why the transcript prints `0.816` where
> this prose prints `0.80`. **The transcript is right to use the tighter one:** it is the
> threshold at which the chain actually closes at the calibration this document runs at, so
> counting posets against it is the conservative count. **The verdict of this section is
> unaffected either way** — `0.8163` is still an ordinary reading of "a constant fraction",
> and it is still nowhere near the `0.98` that `§4.3`'s "too weak to use" verdict was reached
> against. (`mg-94c3` reproduces the column's four figures `1/3, 5/26, 39/274, 523/4069`
> exactly, on code that never read this document.)

| `c` | `ε_dem` at `ε_leak = 0.20` | window `n ≤` | `ε_dem` at the superseded `ε_leak = 0.02` |
|---|---|---|---|
| `0.80` | `0` — does not close | — | does not close |
| `0.82` | `1/41` | 80 | does not close |
| `0.85` | `1/17` | 32 | does not close |
| `0.90` | `1/9` | 16 | does not close |
| `0.95` | `3/19` | 11 | does not close |
| `0.99` | `19/99` | 9 | `1/99` → 196 |
| `1.00` | `1/5` | 8 | `1/50` → 98 |

**Two things this table says.**

1. **The threshold on `c` moved 0.98 → 0.80 with mg-e35c F5's 100× repair.** `c > 0.98` is
   not an ordinary reading of "a constant fraction"; `c > 0.80` is. `§4.3` was written
   against the superseded calibration and **has never been re-examined against the repaired
   one**: the supersession banner at the head of `Op-Form` lists §§6.4–7.4 and §10, §4.3 is
   not among them, ledger claim 15 still reads `PROVEN`, and the independent audit
   `CONFIRMED` it and called it *"the second durable win"*. The audit confirmed the
   arithmetic, which is correct; the usability verdict is what the repair moves.
2. **At `c → 1` the literal reading is the STRONGEST of the four chains.** `ε_dem → ε_leak
   = 0.20`, against `0.02` for the `C₃`-free monotone-sweep chain — a factor of
   `2/ε_leak = 10` — because it never spends the Cheeger square. And `c → 1` is the
   conjecture's *own* alternative wording, `1−o(1)`, which `§4.3` describes as "the
   gap-form in disguise". It is not in disguise; it is a *better* form than the gap-form,
   for the same reason.

**The correct verdict on the literal reading is `UNQUANTIFIED at a now-explicit
threshold`, not `too weak to use`** — and that is an actionable difference, because `c` is
measurable and the source's own computational programme item 7 already calls for measuring
it ("the best cut and best prefix Rayleigh quotients").

---

## 6. Four chains, four relations, and the ticket's is the most pessimistic

| | what it bounds | `ε_dem` | window `n ≥` | `C₃`? |
|---|---|---|---|---|
| **(I) monotone sweep** (this document, §3) | `Φ ≤ √(2ε_spec)` | `ε_leak²/2` | `4/ε_leak² − 1` = **99** | **none** |
| **(II) gap-form prefix capture** | `Φ ≤ C₃·ε_spec` | `ε_leak/C₃` | `2C₃/ε_leak − 1` = `10C₃−1` | linear |
| **(III) degraded prefix Cheeger** (the ticket's — **and the currency §3's theorem sets to 1**) | `Φ ≤ √(2C₃ε_spec)` | `ε_leak²/(2C₃)` | `4C₃/ε_leak² − 1` = `100C₃−1` | linear |
| **(IV) literal prefix capture** (§5) | `Φ ≤ 1−c(1−ε_spec)` | `1 − (1−ε_leak)/c` | `2/ε_dem − 1` | threshold on `c` |

`(III)` at `C₃ = 1` **is** `(I)`. So the ticket's relation is the `C₃`-free chain with a
factor `C₃` inserted at the one place the `C₃`-free chain does not have one — correct
bookkeeping *if and only if* the prefix restriction really does degrade the gap, which
under L2 it does not. **This row, and only this row, is where §3's theorem sets `C₃` to 1.
Row (II) keeps its own `C₃`, which is a different number and is not 1** — see the currency
banner at the head of this document and `mg-94c3 §3`.

**`(II)` is not `(III)` with `C₃` moved.** The gap-form repair — `§4.3`'s own wording,
`1−ρ_prefix ≤ C₃(1−λ_std)` — supplies the **prefix itself**, so Cheeger's square, which is
the price of turning an eigen*value* into a *set*, is never paid: `Φ ≤ 1−ρ ≤ C₃·ε_spec`
directly, by Lemma 2.1. `§4.3` writes *"under **either** repair the loss is a constant
`C₃`, giving `ε_spec ≤ ε_leak²/(2C₃)`"*. That relation follows from the
degraded-prefix-Cheeger repair and **not** from the gap-form repair named in the same
sentence. The two differ by `2/ε_leak = 10` at every `C₃`.

*(This is `PREDICTIONS.md` P14 — the error I bet 25% on, "dropping a Cheeger square the
chain really needs", which is the shape of the conflation this lineage has committed twice
already. It is answered by **enumerating all four chains and labelling which reading each
belongs to**, rather than by asserting that one of them is *the* relation. If a reader
holds a fifth reading, the table is where it should be added.)*

---

## 7. What the machine measured, and why none of it is a bound

Every figure in this section is measured **outside the regime it would be used in**, and
`s3` prints that sentence next to each one rather than once at the top.

**The population is the wrong population, and exactly how is now known.** Three
independent **exact** predicates — the weighted graph `a_ij` is disconnected; the poset has
an ordinal-sum cut point; `Φ* = 0` — **agree on all 5230 posets, 0 disagreements**. So
`1 − λ_std = 0` precisely on the ordinal-sum-decomposable posets, where every currency of
`C₃` is `0/0` and Step 5's conclusion already holds exactly. Restricting to the **4377
primitive** posets: **0 of them** have `1 − λ_std ≤ 2×10⁻²`; the smallest gap in the
population is `0.0562` at `n = 6`. This corroborates mg-c4f5 / mg-e35c A1 from a different
direction — the master bound excludes the target for non-chain posets on `n ≤ 10`
(`n ≤ 100` primitive), and here the **spectral quantity itself** never gets near it.

| quantity | `n=3` | `n=4` | `n=5` | `n=6` | direction |
|---|---|---|---|---|---|
| `max C₃^cut = Φ*_pref/Φ*` (EXACT) | `1` | `3/2` | `6/5` | `15/8` | **up**, not monotone |
| `max C₃^gap` (FLOAT gap) | `1.500` | `1.473` | `1.990` | `2.386` | **up** |
| `min c` (literal fraction) | `0.750` | `0.618` | `0.536` | `0.453` | **down** |
| `c` below the `0.816` threshold | 1/3 | 5/26 | 39/274 | 523/4069 | — |

> **`C₃^cut` MUST BE SQUARED TO MEET §6's `C₃` (`mg-94c3` `C3`, landed at `mg-01ea`).**
> `s3_c3.py`'s docstring carries this sentence and this document did not: `C₃^cut` is spent
> **inside** the Cheeger square, `Φ*_pref ≤ C₃^cut · Φ* ≤ C₃^cut · √(2(1−λ_std))`, i.e.
> `Φ*_pref ≤ √(2·(C₃^cut)²·(1−λ_std))`, **so `Op-Form`'s chain-(III) `C₃` is the SQUARE of
> `C₃^cut`.** A reader comparing this row's `max C₃^cut = 15/8` directly against §6's
> chain-(III) `C₃` is off by exactly that square: `15/8 → 225/64 ≈ 3.52`. The row is printed
> in `C₃^cut` because that is L3's own wording — the ratio of best-prefix to best-cut
> conductance — and the conversion is here rather than left to the script.
> **`C₃^gap` needs no such conversion:** it is the chain-(II) constant and enters
> `Φ ≤ 1−ρ ≤ C₃^gap·ε_spec` linearly, with no Cheeger square to be spent inside.
> *(The `0.816` in the last row is the self-consistent threshold `(1−ε_leak)/(1−ε_spec) =
> 40/49`, not §5's prose `0.80`; §5 reconciles them.)*

**Neither `C₃^cut` nor `C₃^gap` is a bound and neither can be.** A finite population can
**refute** a bound uniform in `n` and can never establish one. What these rows show is the
direction of travel, and in every currency it is the wrong way. **This is a negative result
about the routes that carry a `C₃`, and it is reported as one** — it is also why the
theorem of §3, which carries no `C₃`, is the load-bearing part of this document.

**The theorem's own hypothesis, tested honestly.** Monotonicity of the dominant standard
eigenvector is a **minority** property over the whole population — 1890 YES / 3340 NO /
0 UNDECIDED, 36.1%. I predicted the opposite (`PREDICTIONS.md` P7) and it is kept as
written. But the conjecture is stated *for a minimal counterexample*, where the gap is
small, and stratified by gap it goes the right way:

| `1 − λ_std` band | primitive posets | monotone |
|---|---|---|
| `[0.00, 0.25)` | 2284 | 810 — **35.5%** |
| `[0.25, 0.50)` | 1860 | 216 — 11.6% |
| `[0.50, 0.75)` | 223 | 6 — 2.7% |

and **28 of the 50 primitive posets with the smallest positive gap are monotone** — a
majority. Monotonicity concentrates exactly where L2 claims it. **[HEURISTIC — this is a
correlation over a population that contains no poset in the regime, and it is not evidence
for L2 at unbounded `n`.]** 163 of 5230 posets have a degenerate top standard eigenvalue,
where "*the* dominant eigenvector" is not well defined; the test used is existential, as
L2's own wording is, and returned `UNDECIDED` 0 times.

> **THIS CENSUS IS CORROBORATED BY AN INDEPENDENT ONE, AND `1890 / 3340 / 0` IS THE RIGHT
> ANSWER (`mg-94c3 §0.4`, landed at `mg-01ea`).** `mg-94c3`'s census, on code sharing no
> line with `lib76b2`, reads **1727 YES / 3340 NO / 163 UNDECIDED**, and
> **`1727 + 163 = 1890` exactly**. The 163 are precisely the degenerate top eigenspaces named
> in the paragraph above: `mg-94c3`'s test declines them by its own declared policy (`B3`),
> whereas the existential search used here — existential because **L2's own wording is
> existential**, *"a dominant standard eigenvector is monotone"* — resolves every one of them
> as YES. The `NO` count agrees exactly. **The auditor records its own number as the
> conservative one and this document's as the correct one**; the `0 UNDECIDED` above is a
> property of the stronger test, not an unreported gap in it.

---

## 8. An observation outside this ticket's scope, reported where it was found

`lib2de0.E_leak(A)` computes `|A| − |A ∩ set(p[:|A|])|` — the first `|A|` **positions**
rather than the positions indexed by `A`. For a prefix the two agree; `lib2de0.phi_star()`
calls it on **every** subset. Measured: the two diverge on **8178 of 11316** (poset, cut)
pairs at `n ≤ 5`. Smallest witness: the 2-chain `0 < 1` with `A = {1}`, where the definition
gives `0` and the other convention gives `1`. Both natural readings of `σ(A)` (image of a
position set; image of an element set) give `0` here, because they differ by `σ ↔ σ⁻¹` and
`|A∖σ(A)| = |A∖σ⁻¹(A)|`; the `set(p[:|A|])` convention is neither. The definition used here
is independently confirmed against the source's own matrix identity (`:220–227`) on 310404
(poset, cut) pairs.

**NOTED AND NOT REPAIRED.** `code/direct_prefix_audit_2de0/` is mg-2de0's file and this
ticket does not own it. What it touches — whether `Φ*` and mg-2de0's P9 are affected — is
not assessed here. *(Flagged in advance as `PREDICTIONS.md` H7/P11, before the instrument
existed.)*

---

## 9. Claim ledger

| # | claim | § | label |
|---|---|---|---|
| 1 | `1−ρ(A_k) = n·E\|A_k∖σ(A_k)\|/(k(n−k)) = n·Φ_P(A_k)/max(k,n−k)` | 2 | **PROVEN**, 0/25684 exact |
| 2 | `Φ ≤ 1−ρ ≤ 2Φ` for every `k`; the factor 2 is attained at `k=n/2` | 2 | **PROVEN**, 0/25684 exact |
| 3 | Cheeger's hard half is proved by sweeping threshold sets of `v`, `\|S\| ≤ n/2` | 3.1 | **PROVEN** (standard; written out because the source quotes only the inequality) |
| 4 | `\|A∖σ(A)\| = \|Aᶜ∖σ(Aᶜ)\|`, so `Φ_P` is a function of the cut | 3.2 | **PROVEN**, 0/48616 exact |
| 5 | monotone `v` ⟹ every threshold set is a prefix or a suffix | 3.3 | **PROVEN** |
| 6 | **L2 ⟹ `C₃^(III) = 1`, uniformly in `n` — in chain (III)'s currency, `Φ_pref ≤ √(2C₃ε_spec)`, and in that one only. Chain (II)'s gap-form `C₃` does NOT inherit it** | 3, 6 | **PROVEN, CONDITIONAL on L2** — L2 is open. Currency confirmed at 1032/1032 primitive posets exhibiting L2, worst ratio `0.2603`; the gap-form `C₃` exceeds 1 at **1023 of those same 1032** (`mg-94c3 §3`), so the (II)-substitution is **false**, not merely unlicensed |
| 7 | L2's second disjunct also removes `C₃`; both disjuncts do | 4 | **PROVEN** (reading of `:560–562`) |
| 8 | L3 is a consequence of L2, not an independent lemma | 4 | **PROVEN, CONDITIONAL on L2** |
| 9 | `ε_dem = ε_leak²/2 = 2×10⁻²`, `C₃`-free | 3, 6 | **CONDITIONAL** on 6 and on `ε_leak ≈ 0.20`, which is **HEURISTIC** |
| 10 | `STATE.md:164`'s "the omission runs optimistic" rider is wrong; the `C₃ = 1` value is the correct one | 0 | **CONDITIONAL** on 6, **and therefore on chain (III)'s currency**. `mg-94c3 §3.2` shows the two sentences are about different numbers: `:164`'s `C₃ ≥ 1` is **unconditionally** true of the *gap-form* `C₃` (0 violations over 4376 positive-gap posets, and 1 **is** attained), while this claim is true of the *chain-(III)* `C₃` **conditional on L2**. Whoever owns that row should merge them, not strike one |
| 11 | the literal reading closes iff `c > 1 − ε_leak`; `ε_dem = 1−(1−ε_leak)/c` | 5 | **PROVEN** given claim 1 |
| 12 | that threshold was `0.98` at the superseded calibration and is `0.80` at the repaired one | 5 | **PROVEN** (arithmetic). `0.80` is the **existence** threshold; the **self-consistent** one, evaluated at `ε_spec = ε_leak²/2`, is the tighter `(1−ε_leak)/(1−ε_spec) = 40/49 = 0.8163`, which is what `s3_c3.py` and §7's column use. §5 reconciles them; neither reading moves claim 13 |
| 13 | `Op-Form §4.3` claim 15's *"too weak to use"* does not follow from its own arithmetic | 5 | **PROVEN** — the arithmetic is correct, the usability verdict is not entailed by it |
| 14 | `§4.3` was never re-examined under mg-e35c F5 | 5 | **PROVEN** (the banner lists §§6.4–7.4, §10; claim 15 unamended; audit `CONFIRMED`) |
| 15 | four inequivalent chains; `§4.3`'s displayed relation belongs to (III), not to the gap-form repair it names | 6 | **PROVEN** as a disjunction over the readings enumerated; a fifth reading would go in the table |
| 16 | chains (II) and (III) differ by `2/ε_leak = 10` at every `C₃` | 6 | **PROVEN** (arithmetic) |
| 17 | window `n ≤ 98` under chain (I) | 0, 6 | **CONDITIONAL** on 9 **and on the mg-200d conjecture**, which this ticket otherwise does not use |
| 18 | `1−λ_std = 0` exactly on the ordinal-sum-decomposable posets | 7 | **PROVEN** on `n ≤ 6` (three exact predicates, 0/5230 disagreements); a statement about the population, not a theorem |
| 19 | no poset with `n ≤ 6` is inside the budget | 7 | **PROVEN** on that population (FLOAT gap, margin `0.056` vs `0.02`) |
| 20 | `max C₃^cut` and `max C₃^gap` rise with `n`; `min c` falls | 7 | **HEURISTIC** — direction only; a finite population cannot bound either. `C₃^cut` is spent inside the Cheeger square, so §6's chain-(III) `C₃` is its **SQUARE** (`15/8 → 225/64 ≈ 3.52`); `C₃^gap` is the chain-(II) constant and needs no such conversion |
| 21 | monotonicity is a minority property overall but concentrates at small gap | 7 | **HEURISTIC**. The census `1890 / 3340 / 0` is corroborated by `mg-94c3`'s independent `1727 / 3340 / 163-UNDECIDED`, where `1727 + 163 = 1890` exactly — the 163 are degenerate top eigenspaces its policy declines and this document's existential search (existential because L2's wording is) resolves as YES. **This document's number is the correct one and the auditor's is the conservative one** |
| 22 | `lib2de0.E_leak` diverges from the definition on non-prefix cuts | 8 | **PROVEN**, 8178/11316; consequences **NOT ASSESSED** |
| 23 | L2 itself | — | **OPEN. NOT TOUCHED.** |
| 24 | L4's threshold `ε₀`, `mg-845e`'s clause (a) | — | **OPEN. NOT TOUCHED** — see §11 |

---

## 10. Proposal for pm-onethird — stated as a proposal, not an edit

**Nothing here has been written into `STATE.md`.** `:15` (row 8) and `:164` (mg-345e's row)
are pm-onethird's, and mg-345e owns the second.

> **Proposed amendment to `STATE.md:164`.** The rider currently reads *"the live
> `ε_spec ≲ 2×10⁻²` is the `C₃ = 1` value and `C₃ ≥ 1`, so the omission runs **optimistic**"*.
> Under mg-76b2 the omission is **not** optimistic: `C₃ = 1` is the correct value under
> either disjunct of L2, which is Step 3 of the architecture and one of its four main open
> lemmas, so there is nothing to omit. Suggested replacement: *"the live `ε_spec ≲ 2×10⁻²`
> is the `C₃ = 1` value, and `C₃ = 1` is what L2 delivers — Cheeger's sweep is over
> threshold sets, and a monotone dominant eigenvector's threshold sets are already
> prefixes, so the prefix restriction is free (mg-76b2). `C₃` is not an independent
> unknown; L3 is a consequence of L2. What remains gated is L2 itself and L4's threshold
> `ε₀`."*
>
> **The replacement must carry the currency, and this sentence is part of the proposal
> (`mg-94c3` `C1`, landed at `mg-01ea`).** Whoever lands the above must land it as a
> **chain-(III)** statement: *"`C₃ = 1` in the currency `Op-Form §4.3`'s displayed relation
> uses — the loss inside the Cheeger square, `Φ_pref ≤ √(2C₃ε_spec)`. It is **NOT** 1 in the
> gap-form `1−ρ_pref ≤ C₃(1−λ_std)` that `§4.3` names in the same sentence, where it is
> measured at `1.473 → 2.386` over `n = 4..6` even restricted to posets exhibiting L2
> (`mg-94c3 §3`). Chain (II) therefore does not inherit this result, and substituting
> `C₃ = 1` into it would overstate the window by `10×`."* Note also that `:164`'s existing
> `C₃ ≥ 1` is **unconditionally** true of the gap-form `C₃`, so the two sentences are about
> different numbers and should be **merged** by the owner of that row rather than one struck.
>
> **Proposed amendment to `Op-Form §4.3` / ledger claim 15.** Claim 15's arithmetic stands;
> its verdict does not. Suggested: `PROVEN as arithmetic; the usability verdict is
> SUPERSEDED by mg-e35c F5 (mg-76b2 §5) — the literal form closes for every c > 1 − ε_leak,
> which is c > 0.80 at the repaired calibration (0.8163 = 40/49 self-consistently, at the
> budget eps_spec = eps_leak^2/2) and was c > 0.98 at the superseded one.
> The correct status is UNQUANTIFIED at an explicit threshold.` And `§4.3`'s displayed
> relation should be labelled as belonging to the degraded-prefix-Cheeger reading, since
> the gap-form repair named in the same sentence gives `ε_spec ≤ ε_leak/C₃`.
>
> **Proposed status change to `mg-845e`.** Clause (b) is discharged. The gate is
> `{L4's threshold ε₀, L2}`, both already on the programme's own open-lemma list.

---

## 11. Scope statement

One deliverable, as budgeted. Not done, and deliberately:

- **No L4 attempt.** mg-345e established that Step 6 consumes no branch in which L4's
  modulus appears; an L4 modulus result does not discharge this and none is produced here.
  L4's **threshold** `ε₀` — `mg-845e`'s clause (a) — is untouched and still gates it.
- **No `ε_sup` derivation.** That is mg-6bc2 and it landed at `e1f7bb2`.
- **L2 is not proved.** This document reduces `C₃` to L2; it does not discharge L2. §7's
  monotonicity numbers are a correlation over a population containing no poset in the
  regime, and are labelled HEURISTIC.
- **The mg-200d conjecture is not assumed.** `2/(n+1)` appears only in §6's window column
  and in claim 17, both labelled. Everything else in this document is independent of
  whether that route survives mg-131e.
- **`ε_leak = 0.20` is empirical and is not pinned here.** It is swept in `s4` (B1) rather
  than hardened, per the ticket's instruction. Every headline number is stated
  symbolically beside its value.
- **No `STATE.md` edit, no `Op-Form` edit, no `mg-845e` edit.** §10 is a proposal.
- **`lib2de0` is not repaired** and the consequences of §8 for mg-2de0's `Φ*` and its P9
  are **not assessed**.
- **`n = 7` is not swept** — ~96k posets with up to 5040 linear extensions each and an
  exhaustive `2ⁿ` cut enumeration. Every `n`-growth statement rests on `n ≤ 6` and says so.

**Scope of the `mg-01ea` amendment, added with it.** It changes **how this document is
stated and nothing it says**. No mathematics was re-derived, no script was re-run, and the
population was not re-enumerated: `mg-94c3` reproduced 16/16 of §7's tabulated figures on
code sharing no line with `lib76b2`, and that is taken as settled rather than re-checked
here. It touched **no** other file — not `STATE.md` (the landing of this result there is a
separate item), not `Op-Form`, not the instrument. The `HEURISTIC` label on §7's
monotonicity-concentrates-at-small-gap table is **kept and not softened**: `mg-94c3` ran the
red drill this document did not and found `Φ*_pref ≤ √(2(1−λ_std))` holds at all 3340
**non**-monotone primitive posets as well, so the population supplies **no separating
evidence** for the theorem. **The theorem's support is its proof (§3), not the population.**
