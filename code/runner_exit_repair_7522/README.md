# `code/runner_exit_repair_7522` — the three open sites of mg-05eb

`sh run_all.sh` — about 20 minutes, pure Python 3, no dependencies, no network.

**Target:** the three OPEN items of `682db2c` (mg-05eb), the independent audit of
the arc-wide `| tee` sweep `52aeaf4` (mg-c2b3). The audit's fourth finding —
that the forward repair holds at 17 of 17 both ways — is **not re-opened**.

## What is here

| file | what it answers |
|---|---|
| `PREDICTIONS.md` | every count, with **when each was written**: PREDICTED, INHERITED, or MEASURED FIRST |
| `selftest7522.py` | the classifier in **both senses at every rule**, this tree's own runner by its own rules, and the one claim about `/bin/sh` that the population rule rests on, measured on this machine |
| `s1_population.py` | **OPEN 1** — the population by a PREDICATE OVER CONTENT, at the pin and at HEAD, next to the two rules it replaces |
| `s2_status.py` | **OPEN 1** — the discarded status of everything outside mg-c2b3's population, read directly; and the positive control in both directions at all 8 sites |
| `s3_figure.py` | **OPEN 2** — the `pipefail` figure re-derived under both regexes, and every strength-marked numeric claim of the sweep enumerated and dispositioned |
| `s4_unpin.py` | **OPEN 3** — the anchor × rule 2×2, the comparison that keeps its pin, and the site that needed both fixes |
| `s5_self.py` | this deliverable, checked for the four defects it repairs, on its own bytes |
| `OUTCOMES.md` | findings, prediction misses, and the three defects in this instrument that are recorded rather than smoothed away |

## Verdict in one line

**The population was a filename and it is now a predicate; the figure that was
called confirmed was the one the instrument got wrong and is now re-derived
under a repaired rule; and the pinned caller scan is unpinned for the census
and still pinned for the comparison — with the measured finding that unpinning
was necessary and not sufficient.**

## OPEN 1 — the population is a property now, and it is bigger both ways

`run_all.sh` is a naming convention. `| tee` is a shape. Neither is the defect.
The defect is **a pipeline whose exit status is consumed and whose discarded
stage can fail**, and `s1_population.py` defines the population that way:

| predicate | files | pipelines |
|---|---|---|
| P0 tracked `*.sh` at `bee07a1`, no name rule | 72 | — |
| P1 …containing a real pipeline on a command line | 23 | 53 |
| P2 …status consumed **and** discarded stage can fail | **19** | **26** |
| the sweep's SHAPE rule — a real `\| tee` | 19 | 42 |
| the sweep's NAME rule — a real `\| tee` in a `run_all.sh` | 17 | 34 |

**Two sets fall out, and they are disjoint.**

* **Missed by the NAME rule** — `code/face_geometry_audit_f1b2/run_audit.sh` and
  `code/face_geometry_audit_fcf1/run_audit.sh`: `#!/bin/sh`, `set -e`, **8
  `| tee` pipelines**, unrepaired at HEAD after the sweep reported the arc
  clean. Both are repaired here.
* **Missed by the SHAPE rule** — three `git diff … | wc -c | tr -d ' '` lines in
  `code/state_delegation_audit_16eb/run_all.sh` and
  `code/state_delegation_repair_0049/run_all.sh`. These files **are** named
  `run_all.sh`; the sweep looked for `| tee` and these throw `git diff`'s status
  away without it. Each stands under the sentence *"THE PREDECESSOR DIRECTORIES
  ARE UNMODIFIED — proof, not assertion"*, and a failing `git diff` produced an
  empty stream, `wc -c` reported `0`, and the proof read `0 bytes`. Repaired
  here, byte counts unchanged.

**The retroactive clearance is re-established over the corrected population,
and at the grain the population executes at.** mg-c2b3 read 34 discarded
statuses **at the SITE grain**; `s2_status.py` reads the rest by the same method
at the **EXECUTION** grain — 8 `| tee` invocations plus 8 `git diff`
invocations, because the three `git diff` source lines sit inside `for` loops.
**16 of 16, all zero**, every argv derived from the runner's own bytes.

**This paragraph used to read `45 of 45`**, which added 34 sites to 11 lines and
called the sum a population (`mg-dee4`/F1). The two halves are counted at
different grains and are no longer added: **34 sites inherited from a transcript
this repair did not re-run, plus 16 executions run here.** The verdict survived
the correction; the arithmetic did not.

## OPEN 2 — the figure, and the habit worth more than the figure

`out_k1_census.txt` prints `setting pipefail | ticket 1 | re-derived 0 |
DIFFERS`. Four reader-facing artifacts reported that same number as **1,
"confirmed exactly"**. The ticket was right; `libc2b3.PIPEFAIL_RE` matched only
`set -o pipefail` and the one runner that sets the option writes
`set -euo pipefail`. **The regex is repaired**, the four artifacts are
corrected, and `s3_figure.py` runs both regexes on the same bytes so the
disagreement is exhibited rather than described.

