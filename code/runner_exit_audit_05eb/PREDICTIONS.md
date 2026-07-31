# mg-05eb — predictions, written before any of `j1`–`j4` was run

Independent audit of the `| tee` sweep (`52aeaf4`, mg-c2b3).  Every exit code and
every count below was written **before** the instrument existed.  Misses are kept
as written and scored in `OUTCOMES.md`.

Some of these are not brave, and saying which is part of the record: I had already
read `code/runner_exit_c2b3/out_k1_census.txt` and `out_k2_consume.txt` before
predicting, so any prediction that merely repeats a number the parent published is
marked **[inherited]**.  The ones marked **[mine]** are predictions the parent's
artifacts do not contain an answer to.

## J1 — the census, over a population I declare

| id | prediction | source |
|---|---|---|
| Q1 | `*.sh` at `bee07a1`, whole repo: **72** | [mine] |
| Q2 | of those, named `run_all.sh`: **64** | [inherited] |
| Q3 | `run_all.sh` at `bee07a1` matching the bare grep `\| *tee`: **23** | [inherited] |
| Q4 | `run_all.sh` at `bee07a1` with a REAL `\| tee` pipeline: **17** | [inherited] |
| Q5 | `*.sh` NOT named `run_all.sh`, at `bee07a1`, with a REAL `\| tee` pipeline: **2** | [mine] |
| Q6 | pipelines in those 2 files: **8** | [mine] |
| Q7 | the same two files, **on disk at HEAD, after the sweep**, still pipelined: **2 files / 8 pipelines** | [mine] |
| Q8 | `set -o pipefail` in any `*.sh` at `bee07a1`: **0** | [inherited] |
| Q9 | the ticket's `pipefail: 1` traces to a file that is **not** a `*.sh` runner | [mine] |

## J2 — the retroactive half

| id | prediction | source |
|---|---|---|
| Q10 | `code/species_depth_audit_4700/` exists at `bee07a1`: **NO** | [mine] |
| Q11 | files at HEAD that read the exit status of a `run_all.sh` execution: **≥ 4** (the parent's caller scan, pinned at `bee07a1`, found 3) | [mine] |
| Q12 | claims scored on an AFFECTED runner's exit status that the parent's 9-claim enumeration does not name: **≥ 2** | [mine] |
| Q13 | `code/species_depth_audit_4700/out_q2_wiring.txt`'s two `SWALLOWED` rows still reproduce at HEAD: **NO — they are falsified by the repair** | [mine] |
| Q14 | of the parent's 9 claim rows, sites whose quoted text is still findable at the named file: **9 of 9** | [mine] |

## J3 — the positive control, per fixed runner, both directions

| id | prediction | source |
|---|---|---|
| Q15 | FAIL direction (first repaired step forced to exit 1): **17 of 17 runners exit non-zero** | [mine] |
| Q16 | FAIL direction, reach: **17 of 17 stop at the forced step** (no later step runs) | [mine] |
| Q17 | PASS direction (runner unmodified): **17 of 17 exit 0** | [mine] |
| Q18 | NEGATIVE control — the two `run_audit.sh` runners of Q5, first step forced to exit 1: **2 of 2 exit 0**, i.e. the defect is still live in this repository after the sweep | [mine] |

## J4 — scope

| id | prediction | source |
|---|---|---|
| Q19 | of the 34 pipelines the parent enumerated, now redirect+guard on disk: **34 of 34** | [inherited] |
| Q20 | the sweep says in prose that it repaired the 13 UNAFFECTED sites anyway: **YES** | [mine] |
| Q21 | of the 34 repaired sites, guards that `cat` the transcript on failure (so the diagnosis still reaches the runner's stdout, as `tee` did): **34 of 34** | [mine] |

## Second round — written after J1a/J1c ran and Q8/Q9 MISSED, before J1e existed

Q8 and Q9 missed because I inherited the sweep's answer (`pipefail: 0`) instead of
measuring. The true count is **1**, and the file is `code/state_restructure_34bf/run_all.sh`
(`set -euo pipefail`). That opens two more questions, predicted here before J1e was
written, with the timing said out loud rather than smoothed over:

| id | prediction |
|---|---|
| Q22 | the sweep's doc says *"The shebang is `#!/bin/sh` on all 64 runners (measured)"*. Measured myself: **FALSE — at least one of the 64 is not `#!/bin/sh`** |
| Q23 | reader-facing artifacts of the sweep that assert `pipefail 1 / confirmed exactly / AGREES` while the instrument's own committed transcript prints `re-derived 0 ... DIFFERS`: **4** |

## The floor item — one thing no list in the assignment names

Two, declared here so they cannot be back-filled:

1. **Where the ticket's `pipefail: 1` came from.**  The parent re-derived it as `0`
   and marked it DIFFERS, and stopped there.  A count that is wrong is a lead, not
   a footnote: J1e goes and finds the file.
2. **`tee` also wrote to stdout, and a redirect does not.**  The sweep measured that
   the committed *file* does not move.  It did not measure the other half: on the
   FAILING path, `| tee` put the failing step's diagnosis on the runner's stdout.
   The replacement only does that if the `||` guard `cat`s the transcript.  J4c
   measures it per site (Q21).
