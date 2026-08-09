# OneThird — `C₃^(III) = 1` IS REACHABLE WITHOUT L2, AND I BUILT TWO ROUTES THAT REACH IT — the sweep is test-vector-generic, so L2's "the optimal vector happens to be monotone" becomes "a monotone vector happens to be near-optimal", which is a SCALAR inequality and not a structural one; **BOTH ROUTES CERTIFY `C₃ = 1` AT 4377 OF 4377 PRIMITIVE POSETS `n ≤ 6`, INCLUDING ALL 3340 WHERE L2 FAILS**; and **BOTH CONSTANTS RISE WITH `n` AND SIT AT `0.943` AND `0.812` AT `n = 6`, SO NEITHER MAY BE EXTRAPOLATED TO THE `n ≥ 99` THE CHAIN CONSUMES** — while the *truth* they are chasing rises far more slowly (`0.125 → 0.328`, differences `.097, .049, .037, .019`), which says the phenomenon is stable and **the sweep is what degrades**

**Work item:** `mg-28ff` — filed as the residual of `mg-845e`.
**Branch taken:** **(C)**, named deliberately at the top of `PREDICTIONS.md` before any
computation, because the ticket asks for it to be named and records that this disjunct
shape has paid twice on this lineage.

---

## §0. THE STATE OF THE CONDITIONALITY AFTER THIS TICKET

| | status |
|---|---|
| **L2 itself** | **OPEN. NOT TOUCHED.** I did not prove it, did not refute it, and did not try. |
| **`C₃^(III) = 1` at `n ≤ 6`** | **TRUE, and now PROVED WITHOUT L2** at 4377 of 4377 primitive posets, by two independent L2-free routes with exact rational certificates. It is true with a factor of **3.05** to spare: the smallest `c` that works is `0.327508`, not `1`. |
| **`C₃^(III) = 1` uniformly in `n`** | **STILL CONDITIONAL — and not on L2 any more.** It is now conditional on either of two *scalar* hypotheses, (M♯) or (F) below, each of which I verified exhaustively to `n = 6` and neither of which I can extrapolate, because **both route constants are rising and are within 6 % and 19 % of failure at `n = 6`.** |
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

**Both extra steps are free and both are load-bearing.** `mg-76b2` bounds
`Σ a_ij(h_i+h_j)² ≤ 2Σ d_i h_i² ≤ 2‖h‖²`, discarding `−E(h)` and rounding `d_i` up to 1.
Without them the route below **fails**: with the un-sharpened `2Δ_P R(g)` form the
constant already exceeds 1 at `n = 5` (6 of 275 primitive posets — `b4` R5).

**Machine check of the theorem itself, against brute force.** `selftest28ff` A12:
`Φ*_pref² ≤ R(g)(2Δ_P − R(g))` at **10464 (poset, monotone-vector) pairs**, `Φ*_pref`
computed by exhaustive minimisation over prefixes and `R(g)` in exact `Fraction`s, **0
exceptions**. This is the arm that would catch the theorem being wrong, and it is the
reason the rest of the document is worth reading.

### The hypothesis that replaces L2

Writing `μ_pref = min{ R(g) : g ⊥ 1, g monotone along e }` — a minimum over a cone, not
over a subspace — the theorem gives `C₃^(III) = 1` whenever

> **(M♯)  `μ_pref (2Δ_P − μ_pref) ≤ 2(1 − λ_std)`.**

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
`n = 2..6` — 5230 posets, of which **4377 primitive** and 853 decomposable. `n = 7` is
named families plus a deterministic sample (no `random` module; a fixed LCG).

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
> | 7 | 106 *(sample — NOT a maximum)* | `0.176145` | — |

`C₃ = 1` is not marginally true on this population; it is true by a factor of `3.05`, and
**the differences are shrinking**, which is the signature of a stable phenomenon rather
than one drifting toward failure.

### 4.2 Route (M♯) — the monotone cone

`c♯(P) = μ_pref(2Δ_P − μ_pref) / (2(1−λ_std))`; `c♯ ≤ 1` at a poset means (M♯) holds there.

| `n` | primitive | `c♯` (FLOAT — a MEASUREMENT, see §6) |
|---|---|---|
| 2 | 1 | `0.125000` |
| 3 | 4 | `0.500000` |
| 4 | 27 | `0.636846` |
| 5 | 275 | `0.803289` |
| 6 | **4070** | **`0.943151`** |
| 7 | 40 *(sample)* | `0.850074` |

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
| 7 | 106 *(sample)* | 106 / 106 | `0.832530` |

**100 % at every enumerated `n`, with no eigenvector on the left.**

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
  the difficulty is **not** in the phenomenon. It is in the **Cheeger sweep as an
  instrument** — the square root and the Cauchy–Schwarz throw away a factor that grows
  with `n`. Anyone attacking this next should attack the sweep, not the poset.

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
| **R5** | *(M♯) with `mg-76b2`'s un-sharpened `2Δ_P R(g)`* | **FAILS from `n = 5`** (6 of 275). The discarded Cauchy–Schwarz factor is load-bearing, which is why §2 keeps it. |
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
this ticket wants is against **the sweep's loss**, because §4.5 shows that is where the
degradation lives, and it would serve both.

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
2. **Could the residual be lost on the way out, as `mg-845e`'s nearly was?** That is a
   routing failure, not a mathematical one, and it is handled as the ticket instructs: the
   verdict goes to `pm-onethird` **before** the branch is submitted, not after.
3. **Could a number here be quoted without its scope — the defect struck from
   `roadmap.md` the same day?** Every constant carries `n ≤ 6` and `primitive` in its own
   sentence, §0 says so before any table, and every `n = 7` row is labelled *sample, not a
   maximum* at each appearance. `17/78` appears nowhere, and `ε₀` appears **only as the
   symbol** in §8's chain relation `ε_dem = ε₀²/(2C₃)` — never carrying a value. *(This
   sentence originally read "`ε₀` and `17/78` appear nowhere", which is false of §8 and is
   the exact over-claim this document is about; corrected before commit.)*
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
| P11 (0.35) | it fails somewhere on primitive posets too | **LOST.** 100 % at every `n ≤ 7` tested. |
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
* **Nothing here reaches the `n` the architecture consumes.** Exhaustive to `n = 6`;
  `n = 7` is named families plus a deterministic sample of 90–200 out of ~10⁶ posets, so
  **no `n = 7` number in this document is a maximum**, including the ones that look
  reassuring.
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
