# Does a sub-linear modulus rescue Step 6's consumption of L4 branch (ii)?

**Work item:** mg-3af9 · **Method:** paper-and-pencil, **zero computation** (standing directive).
Every rational below is a hand count on a poset with **four** linear extensions.

**Sources, all pulled and read directly, not accepted from quotation:**
canonical architecture `~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
— `Δ₁` at `:271–275`, the prefix-cut no-inversion fact at `:254–256`, L4 at `:464–474`,
`:476–479`, Steps 2–6 at `:492–515`, the summary box at `:527`, L1–L4 at `:557–569`;
`docs/OneThird-L4-Branch-ii-Consumability.md` (mg-63e3); its audit
`docs/OneThird-L4-Branch-ii-Consumability-IndependentAudit.md` (mg-f825) §§3.1–3.3, 5, 6;
`STATE.md` rows 11, `:132`, the mg-88bd row.

---

## 0. Verdict

**RED, and the witness reaches the regime.**

> **No modulus rescues Step 6's transfer on branch (ii) — sub-linear, linear, or otherwise.**
> The obstruction is not a budget shortfall in `ε`. It is a **normalisation mismatch inside L4's own
> statement**: branch (ii)'s budget is `F(ε)·n`, while the hypothesis `Δ₁` is normalised by
> `min(|A|,|B|)` (`:273`, verified). The ratio `n / min(|A|,|B|)` is **unbounded**, and
> **one** modified interface element — the smallest possible non-trivial certificate — already
> annihilates a side's entire supply of balanced pairs. Since `F(ε)·n ≥ 1` for every `n ≥ 1/F(ε)`,
> and `n` is free once `ε` is fixed, **every strictly positive modulus admits the witness.**
>
> The witness is **W\*** (§4): family **W** of mg-63e3 with its `B`-side chain **lengthened**.
> It satisfies `Δ₁ = 1/(2a)` with `n = a + b` and `b` **free**, so
> **`Δ₁ · n = (a+b)/(2a) → ∞`.** It lives arbitrarily far **outside** `Δ₁·n < 2` — the regime
> mg-f825 §3.1 correctly showed **W** could never leave. Concretely at `a = 4, b = 28`:
> `n = 32`, `Δ₁ = 1/8`, `Δ₁·n = 4`, **one** modified element, sides' **only** incomparable pair
> balanced at exactly `1/2` in `P[A]` and at **`1/4`** in `P`.

**And the audit's `ε/2` threshold is now explained, not merely confirmed.** §3 proves a new
elementary inequality —

> **Theorem A (Budget–Leakage).** Any branch-(ii) certificate `S` satisfies
> **`|S| ≥ Δ₁(A,B) · min(|A|,|B|) = E|A ∖ σ(A)|`.**

— from which mg-f825's threshold falls out as a **structural constant**, not a feature of family
**W**: under the source's own tight reading `ε = Δ₁` (`:461–463`, an *equality*), **no balanced-cut
witness whatsoever** can refute a modulus with `F(ε) < ε/2`. The audit was right about **W** and
right for a reason far more general than it claimed. Theorem A also identifies the *unique*
remaining degree of freedom — **cut balance** — and **W\*** is exactly the family that spends it.

**The one thing a sub-linear modulus does buy, stated precisely, and it is not the ticket's GREEN.**
By Theorem A, adding **either** a cut-balance hypothesis `min(|A|,|B|) ≥ β₀n` **or** re-normalising
the budget to `F(ε)·min(|A|,|B|)` makes any sub-linear modulus **empty branch (ii) outright** under
the tight reading. Step 6 then "consumes" (ii) **vacuously**. But (a) this is a **change to L4**, not
a reading of it; (b) **Steps 2–5 do not deliver the balance hypothesis** — nothing in Steps 3–5 or
L2/L3 constrains `k`, and Cheeger conductance is *defined* to permit unbalanced cuts; and (c) with
(ii) emptied, the whole burden moves to `(i) ∨ (iii)`, and **(iii) as a standalone universal is
already refuted at every `ε`, modulus-free** (mg-f825 F4). The repair **relocates and prices** the
gap. It does not close it.

**What this does and does not do to the record.** mg-63e3's *conclusion* — no modulus exists — is
**re-established here on a correct basis and at full strength**. Its *proof* remains invalid exactly
as mg-f825 found; the corrected argument needs a different family and a different quantifier route,
and both are supplied below. **The `n`-dependence clause that STATE deliberately did not land stays
un-landed, and is now moot**: §5.3 shows that even an `n`-dependent budget cannot exclude **W\***
unless it falls below **one element**, so this work supplies **no** reason to flip the mg-88bd row at
`STATE.md:132`. C3 (*"no argument can consume (ii)"*) remains **declined**.

---

## 1. The question, stated exactly

Step 6 (`:513–515`, verbatim): *"Use near-ordinal-sum stability to transfer a balanced pair from
`P[A_k]` or `P[A_k^c]` to `P`, contradicting minimality."* The statement it needs on branch (ii) is
mg-63e3's **(T)**:

> **(T)** — Let `(A,B)` be a prefix cut with `Δ₁(A,B) ≤ ε`. If `P` becomes `P[A] ⊕ P[B]` after
> removing or modifying at most `F(ε)n` interface elements, then some `1/3`-balanced pair of `P[A]`
> or `P[B]` is still balanced in `P`.

mg-63e3 refuted (T) with family **W**; mg-f825 confirmed every rational in **W** and broke the
*universal*, because **W** is confined to `Δ₁·n < 2` and a witness only enters branch (ii) when
`|S| ≤ F(ε)n`. What survives is: **(T) is false for every `F(ε) = Ω(ε)`.**

**This document asks the residue:** does `F(ε) = ε/4`, or any `F(ε) = o(ε)`, make (T) true?

**A distinction the ticket's phrasing merges, and it matters.** `F(ε) = ε/4` is **not** `o(ε)` — it
is `Θ(ε)`. It is merely *below the `ε/2` threshold*. So there are two questions, and Theorem A
answers them uniformly, because the threshold is a threshold on the constant `F(ε)/ε`, not on the
growth class:

- **(Q1)** linear with a small constant, `F(ε) = cε` with `c < 1/2`;
- **(Q2)** genuinely sub-linear, `F(ε) = o(ε)`.

### 1.1 Two readings of L4's `ε`, and both are answered

The conjecture (`:466–468`) says *"if `Δ₁(A,B) ≤ ε`"* — an **inequality**, `ε` free. The prose that
introduces it (`:461–463`) says *"Suppose a minimal counterexample has a prefix `A_k` with
`Δ₁(A_k,A_k^c) = ε ≪ 1`"* — an **equality**.

| | reading | branch-(ii) budget for a poset with leakage `δ₀` |
|---|---|---|
| **(E1)** | literal conjecture: `ε` is any bound `≥ Δ₁` | `F(ε)·n` for **any** `ε ≥ δ₀` |
| **(E2)** | source's prose / the steelman: apply L4 at the tightest valid `ε` | `F(δ₀)·n` |

**(E2) is the steelman and this document refutes the steelman.** mg-f825 §3.1 implicitly adopted
(E2) (it evaluated the budget at *"the witness's own leakage"*), and that is the correct, charitable
choice: a careful proof applies L4 at the smallest `ε` it can verify. §4's witness refutes (T) under
**both** readings, so the headline is reading-independent. §5.4 records what changes under (E1)
alone — where even the *original* balanced **W** already suffices, a second and independent
correction to the audit's threshold claim, offered as a rider rather than as the load-bearing route.

---

## 2. Setup and the one structural fact the source supplies

Notation as in mg-63e3 §2. `P` a finite poset on `n` elements, `σ` uniform on `LE(P)`,
`p_{xy} = Pr_σ(x <_σ y)` for `x ∥ y`, balanced means `min{p, 1−p} ≥ 1/3`,
`δ(P) = max_{x∥y} min{p_{xy}, 1−p_{xy}}`. For a prefix `A = A_k = {1,…,k}` of the distinguished
linear extension `e`, `B = [n] ∖ A`, `σ(A)` = the first `|A|` elements of `σ`, and (`:271–275`)

  `Δ₁(A,B) = E|A ∖ σ(A)| / min(|A|,|B|)`.

Write `m := min(|A|,|B|)` and `K(σ) := |A ∖ σ(A)| = |σ(A) ∖ A|` (the two are equal since
`|σ(A)| = |A|`). So `E K = Δ₁ · m`.

**Fact 2.1 (source, `:254–256`, verbatim).** *"Since `e` is a linear extension, there is no relation
`b <_P a` with `a ∈ A`, `b ∈ B`."* Hence for a prefix cut, every cross pair is either `a <_P b` or
`a ∥_P b`. **This is the only structural input Theorem A needs, and the source supplies it.**

**Reading of branch (ii).** As in mg-63e3, "removing or modifying at most `F(ε)n` interface
elements" is read as: there is a set `S` of elements, `|S| ≤ F(ε)n`, such that after deleting the
elements of `S` and/or altering the relations incident to them, the resulting poset is an ordinal
sum with the `A`-part below the `B`-part. Theorem A holds under **both** the modification reading
(`P[A] ⊕ P[B]`, summands induced in the original `P`) and the removal reading
(`P[A∖S] ⊕ P[B∖S]`) — the proof never names the summands.

---

## 3. Theorem A — the Budget–Leakage inequality

> **Theorem A.** Let `(A,B)` be a prefix cut of `P` and let `S` be any branch-(ii) certificate, i.e.
> a set of elements whose removal/modification turns `P` into an ordinal sum with all surviving
> `A`-elements below all surviving `B`-elements. Then
>
>   **`|S| ≥ max_σ K(σ) ≥ E K = Δ₁(A,B) · min(|A|,|B|).`**

*Proof.* Fix any `σ ∈ LE(P)` and put `X_σ = A ∖ σ(A)` (the `A`-elements after position `|A|`) and
`Y_σ = σ(A) ∖ A` (the `B`-elements inside the first `|A|` positions); `|X_σ| = |Y_σ| = K(σ)`.

Every element of `Y_σ` occupies a position `≤ |A|` and every element of `X_σ` a position `> |A|`, so
`y <_σ x` for every `(x,y) ∈ X_σ × Y_σ`. Since `σ` is a linear extension, `x ≮_P y`. By Fact 2.1
`y ≮_P x`. Hence

  **every pair in `X_σ × Y_σ` is incomparable in `P`, and it is a cross pair.**  (∗)

Now suppose `x ∈ X_σ ∖ S` and `y ∈ Y_σ ∖ S`. Neither element is removed and neither has its
relations altered, so the pair survives with its relation intact: in the resulting poset `x ∥ y`
with `x` on the `A` side and `y` on the `B` side. That contradicts the result being an ordinal sum
with the `A`-part below the `B`-part. So for every pair in `X_σ × Y_σ`, at least one endpoint lies
in `S`.

If `X_σ ⊆ S` then `|S| ≥ |X_σ| = K(σ)`. Otherwise pick `x₀ ∈ X_σ ∖ S`; then every `y ∈ Y_σ` must lie
in `S`, so `|S| ≥ |Y_σ| = K(σ)`. Either way `|S| ≥ K(σ)`. As `σ` was arbitrary,
`|S| ≥ max_σ K(σ) ≥ E K = Δ₁ m`. ∎

**Remark 3.1 (relation-counting is strictly stronger).** If `|S|` counts modified *relations* rather
than elements, (∗) forces all `K(σ)²` pairs to be repaired, giving `|S| ≥ (max_σ K(σ))² ≥ (Δ₁m)²`.
Every statement below therefore holds a fortiori under relation-counting; element-counting is the
weakest reading and the one used throughout. (mg-f825 §3.6 is right that the two counts differ and
that the difference is not `O(1)`; §4's witness has `|S| = 1` under element-counting and `|S| = 2`
under relation-counting, and both are admitted, so nothing below turns on the choice.)

### 3.1 Corollary — the audit's `ε/2` is a structural constant, not a property of **W**

> **Corollary A1.** If branch (ii) holds with budget `F(ε)n`, then `Δ₁(A,B) ≤ F(ε)·n/m`.
> Equivalently, writing the cut's **balance** `β := m/n ∈ (0, 1/2]`, branch (ii) requires
> **`β · Δ₁ ≤ F(ε)`.**

> **Corollary A2.** Under the tight reading **(E2)** (`ε = Δ₁`), branch (ii) requires
> **`F(ε) ≥ β·ε`**. In particular at a **balanced** cut (`β = 1/2`) it requires **`F(ε) ≥ ε/2`**.

**This is the audit's §3.1 threshold, promoted from a fact about family `W` to a theorem about every
balanced cut.** mg-f825 established *"`W` cannot refute `F(ε) ≤ ε/2`"*; Corollary A2 establishes
*"**no** balanced-cut witness can refute `F(ε) < ε/2`, under (E2)"*. Both the numerical value `1/2`
and its element-counting variant in the audit's table are recovered exactly. So the audit's
obstruction is not an artefact of the family it was aimed at — it is the truth about the whole
balanced regime, and any attempt to refute a sub-linear modulus by building a *better balanced*
witness is **provably doomed**.

Corollary A1 also says precisely where the remaining freedom is: **`β`**. The budget is normalised
by `n`; the hypothesis by `m = βn`. Drive `β → 0` and the budget outruns the hypothesis without
bound. §4 does exactly that.

### 3.2 The minimum non-trivial certificate is **one element**

If `|S| = 0` then `P = P[A] ⊕ P[B]` exactly and transport holds in the strongest possible form —
every `p_{xy}` on a side is preserved on the nose (mg-63e3 Prop. 3.1, re-verified: linear extensions
of an ordinal sum are exactly the concatenations, so `σ` restricts to a uniform linear extension of
each summand). **So a witness needs `|S| ≥ 1`, and `|S| = 1` is the whole game:** if one modified
element suffices to break transport, then *every* budget `≥ 1` is defeated, and the only surviving
moduli are those whose budget is `< 1` element — i.e. those for which branch (ii) *means* "exact
ordinal sum".

---

## 4. Witness **W\*** — outside `Δ₁·n < 2`, at one modified element

Family **W** of mg-63e3 with the `B`-side chain **lengthened and decoupled from `a`**. Everything
in the gadget is unchanged; only `|B|` moves.

> **Definition (W\*).** Fix `a ≥ 3` and `b ≥ max(a, 3)`. Put `n = a + b`.
>
> - `A = {c_1 < c_2 < ⋯ < c_{a−2}} ∪ {x, y}`, with every `c_j < x`, every `c_j < y`, and `x ∥ y`.
>   So `P[A] = C_{a−2} ⊕ AC_2`.
> - `B = {b_1 < b_2 < ⋯ < b_b}`, a chain. `|A| = a`, `|B| = b`, so `m = min(|A|,|B|) = a`.
> - Cross relations: **all** of `A <` **all** of `B`, **except** that `x < b_1` and `x < b_2` are
>   deleted (i.e. mg-63e3's parameter `t = 2`, held fixed).

`W\*(a, a) = W(a)`. The change is `b`, and `b` is free.

**Lemma 4.1 (it is a poset, and `A` is a prefix cut).** The relation is transitive: the only
elements below `x` are the `c_j`, and each `c_j < b_i` is retained directly, so no deleted relation
is forced back through `x`; nothing lies strictly between `x` and `b_1` or `b_2`. `A` is a down-set
(below `c_j`: earlier `c`'s; below `x` and below `y`: only `c`'s), so `A` is a prefix of a linear
extension `e` and Fact 2.1 applies. Restoring the two deleted crosses yields exactly
`P[A] ⊕ P[B]`. ∎

**Lemma 4.2 (four linear extensions).** The `n − 1` elements other than `x` are totally ordered:
`c_1 < ⋯ < c_{a−2} < y < b_1 < ⋯ < b_b`. `x` is above exactly `c_1,…,c_{a−2}` and below exactly
`b_3,…,b_b`. So `LE(P)` is in bijection with the **four** insertion slots for `x` in the open gap
containing `y, b_1, b_2`, and `σ` is uniform on them:

| slot | linear extension | `x < y`? | `x < b_1`? | `x < b_2`? | first `a` elements | `K` |
|---|---|---|---|---|---|---|
| 0 | `c… x y b_1 b_2 b_3 …` | ✔ | ✔ | ✔ | `{c…, x, y}` | 0 |
| 1 | `c… y x b_1 b_2 b_3 …` | ✘ | ✔ | ✔ | `{c…, y, x}` | 0 |
| 2 | `c… y b_1 x b_2 b_3 …` | ✘ | ✘ | ✔ | `{c…, y, b_1}` | 1 |
| 3 | `c… y b_1 b_2 x b_3 …` | ✘ | ✘ | ✘ | `{c…, y, b_1}` | 1 |

(The "first `a` elements" column: `a−2` c's plus two more.) ∎

**All the exact rationals, and there are six:**

| quantity | value | hand count |
|---|---|---|
| `#LE(P)` | `4` | Lemma 4.2 |
| `p^P_{xy}` | `1/4` | slot 0 only |
| `p^{P[A]}_{xy}` | `1/2` | `P[A] = C_{a−2} ⊕ AC_2` has 2 linear extensions |
| `E K = E\|A ∖ σ(A)\|` | `1/2` | `K = 1` in slots 2, 3 |
| **`Δ₁(A,B)`** | **`1/(2a)`** | `(1/2) / min(a,b) = (1/2)/a`, using `b ≥ a` |
| `p^P_{x,b_1}`, `p^P_{x,b_2}` | `1/2`, `3/4` | slots `{0,1}` resp. `{0,1,2}` |

