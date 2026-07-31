# The arc-wide `| tee` sweep — a runner that prints failures and exits 0

**Ticket:** mg-c2b3.
**Code:** `code/runner_exit_c2b3/` (`run_all.sh`, ~4 min), plus 17 repaired
`run_all.sh` across the arc.
**Predecessors:** mg-f922 / mg-e1d0 (found and fixed it once), mg-821e /
`41ac5d4` (found and fixed it again, on its own runner, and said explicitly that
the rest of the arc was out of its scope).

---

## 0. The defect, and why it is the kind that hides

In POSIX `sh`, a pipeline's exit status is the status of its **last** command.

```sh
python3 selftest.py | tee out_selftest.txt     # status is TEE's, always 0
```

`set -e` sees that 0. So the self-test prints six failures, exits 1, and the
runner carries on to the end and exits 0.

Printing a failure and reporting a failure are two different things, and a pipe
separates them silently. That is the whole defect, and it is invisible in
exactly the situation you care about: as long as everything passes, a runner
with the defect and a runner without it are the same runner.

mg-821e hit it the only way it can be hit — by writing an instrument that
*depended* on the exit code, watching its own self-test go red, and watching the
run finish green.

---

## 1. The census, re-derived

The ticket's numbers were 63 / 23 / 1 and asked to be re-derived rather than
trusted. They are, at `bee07a1` (the revision the ticket cites, pinned — not
`HEAD`, which after this repair would compare the tree with itself):

| | ticket | re-derived | |
|---|---|---|---|
| `run_all.sh` in the tree | 63 | **64** | `code/hodge_leverage_repair_8eca/` landed in `bee07a1`, after the ticket was written. It has no `\| tee`. |
| matching the bare grep `\| *tee` | 23 | **23** | confirmed exactly |
| containing a real `\| tee` **pipeline** | — | **17** | the ticket did not separate this |
| setting `pipefail` | 1 | **1** | confirmed exactly — `code/state_restructure_34bf/` |

### The six the grep counted and the parser did not

**Every one of them is a header comment saying the runner does *not* use
`| tee`.** They are the trees that already carry the repair:

```
code/face_geometry_audit_c4c8/run_all.sh    :34   # NOT `python3 x.py | tee out.txt`, and that is deliberate…
code/face_geometry_audit_d0e2/run_all.sh    :20   # NOT `python3 x.py | tee out.txt`.  A pipeline's exit status…
code/face_geometry_audit_e7bc/run_all.sh    :31   # NOT `python3 x.py | tee out.txt`, and that is deliberate…
code/face_geometry_instr_5f9a/run_all.sh    :48   # NOT `python3 x.py | tee out.txt`, and that is deliberate…
code/hodge_leverage_audit_f922/run_all.sh   :42   # NOT `python3 audit_repair.py | tee out_audit.txt`…
code/species_sites_821e/run_all.sh          :28   # NOT `| tee`: in a pipeline `set -e` sees the exit status of `tee`…
```

A census that cannot tell a pipeline from a sentence about a pipeline reports
the repaired trees as broken. `libc2b3.tee_pipelines()` strips comments and
quoted strings first, and `selftestc2b3.py` drives that rule in both senses —
including the check that the bare grep and the parser must **disagree** on a
comment, so the two cannot silently converge.

A seventh tree, `code/hodge_leverage_landing_e1d0/`, is not in the 23 at all,
because its repair removed the word entirely: `> out_verify.txt || status=$?`.
Its header says *"It used to pipe into `tee`, so under `set -e` the pipeline's
status was tee's and the runner exited 0."*

**So the defect was found and fixed twice, one runner at a time, before this
sweep. Neither generalised; both said so. That is why the arc-wide count was
still 17.**

---

## 2. Not uniform — which of the 17 were actually affected

The ticket is explicit that `| tee` is only dangerous where something consumes
the status. Three consumers, measured separately:

- **C1** — `set -e` inside the runner. 16 of 17 have it.
- **C2** — an external caller that reads the runner's status. Two exist.
- **C3** — the target's own **designed** failure route (`sys.exit(non-zero)`,
  `assert`, an explicit `raise`; for a `.sh` target, `set -e`). Measured, not
  assumed — `assert` was the answer for several self-tests, and a rule that only
  knew `sys.exit` would have called them incapable of failing.

A line is **AFFECTED** when `(C1 or C2) and C3`.

> **21 of 34 pipelines are AFFECTED, across 15 of 17 runners.**

