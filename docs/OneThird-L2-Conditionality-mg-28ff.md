# OneThird — `C₃^(III) = 1` IS REACHABLE WITHOUT L2, AND I BUILT TWO ROUTES THAT REACH IT — the sweep is test-vector-generic, so L2's "the optimal vector happens to be monotone" becomes "a monotone vector happens to be near-optimal", which is a SCALAR inequality and not a structural one; **BOTH ROUTES CERTIFY `C₃ = 1` AT 4377 OF 4377 PRIMITIVE POSETS `n ≤ 6`, INCLUDING ALL 3340 WHERE L2 FAILS**; and **BOTH CONSTANTS RISE WITH `n` AND SIT AT `0.943` AND `0.812` AT `n = 6`, SO NEITHER MAY BE EXTRAPOLATED TO THE `n ≥ 99` THE CHAIN CONSUMES** — while the *truth* they are chasing rises far more slowly (`0.125 → 0.328`, differences `.097, .049, .037, .019`), which says the phenomenon is stable and **the sweep is what degrades**

**Work item:** `mg-28ff` — filed as the residual of `mg-845e`.
**Branch taken:** **(C)**, named deliberately at the top of `PREDICTIONS.md` before any
computation, because the ticket asks for it to be named and records that this disjunct
shape has paid twice on this lineage.

---

## §0.0 REPAIRS LANDED AFTER `mg-29fe`'s INDEPENDENT AUDIT — NO FIGURE WITHDRAWN

`mg-29fe` audited this document and **confirmed the affirmative half against four
falsification arms** (T1 48318/48318, T2 65396/65396, T3 21120/21120 with a mutation control
that fires at 260 pairs, T4 36116/36116). It proposed repairs and landed none of them; they
are landed here by `mg-b58d`. **Nothing below is a withdrawal.** Every figure in this
document stands. What was wrong was three *labels*, one *diagnosis*, one over-claim, one
**under**-claim, and one prose-versus-theorem mismatch.

| # | site | what was wrong | now |
|---|---|---|---|
| **1** | §4.3 summary | *"100 % at every **enumerated** `n`"* read a **sample** as an enumeration, and is **false of the truth** — the exhaustive `n = 7` (`mg-51f4`) has (F) failing at **168 of 86278** primitive posets | §4.3 |
| **2** | §8.1 item 3 | the document's **own scope self-audit** was false at **2 of its 3** `n = 7` rows | §8.1 |
| **3** | §4.2 | its `n = 7` population is a **different sample** from §4.1's and §4.3's — 90 drawn (40 primitive) versus 200 drawn (106 primitive) — and that was unstated | §4.1–§4.3 |
| **4** | §4.5 bullet 3 | the whole rise was attributed to the Cheeger sweep; the **monotone-cone price `ρ`** was never named, and route (F) contains **no sweep at all** | §4.5 |
| **5** | §2 | *"both are load-bearing **and I measured it**"* — R5 measures **one** of the two steps | §2, §7 R5 |
| **6** | §2 | **an UNDER-claim, and the larger error:** dropping **both** steps leaves `c = ρ`, so the route collapses back onto L2 exactly, failing from **`n = 4`** | §2, §7 R5 |
| **7** | §2, §4.2 | **(M♯)** as stated dropped the second branch its own **theorem** carries; the **code** always had it | §2, §4.2 |

**THE COMMIT SUBJECT IS IN THE PERMANENT GIT RECORD AND CANNOT BE EDITED.** `cb496e9` says
*"(F) certifies at 100% of primitive posets at **EVERY n = 2..7**"*, **unqualified**. That
sentence is false of the truth at `n = 7` and this document is the only place it can be
corrected. Anyone reading the subject line must read §4.3 here before quoting it.

**The repair was checked against the defect it repairs.** This is a labelling repair, so it
can carry a labelling defect. The check, run rather than asserted: every `n = 7` figure
written below carries, **in its own sentence or cell**, (a) the word `sample` or
`EXHAUSTIVE`, (b) the **size and provenance** of that population, and (c) for samples, *not
a maximum*. §8.1 item 3 now states which rows carry which, and is itself the thing repair 2
found wrong — so it is stated as a checkable list, not as a blanket assurance.

---

## §0. THE STATE OF THE CONDITIONALITY AFTER THIS TICKET

| | status |
|---|---|
| **L2 itself** | **OPEN. NOT TOUCHED.** I did not prove it, did not refute it, and did not try. |
| **`C₃^(III) = 1` at `n ≤ 6`** | **TRUE, and now PROVED WITHOUT L2** at 4377 of 4377 primitive posets, by two independent L2-free routes with exact rational certificates. It is true with a factor of **3.05** to spare: the smallest `c` that works is `0.327508`, not `1`. |
| **`C₃^(III) = 1` uniformly in `n`** | **STILL CONDITIONAL — and not on L2 any more.** It is now conditional on either of two *scalar* hypotheses, (M♯) or (F) below, each of which I verified exhaustively to `n = 6` and neither of which I can extrapolate, because **both route constants are rising and are within 6 % and 19 % of failure at `n = 6`.** **POST-LANDING (`mg-51f4`, exhaustive `n = 7`): the extrapolation was right and both hypotheses are now FALSE at `n = 7` individually** — `c♯ = 1.018707`, `f* = 1.297074`. **Their DISJUNCTION survives at 86278 of 86278**, and that is the object §8's diagram places under `C₃ = 1`. See §0's note and §4.5a. |
| **The `n` the architecture consumes** | `n ≥ 99` (`mg-76b2` §6, chain (I)/(III) at `C₃ = 1`). **My exhaustive evidence stops at `n = 6` and my `n = 7` evidence is a sample.** Nothing here touches the operating range, and I say so before anyone quotes a number out of it. |

**The one-sentence version.** L2 is a statement about the *order structure* of an
eigenvector, and nothing in the corpus was ever going to move it; what the theorem
actually needs is a *scalar* comparison between two Rayleigh quotients, and that is a
target a computation can attack — which is what makes this a different ticket from the
one that sat dead for two days.

**What may not be quoted without its scope.** `c_true = 0.327508`, `c♯ = 0.943151` and
`f* = 0.811654` are maxima over the **exhaustively enumerated primitive posets on at most
6 elements**. They are not bounds in `n`. Every one of them is **rising** in `n`. The
`n = 7` figures in this document come from named families plus a deterministic sample of
90–200 posets out of a population of order 10⁶, so **the `n = 7` rows are not maxima and
must never be read as if they were.** (This document was written after `roadmap.md` was
struck the same day for carrying `17/78` without its scope; the lesson is the reason this
paragraph exists.)

> **AND THE SAMPLE HAS SINCE BEEN MEASURED AGAINST THE TRUTH, WHICH IS WHY THAT PARAGRAPH
> WAS NOT DECORATION.** `mg-51f4` enumerated **all 96428 naturally labelled posets on `[7]`,
> 86278 of them primitive** (`code/sweep_loss_51f4/out_s3_n7.txt`) — the first genuine
> `n = 7` maximum in this lineage. Against the samples used here:
>
> | `n = 7`, primitive | this document (**SAMPLE**) | `mg-51f4` (**EXHAUSTIVE**, 86278) |
> |---|---|---|
> | `c_true` | `0.176145` *(106-poset sample)* | **`0.340719`** |
> | `c♯` | `0.850074` *(40-poset sample)* | **`1.018707`** — over `1` |
> | `f*` | `0.832530` *(106-poset sample)* | **`1.297074`** — over `1` |
>
> **The sample understated `c_true` by 1.93×, and it understated BOTH route constants across
> the `1` boundary.** Three consequences, and they do not all point the same way:
>
> 1. **The blanket labelling in this paragraph and in §10 was right, and by a wide margin.**
> 2. **It makes the three labelling defects of §0.0 material rather than cosmetic** — a
>    reader who took §4.3's old *"every enumerated `n`"* at face value would have concluded
>    route (F) certifies at every `n ≤ 7`. It does not: it **fails at 168 of 86278**. That is
>    the `17/78` failure mode one population over, now **demonstrated rather than feared**.
> 3. **The thesis of §4.1 and §4.5 survives its first test beyond its own evidence.**
>    `c_true(7) = 0.340719` is an increment of `+0.013211` after `+0.019169` — **still
>    strictly decreasing.** The *"differences are shrinking"* reading is confirmed at an `n`
>    the document never reached.
>
> **And the disjunction is untouched at `n = 7`:** the two failure sets are **disjoint**, so
> `min(c♯, f*) ≤ 1` at **86278 of 86278** — which is the object §8's dependency diagram
> actually places under `C₃ = 1`, and which §4.5 does not carry.