**The three facts that make it a witness.**

1. **`Δ₁` does not see `b`.** `E K = 1/2` regardless of `b` (only `x` can leak, and only in slots 2
   and 3), and `m = a` as soon as `b ≥ a`. So `Δ₁ = 1/(2a)` is a function of `a` **alone**.
2. **`n` is free at fixed `Δ₁`.** `n = a + b` with `b` unbounded. Hence
   **`Δ₁ · n = (a+b)/(2a)` is unbounded.**
3. **One element repairs it.** `P` and `P[A] ⊕ P[B]` differ only on the cross pairs `(x,b_1)` and
   `(x,b_2)`; both involve `x`, so **`S = {x}`**, `|S| = 1`. And `x` is an interface element (it is
   incomparable to `B`-elements). Under the removal reading, deleting `x` also works and gives
   `chain ⊕ chain`, again `|S| = 1`.

**The sides' entire supply of balanced pairs is one pair.** In `P[A]` every `c_j` is comparable to
everything, so `{x,y}` is the only incomparable pair; `P[B]` is a chain and has none. That pair is
balanced **at exactly `1/2`** in `P[A]`, and it sits at **`1/4`** in `P`.

> **Theorem B (no modulus rescues transport).** Let `F` be any function with `F(ε) > 0`. Fix `a ≥ 3`
> and set `ε := 1/(2a)`. Choose any `b ≥ max(a, 3, 1/F(ε))`. Then `W\*(a,b)` satisfies:
>
> - `Δ₁(A,B) = ε` — so the hypothesis `Δ₁ ≤ ε` holds, **with equality**, and reading (E2) is
>   satisfied as well as (E1);
> - branch (ii) holds with `|S| = 1 ≤ F(ε)·n`, since `n ≥ b ≥ 1/F(ε)`;
> - the sides' **only** incomparable pair is balanced at `1/2`, and `p^P_{xy} = 1/4 < 1/3`.
>
> Hence **(T) is false at `ε`.** Since `a` is arbitrary, (T) is false at every `ε` in
> `{1/(2a) : a ≥ 3}`, a sequence tending to `0`. **Therefore (T) holds for no modulus `F` that is
> strictly positive on such a sequence** — in particular for no `F(ε) = cε` with any `c > 0`
> (answering **Q1**, including `ε/4`), and for no `F(ε) = o(ε)` however slowly it decays
> (answering **Q2**). ∎

