# Can Step 6 consume L4's branch (ii)? — the ordinal-sum route, run down

**Work item:** mg-63e3 · **Method:** paper-and-pencil, **zero computation** (standing directive; nothing
here needs any — every number below is a hand-checked rational on posets of ≤ 8 elements).

**Sources:** canonical architecture
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
(L4 at `:464–474`, Steps 2–6 at `:492–515`, L1–L4 at `:557–569`, `Δ₁` at `:273`, `δ` at `:65`);
`docs/OneThird-lambda-std-Operative-Form-IndependentAudit.md` §6.2 (F3), F11, ledger rows P2/P8/29;
`docs/OneThird-lambda-std-Operative-Form.md` §3.3; `STATE.md` rows 11, mg-88bd, mg-e2de.

---

## 0. Verdict

**RED on the ticket's primary question, as asked about the stated architecture.**

> **Step 6 as written cannot consume branch (ii).** Step 6's stated mechanism is *"transfer a balanced
> pair from `P[A_k]` or `P[A_k^c]` to `P`"* (`:513–515`), justified by minimality. In branch (ii) that
> transfer **provably fails**, and it fails at *arbitrarily small leakage*: there is a hand-checkable
> family with `Δ₁ = 1/n`, in which branch (ii) holds after **two** interface modifications, the sides'
> **entire** supply of balanced pairs is a single pair balanced at exactly `p = 1/2`, and that pair sits
> at `p = 1/4` in `P`. Shrinking `ε` does not repair this — the family is parameterised so that the
> leakage goes to `0` while the displacement stays `≥ 1/4`. So **no improvement to Steps 2–5 can supply
> the missing modulus, because there is no modulus.**

**The ordinal-sum route specifically: REFUTED, and informatively.** The route was — (ii) hands you an
ordinal-sum structure, `δ(A ⊕ B) = max(δ(A), δ(B))` plus minimality hands you a balanced pair inside a
side, and the identity transports it up. Steps 1–4 of that route are sound and in fact stronger than
the corpus records (the exact ordinal sum preserves **every** `p_{xy}` on the nose, not just the
maximum — Prop. 3.1). **The route dies entirely at its unstated fifth step**, the passage from the
*exact* sum `P'` back to `P`, which the identity says nothing about and which is *verbatim branch
(iii)'s conclusion* — a disjunct of the same conjecture, hence unavailable as a hypothesis inside case
(ii), and in any case **false** (Thm 4.2).

**AMBER on branch (ii) as a whole, with the missing hypothesis named.** This is **not** a proof that
(ii) is unconsumable. The witness shows precisely *where* the balanced pair actually is — **at the
interface, not on a side** — and that suggests a specific, minimality-free lemma **(IB)** (§7) which
would consume (ii). Two independent hand families support (IB). (IB) is a **new** proof obligation
found nowhere in the corpus, it is **a special case of the 1/3–2/3 conjecture itself**, and — this is
the architectural sting — **minimality plays no role in it**.

**Daniel-level consequence, stated without softening.** The architecture as written spends minimality
**twice**: once to start the spectral chain (`δ(P) < 1/3` ⟹ bad mixing ⟹ … ⟹ thin prefix), and once
again at Step 6 to produce the pair. On branch (ii) **the second spend is provably unavailable.** The
honest description of the program on that branch is therefore: *Steps 2–5 reduce the general
conjecture to the near-ordinal-sum subclass; Step 6 must then prove the conjecture on that subclass
outright.* That is a legitimate architecture, but it is **not the advertised one**, and it means the
`⟹ balanced pair by minimality` box at `:527` is wrong on branch (ii). The proof plan needs
restructuring at that box, not completing.

**On the audit's F3.** mg-e35c said *"no repair available, because (ii) genuinely does not deliver a
balanced pair."* The clause after "because" is **CONFIRMED and now proven at a much stronger level**
than F3 argued (F3 argued from (ii)'s wording; §4 here proves the failure is quantitative, survives
`ε → 0`, and cannot be repaired by any modulus). The clause before it — *"no repair available"* — is
**OVERSTATED**: it names a property of the branch, but F3 only established a property of the branch's
*statement*, and it never tested the ordinal-sum route. §7 exhibits a candidate repair. The two claims
must be recorded separately; conflating them is how a live question gets filed as closed. Proposed
STATE.md text in §10 separates them.

---

## 1. The two claims that must not be conflated

Throughout, keep these apart:

| | Claim | Status here |
|---|---|---|
| **C1** | Branch (ii)'s *own statement* delivers no balanced pair. | **PROVEN** (trivially — it is a structural statement) and reinforced: even *augmented with minimality and the ordinal-sum identity*, it delivers none (Thm 4.2). |
| **C2** | Step 6 *as written* consumes branch (ii). | **REFUTED** (Cor. 4.4). |
| **C3** | *No* argument can consume branch (ii). | **NOT ESTABLISHED**, here or in mg-e35c. §7 gives a candidate. |

The audit asserted C1 and wrote it as though it were C3. This document proves C1 and C2-negative, and
declines C3.

---

## 2. Setup

Notation follows the source. `P` a finite poset on `n` elements; `σ` uniform on its linear extensions;
for `x ∥ y`, `p_{xy} = Pr_σ(x <_σ y)`; a pair is **`1/3`-balanced** iff `min{p_{xy}, 1−p_{xy}} ≥ 1/3`;
`δ(P) = max_{x ∥ y} min{p_{xy}, 1−p_{xy}}` (`:65`), with `δ = 0` by convention when `P` is a chain.
`Δ₁(A,B) = E|A ∖ σ(A)| / min(|A|,|B|)` (`:273`), where `σ(A)` denotes the first `|A|` elements of `σ`.
`P[S]` is the induced subposet on `S`.

