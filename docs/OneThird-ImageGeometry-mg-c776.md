# The image of `P ↦ π(Unif(L(P)))` inside `M_n` — characterised, and closed

**Work item:** `mg-c776`, `p8b32`'s recommended successor, adopted by `pm-onethird`.
**Instrument:** [`code/image_geometry_c776/`](../code/image_geometry_c776/) — five arms, all green,
38 s of CPU, transcripts committed and byte-identical on re-run.
**Deliverable kind:** a scoping recommendation to `pm-onethird`, not a decision.

---

## §0. VERDICT, first, because it is a NO and the ticket asked for those early

> **The characterisation exists, it is one line, and it cannot be consumed by anything.**
>
> **`R_n = Fix(r)`** where `r(π) := π(Unif(L(P(π))))` — equivalently, **`R_n` is the set of
> vertex-barycentres of the box-faces of the linear ordering polytope `M_n`**, one point per
> poset, one point per cell of the partition of `M_n` by forced poset. That is exact, it is a
> theorem rather than a measurement, and it is **not** `b4.4`-circular: it names neither `e(P)`
> nor an entropy.
>
> **And it has no convex shadow.** `R_n` contains every vertex of `M_n`, so **`conv(R_n) = M_n`**
> and *every inequality valid on the image is valid on the whole body*. **The ticket's
> first-ranked deliverable — "a separating condition satisfied by image points and violated
> off-image" — provably does not exist in inequality form**, hence not in LP, SDP or
> lift-and-project form either. Imposing hypothesis (1) first does not repair it: all `n!`
> vertices survive hypothesis (1) at every `η`, so `conv(R_n ∩ H) = M_n` too.
>
> **And where the image does meet hypothesis (1), it lands on ground already surveyed.** The
> boundary class saturates the pair-marginal supply bound with **zero slack** — that is
> `docs/FACTS.md` **F23** (`mg-6ff4`), exhaustive to `n = 9`, and this instrument reproduces it
> at `n ≤ 7` by a third route. So there is no slack to exploit there either.
>
> **RECOMMENDATION: close the image-characterisation line.** Not because it failed to produce an
> answer — it produced an exact one — but because the answer is provably unusable in the shape
> row 8 would need, and the one lever that survives (`d` under the frozen hypothesis) is
> `mg-6ff4` §9's own declared non-bridge, not a new target.

---

## §1. The question, and the four shapes the ticket ranked

`mg-8b32`'s `T4` closed the inside of a fiber and its `C3` therefore put **the whole slack of the
`M_n` ceiling on marginal vectors not of the form `π(Unif(L(Q)))`**. Its `C4` made characterising
that set the target. The ticket ranked four shapes of answer; here they are, with what `c1`–`c4`
found.

| # | asked | found | where |
|---|---|---|---|
| 1 | a separating condition satisfied by image points and violated off-image | **exists exactly** (`π = r(π)`), and **provably does not exist as an inequality** | `c1`, `c2` |
| 2 | the image's convex position | **the worst possible**: `conv(R_n) = M_n`; 97.2 % of the image at `n = 5` is non-extreme in its own hull | `c2.1` |
| 3 | how far a non-image point can sit from the image | **exactly `1/6` in sup norm at the one point that matters**, at every `n` | `c4.2`, `c4.3` |
| 4 | whether hypothesis (1) alone confines you near it | **no** — and the nearest image point to the ceiling is the *worst violator of hypothesis (1) there is* | `c4.3` |

---

## §2. The characterisation (`c1`)

**D1 (the cells).** For `π ∈ M_n`, `P(π) = {(x,y) : π_xy = 1}` is a strict partial order
(`mg-8b32` `T1`, cited; re-checked here at 450 exact sampled points of the body). So `M_n` is
partitioned into cells `C_P = {π : P(π) = P}` indexed by posets, and **every cell is non-empty** —
`π(Unif(L(P)))` lies in `C_P`, checked at all 4 469 posets at `n = 3,4,5`.

**D2 (the box-faces).** `F_P := {π ∈ M_n : π_xy = 1 for all x <_P y}` is the face of `M_n` cut out
by the **box** inequalities `π_xy ≤ 1` alone. Since `M_n = conv{δ_σ}` and each `π_xy ≤ 1` is valid,
`vert(F_P) = L(P)` — measured, 0 mismatches.

