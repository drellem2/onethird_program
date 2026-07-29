# Independent adversarial audit — `OneThird-L4-Branch-ii-Sublinear-Modulus.md` (mg-3af9, commit `e2ccee6`)

**Auditor work item:** mg-c8c6 · **Target:** `docs/OneThird-L4-Branch-ii-Sublinear-Modulus.md`, added by `e2ccee6`
(derived from the parent's merge commit per STATE.md Appendix A; the commit adds **one** file and nothing else).
**Method:** paper-and-pencil, **zero computation**. Every poset, every linear-extension count and every
rational below was rebuilt from the poset definitions by hand, not checked against the document's
arithmetic. **Independence:** I did not author the target and did not read its ledger before rebuilding
`W*`. **Routing:** pm-onethird (first-line). **I did not edit `STATE.md`.**

**Sources pulled directly, not accepted from quotation:**
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex` — `Φ_P`/`Φ_P^*`
at `:230–237`, `K_k` at `:243–248`, the prefix no-inversion fact at `:254–256`, `Δ₁` at `:271–275`,
the `ε ≪ 1` prose at `:457–461`, L4 at `:464–474`, `:476–479`, Steps 1–6 at `:490–515`;
`docs/OneThird-L4-Branch-ii-Consumability.md` (mg-63e3) §§4, 5; its audit (mg-f825) §§3.1–3.6;
`STATE.md` rows 11, 132, 133 and Appendix A.

---

## 0. Verdict

> **OVERSTATED.** The headline is **CONFIRMED — and it is the strongest correct result this arc has
> produced.** `W*` is real: I rebuilt it from the poset axioms and it genuinely escapes `Δ₁·n < 2`,
> genuinely carries one modified element, and genuinely defeats every strictly positive modulus,
> sub-linear included. **The escape is constructed, not asserted.** The document also correctly
> self-audits the exact quantifier defect that killed its predecessor, and does not relocate it.
>
> **The over-reach moved.** It is no longer in the headline; it is in the **new general theorem the
> document introduces to explain the headline**. **Theorem A (Budget–Leakage) is BROKEN as scoped.**
> Its proof silently assumes that a certificate's modifications cannot propagate — and *transitivity
> propagates them*. Under the reading the document's own §2 supplies ("*the resulting **poset***"),
> Theorem A is false **by an unbounded factor**, and so is the flagship promotion built on it:
> §3.1's *"any attempt to refute a sub-linear modulus by building a better balanced witness is
> **provably doomed**"*. **I built one** (§4 below, family `V*`, verified by hand at `N = 3` by direct
> enumeration of all 14 linear extensions and by a closed form at general `N`).
>
> So: **`W*` — yes. The promotion from instance to theorem — not as stated.** That is the
> second pressure point the dispatch named, and it is where the document breaks.

**Four-for-four, at a new location — this is the finding pm-onethird should carry forward.**
mg-d112, mg-e35c and mg-f825 each had sound arithmetic and a broken universal *in the headline*.
mg-3af9 **fixed the headline** — §5.1/§5.2's self-audit is correct, and I could not break Theorem B.
It then introduced a *new* universal one level down, to explain the headline, and **that** one is
broken, in the same shape: a property that is incidental to the instance (`W`/`W*`'s certificates
happen to be **local** — only `x`'s own pairs change) read as a law about all certificates. The
pattern is not "these documents over-claim their headlines". The pattern is **"these documents
over-claim whichever statement is the most general one they wrote that day."** The generalisation
step is the object to audit first, wherever it sits.

**Ledger tally:** 30 CONFIRMED · 4 CONFIRMED-conditionally (condition stated by the document) ·
**1 BROKEN as scoped** (claim 4, with 4 dependents demoted to conditional) · 1 BROKEN as labelled
(a §4.1 table row) · 1 unledgered prose reduction · **0 arithmetic errors anywhere.**

---

## 1. The dispatch's four press points, answered first

### 1.1 Does `W*` actually live outside `Δ₁·n < 2`? — **YES. Rebuilt independently. CONFIRMED.**

Rebuilt from the definition with no reference to the document's tables (§3 below). Every one of the
three load-bearing facts holds:

| the claim | my independent finding |
|---|---|
| `B`-chain lengthened, `Δ₁` unchanged | **CONFIRMED.** `EK = 1/2` for every `b ≥ max(a,3)`; only `x` can leak, and only in 2 of 4 slots |
| `Δ₁·n` **unbounded**, not merely larger | **CONFIRMED.** `Δ₁·n = (a+b)/(2a)`, `b` free at fixed `a`; `≥ 2` once `b ≥ 3a`, `→ ∞` |
| **ONE** modified element | **CONFIRMED** under *both* readings — modification (`S = {x}`, the only differing cross pairs are `(x,b_1),(x,b_2)`, both incident to `x`) and removal (delete `x` ⟹ `chain ⊕ chain`) |
| the sides' *only* incomparable pair, `1/2 → 1/4` | **CONFIRMED.** `P[A] = C_{a−2} ⊕ AC_2` has exactly one incomparable pair; `P[B]` is a chain |

**This is not the failure mode the dispatch bet on.** `W*` is a genuine escape and Theorem B is a
genuine theorem. I attacked it four ways (§3.5) and it survived all four.

### 1.2 The Budget–Leakage promotion — **BROKEN as scoped. This is the finding.**

Theorem A's proof contains the step:

> *"Neither element is removed and neither has its relations altered, so the pair survives with its
> relation intact."*

This is **not** a consequence of `x,y ∉ S`. A poset modification made at `S` propagates to pairs
disjoint from `S` **by transitivity**. Concretely (§4.1): let `A` be a 3-chain, `B` a 3-chain, no
cross relations. Then `Δ₁ = 1/2`, `Δ₁·min(|A|,|B|) = 3/2` — and modifying the **single** element
`a_3` (adding `a_3 < b_1`) turns `P` into `P[A] ⊕ P[B]` exactly. `|S| = 1 < 3/2`. **Theorem A is
false**, and the gap is unbounded: two `N`-chains give `Δ₁·m = N/2` against `|S| = 1`.

The general mechanism is one line and it is not a corner case:

> **If `P[A]` has a unique maximal element `z`, then `S = {z}` is a one-element branch-(ii)
> certificate for *any* `Δ₁` whatsoever** — add `z < b` for every `b ∈ B` (all incident to `z`);
> transitivity supplies `a < z < b` for every `a ∈ A`.

`W` and `W*` are immune to this because their `A`-side has **two** maximal elements (`x` and `y`) —
which is exactly why the incidental locality of their certificates was invisible to the author.
**That is the instance's property being read as a law**, precisely as the dispatch predicted, just at
a different inequality than expected.

**What survives, and it is worth keeping.** Theorem A is **fully correct** under the *removal*
reading (deleting `S` leaves the induced subposet, and induced relations cannot be created), and
under a *local* modification reading in which the modified poset is required to agree with `P` on
every pair disjoint from `S`. Both are defensible formalisations of `:469–470`. **The document
neither states the hypothesis nor notices that the two disambiguations differ** — it asserts the
opposite (claim 4's basis: *"holds under **both** readings of (ii), since the proof never names the
summands"*). The problem was never the summands.

**And the promotion's conclusion fails too, not just its proof.** §3.1 asserts that *no balanced-cut
witness* can refute `F(ε) < ε/2` and that better-balanced witnesses are *"provably doomed"*. Under
the transitive-closure reading I exhibit a **balanced-cut witness** (`β = 1/2` exactly) that refutes
(T) with `F(ε)` an unbounded factor below `ε/2` — §4.2. So the failure is not a technicality about
which formalisation is charitable: the two readings give **different mathematics**, and the document
picked neither.

### 1.3 The quantifier — **NOT relocated. CONFIRMED, and stated explicitly as the dispatch asks.**

> **The sub-linear claim holds for EVERY `F` that is strictly positive on the sequence
> `{1/(2a) : a ≥ 3}` — it is a genuine universal over moduli, not a statement along one sequence
> supplied by `W*`.**

The inference direction is the reverse of mg-63e3's and it is valid. Fix `ε = 1/(2a)`; `F(ε)` is then
a **fixed positive number**; `W*(a,b)` supplies **unboundedly many `n`** at that same `ε`
(`Δ₁ = 1/(2a)` is independent of `b`, verified — §3.2 fact 1); choose `b ≥ 1/F(ε)`. No `(ε,n)` pair
is ever locked. Contrast mg-63e3's `W`, where `ε = 1/n` *identically* and the family therefore
ranged over no free `n` at all. **§5.1's self-audit table is accurate and §5.2's diagnosis of its own
predecessor is correct.** I tried to break this and could not.

Two exactness notes for the row, neither fatal:

- The universal is over moduli **strictly positive on that sequence**. A modulus vanishing there is
  not refuted — and `Cor. B2` says so correctly (it degenerates branch (ii) to *exact* ordinal sum).
  §0's flat opening sentence *"No modulus rescues Step 6's transfer on branch (ii) — sub-linear,
  linear, or otherwise"* is literally false for `F ≡ 0`, and is repaired by the very next sentence.
  Repair the sentence, not the theorem.
- `ε` ranges over `{1/(2a)}`, a discrete sequence accumulating at `0`, not over all `ε > 0`. For any
  monotone `F` this is no restriction (vanishing on the sequence forces vanishing on `(0,1/6]`), and
  the document never claims more. **Correctly quantified.**

### 1.4 Consistency with the corrected `STATE` — **it is a state-change, and I say so plainly.**

`mg-c7b7` (`bc75274`) landed row 11's conditional form: *"branch (ii) is unconsumed … for every
modulus `F(ε) = Ω(ε)` — a **conditional** statement, and the condition is load-bearing"*.
**mg-3af9 discharges that condition, and it is entitled to.** Theorem B is sound and `Ω(ε)` was
exactly the gap `W` could not cross. The row **should** move from conditional to unconditional.

**But the row proposed in §9 must not be pasted as written** — it states the Budget–Leakage
inequality flat, as *"elementary"*, with a parenthetical proof sketch that reproduces the broken step.
That is the single most damaging thing in the document, because §9's row is what outlives it, and an
inequality recorded as elementary is an inequality that gets reused without its hypothesis. Required
repairs in §7 below.

The mg-88bd row at `:132` — **correctly does not flip**, and for the right reason (claims 26–27,
both CONFIRMED). `ε_spec` untouched — CONFIRMED. `C3` still declined — CONFIRMED, and correctly so.

---

## 2. What the source actually says (verified line by line, not quoted from the document)

| document's citation | my reading of the source | verdict |
|---|---|---|
| `Δ₁(A,B) = E\|A∖σ(A)\| / min(\|A\|,\|B\|)` (`:271–275`) | verbatim | ✔ |
| *"Since `e` is a linear extension, there is no relation `b <_P a` with `a∈A, b∈B`"* (`:254–256`) | verbatim | ✔ |
| L4 (ii): *"after removing or modifying at most `F(ε)n` interface elements, `P` becomes `P[A]⊕P[B]`"* | verbatim | ✔ |
| L4's quantifier: *"There exists `F(ε)→0` such that if `Δ₁(A,B) ≤ ε`, then one of…"* | verbatim — **`∃F ∀ε ∀(P,A,B)`, `n` unconstrained** | ✔ |
| Step 6 (`:513–515`) | verbatim | ✔ |
| `Φ_P^* = min_{0<\|A\|≤n/2} Φ_P(A)` (`:235–237`) | verbatim — minimisation over **all** cut sizes | ✔ |
| `:457–461` prose gives `Δ₁ = ε` (**equality**) vs `:466` `Δ₁ ≤ ε` (**inequality**) | confirmed, both present | ✔ |

**The (E1)/(E2) tension is real** and the document is right to flag it. It is right, too, that (E2)
is the steelman and that refuting the steelman is worth more. **Scope check passes: no strawman.**
The statement refuted, (T), is the statement Step 6 needs, quantified as the source quantifies it.

---

## 3. `W*`, rebuilt from scratch

Built from the definition alone. `a ≥ 3`, `b ≥ max(a,3)`, `n = a+b`.
`A = {c_1<⋯<c_{a−2}} ∪ {x,y}`, all `c_j < x`, all `c_j < y`, `x ∥ y`. `B = b_1<⋯<b_b`.
All `A < B` except `x<b_1`, `x<b_2` deleted.

### 3.1 It is a poset, and `A` is a prefix cut — CONFIRMED

Transitivity: the only elements below `x` are the `c_j`, and every `c_j < b_i` is retained
**directly**, so no deleted cross is forced back through `x`; nothing sits strictly between `x` and
`b_1` or `b_2` (the elements above `x` are `b_3,…,b_b`, and none is `≤ b_1`). Antisymmetry and
reflexivity are immediate. **`A` is a down-set**: below `c_j` are earlier `c`'s; below `x` and below
`y` are only `c`'s. Hence `A` is a prefix of a linear extension and **Fact 2.1 applies** — I checked
this rather than assuming it, since Theorem A and the whole `K` analysis rest on it.

### 3.2 Exactly four linear extensions, and the six rationals — CONFIRMED

The `n−1` elements other than `x` are totally ordered: `c_1<⋯<c_{a−2}<y<b_1<⋯<b_b` (each link
verified: `c_{a−2}<y` ✔, `y<b_1` ✔). `x` is above exactly the `c_j` and below exactly `b_3,…,b_b`, so
`x` inserts into exactly **four** slots, and `LE(P)` is in bijection with them.

| slot | linear extension | first `a` elements | `K` | `x<y` | `x<b_1` | `x<b_2` |
|---|---|---|---|---|---|---|
| 0 | `c… x y b_1 b_2 b_3…` | `{c…,x,y}` = `A` | **0** | ✔ | ✔ | ✔ |
| 1 | `c… y x b_1 b_2 b_3…` | `{c…,y,x}` = `A` | **0** | ✘ | ✔ | ✔ |
| 2 | `c… y b_1 x b_2 b_3…` | `{c…,y,b_1}` | **1** | ✘ | ✘ | ✔ |
| 3 | `c… y b_1 b_2 x b_3…` | `{c…,y,b_1}` | **1** | ✘ | ✘ | ✘ |

I verified independently that **no element other than `x` can leak**: the `c_j` precede everything
outside `A` and occupy the first `a−2` positions in every extension; `y < b_i` for all `i`, so `y`
sits at position `a−1` or `a`. Hence `K ∈ {0,1}` always, and `K = 1` exactly on slots 2, 3.

`#LE = 4` ✔ · `p^P_{xy} = 1/4` ✔ · `p^{P[A]}_{xy} = 1/2` ✔ (`P[A] = C_{a−2} ⊕ AC_2`, two extensions)
· `EK = 1/2` ✔ · `m = min(a,b) = a` ✔ · **`Δ₁ = 1/(2a)`** ✔ · `p^P_{x,b_1} = 1/2` ✔ ·
`p^P_{x,b_2} = 3/4` ✔. The three incomparable pairs of `P` are `{x,y}`, `{x,b_1}`, `{x,b_2}`, so
`δ(P) = max{1/4, 1/2, 1/4} = 1/2` ✔.

**All six rationals reproduce. `W*(a,a) = W(a)` at `t = 2`** — checked against mg-63e3 §4's
definition and mg-f825's confirmed table: `W`'s general-`t` form gives `t+2` slots, `EK = t/(t+2)`,
`Δ₁ = t/((t+2)a)`, which at `t = 2` is `1/2` and `1/(2a)`. Consistent.

### 3.3 The `a=4, b=28` instance — CONFIRMED element by element

`A = {c_1<c_2<x, c_1<c_2<y, x∥y}`, `B = b_1<⋯<b_{28}`, `n = 32`. Four extensions:
`c1 c2 x y b1…`, `c1 c2 y x b1…`, `c1 c2 y b1 x b2…`, `c1 c2 y b1 b2 x b3…`.
First-4 prefixes: `{c1,c2,x,y}`, `{c1,c2,y,x}`, `{c1,c2,y,b1}`, `{c1,c2,y,b1}` ⟹ `EK = 2/4 = 1/2` ✔.
`min(4,28) = 4` ⟹ `Δ₁ = 1/8` ✔. **`Δ₁·n = 4 > 2`** ✔. One modified element ✔.

### 3.4 Theorem B — CONFIRMED

At `ε := 1/(2a)`: hypothesis `Δ₁ ≤ ε` holds **with equality** (so (E2) as well as (E1)) ✔; branch (ii)
holds with `|S| = 1 ≤ F(ε)·n` once `b ≥ 1/F(ε)`, since `n ≥ b` ✔; the sides' only balanced pair sits
at `1/2` and lands at `1/4 < 1/3` ✔. **(T) is false at `ε`, for every `F` with `F(ε) > 0`.** The only
inequality used is `F(ε)·n ≥ F(ε)·b ≥ 1`. **Correct, and the strongest result in this arc.**

Consistency cross-check the document offers, `|S| = 1 ≥ Δ₁·m = 1/2`: this holds, but note it is a
check against a theorem I refute in §4 — it happens to be a case where Theorem A is true (local
certificate), so it is not evidence for Theorem A's generality.

### 3.5 Four attacks on `W*`, all of which fail

1. **"`Δ₁` secretly depends on `b`."** No — `EK = 1/2` for every `b ≥ 3`, and `m = a` for every
   `b ≥ a`. Both bounds are explicit in the definition. **Attack fails.**
2. **"`|S| = 1` is a relation/element unit trick" (mg-f825 §3.6's live issue).** No — `|S| = 1` under
   element-counting, `|S| = 1` under removal, and the two differing *pairs* number 2. Branch (ii)
   counts elements (`:469–470`, verified). Every count admits the witness at some `n`. **Attack fails.**
3. **"`δ(W*) = 1/2`, so it is not a minimal counterexample and is out of scope."** L4 is universally
   quantified over `P` (`:463–474`, verified) and Step 6 cites it as a general lemma. Restricting (T)
   to frozen `P` makes its conclusion false unless the class *"minimal counterexample ∧ (ii)"* is
   empty. **Attack fails** — this is mg-f825 §2's rebuttal and it still holds. (L4 at `:464–474`.)
4. **"The cut is degenerate — `β → 0`, so Steps 2–5 would never produce it."** This is the strongest
   objection and the document meets it honestly rather than dismissing it: it *is* the mechanism
   (§6), it *is* why a balance hypothesis would help, and the chain provably does not supply one
   (`Φ_P^*` minimises over all cut sizes, `:235–237`, verified). **Attack fails as a refutation, and
   the document converts it into its own §6 and open item F-bal.** Credit where due.

---

## 4. Breaking Theorem A — the counterexamples

Both families below were built by hand from the poset axioms; the `N = 3` case of `V*` is verified by
**direct enumeration of all 14 linear extensions**, and the general-`N` closed form reproduces it.

### 4.1 Theorem A is false under the transitive-closure reading — `U*`

> **`U*(N)`.** `A = a_1<⋯<a_N`, `B = b_1<⋯<b_N`, **no cross relations at all**. `n = 2N`.

`A` is a down-set (nothing outside `A` lies below any `a_i`), so `(A,B)` is a prefix cut and Fact 2.1
holds vacuously. `LE(U*)` = all interleavings of two `N`-chains, uniform. Each position is a
`B`-element with marginal probability `1/2`, so `E[#B in first N] = N/2`, i.e.

  **`EK = N/2`, `m = N`, `Δ₁ = 1/2`, `Δ₁·m = N/2`.**

*Hand check at `N = 3`, by direct count:* shuffles with exactly `j` `a`'s in the first three number
`C(3,j)·C(3,3−j)` = `1, 9, 9, 1`, summing to `C(6,3) = 20` ✔; `E[j] = 30/20 = 3/2`; `EK = 3 − 3/2 =
3/2` ✔ `= N/2`.

**The certificate.** Modify the relations incident to `a_N` — add `a_N < b_1` (`a_N < b_i` follows
from `b_1<b_i`). The resulting **poset** is `a_1<⋯<a_N<b_1<⋯<b_N`, which is exactly `P[A] ⊕ P[B]`.
**`|S| = 1`.**

> **Theorem A claims `|S| ≥ Δ₁·m = N/2`. The truth is `|S| = 1`. The gap is unbounded in `N`.**

At `N = 3`: `|S| = 1` against a claimed lower bound of `3/2` — already a counterexample, on six
elements. Under the *removal* reading the certificate costs `N` (deleting `a_N` leaves two disjoint
chains, not an ordinal sum), and Theorem A is satisfied — **as predicted, the theorem tracks removal,
not modification.**

**Where the proof goes wrong, exactly.** With `σ = b_1…b_N a_1…a_N`, `X_σ = A`, `Y_σ = B`, `K = N`.
Take `x = a_1 ∉ S` and `y = b_1 ∉ S`. The proof says this pair *"survives with its relation intact"*.
It does not: `a_1 < a_N < b_1` in the closure. **Neither endpoint was touched and the pair changed
anyway.** The covering argument is valid; the premise it covers is not.

Remark 3.1 (claim 5, `|S| ≥ (max_σ K)²` under relation-counting) inherits the same defect: in `U*(3)`
it claims `|S| ≥ 9` where **one** added relation suffices. It is true only under the "count pairs
whose comparability status changes" convention — which is the *local* reading again, and which the
remark does not name.

### 4.2 A balanced-cut witness that refutes (T) below `ε/2` — `V*`, against §3.1's *"provably doomed"*

`U*` refutes the inequality but has chain sides, so (T) is vacuous there. This one is not.

> **`V*(N)`, `N ≥ 3`.** `A = {u, v} ∪ {z_1<⋯<z_{N−2}}` with `u,v < z_1` and `u ∥ v`.
> `B = b_1<⋯<b_N`. Cross relations: **`v < b_1`** (hence `v < b_i` for all `i`) **and nothing else** —
> `u`, and every `z_j`, is incomparable to every `b_i`. `n = 2N`, `|A| = |B| = N`, **`β = 1/2` exactly.**

*Poset and prefix cut.* Transitivity: below `v` is nothing, above `b_1` are the later `b`'s, so
`v < b_i` for all `i` and nothing else is forced; `z_1 > v` forces no `z`–`b` relation. `A` is a
down-set (below `u`, `v`: nothing; below `z_j`: `u,v` and earlier `z`'s), and
`u,v,z_1,…,z_{N−2},b_1,…,b_N` is a linear extension with `A` as its prefix. **Prefix cut ✔.**
Fact 2.1 ✔ (the only cross relations point `A → B`).

*The sides.* `P[A] = AC_2 ⊕ C_{N−2}` — its **only** incomparable pair is `{u,v}`, at
`p^{P[A]}_{uv} = 1/2`, **balanced**. `P[B]` is a chain. So the sides' entire supply is one pair, as in
`W*`.

*The certificate — one element.* `z_{N−2}` is the **unique maximum** of `P[A]`. Add `z_{N−2} < b_1`
(one relation, incident to `z_{N−2}`). Closure gives `u < z_1 < ⋯ < z_{N−2} < b_1 < ⋯ < b_N`, so every
`A`-element is below every `B`-element, internal relations untouched: the result **is** `P[A] ⊕ P[B]`.
**`|S| = 1`.**

*Linear extensions.* `u` and `v` are the only minimal elements, so every extension starts with one.
- starts with `u` ⟹ the rest is `LE` of `P∖{u}`, where `v` is the unique minimum, then a free shuffle
  of the `z`-chain (`N−2`) with the `b`-chain (`N`): `C(2N−2, N)` extensions;
- starts with `v` ⟹ `LE` of `P∖{v}` = shuffle of the chain `u<z_1<⋯<z_{N−2}` (`N−1`) with the
  `b`-chain (`N`): `C(2N−1, N)` extensions.

`C(2N−1,N)/C(2N−2,N) = (2N−1)/(N−1)`, so

  **`p^P_{uv} = Pr(u <_σ v) = (N−1)/(3N−2) < 1/3` for every `N`** (since `3N−3 < 3N−2`).

*Leakage.* Conditioning on the two cases and using `E[#B in first r of a uniform shuffle of p and q]
= rq/(p+q)`:

  `EK = (N−1)/(3N−2) · N(N−2)/(2N−2) + (2N−1)/(3N−2) · N(N−1)/(2N−1) = N(3N−4) / (2(3N−2))`,
  so **`Δ₁ = EK/N = (3N−4)/(2(3N−2)) → 1/2`.**

*Hand verification at `N = 3`, all 14 extensions enumerated.* `A = {u,v,z}`, `B = {b_1,b_2,b_3}`.
Starting with `u` (4 extensions): `uvz b_1b_2b_3` (`K=0`), `uvb_1zb_2b_3`, `uvb_1b_2zb_3`,
`uvb_1b_2b_3z` (`K=1` each). Starting with `v` (10 extensions, `v` then a shuffle of `(u,z)` with
`(b_1,b_2,b_3)`): first-three prefixes `{v,u,z}` (`K=0`, ×1), `{v,u,b_1}` (`K=1`, ×3), `{v,b_1,u}`
(`K=1`, ×3), `{v,b_1,b_2}` (`K=2`, ×3). **`ΣK = 3 + 12 = 15`, `EK = 15/14`** — and the closed form
gives `3·5/(2·7) = 15/14` ✔. `Δ₁ = 5/14` ✔. `p^P_{uv} = 4/14 = 2/7 < 1/3` ✔ (closed form `2/7` ✔).

**Consequences.**

| statement | `V*` says |
|---|---|
| **Theorem A**, `\|S\| ≥ Δ₁·m` | **FALSE.** `Δ₁·m = N(3N−4)/(2(3N−2)) ≈ N/2` vs `\|S\| = 1` |
| **Corollary A2**, balanced cut ⟹ `F(ε) ≥ ε/2` | **FALSE.** Admission needs only `F(ε) ≥ 1/(2N)`; `ε/2 → 1/4`. At `N=3` already: `1/6 < 5/28 = ε/2` |
| **§3.1**, *"any better-balanced witness is **provably doomed**"* | **FALSE.** `V*` is balanced (`β = 1/2`), refutes (T) (only side pair `1/2 → (N−1)/(3N−2) < 1/3`), and is admitted by moduli far below `ε/2` — e.g. `F(ε) = ε/100` admits `V*(100)` |
| **Corollary A3 / §6's vacuity mechanism** | **CONDITIONAL** on the same reading; a balance hypothesis does *not* empty branch (ii) if certificates may propagate |
| **Theorem B / `W*` / the headline** | **UNTOUCHED.** `W*`'s certificate is local, so it is admitted under every reading |

**Under the *removal* or *local* reading, `V*` costs `N−1` (the minimum vertex cover of the
`(N−1)×N` grid of cross-incomparabilities), Theorem A holds, and `V*` is not a counterexample.**
The entire dispute is the unstated hypothesis — which is why the fix is a hypothesis, not a retraction.

### 4.3 Why this is the predicted defect, in the predicted place

The dispatch: *"A promotion from instance to theorem is exactly where an instance's incidental
property gets read as a law."* The incidental property is **locality of the certificate**. In `W` and
`W*`, `S = {x}` and the only pairs that change are `x`'s own, because the `A`-side has two maximal
elements and the gadget deletes crosses at one of them. Every certificate the author had ever
examined was local. The proof then assumes locality of *all* certificates — in a single subordinate
clause, with no hypothesis and no remark — and the document's §2 explicitly certifies the result
under both readings it names. **The arithmetic is, once again, flawless. The generalisation is,
once again, one quantifier too wide.**

---

## 5. Claim ledger — exhaustive, including reductions asserted in prose

Every numbered claim of §10, every prose reduction of the R-table, **and the claims made in prose
that the document's own ledger omits** (the mg-63e3 failure mode the dispatch names).

### 5.1 The numbered claims

| # | § | document's label | **audit** |
|---|---|---|---|
| 1 | 2 | PROVEN (textual) | **CONFIRMED.** `Δ₁` at `:271–275`, budget `F(ε)n` at `:469–470`; normalisations do differ |
| 2 | 2.1 | PROVEN | **CONFIRMED.** `:254–256` verbatim |
| 3 | 3 (∗) | PROVEN | **CONFIRMED.** Positions `≤\|A\|` vs `>\|A\|` give `y <_σ x` ⟹ `x ≮_P y`; Fact 2.1 gives `y ≮_P x`. Cross-incomparability, correctly derived |
| **4** | **3** | **PROVEN** — *"holds under both readings"* | **BROKEN AS SCOPED.** CONFIRMED under the removal reading and under a local modification reading; **FALSE, by an unbounded factor, under the transitive-closure modification reading** (§4.1, `U*`). The proof's clause *"neither has its relations altered, so the pair survives"* is an unstated non-propagation hypothesis. The offered basis (*"the proof never names the summands"*) is not the issue |
| 5 | 3.1 | PROVEN | **CONDITIONAL, mislabelled.** True under "count pairs whose status changes"; **false** under "count relations added" — `U*(3)` needs one added relation against a claimed `≥ 9`. The remark names neither convention |
| 6 | A1 | PROVEN | **CONFIRMED given claim 4** ⟹ inherits claim 4's condition. The algebra (`β·Δ₁ ≤ F(ε)`) is exact |
| 7 | A2 | PROVEN *given (E2)* | **CONDITIONAL on (E2) *and* on claim 4's reading** — the document states the first condition and not the second. Under the transitive-closure reading it is **FALSE** (`V*`, §4.2) |
| **8** | **3.1** | **PROVEN *given (E2)*** — *"no balanced-cut witness can refute `F(ε) < ε/2`"* | **BROKEN under the transitive-closure reading** (`V*` is a balanced-cut witness refuting (T) at `F(ε) ≪ ε/2`); CONFIRMED under removal/local. **This is the flagship promotion and it must not land unconditioned.** Minor separate note: mg-f825's constant is `ε/2` as an *infimum over `t`*, approached and never attained, so *"recovered exactly"* is a shade generous at the endpoint |
| 9 | 3.2 | PROVEN | **CONFIRMED.** `LE(P[A]⊕P[B])` = concatenations, so same-side `p` values are preserved exactly. Re-derived, not read |
| 10 | 3.2 | PROVEN | **CONFIRMED** |
| 11 | 4.1 | PROVEN | **CONFIRMED.** Transitivity and the down-set property re-checked independently (§3.1) |
| 12 | 4.2 | PROVEN | **CONFIRMED.** Four slots; I verified separately that no element but `x` can leak |
| 13 | 4 | PROVEN | **CONFIRMED.** All six rationals reproduced by hand, plus the `a=4,b=28` instance element by element |
| 14 | 4 | PROVEN | **CONFIRMED.** `EK = 1/2` and `m = a` for every `b ≥ max(a,3)`. **This is the load-bearing fact of the escape and it holds** |
| 15 | 4 | PROVEN | **CONFIRMED.** `{x,y}` is `P[A]`'s only incomparable pair; `P[B]` is a chain |
| 16 | 4 | PROVEN | **CONFIRMED** under both readings; `x` is an interface element |
| **17** | **4** | **PROVEN — Theorem B** | **CONFIRMED.** Independently rebuilt. Survived four attacks (§3.5) |
| 18 | 4 | PROVEN | **CONFIRMED.** Both `cε` and `o(ε)` are strictly positive at each `ε = 1/(2a)` |
| **19** | **B1** | **PROVEN** | **CONFIRMED.** `Δ₁·n = (a+b)/(2a)`, `≥ 2` iff `b ≥ 3a`, unbounded. **The escape is real** |
| 20 | B2 | PROVEN | **CONFIRMED** |
| 21 | 4.1 | PROVEN | **CONFIRMED.** `1/4 < 1/3 − F(ε)` iff `F(ε) < 1/12`; under the repaired (iii) predicate `[1/3,2/3]`, refuted at every `ε` |
| 22 | 4.1 | PROVEN | **CONFIRMED.** `p^P_{x,b_1} = 1/2` ⟹ branch (i) holds ⟹ L4 not refuted; `δ(W*) = 1/2` re-derived from all three incomparable pairs |
| 23 | 4.1 | PROVEN (logic) | **CONFIRMED.** Sound, and identical in shape to mg-f825 §2, correctly attributed |
| 24 | 5.1 | PROVEN (self-audit) | **CONFIRMED.** The table is accurate: `ε` fixed by `a`, `n` varied by `b`, `\|S\|` invariant |
| 25 | 5.2 | PROVEN (logic) | **CONFIRMED.** The inference runs `ε` first, `n` free — the reverse of mg-63e3's Cor. 4.3, and valid |
| 26 | 5.3 | PROVEN | **CONFIRMED.** `F(ε,n)` excludes `W*` only if `F(ε,n)·n < 1` for all `n` |
| 27 | 5.3 | PROVEN (logic) | **CONFIRMED.** No `n`-dependence requirement arises, so the `:132` row does not flip. **Correct restraint — this is the trap the previous deliverable fell into, and this one does not** |
| 28 | 5.4 | PROVEN *given (E1)* | **CONFIRMED-conditional**, with one condition under-argued: *"`F(ε) ≤ ε`, which any useful modulus satisfies for small `ε`"* is asserted, not shown, and is **false for `F(ε) = √ε`** — a legitimate L4 modulus (`F → 0`). The rider is correctly flagged as a rider; the parenthetical should say "assume", not "any useful modulus" |
| 29 | 1.1, 8 | PROVEN (textual) | **CONFIRMED.** Both lines pulled; the source is inconsistent |
| 30 | A3, 6.1 | PROVEN *given (E2)* | **CONDITIONAL on (E2) *and* on claim 4's reading.** Second condition unstated. Under transitive closure, a balance hypothesis does not empty (ii) |
| 31 | 6.2 | PROVEN (textual) | **CONFIRMED.** No step of 1–6 constrains `k`; `Φ_P^*` minimises over all cut sizes (`:235–237`, verified). L3 says nothing about balance |
| 32 | 8 | OPEN — stated, not claimed | **CORRECTLY LABELLED.** See §6 for a strength note on its billing |
| 33 | 7 | PROVEN (logic) | **CONFIRMED.** `ε_spec` prices Step 2's input, upstream; distinct object from `ε_leak` (the mg-e35c collision), kept distinct throughout |
| 34 | 7 | PROVEN (by inspection) | **CONFIRMED.** Theorem B uses only `F(ε)n ≥ 1`; the refuted `Θ(1/n)` premise appears nowhere |
| 35 | 6.3 | PROVEN | **CONFIRMED.** `W*` is not a chain, is one modification from an ordinal sum, and has a balanced pair — consistent with repaired (IB) |
| 36 | 4.1, 6.3 | NOT ESTABLISHED — declined | **CORRECTLY DECLINED.** Theorem B refutes the *stated transfer*, not every argument. **Keep declined** |
| 37 | 0, 9 | PROVEN | **CONFIRMED.** Conclusion re-established by a different family and a different quantifier route; mg-f825's break of the original proof stands |

### 5.2 The prose reductions the document ledgers

| # | **audit** |
|---|---|
| R-a | **BROKEN under the transitive-closure reading** (it is claim 8). Under removal/local: CONFIRMED. **The single clause most in need of a condition before it reaches `STATE.md`** |
| R-b | **CONDITIONAL.** *"`β` is the unique remaining degree of freedom"* is a consequence of claim 6, hence of claim 4. Under transitive closure the certificate's **locality** is a second free parameter, and `V*` spends *that* one at `β = 1/2` |
| R-c | **CORRECTLY LABELLED CONDITIONAL**, and the document deserves credit for not asserting it as available. Add claim 4's reading as a third condition |
| R-d | **CORRECTLY SPLIT** — PROVEN about the text, HEURISTIC about what a completed Step 4 could deliver. This is exactly the right labelling and the arc has not always managed it |
| R-e | **CONFIRMED.** mg-f825 §6's modulus-free refutation of standalone (iii) is independent of everything at issue here, and `W*` does reproduce it at unbounded `n` |
| R-f | **CONFIRMED** |
| R-g | **CONFIRMED in substance, over-attributed in form.** That the failure persists at every `ε` is claim 17 and is solid. That it is *"removed by re-normalisation"* is claim 30, hence conditional; so the *localisation* to the normalisation is conditional even though the *failure* is not |
| R-h | **CONFIRMED.** `Δ₁ = ε` with equality in `W*`, so (E2) is met and (E1) is weaker. Reading-independence of **Theorem B** holds — note this is reading-independence in `ε`, not in the (ii)-certificate sense at issue in §4 |

### 5.3 Claims made in prose and **missing from the document's own ledger**

| where | claim | **audit** |
|---|---|---|
| §4.1, table row 3 | *"`(ii) + minimality ⟹ balanced pair in P` — **REFUTED**"* | **BROKEN AS LABELLED.** `W*` **has** a balanced pair in `P` (`p^P_{x,b_1} = 1/2`) and is not a minimal counterexample, so it neither satisfies the hypothesis nor violates the conclusion. What `W*` refutes is the *route* — "the pair minimality supplies is a side pair, and side pairs need not transport" — which is just (T) again, i.e. row 1. The document's own §4.1 motto (*"`W*` refutes implications, not theorems"*) is violated by its own table two rows above the motto. **Restate as a route refutation or delete the row** |
| §3.1 | *"any attempt to refute a sub-linear modulus by building a better balanced witness is **provably doomed**"* | Content = claim 8, so formally ledgered; but it is the document's **strongest universal** and appears in prose in its strongest form. **REFUTED under the transitive-closure reading** (§4.2) |
| §8, item 3 | *"narrowing (ii) strengthens the conjecture"* | **CONFIRMED.** Shrinking the budget shrinks a disjunct, so L4 becomes strictly harder. Correct and unledgered |
| §5.3 | *"the clause was aimed at the wrong object"* | **CONFIRMED** as a characterisation, and the operative conclusion (do not land it) is right |

**No result stronger than the headline is missing from the ledger** — the mg-63e3 omission is not
repeated. The omissions here are one mislabelled row and two harmless prose asides.

---

## 6. Template steps not yet covered

**Step 3 — label audit.** Labels are largely honest, and the ledger's use of *"PROVEN **given (E2)**"*
is genuinely good practice. Two demotions required: claim 4 (and 5), and the four claims that inherit
from it (6, 7, 8, 30) plus R-a/R-b/R-g. **No heuristic is promoted to a proven-sounding headline** —
R-d in particular is split correctly.

**Step 4 — scope check.** §0's headline matches §4's proof. **No strawman**: (T) is the statement
Step 6 needs, at the source's own quantifiers, and all cited `.tex` ranges verify verbatim. One
literal-falsity nit at `F ≡ 0`, repaired in the next sentence (§1.3).

**Step 4b — strength check on the proposed target `F-bal`.** Run forward: `F-bal` (Cheeger sweeping
delivers a prefix cut with `min(k,n−k) ≥ β₀n` at controlled loss in `Φ`) ⟹ [via A3] any `o(ε)` modulus
**empties** branch (ii) ⟹ the burden falls on `(i) ∨ (iii)` ⟹ `(iii)` standalone is already refuted at
every `ε`, modulus-free. **So `F-bal` is not a sufficient condition masquerading as a step — it is
strictly weaker than the goal, and the document says so.** But its billing is too strong: *"the single
question on which the value of a sub-linear modulus now turns"* is (a) conditional on claim 4's
reading, and (b) about a route the document itself shows terminates in an already-refuted disjunct.
**Landing `F-bal` as an open item: yes. Landing that sentence: no.**

*Falsifier quantifier.* §5.2's falsifier for Theorem B ("a modulus with `F(ε) > 0` admitting no member
of `W*`, i.e. `F(ε)n < 1` for all `n`") is correctly stated and correctly quantified — over `n` at
fixed `ε`, which is the parameter at issue. **The step-4b defect is not present.**

**Step 4d — quantifier audit.** Answered in §1.3: **the defect is not relocated.** The one universal
that *is* wrongly quantified is Theorem A's — quantified over all certificates on evidence from
certificates that are all local.

**Step 5 — object/coordinate check.** `Δ₁` (Axis 1) vs `δ` (Axis 2) kept distinct ✔. `p^P` vs
`p^{P[A]}` distinct ✔. `ε_spec` vs `ε_leak` distinct and correctly separated ✔. `F`'s **two roles** —
budget in (ii), tolerance in (iii) — the coordinate mg-f825 named: **handled correctly here**; claim 21
uses the tolerance role and claim 17 the budget role, without merging them. **No conflation found.**

**Step 6 — cross-doc consistency.** The document supersedes mg-c7b7's conditional row 11 clause
(justified — §1.4), amends the mg-63e3 row to *"conclusion re-established, proof still invalid"*
(accurate), leaves the mg-88bd `:132` row unflipped (correct), keeps `C3` declined (correct), and
keeps repaired-(IB) live with `W*` as a third supporting instance (checked: `W*` is not a chain, is
one modification from an ordinal sum, and has a balanced pair — the instance is genuine). **It does
not contradict any merged claim except the one it is entitled to discharge.**

**Step 7 — constraint compliance. CLEAN, verified at the commit and not from the document's own
sentence.** `git show e2ccee6 --name-status` reports exactly one line: `A
docs/OneThird-L4-Branch-ii-Sublinear-Modulus.md`. Zero scripts, zero datasets, zero enumerations; the
only code block is a four-line hand-written list of linear extensions. **This audit is likewise
computation-free** — every count above is a hand count on posets with at most 20 linear extensions.

---

## 7. What must change before §9's row lands (for pm-onethird)

**Land, unchanged — this is real and it is the arc's best result:**

- The **RED at full strength**: no strictly positive modulus rescues Step 6's stated transfer on
  branch (ii); `F(ε) = ε/4` and every `F(ε) = o(ε)` included. Row 11's `Ω(ε)` condition is
  **discharged** and the conditional form can go.
- **`W*`**, with its parameters: `Δ₁ = 1/(2a)` independent of `b`, `Δ₁·n = (a+b)/(2a)` unbounded, one
  modified element, `1/2 → 1/4`, the `a=4,b=28` instance. **Fully rebuilt and confirmed.**
- The degenerate-escape clause (`F ≡ 0` ⟹ (ii) means exact ordinal sum ⟹ L4 strictly stronger).
- `(ii) ⟹ (iii)` refuted at every modulus; L4 itself not refuted (branch (i) holds); conjecture untouched.
- No `n`-dependence clause; **the `:132` mg-88bd row does not flip**; `ε_spec` untouched; `C3` declined.
- The normalisation diagnosis *as a description of `W*`* — budget `~ n`, hypothesis `~ min(|A|,|B|)`,
  and `W*` spends the ratio.

**Do not land as written — repair first:**

1. **The Budget–Leakage clause.** The row states `|S| ≥ Δ₁·min(|A|,|B|)` flat, calls it *"elementary"*,
   and reproduces the broken step in its parenthetical. **It is false as stated** (`U*`: two `N`-chains,
   `Δ₁·m = N/2`, `|S| = 1`). Land it only with its hypothesis: *"for certificates that do not propagate
   — i.e. under the removal reading, or under a modification reading in which the modified poset agrees
   with `P` off `S`."* An inequality recorded as elementary will be reused without its hypothesis.
2. **The promotion clause.** *"No balanced-cut witness can refute `F(ε) < ε/2`"* must carry the same
   condition. Under the transitive-closure reading there **is** such a witness (`V*`, `β = 1/2`,
   `F(ε) ≈ 1/(2N) ≪ ε/2`). Delete *"provably doomed"* in every form.
3. **The vacuity clause** (`o(ε)` empties (ii) given balance or re-normalisation): same condition.
   The honest *"this is a change to L4, not a reading of it"* and *"Steps 2–5 do not deliver it"*
   halves are sound and should stay.
4. **`F-bal`**: land as an open item; drop *"the single question on which the value of a sub-linear
   modulus now turns"*.
5. **The §4.1 table row** *"(ii) + minimality ⟹ balanced pair in `P` — REFUTED"*: restate as a route
   refutation or delete it. `W*` satisfies that conclusion.
6. **A new open item is now owed** and it is cheap and consequential:
   **(RD) — which reading does branch (ii) carry?** `:469–470` does not say whether a modification at
   `S` may propagate. The two disambiguations are **not equivalent**: under one, every prefix cut whose
   `A`-side has a unique maximal element is in branch (ii) at `|S| = 1` regardless of `Δ₁`, which makes
   branch (ii) far more inclusive and (T) correspondingly *easier* to refute; under the other, `|S|` is
   bounded below by `Δ₁·min(|A|,|B|)`. **Every threshold statement in this arc — mg-f825's `ε/2`,
   mg-3af9's Theorem A, and any future budget calibration — depends on the answer.** Recommend the
   source be tightened, alongside the (E1)/(E2) drafting flag mg-3af9 already raises. Note the
   direction of the risk: **the permissive reading strengthens mg-3af9's RED and weakens its
   Theorem A** — nothing in the headline is at stake, only the generalisation.

---

## 8. Honest net

**Real progress, and more of it than the last two deliverables produced.** `W*` is a genuine
construction that reaches a regime the previous witness provably could not, and it converts a
conditional row into an unconditional one that I could not break. The self-audit in §5.1–5.2 is the
first time in this arc that a deliverable has correctly diagnosed and avoided its predecessor's
quantifier defect. The restraint on the `n`-dependence clause and on `C3` is exactly right, and the
document declines to claim the vacuity route as a repair when it would have been easy to.

**Against that: one broken universal, in the newly-general theorem rather than the headline.** The
Budget–Leakage inequality — the document's own bid to turn one family's fact into a law — is false
under a reading its own §2 licenses, by an unbounded factor, and the flagship *"provably doomed"*
promotion falls with it. **The mathematics is right; the generalisation is one quantifier too wide —
which is the same verdict shape as the last three audits in this arc, at a different generalisation
each time.**

The forward-looking version, for pm-onethird: **stop auditing these documents' headlines first.**
Audit **whichever statement in the document is the most general one it wrote** — because that is
where the incidental property of the instance gets read as a law, and that is now four for four.