**L4 as stated** (`:464–474`). There exists `F(ε) → 0` such that if `Δ₁(A,B) ≤ ε` then one of:

- **(i)** `P` contains a `1/3`-balanced pair;
- **(ii)** after removing or modifying at most `F(ε)n` interface elements, `P` becomes `P[A] ⊕ P[B]`;
- **(iii)** a balanced pair in `P[A]` or `P[B]` remains balanced up to error `F(ε)` in `P`.

**Reading adopted for (ii).** *"`P` becomes `P[A] ⊕ P[B]`"* names the **induced** subposets of the
original `P` as the summands, so the modifications alter only **cross** relations (`A`-to-`B`), never
relations internal to a side. This is the charitable reading and the one the ordinal-sum route needs;
it is flagged as an ambiguity in the ledger (row L4). Under the *removal* reading the summands are
`P[A∖S], P[B∖S]` and everything below goes through unchanged, with one extra restriction noted in §6.

---

## 3. The ordinal-sum route, stated precisely — and its first four steps, which are sound

> **R1.** Branch (ii) holds: there is `S`, `|S| ≤ F(ε)n`, with `P' := P` -after-modifying-`S` `= P[A] ⊕ P[B]`.
> **R2.** `δ(P[A] ⊕ P[B]) = max(δ(P[A]), δ(P[B]))` — the ordinal-sum-inert observation (STATE, mg-e2de row).
> **R3.** `P[A]`, `P[B]` are strictly smaller than the minimal counterexample `P`, so each is a chain or has `δ ≥ 1/3`.
> **R4.** Hence `δ(P') ≥ 1/3` (provided not both sides are chains): `P'` has a `1/3`-balanced pair.
> **R5.** *(unstated in the route, and the whole of it)* Therefore `P` has a `1/3`-balanced pair.

**Proposition 3.1 (R2, and it is stronger than the corpus records).** *Let `Q = A ⊕ B`. Then `x ∥_Q y`
iff `x,y` are both in `A` or both in `B`; the linear extensions of `Q` are exactly the concatenations
of a linear extension of `A` with one of `B`; and consequently*
> `p^Q_{xy} = p^A_{xy}` *for every `x ∥ y` in `A`, and* `p^Q_{xy} = p^B_{xy}` *for every `x ∥ y` in `B`.*

*Hence `{ p^Q_{xy} : x ∥_Q y } = { p^A } ∪ { p^B }` and `δ(Q) = max(δ(A), δ(B))`.*

*Proof.* Every `a ∈ A` satisfies `a <_Q b` for every `b ∈ B`, so no cross pair is incomparable, and
every linear extension of `Q` places all of `A` before all of `B`; the two blocks are then constrained
only by their own orders, and the map (lin.ext. `A`, lin.ext. `B`) `↦` concatenation is a bijection
onto lin.ext.(`Q`). Uniformity of `σ_Q` therefore restricts to uniformity on each block independently,
giving the displayed identity. The `δ` identity follows by taking `max ∘ min{·, 1−·}`. ∎

Two things to notice, because both matter downstream:

- **The identity is not merely about `δ`; it is pairwise and exact.** For the *exact* ordinal sum, the
  transport we want holds in the strongest imaginable form — zero displacement, every pair. This is the
  most favourable possible starting point for the route, and it is genuinely free.
- **It is a statement about `P'`, not about `P`.** R2 does not mention `P` at all. Everything the
  identity buys is spent before R5 begins.

**R3 is sound (the ticket's second "look hardest" item).** `A, B ≠ ∅` (else `min(|A|,|B|) = 0` and `Δ₁`
is undefined), so `|A|, |B| ≤ n − 1 < n`. Minimality of `P` is minimality in the number of elements, so
every poset on fewer elements satisfies the conjecture: is a chain, or has `δ ≥ 1/3`. Under the adopted
reading `P[A], P[B]` are induced subposets of the *original* `P`, so they are literally posets on `< n`
elements and are in scope. Under the removal reading they are induced on `A∖S, B∖S`, still `< n`, still
in scope. **The scope question is not where the route fails.** Two riders, both real:

- **(a) The chain escape.** If **both** sides are chains, `P' = ` chain `⊕` chain `= ` chain, `δ(P') = 0`,
  and R4 fails outright — minimality yields nothing whatsoever. The source flags this in passing
  (`:477`, *"unless that side is a chain"*) and never handles it. This is a **second, independent gap in
  the route, prior to R5**, and it is exactly the case in which minimality is vacuous. It is not
  vacuous-by-emptiness: §7's second family is precisely a near-chain of this shape.
- **(b) One side suffices.** R4 needs only *one* non-chain side, so (a) bites only in the both-chains
  case. §4's witness has `P[B]` an honest chain and still kills the route through the other side.

So R1–R4 are fine. The route stands or falls on **R5**.

---

## 4. R5 is false — and false at arbitrarily small leakage

R5 is not supplied by R1–R4. It is not supplied by Prop. 3.1, which speaks only of `P'`. Written out,
what R5 asks for is:

