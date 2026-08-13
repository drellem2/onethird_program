# What the image result closes — the generalisation, and the one clause the paraphrase dropped

**Work item:** `mg-3da1`, `mg-c776`'s successor carrier, filed by the mayor 2026-08-13 so that
item could close.
**Instrument:** [`code/image_closure_3da1/`](../code/image_closure_3da1/) — four arms, all green,
11 s, transcripts committed and byte-identical on re-run, **importing nothing from this estate**.
**Deliverable kind:** a corroboration and a correction, plus the landing `mg-c776` did not get.

---

## §0. VERDICT

> **`mg-c776`'s theorem is right, and it is stronger than it was stated.** No restriction of `M_n`
> phrased as *"`π` must be realizable"* can lower a linear ceiling — not `R_n`, not any other
> canonical measure, not any class anyone writes down later — because `π(δ_σ) = δ_σ` is a vertex of
> `M_n`. **Realizability is vacuous at the vertices.** The cut is dead in the strongest available
> form, and that closure is permanent.
>
> **And this work item's own title overstates it by one clause.** *"…and therefore CANNOT TIGHTEN
> ANYTHING"* does not follow, and the counter-measurement is in `mg-c776`'s own `c2.4`: inside the
> convex cell of hypothesis (1) read on the **measure**, the image ceiling is a **`d`-fraction** of
> the body's — at `n = 5`, a **fifth**. Reproduced here term for term on independent code.
>
> **What that changes is where the line went, not whether it died.** The image converts row 8's
> wall into *how large can `d` be for a frozen poset* — which is residual **(R)**, already on the
> board and already correctly ordered. Nobody should re-open the cut. Nobody should record `d` as
> closed either.
>
> **RECOMMENDATION: land the closure and the qualifier together, at the site a reader reads.**
> Done here in `STATE.md` and `docs/CONCEPTS.md` §5.

---

## §1. Why this item existed, and what it found instead

`mg-3da1` is a **successor carrier**: `mg-c776` declared a remainder, pogod refused to close it
with no successor named, and the mayor filed this to carry whatever the remainder turned out to be.
Its body was written from `pc776`'s commit messages and hands the judgement to `pm-onethird`.

The remainder turned out to have two parts, and only one of them was known:

1. **The result was not landed anywhere a reader is aimed.** Measured over `STATE.md` at
   `860c0a1`: `image` **0**, `c776` **0**, `R_n` **0** — and `realizab` **exactly 1**, which is
   row 8's *"every route below `1` must add a realizability fact"*. So the canonical document
   carried the sentence that generated the whole line and no trace of the answer to it, and a
   reader following that sentence was aimed straight at the closed door.

   `docs/FACTS.md` is not the second site either: all **9** of its `mg-c776` mentions sit inside
   the **F25** entry, which is `mg-8b32`'s marginal-fiber fact that `mg-c776` merely *re-derived*.
   The convex-shadow result appears once (`:981`) as a supporting clause in that entry's `NOT`
   field. **It has no entry of its own anywhere**, which is correct — §5 explains why it must not
   have one — and which is exactly why the `STATE.md` landing is the whole remedy.
2. **The paraphrase that carried it strengthened it.** §3 below.

---

## §2. The generalisation (`d1`)

> **T-3da1.** Let `C` be **any** class of probability measures on `S_n` containing every point
> mass, and let `S = { π(μ) : μ ∈ C }` be its marginal image. Then **`conv(S) = M_n`**.
>
> *Proof.* `π(δ_σ) = δ_σ` is a vertex of `M_n`, so `vert(M_n) ⊆ S ⊆ M_n`, and a set containing
> every vertex of a polytope has that polytope as its hull. ∎

**Corollary.** No restriction of the marginal body phrased as *"`π` must be realizable"* can lower
a linear ceiling over `M_n`. **Realizability and extremality point the same way**: every vertex is
the marginal vector of a point mass, which is as realizable as a measure gets.

That is strictly more general than `mg-c776`'s `T2`, which is the case `C = {Unif(L(P))}`. It
disposes of every candidate of this shape at once — including ones not yet written down — and it
says which property of a proposed restriction must be checked **first**: *does it exclude a vertex?*

**Measured on four genuinely different restrictions** (`d1.2`, `n = 4`), all four holding all 24
vertices:

