# How far a constraint-pruned search for a frozen counterexample can reach — `mg-abe8`

**Verdict, plainly, because the ticket asked for it plainly: THE STRUCTURAL CONSTRAINTS DO NOT
PRUNE ENOUGH, AND THE COMPUTER-CHECKING FINISH DOES NOT FIRE AT ANY TARGET `n` A BOUND WOULD
PLAUSIBLY LEAVE.** The reach of an exhaustive constraint-pruned search is `n ≈ 13` on this box,
`n ≈ 15` on a serious cluster, `n ≈ 17` on a national-scale allocation, and `n ≈ 19` if every CPU
on Earth ran for a decade. The literature is at `n = 14`. The four structural constraints a
minimal counterexample is known to satisfy — rigid, width ≥ 3, an element incomparable to ≥ 7
others, primitive — together buy **`0.07` bits at `n = 20` and `0.00` bits at `n = 36`**, which is
**one hundredth of one element** of reach.

**Kind: `FP` at `n ≤ 9` (exhaustive), sampled above, and a COST MODEL throughout.** No claim here
is `U`. The model's one external check is that it independently reproduces the literature's actual
frontier at `n = 14–16`.

Instrument: [`code/search_reach_abe8/`](../code/search_reach_abe8/). Predictions committed at
`b6e17e8` before any script existed; scored in
[`OUTCOMES.md`](../code/search_reach_abe8/OUTCOMES.md) at 10 HELD / 3 MISSED, with four defects of
my own kept in the source.

---

## 0. What changed under this ticket while it ran, and what did not

The ticket was written to test the unexamined premise in Daniel's finishing step
(2026-08-07 19:34): *"Any upper bound could be decisive bc it could allow us to use other
techniques like computer checking etc to finish off the conjecture."* The premise being tested is
**that the resulting finite window can actually be checked**.

**`mg-00a1` returned mid-run and removed the window entirely**: the disjunctive per-slot value is
`Θ(n²)`, superlinear, so there is no bound of the form `c·n + O(1)` on that route and hence no
finite window (pm-onethird, 2026-08-07 20:12). This document is therefore written the way
pm-onethird asked and the way it should have been written anyway: **reach as a function of target
`n`**, useful for any future bound from any route, and useful on its own for the question of
extending this corpus's `n = 14` verification. The old window ends `34 / 98 / 398` appear once, in
[`s4/H`](../code/search_reach_abe8/out_s4_reach.txt), marked **illustrative and not live**.

Nothing measured moved. The instrument was already parameterised by target `n`.

---

## 1. The answer, as a function of target `n`

Work is measured in **elementary operations** — cells of the dynamic program that certifies one
candidate non-frozen. The model is

> `WORK(n) = N(n) × c(n) / 2^(pruning bits)`

with `N(n)` the candidates to visit, `c(n)` the cost of rejecting one, and the pruning
**measured**, not assumed. Every conservatism in it runs toward making the search look *more*
feasible.

| target `n` | `log₂ N(n)` | `log₂ c(n)` | pruning | `log₂ WORK` | in powers of 10 |
|---|---|---|---|---|---|
| 13 | 34.98 | 11.38 | 0.57 | **45.79** | `10^13.8` |
| 14 | 40.28 | 11.95 | 0.67 | **51.56** | `10^15.5` |
| 15 | 45.96 | 12.50 | 0.46 | **58.00** | `10^17.5` |
| 16 | 51.99 | 13.05 | 0.25 | **64.79** | `10^19.5` |
| 18 | 65.16 | 14.13 | 0.16 | **79.14** | `10^23.8` |
| 20 | 79.79 | 15.20 | 0.07 | **94.92** | `10^28.6` |
| 25 | 122.75 | 17.80 | 0.02 | **140.53** | `10^42.3` |
| 34 | 223.07 | 22.35 | 0.01 | **245.42** | `10^73.9` |
| 50 | 474.43 | 30.21 | 0.00 | **504.64** | `10^151.9` |
| 98 | 1789.12 | 53.09 | 0.00 | **1842.21** | `10^554.6` |

and against named machines:

| budget | ops | **reach** |
|---|---|---|
| this 10-core box, 24 h, optimal C at `10⁹` cell-ops/s/core | `2^49.6` | **`n = 13`** |
| a 1000-core cluster for a month | `2^61.2` | **`n = 15`** |
| `10⁶` cores for a year — larger than any computation ever run on this problem | `2^74.7` | **`n = 17`** |
| every CPU on Earth for a decade (`~10²⁸` ops) — a ceiling, not a machine | `2^93` | **`n = 19`** |
| the Sun's entire output over the age of the universe at the Landauer limit (`~5×10⁶⁴` ops) | `2^215` | **`n = 31`** |

