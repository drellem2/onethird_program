# `code/runner_exit_c2b3` — the arc-wide `| tee` / exit-status sweep (mg-c2b3)

`sh run_all.sh` — about 4 minutes, pure Python 3, no dependencies, no network.

## The defect in one line

In POSIX sh a pipeline's exit status is its **last** command's. `cmd | tee out`
therefore reports `tee`'s status, which is 0 whenever tee could write the file.
`set -e` sees that 0. **A runner can print six failures and exit 0.**

## What this tree contains

| file | what it answers |
|---|---|
| `selftestc2b3.py` | the classifier, driven in **both senses** at every rule, plus this tree's own runner checked by its own rules |
| `k1_census.py` | the census, re-derived at `bee07a1` and on disk. Ticket said 63 / 23 / 1 |
| `k2_consume.py` | per runner and per line: **is the status actually consumed**, and by what |
| `k3_retro.py` | **which past "clean run" claims depended on an affected runner's exit code**, and what settles each |
| `k4_control.py` | the positive control: a step is made to fail and the **runner's** exit code is read, on the pre-repair text and on the post-repair text |

## The numbers

| | ticket | re-derived |
|---|---|---|
| `run_all.sh` in the tree | 63 | **64** — `code/hodge_leverage_repair_8eca/` landed in `bee07a1`, after the ticket |
| matching the bare grep `\| *tee` | 23 | **23** — confirmed exactly |
| containing a **real `\| tee` pipeline** | — | **17** |
| setting `pipefail` | 1 | **1** — confirmed exactly |

**The 23 and the 17 differ by six, and the six are the repaired trees.** Their
header comments say *"NOT `| tee`"* and a bare grep counts the sentence.
Counted as pipelines, the trees that already carry the fix are indistinguishable
from the ones that do not — which is the confusion this ticket exists to end.

## Per-runner, not uniform — which of the 17 were actually affected

A pipeline is only dangerous where something consumes the status. Three
consumers are measured separately (`set -e` in the runner; an external caller;
the target's own ability to fail by design) and a line is **AFFECTED** only when
the conjunction holds. **21 of 34 pipelines, across 15 of 17 runners.** The
other 13 are named in `K2c` with which clause of the conjunction fails, and one
runner — `code/species_audit_7dd3/` — has a *different* defect and is written up
separately in `K2d`: it has no `set -e` at all, so it exited 0 unconditionally,
and de-pipelining alone would not have fixed it.

## The retroactive answer

**Three claims were at risk, and all three live in one file.** The arc reads its
results from committed transcripts and byte-comparisons almost everywhere, and
from an exit status in exactly one place: `code/species_sites_821e/p3_wiring.py`,
which scores three species runners on `code == 0` and `code != 0`. That is why
the exposure is three claims and not thirty — and also why the defect survived:
nothing depended on the status, so nothing noticed it was gone, until mg-821e
wrote the one instrument that did depend on it and found its own runner green
with six failures on screen.

Everything settled **SAFE** is marked safe with its reason rather than left
ambiguous — including the byte-comparison cases the ticket names, where the
bytes never travel through the pipeline at all.

## The mechanism, and why

```sh
python3 x.py > out_x.txt || {
    cat out_x.txt; echo "x.py FAILED"; exit 1; }
cat out_x.txt
```

**Not `set -o pipefail`:** the shebang is `#!/bin/sh`, which on Linux is dash.
`set -o pipefail` there prints *Illegal option* and returns non-zero, so under
`set -e` it would abort the runner at the line meant to make it safer — working
on macOS and failing elsewhere, the worst possible split for a control.
`${PIPESTATUS[0]}` is bash-only for the same reason.

**This one:** it is POSIX; it is what mg-e1d0 and mg-821e already used here, so
the arc now has one idiom instead of three; and it writes the transcript with
the same bytes `tee` wrote, so no committed `out_*.txt` moves and no
byte-comparison in the arc is disturbed. `K3d` measures that rather than
asserting it.

**What it costs:** `tee` streams and a redirect does not. On the long runners
the transcript now appears at the end of each step instead of live.

## The general form, applied to this tree

This deliverable is a script that reports on scripts, so it can discard its own
verdict exactly as its subjects did. What was checked, in the artifact itself:

1. **This runner contains no pipeline at all** — not one `|` outside a comment
   on a command line. That is the branch that *cannot* exhibit the defect, and
   the reason is structural: a pipeline is the only POSIX-sh construct whose
   exit status belongs to a command other than the one being scored.
   `selftestc2b3.py` §H measures it on the runner's bytes.
2. Every subprocess in `k3_retro.py` and `k4_control.py` uses a **list argv with
   no `shell=True`**, so `returncode` is the target's own status.
3. `returncode` is read on **every** path including the timeout path, where it
   prints as `-` rather than as 0.
4. Every K4 verdict is a **conjunction of exit code and reach** — scoring only
   one of them would reproduce the defect while testing for it. `K4b` shows
   **eight** sites where the exit code alone would have lied.
5. Both K3 and K4 compare against the **pinned** `bee07a1`, not `HEAD`. Anchored
   to HEAD they would compare the repaired tree with itself (mg-821e, 41ac5d4).
6. **What is not mechanical is named**: two rows of `K2a`'s caller table are
   hand-added, because a line-local scan cannot resolve a path built from a loop
   variable or from a `cp -R` two lines earlier. Both are in the AFFECTED
   column; dropping them silently would have reported one caller instead of
   three.
7. **The byte-identity is measured, not deduced**: `K3f` actually runs a
   repaired runner (`code/face_geometry/`, the subject of claim C6) and checks
   its transcripts did not move — and names four transcripts elsewhere that do
   *not* regenerate, with the measurement showing that drift reproduces on a
   pristine `bee07a1` checkout and is therefore not this repair's.
8. **Limits stated rather than omitted**: K3b settles the at-risk claims at HEAD
   and at the revisions those claims name — it cannot re-run every target at
   every intermediate commit, and does not claim to. K4 stubs the batteries, so
   it proves the runners propagate status and does *not* re-prove the batteries
   pass; K3b does that.
