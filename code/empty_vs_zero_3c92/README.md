# `mg-3c92` — EMPTY is not zero, and the estate already knew

**The carry-forward this directory inherits, in `mg-9b6b`'s own words:**

> any arm that can return "no answer" and "the answer is zero" must print them
> differently, because the estate has now demonstrated one place where
> conflating them made a closed route read as open.

That is a proposal about **every arm in the estate**, and a proposal about every
arm is worth what its enforcement is worth. This directory measures both halves:
whether the estate exhibits the defect, and whether a matcher can see it.

---

## 1. The finding I would keep if only one survived

**The rule is already practice, at about nine sites in ten, and it was never
written down.** Two spellings answer the question independently:

| spelling | keeps EMPTY | loses it | keeps |
|---|---:|---:|---:|
| `f(X) if X else <fallback>` | 734 | 93 | **88.8%** |
| `max/min/next(…, default=…)` | 101 | 16 | **86.3%** |

They share no syntax and no population, and **they agree to one part in forty**.
`None` and a string are not numbers; a reader who gets one back cannot mistake it
for a computed answer, and that is the whole of the criterion.

So `mg-9b6b`'s proposal is not a reform. It is a **description** of what this
estate does by habit — and the reason to write it down is not to change the
88.8% but to make the **one in ten** visible, because the one in ten is where a
closed route reads as open.

⚠️ **The 550 string fallbacks are counted and are not a claim of intent.** Most
are display defaults (`" %s" % x if x else ""`) that satisfy the criterion
incidentally. The criterion is about what a **reader** can recover, never about
what an author meant. The `default=` row carries no such doubt: 89 of its 101 are
`None`, on the same call, in the same line, by the same hand that could have
typed `0`.

## 2. The one in ten, and how far it reaches

93 guarded ternaries choose a **number** for the empty case. The verdict on each
asks one narrow question:

> is the fallback the operation's **own value** on the empty input, or a
> **choice** made because the operation has no value there?

`sum(∅) = 0` and `len(∅) = 0` are definitions — the printed `0` inverts, and a
reader recovers the empty case from it. `max(∅)`, `min(∅)` and `x/0` have no
value — whatever is printed is a choice, and EMPTY has become 0. That is
decidable from the operation for **70 of the 93**; the remaining 23 carry a hand
verdict with a reason, in `z1_census.HAND`, and the arm **refuses** if that table
is incomplete or names a site the census did not find.

**61 COLLAPSE, 32 SOUND. 24 of the 61 are rendered into text at the site
itself** — the family `mg-9b6b`'s finding is about, and 17 of those 24 are a
percentage or a ratio: a `0.0%` printed for an **empty** population, which is not
wrong arithmetic but a reading of the population that the population does not
support.

⚠️ **COLLAPSE is not an accusation and this directory never uses it as one.** It
says the printed value cannot be inverted by a reader. Whether that matters is a
question about the reader, and `mg-9b6b` is the one case in this estate where the
answer is known to be yes.

## 3. What decides the shape of the remedy: it cannot be a lint

**1 004 sites take `sum(…)` over a filtered comprehension.** `sum([]) == 0` is
the **language's** collapse, not the author's: there is no fallback in the
source, no guard to find, and the printed `0` is byte-identical whether the
selection was empty or genuinely summed to nothing. None of those 1 004 is a
defect and no arm here says so — they are the measurement of what a matcher
**cannot reach**, and they are **11× the class it can**.

A rule enforced by looking would therefore be silent on the larger part of its
own subject while reporting confidently on the smaller. The rule has to be a
**reporting discipline** — what an arm prints when it has no answer — and not a
check anything runs. That is why this suite is **not on `build.sh`**, and the
reason is not cost: nothing here is a property the estate must hold, and a census
that gates is one its subjects learn to spell around. The first thing they would
spell around is §1's 88.8%, which is only worth having while nobody is scored on
it.

## 4. The instrument, and the two directions it is checked in

`ast`, not `grep`. The two most common `… else 0` shapes in this corpus are
`sys.exit(1 if bad else 0)` (177 of them) and matrix indicators `(deg[i] if i == j else
0)`, and no regex separates either from `max(xs) if xs else 0`. The census
requires a **bare** truthiness guard and requires a name from the guard to appear
in the true branch; dropping the second requirement takes the class from 93 to
520, so it carries 82% of the census and `z1` §8 prints both numbers rather than
asserting the requirement matters.

