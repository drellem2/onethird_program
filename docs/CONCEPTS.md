# CONCEPTS — how we picture the space

**What this file is.** The **mental model**: what the objects mean, how to picture them, and which
intuitions have earned their keep. Filed on Daniel's request (`mg-602d`, 2026-08-12): *"In general I
would like to hear (and we should track) conceptual gains. Perhaps even keep a succinct conceptual
document of how we see the space."* It is not a fourth home for formal status:

| file | the question it answers |
|---|---|
| [`STATE.md`](../STATE.md) | **status** — what is proven, what the target is, what has already been walked |
| [`docs/FACTS.md`](FACTS.md) | **statements** — true things, each with its kind and its exact scope |
| **this file** | **meaning** — how to *think* about the problem |

A reader of the first two learns what is true. A reader of this should learn how to think about the
problem, in one sitting. **Succinct is a requirement, not a style note:** the moment this file needs
an index it has become a second `STATE.md`, and the repair is to cut it, not to reorganise it.

**The two rules that keep it honest**, because a conceptual document is the easiest place in the
estate to accumulate confident prose that no longer matches the formal record:

1. **Every claim points at the artifact that earns it**, and formal facts are **cited, never
   restated** — a citation cannot drift and a paraphrase can.
2. **Anything not yet earned is marked `BELIEF` in the sentence itself**, not in a footnote, and
   lives in §6. A claim that points at nothing and is not a stated belief does not belong here.

[`code/concepts_gate_602d/`](../code/concepts_gate_602d/) checks the **structure** of both on every
merge — no row of §2 or §5 missing its pointer, no item of §6 missing its marker — and that the file
stays inside a declared word ceiling. It cannot check that a pointer is *right*, only that one is
*there*: the same split, for the same reason, as [`docs/FACTS.md`](FACTS.md)'s own gate.

---

## 1. The objects, in words before symbols

**The problem.** A finite poset `P` is `n` things with some pairs ordered and the rest
*incomparable*. A **linear extension** is one way of laying all `n` out in a line without
contradicting the order; `L(P)` is the set of them, always with the uniform measure. Think of sorting
under partial information: `L(P)` is the set of orders still consistent with what you know, and
asking *"is `x` before `y`?"* splits it in two. The **1/3–2/3 conjecture** says that unless `P` is
already a chain, some incomparable pair splits it nearly evenly — `p_xy ∈ [1/3, 2/3]` — so
`O(log |L(P)|)` comparisons always suffice.

**The object we argue about is a counterexample nobody has seen.** Every route assumes a *minimal*
counterexample and derives a contradiction. Such a `P` is **frozen** (every incomparable pair more
than `2/3`-decided, `δ(P) < 1/3`) and **primitive** (incomparability graph connected, i.e. not an
ordinal sum) — [`STATE.md`](../STATE.md) glossary, rows 1–2. **The frozen class is empty at every `n`
this corpus can enumerate** (the conjecture is verified through order 11 refereed, order 14 on an
unrefereed preprint; `mg-33f5`), so every measurement we take is on posets that are *not*
counterexamples. That is the standing reason a clean empirical
sweep is worth so little here, and the most useful thing to hold in mind while reading any number in
this repository.

**Why 1/3, and not 0.276 or any other constant.** Of any three elements at most two of the cyclic
events `x<y`, `y<z`, `z<x` hold in a given order, so those probabilities sum to `≤ 2` and no three
pairwise orientations can all exceed `2/3`. Below `δ = 1/3` the strong-majority relation is therefore
a tournament with **no 3-cycle**, hence transitive, hence itself a total order — the **distinguished
order `e`**. `2/3` is exactly the strong-3-cycle threshold; that is where the magic number comes
from, and it is elementary and proven ([`STATE.md`](../STATE.md) *Why 1/3 — the elementary anchor*).
Coherence with `e` is **necessary and not sufficient**, and that gap is the whole difficulty: the
abstract two-atom law coheres perfectly and has `Θ(n²)` inversions (*obstruction 4*).

**The two axes**, and the programme is the attempt to connect them:

