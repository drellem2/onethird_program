# mg-a71f — A BUCKET THAT COULD NOT FIRE, AND A RECORD ITS OWN PRODUCER CANNOT READ

**`transcript_census_1abe`'s `TIMED-OUT` bucket was unreachable by construction
for every suite whose runner redirects into its own transcripts — 82 of the 115
transcript-carrying directories at `81214a9`, the as-of of the census this
repairs, and 111 of 174 at `cdec2e8` today. Both detectors under-count by
design. It is repaired, and the census is re-run against the same population
with the repaired instrument. The old census's numbers are preserved verbatim
beside the new ones and nothing is overwritten.**

**A bucket that cannot fire does not merely lose information. This one
MANUFACTURED damage: a suite killed at the budget was bucketed `DIFFERS`
against a zero-byte file, and `conclusion_verdict(committed, "")` scores that
`FLIPS`, which is the census's word for A FALSE RECORD AT ITS CARRYING COMMIT.**

**`audit_c067/out_c1_rebase.txt` is ANNOTATED and was NOT re-run. Its `5` is
true; its producer answers `0` today because it matches by subject inside `git
log main -n 40` and `main` is 238 commits past the carrier. A re-run writes 0
over a 5 that is true.**

All figures below name the revision they are facts about. Everything is derived
by `sh run_all.sh`, whose transcripts are committed beside it, plus the
census's own re-run in `code/transcript_census_1abe/`.

---

## 0. WHAT WAS WRONG, IN THREE LINES OF SOMEBODY ELSE'S CODE

cf8e5 found this and deliberately did not repair it. The mechanism, unchanged
from its account:

| | |
|---|---|
| `t2_census.py` starts the runner | `subprocess.Popen(["sh", "run_all.sh"])` — and the FIRST thing a POSIX shell does with `python3 t.py > out_t.txt` is **create `out_t.txt`**, before the producer runs |
| `collect()` reads it back | returns the file's **bytes if it exists**, and `None` only if it does not |
| the `TIMED-OUT` branch is guarded by | `if got[p] is None` — *the file being absent* |

A killed run therefore leaves a file that **exists**, holds zero or partial
bytes, and is **not** the committed blob. So it was bucketed `DIFFERS`, handed
to `conclusion_verdict(committed, "")`, and scored `FLIPS`.

mg-1abe's README §2 promises the exact opposite, in as many words:

> `TIMED-OUT` is never folded into `DIFFERS`. "I did not finish measuring" and
> "it does not reproduce" are different claims and only one is about the
> subject.

The rule is right. The instrument did the opposite of it, always — not on a
slow machine, and not sometimes. **By construction, for every suite in this arc
that has a runner.**

---

## 1. THE REPAIR

One line, in `code/transcript_census_1abe/t2_census.py`:

```python
-  if got[p] is None:
+  if got[p] is None or (status == "timeout" and got[p] != committed[p]):
```

The guard is now the timeout **status**, not the file's absence.

**THE ONE PLACE THIS IS A JUDGEMENT AND NOT A MECHANISM.** The conservative
repair buckets *every* row of a killed suite as `TIMED-OUT`. This one keeps a
row that already matched the committed blob **byte-for-byte**, because a
truncated write cannot forge the whole blob — the match is proof the producer
finished that file before the axe fell. `a1`'s A1b prints both columns so a
reader who disagrees can subtract, and the census's own `T2f` names every such
row. Two further changes come with it, both the same defect:

- the determinism control no longer fires after a timeout. Two killed runs
  disagreeing is a fact about where the axe fell, not about the producer, and
  it cost a second full budget to learn nothing.
- `T2f` in the census transcript now **reports the size of the correction** —
  how many rows were killed with the shell's file already in place — instead of
  leaving it to be inferred from a diff of two transcripts.

### The control that could refuse it

`a1_bucket.py` is built to refuse in four directions, and it is pointed at
**transcribed** classifiers whose transcriptions are checked against real blobs
before anything is scored against them.

