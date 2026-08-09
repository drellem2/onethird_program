# PREDICTIONS — mg-28ff, "L2 IS THE LAST CONDITIONALITY AND NOTHING ATTACKS IT"

Committed **before one line of `lib28ff.py` is written and before any number is computed.**
Everything below is a bet or a disclosure, not a result.

The ticket offers three branches. **I am taking (C) deliberately, and naming it as the
ticket asks me to name it**: *show `C₃ = 1` is reachable WITHOUT L2*. The ticket records
that this disjunct shape has paid twice on this lineage (it unblocked `mg-6bc2`, it
discharged `mg-845e`'s clause (b)); I am not proving L2 (branch A) and I do not expect to
refute it (branch B), and I say so at the top rather than after failing at them.

---

## H — EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

I read the following **before** writing this file. Every prediction whose answer is already
contained in what I read is tagged **[FORMALITY]** and is a *reproduction*, not a test.

* **H1. The dispatch body pre-answered the central empirical question.** It states verbatim
  that `mg-94c3` ran a red drill in which **3340 NON-monotone primitive posets** exist and
  `Φ*_pref ≤ √(2(1−λ_std))` **holds at all of them**. So "does the target inequality hold
  where L2 fails, at `n ≤ 6`?" is a question I already know the answer to. Any finding of
  mine that it holds is a REPRODUCTION on an independent code path, and I will label it
  that way rather than presenting it as discovery.
* **H2.** The dispatch also printed `C₃^gap ∈ {1.500, 1.473, 1.990, 2.386}` and "exceeds 1
  at 1023 of those same 1032", and `C₃^cut > 1` at 10. Chain (II)'s failure is pre-answered.
* **H3. I read `mg-76b2` §3 in full — Lemmas 3.1/3.2/3.3 and the theorem — before writing
  this file.** So my observation that **Lemma 3.1's proof never uses the minimality of `v`**
  is a *reading*, not a blind prediction. It is the hinge of my whole approach and I am not
  going to pretend I guessed it. Tagged [FORMALITY] wherever it appears.
* **H4.** I read `mg-845e`'s closing note and the mayor's scope warning about `17/78`.
  `ε₀` is **out of scope for this ticket** and no number of mine will be an `ε₀` bound.
* **H5.** I have NOT read `lib76b2.py` past line 300, have NOT opened `libA94.py`,
  `a1_algebra.py`–`a4_census.py`, or any `out_*.txt` of either parent, and will not: my
  instrument is written from scratch so that a shared defect cannot survive both.

---

## THE PLAN, STATED BEFORE IT IS RUN

`mg-76b2`'s theorem is: L2's first disjunct ⟹ the Fiedler sweep lands in the prefix family
⟹ `Φ*_pref ≤ √(2(1−λ_std))` ⟹ `C₃^(III) = 1`. L2 enters at exactly one place: **Lemma 3.3**
(monotone ⟹ prefix). Lemma 3.1 is test-vector-generic.

So I invert the quantifier. Instead of *"the optimal vector happens to be monotone"* I ask
for *"a monotone vector that happens to be near-optimal"*:

> **(M)** `Δ_P · μ_pref ≤ 1 − λ_std`, where `μ_pref = min{ R(g) : g ⊥ 1, g monotone along e }`
> and `Δ_P = max_i (1 − (S_P)_{ii})`.

(M) is implied by L2's first disjunct (which gives `μ_pref = 1−λ_std` and `Δ_P ≤ 1`), is
**strictly weaker**, is **quantitative**, and is **finitely checkable at each `n`**. The
measurement that decides the ticket is

> **`c* := max_P Δ_P · μ_pref / (1 − λ_std)`** over primitive posets.

`c* ≤ 1` ⟹ `C₃^(III) = 1` with no L2 anywhere. `c* = c > 1` ⟹ **`C₃^(III) ≤ c`
unconditionally** — which is still a discharge of the *unquantified*-constant defect even
if it is not a discharge to 1, and feeds `ε_dem = ε_leak²/(2C₃)` directly.

---

## P — PREDICTIONS

### Structural

* **P1 [FORMALITY, H3].** Lemma 3.1's proof uses the minimality of `v` only through
  `R(v) = 1−λ_std`; substituting any `g ⊥ 1` gives `min_t Φ(level set of g) ≤ √(2Δ_P R(g))`,
  and the `Δ_P` is a free sharpening the parent left on the table (its proof writes
  `d_i ≤ 1` where `d_i ≤ Δ_P` is available). Confidence 0.90.
* **P2 [BET, 0.85].** `{ψ_k}` with `ψ_k(i) = k/n − 1[i<k]` is a basis of `1^⊥`, the monotone
  cone is exactly `{Σ c_k ψ_k : c ≥ 0}`, and in that basis `Q_{kl} = ⟨ψ_k,(I−S_P)ψ_l⟩` is a
  **sum of `a_ij` over `i < k∧l ≤ k∨l ≤ j`** with `Q_{kk} = leak(A_k)` exactly, while
  `N_{kl} = min(k,l) − kl/n`. If `Q_{kk} ≠ leak(A_k)` on any poset my algebra is wrong and
  everything downstream is void. **This is a hard control, not a prediction.**
* **P3 [BET, 0.95].** `Σ_{k=1}^{n−1} leak(A_k) = ½·E[Σ_i |i − pos(i)|]` — the prefix leaks
  sum to half the expected **Spearman footrule** between `e` and a uniform random linear
  extension. Exact identity, no L2. (I derived this on paper before writing this file; the
  0.95 is the chance my derivation survives the machine, not the chance it is interesting.)

### The measurement

* **P4 [PRINCIPAL LIVE BET, 0.25].** `c* ≤ 1` — i.e. (M) holds at **every** primitive poset
  at `n ≤ 6`, including all 3340 where L2's first disjunct fails, and branch (C) lands at
  `C₃ = 1`. I put it *low*: `Δ_P` is typically close to 1, so (M) demands `μ_pref ≈ 1−λ_std`,
  which is nearly L2 itself. 3340 chances to fail is a lot of chances.
* **P5 [BET, 0.55].** `c* ≤ 2`.
* **P6 [BET, 0.80].** `c* ≤ 4`.
* **P7 [BET, 0.50].** The poset attaining `c*` has a non-trivial automorphism, i.e. the
  extremal case is a *degenerate top eigenspace* case and not a generic one. Named in
  advance so I cannot rationalise whatever I find.
* **P8 [BET, 0.65].** `c*` **rises** from `n=5` to `n=6`. If it rises, (M) is `n`-dependent
  and the honest headline is a *measurement*, not a uniform constant — and I must say so.

### The explicit routes

* **P9 [BET, 0.45].** The **explicit position vector** `g_pos = (0,1,…,n−1)` centred —
  whose Rayleigh quotient is exactly `1 − E[Spearman ρ]` — fails to certify the target at a
  **majority** of the primitive posets where L2 fails. (It is the cheapest possible monotone
  test vector; if it worked the parents would not have needed L2.)
* **P10 [BET, 0.95, WITH ITS REASON].** The purely combinatorial averaged bound
  `Φ*_pref ≤ E[D_F] / (2⌊n²/4⌋)` (the linear co-area bound, P3's identity divided by
  `Σ_k min(k,n−k) = ⌊n²/4⌋`) **fails** to certify the target on **decomposable** posets, for
  a reason I can state before running it: an ordinal sum has `1−λ_std = 0`, so the target's
  right-hand side is `0`, while `E[D_F] > 0` at every decomposable non-chain. **Therefore
  the footrule route must be restricted to primitive posets before it is even tested** —
  and I am recording that I knew this in advance rather than discovering it as a surprise.
* **P11 [BET, 0.35].** Even restricted to primitive posets the footrule route fails
  somewhere at `n ≤ 6`.

### Reproductions I owe

* **P12 [FORMALITY, H1].** `Φ*_pref² ≤ 2(1−λ_std)` holds at **every** poset `n ≤ 6`, on my
  code path. Reproduction of `mg-94c3`'s red drill.
* **P13 [BET, 0.60].** My count of posets exhibiting L2's first disjunct at `n ≤ 6` will be
  **1890**, matching `mg-76b2`, and not 1727 (`mg-94c3`'s conservative count, which declines
  163 degenerate top eigenspaces). My `μ_pref = 1−λ_std` test resolves degeneracy by
  construction — it asks whether the cone meets the eigenspace, which is L2's own existential
  wording — so it should land on the *existential* number.
* **P14 [FORMALITY, mg-76b2 §3].** "The prefix minimises `leak` among sets of its size" is
  **false**; I will exhibit the smallest explicit witness.

---

## E — ERRORS OF MY OWN, FILED IN ADVANCE WITH THEIR GUARDS

* **E1. Conflating `ε_spec` with `1−λ_std`.** They are not the same object: `1−λ_std` is the
  poset's actual gap, `ε_spec` is the architecture's budget, and the chain only needs
  `1−λ_std ≤ ε_spec`. **Guard:** every verdict is stated against `1−λ_std` and the word
  `ε_spec` appears only when quoting `Op-Form §4.3`.
* **E2. Computing `μ_pref` by an unconstrained eigen and forgetting the cone.** **Guard:**
  every returned `g` is asserted monotone at the point of use, and `R(g) ≥ 1−λ_std` is
  asserted for every `g` I ever build. A single violation means my Rayleigh or my pencil is
  wrong, and the run must abort rather than print.
* **E3. Letting a float decide a verdict.** **Guard:** every published inequality is checked
  in exact `Fraction` arithmetic by a rational PSD test (`r ≤ 1−λ_std` ⟺ `(I−S_P) − r(I−J/n)`
  positive semidefinite, decided by exact characteristic-polynomial coefficient signs).
  Floats may only *find* candidate vectors, never *certify* them. Anything that cannot be
  made exact is printed with the label `FLOAT` at the print site.
* **E4. Reporting "the route certifies at 100%" with no evidence the test can fail.**
  **Guard:** a mutation arm that scales the certificate constant until failures appear, and
  a red drill on a population where the target is known to be false (decomposable posets,
  by P10). A control that cannot fail is not a control.
* **E5. Publishing a number without its scope — the defect that cost this lineage a strike
  on `roadmap.md` today.** **Guard:** `c*` may not be written anywhere without `n ≤ 6` and
  `primitive` in the same sentence. `17/78` and `ε₀` do not appear in my output at all.
* **E6. Selling a weakening as a discharge.** (M) is **unproved**. If `c* ≤ 1` I have
  replaced one open hypothesis with a weaker open hypothesis plus an exhaustive finite
  verification — that is progress and it is not a proof. **Guard:** the headline must carry
  the word "weaker" and the document must state, in its own §0, what is still open.
* **E7. Claiming `c*` is a bound when it is a maximum over an enumerated population.**
  **Guard:** the certificate direction (`∃` monotone `g` with `Δ_P R(g) ≤ c·(1−λ_std)`) is
  exactly certifiable and is a theorem at each poset; the extremal direction ("`c*` cannot be
  lowered") rests on a cone minimisation I compute in float, and must be labelled a
  MEASUREMENT, not a lower bound.

---

*Filed by `mg-28ff` before any computation. Scored in `README.md` §P after the run.*
