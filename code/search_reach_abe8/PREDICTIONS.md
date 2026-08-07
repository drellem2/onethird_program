# `mg-abe8` — predictions for the **REACH OF A CONSTRAINT-PRUNED SEARCH**

**Committed before any script of this instrument exists.** Nothing below has been run *by this
instrument*. The hand measurements in §0 were made before any prediction was written, with the
existing `code/counterexample_probe_24a3/core.py` enumerator and with arithmetic, and they are
disclosed here as **measurements** rather than laundered into predictions — because three of them
(H4, H5, H6) already decide the ticket, and saying so in advance is the only honest way to file
predictions on a question I can already see the shape of.

The ticket asks: *how far can a targeted search for a frozen counterexample actually reach, and
what dominates the cost?* It explicitly permits — and pre-values equally — a **negative** answer.
I am predicting a negative answer, and §0 says why I already believe it, so that P1–P13 are not
read as discoveries.

**Constraints used, and their source.** `mg-5998` is **still `available`** — it has not landed, so
I take its list directly and attribute it to `mg-5998`'s own citations, which `mg-5998` itself
declares are **not independently verified** (only Peczarski 2008 is). I have verified **none** of
them and I do not need to: my finding is that they do not prune, and a constraint that does not
prune does not prune whether or not it is correctly attributed. The four I use:

| constraint | source as recorded in `mg-5998` | verified by me |
|---|---|---|
| **rigid** — `Aut(P) = 1` | Peczarski 2017 | no |
| **width ≥ 3** | Linial 1984 | no |
| **not 6-thin** — some element incomparable to ≥ 7 others | Peczarski, *Order* 25 (2008) 91–103 | no |
| **primitive** — incomparability graph connected | this corpus, `STATE.md:47` (row 2) | no (it is a `U`-row here) |

⚠️ **`rigid` is the literature's `Aut(P) = 1`, NOT `STATE.md:169`'s "extremal-rigidity".**
`mg-5998` §"two word collisions" is right that landing the word bare is wrong, and this document
uses `Aut(P) = 1` in every operative sentence for exactly that reason.

`frozen` throughout is `STATE.md:46`'s: `δ(P) < 1/3`, every incomparable pair `>2/3`-decided.

---

## 0. Hand measurements, disclosed (made before any prediction below was written)

**H1 — the corpus's own enumerator reaches `n = 9` in 52 s and that is where Python stops.**
Run just now against `code/counterexample_probe_24a3/core.py` (`all_posets_by_extension`,
unmodified, not my code): `n = 7 → 2045` (0.3 s), `n = 8 → 16999` (3.7 s), `n = 9 → 183231`
(52 s). The step ratio is ~14× in count and ~14× in time, so `n = 10` is ~12 min and several GB
and `n = 11` is ~3 h. **This is the actual machine cost of the thing the ticket is about, measured
rather than assumed, and it is the calibration point for everything downstream.**

**H2 — the population is A000112 and I have re-derived it independently to `n = 9`.** The
enumerator's counts `2, 5, 16, 63, 318, 2045, 16999, 183231` agree with the recalled OEIS A000112
at every `n ≤ 9`. Above that I am *quoting* A000112 (`n = 10..16`:
`2567284, 46749427, 1104891746, 33823827452, 1338193159771, 68275077901156, 4483130665195087`)
and have **not** verified those terms. They are used only for the growth rate, and the growth rate
is confirmed independently by Kleitman–Rothschild (`log₂ N(n) = n²/4 + 3n/2 + O(log n)`), so a
transcription error in one term would not move the conclusion.

**H3 — the growth is ~`0.365` bits per element per element, and it is still ACCELERATING at
`n = 16`.** With `g(n) = log₂(N(n)/N(n−1))`: `g(12..16) = 4.563, 4.936, 5.306, 5.673, 6.037`.
Second differences: `0.373, 0.370, 0.367, 0.364`. The asymptotic value of `g′` is `1/2` (KR), so
**a linear extrapolation of `g` with slope `0.365` UNDERSTATES `N(n)` for every `n > 16`** — I use
it deliberately, because it is the extrapolation most favourable to a search succeeding, and my
conclusion is that a search fails.

**H4 — FROZEN-NESS CANNOT PRUNE THE SEARCH TREE, AND THIS IS A PROOF, NOT A MEASUREMENT.**
Every enumeration of posets on `n` elements that is feasible at all builds them from posets on
`n − 1` elements (delete a maximal element; its down-set is an order ideal — this is exactly
`all_posets_by_extension`). Pruning means discarding a parent. But `P` is a **minimal**
counterexample, so **every** proper induced subposet of `P` — in particular `P` minus a maximal
element — **satisfies** the conjecture and is **not** frozen. The parents of the object we are
hunting are precisely the non-frozen posets. And the frozen class is empty at every `n` this
corpus can enumerate, so *the non-frozen posets are all of them*. **The target property prunes
exactly zero parents, by the definition of minimality.** This is why "the frozen class is empty at
every `n` we can reach" — the ticket's stated hypothesis — is **not** the pruning signal it looks
like: emptiness at level `n−1` is not a filter on level `n−1`, it is the statement that the filter
passes everything.