---

## §1. WHERE L2 ACTUALLY ENTERS, AND THE QUANTIFIER THAT MOVES

`mg-76b2` §3 proves `C₃^(III) = 1` from L2 in three lemmas:

* **Lemma 3.1** — sweep a vector `v` attaining `1 − λ_std`; some level set `S` of `v` with
  `|S| ≤ n/2` has `Φ_P(S) ≤ √(2(1−λ_std))`.
* **Lemma 3.2** — `Φ_P` is a function of the cut, so a suffix delivers its complementary
  prefix at the same number.
* **Lemma 3.3** — *if `v` is monotone along `e`, its level sets are prefixes and suffixes.*

**L2 is used at Lemma 3.3 and nowhere else.** Read Lemma 3.1's proof and the minimality of
`v` appears exactly once, at `R(g) ≤ R(v) = 1−λ_std`; every other step — the median shift,
the `g₊/g₋` split, the mediant inequality, Cauchy–Schwarz, the co-area formula — is
indifferent to where the vector came from. **The sweep is test-vector-generic.**

So the hypothesis can be moved across the quantifier:

> L2 asks that **the optimal vector happen to be monotone**.
> All the theorem needs is that **some monotone vector happen to be near-optimal**.

The second is *not* implied by the first being false, and it is not a structural statement
at all: it is a comparison of two numbers. That is the whole content of this ticket.

*(Disclosed, not laundered: I read `mg-76b2` §3 in full before writing `PREDICTIONS.md`,
so the observation above is a **reading**, not a blind prediction. It is tagged
`[FORMALITY]` there as P1 and I am not going to present it as a guess.)*

---

## §2. THE THEOREM — L2-FREE, AND SHARPER THAN THE ONE IT REPLACES

> **THEOREM (L2-free sweep).** *Let `P` be a poset with distinguished linear extension `e`,
> let `Δ_P = maxᵢ (1 − (S_P)ᵢᵢ) ≤ 1`, and let `g ⊥ 1` be **any** vector that is monotone
> along `e`, with Rayleigh quotient `R(g) = ⟨g,(I−S_P)g⟩/‖g‖²`. Then*
> $$\Phi^{*}_{\mathrm{pref}}(P)^{2}\;\le\;R(g)\,\bigl(2\Delta_P-R(g)\bigr)\qquad\text{when }R(g)\le\Delta_P,\qquad \le\;\Delta_P^{2}\ \text{ otherwise.}$$

**Proof.** Verbatim `mg-76b2` Lemma 3.1, with `v` replaced by `g` and two steps that the
parent had available and did not take.

Let `m` be a median of `g`, chosen so `|{g>m}| ≤ n/2` and `|{g<m}| ≤ n/2`. Energy is
shift-invariant and `‖g−m‖² = ‖g‖² + nm² ≥ ‖g‖²`, so `R(g−m) ≤ R(g)`. Split
`g−m = (g−m)₊ − (g−m)₋`; edgewise `(a₊−b₊)² + (a₋−b₋)² ≤ (a−b)²` and the two squared norms
add, so by the mediant inequality one of them, call it `h`, has `R(h) ≤ R(g)`. `h ≥ 0` and
`|supp(h)| ≤ n/2`. Now

$$\sum_{\{i,j\}}a_{ij}\bigl|h_i^2-h_j^2\bigr|\;\le\;E(h)^{1/2}\Bigl(\sum_{\{i,j\}}a_{ij}(h_i+h_j)^2\Bigr)^{1/2},$$

and — **this is the first of the two steps** — the right-hand factor is not merely bounded,
it is an identity:
`Σ a_ij (h_i+h_j)² = 2 Σ_i d_i h_i² − E(h) ≤ 2Δ_P‖h‖² − E(h)`, where `d_i = 1 − (S_P)_ii`
is the degree, **and the second step is keeping `Δ_P` where the parent wrote `1`.** The
co-area formula on the level sets of `h²` then gives

$$\min_t \Phi_P(\{h^2>t\})\;\le\;\frac{\sum a_{ij}|h_i^2-h_j^2|}{\|h\|^2}\;\le\;\sqrt{R(h)\bigl(2\Delta_P-R(h)\bigr)}.$$

Every `{h² > t}` is a level set of `h`, hence of `g`; `g` is monotone, so by
`mg-76b2` Lemma 3.3 each is a prefix or a suffix, and by its Lemma 3.2 a suffix delivers
its complementary prefix at the same `Φ`. Finally `t ↦ t(2Δ−t)` increases on `[0,Δ]` and
`R(h) ≤ R(g)`, which gives the two cases as stated. ∎

**Both extra steps are free.** `mg-76b2` bounds `Σ a_ij(h_i+h_j)² ≤ 2Σ d_i h_i² ≤ 2‖h‖²`,
discarding `−E(h)` (call keeping it **S2**) and rounding `d_i` up to 1 (call keeping `Δ_P`
**S1**).

> **THEY ARE LOAD-BEARING VERY UNEQUALLY, AND R5 MEASURES ONLY ONE OF THEM.** *(Repairs 5
> and 6, from `mg-29fe` §6; the 2×2 is that audit's, computed exactly by copositivity
> bisection, `code/l2_audit_29fe/out_s3_counterfactual.txt`. An earlier version of this
> paragraph read "both are load-bearing **and I measured it**", which is measured for one of
> the two.)*
>
> Two steps make **four** bounds, and each has a closed form in `ρ = μ_pref/(1−λ_std)`,
> `Δ_P` and the gap, so the 2×2 is exactly computable. Failure counts over **exhaustively
> enumerated primitive posets**, a poset scored FAIL only when the *lower* bracket end
> already exceeds `1`:
>
> | | S1 (`d_i ≤ Δ_P`) | S2 (evaluate `−E(h)`) | constant | `n=4` | `n=5` | `n=6` | max at `n=6` |
> |---|---|---|---|---|---|---|---|
> | **V11** — §2 as it stands | ✔ | ✔ | `ρΔ_P − ρ²(1−λ)/2` | 0 | 0 | **0** | `0.943151` |
> | **V10** — ***the cell R5 tests*** | ✔ | ✖ | `ρΔ_P` | 0 | **6** | **192** | `1.156724` |
> | **V01** — ***the cell nobody ran*** | ✖ | ✔ | `ρ − ρ²(1−λ)/2` | 0 | **0** | **1** | `1.028754` |
> | **V00** — mg-76b2's own form | ✖ | ✖ | **`ρ`** | **10** | **166** | **3164** | `1.217605` |
>
> * **THE OVER-CLAIM (repair 5).** R5 **keeps `Δ_P`** and discards only `−E(h)`, so it is the
>   **V10** cell: it establishes that **S2** is load-bearing (`6 of 275` at `n = 5`, `192 of
>   4070` at `n = 6`) and says **nothing whatever about S1**. The untested cell **V01** —
>   keep `−E(h)`, discard `Δ_P` — has **0 failures at `n ≤ 5`** and first fails at `n = 6`, at
>   **1 poset of 4070**. So "both are load-bearing" is **true**, and true only from `n = 6`;
>   at the `n = 5` where the old sentence made its claim **S1 is not load-bearing at all**;
>   and the two are unequal by **two orders of magnitude** (`192` versus `1`). The repair is
>   one clause, not a retraction: **the cited evidence cannot support the S1 half.**
> * **THE UNDER-CLAIM (repair 6), AND IT IS THE LARGER ERROR — THIS DOCUMENT UNDERSTATED ITS
>   OWN STRONGEST RESULT.** **`V00 = ρ` exactly.** So `mg-76b2`'s un-sharpened sweep, applied
>   to a monotone vector, certifies `C₃ = 1` at a poset **if and only if `ρ ≤ 1`, i.e. if and
>   only if L2's first disjunct holds there** — and the measurement confirms it exactly:
>   V00's failure counts `0, 0, 10, 166, 3164` **equal the L2-failure counts at every `n`**
>   and sum to **3340**, this document's own census figure (§5). **WITHOUT THE TWO STEPS THE
>   QUANTIFIER MOVE BUYS NOTHING AT ALL — the L2-free route collapses back onto L2 itself.**
>   That is a far stronger justification for the two steps than *"the constant exceeds 1 at
>   `n = 5`"*, and it moves the first failure from `n = 5` to **`n = 4`**.

