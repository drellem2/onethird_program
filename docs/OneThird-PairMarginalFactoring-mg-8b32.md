# Which functions of `P` factor through the pair marginals — mg-8b32

**Verdict: the poset level is CLOSED, and the closure is one line.** `P = {(x,y) : pi_xy = 1}` — the
poset is read off the marginal vector by looking at which entries equal `1`. So **every** function of
`P` factors through the pair marginals, the enumeration Daniel proposed dies at every entry
simultaneously rather than one entry at a time, and the requested deliverable — *"a single explicit
function of `P` that provably does not factor through the pair marginals"* — **does not exist**.

**The surplus is real, and it belongs to the MEASURE rather than to the poset.** A marginal vector
determines `P` and does not determine `supp(mu)` or the weights. Explicit non-factoring separators
exist in both of those, and one of them is an exact realizability certificate.

**And the surplus does not buy a bound, for a reason worth more than the surplus.** The `M_n`
relaxation is already *tight* over the fiber of every realizable marginal vector, so the whole slack
of the `M_n` ceiling sits at marginal vectors that are **not** of the form `pi(Unif(L(Q)))`. That
relocates the realizability fact `STATE.md` row 8 says every route below `1` needs: it is not a
statistic of a measure and not an invariant of a poset — **it is a characterisation of which marginal
vectors occur.**

Instrument: [`code/marginal_factoring_8b32/`](../code/marginal_factoring_8b32/), five arms, all
green, 106 s, transcripts committed. Deterministic and no transcript here is operator-valued.

---

## 0. Scope, and what is cited rather than re-derived

| statement | kind | scope |
|---|---|---|
| **T1**, **C1**, **C2** (§1) | `U-id` — a proof, all `n` | proved; measured exhaustively at `n = 3,4,5` (`b1.1`, all 19 / 219 / 4231 labelled posets) |
| **T4**, **C3** (§4) | `U-id` — a proof, all `n` | proved; the exact set containment it rests on measured at `n = 3,4` exhaustive and at the `n = 6` witness (`b4.1`) |
| the set-level witness exists inside hypothesis (1) (§3) | `FP✗` — one exhibit, universal-strength for the existence claim | one poset, `n = 6`, `e(P) = 9`; all `2^9` subsets tested (`b3.2`) |
| the frequency counts (`27 of 195` at `n = 4`, `5 posets` in the `n = 6` hypothesis population) | `FP` | exhaustive at the stated `n` and **silent above it** |
| `L(P)` is a weak-order ideal under `L*` | `FP`, `n <= 6` here | computed on the witness only; the classical statement is not cited because it was not checked |

**Cited, not re-run.** `mg-0fc6` `a2.3` — two `n = 6` measures with identical pair marginals, one a
linear-extension measure and one not — is the obstruction this whole note stands on. It is a proof
and it is already independently replicated by `mg-8748` `c4.1`. **This directory is a third
instrument on it** (§2), reached by a different search, and it does not re-run `a2.3` itself.

**Not touched.** `mg-0fc6`'s `M_n` separation sweep and its `PREDICTIONS.md`. §5 says exactly how
this note's separator relates to that file's pre-registered condition 2, because the honest answer is
*"outside its scope"* and not *"it fired late"*.

---

## 1. The answer: `P` is a function of the pair marginals

> **T1.** For any probability measure `mu` on `S_n` with marginal vector `pi`, put
> `P(pi) := {(x,y) : pi_xy = 1}`. Then **(a)** `P(pi)` is a strict partial order; **(b)**
> `supp(mu) ⊆ L(P(pi))`; **(c)** if `mu` is realizable — uniform on `L(Q)` for some poset `Q` —
> then `Q = P(pi)`; **(d)** `P(pi)` is a function of `pi` and of nothing else.
>
> *Proof.* `pi_xy = 1` says exactly that `x` precedes `y` in **every** order in `supp(mu)`, so the
> relation is an intersection of linear orders: irreflexive, asymmetric, transitive — that is (a),
> and (b) is the same sentence read the other way. For (c): if `mu = Unif(L(Q))` then `x <_Q y`
> gives `pi_xy = 1`, and `x ∥_Q y` gives extensions both ways, so `pi_xy < 1`; the two sets
> coincide. (d) is the definition. ∎

> **C1 (the collapse).** Every function of `P` factors through the pair marginals. Hence no function
> of `P`, at any tier, takes different values on `a2.3`'s two measures, and by `a2.3` none can inject
> realizability.

> **C2.** `P ↦ pi(Unif(L(P)))` is **injective**: distinct posets have distinct marginal vectors.

