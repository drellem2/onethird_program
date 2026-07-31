# INDEPENDENT AUDIT of the arc-wide `| tee` sweep (mg-c2b3, `52aeaf4`)

**Auditor:** mg-05eb (pre-filed in the same action as its parent; no coordination)
**Target:** `52aeaf4` — *"control+repair: THE ARC-WIDE `| tee` SWEEP, AND WHICH PAST GREENS
DEPENDED ON A SWALLOWED EXIT CODE — 17 runners repaired with the defect REPRODUCED and then
CAUGHT at 34 of 34 sites, and the retroactive answer is three claims, all in one file"*
**Audited:** `code/runner_exit_c2b3/` (`k1_census.py`, `k2_consume.py`, `k3_retro.py`,
`k4_control.py`, `libc2b3.py`, their committed transcripts, `README.md`, `OUTCOMES.md`), the
17 runners the commit repaired plus the one it added, and `docs/OneThird-RunnerExit-ArcWideSweep.md`
**Audit code:** `code/runner_exit_audit_05eb/` — `sh run_all.sh`, ~25 minutes. Its parser is
written from scratch; it imports nothing from `libc2b3.py`, because an audit that borrows the
parser it is auditing cannot disagree with it about what a pipeline is.

---

## VERDICT

**The forward repair is right, the retroactive METHOD is right, and both were applied to a
population defined by a filename.** Seventeen runners now stop when a step fails — measured
here on the real runners, in both directions, at 17 of 17. The routing of every past claim
into *byte-comparison / printed output / exit status* and the settling of only the third class
is the correct shape for the retroactive question, and the nine claims are dispositioned one
at a time with a reason each, which is what the assignment asked me to check.

**Three findings, and each of them is about where the sweep looked rather than how it looked.**

1. **The population is `run_all.sh`, and two runners with 8 real `| tee` pipelines are not
   called that.** They are unrepaired at HEAD, and this audit reproduces the defect on them.
2. **The one census figure the sweep says it "confirmed exactly" is the one its instrument got
   wrong** — and four reader-facing artifacts assert a measurement that the instrument's own
   committed transcript contradicts.
3. **A past claim that reads two affected runners' exit codes is outside the enumeration,**
   because the caller scan is pinned to a revision that predates the claim. Re-run at HEAD,
   two of its committed rows no longer hold.

On the fourth question the assignment raises — did it fix runners that did not need fixing,
and did it say so — **the sweep is clean**, and §4 says so with a measurement rather than
with a shrug.

---

## 1. THE RETROACTIVE HALF, WHICH IS THE HARD HALF

### 1.1 What the sweep did, and it is the right shape

`k3_retro.py` routes every past claim into one of three kinds and settles only the third:

| | route | why it is or is not at risk |
|---|---|---|
| R1 | a committed **byte-comparison** | the bytes never travel through the pipeline; `tee f` and `> f` write the same file |
| R2 | the **printed output** | printed and committed whatever the status was |
| R3 | the **exit status** | AT RISK |

That is correct, and the per-claim discipline is real: nine claims, each with a site, a quoted
claim, a disposition and a stated reason; seven marked SAFE *with the reason* rather than left
ambiguous; two AT RISK and settled by going and getting the number the pipeline discarded.
**§J2d checks the narrower thing a hand-written list rots at** — does each named file still
exist and still contain the quoted text? **9 of 9.**

### 1.2 The claim the enumeration did not consider

The nine are a Python literal in `k3_retro.py`, hand-written. So this audit did not check the
nine; it built the list **mechanically** and asked what falls outside.

`code/species_depth_audit_4700/q2_wiring.py` executes three species trees' `run_all.sh`
**twenty-one times** through `run_runner()` — `subprocess.run(["sh", "run_all.sh"], …)`,
returning `p.returncode` — and scores that status at **8 sites**, including one whose variable
is literally called `swallowed`:

```python
swallowed = (rc == 0)
```

Two of its three trees — `species_repair_a4ef` and `species_remainder_f8fa` — had a `| tee`
pipeline at the pin. Its committed transcript contains:

```
code/species_repair_a4ef      exit 0   printed *** FAILED ***: yes  SWALLOWED
code/species_remainder_f8fa   exit 0   printed *** FAILED ***: yes  SWALLOWED
```

Those two rows are claims read off an affected runner's exit code and nothing else — R3 by the
sweep's own routing. **They are not among the nine.**

