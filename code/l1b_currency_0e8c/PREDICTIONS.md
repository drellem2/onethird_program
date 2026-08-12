# mg-0e8c — PREDICTIONS, filed before one line of the instrument exists

**THE EXPOSURE IS DISCLOSED RATHER THAN LAUNDERED.** Before writing these I read `STATE.md`
(the L1b blockquote at `:21` and row 8 at `:125`), `docs/OneThird-PairBias-Independence-mg-345e.md`
§2, `docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md` §; `docs/CONCEPTS.md` §4 and
`docs/OneThird-ProofShape-mg-3af8.md` §4. Several answers below are therefore **REPORTS at zero
credit** — I am recording what the corpus already says so that the instrument's agreement with it
cannot later be sold as confirmation. Which is which is marked on every line.

---

## The question

`STATE.md` row 8 states the wall as

> frozen ⟹ `1 − λ_std ≤ ε_spec`, a constant uniform in `n` — in inversion terms **(LIB-const)**
> `E[inv_e] ≤ (ε_spec/6)(n²−1)`

and marks it `OPEN`, while the **same cell** records `ε_sup < 1` as **PROVEN** (`Op-Form`
Claim 6.1, pair-bias, L4-independent). Daniel's challenge: if a uniform constant is already
proven, the stated form is already discharged, and the open content is a **size**, not an
existence.

---

## R — REPORTS (zero credit; I read these before predicting)

- **R1.** `mg-345e` §2 already states, in so many words, that the pair-bias derivation of an
  explicit absolute `ε_spec` uniform in `n` *"already exists, it is already proven, and it lands
  at `1`."* Its dependency list is 5 items and L4 is not among them.
- **R2.** The master bound is `1 − λ_std ≤ 6E[inv_e]/(n²−1)` (`Op-Form:§6.1`, cited at
  `mg-345e:118`). It runs **inversions ⟹ spectrum**, one direction.
- **R3.** `mg-2de0`'s audit already records, at the **antichain**, that the footrule form of the
  master bound equals `1` exactly at every `n` and that *"the spectral chain is already vacuous at
  its FIRST step."* That sentence exists; it has never been connected to row 8's own phrasing.
- **R4.** `ε_dem ≈ 2×10⁻²` and the published gap factor is ~50 (`STATE.md:21`).

## P — LIVE predictions (my own, unmeasured at filing time)

- **P1 (the verdict).** **Daniel is RIGHT.** `ε_sup < 1` discharges row 8's stated form: the
  conjunction of Claim 6.1 and the master bound is a proof of *"frozen ⟹ `1 − λ_std ≤ ε_spec` for
  an explicit absolute constant uniform in `n`"*. Confidence **high** — but it is R1 restated, so
  most of the credit is already spent; what is live is that nobody has drawn the consequence for
  the row's **status**.

- **P2 (the vacuity, and this one is live).** The **spectral** half is not merely
  already-satisfied but **VACUOUS at `ε_spec = 1`**: I predict `λ_std ≥ 0` for **every** poset, so
  `1 − λ_std ≤ 1` holds with **no hypothesis at all**. Mechanism I am betting on: `S_P = (T+Tᵀ)/2`
  is a symmetric doubly-stochastic matrix with non-negative entries, so `M = I − S_P` is a genuine
  weighted-graph Laplacian, and `1 − λ_std = λ₂(M)`; I predict `λ₂(M) ≤ 1` throughout. **I have not
  proven `λ₂(M) ≤ 1` in general and I may be wrong** — the generic Laplacian bound I can write down
  is `λ₂ ≤ n/(n−1) · min_i(1 − T[i][i])`, which permits values slightly **above** 1.
  **Falsifiable:** one poset on `n ≤ 6` with `1 − λ_std > 1` kills it.

- **P3 (the antichain is the maximiser).** `max{1 − λ_std}` over all posets on `n` elements is
  **exactly 1**, attained at the antichain and nowhere strictly exceeded. Live.

- **P4 (the inversion half is NOT vacuous — the two halves come apart).** At `ε_spec = 1` the
  inversion form `E[inv_e] ≤ (n²−1)/6` **fails** at the antichain, where `E[inv_e] = n(n−1)/4`
  (hand-arithmetic: `n=6` gives `7.5 > 5.833`). So the two forms row 8 joins with *"in inversion
  terms"* — and `CONCEPTS.md` §4 joins with the word ***"equivalently"*** — land on **opposite
  sides of vacuity** at the constant that is proven. Live, and it is the sharper half of P2.

- **P5 (the frozen population).** I predict the frozen class `δ(P) < 1/3` is **NON-EMPTY** at
  `n ≤ 6` and consists **only of posets with no incomparable pair at all** — i.e. the chains, for
  which `δ = 0` vacuously — with **zero** posets carrying an incomparable pair and `δ < 1/3`.
  Confidence **medium**; `mg-7c78` predicted the frozen population EMPTY, which is a different
  prediction from mine, and I have not checked which convention it used. **Falsifiable both ways.**

- **P6 (the sites).** Exactly **three** canonical sites state L1b in the existence form:
  `STATE.md:21` (the blockquote), `STATE.md:125` (row 8), `docs/CONCEPTS.md` §4, and
  `docs/OneThird-ProofShape-mg-3af8.md` §4 — that is **four**, and I am predicting four while
  writing "three", so: **four**, and I predict a grep finds **no fifth** in `docs/` outside the
  per-attempt write-ups. Live.

- **P7 (the self-contradiction).** I predict `docs/OneThird-ProofShape-mg-3af8.md` §4 states the
  wall in the existence form and then, **within 20 lines**, states `ε_sup < 1` as **proven** — i.e.
  the document refutes its own statement of the open problem on the same page. Live at filing;
  I have read §4 but not counted the lines.

## What would make me say Daniel is WRONG

Any one of:
- the master bound runs the other way, so Claim 6.1's inversion bound does not reach `1 − λ_std`;
- `ε_sup` is in `ε_c3ca` units (the `1/6` normalisation) and does not convert to `ε_spec` without
  a factor nobody has paid — the ledger's own two-currency warning;
- `Op-Form` Claim 6.1's hypothesis is strictly stronger than `δ(P) < 1/3`.

I predict **none** of the three holds. If any does, the verdict flips and the row stands.