| arm | what it would catch |
|---|---|
| A1a | a transcription that is not what ran — both sides checked against blobs, the BEFORE side by **blob sha** |
| A1b | the four states a `SIGKILL` at the budget can leave, through both classifiers |
| A1c | what the `DIFFERS` route then computes — `conclusion_verdict(x, "")` is `FLIPS` |
| **A1d** | **the arm that guards the repair.** Every non-timeout status × every file state, both classifiers, exhaustively. The repair is licensed to move the timeout row and nothing else; any other movement is a SELF-ERROR |
| A1e | the reach, over the whole arc, by a proxy that names the direction it can be wrong in |

`a3_endtoend.py` then runs the census's **own `t2_census.py`, unmodified**, at a
forced budget it cannot meet, and requires the bucket to fire — because a
checked transcription is still not the thing itself, and the classifier lives
downstream of a real `Popen`, a real kill to a process group, and a real
`collect()` off a real disk.

---

## 2. THE RE-RUN, AND WHY IT IS AT `81214a9`

**The 107 are defined at `81214a9`.** Only a run at that as-of can size *that*
set; a run at today's `main` would measure a different, larger population and
could not answer the question the ticket asked. It would also make the census
re-enter three censuses that did not exist at `81214a9` — `census_remainder_f8e5`,
`census_repair_f3ff`, `census_audit_4d3b` — each of which spawns worktrees of
its own.

So: **same as-of, same population (541 transcripts, 164 groups), same 900 s
budget, repaired instrument.** The delta is attributable to the instrument and
to the passage of time, and `a4` refuses to conflate those two.

**IT COULD NOT BE DERIVED ON PAPER, AND THAT IS THE COST OF THE DEFECT.** The
old census's transcript records, for a `DIFFERS` row, `conclusion FLIPS/HELD/…`
and nothing else — no run status, no duration. **The old run's timeouts are not
recoverable from its own output.** There is no arithmetic that splits 112 into
timeouts and differences; the evidence that would have sized the bucket was
never written down, because the bucket could not fire. The only instrument that
can answer is the repaired census, re-run.

### The cost the ticket sized, paid in full

Editing that suite **displaces all 8 of its transcripts**, and the ticket said
so before authorising it. The mechanism is R1: a transcript declares a
`code-digest` over the directory's **committed** code, so changing a script
after the transcripts were written makes every one of them declare a digest of
code that did not produce it. The only honest response is to freeze the code,
commit, and re-run the whole suite — which is what R1 is shaped to force, and it
forced it twice here (see D7).

And **all 8 of them declare `reads-outside-tree: yes`** in their own headers —
measured, not assumed: 8 of 8 committed transcripts on `main` carry that line.
Every one of them reads refs, `main`'s history, or the file list of `main`, so
every one was already displaced by `main` moving, with or without this edit.
That is the census's own T2e finding — *a producer that reads repository-global
state is displaced by the next commit anyone makes* — arriving at the census.

### What the re-run is NOT

- **NOT a correction applied to the old census's numbers.** It is a different
  measurement. The old transcript stands in this directory verbatim as
  `prior_1abe_t2_census_at_81214a9.txt` and is printed beside the new counts in
  `a4`'s A4e rather than replaced by them.
- **NOT a weakening of `112`.** `112` stands as an UPPER BOUND on
  non-reproduction whose slack is unsized. cf8e5 was explicit that nothing here
  weakens it, and this run did not measure it.
- **NOT a property of the arc alone.** `TIMED-OUT` is a fact about the
  repository **and the machine**, which is the census's own T2d disclosure. This
  run happened on a box at a load average above 30 with other agents on it. A
  quieter box moves rows back out of the bucket.

---

## 3. `audit_c067/out_c1_rebase.txt` — ANNOTATED, NOT RE-RUN

**A re-run writes 0 over a 5 that is true.**

`C1a` asserts that mg-132a's 5 commits were replayed onto a larger tree by the
refinery's rebase. They were. `c1_rebase.py:48` pairs each pre-rebase commit
with its replayed twin **by subject**, inside `git log --format=%H%x1f%s main -n
40`. The ref moves; the literal does not. The transcript's carrying commit is
`47e56b3` and `main` is **238 commits past it**, so every twin fell out of the
back of that window while staying exactly where it was.

The producer's own docstring guards the **ref** by name — *"any single ref name
here is a hard-coded anchor of exactly the kind this audit exists to complain
about"* — and leaves the **window** hard-coded three lines below it.