`z0` runs first and carries D0 — the pin resolves, is an ancestor of
`origin/main`, 1 249 files, 0 unparseable, class non-empty — because **every
central figure here is a small number, and a broken walk returns one for free**.

- **D1 must FIRE** on `mg-9b6b`'s own collapse, reconstructed. A detector that
  cannot flag the estate's single demonstrated instance is measuring something
  else, whatever else it flags.
- **D2 must NOT** flag the spelling that shipped — read out of the tree at the
  pin rather than re-typed (`mg-d2c2`). It is in **no class at all**, out on two
  independent grounds, and **which ground does the work is measured** by
  substituting on that line rather than argued.
- **Five plants**, one broken function each, the clean library asserted green
  **before and after** every one and re-measured rather than assumed. Two worlds
  are **required-inert** (D8: prose does not move the count; D9: an arithmetic
  `%` is not a print), because a detector that answers differently when a comment
  is reworded is measuring text.

## 5. What is not here, said plainly

- **The rule is ONE-DIRECTIONAL.** A site is a **proof** that a number was chosen
  for the empty case. **Absence proves nothing**: the collapse can live in a
  helper, in a `dict.get(k, 0)`, in a `%d` of a defaulted `None`, or in `sum([])`
  where there is nothing in the source to match on at all. The false-negative
  direction is unbounded and is stated everywhere the figures are.
- **PRINTED is syntactic containment**, and a **declared under-count**: a site
  assigned on one line and printed on the next is not counted.
  `code/audit_330a/s1_anchors.py:160` is exactly that and appears in this census
  as **not** printed, one line above the `print` that renders it. The direction
  is safe — PRINTED is a proof, NOT-PRINTED is not.
- **PRESERVING is drawn from the same syntactic family as GUARDED**, which is
  what makes §1's ratio a ratio rather than arithmetic over two populations. It
  costs something and the cost is declared: a line whose guard is a **comparison**
  is in neither class however carefully it keeps EMPTY apart — and `mg-9b6b`'s own
  shipped line is exactly such a line.
- **Nothing is repaired.** 61 collapses are reported and none is fixed. They sit
  in **31 directories**, each of which owns its own; a repair here would move
  those directories' committed transcripts and this branch would owe the
  refreshes, for a measurement nobody asked to be binding. (31 is the count of
  *directories touched*, not of transcripts that would move — that second number
  is not measured here, and it is the smaller claim that is safe to make.)
- **`STATE.md` is untouched**, so the ratchet is untouched and no twin re-pin is
  owed. `docs/FACTS.md` gets **no** entry — every measurement here is consumed by
  this landing, which is the registry's own homelessness test (`mg-3da1`) — and
  `docs/CONCEPTS.md` gets no row.

## 6. Reproduction

```sh
sh code/empty_vs_zero_3c92/run_all.sh     # ~60 s, exit 0 green / 1 fired / 2 refused
```

Every figure except `z1` §10 is a function of one commit (`AS_OF = 179da0a`),
read with `git show` and never off the worktree, so both transcripts have a fixed
point. §10 — the reflexive scan of this directory by its own rule — **must** read
the worktree, because this directory is younger than the pin and is in no tree the
pin can name: an exemption by **arithmetic** and not by rule, declared at the
section rather than left to be found. Two consecutive runs are byte-identical on
both transcripts; there is no clock and no randomness anywhere in the suite.

## 7. What remains

`PREDICTIONS.md` carries the exposure of every claim above, including the four
predictions this run **refuted** — and the one worth reading is **P1**, which was
refuted by exactly the confusion the ticket exists to describe, inside the
pre-registration of the directory measuring it: a probe returned *nothing at all*,
*nothing at all* was read as *zero*, and it was published as a measured fact.

Named and **not** done here:

- **The 1 004 are counted and not read.** Whether any of them ever renders a `0`
  for an empty selection onto a committed page is unknown; deciding it needs a
  reader per site, and nothing scans for it.
- **PRINTED stops at the expression.** A dataflow-aware version would raise the
  24, and by how much is not estimated here because an estimate would be a
  number nobody measured.
- **The compliance figure has no instrument watching it.** §1's 88.8% is a
  snapshot at one commit and nothing in this repository re-takes it; a directory
  landing tomorrow moves it and turns nothing red, by design.
