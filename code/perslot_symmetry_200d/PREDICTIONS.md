# `mg-200d` — predictions for **what PER-SLOT adjacency symmetry buys**

**Committed before any script of this instrument exists.** Nothing below has been run. The
hand measurements in §0 were made with pencil and `git show` only, and are disclosed here as
*measurements*, not laundered into predictions — several of them already decide part of the
ticket, and saying so in advance is the point.

Parent: `mg-6bc2` (`90d19e7`, branch `polecat-a6bc2`, **not yet merged to `main`** — its
`code/pairbias_sharpening_6bc2/` is read out of that branch, not out of my worktree).

---

## 0. Hand measurements, disclosed (made before any script existed)

**H1 — `mg-6bc2`'s own §5 states the swap-bijection fact for INCOMPARABLE `x,y`, and its
script tests ALL pairs.** `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md:222` reads
*"For **incomparable** `x,y`, the swap map is a bijection of `L(P)`"*. Its
`v2_optimiser.py:per_slot_violations` loops `for x in range(n): for y in range(n): if x < y:`
— every pair — and `lp6bc2.py:measure_stats` does the same for the aggregate form. So the
violation counts in its table `§5` include pairs that a real poset is **entitled** to violate.

**H2 — all-pairs per-slot symmetry holds for `uniform L(P)` iff `P` is an antichain.** If `P`
has any cover `x ⋖ y` then some `L ∈ L(P)` places `y` immediately after `x` at some slot `k`, so
`J_k(x,y) > 0`; and `x <_P y` gives `J_k(y,x) = 0` for every `k`. Every non-antichain has a
cover. The **aggregate** form fails on the same witness, so H2 covers both forms.

**H3 — hence the literal reading excludes every realisable measure in the relaxation, not just
the frozen ones.** The antichain's uniform measure has every pair flipped with probability
`1/2 > 1/3`, so it is not in `M_n` either. `M_n ∩ {all-pairs adjacency symmetry} ∩ {realisable}
= ∅` for every `n ≥ 2`. A number computed under the literal reading is **not an upper bound for
any poset**.

**H4 — at `n = 3` the literal per-slot EQUALITY form is INFEASIBLE.** Writing
`m₀,a,b,c,d,f` for the masses of `(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)`, the six
equations `J_k(x,y) = J_k(y,x)` (3 pairs × 2 slots) read `m₀=b, d=f, a=d, b=c, c=f, m₀=a` and
force `m₀=a=b=c=d=f=1/6` — the uniform measure on `S₃`, whose pair flips are `1/2 > 1/3`.

**H5 — the sharpest BRANCH-FREE linear consequence of realisability is an INEQUALITY, not the
equality.** With `e = ` identity a linear extension of `P`, each pair `x<y` is either comparable
(`J_k(y,x) = 0 ∀k`) or incomparable (`J_k(x,y) = J_k(y,x) ∀k`). Both cases satisfy
**`J_k(y,x) ≤ J_k(x,y)`**, which is therefore valid for every poset and needs no case split.

**H6 — that surrogate buys NOTHING at `n = 3`, by hand.** `m₀ = 1/3`, `a = b = c = d = 1/6`,
`f = 0` is feasible for the flip caps, satisfies all six surrogate inequalities *and* all three
sound aggregate ones, and has `E[inv] = 1 = C(3,2)/3`. The baseline optimum survives.

**H7 — `mg-6bc2`'s optimisers are SUB-PROBABILITY measures and its adjacency diagnostics are
computed on them.** Its LP carries `Σ μ ≤ 1`; the returned `n = 3` support is
`{(0,2,1): 1/3, (1,2,0): 1/3}`, total mass `2/3`. Completing to a measure by the only choice
that changes no objective value — `1/3` on the identity — turns its reported `n = 3` **aggregate**
count from `0` to `4`, because the identity contributes `J(0,1)` and `J(1,2)` and nothing
contributes `J(1,0)`.

**H8 — with `Σ μ = 1` the aggregate EQUALITY form already bites at `n = 3`, by hand.** Value `1`
needs all three flip caps tight, which forces `b = d` and `a = c`; the aggregate equalities then
reduce to `m₀ = f`, total mass gives `m₀+a+b = 1/2`, and the first flip cap gives `m₀+a+b = 1/3`.
Contradiction. So the aggregate optimum under `Σ μ = 1` is **strictly below `1`** at `n = 3`.

---

## 1. Predictions

Scored `HELD` / `REFUTED` in `OUTCOMES.md`, kept as written either way.