**Read the last row twice.** It is not a machine; it is the physics. Even spending the Sun on it,
an exhaustive constraint-pruned search does not reach `n = 34`.

### The model is calibrated against the one external fact available

`1/3–2/3` is verified to `n = 14` (`mg-33f5`; `n = 12` refereed). That number came from a real
computation with real cleverness, and it is the only check this model has. The model says `n = 14`
costs `0.11` core-years and `n = 16` costs `1016` core-years — i.e. it puts the single-machine
frontier at `n = 14–16`. **The literature is at `n = 14`.** The model is calibrated, and if
anything optimistic.

---

## 2. Which constraint prunes hardest — and why the question has no useful answer

The four, with their sources as recorded in `mg-5998`. **`mg-5998` is still `available` (unlanded)
and declares its own attributions unverified except Peczarski 2008; I verified none of them and
did not need to — a constraint that does not prune does not prune whether or not it is correctly
attributed.**

⚠️ **`rigid` here is the literature's `Aut(P) = 1`, NOT `STATE.md:169`'s "extremal rigidity"**,
which is a statement about the value set `δ` takes. `mg-5998` is right that landing the word bare
is wrong; every operative sentence below says `Aut(P) = 1`.

**Pruning is `−log₂(surviving/total)` and nothing else.** The inverted form reports `19.93` bits
where the correct one reports `1.4×10⁻⁶`; it was filed as my most likely error before any code
existed (`PREDICTIONS` P14) and selftest NC1 exhibits it.

### Exhaustive, `n = 2..9` — every one of the four is WEAKER at `n = 9` than at `n = 6`

| constraint | bits at `n = 6` | bits at `n = 8` | bits at `n = 9` | direction |
|---|---|---|---|---|
| `Aut(P) = 1` (Peczarski 2017, unverified) | 1.640 | 1.310 | **1.131** | weaker |
| width ≥ 3 (Linial 1984, unverified) | 0.388 | 0.062 | **0.018** | weaker |
| not 6-thin (Peczarski 2008, unverified) | ∞ | 3.055 | **1.327** | weaker |
| primitive (`STATE.md:47`) | 0.789 | 0.441 | **0.323** | weaker |
| **all four together** | ∞ | 4.727 | **2.591** | weaker |

### KR-model, `n = 10..40` — the trend does not turn, it completes

| `n` | rigid | width ≥ 3 | not 6-thin | primitive | **all four** | bits |
|---|---|---|---|---|---|---|
| 10 | 31.75 % | 100 % | 99.75 % | 100 % | 31.75 % | 1.66 |
| 16 | 84.00 % | 100 % | 100 % | 100 % | 84.00 % | 0.25 |
| 20 | 95.25 % | 100 % | 100 % | 100 % | 95.25 % | **0.07** |
| 28 | 99.50 % | 100 % | 100 % | 100 % | 99.50 % | 0.01 |
| 40 | 100.00 % | 100 % | 100 % | 100 % | 100.00 % | **0.00** |

*(Kleitman–Rothschild sampling, 400 per size. A **model**, not the uniform measure; KR prove it
captures a `1−o(1)` fraction of posets but converges slowly, so these are **directional**. They
agree in direction and order of magnitude with the exhaustive census where the two overlap.)*

### So: 6-thinness prunes hardest, and that is the finding, not a consolation

Of the four, "some element incomparable to ≥ 7 others" is strongest wherever it is not vacuous —
`3.055` bits at `n = 8` against rigidity's `1.310`. **And it is the one that decays fastest.** At
`n = 8` it forces `P = 1 ⊔ Q`, so exactly `2045` of `16999` survive. At `n = 16` every KR poset
already satisfies it, because the middle antichain has `~n/2 ≥ 8` mutually incomparable elements.

> **The constraints prune hardest exactly where the search is already feasible, and vanish exactly
> where it is not.** That is not an accident of these three. Rigidity, width ≥ 3 and non-6-thinness
> are all **almost-sure properties of a random poset**, and an almost-sure property prunes `o(1)`
> bits *by definition*. Any constraint of that category is worth zero to a search, however deep the
> theorem behind it.

---

## 3. Frozen-ness cannot prune the search tree, and that is a proof

The ticket's own hypothesis was that emptiness of the frozen class might be a strong pruning
signal: *"if frozen-ness prunes as hard at `n = 20` as it appears to at `n ≤ 14`, the reachable
range may be far larger than naive enumeration suggests."*

**It is not a pruning signal, and the reason is structural rather than empirical.**

Every enumeration of posets that is feasible at all builds size `n` from size `n−1` by adjoining a
maximal element (its strict down-set is an order ideal). *Pruning means discarding a parent.* But
`P` is a **minimal** counterexample, so every proper induced subposet of `P` — in particular `P`
minus a maximal element — **satisfies** the conjecture and is **not frozen**. The parents of the
object being hunted are precisely the non-frozen posets. And the frozen class is empty at every
`n` reachable, so *the non-frozen posets are all of them*.