> *(T) — the transport statement:* if `P` is within `F(ε)n` interface modifications of `P[A] ⊕ P[B]`,
> then some balanced pair of a side is still balanced in `P`.

**Observation 4.1.** (T) is **verbatim branch (iii)'s conclusion**, under a *stronger* hypothesis
(branch (ii) rather than `Δ₁ ≤ ε`). It is therefore (a) **not available as a lemma inside case (ii)** —
L4's conclusion is a disjunction, and one may not invoke one disjunct while reasoning inside another;
and (b) exactly the object mg-3ce3 probed and mg-e35c F2 discussed. The ordinal-sum route does not
*close* (ii); at its best it *reduces (ii) to (iii)*.

That reduction would still be worth having — if (T) were true. It is not.

### Witness **W**

Fix `a ≥ 3` and `1 ≤ t ≤ a−1`. Put `n = 2a`.

- `A = {c_1 < c_2 < ⋯ < c_{a−2}} ∪ {x, y}` with every `c_j <  x`, every `c_j < y`, and `x ∥ y`.
  So `P[A] = C_{a−2} ⊕ AC_2`, an `(a−2)`-chain with a free 2-antichain on top.
- `B = {b_1 < b_2 < ⋯ < b_a}`, a chain.
- Cross relations: **all** of `A < ` **all** of `B`, **except** the `t` relations `x < b_1, …, x < b_t`,
  which are deleted — so `x ∥ b_i` for `i ≤ t`, and `x < b_{t+1}`.

This is a poset (`c_1 ⋯ c_{a−2}, y, b_1, ⋯, b_t, x, b_{t+1}, ⋯, b_a` is a linear extension), and
restoring the `t` deleted crosses turns it into exactly `P[A] ⊕ P[B]`, so **branch (ii) holds with
`|S| = t` interface elements modified** (`t` relations, touching `t+1` elements — either count is `t + O(1)`).

**Lemma 4.1 (structure of `σ_P`).** *The `2a−1` elements other than `x` are totally ordered by `P`:*
`c_1 < ⋯ < c_{a−2} < y < b_1 < ⋯ < b_a`. *`x` is above exactly `c_1, …, c_{a−2}` and below exactly
`b_{t+1}, …, b_a`. Hence the linear extensions of `P` are in bijection with the `t+2` insertion slots
for `x` strictly after `c_{a−2}` and strictly before `b_{t+1}`, namely:*

| slot | resulting linear extension | `x < y`? | `x < b_1`? |
|---|---|---|---|
| 0 | `c… x y b_1 b_2 … ` | ✔ | ✔ |
| 1 | `c… y x b_1 b_2 … ` | ✘ | ✔ |
| 2 | `c… y b_1 x b_2 … ` | ✘ | ✘ |
| … | | ✘ | ✘ |
| `t+1` | `c… y b_1 … b_t x b_{t+1} …` | ✘ | ✘ |

*and `σ` is uniform on these `t+2` extensions.*

**Consequences, all exact rationals:**

- `p^P_{xy} = 1/(t+2)` (only slot 0 puts `x` before `y`).
- `p^{P[A]}_{xy} = 1/2` — `P[A] = C_{a−2} ⊕ AC_2` has exactly two linear extensions.
- `E|A ∖ σ(A)| = t/(t+2)`: `x` is the only element of `A` that can escape the first `a` positions, and
  it does so in slots `2 … t+1`. Hence **`Δ₁(A,B) = t / ((t+2)·a)`.**
- **The sides' entire supply of incomparable pairs is `{x,y}`.** In `P[A]` every `c_j` is comparable to
  everything, so `{x,y}` is the only incomparable pair; `P[B]` is a chain and has none.

**Theorem 4.2 (R5 / (T) is false).** *Take `t = 2`. Then*

> `Δ₁(A,B) = 1/(2a) = 1/n`, *branch (ii) holds after **two** interface modifications, the sides'
> **only** balanced pair is `{x,y}` with `p^{P[A]}_{xy} = 1/2` — perfectly balanced — and*
> **`p^P_{xy} = 1/4 < 1/3`.**

*So there is no balanced pair of a side that survives into `P`, in either the stated form (`p^P ∈
[1/3 − F, 2/3 + F]` fails once `F < 1/12`) or the repaired exact form (`p^P ∈ [1/3, 2/3]` fails
outright). As `a → ∞` the hypothesis `Δ₁ = 1/n → 0` while the displacement stays `= 1/4`.* ∎

**Corollary 4.3 (shrinking `ε` does not repair it — this is the load-bearing point).** *The witness
family attains displacement `1/4` at leakage `1/n`, which is (up to constants) the smallest nonzero
leakage a prefix cut can have. Therefore **no strengthening of Steps 2–5 helps.** Steps 2–5 exist only
to make `ε` small; the failure is not a large-`ε` failure. There is no modulus `F` to check against the
chain's delivery, because there is no `F` for which (T) is true.*

**Corollary 4.4 (the answer to the ticket).** *Step 6 as written — "use near-ordinal-sum stability to
transfer a balanced pair from `P[A_k]` or `P[A_k^c]` to `P`, contradicting minimality" (`:513–515`) —
**cannot consume branch (ii)**. Minimality's only output on branch (ii) is "each non-chain side has a
balanced pair"; Thm 4.2 shows that output need not transport, at any leakage.* ∎

