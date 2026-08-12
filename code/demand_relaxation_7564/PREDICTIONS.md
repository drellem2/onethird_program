# `mg-7564` — PREDICTIONS, filed before one line of this instrument existed

Deliverable: [`docs/OneThird-DemandRelaxation-mg-7564.md`](../../docs/OneThird-DemandRelaxation-mg-7564.md).

## ⚠️ EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

This ticket is a **search of the corpus followed by an arithmetic join**, not a discovery
sweep. Before writing this file I had already read, in full:

- `docs/OneThird-ChainSelection-mg-9461.md` (§0, §4.3, §4.4, §5)
- `docs/OneThird-C3-PrefixCapture-mg-76b2.md` (§6, §10)
- `docs/OneThird-ChainIV-CaptureFraction-mg-81ff.md` (§0.4, §0.5)
- `docs/OneThird-ChainIV-CaptureFraction-mg-00b3-IndependentAudit.md` (§0.4, §0.5)
- `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` (§3.1, §6)
- `code/chain_selection_9461/out_s1_chains.txt` — **which already contains most of the
  four-chain arithmetic this instrument recomputes.**

So **`R1`–`R5` below are REPORTS at zero credit.** They are recorded because a prediction
file whose entries are all safe is worse than one that says which entries were safe. Only
`P1`–`P4` are live bets: they are the join nothing in the corpus performs, and I had not
done the arithmetic when I wrote them.

## REPORTS (zero credit — already read before filing)

| # | statement |
|---|---|
| **R1** | The demand side **has** been attacked: `mg-345e`, `mg-76b2`/`mg-94c3`, `mg-9461`/`mg-39bf`, `mg-81ff`/`mg-00b3`. It is not an unexplored half. |
| **R2** | There are (at least) **three** `C₃`s, not two: `C₃^(III)`, `C₃^gap`, `C₃^cut`. The one in `ε_dem = ε_leak²/(2C₃)` is `C₃^(III)`. |
| **R3** | `C₃ ≥ 1` unconditionally is a statement about the **gap-form** `C₃`, per `mg-76b2` §10. |
| **R4** | `ε_leak = 0.20` is an **empirical FP calibration**, is L4's threshold `ε₀`, and errs **optimistic** in the required scope. |
| **R5** | `mg-9461` prices the whole chain question at `10×` and the residual wall at `5×`. |

## LIVE BETS

| # | odds I gave myself | statement | how it is scored |
|---|---|---|---|
| **P1** | 70% | Recomputing the four chains from each chain's own `Φ` bound, in exact rationals, on code sharing no line with `lib9461`, **reproduces `out_s1_chains.txt` §A exactly at every row.** | `d1` prints both and diffs them |
| **P2** | 55% | **Nothing in the corpus joins the `ε_dem` currency to the `d·q̄` currency.** `1/150` appears only against `ε_spec = 1/50`; no document states what `d·q̄` the *relaxed* chains would permit. | grep, printed in `d1` |
| **P3** | 60% | With `q̄ = 1/3` (pinned at every boundary maximiser at every `n ≤ 7`, `mg-6bc2` §3.1) the demand is a **pure density bound**, and the numbers are `d ≤ 1/50` (chain III) and `d ≤ 1/5` (chain IV ceiling) — i.e. **2%** and **20%** of pairs incomparable. | `d1` computes it |
| **P4** | 45% | Carrying `mg-00b3`'s **in-regime** `C₃^gap` into the ladder, chain (II)'s relaxation is **negative** by `n = 25` (worse than chain III), while chain (IV)'s survives at roughly `6–7×` rather than `10×`. | `d2` computes it |

## WHAT THIS INSTRUMENT DOES NOT DO, STATED BEFORE IT RUNS

- **It enumerates no posets.** Every measured input (`C₃^gap`, `c`, `gap`) is **cited** from
  `mg-94c3` / `mg-81ff` / `mg-00b3` and typed in as an exact rational or as the decimal those
  documents print. Nothing here re-measures a poset and nothing here should be read as
  corroborating one.
- **It computes no window figure** (`n ≥ N`). `mg-131e` voided the supply those rest on.
- **It does not re-derive `ε_leak`, `ε_sup`, or `C₃^(III) = 1`.** Those are cited with their
  status attached.
- **It proves nothing about the conjecture.** It is arithmetic on other people's numbers, and
  its only original content is which numbers are put next to which.