**H5 — THE 6-THINNESS CONSTRAINT IS STRONGEST EXACTLY WHERE THE SEARCH IS ALREADY FEASIBLE AND
VACUOUS EXACTLY WHERE IT IS NOT.** "Some element incomparable to ≥ 7 others" needs `n ≥ 8`. At
`n = 8` it forces an element incomparable to *all* seven others, i.e. `P = 1 ⊔ Q` with `Q` any
poset on 7 elements, so **exactly `2045` of `16999` survive — `12.03 %`, a pruning of `3.05`
bits.** At `n = 34` the Kleitman–Rothschild typical poset has a middle antichain of `~17`
elements, every one of which is incomparable to `~16` others, so the constraint is satisfied by
almost every poset and prunes `→ 0` bits. **The pruning runs the wrong way in `n`.** By hand I
expect the same of the other three: rigidity, width ≥ 3 and primitivity are all *almost-sure*
properties of a random poset (KR), so each prunes `o(1)` bits asymptotically.

**H6 — THE PRUNING/REACH EXCHANGE RATE IS `g(n)` BITS PER ELEMENT, AND IT IS BRUTAL.** A pruning
factor of `2^b` buys `Δn = b / g(n)` extra elements. At `n = 15`, `g = 5.67`, so **a constraint
that discards 99.9 % of the population (`b = 10`) buys under two elements**, and a constraint that
discards all but one poset in a million (`b = 20`) buys **three**. This single line is, I think,
the whole answer to "which constraint prunes hardest" — the question has no interesting answer
because *no constraint expressible as a density can matter*. Only a constraint that changes the
**exponent** — collapsing `2^{n²/4}` to `2^{O(n log n)}` — moves the reach, and that is a
classification theorem, not a shape constraint.

**H7 — THE PER-CANDIDATE COST IS ITSELF EXPONENTIAL AND IS OMITTED FROM EVERY NAIVE ESTIMATE.**
`δ(P)` is a ratio of linear-extension counts. Counting linear extensions is `#P`-complete
(Brightwell–Winkler 1991 — recalled, not verified). The corpus's own method is the down-set DP,
whose cost is `Θ(#ideals(P) · n)`; a KR-typical poset has a middle antichain of `n/2`, so
`#ideals ≥ 2^{n/2}`. **Per-candidate cost therefore rises from `~10²` operations at `n = 9` to
`≥ 2^{17} ≈ 10⁵` at `n = 34`** — three to four extra orders of magnitude that a "posets/second"
estimate silently drops.

**H8 — the two windows are `15..34`, `15..98`, `15..398`.** The lower end is `15` (verified to
`n = 14`, `mg-33f5`; the ticket says so), not `1`. I note this because "the window is `n ≤ 34`"
reads as 34 cases and is 20.

---

## 1. Predictions

Scored HELD / MISSED / UNRESOLVED in `OUTCOMES.md` after the instrument runs.

**P1.** All four literature constraints have surviving fraction **increasing** in `n` over the
exhaustive range `n = 6..9` — i.e. every one of them prunes **less** at `n = 9` than at `n = 6`.
*(Confidence: high for 6-thinness by H5; moderate for the other three.)*

**P2.** The **joint** surviving fraction of all four constraints together, at `n = 9`, is **above
5 %** — i.e. the four literature constraints together prune **under 4.4 bits**, hence under
`4.4/3.43 ≈ 1.3` elements of reach at `n = 9`.

**P3.** Rigidity (`Aut(P) = 1`) prunes **less than 1.0 bit** at `n = 9` and its pruning is
**decreasing** in `n`.

**P4.** Primitivity prunes **less than 1.0 bit** at `n = 9`, and its surviving fraction is
`1 − Θ(2^{1−g(n)})`, i.e. `→ 1`. Concretely I predict the ordinal-decomposable fraction at `n = 9`
lies in `[3 %, 12 %]`.

**P5.** Width ≥ 3 prunes **less than 0.1 bit** at `n = 9`.

**P6.** 6-thinness is the **hardest-pruning of the four at every `n` where it is not vacuous**,
and is nonetheless the one whose pruning **decays fastest** — it prunes `3.05` bits at `n = 8`
(hand-measured, H5) and I predict **under `2.0` bits at `n = 9`**.