**Amplification.** Taking `t = ⌈√n⌉` instead of `2` gives `Δ₁ = t/((t+2)a) < 1/a = 2/n` and
`p^P_{xy} = 1/(t+2) = Θ(n^{−1/2}) → 0`, with `t = o(n)` modifications — inside branch (ii)'s budget for
any modulus `F(ε) ≳ √ε`. **The side's balanced pair is not merely nudged out of `[1/3,2/3]`; it is
annihilated.**

**The exact tolerance, and it is one.** In family **W**, `t = 0` gives `p^P = 1/2`, `t = 1` gives
`p^P = 1/3` **exactly** — on the boundary, with zero slack — and `t = 2` gives `1/4`. So

> **transport survives `t ≤ 1` and dies at `t = 2`: branch (ii)'s transport tolerance in this family is
> exactly one interface modification.**

This requires `F(ε)·n ≤ 1`, i.e. `F(ε) ≤ 1/n` — **not a modulus in `ε` at all**. This **vindicates the
shape** of mg-88bd §3.3's own steelman (*"a proof routing through (ii) needs the modified set `O(1)`,
forcing `n`-dependence"*), which §3.3 dismissed on the ground that *"the source never uses (ii)"* and
which mg-e35c F1 correctly flagged as a false universal. It is now not a steelman but a **derived
requirement**, and it is **tighter than `O(1)`: it is `≤ 1`.**

### Why it fails — the structural reason

**Proposition 4.5 (non-Lipschitzness).** *The map (poset) `↦` (linear-extension distribution) is not
Lipschitz, in any modulus, in the number of modified relations or elements. In family **W**,
`d_TV(σ_P, σ_{P'}) = 1/2` at `t = 2` and `→ 1` for `t = ⌈√n⌉`, while the individual functional
`p_{xy}` moves from `1/2` to `Θ(n^{−1/2})`.*

The mechanism, and it is why every "only pairs touching `S` are at risk" intuition fails: **`p_{xy}` is
a global functional of the entire poset.** Half the destroyed pair — `y` — participates in **no**
modification, and none of the modifications says anything about `y`. What moves is `x`'s *position
law*: deleting `x`'s obligations to the bottom of the `B`-chain frees `x` to slide `t` slots later, and
`p_{xy}` reads that law against `y`'s fixed position. The displacement is therefore driven by a
quantity — how far the freed element can slide — that **the modification count does not control**: `t`
deletions buy `t` slots of slide, and slide is what `p` measures. **No bound of the form
`|Δp| ≤ g(|S|)` with `g → 0` can hold.** This is the structural reason the ticket asked for, and it is
what makes Cor. 4.3 a proof rather than a failed attempt.

---

## 5. What the witness does — and does not — refute

Recorded explicitly, because the mistake is easy and the ticket asks for it.

| Statement | Status under **W** |
|---|---|
| `(ii) ⟹ (iii)` (the cheap absorption repair: "drop (ii), keep (i)∨(iii)") | **REFUTED.** In **W** branch (ii) holds and (iii) fails in both its stated and its repaired form. So (ii) cannot be absorbed into (iii). |
| `(ii) + minimality ⟹ balanced pair in P` | **REFUTED** as an inference (Cor. 4.4). |
| Branch (iii) as a **standalone universal** (`Δ₁ ≤ ε ⟹ some side pair preserved`) | **REFUTED.** But (iii) was never asserted standalone — it is a disjunct. See §9. |
| **L4 itself** | **NOT refuted.** In **W**, branch **(i)** holds: `{x, b_1}` has `p^P = 1/2` (slots 0,1 out of 4), so `δ(P) = 1/2`. **W** is fully consistent with L4 and with the 1/3–2/3 conjecture. |
| The 1/3–2/3 conjecture | **NOT touched.** **W** is not a counterexample and is not a minimal counterexample. |

**W** refutes *implications*, which is exactly what a route is made of. It refutes no *theorem*.

---

## 6. Riders on the two readings of (ii)

- **Removal reading.** If the `F(ε)n` interface elements are *removed*, then `P' = P[A∖S] ⊕ P[B∖S]` is
  an induced subposet of `P` on `n − |S|` elements. Minimality still applies (it is strictly smaller),
  R2/R4 are unchanged, and R5 acquires **one extra burden**: the transported pair must avoid `S`. The
  gap is the same gap, one restriction worse. Note also that induced subposets do **not** preserve
  `p_{xy}` — the same non-Lipschitz phenomenon of Prop. 4.5 applies verbatim; e.g. in `C_m ⊕ AC_2`-plus-free-point
  configurations a single deletion moves a pair from `1/3` to `1/2`.
- **Modification reading** (adopted). Modifications touch only cross relations, so `P[A], P[B]` are
  genuine induced subposets of `P`. This is the reading **W** is built in.
- **If modifications were allowed *inside* a side**, then `P[A]` as a summand of `P'` need not equal
  `P[A]` as an induced subposet of `P`, and R3's appeal to minimality applies to the wrong object. The
  source's wording ("interface elements") excludes this; recorded as a drafting ambiguity, not a defect.

---

## 7. What the witness shows positively — where the balanced pair actually is

**W** does not merely kill the route; it says where the pair went. In **W**:

- the side pair `{x,y}` is driven from `1/2` to `1/4`;
- but the modification **creates** interface incomparabilities `x ∥ b_1, …, x ∥ b_t`, with
  `p^P_{x,b_i} = (i+1)/(t+2)` — hand-check from Lemma 4.1's table: `x < b_i` in slots `0 … i`. At
  `t = 2`, `p^P_{x,b_1} = 2/4 = 1/2`, **perfectly balanced**.

