# OneThird — SCOPE `compression2.tex`: **it is a different construction from the closed arc, its own headline is a real theorem, and it is REALIZABILITY-BLIND — the poset-dependence washes out at one named site.** `scope-recommendation`

**Work item.** `mg-0fc6` (repo `onethird_program`), filed by `pm-onethird` as the successor
`mg-69f1` should have declared and did not.
**Subject.** [`docs/imports/compression2.tex`](imports/compression2.tex) — Daniel's second
compression drop, dropped 2026-08-13T00:02Z, imported verbatim by `mg-69f1` and **read by nothing
until this ticket**.
**Read against.** Daniel's own stated target, volunteered unprompted at 00:40Z: *"right now i'm
attracted to compression as a vehicle for realizability … we can combine them in convex
combinations … we can design them via poset structure which gives the missing ingredient."*
**Instrument.** [`code/compression2_scope_0fc6/`](../code/compression2_scope_0fc6/), `run_all.sh`,
**~35 s measured**. Pre-registered at `2edf68a` before one line of it existed.
**Cited, not re-measured.** `mg-8d66`, `mg-145f`, `mg-409a` — and see §5 for **where** they are
allowed to be quoted, which is one paragraph of the note and not the note.

---

## 0. RECOMMENDATION

This is a recommendation to `pm-onethird`, not a decision.

> ### **SCOPE: `low`, and low for a *different reason* than the first drop was.**
>
> `compression.tex` came back 3/10 because its route was **closed by ceiling at every `k`**.
> `compression2.tex` is **not that object** and that closure does **not** apply to it — measured,
> not assumed (`a4.2`: the scale partition is not an admissible `k`-foliation; its fibers are not
> cubes). It is a genuinely different construction and it deserves the separate reading it has
> now had.
>
> It scores low on its own terms:
>
> 1. **Its headline (6) is a correct theorem that is numerically empty** at every `n` this
>    programme reaches — weaker than the free bound `e(P) ≤ n!` below `n = 16,777,063`.
> 2. **It emits the wrong currency, in the wrong direction.** It consumes an inversion bound and
>    returns an entropy bound; `STATE.md:158`'s untried slot wants `log e(P) → E[inv_e]`, and
>    `a3.2` measures that a bound of this shape cannot deliver it.
> 3. **It is realizability-blind** — §2, and this is the answer to what Daniel actually asked.
>
> ### **AND ONE PART SHOULD NOT BE FILED WITH THE REST.**
>
> `a4.3b` measures that `compression2`'s scales are a **filtration**, so a convex combination of
> its increments is a genuine Littlewood–Paley multiplier — **canonical, where the same step on
> `compression.tex`'s transverse pair is not a projection at all.** Daniel's convex-combination
> instinct is *right on this family and wrong on the other*, and that distinction is worth
> keeping whatever happens to the rest of the note.

---

## 1. What the note proposes, in one paragraph, in Daniel's terms

Put the elements in the order of the distinguished extension `L*` and bisect recursively. At each
node of that dyadic tree, record only the merge word — which half each successive element came
from. That is merge sort's recording tape, and it is **lossless**: the tuple of words determines
`L` and `L` determines the tuple (`a1.1`, 89,926 linear extensions, 0 collisions). Inversion
distance to `L*` then splits **exactly by scale**, because every pair is separated at exactly one
node, and each node's contribution is the area between the random merge path and the canonical
one. The 1/3–2/3 bias says each node's area is `≤ m²/3` rather than the unconstrained `m²/2`, so
the merge path at *every* node is macroscopically displaced toward `L*`; an elementary Pinsker
argument turns that displacement into a constant entropy loss per node, and summing over the
`n log₂ n` total word length gives `log₂ e(P) ≤ 0.9399 · n log₂ n`. The note's own view is that
the entropy saving is secondary and the real prize is its identity (8): **one BK swap moves one
word at one scale**, which would convert the spectral problem into a multiscale family of
median-graph problems.

**Note the word "compression" is doing different work in the two drops.** `compression.tex`'s
`C_o` genuinely **forgets** — it is a quotient. `compression2`'s encoding forgets **nothing** — it
is a re-coordinatisation. They are two different kinds of object, and *"combine them in convex
combinations"* is not type-correct until one says which object is being combined (`P11`, and §4).

