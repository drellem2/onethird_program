# mg-1abe — WHICH REVISION IS EACH COMMITTED FIGURE A FACT ABOUT?

**398 of 541 committed transcripts reproduce from the commit that carries them.
112 do not. 31 have no runner in the tree at all, so nothing can be said about
them. The buckets sum to 541 and nothing is rounded into a neighbour.**

**Of the 112 that do not reproduce, 5 are FALSE RECORDS — a decision changes
when they are re-run where they sit. That is the number the ticket is about,
and it is 5 of 541, not 112 of 541.**

**And the ticket's mechanism is not the main cause. 103 of the 112 have a
producer that reads repository-global state: they were displaced by the next
commit anyone made, with no rebase and no regeneration anywhere near them. 19
have a producer that is outright NONDETERMINISTIC and could never have
reproduced, at any commit, for anyone.**

All figures below are facts about `81214a9`, and about no other revision. By
the time this merges, `main` will have moved past it. That is not an accident
of timing; it is the subject.

Everything below is derived by `sh run_all.sh`, whose transcripts are committed
beside it. Every count names the population it is over and the grain of its
value. Where this repair repeats a number from another agent or artifact, it
says whose it is and whether it was re-derived — and it re-derived what it
could.

---

## 0. THE ANSWER TO THE QUESTION THAT WAS ASKED

The ticket says the first part is the point: *measure the blast radius, publish
the three counts with the denominator named, and do not fix anything until it
is measured.* Nothing in this directory changes a single committed transcript
belonging to another ticket. The census is the deliverable.

### CLASS 2 — the blast radius. Population: 541 committed transcripts at `81214a9`. Grain: one verdict per transcript file.

| bucket | count | of 541 |
|---|---:|---:|
| `REPRODUCES` — the runner rewrote the file, bytes identical | **398** | 74% |
| `DIFFERS` — the runner rewrote it, bytes not identical | **112** | 21% |
| `NO-RUNNER` — no `run_all.sh` in that directory at that commit | **31** | 6% |
| `NOT-REGENERATED` — runner completed, never wrote this file | 0 | |
| `RUNNER-FAILED` — runner could not start | 0 | |
| `TIMED-OUT` — exceeded the 900 s budget | 0 | |

510 transcripts were re-run to completion; of those, **398 reproduce and 112 do
not**. The remaining 31 were never measured against their bytes and are
reported as such rather than as reproductions.

### CLASS 1 — bookkeeping. Population: 6516 resolvable SHA sites at `81214a9`. Grain: one verdict per (file, token) site.

| | count |
|---|---:|
| sites recording a commit not on `main` | **649** of 6516 |
| distinct recorded commits not reachable from `main` | 66 of 284 |
| …of which have a patch-id-identical twin on `main` (**STALE, not lost**) | **65** (98%) |
| …with no twin | 1 |

The single commit with no twin is a *flip construction* — a mutation commit
made by mg-0120's instrument to demonstrate a failure, never intended to land.
It is named in `out_t3_shas.txt`.

**The two classes are reported apart on purpose.** 649 sites and 112
transcripts are not the same kind of damage and adding them would make the
remedy look bigger than it is.

---

## 1. THE POPULATION, AND WHAT IT EXCLUDES

541 committed transcripts, over 115 directories and 140 carrying commits, at
`81214a9`. 16 tracked `.txt` files under `code/` are **excluded** by the
definition and every one is named in `out_t1_population.txt`.

The definition is mechanical — `code/<one-dir>/out_*.txt` at the named revision
— so the denominator can be recomputed with one `git ls-tree` and no reference
to this instrument. `t1_population.py` prints every tracked `.txt` the
definition **excludes**, by name, because a denominator whose exclusions are
invisible is a denominator nobody can argue with.

The **carrying commit** of a transcript is `git log -1 <rev> -- <path>`: the
commit whose tree it currently sits in. That is the commit a reader checks out
to see the transcript in context, so it is the commit the transcript implicitly
claims to be a fact about.

---

## 2. THE METHOD, AND WHY IT IS NOT THE OBVIOUS ONE

