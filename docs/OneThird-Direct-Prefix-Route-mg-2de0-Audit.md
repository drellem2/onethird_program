# The direct-prefix route (mg-00b9 Lemma A / Lemma B) — INDEPENDENT AUDIT

**Item:** mg-2de0 · **Audits:** mg-00b9 (analysis-only, landed no edits, no independent pass)
**Instrument:** `code/direct_prefix_audit_2de0/` · **Predictions:** committed at `e9702ee`,
before any script of this audit existed.

**Operator scope, checked before every use.** Every object here is on the **transport axis**:
`λ_std` (top eigenvalue of the symmetrised transport operator `S_P` on `1⊥`), `Φ_P` / `Δ₁`
(transport conductance, L1 ordinal-sum defect), `inv_e`, footrule. **Nothing here is `Δ_AT`,
`A(P)`, or the Hodge axis.** `λ_std` is never computed anywhere in this instrument — only the
corpus's master *bound* on `1 − λ_std` is evaluated, and it is named as a bound at every site.
The single appearance of the balance axis is `δ` in §5, which is correct there: §5 audits the
step that converts a **width** bound into a **`δ`** bound.

---

## 0. The answer to the ticket's question

> Does the contradiction follow with NO spectral statement?

**On the route as mg-00b9 states it: no — its central inequality is false, and the falsifier
mg-2de0 calls impossible exists.** **On the route repaired: yes, and the repair is one
character wide.** Lemma A is an exact identity and survives everything. Lemma B's middle step
is false, the falsity reaches the outer bound, and replacing `n²` with `n² − 1` fixes it and
*improves* mg-00b9's own headline number to exactly `2/3`.

| claim | verdict |
|---|---|
| **Lemma A** `Σₖ Kₖ(σ) = D(σ)/2` | **CONFIRMED**, 0 exceptions / 5912 permutations. Exact, per-`σ`, and **poset-free** |
| **Lemma B I1** (mediant + Lemma A) | **CONFIRMED**, 0 exceptions / 3443 (poset, β) cells |
| **Lemma B I2** `Σₖ min(k,n−k) ≥ (1−4β²)n²/4` | **FALSE**, 62 of 183 (n, β) grid cells |
| **Lemma B middle form** as a bound | **FALSIFIED on real posets**, 17 of 3443 cells, `n` ∈ {3,4,5} |
| **Lemma B outer form** (the one mg-2de0 says cannot be falsified) | **FALSIFIED**, 8 of 3443 cells, **2 of them at β=0** |
| **The repair** `2E[D]/(n²−1)` | **CONFIRMED**, 0 exceptions, and **tight** at the witness |
| **Non-vacuity: direct 2/3 vs Cheeger √2** | **CONFIRMED** — and **like-for-like**, and the direct route bounds the *harder* quantity |
| **The stated REASON for that gap ("the Cheeger square")** | **NOT SUPPORTED at that input** — the spectral chain is vacuous one step earlier |
| **`3/ε_leak`, same `ε_leak`?** | **YES, same `ε_leak`.** But the factor is `β=0`-only; at β=1/4 it is `2.25/ε_leak` |
| **Item (b) `1.22/√μ ≥ 2.1`** | **CONFIRMED at β=0**; degrades to `0.92/√μ ≥ 1.59` at β=1/4. No crossover either way |
| **Item (e) Linial** | **CONFIRMED as used**, 0 exceptions / 3210 width-≤2 posets — **plus a missing rider** |
| **Priority 4 sites** | **five** lines, not three; two of the brief's three line numbers are **stale** |

---

## 1. Lemma A — CONFIRMED, and it is stronger than stated

I derived it from the definitions without reading mg-00b9's derivation:

> Fix `x`. `Kₖ` counts `x` exactly when `rank_e(x) ≤ k < pos_σ(x)`, i.e. for the `k` in the
> integer interval `[rank_e(x), pos_σ(x) − 1]` — which has `pos − rank` members when positive
> and none otherwise, and lies inside `[1, n−1]` automatically. So
> `Σₖ Kₖ(σ) = Σₓ (pos_σ(x) − rank_e(x))⁺`. Both `pos_σ` and `rank_e` are bijections onto the
> same `n` positions, so `Σₓ (pos − rank) = 0`, hence the positive and negative parts are
> equal and each is half of `Σₓ |pos − rank| = D(σ)`. ∎