**T1 (the retraction).** `r(π) := π(Unif(L(P(π))))` satisfies `P(r(π)) = P(π)`, hence `r∘r = r`.

> *Proof.* If `x <_{P(π)} y` then every linear extension puts `x` first, so `r(π)_xy = 1`. If
> `x ∥ y` in `P(π)` then some extension puts each first, so `0 < r(π)_xy < 1`. ∎

**C1 (the characterisation).** `π ∈ R_n` **iff** `π = r(π)`; equivalently
**`R_n = { barycentre of vert(F) : F a box-face of M_n }`**, and the image is a *transversal* of
the cells — exactly one point in each. `|R_n| = 19, 219, 4231` at `n = 3,4,5`, which re-confirms
`mg-8b32`'s `C2` injectivity from a different marginal algorithm.

**It is not `b4.4`'s circular separator.** `gap(μ) = log₂ e(P(π)) − H(μ)` is circular because its
first term is the quantity the programme bounds. The fixed-point condition mentions neither. What
it costs instead is §3, which is a different and heavier objection.

**One measured caution, kept rather than tidied away** (`c1.4`). The planted near-miss
"barycentre of the face's *first two* vertices" is **idempotent on all 219 posets at `n = 4`** — it
is another retraction of `M_n` onto another set. So **idempotence is not the content of `T1`;
*which* set is fixed is.** The second near-miss (drop one extension) fails idempotence at 74 of
219, which is what keeps `c1.3`'s check non-vacuous.

---

## §3. Why the characterisation cannot be consumed (`c2`)

**T2.** `R_n` contains every vertex of `M_n` — a total order `P` has `L(P) = {P}`, so its image
point *is* the vertex `δ_P`. Hence **`conv(R_n) = M_n`**, and every inequality valid on `R_n` is
valid on all of `M_n`. ∎

Measured as a vacuity guard rather than a second proof: over 300 seeded integer directions at
`n = 3,4`, `max over R_n` equals `max over M_n` every time, **0 separations**.

**Three consequences, in increasing order of how much they cost the programme.**

1. **No cut exists.** Any family of valid inequalities for the realizable set is a family of valid
   inequalities for `M_n`, so adding realizability to the `M_n` program as *constraints* changes
   nothing. This is not "we did not find one" — it is a theorem, in one line.
2. **No convex relaxation of any strength helps.** LP, SDP and any lift-and-project hierarchy all
   produce convex sets containing `conv(R_n) = M_n`. The strength of the relaxation is irrelevant.
3. **Imposing hypothesis (1) first does not repair it** (`c2.3`). A total order has no incomparable
   pair, so its `δ` is a maximum over the empty set — `0`. All `n!` vertices are in `R_n ∩ H` at
   every `η`, so `conv(R_n ∩ H) = M_n` as well.

**What remains is non-convex**, and there are exactly two shapes of it on the table: the fixed-point
condition of §2, and an arithmetic one (`U-id`: every coordinate of `π(Unif(L(P)))` is a multiple of
`1/e(P)`, since it is a count over `e(P)` extensions). Neither is a constraint an optimisation can
consume.

**Where the comparison is NOT vacuous** (`c2.4`). Hypothesis (1) is itself non-convex — *"every pair
flipped with probability `≤ 1/3 − η`"* is a union of `2^C(n,2)` orthant cells. Fix the cell
(`L* = identity`, i.e. `π_ji ≤ 1/3` for `i < j`) and inside it the objective is linear, the region
is a polytope `K`, and `R_n ∩ K` is a handful of points:

| `n` | `max E[inv_e]` over `K` | over `R_n ∩ K` | ratio |
|---|---|---|---|
| 3 | `1` | `2/3` | `2/3` |
| 4 | `2` | `2/3` | `1/3` |
| 5 | `10/3` | `2/3` | `1/5` |
| 6 | `5` | `4/3` | `4/15` |

**The ratio is `d`, the incomparability density**, and §4 says why that is not an opening.

---

## §4. Inside hypothesis (1) the image is F23, and F23 is already further along

`c3` was written before its author read `docs/FACTS.md` **F23**, and it re-derives F23. That is
stated here rather than presented as a finding, and the arm's own header now says so.