**Frozen-ness discards exactly zero parents, by the definition of minimality.** The property is
*anti-hereditary* in the only direction a search could use.

Measured confirmation of the two halves, at `n ≤ 8` exhaustively:

| `n` | posets | frozen | `δ = 1/3` exactly | min `δ` over non-chains |
|---|---|---|---|---|
| 5 | 63 | 0 | 3 | `1/3` |
| 6 | 318 | 0 | 5 | `1/3` |
| 7 | 2045 | 0 | 8 | `1/3` |
| 8 | 16999 | 0 | 12 | `1/3` |

The population sits **on** the threshold at every `n` and never crosses it. That is why "the frozen
class is empty" is not a filter: a filter that rejects nothing is not a filter.

### And it does not even prune at `n = 20`, in the other sense either

Tested directly on KR-model posets in exact rationals, `n = 10..28`:

| `n` | samples | frozen | min `δ` | **mean incomparable pairs examined before rejection** |
|---|---|---|---|---|
| 14 | 200 | 0 | 0.3333 | 1.16 |
| 20 | 80 | 0 | 0.3363 | **1.02** |
| 24 | 30 | 0 | 0.3895 | **1.00** |
| 28 | 30 | 0 | 0.4210 | **1.00** |

A typical poset at `n = 28` is certified non-frozen after examining **one** incomparable pair out
of the `~n²/8 ≈ 98` it has. **Frozen-ness is a cheap TEST, not a strong FILTER**, and those are
different quantities: a cheap test makes each visit cheap, but does not remove a single candidate
from the list of visits. Only removing candidates buys reach.

Note also that `min δ` **rises** with `n` in this population (`0.333 → 0.421`). The KR-typical
poset gets *further* from the threshold as `n` grows. A counterexample, if one exists, is
atypical — which is exactly why the KR figures are the right ones for **cost** (they describe the
bulk that a search must grind through) and the wrong ones for **existence**.

---

## 4. What dominates the cost, and the part every naive estimate drops

Two factors, and only the first is usually counted.

**(a) `N(n)`, the number of candidates.** `A000112`, re-derived here to `n = 9` and quoted to
`n = 16`. `log₂ N(n) = n²/4 + 3n/2 + O(log n)` (Kleitman–Rothschild). The instrument uses a
**conservative** extrapolation above `n = 16` — a linear fit to `g(n) = log₂(N(n)/N(n−1))` with
slope `0.365`, against the true asymptotic slope `1/2` — because it *understates* `N(n)` and
therefore flatters the search.

**(b) `c(n)`, the cost of rejecting one candidate — exponential, and routinely omitted.** Deciding
`δ(P) ≥ 1/3` means counting linear extensions, which is `#P`-complete (Brightwell–Winkler 1991;
recalled, not verified here). The exact method available is the down-set DP. Its cost is **not**
`Θ(2ⁿ)` — the marginals need `e(S)` only for ideals and filters, both closed under deleting a
maximal element, so a memoised recursion touches `2 × #ideals` subsets. Measured on KR posets:

> `log₂ #ideals(n) = 0.4564 n + 1.749` (least squares, `n = 12..40`, max residual `0.108` bits)

so `#ideals` is `~2^17` at `n = 34` against `~45` at `n = 9`. **That is `22.35` bits of
per-candidate cost at `n = 34`, worth about 1.8 elements of reach on its own** — three orders of
magnitude that a "posets per second" estimate drops on the floor.

**What does *not* help.** Early exit — stopping at the first balanced pair instead of computing
`δ` — saves a measured `2.6×` at `n = 4` rising to `10.5×` at `n = 9`. A constant factor of ten is
**1.3 elements** at `n = 20`. It does not touch the exponential, because the DP producing the
marginals is the cost whether one pair is examined or all of them.

---

## 5. The exchange rate — what a future structural result would be worth

This is the number to keep. A pruning of `b` bits buys `Δn = b / g(n)` extra elements.

| `n` | `g(n)` | bits for **+1** element | bits for **+5** | what a 99.9 %-discarding constraint buys |
|---|---|---|---|---|
| 14 | 5.31 | 5.3 | 26.5 | **+1.88** elements |
| 20 | 7.50 | 7.5 | 37.5 | **+1.33** elements |
| 34 | 12.61 | 12.6 | 63.0 | **+0.79** elements |
| 98 | 35.97 | 36.0 | 179.8 | **+0.28** elements |

**A constraint that discards 999 posets out of every 1000 buys under two elements of reach, and
under one element above `n ≈ 30`.** For comparison, the four literature constraints together
deliver `0.07` bits at `n = 20` — `+0.01` elements. One hundredth of one.

