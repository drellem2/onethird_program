# mg-f8e5 — THE DISPOSAL OF mg-1abe's REMAINDER

**The measured damage of this class is THREE FALSE RECORDS, NOT FIVE. Two of
the five are not damage, for two different reasons, and neither is a near
miss.**

**`code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt` REPRODUCES
BYTE-FOR-BYTE** at its own carrying commit. It needs **1470 seconds** against
the census's 900-second budget.

**`code/audit_c067/out_c1_rebase.txt` IS TRUE AND ITS OWN PRODUCER CAN NO
LONGER SEE THAT.** It says five commits were replayed by a rebase; re-run
today it says zero — because `c1_rebase.py:48` matches them by subject against
`git log main -n 40` and `main` has grown **226** commits past the carrying
commit. Nothing died: all six off-`main` commits it names are still twinned on
`main`, **6 of 6**, when the same match is run unbounded. **Its remedy is the
opposite of a re-run: a re-run would write `0` over a `5` that is true.**

**mg-1abe's `TIMED-OUT` bucket is UNREACHABLE BY CONSTRUCTION.** Its README
promises, in so many words, that "`TIMED-OUT` is never folded into `DIFFERS`"
— and its instrument does the opposite of that, always, for every suite in the
arc whose runner redirects into its own transcripts, which is 99 of 166
transcript-carrying directories. A POSIX shell creates `out_x.txt` before the
producer runs; `collect()` returns bytes for any file that exists; the
`TIMED-OUT` branch is guarded by `if got[p] is None`. So a killed run is
bucketed `DIFFERS`, and `conclusion_verdict(committed, "")` is `FLIPS`.

**That accounts for one of the two. It is a correction to the FIVE and not to
the 112.** A row wrongly in
`DIFFERS` is still a row that did not reproduce in the census's run, and the
census reports 112 as `DIFFERS`, not as damage. What this finding does to the
112 is make it an upper bound whose slack is unmeasured. **I did not re-run the
other 107 to size it** and I say so rather than estimating it.

**AND THIS INSTRUMENT COMMITTED THE SAME DEFECT, INSIDE AN HOUR OF REPORTING
IT.** `lib_1abe`'s producer regex captures the command *after* the interpreter,
because mg-1abe never executes it — it runs the whole `run_all.sh`. `d1` did
execute it, so all five producers ran as `-u c1_rebase.py > out_c1_rebase.txt`,
the shell answered 127, the redirection had already created an empty
transcript, and d1 printed *FLIP re-derived — 8 decision rows lost* off a file
nothing had written. Repaired at `invocation()`; forbidden by `selftest` S8,
which took three attempts to get right.

Everything below is derived by `sh run_all.sh`, whose transcripts are committed
beside it. Every count names its population. Where a number is mg-1abe's, it is
tagged as a reproduction rather than presented as a finding.

---

## 0. WHAT THE TICKET ASKED FOR, AND WHERE EACH ANSWER IS

| the ticket | the answer |
|---|---|
| 1. dispose of the five false records individually | §1, `out_d1_five.txt` |
| 2. account for the 31 unmeasured | §2, `out_d2_unmeasured.txt` |
| 3. adopt the convention and make it CHECKABLE | §3, `out_d3_adopt.txt` |
| 4. confirm the own-defect fix landed, and sweep for its shape | §4, `out_d4_movingref.txt` |
| — correct my framing | §5 |

---

## 1. THE FIVE, DISPOSED OF ONE AT A TIME

`out_d1_five.txt`. Each is re-run by its **own suite's producer**, as that
suite's runner spells it, in a detached worktree at the commit carrying it,
with the worktree asserted clean before it starts.

**THE ADJUDICATION IS THE DELIVERABLE, and my first version of it was wrong.**
A decision that changes on re-run has three causes and only one is damage:

| | |
|---|---|
| `RECORD-IS-FALSE` | the world at the carrying commit disagrees with the record. A reader who checks out that commit is misled. **This is the damage.** |
| `RERUN-CANNOT-SEE` | the world is as the record describes and the *instrument* has lost its view of it. The record is the only surviving witness and **re-running destroys it.** |
| `NOT-A-FALSE-RECORD` | the re-run is byte-identical. There is nothing to adjudicate. |