**Why they could not have been, and this is the interesting part.** `k2_consume.py`'s caller
scan enumerates its population with `git ls-tree -r --name-only bee07a1`. `code/species_depth_audit_4700/`
landed in `5c16f5c`, *after* `bee07a1` and *before* the sweep. Pinning is **correct** for the
byte-comparison in `K3d` — anchored to HEAD it would compare the repaired tree with itself,
which is mg-821e's own finding, recorded in this very tree. It is **wrong** for a caller scan,
because a consumer that landed after the pin is invisible to it and is nonetheless a consumer.
The pin that fixes one defect opens the hole for another, and nothing in the sweep separates
the two uses.

**Measured, not argued.** §J2c reinstates mg-4700's own `RED_STUB`, byte-identical, over the
same three self-tests and re-runs the three runners at HEAD:

```
code/species_repair_a4ef      exit 1    printed *** FAILED ***: yes  stopped the run
code/species_remainder_f8fa   exit 1    printed *** FAILED ***: yes  stopped the run
code/species_repair_6f61      exit 1    printed *** FAILED ***: no   stopped the run
```

**Both rows flip.** This is not a defect in the repair — the repair is *why* they flip. It is a
past claim that depended on an affected runner's exit code, which is exactly the population
item 3 of the ticket names, and two committed rows in this repository now assert an exit code
the tree no longer produces with no artifact of the sweep saying so.

### 1.3 The sweep's headline, tested

> *"the arc reads its results from committed transcripts and byte-comparisons almost
> everywhere, and reads them from an exit status in exactly ONE file"*

§J2a scans every tracked `.py` and `.sh` at the pin and at HEAD for files that **both** execute
a shell script **and** score a variable against 0. Resolving imported helpers matters: the one
file the sweep names reaches its runners through `run_runner(t)`, which contains neither `sh`
nor `.sh` on the calling line — a line-local rule cannot see it, and my own first draft missed
`p3_wiring.py` for exactly that reason.

**R3 consumer files: 9 at `bee07a1`, 13 at HEAD.** Of those, three score the exit status of a
runner that was affected:

| file | in the nine? |
|---|---|
| `code/species_sites_821e/p3_wiring.py` | yes — the sweep names it |
| `code/species_depth_audit_4700/q2_wiring.py` | **no** — §1.2 |
| `code/runner_exit_c2b3/k3_retro.py` | no — but it is the sweep's own instrument |

**The third row is listed and then set aside**, because counting the sweep's own contemporaneous
instrument as a past exposure would double the size of this finding. As a count of files that
score a runner's exit status, "exactly one" is wrong three ways. **As a count of past claims at
risk it is wrong once, and the once is §1.2.**

### 1.4 A second hole in the caller scan, checked and empty

`k2_consume.py` builds its caller population as

```python
files = [f for f in … if (f.endswith(".py") or f.endswith(".sh"))
         and not f.endswith("/run_all.sh")]
```

— every `run_all.sh` is **excluded from being a caller**. A runner that runs another runner
under `set -e` consumes its status and cannot appear in that table. §J2a2 measures it: **3 of
the repository's shell-level runner executions are invisible to `K2a` by that filter, and none
of them targets an affected runner.** The hole is real and empty. It is reported anyway,
because a hole that happens to be empty and a hole that was checked and found empty are the
same table row and completely different evidence.

---

## 2. THE COUNTS, RE-DERIVED WITH MY OWN INSTRUMENT

The ticket said **63 / 23 / 1**. The sweep re-derived **64 / 23 / 0**. §J1 re-derives them from
a parser that has never seen `libc2b3.py`, over a population it declares: **every tracked
`*.sh` in the repository**, not every file named `run_all.sh`.

| | ticket | sweep | mg-05eb | |
|---|---|---|---|---|
| `run_all.sh` in the tree at `bee07a1` | 63 | 64 | **64** | agrees with the sweep |
| matching the bare grep `\| *tee` | 23 | 23 | **23** | agrees |
| containing a real `\| tee` **pipeline** | — | 17 | **17** | agrees |
| the six the grep counts and the parser does not | — | 6 | **6** | agrees, from an independent rule |
| setting `pipefail` | 1 | **0** | **1** | **the ticket was right and the sweep is wrong** |
| **`*.sh` NOT named `run_all.sh` with a real pipeline** | — | *not in the population* | **2 files, 8 pipelines** | §3 |