**Machine check of the theorem itself, against brute force.** `selftest28ff` A12:
`Φ*_pref² ≤ R(g)(2Δ_P − R(g))` at **10464 (poset, monotone-vector) pairs**, `Φ*_pref`
computed by exhaustive minimisation over prefixes and `R(g)` in exact `Fraction`s, **0
exceptions**. This is the arm that would catch the theorem being wrong, and it is the
reason the rest of the document is worth reading.

### The hypothesis that replaces L2

Writing `μ_pref = min{ R(g) : g ⊥ 1, g monotone along e }` — a minimum over a cone, not
over a subspace — the theorem gives `C₃^(III) = 1` whenever

> **(M♯)  `μ_pref (2Δ_P − μ_pref) ≤ 2(1 − λ_std)` when `μ_pref ≤ Δ_P`,
> and `Δ_P² ≤ 2(1 − λ_std)` when `μ_pref > Δ_P`.**

> **REPAIR 7 — THE SECOND BRANCH WAS IN THE CODE AND NOT IN THE PROSE.** *(`mg-29fe` §6.1.)*
> The theorem above has **two** cases; (M♯) and §4.2's `c♯` were written with **one**. Since
> `t ↦ t(2Δ−t)` **decreases** for `t > Δ`, the one-case form **understates** what the theorem
> delivers when `μ_pref > Δ_P` — there the truth is `Δ_P²` and `μ(2Δ−μ) < Δ_P²` — so **the
> one-case (M♯) could hold at a poset where the theorem does not deliver `C₃ = 1`.** As a
> *stated* sufficient condition that is unsound in that regime, and it is repaired above.
> **It moves no published number and it never touched the instrument.** `mg-29fe` re-ran the
> whole `n ≤ 6` sweep with the branch restored (`code/l2_audit_29fe/out_s5_branch.txt`):
> `μ_pref > Δ_P` at exactly **one poset per `n`**, and the branched maximum differs from the
> one-case maximum **only at `n = 2`**. At `n = 3..6` both give `0.500000, 0.636846,
> 0.803289, 0.943151` — §4.2's published column exactly. And §4.2's `c♯(2) = 0.125000` **is**
> the branched value, i.e. **`lib28ff.py` implemented the branch this prose omitted.** A
> prose repair, not a withdrawal. *(`mg-29fe` found it by shipping the same defect: its own
> `s3` implemented (M♯) exactly as stated here, one case, and printed `c♯(2) = 0.000000`.)*

**(M♯) is implied by L2's first disjunct** (which gives `μ_pref = 1−λ_std`, whence the left
side is `(2Δ_P − μ_pref)(1−λ_std) ≤ 2(1−λ_std)`), **and is strictly weaker**: it holds at
posets where no dominant standard eigenvector is monotone, which is exactly the population
`mg-94c3`'s red drill isolated. It is a comparison of two rational numbers.

**The cone is a computable object, and that is the point.** In the basis
`ψ_k(i) = k/n − 1[i<k]` — which spans `1^⊥` — the monotone cone is *exactly* `{Σ c_k ψ_k :
c ≥ 0}`, and the pencil has closed forms verified against their definitions at all 5230
posets (`selftest` A4):

$$Q_{k\ell}=\sum_{i<\min(k,\ell)}\ \sum_{j\ge\max(k,\ell)}a_{ij},\qquad N_{k\ell}=\min(k,\ell)-\tfrac{k\ell}{n},\qquad Q_{kk}=\mathrm{leak}(A_k).$$

`Q_kk = leak(A_k)` is a hard control, not a remark: the diagonal of the energy form in this
basis *is* the prefix leak, so a defect in either object shows up as a mismatch.

---

## §3. A SECOND ROUTE WITH NO EIGENVECTOR IN IT AT ALL — THE FOOTRULE

> **IDENTITY (exact, unconditional).**
> $$\sum_{k=1}^{n-1}\mathrm{leak}(A_k)\;=\;\tfrac12\,\mathbb E\Bigl[\sum_i |i-\mathrm{pos}(i)|\Bigr]$$
> *— the prefix leaks sum to half the expected **Spearman footrule** between `e` and a
> uniform random linear extension.*

*Proof.* `leak(A_k) = E #{i : i < k ≤ pos(i)}`, so
`Σ_k leak(A_k) = E Σ_i #{k : i < k ≤ pos(i)} = E Σ_i max(0, pos(i)−i) = ½ E Σ_i |pos(i)−i|`,
the last step because `Σ_i (pos(i)−i) = 0` for every permutation. ∎
**Machine-checked at all 5230 posets `n ≤ 6` and 98 at `n = 7`, exactly, 0 exceptions**
(`selftest` A10, `b1`); and the mutated constant `1/3` is satisfied by **0** posets with a
nonzero footrule (`selftest` C2), so the identity is not an artefact of a loose check.

Since `min_k a_k/b_k ≤ (Σa_k)/(Σb_k)` and `Σ_{k=1}^{n-1} min(k,n−k) = ⌊n²/4⌋`:

> **COROLLARY (the linear co-area bound, unconditional).**
> $$\Phi^{*}_{\mathrm{pref}}\;\le\;\frac{\mathbb E[D_F]}{2\lfloor n^2/4\rfloor}.$$

Hence `C₃^(III) = 1` whenever

> **(F)  `E[D_F]² ≤ 8⌊n²/4⌋²(1 − λ_std)`.**

**There is no eigenvector on the left-hand side of (F) at all** — no monotonicity, no
eigenspace, no degeneracy policy. It compares an expected permutation distance with a
spectral gap. That is a different kind of object from L2 and it is the reason this route is
worth having even though it is weaker than (M♯) in the measurements below.

**Its known failure was filed before it was run.** `PREDICTIONS.md` P10 records, with its
reason, that (F) must fail on every decomposable non-chain: there `1−λ_std = 0`, so the
right side is `0` while `E[D_F] > 0`. `b1` confirms exactly that — on decomposable posets
the route certifies precisely the chains, `1` per `n`. **(F) is a statement about primitive
posets and must be quoted as one.** The architecture's Step 1 reduces to primitive posets,
so this costs nothing; saying it out loud costs nothing either.

---

## §4. THE MEASUREMENT