A note is prepended to the transcript in the format mg-56dc used at
`code/runner_exit_c2b3/out_k1_census.txt`. Every factual clause of it is
**re-derived on every run** by `a2_c067_annotation.py`, which never executes
`c1_rebase.py` and never writes into `code/audit_c067`:

| arm | as of `cdec2e8` |
|---|---|
| A2a | the note appears exactly once, and the **8944 bytes below it are byte-identical** to the blob at `47e56b3`. The annotation added 3464 bytes above the record and changed none of it |
| A2b | every off-`main` commit the record names is **still twinned on `main` by subject, 6 of 6**, when the search is not bounded by a literal. Population derived from the transcript's own text, not from a list I chose |
| A2c | **6 of 6** twins are on `main` **and** outside `main -n 40`. Both halves required: present, and unreachable by the walk that looks for them |
| A2d | all 6 objects still resolve; **1 distinct ref** holds them |
| **A2e** | **the arm that can condemn the note.** The producer's live answer is computed by reading `main`'s log the way line 48 reads it: **0 pairs, against a record asserting 5.** If this ever becomes 5, the note must be withdrawn, and this arm is how anyone finds out |

**NOT DONE HERE, and named rather than left implicit:** `c1_rebase.py`'s window
is **not repaired**. Removing the `-n 40` would make the producer see the 5
again *and* rewrite the transcript — the thing the note exists to prevent.
Repairing the producer and preserving the record are separate acts and only the
second is authorised here.

---

## 4. DEFECTS OF MY OWN, ALL KEPT

**D1 — I read the pre-repair instrument at a commit where it does not exist,
and the control refused on its first execution.** `a1`'s first draft took the
BEFORE side of the comparison from `81214a9`, reasoning that every published
census figure is a fact about that commit. They are — and
`code/transcript_census_1abe/t2_census.py` **is not there**. `81214a9` is the
revision the census *measured*; the census's own code was committed after the
run that measured it. A `[SELF-ERR]` on the first run is the only reason this
sentence is not a false one.

**D2 — and the obvious fix was the defect this ticket annotates, committed
inside the annotation.** `git log -1 main -- t2_census.py` names the pre-repair
source correctly today and names **the repair itself** the moment this merges.
The arm checking "the pre-repair guard looked like this" would then fail
forever, on a true statement, for exactly the reason
`audit_c067/out_c1_rebase.txt` fails. The pre-repair source is therefore pinned
by its **blob sha** — this census's own remedy (*"NOT a commit sha — a commit
sha is displaced by every rebase, a blob digest is not"*), applied to the
instrument that proposed it.

**D3 — my repair's own detail strings created a parser hazard, and W3 exists
because of it.** The repaired detail column ends `…the PRE-mg-a71f guard called
this DIFFERS`. A parser asking *is `DIFFERS` in this line* would score the
repaired verdict as the defect it repairs — **in exactly the rows the repair
moved, and nowhere else**, so it would be invisible on a sample. `a0`'s W3 is a
planted world for it.

**D4 — I counted one ref three times.** `a2`'s A2d' reported the pre-rebase
commits hanging off "2 refs", which were `origin/polecat-132a` and
`refs/remotes/origin/polecat-132a` — **the same ref under two spellings**, taken
from the producer's own candidate list. A fragility figure reported as twice as
safe as it is, in the arm whose whole subject is how little is holding those
objects up. Deduped by canonical ref path: it is **1**, and cf8e5's `C1a''`
forecast of 2 → 1 has landed.

**D5 — `a3`'s first draft asserted the opposite of what it meant.** The arm
checking that the detail column explains the bucket was written `"…" not in
row[0]`, which passes when the explanation is absent. Caught by reading it, not
by running it — it would have gone green either way while the repair was
working, which is the worse half of the finding.

**D7 — I wrote a duration I had never measured into the docstring of the repair
itself, and it cost the re-run a restart.** The repaired `t2_census.py` said
*"for eight weeks this bucket COULD NOT FIRE"*. The census's `t2_census.py` was
first committed at `e2b08cf` on **2026-08-06**, four days before this ticket,
and the entire repository is 22 days old. Eight weeks was a number that felt
like the right size for the finding, which is the whole failure. Caught by
re-reading my own diff about twenty minutes into the ~4-hour re-run — so the run
was **killed, the sentence corrected, the code re-committed and the run
restarted**, because the alternative was to publish transcripts whose declared
`code-digest` was of code I intended to change. That is R1 doing exactly what it
is shaped to do, to its author.

