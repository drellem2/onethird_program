# Is an UPPER bound on the incomparability density `d` available for a FROZEN poset, from anything that is not the conjecture? — **NO, AND THE NO IS ONE LINE OF CONTRAPOSITION**

`mg-0b96`, 2026-08-13, `mg-c776`'s named successor. **A NO-hunt, not a construction**, and it came
back NO. Instrument: [`code/frozen_density_0b96/`](../code/frozen_density_0b96/) — five arms,
standard library only, exact rationals on every verdict path, ~2.5 min. Predictions with the
exposure disclosed per line: [`code/frozen_density_0b96/PREDICTIONS.md`](../code/frozen_density_0b96/PREDICTIONS.md).

---

> ## THE VERDICT
>
> **A frozen-class density ceiling IS the (1/3)–(2/3) conjecture on a sub-class, by contraposition,
> at every strength.** For `D ∈ [0,1)`,
>
>     (1_D)  every frozen poset has d(P) ≤ D          ⟺     (2_D)  every poset with d(P) > D
>            [frozen = δ(P) < 1/3, STRICT]                          has δ(P) ≥ 1/3
>
> and `(2_D)` is the conjecture **verbatim**, restricted to `{P : d(P) > D}`. **At `D = 0` the
> restriction removes only chains, so `(1_0)` is the conjecture with nothing removed** — `{d > 0}`
> IS the set of non-chain posets, measured exhaustively to `n = 7`. `D` is a dial between the
> conjecture and
> nothing, and **there is no value of it at which the statement stops being the conjecture and
> starts being a lemma toward one.**
>
> **AND AT THE ONLY STRENGTH ROW 8 CAN CONSUME, THE PRICE IS 84 ORDERS.** `ε_sup = d·n/(n+1)`
> (`mg-0e8c`), so the ceiling that closes row 8 is `D_needed = ε_dem·(n+1)/n ≈ 2×10⁻²`. Primitivity
> forces `d ≥ 2/n` and a minimal counterexample is primitive, so the two meet **first at `n = 99`**:
> proving `(1_{D_needed})` proves the conjecture at **every order below 99**, against a census
> frontier of **14**. That reproduces `mg-33f5`'s `T2 = 100` from the density side — the two differ
> by exactly the `n/(n+1)` factor T2 drops, which is agreement to one unit and not a correction.
>
> **THE ANSWER IS NOT A FLAT NO, AND THAT MATTERS MORE THAN THE NO.** An unconditional upper bound
> does exist and owes nothing to the conjecture: two elements with the same strict up- and down-set
> are swapped by an automorphism, so `Pr = 1/2` and `δ ≥ 1/2`; hence a frozen poset has at most one
> element comparable to nothing, and **`d ≤ 1 − ⌈(n−1)/2⌉/C(n,2) = 1 − Θ(1/n)`**, kind `U`, all `n`.
> It is **SHARP on its own class** — attained at every `n = 3…8` — and it is worth `ε_sup = 0.98` at
> `n = 99`, short of `ε_dem` by a factor of **49**, *widening* with `n`. `mg-345e`'s P5 grep found
> zero frozen-conditional upper bounds on `d` in this corpus; this is one, and filing it is what
> stops the next arc reading that zero as "none can exist" or re-deriving it as a door.
>
> **THE LITERATURE SURVEY, MEASURED RATHER THAN READ.** Of the seven class exclusions `mg-33f5` §2
> lists, **five deliver any upper bound on `d` at all** at `n = 9` and the strongest is `5/6`;
> jointly they leave a residue of **28 611 posets at `n = 9`** whose maximum density is `7/9`
> **= `1 − 2/n` exactly, as it is at `n = 8` (`3/4`, 452 posets)**. And there is an **explicit
> family** — verified outside all seven classes at every `n = 15…40`, `d` from `0.838` to `0.947` —
> whose range **starts where the census frontier ends**. So at every `n ≥ 15` there is a NAMED poset
> of density above `0.83` that nothing on the record decides either way.
>
> ⚠️ **THE RESIDUE IS EMPTY BELOW `n = 8` AND AN INSTRUMENT STOPPING AT `n = 7` WOULD HAVE REPORTED
> TOTAL LITERATURE COVERAGE.** Every poset on at most 7 elements is 6-thin, because no element can
> be incomparable with more than `n − 1 ≤ 6` others (measured: max incomparability degree over every
> poset at `n = 7` is exactly 6). That is a fact about the population's size read as a fact about
> the literature's reach, and it is the trap this measurement had to be taken past.
>
> ⚠️ **AND NONE OF IT IS A FROZEN-CLASS MEASUREMENT.** The frozen class is empty at every `n` any
> enumerator reaches — re-established here exhaustively to `n = 8` rather than quoted — so this is a
> question about what is **provable**, not about what is enumerable, and every arm says so.