| restriction | points | note |
|---|---|---|
| `π(Unif(L(P)))` — `mg-c776`'s `R_n` | 219 | |
| `π(μ_P)`, `μ_P ∝ 1/(1+inv(σ))` — a different canonical measure | 219 | **390 of 414 points differ** from `R_n`; same obstruction |
| `supp(μ) ⊆ L(P)` for some `P` — the widest reading | all of `M_n` | **vacuous outright**: `L(antichain) = S_n` |
| `U-id`: every coordinate a multiple of `1/e(P)` | ⊇ `R_n` | holds at every vertex, where `e(P) = 1` |

The third row is worth its own sentence: the widest reading of "realizable" that the pair-marginal
level can express **restricts nothing at all**, because the antichain's linear extensions are the
whole symmetric group.

**And `d1.1` re-measures `mg-c776` `c2.1` on independent code**: `vert(M_n) ⊆ R_n` at `n = 3,4,5`,
every vertex `r`-fixed, `|R_n| = 19, 219, 4231`.

---

## §3. THE CORRECTION — the image does tighten, by exactly `d` (`d3`)

Two readings, both true, and the title carries only the first.

| reading | body ceiling | image ceiling | ratio |
|---|---|---|---|
| **A** — global; hypothesis (1) read on the **poset** | `10` | `10` | **`1`** |
| **B** — inside the cell; hypothesis (1) read on the **measure** | `10/3` | `2/3` | **`1/5`** |

*(at `n = 5`; `d3.4`)*

`mg-c776` `c2.4`'s table, reproduced from an independent poset enumerator, linear-extension
routine and marginal:

| `n` | ceiling on `K` | best image point in `K` | ratio | `m` | `d = m/C(n,2)` | `e(P)` |
|---|---|---|---|---|---|---|
| 3 | `1` | `2/3` | `2/3` | 2 | `2/3` | 3 |
| 4 | `2` | `2/3` | `1/3` | 2 | `1/3` | 3 |
| 5 | `10/3` | `2/3` | `1/5` | 2 | `1/5` | 3 |
| 6 | `5` | `4/3` | `4/15` | 4 | `4/15` | 9 |

Term for term. And two exact identities behind it, not fits:

- **the maximum is `m/3`** — the maximiser sits at flip exactly `1/3` on each of its `m`
  incomparable pairs and `0` on the rest;
- **the ratio is exactly `d`** — `(m/3)/(C(n,2)/3) = m/C(n,2)`.

So the cell reading is carried by **one number, `m`**. That is what makes it a *reduction* rather
than an improvement: it converts row 8's question into *how large can `m` be for a frozen poset*.

### What separates reading B from `T-3da1`

**Vertex exclusion, and nothing else** (`d1.4`).

- realizability excludes **no** vertex → hull `= M_n` → ratio `1`;
- hypothesis (1) on the **poset** excludes **no** vertex — a total order's `δ` is a maximum over the
  empty set (`mg-c776` `c2.3`) → hull `= M_n` → ratio `1`;
- hypothesis (1) on the **measure**, in the cell `L* = identity`, excludes `n! − 1` of the `n!`,
  leaving `δ_id` alone → hull a proper subset → ratio `d`.

Measured: exactly **one** vertex survives the cell at `n = 3,4,5`, and it is the identity.

### Where the overclaim entered, and where it did not

**Not in `mg-c776`.** That directory's `README.md` §1 states the careful version —
*"no fact about the image can move `eps` except through `d`"* — and its deliverable §3 prints the
`c2.4` table under the heading *"Where the comparison is NOT vacuous"*. The half without the
qualifier is what travelled into the work-item title, and from there into anything a dispatcher
reads. This is `mg-2959`'s shape one estate over: **the prose is the surface no instrument covered.**

---

## §4. The guard that guards nothing (`d2`)

`mg-c776` `c2.2` reports `0 separations` over 300 seeded directions and the deliverable labels it
*"a vacuity guard rather than a second proof"*. That label is correct. What was missing is the
measurement it implies — a guard is only worth reading if it can go red.

**It cannot** (`d2.2`). Once `vert(M_n) ⊆ R_n` is known, `max over R_n = max over M_n` for
**every** direction, because a linear functional is maximised at a vertex and every vertex is in
the image. All 300 maxima are attained at a vertex of `M_n`. `0 separations` is `c2.1` restated,
and it would read the same at 3 directions or 3 million.