Four of the five re-derivations agree, and agreeing from a parser written from scratch is worth
more than agreeing from the same one. The fifth is a finding.

### 2.1 `pipefail: 1` — the number said to be confirmed is the number that is wrong

```
libc2b3.PIPEFAIL_RE = re.compile(r"^\s*set\s+-o\s+pipefail")
```

The one runner in this repository that sets the option writes it in the combined form —
`code/state_restructure_34bf/run_all.sh:4: set -euo pipefail` — which that pattern cannot
match. So `out_k1_census.txt` prints:

```
setting pipefail                   ticket  1   re-derived  0   DIFFERS
```

and **four reader-facing artifacts say the opposite**:

```
code/runner_exit_c2b3/README.md:28          | setting `pipefail` | 1 | **1** — confirmed exactly |
code/runner_exit_c2b3/OUTCOMES.md:132       | `pipefail` | 1 | **1** | AGREES |
docs/OneThird-RunnerExit-ArcWideSweep.md:45 | setting `pipefail` | 1 | **1** | confirmed exactly
                                              — `code/state_restructure_34bf/` |
code/runner_exit_c2b3/k1_census.py:18         "The pipefail count (1) is confirmed exactly."
```

The document even **names the right file**. The prose is right about the world and wrong about
its own measurement — the author knew the answer and nobody reconciled it with the transcript
the instrument printed. That is the SUMMARY-vs-ROWS defect this arc repaired in mg-8aae and
mg-8eca, reproduced inside the artifact that repairs swallowed statuses.

The same blind spot produced a second sentence, and §J1e measures it:

> *"The shebang is `#!/bin/sh` on all 64 runners (measured)."*

**False at 5 of 64** — four `#!/bin/bash` and one `#!/usr/bin/env bash`. The mechanism argument
is not damaged: the one runner that sets `pipefail` legitimately does so because it really is
bash. What is damaged is the word *measured*.

---

## 3. THE POPULATION IS A NAMING CONVENTION

A pipeline in a file called `run_audit.sh` swallows exactly the same status as a pipeline in a
file called `run_all.sh`. §J1a declares the population as every tracked `*.sh` and finds:

```
code/face_geometry_audit_f1b2/run_audit.sh   set -e: yes
    14   python3 audit_scoring.py            | tee out_scoring.txt
    15   python3 audit_gates.py              | tee out_gates.txt
    16   python3 audit_theorem_and_content.py | tee out_theorem.txt
    17   python3 audit_injections.py         | tee out_injections.txt
    18   python3 audit_nmax2.py              | tee out_nmax.txt
code/face_geometry_audit_fcf1/run_audit.sh   set -e: yes
    16   python3 audit_nc4.py 5 | tee out_nc4.txt
    20   python3 audit_extra.py | tee out_extra.txt
    24   python3 audit_gauge.py | tee out_gauge.txt
```

Both are `#!/bin/sh`, both set `set -e`, both are the entry point their document names
(*"`run_audit.sh` regenerates all five"*, `docs/audit-mg-8a12-nc4-scoring-repair.md:12`), and
both are **unrepaired at HEAD**.

> Over the population a reader would assume — shell runners in this repository — the sweep is
> **17 of 19 files and 34 of 42 pipelines**, not 17 of 17 and 34 of 34.

§J3c is the negative control and it is the point: the same instrument, the same forced failure,
the same reading of the runner's own exit code. See §4.2.

---

## 4. THE POSITIVE CONTROL — BEHAVIOUR, NOT PRESENCE

Nothing in §J3 reads a runner's text. Every row is `/bin/sh run_all.sh` and the number the
kernel returned.

**The forced failure is not a stub.** The target instrument runs in full, prints all of its real
output, and is then made to report failure by an `atexit` hook injected through `PYTHONPATH`
into the process whose `sys.argv[0]` is that target. Its bytes and its line numbers are never
touched. (`atexit` rather than an appended `raise SystemExit(1)`: two of these targets end in
`sys.exit(main())`, where an appended forcer never runs at all — see `OUTCOMES.md` D1.)

Each row is a **conjunction** of three things, because any one alone passes rows that are wrong:

* the runner's exit code is non-zero;
* the forced failure really happened **in the target** (its marker is in the step's own
  transcript);
* **no later step ran** — measured by stamping every later transcript to epoch 0 and
  re-reading its mtime *before* any restore.