**Two things the statement does not show, which the derivation does.** It is an identity
**per `σ`**, not in expectation. And it is **poset-free** — `P` appears nowhere; the poset
enters only when `σ` is restricted to `L(P)` to take an expectation. So its widest population
is *all permutations*, and the poset check is a control.

**Measured** (`out_a1_lemma_a.txt`): 0 exceptions over **all 5912 permutations** for `n=2..7`;
0 over **13815 (poset, linear extension) pairs** across 431 posets; 0 in expectation over those
431 posets. The two proof steps (the counting exchange, the cancellation) are scored separately
so a failure would localise.

mg-00b9's evidence was one hand-check (`n=4` antichain: `3/4 + 1 + 3/4 = 5/2`). I reproduced it
and extended it by 33 named posets and 5912 permutations. **A single value could not have
distinguished Lemma A from its factor-2 variant** — see next.

### 1a. A factor-2 documentation defect this pins: `STATE.md:28`

`STATE.md:28` records `Σ prefix-violations = footrule ≍ inv`. Lemma A says the sum of `Kₖ` is
`footrule/2`. Both are true, of **different objects**:

- one-sided, `Kₖ = |A_k ∖ σ(A_k)|` — the reading the corpus **pins** at
  `docs/OneThird-lambda-std-Operative-Form.md:84` and its audit `:227` — sums to `D/2`;
- symmetric difference, `|A_k Δ σ(A_k)| = 2Kₖ`, sums to `D`.

Verified: `|A_k ∖ σ(A_k)| = |σ(A_k) ∖ A_k|` for all 4166 (permutation, `k`) pairs, which is
*why* the gap is exactly 2 and not something `σ`-dependent. `STATE.md:28` is the **only** site
in the corpus using the phrase "prefix-violations" and it states no normalisation, so the
ledger's identity is **true under a reading its own definitions section contradicts**.
Recommendation in §6.

Pleasant cross-check: `STATE.md:27` records `ΣK_m ≤ inv ≤ 2ΣK_m`. Substituting Lemma A gives
`D/2 ≤ inv ≤ D`, which is exactly Diaconis–Graham. **Lemma A is not new to the corpus — it is
already implicit in ledger row 27**, unnamed and with its normalisation unpinned. That is worth
knowing: the route's foundation is older and safer than mg-00b9 presents it.

---

## 2. Lemma B — I1 CONFIRMED, I2 FALSE, and the falsity reaches the outer bound

Lemma B depends on Lemma A. Lemma A survived, so B is not dead at the root. Scoring the three
inequalities **separately** is what localises the defect:

### I1 (mediant + Lemma A) — CONFIRMED, 0 / 3443 cells

`min_k (a_k/b_k) ≤ (Σa_k)/(Σb_k)` with `a_k = E[Kₖ]`, `b_k = min(k,n−k)` over `k ∈ K_β`, then
the numerator enlarged to `E[D]/2` by Lemma A. Sound: every `E[Kₖ] ≥ 0`.

**Headroom finding.** That enlargement can give away *everything*. On the balanced ordinal sum
`A₂ < A₂` at `n=4, β=1/3`, the sharp in-range mediant is **0** while Lemma B's bound is
positive — ratio **0**. The enlargement is not merely lossy, it is unboundedly lossy, and it is
worst **at the near-ordinal-sum posets, which is the architecture's regime of interest**. The
sharp form `(Σ_{k∈K_β} E[Kₖ])/Σ_{k∈K_β} min(k,n−k)` is verified to hold on all 3443 cells. So
the route has real unexploited headroom and its own numbers understate it.

### I2 — FALSE, 62 of 183 (n, β) grid cells