---

## §1. The question, and why it is the only one left

Three independent arcs converged on `d` under the frozen hypothesis and none asked whether it can
exist:

- **`mg-8b32`** closed the fiber level: the `M_n` relaxation is already tight fiber by fiber.
- **`mg-6ff4`** measured `d` **at the boundary** — `max{d : δ = 1/3} = 4⌊n/3⌋/(n(n−1))`, `FP` to
  `n = 9`, [`docs/FACTS.md`](FACTS.md) F23 — and its §9 says in as many words that it *"does not
  bridge"* boundary to frozen.
- **`mg-c776`** closed the image level: `conv(R_n) = M_n`, so no inequality-shaped realizability
  condition exists at all, and where the image meets hypothesis (1) it lands on F23's class, which
  **saturates** the pair bound with zero slack.

Row 8's residual after all three: *every route below `1` must add a realizability fact*, and the one
surviving lever is `d` under freezing. `mg-c776` §6 filed the successor in one sentence: **"is any
upper bound on `d` for a frozen poset available from something that is not the conjecture?"** This
document answers it.

## §2. The answer (`d1`)

**THEOREM.** For every `D ∈ [0,1)`, `(1_D) ⟺ (2_D)`. *Proof: contraposition, twice. `d(P) > D ≥ 0`
forces `m ≥ 1`, so the restricted class never lands on a chain and `(2_D)` is never a vacuous
reading of the conjecture.* **Kind `U-id`** — an identity of statements.

Three things around it are not one word, and each is the kind of thing that gets asserted:

1. **The two sides agree poset by poset**, computed through opposite comparisons, over every
   isomorphism class at `n ≤ 7` (2 044 non-chain posets at `n = 7`) × 9 values of `D`, **0
   disagreements**. ⚠️ This is a control on the **implementation**; a tautology's warrant cannot be
   improved by a run. What a run catches is `frozen` and `δ ≥ 1/3` failing to be complements in
   code, which every number in this directory rests on.
2. **`(2_D)` is never a statement about nothing.** `|{d > D}|` is non-empty at every `D < 1` and
   every `n ≥ 2` — the antichain sits at `d = 1`. A weakening that emptied its own hypothesis would
   be the way this equivalence could be true and worthless.
3. **`D = 0` recovers the conjecture verbatim.** `{d > 0}` is exactly the set of non-chain posets —
   1, 4, 15, 62, 317, 2 044 at `n = 2…7`, matching the non-chain count at every `n`.

**How this differs from `b4.4`'s circularity, and it is worth stating because the shapes rhyme.**
`b4.4`'s `gap = 0` separator is exact and **circular** — it names the very quantity the programme
bounds. This one is not circular: `d` is an elementary combinatorial count and names nothing from
the argument. It is **the conjecture on a sub-class**, which is a different and, for a lever, worse
thing to be: a circular statement is unusable and visibly so, whereas a sub-case of the target looks
exactly like a lemma until somebody prices it.

## §3. The price, at the only strength row 8 can use (`d2`)

`ε_sup = d·n/(n+1)` and the wall is already down — proven, all `n`, L4-free — at `ε_sup ≤ ε_dem`.
So the ceiling that closes row 8 is `D_needed(n) = ε_dem·(n+1)/n`, which is `2×10⁻²` to two figures
at **every** `n`; it does not soften.

| | |
|---|---|
| what row 8 needs | `d ≤ D_needed(n) ≈ 2×10⁻²` |
| what primitivity forces from below | `m ≥ n−1`, so `d ≥ 2/n` (`STATE.md:55`, ledger row 2) |
| first `n` at which a primitive poset can meet the ceiling | **`n = 99`** |
| conjecture verified through | `n = 14` (Gupta, preprint; refereed frontier 11) |
| orders the ceiling would deliver that no census has reached | **15 … 98 = 84 orders** |

