# mg-d3c7 — INDEPENDENT AUDIT of mg-3969 (L4's threshold `ε₀`)

**Work item:** `mg-d3c7`, pre-filed in the same action as its parent `mg-3969`.
**Parent under audit:** `docs/OneThird-L4-Threshold-eps0-mg-3969.md` at `6fdf0ec`,
plus `code/eps0_threshold_3969/`.
**My instrument:** `code/eps0_audit_d3c7/` — written from the source definitions,
sharing no code with the parent's. Exact `Fraction` throughout.
**Predictions:** `code/eps0_audit_d3c7/PREDICTIONS.md`, committed at `b2e5fcd`
before the parent's document, its code, or L4's source were opened.

---

## 0. Verdict

> **CONFIRMED ON THE CENTRAL VERDICT, WITH ONE MATERIAL FINDING AGAINST THE
> HEADLINE NUMBER'S SCOPE.**
>
> **The gate did not fire.** `mg-3969` answered the **THRESHOLD** question, not the
> modulus question. I checked this first, as instructed, and I checked it by reading
> the argument rather than by accepting the parent's own `K10` disclosure.
>
> **`ε₀` really is not in the source.** I read L4 at source myself and ran my own
> byte-wise search over the whole 603-line file, broader than the parent's
> eleven-line one: **`\varepsilon_0` / `eps_0` / `epsilon_0` occur 0 times in the
> entire document**, `F(` occurs exactly 3 times and all 3 are inside L4, and the
> only smallness demand on L4's leakage `ε` is the informal `ε ≪ 1` at `:459`.
>
> **`17/78` reproduces exactly on my own code path**, as does every other number
> the parent publishes: `e(P) = 26`, `Δ₁ = 17/78`, all four landing values, the
> `42` failures at `n ≤ 6`, the `682` at `n ≤ 7`, the `335 496` in-scope cuts, the
> `13/111`, and all eight arithmetic figures. **I also searched for the thing the
> parent's negative says does not exist** — a `U_either` violator thinner than
> `17/78` — exhaustively over all 96 428 naturally labelled posets on `[7]` and all
> 578 568 prefix cuts, and **there is none.** In the parent's own scope the ceiling
> is right.
>
> **THE FINDING: `17/78` IS SCOPE-DEPENDENT, AND IN THE SCOPE `mg-3969` ITSELF
> NAMES AS THE ARCHITECTURALLY REQUIRED ONE, THE CEILING IS NOT `17/78` — IT IS
> `0`.** The parent's sweeps skip every cut at which *either* side is a chain. Its
> §9 discloses this, calls it "a coverage gap I did not close", and predicts
> correctly that closing it "can only make my ceiling too high … a sweep that
> includes them may lower both". I closed it. It does not merely lower the ceiling:
> **there is an infinite family of violators with `Δ₁ → 0`** — a chain
> `c₁<⋯<c_{n−1}` plus one isolated element, cut at `A = {z, c₁,…,c_{k−1}}` with
> `n = 2k+1`, giving `Δ₁ = (k+1)/((2k+1)k) → 0` with **every** balanced-in-side pair
> evicted at every `k ≥ 3`. Verified in exact rationals to `k = 200`, hand formula
> agreeing at every member, brute-force `n!` path agreeing at `n ≤ 9`.
>
> So the parent's §0 table row — *"`U_either` — the `F`-free repaired transfer,
> **either** side, asserted for **all** posets | `ε₀ ≤ 17/78`, uniformly in `n` |
> **PROVEN**"* — **names a statement it does not bound.** The statement as worded
> ("asserted for all posets") has `ε₀ = 0`; the bound `17/78` belongs to the
> both-sides-non-chain restriction of it. Three downstream claims inherit the
> defect: §0's *"`ε₀` cannot be raised by more than 9 %, ever, at any `n`"*, §7's
> recommendation to release `mg-845e` against *"`ε₀(U_either) ∈ (0, 17/78]`, which
> is the only one a proof can ever produce"* (that interval is **empty** in the
> required scope), and §10's proposed `STATE.md` text, which carries `17/78` and
> *"under 9 % of headroom and no more"* with no scope qualifier at all.
>
> **This does not touch L4, and it strengthens rather than weakens the parent's
> own headline.** My family satisfies L4-as-stated via disjunct **(i)** —
> `δ(P) = ⌊n/2⌋/n ≥ 1/3` at every member — so what it refutes is the parent's
> deliberately **(i)-free** surrogate `U_either`, not the conjecture at `:464–474`.
> And the parent's leading conclusion is that the *consumable* `ε₀^cons` is
> unmeasurable and that proving it positive **is** the 1/3–2/3 conjecture. My
> finding says the "honest, refutable" surrogate the parent offered as the
> replacement target is itself dead. **There is no measurable positive threshold
> here at all** — which is the parent's own thesis, one notch sharper.
>
> **Two smaller findings**, both presentational, both fully reconciled below: the
> document prints two different totals for what reads as one sweep (`604 230` in
> §5.2 vs `604 250` in §6.0 — the difference is exactly the chain posets), and
> Claim 6.2's `n = 6` fallback witness at `1/7` sits at an `|A| = |B| = 3` **tie**
> cut, so "the smaller side" there is a designated choice rather than a size fact.
>
> **Six of my eight substantive predictions LOST.** The parent is stronger than I
> bet against it on every re-derivation I attempted, including my principal live
> bet. The scorecard is §8.

---

## 1. The gate, checked first — DID NOT FIRE

