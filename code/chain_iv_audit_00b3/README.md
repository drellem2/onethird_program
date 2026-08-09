# `code/chain_iv_audit_00b3/` — mg-00b3's instrument (INDEPENDENT AUDIT of mg-81ff)

**Question.** Not *is `c > 0.80` establishable* — that is `mg-81ff`'s question and the
ticket forbids re-attacking its answer. The question here is whether **`mg-81ff`'s own
self-caught correction survives**: the stratification **reversal**, the **two in-regime
families**, and the headline **`chain (IV) is chain (II)`**.

**Deliverable.** [`docs/OneThird-ChainIV-CaptureFraction-mg-00b3-IndependentAudit.md`](../../docs/OneThird-ChainIV-CaptureFraction-mg-00b3-IndependentAudit.md)

**Answer, in one line.** The reversal is **real and not an artefact of binning** — but the
word *monotonically* is carried by the six chosen bands; the **two families are one poset
under two labellings**; and a **third family, found by search rather than construction,
sits inside the budget with `C₃^gap` rising through `10.55` where `mg-81ff`'s family sits
at `1.03`.

## Run

```sh
sh run_all.sh          # ~4 min cold, ~40 s warm
```

| file | what it is |
|---|---|
| `lib00b3.py` | posets, push-DP transport via the dual, integer-cut `Q_k`, exact `λ₂` by positive-definiteness, the named families |
| `tridiag.py` | Householder + Sturm bisection — the fast `λ₂` the 86 277-row sweep needs |
| `sweep.py` | one exhaustive pass per `n`, cached **outside** the repo |
| `a0_controls.py` | 20 controls, `(A)`–`(G)`, each with a live negative arm |
| `a1_population.py` | ticket items **3** and **4**: the population, `D_k`, and whether `n ≤ 6` was run as a control |
| `a2_reversal.py` | ticket item **1**: the reversal, attacked four ways |
| `a3_regime.py` | ticket item **2**: the two families, and the third one |
| `a4_identity.py` | the headline: the identity, the demand algebra, and the class-level quantifier |
| `out_*.txt` | transcripts, committed |

## No shared code, and the differences are structural

`lib81ff` and this file agree on nothing but the definitions, which both take from
`Op-Form §4.3` / `mg-76b2` rather than from each other.

| | `lib81ff` | `lib00b3` |
|---|---|---|
| enumeration | extend a poset on `[n−1]` by a down-closed set | mask the `C(n,2)` natural pairs, keep the transitively closed |
| transport | two DPs, a forward `e[S]` and a backward `g[S]` | **one** push DP, applied to `P` and to its **dual** |
| `Q_k` | sum over weighted edges of a centred vector | an **integer cut count** — the centred prefix indicator jumps by exactly `n` across the cut and `0` elsewhere |
| exact `λ₂` | Sylvester on the pencil `BᵀLB − q·BᵀB` | no pencil, no basis change: `λ₂ > q ⟺ L − q(I−J/n) + J/n ≻ 0` |
| fast `λ₂` | Jacobi | Householder tridiagonalisation + Sturm |

That the two land on the same 86 278 posets and the same fourteen band minima is
therefore a **result**, not an inheritance.

## One defect of my own, caught by a control, kept in the history

`a0 (A)` **failed on its first run**, at 3280 of 5230 posets. It compared the two
down-set enumerators as **lists**. The sets are identical at every one of the 5230 (zero
set-differences); what differs is the order *within* a popcount, because the scan
discovers by increasing mask value and the lattice walk by BFS. The push DP consumes
exactly one property of that order — popcount non-decreasing — and both have it. So the
failure was **my control's, not my instrument's**, and asserting list equality would have
made `a3`'s `n = 28` rows unreachable for a reason that does not exist. The control now
asserts the two things that are load-bearing (same set, popcount-monotone) and keeps the
negative arm that shows the closure test is doing work (dropping it walks 65 536 states
instead of 32).

## No `PREDICTIONS.md`, and why

Same reason `mg-81ff` gives, and it applies harder here: my dispatch printed
`mg-81ff`'s conclusions in full — the band table's two endpoint values at both `n`, all
four `D_k` values, both in-regime families' `c`, the primitive counts, `0.412700`,
`3.075`, and the headline — so a predictions file written after reading it would be
theatre. The exposure, stated instead:

- **Pre-answered, therefore CHECKS and not findings:** every figure in `a1`, the seven
  band minima in `a2 (R1)`, and the two families' rows in `a3 (F1)`.
- **Not pre-answered, therefore this instrument's own:** the re-binning of `a2 (R2)`–`(R4)`
  and the bin-free crossings of `(R5)`; the isomorphism of `N` and `N'`; the staircase
  family and every row of it; the class-level quantifier of `a4 (I3)`.

## Not done

- **No `n = 8` sweep** (~2.8M posets). The reversal is tested at `n = 6` and `n = 7` only,
  which is two values of `n` and I do not treat it as more.
- **No proof that `C₃^gap(S_n) → ∞`.** Thirteen exact in-regime points rising with a clean
  linear fit is a direction; the limit needs an asymptotic for `λ₂(S_n)` uniform in `n`.
  This is the same line `mg-81ff` correctly refuses to cross for `c(D_k) → 0`, and the
  refutation of `C₃^gap ≤ 10` on the regime class does not need it — it needs one witness
  and has one (`S_26`, exact).
- **No attempt at `ε₀`, `L2`, or `C₃ = 1`** — the ticket forbids all three.
- **`17/78` does not appear** anywhere in this directory, with or without its scope.
- **No window figure** (`mg-131e` voided it), **`STATE.md` untouched**, and `mg-81ff`'s own
  document not edited — the corrections named here are `pm-onethird`'s to land or refuse.