Population: **every poset on `{0,…,n−1}` for which the identity is a linear extension**,
`n = 2..6` — 5230 posets, of which **4377 primitive** and 853 decomposable. `n = 7` is named
families plus a deterministic sample (no `random` module; a fixed LCG) — **and it is TWO
different draws, not one: `sample_posets(7, 90)` (40 primitive) feeds §4.2, and
`sample_posets(7, 200)` (106 primitive) feeds §4.1 and §4.3.** Both are reproducible; neither
is a maximum. *(Repair 3 — this sentence previously said "a deterministic sample", singular.)*
Every exhaustive `n = 7` row below is `mg-51f4`'s population of **86278 primitive posets**,
attributed as such, and was **not** computed by this instrument.

Every verdict below is **EXACT**. `r ≤ 1−λ_std` is decided without ever computing an
eigenvalue, as positive semidefiniteness of `(I−S_P) − r(I−J/n)`, and PSD of a rational
symmetric matrix is decided by the signs of its characteristic polynomial's coefficients
(Faddeev–LeVerrier). Floats appear only in the *search* for candidate vectors; every
candidate is rationalised and re-verified exactly before it is believed.

### 4.1 The target holds, and it holds with a factor of 3 to spare

| | `n≤6`, all 5230 posets |
|---|---|
| `Φ*_pref² ≤ 2(1−λ_std)` | **5230 / 5230**, EXACT |

This reproduces `mg-94c3`'s red drill on a code path sharing nothing with it, and it is
tagged `[FORMALITY]` in `PREDICTIONS.md` P12 because **the ticket body told me the answer
before I started**. What is *not* a reproduction is how much room there is:

> **`c_true(n) = max Φ*_pref² / (2(1−λ_std))` over primitive posets — the smallest `C₃^(III)`
> that is TRUE at that `n`, route-independent. EXACT bracket by bisection on the PSD test.**
>
> | `n` | primitive | `c_true` | Δ from previous |
> |---|---|---|---|
> | 2 | 1 | `0.125000` | — |
> | 3 | 4 | `0.222222` | `+0.0972` |
> | 4 | 27 | `0.271353` | `+0.0491` |
> | 5 | 275 | `0.308339` | `+0.0370` |
> | 6 | **4070** | **`0.327508`** | `+0.0192` |
> | 7 | 106 primitive of **200 drawn** *(SAMPLE — NOT a maximum; `b5_trend.py:48`)* | `0.176145` | — |
> | 7 | **86278 — EXHAUSTIVE** *(`mg-51f4`, not this instrument)* | **`0.340719`** | `+0.0132` |

`C₃ = 1` is not marginally true on this population; it is true by a factor of `3.05`, and
**the differences are shrinking**, which is the signature of a stable phenomenon rather
than one drifting toward failure.

**The `n = 7` sample row understates the truth by 1.93×** — which is why it is carried and
never used, and why it is now printed beside the exhaustive row rather than alone. **The
exhaustive row confirms the shrinking-increment reading rather than breaking it**
(`+0.0192 → +0.0132`); the two `n = 7` rows are two *different* populations and neither may
be substituted for the other. *(Repairs 1 and 3.)*

### 4.2 Route (M♯) — the monotone cone

`c♯(P) = μ_pref(2Δ_P − μ_pref) / (2(1−λ_std))` **when `μ_pref ≤ Δ_P`, and `Δ_P²/(2(1−λ_std))`
otherwise** — the theorem's second branch, which this line previously dropped and
`lib28ff.py` always carried (repair 7, §2). `c♯ ≤ 1` at a poset means (M♯) holds there.

| `n` | primitive | `c♯` (FLOAT — a MEASUREMENT, see §6) |
|---|---|---|
| 2 | 1 | `0.125000` |
| 3 | 4 | `0.500000` |
| 4 | 27 | `0.636846` |
| 5 | 275 | `0.803289` |
| 6 | **4070** | **`0.943151`** |
| 7 | 40 primitive of **90 drawn** *(SAMPLE — NOT a maximum; `b2_census.py:138`)* | `0.850074` |
| 7 | **86278 — EXHAUSTIVE** *(`mg-51f4`, not this instrument)* | **`1.018707` — over `1`** |

> **REPAIR 3 — THIS `n = 7` ROW IS A DIFFERENT SAMPLE FROM §4.1's AND §4.3's, AND THAT WAS
> UNSTATED.** `b2_census.py:138` draws `sample_posets(7, 90)`, of which **40 are primitive**;
> `b1_footrule.py:73` and `b5_trend.py:48` draw `sample_posets(7, 200)`, of which **106 are
> primitive**. All three rows were labelled `(sample)` and all three are samples — they are
> simply **not the same sample**, so the three `n = 7` rows of §4.1, §4.2 and §4.3 are
> **three sections over two populations** and were never comparable row-wise. Both draws are
> deterministic (a fixed LCG, no `random` module), so both are reproducible; neither is a
> maximum. *(`mg-29fe` §4 defect 3.)*
>
> **And the exhaustive row is the reason this matters rather than being tidiness:** the
> 40-poset sample reads `0.850074`, the truth is `1.018707`, so **the sample sits on the safe
> side of a boundary the truth is on the wrong side of.** Route (M♯) **fails** at `n = 7`.

**EXACT certificate ladder, pooled over all 4377 primitive posets `n ≤ 6`** — for each `c`,
the number at which a *rational* monotone `g` was exhibited and verified to satisfy
`R(g)(2Δ_P−R(g)) ≤ 2c(1−λ_std)`:

| `c` | certified |
|---|---|
| `1/2` | 29 / 4377 |
| `3/4` | 3435 / 4377 |
| `9/10` | 4372 / 4377 |
| **`1`** | **4377 / 4377** ← `C₃ = 1`, with no L2 |
| `3/2`, `2` | 4377 / 4377 |

**This is the affirmative answer to branch (C), and this table is its whole content.**
`C₃^(III) = 1` is derived at every primitive poset `n ≤ 6` — including all **3340** where
L2's first disjunct fails — from a theorem plus an exhibited rational vector, with no
appeal to L2 anywhere.

### 4.3 Route (F) — the footrule

| `n` | primitive | certified at | `f*` = worst `[E[D_F]/(2⌊n²/4⌋)]²/(2(1−λ_std))`, EXACT |
|---|---|---|---|
| 2 | 1 | 1 / 1 | `0.125000` |
| 3 | 4 | 4 / 4 | `0.250000` |
| 4 | 27 | 27 / 27 | `0.306250` |
| 5 | 275 | 275 / 275 | `0.550750` |
| 6 | **4070** | **4070 / 4070** | **`0.811654`** |
| 7 | 106 primitive of **200 drawn** *(SAMPLE — NOT a maximum; `b1_footrule.py:73`)* | 106 / 106 | `0.832530` |
| 7 | **86278 — EXHAUSTIVE** *(`mg-51f4`, not this instrument)* | **86110 / 86278 — FAILS AT 168** | **`1.297074` — over `1`** |

> ### REPAIR 1 — THE SENTENCE THAT STOOD HERE READ A SAMPLE AS AN ENUMERATION, AND IT IS FALSE OF THE TRUTH
>
> **It read:** *"100 % at every **enumerated** `n`, with no eigenvector on the left."* The
> `n = 7` row directly above it is **sampled, not enumerated**, and the exhaustive `n = 7`
> population settles it the wrong way: **route (F) fails at 168 of 86278 primitive posets**
> (`code/sweep_loss_51f4/out_s3_n7.txt`), with `f* = 1.297074` at the extremal — two
> antichains `{0,1,2}`, `{3,4,5,6}`, all `a < b` except `(2,3)`, independently re-verified to
> every digit by `mg-29fe` on a third instrument.
>
> **It now reads:** *"**100 % at every exhaustively enumerated `n` — that is, `n ≤ 6` — and
> at all 106 primitive members of the 200-poset `n = 7` sample. At `n = 7` exhaustively the
> route FAILS, at 168 of 86278.**" With no eigenvector on the left, which is unaffected.*
>
> **THE COMMIT SUBJECT OF `cb496e9` CANNOT BE REPAIRED.** It says *"(F) certifies at 100% of
> primitive posets at **EVERY n = 2..7**"* — unqualified, in the permanent git record. This
> paragraph is the only correction that can exist. **This is the `17/78` shape one population
> over: a maximum over a sample published as a maximum over an `n`.**

