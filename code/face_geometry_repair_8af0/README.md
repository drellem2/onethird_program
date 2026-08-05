# mg-8af0 — landing mg-fcb2's F1, F2 and F3 on NEGATIVE CONTROL 4

mg-fcb2 audited the merged mg-e35b repair (`5f542f0`) and returned six findings. Three are
assigned here, and the brief mandates their **order**:

> Fix F2 FIRST, then F1. F2 is the reason F1 survived a table that was supposed to enumerate
> exactly this; repairing F1 while the verifier still scores against a literal leaves the
> mechanism that hid it fully intact and the next count will land in the same blind spot.

That order is in the git history and is checkable: `903a2e9` (F2) precedes `a8d1723` (F1).

| finding | what it was | landed by |
|---|---|---|
| **F2** | `verify_e35b.py:402` scored `forced == 3 and len(table) == 11` — **a condition on the literal beside it** | `903a2e9` |
| **F1** | `controls.py` printed *"the named load-bearing site is corrupted on %d/%d posets"* with `% (N, N, …)` — **the same expression twice** | `a8d1723` |
| **F3** | *"no ridge in ≥ 3 facets, I4 zero"* labelled COULD MOVE, and *"its zero is the only one of the four that is a result"* | this commit |

---

## F2 — the scoring mechanism, not the string

The row named the population **EVERY COUNT THIS REPAIR PRINTS** and measured the length of the
list underneath it. **No change to `controls.py` and no change to the artifact could move it.**
That is why F1 survived: the tautological `86/86` is not in the table, and nothing was going to
notice that it wasn't.

Three rows replace it, each scored against something **outside the file**, each carrying its
population and grain **in its own name**:

| row | population | grain | goes red when |
|---|---|---|---|
| **V6a ANCHORED** | the 12 `TABLE` entries | one entry | a classified count is removed or reworded in the artifact |
| **V6b CENSUS** | the `%`-format expressions lexically inside `negative_control_incidence` | one conversion specifier (184 of them) | a count is added to or removed from the source |
| **V6c REGENERATED** | the artifact | one byte | `controls_output.txt` is hand-edited or stale |

`forced` is still computed and printed. **It is no longer scored** — "3 of my own 12 rows say
FORCED" is a fact about this file, and scoring it is what produced the defect.

**The other four channels are enumerated, not hoped about.** A value can reach the artifact
through an f-string, a `.format` call, a `str()`/`repr()`/`format()` call, or a `%` whose left
operand is not a string literal — `ast` cannot tell that last one from arithmetic. Each is
counted and each is part of the declared census, so **a channel opening is itself a red row**.
The one non-literal `%` in the section today is `i % 3` inside a sign vector; it is declared as
**1**, not exempted, because an exemption nobody counts is how this class of defect gets in.

### The rows are watched firing

`demo_f2_row_can_go_red.py` — **20 cells, five constructions × four rows**, all as
`PREDICTIONS.md` E5/E6c forecast before the code existed:

```
  construction                                                     old row   V6a       V6b       V6c
  C1 twelfth count added to the ARTIFACT by hand                   GREEN     GREEN     GREEN     RED
  C2 twelfth count added to CONTROLS.PY, artifact regenerated      GREEN     GREEN     RED       GREEN
  C3 a classified count reworded in the ARTIFACT (61/86 -> 61/87)  GREEN     RED       GREEN     RED
  C4 the same count reworded AT THE SOURCE, values unchanged       GREEN     RED       GREEN     GREEN
  C5 mg-8af0's OWN edit to the table literal, repo untouched       RED       GREEN     GREEN     GREEN
```

**C1 is mg-fcb2's own construction, verbatim.** **C5 is the point**: the only input the old
condition ever responded to is an edit to its own literal. **C4 is red for V6a alone**, so none
of the three replacements is redundant.

---

## F1 — the count is measured, and the sentence was *false*, not merely unmovable

The numerator is now `mutation_applied_at_site` asked of **every** poset in the sweep rather
than of the vacuous column alone.

**The digits do not change: 86/86 before, 86/86 after.** That is the finding rather than an
anticlimax — no reader could have caught this from the artifact, which is exactly why F2 had to
be landed first. `probe_f1_count_moves.py` constructs the two inputs that separate a measurement
from a tautology:

| population | tautology prints | measured |
|---|---|---|
| shipped, 2 ≤ n ≤ 5 | 86/86 | **86/86** |
| **n = 1 admitted**, 1 ≤ n ≤ 5 | 87/87 | **86/87** |
| **corruption made a no-op** | 86/86 | **0/86** |

At n = 1 both `le_to_facet` and `le_to_facet_offbyone` return the **empty chain**, so the site
is not corrupted there. **On that population the shipped sentence is FALSE**, which a
cannot-move finding does not by itself establish — mg-fcb2 constructed it and it reproduces.

The sentence now carries its population (the posets the section sweeps, 2 ≤ n ≤ 5) and its
grain (one poset; corrupted iff the facet **list** differs), and names both moving inputs
without quoting numbers the run does not compute. `verify_e35b.py` gains **V7**, which
re-derives 86/86 from `top_laplacians` rather than from the helper `controls.py` uses, and the
**twelfth** table entry — the count that was printed, was a tautology, and was absent from a
table headed with its own population.

---

## F3 — the zero is forced on **all four** rows, not three

mg-e35b wrote that three of the four ≥ 3-facet zeros are forced and that I4's *"is the only one
of the four that is a result"*. **That is false**, and it is this section's own defect shape one
more time: a property recorded as an 86-poset measurement.

**The forcing is a property of the facet family, not of the mutation.** Both maps are prefix
families, so every facet is a strictly increasing chain of masks of sizes 1..n−1. A ridge is
such a chain with the level of some size *k* deleted; a facet containing it re-inserts a mask of
size *k* between the surviving levels of sizes *k*−1 and *k*+1 — two sets differing in exactly
two elements, so **exactly two candidates**. Hence no ridge lies in more than 2 facets, at any
n ≥ 3, **whichever map built it** — which also makes swap01's zero and the uncorrupted build's
zero forced.

**mg-8af0's own brief states the forcing in a form that does not cover n = 2, and this repair
needed the second case.** `PREDICTIONS.md` E4 recorded that before any of this code was written.
At n = 2 a facet is a single mask, the unique ridge is the **empty chain**, and every facet
contains it — there is no level to re-insert. The bound holds there because |L(P)| ≤ 2 when
n = 2. Exactly **1** poset (the 2-element antichain) hits that case.

`probe_f3_ridge_multiplicity.py` checks the **premise** (every facet is a chain of masks of
sizes 1..n−1) and the **bound** over all five modes plus the uncorrupted build, every poset
2 ≤ n ≤ 6: **2424 (poset, mode) builds, 76554 facets, 0 premise violations, maximum ridge
multiplicity 2 on every mode.** The brief's *"810 families over n ≤ 6"* is a third population —
405 posets with 1 ≤ n ≤ 6 × 2 facet maps — and is reproduced separately so the three are not
read as one.

`verify_e35b.py` gains **V4c** (the same check at n ≤ 5, with the n = 2 builds counted
separately) and the table entry is relabelled **FORCED BY CONSTRUCTION**.

---

## Predictions, scored

`PREDICTIONS.md` was committed at `41bdbfa`, before any script of this repair existed. **Two
misses, kept as written.**

| | prediction | result |
|---|---|---|
| E1 | site count = 86/86, digits unchanged | **HIT** |
| E2 | n = 1 admitted → 86/87 | **HIT** |
| E3 | no-op corruption → 0/86 | **HIT** |
| E4 | the brief's forcing is incomplete at n = 2 and my repair needs a second case | **HIT** |
| E4a | max multiplicity 2, zero ridges in ≥ 3 facets, n ≤ 6 | **HIT** |
| E4b | 0 premise violations | **HIT** |
| E4c | 1 poset in the n = 2 degenerate case | **HIT** |
| E4d | 810 = 405 posets (1 ≤ n ≤ 6) × 2 facet maps | **HIT** |
| E5a | old row GREEN on a twelfth count added to the artifact | **HIT** (C1) |
| E5b | old row GREEN on a twelfth count added at the source | **HIT** (C2) |
| E5c | old row RED only on an edit to its own literal | **HIT** (C5) |
| E6a | census > 11; **point estimate 85, band 55–120** | **MISS — 184** |
| E6b | 0 f-strings in the section | **HIT** (see below) |
| E6c | the repaired rows go red on those inputs | **HIT** |
| E7 | the artifact regenerates byte-identically | **HIT** — so V6c exists |
| E8 | the F1 commit moves no digit in the artifact | **HIT** — every count in that diff is unchanged; the digits added are ticket ids and the two witnesses named in prose |
| E9 | F2 commit precedes F1; **F1's diff to verify_e35b.py is empty** | **HALF-MISS** — order holds, the second clause does not |
| E10 | five exit codes | **HIT, 5/5** |