### 4.1 The seventeen fixed runners — RED

The first scored step of each runner is forced to fail. Every column must hold.

```
  runner                                    forced target          exit  ran    stdout   later ran  verdict
  code/branching_audit_2060/run_all.sh       ./b0_repro.sh          1     yes    yes      none       caught
  code/branching_locate_db09/run_all.sh      selftestdb09.py        1     yes    yes      none       caught
  code/face_geometry/run_all.sh              controls.py            1     yes    yes      none       caught
  code/face_geometry_audit_1c80/run_all.sh   a1_gates.py            1     yes    yes      none       caught
  code/face_geometry_audit_6653/run_all.sh   verify_claims.py       1     yes    yes      none       caught
  code/face_geometry_audit_e720/run_all.sh   verify_landing_claims.py 1   yes    yes      none       caught
  code/face_geometry_landing_7d5a/run_all.sh verify_landing.py      1     yes    yes      none       caught
  code/face_geometry_landing_da45/run_all.sh verify_landing.py      1     yes    yes      none       caught
  code/landscape_audit_d673/run_all.sh       audit_populations.py   1     yes    yes      none       caught
  code/species_7d75/run_all.sh               selftest.py            1     yes    yes      none       caught
  code/species_audit_73df/run_all.sh         selftest73df.py        1     yes    yes      none       caught
  code/species_audit_7dd3/run_all.sh         selftest7dd3.py        1     yes    yes      none       caught
  code/species_audit_a61f/run_all.sh         selftesta61f.py        1     yes    yes      none       caught
  code/species_extent_audit_6cb9/run_all.sh  selftest6cb9.py        1     yes    yes      none       caught
  code/species_extent_d633/run_all.sh        selftestd633.py        1     yes    yes      none       caught
  code/species_remainder_f8fa/run_all.sh     selftestf8fa.py        1     yes    yes      none       caught
  code/species_repair_a4ef/run_all.sh        selftesta4ef.py        1     yes    yes      none       caught
```

**17 of 17 exit non-zero, with the forced failure verified to have happened in the target and
no later step having run.** `code/species_audit_7dd3/` is worth singling out: the sweep found
it had a *different* defect — no `set -e` at all, so it exited 0 unconditionally and
de-pipelining alone would not have fixed it. It catches here, so that repair works too.

### 4.2 The same seventeen, unmodified — GREEN

**17 of 17 exit 0**, from 4.1 s (`species_remainder_f8fa`) to 199.0 s
(`branching_audit_2060`); 1108 s of wall clock for both directions. Without this column
"always exits non-zero" would have scored a perfect 4.1.

### 4.3 The negative control — the two runners the population excluded

Same instrument, same forced failure, same reading of the runner's own exit code:

```
  code/face_geometry_audit_f1b2/run_audit.sh audit_scoring.py  0  ran: yes  stdout: yes
        later ran: out_gates.txt,out_theorem.txt,out_injections.txt,out_nmax.txt   *** SWALLOWED ***
  code/face_geometry_audit_fcf1/run_audit.sh audit_nc4.py      0  ran: yes  stdout: yes
        later ran: out_extra.txt,out_gauge.txt                                     *** SWALLOWED ***
```

**2 of 2.** A `set -e` runner in this repository prints `*** MG-05EB FORCED FAILURE ***` from
its own step, runs every subsequent step anyway, and exits **0** — after the sweep. That is
not an argument that the population should have been wider; it is the defect, executing.

---

## 5. DID IT FIX RUNNERS THAT DID NOT NEED FIXING, AND DID IT SAY SO?

**All 34 pipeline sites are repaired: 34 redirects with an explicit `||` guard, 0 plain
redirects, 0 sites with no redirect at all.** So the repair is uniform, and the sweep measured
that only 21 of 34 were affected.

**A uniform fix is not wrong. An unstated one is — and this one is stated.** §J4b checks five
specific sentences and finds five:

| | where |
|---|---|
| the 13 unaffected are named individually | `out_k2_consume.txt` §K2c |
| *"Repaired anyway"* appears beside them | `out_k2_consume.txt` |
| the 21-of-34 split is in the reader-facing document | `docs/OneThird-RunnerExit-ArcWideSweep.md:92` |
| the document says the unaffected sites were repaired anyway | *"Repaired anyway, and listed so that `all 34 carried a verdict` is not asserted when it is false"* |
| the commit message carries the distinction | `NOT UNIFORM` |

