# mg-03cf — the checks behind `docs/FACTS.md`

Two arms, standard library only, **1.2 s measured** on this host. Wired into `./build.sh`.

```sh
code/facts_registry_03cf/run_all.sh
```

| arm | subject | population |
|---|---|---|
| `f0_registry_discipline` | the registry's own entries — every field present, every `KIND` a real mark, the `STATE.md` pointer not drifted, every link resolving | all 16 entries of `docs/FACTS.md` |
| `f1_adjacency_corollary` | `F1` and its frozen corollary, on an implementation importing nothing from this repository | `n = 3,4,5` exhaustive + `n = 6` sampled 400 (seed 20260812) — 4 716 posets, 21 063 incomparable pairs |

---

## Why there are exactly two arms and not sixteen

`docs/FACTS.md` is a **registry**, not a re-derivation. Fifteen of its sixteen entries are read
from deliverables that already certified them, and re-running those certifications here would
produce agreement that is a second reading of one implementation — `mg-8bc7`'s D6 and
`mg-8d66`'s D5, both kept in their own documents. So the arms cover the two things the registry
adds and the sources do not:

1. **`f0` — the remedy is an artifact of the same kind as the defect.** The registry exists
   because a figure quoted away from its population is how `0/132` happened (`STATE.md` row 3b).
   A registry whose own entries carried figures without their frames would be that defect at
   scale, wearing the language of a fix. So `f0` asks the registry the question the registry
   asks everyone else. **It caught its own author** — see D1 below.
2. **`f1` — the one registered statement that is not verbatim in its source.** `F1`'s frozen
   corollary is derived at `mg-03cf` and appears nowhere in the corpus. A registry entry
   carrying a derivation nobody has run is precisely what the registry is against.

## What `f0` does NOT check, said so its green is not over-read

It checks **structure**, not truth. It cannot tell whether a `SCOPE` line is correct, or whether
it is the right scope for its statement — that is a reading of six source documents, and it was
done by hand at `mg-03cf`, not by this file. What it catches is an entry **missing** the field,
which is the failure mode that scales: an entry added in a hurry six months from now with the
number and without the population.

## What `f1` CANNOT do, and this is the more important half

`F1`'s corollary is `δ(P) < 1/3 ⟹ P(adj) ≤ 2δ(P)` at every incomparable pair. `δ(P) < 1/3` is
the (1/3)–(2/3) counterexample condition and the conjecture is verified to `n = 14` (`mg-33f5`).
**So the population of frozen posets any instrument can enumerate is empty**, `f1` reports
`0 frozen posets` by construction, and its `0 failures` is zero failures in an empty population.
The arm runs the check anyway and prints the reason beside the zero, so that the number is never
read as a clean sweep. The corollary's entire warrant is its one-line derivation from `F1`.

## Corroboration that is not circular

`f1_adjacency_corollary.py` imports nothing from this repository. Its generator is checked
against **OEIS A001035** (3, 19, 219, 4231 labeled posets at `n = 2,3,4,5`) and its
linear-extension enumerator against `|L(antichain₅)| = 120`, `|L(chain₅)| = 1`, before it is
allowed to count anything. Its `n ≤ 5` sub-population reproduces `mg-8d66` `k4.2`'s **18 373**
incomparable pairs **exactly** — an independent implementation landing on the same population
size, which is the strongest available check that the two arms are talking about the same
objects.

## Positive controls

`f0` §5 plants two defects in a copy of the registry text and shows both **CAUGHT**: an entry
whose `SCOPE` field is renamed, and an entry graded with an invented mark (`` `probably` ``).
The suite's **status path** was demonstrated non-fail-open by planting a required field that no
entry has: `run_all.sh` exits **1**, and **0** with the plant removed.

---

## Defects of my own, kept

**D1 — `f0` went red on its author's own first draft, and the defect was the exact one it
exists to catch.** `F8`'s scope field was written `**SCOPE, and it is the whole content of the
entry.**` — a field renamed in passing, inside the entry with the most delicate frame in the
file (`n ≤ 5` exhaustive, `n = 6` sampled at 60, an unexplained regularity). Nothing about the
prose was wrong; the *field* was gone, which is how the next reader's parser, or the next
reader, stops seeing it. Fixed to `**SCOPE.**` with the emphasis moved into the sentence. **I
would not have found this by reading.**

**D2 — my first `run_all.sh` was fail-open, in a suite about controls that cannot fire.**
`python3 arm.py | tee out.txt` returns **tee's** exit status, so `set -e` could never see a red
arm — mg-06d1's D2 exactly, reproduced by me one commit after reading it. The status path now
runs each arm without a pipeline and reads `$?` from the arm. Demonstrated above.

**D3 — my first `f0` §3 anchored on a date string.** It matched
`Seeded 2026-08-12 with (\d+) entries` in `STATE.md`, so rewording the pointer paragraph — a
change with no mathematical content whatsoever — would have turned a **merge gate** red. That
is a wrong-direction control (mg-e35b's shape): red when nothing moved. Re-anchored on the
**link** to `docs/FACTS.md`, which is the thing that must not disappear, with the count read
from whatever wording surrounds it.

**D4 — `f1` is a second implementation, not a second population.** Its `n = 3,4,5` sweep covers
the same posets `mg-8d66` `k4.2` covers. Agreement is corroboration of the *code*, and the
`n = 6` sample of 400 is the only genuinely new population, which is small and is stated as
such in the transcript.

**D5 — one host, one arithmetic.** Everything here is exact rationals or integer counts, so
there is no float tolerance to be host-dependent — but the runtime figure (1.2 s) and the
`build.sh` arithmetic (~44 s → ~45 s) are measured on this machine only.
