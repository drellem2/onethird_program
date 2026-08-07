# `code/search_reach_abe8` — how far a constraint-pruned search can reach (`mg-abe8`)

**A feasibility-and-cost instrument. It does not run a search, and running one is out of
scope by the ticket's own instruction.** Total cost of everything here: under 7 minutes,
one process, one core.

## The question

`mg-abe8` asks how far a *targeted* search for a frozen counterexample (`δ(P) < 1/3`,
`STATE.md:46`) can actually reach, given that a minimal counterexample is known to be **rigid**
(`Aut(P) = 1`), of **width ≥ 3**, and to carry an **element incomparable to ≥ 7 others**
(`mg-5998`, whose attributions are **not** verified there or here), plus **primitive**
(`STATE.md:47`).

## The answer

**The constraints do not prune enough, and not by a margin better code could close.** All four
together prune `2.59` bits at `n = 9`, `0.07` bits at `n = 20`, and `0.00` bits at `n = 36` —
because every one of them is an *almost-sure* property of a random poset, and an almost-sure
property prunes `o(1)` bits by definition. Reach is `n ≈ 15` for a serious cluster and
`n ≈ 19` for a planetary ceiling. The full argument is in
[`docs/OneThird-SearchReach-mg-abe8.md`](../../docs/OneThird-SearchReach-mg-abe8.md).

## Files

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed at `b6e17e8`, **before any script here existed**; eight hand measurements disclosed, a pre-committed negative verdict at P10, two likely errors filed at P14/P15 |
| `OUTCOMES.md` | scoring, plus four defects of my own kept in the source |
| `libabe8.py` | posets, `δ` (two implementations), the four constraints, `prune_bits`, the A000112 growth models, the KR sampler. Imports nothing from this repo. |
| `selftestabe8.py` | 30 checks including **five negative controls**, each of which must FAIL for the suite to mean anything |
| `s1_census.py` | exhaustive constraint-density census, `n = 2..9`; frozen census and `δ` distribution, `n ≤ 8` |
| `s2_percandidate.py` | what one candidate costs: measured wall-clock, cheapest-correct-rejection, `#ideals` to `n = 40` |
| `s3_largen.py` | do the constraints still prune at `n = 12..40`? does frozen-ness? (KR model, labelled as such) |
| `s4_reach.py` | the cost model, the budgets and the machines they assume, the calibration against the literature's `n = 14`, and the exchange rate |
| `run_all.sh` | runs all five in order |
| `out_*.txt` | committed transcripts |

## Two things to read before quoting a number

1. **`prune_bits` is `−log₂(surviving/total)` and nothing else.** The inverted form
   (`−log₂(excluded/total)`) reports `19.93` bits where the right one reports `1.4e-06`.
   `PREDICTIONS.md` P14 filed this as my most likely error before any code existed; selftest NC1
   exhibits it.
2. **Everything above `n = 9` is a model, not a census.** `n ≤ 9` is exhaustive; `n = 10..40` is
   Kleitman–Rothschild sampling, which KR prove captures a `1 − o(1)` fraction of posets but
   whose convergence is slow. Directional, and labelled KR-model at every site.

## Provenance note

The motivating premise changed mid-run. The ticket framed this as gating Daniel's finishing
step ("an upper bound lets us finish by computer checking") against windows `n ≤ 34 / 98 / 398`.
`mg-00a1` returned during the run with `Θ(n²)` — **superlinear, so there is no `c·n + O(1)` bound
and no window** (pm-onethird, 2026-08-07 20:12). The instrument was already written as
reach-versus-target-`n`, so no measurement moved; the three window ends survive in `s4/H` as
**illustrative markers explicitly marked not live**.