**With no eigenvector on the left** — that part of the old sentence is untouched and is what
route (F) was worth having for.

> **A PRECISION NOTE ON THIS TABLE'S `f*` COLUMN, IN THE CONSERVATIVE DIRECTION.** *(`mg-29fe`
> §6.5 R7 — landed here because this table is being repaired anyway; it withdraws nothing.)*
> The column is headed `EXACT`, and the bracket **is** exact, but it is only `3.8e-6` wide:
> `b1_footrule.py:77` bisects **20 steps over `[0,4]`**, and the instrument printed **five**
> decimals where six are shown here. Bracketed to `1.8e-12`, the true values are
> **`0.550747`** and **`0.811649`** (independently confirmed by `mg-51f4`). The figures
> printed above are the **upper** bracket ends, so they **over**-state the route's constant —
> they err toward over-stating the danger, never under-stating it, and `19 %` of headroom is
> `19 %` either way. The point of the note is that `c_true`'s neighbouring column really is
> tight to six decimals and this one is not, so the two read as equally resolved when they
> are not.

### 4.4 The explicit vectors, ranked (`b3`)

How many primitive posets each *named* construction certifies `C₃ = 1` at, EXACTLY:

| construction | `n = 5` | `n = 6` |
|---|---|---|
| `g_pos` — the centred position vector, knows nothing about `P` | 205 / 275 | 2590 / 4070 |
| `g_sort` — the monotone **rearrangement** of a dominant standard eigenvector | 275 / 275 | **4029 / 4070** |
| `g_cone` — the cone minimiser | 275 / 275 | **4070 / 4070** |

`g_sort` is the natural repair of L2 — *sort the eigenvector that refused to be monotone* —
and it very nearly suffices on its own. A closed form worth recording, verified exactly at
all 5230 posets:

$$R(g_{\mathrm{pos}})\;=\;\frac{6\,\mathbb E\bigl[\sum_i (i-\mathrm{pos}(i))^2\bigr]}{n(n^2-1)}\;=\;1-\mathbb E[\rho_{\text{Spearman}}],$$

so the cheapest possible test vector's Rayleigh quotient *is* one minus the expected
Spearman rank correlation between `e` and a uniform random linear extension.

### 4.5 THE FINDING THAT MATTERS MOST, AND IT IS A NEGATIVE

Put the three columns side by side:

| `n` | `c_true` (the truth) | `c♯` (cone route) | `f*` (footrule route) |
|---|---|---|---|
| 3 | `0.222` | `0.500` | `0.250` |
| 4 | `0.271` | `0.637` | `0.306` |
| 5 | `0.308` | `0.803` | `0.551` |
| 6 | **`0.328`** | **`0.943`** | **`0.812`** |

**The truth is nearly flat and its increments are shrinking; both of my routes are climbing
fast toward the `1` they must stay under.** At `n = 6` the cone route has 6 % of headroom
left and the footrule route 19 %. Simple extrapolation of either puts it through `1` within
a step or two of `n = 7`, and **the architecture consumes `n ≥ 99`**.

So the honest statement of what this ticket produced is:

* **`C₃^(III) = 1` needs no L2 at `n ≤ 6`.** That is proved, exhaustively, exactly, at
  4377 of 4377 primitive posets.
* **`C₃^(III) = 1` uniformly in `n` is NOT established by either route**, and the evidence
  I gathered is evidence *against* either route being the one that establishes it — not
  because they fail, but because the *slack they consume grows while the slack available
  does not*.
* The diagnosis is specific and it is not "L2 is needed after all": `c_true` is stable, so
  the difficulty is **not** in the phenomenon. **It is in TWO places, and they behave
  differently** — see the repair immediately below, which replaces the single-cause
  sentence that stood here.

### 4.5a REPAIR 4 — THE DIAGNOSIS. THE SWEEP IS CAPPED BELOW `1` FOREVER; THE CHANNEL THAT CAN KILL THE ROUTE IS THE MONOTONE-CONE PRICE, WHICH THIS SECTION NEVER NAMED

**The sentence that stood in bullet 3 above** — *"It is in the **Cheeger sweep as an
instrument** — the square root and the Cauchy–Schwarz throw away a factor that grows with
`n`. Anyone attacking this next should attack the sweep, not the poset."* — **is a true
measurement and a wrong diagnosis.** `mg-29fe` §3; the algebra is an identity and needs no
computation.

**The algebra.** Write **`ρ = μ_pref/(1−λ_std) ≥ 1`** — the **price of the quantifier move**,
how far the best *monotone* vector is from the true optimum. **`ρ = 1` is exactly L2's first
disjunct.** Substituting `μ_pref = ρ(1−λ_std)` into `c♯` and cancelling gives an **identity**:

$$c^{\sharp}\;=\;\rho\,\Delta_P\;-\;\frac{\rho^{2}(1-\lambda_{\mathrm{std}})}{2},\qquad\text{and since }\Delta_P\le 1,\qquad c^{\sharp}\;\le\;\rho\,\Delta_P\;\le\;\rho.$$

`Δ_P = max_i(1 − (S_P)_ii) = max_i Pr[pos(i) ≠ i] ≤ 1` is a **probability complement**, so
the bound is unconditional. Two consequences follow with **no computation at all**:

> **(A) If `ρ = 1` then `c♯ = Δ_P − (1−λ_std)/2 < 1` at every poset and every `n`.** The
> sharpened sweep, **fed an optimal vector, cannot reach `1`.** Not at `n = 7`, not at
> `n = 99`, not ever. *(Consequence (A) is `mg-51f4`'s, filed pre-run at `01c206f`,
> `20:24:09Z`, 33 minutes before `mg-29fe`'s mail. Priority recorded where it is due.)*
>
> **(B) Therefore `c♯ > 1` REQUIRES `ρ > 1/Δ_P > 1`.** The **only** channel through which
> route (M♯) can fail is the **monotone-cone relaxation**.

**The measurement that separates the two.** `c_sweepL2 := Δ_P − (1−λ_std)/2` is this route's
constant **with the cone price switched off**; it is fully exact and needs no cone
minimisation. Maxima over **exhaustively enumerated primitive posets `n ≤ 6`**
(`code/l2_audit_29fe/out_s1_truth_and_sweep.txt`):

| `n` | `c_true` (truth) | **`c_sweepL2`** — THE SWEEP ALONE | `max Δ_P` | `c♯` (this document) |
|---|---|---|---|---|
| 3 | `0.222222` | `0.500000` | `0.666667` | `0.500000` |
| 4 | `0.271353` | `0.636846` | `0.833333` | `0.636846` |
| 5 | `0.308339` | `0.752421` | `0.900000` | `0.803289` |
| 6 | `0.327508` | **`0.825114`** | `0.950000` | **`0.943151`** |

**Read column-wise, not row-wise.** At `n = 3` and `n = 4` the sweep-alone column **equals
`c♯` to six decimals** — **there this document's diagnosis is exactly right, and that is why
it was believable.** At `n = 5` and `n = 6` they **separate**, and the separation is the cone
price: measured at `c♯`'s **own argmax** (not by differencing two maxima attained at
different posets — that error was made and corrected by `mg-51f4`), the price is **14.1 % at
`n = 6`**. The sweep column is **bounded by `Δ_P < 1` forever**; the cone column is bounded
by nothing. **This section's own urgency argument — *"simple extrapolation of either puts it
through `1`"* — is an extrapolation of the term the sentence did not name.**

