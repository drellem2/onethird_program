# mg-8af0 — predictions, committed BEFORE any script of this repair exists

Parent: **mg-fcb2**'s independent audit of the merged **mg-e35b** repair (`5f542f0`) to
NEGATIVE CONTROL 4. Three findings are assigned to me:

- **F1** — `controls.py:1927` prints *"the named load-bearing site is corrupted on %d/%d
  posets"* with **the same expression twice** (`% (N, N, …)`). A count that cannot move,
  in the very sentence that lands mg-fcf1's F3 (tautologies).
- **F2** — `verify_e35b.py:402` scores `forced == 3 and len(table) == 11` **against the
  literal `table` beside it**, under a heading that says *"EVERY COUNT THIS REPAIR
  PRINTS"*. That is why F1 survived: the 86/86 is not in the table.
- **F3** — *"no ridge in ≥ 3 facets, I4 zero"* is labelled **COULD MOVE** and is claimed
  to be *"the only one of the four that is a result"*. The brief says it cannot move at
  any n.

**Order is mandated and is the point:** F2 before F1. Repairing the count while the
verifier still scores against a literal leaves the mechanism that hid it intact.

Nothing below has been run. `controls.py`, `verify_e35b.py` and `face_complex.py` have
been **read**; no interpreter has been started in this worktree. Every number here is a
prediction from source, and misses are kept as written.

---

## The population and the grain, once, for everything below

- **P86** — the 86 posets up to isomorphism with **2 ≤ n ≤ 5**. This is `ps` in both
  `negative_control_incidence` and `verify_e35b.main`. Grain of every count over it:
  **one poset**.
- **P297** — the 297 **(poset, row)** pairs on which some mutation bites. Grain: one
  (poset, mutation) pair.
- **SITES** — the `%`-format *conversion specifiers* lexically inside the function
  `negative_control_incidence` in `controls.py`. Grain: **one specifier**, not one
  distinct value and not one printed line.

---

## E1 — the F1 numerator, on P86

`le_to_facet` is corrupted (the facet list actually differs) on **86 of 86**. So the
repaired expression prints **the same digits** as the tautology it replaces.

**E1 is the reason F1 survived a table headed "every count this repair prints", and it
is why fixing the string alone would be worthless:** the sentence was not wrong at
n ≤ 5, it was *unfalsifiable*. Predicting the digits do not move is predicting that no
reader could have caught this by reading the output.

## E2 — the constructed input that moves it (n = 1 admitted)

Both `le_to_facet` and `le_to_facet_offbyone` return the **empty chain** on the
one-letter word, so the site is not corrupted at n = 1. Over **1 ≤ n ≤ 5** (87 posets)
the repaired expression prints **86/87**; the tautology prints 87/87.

## E3 — the second constructed input (corruption made a no-op)

With `le_to_facet_offbyone` replaced by `le_to_facet`, the repaired expression prints
**0/86**; the tautology prints 86/86.

## E4 — F3's forcing, and my correction to the brief's version of it

The brief states the forcing as: *both facet maps return a chain of masks of sizes
1..n−1, so deleting one level leaves exactly two candidates to re-insert.*

**I predict that argument is incomplete, and that my repair needs a second case.** It is
the n ≥ 3 case. At **n = 2** a facet is a chain of length 1, its unique ridge is the
**empty chain**, and every facet contains it — there is no "level to re-insert" and the
bound holds for a different reason, namely |L(P)| ≤ 2 when n = 2. I predict:

- **E4a** — over all five modes and all posets **2 ≤ n ≤ 6**, the maximum ridge
  multiplicity is exactly **2**, and the number of (poset, mode) pairs where a ridge
  lies in ≥ 3 facets is **0**.
- **E4b** — every facet built by either map, in every mode, is a strictly increasing
  chain of masks of sizes exactly 1..n−1: **0 violations** over the same population.
  This is the premise the forcing rests on, and it is checkable rather than arguable.