- **Axis 1 — near-ordinal-sumness.** *How close is `P` to a stack of blocks that never interleave?*
  `λ_std`, inversion count, squared displacement, interface thinness and cross-cut entropy are **the
  same axis in different units**, tied by exact identities ([`STATE.md:17`](../STATE.md),
  *Equivalence dictionary*).
- **Axis 2 — balance / frozenness.** `δ(P) < 1/3`: the counterexample condition, a genuinely
  different axis.

⚠️ **The standing hazard is `δ` against `Δ₁`** — a balance constant on Axis 2 against the fatness of
a cut interface on Axis 1. [`STATE.md`](../STATE.md)'s glossary is devoted to that pair and is
**cited here, not duplicated**.

---

## 2. The quantities, and what each one MEANS

`STATE.md`'s glossary says what these are *defined* to be; this says what they *mean*. That is the
half that had never been written down — Daniel asked *"what is alpha?"* about a quantity central to
four work items and three mails, with the formal record complete and the conceptual one absent.

| quantity | what it means, in one sentence | pointer |
|---|---|---|
| `δ(P)` | How balanced the **most balanced** incomparable pair is — one number summarising the best question you could ask. `< 1/3` is *frozen*: every question is nearly settled already. | [`STATE.md`](../STATE.md) glossary |
| `λ_std` | How **rigid** the element→position assignment is. `= 1` exactly when `P` is an ordinal sum; it falls away from `1` as elements are free to slosh between positions. ⚠️ It is defined **relative to a chosen reference order** and moves by up to `1/3` across choices — frozen is what makes `e` canonical, so that is a hypothesis doing work, not a convention. | row 1 (`U`); [`STATE.md`](../STATE.md) glossary, `mg-c4f5` |
| `E[inv_e]` | How far a random extension typically is from the distinguished order, counted in flipped pairs. **This is the live currency of the whole programme** — a proof would be delivered in these units and merely reported in eigenvalues. | [`STATE.md:25`](../STATE.md) rider (`mg-05ec` §5) |
| `λ₂^BK` | How **slowly** the random walk on `L(P)` mixes, where a step swaps one adjacent incomparable pair. A property of a *dynamics*, not of the measure. | `mg-05ec` §1–2 |
| `alpha(P)` | **The compression arc's quantity.** Cut `L(P)` into fibers two ways — by the odd-position swaps and by the even ones. `alpha` is the worst case, over all non-constant functions, of how much of a function's variance lives *inside* fibers (summed over the two cuts) rather than between them. It is what a single round of that compression is guaranteed to **see**, i.e. the scheme's efficiency, and the route needed it above `2`. | [`docs/FACTS.md`](FACTS.md) notation, F6–F7; `mg-409a`, `mg-8d66` |
| `Δ₁(A)` | How **fat the interface** of a cut is — what fraction of a set leaks out under one step. Cut geometry, Axis 1. **Not `δ`.** | [`STATE.md`](../STATE.md) glossary |

---

## 3. The three spectra, and why there are three

The clearest conceptual gain of the 2026-08-12 stock-take (`mg-05ec` §1), and what three separate
documents got wrong. **There are three spectra, and the third is what makes the other two easy to tell apart.**

- **Picture A — the destination.** Draw a random linear extension; ask how often element `x` lands
  in slot `i`. That fills an `n × n` table — a **static summary of the measure**, with no time in
  it. `λ_std` is its top eigenvalue off the constants.
- **Picture B — the journey.** Make every linear extension a vertex, join two that differ by one
  adjacent swap, run the walk. `λ₂^BK` is its second eigenvalue: a property of a **dynamics** whose
  stationary distribution happens to be Picture A's measure.
- **Picture C — the `S_n` walk.** Walk on *all* of `S_n`, stepping by a random linear extension read
  as a permutation. `S_n` acts on itself, so this walk decomposes by representation theory, and
  **the standard `(n−1)`-dimensional block is exactly Picture A's matrix** — row 3a,
  `S_P = ρ_std(η_P)`, `U-id`, **proven**.

> **One sentence to keep: `λ_std` is a property of the *measure*; `λ₂^BK` is a property of a *walk*
> whose stationary distribution is that measure. One lives on `n` elements, the other on `|L(P)|`
> extensions, which is typically exponentially larger.**

