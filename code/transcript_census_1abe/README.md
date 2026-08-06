# mg-1abe — WHICH REVISION IS EACH COMMITTED FIGURE A FACT ABOUT?

**TBD-HEADLINE**

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

**TBD-COUNTS-TABLE**

---

## 1. THE POPULATION, AND WHAT IT EXCLUDES

**TBD-POPULATION**

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
rule fails on 222 of the 510 names. Guessing wrong inflates *cannot be run* and
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

**TBD-CLASS2-BREAKDOWN**

---

## 4. CORRECT MY FRAMING — THE LARGEST CAUSE IS NEITHER OF THE TICKET'S TWO

The ticket asserts one mechanism (the refinery's rebase) behind three sightings
and adds a fourth sighting whose cause is regeneration. It asks to be corrected
if the causes differ. They do.

**TBD-CAUSE**

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

**TBD-SIGHTINGS**

---

## 6. CLASS 1 — SIZED SEPARATELY, ON PURPOSE

**TBD-CLASS1**

The addendum is right that merging the two classes overstates the damage. A
recorded identifier whose content is provably on `main` is bookkeeping. A
transcript that cannot be reproduced from the commit it sits on is a corrupted
record. Reporting them as one number makes the remedy look bigger than it is.

---

## 7. THE THIRD BUCKET NOBODY HAD COUNTED — AND A FALSE NEGATIVE IN THE
##    INSTRUMENT THE TICKET RECOMMENDS

**TBD-REBASE**

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

**TBD-CONTROL**

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

**TBD-SCREEN**

---

## 9. THE CAP THE TICKET ASKED FOR — ALREADY FIXED — AND THE SHAPE SWEPT

`unreachable[:3]` in `code/audit_c067/c2_anchors.py` **does not exist on
`main`.** mg-c3a2 removed it in `5bd0d71`; the only surviving occurrence of the
string in that file is inside the comment explaining the removal. This was
disclosed as D3 in `PREDICTIONS.md` before any script of this census existed,
and nothing here re-fixes it.

What was done instead is the thing the ticket says about it — that it is *the
arc's most repeated shape* — so the shape was swept for.

**TBD-CAPS**

**Nothing in another ticket's directory was edited.** Repairing a live cap
would change that suite's code, which would displace its committed transcripts,
which is the defect under study. The finding is reported; the file is left
alone. That is a judgement and it is stated so it can be overruled.

---

## 10. PREDICTIONS, SCORED

**TBD-PREDICTIONS**

---

## 11. DEFECTS OF THIS INSTRUMENT, KEPT

**TBD-DEFECTS**

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