- **E4c** — at n = 2 there is at least one poset whose unique ridge lies in exactly 2
  facets **by the degenerate route** (the empty chain in both facets), not by the
  two-re-insertions route. Count of such posets over 2 ≤ n ≤ 6: **1** (the 2-element
  antichain is the only poset with n = 2 and |L(P)| = 2).
- **E4d** — posets up to isomorphism with 1 ≤ n ≤ 6 number **405**, so "810 families"
  in the brief is 405 posets × 2 facet maps. If that is not what 810 counts, E4d misses.

**So the correction to controls.py is larger than the brief asks for:** not "I4's zero is
forced too", but **all four zeros are forced, and so is swap01's, and so is the
uncorrupted build's** — the property is a theorem about chains of prefixes and has
nothing to do with which mutation ran. I predict the honest replacement removes the
sentence *"its zero is the only one of the four that is a result"* outright rather than
moving the word "result" to another row.

## E5 — the F2 defect, demonstrated at the commit where it is still present

- **E5a** — with the artifact given a **twelfth** printed count and `verify_e35b.py`
  untouched, the V6 row prints **[PASS]**. (This is mg-fcb2's own construction; I am
  predicting it reproduces.)
- **E5b** — with `controls.py` given an entirely new printed count and the artifact
  regenerated, the V6 row prints **[PASS]**.
- **E5c** — the pre-repair row *does* move under one input and one only: an edit to the
  literal `table` in its own file. Relabelling I4's zero (F3) raises `forced` from 3 to
  4 and turns the row **[FAIL]** with the artifact untouched. **That is the exact shape
  of the defect** — the row is sensitive only to itself.

## E6 — the census, after repair

- **E6a** — SITES (see grain above) is **more than 11** — strictly more printed numeric
  positions than the classification table has rows — so no per-row mapping is available
  and the census must be reported at its own grain. Point estimate **85**, predicted
  band **55–120**.
- **E6b** — `negative_control_incidence` contains **0** f-strings, so a `%`-specifier
  census sees every formatted value in it. If this misses, the census has a silent
  channel on day one and I will say so rather than patch the number.
- **E6c** — the repaired row goes **RED** on E5a's input and on E5b's input, and RED
  when a classified count's anchor is deleted from the artifact.

## E7 — artifact regeneration

`controls.py` prints no timestamps, paths or hashes, so a fresh `python3 controls.py 5`
reproduces the committed `controls_output.txt` **byte for byte** at the pre-repair
commit. If true I will score the artifact against a fresh run, which closes the channel
the census cannot see (a hand-edited artifact); if false I will state that channel as
open rather than pretend the census covers it.

## E8 — what the F1 commit does to the artifact

Because of E1, the F1 repair changes **no digit** in `controls_output.txt`. Every byte
that moves in that commit is prose I added (population, grain, and the n = 1 witness).

## E9 — order, checkable after the fact

`git log --reverse` shows the F2 commit **before** the F1 commit, and the F1 commit's
diff to `verify_e35b.py` is **empty**.

## E10 — exit codes, all of them, before running anything

| runner | predicted exit |
|---|---|
| `code/face_geometry/run_all.sh` after repair | **0** |
| `code/face_geometry_repair_e35b/run_all.sh` after repair | **0** |
| `verify_e35b.py` at pre-repair commit, artifact untouched | **0** |
| `verify_e35b.py` **repaired**, against the **pre-repair** artifact | **1** |
| the F2 demonstration script | **0** (it asserts the old row fails to fire and the new one fires) |

## E11 — against myself

The pre-filed audit **mg-d3f3** will find **at least one printed count in code this
repair adds** that this repair does not classify. Eight consecutive generations put
their worst finding in what the commit added past what it was asked for; I have no
reason to think I am the ninth exception, and I am recording that before I write the
code rather than after the audit says so.

## E12 — against myself, sharper

The census (E6) is a **tripwire, not a proof of classification**: it fires when the set
of printed numeric positions changes, and it does **not** check that the 11 (12) entries
are the right ones or that their verdicts are correct. I predict mg-d3f3 records that
gap as a finding. It is stated here so that it is a **declared limit** and not a
discovery.