The other 13 are listed by name in `K2c` with which clause fails:

- **12 fail C3** — the target has no designed failure route, so the pipeline
  discarded no *verdict*. It still discarded a *crash*: an `ImportError` or a
  missing input exits 1 and the runner would not have seen it. Repaired anyway,
  and listed so that "all 34 carried a verdict" is not asserted when it is
  false.
- **1 fails C1+C2** — `code/species_audit_7dd3/`, and it is a different defect.

### The one that needed more than de-pipelining

`code/species_audit_7dd3/run_all.sh` has **no `set -e`**, and every step after
the self-test ends in `|| true`. Its own header says *"The self-test is the only
file whose exit code is a statement about this instrument rather than about the
repair."*

It was not. With no `set -e` the runner's status is its last command's, and the
last command is an `echo` — **the runner exited 0 unconditionally, with or
without the pipeline.** Removing the pipe alone would not have fixed it. The
repair is an explicit `|| { …; exit 1; }` guard on the self-test, which is what
makes the header true; the `|| true` on `d1`–`d6` is deliberate and untouched.

---

## 3. The retroactive question — which past "clean run" claims depended on this?

This is the load-bearing item, and the answer has a shape worth stating before
the list.

**A past claim depended on an affected runner's exit code only if it was read
*off the status*.** Three routes, and only the third is exposed:

- **R1 — a committed byte-comparison.** `diff` of a regenerated transcript
  against the committed one. The bytes never travel through the pipeline:
  `tee out` and `> out` write the same stream. **SAFE**, and marked so
  explicitly.
- **R2 — the printed output.** A `TOTAL BAD:` line, a headline grep, a
  transcript a reader reads. Printed and committed whatever the status was.
  **SAFE.**
- **R3 — the exit status.** `code == 0`, `code != 0`, `set -e` aborting.
  **AT RISK.**

Nine claims were enumerated. **Six are SAFE, three are AT RISK — and all three
live in one file.**

| | site | route | disposition |
|---|---|---|---|
| **C1** | `species_sites_821e/p3_wiring.py:219` (P3b) | R3 | **AT RISK** — settled |
| **C2** | `species_sites_821e/p3_wiring.py:255` (P3c `caught`) | R3 | SAFE by mechanism, and measured |
| **C3** | `species_sites_821e/p3_wiring.py:256` (P3c `missed`) | R3 | **AT RISK** — settled |
| C4 | `branching_audit_2060/b0_repro.sh:10-23` | R1 | SAFE — the five `diff -q` calls |
| C5 | `…ExtentRepair-IndependentAudit.md:254` | R2 | SAFE — the committed transcript |
| C6 | `…StateLanding2-IndependentAudit.md:314` | R1 | SAFE — the verdict is `git status` |
| C7 | `OneThird-Landscape-Where-This-Lives.md:363` | R2 | SAFE — a reproduction claim about output |
| C8 | `hodge_leverage_audit_f922/audit_repair.py:500` | R3 | SAFE — this is the precedent, not an exposure |
| C9 | `docs/landing-mg-1c80-instrumented-predicate.md:175` | R2 | SAFE — and the claim is **true**, checked |

### Why the exposure is three and not thirty

**The arc reads its results from committed transcripts and byte-comparisons
almost everywhere, and from an exit status in exactly one file.** That is the
answer, and it is also the explanation for how the defect survived so long:
nothing depended on the status, so nothing noticed it was gone — until mg-821e
wrote the one instrument that did.

### C1 and C3, settled

`p3_wiring.py` scores three species runners:

```python
ok     = (code == 0 and present and code_u == 0 and gone)     # P3b
caught = (code_w != 0 and "STANDING UN-STRUCK" in out_w)      # P3c
missed = (code_u == 0)                                        # P3c
```

Two of its three trees — `species_repair_a4ef` and `species_remainder_f8fa` —
were affected, so `code == 0` was true whether or not their self-tests passed.
`code_u == 0` is worse: it is the *historical failure being reproduced*, and an
affected runner exits 0 either because nothing was detected or because
something was and the pipeline ate it. The row cannot tell those apart.

The substantive half of P3b — `present` and `gone`, the check's own output
appearing in stdout and disappearing when the wiring is deleted — is **R2 and
stands untouched**. Only the `code == 0` conjuncts were unsupported.

