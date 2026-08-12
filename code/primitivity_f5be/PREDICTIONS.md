# `mg-f5be` — predictions, with the exposure disclosed rather than laundered

Filed before one line of `libf5be.py` exists. The repo's standard (`mg-b417`, `mg-a0d6`,
`mg-8d66`) is that a prediction filed after the fact is a **report** and that saying so is
worth more than the appearance of a bet. So, first, what I already know when I write this.

## Exposure

- **H1 — I have read `docs/OneThird-Compression-W4-Rate-mg-409a.md` IN FULL, including its
  §3 ceiling proof, before writing this.** I therefore know that the ceiling proof in the
  deliverable is **NOT** the chain `pm-onethird` writes in the ticket. That is already a
  finding and it is not a prediction; it is stated in P0 below at zero credit.
- **H2 — I have DERIVED `pm-onethird`'s chain on paper**, from §2's `L1`/`L2` plus
  `lib409a.bk_energy`'s normalisation, and from a swap involution for the second link. I have
  run **no code**. P1 and P2 are therefore paper-derivations, not measurements — genuine bets
  against my own algebra being wrong, but at high stated probability and not blind.
- **H3 — I know from `mg-145f` (relayed in the ticket, not yet re-read by me at filing time)
  that the frozen class is expected to be EMPTY at every enumerable `n`.** P6's "vacuous" is
  therefore near-certain and is filed to pin the *reporting* obligation, not the fact.
- **H4 — the ticket wants its own author's reading attacked, and I am aware that an agent
  under that instruction has an incentive to manufacture a refutation.** The specific shape I
  must not produce is a "refutation" that is really a restatement of the same inequality with
  a sign flipped. My guard: P1/P2 predict `pm-onethird` is **right** on the mathematics, and
  the only thing I expect to take off him is the *significance*, which is the hardest shape
  to fake in the direction of a manufactured kill.
- **H5 — I have NOT read `mg-05ec` or `mg-8d66`'s deliverable at filing time**, only the
  ticket's one-line relays of them.

## Predictions

| # | claim | p | status when filed |
|---|---|---|---|
| **P0** | `mg-409a`'s ceiling proof is an **odd-fiber-indicator / `Ran Q_o = 0`** case split, and the string `4 p (1-p)` does **not** appear in it | 1.00 | **report** (H1: read) |
| **P1** | `R_M(f_xy) = P(x,y adjacent) / (4 p (1−p))` **exactly**, at every incomparable pair of every poset — i.e. `pm-onethird`'s first term is a true consequence of `mg-409a`'s `L1`+`L2` under `lib409a`'s normalisation | 0.93 | live (paper only) |
| **P2** | `P(x,y adjacent) ≤ 2·min(p, 1−p)` at every incomparable pair, by the adjacent-swap involution — hence `alpha ≤ 1/(2·max(p,1−p))` and `pm-onethird`'s chain is **CORRECT** | 0.92 | live (paper only) |
| **P3** | the chain is available at **every** incomparable pair, not a distinguished one, so the most extreme pair may be chosen: `alpha(P) ≤ 1/(2(1−μ(P)))` with `μ(P) = min over incomparable pairs of min(p,1−p)` | 0.95 | live |
| **P4** | `alpha = 1` is **NOT attained by any primitive poset** at any `n` in range (`n ≤ 6` exhaustive), and the primitive maximum is strictly below 1 | 0.65 | live |
| **P5** | the primitive maximum is nevertheless **> 3/4** at some `n ≤ 6` — i.e. primitivity alone does not deliver the frozen bound | 0.60 | live |
| **P6** | the frozen class (`δ(P) < 1/3`) is **EMPTY** at every `n ≤ 6`, so the frozen measurement is **VACUOUS** and must be reported as vacuous rather than as a maximum of 0 | 0.98 | live (H3) |
| **P7** | the **near**-frozen ceiling is materially lower than 3/4: at the least-balanced pair actually available (`μ_min ≈ 0.276`, the Kahn–Saks extremal value) the chain returns `≈ 0.69`, and measured `alpha` at the minimising posets is **far below even that** | 0.70 | live |
| **P8** | the verdict is **closure-holds-on-primitives**, and `pm-onethird`'s reading is RIGHT ON THE MATHEMATICS but the strengthening is **not load-bearing** — because `alpha ≤ 1` is a *proved bound at every poset*, not an empirical max over a witness set, so no restriction of the class can raise it | 0.85 | live |
| **P9** | at least one **decomposable, non-ordinal-sum** poset (a disjoint union, or a substitution that is not an ordinal sum) also attains `alpha = 1` — i.e. `Z_n` is not the only witness shape | 0.40 | live |

## Named conditions under which I would report `closure-fails-on-primitives`

Filed in advance so a reversal cannot be assembled after the fact.

1. Any primitive poset with `alpha > 1`. (This would refute `mg-409a` §3 outright, not merely
   its class restriction, since that proof is unconditional.)
2. Any poset, primitive or not, where the measured `alpha` **exceeds** the exhibited exact
   pair bound `min_{x‖y} R_M(f_xy)` — which would break `L2` and with it both chains.
3. A frozen poset (`δ < 1/3`) at any `n` in range. That is a counterexample to (1/3)–(2/3)
   and would make every question here secondary.
4. `pm-onethird`'s chain failing at some pair — either link — which would mean the tighter
   ceiling is not available and only the unconditional `≤ 1` survives.

## Errors I expect to be able to make here

- **E1 — conflating `δ(P)` with `μ(P)`.** `δ = max_{x‖y} min(p,1−p)` (the conjecture's
  quantity, a *best* pair); `μ = min_{x‖y} min(p,1−p)` (a *worst* pair). The chain uses `μ`.
  Frozen ⟹ `δ < 1/3` ⟹ `μ ≤ δ < 1/3`, so the implication runs, but only in that direction,
  and swapping them silently would make P3 false and P7 nonsense.
- **E2 — "primitive" is ambiguous and I must fix it.** Prime/indecomposable under *modular*
  (substitution) decomposition is strictly stronger than ordinal-sum-indecomposable. Daniel's
  word was "primitive"; I will measure **both**, plus connectivity, and report all three, so
  that whichever he meant is answered.
- **E3 — reporting an empty class as a zero.** The frozen maximum is not `0`; there is no
  maximum. `max()` over an empty list must raise, not return a sentinel that prints as a
  number. Planted as a control.
- **E4 — a float `alpha` compared against an exact bound and "passing" by rounding.** Every
  verdict must be an exact rational comparison or an exhibited rational witness; floats are
  measurement only. Same exposure as `mg-409a`'s D6.
- **E5 — an enumeration that silently misses iso classes.** The augmentation generator must
  reproduce 1, 2, 5, 16, 63, 318 for `n = 1…6` or it is wrong. Planted as a positive control.
- **E6 — treating a chain (`|L(P)| = 1`) as vacuously frozen.** It has no incomparable pair,
  so `δ` is a max over an empty set and the chain has no pair to stand on. Excluded
  explicitly, and the exclusion is itself an arm.