**The balance is not destroyed. It migrates from the side to the interface.** Step 6 looks for it on
the side; it is at the interface.

**Second family, independent, covering the chain escape §3(a).** Let `P = C_a ⊕ C_a` (chains
`c_1 < ⋯ < c_a` and `b_1 < ⋯ < b_a`, all `c < ` all `b`), with the `t` crosses `c_a < b_1, …, c_a < b_t`
deleted. Both sides are chains, so **minimality yields literally nothing**. The same slot argument
(`c_a` inserts into `t+1` slots after `c_{a−1}` and before `b_{t+1}`) gives
`p^P_{c_a, b_i} = i/(t+1)` and `Δ₁ = t/((t+1)a) < 1/a`. At `t = 2`: `p = 1/3` and `2/3` — **both
interface pairs are balanced**, at the boundary, and branch (i) holds. So the case where the route's
prerequisite R4 fails outright is *also* rescued by an interface pair.

This is the shape of the missing lemma:

> **(IB) — Interface Balance.** There is `c > 0` and a modulus `G` such that: if `P` is not a chain and
> `P` is within `G(ε)n` interface modifications of an ordinal sum `P[A] ⊕ P[B]` across a cut with
> `Δ₁(A,B) ≤ ε`, then `P` has a `1/3`-balanced pair — and one may take it to be an **interface** pair,
> i.e. a pair `x ∥ y` with `x ∈ A, y ∈ B`.

**Properties of (IB), all of which must be recorded together:**

1. **(IB) would consume branch (ii)**, and it is the only candidate on the table that does. It is the
   named additional hypothesis the AMBER verdict rests on.
2. **(IB) is minimality-free.** It makes no reference to `P` being a minimal counterexample. Therefore
   **(IB) is a special case of the 1/3–2/3 conjecture, not a reduction of it.** On branch (ii) the
   architecture is not "reduce to minimality"; it is "reduce to a subclass, then prove the conjecture on
   that subclass directly". Minimality is spent once (starting the spectral chain), not twice.
3. **(IB) is supported by two hand families and by nothing else.** Both families above satisfy it, and
   the second does so in exactly the regime where minimality is vacuous. That is encouraging and it is
   two data points.
4. **(IB) is unproven, is not implied by L1–L3, and appears nowhere in the corpus.** It is a new open
   item, not a bookkeeping repair.
5. **In a minimal counterexample the rescue mechanism is exactly what is excluded.** If `δ(P) < 1/3`
   then *every* incomparable pair of `P` is unbalanced, interface pairs included — so a minimal
   counterexample is precisely a `P` where the migration observed in both families does not happen.
   That is either the reason the class "minimal counterexample + branch (ii)" is empty (which is what
   (IB) would prove) or the reason it is not. **This is the live question, and it is now stated.**

---

## 8. Modulus check against Steps 4/5 (the ticket's closing requirement)

The ticket asks: if the route closes, state the modulus and check it against what Steps 4/5 deliver.

**The route does not close, and the check is vacuous in an unusual and important direction.** Ordinarily
a repair "needs a stronger `ε` than the chain produces" and one prices the shortfall. Here there is **no
`ε` at which (T) holds** (Cor. 4.3): the witness family attains its full displacement at `Δ₁ = 1/n`. So:

- the transport failure is **not** a budget problem;
- **mg-88bd's `ε_spec` pinning is untouched by this finding** — it prices Step 2's input, which sits
  upstream of the failure, and remains CONDITIONAL exactly as STATE row mg-88bd records it;
- the one quantitative statement that *is* delivered is the tolerance `F(ε)n ≤ 1` of §4, which is an
  `n`-dependent condition and hence not a modulus in `ε` — feeding directly into the `n`-dependence
  question mg-e35c F1 left open.

---

## 9. Consequence for mg-3ce3's green — a flag, not a verdict

mg-3ce3 tested the **repaired** branch-(iii) predicate (exact preservation of a side pair in
`[1/3, 2/3]`) and, per STATE's mg-88bd row, reports **0 RED / 6681 up to `ε = 0.20`**.

**Family W at `a = 4`, `t = 2` is `n = 8`, `Δ₁ = 1/8 = 0.125`, and it is a RED for that predicate.**
Fully written out — `A = {c_1 < c_2 < x, y}`, `B = {b_1 < b_2 < b_3 < b_4}`, all `A < B` except
`x ∥ b_1, b_2`; the four linear extensions are

```
c1 c2 x  y  b1 b2 b3 b4
c1 c2 y  x  b1 b2 b3 b4
c1 c2 y  b1 x  b2 b3 b4
c1 c2 y  b1 b2 x  b3 b4
```

giving `p^P_{xy} = 1/4`, `p^{P[A]}_{xy} = 1/2`, `E|A∖σ(A)| = 1/2`, `Δ₁ = 1/8`, and `{x,y}` the unique
incomparable pair of either side.

`0.125 < 0.20`, so **either the probe's search family does not reach this poset, or its predicate
differs from the one stated.** The mechanism suggests the former, and suggests the specific reason:
the corroborating witness STATE records for that probe is `8AC ⊕ 8AC`-minus-**one**-cross. Two
independent structural facts make that family the *most* transport-robust one available and this the
*least*:

- **antichain sides are structurally insensitive** — removing one cross from `AC_a ⊕ AC_a` shifts a side
  pair by `O(1/a²)`, because the freed element can only overtake the single `b` whose relation was cut,
  whereas in **W** the freed element `x` can slide past a whole *chain* segment;
- **one cross removal is exactly the boundary** — §4 shows `t = 1` lands on `p = 1/3` with zero slack and
  `t = 2` breaks it. A family that only ever removes one cross **cannot** produce a RED in this shape.

**This is flagged, not asserted:** `docs/OneThird-L4-NearOrdinalSum-Stability-Probe.md` is not in-tree
in this repo at `main` (the docs directory holds only the two `lambda-std-Operative-Form` files and the
HTML), so the probe's family and predicate could not be inspected, and the standing no-computation
directive means nothing was run. **Recommended action for pm-onethird:** hand this `n = 8` instance to
whoever owns mg-3ce3 as a one-line falsifier check. If it is a RED, the probe's `ε ≈ 0.20` calibration —
which mg-e35c F5 uses to move `ε_spec` by two orders of magnitude — is measuring a family artifact.

---

## 10. Proposed STATE.md text — a **proposal to pm-onethird**, not an edit

Expected to be audited as a primary target in its own right (Appendix A step 4c). Deliberately
conservative: it claims C1 and ¬C2 and explicitly declines C3.

**Row 11 — replacement text for the second half (from "and branch (ii) is…"):**

> …and **branch (ii) is unconsumable by Step 6 *as written* — PROVEN, and the reason is not the branch's
> wording but a quantitative failure that survives `ε → 0`** (mg-63e3). Step 6's stated mechanism is
> *transfer a balanced pair from a side to `P`*; the ordinal-sum route for supplying it — (ii) gives the
> sum, `δ(A⊕B) = max(δ(A),δ(B))` plus minimality gives a pair in a side, the identity transports it —
> **fails at its last step, which is unstated and is verbatim branch (iii)'s conclusion**, hence
> unavailable inside case (ii) *and false*. Hand witness `W` (`n = 2a`, `A = C_{a−2} ⊕ AC_2`,
> `B = C_a`, two crosses `x < b_1, x < b_2` deleted): `Δ₁ = 1/n`, branch (ii) holds after **two**
> interface modifications, the sides' **only** incomparable pair is balanced at exactly `1/2` in
> `P[A]` and sits at **`1/4`** in `P`. **Shrinking `ε` does not help** — the displacement is attained at
> the smallest nonzero leakage a prefix cut admits — so **no improvement to Steps 2–5 supplies the
> missing modulus, because there is no modulus.** Structural cause: `p_{xy}` is a *global* functional
> of the poset and the poset `↦` LE-distribution map is **not Lipschitz in the modification count** —
> in `W`, `y` (half the destroyed pair) participates in no modification; what moves is `x`'s *position
> law*, since `t` deletions buy `t` slots of slide and slide is exactly what `p` measures, so no bound
> `|Δp| ≤ g(|S|)` with `g → 0` can hold. Exact tolerance in `W`:
> `t ≤ 1` survives (`t=1` gives `p = 1/3`, zero slack), `t = 2` dies — so transport needs
> `F(ε)n ≤ 1`, an `n`-dependent condition, **vindicating the shape of mg-88bd §3.3's own dismissed
> steelman and tightening it from `O(1)` to `≤ 1`**. Corollaries: **`(ii) ⟹ (iii)` is REFUTED**, so the
> cheap repair "drop (ii), keep (i)∨(iii)" is **unavailable**; and R4 has a *second*, prior gap the
> source flags and never handles (`:477`) — if **both** sides are chains, minimality yields nothing at
> all. **`W` refutes implications, not theorems: L4 itself survives via branch (i)** (`{x,b_1}` has
> `p = 1/2`), and the 1/3–2/3 conjecture is untouched.
> **Do not record this as "branch (ii) is unrepairable" — that is a different claim and it is not
> established** (and mg-e35c F3's *"no repair available"* is OVERSTATED in exactly that way; its
> *reason* clause is CONFIRMED and now proven far more strongly). `W` shows **where the pair actually
> is: balance migrates from the side to the interface** — in `W`, `p^P_{x,b_1} = 1/2` exactly; in the
> both-chains family `C_a ⊕ C_a` minus two crosses, `p^P_{c_a,b_1} = 1/3`, `p^P_{c_a,b_2} = 2/3`. The
> named candidate repair is **(IB)**: *`P` not a chain and within `G(ε)n` interface modifications of an
> ordinal sum ⟹ `P` has a balanced **interface** pair.* **(IB) is minimality-free, hence a special case
> of the 1/3–2/3 conjecture itself, not a reduction of it** — so on branch (ii) the architecture is
> *"Steps 2–5 reduce to the near-ordinal-sum subclass; Step 6 proves the conjecture there outright"*,
> and the `⟹ balanced pair by minimality` box at `:527` is **wrong on that branch**: minimality is spent
> once (starting the chain), not twice. **(IB) is new, unproven, implied by nothing in L1–L3, and
> appears nowhere in the corpus.** It is supported by the two hand families and nothing else, and in a
> minimal counterexample its rescue mechanism is exactly what `δ(P) < 1/3` forbids — which is either why
> "minimal counterexample + (ii)" is empty, or why it is not. **That is the live question.**
> **Separate flag, unresolved:** family `W` at `a = 4, t = 2` is `n = 8`, `Δ₁ = 0.125`, and is a **RED
> for the repaired branch-(iii) predicate** that mg-3ce3 reports `0 RED / 6681` on up to `ε = 0.20`.
> Not run (no-computation directive) and the probe doc is not in-tree; the likely cause is family
> selection — antichain sides shift by `O(1/a²)` per cross removal and **one** cross removal is exactly
> the zero-slack boundary, so an `AC ⊕ AC`-minus-one-cross family *cannot* produce this RED. If it
> confirms, mg-3ce3's `ε ≈ 0.20` — which mg-e35c F5 uses to move `ε_spec` by two orders of magnitude —
> is a family artifact. **Owner: pm-onethird to route to mg-3ce3.**