## 2. THE CRUX: does "design them via poset structure" inject realizability?

**No. It only appears to, and the wash-out has one named site.**

The programme's requirement is on the record and is sharp — `STATE.md:21`: *"every route below `1`
must add a **realizability** fact"*, and `:23`: the bridge *"is hard because it must use that `σ`
ranges over a **real poset's** linear extensions — it is false for abstract frozen
distributions."* `a2` tests `compression2` against exactly that, with the oracle **watched
discriminating first** (`a2.1`: accepts all 4,469 uniform linear-extension measures at `n ≤ 5`,
rejects three constructed non-examples including the corpus's own two-atom law).

The exhibit is constructive:

```
  mu1 and mu2 have IDENTICAL pair marginals
  mu1 IS a linear-extension measure · mu2 is NOT (not uniform on its support)
  BOTH sit inside hypothesis (1), same value, max flip = 1/3
  the note's ONLY input, (1), takes the same value on both        1/3
  every step of the note returns the SAME verdict on both
       H(mu1) = 3.169925   H(mu2) = 3.149673 — the MEASURES differ; the note's INPUT does not
```

> **The poset-dependence washes out at exactly one place: `L*` and hypothesis (1) are both
> functions of the PAIR MARGINALS, and the dyadic tree is a function of `L*`. Nothing downstream
> reads `P` again.**

That is the answer to Daniel's design. The dyadic tree *is* built from poset structure — but only
through `L*`, and `L*` is a marginal object. A compression parameterised by the poset still has to
**constrain something an abstract frozen measure could not satisfy**, and this one does not: the
whole chain runs verbatim on a measure that is not any poset's, at `n = 4, 6, 8` (`a2.2`).

**What would have changed this verdict was filed in advance.** `PREDICTIONS.md` names four
conditions under which `P5` would have lost — a step that fails for some non-realizable
`μ ∈ M_n(0)`; a bounded quantity that separates the realizable measures inside the information
set; a dependence of the tree on `P` beyond `L*`; a conclusion false for a frozen measure and true
for every poset in the same information set. **None fired.**

## 3. The headline, priced

**(6) is true, is not sharp, and is numerically empty where we live.**

| | measured |
|---|---|
| first `n` at which `0.9399·n log₂ n < log₂ n!` | **16,777,063** (`a1.6`, binary search) |
| `max{H(μ) : μ ∈ M_n} / log₂ n!`, `n = 3…7` | `0.907, 0.900, 0.893, 0.887, 0.883` (`a3.1`) |
| …as a fraction of the note's own ceiling | `52.5% … 58.8%` |
| the obvious witness `(2/3)Unif + (1/3)δ_{L*}` | `0.882 … 0.741` of `log₂ n!` — **below** the optimum by ~0.13, so the measure a reader reaches for understates the set |
| the note's per-node lemma vs. `log₂ C(2m,m)` | weaker for every `m < 27` (`a0.7`) — below 54-element blocks it says less than *"the word is a word"* |

Asymptotically (6) is a real constant-factor theorem and the note's own defence of it is correct:
it does **not** follow from a single global inversion bound, because the 1/3 constraint holds
*per pair* and therefore at every block at every scale. That is a genuine mechanism. It is also
`Θ(n)` bits at each of `Θ(log n)` scales against a target that needs the *first* `n log₂ n` of
those bits back, which is why the crossover sits at `1.7 × 10⁷`.

**And the direction is the harder problem.** The note proves `inversions ⟹ entropy`;
`STATE.md:158`'s untried slot wants `entropy ⟹ inversions`. `a3.2` measures that the reverse
cannot be had from a bound of this shape: the two-atom law has `H = 0.9183` bits **at every `n`**
— eight orders of magnitude below the note's ceiling at `n = 10⁶` — and simultaneously the
**largest** `E[inv_e]` anything in `M_n` can have. Low entropy and maximal inversions coexist.

`a3.3` closes the loop by re-deriving `max E[inv_e]` over `M_n` on code that shares nothing with
`Op-Form`: `= C(n,2)/3`, i.e. `ε_spec = n/(n+1)`, attained by the two-atom law, `n = 3…59`.
**The note's hypothesis IS the pair-bias information set, and the wall's currency on that set is
already at equality** (`Op-Form` Claim 6.1 / `mg-6bc2` Claim 3.1, `STATE.md:21`). That — not
`mg-8d66`, not `mg-145f` — is the closure that bites the main body.

## 4. Daniel's three questions, answered

**(1) *"compressions that preserve linear statistics" and "compressions that reduce entropy a
lot" — one family or two?* Two, and they are different KINDS.** `compression.tex`'s `C_o`/`C_e`
are a **quotient** (they forget alternate prefixes; the energy identity is about what survives).
`compression2`'s merge encoding is a **bijection** (`a1.1`, 0 collisions across 89,926
extensions). The first can preserve a statistic because it discards; the second discards nothing
and its "entropy reduction" is a bound on `H(L)`, not a property of a map. **Combining them
convexly is not type-correct as stated** until the object is chosen.