The claim is `Σ_{k∈K_β} min(k,n−k) ≥ (1−4β²)n²/4`. The right side is the **integral**
`∫_{βn}^{(1−β)n} min(t, n−t) dt`; the left is a **discrete sum over the integers** in the same
interval. `min(k,n−k)` is concave, so midpoint gives `f(k) ≥ ∫_{k−1/2}^{k+1/2} f` — but the
range that recovers is `[⌈βn⌉ − 1/2, ⌊(1−β)n⌋ + 1/2]`, which **need not contain**
`[βn, (1−β)n]`. The endpoints' ceil/floor is never paid for.

At **β = 0** the failure is exact and clean:

> `Σ_{k=1}^{n−1} min(k, n−k) = ⌊n²/4⌋`, which is `n²/4` for even `n` and **`(n²−1)/4` for odd
> `n`** — short of the claim by exactly `1/4`.

Measured: at β=0 the failures are **exactly the odd `n`** (3,5,…,23 in range). At β>0 it fails
much more widely (n=4 β=1/3, n=5 β=1/4, n=9 β=1/4, …). **62 of 183 cells.**

### The middle form as a bound — FALSIFIED on 17 of 3443 real (poset, β) cells

A false proof step is not yet a false bound. This one is: `n` ∈ {3, 4, 5}, including **`n=5` at
β=0** (three distinct labelled posets). Sample: antichain `n=3`, truth `2/3`, claimed `16/27`.

### The outer form — FALSIFIED, and this is the ticket's "impossible"

mg-2de0's falsifier line reads:

> *"exhibit a poset with `min_k Δ₁(A_k) > 4E[inv_e]/n²`. **Lemma A is an identity, so this
> should be impossible** — that is the check to run if anyone doubts the route."*

**Here is one, at β=0.** `P` on `{0,1,2}`: the chain `0 < 2`, with `1` incomparable to both.
Three linear extensions: `(0,1,2), (0,2,1), (1,0,2)`.

| quantity | value |
|---|---|
| `E[D]` | `4/3` |
| `E[inv_e]` | `2/3` |
| `E[K₁] = E[K₂]` | `1/3` each — and `1/3 + 1/3 = 2/3 = E[D]/2` ✓ Lemma A holds |
| **truth** `min_k Δ₁(A_k)` | **`1/3`** |
| **claimed** `4E[inv_e]/n²` | **`8/27 ≈ 0.2963`** |

`1/3 > 8/27`. **The outer bound is false there.** Hand-computed and machine-confirmed; a second
witness at `n=5` (β=0) and six more at β>0.

**Why the reasoning failed.** "Lemma A is an identity, so this should be impossible" is a **non
sequitur**. Lemma A secures **I1 only**. I2 is a separate, false step, and I3
(Diaconis–Graham `D ≤ 2·inv`) is the only slack that could absorb it. At this witness
`2E[inv] − E[D] = 0` **exactly** — DG has *zero* slack — so I2's deficit passes straight
through. The falsifier is not exotic: it is the smallest non-trivial poset that is neither a
chain nor an antichain, and it is found by looking where DG is tight.

### The repair — CONFIRMED, and it makes mg-00b9's own headline *better*

> **β = 0:** `min_k Δ₁(A_k) ≤ (E[D]/2)/⌊n²/4⌋ ≤ 2E[D]/(n²−1)`
> **general β:** `min_k Δ₁(A_k) ≤ (E[D]/2)/Σ_{k∈K_β} min(k,n−k)`

0 exceptions on all 431 posets and all 3443 cells. Three things recommend it:

1. It is **tight at the falsifying witness**: `(4/3 ÷ 2)/2 = 1/3` = truth exactly.
2. At the antichain it gives **exactly `2/3` for every `n`** — mg-00b9's stated `n²` form gives
   `2(n²−1)/(3n²) < 2/3` and never attains its own headline.
3. `(n² − 1)` is **the corpus's own denominator** for the master bound (`STATE.md:130`), so the
   repair puts the direct route on the normalisation the ledger already uses.

---

## 3. Priority 2 — non-vacuity: the conclusion holds, the stated reason does not

**`2/3` — CONFIRMED, as the repaired bound.** Antichain closed forms (hand-derived, then
verified against enumeration to `n=8`): `E[Kₖ] = k(n−k)/n`, `Δ₁(A_k) = max(k,n−k)/n`,
`E[D] = (n²−1)/3`, so `min_k Δ₁(A_k) = ⌈n/2⌉/n`.