The brief: *"Did the parent answer the THRESHOLD question or the MODULUS question?
… If the parent's argument routes through `mg-3af9` / `mg-c8c6` … then it has
answered the wrong question, and that is the finding. Check this before you check
anything else."*

**Defect criterion, bound in `PREDICTIONS.md` §B before I looked:** the gate fires
only if an `mg-3af9`/`mg-c8c6` citation supports a step in the chain answering
question 1 (`n`-freeness) or question 2 (value). A citation used to *distinguish*
the modulus from the threshold, or to answer question 3's disjunct, is correct use.

**Every occurrence in the parent's deliverable** (`grep` over the document and all
of `code/eps0_threshold_3969/`):

| site | use | verdict |
|---|---|---|
| `:225` | §5.1's three-bullet inventory of what Step 6 knows: *"disjunct (ii) is unavailable — `mg-3af9`, UNCONDITIONAL, audited `mg-c8c6`"*, with an inline parenthetical saying it is cited only to say the branch is not in play | **bookkeeping, not a step** |
| `:441` | the `K10` row of the ruled-out table, which flags it as *"NOT ABOUT THE THRESHOLD AT ALL"* | **self-disclosure** |
| `:459` | §9's *"I did not use `mg-3af9` to answer question 1"* | **self-disclosure** |
| code | 0 occurrences | — |

**I did not accept `K10`.** I read §1 and §3 — the sections that actually answer
question 1 — end to end. They use exactly three inputs: the text of L4 at
`:464–474`; the definition of `Δ₁` at `:270–278`; and the `Δ₁ ≤ 1` bound. No
consumption result appears in either. Deleting `:225` would remove a sentence of
context from §5.1 and change no conclusion anywhere.

