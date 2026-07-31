# The population was a filename

*Repair of the three open sites of `mg-05eb`, the independent audit of the
arc-wide `| tee` sweep (`mg-c2b3`, `52aeaf4`).*

Instrument: `code/runner_exit_repair_7522/`. `sh run_all.sh`, about 20 minutes,
pure Python 3, no dependencies, no network. Every figure below is printed by a
probe in that directory next to the predicate that produced it.

---

## The short version

`mg-c2b3` swept the arc for a real defect — a `| tee` pipeline discards the exit
status of the step before it, so a runner can print six failures and exit 0 —
and repaired 17 runners at 34 sites with the defect reproduced and then caught
in both directions. **That forward repair holds and is not re-opened here.**

Three things it got wrong were about *populations and anchors*, and all three
are of a kind:

1. **The population was a filename.** Two runners called `run_audit.sh` were
   still swallowing at `HEAD` after the sweep declared the arc clean.
2. **The one figure the sweep said it had confirmed was the one its instrument
   had got wrong.**
3. **A pinned caller scan cannot see callers added after the pin.** The pin was
   the right fix for a comparison and the wrong anchor for a census.

And one more, found by doing (1) properly: **the population was also a shape.**

---

## 1 — a naming convention is not a property

The sweep scoped itself as *"63 `run_all.sh`, 23 containing `| tee`"*. Two
things in that sentence are not properties of the defect. `run_all.sh` is a
**name**. `| tee` is a **shape**. The defect is neither:

> **A pipeline whose exit status is CONSUMED, and whose DISCARDED stage can
> fail.**

Defined that way, over every tracked `*.sh` at the sweep's own revision:

| predicate | files | pipelines |
|---|---|---|
| P0 tracked `*.sh`, any depth, no name rule | 72 | — |
| P1 …containing a real pipeline on a command line | 23 | 53 |
| **P2 …status consumed and discarded stage can fail** | **19** | **26** |
| the sweep's SHAPE rule — a real `\| tee` | 19 | 42 |
| the sweep's NAME rule — a real `\| tee` in a `run_all.sh` | 17 | 34 |

**Two sets fall outside the sweep, and they are disjoint.**

**Missed by the name rule** — `code/face_geometry_audit_f1b2/run_audit.sh` and
`code/face_geometry_audit_fcf1/run_audit.sh`. Both `#!/bin/sh`, both `set -e`,
**8 `| tee` pipelines** between them, unrepaired at `HEAD`. The positive control
runs them at every one of those 8 sites in both directions: on the pre-repair
bytes a step forced to fail leaves the runner **exiting 0 with every later step
still running, 8 of 8**; on the repaired bytes the runner **exits non-zero and
stops, 8 of 8**. The defect was alive in this repository after the sweep, and
that is measured on the real runner text rather than argued from the spec.

**Missed by the shape rule** — three lines of the form

```sh
n=$(git diff "$base..HEAD" -- "$dir" | wc -c | tr -d ' ')
```

in `code/state_delegation_audit_16eb/run_all.sh` and
`code/state_delegation_repair_0049/run_all.sh`, under `set -e`, printed beneath
the sentence *"THE PREDECESSOR DIRECTORIES ARE UNMODIFIED — proof, not
assertion."* The pipeline's status is `tr`'s. A `git diff` that failed produced
an empty stream, `wc -c` reported `0`, and the proof read `-> 0 bytes`.

**These files ARE named `run_all.sh`.** The name rule contained them and the
shape rule dropped them. A sweep keyed on either misses one of the two sets;
only the property covers both.

### The clearance, re-established over the corrected population

The sweep settled its retroactive question by running all 34 tee'd targets
directly and reading the number the pipeline discarded: 34 of 34 exit 0. That
result is **sound about its population and silent about the rest.** The same
method, unchanged, is applied here to the 11 members the sweep's filename never
reached: **11 of 11 exit 0.** The corrected population is 45 and every member of
it has now had its discarded status read.

What that does *not* establish, stated rather than omitted: the same fact at
every intermediate commit. It is read at `HEAD`, on one machine, and the rows
say so.

---

## 2 — the strongest wording marks where the author stopped looking

`out_k1_census.txt`, the sweep's own committed transcript, prints

```
setting pipefail                   ticket  1   re-derived  0   DIFFERS
```

and four reader-facing artifacts — the README, `OUTCOMES.md`, the published
document, and `k1_census.py`'s own docstring — reported that same number as
**1, "confirmed exactly"**. The document even named the right file.

**The ticket was right.** `libc2b3.PIPEFAIL_RE` was `^\s*set\s+-o\s+pipefail` —
one spelling of the option — and the single runner in the arc that sets it,
`code/state_restructure_34bf/run_all.sh`, writes `set -euo pipefail`. The regex
is repaired, and both rules are run on the same bytes so the disagreement is
exhibited rather than described: the old rule re-derives **0**, the new rule
re-derives **1**, the ticket said **1**.

### The general form, which is worth more than the figure

> **"Confirmed exactly", "verified", "byte-identical" and their relatives mark
> the place where the author stopped looking. They are a reason to check
> FIRST, not a reason to skip.**

Applied, mechanically, to the sweep itself. The population of reader-facing
artifacts is derived from `git show --name-only 52aeaf4` rather than from the
four files the audit happened to name — a hand-list is a filename rule, and
that is the defect one section up. **18 strength-marked numeric claims**, every
one dispositioned with the reason. **Four were wrong:**

* the two `pipefail` rows (README and the published document);
* `k1_census.py`'s docstring;
* *"the shebang is `#!/bin/sh` on all 64 runners (measured)"* — it is **59 of
  64**, and the other five are `#!/bin/bash` or `#!/usr/bin/env bash`.