*Proof.* Lemmas 4.1, 4.2 and the table. The only inequality used is `F(ε)·n ≥ F(ε)·b ≥ 1 = |S|`. ∎

> **Corollary B1 (it reaches the regime).** `Δ₁ · n = (a+b)/(2a)`, which is `≥ 2` as soon as
> `b ≥ 3a` and is unbounded in `b`. **W\*** therefore lives arbitrarily far **outside**
> `Δ₁·n < 2`, the regime mg-f825 §3.1 proved **W** could never leave. The ticket's RED criterion is
> met. ∎

> **Corollary B2 (the only escape, and it is degenerate).** By §3.2, the sole way for a modulus to
> exclude **W\*** at `ε` is `F(ε)·n < 1` for **every** admissible `n` — which for fixed `ε` forces
> `F(ε) = 0`. Then branch (ii) reads *"`P` is exactly `P[A] ⊕ P[B]`"*, transport holds trivially and
> exactly (Prop. 3.1), and Step 6 does consume (ii) — but only because (ii) has been degenerated
> out of existence. **L4 with `F ≡ 0` in branch (ii) is a strictly stronger conjecture**, and its
> whole burden then falls on `(i) ∨ (iii)`. ∎

**Fully written out at `a = 4, b = 28` — `n = 32`, and `Δ₁·n = 4 > 2`.**
`A = {c_1 < c_2 < x,\; c_1 < c_2 < y,\; x ∥ y}` (4 elements), `B = b_1 < ⋯ < b_{28}`, all `A < B`
except `x ∥ b_1` and `x ∥ b_2`. The four linear extensions are