**F23** (`mg-6ff4` §5.1) already carries: over the boundary class `δ(P) = 1/3`, the density maximum
is `4⌊n/3⌋/(n(n−1))`, and at **every** member `ε_spec = d·n/(n+1)` **exactly** — the class is the
**equality case** of the supply bound `ε_sup` (`mg-0e8c`, `STATE.md:125`), with **zero slack**.
Exhaustive over isomorphism classes to `n = 9`.

**What `c3` adds is corroboration by a third route, and two agreements worth recording:**

- the density maxima `2/3, 1/3, 1/5, 4/15, 4/21` at `n = 3…7` agree with F23's closed form at
  every term, from a *full labelled extension sweep* at `n ≤ 6` (134 492 posets) plus the
  `L*`-restricted chain sweep at `n = 7` — not `mg-6ff4`'s isomorphism-class census and not
  `mg-7c78`'s width sweep;
- `|B_n| = 1, 2, 3, 5, 8` at `n = 3…7`, counting posets with `L* = identity`, agrees with
  `mg-6ff4`'s class count `Σ_k C(n−2k, k)` at every term — so the two enumerations agree on the
  **size** of the population as well as on its extremes;
- and `48` labelled boundary posets at `n = 4` is `mg-8b32` `b4.3`'s `72 of 219` minus its 24 total
  orders, which is how the two instruments are known to be talking about the same set.

**THE POPULATION WARNING GOVERNS ALL OF IT.** `δ < 1/3` is the counterexample condition and the
conjecture is verified to `n = 14` (`mg-33f5`), so **the strictly frozen population is empty at
every `n` an instrument can reach** — re-established here exhaustively over all 134 492 labelled
posets at `n ≤ 6` rather than quoted. Every number in `c3` is on the **closed boundary**, which is a
different class from the hypothesis. This is F1's corollary warning, and F23 carries it too.

**The consequence this ticket adds, reached from the image side.** If the image contributes *zero
slack* where it meets hypothesis (1), then the only remaining question row 8 can ask **of the
image** is how large `d` can be for a **frozen** poset. That is F23's own `NOT` field —
*"this is not a realizability fact and it is the opposite of one"* — and `mg-6ff4` §9 states in its
own words that it *"does not bridge"* boundary to frozen. Three arcs have now arrived at `d` from
three directions and none of them has asked whether the lever exists.

---

## §5. The distances, and the answer to "does hypothesis (1) confine you?" (`c4`)

