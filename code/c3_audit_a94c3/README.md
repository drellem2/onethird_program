# `c3_audit_a94c3` — mg-94c3's independent audit of mg-76b2

**Work item.** `mg-94c3`. **Audits.**
[`docs/OneThird-C3-PrefixCapture-mg-76b2.md`](../../docs/OneThird-C3-PrefixCapture-mg-76b2.md)
and `code/c3_prefix_capture_76b2/`, as merged at `7b7d093`.
**Deliverable.**
[`docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md`](../../docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md).
**Predictions.** [`PREDICTIONS.md`](PREDICTIONS.md), committed at `e200f18` **before any script
of this instrument existed**.

```
sh run_all.sh          # ~30 s, all sections expected to exit 0
```

## 1. Independence, concretely

`libA94.py` shares **no line** with `lib76b2.py`. It is written from
`spectral_near_ordinal_sum_program.tex` directly:

| object | source line | why it matters here |
|---|---|---|
| `R(σ)e_a = e_{σ(a)}`, `(T_P)_{xa} = Pr[x` at position `a]` | `tex:130–146` | fixes `σ : position → element`, the exact point at which `mg-76b2 §8` reports a live bug in a sibling instrument |
| `S_P = ((T_P+T_Pᵀ)/2)|_H` | `tex:160–163` | |
| `⟨1_A,(I−S_P)1_A⟩ = E|A∖σ(A)|` | `tex:220–227` | checked BOTH ways (matrix, and counting over `L(P)`) — a single path can be wrong the same way twice |
| `Φ_P(A) = E|A∖σ(A)|/|A|`, `Δ₁` | `tex:229–237`, `:270–278` | |

There is **no numpy on this machine**, so the eigen path is a hand-written cyclic Jacobi
solver. That is an accident of the environment and it is the right accident: the two
instruments share no linear-algebra dependency either.

Exact `Fraction` arithmetic for every conductance, Rayleigh quotient and ratio built from
them. Floating point **only** for eigenvalues, and every figure that depends on one is
labelled FLOAT where it is printed.

## 2. Sections

| script | what it does |
|---|---|
| `selftesta94c3.py` | **NC1–NC6, the negative controls.** Every detector shown failing on purpose. |
| `a1_algebra.py` | **The one thing the ticket asks first.** Re-derives `n ≥ 4C₃/ε_leak² − 1` from Op-Form, exact rationals, brute-force search vs closed form at 30 grid points; checks WHICH normalisation each side is in; exhibits invariance under consistent conversion and the ~6× error under a mixed one; re-derives all four chains. |
| `a2_dictionary.py` | Re-derives Lemmas 2.1, 3.1, 3.2, 3.3 from the source and measures each. Scores P1, P2, P3. |
| `a3_currency.py` | The adversarial section: three currencies for `C₃`, measured **restricted to posets that exhibit L2's first disjunct**. Scores P4, P5, P8. |
| `a4_census.py` | The L4 census (verified at `mg-3ce3`'s source, in another repo) and the `mg-200d` census. Scores P6, P7. Re-checks mg-76b2's claim 14 against Op-Form. |

## 3. Scoring

| # | outcome | note |
|---|---|---|
| P1 | **HELD** | 0/25684; factor 2 attained 4812× |
| P2 | **HELD** | 0/4377; worst `Φ²/(2(1−λ_std)) = 0.2813` |
| P3 | **HELD** | 0/6132; red drill 3340/3340 |
| P4 | **HELD** (bet 70%) | `C₃^gap > 1` at 1023 of 1032 posets **that exhibit L2's FIRST DISJUNCT**, worst `2.386`. This is correction `C1`. *(scope added at the claim, `mg-be0b`; this read "that exhibit L2". `L2` is a **disjunction**, so the unqualified form claims a population this instrument never built — its filter is `mono == "YES"`. **No figure moves and nothing is marked false**: `1023 of 1032` was true as measured. The `a3_currency.py` row above already carried the scope and always did.)* |
| P5 | **MISSED** (bet 45%) | 16/16 of §7's figures reproduce — once a defect of *mine* is removed (§4 below) |
| P6 | **HELD** (bet 80%) | and verified at `mg-3ce3`'s predicate, not against mg-76b2's scope statement |
| P7 | **HELD** (bet 75%) | 1 of 24 claims falls; 6 machine-bare sites all read as labelled by hand |
| P8 | **HELD** (bet 65%) | chain-(III) constant is `1` at 1032/1032 |
| P9 | **AVOIDED, and it was live** | the error I filed against myself — reading `Φ*_pref/Φ*` as what the theorem is about. P4's result is exactly the material that would have produced it. |
| P10 | **AVOIDED** | `C1` is reported as FRAMING, in the ticket's own words |

Hand measurements `H1`–`H10` were **disclosed in `PREDICTIONS.md` before any script existed**
and are NOT scored as predictions. `H4` (invariance under consistent conversion) and `H5` (the
mixing error is worth ~6×, optimistically) are the two that carry the audit's headline, and
both were derived by hand first and machine-confirmed second.

## 4. Defects of this instrument, kept in the source

Three of the four were caught by my own negative controls firing **against correct code**.

1. **`c = ρ_max/λ_std` divided by zero at the antichain** (`λ_std = 0`, so `c` is `0/0`) and
   printed `min c = 0.000` at every `n`. `mg-76b2`'s population is smaller than mine by
   exactly 1 at every `n` and **its exclusion is the correct one**. `P5` scored HELD on this
   artefact before the fix and MISSED after — the fix cost me a prediction and it is reported
   that way round.
2. **`NC2` dropped its own hypothesis**: it asserted Lemma 3.3's conclusion about whatever
   vector Jacobi returned for the antichain — `[0.707,−0.707,0,0]`, not monotone — and failed
   against correct code. Fixed by using the source's own tied vector `(a,a,a,−3a)`.
3. **`NC3` ran `n = 3,4,5`** and reported `8177/11312` against `mg-76b2`'s `8178/11316`. Its
   `n ≤ 5` **includes `n = 2`** and the single missing disagreement is the 2-chain witness the
   document itself names.
4. **The conditional-marker classifier counted the word `window`** — the noun a conditional
   qualifies, not the qualifier. `NC5` caught it. The 6 remaining machine-bare sites are
   reported and then read **by hand**, not tuned away; tuning the regex until it returned `0`
   would have made the census unfalsifiable.

## 5. Declared limits

- `n ≤ 6`. Every `n`-growth statement is a **direction**; a finite population can refute a
  uniform-in-`n` bound and can never establish one.
- `0` of `4376` primitive posets here are inside the budget `ε_spec ≤ 2×10⁻²` (smallest gap
  `0.0562`), so **every `C₃` figure is measured outside the regime it would be used in**.
- Degenerate top eigenspaces (163 posets) return `UNDECIDED` rather than being searched, so the
  monotonicity test is *sufficient* only and `mg-76b2`'s existential search is the stronger
  instrument. `1727 + 163 = 1890` reconciles the two counts exactly.
- `ε_leak = 0.20` is **HEURISTIC** — `mg-3ce3`'s envelope — and is not pinned here.
- Every `1−λ_std` is FLOAT (Jacobi). Comparisons that could turn on float noise are stated with
  their tolerance (`1e-9` for eigen-multiplicity and inequality slack, `1e-12` for zero-gap).
