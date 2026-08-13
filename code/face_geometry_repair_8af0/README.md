# mg-8af0 — landing mg-fcb2's F1, F2 and F3 on NEGATIVE CONTROL 4

mg-fcb2 audited the merged mg-e35b repair (`5f542f0`) and returned six findings. Three are
assigned here, and the brief mandates their **order**:

> Fix F2 FIRST, then F1. F2 is the reason F1 survived a table that was supposed to enumerate
> exactly this; repairing F1 while the verifier still scores against a literal leaves the
> mechanism that hid it fully intact and the next count will land in the same blind spot.

That order is in the git history and is checkable: `903a2e9` (F2) precedes `a8d1723` (F1).
(Post-rebase, the landed commits are `c420303`/`0c3a2ba`/`534c06b`/`66130f8`/`2657490`; every
file each repair commit touches carries the same blob pre- and post-rebase, so no work was
lost — measured by mg-d3f3's `a4.1`/`a4.2`.)

**The ordering was obeyed and it is not evidence, which this document did not say (mg-d3f3's
F-4, landed by mg-fa8a).** The committed transcripts at the three repair commits read
`0c3a2ba` **26 checks, 0 refuted**; `534c06b` **27 checks, 0 refuted**; `66130f8` **28 checks, 0
refuted**. **The repaired verifier was never watched failing on the real tree.** On the branch
that landed, F2-before-F1 is a *commit ordering*, not a demonstration — and `a1` says why it
could not have been one: F1's repair moved no digit (86/86 → 86/86), so F1's *return* moves none
either, and V6a/V6c/V6d are substring and byte comparisons against unchanged bytes. Worth
recording: the **sibling** branch of the same ticket (`0c39f34`, never merged) *did* exit 1 at
its F2 commit, because it added V7 at F2 time rather than at F1 time. The evidence that the
replacement rows fire lives in `demo_f2_row_can_go_red.py`, which is where a demonstration
belongs, and it now carries **C6** — F1 put back at the source — for the row that answers this.

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
population and grain **in its own name** — and a fourth was added later, by mg-fa8a, for the
channel none of the three could see:

| row | population | grain | goes red when |
|---|---|---|---|
| **V6a ANCHORED** | the 12 `TABLE` entries | one entry | a classified count is removed or reworded in the artifact |
| **V6b CENSUS** | the `%`-format expressions lexically inside `negative_control_incidence` | one conversion specifier (184 of them) | the **multiset of conversion types** in that one function moves |
| **V6c REGENERATED** | the artifact | one byte | `controls_output.txt` is hand-edited or stale |
| **V7b OPERAND** (mg-fa8a) | adjacent integer conversions separated by `/` in a `%`-format with a literal left operand, **anywhere in `controls.py`** | one such pair | a `%d/%d` is supplied the same source expression on both sides, or the F1 site stops being in the population |

**V7b is the row that reads `.right`, and it is the only one.** It is scored against
`controls.py`'s **operand tuples**, so it is the first row in this repair that could see a defect
whose whole content is which expression was supplied — which is what F1 was. Its limit is
declared beside it and printed into the transcript: it catches *the same expression on both sides
of a `/`*, not two different expressions that happen to be equal, and not an unmovable count that
is not one side of a ratio.

**V6b's cell said *"a count is added to or removed from the source"* and that is not the
measurement (mg-d3f3's F-3, landed by mg-fa8a).** What it compares is a seven-field dict of
conversion-type **multiplicities**, over **one** of the eleven calls `main()` makes. Two
constructions, both run: remove one `%d`-bearing count from `negative_control_incidence` and add
a different one → **census identical, every row green, exit 0**, a count added and a count
removed; and add a printed count to the *sibling* `negative_control_construction` → it **reaches
the artifact** and moves none of V6a/V6b/V6c/V6d, exit 0. The same count added *inside* the
section turns V6b and V6d red, so neither construction is reporting a row that never fires.
**"TRIPWIRE" is honest about the mechanism and was not honest about the scope**; the row name
and the two docstrings now carry the population, and the measurement is unchanged. Fixing the
name rather than widening the row is deliberate: a row whose name overstates it has a **naming**
defect, and weakening the row to make the old name true would be the same error pointed the
other way.

`forced` is still computed and printed. **It is no longer scored** — "3 of my own 12 rows say
FORCED" is a fact about this file, and scoring it is what produced the defect.

**The other four channels are enumerated, not hoped about.** A value can reach the artifact
through an f-string, a `.format` call, a `str()`/`repr()`/`format()` call, or a `%` whose left
operand is not a string literal — `ast` cannot tell that last one from arithmetic. Each is
counted and each is part of the declared census, so **a channel opening is itself a red row**.
The one non-literal `%` in the section today is `i % 3` inside a sign vector; it is declared as
**1**, not exempted, because an exemption nobody counts is how this class of defect gets in.

### The rows are watched firing

`demo_f2_row_can_go_red.py` — **30 cells, six constructions × five rows**. C1–C5 are as
`PREDICTIONS.md` E5/E6c forecast before the code existed; C6 and the V7b column were added by
mg-fa8a and are predicted in that file's own docstring:

```
  construction                                                     old row   V6a       V6b       V6c       V7b
  C1 twelfth count added to the ARTIFACT by hand                   GREEN     GREEN     GREEN     RED       GREEN
  C2 twelfth count added to CONTROLS.PY, artifact regenerated      GREEN     GREEN     RED       GREEN     GREEN
  C3 a classified count reworded in the ARTIFACT (61/86 -> 61/87)  GREEN     RED       GREEN     RED       GREEN
  C4 the same count reworded AT THE SOURCE, values unchanged       GREEN     RED       GREEN     GREEN     GREEN
  C5 mg-8af0's OWN edit to the table literal, repo untouched       RED       GREEN     GREEN     GREEN     GREEN
  C6 mg-fcb2's F1 PUT BACK at the source, artifact regenerated     GREEN     GREEN     GREEN     GREEN     RED
```

**C1 is mg-fcb2's own construction, verbatim.** **C5 is the point**: the only input the old
condition ever responded to is an edit to its own literal. **C4 is red for V6a alone** and **C6
is red for V7b alone**, so none of the four replacements is redundant.

**C6 is the row this table did not have, and it is four greens wide.** The defect this ticket was
named after, put back at the source, moves *nothing* the F2 repair added — and it moves no byte
of the artifact either: **41081 against the committed 41081**, measured in the demonstration
rather than asserted here. mg-d3f3 ran the same construction against **all 35 scored artefacts**
of this repair and scored **0 red**; V7b is the answer to that number and the C6 row is where it
is checked.

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

**V7 is not a check on F1, and mg-d3f3's F-1 is that this document said it was.** V7 asks
whether the *number* is 86 by a second route; the tautology answered 86 too. **The row that
asks whether the F1 defect is present is `V7b OPERAND`, added by mg-fa8a**: it `ast`-parses
`controls.py`, reads the **`.right`** of every `%`-expression, and scores that no `%d/%d`
anywhere in the file is supplied the same source expression on both sides — with the F1 site
itself required to be in that population, so the row cannot pass by the sentence being deleted.
mg-d3f3 measured **2 accesses to `.left` and 0 to `.right`** across every source-reading
artefact of this repair; V7b is the first. It reads 35 pairs, 0 repeating, the F1 site
resolving to `site_rows[3][1] / N` at `controls.py:2245`.

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

## F3 — the bound is **tight**, and the routine is **watched reporting 3** (mg-36f5)

**Ported from `polecat-z8af0`.** This ticket was **dispatched twice**. `cat-x8af0`'s first
submit failed at the refinery's `fetch` stage on `Could not resolve host: github.com`; its
claim was released; `cat-z8af0` was dispatched onto the same item **four seconds later** and
re-derived the whole repair over 43 minutes and 5 commits, under different filenames. x8af0's
branch was resubmitted and merged as `2657490`; z8af0 was stopped two seconds after a merge it
had no part in and **never submitted**. mg-687f audited both strands and established that main
is **ahead** of that branch on the mathematics — `controls.py` here withdraws the claim for
`facet_swap01` and the uncorrupted build too, and covers the n = 2 case z8af0's argument does
not reach. So this is a port of **two named results**, not a merge of the branch. Source:
branch `polecat-z8af0` at `98a5ff0`, file `code/face_geometry_repair_8af0/forcing_8af0.py`
(commit `a82acb3`), sections S3 and S4.

`probe_f3_tightness.py` — **10 checks, 0 refuted, 4.7 s.** Two things above are **measured** and
neither was on main:

### (1) The bound is TIGHT, and **"consecutive" is not the dividing line**

`probe_f3_ridge_multiplicity.py` measures the **premise** (every facet is a chain of masks of
sizes 1..n−1) and it measures the **bound** (no ridge in ≥ 3 facets). `verify_e35b.py`'s V4c
measures the same pair at n ≤ 5. **Neither asks whether the premise can be weakened** — so
"the zero is forced by the premise" sat on main with no measurement of how much of the premise
it needs, and the obvious generalisation was left looking open.

Swept over **every** level-size profile of length ≥ 2 at n = 3, 4, 5, 6 — **42 profiles** —
multiplicity ≤ 2 holds on **exactly one profile at each n: the full profile 1..n−1**, which is
exactly the profile both facet maps produce. At n = 5:

```
    [1, 2]      consecutive but partial   4       [1, 2, 3]   consecutive but partial   3
    [1, 3]      gapped                    6       [1, 2, 4]   gapped                    3
    [1, 4]      gapped                    4       [1, 3, 4]   gapped                    3
    [2, 3]      consecutive but partial   3       [2, 3, 4]   consecutive but partial   3
    [2, 4]      gapped                    6       [1, 2, 3, 4] THE FULL PROFILE         2
    [3, 4]      consecutive but partial   4
```

**`[1,2]` is consecutive and gives 4. `[2,3]` is consecutive and gives 3.** All **5**
consecutive-but-partial profiles at n = 5 admit a ridge in ≥ 3 facets. So I4's zero rests on
**the whole of the premise, not part of it**, and *"the premise can be weakened to consecutive"*
is **closed** rather than open.

**z8af0's own sweep fired on its author**: its first form predicted the dividing line *was*
consecutiveness, and the sweep refuted it on its own output; the branch kept the failing
transcript. That is why the row is stated this way and not more loosely.

### (2) A negative control — the routine is **seen reporting 3**

Main's *"0 families with a ridge in ≥ 3 facets"* was, on main, **the answer of a procedure never
observed to say anything else**. A routine returning 2 unconditionally prints every number this
repair prints. A constructed family with profile `[1, 3]` over a 3-element ground set — the
premise fails on it — reports **3**; the full profile `[1, 2]` over the *same* ground set
reports **2**.

**The control runs the PUBLISHED routine, and that is not free.** z8af0 ran its control through
a ridge-multiplicity routine it had written itself, which observes a *private re-implementation*
reporting 3 and leaves the published zero exactly as unwitnessed as it found it — this repair's
own defect shape, one level up. So `ridge_multiplicity` here is a thin wrapper over
**`face_complex.boundary_matrix`, the function `top_laplacians` itself calls**, and **T1
measures** it against `top_laplacians`'s own `ridge_facets` over all **2424 builds** rather than
asserting agreement: **0 disagreements on 2020 of them** (five modes), and **exactly 15** under
`ridge_drop` — **by construction and only downward**, because that mode deletes a ridge row
*after* the incidence is computed, and on all 15 (every one with |L(P)| = 2) the deleted ridge
was the only multiplicity-2 ridge there was. The one place the two routines differ **cannot
manufacture a ≥ 3** — and those 15 are also why T1 is an observation rather than a value
compared with itself.

The 11 numbers at n = 5 reproduce z8af0's transcript **row for row**. Its routine was
hand-rolled and this one goes through the library, so **the agreement is evidence**.

### (3) The port is subject to the defect it repairs, so it is checked for it

A negative control is an instrument, and an instrument that cannot fail is what this whole arc
is about. Three ways this port could have shipped its own defect, each closed by a row rather
than by an argument:

| the way it could fail | the row |
|---|---|
| the control runs a **private** routine, so main's published zero stays unwitnessed | **T1** — the wrapper is `boundary_matrix`, and agreement with `top_laplacians` is measured over 2424 builds |
| **T1 itself** compares a value with itself and cannot come out otherwise | the **15** `ridge_drop` disagreements — a value compared with itself does not produce them |
| the sweep passes while measuring **nothing** — an empty family has multiplicity 0, which is ≤ 2 | **T4's second row** — 42 profiles, smallest family 6 facets, no empty family |
| the tightness and control rows are satisfied by the very instrument they rule out | **T5** — both re-scored against a stub returning 2 for everything; **all three go red** |

**T5 is the load-bearing one.** Run with a routine that can only say 2 — the instrument main's
zero would come from if the objection were right — **7 of the 10 rows go red and the probe exits
1.** The three that survive are the ones that *should*: the full profile genuinely reports 2,
the non-empty-family row does not consult the routine at all, and T5 carries its own stub.

### What did NOT port, and the measurement that replaced it

The branch also carried `out_verify_e35b_F2COMMIT_exit1.txt` — **its** verifier exiting 1 on the
**real tree** at **its** F2 commit with F1 still present. It does not port: it is a transcript
of a **different script** on a **different tree**, and shipping it would put a record in this
tree that nothing in this tree can regenerate — this repair's own defect shape. **Main's
verifier was run on the real tree instead, at two commits, and the result is not the branch's:**

```sh
mkdir /tmp/f2 && git archive 0c3a2ba | tar -x -C /tmp/f2          # main's F2 commit, F1 unrepaired
cd /tmp/f2 && python3 code/face_geometry_repair_e35b/verify_e35b.py; echo $?   # 26 checks, 0 refuted; 0
```

**At main's F2 commit the verifier exits 0**, so the historical row the branch's transcript
records has **no counterpart here**: main's V6a/V6b/V6c are green on the real tree with F1
still present, which is what this README already implies (*"V6b would not have caught F1"* —
substituting a different expression into an existing `%d` moves no specifier).

**On main's tree today it exits 1, and that is a live finding this port did not create.**
`verify_e35b.py` on `main` at the time of writing: **28 checks, 1 REFUTED — V6b CENSUS,
measured 210 specifiers against a declared 184.** Bisected: `de86fee~1` measures 184,
`de86fee` measures 210. **`de86fee` (mg-17aa) rewrote `negative_control_incidence` and added 26
formatted values without re-declaring the census.** So V6b **has** been observed firing on a
real, unconstructed input — *it is firing right now, exactly as designed, and nobody has
answered it*. A consequence: `demo_f2_row_can_go_red.py` also exits 1 on main today (V6b is red
on its baseline, hence red in all five constructions), and its committed transcript
`out_demo_f2.txt` predates that and is **stale**.

**Neither is repaired here, and `out_demo_f2.txt` is deliberately left unregenerated.**
Re-declaring 184 → 210 is a decision about somebody else's tripwire — the one edit that silences
a live disagreement without answering it — and it belongs to whoever owns mg-17aa's debt, not to
a port of two F3 results. It is recorded here rather than left for the next runner to rediscover.

> **ANSWERED by mg-843d, 2026-08-13, and the paragraph above is why it could be.** Filing it
> rather than fixing it was right: the question was whether the 26 values belong in the census,
> and it is decided at the **site** level — mg-17aa's rewrite removed 5 sites (28 specifiers) and
> added 11 (54), all of them its own row rewrite, all of them `%`-format expressions inside the
> function, which is the population `census()` declares. **They belong; the declaration was the
> stale side and it moved to 210 with that derivation recorded at the declaration itself.** Two
> things came out of answering it that moving the number would not have produced: only **11** of
> the 26 are new *printed* values (14 sit in a branch mg-17aa keeps on purpose and the run never
> takes, 2 are an eagerly-evaluated `dict.get` default), which is now measured and scored as a
> new **V6d REACH** row with its own five-construction demonstration; and
> `code/face_geometry_repair_e35b/run_all.sh` is now **one of `build.sh`'s gated suites**, which is the
> half of the finding this section named — *nothing ran it.* See
> `code/face_geometry_repair_e35b/README.md`, "The census question, answered".
>
> **`out_demo_f2.txt` needed no regeneration and none was done.** With V6b green again the
> demonstration reproduces the committed transcript **byte for byte**, 20/20 cells. It was not a
> stale record; it was a correct record of a tree that had drifted away and has drifted back.
> Leaving it unregenerated rather than papering over the disagreement is what made that
> checkable.

*(That block records mg-843d. mg-fa8a did regenerate `out_demo_f2.txt`, because it changed the
demonstration itself — a sixth construction and a fifth column, **30/30 cells**.)*

### Not shown

- **n > 6.** The sweep is n = 3..6. The argument in the docstring of
  `probe_f3_ridge_multiplicity.py` is general; the tightness statement here is measured, not
  proved.
- **n = 3 carries no separating content** — it has exactly one profile of length ≥ 2 and that
  profile *is* the full one. The separation is measured at n = 4, 5 and 6.
- **Tightness is about the level-size profile, not about facet families in general.** Every
  family swept here is *all* chains with a given profile. A sparser family with a partial
  profile may well have multiplicity ≤ 2; what is shown is that the profile alone stops
  guaranteeing it.

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
| E10 | five exit codes | **HIT 4/5, and the fifth was never run** — corrected by mg-fa8a, see below |

**E6a, in detail, because a factor of two is not a rounding error.** I predicted 85 formatted
values in the section and there are **184** (150 integer, 34 string). The prediction was made by
eye from a function I had read but not counted, and being wrong by 2.2× is the reason the census
is a **declared measurement** and not a number written into prose. ~~What the miss changes: with
184 sites and 12 table entries there is no per-count mapping available, so V6b **cannot** be a
coverage check and is scored as a tripwire with that word in its own row name.~~

**That causal claim is false and is withdrawn (mg-d3f3's F-6, landed by mg-fa8a).** The miss
changed **nothing** about V6b's grain. E6a itself derived the conclusion *before measuring
anything*, from `SITES > 11`: *"E6a — SITES … is **more than 11** … so no per-row mapping is
available and the census must be reported at its own grain."* 85 > 11 and 184 > 11 give the
same verdict, so the 2.2× miss is not what made V6b a tripwire — **the reason was already in
the prediction that missed.** The addendum asked whether the miss and the limitation "agree";
they do not disagree about a *number* (both say 184), they disagree about a *cause*. What the
miss is really evidence about is **reading a thousand-line function by eye**, and that sentence
was not in the scoring table until now.

**E10, corrected: it was scored HIT 5/5 and the fourth row was never run (mg-d3f3's F-5, landed
by mg-fa8a).** Four of the five have a committed artefact behind them. The fourth —
*"`verify_e35b.py` **repaired**, against the **pre-repair** artifact → 1"* — has none, and
nothing in this repair builds that world. mg-d3f3's `a5` built it from `git`, in all three
readings the sentence admits:

| reading | measured | E10 said | |
|---|---|---|---|
| R-a the whole pre-repair tree (`5f542f0`), repaired verifier (`66130f8`) | **0** | 1 | MISS |
| R-b the repaired tree with a stale artifact from `5f542f0` | **1** | 1 | HIT |
| R-c the real tree at the F2 commit | **0** | 1 | MISS |

**HIT under one reading of three, and the one that comes out 1 is the stale-artifact reading —
where V6c fires, and V6c is a row about staleness, not about F1.** Under both readings that are
*about F1*, the answer is **0**. R-a is the sharpest measurement in mg-d3f3's audit and it is
about this instrument, not about that prediction: **the complete repaired verifier, run against
`code/face_geometry/` as it was before this repair touched anything, reports 28 checks, 0
refuted.** It did not separate the repaired tree from the unrepaired one, because every
difference this repair made lives in prose, in the operand of one `%`, and in the verifier's own
`TABLE` — and until `V7b OPERAND` **no row read any of those three**. This README draws the
run/reasoned distinction elsewhere repeatedly and at its own expense; E10's fourth row is the
one place it did not, and it is corrected here rather than dropped.

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
  `code/face_geometry_repair_e35b/run_all.sh` exits 0 with **28 checks, 0 refuted**. *(Both
  numbers record the tree this repair shipped on. Since mg-843d that runner has a second step and
  the verifier has 29 checks; since mg-fa8a's `V7b OPERAND` it has **30**. See "Running it"
  below.)*
- **It did not touch mg-fcb2's F4** (V6's justification for "NOT-GAUGE on 288 of 297"), which is
  not in this ticket's brief, nor the two findings of the six the brief does not assign.
- **V6b does not check that the 12 entries are the right ones.** It fires when the set of
  printed positions changes. `PREDICTIONS.md` E12 declared that limit before the code existed,
  and the demonstration prints it as a NOT-SHOWN line.
- **V6b would not have caught F1.** Substituting a different expression into an existing `%d`
  moves no specifier. The census closes the *next* count, not this one, which is exactly what
  the brief asked for.

  **The sentence that used to end that bullet was false and is withdrawn (mg-d3f3's F-1, landed
  by mg-fa8a).** It read *"That is why F1 needed V7 and not just a census."* **V7 is GREEN with
  F1 present** — measured, `a1.2` — because V7 checks `site == 86 and "corrupted on 86/86
  posets" in art` and both halves are true of the tautology too, which is this repair's own E1.
  V7's in-file comment never claimed otherwise (*"what this row CANNOT do is tell whether 86/86
  is the right answer for the right reason"*); the prose here did, and naming a remedy that does
  not remedy is the half of a declared limit that reads as candour. What F1 needed is a row that
  reads the **operand** of the `%` rather than the digits it prints. That row is **V7b OPERAND**,
  added by mg-fa8a in `verify_e35b.py`, and it is watched going red on construction **C6** of
  `demo_f2_row_can_go_red.py` — F1 back at the source, artifact byte-identical at 41081, and
  V7b the only one of five rows that moves.
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
sh code/face_geometry_repair_8af0/run_all.sh     # 37.6 s, 4 steps since mg-36f5, exit 0 since mg-843d
python3 code/face_geometry_repair_8af0/probe_f3_tightness.py   # 5.6 s, 8 checks, exit 0
sh code/face_geometry_repair_e35b/run_all.sh     # 43.9 s, exit 0, 30 checks + the V6d demo (mg-fa8a)
sh code/face_geometry/run_all.sh                 # ~20 s, exit 0
```

The first line read **`~32 s ... EXIT 1 today, see below`** until mg-843d, and the `1` was
`demo_f2_row_can_go_red.py` inheriting V6b's red baseline — it is 0 again now that the census is
answered, with `out_demo_f2.txt` unchanged. The third line read **`~5 s, exit 0, 28 checks`**; it
is the longer of the two runners now, and unlike every other line here it is **not** hand-invoked
— it is one of `build.sh`'s gated suites. Both re-measured on 2026-08-13, not carried forward.  **Every figure in this block was
re-measured again at mg-fa8a**, on the tree that ships this line, and the first two moved: the
8af0 runner is 32.0 s -> 37.6 s because `demo_f2_row_can_go_red.py` gained a sixth construction
(C6, F1 put back at the source), which is 26.95 s of the 37.6 on its own.  That is the price of
the demonstration and it is stated with the number rather than absorbed.

The first runner re-raises the **first** non-zero status, not the last, so an early refutation
cannot be overwritten by a later pass — and that path was tested with a deliberately failing
step before it was committed (mg-f922, mg-c2b3 are both about runners that could not fail).