**(2) *Is the convex-combination step sound?* Two different answers, because there are two
families — and this is the note's best news.**

- **On `compression.tex`'s transverse pair: no, and Daniel's suspicion is correct.**
  `(Π_o + Π_e)/2` is **not idempotent** at 40 of 40 posets where the two differ (`a4.3a`). It is a
  self-adjoint operator with spectrum in `[0,1]`; there is no σ-algebra it is the conditional
  expectation of. **That is fine if the quadratic form is what is wanted — but it is not a new
  degree of freedom**: `mg-8d66`'s `kI − Σ Π_i` *is* `k(I − ` the equal-weight convex combination
  `)`, so "combine compressions convexly" is the object that arc already priced.
- **On `compression2`'s scales: yes, and canonically.** The projections are a **filtration**
  (`Π_a Π_b = Π_min(a,b)`, and the finest is the identity), so the increments are mutually
  orthogonal and `Var(f) = Σ_l ‖D_l f‖²` exactly. A weighted combination of increments **commutes
  with every `Π_k`** — a Littlewood–Paley multiplier, diagonal in the scale decomposition, with
  spectrum `{λ_l}` (`a4.3b`).

  *Honest scoping of that:* the variance identity is Pythagoras and holds for **any** filtration.
  The content is the **nestedness**, which is by construction of the dyadic tree. It is still a
  real structural difference from the transverse pair, and it is the one place Daniel's stated
  design is strictly better than the objects the closed arc used.

**(3) *Does poset-design inject realizability?* No — §2.** One named site, `L*` and (1) both
being functions of the pair marginals.

## 5. The note's closing paragraph — the ONE place the spectral closure is the right citation

The note says its most promising part is (8), and asks *"whether the Dirichlet form of the
standard statistic admits a corresponding scale decomposition… the real gain is that the spectral
problem has been converted into a multiscale family of median-graph problems."* That paragraph,
and only that paragraph, aims at the spectral problem by name.

**Identity (8) is exact** — `a4.1`, 197,520 BK edges at `n = 4, 6, 8`: exactly one word changes,
by one adjacent `AC↔CA`, at the LCA of the swapped pair, every time.

**And `mg-8d66` still does not apply to it.** `a4.2`: the scale partition is by the LCA of the
swapped *elements*, not by word *position*; the same position carries edges of several scales and
vice versa, and 14,016 of 94,656 fibers have non-power-of-2 size — **they are not cubes**.
`mg-8d66`'s ceiling is a statement about cube foliations from non-adjacent position classes and
does not reach this object. **Quoting it here would be the error the ticket warned against.**

**So the question was answered directly, in `a5`, and the answer is negative.**

- The Dirichlet form **is** graded by scale: `E = Σ_l E_l`, exact, because the edge set partitions.
- The grading **annihilates the coarse filtration**: `E_l(Π_l f) = 0`, exact. This is (8) restated
  as a statement about quadratic forms, and it is the strongest true thing in this direction.
- **The alignment that the note needs is FALSE.** `E_l(f) = E_l(D_l f)` — which would make the
  Rayleigh quotient a ratio of two sums over the same index — fails at 3 of 5 posets measured.
  `E_l` annihilates everything **coarser** than `l` but **reads everything finer**: a scale-`l`
  edge holds the finer words fixed, and `f` is still a function of them, so `f(L) − f(L')` does
  not survive the averaging inside `Π_{l+1}`. The structure is **triangular**,
  `E(f) = Σ_l E_l(Q_l f)` with `Q_l = I − Π_l`, not diagonal.
