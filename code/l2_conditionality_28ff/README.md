# `code/l2_conditionality_28ff` — the instrument for `mg-28ff`

**Question.** `mg-76b2` proves `C₃^(III) = 1` *conditional on L2*, and `mg-28ff` records that
L2 is the last conditionality under `ε_dem = ε₀²/2` with nothing in any status attacking it.
This instrument takes the ticket's **branch (C)**: show `C₃ = 1` is reachable *without* L2.

**Answer.** Yes at `n ≤ 6`, by two independent L2-free routes, at 4377 of 4377 primitive
posets including all 3340 where L2 fails — and **no** uniformly in `n`, because both route
constants rise (`0.943` and `0.812` at `n = 6`) while the truth they chase does not
(`0.328`). See `docs/OneThird-L2-Conditionality-mg-28ff.md`.

## Files

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed at `8c28781`, **before one line of `lib28ff.py` existed** |
| `lib28ff.py` | written from scratch; shares no code with `lib76b2`, `libA94`, `lib_d3c7`, `lib3969` |
| `selftest28ff.py` | **20/20 forced arms**, A1–A13 plus negative controls C1–C7 |
| `b1_footrule.py` | the footrule identity, the linear co-area bound, route (F) and its margin `f*` |
| `b2_census.py` | the main sweep: route (M♯), the constant `c♯`, and the EXACT certificate ladder |
| `b3_routes.py` | the three explicit monotone test vectors ranked, and `R(g_pos) = 1 − E[Spearman ρ]` |
| `b4_ruled_out.py` | the seven candidates ruled out, with witnesses, incl. the R7 red drill |
| `b5_trend.py` | `c_true(n)` — the route-independent truth — and the L2 census reconciliation |

`sh run_all.sh` reproduces every `out_*.txt`.

## The two commitments that make the numbers worth reading

1. **No float decides a verdict.** `r ≤ 1−λ_std` is settled without computing an eigenvalue,
   as exact PSD of `(I−S_P) − r(I−J/n)` via Faddeev–LeVerrier coefficient signs. Floats only
   *search* for candidate vectors; each is rationalised and re-verified exactly.
2. **A control that cannot fail is not a control.** A12 tests the L2-free sweep theorem
   against exhaustive brute force (10464 pairs). C6's ladder and C7 exist because the first
   version of C6 *could not fail* and had to be replaced — and the replacement produced
   `c_true`, the most informative number in the document. R7 fires: the pipeline prints FAIL
   on synthetic graphs where the target is genuinely false.

Two real defects in this instrument were caught by its own arms before publication: a sign
error in the exact PSD test (A6) and a badly designed bracket-agreement control (A7).