Let `π*` be the marginal vector of the two-atom law `(2/3)δ_id + (1/3)δ_rev`: every pair flipped at
exactly `1/3`, `E[inv_e] = C(n,2)/3`, `ε_spec = n/(n+1)` — **the whole `M_n` ceiling** (`mg-6bc2`
Claim 3.1 / `mg-0fc6` `a3.3`, cited for all `n`; the witness is rebuilt here so the table's numbers
are this instrument's own).

- **`T4`.** `P(π*)` is the **antichain** — no coordinate of `π*` is `1` — so the unique image point
  in `π*`'s own cell is `r(π*) = π(Unif(S_n))`, every coordinate `1/2`, and
  `‖π* − r(π*)‖_∞ = 1/6` **exactly, at every `n`** (checked `n = 3…6`).
- **`T5`.** And no image point is closer: every other poset has a comparable pair, whose coordinate
  is `0` or `1` against `π*`'s `1/3`. Exhaustive over the whole image at `n = 3,4,5`:
  `min ‖π* − ·‖_∞ = 1/6`, **attained uniquely at the antichain**.
- **`C3` (the ticket's fourth question).** The antichain has `δ = 1/2` — the single **worst**
  violator of hypothesis (1) there is. So the point carrying the entire ceiling satisfies
  hypothesis (1) at every pair with the bound attained, and the image point nearest it is as far
  outside hypothesis (1) as any point gets. **Hypothesis (1) does not confine a measure to the
  neighbourhood of the image.**
- **And `r` moves the objective the wrong way** (`c4.4`): `E[inv_e]` goes `C(n,2)/3 → C(n,2)/2`
  under the retraction and `δ` goes `1/3 → 1/2`. *"Project onto the image"* is not a repair; it is
  a bigger violation.

`c4.5` samples `dist(π, R_n)` over the body (120 exact points, `n = 3,4`; largest found `13/38` and
`4/11`) and is **labelled a lower bound, not a maximum** — the sup over `M_n` is not computed and is
not claimed.

---

## §6. Recommendation to `pm-onethird`

**Close the image-characterisation line.** In one paragraph: the target was well posed, the answer
is exact and short, and it is unusable — `conv(R_n) = M_n` is a theorem that kills every
inequality-shaped, LP-shaped and SDP-shaped consumer at once, before and after hypothesis (1) is
imposed; and the only region where the image is describable in closed form is F23's boundary class,
which sits **exactly on** the pair bound and therefore exhibits no slack for a realizability
argument to exploit. Nothing in row 8's route survives contact with either fact.

**What I would file next, and it is a NO-hunt rather than a construction.** Three independent arcs
— `mg-8b32` (fiber tightness), `mg-6ff4` (boundary density), and this one (image geometry) — have
each concluded that `d` **under the frozen hypothesis** is the only remaining lever, and none has
asked whether that lever can exist. `mg-6ff4` §9 declares the boundary → frozen bridge unbuilt;
`mg-345e` records that every density fact on record is a **lower** bound on `d`. The cheap
question is therefore: **is any upper bound on `d` for a frozen poset available from something
that is not the conjecture?** A NO on the record is worth more than a fourth arc arriving at the
same lever from a fifth direction. That is the successor this item names.

**What I would NOT do:** enumerate the facets of `conv(R_n ∩ K)` cell by cell. It is computable at
`n ≤ 7` and it will reproduce F23 — the cell's realizable maximum *is* `d ×` the ceiling, so any
facet found there is the density statement in another basis.

---

## §7. Where this could be wrong

- **`c2`'s theorem is only as strong as its quantifier.** `conv(R_n) = M_n` says nothing about
  *non-convex* certificates, and §3 names two that exist. What it forecloses is the shape an
  optimisation consumes, not every shape.
- **`c3` is `FP` at `n ≤ 7` and F23 is `FP` at `n ≤ 9`.** Neither says anything at `n = 10`, and
  both are about the boundary, not about frozen posets. The `1,2,3,5,8` sequence is not claimed as
  Fibonacci here; it is claimed as agreeing with `mg-6ff4`'s `Σ_k C(n−2k,k)` at five terms.
- **`c4.5` is a sample** and says so in its own verdict line.
- **`π*`'s maximality over `M_n` is cited, not re-derived.** This instrument rebuilds the witness
  and confirms its value; that `n/(n+1)` is the *maximum* is `mg-6bc2` Claim 3.1's.
- **The tier of `c1`'s `T1` is a proof and the tier of everything in `c3` is a census**, and
  `STATE.md:99`'s standing rule applies to any sentence aggregating them: the weakest kind in the
  set is `FP`.

---

## §8. The two facts `mg-8b32` left homeless — one filed, one already registered

`p8b32` declined to file both because nothing cited them; this ticket cites them, so both were
taken up. They did not end in the same place, and the difference is the point.

1. **"No hypothesis-population poset at `n ≤ 5` has a non-trivial marginal fiber."** Genuinely
   homeless — **filed as F25**, and **re-derived here independently** (`c3.4`, by the rank of the
   marginal map on `L(P)`, sharing no code with `lib8b32`'s `kernel_basis`). It also gained a
   **reason**, which a second measurement alone would not have given: below `n = 6` every poset in
   the population has `e(P) = 3` with `m = 2` pairs at `1/3`, and the marginal map is injective on
   a 3-point support carrying 2 independent pair coordinates. The first `e(P) = 9` member appears
   at `n = 6`, which is where the fiber first has room. So `a2.3`'s `n = 6` was **forced**.
2. **"The `n = 6` hypothesis population with `L* = identity` is 5 posets."** **Not filed, and
   deliberately** — F23 already carries the class count `Σ_k C(n−2k, k)`, which is `5` at `n = 6`.
   Filing it would put a numerical instance of a registered closed form into the registry as a new
   entry, which is exactly what `docs/FACTS.md`'s admission test forbids. It is recorded inside F25
   as a cross-reference, with the agreement at `n = 3…7` that this branch measured.

---

## §9. Provenance

`pc776`, 2026-08-13, from `mg-c776` — `p8b32`'s recommended successor, adopted by `pm-onethird`.
Nothing here imports `lib0fc6`; `lib8b32` is imported by the selftest arm alone and by no arm that
produces a finding. `a2.3` is cited and not re-run, `mg-0fc6`'s `M_n` separation sweep is not
touched, and `mg-6ff4`'s boundary census is cited as the prior claim on every number in `c3`.