| # | prediction | why I believe it |
|---|---|---|
| **P1** | Baseline LP (`Σ μ = 1`, flips `≤ 1/3`, no symmetry) returns `C(n,2)/3` exactly at `n = 3,4,5,6`, i.e. `ε_spec = n/(n+1)`. | Control. Reproduces `mg-6bc2`'s theorem on an independently written solver. If this fails, nothing else here is readable. |
| **P2** | The **sound branch-free surrogate** `J_k(y,x) ≤ J_k(x,y)` buys **NOTHING** at every `n` tested — value stays `C(n,2)/3`. | H6 gives `n = 3`. The surrogate only forbids *backward-heavy* adjacency, and mass can always be shifted onto forward-heavy permutations without touching the flip caps. |
| **P3** | The sound **aggregate** surrogate `J(y,x) ≤ J(x,y)` also buys nothing at every `n` tested. | Strictly weaker than P2's constraint set. |
| **P4** | The **disjunctive** (per-pair comparable-or-symmetric) per-slot value is **strictly below** `C(n,2)/3` at every `n ≥ 3`. | This is the real content: the information lives in the *non-convexity*. Hand-checked at `n = 3` — see P5. |
| **P5** | At `n = 3` the disjunctive per-slot value is exactly **`2/3`**, attained on the branch where `{0,2}` is comparable and `{0,1}`, `{1,2}` are incomparable, giving `ε_spec = 1/2` against the baseline `3/4`. | Hand-solved: that branch forces `b = a = m₀ = 1/3`, all three flip caps satisfied, `E[inv] = 2/3`. I have **not** checked the other seven branches by hand, so "exactly" is the prediction and `≥ 2/3` is the part I know. |
| **P6** | The disjunctive value with the **aggregate** symmetry (instead of per-slot) is **strictly larger** than the per-slot one at some `n ≤ 5` — i.e. `mg-6bc2`'s aggregate/per-slot distinction survives being made sound. | Per-slot is strictly stronger pointwise. But it could still be inert; I am predicting it is not. |
| **P7** | The **control** — disjunctive branching with **no** symmetry constraint at all — returns exactly `C(n,2)/3`. | `{q = 0} ∪ {q ≤ 1/3} = {q ≤ 1/3}`; the branching alone must buy zero, or my gain is an artefact of the branch structure rather than of symmetry. This is the single most important control in the instrument. |
| **P8** | The literal per-slot EQUALITY LP is **infeasible at `n = 3`** (H4) and **feasible at `n = 4` and `n = 5`**, with a value strictly below `C(n,2)/3`. | `n = 4` has 24 unknowns against 18 equations, `n = 5` has 120 against 40; the equation count stops binding fast. |
| **P9** | The literal aggregate EQUALITY LP is feasible at `n = 3` with value strictly between `2/3` and `1`. | H8 kills `1`; nothing I know kills feasibility. |
| **P10** | The disjunctive per-slot value, as a fraction of `C(n,2)/3`, does **not** fall as `n` grows over `n = 3,4,5` — the gain does not compound. | Sizing discipline. `ε_spec = 3·d·q̄·n/(n+1)`; Daniel's `1/6` needs a factor `6` and closing the wall needs `50`. I expect a factor near `3/2`, i.e. a **milestone, not a wall-breaker**, and I am predicting in advance that this document must say so. |
| **P11** | `n = 6` will be reached for the branch-free LPs and **not** for the disjunctive one (`2^15 = 32768` exact-rational LPs over 720 columns). What is not computed will be declared, not quietly dropped. | Arithmetic. |

## 2. My two most likely errors, filed in advance

**P12 — that I convince myself the disjunctive LP is "poset enumeration" in disguise and either
refuse it (losing the whole finding) or run it while pretending the question does not arise.**
It is not: no poset is constructed, transitivity is never imposed, and each branch is a set of
*measures on `S_n`*. But the branch index set is `2^C(n,2)`, which is the same shape as a
comparability-pattern sweep, and the honest move is to say so out loud and say why the ticket's
refusal is not violated — not to hope nobody notices.

**P13 — that I report the disjunctive value as "what per-slot adjacency symmetry buys" when part
of it is bought by the branch structure.** P7 is the control that separates them and it must be
run and reported *whatever it says*. If P7 comes back below `C(n,2)/3`, my headline is wrong and
the whole gain is mis-attributed.

## 3. Declared out of scope before starting

No `L4`, no `C₃`, no `ε_dem`. No poset enumeration and no transitivity closure. No computation of
what **full** realizability buys. No re-derivation of `mg-92e6`'s symmetry lemma, `mg-210d`'s
master bound, or Diaconis–Graham. The `.tex` sources are not opened.