**On item 4 the sweep is clean.** This section is written so that it *can* come back clean,
and it does; a scope audit that can only report faults is not measuring anything.

*A probe of mine was wrong here and the correction is on the record.* Its first version
searched the document for the literal string `"34 of 34"`, did not find it, and scored the
sweep as not having stated its uniform repair — while the document says it in different words.
Looking for a form of words rather than for the claim is the same error as counting a header
comment as a pipeline. Prediction Q20 was right and my instrument was wrong; `OUTCOMES.md` D3.

---

## 6. THE FLOOR ITEM — audited because no list named it

`tee` writes the step's output to the file **and to the runner's stdout**, on the failing path
as much as the passing one. A redirect writes only the file. The sweep measured that the
committed **file** does not move (`K3d`, `K3f`) and named the streaming cost in its README.
Nobody measured the other half: **on the failing path, does the diagnosis still reach the
runner's stdout?** It does only where the `||` guard `cat`s the transcript.

§J4c is that census, per site: **34 of 34 guards `cat`**. And §J3a measures it live rather
than from the text — the `stdout` column is **yes at 17 of 17**, on runs where the step really
did fail.

**The check comes back clean.** It is reported because being true by construction at 34 of 34
is a row, and an assumption is not. Had even one guard omitted the `cat`, the repair would have
traded a swallowed status for a swallowed diagnosis, and *"no committed transcript moves"*
would have been true and would not have covered it.

---

## 7. THE GENERAL FORM, APPLIED TO THIS AUDIT

This deliverable is a script that reports on scripts, so it can discard its own verdict exactly
as its subjects did. What was checked, in the artifact itself:

1. **`code/runner_exit_audit_05eb/run_all.sh` contains no pipeline of any kind** — not `| tee`,
   not `| grep`. That is the branch which *cannot* exhibit the defect, and the reason is
   structural: a pipeline is the only POSIX-sh construct whose exit status belongs to a command
   other than the one being scored. §S6 measures it on the runner's own bytes.
2. Every subprocess is a **list argv with no `shell=True`**. §S7 checks it by **parsing** each
   file, not grepping it — a grep for `shell=True` scores a docstring that promises not to use
   it, which is the header-comment error one level down, and it scored four of my own files BAD
   before it was fixed.
3. `returncode` is read on **every** path including the timeout path, which prints `-`, never `0`.
4. Every `J3` verdict is a **conjunction** — exit code, the forced failure having really
   happened in the target, and no later step having run. "Did the diagnosis reach stdout" is a
   **separate** column on purpose: merging it into the verdict would have hidden §6 entirely.
5. `later ran` is measured by stamping every later transcript to epoch 0 and re-reading its
   mtime **before any restore**. The first draft read it afterwards, and `git checkout -- .`
   rewrites tracked files unconditionally, so every runner looked as though all its later steps
   had run.
6. **The parser is written from scratch.** Its agreement with `libc2b3.py` on 64 / 23 / 17 / 6
   is therefore evidence; its disagreement on `pipefail` is §2.1.
7. **Both revisions, and the pin is the finding.** `J1` reports at `bee07a1` and on disk; `J2a`
   scans at both because a scan pinned to one revision is a statement about that revision.
8. **The forced failure is not a stub**, so `J3` measures real instruments reporting real
   non-zero statuses through real runners.
9. **Limits stated rather than omitted.** `J2a` finds consumers syntactically; a caller that
   assembles a runner path at runtime is invisible to it, exactly as it was to `K2a`. `J3`
   forces the batteries to fail and therefore does **not** re-prove that they pass — `J3b`
   shows only that each runner is 0 unmodified, on this machine, at HEAD.
10. **My own misses are kept as written.** Two of 23 predictions missed, both because I
    inherited the sweep's answer instead of measuring it, and the whole of §2.1 is downstream
    of that. Three defects in this instrument are written up in `OUTCOMES.md` rather than
    smoothed away.

---

## WHAT THIS AUDIT DOES NOT CLAIM

* It does not re-prove the batteries. `J3` forces them to fail on purpose.
* It does not settle the R3 claims at every intermediate commit — neither does the sweep, and
  the sweep says so.
* It does not re-litigate the R1/R2/R3 routing; it adopts it, because it is right.
* `J2a`'s consumer rule is syntactic and wider than `K2a`'s, but wider is not total.