**D6 — the reach figure is FOUR numbers, not one, and none of them is wrong.**
The ticket's headline says *99 of 166*. That is cf8e5's **README** figure, at
`e35b51c`. cf8e5's own committed transcript, `out_d5_timeout.txt`, says **101 of
169** at `bc965aa` — a later commit the same day. Both are correctly labelled
with their as-of and neither is false; the ticket picked up the one from the
prose. Measured here, with a detector of my own that counts `undetermined` in
its own row rather than folding it either way:

| as-of | date | reach | source |
|---|---|---|---|
| `e35b51c` | 2026-08-10 | 99 of 166 | cf8e5's README — the ticket's headline |
| `bc965aa` | 2026-08-10 | 101 of 169 | cf8e5's `out_d5_timeout.txt` |
| `81214a9` | 2026-08-06 | **82 of 115** | `a1e` — the as-of of the re-run, so the figure that goes with these census numbers |
| `cdec2e8` | 2026-08-10 | **111 of 174** | `a1e` — today |

The two detectors are not the same rule and the difference is not adjudicated
here: cf8e5's requires a literal `.txt`, mine does not, and mine leaves 27
directories `undetermined` at `81214a9`. Both under-count by design. Quoting any
one of these as a present-tense fact about the arc would have been the arc's own
recurring defect, which is why the row that matters for §2's numbers is the
`81214a9` one and it is stated with its population.

---

## 5. WHAT IS NOT DONE, AND IS NOT PRETENDED

- **No `PREDICTIONS.md`.** The convention in this arc is to commit predictions
  *before* the instrument exists. I did not, so I do not file a file that
  claims I did.
- **`c1_rebase.py` is not repaired** (§3).
- **The 900 s budget is not defended.** Rows in `TIMED-OUT` are rows this run
  did not measure; whether they reproduce is open, and `--timeout N` moves the
  line.
- **`census_remainder_f8e5/out_d5_timeout.txt` will stop reproducing when this
  merges.** Its `D5a` arm checks that t2's `TIMED-OUT` branch is guarded by
  `got[p] is None`, and after this merge it is not. That is the repair landing,
  not that record being wrong — the same shape as
  `runner_exit_c2b3/out_k1_census.txt`. It is cf8e5's directory and nothing here
  edits it; this line is the notice.
- **A census at today's `main` is not run.** It is a larger, different
  measurement and it cannot size the 107.

### Two things next to the repair that were looked at and left alone

Noted rather than fixed, because neither is what this ticket authorised, and
because an unfixed thing that is written down is worth more than one that is
quietly widened into.

- **`run_suite` waits on the runner, not on its descendants.** It starts the
  suite with `start_new_session=True` and kills the process *group* on timeout,
  but a suite whose own children outlive it returns `ok` while a transcript may
  still be being written. That is a race the repair does not touch and did not
  introduce. It has not been observed firing.
- **`RUNNER-FAILED` may be the wrong name for what it catches.** It buckets a
  missing transcript whenever the runner exited non-zero — and in this arc a
  non-zero exit is the **normal** state of an instrument that found what it was
  sent to find, which is the exit convention `run_all.sh` states at the top of
  every suite. A suite that legitimately exits 1 and legitimately does not write
  some file lands in a bucket whose name says it could not start. Both that
  bucket and `NOT-REGENERATED` were **0 of 541** in the prior census, so nothing
  is riding on it today.

---

## 6. THE FILES

| file | what it is |
|---|---|
| `a0_selftest.py` | the parsers against six planted worlds, including one built from the hazard the repair introduced |
| `a1_bucket.py` | the bucket before and after, on the same states, with the arm that guards the repair |
| `a2_c067_annotation.py` | every clause of the c067 note, re-derived; never executes its producer |
| `a3_endtoend.py` | the census's own `t2_census.py`, unmodified, at a budget it cannot meet |
| `a4_size107.py` | the two censuses of one population, transitioned row by row |
| `prior_1abe_t2_census_at_81214a9.txt` | the PRIOR census, verbatim. Not overwritten, not summarised |
| `prior_1abe_t1_population_at_81214a9.txt` | its population transcript, likewise |