**The ticket's premise was the thing to check, and it is false.** The ticket says *"the poset `P` is
strictly more than its pair marginals — `a2.3` proves it, since it exhibits two measures with
identical pair marginals of which only one is a poset's."* The inference does not go through:
`a2.3`'s `mu2` is `mu1` perturbed **over the same support**, so `mu2`'s marginal vector has the same
`1`-entries and `P(pi(mu2)) = P(pi(mu1)) = P`. The two measures do not even disagree about *which
poset they are about*. What they disagree about is the weights.

**This is also `mg-0fc6`'s own finding, one level up.** That note measured that `L*` is a function of
the pair marginals and called it *"a marginal object"*. `L*` is a function of `P`; T1 says the whole
of `P` is marginal, so `L*` was never the special case it looked like. Its `a2` oracle's docstring
already contains the argument — *"that `P` is forced: it is the intersection of the orders in the
support"* — computed there from the support, when the same object is `{pi = 1}`.

### The candidates Daniel named, and their verdicts

| candidate | tier — what it reads | verdict | reason |
|---|---|---|---|
| the **BK graph** on `L(P)` — *the original question* | `P` | **FACTORS** | C1; computed identical on both witnesses (`b2.2`) |
| the **BK graph** on `supp(mu)` | `supp(mu)` | **does NOT factor** | 12 edges against 0 on §3's witness (`b2.3`) |
| the **distinguished extension `L*`** | `pi` | **FACTORS** | definitional; `mg-0fc6` measured it, T1 explains it |
| **`L*` is a MEMBER of the support** | `supp(mu)` | **does NOT factor** | `True` / `False` on §3's witness (`b2.3`) |
| **`L(P)` convex in weak Bruhat order** | `P` | **FACTORS** | C1. And with a natural labelling `L(P)` is a weak-order *ideal*, so convexity is automatic (`b2.2`) |
| **`supp(mu)` a weak-order ideal under `L*`** | `supp(mu)` | **does NOT factor** | `True` / `False` on §3's witness and on the two-atom witness (`b3.3`) |
| **cohomology of the category of posets**, evaluated at `P` | `P` | **FACTORS** | C1. Its input is `P`; a functor of `P` is a function of `pi` |
| dimension, height, width, jump number, Möbius function, order complex, order & chain polytopes | `P` | **FACTORS** | C1; six of them computed identical as a vacuity guard (`b2.2`) |
| **F8 — `alpha`** | `P` | **FACTORS** | C1, and by a stronger route than F8's own: F8's determination is `FP` and *unexplained*, C1 is a proof |
| **F17** — three mutually adjacent extensions, on `L(P)` | `P` | **FACTORS** | C1 |
| **F17**, read on `supp(mu)` | `supp(mu)` | **BLIND HERE** | agrees on both witnesses this corpus has; one evaluation, no proof either way (`b3.4`) |
| **F22** — no 3-antichain ⟹ `e` exists and is unique | `P` | **FACTORS** | C1 |
| **F13** (reversal symmetry), **F15** (F5's equality set), **F19** (`δ = 1/3` adjacency) | `P` / `pi` | **FACTORS** | C1; F19 is a function of `δ` and `e`, both marginal |
| **`H(mu)`** | weights | **does NOT factor** | `a2.3`, and recomputed here (`b2.4`) |
| **`gap(mu) = log2 e(P(pi)) − H(mu)`** | weights | **does NOT factor**, and is **zero exactly on the realizable measures** | §4 |

**The one objection, answered.** C1 says a function whose *only* input is `P` factors. Someone could
reply that in the programme's setting `P` is handed to the construction independently of `mu`, so it
is extra data rather than a function of `pi(mu)`. It is not, and the reason is what makes the
relaxation a relaxation: a bound on `e(P)` proved by relaxing to `M_n` has to hold for **every**
`mu` sharing `Unif(L(P))`'s marginals, and T1 says every such `mu` has `P(pi(mu)) = P`. The poset is
constant on the fiber the adversary is allowed to move inside, so reading it off the marginals costs
nothing and adds nothing. What is **not** covered by C1 is a construction reading a poset together
with data not determined by it — that is outside this category and outside this note.

**A correction to the ticket's own procedure, which the table needs.** The ticket says *"same value
on both → it factors → dead"*. That is too strong: agreement at **one** point of a fiber is one
evaluation, not a proof of factoring. What agreement does prove is the thing the ticket cares
about — that the candidate cannot separate *that* realizable measure from *that* non-realizable
one. So the table carries three verdicts, not two, and `BLIND HERE` is not `FACTORS`. Every
`FACTORS` above is a consequence of C1, which is a proof; none of them rests on agreement.

---

## 2. The witness, reached by a third route

`b1.3` searches for a hypothesis-population poset whose **marginal fiber is not a point** — i.e. a
non-trivial kernel of the marginal map, the whole space of `a2.3`-style directions rather than one
construction of one of them. It lands on `n = 6`, `e(P) = 9`, `max flip = 1/3`: `a2.3`'s witness,
found by a different search, after `mg-8748`'s `c4.1` found it by a third.

**The search is exhaustive and the restriction that makes it cheap is exact.** `L*` is always a
linear extension of `P` (if `x <_P y` then `pi_xy = 1 > 1/2`), so every poset with a coherent `L*`
is a subrelation of the total order `L*`; relabelling `L*` to the identity, the whole `n = 6`
hypothesis population sits among the transitive subrelations of the 6-chain — `2^15` candidates
rather than `3^15`.

Two measured facts fall out that are worth keeping:

- **The `n = 6` hypothesis population with `L* = identity` is 5 posets.** (`FP`, `n = 6`.)
- **No hypothesis-population poset at `n <= 5` has a non-trivial marginal fiber at all** —
  so `a2.3`-style weight witnesses do not exist below `n = 6`, and `a2.3`'s `n = 6` was forced, not
  chosen. (`FP`, `n <= 5` exhaustive.)

---

## 3. The support-level witness the ticket says is missing — it exists, inside hypothesis (1)

The ticket's 15:15Z correction is right and is the sharpest thing in it: `a2.3`'s two measures
**share a support**, so every predicate reading only the support agrees on them for a reason that
has nothing to do with factoring, and support-level candidates need their own witness — *"two SETS
of permutations with identical pair marginals, one of which is `L(P)` for some poset and one of
which is not"*. It says the corpus does not have one and that it may not exist.

**It exists twice over.**

**(a) A weak one is already in `mg-0fc6`'s own control list, unrecognised.** `a2.1`'s third control is
the two-atom measure, and `Unif({sigma, sigma^rev})` has every pair marginal at `1/2` — which is
exactly `Unif(S_n) = Unif(L(antichain))`'s marginal vector. Two sets, identical marginals, one a
poset's and one not. Its defect is `mg-0fc6`'s own `D4`: the antichain's max flip is `1/2`, so that
pair sits **outside** hypothesis (1).

**(b) The binding one is inside hypothesis (1), at the same `n = 6, e(P) = 9` poset `a2.3` used.**
Six 3-element and six 6-element **proper subsets of `L(P)`** carry `L(P)`'s pair marginals exactly
(`b3.2`, all `2^9` subsets tested). None is a linear-extension set — and cannot be, by C2: the same
marginals force the same `P`, and a proper subset of `L(P)` is not `L(P)`.

The whole fiber over that marginal vector is enumerated exactly in `b3.1`: **6 vertices, every one
of support size 3 against `e(P) = 9`, not one realizable, and 4 of the 6 do not contain `L*`.** The
only realizable point of the fiber is `Unif(L(P))`, which is interior to it.

**So every support-level candidate is now testable at a witness compression2's own standing
assumption admits**, and §1's table is complete rather than partly deferred.

**Frequency, with its scope attached.** Proper same-marginal subsets are not rare in general — 1 of
13 posets at `n = 3` and 27 of 195 at `n = 4` admit one (exhaustive over all labelled posets and
all their subsets) — but **none of those carriers is in the hypothesis population at `n = 3` or
`4`**, so the `n = 6` witness is the first one inside it. `n = 5` is not swept (the subset
enumeration is `2^|L(P)|` and `|L(P)|` reaches 120), and `n = 6` is one poset. The **existence**
claim needs only that poset; the **frequency** counts say nothing above `n = 4`.

---

## 4. Why the surplus does not buy a bound — and what the target becomes

> **T4 (the relaxation is already tight, fiber by fiber).** For every poset `P`,
> `max { H(nu) : pi(nu) = pi(Unif(L(P))) } = log2 e(P)`, attained **uniquely** at `Unif(L(P))`.
>
> *Proof.* By T1(b) every `nu` in that fiber has `supp(nu) ⊆ L(P(pi)) = L(P)`, so
> `H(nu) <= log2 |L(P)|`, with equality iff `nu` is uniform on all of `L(P)`. ∎

> **C3.** Hypothesis (1) is a function of `pi`, so if `mu ∈ M_n` has a **realizable** marginal
> vector then the poset `P(pi(mu))` is itself in the hypothesis population and
> `H(mu) <= log2 e(P(pi(mu)))`. **Therefore the entire gap between the `M_n` ceiling and
> `max { log2 e(P) : P in the hypothesis population }` is carried by measures whose marginal vector
> is NOT of the form `pi(Unif(L(Q)))`.**

> **C4 (the corrected target).** The realizability fact `STATE.md` row 8 requires — *"every route
> below `1` must add a realizability fact"* — is therefore **not** a function of `P` (C1 kills those)
> and **not** a constraint on the inside of a fiber (T4 says the fiber is already exact). It is a
> constraint on **which marginal vectors occur**: a characterisation of the image of
> `P ↦ pi(Unif(L(P)))` inside `M_n`. By C2 that image is in bijection with the posets, so it is a
> **finite** set of points inside a **full-dimensional** body. `b4.3` measures both ends at `n = 4`:
> 72 of 219 labelled posets are inside hypothesis (1), and the marginal vectors reachable inside
> hypothesis (1) span the full 6-dimensional space.

### The separator exists, is exact, and is circular — and the circularity is the finding

`gap(mu) := log2 e(P(pi(mu))) − H(mu)` is `>= 0` always and `= 0` **exactly** on the realizable
measures (T1(b) + T4). It does not factor through `pi`, and `b4.2` measures it on four witnesses:
`0` on `Unif(L(P))`, `0.0839` on the `a2.3`-shaped weight witness, `1.585` on §3's set witness,
`8.492` on the two-atom measure.

**And it cannot become a bound, for a reason visible in its own formula.** Its first term is
`log2 e(P)` — the very quantity the programme is bounding. Imposing `gap = 0` on `M_n` returns
`max { log2 e(P) : P in the hypothesis population }`, which is the un-relaxed problem written out;
`b4.4` measures that the zero set is exactly the hypothesis-population uniform linear-extension
measures and that every tilt off it is caught.

**So the useful successor question is not "find a separator" — one is exhibited above — but "bound
the gap above by something that is not `e(P)`", or equivalently characterise the realizable marginal
vectors directly.**

---

## 5. Relation to `mg-0fc6`'s pre-registered conditions, stated rather than left to be inferred

`PREDICTIONS.md` condition 2 was *"any quantity **the note bounds** whose value separates the
linear-extension measures inside `M_n(0)` from the rest"*. §4's `gap` is **not a quantity
compression2 bounds** — it is built here from `H` and `e(P(pi))` — so **condition 2 did not fire and
was not supposed to**. Nothing in this note retro-fires that bet, and the ticket's instruction to
treat the non-firing as *evidence that separation is hard* rather than as a theorem is respected:
what §4 shows is that separation is **easy** and **useless**, which is a different statement from
either, and is compatible with both.

---

## 6. Recommendation to `pm-onethird`

1. **Close the "design a compression from the poset" route at the poset level, by C1 rather than by
   sweep.** It is one line, it is a proof, and it covers Daniel's whole candidate list including the
   BK graph, the weak-Bruhat structure and the cohomology entry. **Do not spend a ticket enumerating
   poset invariants**; the enumeration is answered wholesale.
2. **Do not close the site.** The surplus is non-empty and explicit, and it is exactly `supp(mu)` and
   the weights. A construction that reads the support of the measure it is applied to is not covered
   by the obstruction — `b2.3` exhibits four such predicates, including the BK graph read on
   `supp(mu)` rather than on `L(P)`, which is Daniel's own object with the input corrected.
3. **The successor worth filing is C4's, and it is not a compression.** *Characterise the image of*
   `P ↦ pi(Unif(L(P)))` *inside* `M_n`. C3 puts the whole `M_n` slack there; C2 says the image is in
   bijection with posets; §3 says a marginal vector alone does not tell you whether you are on it,
   which is precisely why the characterisation is worth having. This is the same wall `STATE.md`
   row 8 names, moved from *"add a realizability fact"* to a definite question about a subset of a
   cube.
4. **Two corpus-native facts fell out and neither has a consumer**, so they belong in
   `docs/FACTS.md` rather than here if `pm-onethird` wants them kept: no hypothesis-population poset
   at `n <= 5` has a non-trivial marginal fiber (`FP`, `n <= 5` exhaustive), and the `n = 6`
   hypothesis population with `L* = identity` is 5 posets (`FP`, `n = 6`). **They are not filed by
   this ticket** — both are findings of this deliverable, which fails `FACTS.md`'s homelessness
   test until something else cites them.

---

*`mg-8b32`, `p8b32`, 2026-08-13. Instrument
[`code/marginal_factoring_8b32/`](../code/marginal_factoring_8b32/). Daniel's three framing messages
are quoted in the ticket body; the correction that the question is not about the BK graph is his,
and §1's two BK-graph rows are the answer to the original form of it.*
