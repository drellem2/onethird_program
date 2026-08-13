# `code/frozen_density_0b96/` — can a frozen poset's density be bounded ABOVE, by anything that is not the conjecture?

The instrument for `mg-0b96`. Deliverable:
[`docs/OneThird-FrozenDensity-mg-0b96.md`](../../docs/OneThird-FrozenDensity-mg-0b96.md).
Predictions, with the exposure disclosed per line: [`PREDICTIONS.md`](PREDICTIONS.md).

**The question.** `STATE.md` row 8's supply bound is `ε_sup = d·n/(n+1)`, so the wall is already
down at `d ≲ ε_dem ≈ 2×10⁻²` and the open region is the dense one. Three arcs — `mg-8b32`,
`mg-6ff4`, `mg-c776` — have each concluded that `d` **under the frozen hypothesis** is the only
remaining lever, and none asked whether the lever can exist. This asks.

**The answer, in one line.** A frozen-class ceiling `d(P) ≤ D` **is** the (1/3)–(2/3) conjecture on
`{P : d(P) > D}`, by contraposition, at every `D`; at `D = 0` it is the conjecture verbatim; at the
only `D` row 8 can consume it delivers the conjecture at every order below 99, against a census
frontier of 14. One unconditional upper bound does exist and it is worth `1 − Θ(1/n)`.

⚠️ **THE FROZEN CLASS IS EMPTY AT EVERY `n` ANY ENUMERATOR REACHES.** Nothing here is a measurement
*on* frozen posets. `d0` T6 re-establishes the emptiness on this instrument's own population, so
that no zero printed later is read as a clean sweep.

## The arms

| arm | what it does | cost |
|---|---|---|
| `d0_selftest.py` | the controls, **including two that must come back the other way**: T6 the population warning (the frozen class is empty here, measured), and T7 a **must-say-YES** control — the same machinery asked for a ceiling on the non-empty pseudo-frozen class `δ < 1/2`, which returns one strictly below 1. Plus the imported enumerator against OEIS A000112, the imported `δ` against brute-force enumeration of `L(P)`, `is_rigid` against a full `n!` search, and a witness pair for each of the seven class predicates. | ~14 s |
| `d1_equivalence.py` | **the finding**: `(1_D) ⟺ (2_D)` by contraposition, the two sides computed by different code paths and compared poset by poset over `n ≤ 7`; non-vacuity of `{d > D}`; the `D = 0` degeneration to the conjecture verbatim; and the strictness distinction, recorded as **un-witnessed** because no witness can exist in an empty class. | ~2 s |
| `d2_price.py` | what the lever costs at the only strength row 8 can use: `D_needed(n) = ε_dem(n+1)/n`, primitivity's `d ≥ 2/n`, the crossing at **`n = 99`** (reconciled with `mg-33f5`'s `T2 = 100`, which drops the `n/(n+1)`), and the **84 orders** past the census frontier that proving it would deliver. | <1 s |
| `d3_literature.py [nmax]` | the survey, **measured on the definitions**: for each of the seven class exclusions `mg-33f5` §2 lists, `max{d(P) : P ∉ C}` — the best upper bound that exclusion can deliver — exhaustive to `n = 9`; the joint residue; why it is empty below `n = 8`; and an **explicit family**, verified at every `n = 15…40`, outside all seven classes at `d = 1 − Θ(1/n)`. | ~2 min at `n = 9` |
| `d4_unconditional.py` | the one upper bound that **does** exist and owes nothing to the conjecture — interchangeable elements force `δ ≥ 1/2`, so `d ≤ 1 − ⌈(n−1)/2⌉/C(n,2)` — verified, priced against `ε_dem`, and shown to move the wrong way in `n`. Plus `max{d : P rigid}`, the ceiling on every argument of that shape. | ~7 s |

`sh run_all.sh` runs all five and reports the worst exit. **This suite is NOT in `build.sh`** — it
is a one-off measurement, not a control, and the committed `out_*.txt` are its record.

## What is imported, and what is deliberately not

`lib6ff4` (`code/boundary_epsilon_6ff4/`) supplies poset enumeration, `δ`, exact pair biases and
`width`. That is **reuse of a controlled primitive**, the same call `lib30bd` makes on
`lib_f771.verdict_for`, and `d0` T1/T2 re-check both the enumerator and `δ` here anyway — an import
whose controls live in another directory is an unchecked dependency from this one's point of view,
and this arm's whole subject is a claim nobody re-checked.

Every **class predicate** is written here and imported from nowhere, because none of them existed
in this repository and each is a **literature definition** — the thing most likely to be wrong. `d0`
T3 puts a hand-built in/out witness to each.

## The three kinds in play, kept apart

A sentence aggregating them must say the weakest (`STATE.md`'s standing rule).

| | what it is | kind |
|---|---|---|
| `d1`'s equivalence | contraposition | **`U-id`** — it is an identity of statements, and the run checks the implementation, not the theorem |
| `d4`'s bound | a proof, no census in it | **`U`** |
| every census here (`d3`'s residue, `d4`'s rigid ceiling, `d0`'s populations) | exhaustive at `n ≤ 9` | **`FP`** — and says nothing at `n = 10` |
| `d3`'s explicit family | computed membership, `n = 15…40`, uniform construction | **`FP`** over that range; asymmetry for general `n` is **not proved here** |

## Where this could be wrong

- **The class predicates are readings of definitions.** `N`-free is read on **covers**; a different
  reading gives a different class. "height two / bipartite" is included although `mg-33f5` §2's
  table gives it **no source** — including a class the literature may not have can only *shrink*
  the residue, so the generosity runs against this directory's own finding.
- **`d3`'s residue is a residue of the CLASS EXCLUSIONS ONLY.** At `n = 8, 9` its members are also
  decided by the `n ≤ 14` census. The two kinds are printed side by side and must not be added.
  The explicit family is the part outside both.
- **The family is `FP` over `n = 15…40`.** The construction is uniform and each membership is
  computed rather than argued, but no proof of asymmetry at general `n` is given here.
- **`d2 m5`'s census cost is an asymptotic estimate**, loose by ~9 bits at the one `n` where it can
  be checked, and loose in the direction that overstates the cost. It is used only to say the
  order-98 census is out of reach by a margin no constant would close.
- **Nothing here shows the ceiling is FALSE.** Every finding is about what proving it would deliver
  and what the record currently delivers. `d4 m5` names the one shape of result that would change
  the verdict — a density-to-balance bound `δ(P) ≥ f(d)` — and does not rule it out.