The ticket says: re-run its producing script at the commit that carries it. The
producing script cannot be guessed from the transcript's name — this arc's
runners spell their producers through `for` loops, `run()` helpers,
`${name%.py}` strips and `$(basename …)` substitutions, and a filename-matching
rule fails on 202 of the 541 names. Guessing wrong inflates *cannot be run* and
makes the damage look smaller than it is.

So the instrument is **each suite's own `run_all.sh`, as it stood at the
carrying commit**, executed in a detached worktree checked out at that commit.
The reproduction procedure is the arc's own, not a second one written by me
that happens to agree with it today.

Two consequences are worth stating before the numbers.

- **`TIMED-OUT` is never folded into `DIFFERS`.** "I did not finish measuring"
  and "it does not reproduce" are different claims and only one is about the
  subject.
- **Every `DIFFERS` group is run a second time at the same commit.** If two
  re-runs disagree with each other, the producer is nondeterministic and the
  transcript could never have reproduced, at any commit, for anyone. That is a
  cause the ticket does not name.

---

## 3. DISPLACED IS NOT THE SAME AS WRONG — AND TWO ANSWERS ARE NOT ENOUGH

The ticket asks, for each non-reproducing transcript, whether the recorded
conclusion still holds, and contrasts mg-b2af (correct about the tree it
measured) with mg-c3a2 (contradicted by its own commit). Measuring that needs
**three** answers, not two, and the first version of this census got it wrong.

A `[FINDING]` row in this arc carries a sentence, and the sentence carries
counts. Comparing whole lines calls a moved count a changed verdict. So the
grain is:

| answer | meaning |
|---|---|
| `FLIPS` | a **decision** changed — `[OK]` became `[FINDING]`, or a decision row appeared or vanished. A false record at its carrying commit. |
| `HELD-DRIFTED` | every decision stands, and a **figure inside one of them** moved. The verdict is true and a stated number is not. |
| `HELD` | decisions and their figures intact; only surrounding rows moved. |
| `NO-VERDICT` | the transcript states no conclusion this instrument can read. |

`selftest_1abe.py` S2'' keeps the miss: **the whole-line grain reported five of
mg-c067's six transcripts as false records, and they are not.** Their verdicts
all stand; their population counts moved. Had that grain shipped, this census
would have overstated the damage in exactly the way the ticket's addendum warns
against.

### The 112, by what happened to the conclusion

| answer | count | reading |
|---|---:|---|
| `FLIPS` | **5** | a decision changed. **A false record at its carrying commit.** |
| `HELD-DRIFTED` | 9 | every decision stands, a figure inside one moved. Not a false verdict; a false number. |
| `HELD` | 43 | decisions and their figures intact. True of the tree it measured — mg-b2af's class. |
| `NO-VERDICT` | 55 | states no conclusion this instrument can read. |

**The five false records, named in full:**

```
code/audit_c067/out_c1_rebase.txt
code/hash_population_6e58/out_p2_population.txt
code/hash_population_6e58/out_p3_unrestricted.txt
code/hodge_leverage_audit_f922/out_audit.txt
code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt
```

Note what the 55 `NO-VERDICT` rows mean: for those, *this instrument cannot
tell you whether the conclusion still holds*, because it cannot find a
conclusion to compare. They are not a clean bill of health and they are not
counted as one.

**19 transcripts have a NONDETERMINISTIC producer** — two re-runs at the *same*
commit disagree with each other. These could never have reproduced, anywhere,
for anyone. Neither rebase nor regeneration explains a single one.

---

## 4. CORRECT MY FRAMING — THE LARGEST CAUSE IS NEITHER OF THE TICKET'S TWO