**"against a truth of 1/2" is an even-`n` statement.** At odd `n` the truth is `(n+1)/(2n) >
1/2`, and **at `n=3` it is `2/3` — equal to the bound**, so the factor is `1.0000` there, not
`4/3`. The `4/3` is the even-`n` and large-`n` value. Grain matters here because `n=3` is also
where the stated form is false.

**`√2` — CONFIRMED and vacuous.** `Φ_P(A) ≤ 1` on all **12702** (poset, cut) pairs, so any
bound `≥ 1` carries no information; `√2 = 1.414… ≥ 1`.

**But the attribution to the Cheeger square is not supported at that input.** At the antichain
the master bound alone is `3E[D]/(n²−1) = 3·((n²−1)/3)/(n²−1) = **1** exactly, every `n`. So
`1 − λ_std ≤ 1`, which every `λ_std ∈ [−1,1]` already satisfies:

> **the spectral chain is already vacuous at its FIRST step, before Cheeger is applied.**
> `√2 = √(2·1)` is vacuous because its *input* is vacuous, not because the square is lossy.

This is the corpus's own observation (`STATE.md:130` "equality at the antichain";
`Op-Form:328`), re-derived here. mg-00b9's "the entire difference is the Cheeger **square**
(tex:318–324), paid only for the detour" is therefore **the wrong diagnosis at the antichain** —
the antichain kills the chain one step earlier than the square. The **conclusion** (direct is
non-vacuous where spectral is vacuous) survives intact; the square's price is real and is
measured correctly in §4, which is the only place it can be read off.

**Is the comparison like-for-like? Yes — and better than that.** Direct bounds
`min_k Δ₁(A_k)` (prefixes); Cheeger bounds `Φ*` (all cuts). `Φ* ≤ min_k Δ₁(A_k)` always —
verified, 0 exceptions / 431 posets, strict on 65 of them. So the direct route bounds the
**larger, harder** number and still gets the better answer: the comparison is **conservative in
the direct route's favour**. And at the antichain specifically, `Φ* = min_k Δ₁(A_k)` **exactly**
(0 exceptions, `n=2..7`) — the prefix family already attains the global cut minimum there, so at
the one input where mg-00b9 evaluates both, the two routes bound the **same number** and the
comparison is exactly like-for-like.

One provenance rider: the spectral side's second step, the Cheeger **sweep** half
`(Φ*)²/2 ≤ 1 − λ_std`, appears in **no ledger row** and is unproven for `S_P` in this corpus
(mg-2de0 item 4). The direct route uses only Lemma A, the mediant inequality, and DG. **So the
direct route also wins on provenance**, independently of any number.

---

## 4. Priority 3 — `3/ε_leak`: same `ε_leak`, wrong `β`

**Q: are the two requirements at the same `ε_leak`? YES.** Traced symbol by symbol: both are
the requirement for the same conclusion, *leak parameter ≤ `ε_leak`*, at the same `ε_leak`.
Direct: `E[inv] ≤ ε_leak·Σ_{k∈K_β} min(k,n−k)`. Spectral: `Φ* ≤ ε_leak` forces
`ε_spec = ε_leak²/2` through the sweep half, then the master bound gives
`E[inv] ≤ (ε_spec/6)(n²−1)`. **The comparison is well-posed.**

Write the `ε_leak`-free multiplier `M(n,β) = 12·Σ_{k∈K_β} min(k,n−k)/(n²−1)`; the ratio is
`M/ε_leak`.

| β | `M` exact | claimed |
|---|---|---|
| 0 | **exactly 3** for odd `n`; `3n²/(n²−1) > 3` for even `n` | 3 ✓ |
| 1/4 | `2.0`–`2.45` for `n ≥ 5` (→ 9/4) | 9/4 = 2.25 |
| 1/3 | `1.6`–`2.01` | 5/3 |

**So `3/ε_leak` is CONFIRMED — at β = 0 only.** 0 exceptions / 37 values of `n`.

**And β = 0 is where the lemma's entire selling point is switched off.** At β=0 the `k`-range is
all of `[1, n−1]` and the selected `k` may be `1` — there is **no balance guarantee at all**,
so item (d) (discharging the geometric half of F-bal, the thing that makes a *balanced* prefix
worth having) delivers nothing. At the β=1/4 the ticket itself prices, the honest multiplier is
`2.25`:

| `ε_leak` | headline `3/ε_leak` | honest at β=1/4 |
|---|---|---|
| 0.20 (mg-e35c F5) | 15× | **11.25×** |
| 0.02 | 150× | **112.5×** |

mg-00b9's own (a) writes `(1−4β²)` **into** the direct requirement and then reports the ratio
**without** it. That is the one place the comparison crosses parameter settings — **not in
`ε_leak` (same), but in `β`**. The two cannot both be claimed at once.

*Measured exception, reported not smoothed:* at `n = 3` and `n = 4` the β=1/4 window is
`[1, n−1]` — **identical to the β=0 window** — so `M ≥ 3` survives there. Not because the
headline tolerates a real balance constraint, but because at those `n` the constraint is
vacuous. For `n ≥ 5`, `M(n,1/4) < 3` with 0 exceptions / 35.

**Item (b) — CONFIRMED at β=0.** With `μ = E[D]/n² ≤ 1/3`: direct `2μ`, Cheeger `√(6μ)`, ratio
`√6/(2√μ) = 1.2247/√μ`, `= 2.1213` at `μ = 1/3`, growing without bound as `μ → 0`. No
crossover. At β=1/4 it degrades to `0.9186/√μ`, `= 1.5910` at `μ = 1/3` — still no crossover
(that needs `μ > 0.844`), but `≥ 2.1` is a β=0 figure. Same defect, same cause.

**Minor, and against mg-00b9's own conclusion:** it renders the spectral requirement with `n²`
where the corpus has `(n²−1)`. Since `(n²−1) < n²`, mg-00b9 gives the spectral route a *larger*
budget than the ledger does, i.e. **understates its own advantage**. Harmless, direction
confirmed.

**Item (f) is not an independent second win.** `1.5·ε_leak / ε_spec` with `ε_spec = ε_leak²/2`
is `3/ε_leak` — verified identically equal to §4's factor. It is the **same Cheeger square
re-expressed on the density axis**; reporting both as separate gains double-counts one square.
Separately, the "`n ≥ 100 → n ≥ 6.7`" drop compares `2/ε_spec` at `ε_spec = 0.02` against
`2/(1.5·ε_leak)` at `ε_leak = 0.20` — two different formulas at two calibrations that happen to
satisfy `ε_spec = ε_leak²/2`, so the comparison is not wrong but it is not the like-for-like it
reads as. I did **not** re-derive the `n ≥ 2/ε_spec` artifact itself; out of scope.

The ticket's own counterweight stands and this audit does not touch it: **mg-e2de and
primitivity `m ≥ n−1` are wrong-signed against (R), and a discount on a constant does not
repair a wrong-signed lever.**

---

## 5. Item (e) — the Linial citation: CONFIRMED as used, plus a missing rider

I **cannot** re-derive Linial's theorem and I do not. I checked the citation **as used**, which
is answerable on a finite population, with an instrument that could have refuted it:

- **"both sides chains ⟹ width ≤ 2"** — 0 exceptions / **508** posets (every bipartition of
  `{0..n−1}` into two increasing chains, `n=2..8`).
- **"width ≤ 2 ⟹ δ ≥ 1/3"** — 0 exceptions / **3210** labelled posets of width ≤ 2 with an
  incomparable pair, `n=2..7`. Tightest cell **`δ = 1/3` exactly** (the 2-chain plus a free
  point), so the bound is attained and the check is not slack.
- **Negative control** — the same sweep at width ≥ 3: 0 exceptions / **98442**, tightest cell
  `δ = 14/39 ≈ 0.359`. The two families have **different** tightest cells, so the width-≤2
  restriction is doing real work on this population and §5's positive is not vacuous.

**The missing rider.** `δ` is a maximum over incomparable pairs. **A chain has no incomparable
pair and therefore no `δ`.** Item (e) as worded — "both sides chains ⟹ width ≤ 2 ⟹ Linial ⟹
`δ ≥ 1/3`" — is **malformed** on the 12 members of the two-chain population that are themselves
chains; the instrument skips them explicitly rather than counting them as passing. The rider
needed is **"and `P` is not itself a chain"**, which is one of the two hypotheses Linial's
theorem requires. It is **harmless in context** — a minimal counterexample is not a chain — but
it is a rider mg-00b9's statement does not carry, and "closes for free" should read "closes for
free, given non-chain-ness, which minimality supplies."

**What I could not do.** `tex:481–483` is unresolvable from this repo (§7).

---

## 6. Priority 4 — the propagation sites. REPORT ONLY; pm-onethird to land

**I made no edit to `STATE.md`.** It is pm-onethird's ledger and is being restructured under
mg-ea0e. Every line number below is measured at HEAD (`81214a9`, 386 lines) and **two of the
brief's three are stale** — line numbers rot, which is the argument for landing by content
match rather than by offset.

### 6a. The limit form vs the operative form — **five** sites, not three

`STATE.md:132` records the operative form from mg-88bd (audited mg-e35c): the architecture
consumes **`1 − λ_std ≤ ε_spec` for an explicit absolute constant, uniform in `n`** — not the
limit. The limit form `λ_std → 1` still stands at:

| line | site | brief says |
|---|---|---|
| **:13** | the one-paragraph state, L1b blockquote | ✓ named |
| **:21** | Axis-1 bullet, "two axes, one bridge" | **NOT named — omitted** |
| **:57** | mermaid **node C** | brief says `:56`, which is **node B** ("The BK walk mixes badly") — **off by one** |
| **:62** | mermaid **B→C arrow label** ("L1b: bad mixing ⟹ λ_std→1") | **NOT named — the diagram states it twice** |
| **:86** | ledger row 8 | ✓ named |

Recommended: at each site, state the operative form as what the architecture consumes and the
limit form as strictly stronger, carrying the three mg-88bd §10 riders as corrected by mg-e35c
F5 — or the row reads as better news than it is. **`:132` and `:172` already carry the
conditional correctly and need no change.** Note `:172`'s own words: *"both of the corpus's
asymptotic renderings … are genuinely stronger than the architecture needs"* — the ledger
already knows; five top-line sites have not been told.

### 6b. The C→D arrow label — substance confirmed, line number stale

The brief says `:65`. At HEAD **`:65` is the E→F arrow** ("a balanced pair contradicts δ<1/3").
**The C→D arrow is `:63`**, and its label is *"PROVEN+emp — easy/Buser bounds the gap by any
cut; + L3 best-cut-is-a-prefix (125/126)"*.

**The substance is confirmed.** easy/Buser (row 5, `:83`) is
`1−λ_std ≤ n·leak(A)/(|A||Aᶜ|)` — the **cut ⟹ gap** direction. The C→D arrow goes
**gap ⟹ cut**, and needs `(Φ*)²/2 ≤ 1 − λ_std`, the **sweep** half, which appears in **no
ledger row**. Recommended: ledger the sweep half as proven-by-citation *for `S_P` specifically*,
or record it as a **third open dependency**. This audit found an independent reason it matters:
§3 shows the sweep half is the only step of the spectral chain the direct route does not need,
and §4 shows its square is the whole `3/ε_leak`.

### 6c. `STATE.md:28` — pin the normalisation (new, from §1a)

`Σ prefix-violations = footrule ≍ inv` is **true only under the symmetric-difference reading**
and false by a factor of 2 under the one-sided `Kₖ` the corpus pins at
`docs/OneThird-lambda-std-Operative-Form.md:84`. Recommended: `Σₖ |A_k ∖ σ(A_k)| = footrule/2`
(Lemma A), and note it is `STATE.md:27` restated — `ΣK_m ≤ inv ≤ 2ΣK_m` **is** Diaconis–Graham
once Lemma A is substituted.

### 6d. If the repaired Lemma B is landed

Record it as `min_k Δ₁(A_k) ≤ (E[D]/2)/Σ_{k∈K_β} min(k,n−k)`, with the β=0 specialisation
`≤ 2E[D]/(n² − 1)`. **Do not record the `n²` form**: it is false at `n=3` and it does not attain
its own `2/3`.

---

## 7. What I did NOT do, and could not

- **I did not read the source `.tex`.** This repo tracks **0** `.tex` files. The two on this
  host outside `.pogo` (`~/Documents/onethird.tex`, 364 lines; `onethird_annals.tex`, 356
  lines) contain **0** occurrences of "Cheeger" and cannot carry a line 481. So **`tex:318–324`
  and `tex:481–483` are unresolvable from the audited repo** — including the two claims mg-2de0
  asked me to verify *against the source*. I audited both as restated in mg-2de0's body and
  cross-checked against the corpus's own restatements. **This is a structural finding, not an
  excuse: the arc's most-cited external anchor is not in the repository that is the arc's
  ledger, so no audit performed in this repo can check a `tex:` citation.**
- **I did not verify the Cheeger sweep half** `(Φ*)²/2 ≤ 1 − λ_std` for `S_P`. I evaluated it
  as stated and filed **no prediction** on it.
- **I did not compute `λ_std`.** Only the corpus's master bound on `1 − λ_std`, named as a
  bound everywhere.
- **I did not re-derive** Linial's theorem, the master bound, Theorem E, or Diaconis–Graham.
  Cited; DG's *use* was checked (§2, `inv_e` = Kendall `inv` on `L(P)`, 0 exceptions / 13815).
- **I did not touch `STATE.md`.** §6 is a recommendation set for pm-onethird.
- **I did not address mg-2de0 item 2** ((iii)|frozen, and the off-class mg-3ce3 evidence). It
  is a separate, self-contained item and this audit spent its budget on Priorities 1–4.
- **Everything empirical is `n ≤ 8`** (`n ≤ 24` for the pure `(n, β)` grid, `n ≤ 59` for the
  `⌊n²/4⌋` identity). No claim here is asymptotic **except** those with closed forms verified
  against enumeration and labelled as extrapolations at the print site.

## 8. Defects of THIS instrument, recorded

1. **My runner returned exit 0 having executed nothing.** `run_all.sh` v1 used `declare -A`,
   which macOS's bash 3.2 lacks; under `set -u` it died on line 21 and **still reported 0**.
   That is exactly the returned-0-vs-examined-nothing conflation this arc has been repairing —
   committed by me, in my own runner, on its first execution. Fixed with an
   examined-nothing guard (`< 10` lines is a hard failure regardless of exit code), and the
   history is kept in the runner's header comment rather than quietly erased.
2. **Two population labels contradicted their own counts.** A1.4 was labelled "32 named + 16 on
   n=4 + 63 on n=5" while its loop measured **431**; 16 and 63 are the **unlabelled** poset
   counts, a different grain from the **labelled-with-`e`-as-identity** posets the loop builds
   (40 and 357). A1.7 said 32 where the loop measured 34. Both corrected to measured values,
   with the grain named.
3. **My own `PREDICTIONS.md` P1 says 5912 permutations as "5913".** `2+6+24+120+720+5040 =
   5912`. Recorded as a missed figure; the predictions commit is **not** amended.
4. **My selftest fired on me.** A drill asserted `δ(V) = 1/3` for `V = {0<1, 0<2}` while its own
   parenthetical said "the pair splits 1/1" — which is `1/2`. The code was right and my hand
   value wrong. Kept, corrected, and the true `1/3` witness (2-chain plus a free point) added.
5. **A4's `M` was a float inside a verdict**, violating this instrument's own stated rule that
   floats appear only in display columns. Converted to exact `Fraction`; the verdicts did not
   change, which is luck, not design.
6. **A5 is slow** (~3 min: 98442 posets × their linear extensions). Not truncated, not sampled,
   and the cost is stated rather than hidden behind a cap.
7. **`all_posets(7)` is unreachable** (2²¹ masks). §5's exhaustive sweep is `n ≤ 7` via a
   cheaper filter; the two-chain sweep reaches `n=8`. Where a population stops, the print site
   says so.