```
c1 c2 x  y  b1 b2 b3 b4 ... b28
c1 c2 y  x  b1 b2 b3 b4 ... b28
c1 c2 y  b1 x  b2 b3 b4 ... b28
c1 c2 y  b1 b2 x  b3 b4 ... b28
```

`p^P_{xy} = 1/4`; `p^{P[A]}_{xy} = 1/2`; first-4 prefixes `{c1,c2,x,y}, {c1,c2,y,x}, {c1,c2,y,b1},
{c1,c2,y,b1}` give `E K = 2/4 = 1/2`; `min(|A|,|B|) = min(4,28) = 4`, so `Δ₁ = (1/2)/4 = 1/8` and
`Δ₁·n = 4`. **One** modified element. This single poset refutes (T) for every modulus with
`F(1/8) ≥ 1/32`; to refute `F(1/8) = c` for smaller `c`, take `b = ⌈1/c⌉`.

**Consistency with Theorem A**, as a check on both: `|S| = 1 ≥ Δ₁·m = 1/2`. ✔

### 4.1 What **W\*** refutes and what it does not

| statement | status under **W\*** |
|---|---|
| **(T)**, at **every** modulus | **REFUTED** (Thm B) |
| `(ii) ⟹ (iii)` at every modulus with `F(ε) < 1/12` | **REFUTED** — `p^P = 1/4`, and `1/3 − F(ε) > 1/4`. Since `F(ε) → 0` this holds for all small `ε`. Against the *repaired* (iii) predicate (`p^P ∈ [1/3,2/3]`) it fails outright at every `ε` |
| `(ii) + minimality ⟹ balanced pair in P` | **REFUTED** — minimality's only output on (ii) is side pairs, and the side pair does not transport |
| **L4 itself** | **NOT refuted.** Branch **(i)** holds: `p^P_{x,b_1} = 1/2`, so `δ(P) = 1/2` |
| the 1/3–2/3 conjecture | **NOT touched.** `W\*` is not a counterexample and not a minimal counterexample |
| **C3** — *no argument can consume (ii)* | **STILL DECLINED.** `W\*` is a third supporting instance for the *repaired* (IB) of §6.3 |

**The obvious objection, and it does not land.** *"`δ(W\*) = 1/2`, so `W\*` is not a minimal
counterexample and is out of scope."* Step 6 cites near-ordinal-sum stability as a **general lemma**
(`:514`, and L4 at `:464–474` is universally quantified over `P`); a general lemma with a
counterexample cannot be cited. Restricting (T)'s hypothesis to frozen `P` does not rescue it
either: a frozen `P` has no balanced pair anywhere, so "transport into a frozen `P`" is false unless
the class *"minimal counterexample ∧ branch (ii)"* is empty — which renames the problem rather than
solving it. This is mg-f825 §2's rebuttal and mg-63e3 §7 property 5, and both apply here verbatim.

---

## 5. Quantifier audit — of my own family, first (Appendix A step 4d)

This arc has failed at a quantifier three times. The construction above is a quantifier
construction, so it is audited before anything is concluded from it.

### 5.1 What **W\*** holds fixed, and what it varies

| parameter | held / varied | why |
|---|---|---|
| `t = 2` | **fixed** | fixes the displacement `1/2 → 1/4`; nothing is quantified over `t` |
| `a` | **fixed within one instance**; ranges over `a ≥ 3` across instances | fixes `ε = Δ₁ = 1/(2a)`; the conclusion quantifies over `ε`, and each `ε` is served by one `a` |
| `b` | **varied, unboundedly, at fixed `a`** | this is the free parameter |
| `n = a + b` | **varied, at fixed `ε`** | **this is the parameter the conclusion quantifies over** |
| `\|S\| = 1` | **fixed** | independent of `a`, `b`, `n` |

**The parameter I quantify over is `n` at fixed `ε`, and it is exactly the parameter the family
varies.** No relation between `ε` and `n` is locked: for each `ε = 1/(2a)`, **every** `n ≥ a + max(a,3)`
is realised by the family. That is precisely the freedom L4's universal grants (L4 is
`∃F ∀ε ∀(P,A,B)`, with no constraint tying `n` to `ε`) and precisely the freedom **W** lacked.

### 5.2 The mistake this is *not*

mg-63e3's Cor. 4.3 inferred *"transport needs `F(ε)n ≤ 1`, hence `F` must depend on `n`"* from a
family in which `ε = 1/n` **identically** — a constraint read off at one locked `(ε,n)` pair and
generalised over a quantifier the family never ranged across. mg-f825 §3.2 broke it, correctly.

The inference here runs in the **opposite direction** and does not need that step. Fix `ε`; then
`F(ε)` is a **fixed positive number**; then `F(ε)·n ≥ 1` for all `n ≥ 1/F(ε)`; and the universal
ranges over all `n`. Nothing is generalised from a locked pair, because there is no locked pair:
the family supplies unboundedly many `n` at each fixed `ε`.

**Falsifier test (Appendix A step 4b).** What would refute Theorem B? A modulus `F` with `F(ε) > 0`
for some `ε` in the target sequence, admitting no member of `W\*` — i.e. with `F(ε)·n < 1` for all
`n`. That is impossible for `F(ε) > 0`, and Theorem B claims nothing more. It does **not** claim
that no modulus at all exists for L4 (L4 survives via branch (i) in every member of `W\*`), and it
does **not** claim anything about branches (i) or (iii) beyond the row in §4.1.

