# mg-6bc2 — predictions, committed BEFORE any script of this instrument exists

**Work item.** `mg-6bc2` — sharpen `ε_sup` by pair bias; say what makes it `1/6`, or say what the
pair-bias argument actually gives and where it stops.

**What this instrument is.** One exact-rational LP. It computes, over *all* probability measures on
`S_n` subject only to "every pair is flipped with probability `≤ 1/3` against a fixed reference
order `e`", the maximum of `E[inv_e]` and the maximum of `E[footrule]`. That feasible set is the
**marginal relaxation** — the formalisation of "pair bias alone". It is not a poset sweep and it
enumerates no posets; the refusal `mg-345e` declared and I am keeping stands (§ *not done*, below).

---

## Hand measurements, disclosed rather than laundered into predictions

Things I already knew by hand or by reading, before writing any script. They are **not**
predictions and are not scored.

- **H1.** `Op-Form` Claim 6.1 (`docs/OneThird-lambda-std-Operative-Form.md:399`) proves
  `E[inv_e] < m/3`, and `Op-Form:§6.3` converts it to `ε_spec < d·n/(n+1) < 1`. Read, not derived
  here.
- **H2.** I derived by hand, before scripting, that the **two-atom law** `μ = (1−p)δ_e + p·δ_{rev e}`
  at `p = 1/3−η` has *every* pair flipped with probability exactly `1/3−η` and
  `E[inv_e] = (1/3−η)·C(n,2)` — i.e. it **attains** the bound `m/3` at `d = 1`. So I already
  expected P1/P3 to hold; the LP is a check on my algebra, not a discovery procedure.
- **H3.** I computed by hand that the same two-atom law scores only `1/2` in the **footrule** form
  of the master bound (`3E[F]/(n²−1)`), because the reversal has `F ≈ n²/2` while `2·inv ≈ n²`.
  This is what made the footrule form look like a possible free factor of 2 and is the reason this
  LP exists.
- **H4.** I then constructed by hand a **hierarchical block-rotation** family (level `ℓ` = `2^ℓ`
  blocks, each internally half-rotated, mass `1/3` on each of levels 0,1,2) whose flip-sets are
  pairwise disjoint, giving `E[F] = 7n²/24` and hence `3E[F]/(n²−1) → 7/8`. So I already knew
  before running that the footrule form cannot buy a factor of 2, and can buy at most `1/8`.
  **This kills my own lead before the machine gets a vote**, and it is why P2 is stated as a
  narrow interval rather than as "the footrule form wins".
- **H5.** `mg-c4f5`'s audit records, at `docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415`,
  *"Freezing unconditionally gives only `ε < 1/6 ≈ 0.167`"*, and `mg-c3ca:172` defines that `ε` by
  `E[inv_e] ≤ ε n²`. I read both before writing this file. So I already know the corpus contains a
  **supply-side `1/6`**, and that `mg-345e:292`'s *"`1/6` occurs twice in this corpus and neither
  occurrence is a supply-side derivation"* is wrong on both counts.
- **H6.** `E_unif[inv] = C(n,2)/2` and `E_unif[footrule] = (n²−1)/3`; the master bound is sharp at
  the antichain in the footrule form and lossy by `3/2` in the inversion form (`Op-Form:§6.1`,
  §6.3). Read, and re-derived by hand.

---

## Predictions

| # | prediction |
|---|---|
| **P1** | The LP maximum of `E[inv_e]` is **exactly `C(n,2)/3`** (at cap `1/3`), for every `n` tested — i.e. the marginal relaxation is *saturated* and `Op-Form` Claim 6.1 is **not a lossy step**. |
| **P2** | The LP maximum of `E[footrule]` is **strictly less** than `(n²−1)/3` (the value that would make the footrule form worth `ε = 1`), and the ratio `3·max E[F]/(n²−1)` lands in **`[3/4, 1)`** at every `n` tested. |
| **P3** | The two-atom law **attains** the `E[inv_e]` optimum (P1's optimum is achieved by an explicit 2-support measure). |
| **P4** | The two-atom law does **not** attain the `E[footrule]` optimum — it scores `≈ 1/2` where the optimum is `≥ 3/4`. |
| **P5** | The footrule optimum ratio is **non-decreasing in `n`** over the range tested. |
| **P6** | Neither optimum is attained by a measure that is the linear-extension measure of any poset — every optimiser violates **adjacency symmetry** (`Pr[x` immediately precedes `y] = Pr[y` immediately precedes `x]` for incomparable `x,y`, `mg-92e6`), which is the corpus's already-proven joint fact. |
| **P7** | **My most likely error, filed in advance.** That the small-`n` LP values mislead about the `n → ∞` limit for the footrule form: the ratio in P2 is a *finite-`n`* number and my hand construction (H4) is *asymptotic*, and these are different objects. If the LP ratio at `n = 6,7` disagrees with `7/8`, the honest reading is that **neither** settles the limit, not that one refutes the other. I expect to be tempted to report the LP number as if it were the limit. |
| **P8** | **Second most likely error.** Reporting "pair bias gives `1/6`" and "pair bias gives `1`" as two *findings* rather than as **one fact in two normalisations** (`ε_spec = 6·E[inv]/(n²−1)` vs `ε_c3ca = E[inv]/n²`). The whole value of this ticket is that they are the same statement; writing them as two invites exactly the miscitation `mg-33f5` warns about. |

## Not done, deliberately

- **No poset enumeration.** `mg-345e` declared and refused it and I am keeping the refusal: the
  1/3–2/3 conjecture is verified to `n = 14`, so the frozen class is **empty** at every `n` this
  corpus can enumerate, and any empirical calibration of `ε_sup` would measure a hypothetical
  population. This LP is over **measures on `S_n`**, not over posets.
- **No attempt at L4, `C₃`, or `ε_dem`.** All three are out of scope by the ticket's own wording.
- **No attempt to compute the LP value under adjacency symmetry added.** P6 only checks that the
  optimisers violate it; it does not compute the improved optimum.
