# `code/image_closure_3da1/` — what `mg-c776`'s image result closes, and what it does not

Deliverable: [`docs/OneThird-ImageClosure-mg-3da1.md`](../../docs/OneThird-ImageClosure-mg-3da1.md).

Subject: this work item's own title. `mg-3da1` was filed as `mg-c776`'s successor carrier so that
item could close, and it carries `mg-c776`'s result in a paraphrase:

> *"The image characterisation is EXACT and therefore **CANNOT TIGHTEN ANYTHING**: `conv(R_n) = M_n`
> because the image contains every vertex, so every inequality valid on the image is valid on the
> whole body."*

The clause after the colon is a theorem. The clause before it does not follow, and the
counter-measurement is in `mg-c776`'s own instrument one section along.

## 1. The three findings

| # | finding | arm |
|---|---|---|
| 1 | **The closure generalises far past `R_n`.** *No* restriction of `M_n` phrased as "`π` must be realizable" can lower a linear ceiling — for **any** class of measures containing the point masses — because `π(δ_σ) = δ_σ` is a vertex. **Realizability is vacuous at the vertices.** Four different restrictions, same obstruction | `d1` |
| 2 | **The direction sweep that guards this has no power.** `c2.2`'s `0 separations` is `c2.1` restated: a linear functional is maximised at a vertex and every vertex is in the image, so no direction can separate *at any sample size*. Put to a world where a separation exists, the same sweep detects it at a rate tracking `1/n!` | `d2` |
| 3 | **THE CORRECTION — the image *does* tighten, by exactly `d`.** Inside the convex cell of hypothesis (1) read on the *measure*, the image ceiling is `m/3` against the body's `C(n,2)/3`, a ratio of exactly the incomparability density `d`. At `n = 5` the image ceiling is a **fifth** of the body's | `d3` |

## 2. What separates finding 3 from finding 1

One thing, and `d1.4` measures it: **whether the restriction excludes a vertex of `M_n`.**

- Realizability excludes **none** — every vertex is a point mass's marginal vector. Hull `= M_n`.
- Hypothesis (1) read on the **poset** excludes **none** — a total order's `δ` is a maximum over
  the empty set (`mg-c776` `c2.3`). Hull `= M_n`.
- Hypothesis (1) read on the **measure**, inside the cell `L* = identity`, excludes `n! − 1` of the
  `n!`, leaving `δ_id` alone. Hull is a proper subset, and the ceiling drops by the factor `d`.

So "cannot tighten anything" is the first two readings stated without the third beside them.

## 3. What is actually closed, stated so it stays closed

**The cut is dead, in the strongest available form.** `mg-c776`'s ticket ranked a separating
inequality first; `d1` shows no such inequality exists for *any* realizability restriction, hence
none in LP, SDP or lift-and-project form. That is a permanent closure and it is one line.

**`d` is not dead.** The image converts row 8's wall into *how large can `d` be for a frozen
poset* — residual **(R)**, already on `STATE.md`'s board and already correctly ordered.
`STATE.md` §6 records the prior honestly: a search for a frozen-conditional **upper** bound on `d`
returns zero, and every density fact on record points the other way. The line does not die; it
lands on a residual that was already there.

## 4. Controls

- **Nothing in this estate is imported.** Not `lib_c776`, not `lib8b32`, not anything under
  `code/`. A shared poset enumerator would move both readings the same way and the agreement
  would be an artifact of the shared code rather than corroboration. What the two directories
  share is OEIS A001035 and the definitions.
- **`d0` runs first and everything rests on it**: labelled poset counts against **A001035** at
  `n = 1..5` (`1, 3, 19, 219, 4231`); `e(P)` against a minimal-element recursion that never
  enumerates a permutation; the marginal against an average of vertex vectors; `r`'s idempotence
  re-checked rather than cited.
- **Planted defects, three, each put to the control that must catch it** — and **one of them came
  back inert and is printed rather than swapped out**: weakening `pos[i] < pos[j]` to `<=` changes
  nothing, because coordinates are indexed by pairs with `i ≠ j` and two elements never share a
  position. A plant has to be a defect the domain can *express*; that one is a defect the domain
  forbids, so it reports green against a correct library and says nothing about the control's
  power. The live plant reads element **labels** where it should read **positions** and collapses
  all `n!` vertices onto one.
- **Exact arithmetic throughout.** Every number here is a `Fraction`. The claims are equalities
  between rationals (`d = m/C(n,2)`, `max = m/3`) and a float comparison would turn an exact
  statement into a tolerance — fatal for a question that is entirely about whether a bound is
  *attained*.
- **`d3.1`'s population restriction is derived and then checked**, not assumed: the `n = 6` sweep
  runs over transitive subrelations of the identity chain (`2^15` instead of `3^15`), and that
  restriction is verified exhaustively against the **full** labelled population at `n = 3,4,5`.
- **Two consecutive `./run_all.sh` runs are byte-identical.** The direction sweeps use a
  hand-written LCG rather than `random.seed(...)` so the stream cannot drift between hosts.

## 5. Scope, stated rather than left to be discovered

- `n ≤ 5` exhaustive over the full labelled population; `n = 6` for `d3` only, over the derived
  chain-subrelation population. `mg-c776` reaches `n = 7` on its own boundary arm and `mg-6ff4`'s
  F23 is exhaustive to `n = 9` — **nothing here is the furthest reach of anything**, and no number
  in this directory is offered as a new boundary figure.
- **The population warning governs `d3` exactly as it governs `mg-c776` `c3`.** `δ < 1/3` is the
  counterexample condition and the conjecture is verified to `n = 14`, so the strictly frozen
  population is empty at every `n` reachable here. `d3`'s maximisers sit on the **closed boundary**,
  which is a different class from the hypothesis. `docs/FACTS.md` F1's corollary warning applies
  verbatim and no `d3` number may be quoted without it.
- **This directory corrects a paraphrase, not `mg-c776`.** That directory's own `README.md` §1
  already states the careful version — *"no fact about the image can move `eps` except through
  `d`"* — and its deliverable §3 prints the `c2.4` table under *"Where the comparison is NOT
  vacuous"*. What travelled into the work-item title was the half without the qualifier.

## 6. Provenance

`p3da1`, 2026-08-13, from `mg-3da1` — `mg-c776`'s successor carrier, filed by the mayor.