### 5.3 The `n`-dependence question is settled negatively — and no row flips

STATE `:132` records that *"if L4 needs an `n`-dependent modulus the answer flips"* for mg-88bd, and
mg-63e3's `n`-dependence clause was deliberately **not** landed (commit `bc75274`). Theorem B bears
on this, and in the **conservative** direction:

> Allowing the budget to depend on `n` as well as `ε` — a function `F(ε,n)` — does **not** exclude
> `W\*`. Exclusion requires `F(ε,n)·n < 1` for all `n`, i.e. a budget below **one element**, i.e.
> branch (ii) degenerated to exact ordinal sum (Cor. B2).

So branch-(ii) transport is not the kind of thing an `n`-dependent modulus repairs; the
`n`-dependence question is **moot for this branch**. **This supplies no reason to flip the mg-88bd
row, and none should be recorded.** The clause STATE declined to land should stay declined — not
because it is unproven, but because the corrected analysis shows it was aimed at the wrong object.

### 5.4 Rider — under the literal reading (E1) even the original **W** suffices

Not load-bearing; recorded because it is a second correction to the audit's threshold and because
declining to state it would be the same omission mg-f825 F4 charged mg-63e3 with.

Under **(E1)**, `ε` is any bound `≥ Δ₁`, so the budget is `F(ε)n` with `ε` chosen **freely**. Fix
`ε` and put `c := F(ε) > 0`. Take the balanced family `W(a)` at `t = 2`, where `Δ₁ = 1/n` with
`n = 2a`, and choose `n` to be the least even integer `≥ 1/c`. Then `Δ₁ = 1/n ≤ c ≤ ε` (using
`F(ε) ≤ ε`, which any useful modulus satisfies for small `ε`), so the hypothesis `Δ₁ ≤ ε` holds;
and the budget is `F(ε)·n = c·n ≥ 1 = |S|`, so branch (ii) holds. Transport fails as in **W**.

So under (E1), **W** already refutes every strictly positive modulus, and mg-f825 §3.1's threshold
survives only under (E2). **This is a rider, not the result**, for a deliberate reason: (E2) is the
source's own prose (`:461–463`) and the charitable reading, and a refutation that needs the loose
reading is worth much less than one that does not. **Theorem B needs neither.**

---

## 6. What a sub-linear modulus *does* buy — and why it is not a repair

### 6.1 The vacuity mechanism, stated precisely

By Corollary A2, under (E2) a cut of balance `β` enters branch (ii) only if `F(ε) ≥ βε`. So:

> **Corollary A3.** Fix `β₀ > 0`. If `F(ε) < β₀ε` — in particular for **every** `F(ε) = o(ε)`, at
> all small `ε` — then **no cut with `min(|A|,|B|) ≥ β₀n` enters branch (ii) at all**, under
> reading (E2).

Branch (ii) is then **empty on balanced cuts**, and Step 6 consumes it vacuously. This is a real
mechanism and it is the honest core of the ticket's "does sub-linear rescue it" intuition. It is
**not** what Theorem B refutes: Theorem B's witness escapes precisely by having `β = a/(a+b) → 0`.

### 6.2 Three reasons it is not a repair

1. **It needs a hypothesis L4 does not state.** Corollary A3 requires a lower bound on `β`. L4
   (`:464–474`) has none, and `Δ₁`'s own `min(|A|,|B|)` normalisation (`:273`) shows the source
   *anticipated* unbalanced cuts. Equivalently one may re-normalise the budget to
   `F(ε)·min(|A|,|B|)`, which by Theorem A forces `F(ε) ≥ Δ₁` for branch (ii) to be non-empty and
   hence empties it for every sub-linear `F` under (E2). **Either move changes L4; neither is a
   reading of it.**
2. **The chain does not deliver the hypothesis.** Step 3 asks for *"a low-conductance prefix"*,
   Step 4 for `A_k = {1,…,k}` with `Φ_P(A_k) ≲ √ε`, Step 5 for `E K_k ≪ min(k, n−k)`. **No step
   constrains `k`**, and `Φ_P^\ast = min_{0<|A|≤n/2} Φ_P(A)` (`:235–237`) is *defined* by
   minimisation over all cut sizes — conductance is the standard normalisation that makes small
   cuts admissible. L3 (*prefix Cheeger lemma*, `:565`) says nothing about balance either.
   Per the ticket's own criterion — *a repair needing a stronger input than Steps 4/5 produce is
   not a repair* — this repair needs an input the chain does not produce. Whether L3 can be
   strengthened to deliver a balanced prefix is a **new open item** (named **F-bal** in §8).
3. **It relocates the burden onto an already-refuted disjunct.** With (ii) emptied, L4 reduces to
   `(i) ∨ (iii)`. For a minimal counterexample (i) is unavailable by definition, so everything rests
   on (iii) — and **(iii) as a standalone universal is refuted at every `ε > 0`, for every modulus,
   modulus-free** (mg-f825 §6, confirmed here: `W\*` reproduces that refutation at unbounded `n`).
   Emptying (ii) does not make (iii) true.

### 6.3 What survives of (IB)

mg-f825 §5 refuted (IB)'s **interface** clause (an exact ordinal sum with a non-chain side has no
incomparable interface pair at all) and confirmed that the half doing the architectural work —
*"`P` has a `1/3`-balanced pair"* — survives. **W\*** is consistent with the repaired (IB): it is
not a chain, it is one modification from an ordinal sum, and it has a balanced pair
(`p^P_{x,b_1} = 1/2`, which here happens to be an interface pair). So `W\*` is a **third supporting
instance** for the repaired (IB), and mg-63e3's §7 property 5 — that a minimal counterexample is
exactly where the migration mechanism is excluded — is untouched by anything here and remains the
live question.

---

## 7. Modulus check against the chain (the ticket's closing requirement)

The ticket asks, if the route closes, to state the modulus and check that Steps 4/5 deliver it, and
to cross-check against mg-88bd's `ε_spec` and the audit's warning that the budget is unpinned by
roughly two orders of magnitude.

**The route does not close, and the check is vacuous — but for a different and more precise reason
than mg-63e3 gave.** mg-63e3 said the check was vacuous because *"there is no `ε` at which (T)
holds"*, resting on the false premise that `1/n` is the smallest nonzero prefix leakage (mg-f825 §4
refuted this: the floor is `Θ(1/n²)`). That premise is not used here and is not needed. The correct
statement:

- **The failure is not a budget failure in `ε`.** It is a normalisation mismatch between `F(ε)·n`
  and `Δ₁ = EK/min(|A|,|B|)`, made lethal by the fact that the minimal certificate is **one
  element** (§3.2). Shrinking `ε` shrinks `F(ε)` but never below the point where `F(ε)n < 1` for
  *all* `n`.
- **`ε_spec` is untouched.** mg-88bd's pinning prices Step 2's input, which sits upstream of the
  branch-(ii) failure. Its STATE row stands exactly as recorded. The two-orders-of-magnitude
  looseness that mg-e35c F5 flagged is a looseness in `ε`, and no value of `ε` changes Theorem B's
  conclusion.
- **No `n`-dependence flip.** §5.3.
- **The one quantity a repair would have to price is `β`, not `ε`** — and nothing in Steps 2–5 or
  L1–L3 prices it. That is the new demand this document puts on the chain.

---

## 8. Open items this produces

- **F-bal (new).** Can L3 (*prefix Cheeger lemma*, `:565`) be strengthened to deliver a prefix cut
  with `min(k, n−k) ≥ β₀ n` for an absolute `β₀ > 0`, at quantitatively controlled loss in `Φ`? If
  yes, Corollary A3 makes a sub-linear modulus empty branch (ii) under (E2), and the architecture's
  branch-(ii) problem is replaced by an (already-hard, already-refuted-as-standalone) branch-(iii)
  problem. If no, branch (ii) is dead at every modulus and Step 6 must be restructured. **This is
  the single question on which the value of a sub-linear modulus now turns.**
- **The (E1)/(E2) reading of `ε`.** `:461–463` (equality) and `:466` (inequality) disagree. Under
  (E1) the branch-(ii) budget is meaninglessly generous and even balanced `W` kills it (§5.4).
  Recommend the source fix the wording to the tight reading. This is a drafting repair, not an
  architectural one, but it is load-bearing for every threshold statement in this arc.
- **Re-normalising branch (ii)'s budget** to `F(ε)·min(|A|,|B|)` is the minimal edit that makes
  Corollary A2 bind without an extra hypothesis. Whether L4 is still *true* with that budget is
  open — narrowing (ii) strengthens the conjecture.

---

## 9. Proposed STATE.md text — a **proposal to pm-onethird**, not an edit

Expected to be audited as a primary target in its own right (Appendix A step 4c). Written to claim
only what §§3–5 prove, and to leave the declined claims declined.

**Row 11 — replacement for the clause *"and branch (ii) is unconsumed by Step 6's stated transfer
for every modulus `F(ε) = Ω(ε)`" — a *conditional* statement, and the condition is load-bearing"*:**

> …and **branch (ii) is unconsumed by Step 6's stated transfer for *every* modulus — PROVEN, and the
> `Ω(ε)` condition is now discharged** (mg-3af9). The obstruction is **not** a budget shortfall in
> `ε` but a **normalisation mismatch inside L4's own statement**: branch (ii)'s budget is `F(ε)·n`
> while `Δ₁` is normalised by `min(|A|,|B|)` (`:273`), and the ratio `n/min(|A|,|B|)` is unbounded.
> Two ingredients: **(a) Budget–Leakage inequality** — any branch-(ii) certificate satisfies
> `|S| ≥ Δ₁·min(|A|,|B|)` (elementary; every `A`-element left after position `|A|` is incomparable
> to every `B`-element that entered, so `S` must cover a `K×K` grid of cross-incomparabilities).
> This **promotes mg-f825 §3.1's `ε/2` from a fact about family `W` to a theorem about every
> balanced cut**: under the source's own tight reading `ε = Δ₁` (`:461–463`), **no** balanced-cut
> witness can refute `F(ε) < ε/2`, so the audit's obstruction was universal, and the only remaining
> freedom is the cut's **balance** `β = min(|A|,|B|)/n`. **(b) Witness `W\*`** — family `W` with its
> `B`-chain lengthened and decoupled from `a`: `A = C_{a−2} ⊕ AC_2` (`a` elements), `B = C_b`
> (`b ≥ a` elements), `x < b_1` and `x < b_2` deleted. Then `E K = 1/2` and `Δ₁ = 1/(2a)`
> **independently of `b`**, so `n = a+b` is free at fixed `ε` and **`Δ₁·n = (a+b)/(2a)` is
> unbounded** — `W\*` lives arbitrarily far **outside `Δ₁·n < 2`**, the regime `W` provably could not
> leave. **One** modified interface element (`S = {x}`; the minimum possible, since `|S| = 0` means
> exact ordinal sum and transport then holds exactly), the sides' **only** incomparable pair balanced
> at exactly `1/2` in `P[A]` and at **`1/4`** in `P`. Since `F(ε)·n ≥ 1` for every `n ≥ 1/F(ε)`,
> **every strictly positive modulus admits `W\*`** — `F(ε) = ε/4` (linear, small constant) and every
> `F(ε) = o(ε)` alike. Concrete instance: `a = 4, b = 28`, `n = 32`, `Δ₁ = 1/8`, `Δ₁·n = 4`, four
> linear extensions. **Escape, and it is degenerate:** only `F(ε) = 0` excludes it, which reads
> branch (ii) as *"`P` is exactly `P[A] ⊕ P[B]`"* — transport then holds trivially, but L4 is
> thereby a strictly stronger conjecture with the burden on `(i) ∨ (iii)`.
> **`(ii) ⟹ (iii)` is REFUTED at every modulus**, so the "drop (ii), keep (i)∨(iii)" repair remains
> unavailable. **`W\*` refutes implications, not theorems: L4 itself survives via branch (i)**
> (`p^P_{x,b_1} = 1/2`), and the 1/3–2/3 conjecture is untouched.
> **What a sub-linear modulus *does* buy, and it is not a repair:** by (a), if the cut is balanced
> (`β ≥ β₀`) **or** the budget is re-normalised to `F(ε)·min(|A|,|B|)`, then any `F(ε) = o(ε)`
> **empties branch (ii) outright** under the tight reading — Step 6 consumes it vacuously. But that
> is a **change to L4, not a reading of it**; **Steps 2–5 do not deliver it** (no step constrains
> `k`, and `Φ_P^\ast` is *defined* by minimisation over all cut sizes at `:235–237`, so conductance
> permits unbalanced cuts); and it relocates the burden onto **(iii)**, which is **already refuted as
> a standalone universal at every `ε`, modulus-free** (mg-f825). New open item **F-bal**: *can L3 be
> strengthened to deliver a prefix cut with `min(k,n−k) ≥ β₀n` at controlled loss in `Φ`?* — the
> single question on which the value of a sub-linear modulus now turns.
> **Deliberately NOT claimed:** **C3** (*no argument can consume (ii)*) remains **DECLINED** — the
> repaired **(IB)** is still live and `W\*` is a third supporting instance for it. **No
> `n`-dependence clause is landed and none is warranted:** an `n`-dependent budget `F(ε,n)` does
> **not** exclude `W\*` either (exclusion still requires a budget below one element), so the
> `n`-dependence question is **moot for this branch** and **the mg-88bd row at `:132` does not
> flip**. `ε_spec` is untouched — it prices Step 2's input, upstream of the failure, and no value of
> `ε` changes the conclusion. The quantity a repair would have to price is **`β`, not `ε`**, and
> nothing in Steps 2–5 or L1–L3 prices it.

