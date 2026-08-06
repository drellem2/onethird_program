# mg-2de0 — PREDICTIONS for the independent audit of the mg-00b9 direct-prefix route (Lemma A / Lemma B)

**Committed BEFORE any script of this audit exists.** Nothing in `code/direct_prefix_audit_2de0/`
other than this file is present in the commit that carries it. That is the point: the scoring below
is checkable against a revision at which the instrument did not exist.

**Operator scope, declared up front.** Every object below is on the **TRANSPORT axis**:
`λ_std` = top eigenvalue of the symmetrised transport operator `S_P` on `1⊥`; `Φ_P` / `Δ₁` =
transport conductance / L1 ordinal-sum defect; `inv_e`, footrule. **Nothing here is `Δ_AT`, `A(P)`,
or the Hodge axis.** Every claim I score, I first checked which operator it is about.

---

## 0. What I audit, and what I do not

mg-00b9 is analysis-only and landed no edits. It has **no result blob** (`mg show mg-00b9 --json`
→ `.result = null`), so the auditable statement of its claims is the restatement in **mg-2de0's own
body**, which is what I audit. I derive Lemma A and Lemma B **from the definitions**; I do not
check mg-00b9's derivation.

Definitions I take from the corpus (cited, not re-derived):

| object | definition | site |
|---|---|---|
| `A_k` | `{1,…,k}` — the first `k` elements of the reference order `e` | `docs/OneThird-lambda-std-Operative-Form.md:84` |
| `K_k(σ)` | `\|A_k ∖ σ(A_k)\|` | same, `:84`; audit `:227` |
| `Δ₁(A)` | `E\|A ∖ σ(A)\| / min(\|A\|,\|Aᶜ\|)` | `STATE.md:39` |
| footrule `D(σ)` | `Σ_x \|pos_σ(x) − rank_e(x)\|` | `docs/…Operative-Form.md:328` |
| master bound | `1−λ_std ≤ 3E[D]/(n²−1) ≤ 6E[inv]/(n²−1)`, equality at the antichain | `STATE.md:130`, `docs/…Operative-Form.md:320` |
| spectral requirement | `E[inv_e] ≤ (ε_spec/6)(n²−1)` | `docs/…Operative-Form.md:§6.2` |

**Out of scope, and why.** The two claims mg-2de0 asks me to verify *against the source* — the
Cheeger sweep half at `tex:318–324` and the "unless that side is a chain" caveat at `tex:481–483` —
**cannot be resolved from this repo**: it tracks **0** `.tex` files. See disclosure D7.

---

## 1. Disclosures — figures I had ALREADY derived by hand before writing this file

These are **measurements, not predictions.** Filing them as predictions would launder work already
done into foresight. They are listed so that the scored predictions in §2 can be read net of them.

- **D1.** I derived Lemma A independently. It comes out as an **exact per-`σ` identity**, and it is
  **poset-free** — a statement about permutations, in which `P` plays no role at all. The poset
  enters only when `σ` is restricted to `L(P)` to take an expectation.
- **D2.** `Σ_{k=1}^{n−1} min(k, n−k) = ⌊n²/4⌋` by hand: `n²/4` for even `n`, `(n²−1)/4` for **odd**
  `n`. So Lemma B's middle step `Σ_k min(k,n−k) ≥ (1−4β²)n²/4` is **false at `β=0` for every odd
  `n`**, by `1/4`.
- **D3.** I hand-evaluated Lemma B's middle form at the **`n=3` antichain**, `β=0`: truth
  `min_k Δ₁(A_k) = 2/3`; claimed `2E[D]/n² = 16/27 ≈ 0.5926`. The **middle form is false there**.
  The **outer** form `4E[inv]/n² = 2/3` is exactly **tight**, not violated, at the same point.
- **D4.** Antichain closed forms, hand-derived: `E[K_k] = k(n−k)/n`, `Δ₁(A_k) = max(k,n−k)/n`,
  `Σ_k E[K_k] = (n²−1)/6`.
- **D5.** Arithmetic already checked: `3/0.20 = 15`, `3/0.02 = 150`, `√6/2 = 1.2247`,
  `1.2247/√(1/3) = 2.121`.
- **D6.** I had already grepped `STATE.md` at HEAD and found the brief's line numbers stale
  (see P12, P13). The *substance* of both documentary items I had not yet checked.