### The five, named, with what each asserts and what is true at its commit

**① `code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt` @ `3bf0cd2` —
NOT A FALSE RECORD. REMEDY: NONE.**
It **reproduces byte-for-byte**, exit 0, in **1470 seconds** against the
census's 900-second budget. Its producer is the one in the arc that never
touches git — its own header states a reproduction contract *in terms of the
files it reads* rather than a commit — and it holds. Nothing is wrong with this
record; what is wrong is the bucket that could not report a budget (§1b).

**② `code/audit_c067/out_c1_rebase.txt` @ `47e56b3` —
RERUN-CANNOT-SEE (B). REMEDY: ANNOTATE + DO NOT RE-RUN.**

- *asserts*: `[CONFIRMED] C1a mg-132a's **5** commit(s) were REPLAYED onto a
  larger tree by the merge.`
- *its own producer, re-run there today*: `[REFUTED] C1a … **0** commit(s) …`
- *what is actually true*: **the record is right.** `c1_rebase.py:48` matches
  the pre-rebase commits **by subject** against `git log main **-n 40**`, and
  `main` has grown **226 commits** past the carrying commit — the walk stops
  short. Nothing died: the objects resolve, `origin/polecat-132a` still points
  at them, and **all 6 off-`main` commits it names are still twinned on `main`,
  6 of 6**, when the same match is run without the bound (D1d′).
- The producer's own docstring guards the **ref** by name — *"any single ref
  name here is a hard-coded anchor of exactly the kind this audit exists to
  complain about"* — and leaves the **window** hard-coded three lines below it.
- *remedy*: annotate, and **do not re-run** — a re-run writes `0` over a `5`
  that is true.

**③ `code/hash_population_6e58/out_p2_population.txt` @ `fe6a495` —
RECORD-IS-FALSE. REMEDY: ANNOTATE (unpinnable under R2).**

- *asserts*: `SELF-ERRORS: 0` over `git log` call sites in `code/**/*.py`.
- *true at its commit*: **`SELF-ERRORS: 1`** — the producer's own tripwire
  fires: *"1 POP-D row(s) were counted and never read. An unexamined count is
  what this ticket is about."* The population moved from 88 486 to 93 352
  `ast.Call` nodes beneath it.
- *remedy*: its population **is the repository**, so no tree digest can pin it
  and a re-run is stale at the next commit anyone makes. What it needs is to
  **say which revision it is a fact about**.

**④ `code/hash_population_6e58/out_p3_unrestricted.txt` @ `fe6a495` —
RECORD-IS-FALSE. REMEDY: ANNOTATE (unpinnable under R2).**

- *asserts*: `SELF-ERRORS: 0`, and `NEW SINCE THIS ADJUDICATION WAS WRITTEN: 0`.
- *true at its commit*: **`SELF-ERRORS: 1`**, and **5** new `UNRESTRICTED`
  sites appeared after its hand adjudication was written — each named by the
  producer itself.
- Same remedy and same reason as ③. **These two are the cleanest false records
  of the five**: the instrument that produced them detects its own displacement
  and says so, and the committed bytes predate that.

**⑤ `code/hodge_leverage_audit_f922/out_audit.txt` @ `553033a` —
RECORD-IS-FALSE. REMEDY: ANNOTATE — AND THE REVISION IS KNOWN.**

- *asserts*: under *"every site in the repository that states A5"*, a list of
  **7** files.
- *true at its commit*: **8**. `docs/OneThird-Hodge-Side-Leverage-Mg3c24Repair-
  IndependentAudit.md` states A5 and carries the enlargement, and the committed
  list does not contain it. The finding `F-A` is untouched — the falsehood is
  the *completeness* of an enumeration, in the safe direction.
- **It reproduces EXACTLY at `bbe83b5`** (D1c) — so for this one the ticket's
  originating question has a literal answer: *that* is the revision it is a
  fact about, and the annotation writes itself.

### The count

| | |
|---|---:|
| named by mg-1abe as false records | 5 |
| …that reproduce byte-for-byte and are not false at all | **1** |
| …that are TRUE at their commit, with the instrument blind | **1** |
| **…that are FALSE at the commit carrying them — the damage** | **3** |