**And it is confirmed at the witness.** The exhaustive `n = 7` (M♯) failure has
`ρ = 1.221325` against `1/Δ_P = 1.055556`, so **`ρ > 1/Δ_P`** — the route dies through the
cone price exactly as (B) requires. A route that died through the sweep alone would
contradict the identity.

**ROUTE (F) CONTAINS NO CHEEGER SWEEP AT ALL, SO A SINGLE CAUSE CANNOT COVER THIS SECTION'S
OWN TWO COLUMNS.** *(`mg-29fe` §3.4.)* Route (F)'s bound is the **linear co-area/footrule**
inequality of §3 — `min_k a_k/b_k ≤ Σa/Σb` — with **no Cauchy–Schwarz, no square root of a
Rayleigh quotient and no eigenvector**, as §3 says twice. Whatever makes `f*` climb
`0.125 → 0.812` therefore **cannot** be the Cheeger sweep. `mg-51f4` puts a floor on the
asymmetry: (F) obeys `f* ≥ ρ_n²γ/2` with `ρ_n = (n²−1)/(6⌊n²/4⌋) → 2/3`, **a floor that
vanishes with `γ` instead of rising toward `1`**. So (M♯) carries a floor climbing toward
`Δ_P` and (F) carries **none**: the two routes **do not share a degrading factor at all.**

> **SO THE DIAGNOSIS SHOULD READ:** the sweep's loss grows but is **provably capped below `1`
> at every `n`**; what decides whether route (M♯) survives is **`ρ`, the price of the
> quantifier move — precisely the quantity L2 sets to `1`.** That is sharper and **less
> comfortable** than the sentence it replaces, because it says the new route's failure
> channel is the **same quantity the old hypothesis controlled**: the move buys a
> *relaxation* of L2 (`ρ ≲ 1/Δ_P` rather than `ρ = 1`), **not an escape from it**.
> **A successor must measure `ρ`. Attacking the sweep lowers the constant but cannot save
> the route.**

**One thing this section overstates about its own object.** (M♯) and (F) are each
*separately* sufficient, so what the architecture consumes is `min(c♯, f*)`, not either
column. Exactly: `c_or(n) = 0.125000, 0.250000, 0.306250, 0.550747, 0.753639` at `n = 2..6`
— **strictly below both published columns** — and at the exhaustive `n = 7` the two failure
sets are **disjoint**, so the disjunction survives at **86278 of 86278**. *"Both of my routes
are climbing fast toward the `1` they must stay under"* is true of each column separately and
**overstates the danger to the disjunction**, which is what §8's dependency diagram actually
places under `C₃ = 1`. §8 gets this right; this section's presentation did not carry it.

---

## §5. THE L2 CENSUS, AND A RECONCILIATION OF THE TWO PARENTS' NUMBERS

`μ_pref = 1−λ_std` **is** L2's first disjunct: it says the top standard eigenspace meets the
monotone cone, which is the existential form L2 is written in. Computing it as a cone
minimum resolves degenerate eigenspaces by construction rather than by policy.

| | count |
|---|---|
| all posets `n ≤ 6` | 5230 |
| exhibiting L2's first disjunct | **1890** = **1037** primitive + 853 decomposable |
| primitive | 4377 |
| primitive where L2 **fails** | **3340** |
| **degenerate top standard eigenspace** | **163 — and all 163 exhibit L2** |

* **1890 and 1037 are `mg-76b2`'s numbers exactly**, reached on an instrument that shares
  no code with it. `PREDICTIONS.md` P13 bet 0.60 on 1890 and **wins**.
* **3340 is the ticket's own number exactly.**
* **`1890 − 1727 = 163`, and there are exactly 163 degenerate cases, all of them
  L2-exhibiting.** That is a complete reconciliation of `mg-76b2` with `mg-94c3`: the
  auditor's conservative 1727 plus the 163 top eigenspaces its policy declines is the
  parent's 1890, and the disagreement was never about a fact — it was about whether an
  existential wording licenses an existential search. It does; L2 says *"a* dominant
  standard eigenvector".
* **One discrepancy I record and do NOT adjudicate.** `mg-94c3` §3 reports **1032**
  primitive posets exhibiting L2; I count **1037**, as does `mg-76b2`'s own machine
  corroboration ("1037 of 1037"). Five posets. I have no basis for saying which convention
  produces which number without opening `libA94.py`, which I deliberately did not do, and
  a five-poset difference changes nothing in this document — every table above is keyed on
  4377 and 3340, not on 1037. **Whoever owns those two documents should close it; it is not
  mine to close and I am not going to guess.**

---

## §6. TWO DIRECTIONS, TWO EPISTEMIC STATUSES

`PREDICTIONS.md` E7 filed the risk that I would sell a maximum over an enumerated
population as a bound. The guard, honoured:

* **The certificate direction is a theorem at each poset.** "There *is* a monotone `g` with
  `R(g)(2Δ_P−R(g)) ≤ 2c(1−λ_std)`" is witnessed by an exhibited rational vector and decided
  by an exact PSD test. §4.2's ladder and §4.3's counts are of this kind.
* **The extremal direction is a MEASUREMENT.** "`c♯` cannot be lowered" rests on a float
  minimisation over the cone (support enumeration plus a float generalized eigenproblem),
  and is labelled FLOAT wherever it appears. `c_true` and `f*` are the exceptions: those
  are exact brackets by bisection on the PSD test, with no float in the decision at all.

---

## §7. CANDIDATES RULED OUT (`b4`)

The ticket: *"If you answer in the negative on any branch, ENUMERATE THE CANDIDATES YOU
RULED OUT."* My answer is affirmative-but-conditional, which owes the same debt.

| | candidate | verdict |
|---|---|---|
| **R1** | *the prefix minimises `leak` among sets of its own size* — would make plain Cheeger transport to prefixes for free, killing L2 outright | **FALSE at 5111 of 5230.** Smallest witness: `n = 3`, `0 < 1`; at size 2 the prefix `{0,1}` leaks `2/3` while `{1,2}` leaks `1/3`. |
| **R2** | *`Φ*_pref = Φ*`* | **FALSE at 468 of 5230** — independently reproducing `mg-76b2`'s 468. The prefix restriction really can cost something. |
| **R3** | *the position vector is a dominant standard eigenvector* — would make L2 automatic | **FALSE at 4371 of 4377 primitive.** |
| **R4** | *the monotone rearrangement `g_sort` suffices* | **NOT ruled out — measured.** 4029/4070 at `n = 6`; it fails at 41. |
| **R5** | *(M♯) with `mg-76b2`'s un-sharpened `2Δ_P R(g)`* | **FAILS from `n = 5`** (6 of 275). The discarded Cauchy–Schwarz factor (**S2**) is load-bearing, which is why §2 keeps it. **SCOPE, per repair 5: this row keeps `Δ_P`, so it is the V10 cell and it measures S2 ONLY.** Discarding `Δ_P` instead (V01) first fails at `n = 6`, at **1 of 4070**; discarding **both** (V00) gives `c = ρ` and fails from `n = 4` at `10, 166, 3164` — **the L2-failure counts themselves**. See §2. |
| **R6** | *the footrule route without restricting to primitive* | **FAILS at every decomposable non-chain**, for the reason filed in P10 *before* the run. |
| **R7** | *is the verdict pipeline vacuous?* | **NO — RED DRILL FIRES.** On a synthetic 6-vertex weighted graph whose only thin cut is not a prefix (clusters `{0,3}` and `{1,2,4,5}`, weak bridge), the target **FAILS** at bridge weights `1/200` and `1/1000` and holds at `1/10` and `1/40`. The machinery can print FAIL and does. |

Two things I did **not** attempt and say so rather than leaving them ambiguous: **L2's
second disjunct** ("or directly produce a low-conductance prefix") is untouched, and
**chain (II)'s gap-form `C₃`** is taken from `mg-94c3` as read — it exceeds 1 at 1023 of
1032 and rises, I did not re-derive it, and nothing in this document is about it.