- **D7.** I had already established that this repo tracks **0** `.tex` files, and that the two
  `.tex` files on this host outside `.pogo` (`~/Documents/onethird.tex`, 364 lines;
  `~/Documents/onethird_annals.tex`, 356 lines) contain **0** occurrences of "Cheeger" and cannot
  carry a line 481. The `tex:` citations therefore point outside the audited repo.

---

## 2. Predictions, scored

Each carries the **population** it is over and the **grain** at which it is measured.

### Lemma A

- **P1.** Lemma A `Σ_{k=1}^{n−1} K_k(σ) = D(σ)/2` holds with **0 exceptions**.
  *Population:* all `n!` permutations for `n = 2..7` (5913 permutations), **plus** every linear
  extension of every poset in the poset population. *Grain:* per-permutation, exact `Fraction`.
- **P2.** `STATE.md:28` (`Σ prefix-violations = footrule ≍ inv`) is **off by a factor of 2** against
  Lemma A under the reading `prefix-violations at k = K_k`, and **correct** under the reading
  `= |A_k Δ σ(A_k)| = 2K_k`. I predict the corpus **pins neither reading**: exactly **1** site in
  the corpus uses the phrase "prefix-violation" (`STATE.md:28`) and it defines nothing.
  *Population:* all tracked `.md`. *Grain:* per-site.

### Lemma B — the three inequalities scored SEPARATELY

Lemma B depends on Lemma A. If P1 fails, B fails with it and I will say so first.

- **P3.** Inequality 1 (mediant + Lemma A),
  `min_{k∈K_β} Δ₁(A_k) ≤ (E[D]/2) / Σ_{k∈K_β} min(k,n−k)`: **0 exceptions**.
  *Population:* every (poset, β) cell. *Grain:* per-cell, exact rational.
- **P4.** Inequality 2, `Σ_{k∈K_β} min(k,n−k) ≥ (1−4β²)n²/4`: **fails**, and not rarely. At `β=0`
  it fails **exactly on the odd `n`** (D2). At `β>0` I predict it fails on a **majority** of cells
  with `βn ∉ ℤ`, because `⌈βn⌉` overshoots by up to 1 at each end and the integral it replaces is
  short by `Θ(βn)`. *Population:* the (n, β) grid. *Grain:* per-cell.
- **P5.** The **composite middle form** `min_k Δ₁(A_k) ≤ 2E[D]/((1−4β²)n²)` is **false on a real
  poset**, i.e. the P4 proof gap is not absorbed downstream. Known witness `n=3` antichain, `β=0`
  (D3). **I predict ≥ 1 further witness with `n ≥ 5`**, at some `β > 0`.
- **P6.** The **outer form** `min_k Δ₁(A_k) ≤ 4E[inv_e]/((1−4β²)n²)` survives at `β=0` on **every**
  poset tested (the Diaconis–Graham slack `D ≤ 2·inv` absorbs the `⌊n²/4⌋` deficit), and I predict
  it **fails** at some `β > 0`, because `(1−4β²)` degrades faster than the DG slack grows.
  **If it does not fail anywhere, that is a stronger positive than mg-00b9 claimed and I will
  report it as such** — this prediction is the instrument that could show the positive.
- **P7.** The **repair** I will propose,
  `min_k Δ₁(A_k) ≤ (E[D]/2)/⌊n²/4⌋ ≤ 2E[D]/(n²−1)` at `β=0`, holds with **0 exceptions**, and
  evaluates to **exactly 2/3** at the antichain for **every** `n ≥ 2` — recovering mg-00b9's
  headline `2/3`, which its own stated `n²` form does **not** attain.

### Non-vacuity (Priority 2)

- **P8.** At the antichain the master bound `3E[D]/(n²−1)` equals **exactly 1** for every `n`, so
  the spectral chain is **already vacuous at its first step, before Cheeger is applied**. Therefore
  attributing the antichain vacuity to the **Cheeger square** is **not supported at that input**;
  `√2 = √(2·1)` is vacuous because its *input* is, not because the square is lossy. The square's
  price is real but must be read off the **requirement** comparison (Priority 3), not the antichain.