**The load-bearing asymmetry.** By Schur, Picture C guarantees `λ_std` *is* an eigenvalue of the
`S_n` walk. Nothing of that shape exists on the BK side: **`L(P)` carries no `S_n` action at all** —
a swap at position `i` fires only when the two elements sitting there are incomparable, so which
moves exist depends on where you are standing. No irrep decomposition of `ℝ^{L(P)}`, no "standard
sector" inside it, and therefore **no guarantee that `λ_std` is anywhere in the BK spectrum**
(`mg-05ec` §1). Every attempt to carry a bound across has died on that missing guarantee.

---

## 4. The bridge

**There is exactly one bridge between the two axes, it is real, it is `OPEN`, and it is the whole
remaining gap: L1b** — *frozen ⟹ `E[inv_e] ≤ (ε/6)(n²−1)` for a constant `ε ≤ ε_dem ≈ 2×10⁻²`*
(row 8). Picture it as a **rigidity** statement: *if every question about `P` is nearly settled,
then `P` is nearly a stack of blocks.* **What is open is the SIZE of that constant, not its
existence** — `ε_sup < 1` is proven, and at it the spectral rendering `1 − λ_std ≤ ε` is
**vacuous** (`mg-0e8c`). The two renderings are **not equivalent**: the master bound runs
inversions ⟹ spectrum one way only, and 82 posets at `n = 6` separate them (`mg-0e8c` a3/C3).

**It is not spectral in any load-bearing sense** (`mg-05ec` §5, landed at
[`STATE.md:25`](../STATE.md)). `λ_std` is one unit among five on Axis 1; `mg-210d`'s master bound
`1 − λ_std ≤ 6E[inv_e]/(n²−1)` is the conversion; the reduction consumes rows 5 and 7 and nothing
else — no sector decomposition, no representation theory. The spectral objects keep two honest jobs:
a **dictionary** (row 3a, which licenses the word *"standard"*) and **one proven ingredient** (row 5,
Buser). A vocabulary and a lemma are not a route.

**So the diagram's `A → B → C` is not where the work is.** Row 8 routes `A → C` directly, and not one
of the three live residuals — `(B-cov)`, `(EQ)`, `(R)` — attacks a spectrum: two are counting
statistics of `L(P)`, the third a pure count on `P`. Node `B` is presently **unconsumed**, and
returns to the critical path the moment anyone proves L1b *through* the BK cut
([`STATE.md:78`](../STATE.md), marked **documentary**, not mathematical).

**Where the difficulty sits.** Pair-by-pair information is **exhausted** — the best constant any
pair-marginal argument reaches is an equality, not a bound awaiting sharpening (`mg-6bc2` Claim 3.1)
— and both faces of the single lemma are **false for abstract frozen distributions**. So the proof
must reach into the **joint law** of a real poset's linear extensions, and that obstruction has no
eigenvalue anywhere in it.