---

## §8. WHAT THIS BUYS `mg-845e`'s SUCCESSOR

`ε_dem = ε₀²/(2C₃)` (Op-Form §4.2 / `mg-76b2` §6 row (III)). The chain reduced today to
`ε_dem = ε₀²/2`, which is `C₃ = 1`, which was conditional on L2 with **no live ticket
attacking L2** — the shape that killed `mg-845e` for two days.

After this ticket the dependency is:

```
   BEFORE:  eps_dem = eps_0^2 / 2   <=   C_3 = 1   <=   L2   <=   (nothing in the corpus)

   AFTER:   eps_dem = eps_0^2 / 2   <=   C_3 = 1   <=   L2                        [unchanged, still open]
                                                   <=   (M#)  scalar, exhaustive to n=6
                                                   <=   (F)   scalar, no eigenvector, exhaustive to n=6
```

**The conditionality is no longer a single point of failure and it is no longer structural.**
Three independent sufficient hypotheses now sit under `C₃ = 1`, two of them scalar
inequalities that a computation can attack at any `n` a computation can reach.

**And the honest limit, stated where it cannot be separated from the gain:** all three are
open at the `n ≥ 99` the chain consumes, my exhaustive evidence stops at `n = 6`, and the
two new hypotheses have measured headroom of 6 % and 19 % at `n = 6` **and falling**. If a
successor is filed against exactly one of (M♯) and (F), it will be the same mistake
`mg-845e` recorded — a driver for one clause of a gate and not the other. The successor
this ticket wants is against **what §4.5 shows the degradation to be**, and it would serve
both.

> **AMENDED BY REPAIR 4.** This sentence originally read *"against **the sweep's loss**,
> because §4.5 shows that is where the degradation lives"*. §4.5a shows the sweep's loss is
> **capped below `1` at every `n`** and cannot by itself kill either route, so a successor
> filed against the sweep alone would be filed against the one channel that provably cannot
> fail. **For route (M♯) the target is `ρ`, the price of the quantifier move**; route (F)
> contains no sweep at all and needs its own. What serves both is a driver against the
> **disjunction** `min(c♯, f*)` — whose exact values (`0.125000 … 0.753639` at `n ≤ 6`, and
> **86278/86278 surviving** at the exhaustive `n = 7`) sit strictly below either column. That
> is the object this diagram places under `C₃ = 1`, and it is the one to file against.

### 8.1 THE REMEDY IS AN ARTEFACT OF THE SAME KIND AS THE DEFECT, SO I CHECKED IT AGAINST THE DEFECT

The defect this ticket exists to repair is *"a conditionality with nothing in the corpus
that would ever move it — dead, not waiting."* My remedy is **two more conditionalities**.
So the remedy is exactly the kind of thing that can carry the defect, and the enumeration
is owed:

1. **Is (M♯) movable in a way L2 was not?** **Yes, and that is the whole justification for
   the ticket.** L2 is a structural claim about an eigenvector's order; nothing computable
   advances it, which is why it sat with no ticket in any status. (M♯) and (F) are scalar
   inequalities between quantities any enumeration computes exactly. `n = 7` exhaustive is
   reachable with more compute than I had; `n = 8` with better enumeration. **A hypothesis
   a bigger sweep can falsify is not the same object as one nothing can touch** — and
   §4.5 is itself an instance of moving them, since it is evidence about their fate
   gathered inside a single ticket. Nothing comparable was ever produced about L2.

   > **THIS ITEM IS THE ONE THAT AGED BEST, AND IT AGED WITHIN THE DAY.** `n = 7` exhaustive
   > was not merely *reachable* — `mg-51f4` **ran it**, all 96428 posets (86278 primitive),
   > and **both hypotheses were falsified there**: `c♯ = 1.018707` and `f* = 1.297074`. That
   > is the claim of this item discharged in the only way that counts — a hypothesis a bigger
   > sweep could falsify was falsified by a bigger sweep, days after being filed, which is
   > exactly what could never have happened to L2. **The two conditionalities were the right
   > kind of object; both are now known false at `n = 7` individually, and their
   > DISJUNCTION — the thing §8's diagram actually places under `C₃ = 1` — survives at
   > 86278 of 86278.**
2. **Could the residual be lost on the way out, as `mg-845e`'s nearly was?** That is a
   routing failure, not a mathematical one, and it is handled as the ticket instructs: the
   verdict goes to `pm-onethird` **before** the branch is submitted, not after.
3. **Could a number here be quoted without its scope — the defect struck from
   `roadmap.md` the same day?** Every constant carries `n ≤ 6` and `primitive` in its own
   sentence, and §0 says so before any table. `17/78` appears nowhere, and `ε₀` appears
   **only as the symbol** in §8's chain relation `ε_dem = ε₀²/(2C₃)` — never carrying a
   value. *(This sentence originally read "`ε₀` and `17/78` appear nowhere", which is false
   of §8 and is the exact over-claim this document is about; corrected before commit.)*

   > **REPAIR 2 — THIS ITEM'S OWN SCOPE SELF-AUDIT WAS FALSE AT 2 OF ITS 3 ROWS, AND THAT IS
   > WORSE THAN THE DEFECT IT WAS WRITTEN TO CATCH.** It asserted: *"every `n = 7` row is
   > labelled **sample, not a maximum** at each appearance."* **It was not.** Only §4.1's row
   > carried *"NOT a maximum"*; §4.2's and §4.3's carried `(sample)` **alone**. So **the check
   > written to prevent the `17/78` defect was itself inaccurate about its own document** —
   > the §8.1 pattern applied to §8.1, and precisely the failure mode of writing a self-audit
   > and then letting its **existence** stand in for its **correctness**.
   >
   > **Repaired at the rows, not only here.** §4.1, §4.2 and §4.3 now each carry, per
   > `n = 7` row: the word **SAMPLE**, **NOT a maximum**, the **draw size and primitive
   > count**, and the **file:line that produced it** — and each is printed beside the
   > **EXHAUSTIVE** `mg-51f4` row, which is labelled as another instrument's. The two draws
   > are different (90 and 200; repair 3), which this item also failed to notice.
   >
   > **This item is now a checkable list rather than a blanket assurance**, because a blanket
   > assurance is exactly what was false. The current state, verifiable by reading the three
   > tables:
   >
   > | row | `SAMPLE` | `NOT a maximum` | draw / primitive | provenance |
   > |---|---|---|---|---|
   > | §4.1 `c_true(7)` | ✔ | ✔ | 200 / 106 | `b5_trend.py:48` |
   > | §4.2 `c♯(7)` | ✔ | ✔ | **90 / 40** | `b2_census.py:138` |
   > | §4.3 `f*(7)` | ✔ | ✔ | 200 / 106 | `b1_footrule.py:73` |
   >
   > **And the defect was material, not cosmetic**: the exhaustive `n = 7` has both route
   > constants **over `1`** and route (F) failing at **168 of 86278** (§0, §4.3).
4. **Could I have replaced one open lemma with a strictly harder pair?** No, but the gain
   is narrower than it looks: (M♯) and (F) are each *sufficient*, so `C₃ = 1` now rests on
   **three** independent routes instead of one and no single failure is fatal. That is
   strictly better than the position before this ticket. It is **not** the same thing as
   progress toward a proof, which §4.5 says is unlikely along either new route.

---

## §9. PREDICTIONS SCORED

`PREDICTIONS.md` was committed at `8c28781`, before one line of `lib28ff.py` existed.