- **P9.** `Φ_P(A) ≤ 1` for **every** cut of **every** poset tested, so a bound of `√2 ≈ 1.414` is
  vacuous. And `min_{all cuts} Φ_P ≤ min_{prefixes} Δ₁(A_k)` on every poset tested — so the direct
  route bounds the **harder** (larger) quantity and still gets the better number. The comparison is
  therefore **conservative in the direct route's favour**, i.e. like-for-like or better, not
  inflated. *Population:* all `2^n` cuts of every poset with `n ≤ 7`. *Grain:* per-cut.

### The 3/ε_leak claim (Priority 3)

- **P10.** Both requirements are at the **same `ε_leak`** — but the headline ratio is not the
  general one. The exact ratio is `3(1−4β²)/ε_leak`. The reported **`3/ε_leak` is the `β=0`
  specialisation**, and at `β=0` the lemma's *entire selling point* (a **balanced** prefix,
  item (d)) is switched off. At the `β=1/4` the ticket itself prices, the honest factor is
  **`2.25/ε_leak` = 11.25× at `ε_leak=0.20`, not 15×**. So the headline factor and the balance
  guarantee **cannot both be claimed at once**.
- **P11.** Item (b) (`direct 2μ` vs `Cheeger √(6μ)`, ratio `1.2247/√μ ≥ 2.121` at `μ ≤ 1/3`) is
  **correct at `β=0`** and degrades to `0.9186/√μ` (`≥ 1.59` at `μ = 1/3`) at `β=1/4`.
  **No crossover** in the admissible range either way (`β=1/4` crossover would need `μ > 0.844`).
- **P12 (minor, favourable to spectral).** mg-00b9 renders the spectral requirement with `n²`
  where the corpus has `(n²−1)` (`docs/…Operative-Form.md:§6.2`). Predict the direction: the
  corpus's form is **stricter** than mg-00b9's rendering, so the rendering **understates** the
  spectral requirement — an error against mg-00b9's own conclusion, i.e. harmless to it.

### Documentary (Priority 4) — report only, NO STATE.md edits

- **P13.** The limit-form top-line site set is **five** lines, not three: `:13`, `:21`, `:57`,
  `:62`, `:86`. The brief's **`:56` is off by one** — line 56 is mermaid node **B** ("The BK walk
  mixes badly"), not node C. The brief **omits `:21`** (the Axis-1 bullet) and **omits `:62`** (the
  B→C arrow label, which states the limit form a second time inside the same diagram).
  *Population:* all 386 lines of `STATE.md` at HEAD. *Grain:* per-line.
- **P14.** The C→D arrow is **`:63`**, not `:65`; `:65` is the **E→F** arrow ("a balanced pair
  contradicts δ<1/3"). The **substance** of item 4 is confirmed: `:63` labels the arrow with
  easy/Buser (row 5), which is the **cut ⟹ gap** direction, and the arrow needs
  `(Φ*)²/2 ≤ 1−λ_std`, the **sweep** half, which is in **no** ledger row.
- **P15.** Linial's width-2 theorem, as *used* by item (e), needs a rider mg-00b9 does not carry:
  `δ ≥ 1/3` for width `≤ 2` requires **at least one incomparable pair** (a chain has no `δ`).
  I predict: over **all** posets of width `≤ 2` with `n ≤ 7` that have an incomparable pair,
  `δ ≥ 1/3` holds with **0 exceptions** — an instrument that could have refuted the citation as
  used, on a finite population, without re-proving Linial. And "both sides chains ⟹ width ≤ 2"
  I predict **0 exceptions** over all posets tested that are a union of two chains.

---

## 3. What would make me report a NEGATIVE

If P1 fails on a single permutation, Lemma A is dead and Lemma B with it, and that is the report —
the rest of the arc's re-pricing does not survive it. If P6 fails at `β = 0`, the route's outer
bound is dead as stated and only the repaired form of P7 survives. If P9's second half reverses on
any poset (`min_{cuts} Φ_P > min_k Δ₁(A_k)`), the Priority-2 comparison is **not** conservative and
I withdraw the "favourable" reading of it.

## 4. No prediction filed

I file **no** prediction on whether the Cheeger sweep half `(Φ*)²/2 ≤ 1−λ_std` is true for `S_P`.
I cannot resolve the citation (D7) and I will not guess at a claim whose source I could not open.
