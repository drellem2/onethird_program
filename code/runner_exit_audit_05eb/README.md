# `code/runner_exit_audit_05eb` — independent audit of the arc-wide `| tee` sweep

`sh run_all.sh` — about 25 minutes, pure Python 3, no dependencies, no network.

**Target:** `52aeaf4` (mg-c2b3), *"THE ARC-WIDE `| tee` SWEEP, AND WHICH PAST GREENS
DEPENDED ON A SWALLOWED EXIT CODE"*, and its tree `code/runner_exit_c2b3/`.
Pre-filed in the same action as its parent; no coordination.

## What is here

| file | what it answers |
|---|---|
| `PREDICTIONS.md` | every exit code and count, predicted before the instrument existed; misses kept as written |
| `selftest05eb.py` | the classifier, driven in **both senses** at every rule, plus this tree's own runner checked by its own rules |
| `j1_census.py` | the census re-derived from a parser written from scratch, over **every `*.sh`**, not every file named `run_all.sh` |
| `j2_retro.py` | the retroactive half, re-asked from a **mechanical** consumer scan instead of a hand-written list |
| `j3_control.py` | the positive control: each fixed runner's first scored step made to fail, and the **runner's** exit code read — plus the same instrument on the runners the sweep never saw |
| `j4_scope.py` | did it fix runners that did not need fixing, and did it say so |
| `OUTCOMES.md` | findings, prediction misses, and the two defects in this instrument that were caught and are recorded rather than smoothed away |

## Verdict in one line

**The sweep's forward repair is sound and its retroactive method is right — and
its population is a filename, its census is wrong about the one number it says it
confirmed, and one past claim that reads two affected runners' exit codes is
outside its enumeration because the enumeration was pinned to a revision that
predates the claim.**

## The four findings

**F1 — the population is a naming convention, and two runners fall outside it.**
The sweep's census is over files named `run_all.sh`. `code/face_geometry_audit_f1b2/run_audit.sh`
and `code/face_geometry_audit_fcf1/run_audit.sh` are `#!/bin/sh`, set `set -e`, and
carry **8 real `| tee` pipelines between them**. They are unrepaired at HEAD.
Over shell runners rather than over one filename, the sweep is **17 of 19 files
and 34 of 42 pipelines**. `J3c` forces a step in each to fail and reads the
runner's exit code: **the defect is alive in this repository after the sweep**.

**F2 — the one census number the sweep says it confirmed is the one it got wrong.**
The ticket said `pipefail: 1`. `out_k1_census.txt` prints `ticket 1 / re-derived 0
/ DIFFERS`. Four reader-facing artifacts — the README, `OUTCOMES.md`, the
published document, and `k1_census.py`'s own docstring — say **1, "confirmed
exactly"**, and the document even names the right file. The ticket was right;
`libc2b3.PIPEFAIL_RE` is `^\s*set\s+-o\s+pipefail`, and the one runner that sets
the option writes `set -euo pipefail`. The same blind spot produced *"The shebang
is `#!/bin/sh` on all 64 runners (measured)"*, which is false at **5 of 64**.

> **The transcript this finding cites is a HISTORICAL RECORD and it will not
> reproduce at HEAD.** `libc2b3.PIPEFAIL_RE` was repaired by **mg-7522** at
> `1ee1f1b`; re-run `k1_census.py` today and the same row re-derives as `1` and
> the verdict is the opposite of the one quoted above. That is the repair
> landing, not this finding being wrong. `out_k1_census.txt` was deliberately
> **not** regenerated — by mg-7522, by mg-70c7 at `d456f58`, and again by
> mg-56dc — because regenerating it would destroy the record this paragraph
> cites; the file now carries the same note at its head, and the corrected
> reading is published in `code/runner_exit_repair_7522/out_s3_figure.txt`.
> *(Added by mg-56dc: preserving evidence without labelling it converts a
> citation into a false witness.)*

**F3 — a claim the enumeration did not consider, and it is R3.**
`code/species_depth_audit_4700/q2_wiring.py` executes three species `run_all.sh`
twenty-one times and scores them on `rc == 0` / `rc != 0` at **8 sites**, and two
of the three trees were affected. Its committed transcript contains

```
code/species_repair_a4ef      exit 0   printed *** FAILED ***: yes  SWALLOWED
code/species_remainder_f8fa   exit 0   printed *** FAILED ***: yes  SWALLOWED
```

which is a claim read off an affected runner's exit code and nothing else. It is
not among the nine. **It could not have been:** the sweep's caller scan runs at
the pinned `bee07a1`, and that tree landed in `5c16f5c`, after the pin. Pinning is
correct for the byte-comparison — anchoring to HEAD would compare the repaired
tree with itself, which is mg-821e's own finding — and wrong for a caller scan.
`J2c` re-runs the probe at HEAD: **both rows flip**, measured, not argued.

**F4 — on scope, the sweep is clean, and this audit says so with a measurement.**
It names the 13 unaffected pipelines individually, states which clause of the
conjunction each fails, writes *"Repaired anyway"* beside them, and carries `NOT
UNIFORM` in the commit message. `J4b` checks five specific sentences and finds
five. Item 4 of the assignment is answered in the sweep's favour.

## The floor item — audited because no list named it

`tee` wrote the failing step's diagnosis to the runner's **stdout**. A redirect
does not. The sweep measured that the committed **file** does not move (`K3d`,
`K3f`); nothing measured the terminal. `J4c` is that census, per site, and `J3a`
measures it live on all 17 runners.

## The general form, applied to this tree

This deliverable is a script that reports on scripts, so it can discard its own
verdict exactly as its subjects did. Enumerated, with the reason:

1. **This runner contains no pipeline of any kind** — not `| tee`, not `| grep`.
   `selftest05eb.py` §S6 measures it on the runner's own bytes and fails if an
   edit adds one.
2. Every subprocess is a **list argv with no `shell=True`**; §S7 checks every
   `.py` here for `shell=True` and `os.system(`.
3. `returncode` is read on **every** path including the timeout path, which
   prints `-` and never `0`.
4. Every `J3` verdict is a **conjunction** of exit code, the forced failure
   having really happened in the target, and no later step having run. `J3a`
   reports "did it reach stdout" as a **separate** column, because merging it
   with "did it run" would have hidden `J4c`.
5. `later ran` is measured by stamping every later transcript to epoch 0 and
   re-reading its mtime **before any restore** — `git checkout -- .` rewrites
   files unconditionally and the first draft of `J3` read it afterwards and
   reported eight false positives.
6. `J1` compares against the **pinned** `bee07a1` and on disk, and reports both.
   `J2a` runs at both revisions **because the pin is the finding**.
7. **The forced failure is not a stub.** The target runs in full and is made to
   report failure by an `atexit` hook injected through `PYTHONPATH`, so its bytes
   and line numbers are untouched. The first draft appended `raise SystemExit(1)`,
   which never fires on a script ending in `sys.exit(main())` — two of these do,
   and it printed `*** NOT CAUGHT ***` against two sound runners. Recorded in
   `OUTCOMES.md`, not quietly fixed.
8. **Limits stated rather than omitted.** `J2a` finds consumers by a syntactic
   rule; a caller that assembles a runner path at runtime is invisible to it,
   exactly as it was to `K2a`. `J3` forces the batteries to fail and therefore
   does *not* re-prove that they pass — `J3b` shows only that each runner is 0
   unmodified on this machine at HEAD.