**THE MEASURED DAMAGE OF THIS CLASS IS THREE.** Two of the five are not damage,
for two different reasons, and both are printed rather than dropped — a
disposal that quietly kept the number at five would be the same over-report
this ticket exists to prevent, an order of magnitude smaller.

**NOTHING IN ANOTHER TICKET'S DIRECTORY IS EDITED.** These remedies are a
disposal *record*. mg-1abe's rule is that a transcript which does not reproduce
is a MEASUREMENT and overwriting it destroys it — and for ② the remedy forbids
re-running outright.

---

## 2. THE 31 UNMEASURED — 24 OF THEM REPRODUCE

`out_d2_unmeasured.txt`. mg-1abe bucketed 31 transcripts `NO-RUNNER` and said,
correctly, that its census says **nothing** about them — *"not they are fine:
nothing"*. Its defect 7 keeps that as a defect. "Reported as such" was the
right call for a census. It is not a resting place.

**The population re-derives exactly: 31 over 10 directories at `81214a9`** —
a reproduction of the census's bucket, not a finding.

### Why each was unmeasurable

`NO-RUNNER` is a fact about a **filename**, not about reproducibility. Three
tiers, and every recovered producer is **executed**, because a filename that
maps is not a producer that reproduces:

| tier | what it is | count |
|---|---|---:|
| `T2-OTHER-SH` | the suite **has a runner**, called `run_audit.sh`. The census's rule is the literal string `run_all.sh`. | **12** |
| `T3-NAME-MAP` | no runner of any name; only the arc's `out_<stem>.txt` ↔ `<stem>.py` convention connects a transcript to a script. A **guess**, labelled as one. | **16** |
| `T4-NONE` | no producer at that commit by any rule. | **3** |

Three of the ten directories — `face_geometry_audit_f1b2`, `…_fcf1`,
`semigroup_note_audit_66a6` — carry a `run_audit.sh` that **names its producer
outright**. Recovering them needed one widened string. It also needed a
**fourth runner form the census's parser does not read**: those runners spell
`python3 audit_gates.py | tee out_gates.txt`, and `lib_1abe.parse_producers`
reads only `>` redirections, `for` loops and shell functions.

### What they say, now that they have been run

| | |
|---|---:|
| `REPRODUCES` | **24** |
| `DIFFERS` | **0** |
| `T3-UNRESOLVED` — a guessed producer disagreed; guess-was-wrong and does-not-reproduce are indistinguishable | 3 |
| `RUNNER-FAILED` | 1 |
| `UNMEASURABLE` — no producer at any commit | 3 |

**24 of the 31 reproduce and none of the measured ones differ.** So the
census's 398 is a floor: **422 of 541 transcripts are now known to reproduce
from the commit carrying them**, and the unmeasured residue is 7, not 31.

### What is left, and whether it can be closed

- **3 UNMEASURABLE** (`face_geometry_audit_e0ce/out_n5.txt`, `…/out_n6.txt`,
  `state_visibility_audit_65eb/out_anchor65eb_bd24efc.txt`) — **not closable
  from this repository.** No script at that commit that the transcript's name
  reaches, and no runner that names it. Closing them needs the producer, which
  was never committed.
- **3 T3-UNRESOLVED** (all in `state_visibility_audit_65eb`) — **closable by
  one piece of information nobody has to re-derive: the command that produced
  the file.** Under the convention adopted in §3, a transcript declares its own
  producing code, so this bucket cannot recur.
- **1 RUNNER-FAILED** (`face_geometry_audit_5630/out_x3_equivalence.txt`) — its
  producer ran and did not reach a decision. A fact about the run; a larger
  budget or a different machine may move it.

### And the bucket has grown while nobody was looking

The same rule at today's `main` returns **140 transcripts over 31
directories** — a **4.5×** growth in the set nothing can say anything about.
Those 109 are **named and not disposed of**: measuring them is a new census,
not this disposal.

---

## 1b. THE FIFTH IS NOT A FALSE RECORD — AND THE BUCKET THAT SHOULD HAVE HELD IT CANNOT BE REACHED

`out_d5_timeout.txt`. mg-1abe's §2 states the rule its 112 depends on:

> "`TIMED-OUT` is never folded into `DIFFERS`. 'I did not finish measuring' and
> 'it does not reproduce' are different claims and only one is about the
> subject."