**Settlement:** the pipeline threw away exactly one number, so go and get it.
`K3b` runs every one of the 34 tee'd targets directly, with nothing in the way,
and reads its status. Result in the committed transcript.

**What that does not cover, said in the table and not in a footnote:** it
measures the tree as it stands. A target that exits 0 today could have exited 1
at an intermediate commit. Where a claim names a revision, the revision is used;
where it does not, the row says so.

### C2, the one claim that needed a *non-zero* exit — and why it is safe

`caught = (code_w != 0 and …)` is the one place in the arc where a runner's
non-zero exit is the evidence. A swallowed status would have made it **fail**,
not pass. It passed.

The non-zero comes from the cross-section block at `run_all.sh:25-29`:

```sh
E2OUT=$(python3 ../species_extent_d633/e2_crosssection.py) || {
    echo "$E2OUT" | grep 'STANDING UN-STRUCK' || true
    echo "E2 CROSS-SECTION FAILED -- a struck claim stands un-struck elsewhere"
    exit 1
}
```

A command substitution and an explicit guard, **containing no pipeline**. The
tee'd self-test sits above it and could not have produced the exit. `K3c`
locates that block at both revisions and checks it for a pipeline, so this is
not left as an argument from reading.

### C8 — who already knew

mg-f922's `audit_repair.py:500` recorded the defect and *measured* it:
*"verifier exits 1, its runner exits 0 — the runner cannot report the failure."*
That runner (`hodge_leverage_landing_e1d0`) was repaired, so f922's `record(…)`
now evaluates **false** against the tree: a frozen audit whose finding was
fixed. Nothing here touches e1d0 or f922. The row is in the table because item 3
asks which past claims the defect touched, and this one is the answer to *who
knew*.

---

## 4. The fix, and why this mechanism

```sh
python3 x.py > out_x.txt || {
    cat out_x.txt; echo "x.py FAILED"; exit 1; }
cat out_x.txt
```

**Not `set -o pipefail`.** The shebang is `#!/bin/sh` on all 64 runners
(measured). On Linux that is normally dash, which has no `pipefail`:
`set -o pipefail` there writes *"Illegal option -o pipefail"* and returns
non-zero, and under `set -e` that **aborts the runner at the line that was
supposed to make it safer**. It would work on macOS, where `/bin/sh` is bash in
POSIX mode, and fail on the other half of the world — the worst possible split
for a control.

**Not `${PIPESTATUS[0]}`.** Bash-only for the same reason, and it needs a
separate `if` after every pipeline anyway.

**This one.** POSIX; already used by mg-e1d0 and mg-821e in this repository, so
the arc now has **one** idiom instead of three; and it writes the transcript with
the same bytes `tee` wrote, so no committed `out_*.txt` moves and no
byte-comparison in the arc is disturbed. `K3d` measures that rather than
asserting it.

**What it costs, stated because it is a real regression.** `tee` streams; a
redirect does not. On the long runners the transcript appears at the end of each
step instead of live. Correctness over progress bars — and the alternative that
keeps streaming is `pipefail`, which is not available here.

**A note on the notes.** Each repaired runner carries a comment explaining the
change, and each is deliberately worded *without* writing the old pipeline out.
Seventeen new comments containing the literal `| tee` would have raised the bare
grep's count from 23 to 40 and left the next reader with a worse version of the
problem this ticket started from.

---

## 5. The positive control — the defect reproduced, then repaired, at every site

The ticket asks for a positive control per fixed runner: make its self-test fail
on purpose and confirm the **runner** exits non-zero.

`K4` runs a two-by-two at every one of the 34 sites. Each runner is copied to a
temp directory with every script it launches replaced by a stub that prints a
marker and exits with a chosen code:

| runner text | target | expected exit | expected reach |
|---|---|---|---|
| pre-repair | exits 0 | 0 | reaches the end (baseline) |
| **pre-repair** | **exits 1** | **0 ← the defect** | **reaches the end** |
| post-repair | exits 0 | 0 | reaches the end |
| **post-repair** | **exits 1** | **non-zero ← the fix** | **stops at the target** |

Row 2 is the point: **the defect is reproduced on the real runner text, at every
site, rather than argued from the POSIX spec.** A control that only ran rows 3
and 4 would show a working runner and would never show it had been broken.

### Why every verdict is a conjunction of exit code *and* reach

Because the defect under repair *is* the separation of "printed a failure" from
"exited non-zero". An instrument that scored only one of them would be
reproducing the defect while testing for it.

