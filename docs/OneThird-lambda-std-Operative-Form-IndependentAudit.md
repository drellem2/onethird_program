# INDEPENDENT AUDIT — `OneThird-lambda-std-Operative-Form.md` (mg-88bd)

**Auditor.** `mg-e35c`. I did not author the target and had no contact with its author.
**Target.** `docs/OneThird-lambda-std-Operative-Form.md` @ `64463ae` (589 lines), origin/main.
**Method.** Paper-and-pencil. **Zero computation** — no scripts, no enumeration, no data. Every
number below I re-derived by hand; every quotation I pulled from the primary file myself
*before* reading the target's characterisation of it.
**Template.** STATE.md Appendix A, including step 4b (strength check + falsifier quantifier,
added at `ea46754`), plus the targeting in the mg-e35c brief.

**Process note (not a judgement on the work).** The standing pre-PM-review audit stage did not fire
for mg-88bd; it merged 13 minutes after filing and reached pm-onethird unaudited. This audit is
therefore first-line, and pm-onethird is second-line behind it rather than the only other reader.

---

## 0. Verdict

> **Overall: OVERSTATED.** Not BROKEN — the mathematics is clean and every re-derivable step
> re-derives. But three of the four headline claims are stated more strongly in §0 / §10 (the text
> proposed for STATE.md) than the body or the ledger supports, and one of them fails in the
> direction the brief asked me to watch.
>
> **Zero BROKEN mathematical claims.** I re-derived all 15 hand-checkable items independently
> (antichain conductance, antichain `λ_std` from the source's own Rayleigh form, the Cheeger
> equality, `E_unif[footrule]`, the `P_0` witness, Claim 6.1, the whole constant budget, both
> §7 arithmetic claims, the §3.3 exponents). All correct. **Two BROKEN *derivations of labels /
> attributions*** — F5 and F6 below — neither of which changes a mathematical statement.
>
> **The core verdict — the operative form is `1 − λ_std ≤ ε_spec`, absolute constant, uniform in
> `n` — is CONFIRMED, but conditionally, and the condition is heavier than the document conveys:**
> it is what the *stated* architecture consumes, and L4-as-stated (row 11, OPEN/AMBER) is the very
> thing whose provability at an `n`-free modulus is in doubt. §3.3 refutes a steelman for
> `n`-dependence; **it is not the strongest steelman** (F1).
>
> **Headline-by-headline:**
> - **"It is a FOURTH form."** OVERSTATED (F4). It is the source's *third* form — Step 2's
>   `λ_std ≥ 1 − ε`, applied to the single hypothetical minimal counterexample, where there is no
>   quantifier over `n` to be missing. The real and correct news is about the corpus's two
>   *asymptotic* renderings (STATE.md's limit, mg-7ae7's rate), both of which genuinely are
>   stronger than needed.
> - **"The `Φ → Δ₁` conversion is the identity."** **CONFIRMED, and stronger than stated** (F7):
>   the source defines `Φ_P` *only* on `0 < |A| ≤ n/2`, so the two are the same function on the
>   whole of `Φ`'s domain. The `|A| ≤ n/2` rider is not a restriction, it is the domain.
> - **"Branch (iii) does not close Step 6."** Arithmetic CONFIRMED; **framing OVERSTATED** (F2).
>   The source's *own* statement of L4 in the open-lemma list (`:567–569`, "**preserving** a
>   balanced pair from one side") and its own prose (`:476–479`, "the task is to show that the thin
>   interface **cannot destroy** all such pairs") already read as the repaired form. The document
>   cites `:556–570` in §1 and does not check L4 there. This is an internal drafting inconsistency
>   in the source, not a defect in the architecture's intent. And a **second, larger Step-6 gap of
>   the same type — branch (ii) is unconsumed — is implied by the document's own §3.3 sentence and
>   never recorded** (F3).
> - **"The weakening buys the mg-210d route nothing."** **OVERSTATED — and this is the false loss
>   the brief warned about** (F8). The route's *conclusion* survives, and survives more robustly
>   than the document argues (see F9 — it does not need the numeric budget at all). But the
>   weakening demonstrably buys something the document does not record: it converts mg-210d's
>   Residual **(R)** from *categorically* insufficient to *quantitatively* insufficient, which
>   **retires the honest caveat currently carried at STATE.md:130 and :147** ("(R) yields a constant
>   `λ_std`, which does not by itself give `δ`"). Under this document's own verdict, a constant
>   `λ_std` **is** the currency the downstream consumes. A door recorded as the wrong shape is now
>   the right shape with the wrong size.
>
> **Satisfiability (brief point 5): CONFIRMED non-trivially satisfiable**, with a hand witness the
> document does not have (§4). The document's §7.2 only excludes vacuity-*by-universality*; the
> brief asked about vacuity-*by-emptiness*, which §7.2 does not touch.
>
> **Constraint compliance: CLEAN.** One `.md` file, 589 insertions, no scripts, no data, no
> enumeration — verified against the commit, not the document's sentence. Every constant is
> hand-derivable except the two imported from mg-3ce3's already-merged table, which are
> quoted verbatim and labelled HEURISTIC.
>
> **Honest net: a genuine notation catch plus a re-pricing; not new mathematics.** The durable win
> is the `ε_spec` / `ε_leak` collision and the square between them — real, verified, and it does
> dissolve the limit-vs-rate confusion. The second durable win is §4.3's catch that Prefix-capture
> *as literally worded* is too weak to use. Both survive this audit intact.

---

## 1. What I checked against

| artifact | path | status |
|---|---|---|
| target | `docs/OneThird-lambda-std-Operative-Form.md` @ `64463ae` | 589 lines ✓ |
| canonical source | `~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex` | exists, **603 lines** ✓ (target's count is right) |
| BK side | `one_third_width_three/step8.tex` | Theorem E + `rem:n-dependence-g1` ✓ |
| L4 probe | `one_third_width_three/docs/OneThird-L4-NearOrdinalSum-Stability-Probe.md` | ✓ |
| master bound | `one_third_width_three/docs/probe-lambda-constant-bound.md` (mg-210d) | ✓ |
| corpus | `STATE.md` @ `ea46754` | ✓ |

**Every line reference in the target resolves and every quotation is verbatim.** I checked
`:229–237`, `:239–250`, `:270–278`, `:317–324`, `:360–364`, `:400–424`, `:459`, `:464–474`,
`:492–497`, `:502–507`, `:509–512`, `:514–515`, `:556–570` in the tex, `step8.tex:57–73` and
`:290–305`, and the probe's `:86–88`, `:110–116`, `:136–144`, `:149`. Citation hygiene is
**exemplary**; nothing is paraphrased into being stronger than the source. Two riders (F2, F12).

### 1.1 Constraint compliance — checked against the commit

`git show --numstat 64463ae` → `589 0 docs/OneThird-lambda-std-Operative-Form.md`. One file. The
repo has never contained a non-`.md` artifact other than `docs/state-of-the-wall.html`.
**No dataset, no script, no enumeration. CLEAN.**

Constants that could not have been hand-derived — there are exactly three, all imported and all
labelled:

| constant | provenance | verdict |
|---|---|---|
| `F(0.02) = 0.073`, `F(0.05) = 0.198` | mg-3ce3 envelope table, quoted verbatim | read-off, correctly labelled **HEURISTIC** ✓ |
| `D ≈ 0.32·ε^0.55` | mg-3ce3 power fit, quoted verbatim | read-off, correctly labelled **HEURISTIC** ✓ |
| `0 RED / 6681`, `n ≤ 16`, `ε ≤ 0.20` | mg-3ce3 results, quoted verbatim | read-off ✓ |

Everything else (`2×10⁻⁴`, `3.3×10⁻⁵`, `5×10³`, `10⁵`, `n ≥ 101`, `n^{−1.82}`, `n^{−3.64}`,
`(n²−1)/3`, `n(n²−1)/3`, `1/6`, `d·n/(n+1)`) I re-derived by hand. All correct.

**One consistency rider on the imported numbers:** §3.3 uses the *fitted* modulus and §6.4 uses the
*envelope*, and they disagree by ≈3× (fit gives `F(0.05) ≈ 0.062`, envelope gives `0.198`). Both
readings are legitimate — one is a fit through the mass, the other a worst-case envelope — but each
section picks the one that pushes its own conclusion harder (the loose fit makes the steelman look
extravagant; the tight envelope makes the budget look tiny). Not an error; worth knowing before
either number is quoted onward.

---

## 2. Press point 1 — §3.2, "the quantifier is the answer"

**The document's claim.** L4's `F` is a function of `ε` alone; therefore `ε` must be an absolute
constant below a threshold, and requiring `ε → 0` with `n` buys nothing. Labelled
*"[PROVEN — as a reading of the stated form; the reading is argued, not assumed]"*.

**Verdict: CONFIRMED as a reading. Support 1 is OVERSTATED. And §3.3 refutes the wrong steelman.**

### 2.1 The reading itself is right

I built the derivation myself from the primary text before reading §3.2. L4 (`:464–474`, verbatim,
I pulled it) is a single sentence: *"There exists `F(ε) → 0` such that if `Δ₁(A,B) ≤ ε`, then one of
(i)/(ii)/(iii)."* Its consumer, Step 6 (`:514–515`, verbatim): *"Use near-ordinal-sum stability to
transfer a balanced pair from `P[A_k]` or `P[A_k^c]` to `P`, contradicting minimality."* The
predicate contradicted is `δ(P) < 1/3` — a max over pairs of a probability against the absolute
constant `1/3`. Nothing in that sentence carries an `n`. So the threshold `ε_0` at which `F(ε_0)`
becomes small enough is `n`-free. **Support 2 is the real argument and it is sound.**

### 2.2 Support 1 ("an `n`-dependent `F` would be unstatable") is OVERSTATED

The document argues that if `F` were `F_n`, then `"F(ε) → 0"` would "have no referent" and branch
(ii) "would be a schema, not a statement". That is too strong. A doubly-indexed modulus
`F(ε, n)` with `lim_{ε→0} sup_n F(ε,n) = 0`, or with the limit taken at each fixed `n`, is an
entirely ordinary object in stability theory and is perfectly statable; branch (ii) then reads
`F(ε,n)·n` with no loss of sense. The correct and sufficient claim is the weak one: **as literally
written, `F` carries no `n`.** The document does not need the stronger version, and the stronger
version is false. Downgrade support 1 to a reading claim; support 2 carries the section alone.

### 2.3 The steelman I built before reading §3.3 — and it is not theirs (**F1**)

I was asked to rebuild the steelman independently. Mine is not the document's.

**§3.3's steelman:** a proof routes through branch **(ii)** and needs the modified set to be `O(1)`
rather than a constant fraction, forcing `F(ε)n = O(1)` hence `ε = Θ(n^{−1.82})`. §3.3 dismisses it
on the ground that *"the source never uses (ii)"* — which is correct (Step 6 consumes (i)/(iii)).

**My steelman lives inside branch (iii), the branch Step 6 *does* consume, so that dismissal does
not reach it:**

> `Δ₁(A,B) ≤ ε` says `E|A ∖ σ(A)| ≤ ε·min(|A|,|B|)`. At **fixed constant `ε`**, the expected number
> of leaked elements is `≈ εk` and **grows without bound in `n`**. Branch (iii) is the stability
> version of an exact fact: if `P = P[A] ⊕ P[B]`, then a uniform linear extension of `P` restricts
> to a uniform linear extension of `P[A]`, so `p^P_{xy} = p^{P[A]}_{xy}` *exactly*. The natural
> route to the stability version couples `σ` to a non-leaking extension — and that coupling costs
> `Pr[at least one leak]`, which is bounded by `E|A ∖ σ(A)| ≤ εk` and is therefore **vacuous once
> `k ≥ 1/ε`**. So the obvious proof of branch (iii) needs the *leaked count*, not the leaked
> *density*, to be `O(1)`: `εk = O(1)`, i.e. **`ε = O(1/n)`**.

This is the same *shape* as §3.3's objection (a count, not a density) but sited in the consumed
branch, and it needs no fitted modulus. It is the strongest form of the objection, and **§3.3 does
not state or refute it.**

**Does it overturn the verdict?** No — and I want to be exact about why, because this cuts both
ways.

- Formally it does not touch the document's claim, which is about what the *stated* L4 requires,
  and the stated L4 has an `n`-free `F` by inspection.
- Priced out, my steelman gives `ε_leak = Θ(1/n)` ⟹ `ε_spec = Θ(1/n²)` ⟹ `E[inv_e] = O(1)` — again
  stronger than LIB, again "a different programme", so the document's dismissal *conclusion* would
  have survived had it engaged this version.
- **But it is verdict-critical in one respect the document does not flag:** if L4 with an `n`-free
  modulus is *false*, the answer to the ticket's question flips from "no `n`-dependence" to "yes".
  The document's verdict is therefore conditional on an **OPEN, AMBER-rated conjecture (row 11)
  being true in its stated form** — and §3.2's own support 1 is not evidence that it is, only that
  it is what was written down. §0 and §10 assert what "the architecture requires" without that
  conditional.
- The document itself names the one cheap check that would bear on it — re-stratifying mg-3ce3's
  survival data by `n` at fixed `ε` — and correctly declines to run it under the no-computation
  directive (§7.1, §11). **That is exactly the check my steelman calls for, which makes its absence
  from §3.3 the more conspicuous.** I concur with not running it; I do not concur with §3.3's
  "the only route by which L4 could demand `ε → 0` with `n` is branch (ii)", which is a universal
  and is false.

**Ledger consequence:** the "only route" sentence is an in-prose universal that never reached the
document's own ledger. Row **P1** below.

---

## 3. Press point 2 — §2, "the `Φ → Δ₁` conversion is the identity, not a bound"

**Re-derived independently, from the source's definitions, before reading Lemma 2.1's proof.**

Source `:229–237`, verbatim:

```
Definition (Transport conductance). For 0 < |A| <= n/2, define
  Phi_P(A) = E_{sigma in LE(P)} |A \ sigma(A)| / |A|,
  Phi_P^* = min_{0 < |A| <= n/2} Phi_P(A).
```

Source `:270–278`, verbatim:

```
Definition (L^1 ordinal-sum defect).  Delta_1(A,B) = E|A \ sigma(A)| / min(|A|,|B|).
```

Numerators identical. For `|A| ≤ n/2`, `|B| = n − |A| ≥ |A|` so `min(|A|,|B|) = |A|`. Denominators
identical. **`Φ_P ≡ Δ₁` — CONFIRMED.**

**And the document understates its own lemma (F7).** `Φ_P` is defined by the source *only* on
`0 < |A| ≤ n/2`, and `Φ_P^*` is a min over exactly that range. So `|A| ≤ n/2` is not a hypothesis
restricting the identity — **it is the whole domain of `Φ_P`.** The two symbols denote the same
function everywhere both are defined. Corollary 2.2 ("Steps 4 and 5 state the same inequality about
the same number") follows: Step 4 (`:502–507`) bounds `Φ_P(A_k)`, Step 5 (`:509–512`) bounds
`E K_k` against `min(k, n−k)`, and `K_k = |A_k ∖ σ(A_k)|` (`:246`), so Step 5 is `Δ₁(A_k,A_k^c) ≪ 1`
which is `Φ_P(A_k) ≪ 1`. **Step 5 adds no bound; it re-reads Step 4. CONFIRMED.**

**Robustness note (the brief asked what re-prices if this is wrong).** Nothing does, even under
adversarial assumptions. Had the source normalised `Φ` differently — e.g. by the Buser weight
`|A||A^c|/n` used at STATE.md row 5 — the ratio to `Δ₁` would be `n/(n−k) ∈ [1,2]` for `k ≤ n/2`.
**Every plausible normalisation differs by a factor in `[1,2]`, i.e. by a constant, so the
conclusion "no `n` enters here" is safe with room to spare.** The identity is exact; its role would
survive even if it were not.

**Free observation.** The identity also silently fixes a trap the document does not mention. If one
took `Φ_P(A) = E|A∖σ(A)|/|A|` at face value for *all* `A`, then at the antichain `Φ_P(A_{n−1}) =
1/n → 0`, and the quoted Cheeger sandwich `1 − λ_std ≤ 2Φ^*` would read `1 ≤ 2/n` — **false**. The
source's restriction of `Φ^*` to `|A| ≤ n/2` is what makes the sandwich true, and it is precisely
the restriction under which Lemma 2.1 holds. The document's `|A| ≤ n/2` is load-bearing for more
than it says.

---

## 4. Press point 5 — is the new form satisfiable non-trivially?

The brief is right that the §1.6-style "vacuous under the conjecture" escape is unavailable here:
this is a statement about the architecture's *requirement*, not about the frozen class.

**The document's §7.2 answers a different question.** It shows every antichain prefix has
`Δ₁ ≥ 1/2 ≫ ε_0`, i.e. the condition is not satisfied by *everything*. That excludes
vacuity-by-universality. It says nothing about vacuity-by-emptiness — whether *anything*
non-degenerate satisfies it. **Verdict on §7.2 as written: CONFIRMED but answering the wrong
worry.** I answer the right one:

**Witness family (mine, hand-derived, no computation).** Let `W_n = C_n ⊔ C_1`: a chain
`x_1 < ⋯ < x_n` plus one free element `z`, on `n+1` elements. (This is the corpus's own `W_m`,
STATE.md:102.)

- **`W_n` is primitive, not an ordinal sum.** Its incomparability graph is the star `K_{1,n}`
  (`z` incomparable to every `x_i`), which is connected. So `λ_std(W_n) < 1` strictly — this is not
  the degenerate `λ_std = 1` case.
- **Its prefixes are thin, at rate `1/(n+1)`.** Take `A = {x_1,…,x_k}`. A uniform linear extension
  places `z` in one of `n+1` slots uniformly. If `z` lands in the first `k` positions, exactly one
  element of `A` (namely `x_k`) is pushed past the cut; otherwise none. So
  `E|A ∖ σ(A)| = k/(n+1)` and `Φ_{W}(A) = Δ₁(A,A^c) = 1/(n+1)`, **independent of `k`.**
- **Hence `Φ^*(W_n) = 1/(n+1)` and, by the sandwich's easy half, `1 − λ_std(W_n) ≤ 2/(n+1)`.**

So for `n + 1 ≥ 2/ε_spec` the family `W_n` satisfies `1 − λ_std ≤ ε_spec` while being primitive and
having a genuinely non-trivial linear-extension geometry (`E[inv_e] = Θ(n)`). **The class is
non-empty and is not populated only by objects that trivially satisfy everything. The operative
form is non-vacuous. CONFIRMED.**

Cross-check against the corpus, independent of my derivation: mg-3ce3's cleanest witness is
`8AC ⊕ 8AC` with one cross-relation deleted — `n = 16`, `ε = Δ₁ = 0.0019`, `λ_std = 0.996`. A real
poset, thin interface, near-1 `λ_std`. Consistent with `W_n`.

**Rider, in fairness to the document.** Non-vacuity of L4's hypothesis class is what I established.
Satisfiability *under freezing* — i.e. whether any frozen poset has `1 − λ_std ≤ ε_spec` — is the
wall itself (L1b) and is not answerable here; and if the conjecture is true, no frozen poset exists
and the question is moot. That asymmetry is correct and the document does not abuse it.

---

## 5. Press point 6 — §4.2, direction and magnitude on the Cheeger sandwich

**Sandwich, pulled verbatim (`:317–324`) before reading §4.2:**

```
(Phi_P^*)^2 / 2  <=  1 - lambda_std(P)  <=  2 Phi_P^*.
```

Absolute constants `1/2` and `2`. **No `n`, anywhere, in the source's statement.** ✓

**Direction check.** The document needs `Φ^*` *small* from the gap being small. That requires the
**left** inequality (the hard/Cheeger half): `(Φ^*)²/2 ≤ 1 − λ_std ≤ ε_spec` ⟹ `Φ^* ≤ √(2 ε_spec)`.
The document says it uses "the lower half of the Cheeger sandwich" and does exactly that.
**Direction CONFIRMED — no lower/upper conflation.** Then `ε_spec ≤ ½ ε_leak²` gives
`Φ^* ≤ ε_leak` ✓, and this reproduces Step 4's own `Φ_P(A_k) ≲ √ε` (`:506`) ✓ — the source and the
derivation agree, which is a good sign, not a circularity (the source states the `√`, the document
prices it).

**Magnitude check — is an `n` hiding inside the square?** No. `Φ^*` is an `n`-dependent *quantity*,
but the *relation* `ε_spec ≤ ε_leak²/2` is between two thresholds and inherits the sandwich's
absolute constants. Squaring `0.02` gives `4×10⁻⁴`; halving gives `2×10⁻⁴`. **A constant. CONFIRMED.**

**Positive control — recomputed, not read.** Antichain on `n` elements, `σ` uniform:

- `E|A ∖ σ(A)| = Σ_{x∈A} Pr[pos(x) > k] = k(n−k)/n` ✓, so `Φ_P(A) = Δ₁ = (n−k)/n` for `k ≤ n/2` ✓,
  minimised at `k = n/2` at value `1/2` ✓. (For `k > n/2`, `Δ₁ = k/n > 1/2` — so **every** prefix
  has `Δ₁ ≥ 1/2`, confirming §7.2 / Claim 31 ✓.)
- `1 − λ_std = 1`: I derived this from the source's *own* Rayleigh form (`:310–315`) rather than
  from `T_P = J/n`. For `f ⊥ 1`, `E_σ Σ_i (f(i) − f(σ(i)))² = Σ_i[f(i)² − 2f(i)·0 + ‖f‖²/n] =
  2‖f‖²`; halved and normalised, the quotient is `1` for **every** `f ⊥ 1`. So `1 − λ_std = 1`,
  `λ_std = 0` ✓.
- Sandwich: `1 ≤ 2 · (1/2) = 1` — **equality** ✓.

**One parity rider.** `Φ^* = 1/2` exactly requires `n` even. For `n` odd the largest admissible `k`
is `(n−1)/2`, giving `Φ^* = (n+1)/(2n) > 1/2` and `2Φ^* = (n+1)/n > 1`: the sandwich is **strict**,
tight only as `n → ∞`. "Equality at the antichain" is an even-`n` statement. Harmless — nothing
downstream uses equality — but it is a table entry (ledger row 14) that is not literally true at
every `n`, so I record it.

**Master-bound antichain equality (§6.1), recomputed.** `Σ_{i,j}|j−i| = 2Σ_{d=1}^{n−1} d(n−d) =
2[n·n(n−1)/2 − (n−1)n(2n−1)/6] = n(n²−1)/3` ✓, so `E_unif[footrule] = (1/n)·n(n²−1)/3 = (n²−1)/3` ✓,
and `3·(n²−1)/3 / (n²−1) = 1 = 1 − λ_std` ✓ — **exact equality at every `n`**, unlike the Cheeger
one. Ledger row 22 CONFIRMED, row 21's equality claim CONFIRMED.

**Inversion form's `3/2` loss, recomputed.** `E_unif[inv] = C(n,2)/2`, so
`6E[inv]/(n²−1) = 3n/(2(n+1)) → 3/2` against a truth of `1` ✓. The document's "factor `3/2` lossy
at the antichain, since `D ≤ 2I` is not tight there" ✓ CONFIRMED.

---

## 6. Press point 3 — §3.4, the branch-(iii) refutation

This refutes canonical (source) work, so I pulled the source text **first**.

**The claim's arithmetic is right.** Minimality gives `δ(P[A]) ≥ 1/3`, i.e. a pair with
`p^{P[A]}_{xy} ∈ [1/3, 2/3]`. Branch (iii) yields `p^P_{xy} ∈ [1/3 − F, 2/3 + F]` (or the drift
reading, which implies it). `δ(P) < 1/3` says only `p^P_{xy} ∉ [1/3, 2/3]`, which is consistent with
`p^P_{xy} ∈ [1/3 − F, 1/3) ∪ (2/3, 2/3 + F]`. **No contradiction, for any `F > 0`. CONFIRMED.**

**Claim 3.3's witness, recomputed by hand.** `P_0 = {a<b} ⊔ {c}`. Linear extensions: `abc`, `acb`,
`cab` — three ✓ (`b` must follow `a`; `c` free in 3 slots). `p_{ac} = Pr[a ≺ c] = 2/3` (`abc`,`acb`)
✓; `p_{bc} = Pr[b ≺ c] = 1/3` (`abc` only) ✓. `min(p,1−p) = 1/3` for both incomparable pairs, so
`δ(P_0) = 1/3` with **zero slack** ✓. CONFIRMED. And the "`n`-dependence does not repair this"
note is right: `F(ε) > 0` at each finite `n` while the slack can be `0` at that same `n` ✓.

### 6.1 But the framing is OVERSTATED (**F2**)

The document presents this as "a separate defect found on the way … load-bearing for anyone who
writes L4 down as a lemma". Two things in the source, both of which the document had in hand,
soften it to a drafting inconsistency:

1. **`:476–479`, the paragraph immediately after the conjecture** — which the document does not
   quote: *"Since `P[A]` and `P[B]` are smaller than a minimal counterexample, minimality should
   provide a balanced pair on one side unless that side is a chain. **The task is to show that the
   thin interface cannot destroy all such pairs.**"* "Cannot destroy" is exact preservation — the
   document's own recommended repair.
2. **`:567–569`, the source's own statement of L4 in the open-lemma list** — inside `:556–570`,
   which the document *does* cite (in §1, for a different purpose): *"**L4. Near-ordinal-sum
   stability lemma.** Sufficiently small prefix leakage contradicts minimality by **preserving** a
   balanced pair from one side."* Again exact preservation, `F` absent.

So the source states the repaired form **twice** and the loose `F(ε)`-flavoured wording **once**,
in the conjecture body. **Verdict: Claim 3.2 CONFIRMED as arithmetic; §3.4's headline "branch (iii)
does not close Step 6" is OVERSTATED as a finding** — it is an internal inconsistency between three
statements of L4 in one source, and the majority reading is already the repaired one. The
recommendation (restate (iii) as exact preservation) is correct and worth landing; the framing as a
newly-found architectural defect is not. This matters because §10 proposes STATE.md row 11 carry
the note.

### 6.2 The document's own §3.3 implies a second, larger Step-6 gap it never records (**F3**)

§3.3 observes, correctly and in passing: *"Branch (ii) is a structural alternative that no stated
step consumes."* The consequence is not drawn. L4's conclusion is a **disjunction**. If (ii) is the
branch that holds for some `P` in the hypothesis class, Step 6 has nothing to consume and **no
contradiction is produced** — the same failure §3.4 documents for (iii), but with no repair
available, because (ii) genuinely does not deliver a balanced pair.

Combining with §3.4's own result: **as literally stated, L4 closes Step 6 only via branch (i)** —
and (i) ("`P` contains a `1/3`-balanced pair") is the trivial branch that *is* the conclusion. The
honest statement of the §3.4 finding is therefore stronger and more uncomfortable than the one
made: **the stated L4 does not close Step 6 through either of its two non-trivial branches.**

This is a claim asserted-by-implication in prose that escaped the document's 36-row ledger. Row
**P2** below. It is a defect in the *source*, not in the target — but the target found the premise
and stopped one line short of the conclusion, while §7.1 goes on to assert that "the conclusion L4
draws from thinness is `P` has a balanced pair", which is true of (i) and (iii) and **false of (ii)**.

---

## 7. Press point 4 — "buys the mg-210d route nothing", audited in BOTH directions

Per the brief, the failure that matters here is the **false loss**. I ran both.

### 7.1 False-win direction: is there a hidden win being claimed? — **No**

§7.3's arithmetic is right. `ε_spec ≈ 2×10⁻⁴` with Claim 6.1 requires incomparability density
`d ≲ 2×10⁻⁴`, i.e. `m ≤ 2×10⁻⁴·C(n,2)`. For `m ≥ 1` we need `n(n−1) ≥ 10⁴`, i.e. `n ≥ 101`
(`100·99 = 9900 < 10⁴ ≤ 10100 = 101·100`) ✓. **Claim 7.2 CONFIRMED.** No win is smuggled in.

### 7.2 The bound the document proves is weaker than the one available (**audit addition A1**)

Claim 7.2 uses only `m ≥ 1` (non-chain). But **minimal counterexamples are primitive** (STATE.md
glossary; row 2), and a connected incomparability graph has `m ≥ n − 1`, hence

```
d = m / C(n,2)  >=  (n-1) / [n(n-1)/2]  =  2/n.
```

So `d ≤ ε_spec` forces **`n ≥ 2/ε_spec = 10⁴`**, not `n ≥ 101`. The master bound cannot deliver the
architecture's target for **any primitive poset on fewer than ~10⁴ elements** — a factor-100
strengthening of the document's own conclusion, using exactly the ingredient mg-210d recorded as
"wrong-signed" (primitivity gives a *lower* bound on `m`, which degrades the bound — here that is
the point). One line, no computation. Free for pm-onethird to land alongside Claim 7.2.

### 7.3 False-loss direction: what would have to be true for the weakening to buy something? (**F8**)

Two things could make the weakening a gain. I state both explicitly, as the brief asks.

**(a) A tool that delivers a *constant* gap bound but not a vanishing one becomes usable.** Under
the limit form `λ_std → 1`, any bound whose output is a constant `< 1` is **categorically** useless:
a constant is not a limit. Under the operative form, such a bound is **exactly the right shape** and
fails only if its constant exceeds `ε_spec`. **This condition holds, and the corpus has such a tool
on record.** mg-210d's **Residual (R)** — *is there a constant `D < 1` with `d(P) ≤ D` on every
frozen poset?* — yields `1 − λ_std ≤ D` immediately (STATE.md:130). Under the old target that was
recorded, correctly at the time, as *not enough*:

> STATE.md:130 — *"Honest caveat: (R) ⟹ a **constant λ_std**, which does **not** by itself give `δ`
> (rate ≠ the problem; the `λ_std → δ` conversion stays open)."*
> STATE.md:147 — *"even (R) yields a **constant** `λ_std`, not `δ` … so (R) is progress on the
> spectral sub-question, not a route to the conjecture on its own."*

**If this document's verdict is right, that caveat is wrong.** The `λ_std → δ` conversion is
precisely Steps 3–6, and this document's whole point is that Steps 3–6 consume **a constant**. So
(R) with `D ≤ ε_spec` does not merely bound `λ_std` — it **discharges Step 2, which is the wall.**
(R)'s insufficiency moves from *categorical* (wrong currency) to *quantitative* (right currency,
`D` must be `≤ 2×10⁻⁴`, which by §7.2 above additionally forces `n ≥ 10⁴`).

That is a state-change of a recorded residual, produced by this document's own verdict, and the
document does not record it — while §0 and §10 tell the reader the weakening buys that route
**nothing**. **This is the door-marked-shut failure the brief warned about, and it is present.**
Not fatal: (R) remains open and now needs a much smaller constant, so nobody is being told to walk
through an open door. But **STATE.md:130 and :147 carry a caveat that this document silently
falsifies**, and the §10 proposal would land text reinforcing it.

**(b) The budget constant could be larger than `2×10⁻⁴`, in which case the "not good news" framing
softens.** See F5 — it is, on the document's own recommended reading, by two orders of magnitude.

### 7.4 The conclusion survives anyway — but not for the reason given (**F9**)

The document argues "buys nothing" **through the numeric budget** (`ε_spec ≈ 2×10⁻⁴` ⟹ `n ≥ 101`
⟹ route dead). That argument is hostage to a HEURISTIC constant. There is a **constant-free**
argument for the same conclusion, which the document does not give and which is strictly better:

> The mg-210d route's *unconditional* output is `1 − λ_std < d·n/(n+1)` with `d ≤ 1`, i.e.
> `ε_spec < 1` — and `ε_spec < 1` is useless for **any** constant target `< 1`, whatever its value.
> Without (R), the route delivers nothing at any budget; with (R), it delivers `D`. Neither
> statement mentions `2×10⁻⁴`.

So: **"the relaxation does not rescue the route" is CONFIRMED and is robust to the budget. "It buys
the route nothing" is OVERSTATED** — it buys (R) a change of category, per 7.3(a). The right
sentence for STATE.md is: *the relaxation does not rescue the mg-210d route, whose unconditional
output is `ε_spec < 1`; what it does change is that (R) is now shape-correct, so the caveat that a
constant `λ_std` is the wrong currency should be withdrawn.*

### 7.5 §7.4's "numerically stronger below `n ≈ 10⁵`" — direction robust, range not

Recomputed: `(LIB) ≈ 3Cn` vs `(LIB-const) = (ε_spec/6)n² = 3.3×10⁻⁵n²` cross at
`n ≈ 3/3.3×10⁻⁵ ≈ 9×10⁴` ✓; at `n = 100`, `300C` vs `0.33` ✓. Arithmetic correct, label HEURISTIC
correct. **But the sensitivity is larger than "the number `10⁵` is not robust" conveys:** at
`ε_spec = 0.02` (the value the document's own recommended (iii)-repair supports — F5) the crossover
falls to `n ≈ 900`, which is inside the range where an unknown minimal counterexample could live.
The *direction* is robust below the crossover; the claim that the crossover is beyond "every
plausible range" is not.

---

## 8. The two BROKEN derivations

### F5 — §6.4's budget row is BROKEN as labelled, and it is the numeric spine of §7

| row | as printed |
|---|---|
| L4 usable | `F(ε_leak) <` pair's slack; slack `≤ 1/6` for a centred pair | §3 | **PROVEN (given the repaired (iii))** |

Three problems, compounding:

1. **The label is backwards.** Under the *repaired* (iii) that §3.4 recommends — "a balanced pair
   remains **in `[1/3,2/3]`**" — **`F` does not appear in the statement at all**, so there is no
   `F(ε_leak) < slack` condition to calibrate. The row can only be derived under the **stated**
   (iii), i.e. the reading §3.4 of the same document proves cannot close Step 6.
2. **Under the stated (iii), the row contradicts Claim 3.3.** §3.4 proves the available slack can
   be **`0`** (the `P_0` witness), so *no* `F > 0` satisfies `F < slack`. `1/6` is the slack of a
   *centred* pair, i.e. the **maximum possible**; the row uses a maximum as if it were a guarantee.
   `F(ε) < 1/6` is a **necessary** condition read as a **calibration point**.
3. **The consequence is quantitative and one-directional.** Under the repaired (iii) the correct
   empirical calibration is not `F` at all but the `ε` at which mg-3ce3's `survives` predicate first
   fails — and the probe reports **`0` RED events across all 6681 posets up to `ε = 0.20`**. That
   supports `ε_leak ≈ 0.20`, hence `ε_spec ≤ 0.2²/2 = 2×10⁻²` — **100× larger than the document's
   `2×10⁻⁴`.**

**Every pessimistic number in §7 moves with it.** At `ε_spec = 2×10⁻²`: Claim 7.2's "`n ≤ 100`"
becomes "`n ≤ 10`" (`m ≥ 1` needs `n(n−1) ≥ 100`, i.e. `n ≥ 11`); the primitive version (A1) becomes
`n ≥ 100`; §7.4's crossover becomes `n ≈ 900`. **The direction of the error inflates the pessimism**
— which is exactly the direction the brief flagged, since a deliverable that declines to claim a win
is not thereby correct.

**Verdict: row BROKEN as labelled; the constant `2×10⁻⁴` is not merely "not pinned" (§6.4's own
honest phrase) but unpinned by two orders of magnitude in a direction that changes the tone of the
strategic conclusion.** §6.4's "so the form is pinned; the constant is not" is right, and §7 then
uses the unpinned constant as though it were pinned. Mitigation: the conclusion of §7.3 survives
anyway via F9's constant-free argument, so this breaks the *reasoning*, not the *verdict*.

### F6 — §7.3 / ledger 34: the master bound is misattributed (object conflation)

The document writes: *"The master bound uses a **single test vector** — the centred linear position
function `ũ` (`tex:400–424`) — and consumes freezing exactly once, at the per-pair `<1/3` level. Its
antichain-sharpness is a property of `ũ`."* Labelled **PROVEN**.

**Both halves are wrong; I checked mg-210d's actual derivation.** `probe-lambda-constant-bound.md`
Theorem 2.4 builds the master bound from:

- **Lemma 1.1 (Buser tool)**, an *unconditional* cut bound `1 − λ_std ≤ n·leak(A)/(|A||A^c|)`, proven
  with the **indicator** test vector `f = 1_A − a·1` — a *different vector for each cut*;
- applied to **all `n − 1` prefix cuts**, then relaxed by a **mediant inequality**
  `min_k(a_k/b_k) ≤ (Σa_k)/(Σb_k)` with Lemmas 2.1–2.3.

So it is a **minimum over `n − 1` indicator test vectors, further relaxed by an averaging step** —
not a single test vector. And **freezing is not consumed in it at all**: Lemma 1.1 and Theorem 2.4
are unconditional; freezing enters only downstream, in the document's own Claim 6.1.

What the document actually described is the *tex's* separate crude bound at `:400–424`, which uses
`ũ`, does consume `Pr[j ≺ i] < 1/3` exactly once (`:416`), and yields `λ_std > 1/3`. **Two distinct
tools have been merged into one.** This is precisely the object-check failure Appendix A step 5 asks
for.

**Does the conclusion survive? Yes.** "This is a limit of the tool, not a lower bound on the
problem" holds for the correct tool too: a min over *prefix* indicator cuts, weakened by a mediant
step, tight at the antichain, says nothing about the variational problem over all `f ∈ H` or about
reverse-Cheeger transfer. **Substance CONFIRMED, attribution BROKEN, label PROVEN unearned.**

### Audit addition A2 — the source's own `ũ` beats the recorded master bound by a factor `n`

Having separated the two tools, the `ũ` bound is worth pricing, because the corpus has never done
it. From `tex:409–415`, `‖ũ‖² − ⟨ũ, R(σ)ũ⟩ = (n−1)^{−2} Σ_{i<j, j≺_σ i}(j−i)`. That weighted
inversion sum is exactly **half the squared displacement**:

```
sum_{i<j, j prec_sigma i} (j - i)  =  (1/2) sum_x (pos_sigma(x) - x)^2
```

(hand-verified on `21`; `213`, `231`, `132`, `321`; `2143`, `3412` — 7 cases, all exact). With
`‖ũ‖² = n(n²−1)/(12(n−1)²)`, the Rayleigh quotient gives

```
1 - lambda_std  <=  6 E[ sum disp^2 ] / ( n (n^2 - 1) ).
```

Antichain check: `E[Σdisp²] = n(n²−1)/6`, so the bound is `1` — **also exactly sharp at the
antichain** ✓ (so it is no escape from §7.3's diagnosis). But comparing the two:

- **Always within a factor 2 of the master bound** (`Σdisp² ≤ (n−1)Σ|disp|` gives ratio `≤ 2(n−1)/n`);
- **Better by `Θ(n)` whenever displacements are bounded.** Under **(B)**, `E[Σdisp²] = O(E[Σ|disp|])`
  and (B) ⟹ LIB (STATE.md Thm 3.3) gives `E[Σ|disp|] ≤ 2E[inv] = O(n)`, so
  **`1 − λ_std = O(1/n²)`.**

**This sharpens STATE.md:131's "Given (B), the mg-210d master bound alone yields
`1 − λ_std = O(1/n)`" to `O(1/n²)`, using a test vector already written down in the canonical
source.** Offered to pm-onethird as a free by-product, hand-derived, no computation. It does not
reopen anything — both bounds are antichain-sharp, so §7.3's redirect ("find a bound that is not
antichain-sharp") stands unchanged.

---

## 9. Scope check on the headline (Appendix A step 4)

### F4 — "a FOURTH form" is OVERSTATED

The document's §5.1 table separates form 3 ("fixed constant `λ_std ≥ 1 − ε`", tex Step 2 — *"right
shape, quantifier missing"*) from form 4 (*"operative"* — same inequality, quantifier explicit). **The
only difference between forms 3 and 4 is a quantifier over `n`.** But Step 2 (`:492–497`) is applied
to a *single hypothetical minimal counterexample* `P` fixed at Step 1 (`:489–490`). For one fixed
poset **there is no quantifier over `n` to state**: `ε` is a constant fixed by downstream needs, `P`
has whatever size it has, and the source's Step 2 already *is* the operative form.

The "missing quantifier" is an artifact of reading Step 2 as a statement about an `n`-indexed
family — which is how **STATE.md's limit** and **mg-7ae7's rate** state it, and that is the real
finding. **Verdict: the substance (ledger 18) is CONFIRMED; "it is a fourth form, not one of the
three" is OVERSTATED.** The accurate headline is: *the source's own Step-2 form is the operative
one; the corpus has been carrying two asymptotic renderings of it, both strictly stronger than the
consumer needs.* The document's §5.1 body actually says this ("The corpus's third form is the
operative one") — §0 and the commit subject upsell it.

### F10 — §0 / §10 labels do not match the ledger

Appendix A step 3 asks whether any heuristic is promoted to a proven-sounding headline. Two are:

| statement | §0 / §10 | own ledger |
|---|---|---|
| "the weakening … buys the mg-210d route **nothing**" | flat assertion, §0 and §10 rider (b) | row 33 **CONDITIONAL** on 28 (HEURISTIC) + 32 |
| "the constant is small (`ε_spec ≲ 2×10⁻⁴`), which makes the requirement numerically stronger than LIB at every `n` below roughly `10⁵`" | flat assertion, §0 and §10 rider (a) | row 35 **HEURISTIC** |

The ledger is honest; the summary is not, and **§10 is the text proposed for STATE.md** — so the
downgrade would be lost exactly where it matters. pm-onethird should not land §10 riders (a) and (b)
in their present flat form.

### F11 — §7.1's premise is false on branch (ii)

"The conclusion L4 draws from thinness is *`P` has a balanced pair*" holds for branches (i) and
(iii) and **fails for (ii)**, which yields a structural statement and no pair. The logic claim
(breadth does not break the contradiction) is still CONFIRMED for the branches Step 6 consumes, but
the premise as stated is not universal. Cross-references F3.

### F12 — two citation riders (neither is an error in the target)

- **§5.2 leans on `step8.tex` Theorem E, which is stated for *width-3* indecomposable
  `γ`-counterexamples** (`:57–62`, verbatim: *"If `P` is a width-3 indecomposable
  `γ`-counterexample…"*). This programme is explicitly any-width (STATE.md:3, :91). The provenance
  argument — that the `1/n` is the tool's output shape and the consumer discards it — is unaffected,
  and the quotations are verbatim and correct (**ledger 20 CONFIRMED**). But STATE.md row 6 records
  Theorem E's width as **"any"**, and step8.tex states it for width-3. That discrepancy pre-dates
  this document and is out of my scope; flagging it for pm-onethird since §5.2 now leans on it.
- **§7.1 quotes mg-3ce3's "0 RED / 6681" without noting that the probe's *stricter* smaller-side
  reading is not uniform** — the probe records **89 posets losing every balanced pair on the smaller
  side**, and smaller-side survival rates of `0.9938 / 0.9890 / 0.9870` at `ε ≤ 0.10 / 0.15 / 0.20`.
  The architecture consumes the **either-side** reading (Step 6: *"from `P[A_k]` **or**
  `P[A_k^c]`"*), so the document's use is **legitimate** — but the omission makes the evidence read
  as cleaner than the probe reports it.

---

## 10. CLAIM LEDGER — all 36 document rows

Verdicts per the mg-e35c brief: **CONFIRMED / OVERSTATED / BROKEN / UNCHECKED**. "CONFIRMED" means I
re-derived it independently or verified the quotation against the primary file myself.

| # | claim (§) | doc label | **audit verdict** | note |
|---|---|---|---|---|
| 1 | `Φ_P(A) = Δ₁(A,A^c)` for `\|A\| ≤ n/2` (2.1) | PROVEN | **CONFIRMED** | re-derived from `:229–237` + `:270–278`; stronger than stated — that *is* `Φ`'s domain (F7) |
| 2 | Steps 4 and 5 state the same inequality about the same number (2.2) | PROVEN | **CONFIRMED** | `K_k = \|A_k∖σ(A_k)\|` at `:246`; Step 5 adds no bound |
| 3 | `ε` denotes two distinct quantities, spectral vs leakage (1) | PROVEN | **CONFIRMED** | `:495` vs `:459`/`:466`; related by a square. The document's best contribution |
| 4 | L4's `F` is `n`-free; `ε` must be an absolute constant (3.2) | PROVEN as a reading | **CONFIRMED** as a reading | support 2 carries it; **support 1 ("unstatable") OVERSTATED** — `F(ε,n)` is perfectly statable (F1) |
| 5 | Nothing downstream of Step 5 contains an `n` (3.2) | PROVEN | **CONFIRMED** | `:514–515` + `δ<1/3` vs absolute `1/3`; verified |
| 6 | mg-3ce3's pooled envelope is usage evidence for the `n`-free reading (3.2) | HEURISTIC | **CONFIRMED** | envelope is at absolute thresholds pooled over `n=5..16` ✓; label correct |
| 7 | branch-(ii)-`O(1)` steelman ⟹ `E[inv_e]=o(1)` (3.3) | HEURISTIC | **CONFIRMED** | exponents recomputed: `n^{−1.82}`, `n^{−3.64}`, `o(1)` ✓ |
| 8 | Branch (iii) as stated cannot produce the Step 6 contradiction (3.4) | PROVEN | **CONFIRMED** (arithmetic) | framing **OVERSTATED** — source states the repaired form at `:476–479` and `:567–569` (F2) |
| 9 | `δ({a<b}⊔{c}) = 1/3` exactly (3.4) | PROVEN | **CONFIRMED** | 3 extensions, `p_{ac}=2/3`, `p_{bc}=1/3`, recomputed |
| 10 | The endpoint gap is not repaired by any `n`-dependence (3.4) | PROVEN | **CONFIRMED** | `F(ε)>0` at each finite `n`; slack can be `0` there |
| 11 | mg-3ce3 tested the *repaired* form of (iii) (3.4) | PROVEN | **CONFIRMED** | probe `:85–88` verbatim: *"`p^P_xy ∈ [⅓,⅔]`"* ✓ |
| 12 | "`≪`" in Step 5 = constant fraction, not `o(min(k,n−k))` (4.1) | CONDITIONAL on 4 | **CONFIRMED** conditional | inherits 4's conditionality, correctly flagged |
| 13 | `ε_spec ≤ ε_leak²/2`; the Cheeger square is a constant loss (4.2) | PROVEN given `:318–324` | **CONFIRMED** | sandwich verbatim, absolute constants; **direction correct** (lower half used) |
| 14 | Antichain: `λ_std=0`, `Δ₁ ≥ 1/2` on every prefix, RH Cheeger is equality (4.2) | PROVEN | **CONFIRMED** | all three recomputed; **equality is even-`n` only** (§5 parity rider) |
| 15 | Prefix capture as literally worded gives a constant floor — too weak to use (4.3) | PROVEN | **CONFIRMED** | `:360–364` verbatim; `ρ ≥ cλ` ⟹ `1−ρ ≈ 1−c`, a floor. A genuine and useful catch |
| 16 | Under either repair, L3's loss is a constant `C_3` (4.3) | CONDITIONAL | **CONFIRMED** conditional | correctly labelled |
| 17 | L3 is the last candidate site; chain is `n`-free end to end (4.3) | CONDITIONAL on 1,4,13,16 | **CONFIRMED** conditional | I walked the chain independently and found no further site |
| 18 | Operative form: `1−λ_std ≤ ε_spec`, absolute constant, uniform in `n` (5.1) | CONDITIONAL on 17 | **CONFIRMED** conditional | substance right; **"a FOURTH form" OVERSTATED** (F4) |
| 19 | rate ⟹ limit ⟹ constant-for-large-`n`; neither supplies uniformity (5.1) | PROVEN | **CONFIRMED** | and the ~~`N_0`-unspecified~~ **`N_0`-underivable** point is the real content — **the verdict stands; only the word moves.** *Unspecified* understates it: **no `N_0` works for the class at all** (mg-c4f5 §5.3, landed `STATE.md` by mg-5ce3; struck at the target `§5.1` table by mg-4417, which records the a-fortiori step, since §5.3's own hypothesis is `o(n²)` and this row's is the limit). Per-family thresholds are **TRUE and untouched** |
| 20 | mg-7ae7's `1/(γn)` is inherited from Theorem E's output shape (5.2) | PROVEN | **CONFIRMED** | `step8.tex:68–72` and `:290–305` verbatim ✓; **rider: Theorem E is width-3** (F12) |
| 21 | Master bound `≤ 3E[D]/(n²−1) ≤ 6E[I]/(n²−1)` (6.1) | CONDITIONAL (mg-210d) | **CONFIRMED** | second inequality = DG upper half ✓; antichain equality recomputed ✓ |
| 22 | `E_unif[footrule] = (n²−1)/3` (6.1) | PROVEN | **CONFIRMED** | `Σ\|j−i\| = n(n²−1)/3`, recomputed |
| 23 | (LIB-const) `E[inv_e] ≤ (ε_spec/6)(n²−1)` (6.2) | CONDITIONAL | **CONFIRMED** conditional | arithmetic exact |
| 24 | (LIB) ⊊ (LIB-weak) ⊊ (LIB-const) (6.2) | PROVEN as classes / CONDITIONAL as requirement | **CONFIRMED** with the split label | the split is necessary and the document makes it in §0 |
| 25 | Frozen ⟹ `E[inv_e] < m/3` (6.3) | PROVEN | **CONFIRMED** | each incomparable pair inverts w.p. `< 1/3` by coherence with `e`; sum over `m` |
| 26 | Freezing alone gives (LIB-const) with constant `2/3` (6.3) | PROVEN | **CONFIRMED** | `m/3 ≤ (2/3)·C(n,2)/2` ✓ |
| 27 | Claim 6.1 through the master bound reproduces `1−λ_std < d·n/(n+1)` (6.3) | PROVEN | **CONFIRMED** | `6(m/3)/(n²−1) = 2m/(n²−1) = d·n/(n+1)` ✓; matches mg-210d `:239` exactly |
| 28 | Budget `ε_leak ≈ 0.02`, `ε_spec ≈ 2×10⁻⁴/C_3` (6.4) | HEURISTIC + UNQUANTIFIED | **BROKEN** as derived | the "L4 usable" row it rests on is self-inconsistent (**F5**); under the document's own repair the probe supports `ε_leak ≈ 0.20` ⟹ `ε_spec ≈ 2×10⁻²` |
| 29 | Breadth relocates burden onto L4, does not break the contradiction (7.1) | PROVEN (logic) | **CONFIRMED** with rider | logic sound for (i)/(iii); **premise false on branch (ii)** (F11) |
| 30 | mg-3ce3 stress-tested at `ε` an order above budget: 0 RED / 6681 (7.1) | HEURISTIC | **CONFIRMED** | verbatim ✓; **rider: the smaller-side reading has 89 failures, unmentioned** (F12) |
| 31 | Not vacuous: every antichain prefix has `Δ₁ ≥ 1/2` (7.2) | PROVEN | **CONFIRMED** | recomputed both regimes; **but answers vacuity-by-universality, not by-emptiness** (§4) |
| 32 | Master bound cannot deliver the target for any non-chain poset on `n ≤ 100` (7.3) | PROVEN given 28 | **CONFIRMED** given 28 | arithmetic exact; **weaker than available — primitivity gives `n ≤ 10⁴`** (A1); moves to `n ≤ 10` under F5's budget |
| 33 | mg-210d's "best constant = 0" survives; the relaxation buys that route nothing (7.3) | CONDITIONAL | **OVERSTATED** | first half **CONFIRMED and robust** (F9, constant-free); "**buys nothing**" is a **false loss** — it re-prices (R) from categorical to quantitative insufficiency and falsifies STATE.md:130/:147's caveat (**F8**) |
| 34 | 33 is a limit of the tool (`ũ` antichain-sharp), not of the problem (7.3) | PROVEN | **BROKEN** attribution / **CONFIRMED** substance | the master bound is Buser-over-`n−1`-prefix-cuts + a mediant step, and is **unconditional**; `ũ` (`tex:400–424`) is a *different* tool (**F6**) |
| 35 | (LIB-const) numerically stronger than (LIB) below `n ≈ 10⁵` (7.4) | HEURISTIC | **CONFIRMED** as arithmetic | crossover recomputed ✓; **"every plausible range" OVERSTATED** — `n ≈ 900` under F5's budget |
| 36 | `C_3`, `F`, the (iii) repair, the `o(·)` licence remain open (8) | UNQUANTIFIED/OPEN | **CONFIRMED** | honest and complete as far as it goes |

### 10.1 Claims asserted in prose that escaped the document's own ledger

*(mg-0ed7's Finding 7.5 shipped refuted by exactly this route, so these are enumerated separately.)*

| # | in-prose claim | § | **audit verdict** |
|---|---|---|---|
| P1 | *"The **only** route by which L4 could demand `ε → 0` with `n` is if a proof went through branch (ii)"* | 3.3 | **BROKEN as a universal** — the leakage-count objection lives in branch (iii) (**F1**). Its *conclusion* (such a route demands more than either debated form) would survive; the universal does not |
| P2 | *"Branch (ii) is a structural alternative that no stated step consumes"* | 3.3 | **CONFIRMED**, and its **unrecorded consequence** is that Step 6 has a second, unrepairable gap; as stated, L4 closes Step 6 only via the trivial branch (i) (**F3**) |
| P3 | *"The operative form is a **fourth form**, not one of the three in the corpus"* | 0, 5.1 | **OVERSTATED** — it is the source's third form read at a single fixed poset (**F4**) |
| P4 | *"…and it buys the mg-210d route **nothing**"* (flat) | 0 | **OVERSTATED** — see row 33 / **F8**; also a label mismatch against the document's own CONDITIONAL row 33 (**F10**) |
| P5 | *"F(ε_leak) < pair's slack; slack ≤ 1/6 for a centred pair — PROVEN (given the repaired (iii))"* | 6.4 | **BROKEN** — under the repaired (iii) `F` is absent from the statement; under the stated (iii) §3.4 proves the slack can be `0` (**F5**) |
| P6 | *"The master bound uses a single test vector `ũ` … and consumes freezing exactly once"* | 7.3 | **BROKEN** — misidentifies the tool and its hypotheses; conclusion survives (**F6**) |
| P7 | *"An `n`-dependent `F` … would be a schema, not a statement"* | 3.2 | **OVERSTATED** — doubly-indexed moduli are statable (§2.2) |
| P8 | *"The conclusion L4 draws from thinness is '`P` has a balanced pair'"* | 7.1 | **OVERSTATED** — true of (i)/(iii), false of (ii) (**F11**) |
| P9 | *"If `Δ₁ ≤ ε_0` held trivially, Step 4's output would carry no information"* (framed as the vacuity check) | 7.2 | **CONFIRMED but incomplete** — excludes vacuity-by-universality only; vacuity-by-emptiness answered independently in §4 above (**satisfiable**, witness `C_n ⊔ C_1`) |
| P10 | *"So there is no reading of the source under which `n` enters at L3"* | 4.3 | **CONFIRMED** as a disjunction over the two readings offered; correctly marked CONDITIONAL in row 16 |
| P11 | *"Every numerical statement below is … a hand identity, a quoted line, or a labelled read-off"* (method claim) | preamble | **CONFIRMED** against the commit — see §1.1 |
| P12 | *"the entire empirical base lives at `n ≤ 16`"* | 7.4 | **CONFIRMED** — mg-3ce3 tops out at `n=16`; other corpus data at `n ≤ 7` |
| P13 | *"Nothing has been written into STATE.md"* | 10, 11 | **CONFIRMED** — commit touches one file; STATE.md untouched. Scope discipline honoured exactly |

**Nothing is UNCHECKED.** Every row above was either re-derived, recomputed, or verified verbatim
against a primary file. The one item I could not settle — whether L4 with an `n`-free modulus is
*true* — is not a claim the document makes.

---

## 11. Step 4b — strength check, run forward

The document proposes no new hypothesis as a target, so 4b's main clause has little purchase. Two
applications do bite:

1. **Run (LIB-const) forward.** `E[inv_e] ≤ (ε_spec/6)(n²−1)` ⟹ (master bound) `1−λ_std ≤ ε_spec` ⟹
   (Cheeger) a `√(2ε_spec)`-conductance cut ⟹ (L3) a thin prefix ⟹ (L4) a balanced pair ⟹
   contradiction. So (LIB-const) is **exactly** as strong as the wall, by construction — it is
   *defined* as what the wall consumes, not proposed as a step below it. **No 4b violation.** The
   document is careful about this and §7 is itself a strength check, correctly run.
2. **Falsifier quantifier.** The document's one falsifier-shaped object is Claim 3.3's `P_0`
   witness, used to deny *interior slack*. Check the quantifier: `P_0` denies a **universal**
   strengthening of minimality ("*every* smaller poset has a pair with `p ∈ [1/3+c, 2/3−c]`"), and
   that is exactly the statement §3.4 needs to deny. **The quantifier is correct — no
   `e`-minimum-to-`max_x` slip.** One rider: `P_0` does not exclude a *class-restricted* slack claim
   (e.g. slack available on the specific `P[A]` a Cheeger sweep produces), and §3.4 does not claim
   it does.

**4b verdict: PASS.**

---

## 12. Cross-doc consistency (Appendix A step 6)

| prior claim | where | this document's effect | sound? |
|---|---|---|---|
| L1b conclusion stated as the limit `λ_std → 1` | STATE.md:13, row 8, :102 | **stronger than required** | **YES**, given L4 as stated |
| mg-7ae7's rate `1−λ_std ≤ C/(γn)` | mg-7ae7 | **much stronger than required; inherited from Theorem E's output shape** | **YES** — verbatim-supported |
| *"(R) yields a **constant** `λ_std`, which does not by itself give `δ`"* | STATE.md:130, :147 | **falsified by this document's own verdict** — a constant `λ_std` is exactly what Steps 3–6 consume | **YES, and unrecorded (F8)** — the document instead tells the reader the relaxation buys that route nothing |
| *"Given (B), the mg-210d master bound alone yields `1−λ_std = O(1/n)`"* | STATE.md:131 | untouched by the document; **sharpenable to `O(1/n²)`** via the source's own `ũ` | **A2**, offered |
| L4 branch (iii) as stated | tex `:471–472` | repair recommended | **YES** as arithmetic; **but the source already states the repaired form at `:476–479` and `:567–569`** (F2) |
| Theorem E recorded as width **"any"** | STATE.md row 6 | leaned on by §5.2 | **pre-existing discrepancy** — `step8.tex:59–60` says width-3 (F12); out of scope, flagged |

---

## 13. What pm-onethird should land, and what to hold

**Land (verified here, hand-checkable, no computation):**

1. **The `ε_spec` / `ε_leak` collision and the square between them.** Real, verified verbatim, and
   it does dissolve the limit-vs-rate confusion. The document's most durable contribution.
2. **`Φ_P ≡ Δ₁` on `Φ`'s whole domain** — Steps 4 and 5 are one inequality, not two.
3. **mg-7ae7's `1/(γn)` is inherited from Theorem E's output shape and discarded by Theorem E's own
   consumer.** Verbatim-supported both ends (§10 rider (c)) — land as written.
4. **Prefix-capture as literally worded is too weak to use** (§4.3) — a constant floor, not a small
   gap. Correct and useful; it makes L3's statement, not just its constant, an open item.
5. **The operative form itself**, `1 − λ_std ≤ ε_spec` at every `n` — **with the conditional made
   explicit**: this is what the *stated* architecture consumes, and L4-as-stated (row 11, OPEN) is
   the object whose `n`-free modulus is unverified (F1).

**Amend before landing:**

6. **§10 rider (b) — "buys the mg-210d route nothing".** Replace with: *the relaxation does not
   rescue the mg-210d route, whose unconditional output is `ε_spec < 1` — a constant-free fact, so
   this does not depend on the budget. What it **does** change is that a constant `λ_std` is now the
   right currency, so Residual **(R)** is shape-correct and its insufficiency is quantitative
   (`D ≤ ε_spec`), not categorical. **The caveat at STATE.md:130 and :147 — "(R) yields a constant
   `λ_std`, which does not by itself give `δ`" — should be withdrawn.*** (F8, F9)
7. **§10 rider (a) — the `2×10⁻⁴` budget and the `10⁵` crossover.** Do **not** land as flat text.
   The budget's derivation is self-inconsistent (F5): it is calibrated under the branch-(iii) reading
   the same document proves broken, and under the recommended repair the probe supports `ε_spec` two
   orders of magnitude larger, moving the crossover to `n ≈ 900`. Land it as: *the constant is
   unpinned by ~2 orders of magnitude and the pessimistic reading is the smaller one.*
8. **Claim 7.2's threshold.** `n ≤ 100` → **`n ≤ 10⁴` for primitive posets** (A1), which is the
   relevant class since minimal counterexamples are primitive.
9. **Ledger 34's attribution.** The master bound is Buser-over-prefix-cuts + a mediant relaxation,
   unconditional; not the `ũ` bound and it does not consume freezing (F6). The conclusion ("a limit
   of the tool") stands and can be restated correctly in one line.
10. **Row 11 note on branch (iii).** Land the repair, but as *"the conjecture body's wording of (iii)
    is inconsistent with the source's own L4 (`:567–569`) and its own following paragraph
    (`:476–479`), both of which already state exact preservation"* — not as a newly-found defect
    (F2). **And add branch (ii): as stated, L4 closes Step 6 only via the trivial branch (i)** (F3).

**Hold / do not act on:**

11. **"A fourth form."** It is the source's third form with the quantifier made explicit (F4). The
    news is about the corpus's two asymptotic renderings; say that instead.
12. **The `n`-stratification check** (mg-3ce3 survival by `n` at fixed `ε`). Correctly flagged and
    not run under the no-computation directive. I concur — **but note it is exactly the check my
    steelman (F1) calls for**, so it is now the single highest-value cheap check on the board if the
    directive is ever lifted for it. Daniel's call, not mine.

---

## 14. Net

**Re-pricing plus one genuine notation catch; not new mathematics — and the document says so
itself in every place except its §0.**

Nothing in the corpus's `[PROVEN]` inventory is withdrawn by this document, and nothing in this
document's inventory is withdrawn by me. The backward chain L4 → Step 5 → Step 4 → Step 3 → Step 2
is correctly walked, every conversion in it is correctly priced, and the conclusion that no `n`
enters is right **for the architecture as written**. The document's own caution ("the form is
pinned; the constant is not") is the honest summary of its own contents, and §7 is a strength check
the author ran unprompted and reported against their own interest.

Against that: the constant it declines to pin is then used to reach the strategic conclusion, and
the strategic conclusion is stated flatly in the text proposed for STATE.md. The "buys nothing"
verdict — the expensive claim, per the brief — is right about the route and wrong about the
residual, and the direction of that error is to close a door. **A deliverable that declines to claim
a win is not thereby correct**, and here the declining is where the one landable state-change got
lost.

**Overall verdict on "the claims are sound and correctly labelled": OVERSTATED.**
Sound: yes, with two broken derivations that do not propagate to a mathematical statement.
Correctly labelled: in the ledger, yes; in §0 and §10, no.

---

*Audit by `mg-e35c`. Paper-and-pencil throughout; no scripts, no data, no enumeration. Routed to
pm-onethird as first-line. STATE.md deliberately untouched — the consequences above are
pm-onethird's to land, and `mg-1fdb` has only just finished reconciling the same lines.*