The rule is right. The instrument inverts it, always. Three lines of the
census's own code, each checked against its source before being reasoned about
(D5a, five clauses, all present):

| | |
|---|---|
| `t2_census.py:112` | `sh run_all.sh` is started. The first thing a POSIX shell does with `python3 x.py > out_x.txt` is **create `out_x.txt`**, before the producer runs. |
| `t2_census.py:134` | `collect()` returns the file's **bytes if it exists**, and `None` only if it does not. |
| `t2_census.py:225` | the `TIMED-OUT` bucket is guarded by `if got[p] is None`. |

So of the three states a SIGKILL at the budget can leave, **two are bucketed
`DIFFERS`** and only the one where the shell never ran reaches `TIMED-OUT`
(D5b, three arms, all forced). And `conclusion_verdict(committed, "")` is
**`FLIPS`** — an empty file loses every decision row (D5c).

**Fired for real, cheaply**: `hodge_leverage_repair_ff3e`'s runner started at
its carrying commit and killed after 8 seconds the same way `run_suite` kills
it — `start_new_session=True`, `os.killpg(..., SIGKILL)` — leaves the
transcript **existing and 0 bytes** (python buffers stdout when it is not a
tty). `collect()` returns `b""`; `got[p] is None` is False; the row is
`DIFFERS`; the conclusion is `FLIPS` (D5d).

**Exposure, counted rather than guessed:** the `TIMED-OUT` bucket is
unreachable for **99 of 166** transcript-carrying directories at `e35b51c` —
every one whose runner redirects (or `tee`s) into a transcript. mg-1abe's own
defect 8 reads *"It is 0 here at 900 s on this machine"*: a 0 that is a
property of the guard, not of the machine. 39 more redirect into no transcript
at all and are counted apart rather than assumed safe.

**The repair is one line and is NOT applied**, and the judgement is stated so it
can be overruled: editing `t2_census.py` changes that suite's code, which
displaces all eight of its committed transcripts — the defect under study — and
re-running the census costs about two hours and produces a *different* census
because `main` has moved. What is landed here is the measurement, so the next
reader finds the number rather than the idea.

```
t2_census.py:224   for p in paths:
-                      if got[p] is None:
+                      if status == "timeout":
+                          verdict[p] = "TIMED-OUT"; ...
+                      elif got[p] is None:
```

**What this does NOT move**, said where it cannot be missed:

- **not the 112.** A row wrongly in `DIFFERS` is still a row that did not
  reproduce in the census's run, and the census reports 112 as `DIFFERS`, not
  as damage. It becomes an upper bound whose slack is unmeasured — and I did
  not re-run the other 107 to size it.
- **not the 398.** A byte-identical transcript cannot be a truncation artefact.
  The bucket is safe in the direction that matters.

---

## 3. THE CONVENTION, ADOPTED AND MADE CHECKABLE

`out_d3_adopt.txt`. mg-1abe proposed R1/R2/R3, adopted them in one directory,
and put the size of that honestly: *"Coverage over the existing arc is 0 of 541
and will stay there until something adopts it."* It also scored its own P5.2 a
**MISS** for shipping a control that was *vacuously green* — R3 had nothing to
refuse. Three things are added here.

**R3 IS RUN OVER THE WHOLE ARC AND `UNDECLARED` IS COUNTED.** One verdict per
tracked `code/<dir>/out_*.txt`, nothing executed, each row a digest recomputed
from the tree at that transcript's carrying commit. A directory that has not
adopted is a **finding with a number**, not silence. That is the difference
between a control and a ritual: a control whose only reachable answer is green
has not been shown able to refuse.

**THE CONTROL IS SHOWN REFUSING SOMETHING**, three constructions against a real
tree, all forced: a true digest **accepts**; one hex digit changed **REFUSES**;
and a digest that is *true of the wrong directory* **REFUSES**. The third arm
is this suite's own first defect (§7.1) and it is the one R3 could most easily
have been built unable to see.

**R2 IS MADE CHECKABLE.** mg-1abe: *"R2 is declared by the author and is not
verified. A checkable version needs the producer run under a harness that
intercepts `git`. That is worth building and is not built here."* A
git-intercepting harness is one instrument; it is not the only one. A **static
read of the producing code** answers the same question at exactly the grain the
census already trusts — its own 103-of-112 cause split is the same static
proxy and says so on its row. Its limits are stated before its numbers:

- **it CAN** refuse a `reads-outside-tree: no` from a producer that calls `git
  log`. That is the direction that matters: a false `no` is a transcript
  claiming to be pinnable when it is not.
- **it CANNOT** confirm a `yes`. A producer may import git and never reach the
  call on the path that produced these bytes. A `yes` the static read agrees
  with is CONSISTENT, not verified.

And the static test is shown answering **both ways** over 171 directories — 88
reach outside their tree, 83 do not — because a test that returned `yes`
everywhere would be `x == x` with a name on it.

**THE SECOND ADOPTER SURVIVES ITS OWN PUBLISHING STEP, AND THE ROW THAT SAYS SO
CANNOT SEE THE END OF ITS OWN OUTPUT.** `d3` reports **5 of 6**, and the sixth
is `out_d3_adopt.txt` — read off disk while `d3` is still buffering it, so it
declares nothing at the moment it looks. Checked afterwards, all **6 of 6**
declare `0788236564d650ea`, the digest recomputed from the committed tree.
That is mg-1abe's defect 6 exactly, reproduced rather than hidden: a check that
measures its subject mid-write is worth keeping visible.

**AND R1 DISCIPLINED ITS OWN AUTHOR.** The digest covers the `.py`/`.sh` blobs
as committed, so editing a script after the transcripts were written makes
every transcript declare a digest of code that did not produce it. There is no
way round it except the honest one: freeze the code, commit it, re-run the
whole suite, then commit the transcripts. That cost this item a full extra pass
and it is what R1 is shaped to force.

**WHAT ADOPTION IS NOT.** Nothing here makes a suite adopt. A convention with a
control is not a gate, and wiring this into a gate would refuse merges for a
state that is normal across the whole arc — mg-1abe measured that trade and
refused it, and nothing here reopens it. What changed is that the gap is now a
number a control prints on every run instead of a sentence in a README.

---

## 4. THE OWN-DEFECT: CONFIRMED, AND ITS SHAPE SWEPT

`out_d4_movingref.txt`.