**E6a, in detail, because a factor of two is not a rounding error.** I predicted 85 formatted
values in the section and there are **184** (150 integer, 34 string). The prediction was made by
eye from a function I had read but not counted, and being wrong by 2.2× is the reason the census
is a **declared measurement** and not a number written into prose. What the miss changes: with
184 sites and 12 table entries there is no per-count mapping available, so V6b **cannot** be a
coverage check and is scored as a tripwire with that word in its own row name.

**E6b was right and incomplete.** There are 0 f-strings, as predicted. But writing the census
turned up a channel the prediction did not name — a `%` whose left operand is not a string
literal, which `ast` cannot distinguish from arithmetic. There is exactly one (`i % 3`). It is
counted rather than exempted. **The channel existed on day one of the instrument and the
prediction did not see it**; that is recorded here rather than quietly folded into the number.

**E9, in detail.** The order holds and is the load-bearing half. The second clause — that F1
would not need to touch `verify_e35b.py` — was written on the assumption that a repair can
change a count without touching the verifier. **That is precisely the property F2 removes**, and
the F1 commit adds the twelfth table entry and V7 because the count is now classified. The miss
is informative and is kept.

---

## What this repair did NOT do

- **It did not re-audit mg-e35b's mathematics.** The dichotomy (297 = 288 + 9 + 0), the
  gauge/non-similar splits, the vacuity separation and the absorbability routing are untouched
  and re-run green: `code/face_geometry/run_all.sh` exits 0,
  `code/face_geometry_repair_e35b/run_all.sh` exits 0 with **28 checks, 0 refuted**.
- **It did not touch mg-fcb2's F4** (V6's justification for "NOT-GAUGE on 288 of 297"), which is
  not in this ticket's brief, nor the two findings of the six the brief does not assign.
- **V6b does not check that the 12 entries are the right ones.** It fires when the set of
  printed positions changes. `PREDICTIONS.md` E12 declared that limit before the code existed,
  and the demonstration prints it as a NOT-SHOWN line.
- **V6b would not have caught F1.** Substituting a different expression into an existing `%d`
  moves no specifier. That is why F1 needed V7 and not just a census — the census closes the
  *next* count, not this one, which is exactly what the brief asked for.
- **The n ≥ 3 forcing argument is not machine-checked for n > 6.** The argument is general; the
  sweep that makes its premise a checked fact rather than a reading of two functions is not.
- **No claim is made that 86/86 is right for the right reason.** V7 is a second route to one
  number. The evidence that it is a measurement is the pair of inputs that move it.
- **STATE.md was not edited.** The coverage numbers are routed to pm-onethird, which is the
  choice mg-2789 and mg-e35b both made at this site.
- **mg-fcb2's own transcript was not re-run and will not go green.** Its check `A1.4a` scores
  `worst >= 3` — the *mathematical* claim the artifact used to make, not the artifact's wording —
  so it stays `[REFUTED]` after this repair and should. `code/face_geometry_audit_fcb2/` is
  untouched; an audit's transcript is a record of what it found, not a status board.
- **mg-e35b's README was annotated, not rewritten.** The false sentence stays visible with the
  correction under it.

## Running it

```sh
sh code/face_geometry_repair_8af0/run_all.sh     # ~21 s, exit 0
sh code/face_geometry_repair_e35b/run_all.sh     # ~5 s,  exit 0, 28 checks
sh code/face_geometry/run_all.sh                 # ~20 s, exit 0
```

The first runner re-raises the **first** non-zero status, not the last, so an early refutation
cannot be overwritten by a later pass — and that path was tested with a deliberately failing
step before it was committed (mg-f922, mg-c2b3 are both about runners that could not fail).
