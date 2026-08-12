# `mg-8d66` — predictions, with the exposure disclosed rather than laundered

Filed before `lib8d66.py`'s arms exist, **but not before I had looked.** The repo's standard
(`mg-b417`, `mg-a0d6`) is that a prediction filed after the fact is a report, and that saying
so is worth more than the appearance of a bet. So:

## Exposure

- **H1 — I DERIVED THE ANSWER ON PAPER BEFORE WRITING ANY CODE**, and then ran a ~40-line
  scratch probe (`scratchpad/probe.py`, not committed) that checked four of the claims below
  at **n = 4 exhaustive (195 posets) and n = 5 exhaustive (4 111 posets)** and returned
  `0` failures on all four. P1–P4 are therefore **REPORTS OF A MEASUREMENT ALREADY TAKEN**,
  not bets, and should be read at zero credit. What remains genuinely open when this file is
  written is P5–P9.
- **H2 — I read `docs/OneThird-Compression-W4-Rate-mg-409a.md` in full, including its §3
  ceiling proof and its §4 antichain closed form, before deriving anything.** My witness (the
  pair indicator `f_xy`) is the same function `mg-409a`'s L1/L2 already use. The step that is
  mine is *why it is `k`-independent*, not the choice of function.
- **H3 — the mayor's dispatch note says confirming the derivation is the failure mode.** I am
  aware that an agent under that instruction has an incentive to manufacture a refutation. The
  guard I can offer is that my answer **confirms `pm-onethird`'s stated premise exactly** and
  refutes only the conclusion he draws from it, which is the shape that is hardest to fake.

## Predictions

| # | claim | p | status when filed |
|---|---|---|---|
| **P1** | `Q_finest = ((n−1)/2)·(I − P_BK)` as an **exact matrix identity** — the finest admissible partition's operator IS the BK generator rescaled | 0.99 | **report** (probe: 0 failures, n = 4, 5) |
| **P2** | `<f, Q_S f> ≤ <f, Q_finest f>` for every admissible `S` and every `f` — refining a class can only raise the form | 0.99 | **report** (probe: 0 failures) |
| **P3** | `<f_xy, Q_S f_xy>` is **the same rational for every admissible `S`** — the pair witness cannot see `k` | 0.99 | **report** (probe: 0 failures) |
| **P4** | `alpha_S ≤ 1` at every poset for every admissible `S` | 0.99 | **report** (probe: 0 failures) |
| **P5** | the ceiling `1` is **attained at every `k`**, at `Z_n`, `n = 4..10`, both directions exact | 0.85 | live |
| **P6** | `mg-409a`'s own ceiling proof (odd-fiber indicator) generalises only to `alpha_k ≤ k−1`, which is **above the bar from `k = 4`** — i.e. `pm-onethird`'s expectation was the reasonable one and needed a different witness to kill | 0.80 | live |
| **P7** | the maximum admissible `k` is `n−1` and the minimum is `2`, with the `k = 2` partition **unique** — so the class is **not** closed by counting | 0.90 | live |
| **P8** | at a **fixed** poset `alpha_k` strictly rises with refinement at a majority of `n = 5` posets — the effect `pm-onethird` predicts is real, it just terminates below 1 | 0.70 | live |
| **P9** | the operator inequality `((n−1)/2)(I − P_BK) ⪰ Q_S` is **strict** at some `S` and some poset, i.e. `pm-onethird`'s `=` is genuinely a `≥` | 0.85 | live |

## Named conditions under which I would report `class-alive-at-k>2`

Filed in advance so a verdict cannot be assembled after the fact.

1. Any admissible partition `S` at any poset with `alpha_S > 1`.
2. Any counterexample to `Q_finest = ((n−1)/2)(I − P_BK)` — which would mean the finest
   foliation is **not** the original chain and the ceiling argument loses its anchor.
3. Any `f` and admissible `S` with `<f, Q_S f> > ((n−1)/2)·E_BK(f)` — the inequality running
   the wrong way, which would make the compression bound stronger than the chain it bounds.
4. `max_k` growing fast enough, together with a ceiling of `k−1` surviving, that some `k` puts
   the reachable `alpha_k` above `3` — i.e. if the `k−1` bound were the true ceiling.

## Errors I expect to be able to make here

- **E1** — reading `alpha_k` rising **at a fixed poset** as the ceiling rising. Those are two
  quantities and `pm-onethird`'s derivation slides between them; so can mine.
- **E2** — treating the `k` foliations symmetrically. `mg-8bc7` measured that they are not
  interchangeable (rank `Pi_o < rank Pi_e` at 127 of 219 posets at `n = 4`); every step below
  must be a per-class sum and never an average.
- **E3** — a "partition" that is not one: dropping a position, or repeating one, silently
  breaks the per-position sum, and every identity here would move. Arm `k0` plants both.
- **E4** — a class with two **adjacent** positions is not a class; its fiber is not a cube and
  the Efron–Stein step fails. Planted in `k0` and it must go red.
- **E5** — confusing `Var(f)` with `||f||²`. They agree only on `1-perp`.
- **E6** — quoting a float from Jacobi as a verdict. `mg-409a`'s D6 is the same exposure.