**Also proposed — the mg-63e3 row.** Its `Cor. 4.3` / ledger claim 13 (*"there is no modulus"*)
should be recorded as **conclusion re-established, proof still invalid**: the conclusion now holds at
full strength via mg-3af9, but by a different family and a different quantifier route; mg-f825's
break of the original argument stands, as does its refutation of the `Θ(1/n)`-leakage-floor premise
(mg-3af9 does not use that premise).

**Also proposed — a drafting flag on the source.** `:461–463` states `Δ₁ = ε` (equality) while
`:466` states `Δ₁ ≤ ε` (inequality). Every threshold statement in this arc depends on which is
operative. Under the loose reading even the *original* balanced `W` refutes every strictly positive
modulus (mg-3af9 §5.4). Recommend the source be tightened to the equality reading; mg-3af9's
headline holds under **both**, so nothing above depends on the resolution.

---

## 10. Claim ledger

Every claim, **including reductions asserted in prose**.

| # | Claim | § | Label | Basis / condition |
|---|---|---|---|---|
| 1 | `Δ₁ = E\|A∖σ(A)\|/min(\|A\|,\|B\|)`; branch (ii)'s budget is `F(ε)·n` — different normalisations | 2 | **PROVEN** (textual) | `:271–275` and `:469–470`, both pulled and read directly |
| 2 | For a prefix cut there is no `b <_P a` with `a∈A, b∈B` | 2.1 | **PROVEN** | Source `:254–256`, verbatim |
| 3 | Every pair in `X_σ × Y_σ` is an incomparable cross pair | 3 (∗) | **PROVEN** | Positions `≤\|A\|` vs `>\|A\|`, plus claim 2 |
| 4 | **Budget–Leakage: `\|S\| ≥ max_σ K(σ) ≥ Δ₁·min(\|A\|,\|B\|)`** | 3 | **PROVEN** | Covering argument on (∗); holds under both readings of (ii), since the proof never names the summands |
| 5 | Under relation-counting the bound is `\|S\| ≥ (max_σ K)²` | 3.1 | **PROVEN** | All `K²` pairs must be repaired |
| 6 | Branch (ii) requires `β·Δ₁ ≤ F(ε)`, `β := min(\|A\|,\|B\|)/n` | A1 | **PROVEN** | Claim 4 |
| 7 | Under reading (E2), a balanced cut requires `F(ε) ≥ ε/2` | A2 | **PROVEN** *given (E2)* | Claim 6 at `β = 1/2`. **CONDITIONAL on the reading**, which is stated |
| 8 | **No balanced-cut witness can refute `F(ε) < ε/2` under (E2)** — mg-f825 §3.1's threshold is structural, not a property of `W` | 3.1 | **PROVEN** *given (E2)* | Claim 7 is a statement about all cuts, not one family |
| 9 | `\|S\| = 0` ⟹ transport holds exactly, every side pair preserved | 3.2 | **PROVEN** | mg-63e3 Prop. 3.1, re-verified (LEs of an ordinal sum are the concatenations) |
| 10 | The minimal non-trivial certificate is `\|S\| = 1` | 3.2 | **PROVEN** | Claim 9 |
| 11 | `W\*` is a poset; `A` is a down-set, hence a prefix cut; restoring 2 crosses gives `P[A] ⊕ P[B]` | 4.1 | **PROVEN** | Transitivity checked; linear extension exhibited |
| 12 | `LE(W\*)` = 4, given by `x`'s insertion slot | 4.2 | **PROVEN** | All `n−1` other elements totally ordered; gap contains `y,b_1,b_2` |
| 13 | `p^P_{xy}=1/4`; `p^{P[A]}_{xy}=1/2`; `EK=1/2`; `Δ₁=1/(2a)`; `p^P_{x,b_1}=1/2`; `p^P_{x,b_2}=3/4` | 4 | **PROVEN** | Hand count from the Lemma 4.2 table; `a=4,b=28` instance written out in full |
| 14 | `E K = 1/2` and `Δ₁ = 1/(2a)` are **independent of `b`** (given `b ≥ max(a,3)`) | 4 | **PROVEN** | Only `x` can leak, and only in slots 2,3; `min(a,b)=a` |
| 15 | `{x,y}` is the **only** incomparable pair of `P[A] ∪ P[B]` | 4 | **PROVEN** | Every `c_j` is comparable to all of `A`; `P[B]` is a chain |
| 16 | `S = {x}`, `\|S\| = 1`, and `x` is an interface element; also `\|S\|=1` under the removal reading | 4 | **PROVEN** | The only differing cross pairs are `(x,b_1),(x,b_2)`; deleting `x` leaves `chain ⊕ chain` |
| 17 | **Theorem B: (T) is false at every `ε ∈ {1/(2a)}` for every `F` with `F(ε)>0`** | 4 | **PROVEN** | Claims 11–16; the only inequality used is `F(ε)n ≥ F(ε)b ≥ 1` |
| 18 | Hence no `F(ε)=cε` (`c>0`, incl. `ε/4`) and no `F(ε)=o(ε)` rescues transport | 4 | **PROVEN** | Claim 17; both classes are strictly positive |
| 19 | **`Δ₁·n = (a+b)/(2a)` is unbounded — `W\*` is outside `Δ₁·n < 2`** | B1 | **PROVEN** | Claim 14; `≥2` once `b ≥ 3a` |
| 20 | The only excluding modulus is `F(ε)=0`, degenerating (ii) to exact ordinal sum | B2 | **PROVEN** | Claims 10, 17 |
| 21 | `(ii) ⟹ (iii)` refuted at every modulus with `F(ε)<1/12`; at every `ε` for the repaired predicate | 4.1 | **PROVEN** | `p^P = 1/4`; `F(ε)→0` |
| 22 | `W\*` does **not** refute L4 and does not touch the 1/3–2/3 conjecture | 4.1 | **PROVEN** | Branch (i) holds: `p^P_{x,b_1}=1/2`, `δ(W\*)=1/2` |
| 23 | The "`δ(W\*)=1/2`, so out of scope" objection fails | 4.1 | **PROVEN** (logic) | Step 6 cites a general lemma; restricting to frozen `P` makes transport false unless the class is empty |
| 24 | `W\*` holds `ε` fixed and varies `n` — the parameter quantified over is the one varied | 5.1 | **PROVEN** (self-audit) | Table in §5.1; `Δ₁` depends on `a` only (claim 14) |
| 25 | The inference of claim 17 is not mg-63e3's Cor. 4.3 defect | 5.2 | **PROVEN** (logic) | `ε` fixed first, `F(ε)` then a fixed number, `n` free; no generalisation from a locked pair |
| 26 | **An `n`-dependent budget `F(ε,n)` does not exclude `W\*` either** | 5.3 | **PROVEN** | Exclusion needs `F(ε,n)·n<1` for all `n`, i.e. below one element |
| 27 | **No flip of the mg-88bd row at `:132` is warranted by this work** | 5.3 | **PROVEN** (logic) | Claim 26 supplies no `n`-dependence requirement; `ε_spec` is upstream (claim 33) |
| 28 | Under reading (E1), the original balanced `W` already refutes every strictly positive modulus | 5.4 | **PROVEN** *given (E1)* | Choose `n = ⌈1/F(ε)⌉`; `Δ₁ = 1/n ≤ F(ε) ≤ ε`. **CONDITIONAL on (E1)**, and on `F(ε) ≤ ε` for small `ε` |
| 29 | The source is internally inconsistent on `ε` (`:461–463` equality vs `:466` inequality) | 1.1, 8 | **PROVEN** (textual) | Both lines pulled and read |
| 30 | If `β ≥ β₀` or the budget is `F(ε)·min(\|A\|,\|B\|)`, any `F(ε)=o(ε)` **empties** branch (ii) | A3, 6.1 | **PROVEN** *given (E2)* | Claim 6. **CONDITIONAL on the reading and on the added hypothesis / re-normalisation** |
| 31 | Steps 2–5 and L1–L3 do **not** deliver a balance hypothesis | 6.2 | **PROVEN** (textual) | No step constrains `k`; `Φ_P^\ast = min_{0<\|A\|≤n/2}Φ_P(A)` at `:235–237` minimises over all cut sizes |
| 32 | Whether L3 can be strengthened to deliver `min(k,n−k) ≥ β₀n` (**F-bal**) | 8 | **OPEN — stated, not claimed** | New open item; nothing here bears on its answer |
| 33 | `ε_spec` / mg-88bd is untouched | 7 | **PROVEN** (logic) | It prices Step 2's input, upstream of the failure; no `ε` changes claim 17 |
| 34 | mg-63e3's `Θ(1/n)`-leakage-floor premise is **not used** anywhere here | 7 | **PROVEN** (by inspection) | mg-f825 §4 refuted it (`Θ(1/n²)`); Theorem B needs only `F(ε)n ≥ 1` |
| 35 | `W\*` is consistent with the **repaired** (IB) and is a third supporting instance | 6.3 | **PROVEN** | Not a chain, one modification from an ordinal sum, `p^P_{x,b_1}=1/2` |
| 36 | **C3** — *branch (ii) is unconsumable by any argument* | 4.1, 6.3 | **NOT ESTABLISHED — explicitly declined** | Theorem B refutes the *stated transfer*, not every possible argument |
| 37 | mg-63e3's *conclusion* (no modulus) is re-established; its *proof* remains invalid | 0, 9 | **PROVEN** | Claim 17 is a different family and a different quantifier route; mg-f825 §3.2's break stands |

