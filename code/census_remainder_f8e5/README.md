# mg-f8e5 — THE DISPOSAL OF mg-1abe's REMAINDER

**The measured damage of this class is FOUR FALSE RECORDS, NOT FIVE — and the
fifth is not a near miss, it is a suite that ran out of time.
`code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt` REPRODUCES BYTE-FOR-BYTE
at its own carrying commit. It needs about twenty-two minutes against the
census's nine-hundred-second budget.**

**mg-1abe's `TIMED-OUT` bucket is UNREACHABLE BY CONSTRUCTION.** Its README
promises, in so many words, that "`TIMED-OUT` is never folded into `DIFFERS`"
— and its instrument does the opposite of that, always, for every suite in the
arc whose runner redirects into its own transcripts, which is 99 of 166
transcript-carrying directories. A POSIX shell creates `out_x.txt` before the
producer runs; `collect()` returns bytes for any file that exists; the
`TIMED-OUT` branch is guarded by `if got[p] is None`. So a killed run is
bucketed `DIFFERS`, and `conclusion_verdict(committed, "")` is `FLIPS`.

**That is a correction to the FIVE and not to the 112.** A row wrongly in
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

*(filled from `out_d1_five.txt`)*

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

**1. THE DAMAGE IS FOUR, NOT FIVE.** The ticket's headline number is one too
large, and the reason is not a judgement call about grain — it is a suite that
ran out of time and was bucketed as a false record because the bucket for
running out of time cannot be reached. §1 and `out_d5_timeout.txt`.

**2. "FIVE FALSE RECORDS" IS STILL THE UNION OF TWO THINGS WITH OPPOSITE
REMEDIES.** A decision that changes on re-run means either the record is wrong
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

*(filled after the run)*

---

## 7. DEFECTS OF THIS INSTRUMENT, KEPT

Six, all kept rather than tuned away. Three were caught by controls filed in
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

**4. MY MOVING-REF DETECTOR MISSED THE ONE CASE WHOSE ANSWER IS KNOWN.** It
read only the driven scripts and scored mg-1abe's own pre-fix suite
`ONE-SCRIPT`, because those eight scripts never name `main` — they call a local
helper whose default is. Caught by the D4b control, which exists precisely
because it is run where the answer is published in advance. Fixed by one level
of indirection through the directory's own helpers; kept as `selftest` S3''.

**5. I KILLED A TREE-MUTATING PRODUCER MID-RUN AND ALMOST READ THE WRECKAGE AS
A RESULT.** My first re-run of `hodge_leverage_repair_ff3e` was killed by a
two-minute tool timeout while it had three documents mutated. The next run
correctly REFUSED — *"REFUSING TO RUN: these are dirty"* — and the refusal read
exactly like a census verdict for about a minute, until I ran `git status`.
Kept as `PREDICTIONS.md` D5, and guarded: every re-run asserts a clean worktree
before it starts (`dirty_paths`, `selftest` S4).

**6. THE T3 RECOVERY TIER IS A GUESS AND ITS FAILURES ARE UNRESOLVABLE.** When
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
- **I did not run this census at more than one revision.** Every number here is
  a fact about the commit printed as `as-of` in each transcript and about no
  other — which is the subject, not an accident of timing.
