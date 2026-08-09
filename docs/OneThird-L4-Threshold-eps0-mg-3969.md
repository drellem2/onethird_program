# L4's THRESHOLD `ε₀` — is it `n`-free, and what is its value?

**Work item:** `mg-3969` (clause (a) of `mg-845e`'s gate) · **Independent audit pre-filed:** `mg-d3c7`
**Method:** source reading + hand derivation + one exhaustive exact-rational instrument
(`code/eps0_threshold_3969/`, all `Fraction`, no float on any decision path).
**Source, read at source and not through any restatement:**
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
(603 lines; L4 at `:464–474`, Steps 1–6 at `:488–516`, `Δ₁` at `:270–278`, `Φ` at `:229–237`,
`δ` at `:63–66`, L1–L4 at `:556–570`).

---

## 0. Verdict

> **1. Is `ε₀` `n`-free?**
> **THE SOURCE DELIVERS NEITHER AN `n`-FREE `ε₀` NOR AN `ε₀(n)`. IT DELIVERS NO `ε₀` AT ALL.**
> L4 as it actually appears carries **no threshold, no domain restriction and no smallness
> hypothesis**. The strings `\varepsilon_0`, `eps_0`, `epsilon_0` occur **0 times in the whole
> document**; the word "threshold" occurs 3 times and **none of the three is a threshold on `ε`**
> (two are eigenvector *threshold sets*, `:326`, `:361`); the phrase "sufficiently small `ε`"
> occurs **exactly once**, at `:497`, and that `ε` is the **spectral** one in Step 2, **not L4's
> leakage `ε`**. Question 1's dichotomy is a false dichotomy *at source*: both horns presuppose
> that the source hands over an `ε₀`, and it does not.
>
> **The form is `n`-free; the existence of a positive value is open and is the conjecture itself.**
> The only smallness demand on L4's `ε` anywhere in the source is the informal **`Δ₁(A_k,A_k^c)=ε≪1`
> at `:459`** — a comparison against the absolute constant `1`, with **no `n` in it**. `n` occurs
> **exactly once** in all eleven lines of L4 (`:464–474`), in `F(ε)n` at `:469`, and **nowhere in
> its hypothesis**. So the statement has **no site at which an `n` could enter a threshold**. That
> settles the *form* and it settles nothing else.
>
> **2. What is its value?** **The source pins no value, and §4 shows the value has no `F`-free
> derivation route.** Two numbers can nevertheless be given, and they are *upper* bounds, derived
> and witnessed rather than asserted — but they bound a **different and strictly stronger**
> statement than the one Step 6 consumes (§5–§6):
>
> | statement | bound | witness | status |
> |---|---|---|---|
> | `U_either` — the `F`-free repaired transfer, **either** side, asserted for **all** posets | **`ε₀ ≤ 17/78 = 0.21795`**, uniformly in `n` | `n = 6`, exhibited, re-derived by a second code path | **PROVEN** |
> | `U_smaller` — same, **smaller** side only | **`ε₀ ≤ 1/7 = 0.14286`**, uniformly in `n` | `n = 6`, exhibited | **PROVEN** |
> | `S` — what **Step 6** actually consumes | **`ε₀ = 1` on every poset that can be exhibited** | 604,230 prefix cuts, `n ≤ 7`, exhaustive | **PROVEN, AND VACUOUS** |
>
> **The corpus's operative `ε₀ ≈ 0.20` now has a proven ceiling `17/78 = 0.2179` immediately above
> it:** the ceiling exceeds the calibration by a factor `(17/78)/0.20 = 1.0897`, so **`ε₀` cannot be
> raised by more than 9 %**, ever, at any `n`.
>
> **3. THE DISJUNCT FIRES, AND IT FIRES SPLIT.** `ε_dem`'s **form** is reachable without `ε₀`;
> `ε_dem`'s **value** is not, and cannot be. With `C₃ = 1` (`mg-76b2`, conditional on L2) the demand
> chain collapses to **`ε_dem = ε₀²/2` — one equation, one unknown, and the unknown is this
> ticket's**. Every digit of the corpus's budget is `ε₀²/2`: `0.02²/2 = 2×10⁻⁴`,
> `0.20²/2 = 2×10⁻²`, and **the "100× too pessimistic" of the `mg-e35c` F5 banner is exactly the
> square of a 10× move in `ε₀`**. So "the constant that is consumed" is **not unpinned by two
> orders of magnitude for two reasons — it is unpinned for exactly one, and that one is `ε₀`.**
>
> **AND THE ONE THAT MATTERS FOR `mg-845e`:** the threshold Step 6 consumes is **not measurable and
> not boundable**, because on the class where it is consumed — minimal counterexamples — disjunct
> (i) is **false by hypothesis**, and on every poset that is not a counterexample disjunct (i) is
> **true at `ε = 1`**. Proving any positive value for it **is** the 1/3–2/3 conjecture on the
> thin-interface class (§5.3). `mg-845e` should therefore be released against the *uniform*
> threshold `ε₀(U_either) ∈ (0, 17/78]`, which is the only one a proof can ever produce.

---

## 1. The source, quoted in full, and the four things it does not say

L4, verbatim, `:464–474` — the whole of it, no elision:

```tex
\begin{conjecture}[Near-ordinal-sum stability]
There exists \(F(\varepsilon)\to0\) such that if
\(\Delta_1(A,B)\le\varepsilon\), then one of the following holds:
\begin{enumerate}[label=(\roman*)]
\item \(P\) contains a \(1/3\)-balanced pair;
\item after removing or modifying at most \(F(\varepsilon)n\) interface
elements, \(P\) becomes \(P[A]\oplus P[B]\);
\item a balanced pair in \(P[A]\) or \(P[B]\) remains balanced up to
error \(F(\varepsilon)\) in \(P\).
\end{enumerate}
\end{conjecture}
```

and its two-sentence setup, `:457–462`:

```tex
Suppose a minimal counterexample has a prefix \(A_k\) with
\[
\Delta_1(A_k,A_k^c)=\varepsilon\ll1.
\]
```

and L4's one-sentence summary in the *Main open lemmas* list, `:567–569`:

```tex
\item \textbf{Near-ordinal-sum stability lemma.} Sufficiently small
prefix leakage contradicts minimality by preserving a balanced pair
from one side.
```

**What is not there, checked byte-wise over the whole 603-line file:**

| looked for | occurrences | where |
|---|---|---|
| `\varepsilon_0` / `eps_0` / `epsilon_0` | **0** | — |
| `threshold` | 3 | `:326`, `:361` — *threshold sets of an eigenvector*, a different sense; `:548` — "falsification tests" prose |
| `sufficiently small` | **1** | `:497`, **Step 2**, on `λ_std ≥ 1−ε` — the **spectral** `ε` |
| `absolute constant` | 0 | — |
| any smallness demand on L4's leakage `ε` | **1** | `:459`, the informal **`ε ≪ 1`**, *outside* the conjecture environment |

Four consequences, each of which is a reading of the quoted text and nothing else:

1. **L4's implication is asserted at every `ε`.** `\begin{conjecture}` … "if `Δ₁(A,B) ≤ ε`, then …"
   has no antecedent restricting `ε`. The only condition attached to `ε` anywhere in the statement
   is `F(ε) → 0`, and that is a condition **on `F`**, not a restriction on `F`'s domain.
2. **`ε` is bounded by `1` for free.** `|A \ σ(A)| = |σ(A) \ A| ≤ |[n] \ A| = |B|` and
   `|A \ σ(A)| ≤ |A|`, so `E|A\σ(A)| ≤ min(|A|,|B|)` and hence **`Δ₁ ≤ 1` always**, attained iff
   `A ∩ σ(A) = ∅` almost surely. *(Instrument NC3 confirms the bound and reports it approached:
   `max Δ₁ = (n−1)/n` at the antichain, `2/3, 3/4, 4/5, 5/6, 6/7` at `n = 3..7`.)* **[PROVEN]**
   So *"L4 as literally stated has threshold `ε₀ = 1`, `n`-free"* is a true sentence, and a useless
   one: at `ε` near `1` the conclusion is satisfied by an `F` near `1`, which no consumer can use.
3. **`n` occurs once in L4 and never in its hypothesis.** The hypothesis `Δ₁(A,B) ≤ ε` is a
   comparison of a **per-element density** — that is precisely what `Δ₁`'s `min(|A|,|B|)`
   denominator is for (`:270–278`) — against a bare number. There is no `n`-indexed quantity for a
   threshold to attach itself to. *(This is an `F`-free support and it is not the one `Op-Form`
   §3.2 leans on; see §3.)*
4. **`:497`'s "sufficiently small `ε`" is a different `ε`.** The source uses the symbol for two
   quantities (`Op-Form` §1, re-verified here at source): **spectral** at `:494–497` and `:502–507`,
   **leakage** at `:459` and `:466`. `:497` is the spectral one. Anyone who reads the source's one
   "sufficiently small" as L4's threshold has crossed the symbol collision.

---

## 2. There are THREE objects called `ε₀` in this corpus, and they are not the same number

This is the third instance on this lineage of one word carrying two objects — after
`ε_spec = {ε_sup, ε_dem}` (`mg-345e`) and modulus-vs-threshold (`mg-6bc2`, `pm-onethird`
2026-08-07). Naming them is most of the work.

| name | definition | who uses it | is it measurable? |
|---|---|---|---|
| **`ε₀^lit`** | the domain of validity of L4 exactly as stated | nobody | `= 1`, `n`-free, information-free (§1.2) |
| **`ε₀^cons`** | `sup{ε : Δ₁ ≤ ε ⟹ (i) or (iii-exact)}` — the statement Step 6 consumes (`mg-345e` §5.1) | `mg-845e`'s demand chain | **NO — §5** |
| **`ε₀^unif`** | the same implication asserted for **all** posets, not only counterexamples | `mg-3ce3`'s probe; `Op-Form` §4.1's `Δ₁ ≤ ε₀·min(k,n−k)` | **YES — §6** |

`ε₀^unif ≤ ε₀^cons` always (a statement true of all posets is true of counterexamples), so every
lower bound on `ε₀^unif` is a lower bound on the consumable one — which is why the programme is
entitled to work with `ε₀^unif`. The corpus's `0.20` is a lower bound on `ε₀^unif`, obtained
empirically. **Nothing in the corpus distinguishes these two, and `ε₀^cons` is the one `mg-845e`
names.**

---

## 3. Question 1, answered on each of the three objects

**`ε₀^lit`: `n`-free, `= 1`, useless.** §1, consequences 1–2.

**`ε₀^cons`: `n`-free *in form*; positivity OPEN and equivalent to the conjecture.** §5.

**`ε₀^unif`: `n`-free *in form*, and bounded above by `17/78` uniformly in `n`.** §6.

**On the `n`-freeness argument the corpus already has, and the one it was missing.** `Op-Form`
§3.2 gives two supports. Support 1 ("`n` appears once, multiplied by `F`") is an argument *about
the modulus*, and `mg-345e` §5.1 correctly warns that leaning on it here would be **circular** —
discarding `F` while standing on an argument made of `F`. Support 2 (the downstream is
dimensionless: the predicate contradicted is `δ(P) < 1/3`, and `[1/3,2/3]` has width `1/3` at every
`n`) is `F`-free and survives. **This document adds a third, which is `F`-free *and*
consumer-free**, so the `n`-freeness of the form no longer rests on any claim about Step 6:

> **Claim 3.1 (the hypothesis is `n`-free).** *L4's hypothesis is `Δ₁(A,B) ≤ ε`, and `Δ₁` is a
> per-element density by construction (`:270–278`): its numerator `E|A\σ(A)|` and its denominator
> `min(|A|,|B|)` are both extensive, so `Δ₁` is dimensionless and takes values in `[0,1]` at every
> `n` (§1.2). A threshold is a restriction on the hypothesis; this hypothesis offers nothing for an
> `n` to attach to.* **[PROVEN — reading of the definition, plus the `Δ₁ ≤ 1` bound]**

**What Claim 3.1 does NOT say, because this is where the whole question actually lives.** That the
*form* admits no `n` does not make the *number* `n`-free. Write `ε₀(n) = sup{ε : the implication
holds for every poset on n elements}`. Each `ε₀(n)` is well defined and `n`-free-ness of the form
says nothing whatever about whether

```
    ε₀ := inf_n ε₀(n)
```

is positive. **`ε₀ > 0` is the entire content of the question and no argument in this corpus
touches it.** The corpus reads "the form has no place for an `n`" as "the threshold is `n`-free",
and those are different statements: the second is the first **plus** `inf_n ε₀(n) > 0`. This
document supplies the ceiling on that `inf` (§6) and proves the `inf` unmeasurable for the
consumed object (§5). It does **not** prove the `inf` positive for anything — that is L4.

---

## 4. Question 2 — the value, and why it has no `F`-free derivation

> **Claim 4.1 (no `F`-free valuation route).** *Any assignment of a numerical value to `ε₀` must
> come from one of exactly two places:*
> *(a) **inverting a modulus** — `ε₀ = F⁻¹(b)` where `b` is the downstream error budget; or*
> *(b) **a direct proof** of the `F`-free repaired statement at an explicit `ε₀`.*
> *There is no third route, because the only `F`-free downstream fact — that `[1/3,2/3]` has width
> `1/3` — is an **error budget**, dimensionally an `F`-value and not an `ε`-value. Converting a
> budget into a threshold **is** a modulus.* **[PROVEN — dimensional, on the two objects' types]**

This is the sting in `mg-345e`'s (correct) threshold-vs-modulus split. Step 6 does not **consume**
`F`; but nothing **computes** `ε₀` without `F`. The split buys the demand side independence from
`F`'s *value*, and it does not buy it a number.

Route (a) is what `Op-Form` §6.4's "L4 usable" row does — `F(ε_leak) <` the pair's slack,
`slack ≤ 1/6` — and it is **BROKEN as labelled** (`mg-e35c` F5): it is calibrated under the literal
branch (iii) that `Op-Form` §3.4 proves cannot close Step 6, and it reads a **necessary** condition
at **maximum** slack as if it were a calibration point. **This is the modulus/threshold conflation
the ticket warns about, in its concrete form: it is a threshold *defined by inverting a modulus*.**

Route (b) is the one that is left, and §6 walks it as far as it goes: it yields **upper** bounds,
because an upper bound needs one witness while a lower bound needs a proof over all posets.

---

## 5. The consumable threshold `ε₀^cons` is not measurable, and pinning it **is** the conjecture

### 5.1 The statement, and what Step 6 knows when it invokes it

Step 6 (`:514–515`) applies L4 to a **minimal counterexample** `P`: `δ(P) < 1/3` (`:71–75`).
So at the moment of use:

* **disjunct (i) is FALSE by hypothesis** — `P` has no 1/3-balanced pair, that is what `δ(P)<1/3`
  means;
* **disjunct (ii) is unavailable** — `mg-3af9`, UNCONDITIONAL, audited `mg-c8c6`
  *(cited here only to say the branch is not in play; it is a **consumption** result and it is
  **not** used anywhere in this document to answer question 1 — see §9)*;
* so the content is **(iii)** alone, in the `F`-free exact form `mg-e35c` F5 recommends:
  *a pair balanced in `P[A]` or `P[B]` remains in `[1/3,2/3]` in `P`*.

Minimality supplies exactly what (iii) needs and no more: both sides are proper induced subposets
of a minimal counterexample, hence `δ(P[A]), δ(P[B]) ≥ 1/3` **unless a side is a chain**.

> **Remark 5.0 (the both-sides-chain escape is closed, and not by L4).** If `P[A]` and `P[B]` are
> both chains then `P` has width `≤ 2` — a 3-element antichain would put two of its elements on one
> side — and the 1/3–2/3 conjecture is a **theorem** for width 2 (Linial). So the case in which
> (iii) has no pair to transfer is settled in the literature and is not a gap in the architecture.
> **[PROVEN modulo the cited theorem; the width bound is one line and is proved here]**

### 5.2 Therefore no computation can bound it

**Claim 5.1.** *On every poset that satisfies the 1/3–2/3 conjecture, the consumable statement
`S(ε)` holds at `ε = 1`, via disjunct (i) alone. Hence `ε₀^cons` measured on any exhibitable
population is `1`, `n`-free, and carries zero information about the object Step 6 consumes.*
**[PROVEN — trivial, and verified exhaustively]**

Instrument **A1** (`code/eps0_threshold_3969/a1_vacuity.py`), exhaustive over **every** poset on
`n ≤ 7` at **every** prefix cut, exact rationals:

| `n` | posets | non-chain | prefix cuts | **posets with no balanced pair** | max `Δ₁` |
|---|---|---|---|---|---|
| 3 | 7 | 6 | 12 | **0** | 2/3 |
| 4 | 40 | 39 | 117 | **0** | 3/4 |
| 5 | 357 | 356 | 1 424 | **0** | 4/5 |
| 6 | 4 824 | 4 823 | 24 115 | **0** | 5/6 |
| 7 | 96 428 | 96 427 | 578 562 | **0** | 6/7 |
| **Σ** | **101 656** | **101 651** | **604 230** | **0** | — |

**The enumeration is checked for COMPLETENESS, not merely for size** (control NC5). Counting
(labelled poset, linear extension) pairs two ways must give
`n!·|poset_iter(n)| = Σ_{labelled P} e(P)`, and the right side is computed from an independent
enumeration (all `3^C(n,2)` orientations, transitivity-filtered), so a systematically missing
isomorphism class cannot cancel. It agrees exactly: `42`, `960`, `42 840` at `n = 3,4,5`. A "the
count looks large" check would not have caught a missing class.

**Disjunct (i) fired at all 604 230 cuts.** The transfer disjunct was never *reached*, let alone
tested. This is not a property of the population; it is structural, and it will hold on any
population anyone can build, because building a population where it fails means exhibiting a
counterexample to the 1/3–2/3 conjecture.

### 5.3 …and proving it **is** the programme's conclusion

**Claim 5.2.** *Let `S(ε₀)` be the consumable statement. Then `S(ε₀)` at any `ε₀ > 0`, together
with Steps 1–5, proves the 1/3–2/3 conjecture.* **[PROVEN]**

*Proof.* Suppose a minimal counterexample `P` exists. Steps 1–5 (i.e. L1, L2, L3 and the
distinguished-order theory) produce a prefix `A_k` with `Δ₁(A_k,A_k^c) ≤ ε₀`. Apply `S(ε₀)`.
Disjunct (i) contradicts `δ(P) < 1/3` outright. Disjunct (iii-exact) exhibits an incomparable pair
with `p^P_{xy} ∈ [1/3,2/3]`, hence `min(p, 1−p) ≥ 1/3`, hence `δ(P) ≥ 1/3` — a contradiction. No
minimal counterexample exists; by well-ordering, no counterexample exists. ∎

**Read together, Claims 5.1 and 5.2 answer question 2 for the consumed object exactly:**
`ε₀^cons` cannot be bounded above without refuting the conjecture, and cannot be bounded below
without proving it (modulo L1–L3). **It is not a constant awaiting measurement. It is the last
lemma of the programme wearing a number's clothes.**

---

## 6. The threshold that *can* be pinned — and a proven ceiling on it

`ε₀^unif` is the honest target: it is what a proof would establish, it implies `ε₀^cons`, and —
unlike `ε₀^cons` — it is refutable, so evidence about it means something. Two readings, because
`mg-3ce3` found the distinction is real:

* **`U_either(ε)`** — `Δ₁(A,B) ≤ ε`, neither side a chain ⟹ a pair balanced in `P[A]` **or** in
  `P[B]` is still in `[1/3,2/3]` in `P`. *This is the form Step 6 can use*: minimality supplies
  both sides, so the argument may pick either.
* **`U_smaller(ε)`** — the same with the pair required to come from the **smaller** side.

Instrument **A2** (`a2_uniform.py`), exhaustive to `n = 6`, every poset, every prefix cut,
25 682 cuts of which 11 480 have both sides non-chain:

> **Claim 6.1.** **`ε₀(U_either) ≤ 17/78 = 0.217949…`, uniformly in `n`.** *Witness: `n = 6`,
> `A = {0,1,2}`, `B = {3,4,5}`, strict relations
> `{(0,2),(0,3),(0,4),(0,5),(1,4),(1,5),(2,4),(3,4)}`, `|L(P)| = 26`, `Δ₁ = 17/78`. Both sides are
> the poset `{x<z} ⊔ {y}`; **all four** balanced-in-side pairs leave `[1/3,2/3]` in `P`
> (`2/3 → 9/13`, `2/3 → 19/26`, `2/3 → 19/26`, `1/3 → 4/13`).* **[PROVEN]**
>
> **Claim 6.2.** **`ε₀(U_smaller) ≤ 1/7 = 0.142857…`, uniformly in `n`.** *Witness: `n = 6`,
> `Δ₁ = 1/7`, the unique smaller-side pair goes `1/2 → 5/7`.* **[PROVEN]**

**Why one witness at one `n` bounds an `n`-free threshold at every `n`.** `ε₀` is by definition a
threshold **valid for all `n` at once**. A single violating instance at `n = 6` and `ε = 17/78`
falsifies the statement at every `ε ≥ 17/78`, therefore bounds the uniform threshold, therefore
bounds it at every `n`. (It says nothing about `ε₀(n)` for a *fixed* `n ≠ 6` — see §9.)

**Both witnesses were re-derived by a second, independent code path** (`a3_witness.py`), which
enumerates linear extensions by filtering all `n!` permutations rather than by the recursive
builder used in the sweep, and prints the full certificate pair-by-pair. The numbers agree exactly.

**Where this lands against the corpus's number.** `Op-Form` §7.2's repaired `ε₀ ≈ 0.20` and
`mg-3ce3`'s "0 RED events up to `ε = 0.20`" are *lower*-bound evidence for `ε₀(U_either)`. The
ceiling is `17/78 = 0.2179`, a factor `1.0897` above it. The corpus's operative constant is
therefore correct to within 9 % *of a bound that is now proven*, and it can never be raised further.
**This is not a contradiction of `mg-3ce3`** — its population is dominated by a `Δ₁ ≤ 0.20` filter
(6 555 of its 6 681 stability points) and my witness sits at `0.2179`, just outside it.

**One scoping remark on `mg-3ce3`'s design, offered as coverage information and not as a defect.**
The probe evaluates each poset at its **best (thinnest) prefix**. L4's hypothesis is universally
quantified over cuts — "*if `Δ₁(A,B) ≤ ε`*" — and the architecture's cut is whichever one Cheeger
sweeping hands it (`:502–507`), which is not chosen for thinness. Testing the thinnest cut tests
strictly fewer instances than L4 asserts. My sweep quantifies over **all** prefix cuts, which is
why it reaches a violator the probe's frame excludes.

### 6.1 The failure mechanism — and a prediction of mine that lost

`Op-Form` Claim 3.3 exhibits a poset with `δ = 1/3` *exactly*, and concludes that minimality can
never be strengthened to supply interior slack. **My witness for Claim 6.1 is that objection made
concrete**: both of its sides *are* that zero-slack poset, so every pair the side offers sits on an
endpoint of `[1/3,2/3]` and any drift at all evicts it.

I expected that to be the whole story, and wrote the instrument to say so. **It is not.**
Instrument **A4** (`a4_mechanism.py`) reports 42 `U_either` failures at `n ≤ 6` with **two**
distinct maximal interior slacks: `0` **and `1/6`**. Slack `1/6` is a pair at `p_side = 1/2` — dead
centre of the window, the most interior a pair can be — **pushed out of `[1/3,2/3]` in `P` at
`Δ₁ = 5/19 = 0.263`**. So:

* the endpoint gap is *a* mechanism, not *the* mechanism;
* a repair that assumed a fixed interior slack `c > 0` on the side would **not** be safe — my own
  control fired against my hypothesis and I am reporting the loss;
* `mg-3ce3`'s reading at its `:150–153` — *"a pair sitting comfortably inside the side's interval
  (e.g. `p^side = ½`) cannot be pushed out"* — is stated there **for `ε < 0.05`** and is **not
  contradicted**; but the intuition behind it fails by `ε ≈ 0.263`, and the document does not say
  where it stops being true. That boundary is now known to be `≤ 5/19`.

---

## 7. Question 3 — can `ε_dem` be reached without `ε₀`? The disjunct fires, split

**I am not deriving `ε_dem`; that is `mg-845e` and it stays with `pm-onethird`.** What follows is
only the answer to "is `ε₀` needed at all", which is the question this ticket was filed to answer.

The demand chain has exactly one free input once `mg-76b2` lands. From `Op-Form` §4.2's boxed
`ε_spec ≤ ½ ε_leak²` and `mg-345e` §4's `ε_dem = ε_leak²/(2C₃)`, with `C₃ = 1` uniformly in `n`
(`mg-76b2`, audited `mg-94c3`, **conditional on L2**):

```
      ε_dem  =  ε₀² / 2          — one equation, one unknown, and the unknown is this ticket's
```

Arithmetic check against the corpus's own two calibrations, which is how you can tell the equation
is the right one: `0.02²/2 = 2×10⁻⁴` (the superseded figure) and `0.20²/2 = 2×10⁻²` (the repaired
one), and the `mg-e35c` F5 banner's **"100× too pessimistic" is exactly `10²`, the square of the
10× move in `ε₀`**. Every digit in that banner is a digit of `ε₀`.

**So the answer splits, and both halves are real answers:**

* **`ε_dem`'s FORM — an absolute constant uniform in `n` — IS reachable without `ε₀`.** It needs
  only: `ε₀`'s *form* is `n`-free (§1, §3, `F`-free by Claim 3.1); squaring a constant gives a
  constant (`Op-Form` §4.2, no `n` enters); `C₃ = 1` is uniform in `n` (`mg-76b2`). **`mg-845e`'s
  qualitative half is dischargeable today**, conditional on L2 and on `ε₀ > 0`.
* **`ε_dem`'s VALUE is NOT reachable without `ε₀`, and this is now closed rather than open.**
  `ε_dem = ε₀²/2` has no other input. By Claim 4.1 `ε₀` has no `F`-free valuation route; by Claims
  5.1–5.2 the consumable `ε₀` is unmeasurable and proving it positive proves the conjecture. The
  best that can be offered is the sandwich

  ```
      ε_dem  ≤  (17/78)² / 2  =  289/12168  =  0.023751…       [PROVEN ceiling, uniform in n]
      ε_dem  ≈  (0.20)²  / 2  =  0.02                          [the corpus's calibration]
  ```

  i.e. **`ε_dem ≤ 289/12168 = 0.023751`**, a ceiling the corpus's `2×10⁻²` sits under by a factor
  `1.1875` — **under 19 % of headroom in the demand constant, and none of it is free.**
  *(Stated for the `U_either` threshold; carried through the same chain the corpus already uses, and
  conditional on L2 through `C₃`. This is a bound on an input, not a derivation of `ε_dem`.)*

**Recommendation to `pm-onethird`, who owns the gate.** Clause (a) as worded — *"`ε₀`'s
`n`-freeness and its value"* — **cannot be discharged as worded**, because for the object it names
(`ε₀^cons`) the value question is the conjecture. Re-word the clause against `ε₀^unif`, for which
this document supplies `n`-freeness of form and a proven ceiling `17/78`, and record that the
remaining unknown in `ε_dem` is `ε₀ > 0` and nothing else.

---

## 8. Candidates ruled out — the enumeration, because a bare negative goes unchecked

The ticket asks for this explicitly. Every place an `n`-free `ε₀` **with a value** could have come
from, and why each fails:

| # | candidate source of a value | verdict |
|---|---|---|
| **K1** | L4's statement, `:464–474` | **NO `ε₀` PRESENT.** No domain restriction; 0 occurrences of any threshold symbol in the file. §1 |
| **K2** | the source's one "sufficiently small `ε`", `:497` | **WRONG `ε`.** That is `ε_spec` in Step 2; L4's is the leakage `ε` of `:459`/`:466`. §1.4 |
| **K3** | the source's `ε ≪ 1`, `:459` | **REAL, `n`-FREE IN FORM, VALUELESS.** Informal, outside the conjecture environment, compares to `1`. It is the *only* smallness demand on L4's `ε` in the source |
| **K4** | L4's summary line, `:567–569` ("sufficiently small prefix leakage") | **SAME AS K3, WEAKER.** A prose gloss in the open-lemmas list; no quantifier, no value |
| **K5** | `Op-Form` §3.2's `F : (0,ε₀) → ℝ≥0` | **READER'S ARTEFACT.** `ε₀` is introduced to make "`F(ε)→0`" well-typed. It is a domain of definition; `Op-Form` never assigns it a value and could not |
| **K6** | `Op-Form` §6.4's "L4 usable" row, `ε₀ = F⁻¹(slack)`, `slack ≤ 1/6` | **BROKEN as labelled** (`mg-e35c` F5) **and modulus-derived** — this is the conflation the ticket names, in its concrete form. §4 |
| **K7** | `Op-Form` §4.1's `Δ₁ ≤ ε₀·min(k,n−k)` | **A RE-READING OF `≪`, NOT A VALUE.** It fixes the *form* (constant fraction, not `o(·)`) and explicitly leaves the constant open |
| **K8** | `mg-3ce3`'s empirical envelope, `ε = 0.20`, 6 681 posets, `n ≤ 16` | **CALIBRATION, NOT DERIVATION**, and of `ε₀^unif` not `ε₀^cons`; its frame is `Δ₁ ≤ 0.20` and best-prefix-only, so it could not have found the `17/78` ceiling. §6 |
| **K9** | the downstream window `[1/3,2/3]`, width `1/3` | **AN ERROR BUDGET, NOT A THRESHOLD.** Converting it to an `ε` requires `F`. Claim 4.1 |
| **K10** | `mg-3af9` / `mg-c8c6` (branch (ii) unconsumable for every positive `F`) | **NOT ABOUT THE THRESHOLD AT ALL.** A Step-6 consumption result about the modulus. Cited in §5.1 only to record that branch (ii) is not in play, and used nowhere in the answer to question 1. This is the drift the ticket warned against and it was checked for |
| **K11** | exhaustive computation on real posets | **STRUCTURALLY VACUOUS** for `ε₀^cons` (604 230 cuts, disjunct (i) fired at every one), **and productive for `ε₀^unif`**, where it gives the `17/78` ceiling. §5, §6 |
| **K12** | the archived `UC-Lean-L4` / `F32-L4` items | **DIFFERENT L4.** The `union_closed` cohomology lineage; `pm-onethird`'s 2026-08-09 sweep established this and I did not re-open it |
| **K13** | `Op-Form` Claim 3.2 — literal (iii) closes Step 6 for **no** `F(ε) > 0` — read as "`ε₀ = 0` under the literal reading" | **TRUE BUT NOT A THRESHOLD FACT, AND NOT USED IN THE VERDICT.** It is a Step-6 **consumption** result whose quantifier is over `F`, so reading it as an answer to question 1 is the modulus drift in its subtlest form. It is listed because it is the candidate most likely to be mistaken for an answer. What it *does* license is the choice of the `F`-free repaired (iii) as the object §6 bounds — which is `mg-e35c` F5's recommendation, not a threshold derivation |

---

## 9. What I did NOT do

* **I did not attempt to prove or refute L4**, in any branch, at any modulus. Claims 6.1/6.2 refute
  a *uniform-in-`n` threshold above `17/78`* for the `F`-free repaired transfer read over **all**
  posets. They say **nothing** about L4-as-stated, whose branch (ii) remains available to any poset
  my witnesses cover, and nothing about whether `ε₀ > 0`.
* **I did not derive `ε_dem`.** §7 gives the functional dependence (which is already `Op-Form`
  §4.2's boxed relation) and a ceiling on an input. `mg-845e` is untouched and stays blocked until
  `pm-onethird` re-reads its own gate.
* **I did not re-attack `C₃`.** `C₃ = 1` is taken from `mg-76b2` as read, with its L2 conditionality
  carried through every line that uses it and spent nowhere else.
* **I did not use `mg-3af9` to answer question 1.** See K10.
* **I did not edit `STATE.md`.** Its `ε₀` sentences sit inside `pm-onethird`'s one-paragraph state
  and inside a blocked item's gate; proposed text is in §10 and the verdict was mailed rather than
  landed, so the gate stays where its owner put it.
* **My exhaustive sweeps stop at `n = 7` (vacuity) and `n = 6` (the ceiling).** The `n = 7` uniform
  sweep was launched and is **not** included; if it finds a thinner violator the ceiling drops and
  Claim 6.1 becomes an over-estimate — it can never become wrong in the other direction.
* **The ceiling bounds a uniform threshold, not `ε₀(n)` at a fixed `n`.** Nothing here says
  `ε₀(5) ≤ 17/78`; at `n ≤ 5` there is no `U_either` violator at any `ε` whatever.
* **My sweeps skip every cut at which *either* side is a chain — a coverage gap I did not close.**
  Only the *both*-sides-chain case is genuinely outside the statement (Remark 5.0). When exactly
  **one** side is a chain the architecture still works — the other side supplies the pair — and a
  violator could live there. Excluding those cuts makes the population smaller, so it can only make
  my ceiling **too high**: the bounds stand, and a sweep that includes them may lower both.
* **I used prefix cuts of the identity linear extension.** For a *counterexample* the architecture's
  cut is a prefix of the **distinguished order** (`:82–86`), which exists only for counterexamples;
  on real posets there is no such order, and every poset in my population is presented in a normal
  form where the identity is a linear extension. That is the natural analogue and it is not the
  same object.
* **Linial's width-2 theorem (Remark 5.0) is cited, not proved.** The width bound itself is proved.
* **I did not verify `mg-3ce3`'s own numbers** (`F(ε)` envelope, the 89 smaller-side losses, the
  first-loss `ε = 0.085`). My `U_smaller` ceiling `1/7 = 0.1429` is **independent** and, being on a
  population `mg-3ce3` did not cover (`n ≤ 6` exhaustive vs its sampled `n = 8,9,10` + families),
  neither confirms nor contradicts its `0.085`. Two upper bounds, the smaller of which wins: if
  `0.085` is right, it is the operative ceiling for that reading.

---

## 10. Proposed text (not applied — `pm-onethird`'s to land)

For `STATE.md`'s `ε_dem` sentence:

> `ε_dem` is gated on L4's **threshold** `ε₀`, not its modulus — and `ε₀` **is not in the source**
> (`mg-3969`): L4 `:464–474` carries no threshold, the file's one "sufficiently small `ε`" at
> `:497` is the *spectral* `ε`, and the only smallness demand on the leakage `ε` is the informal
> `ε ≪ 1` at `:459`. Three objects share the name. The one Step 6 consumes is **unmeasurable** —
> on a minimal counterexample disjunct (i) is false by hypothesis, on every exhibitable poset it is
> true at `ε = 1` (604 230 prefix cuts, `n ≤ 7`, 0 exceptions) — and proving it positive **is** the
> conjecture on the thin-interface class. The one a proof can produce is the uniform transfer
> threshold, now capped: **`ε₀ ≤ 17/78 = 0.2179` uniformly in `n`** (witness at `n = 6`), against
> the corpus's calibrated `0.20` — **a factor 1.0897, under 9 % of headroom and no more**. With
> `C₃ = 1` (`mg-76b2`,
> conditional on L2), **`ε_dem = ε₀²/2 ≤ 0.0238`**, and the `mg-e35c` F5 banner's "100×" is exactly
> the square of a 10× move in `ε₀`.

---

## 11. Reproduce

```
python3 code/eps0_threshold_3969/a1_vacuity.py 7    # vacuity of the consumable threshold
python3 code/eps0_threshold_3969/a2_uniform.py 6    # the ceilings, exhaustive
python3 code/eps0_threshold_3969/a3_witness.py      # both witnesses, second code path
python3 code/eps0_threshold_3969/a4_mechanism.py 6  # failure mechanism; my losing prediction
```

Controls, all firing, reported inline by the instruments: **PC1** the `δ = 1/3` endpoint poset
(positive control on the `δ` code); **NC1** chains have `Δ₁ = 0` at every prefix and no `δ`;
**NC2** the antichain reproduces `Op-Form` §4.2's hand computation `Δ₁ = Φ = (n−k)/n` *and*
Lemma 2.1's `Φ = Δ₁` identity, independently, at `n = 4,5,6`; **NC3** `Δ₁ ≤ 1` respected and
approached; **NC4** a deliberately wrong transfer predicate (exact preservation `p^P = p^side`)
fails at 9 986 cuts, so the instrument can tell predicates apart.