And the inverse, which is the operative form: to bring a target inside even the *physical* ceiling
(`2^215` ops), a future result would have to supply

| target `n` | `log₂ WORK` | pruning required | surviving fraction |
|---|---|---|---|
| 34 | 245.4 | **30.5 bits** | 1 in `2^30` |
| 50 | 504.6 | **289.7 bits** | 1 in `2^290` |
| 98 | 1842.2 | **1627.3 bits** | 1 in `2^1627` |

> A theorem delivering hundreds of bits is not a constraint; it is a **classification**. It would
> have to collapse the population from `2^(n²/4)` to something sub-quadratic in the exponent. That
> is a categorically different object from a shape constraint, and it is the only kind of result
> that would change this answer.

**So: what is a future structural result worth, for search purposes?** Nothing, unless it moves the
exponent. This is a statement about search, not about mathematical value.

---

## 6. The one thing that is actually cheap, and it is not a finish

Filed in advance as `PREDICTIONS` P11 so it cannot be claimed as a discovery.

The failure above is specific to **certifying absence**. Everything in §1–§5 is about exhausting a
space, because that is what "no counterexample at `n`" requires. A **satisfiability** hunt is a
different problem: CP/SAT/local search for *one* frozen poset at `n = 15..40`, never exhausting
anything, is not governed by `N(n)` at all and is cheap by comparison.

Two honest riders, because this is the part most likely to be over-read:

1. **It cannot finish the conjecture.** Daniel's step needs *absence*, and absence is the UNSAT
   direction — precisely the one that requires exhausting the space. A refutation hunt that finds
   nothing tells you nothing.
2. **It has a real obstruction of its own.** `δ(P) < 1/3` is a ratio of linear-extension counts and
   is `#P`-hard to evaluate, so it has **no compact propositional encoding**. A solver cannot
   propagate on it; each candidate costs a full `Θ(#ideals · n)` evaluation. That rules out
   off-the-shelf SAT and points at local search or CP with the count as an oracle.

Still: it is the only route in this area whose cost is not `2^(n²/4)`, and §3's measurement makes
it cheaper than it looks — one incomparable pair suffices to reject a typical candidate. **If
anyone is going to spend polecats on searching, spend them there.** Per the ticket, I am not
starting one; this is the mail, not the search.

---

## 7. What this finding is, and what it is not

**It is:** a statement that *the computer-checking step* Daniel named cannot close a window of the
sizes anyone has contemplated, and that the structural constraints available do not change that.
It is a demonstration that the constraints do **not** prune enough, which the ticket pre-valued
equally with a positive answer, and which I am reporting plainly rather than hedged.

**It is not** a statement that an upper bound is not worth pursuing. That was filed in advance as
my second likely error (`PREDICTIONS` P15) precisely so it could be checked. A bound would still
convert an infinite problem into a finite one, make the object concrete, and license `FP`-kind
arguments over a bounded range. `mg-00a1` — which has since refuted the bound on *that route* — is
independent of everything here, and nothing in this document bears on whether some other route can
prove one.

**Nor is it** a claim about the mathematical value of rigidity, width ≥ 3 or non-6-thinness. Those
are real theorems about the shape of a minimal counterexample and `mg-5998` is right that this
corpus should record them. They are worth `0.07` bits *to a search*, and that is a narrow claim
about one use.

## 8. Boundaries, stated rather than implied

- **`n ≤ 9` is exhaustive; everything above is a model.** `n = 10..40` figures are
  Kleitman–Rothschild sampling with 400 samples per size (30–80 for the `δ` measurements above
  `n = 20`). Directional.
- **None of `mg-5998`'s four attributions is verified**, here or there. Used as given, marked
  UNVERIFIED at every site including in code.
- **The KR rigidity test is the layer-preserving one.** A layer-swapping automorphism would be
  missed, which would report *more* rigid posets and hence *less* pruning — the direction that
  flatters this document's conclusion. The necessary condition for one held on `78 of 4000`
  samples, bounding the residual at `2 %`, which cannot move a `0.00`-bit figure.
- **`c(n)` charges no big-integer arithmetic**, and the extrapolation of `N(n)` uses the slower of
  two growth models. Both conservatisms run toward feasibility.
- **No search was run**, per the ticket. The largest computation here is the exhaustive `n ≤ 9`
  census: 183,231 posets, 174 s, one core. Total instrument wall-clock under 7 minutes, single
  process, no fan-out.
- **Not attempted:** `n = 10` exhaustively; exact `δ` above `n = 8` exhaustively; any verification
  of Brightwell–Winkler, Kleitman–Rothschild or Brightwell–Felsner–Trotter, all of which are
  recalled and used as literature; any edit to `STATE.md` or the ledger — this document is a
  finding, and whether it earns a row is pm-onethird's call.