**Also proposed:** the graph edge at `STATE.md:64` currently reads
`"OPEN (2ndary) — L4: thin interface ⟹ balanced pair survives (beat N-poset)"`. On branch (ii) the pair
does **not** survive; the edge label should read
`"OPEN (2ndary) — L4: thin interface ⟹ P has a balanced pair (on branch (ii) NOT by survival from a side — see row 11)"`.

---

## 11. Claim ledger

Every claim, **including reductions asserted in prose** — which is the failure mode this ticket
exists to avoid.

| # | Claim | § | Label | Basis / condition |
|---|---|---|---|---|
| 1 | Lin.ext.(`A ⊕ B`) = concatenations; `p^{A⊕B}_{xy} = p^{A}_{xy}` for `x∥y` in `A` (pairwise exact) | 3.1 | **PROVEN** | Bijection argument, elementary |
| 2 | `δ(A ⊕ B) = max(δ(A), δ(B))` | 3.1 | **PROVEN** | Corollary of 1; independently recorded in STATE mg-e2de row |
| 3 | The identity is a statement about `P'`, not `P`, and is fully spent before R5 | 3 | **PROVEN** (logic) | R2's statement contains no occurrence of `P` |
| 4 | `P[A], P[B]` are strictly smaller than `P` and are in the induction's scope | 3 | **PROVEN** | `A,B ≠ ∅` from `Δ₁`'s denominator; minimality is by element count |
| 5 | "Strictly smaller" survives interface modification, under both readings of (ii) | 3, 6 | **PROVEN** | Removal shrinks the ground set; modification preserves it and the summands are induced subposets |
| 6 | If both sides are chains, R4 fails and minimality yields nothing | 3(a) | **PROVEN** | `δ(chain) = 0`; case flagged at source `:477` and unhandled |
| 7 | (T) is verbatim branch (iii)'s conclusion under a stronger hypothesis; unavailable inside case (ii) | 4.1 | **PROVEN** (logic) | Disjunct of the conjecture being proved |
| 8 | Family `W` is a poset, and branch (ii) holds for it with `\|S\| = t` | 4 | **PROVEN** | Explicit linear extension exhibited; restoring `t` crosses gives the exact sum |
| 9 | `σ_P` is uniform on `t+2` extensions given by `x`'s insertion slot | 4.1 | **PROVEN** | All other `2a−1` elements are totally ordered by `P` |
| 10 | `p^P_{xy} = 1/(t+2)`; `p^{P[A]}_{xy} = 1/2`; `Δ₁ = t/((t+2)a)` | 4 | **PROVEN** | Hand count from Lemma 4.1; `a=4,t=2` case written out in full in §9 |
| 11 | `{x,y}` is the **only** incomparable pair of `P[A] ∪ P[B]` | 4 | **PROVEN** | `c_j` comparable to all of `A`; `P[B]` a chain |
| 12 | **R5 / (T) is false**: `Δ₁ = 1/n`, two modifications, `1/2 → 1/4` | 4.2 | **PROVEN** | Claims 8–11 |
| 13 | **Shrinking `ε` does not repair it; there is no modulus `F`** | 4.3 | **PROVEN** | Displacement attained at `Δ₁ = 1/n`, the smallest nonzero prefix leakage |
| 14 | **Step 6 as written cannot consume branch (ii)** | 4.4 | **PROVEN** | Claim 12 + minimality's only output on (ii) being side pairs |
| 15 | Amplification: `t = ⌈√n⌉` gives `p^P_{xy} = Θ(n^{−1/2})` at `Δ₁ < 2/n`, `o(n)` modifications | 4 | **PROVEN** | Same slot count; budget met by any `F(ε) ≳ √ε` |
| 16 | Transport tolerance in `W` is exactly `t ≤ 1`; requires `F(ε)n ≤ 1` | 4 | **PROVEN** *for family `W`* | `t=1 ⟹ p = 1/3` exactly; `t=2 ⟹ 1/4`. **Conditional as a general claim** — it is a lower bound on the demand, from one family |
| 17 | This vindicates the *shape* of mg-88bd §3.3's steelman and tightens `O(1)` to `≤ 1` | 4 | **PROVEN** given 16 | Cross-refs mg-e35c F1 |
| 18 | Poset `↦` LE-distribution is not Lipschitz in the modification count; `p_{xy}` is global | 4.5 | **PROVEN** | `W`: `d_TV(σ_P,σ_{P'}) = 1/2` at `t=2` (hand-counted: `P'` has 2 extensions at `1/2`, `P` has 4 at `1/4`); `y` participates in no modification; `t` deletions buy `t` slots of slide |
| 19 | **`(ii) ⟹ (iii)` is REFUTED**; the "drop (ii), keep (i)∨(iii)" repair is unavailable | 5 | **PROVEN** | `W` satisfies (ii), fails (iii) in stated and repaired forms |
| 20 | `W` does **not** refute L4, and does not touch the 1/3–2/3 conjecture | 5 | **PROVEN** | `p^P_{x,b_1} = 1/2`, so branch (i) holds and `δ(W) = 1/2` |
| 21 | Balance **migrates to the interface**: `p^P_{x,b_i} = (i+1)/(t+2)` | 7 | **PROVEN** | Lemma 4.1 slot table |
| 22 | Second family `C_a ⊕ C_a` minus `t` crosses: `p^P_{c_a,b_i} = i/(t+1)`, `Δ₁ = t/((t+1)a)`; at `t=2` gives `1/3, 2/3` | 7 | **PROVEN** | Same slot argument, `t+1` slots; covers the both-chains case |
| 23 | **(IB) would consume branch (ii)** | 7 | **CONDITIONAL** — on (IB), which is **UNPROVEN** | (IB) is stated, not proved. Two supporting families, no proof, no counterexample |
| 24 | **(IB) is minimality-free, hence a special case of the 1/3–2/3 conjecture, not a reduction of it** | 7 | **PROVEN** (logic) given (IB)'s statement | (IB)'s statement quantifies over all non-chain near-ordinal-sums; no minimality hypothesis appears |
| 25 | Therefore on branch (ii) minimality is spent **once**, not twice, and `:527`'s `⟹ balanced pair by minimality` is wrong on that branch | 0, 7 | **PROVEN** given 14 + 24 | Follows from 14 (the second spend is unavailable) and 24 |
| 26 | In a minimal counterexample the migration mechanism is excluded (`δ < 1/3` kills interface pairs too) | 7 | **PROVEN** | Definition of `δ(P) < 1/3` |
| 27 | **Branch (ii) is unconsumable by *any* argument (C3)** | 1 | **NOT ESTABLISHED — explicitly declined** | Neither proved nor disproved here or in mg-e35c. §7 gives a live candidate |
| 28 | mg-e35c F3's *"no repair available"* is OVERSTATED; its *reason* clause is CONFIRMED | 0, 1 | **PROVEN** (as a claim about F3's own argument) | F3 argued from (ii)'s wording; it did not test the ordinal-sum route and does not establish C3 |
| 29 | `W` at `a=4, t=2` is a RED for the repaired branch-(iii) predicate at `Δ₁ = 0.125` | 9 | **PROVEN** (that it is a RED); **UNVERIFIED** (that it contradicts mg-3ce3) | The poset and its `p`-values are hand-computed; the probe's family/predicate could not be inspected (doc not in-tree) and nothing was run |
| 30 | The likely cause is family selection (antichain sides `O(1/a²)`; one cross removal is the zero-slack boundary) | 9 | **HEURISTIC** | The `O(1/a²)` estimate is a sketch, not computed; the boundary fact (claim 16) is proven |
| 31 | mg-88bd's `ε_spec` pinning is untouched by this finding | 8 | **PROVEN** (logic) | `ε_spec` prices Step 2's input, upstream of the R5 failure; the failure is not a budget failure (claim 13) |
| 32 | Under the removal reading, R5 acquires the extra burden that the pair must avoid `S` | 6 | **PROVEN** | `P'`'s ground set is `(A∪B)∖S` |
| 33 | "(ii) modifies only cross relations" is the adopted reading; the alternative breaks R3's object | 2, 6 | **CONDITIONAL** on the reading — flagged as a source ambiguity | Source says "interface elements" and names `P[A], P[B]` as summands; both point to the adopted reading |