The ticket asserts one mechanism (the refinery's rebase) behind three sightings
and adds a fourth sighting whose cause is regeneration. It asks to be corrected
if the causes differ. They do.

| cause of the 112 `DIFFERS` | count | share |
|---|---:|---:|
| producer reads repository-global state | **103** | **92%** |
| producer never touches git | 9 | 8% |

(The split is static and labelled as a proxy wherever it appears: it
establishes which transcripts *can* be moved that way, not that a git call is
what moved these particular bytes.)

**A producer that reads repository-global state is displaced by the next commit
anyone makes, on any branch, with no rebase and no regeneration anywhere near
it.** Nothing was done to the transcript; the repository moved underneath it.
This was measured before the census was written — `PREDICTIONS.md` discloses it
as D2, a transcript already found non-reproducing for that reason — so it is a
prediction the census confirms rather than a discovery it stumbled into.

The practical consequence is the one that matters for step 3: **no rebase
policy addresses the majority of this population.** A convention aimed only at
rebase displacement would leave most of the blast radius exactly where it is.

---

## 5. THE TICKET'S OWN THREE SIGHTINGS, RE-DERIVED

**Sighting 2 (mg-c3a2 on mg-c067) — confirmed, and worse than the ticket
says.** mg-c3a2 re-ran those six transcripts *specifically to repair* a
displacement. The re-run measured `de39eb6`, which is mg-c3a2's own pre-rebase
commit. The refinery rebased it to `5bd0d71`. The transcripts now sit at
`47e56b3` declaring a commit that is not on `main`. **The repair for
displacement was displaced by the same mechanism, in the merge that landed it.**
Pure git; no execution; every step in `out_t7_sightings.txt` is a lookup a
reader can repeat.

**Sighting 1 (mg-b2af on mg-330a) — half confirmed, half not confirmed at my
grain.** The suite was run with HEAD at the pre-rebase twin `b94cb1e` (with the
carrier's copy of the suite dropped in, because the twin's tree does not
contain `code/repair_b2af/` at all) and again at its carrying commit.

| | at the twin `b94cb1e` | at the carrier `b1c3467` |
|---|---|---|
| transcripts reproducing byte-for-byte | **0 of 5** | **2 of 5** |

The ticket's second half is confirmed: they do not reproduce where they sit.
Its first half is **not confirmed, and that is a statement about my test before
it is one about the ticket.** The ticket claims ten *figures* reproduce at the
twin; I tested whole-transcript byte equality, which is strictly stronger, in a
synthetic state (carrier's code, twin's HEAD) that nobody ever committed. What
is solid is one figure: `HISTORY-DERIVED` reads **16** at the twin and the
committed transcript says **19** — and the ticket itself dates the 16 → 19
change to *between* the twin and the carrier. On that figure the transcript
matches the later state. That is one figure and it does not settle the other
nine.

**Sighting 3 (mg-132a) — not re-derived.** Its transcripts are in the t2
population and were re-run like any other member. The sighting itself is an
outstanding item, not a finished one.

**So the ticket's framing does need correcting**, and in the direction it
invited: the four sightings do not share one mechanism. Rebase displacement is
real and is a minority. The dominant mechanism is a producer that reads a
repository which then moves.

---

## 6. CLASS 1 — SIZED SEPARATELY, ON PURPOSE

649 of 6516 recorded SHA sites name a commit that is not on `main`. **65 of
the 66 distinct commits involved (98%) have a patch-id-identical twin on
`main`** — the identifier is stale and the content is intact.

The instrument matters here. `git merge-base --is-ancestor` calls all 66
missing. All three of the brief's own samples — mg-f3ff `72e36cb`, mg-fcb2
`064c79c`, mg-65eb `880fc15` — are re-derived in `out_t4_rebase.txt`: ancestry
says *not on main* for every one, patch-id says *identical* for every one.
Those are the mayor's measurements; they are re-derived here rather than
carried forward.

The addendum is right that merging the two classes overstates the damage. A
recorded identifier whose content is provably on `main` is bookkeeping. A
transcript that cannot be reproduced from the commit it sits on is a corrupted
record. Reporting them as one number makes the remedy look bigger than it is.

---

## 7. THE THIRD BUCKET NOBODY HAD COUNTED — AND A FALSE NEGATIVE IN THE
##    INSTRUMENT THE TICKET RECOMMENDS

**Zero.** Over the **234** pre-rebase/on-main pairs still visible in this
object store, **no rebase altered the content of a pre-existing file.**

Getting to that zero took an adjudication the census would have been wrong
without. Patch-id alone flagged **2** candidates:

- one is a **branch rework** — every differing path is *created by the commit
  itself*, so no rebase could have conflicted in it;
- one carries **byte-identical content at all 14 shared paths** and differs
  only because 6 hunks the new base had already absorbed dropped out of the
  replay.

**That second case is a false negative in the instrument this ticket
recommends.** A patch-id compares *diffs*, and a diff is a fact about a base as
well as about a tree. 1 of 234 pairs in this arc carries identical content
under different patch-ids. Patch-id is still the right answer to ancestry's
false negative — but a census built on patch-id alone would have reported that
pair as damage, and my first version did exactly that.

**Coverage bound, stated because it bounds the answer:** this sees only twins
still reachable from some ref or reflog. A twin whose reflog entry has expired
is invisible, and its absence is not evidence that its rebase was clean.

---

## 8. THE CONVENTION, AND A CONTROL THAT CAN CHECK IT

Step 3 asks for a convention, decided and defended, and checkable by a control.

### What was rejected, and why the measurements rejected it

**Record the SHA the run measured and assert it is an ancestor.** Refuted by
t4d: all three of the brief's own samples are patch-id-identical on `main` and
**not** ancestors of it. The assertion would be red on healthy evidence, and a
control that cries wolf on the healthy case gets turned off. Substituting
patch-id for ancestry does not save it either — see §7.

**Re-run post-rebase before submit.** The polecat cannot. The refinery rebases
after submission, and the ticket forbids changing that.

**Have the gate re-run and refuse on mismatch.** This is the one that looks
right and the census is what rules it out. Most of this arc's transcripts do
not reproduce, and the largest reason is not damage — it is the repository
moving. A gate that re-runs and refuses on mismatch would refuse nearly every
merge in this arc for a reason that is not the merge's fault. It is also the
most expensive check available and so the first to be disabled.

### What is proposed

**R1 — DECLARE THE CODE, NOT THE COMMIT.** A producer prints a digest over the
`.py`/`.sh` **blob shas** of the directory that produced it. Blob shas survive
a rebase untouched; commit shas do not, which is the whole subject of this
ticket. `out_*.txt` and `.md` are excluded so that **committing the transcript
cannot invalidate the declaration** — otherwise every transcript ships already
stale and the check becomes a ritual. That trap is mg-bf79's *a publisher is
not a pin*, and R1 is shaped around it. `selftest_1abe.py` S3 tests both halves
against real commits: a transcript-only commit leaves the digest unchanged, a
code commit moves it.

**R2 — DECLARE THE REACH.** A producer prints whether it read
repository-global state. If it did, the transcript is **declared unpinnable**:
no digest can make it a fact about a tree, because it is not one. §4 shows this
is the majority case, and a convention that pretended otherwise would be false
about most of the arc.

**R3 — CHECK R1 WITH A CONTROL THAT NEVER RE-RUNS ANYTHING.** Recompute the
declared digest from the tree at the transcript's carrying commit and compare.
Pure git, O(1) per transcript, no execution. A mismatch means the transcript
was produced by a different version of its own code than the one it is
committed beside — which is mg-c3a2's sighting, the pre-fix run committed
beside the fix, the one nothing caught for five days.

`t5_control.py` ships R3 and is **shown going both ways against a real tree**:
it accepts a transcript declaring `code/audit_c067`'s true digest at `47e56b3`
and refuses one declaring a corrupted value. A control that has only ever been
green has not been shown able to fire.

**This census is the first adopter.** 6 of its own 7 transcripts declare a
`code-digest` agreeing with the tree at HEAD. The seventh is
`out_t5_control.txt` — the control's own transcript, which is still being
written when it reads its directory, so it sees itself declaring nothing. That
is a real defect of this instrument and it is kept rather than special-cased.

**Coverage over the existing arc is 0 of 541** and will stay there until
something adopts it. R1–R3 fix nothing retroactively, and that is the honest
size of the proposal.

### What the convention does not do, stated where it cannot be missed

- It does not make an unreproducible transcript reproduce. R2's answer to those
  is to make them **say so**.
- It checks nothing already committed. Its coverage over the existing arc is
  zero and stays zero.
- **R2 is declared by the author and is not verified.** A checkable version
  needs the producer run under a harness that intercepts `git`. That is worth
  building and is not built here. An unverified declaration presented as a
  check is the shape this whole ticket is about, so it is named rather than
  footnoted.

### A retroactive screen that FAILED, kept red rather than dropped

The obvious cheap screen — flag a transcript whose carrying commit also changed
producing code in its own directory — **flags 439 of 510**, because committing
code and its transcripts together is this arc's normal practice. A screen that
fires on five transcripts in six discriminates nothing. It is kept, red, so
that the next person to have the idea finds the measurement instead of the
idea.

**The screen that does work needs no convention at all:** ask whether a
transcript names its own carrying commit anywhere in its own bytes.

**231 of the 231 transcripts that name a resolvable commit name one that is not
the commit carrying them — and none of them names its carrying commit anywhere
in its own bytes.** 100% of its population, against the failed screen's 84%.
No declaration, no convention, no re-running.

The limit is the other 310: they name no commit at all, so for them the
question *is it the revision it names* has no answer — not a good one and not a
bad one. That is the largest single obstacle to the ticket's framing, and it is
a property of the record rather than of the rebase.

---

## 9. THE CAP THE TICKET ASKED FOR — ALREADY FIXED — AND THE SHAPE SWEPT

`unreachable[:3]` in `code/audit_c067/c2_anchors.py` **does not exist on
`main`.** mg-c3a2 removed it in `5bd0d71`; the only surviving occurrence of the
string in that file is inside the comment explaining the removal. This was
disclosed as D3 in `PREDICTIONS.md` before any script of this census existed,
and nothing here re-fixes it.

What was done instead is the thing the ticket says about it — that it is *the
arc's most repeated shape* — so the shape was swept for.

`t6_caps.py` looks for the shape on the AST: a constant-capped slice **that is
iterated over** — the iterable of a `for` or comprehension, a `.join` argument,
or printed directly — inside a statement whose own string literals claim
completeness.

**The detector is controlled before it is believed.** It finds the defect in
`c2_anchors.py` at `3b73ccc`, where mg-c3a2 says it was, and finds nothing at
`5bd0d71` after the fix. Both answers on the same file.

**Result: 1 live site across 619 `.py` files**, from 133 capped-slice sites in
all — `code/species_sites_821e/p2_sites.py:186`, where `SITES[:5]` is iterated
under a printed sentence containing *every*, and `SITES` has **7** entries. Two
are dropped with nothing marking it. `t6c` prints the surrounding source for
the site so the judgement can be disagreed with rather than taken on trust —
the completeness word there arguably refers to the mutation and not to the
list, which makes it a weaker instance than the one the ticket names.

I predicted at least 5. **There is 1. P6.1 missed**, and the ticket's
generalisation — that this is the arc's most repeated shape — is not supported
at this grain.

**Nothing in another ticket's directory was edited.** Repairing a live cap
would change that suite's code, which would displace its committed transcripts,
which is the defect under study. The finding is reported; the file is left
alone. That is a judgement and it is stated so it can be overruled.

---

## 10. PREDICTIONS, SCORED

`PREDICTIONS.md` was committed in `6da906c`, before `lib_1abe.py` or any `t*.py`
existed in any tree. **Nine held, four missed.** The misses are kept as written.

| | prediction | outcome |
|---|---|---|
| P1.1 | `REPRODUCES` ≥ 250 (point estimate 300) | **HELD** — 398 |
| P1.2 | `DIFFERS` ≥ 100 (point estimate 150) | **HELD** — 112 |
| P1.3 | *cannot be run* between 40 and 90 (point estimate 60) | **MISSED** — 31. I over-estimated how many suites lack a runner; `run_all.sh` coverage in this arc is better than I gave it credit for. |
| P1.4 | the buckets sum to the denominator | **HELD** |
| P2.1 | the largest cause is neither rebase nor regeneration but repository-global reads, > half of non-reproducers | **HELD** — 103 of 112, 92% |
| P2.2 | at least one non-reproducer whose conclusion holds, and at least one whose conclusion flips | **HELD** — 43 and 5 |
| P2.3 | at least one non-reproducer caused by nondeterminism inside the producer | **HELD** — 19 |
| P3.1 | ≥ 90% of off-`main` recorded commits have a patch-id twin | **HELD** — 98% |
| P3.2 | CLASS 1 at least 5× CLASS 2 by raw count | **HELD** — 649 sites against 112 transcripts, 5.8×. The grains differ and the row says so. |
| P4.1 | **zero** conflict-resolving rebases | **HELD**, but only after adjudication — patch-id alone flagged 2, and my first version would have published "2 ALTERED". |
| P5.1 | at least one of this census's own transcripts will not reproduce at its carrying commit | **NOT MEASURED.** `SELF` is 0 because at `81214a9` my transcripts are not published, so t2 never sees them. The prediction is neither confirmed nor refuted, and pretending otherwise would be the fourth sighting in miniature. |
| P5.2 | the control I ship will go RED on `main` as it stands | **MISSED as stated.** R3 is *vacuously green*: coverage is 0 of 541, so it has nothing to refuse. What does go red is T5c, T5c-ii and T6b. I predicted a red control and shipped a green-because-empty one, which is exactly the failure mode the coverage row exists to expose. |
| P6.1 | ≥ 5 live instances of the cap-under-a-completeness-claim shape | **MISSED** — 1. |

---

## 11. DEFECTS OF THIS INSTRUMENT, KEPT

Nine, all kept rather than tuned away.

1. **The conclusion grain was wrong and would have overstated the damage.**
   Comparing whole verdict lines called a moved count a changed verdict, and
   reported five of mg-c067's six transcripts as false records when their
   verdicts all stand. Fixed; the miss is pinned in `selftest_1abe.py` S2''.

2. **This suite resolved `main` once per SCRIPT, and `main` moved between
   them.** In its own first full run t1 measured 537 transcripts at `eacc5e1`
   while t2 started at `81214a9`. A census whose scripts disagree about their
   denominator would have been committing the defect it was filed to measure.
   The revision is now resolved once in `run_all.sh` and passed to every
   script; the incident is recorded in that file's own header.

3. **`t4`'s first version reported 2 rebases as content-altering.** Neither
   was. One was a branch rework, one an absorbed hunk. Patch-id alone is not
   sufficient to name a cause, and the adjudication ladder exists because the
   first answer was wrong.

4. **`t6`'s first detector over-collected by 32×.** It counted every capped
   slice reaching output and reported 33 live sites, nearly all of them
   `sha[:7]` abbreviations inside sentences containing *each*. Requiring the
   slice to be *iterated* cut it to 1. A detector whose population is not what
   its name says is the defect it was hunting.

5. **The `run()` / `name="$1"` runner form was unparsed** until the self-test
   caught it, which would have mislabelled six transcripts' producers.

6. **This control's own transcript declares nothing.** `out_t5_control.txt`
   is still being written when t5 reads its own directory, so the first
   adopter's coverage is 6 of 7 rather than 7 of 7 — by construction, in the
   script that proposes the convention.

7. **31 transcripts have no runner and this census says nothing about them.**
   Not *they are fine* — nothing.

8. **`TIMED-OUT` is machine-dependent** and every other bucket is not. It is 0
   here at 900 s on this machine; a slower or busier box would move rows into
   it. `--jobs` is deliberately kept out of the transcript for the same reason.

9. **The producer-label column resolves 302 of 541.** The other 239 read `?`.
   That is a labelling gap, not a verdict, and t2's table says so on the row.

---

## 12. WHAT I DID NOT DO

- **I did not touch the refinery**, and did not investigate the pogo-side
  tickets mg-393f / mg-5d3f.
- **I did not repair a single committed transcript.** A transcript that does
  not reproduce is a measurement; overwriting it destroys the measurement.
- **I did not re-derive mg-132a's sighting.** It is measured only insofar as
  t2 measures its transcripts. Outstanding, not done.
- **I did not verify R2.** Nothing here checks that a producer's declaration
  about reading repository-global state is true.
- **I did not adopt the convention anywhere but this directory.** No other
  suite emits a `code-digest:` line, and this repair did not add one to any.
- **I did not measure transcripts kept under other names.** `t1a'` names the
  excluded files; they are outside every count in this census.
- **I did not establish, for the `DIFFERS` transcripts, that the specific
  differing bytes are the ones a repository-global read produced.** §4's split
  is a static proxy — it establishes which transcripts *can* be moved that way
  — and it is labelled as one wherever it appears.
- **I did not run the census at more than one revision.** Every number here is
  a fact about the commit printed as `as-of` in each transcript, and about no
  other. By the time this merges, `main` will have moved past it. That is not
  an accident of timing; it is the subject.