**IT LANDED, AND IT IS CHECKED BY ANCESTRY.** `a7d7fb9` resolves and is an
ancestor of `main`. It is deliberately *not* checked by reading
`run_all.sh` in the worktree I am standing in: a file present in my branch is a
fact about my branch (this item's E7). Both halves are there — the revision is
resolved once and handed to every script, **and** the incident that motivated
it is in the runner's own header, where the next person to "simplify" it will
read it.

**THE SHAPE, stated before the detector** so its population is what its name
says: (a) a runner drives ≥2 scripts, (b) ≥2 of them independently resolve a
moving ref, (c) the runner passes no resolved revision down. Rejected
near-misses are printed rather than dropped — one script resolving `main` ten
times is one process and one tree; a runner that resolves once and hands the
sha down is *the fix*.

**THE DETECTOR IS SHOWN GOING BOTH WAYS ON ONE DIRECTORY**, at the only pair in
this repository where the answer is known in advance: `SHAPE` at `a7d7fb9^`,
`PASSES-DOWN` at `main`. **That control earned its place.** My first detector
read only the driven scripts and scored the pre-fix census `ONE-SCRIPT` —
because mg-1abe's eight scripts never name `main` at all; they call
`lib_1abe.main_rev()`, whose default is. One level of indirection through the
directory's own helpers is what the control forced.

**THE SWEEP: 11 of 171 suites carry the shape**, every one named in full. And
the row worth more than the count: **`code/transcript_census_1abe` is the ONLY
suite in the entire arc that passes a resolved revision down.** The fix exists
in exactly the one place that discovered the defect.

**HAS IT FIRED? 3 of the 11**, on the same evidence mg-1abe had for its own —
two committed transcripts of one suite naming *different* revisions in an
`as-of` role: `audit_330a`, `branching_audit_e34a`, `repair_8d5e`. **8 of the
11 are INVISIBLE to this test, not clean**: fewer than two of their transcripts
name a revision at all, and mg-1abe measured 310 of 541 naming no commit
anywhere in their own bytes. A finding here is evidence; a zero is not.

---

## 5. CORRECT MY FRAMING

The ticket asks to be corrected and names its own basis: *"I recovered all of
this from commit subjects and a README I read in fragments, not from a
verdict."* Four corrections, in descending order of how much they move.

**1. THE DAMAGE IS THREE, NOT FIVE.** The ticket's headline number is two too
large, and neither correction is a judgement call about grain. One of the five
is a suite that ran out of time, bucketed as a false record because the bucket
for running out of time **cannot be reached** (§1b). The other is a record that
is TRUE, whose own producer bounds its search by a literal that `main` has
outgrown (§1 ②). §1 and `out_d5_timeout.txt`.

**2. "FIVE FALSE RECORDS" IS THE UNION OF THREE THINGS, TWO OF THEM NOT
DAMAGE, AND TWO OF THEM WITH OPPOSITE REMEDIES.** A decision that changes on re-run means either the record is wrong
at its commit, or *the instrument can no longer see what the record saw*. For
the second, re-running is not the remedy — it is the destruction of the
measurement. §1 splits them and the split changes what should be done to two of
the four.

**3. "THE CENSUS PROPOSES A CONVENTION" UNDERSTATES WHAT WAS MISSING.** The
convention was proposed *and adopted*, in one directory, with a control that
mg-1abe itself scored a MISS for being vacuously green. What was missing is not
the convention: it is a control that counts its own blind spot. §3.

**4. THE OWN-DEFECT IS FIXED AND IS NOT RARE.** The ticket asks whether the
single-resolve fix landed — it did, in `a7d7fb9`, and it is an ancestor of
`main`. The sweep it also asks for finds the same shape alive in other suites,
and finds that **mg-1abe's suite is the only one in the whole arc that passes a
resolved revision down.** §4.

**WHAT THE TICKET GOT RIGHT AND I CHECKED RATHER THAN ASSUMED.** "112
non-reproducing" is not "112 false records" and anyone quoting it as damage is
over-reporting by more than twenty-fold: that is correct, it is mg-1abe's own
distinction, and nothing here weakens it. The instrument, the adjudication and
the coverage bound are sound and I did not re-litigate them.

---

## 6. PREDICTIONS, SCORED

`PREDICTIONS.md` was committed in `c35f296`, before `lib_f8e5.py` or any
`d*.py` existed in any tree. **Eight held, two missed, one is not scorable as
stated.** The misses are kept as written.

| | prediction | outcome |
|---|---|---|
| P1.1 | ≥3 of the 5 have `re-run and re-commit` as the WRONG remedy | **HELD** — 4 of 5. Two say *annotate, unpinnable*, one says *do not re-run*, one says *nothing to remedy*. Only ⑤ could sensibly be re-run, and even there annotation is better because the revision is known. |
| P1.2 | for ≥1, no remedy restores the assertion because its evidence is unreachable — **named in advance as `audit_c067`** | **MISSED, AND THE NAMING WAS RIGHT FOR THE WRONG REASON.** `audit_c067` is the one, and its evidence is **not** unreachable: every object resolves, the ref survives, and all six twins are still on `main`. What is unreachable is the *producer's own search*, bounded by `-n 40`. I predicted the right transcript and the wrong mechanism, and my first adjudication rule inherited the error — it looked only for dead refs and scored ② `RECORD-IS-FALSE`. §7.4. |
| P1.3 | for ≥3 of the 5, the transcript's own bytes name the revision it is a fact about | **MISSED** — **0 of 5** name their own carrying commit. This is mg-1abe's §8 result reproduced at n=5: *231 of 231 transcripts that name a resolvable commit name one that is not the commit carrying them.* |
| P1.4 | for ≥1 of the 5 there is an ancestor commit at which the producer reproduces the committed bytes EXACTLY (put at 0.35) | **HELD** — ⑤ reproduces exactly at `bbe83b5`. The ticket's originating question has a literal answer for one of the five. |
| P2.1 | ≥10 of the 31 are unmeasurable only because the runner is named something other than `run_all.sh` | **HELD** — 12. |
| P2.2 | ≥25 of the 31 have a producing script the name convention reaches | **HELD** — 28 (12 named by a runner, 16 by convention). |
| P2.3 | ≥1 of the 31 has NO producer at any commit | **HELD** — 3, all named. |
| P2.4 | running the recovered producers, ≥5 of the 31 REPRODUCE byte-for-byte (put at 0.30) | **HELD, AND BY A LOT** — **24**, with **0** differing. I put this low on the reasoning that a directory which never had a runner would be older and more repository-coupled. The opposite: suites without runners in this arc are the small arithmetic ones. |
| P3.1 | this suite is green at its own publishing step | **HELD with the known caveat** — every transcript written before `d3` runs declares this directory's own digest; `d3`'s own transcript cannot be in its own count, which is mg-1abe's defect 6 and is printed rather than hidden. |
| P3.2 | the checkable control is RED somewhere on `main` the first time it runs over more than one directory | **HELD** — `UNDECLARED` is 819 of 827 and is a FINDING. R3 itself refuses 0, which is the vacuous half; the coverage row is the half that fires. |
| P3.3 | R2 can be made checkable without a git-intercepting harness, agreeing with the author's declaration at 100% of adopters | **HELD** — 8 of 8 consistent, 0 contradicted, and the static test answers **both** ways over 174 directories (90 / 84). Scored HELD with its limit stated: it can refuse a false `no` and cannot confirm a `yes`. |
| P4.1 | ≥20 suites carry the moving-ref shape | **MISSED** — **11** of 174. I over-estimated. What I did not predict is the sharper row: **exactly one suite in the whole arc passes a resolved revision down**, and it is the one that discovered the defect. |
| P4.2 | ≥1 suite can be shown to have ALREADY been bitten | **HELD** — 3 of the 11, by two committed transcripts naming different revisions in an `as-of` role. |
| P4.3 | the sweep finds the shape in a suite whose runner LOOKS like it resolves once (put at 0.25) | **NOT SCORABLE AS STATED.** Only one suite resolves once at all, and it is the fix. The prediction presumed a population that does not exist, and inventing a near-miss after the fact to score it would be the thing this file exists to prevent. |

**The prediction that mattered most is the one I got wrong.** P1.2 named
`audit_c067` and gave the wrong reason, and because the *rule* I built was
shaped by that reason, the instrument scored ② as damage until I looked at what
its producer actually does. The naming was luck; the rule was the error.

---

## 7. DEFECTS OF THIS INSTRUMENT, KEPT

Seven, all kept rather than tuned away. Four were caught by controls filed in
advance; **one is the defect this whole ticket is about, committed by the
instrument that reports it, within an hour of reporting it.**

**1. MY LEDGER DECLARED SOMEBODY ELSE'S DIGEST AS ITS OWN PROVENANCE.**
`lib_1abe.Ledger.__init__` prints `provenance_block("code/" + SELF_DIR)` where
`SELF_DIR` is bound in *its* module, so every transcript I produced while
importing it unmodified declared `code/transcript_census_1abe`'s digest. It was
a **TRUE digest of the wrong directory** — the worst kind, because R3
recomputes the declared digest from the tree and would have found it AGREEING.
The first adopter of a convention getting it wrong in the one direction the
check cannot see is worth more than the adoption. Fixed in `lib_f8e5.Ledger`;
pinned by `selftest` S1' and by `d3`'s third control arm.

**2. I RAN EVERY PRODUCER WITHOUT ITS INTERPRETER, AND THEN READ THE EMPTY
FILE THAT LEFT.** `lib_1abe._RE_RED` captures the command *after*
`python3`/`sh`, because mg-1abe never executes `spec['cmd']` — it runs the whole
`run_all.sh`. `d1` did execute it. Every one of the five ran as `-u
c1_rebase.py > out_c1_rebase.txt`, the shell answered 127, **the redirection had
already created the transcript**, and d1 printed *"FLIP re-derived — 8 decision
rows lost"* off a file nothing had written. That is `d5`'s entire finding,
reproduced by the instrument that reports it. Fixed at `invocation()`.

**3. AND THE GUARD AGAINST (2) TOOK THREE ATTEMPTS.** *Emptiness* missed it —
the runner folds stderr in, so the file held 313 bytes of shell complaint.
*Exit 127* missed it — `python3 -u no_such_file.py` exits **2**. And the exit
code cannot be the test at all in this arc, where a non-zero exit is the
NORMAL state of an instrument that found what it was sent to find. What works
is: **did it reach its first decision?** A run leaving no verdict-bearing line
where the committed transcript is made of them did not measure anything.
`classify_run()`; `selftest` S8.

**4. MY ADJUDICATION RULE KNEW ONLY ONE OF THE TWO WAYS AN INSTRUMENT GOES
BLIND, AND IT CHANGED A VERDICT.** The rule asked whether the transcript names
commits that no longer hang off a ref. `audit_c067` names commits that all
still resolve, on a ref that still exists — so the rule scored it
`RECORD-IS-FALSE`, i.e. **damage**, when the record is true. The second way is
a **hard-coded window on a moving ref**: `git log main -n 40`, with `main` 226
commits further on. Both clauses now measured and printed; the miss is scored
against `PREDICTIONS.md` P1.2, which named the right transcript for the wrong
reason.

**5. MY MOVING-REF DETECTOR MISSED THE ONE CASE WHOSE ANSWER IS KNOWN.** It
read only the driven scripts and scored mg-1abe's own pre-fix suite
`ONE-SCRIPT`, because those eight scripts never name `main` — they call a local
helper whose default is. Caught by the D4b control, which exists precisely
because it is run where the answer is published in advance. Fixed by one level
of indirection through the directory's own helpers; kept as `selftest` S3''.

**6. I KILLED A TREE-MUTATING PRODUCER MID-RUN AND ALMOST READ THE WRECKAGE AS
A RESULT.** My first re-run of `hodge_leverage_repair_ff3e` was killed by a
two-minute tool timeout while it had three documents mutated. The next run
correctly REFUSED — *"REFUSING TO RUN: these are dirty"* — and the refusal read
exactly like a census verdict for about a minute, until I ran `git status`.
Kept as `PREDICTIONS.md` D5, and guarded: every re-run asserts a clean worktree
before it starts (`dirty_paths`, `selftest` S4).

**7. THE T3 RECOVERY TIER IS A GUESS AND ITS FAILURES ARE UNRESOLVABLE.** When
a guessed producer emits the committed bytes exactly, the guess was right. When
it does not, *the guess was wrong* and *the transcript does not reproduce* are
indistinguishable, and this instrument cannot tell them apart. Every such row
is reported `T3-UNRESOLVED`, never `DIFFERS` — a bucket, not a verdict.

---

## 8. WHAT I DID NOT DO

- **I did not edit any of the five transcripts, or any file in another ticket's
  directory.** mg-1abe's rule is that a transcript which does not reproduce is
  a MEASUREMENT and overwriting it destroys it. What is landed here is a
  disposal *record*.
- **I did not apply the one-line `t2_census.py` repair**, and §1b states the
  reason and whose call it is.
- **I did not re-run the other 107 `DIFFERS` transcripts** to size how many are
  timeout artefacts like the fifth. That is roughly two hours of machine time
  and it is stated as not done rather than estimated. The exposure is bounded
  below by 1 and this instrument does not bound it above.
- **I did not re-derive the 398, the 649-of-6516, the 65 twins or the zero
  third bucket.** They are mg-1abe's, they are sound, and the ticket says not
  to re-litigate them.
- **I did not verify R2 dynamically.** The static check refuses a false `no`
  and cannot confirm a `yes`, and that limit is printed above its own numbers.
- **I did not make anything ENFORCE the convention.** `d3` is a control, not a
  gate, and §3 says why turning it into one is a trade nobody has priced.
- **I did not touch the refinery, `STATE.md`, `roadmap.md`, or any document
  outside `code/census_remainder_f8e5/`.**
- **I did not build the general instrument for the `RERUN-CANNOT-SEE` case.**
  Re-running a producer against a `main` positioned where its reader's was — in
  a `--shared` clone, so no ref moves in this repository — would settle such a
  case with the producer's own code instead of a rule re-implemented by me.
  `D1d'` re-implements the match unbounded and says so.
- **I did not measure the 109 transcripts by which the NO-RUNNER bucket has
  grown since `81214a9`.** They are counted and named as a growth figure; a
  disposal of them is a new census.
- **I did not run this census at more than one revision.** Every number here is
  a fact about the commit printed as `as-of` in each transcript and about no
  other — which is the subject, not an accident of timing.