**The general form.** *"Confirmed exactly", "verified", "byte-identical" mark
where the author stopped looking, so they are a reason to check FIRST.* Applied:
`s3_figure.py` derives the sweep's reader-facing artifacts from
`git show --name-only 52aeaf4`, finds **24** strength-marked numeric claims, and
dispositions every one — with coverage checked in **both** directions, so a hit
with no rule and a rule with no hit are each an error. **It found 20 while the
rule was line-local** (`mg-dee4`/F4): a marker and its figure separated by a
hard wrap scored as neither line, and the window is now one line in either
direction. **Five were wrong:** the
`pipefail` row in the README, in `OUTCOMES.md`, and in the published document;
`k1_census.py`'s docstring; and *"the shebang is `#!/bin/sh` on all 64 runners
(measured)"*, which is **59 of 64**. That last one is the same defect with the
roles reversed: `k2_consume.py` printed *"on 59 of the 64"* and the document
rounded it up to `all`.

## OPEN 3 — the anchor of a census is not the anchor of a comparison

> **A pinned baseline is CORRECT for COMPARING and BLIND for ENUMERATING.**

The pin was mg-821e's right answer to a comparison anchored at `HEAD`, which
stops comparing the moment the repair lands. mg-c2b3 used the same pin for its
**caller scan**, and a caller scan is a census. `k2_consume.py`'s scan is now
unpinned for the enumeration and still pinned for the runner classification,
with both uses named where they meet.

**And a measured finding the ticket's remedy does not cover:** unpinning is
necessary and **not sufficient**. `s4_unpin.py` runs the anchor × rule 2×2 —

| | literal path only | + runtime path |
|---|---|---|
| **pinned `bee07a1`** | 1 site | 19 sites |
| **HEAD, unpinned** | 1 site | 48 sites |

(The `HEAD` row grows as the arc does — that is the point of the row, and
`out_s4_unpin.txt` carries the live count. The load-bearing claim is the cell
the next paragraph names, not the totals.)

— and `code/species_depth_audit_4700/` appears in **exactly one cell**: HEAD ×
runtime-path. The pin and a line-local rule demanding a literal
`<tree>/run_all.sh` are **two independent reasons** the same site fell outside
the enumeration; `run_runner(t)` and `subprocess.run(["sh", "run_all.sh"],
cwd=d)` have no literal path on the executing line. The anchor half is fixed in
mg-c2b3's own scan. The rule half is measured here and **named as a stated limit
inside `k2_consume.py`** rather than left as an absence.

## The general form, applied to this tree

This deliverable defines populations and enumerates over them, and it ships a
`run_all.sh`, so it can exhibit every defect it repairs. `s5_self.py` checks all
four on this tree's own bytes; enumerated, with the branches that honestly
cannot exhibit them:

1. **D1, a population defined by a name.** `lib7522.ls_sh()` has the signature
   `(ref=None)` — no name parameter, so a name filter cannot be applied inside
   the only file-listing primitive. Structural. The 9 places a runner filename
   *does* appear as a filter are listed and dispositioned one at a time; all are
   the sweep's own rule being measured.
2. **D2, an enumeration anchored to a stale revision.** Every anchor in this
   tree is listed with which question it serves. Every population primitive in
   `lib7522.py` defaults to `ref=None`, so a census gets the right anchor by
   default and a comparison has to ask for the pin.
3. **D3, the pipeline defect itself.** This tree's `run_all.sh` is run through
   S1's own P2 predicate: **0 pipelines of any kind, 6 of 6 steps redirect and
   guard**. Every Python subprocess takes a list argv — no shell, no pipeline,
   so `returncode` is the target's own status — and `run_argv` returns `None`
   on timeout, which prints `-` and never `0`.
4. **D4, a strength marker standing in for a check.** A marker inside quotes or
   backticks is the arc naming a form of words; written bare and applied to a
   figure it is a use. That distinction is the same one as *"a comment quoting
   `| tee` is not a pipeline"*, and three of this tree's own checks got it wrong
   first — see `OUTCOMES.md`.

   **This branch reported `0 USES` under a different instrument from the one it
   pointed at its subject** (`mg-dee4`/F3): 3 alternatives here against 9 there,
   with `verified` — named as a marker in `s5_self.py`'s own docstring, in this
   file and in the published document — in the nine and not in the three; and a
   population of `*.py` and `*.sh`, so this README, `OUTCOMES.md`,
   `PREDICTIONS.md` and the published document were all outside it, which is
   where three of `mg-05eb`'s four wrong artifacts were. There is now **one rule
   object**, `lib7522.MARK`, used in both directions; the population includes
   this tree's `*.md` and the document; and a USE is judged **BACKED or
   UNBACKED** by whether every figure on its line is printed by a transcript
   this tree commits. `out_s5_self.txt` carries the four classes with the
   extent, and the extent is in this sentence rather than only in the
   transcript.

**What cannot be checked here, stated rather than omitted:** that the property
predicate is the *right* one. It is written out in full in `lib7522.pipelines`,
`discarded_stages`, `guarded` and `stage_can_fail` precisely so that disagreeing
with it is possible. A predicate nobody can disagree with is not a definition.

## What this repair does not touch

`code/runner_exit_c2b3/out_*.txt` are **not regenerated**. A transcript is the
record of a run at a time; rewriting it would destroy mg-05eb's citations of it
and would not be reproducible anyway — the arc has grown well past the 64
runners that census counted. (The current count is deliberately not written
here: a number that moves belongs in a transcript, and `s3_figure.py` prints
it.) The corrected readings are published here, and `k1_census.py`'s docstring
points at them.