`mg-33f5` §3's `T2` reads `2/ε_spec = 100`; that drops the `n/(n+1)` between `ε_sup` and `d`, and
carrying it gives 99. **Neither is corrected here** — T2 is right at its own precision, and the
point is that the density route reaches a threshold already on the record from a second direction.

**And 84 is the floor of what proving it buys, not the whole.** Above `n = 99` the same ceiling
still forces any frozen primitive poset into the regime where L1b is already a theorem — which is
what row 8 wants. A statement that hands you 84 unreached orders of the conjecture *and* the
regime above them is not an ingredient of a proof; it is a stronger statement wearing a lemma's
clothes.

## §4. The survey (`d3`) — measured on the definitions, not read off a table

`mg-345e`'s P5 grep asked this corpus and got zero. This arm asks the **literature**, in a form a
grep cannot answer: every class exclusion is a set the conjecture is proved on, so what it delivers
about `d` under freezing is `max{d(P) : P ∉ C}` — a frozen poset must lie outside `C`.

| class (`mg-33f5` §2) | source | `max{d : P ∉ C}` at `n = 9` |
|---|---|---|
| width ≤ 2 | Linial 1984 | **1** — no bound at all |
| 6-thin | Peczarski, Order 25 (2008) | **1** — no bound at all |
| semiorder | Brightwell | `17/18` |
| height ≤ 2 | ⚠️ `mg-33f5` §2 lists **no source** | `11/12` |
| `N`-free | Zaguia, EJC 19(2) #P29 | `11/12` |
| cover graph a forest | Zaguia, arXiv:1610.00809 | `8/9` |
| non-trivial automorphism | Peczarski 2017 | `5/6` |

**A cell of `1` means the exclusion says nothing about density: the antichain already lies outside
the class.** The strongest single row is `5/6 = 0.833`; row 8 needs `2×10⁻²`.

**Jointly**, the residue — outside every listed class at once — is **452 posets at `n = 8` with max
`d = 3/4`** and **28 611 at `n = 9` with max `d = 7/9`**. Both equal `1 − 2/n` exactly; the extremal
member carries exactly `n − 1` comparable pairs. ⚠️ Two values of `n` is a pattern, not a law, and
nothing is extrapolated from it — what carries past `n = 9` is the construction:

**`lib0b96.family(n)`** — the incidence poset of an asymmetric unicyclic graph, plus one element
above one edge-element, plus one isolated element when the parity needs it. Comparabilities are
`Θ(n)`. Membership of all seven classes is **computed** at every `n = 15…40`: outside all of them,
at `d` rising from `88/105 ≈ 0.838` to `739/780 ≈ 0.947`. **Its range starts where the census
frontier ends**, so for every `n` it covers there is a named poset of density above `0.83` that no
census and no class exclusion on the record decides.

**The reason the direction is uniform, and it is the survey's actual content.** Every exclusion on
the record cuts the **sparse or structured** side — bounded width, bounded incomparability degree,
forbidden sub-structure, a symmetry. Cutting the sparse side of a class yields a **lower** bound on
`d` (a frozen poset must be *not* 6-thin, so some element is incomparable with ≥ 7 others; must have
width ≥ 3; and so on). **`mg-345e`'s "lower bounds only" is not an accident of what has been written
down — it is what results of this shape produce.**

## §5. The one bound that does exist (`d4`), and it is filed

**LEMMA (`U`).** If `x ≠ y` have the same strict down-set and up-set, `(x y)` is an automorphism, so
`Pr[x < y] = 1/2` and `δ(P) ≥ 1/2`. Verified by computing `δ` rather than trusting the symmetry:
1 179 such posets at `n = 7`, **0 with `δ < 1/2`**.

**COROLLARY (`U`).** A frozen poset has at most one element comparable to nothing, so at least
`⌈(n−1)/2⌉` comparable pairs, so **`d ≤ 1 − ⌈(n−1)/2⌉/C(n,2) = 1 − Θ(1/n)`**. Registered as
[`docs/FACTS.md`](FACTS.md) **F26**.

It is **sharp on its own class** (attained at every `n = 3…8` — read off the table, not asserted
beside it), and it is worth:

| `n` | `d` bound | `ε_sup` at it | short of `ε_dem` by |
|---|---|---|---|
| 15 | `0.9333` | `0.8750` | 43.8× |
| 99 | `0.9899` | `0.9800` | **49.0×** |
| 300 | `0.9967` | `0.9933` | 49.7× |