That last one is the same defect with the roles reversed. `k2_consume.py`
printed *"on 59 of the 64"*. The **instrument was right and the document rounded
it up to `all`** — and then wrote `(measured)` beside it.

---

## 3 — the anchor of a census is not the anchor of a comparison

> **A pinned baseline is CORRECT for COMPARING and BLIND for ENUMERATING.**

`mg-821e` found that a comparison anchored to `HEAD` stops comparing the moment
the repair lands — it compares the repaired tree with itself and reports no
change forever. Pinning it was right, and it stays pinned: anchored to the pin
the byte-comparison sees **154 changed files**; anchored to `HEAD` on a
committed tree it sees **0, by construction**.

`mg-c2b3` inherited that pin and used it for its **caller scan** as well. A
caller scan is not a comparison. It asks *what, in the world, reads a runner's
exit status* — a **census** — and a census anchored to a revision cannot contain
anything added after it. `code/species_depth_audit_4700/` executes three
affected runners twenty-one times and scores them on `rc == 0` at eight sites;
it landed in `5c16f5c`, after the pin. Its committed transcript asserts

```
code/species_repair_a4ef      exit 0   printed *** FAILED ***: yes  SWALLOWED
code/species_remainder_f8fa   exit 0   printed *** FAILED ***: yes  SWALLOWED
```

which is a claim read off an affected runner's exit status and nothing else.

The scan is now **unpinned for the enumeration and still pinned for the
classification**, and both uses are named in the file where they meet.

### And the remedy is half of the fix

Unpinning alone does not find it. The site has **two** independent reasons to be
outside the enumeration, and the anchor is one of them. Measured as a 2×2 of
anchor against rule:

| | literal path only | + runtime path |
|---|---|---|
| **pinned `bee07a1`** | not found | not found |
| **`HEAD`, unpinned** | not found | **FOUND — 8 sites, 5 reading the status** |

(The four cells' *totals* move as the arc grows; `out_s4_unpin.txt` carries the
live ones. What does not move is which cell finds this site.)

**Exactly one cell.** The other reason is a line-local rule demanding a literal
`<tree>/run_all.sh` on the executing line, which `run_runner(t)` and
`subprocess.run(["sh", "run_all.sh"], cwd=d)` do not have. Fixing the anchor
without fixing the rule leaves the site invisible; fixing the rule without
unpinning does too.

The anchor half is fixed in the sweep's own scan. The rule half is measured here
and written into `k2_consume.py` as a **stated limit with a pointer to the
complete runtime-path census**, because a limit that is written down is
checkable and an absence is not.

---

## The deliverable, checked for the defects it repairs

This document and its instrument **define populations and enumerate over them**,
and the instrument ships a `run_all.sh`. So it can exhibit every defect it
repairs, and `s5_self.py` checks all four on its own bytes. Enumerated, with the
branches that honestly cannot exhibit them and the reason:

* **A population defined by a name.** `lib7522.ls_sh()` has the signature
  `(ref=None)`. There is no name parameter, so a name filter cannot be applied
  inside the only file-listing primitive — **structural, not a promise**. The
  nine places a runner filename does appear as a filter are listed and
  dispositioned one at a time; every one is the sweep's own rule being measured
  next to the property rule.
* **A stale anchor.** Every anchor in the tree is listed with which question it
  serves. Every population primitive defaults to `ref=None`, so a census that
  forgets to think about its anchor gets the right one and a comparison has to
  ask for the pin explicitly.
* **A discarded status.** The tree's own `run_all.sh` is run through the same P2
  predicate: **0 pipelines of any kind, 6 of 6 steps redirect and guard**. Every
  Python subprocess takes a list argv — no shell, no pipeline — and `returncode`
  is read on every path including the timeout, which prints `-` and never `0`.
  `selftest7522.py`'s fixtures are strings that are never executed, so no status
  exists there to discard.
* **A strength marker standing in for a check.** **0 uses**, 19 mentions.

**And three defects in this instrument are recorded rather than smoothed away**,
all three the same one and all three caught by the tree's own self-test: a
`shell=True` grep that matched the sentence saying `shell=True` is never used; a
"contains no runner filename" check that read a docstring explaining why there
is no runner filename; and a strength-marker check that counted its own
detecting regex. **All three were greps for a form of words.** Two are now AST
walks and one is an explicit stated rule. When a check for a form of words fails
on its own documentation, the fix is usually not a better pattern but a
different kind of question.

**One prediction missed and is kept as written.** I predicted *2* `SWALLOWED`
rows in `out_q2_wiring.txt` and the probe measures **3 lines containing the
word** — two claim rows and one section header. The substance is right and the
count is not, for the reason this arc keeps finding: I predicted a number of
**claims** and the instrument counted a number of **mentions**.

**What is not checked, stated rather than omitted.** That the property predicate
is the *right* one. It is written out in full in `lib7522.pipelines`,
`discarded_stages`, `guarded` and `stage_can_fail` precisely so that disagreeing
with it is possible. A predicate nobody can disagree with is not a definition.

**And the sweep's committed transcripts are not regenerated.** A transcript is
the record of a run at a time; rewriting `out_k1_census.txt` would destroy
`mg-05eb`'s citations of it and would not be reproducible in any case — the arc
has grown well past the 64 runners that census counted. That current count is
deliberately not written into this document — a number that moves belongs in a
transcript, and `s3_figure.py` prints it. The corrected readings are published in
`code/runner_exit_repair_7522/out_s3_figure.txt`, and the sweep's own docstring,
README and `OUTCOMES.md` point at them.