**This file describes the space; the ARGUMENT is described once, elsewhere.** Where L1b enters the
chain, what the other links are, and why the chain is a closed loop on the frozen hypothesis rather
than a line: [`OneThird-ProofShape-mg-3af8.md`](OneThird-ProofShape-mg-3af8.md) — **cited, not
restated** (`mg-3af8`, on Daniel's question).

---

## 5. Intuitions that have been killed, and by what

This is the section with the most value per line, and the one most likely to be dropped. `FP✗` is a
refutation and carries **universal** strength; `FP` and `documentary` do not.

| the intuition | what killed it | kind · pointer |
|---|---|---|
| A cleverer compression could beat the spectral gap. | At the top of the refinement order the compression operator **is** the chain: `Q_finest = ((n−1)/2)(I − P_BK)`, exactly. So `sup_k alpha_k = ((n−1)/2)·gap_BK` — the best possible output *is* the BK gap, rescaled. | `U-id` · [`FACTS.md`](FACTS.md) F6, `mg-8d66` |
| More foliations — a larger `k` — would raise the ceiling. | `alpha_k ≤ 1` at **every** poset and **every** `k`, attained at every `k`, against a bar in `[2, 3)` that does not decay with `n`. The `k` with the highest ceiling is the one where each fiber is a single swap, i.e. where nothing has been compressed. | `U` + `FP` · `mg-8d66`, `mg-409a` |
| Standard dominance holds unconditionally. | **166 explicit refuters** at moderate-`λ` `n = 7`. ⚠️ Read from `mg-8b64`, never re-measured — here or anywhere. | `FP✗` · [`STATE.md`](../STATE.md) row 3b(a) |
| `λ_std` and `λ₂^BK` are comparable, because the standard sector is a subspace. | Refuted in **both** directions on exact rationals, and never equal at `0/4306`. The schema was valid and its hypothesis false: there is no containment, because they are extrema of *different operators over different spaces*. | `FP✗` · `mg-d1be`, `mg-05ec` §3.1 |
| …but it fails exactly on the ordinal sums, so the useful direction survives. | The set equality holds through `n = 6` and **breaks at `n = 7`**, on an *indecomposable* witness, certified by a separating rational at margin `4.4e-4`. | `FP✗` · `mg-d1be`, `mg-05ec` §3.1 |
| The poset constraint is what breaks the two spectra apart. | Inverted: the obstruction is **maximal where the constraint is empty**. On the antichain the transport gap is `Θ(1)` and the BK gap is `Θ(n⁻³)`; no constant reconciles them. | proven · `mg-05ec` §3.1 |
| `0/132` is a clean sweep supporting the transfer. | It is `0` failures inside a frame — `n ≤ 6` exhaustive **+ `n = 7` top-λ spot only** — chosen so that the known refuters fall outside it, and it is `S_n`-side evidence mis-attributed to the BK side. **Never quotable bare.** | sampling artifact · [`STATE.md`](../STATE.md) row 3b(c), `mg-4a86` |
| `(LIB-weak) ⟹ (LIB-const)` for large enough `n`, so go and find `N₀`. | **No `N₀` works for the class at all**: for any candidate, an `o(n²)` function violating `(LIB-const)` throughout `[1, N₀)` exists. The gap is a *quantifier*, not a constant, so there is nothing to compute. | proven · `mg-c4f5` §5.3 |
| The two faces of the single lemma, `(B)` and `LIB`, are equivalent. | `(B) ⟹ LIB` is one line and unconditional; the converse is **unproven**, and it fails as an inequality between the quantities. `(B)` is strictly the stronger face. | proven + open · `mg-a58f` Thm 3.3 |
| The frozen hypothesis could sharpen the Kahn–Saks bound. | **Provably inert.** Coherence is a logical *consequence* of `δ < 1/3`, so it shrinks the class by zero, and its only residual is a system of *upper* bounds that can never force a positive lower bound. | proven · `mg-61bb` |
| Aleksandrov–Fenchel can separate the fatal flat law from the Kahn–Linial optimum. | **AF is saturated** — both are Stanley equality cases, so no AF *inequality* separates them; and the stability residual that remained was refuted by hand, with the reduction to it proven circular. | proven · `mg-a1ec`, `mg-dcae` |
| The incomparability graph determines `δ`. | Two `n = 6` posets with isomorphic incomparability graphs and the same `e(P)` have `δ = 4/9` and `1/2`. `G` measures an element's positional *spread*; `δ` is about its *location*. | `FP✗` · `mg-e2de` |
| The compression kills a covariance the programme needs. | The covariance it kills is **zero for a trivial reason** and was never nonzero; the one `(B-cov)` needs is a *between-fiber* quantity in the other summand of the law of total variance. The two claims have the same shape and different objects. | `FP` · [`FACTS.md`](FACTS.md) F11 |
| The spectral route is *the* bridge. | The far side is a naming, the one live BK ingredient runs the other way and hands over a cut rather than a number, and the transfer that would make the route spectral is refuted unconditionally and *is* the destination conditionally. | verdict · `mg-05ec` §5 |
| A compression designed from the poset injects realizability — Daniel's *"design them via poset structure"*. | Two `n = 6` measures with **identical pair marginals**, one a linear-extension measure and one not, sit inside `compression2`'s only input, hypothesis (1), at the same value, and every step returns the same verdict. Wash-out site: `L*` and (1) are functions of the pair marginals, the tree a function of `L*`; nothing downstream reads `P`. Kills **this route** — the poset read only through pair marginals — **not** poset-design in general. Independently re-derived, same witness. | `FP✗` (this construction) · `mg-0fc6` §2 `a2.3`, `mg-8748` `c4.1` |
| Restrict `M_n` to the *realizable* `π` and the ceiling comes down — row 8's *"must add a realizability fact"*, read as a constraint on `π`. | **Vacuous at the vertices, for every such restriction at once.** `π(δ_σ) = δ_σ` is a vertex of `M_n`, so any class of measures containing the point masses has marginal image `S` with `conv(S) = M_n` — no separating inequality, hence **no LP, SDP or lift-and-project** route. Measured on four different restrictions, and the widest (`supp(μ) ⊆ L(P)` for some `P`) is no restriction at all, since `L(antichain) = S_n`. ⚠️ **Scope — this kills the CUT, not the image.** Inside the convex cell of hypothesis (1) read on the *measure* the image ceiling is exactly `d ×` the body's (`2/3, 1/3, 1/5, 4/15` at `n = 3…6`), because *that* reading excludes `n!−1` vertices where realizability excludes none. The image **reduces row 8 to `d`** = residual **(R)**. | proven · `mg-c776` `T2`/`c2.4`, generalised `mg-3da1` `T-3da1` ([`OneThird-ImageClosure-mg-3da1.md`](OneThird-ImageClosure-mg-3da1.md)) |

---

## 6. What we believe and cannot prove

Everything here is marked `BELIEF` because none of it is earned. It is recorded so that it can be
attacked, and so that it is never quoted as though it were §5.

- **BELIEF — freezing *every* pair is what pushes the slow mode into the standard sector.** That is
  the conditional standard dominance, i.e. L1b itself. The mechanism story is why we find it
  plausible: off-regime, with a lone frozen pair, the slow BK mode is degree-2 and lands in the wrong
  irrep; in-regime the two gaps track each other (`0.057` vs `0.056`, at **one** `n = 7` poset —
  an anecdote, not evidence). (`mg-05ec` §3.3)
- **BELIEF — the proof will be written in inversions and only reported in eigenvalues.** A judgement
  about method, not a theorem; it follows from what the live routes consume, and a BK-mediated proof
  of L1b would overturn it. (`mg-05ec` §4.4–§5, documentary)
- **BELIEF — `(B-cov)`, the wrong-signed same-side covariance, is where the answer is.** What is
  documented is that three routes converge on it and that it is correctly ordered first; *that it is
  the crux* is our reading. (`STATE.md` *Where the threads converge*, `mg-a58f`)
- **BELIEF — frozen posets have an incomparability-density ceiling `d(P) ≤ D < 1`.** Residual `(R)`,
  and the ground is thin: a search for a frozen-conditional **upper** bound on `d` returns **zero**;
  every density fact on record points the other way. (`mg-210d`, `mg-345e`)
- **BELIEF — the pair-bias multiset determines `alpha`, and there is a mechanism behind it.** Zero
  collisions on three populations, the largest exhaustive one `n = 5`. Filed `UNEXPLAINED`: no proof,
  no mechanism, no counterexample. ([`FACTS.md`](FACTS.md) F8)
- **BELIEF — the conjecture is true.** Nothing in this corpus argues for it. Verification through
  order 11/14 is a *verification range* clearing none of the thresholds this programme needs, and
  **no structural lower bound on a minimal counterexample's size exists in the literature**. The
  confidence is inherited from the field, not derived here. (`mg-33f5`)

---

## 7. Keeping it honest

**Adding a line.** Give it a pointer, or mark it `BELIEF` and put it in §6. If it fits neither, it
is not a conceptual gain yet — it is a hunch, and hunches belong in the work item that will test
them.

**Removing a line.** A conceptual claim that turns out to be wrong is **moved to §5**, not deleted:
a killed intuition is the most valuable line in this file, and deleting it invites the next reader to
have it again. That is the same rule [`docs/FACTS.md`](FACTS.md) applies to refuted entries, for the
same reason.

**Length.** If this file stops being readable in one sitting it has failed at its only job. Cut §5
last.
