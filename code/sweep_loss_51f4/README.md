# `code/sweep_loss_51f4` — the instrument for `mg-51f4`

**Question.** `mg-28ff` landed `C₃^(III) = 1` without L2 at `n ≤ 6` by two routes, `(M♯)` and
`(F)`, and reported that both route constants are **rising** (`0.943` and `0.812` at `n = 6`)
while the truth they chase converges (`0.328`). The ticket asks: *what does the Cheeger sweep
lose as a function of `n`, and can that loss be bounded uniformly?* — and forbids attacking
either route alone.

**Answer.** The loss is **unbounded and that is not the problem**. What decides the routes is:

* `(M♯)` carries an exact **floor** `c♯(P) ≥ Δ_P − (1−λ_std)/2` that no test vector can beat.
* `(F)` carries **no** such floor; its loss is the **mediant** loss `M/Φ*_pref`.
* **Both routes are refuted at `n = 7`, exhaustively and exactly** — `(F)` at 168 of 86278
  primitive posets, `(M♯)` at exactly 4 — and the two failure sets are **disjoint**.
* The object the theorem actually consumes is the **disjunction** `min(c♯, f*)`, which
  survives at **86278 of 86278** with `c_or(7) = 0.894472`.

See `docs/OneThird-SweepLoss-mg-51f4.md`.

## Files

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed at `01c206f`, **before one line of `lib51f4.py` existed** |
| `lib51f4.py` | written from scratch; shares no source line with `lib28ff`, `lib76b2`, `libA94`, `lib_d3c7`, `lib3969`, `lib9461`, and computes the transport by a **different algorithm** (down-set DP, not `n!` enumeration) |
| `s0_selftest.py` | **16/16 forced arms**, A1–A12 plus four negative controls C1, C3, C4, C5 |
| `s1_census.py` | exhaustive `n ≤ 6`: the floor, the loss decomposition, the two regimes, `c_or` |
| `s2_families.py` | the ten named families, and the two exact refutations at family members |
| `s3_n7.py` | **`n = 7` EXHAUSTIVE** — all 96428 posets, streamed; the row that replaces `mg-28ff`'s sample |
| `s4_combined.py` | the one construction on which both route constants rise together |

`sh run_all.sh` reproduces every `out_*.txt`. `s3` takes ~30 min; everything else is minutes.

## The three commitments that make the numbers worth reading

1. **No float decides a verdict.** `γ ≥ r` is settled without computing an eigenvalue, as
   exact definiteness of the pencil `Q − rN` in the `ψ` basis of `1^⊥` (Sylvester's criterion,
   leading minors from one fraction-free Bareiss elimination over the integers). `A6` asserts
   this against an independently written Faddeev–LeVerrier test on the `n × n` Laplacian, at
   3902 (poset, threshold) decisions, and `C1` shows a deliberately wrong Laplacian shift
   disagrees — so `A6` can discriminate.
2. **`μ_pref` is bracketed EXACTLY, not measured.** `mg-28ff` §10 records the cone minimum as a
   float search whose *lower* use is a measurement, which is why it could not refute `(M♯)`.
   Here `μ_pref ≥ t` is decided as **copositivity** of `Q − tN` over the monotone cone, by
   exact KKT enumeration of the `2^{n−1}−1` faces of the simplex. That is the whole reason
   this ticket can say "(M♯) is false at this poset" rather than "c♯ appears to exceed 1".
3. **A control that cannot fail is not a control.** `C4` **failed on its first run** and the
   replacement is a finding: at all 275 primitive posets on 5 elements `f*` is the smaller of
   the two, so at `n ≤ 5` the disjunction *is* route (F) and `min()` does not begin to bite
   until `n = 6`. `A8` asserts that the copositivity test **REFUSES** the Horn matrix rather
   than guessing. `C3` is the red drill: the pipeline prints FAIL on the two witnesses and
   HOLDS on posets where the routes hold, both directions.

## What is exact and what is not

| claim | status |
|---|---|
| `γ` brackets, `Φ*_pref`, `M`, `Δ_P`, `c_true`, `f*` | **EXACT** rationals, every comparison decided exactly |
| `(F) fails at P` | **EXACT** — one decision, `γ < M²/2` |
| `(M♯) fails at P` | **EXACT** where the copositivity bracket was run (`n = 7` exhaustive; families to `n = 15`) |
| `c♯` elsewhere | **UPPER BOUND** from an exhibited monotone vector. It can certify that (M♯) *holds* and can never certify that it fails. |
| every number from a named family | **FAMILY**, never a maximum over its `n`, labelled at each appearance |
| `n = 7` rows | **EXHAUSTIVE MAXIMA** over all 86278 primitive posets — not samples |
