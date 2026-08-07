# `mg-372e` — the `ε_spec = 2/(n+1)` staleness sweep

`mg-131e` refuted `ε_spec = 2/(n+1)` at `n = 6`. `mg-b488` landed that into `STATE.md` and
scoped itself there, saying so at `STATE.md:168`. **The source documents were never corrected.**
This instrument is the count behind that correction — a staleness sweep is a CHORE, not a claim,
so there is no independent audit and the reportable count is the control instead.

| script | what it does |
|---|---|
| `s1_census.py` | sweeps **six spellings** across the whole repo and prints the distribution by spelling and by file. Names what the count is a count of. |
| `s2_classify.py` | carries the hand classification of every `docs/` occurrence and **checks** that in the two repaired documents every occurrence is either marked with the refutation or on an explicit leave-alone allowlist. Exits non-zero if not. |
| `s3_control.py` | mutates the repaired documents **in memory** and asserts the `s2` detector fires. Nothing on disk is touched. |

`sh run_all.sh` runs all three (~1 s).

## Why six spellings and not one

The ticket named `2/(n+1)`. A sibling sweep tonight missed a live defect because its ticket
named one spelling and the live site was written another way. So the patterns are
whitespace-tolerant and cover the same statement in **three currencies**:

* `EPS` — `2/(n+1)`, spaced forms, `\frac{2}{n+1}` — the `ε_spec` normalisation
* `EINV` — `(n−1)/3` — **the same conjecture in `E[inv]` units**, which is how `mg-200d`'s
  Conjecture 4.3 is actually stated
* `DQ` — `2/(3n)` — the same conjecture in `d·q̄` units, `mg-200d §6`
* `PROSE` — *"two over n plus one"*, *"the per-slot constant"*

`s3`'s **M3** plants a live site spelled `2/(n + 1)` with spaces and confirms it is caught. A
sweep grepping the literal string `2/(n+1)` would have returned a clean zero on it.

## The classification, and why most sites are NOT defects

Three kinds, and only the first is a defect:

* **LIVE** — printed as a current value, or as a thing the programme still has. An *open
  conjecture* counts: the reader is not told it is false. **Repaired: struck in place with the
  refutation beside it**, this corpus's own practice.
* **CITED** — named as the refuted formula, or as historical/superseded. Already correct.
* **DERIVED** — inside `mg-131e`'s or `mg-94c3`'s own argument *about* it. Correcting these
  would make a document disagree with its own subject.

A fourth class the ticket did not anticipate and the sweep found:

* **COLLISION** — the same expression, a **different quantity**. `1 − λ_std(W_n) ≤ 2/(n+1)` is
  the Cheeger bound on the witness poset `W_n = C_n ⊔ C_1` and has nothing to do with the
  per-slot value; `n(n−1)/3` is an inversion *radius*. **A blanket edit on the string would have
  corrupted three documents.**

## What the controls establish, and what they do not

`s3` runs four mutations, each pre-declared. **M0 is declared NOT to fire and does not:**
stripping the `~~` glyphs alone leaves the words *"REFUTED"* and *"mg-131e"* in the same block,
so the refutation still travels with the site and the detector is right not to complain. That is
reported rather than tuned away — the detector is keyed on the refutation being *said*, not on
the glyph. `M1`/`M2` strip the glyphs **and** every marker word and fire at 7 and 20 sites.

`s2`'s first version was scoped to the **line** and fired 13 times against correctly-marked
prose, because a markdown strike routinely opens on one line and closes two lines later. It was
widened to the enclosing **block** — the unit a reader actually reads. **No site was moved onto
the allowlist to silence that**; the two allowlist entries added afterwards are inside
`mg-372e`'s own banner, where the formula is printed in order to say which sites were left, and
they are named there with that reason. A pattern relaxed until it returns `0` is unfalsifiable.

**What this does NOT establish.** It does not check the mathematics — `mg-131e` did that and is
cited, not restated. It does not classify `code/` occurrences: those are instrument transcripts
and pre-registration artefacts (`mg-ba78` set the precedent of leaving `PREDICTIONS.md`
byte-identical), and they are counted but deliberately not repaired. And a classification is a
**judgement**: `s2` checks that each site is marked or allowlisted, not that the class is right.