**Reductions asserted in prose and separately labelled** (the mg-88bd failure mode):

| # | Prose reduction | Label |
|---|---|---|
| R-a | "the ordinal-sum route *reduces* (ii) to (iii)" | **PROVEN** — claim 7. And the reduction is worthless, since (iii) is a disjunct of the same conjecture *and* is false here (claim 19) |
| R-b | "minimality's only output on branch (ii) is 'each non-chain side has a balanced pair'" | **PROVEN** — minimality is a statement about strictly smaller posets, and the only strictly smaller posets branch (ii) hands you are the sides |
| R-c | "(IB) closes branch (ii)" | **CONDITIONAL** on (IB) — claim 23. Not asserted as available |
| R-d | "the architecture needs restructuring, not completing, at `:527`" | **PROVEN** for branch (ii) only — claim 25. **Not** asserted for branches (i)/(iii), and **not** asserted as a claim about the program as a whole |

---

## 12. Answers to the ticket's two "look hardest" items

1. **The `F(ε)n` slack.** *This is where it dies, and it dies harder than branch (iii) did.* Branch
   (iii)'s trouble was a *slack* problem — `[1/3−F, 2/3+F]` is consistent with `δ < 1/3` — repairable by
   restating the predicate. Branch (ii)'s trouble is that **the transport itself is false**, at any
   modulus, at arbitrarily small `ε`, with the modified elements disjoint from the destroyed pair. It is
   **not** the same answer as (iii)'s.
2. **Are `P[A], P[B]` in the induction's scope?** **Yes — cleanly, under both readings of (ii)** (claims
   4, 5). *The scope is not the problem.* The two riders are (a) both sides can be chains, in which case
   minimality yields nothing and R4 fails before R5 is reached (claim 6), and (b) if modifications were
   permitted inside a side, R3 would appeal to minimality about the wrong object — excluded by the
   source's wording (claim 33).