| | bet | outcome |
|---|---|---|
| P1 | Lemma 3.1 is test-vector-generic; `Δ_P` is a free sharpening | **[FORMALITY]** — a reading, disclosed as such. Held, and the `Δ_P` sharpening turned out necessary (R5). |
| P2 | the `ψ` pencil's closed forms, `Q_kk = leak(A_k)` | **HELD**, 5230 posets, 0 exceptions — a hard control, not a bet |
| P3 (0.95) | the footrule identity | **HELD** exactly, 5230 + 98 posets |
| **P4 (0.25)** | **`c* ≤ 1` — my principal live bet** | **WON, and only because of a sharpening I had not yet written when I filed it.** With the form I actually had in mind at filing time (`Δ_P·μ_pref ≤ 1−λ_std`) `c*` is **1.027 at `n = 5`** and the bet **loses**; with the Cauchy–Schwarz factor recovered, `c♯ = 0.943` at `n = 6` and it wins. **I am scoring this as a loss on the reasoning and a win on the number**, because the reason I put it at 0.25 — "`Δ_P` sits near 1, so (M) demands `μ_pref ≈ 1−λ_std`" — was correct, and what rescued it was not the population being kind but my instrument getting better mid-ticket. |
| P5 (0.55) | `c* ≤ 2` | **HELD** |
| P6 (0.80) | `c* ≤ 4` | **HELD** |
| **P7 (0.50)** | the extremal poset has a non-trivial automorphism, *i.e. the extremal case is a degenerate top eigenspace case* | **LOST on the object it named, and its stated mechanism is REFUTED.** `c♯`'s argmax at `n=6` — `[(0,1),(0,2),(0,4),(0,5),(1,2),(1,5),(3,4),(3,5),(4,5)]` — has `|Aut| = 1`. The prediction holds only for `c_true`, whose argmax at `n = 4, 5, 6` is a disjoint pair of equal chains with `|Aut| = 2` every time. And the *reason* I gave is wrong at **both** extremals: each has a **1-dimensional** top standard eigenspace (`1−λ_std = 0.236288` and `0.381670`), so symmetry is not acting through degeneracy here. I named the mechanism in advance precisely so I could not rationalise it afterwards, and it did not survive. |
| **P8 (0.65)** | **`c♯` rises from `n=5` to `n=6`** | **HELD — and it is the finding of §4.5.** It rises at *every* step, `0.125 → 0.50 → 0.637 → 0.803 → 0.943`, and so does `f*`. I bet on this and it is the reason the headline carries a negative. |
| **P9 (0.45)** | `g_pos` fails at a **majority** of the L2-failing primitive posets | **LOST.** At `n = 6` `g_pos` certifies 2590 of 4070 — it fails at 1480, well under half of the ≈3170 L2-failing posets there. The cheapest possible test vector does better than I gave it credit for. |
| P10 (0.95) | the footrule route fails on decomposable posets, *for the stated reason* | **HELD**, exactly as reasoned in advance |
| P11 (0.35) | route (F) fails somewhere on primitive posets too | **SCORED LOST HERE ON A SAMPLE, AND IT IS WON ON THE TRUTH.** It read *"LOST. 100 % at every `n ≤ 7` tested"* — the same sample-read-as-enumeration as §4.3 (repair 1), one row over. Correctly: **LOST at every exhaustively enumerated `n` (`n ≤ 6`) and across the 106-poset `n = 7` sample; WON at `n = 7` exhaustively, where (F) fails at 168 of 86278 primitive posets** (`mg-51f4`). A live bet at 0.35 that I recorded as lost was in fact **right**, and I could not see it because I was scoring against a sample. |
| P12 | the target holds at all 5230 | **[FORMALITY]** — pre-answered by the ticket body; reproduced |
| P13 (0.60) | my L2 count lands on **1890**, not 1727 | **HELD**, and §5 reconciles the two parents exactly |
| P14 | "the prefix minimises leak at its size" is false | **[FORMALITY]**; smallest witness exhibited |

**Three live bets lost or half-lost (P4's reasoning, P9, P11), and the one I most wanted to
lose — P8 — held.**

### Errors of my own, caught by the guards that were filed for them

* **E3 fired for real, twice.** `psd_exact` shipped with a **sign error** in
  Faddeev–LeVerrier (`e_k = (−1)^{k+1} c_k`; I stored `c_k`). Arm A6, five hand cases, caught
  it before a single verdict was printed — a PSD test that answers `False` on the identity
  matrix would have made every certificate in this document meaningless. And A7's first
  form asserted a bracket agreement to `1e-8` against a bracket only `6e-8` wide, which is a
  badly designed control that fails for a reason that has nothing to do with the claim;
  replaced by "the float eigenvalue lies inside the exact bracket", which is the statement I
  actually wanted.
* **E4 fired.** My first non-vacuity control on the target (`drop the factor 2 and it must
  fail`) **did not fail** — `Φ*_pref² ≤ 1·(1−λ_std)` holds at all 5230 posets. The control
  was too weak to discriminate, and rather than deleting it I replaced it with a **ladder**
  (`K = 1/10 … 2`), which discriminates (3484 failures at `K=1/10`, 0 at `K=2/3`) and which
  produced `c_true` — the single most informative number in the document. **A control I had
  to strengthen turned into the finding of §4.5.**
* **E7 honoured**: §6 keeps the two directions apart.
* **A defect of mine that no guard caught and that I am recording anyway:** I ran an
  unanchored-enough `pkill` while my own selftest was running and killed it, then spent a
  cycle reading an empty output file as if the run had produced nothing. Nothing downstream
  depends on it; it cost time, not correctness.

---

## §10. NOT DONE

* **L2 is not proved and not refuted.** Branch (A) and branch (B) are untouched. I did not
  run `mg-94c3`'s red drill's own code, and I did not open `libA94.py`, `lib76b2.py` past
  line 300, or either parent's `out_*.txt`.
* **Nothing here reaches the `n` the architecture consumes.** Exhaustive to `n = 6`; **this
  instrument's** `n = 7` work is named families plus a deterministic sample — **two
  different draws, 90 and 200** (repair 3) — out of ~10⁶ posets, so **no `n = 7` number
  produced by `lib28ff.py` is a maximum**, including the ones that look reassuring.
  **The exhaustive `n = 7` rows now printed in §0, §4.1, §4.2 and §4.3 ARE maxima, and they
  are `mg-51f4`'s, not this instrument's** — they are labelled `EXHAUSTIVE` and attributed at
  every appearance. That distinction is the whole of repairs 1–3 and it is stated here so
  that this bullet cannot be quoted as covering rows it does not cover.
* **(M♯) and (F) are both OPEN.** Verifying a hypothesis exhaustively on a finite population
  is not proving it, and §4.5 is my own evidence that neither is likely to be provable in
  the form given.
* **`μ_pref` is computed by a float search** (support enumeration over the cone's faces plus
  a float generalized eigenproblem). Its *upper* use is certified exactly; its *lower* use —
  the claim that `c♯` cannot be reduced — is a measurement, and a better cone minimiser
  could only lower `c♯`, never raise it. So §4.2's table is an upper bound on the truth in
  the direction that matters and the `c♯` trend of §4.5 is, if anything, pessimistic.
* **The 1032-vs-1037 discrepancy is left open**, deliberately (§5).
* **`ε₀` is out of scope and appears nowhere as a number.** `17/78` does not appear in this
  document at all. Both by design (`PREDICTIONS.md` E5).
* **I edited no other document.** `STATE.md`, `roadmap.md` and the `mg-76b2`/`mg-94c3`
  documents are untouched; §5's reconciliation and §8's dependency diagram are proposals for
  whoever owns those files, not landings.

---

*`mg-28ff`. Instrument: `code/l2_conditionality_28ff/` — `lib28ff.py` written from scratch,
sharing no code with `lib76b2`, `libA94`, `lib_d3c7` or `lib3969`; `selftest28ff.py`
**20/20 arms**, including A12 (the theorem against brute force, 10464 pairs) and seven
negative controls, two of which caught real defects in this instrument before it published.*