**P7 (the headline).** With the conservative (`slope 0.365`) growth model, the number of
candidates a **constraint-pruned** search must visit at `n = 34` exceeds `2^{200}`. I predict the
computed figure lands in `[2^{215}, 2^{235}]`.

**P8.** The **reach**, defined as the largest `n` whose pruned candidate count is under a stated
budget:
- `10¹³` visits (a dedicated multi-core month at `10⁶`/s): **`n = 13` or `14`**;
- `10¹⁹` visits (`10⁵` cores × 1 year × `10⁷`/s — a national-scale allocation): **`n = 17` or
  `18`**;
- `10²¹` visits (a deliberately absurd ceiling): **`n = 18` or `19`**.

**P9.** Consequently the reach at the *absurd* ceiling falls short of the **near** end of the
smallest window (`n = 34`) by **more than 100 bits** — a shortfall no engineering can close. I
predict the computed shortfall from `10²¹` visits to `n = 34` lies in `[140, 180]` bits under the
conservative model.

**P10 (pre-committed verdict).** **DANIEL'S FINISHING STEP DOES NOT FIRE at any of `34`, `98`,
`398`.** The constraints do **not** prune enough, and they do not prune enough by a margin of
tens of orders of magnitude rather than a margin that better code could close. I am filing this
as a prediction rather than a finding so that it can be scored, and I will report it in the
ticket's own words — *plainly*, not hedged.

**P11 (the one thing that could rescue it, pre-committed so I cannot claim it as a discovery
afterwards).** The failure is specific to **certifying absence**. A *satisfiability* hunt — a
CP/SAT/local search for one frozen poset at `n = 15..40`, never exhausting the space — is **not**
governed by `N(n)` and is cheap by comparison. It cannot finish the conjecture (absence is what
Daniel's step needs) but it is a live and under-costed **refutation** route. I predict I will
recommend it, and that it is the only actionable positive in this ticket.

**P12.** The per-candidate cost `#ideals` for a KR-model poset at `n = 34` exceeds `2^{17}`, and
including it moves the reach figures of P8 **down by at least one element** at the two larger
budgets.

**P13.** `mg-5998` will still be `available` (unlanded) when I submit, so the constraint table
above will be the corpus's first record of these four in one place — but **as an input I did not
verify**, and I will say so at the site rather than in a boundary section.

---

## 2. My two most likely errors, filed in advance

**P14 — I CONFLATE "THE EXCLUDED SET IS A VANISHING FRACTION" WITH "THE CONSTRAINT PRUNES `n/2`
BITS".** This is a real trap and I nearly fell into it while writing H5. Ordinal-decomposable
posets are a `~2^{1−g(n)}` fraction of all posets; it is tempting to write "primitivity prunes
`g(n) − 1` bits", which is **backwards**. Pruning in bits is `−log₂(fraction SURVIVING)`, and when
the excluded set vanishes the pruning is `≈ 0`, not large. **Every pruning figure in this
instrument must be computed as `−log₂(surviving/total)` and I bind myself to that formula now, in
writing, before any script exists.** If a number in the output is not of that form it is wrong.

**P15 — I SCORE "THE SEARCH IS INFEASIBLE" AS "THE UPPER-BOUND PROGRAMME IS WORTHLESS".** These
are different claims and the second does not follow. An upper bound converts an infinite problem
into a finite one, which is worth having for reasons other than immediate checkability (it makes
the object concrete, it may be improvable, it licenses `FP`-kind arguments over a bounded range).
My verdict is about **Daniel's stated finishing step**, i.e. *"use computer checking to finish off
the conjecture"* — and that step, specifically, is what I am predicting does not fire. If the
report anywhere says the bound is not worth pursuing, that is this error and it should be scored
as a MISS even if every number is right. `mg-00a1` is the bound and is **independent of this
ticket** (mayor's dispatch note, 2026-08-07 20:53); nothing here bears on whether it is provable.

---

## 3. What this instrument will NOT do

- **It will not run a large search.** The ticket forbids it; the whole point is that the search is
  the thing being costed. Exhaustive enumeration stops at `n = 9` (52 s, H1). Everything above
  `n = 9` is a **cost model** and a **sampler**, and every figure derived from them is labelled as
  such.
- **It will not fan out.** Single process, one core, per the mayor's load note. No detached
  workers.
- **It will not attempt the growth bound.** That is `mg-00a1`, held by `p00a1`.
- **It will not assume `ε_leak = 0.20`.** Every reach figure is reported against the window range
  `34 / 98 / 398`, per the ticket.
- **It will not verify the four literature attributions.** `mg-5998` owns that and declares them
  unverified; I use them as given and mark them `U`-by-citation-unverified at the site.