**Reductions asserted in prose, separately labelled** (the failure mode this arc exists to avoid):

| # | Prose reduction | Label |
|---|---|---|
| R-a | *"the audit's `ε/2` threshold is structural, not a property of `W`"* | **PROVEN given (E2)** — claim 8. It is a statement about all balanced cuts, derived from claim 4 |
| R-b | *"Theorem A identifies cut balance as the unique remaining degree of freedom, and `W\*` spends it"* | **PROVEN** — claims 6 + 19. `β` is the only free quantity in `β·Δ₁ ≤ F(ε)` once `Δ₁ ≤ ε` and `F` are fixed |
| R-c | *"a sub-linear modulus rescues Step 6 by **emptying** branch (ii), not by making transport work"* | **CONDITIONAL** — claim 30, on reading (E2) **and** on an added balance hypothesis or a re-normalised budget. **Not asserted as available** |
| R-d | *"the vacuity rescue is not a repair, because the chain does not deliver its hypothesis"* | **PROVEN as a statement about the text** (claim 31: Steps 2–5 / L1–L3 contain no balance clause). **HEURISTIC as a claim about what a completed Step 4 could deliver** — F-bal (claim 32) is open |
| R-e | *"the vacuity rescue relocates the burden onto (iii), which is already refuted as a standalone universal"* | **PROVEN** — the reduction is claim 30 plus mg-f825 §6 (independently reproduced by `W\*` at unbounded `n`) |
| R-f | *"the `n`-dependence question is moot for branch (ii), so no row flips"* | **PROVEN** — claims 26, 27 |
| R-g | *"branch (ii)'s problem is a normalisation mismatch, not a budget shortfall in `ε`"* | **PROVEN** — claims 1, 6, 17: the failure persists at every `ε` and is removed by re-normalisation (claim 30), which localises it to the normalisation |
| R-h | *"Theorem B is reading-independent"* | **PROVEN** — claim 17 verifies `Δ₁ = ε` with **equality**, so the witness satisfies (E2), and (E1) is weaker |

---

## 11. Answers to the ticket's three questions

1. **Does the transport argument close under `F(ε) ≤ ε/2`?** **No.** It closes for no strictly
   positive modulus at all (Thm B). What is true — and it is the audit's insight, now generalised —
   is that no *balanced-cut* witness can refute `F(ε) < ε/2` (Cor. A2). The refutation requires
   unbalancing the cut, which L4 permits and `Δ₁`'s own normalisation anticipates.
2. **A witness outside `Δ₁·n < 2`.** **W\*** (§4), at `Δ₁·n = (a+b)/(2a)`, unbounded; concretely
   `a=4, b=28`, `n=32`, `Δ₁·n = 4`. It is genuinely in branch (ii)'s hypothesis class:
   `Δ₁ = 1/8 = ε` exactly (so both readings of `ε` are satisfied), `A` is a genuine prefix cut of a
   linear extension, and **one** interface element — `x` — carries the whole certificate.
3. **If it closes, state the modulus and check the chain delivers it.** It does not close. The
   nearest thing to a closure is the **vacuity** route of §6, and the chain does **not** deliver its
   hypothesis: nothing in Steps 2–5 or L1–L3 constrains the cut's balance, and `Φ_P^\ast` is defined
   by minimisation over all cut sizes (`:235–237`). The demand a repair would have to price is
   **`β`, not `ε`** — so mg-88bd's `ε_spec` and the two-orders-of-magnitude looseness are untouched,
   and no row flips.