It is not hypothetical: on the pre-repair text, three runners
(`species_7d75`, `species_audit_73df`, `species_audit_a61f`) exit **1** with a
failing step — not because they caught anything, but because they end with a
`grep -h "TOTAL BAD" out_*.txt` that finds nothing in a stubbed transcript. An
exit-code-only control would have called those three healthy. `K4b` prints them
by name.

`K4c` is the control on the control: it checks that the baseline actually
reached the stubs (a harness whose stubs never ran would score every row
"fixed"), and that with **nothing** failing the pre- and post-repair runners
reach identically — so the repair changed behaviour in exactly one circumstance.

### What K4 does not establish

The stubs replace the batteries, so K4 proves the runners propagate status and
does **not** re-prove that the batteries pass. `K3b` does that, for real, once
per target. Running the real batteries four times at 34 sites is roughly forty
hours and would measure the thing that did not change.

---

## 6. The general form, applied to this deliverable

> *"This deliverable is an artifact of the same kind as the defect it repairs:
> it is a script that reports on scripts, and its own reporting can discard its
> own verdict."*

What was checked, in the artifact itself:

1. **`code/runner_exit_c2b3/run_all.sh` contains no pipeline at all** — not one
   `|` outside a comment on a command line. This is the branch that *cannot*
   exhibit the defect, and the reason is structural rather than a promise: a
   pipeline is the only POSIX-sh construct whose exit status belongs to a
   command other than the one being scored, so with none present there is
   nothing for a verdict to hide behind. `selftestc2b3.py` §H measures that on
   the runner's bytes — a stronger row than "`set -e` is set", which is exactly
   what the 17 also had.
2. Every subprocess in `k3_retro.py` and `k4_control.py` uses a **list argv with
   no `shell=True`** — no shell, no pipeline, so `returncode` is the target's
   own status.
3. `returncode` is **read on every path**, including the timeout path, where it
   is `None` and prints as `-` rather than as `0`. A timeout rendered as 0 would
   be this defect wearing a different hat.
4. `git ls-tree` in `K2a` is deliberately **not** `check=True`, because its
   output is then *used* — a failure surfaces as an empty caller table, which is
   visible, rather than as a pass.
5. `K3b` snapshots `git status --porcelain` **before and after**, because
   several targets mutate the worktree and restore it, and a restore that
   silently failed would corrupt `K3d`'s answer.
6. Both `K3` and `K4` compare against the **pinned `bee07a1`**, not `HEAD`.
   Anchored to HEAD, K4's two arms would be the same repaired text and every row
   would pass trivially — mg-821e's finding (`41ac5d4`), applied to this file.
7. **What is not mechanical is named.** Two rows of `K2a`'s caller table are
   hand-added: `b0_repro.sh:10` runs `./run_all.sh` in a directory whose
   identity comes from a `cp -R` two lines earlier, and `p3_wiring.py:214` runs
   `run_runner(t)` over a loop variable. A line-local scan resolves neither.
   Both are in the AFFECTED column; dropping them silently would have reported
   one caller instead of three and made this ticket look smaller than it is.
8. **The limits are stated, because a stated reason is checkable and an omission
   is not.** `K3b` settles the at-risk claims at HEAD and at the revisions the
   claims name; it cannot re-run every target at every intermediate commit and
   does not claim to. `K4` stubs the batteries and says so.

### One thing this sweep deliberately did not do

`code/face_geometry_audit_e720/attack_artifact_check.py` prints the sentence
*"The artifact is the child's stdout, which is what `| tee controls_output.txt`
writes"*, and that sentence is in its **committed transcript**, whose byte
identity that audit claims and defends. The clause naming `| tee` is now stale
as a description of `code/face_geometry/run_all.sh`. Editing it would break a
byte-identity claim that is itself a control. The arc's own convention for a
frozen audit transcript — see the STATUS block in
`code/face_geometry_audit_6653/run_all.sh` — is to record the staleness in prose
beside it rather than to regenerate it. That is what this paragraph is.

---

## 7. Scope

Confined to this arc's `run_all.sh` set, per the ticket. `pogo` and `macguffin`
have no `| tee` in any `.sh`; the four refinery gate scripts contain no
pipelines and all `set -e`. Nothing here touches `STATE.md`: this is a repair to
the runners' plumbing, not a change to any claim about the mathematics, and
inventing a STATE row for it would put a maintenance burden where there is no
claim to maintain.