**And put to a world where a separation does exist** — the same image with one vertex removed,
whose hull *is* strictly smaller — the sweep's detection rate tracks `1/n!` (`d2.3`):

| `n` | `n!` | detects `δ_id` removed, of 300 | pooled rate | `1/n!` |
|---|---|---|---|---|
| 3 | 6 | 56 | `0.147` | `0.167` |
| 4 | 24 | 14 | `0.036` | `0.042` |
| 5 | 120 | **2** | `0.0064` | `0.0083` |

A direction catches a single-vertex removal only when it is maximised **uniquely** there. The
separation is real and exact — the all-ones direction finds it at every `n`, `3 → 5/2`, `6 → 11/2`,
`10 → 19/2` (`d2.4`) — so the low rate is the **sweep's** property, not the planted world's.

**The consequence is estate-wide and is why this is an arm rather than a footnote:** a direction
sweep returning `0 separations` is near-zero evidence that a subset of `M_n` is convexly large.
Where a claim of that shape is load-bearing it needs the containment argument. `mg-c776` has one.

---

## §5. What is closed, what is not, and the honest prior on what is left

**CLOSED, permanently, and generalised past its original statement:** a separating inequality for
the realizable points. Hence no LP, no SDP, no lift-and-project hierarchy. `T-3da1` closes it for
every realizability restriction, not just `R_n`.

**NOT CLOSED:** `d`. The image reduces row 8 to residual **(R)** — *do frozen posets have an
incomparability-density ceiling `d(P) ≤ D < 1`?* — which was already on `STATE.md`'s board, already
correctly ordered, and reopened *quantitatively* by `mg-88bd` as `D ≤ ε_spec`.

**And the prior on (R) is recorded rather than left flattering.** `STATE.md` §6 marks it `BELIEF`
and says the ground is thin: *a search for a frozen-conditional upper bound on `d` returns zero;
every density fact on record points the other way.* `mg-c776` §4 reached `d` from a third
direction and noted that **none of the three arcs asked whether the lever exists**. That question —
*is there a frozen-conditional upper bound on `d` at all* — is the remainder this item hands on,
and the honest expectation is that the answer is no.

**Nothing in this document is a new boundary number.** `n ≤ 5` exhaustive, `n = 6` on `d3` only;
`mg-c776` reaches `n = 7` and F23 is exhaustive to `n = 9`. **The population warning governs every
`d3` number**: `δ < 1/3` is the counterexample condition, the conjecture is verified to `n = 14`,
so the strictly frozen population is empty at every `n` reachable here and `d3`'s maximisers sit on
the **closed boundary** — a different class from the hypothesis. `docs/FACTS.md` F1's corollary
warning applies verbatim.

**No entry is filed in `docs/FACTS.md`.** `T-3da1` fails the registry's homelessness test: it is a
finding of this document's own deliverable and it is consumed here, by the `STATE.md` and
`CONCEPTS.md` landings in §6. `d`'s status is F23's and `mg-6ff4`'s and is already registered.

---

## §6. What landed, and why it could not live in `docs/state-history/`

- **`STATE.md`, *Where the threads converge*, the *Retired or dead* list** — the image line, with
  **both** halves: the cut is dead for every realizability restriction, and what survives is `d`,
  which is `(R)`. It is not a ledger row, so no twin re-pin is required. It could not live in a
  per-attempt file for this estate's standing reason: row 8's *"every route below `1` must add a
  realizability fact"* is read **here**, and a reader following it needs to be told **here** that
  the marginal-level reading of that sentence is provably empty.
- **`docs/CONCEPTS.md` §5, *Intuitions that have been killed*** — with the kill **scoped**. §5
  already carries `mg-0fc6`'s row killing *poset-designed compressions*; a reader seeing that and
  nothing else would reasonably conclude the `π`-level realizability route was still open.
- **`code/state_ratchet_e331/CEILING.json`** — banked up in the same commit, with the words and the
  reason appended to `why`, per its own `how_to_change_this`.

---

## §7. Provenance

`p3da1`, 2026-08-13, from `mg-3da1` — `mg-c776`'s successor carrier, filed by the mayor.