- **Written down anyway, the per-scale bound is not lossy but empty.** `μ_l = 0` at the finest
  scale at every poset measured — the 2×2 merges are single BK edges and do not connect their own
  increment space — so `gap_BK ≥ min_l μ_l` reads `gap_BK ≥ 0`. Visible at `n = 4`.

> **The form is graded and the norm is graded and the two gradings do not match. Grading a form is
> not decoupling it, and the note's step from (8) to "a multiscale family of median-graph
> problems" is exactly that step.**
>
> **This was `a5`'s own asserted lemma, refuted by its own run, and it is kept in the arm rather
> than quietly rewritten** — because the mistake the instrument made is the mistake the note is at
> risk of.

**Finally, the currency.** Even had the decomposition worked, its output is a **lower bound on
`gap_BK`**, and `STATE.md:29` records both halves of what that is worth: the bridge L1b *"is NOT
SPECTRAL IN ANY LOAD-BEARING SENSE"* (`mg-05ec` §5), *"nothing in this programme consumes a BK-gap
lower bound"* (`mg-145f`) — and a **sharp** lower bound is already proven by someone else, Wilson
2004, `gap_BK ≥ (1 − cos(π/n))/(n−1)`. `mg-145f` is an inherited corpus search and not a theorem,
and is quoted here as such; it is quoted **at this paragraph only**.

## 6. What I recommend `pm-onethird` do with this

1. **Do not open an arc on the main body.** Its hypothesis is `M_n(0)`, the currency on `M_n(0)`
   is at equality, and its output is in a direction `a3.2` measures cannot be reversed.
2. **`CONCEPTS.md` §5 (*"Intuitions that have been killed, and by what"*) is where `a2`'s finding
   belongs** — *"a compression designed from the poset injects realizability"* is a natural and
   attractive intuition, it is exactly what Daniel named, and it now has a two-line constructive
   refutation. That file is `pm-onethird`'s and this ticket has not touched it.
3. **Keep `a4.3b` separately from the verdict.** The filtration/multiplier distinction is a small,
   true, reusable fact about which convex combinations are canonical, and it is orthogonal to
   whether this note's route works.
4. **Tell Daniel the target, not just the score.** He is not relitigating the closed arc; he aimed
   somewhere else and said so. The honest report is: *the aim is the right aim — `STATE.md:21`
   says in terms that every route below `1` needs a realizability fact — and this construction
   does not supply one, because it reads the poset only through its pair marginals.* The next
   compression he designs should be checked against `a2.3`'s two-measure exhibit **first**: if the
   construction cannot tell `μ1` from `μ2`, it is marginal-only, whatever it is built from.

---

## 7. Provenance, and the thing that went wrong twice

`mg-69f1` imported this file with a title reading *"IMPORT-ONLY FIRST, then scope. Do NOT repeat
`mg-2ffd`'s split"* — and then closed with **no successor**, which is what `mg-2ffd` had done that
morning. The prose said the right thing twice and had no force. The fix is a **tag**:
`declares-remainder` makes `mg done` refuse without `--successor`, and this ticket recommends it
for any ticket whose title names a second phase.

This ticket was worked by two polecats. `p0fc6` filed the pre-registration (`2edf68a`) and wrote
the instrument, and was stopped at 00:51Z for the redeploy quiesce with `a3` and `a4` written but
never run; its worktree was preserved and read rather than re-derived, and the instruments were
committed **on top of** the pre-registration at `91b0448` so the ordering is a property of the
DAG. `q0fc6` ran `a3` and `a4`, added `a5`, and wrote this document.

**`P5` — realizability-blind, `p = 0.90` — was filed before any instrument existed and is the
unwelcome answer to the question this ticket's own addendum was most hopeful about.** It was
confirmed constructively. That is what the pre-registration was for, and it is only legible
because the commit precedes the results in the history. Eight of eight live bets confirmed; `a5`
is post-hoc and is scored against nothing.
