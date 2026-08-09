# `code/eps0_audit_d3c7/` — mg-d3c7's instrument for the independent audit of mg-3969

Written from the **source** definitions in
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
(603 lines, md5 `db095fbe12ba19f0a8107f962c0d1c8f`):

| object | source | used for |
|---|---|---|
| `p_xy`, `δ(P)` | `:59–66` | balanced pairs, the `[1/3,2/3]` test |
| `σ(A)`, `K_k` | `:239–250` | fixes the reading of `σ(A)` (see C7) |
| `Δ₁(A,B) = E\|A \ σ(A)\| / min(\|A\|,\|B\|)` | `:270–278` | the leakage `ε_leak` — **the normalisation every number here is in** |
| `Φ_P(A) = E\|A \ σ(A)\| / \|A\|` | `:229–237` | the C7b sensitivity control only |
| L4 | `:464–474` | the statement under audit |

**Shares no code with `code/eps0_threshold_3969/`.** None of the parent's four
instruments was run. Exact `Fraction` throughout; no float on any decision path.

**Population.** Naturally labelled posets on `[n]` (identity order is a linear
extension) with `A_k = {0..k−1}` — exactly the set of (poset, linear extension,
prefix cut) triples. Counts `1,1,2,7,40,357,4824,96428` (OEIS A006455) are checked
in C1 and match `mg-3969`'s population sizes at every `n`.

## Files

| file | what it does |
|---|---|
| `PREDICTIONS.md` | committed at `b2e5fcd` before anything was opened; exposure disclosed in §A |
| `lib_d3c7.py` | poset enumeration, linear extensions by down-set DP, `Δ₁`, `p_xy` |
| `b0_selftest.py` | controls C1–C8. **Run this first — it must print `SELFTEST PASSED`** |
| `b1_witness.py` | `mg-3969` Claim 6.1's witness recomputed: `e(P)=26`, `Δ₁=17/78`, all four landings |
| `b2_sweep.py [n]` | exhaustive sweep in `mg-3969`'s scope (both sides non-chain) |
| `b3_smaller_probe.py` | localises the Claim 6.2 `1/7` fallback to an `\|A\|=\|B\|` tie cut |
| `b4_fullsweep.py [n]` | unpruned, and **closes the coverage gap `mg-3969` §9 disclosed** |
| `b5_gapwitness.py` | certifies the gap witnesses on a second code path (`n!` filtering) |
| `b6_family.py` | the infinite family driving the uniform ceiling to `0` |
| `b7_scope_and_arith.py` | D1 L4 untouched · D2 the `58 755` reconciled · D3 all arithmetic · D4 normalisation |

## Headline results

* **Reproduced exactly:** `e(P)=26`, `Δ₁=17/78`, `13/111`, `42` failures at `n≤6`,
  `682` at `n≤7`, `335 496` in-scope cuts, `11 480` at `n≤6`, and all eight
  arithmetic figures.
* **The negative held under attack:** 0 `U_either` violators with `Δ₁ < 17/78`
  anywhere at `n ≤ 7`, in `mg-3969`'s scope.
* **The finding:** with the one-side-chain cuts included — the scope `mg-3969` §9
  itself calls architecturally required — the thinnest violator at `n ≤ 7` is
  `1/7`, and an explicit family (chain plus one isolated element, `n = 2k+1`) drives
  `Δ₁ = (k+1)/((2k+1)k) → 0` with every balanced-in-side pair evicted. So the
  uniform threshold is **`0`, not `≤ 17/78`** — refuted, not capped.
* **L4 is untouched:** every family member satisfies L4's disjunct (i),
  `δ(P) = ⌊n/2⌋/n ≥ 1/3` (D1).

## Controls

C1 poset counts · C2 population reconciliation (this is what explains `mg-3969`'s
`604 230` vs `604 250`) · C3 the double-count identity `Σ_P e(P) = n!·|NLP(n)|`
against an independent enumeration · C4/C5/C6 DP vs brute force on every poset, cut
and pair at `n ≤ 5` · **C7 the two readings of `σ(A)` agree on prefix cuts** (a
control that failed as designed and became a finding — the ambiguity is immaterial)
· **C7b** the replacement sensitivity control, `Φ` vs `Δ₁`, differing on an exactly
predicted set of 698 cuts · C8 `Δ₁ ≤ 1`, attained at `(n−1)/n`.

Full write-up: [`docs/OneThird-L4-Threshold-eps0-mg-d3c7-IndependentAudit.md`](../../docs/OneThird-L4-Threshold-eps0-mg-d3c7-IndependentAudit.md).