**And it moves the wrong way**: the improvement on the trivial `d ≤ 1` *shrinks* with `n`, while
row 8 needs a constant.

**The ceiling on every argument of this shape.** A frozen poset is **rigid** (Peczarski 2017), and
rigidity is the weakest thing any *"this small structure forces a balanced pair"* argument can
force. `max{d : P rigid}` is `11/14` at `n = 8` — so the whole family of such arguments is bounded
by roughly `1 − 2/n`, and the explicit family of §4 is rigid by construction at every `n` it covers.

## §6. Recommendation to `pm-onethird`

**Close the density lever as a route, and record the reason once so a fifth arc does not arrive at
it from a sixth direction.** The lever is not a hard open question that might yield — it is the
conjecture on `{d > D}`, and at row 8's strength it is 84 unreached orders of the conjecture. That
is the same service `b4.4`'s circularity finding performed for the `gap = 0` route, by naming why
rather than by failing quietly.

**What the record should carry, and it is one entry plus one sentence.** F26 (the unconditional
bound), which is filed here; and, if `pm-onethird` wants row 8's cell to stop attracting this
question, the equivalence of §2 stated at the row. **This document does not edit row 8** — `STATE.md`
is at its ratchet ceiling and the wording of the wall is `pm-onethird`'s.

**The one thing that would change this verdict, named so it can be looked for.** A result of the
form **`δ(P) ≥ f(d)`** with `f` increasing and `f(2×10⁻²) ≥ 1/3` — a **density-to-balance** bound
rather than a structure-to-balance one. Nothing of that shape appears in `mg-33f5`'s survey or in
this corpus. **It is not ruled out here**, and it is a different object from everything §4 measured:
every known exclusion is a statement about *structure*, and this would be a statement about *count*.

## §7. Where this could be wrong

- **The class predicates are readings of definitions.** `N`-free is read on **covers**; a different
  reading gives a different class. "height two / bipartite" is included although `mg-33f5` §2 gives
  it **no source** — including a class the literature may not have can only *shrink* the residue,
  so the generosity runs against this document's own finding.
- **`d3`'s residue is a residue of the CLASS EXCLUSIONS ONLY.** At `n = 8, 9` its members are also
  decided by the `n ≤ 14` census. The two kinds are printed side by side and **must not be added**;
  the explicit family is the part outside both.
- **The family is `FP` over `n = 15…40`.** The construction is uniform in `n` and every membership
  is computed, but no proof of asymmetry at general `n` is given.
- **`d2`'s census-cost figure is an asymptotic estimate**, loose by ~9 bits at the one `n` where it
  can be checked, and loose in the direction that *overstates* the cost.
- **Nothing here shows the ceiling is FALSE.** Every finding is about what proving it would deliver
  and what the record currently delivers.
- **The equivalence is `U-id` and everything else here is `FP` or `U`.** Per `STATE.md`'s standing
  rule, any sentence aggregating them must say **`FP`**.

## §8. What was NOT done, per the ticket's own scope discipline

- **The boundary was not re-measured.** F23 stands; no fourth census of that class is here.
- **No facet of `conv(R_n ∩ K)` was enumerated.** `mg-c776` §6 priced it and the ruling stands.
- **No arc was opened on `M_n`.** `mg-0fc6` §7's ruling stands.
- **`STATE.md`'s ledger was not edited.** The pointer sentence moves from 25 entries to 26 for F26,
  which is word-neutral against the ratchet, and nothing else in that file changes.

## §9. Provenance

Instrument [`code/frozen_density_0b96/`](../code/frozen_density_0b96/), five arms, `sh run_all.sh`,
worst exit 0. `lib6ff4` is imported for enumeration and `δ` — a controlled primitive, re-checked
here against OEIS A000112 and against brute-force enumeration of `L(P)` because an import whose
controls live elsewhere is unchecked from here. Every class predicate is written in this directory
and carries a hand-built in/out witness. Two wrong-direction controls: the population warning
(frozen class empty, measured to `n = 8`) and a **must-say-YES** control — the same machinery asked
for a ceiling on the non-empty pseudo-frozen class `δ < 1/2` returns one strictly below 1 at every
`n = 3…7`, which is what makes the NO a fact about the hypothesis rather than about the tool. ⚠️
That control's own ceiling **rises** with `n` (`2/3, 1/2, 7/10, 11/15, 17/21`), which was not
predicted and is reported rather than smoothed.