**GATE: CLEAN.** The parent answered the threshold question. It also, at `K13`,
volunteers the subtler drift candidate (`Op-Form` Claim 3.2 read as "`ε₀ = 0`
under the literal reading") and rules it out for the right reason — the quantifier
there is over `F`. That row is the strongest evidence the parent was actually
looking for the drift rather than reciting a denial of it.

---

## 2. L4 at source — read by me, and my own enumeration of what is not there

**The source is not in either repository.** It is

```
/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex
603 lines · md5 db095fbe12ba19f0a8107f962c0d1c8f · mtime 2026-07-12 16:13
```

**Provenance of my route, stated because it matters.** I did *not* find the file
from the parent. I found `L4` referenced across the corpus, followed
`OneThird-lambda-std-Operative-Form.md:95–98` — which names the canonical source
and says "line references below are to that file" — and opened it directly. So the
*location* came through a restatement (`Op-Form`), and the *text* came from the
source. That is the honest description; the brief's concern is that the parent may
have quoted a restatement, and the check below settles that it did not.

**L4, `:464–474`, as I read it (my own `Read` of the file, not the parent's block):**

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

**This is byte-identical to the parent's §1 block and to `Op-Form` §3.1.** The
parent quoted the source. Eleven lines, `464`–`474`, `F(ε)n` at `:469` — all three
confirmed. *(Per `PREDICTIONS.md` P9 this is **replication**, not independent
corroboration: exposure H2 handed me the line range and the `F(ε)n` before I
started. It carries no weight as evidence and is recorded only because the brief
asks which document and line I read.)*

### 2.1 My own search for a threshold, which is broader than the parent's

The parent checked its table (`:99–107`) over the whole file. I ran my own,
independently phrased, and I add two rows it does not have:

| looked for | my count | where |
|---|---|---|
| `varepsilon_0` / `varepsilon_{0}` / `eps_0` / `epsilon_0` | **0** | nowhere in 603 lines |
| `sufficiently small` / `small enough` / `suitably small` | **1** | `:497` — Step 2, on `λ_std ≥ 1−ε`, the **spectral** `ε` |
| `\ll 1` (any spacing) | **3** | `:445`, `:447`, `:459` |
| `threshold` | **2** | `:326`, `:361` — both *threshold sets of an eigenvector* |
| **`F(`** *(my row)* | **3** | `:465`, `:469`, `:472` — **all three inside L4** |
| **`absolute constant`** *(my row)* | **0** | — |

Two things follow that are mine rather than the parent's:

1. **`F` occurs nowhere outside L4.** So there is no second site in the source at
   which a domain, a threshold, or a growth condition could have been attached to
   `F` and then imported. Whatever `F`'s domain is, the source never says.
2. **The parent's `threshold` count is `3`; mine is `2`.** Its table cites a third
   at `:548` ("falsification tests" prose). My `grep -ni threshold` returns two
   hits, `:326` and `:361`. This is a **miscount of a null result** — both of us
   conclude no hit is a threshold on `ε`, and the parent's extra row is if anything
   *more* conservative — so it changes nothing, and I record it only so the table
   is not quoted onward as exact.

### 2.2 The quantifier order, written out — the brief's item 2

The source sentence is *"There exists `F(ε)→0` such that if `Δ₁(A,B) ≤ ε`, then …"*.
`P`, `n`, `A`, `B` and `ε` are all free in the "such that" clause and therefore all
lie **inside** the scope of the `∃F`. Written out:

```
  ∃F [ lim_{ε→0} F(ε) = 0 ]
      ∀ε > 0  ∀n  ∀P on [n]  ∀(A,B) a partition of [n]
          [ Δ₁(A,B) ≤ ε  ⟹  (i) ∨ (ii) ∨ (iii) ]
```

**`F` is quantified before `n`.** That is `Op-Form` Claim 3.1's result and it is a
statement about the **MODULUS**. It is not what this ticket asked.

**For the THRESHOLD the quantifier question has no referent, and that is the
answer.** There is no `ε₀` variable in the sentence to quantify in the first place.
`ε` is universally quantified with no lower-bounded restriction; the `→0` is a
condition **on `F`**, not a restriction on `F`'s domain. So question 1's dichotomy
("`n`-free `ε₀`, or `ε₀(n)`?") is ill-posed against the source. **I reach the
parent's §0 conclusion, and I reach it from the quantifier rather than from the
string count.**

**The one implicit threshold, and its status — this is mine, not the parent's.**
For `lim_{ε→0} F(ε) = 0` to be well-formed, `F` must be defined on some punctured
right-neighbourhood `(0, δ)` of `0`. `δ` is a genuine hidden threshold: at `ε ≥ δ`
the term `F(ε)n` in branch (ii) has no value. But **`δ` is a parameter of `F`, and
`F` sits inside the same `∃` that precedes `∀n`**. So:

> **The implicit threshold is `n`-free, and it is `n`-free for exactly the same
> reason the modulus is: both are chosen before `n` is seen.** Its *value* is
> whatever the (unknown) `F`'s domain happens to be, so no value can be pinned
> without exhibiting an `F`.

This is the `K5` object — the parent classifies it as a **"reader's artefact"**
introduced by `Op-Form` §3.2 to make `F(ε)→0` well-typed, and says `Op-Form` "never
assigns it a value and could not". I reached `K5` independently, from the quantifier,
before reading `K5`; we agree, and I record that the parent's classification is
correct and slightly understated — the artefact is *forced* by well-typedness, not
merely convenient, and it inherits `n`-freeness from the quantifier order for free.

### 2.3 What this retires

My `PREDICTIONS.md` P4 (my principal live bet, 0.45) was that the parent's negative
would be the **lexical** fact "`ε₀` occurs zero times" standing in for the
**semantic** claim "L4 states no threshold". My guard required me to enumerate all
four smallness-of-`ε` devices at source before scoring it. I did:

| device | present in L4 `:464–474`? | parent's handling |
|---|---|---|
| a named threshold constant | **no** (0 occurrences file-wide) | `K1` |
| an unnamed "sufficiently small" | **no** in L4; the file's one instance at `:497` is the spectral `ε` | `K2` |
| a domain restriction implicit in `F` | **yes, but** it is `F`'s own parameter and `n`-free | `K5` |
| smallness carried by quantifier scope / prose | **yes**: the informal `ε ≪ 1` at `:459`, *outside* the conjecture environment | `K3`, and `K4` for the `:567–569` gloss |

**All four are enumerated by the parent, including the two that are genuinely
present.** P4 is a clean loss. The negative is an enumeration, not a failed search.

---

## 3. `17/78` re-derived — the brief's item 3

### 3.1 My instrument, and its controls

`code/eps0_audit_d3c7/lib_d3c7.py` implements, from the source definitions only:
linear-extension counting by down-set DP; `Δ₁(A_k,B) = E|A_k \ σ(A_k)| / min(k,n−k)`
(`:270–278`); and `p_xy` (`:59–66`). The population is **naturally labelled posets**
on `[n]` — posets for which the identity order is a linear extension — with
`A_k = {0,…,k−1}`, which is exactly the set of (poset, linear extension, prefix cut)
triples. It shares no code with `code/eps0_threshold_3969/`.

`b0_selftest.py`, **all green** (`out_b0_selftest.txt`):

* **C1** poset counts `1,1,2,7,40,357,4824,96428` — OEIS A006455, matching the
  parent's population sizes exactly at every `n`.
* **C3** the double-count identity `Σ_{labelled P} e(P) = n!·|NLP(n)|`, with the left
  side from an *independent* enumeration (filter all relations for antisymmetry and
  transitivity): `1, 4, 42, 960`. A systematically missing isomorphism class cannot
  cancel in this identity.
* **C4/C5/C6** DP `e(P)`, `Δ₁` and `p_xy` against a brute-force `n!`-filtering
  enumerator, **every** poset and cut and pair at `n ≤ 5`: 0 mismatches.
* **C7 — a control that fired, and became a finding.** I built a negative control on
  the *other* reading of `σ(A)` ("the positions of `A`'s elements" rather than "the
  elements at `A`'s positions"). It **failed to discriminate: 0 disagreements over
  1 562 cuts.** That is not a bug — the two readings are *provably* the same number
  on prefix cuts, because `A_k = {0..k−1}` is simultaneously a set of labels and the
  set of positions `0..k−1`, so `|A \ {positions of A}| = k − |{a ∈ A : pos(a) < k}|
  = |A \ σ(A)|`. **The `σ(A)` ambiguity is immaterial here**, which retires a live
  objection to the whole measurement — mine and the parent's. The control is kept
  and now asserts the agreement.
* **C7b** a control that *does* discriminate, since C7 turned out not to: `Φ_P(A_k)`
  (divide by `|A|`, `:229–237`) vs `Δ₁` (divide by `min(|A|,|B|)`). It differs on
  **exactly** the predicted set — `{k > n/2, value ≠ 0}`, 698 cuts, 0 mispredictions.
* **C8** `Δ₁ ≤ 1` everywhere, attained at `(n−1)/n` by the antichain at `n = 3..7`.

### 3.2 The witness, recomputed (`b1_witness.py`)

Taking only the parent's *relation list* — a witness is a claim about a specific
object, so quoting the object is not replication; recomputing its properties is the
check — and recomputing everything else:

| quantity | mg-3969 | mine | |
|---|---|---|---|
| transitively closed as given | — | **yes** | (checked; nothing added) |
| `e(P)` | 26 | **26** | ✔ |
| `Δ₁(A₃,B)` | `17/78` | **`17/78`** | ✔ exact |
| balanced-in-side pairs | 4 | **4** | ✔ |
| their side values | `2/3,2/3,2/3,1/3` | **`2/3,2/3,2/3,1/3`** | ✔ |
| their values in `P` | `9/13, 19/26, 19/26, 4/13` | **`9/13, 19/26, 19/26, 4/13`** | ✔ multiset |
| survivors | 0 | **0** | ✔ |
| interior slack of each side pair | 0 (§6.1) | **0, 0, 0, 0** | ✔ |

`Δ₁` at the poset's other cuts is `4/13, 5/26, 17/78, 5/26, 9/13` — so `k = 3` is
not even the thinnest cut of its own poset, which is the right shape: the ceiling is
a minimum over *violating* cuts, not over cuts.

### 3.3 Why one witness bounds an `n`-free threshold — P5, and why it lost

My `PREDICTIONS.md` P5 (0.40) was that the `n`-freeness of `17/78` would rest on a
finite sweep plus an informal extrapolation, the word "PROVEN" doing work two data
points cannot do. **It lost, and the parent's one-line argument at `:329–332` is
airtight.** Restating it in my own terms to be sure I am not just nodding along:

`ε₀(U_either) := sup{ ε : U_either(ε) holds }`, and `U_either(ε)` is universally
quantified over **all** `n` at once. A single instance at `n = 6` with
`Δ₁ = 17/78` at which the conclusion fails makes `U_either(ε)` **false for every
`ε ≥ 17/78`**, because that instance satisfies the hypothesis `Δ₁ ≤ ε` at every such
`ε`. The satisfied set is downward closed and excludes `17/78`, so
`sup ≤ 17/78`. **No extrapolation occurs; the quantifier does the work.** `≤` (not
`<`) is exactly the right relation, and the parent uses it.

This is the division of labour my error `E3` warned me to look for before attacking
the sweep: the sweep does not prove `n`-freeness, it *finds a witness*, and the
`n`-freeness is a one-line consequence of what `ε₀` means. I filed `E3` in advance
and it fired against me correctly.

### 3.4 The normalisation, named — and the brief named the wrong pair

The brief asks me to say which normalisation I checked in, warning that `ε_spec` and
`ε_c3ca` differ and that a factor discrepancy between them has already produced one
wrong headline.

> **My normalisation is `ε_leak := Δ₁(A,B) = E|A \ σ(A)| / min(|A|,|B|)`,** the `L¹`
> ordinal-sum defect defined at source `:270–278` and identified as L4's leakage `ε`
> (`:466`) by `Op-Form` §1's symbol table.

**This is a THIRD normalisation, and it is neither of the two the brief names.**
`ε_c3ca` and `ε_spec` are two divisions of `E[inv_e]` (`STATE.md:15`:
`÷ n²` and `÷ (n²−1)/6`, ratio `→ 6`). `ε_leak` is not a division of `E[inv_e]` at
all — it is a per-element crossing density — and it reaches `ε_spec` through
**Cheeger**, i.e. by a **square**: `ε_spec ≤ ½·ε_leak²` (`Op-Form` §4.2).

So **the factor-of-6 trap cannot fire on these numbers**, and `17/78` vs the
corpus's `0.20` is like-for-like: `Op-Form`'s row 28 repaired budget is
`ε_leak ≈ 0.20`, the same object. **The trap that *can* fire here is the square,**
and the parent handles it correctly and checks it: `0.02²/2 = 2×10⁻⁴` and
`0.20²/2 = 2×10⁻²` recover both of the corpus's own calibrations, which is a real
consistency check on the equation `ε_dem = ε₀²/2` rather than a restatement of it.

**All eight published arithmetic figures verified exactly** (`b7_scope_and_arith.py`
D3): `17/78 = 0.217949`; `13/111 = 0.117117`; `(17/78)/0.20 = 1.0897`;
`(17/78)²/2 = 289/12168 = 0.023751` (equal as exact `Fraction`s);
`0.023751/0.02 = 1.1875`; and the `mg-e35c` F5 banner's `100×` is exactly
`(0.20/0.02)² = 100`.

**P7 lost too.** I predicted `78` and `111` were pair counts and that `111` was not
a binomial. They are `e(P)·min(|A|,|B|)`: `26 × 3 = 78` and `37 × 3 = 111`. Same kind
of object, and directly comparable.

### 3.5 I searched for the thing the negative says does not exist

The brief: *"A negative is the cheapest thing to assert and the hardest to check …
Try to construct the thing it says does not exist."* The parent's ceiling asserts a
negative — no `U_either` violator thinner than `17/78`.

`b2_sweep.py 7`, exhaustive, **in the parent's own scope**:

| `n` | posets | prefix cuts | both sides non-chain | `U_either` failures |
|---|---|---|---|---|
| 4 | 40 | 120 | 16 | 0 |
| 5 | 357 | 1 428 | 444 | 0 |
| 6 | 4 824 | 24 120 | 11 020 | **42** |
| 7 | 96 428 | 578 568 | 324 016 | **640** |
| **Σ** | **101 656** | **604 230** *(non-chain posets)* | **335 496** | **682** |

**Every one of these matches `mg-3969` exactly** — its `42`, its `682`, its
`335 496`, its `11 480` cumulative at `n ≤ 6` (`16+444+11020`). And:

> **`U_either`: 0 violators with `Δ₁ < 17/78` anywhere at `n ≤ 7`.**
> **`U_smaller`: thinnest at `13/111`, `n = 7`, `k = 4`** — the parent's Claim 6.2,
> at an unequal split (`|A| = 4`, `|B| = 3`), reproduced exactly.

**The negative holds in the parent's scope. I tried to break it and could not.**

---

## 4. THE FINDING — the scope, and the ceiling that is `0`

### 4.1 What mg-3969 says about its own gap

`mg-3969` §9, verbatim:

> *"**My sweeps skip every cut at which *either* side is a chain — a coverage gap I
> did not close.** Only the *both*-sides-chain case is genuinely outside the
> statement (Remark 5.0). When exactly **one** side is a chain the architecture
> still works — the other side supplies the pair — and a violator could live there.
> Excluding those cuts makes the population smaller, so it can only make my ceiling
> **too high**: the bounds stand, and a sweep that includes them may lower both."*

That is an honest, correctly-signed disclosure of an open hole, and I accept every
word of its reasoning. **The architecturally required scope is "at least one side
non-chain"**: on a minimal counterexample disjunct (i) is false by hypothesis, so a
pair must transfer from a side; a single chain side merely means the pair comes from
the other one; and the both-sides-chain case is settled by Remark 5.0 (two chain
sides force width `≤ 2`, and Linial's theorem covers width 2).

**It is cheap to close and it was not closed.** `b4_fullsweep.py 7` closes it.

### 4.2 Closing it (`b4_fullsweep.py`, exhaustive to `n = 7`)

| scope | cuts | `U_either` violators | thinnest `Δ₁` |
|---|---|---|---|
| **BOTH** sides non-chain *(mg-3969's)* | 335 496 | 682 | **`17/78 = 0.217949`** |
| **ONE+** at least one non-chain *(required)* | 604 012 | **2 042** | **`1/7 = 0.142857`** |

`1/7 < 17/78`, and `1/7 = 0.1429` is **below** the corpus's calibrated `0.20`, not
9 % above it. Eight witnesses sit at exactly `1/7`, all at `n = 7`; five are
certified in `b5_gapwitness.py` on the **second code path** (linear extensions by
filtering all `n!` permutations, no down-set DP), with `e(P)`, `Δ₁` and every pair
probability agreeing; and **0 violators exist below `1/7` at `n ≤ 7`.**

The simplest witness is hand-checkable in four lines — and it is far simpler than
the parent's 26-extension one:

> `n = 7`, `P` = the chain `1<2<3<4<5<6` plus one isolated element `0`; `e(P) = 7`.
> `A = {0,1,2,3}`, `B = {4,5,6}` (a chain). `|A \ σ(A)| = 1` exactly when `0` lands
> at position `≥ 4`, i.e. in 3 of the 7 extensions, so `Δ₁ = (3/7)/3 = 1/7`.
> Side `A` is `1<2<3` plus isolated `0`; its only balanced pair is `(0,2)` at
> `p = 1/2`. In `P`, `p_{0,2} = 2/7 < 1/3`. **Evicted. No pair survives.**

### 4.3 The mechanism is `n`-free, and the ceiling collapses to `0`

That witness is the `k = 4` member of a family. Let `P(n,k)` be the chain
`c₁<⋯<c_{n−1}` plus one isolated `z`, with `A = {z, c₁,…,c_{k−1}}` (a down-set, so a
legitimate prefix cut) and `B = {c_k,…,c_{n−1}}` (a chain, contributing no pair).
Then, by four one-line arguments:

* `e(P) = n` — `z` may occupy any slot, the chain is forced;
* `p^P(z < c_j) = j/n`, and in the side `p^A(z < c_j) = j/k`, by the same argument;
* `E|A \ σ(A)| = (n−k)/n`, so **`Δ₁ = (n−k) / (n·min(k, n−k))`**;
* `(z,c_j)` is balanced in the side iff `k/3 ≤ j ≤ 2k/3`, and evicted in `P` iff
  `j/n < 1/3` (it cannot exceed `2/3`, since `j/n < j/k`). So **every**
  balanced-in-side pair is evicted as soon as `2k/3 < n/3`, i.e. **`n > 2k`**.

Taking `n = 2k+1` gives `min(k,n−k) = k` and

```
        Δ₁  =  (k+1) / ((2k+1)·k)   →  0     as k → ∞,
```

with every balanced-in-side pair evicted at every `k ≥ 3`. **Therefore**

> **`ε₀(U_either) = 0` in the architecturally required scope. Not bounded by
> `17/78` — refuted at every positive `ε`.**

And since `|A| = k < n−k = |B|`, the **smaller** side is the non-chain one, so the
same family kills the smaller-side reading: **`ε₀(U_smaller) = 0`** as well.

`b6_family.py` verifies this member by member in exact rationals — `k = 3…20`
tabulated, then `k = 30, 50, 100, 200`; the hand formula for `e(P)` and for `Δ₁`
agrees with the library at **every** member; the brute-force `n!` path agrees at
`n ≤ 9`; and `surviving = 0` at every member. At `k = 200`, `Δ₁ = 201/80200 =
0.0025`, with 67 balanced-in-side pairs and none surviving.

### 4.4 What this does and does not damage — stated carefully

**It does NOT touch L4.** `b7_scope_and_arith.py` D1: every family member has
`δ(P) = ⌊n/2⌋/n ≥ 1/3` (`3/7, 4/9, 5/11, 6/13, …, 15/31`), so **L4's disjunct (i)
holds outright** and L4-as-stated is satisfied. What the family refutes is
`mg-3969`'s deliberately **(i)-free** surrogate — which is the right object for the
parent to have built (its §5.1 explains why (i) must be dropped: on a minimal
counterexample it is false by hypothesis), and which is exactly why the surrogate is
refutable. **I did not attempt to prove or refute L4 and I did not do so.**

**It does NOT overturn Claims 6.1 or 6.2 as stated.** Both carry "neither side a
chain" in their hypotheses, and in that population I reproduce `17/78` and `13/111`
exactly. The family always has a chain side, so it never enters that population.

**It DOES break four things:**

1. **§0's verdict-table row for `U_either`** describes the statement as *"the
   `F`-free repaired transfer, **either** side, asserted for **all** posets"* and
   bounds it at `17/78`, **PROVEN**. The statement as worded has `ε₀ = 0`. The
   statement column and the bound column are about different objects.
2. **§0's *"`ε₀` cannot be raised by more than 9 %, ever, at any `n`"*** and the
   surrounding *"the corpus's operative constant is therefore correct to within 9 %
   of a bound that is now proven"*. In the required scope the calibration `0.20` is
   not 9 % under a ceiling; it is `40 %` above `1/7`, and above `0` by everything.
3. **§7's recommendation** — *"`mg-845e` should therefore be released against the
   uniform threshold `ε₀(U_either) ∈ (0, 17/78]`, which is the only one a proof can
   ever produce."* **That interval is empty in the required scope.** This is the
   most consequential of the four, because it is an instruction to `pm-onethird`
   about how to re-word a gate.
4. **§7's `ε_dem` sandwich and §10's proposed `STATE.md` text.** `ε_dem ≤ 289/12168
   = 0.0238` becomes, at the `n ≤ 7` ONE+ ceiling, `ε_dem ≤ (1/7)²/2 = 1/98 =
   0.0102` — so the corpus's `2×10⁻²` would sit at `1.96×` a proven ceiling rather
   than `1.19×` under one — and with the family, `≤ 0`. §10's text carries `17/78`
   and *"under 9 % of headroom and no more"* with **no scope qualifier at all**, and
   §10 is the text proposed for landing.

**And it strengthens the parent's own headline.** `mg-3969`'s leading conclusion is
that the consumable `ε₀^cons` is unmeasurable and that proving it positive **is** the
conjecture (Claims 5.1–5.2, which I did not re-derive — see §7). It offered
`ε₀^unif` as the honest, refutable replacement target. My finding is that the
replacement target is *itself refuted*. The parent's thesis — that there is no
measurable positive threshold here — comes out sharper, not weaker.

### 4.5 The repair I recommend (not applied — `pm-onethird`'s to land)

> **LANDED BY `mg-5214`, 2026-08-09.** Applied at all four sites named in §4.4 plus both
> findings of §5, in `docs/OneThird-L4-Threshold-eps0-mg-3969.md` — §0 (verdict table now
> carries a population column and a row for the required scope; the "9 %" now names its
> restriction), §5.2/§6.0 (both totals labelled with their populations), §6 (Claims 6.1/6.2
> carry their scope in their own statements; the tie convention is declared), §7 (the
> `ε₀(U_either) ∈ (0, 17/78]` recommendation struck and replaced), §9 (the coverage gap
> recorded as closed) and §10 (proposed `STATE.md` text replaced; the unqualified version kept
> struck). `17/78` and `13/111` are retained everywhere, with their scope. `mg-5214` re-ran
> `b0`, `b4 7`, `b6` and `b7` before editing and reproduced every figure below.
> See `docs/repair-mg-5214-the-ceiling-and-its-population.md`.

Publish `17/78` **with its scope in the same sentence**, and publish the ONE+ result
beside it:

> **`ε₀(U_either) ≤ 17/78 = 0.2179` uniformly in `n`, for cuts at which BOTH sides
> are non-chain** (witness `n = 6`, `mg-3969`; reproduced `mg-d3c7`). **On the full
> architecturally required population — at least one side non-chain, which is what
> Step 6 must survive — the uniform threshold is `0`:** an explicit family (chain
> plus one isolated element, `n = 2k+1`) violates the transfer at
> `Δ₁ = (k+1)/((2k+1)k) → 0` with every balanced-in-side pair evicted (`mg-d3c7`).
> **The uniform reading is therefore refuted, not capped**, and `mg-845e`'s clause
> (a) cannot be re-worded against it. The consumable threshold remains what
> `mg-3969` §5 establishes: unmeasurable, and equivalent to the conjecture.

---

## 5. Two smaller findings, both reconciled exactly

### 5.1 The document prints two different totals for one sweep

`mg-3969` §5.2 reports **604 230** prefix cuts at `n ≤ 7` (and its per-`n` table
`12/117/1424/24115/578562`). §6.0 reports **604 250**, and §6 reports **25 682** at
`n ≤ 6`. A reader will take these for the same sweep; they differ by 20 and 14.

**Reconciled (`b0_selftest.py` C2):** §5.2's A1 counts cuts of **non-chain** posets;
§6's A2 counts cuts of **all** posets. The difference is exactly the chain poset at
each `n`, contributing `n−1` cuts:

```
  n=3..7 chains:  2+3+4+5+6 = 20   ->  604 230 + 20 = 604 250   ✔
  n=3..6 chains:  2+3+4+5   = 14   ->   25 668 + 14 =  25 682   ✔
```

Both numbers are right for their own instrument. **Not a numerical error — a
presentational one**: neither figure is labelled with which population it counts,
and the `604 230` is the one quoted in §10's proposed `STATE.md` text.

### 5.2 Claim 6.2's `n = 6` fallback witness sits at a TIE cut

Claim 6.2 keeps an `n = 6` witness at `Δ₁ = 1/7` — *"unique smaller-side pair
`1/2 → 5/7`"* — as the second-path-certified fallback, and §6.0's table gives `1/7`
as the `n ≤ 6` `U_smaller` ceiling.

**`b3_smaller_probe.py` locates it exactly:** `n = 6`, `k = 3`,
`rel = [0,0,3,2,7,31]`, `e(P) = 7`; side `A` = `{0,1,2}` has pair `(0,1)` at
`1/2 → 3/7` (**survives**); side `B` = `{3,4,5}` has pair `(3,4)` at `1/2 → 5/7`
(**evicted**) — the parent's `1/2 → 5/7`. But **`|A| = |B| = 3`.** There is no
smaller side. Calling `B` "the smaller side" is a designation, not a size fact, and
side `A`'s pair *does* survive.

Under a tie-neutral reading the `n ≤ 6` `U_smaller` ceiling is **`13/74 = 0.17568`**,
not `1/7`:

| tie convention | thinnest `U_smaller` violator, `n ≤ 6` |
|---|---|
| tie ⟹ either side may supply the survivor | `13/74 = 0.175676` |
| tie ⟹ cut out of scope | `13/74 = 0.175676` |
| tie ⟹ a designated side | `1/7 = 0.142857` |

**This is confirmed independently by the failure count.** The one number of the
parent's I could not initially reproduce was its `58 755` `U_smaller` failures at
`n ≤ 7` (I got `58 538`). `b7_scope_and_arith.py` D2 settles it: **`58 755` is
reproduced exactly, and only, under the designated-side convention.** So the
convention is real and consistent throughout the parent's instrument — it is simply
undeclared.

**Impact: none on the headline.** Claim 6.2's operative value `13/111` is at
`n = 7`, `k = 4`, sizes `4` and `3` — genuinely unequal, tie-independent. What is
affected is the `n ≤ 6` fallback and the §6.0 table cell.

---

## 6. What I checked by REPLICATION, not independently

Per the brief's closing instruction, and per `PREDICTIONS.md` §D:

* **The eleven-line span, the `:464–474` range and the `F(ε)n` at `:469`.** Exposure
  H2 handed me all three before I opened anything (a `grep` returned the parent's
  `:28` verbatim). Confirming them is replication and carries no evidential weight.
* **The location of the source file** came from `Op-Form` §1, a restatement. Only
  the *text* is source-read.
* **The relation list of the Claim 6.1 witness** is the parent's. I recomputed every
  property of it, but I did not find that poset independently at `n = 6` — though
  `b2`/`b4` do independently *re-find* `17/78` as the minimum over the whole
  population without using the parent's coordinates, which is the check that matters.
* **The entire framing of "three objects called `ε₀`"** (§2's `ε₀^lit`/`ε₀^cons`/
  `ε₀^unif`) is the parent's taxonomy. I audited the objects; I did not derive the
  taxonomy independently and I have no alternative one to offer.
* **My dispatch prompt printed both of the parent's essay-length commit subjects in
  full**, so I knew "not in the source at all", "three objects", "structurally
  unmeasurable" and "`17/78 = 0.2179`, nine per cent above `0.20`" before I began.
  Every conclusion of mine that agrees with those four is agreement with something I
  was told. What is *not* replication is §3.5 (the search for a thinner violator),
  §4 (the scope finding), §5 (the two reconciliations) and §2.2 (the quantifier
  order derived from the sentence).

---

## 7. What I did NOT do

* **I did not attempt to prove or refute L4**, and §4.4 verifies that my family does
  not accidentally do so: every member satisfies disjunct (i).
* **I did not derive `ε_dem`.** §4.4's `1/98` is the parent's own equation with a
  different input substituted, quoted to size the impact of the scope finding.
* **I did not re-open `C₃`.** `C₃ = 1` appears in this document only inside quotes
  of the parent's §7, with its L2 conditionality intact and spent nowhere.
* **I did not re-derive Claims 5.1 and 5.2** — the vacuity of `ε₀^cons` and its
  equivalence to the conjecture. I read both proofs and believe them; Claim 5.2 is
  four lines and I checked each. But I ran no instrument against A1's 604 230-cut
  vacuity result and did not re-verify "disjunct (i) fired at all 604 230 cuts".
  **My `b4` sweep does corroborate it obliquely** — it found `0` cuts with both sides
  non-chain and *no balanced-in-side pair at all*, across all 604 012 ONE+ cuts —
  but that is a different statement and I do not offer it as a check of A1.
* **I did not run any of the parent's four instruments.** Every number here is from
  `code/eps0_audit_d3c7/`. Where we agree, we agree by two code paths; where the
  parent's `out_*.txt` files disagree with me I would not have noticed, because I
  did not read them.
* **My exhaustive sweeps stop at `n = 7`,** like the parent's. The `ε₀ = 0` result is
  *not* limited by that — it comes from a family with a proof, verified to `k = 200`
  — but the claim "nothing thinner than `1/7` at `n ≤ 7`" is.
* **I did not check `mg-3ce3`, `mg-76b2`, `mg-e35c` F5, `mg-345e` or `Op-Form` §4.2
  against their own sources.** Where the parent cites them I took the citation as
  read. In particular I did not verify that `ε_spec ≤ ½ε_leak²` is correctly derived,
  only that the parent uses it consistently.
* **I did not verify Linial's width-2 theorem** (Remark 5.0), and I did not re-prove
  the width bound.
* **I used prefix cuts of the identity linear extension**, exactly as the parent did,
  and I inherit its §9 caveat that the architecture's cut is a prefix of the
  *distinguished order*, which exists only for counterexamples.
* **I did not edit `STATE.md` or the parent's document.** §4.5's proposed text is
  `pm-onethird`'s to land.
* **I registered no schedule and touched nothing outside `code/eps0_audit_d3c7/` and
  this file.**

---

## 8. My predictions, scored — six of eight LOST

`PREDICTIONS.md`, committed at `b2e5fcd` before anything was opened.

| # | prediction | p | outcome |
|---|---|---|---|
| P1 | the gate did not fire | 0.85 `[FORMALITY]` | **WON** — and the parent checked for the drift itself (`K13`) rather than merely denying it |
| P2 | `mg-3af9`/`mg-c8c6` cited somewhere **load-bearing** | 0.30 `[BET]` | **LOST** — 3 occurrences, all bookkeeping or self-disclosure; §1 and §3 use only the source text and `Δ₁`'s definition |
| P3 | L4's source is `step6.tex` or `step8.tex`, lines `464–474` in one of them | 0.55 `[BET]` | **LOST** — the source is in **neither repository**: a 603-line iCloud file. My sub-bet that `step8.tex`'s band-invariant `(L4)` is one of the "three objects" also **LOST**; the three share the name `ε₀`, not `L4` |
| **P4** | **the negative is a lexical fact standing in for a semantic claim** | **0.45 `[BET]`, principal** | **LOST.** I enumerated all four smallness devices at source per my own guard. The parent enumerates all four, including the two genuinely present (`K3` the `≪1`, `K5` the `F`-domain) — and `K5` is the one I most expected it to miss |
| P5 | `n`-freeness rests on a finite sweep plus informal extrapolation | 0.40 `[BET]` | **LOST** — one witness bounds a sup over a universally-`n`-quantified statement; no extrapolation. My `E3` guard caught me before I published the attack |
| P6 | the "nine per cent" comparison mixes normalisations | 0.30 `[BET]` | **LOST** — both sides are `ε_leak`. **The brief's suggested pair (`ε_spec` vs `ε_c3ca`) was the wrong pair**; the live trap here is the Cheeger **square**, and the parent guards it |
| P7 | `78` and `111` are pair counts, and are different kinds of object | 0.35 `[BET]` | **LOST** — both are `e(P)·min(|A|,|B|)`: `26×3` and `37×3` |
| P8 | "structurally unmeasurable" is an existential over an unexhibitable object | 0.75 `[FORMALITY]` | **WON**, and understated: the parent gives a *two-sided* argument (Claim 5.1 vacuity **and** Claim 5.2 equivalence to the conjecture) |

**My errors, filed in advance, and whether they fired:**

* **E1** (score the negative as defective against the commit subject's compressed
  headline rather than the document's narrower claim) — **did not fire**; I quoted
  §1's own table before scoring P4.
* **E2** (declare a normalisation mismatch from digit-proximity) — **would have
  fired**; my `PREDICTIONS.md` guess that `17/78` lives in `ε_c3ca` because
  `0.218 ≈ 0.167` was **wrong**, and the guard requiring me to locate both
  definitions is what caught it. `ε_leak` is a third normalisation entirely.
* **E3** (attack the sweep for an `n`-freeness proved by argument) — **fired, and
  was caught**; see P5.
* **E4** (read the wrong `L4`) — **did not fire**; the chain is
  `mg-845e` → `mg-3969` → `Op-Form` §1 → source `:464–474`.
* **E5** (treat the ticket's framing as data) — **did not fire**; I did not verify
  the "conflated twice already" claim and did not use it as evidence.
* **E6** (do the forbidden work) — **did not fire on L4 or `C₃`**, and I checked
  explicitly (§4.4) that the family leaves L4 standing. It came closest on `ε_dem`,
  where §4.4 quotes `1/98`; I have marked that as a substitution into the parent's
  equation, not a derivation.

**One defect of my own, caught by a control before publication.** My C7 negative
control on the reading of `σ(A)` was **badly designed**: the two readings are
provably identical on prefix cuts, so it could never have discriminated. Had I not
noticed the `0 disagreements`, I would have shipped a `Δ₁` pipeline with no
sensitivity control at all. I replaced it with C7b (`Φ` vs `Δ₁`, which differs on an
*exactly predicted* set of 698 cuts) and turned C7 into an assertion of the
agreement, which is itself worth having: **the `σ(A)` ambiguity is immaterial on
prefix cuts**, and that retires an objection to both instruments.

---

## 9. Reproduce

```
cd code/eps0_audit_d3c7
python3 b0_selftest.py            # controls; must print SELFTEST PASSED
python3 b1_witness.py             # mg-3969's Claim 6.1 witness, recomputed
python3 b2_sweep.py 6             # exhaustive n<=6, mg-3969's scope
python3 b2_sweep.py 7             # exhaustive n<=7, pruned: no violator under 17/78
python3 b3_smaller_probe.py       # the tie-cut finding behind Claim 6.2's 1/7
python3 b4_fullsweep.py 7         # the coverage gap CLOSED: 17/78 -> 1/7
python3 b5_gapwitness.py          # gap witnesses certified on the n! code path
python3 b6_family.py              # the family: Delta_1 -> 0, eps_0 = 0
python3 b7_scope_and_arith.py     # L4 untouched; 58755 reconciled; all arithmetic
```

Outputs committed as `out_*.txt`. Runtime: `b6` ~2 min, `b4` ~1 min, rest seconds.
