# mg-c2b3 — outcomes, scored against `PREDICTIONS.md`

Scored from the committed transcripts (`out_selftest.txt`, `out_k1_census.txt`,
`out_k2_consume.txt`, `out_k3_retro.txt`, `out_k4_control.txt`).

| | prediction | outcome |
|---|---|---|
| **Q1** | all 34 tee'd targets exit **0** run directly | **HIT** — 34 of 34 |
| **Q2** | `git status --porcelain` identical across K3b | **HIT** |
| **Q3** | zero committed `out_*.txt` outside this tree change | **HIT** — 17 files changed since `bee07a1`, 0 transcripts |
| **Q4** | the defect reproduces at **34 of 34** sites | **HIT** |
| **Q5** | the fix bites at **34 of 34** sites | **HIT** — *after the scoring rule was corrected; see below* |
| **Q6** | pre-repair runner exits non-zero at **exactly 3** sites | **MISS — 8** |
| **Q7** | baseline exits non-zero for `a4ef` and `f8fa` | **HIT**, and incomplete |
| **Q8** | baseline reach identical pre/post at all 17 runners | **HIT** |

---

## Q6 — the miss, and it is a finding rather than a retune

**Predicted:** on the pre-repair text with a step forced to exit 1, the runner
exits non-zero at exactly three sites — `species_7d75/selftest.py`,
`species_audit_73df/selftest73df.py`, `species_audit_a61f/selftesta61f.py`.

**Measured: eight sites, across five runners.** The three above, plus

```
species_remainder_f8fa / selftestf8fa.py     exit 1, reach 5 of 5
species_remainder_f8fa / w1_opposite.py      exit 1, reach 5 of 5
species_remainder_f8fa / w2_typemismatch.py  exit 1, reach 5 of 5
species_remainder_f8fa / w3_scope.py         exit 1, reach 5 of 5
species_repair_a4ef    / selftesta4ef.py     exit 1, reach 4 of 4
```

**Why it missed, and it is not the extent.** Q7 predicted correctly that
`species_repair_a4ef` and `species_remainder_f8fa` have a *non-zero baseline*,
because their cross-section block ends in `echo "$E2OUT" | grep -E …` over a
stub's output. What Q6 did not follow through is that a non-zero baseline
**carries into the pre-repair-failure run too** — the run does not stop, so it
reaches the same terminal `grep` and returns the same 1. The two predictions
were about the same five lines of shell and were written as if they were about
different ones. Q6 also counted per *runner* while the table is per *site*, and
`f8fa` has four sites.

**What the miss does not change.** Nothing. Q6 exists only to justify why K4
scores the defect on **reach** and not on the exit code, and the measured 8 is a
stronger version of that justification than the predicted 3: an exit-code-only
control would have called **eight** sites healthy, not three. The prediction is
kept as written.

## Q5 — a hit only after the scoring rule was corrected, said plainly

The first run of K4 scored **19 of 34**. Fifteen rows were red, and the repair
was not the reason: the rule was `len(q_reach) < len(b_reach)`, which is false
whenever the failing target **is** the last step — a working runner then reaches
exactly as far as the baseline. Ten sites are last steps.

The `reach` measurement was also wrong in the same run, and more interestingly:
stubs printed their marker on **stdout**, and every runner redirects its steps
into a transcript, so `reach` was counting *markers that survived the redirect*
rather than *steps that executed*. `species_7d75` reported a baseline reach of 1
for a runner that launches seven scripts.

Both were fixed by measuring the thing meant to be measured — each stub appends
its name to a file at an absolute path, immune to redirection and to `2>&1` —
and the rule became *the runner exits non-zero AND the target is the last step
that ran AND what ran is a prefix of the baseline*. That is recorded here rather
than quietly corrected, because a control retuned until it passes is the defect
this ticket is about wearing different clothes. The distinguishing fact is that
**the 15 red rows were red for a defect in the instrument and the 34 green rows
are green on a rule that is strictly harder than the one that produced 19**.

## K3c — a first draft that scored 4 of 4 BAD against sound code

`K3c` asks whether C2's non-zero exit could have come from a pipeline. The first
draft checked *"does the five-line block contain a pipeline"* and got **yes**,
four times out of four — because the block's failure **handler** contains
`echo "$E2OUT" | grep 'STANDING UN-STRUCK' || true`. The section's own prose
then said *"There is no pipeline in it"*, contradicting the table directly above
it.

Replaced by the three things that actually have to hold, each measured
separately: **A** the line whose status is read is an assignment from a command
substitution with no pipeline; **B** the handler ends in an unconditional
`exit 1`; **C** every pipeline inside the handler is `|| true`, so none can
abort the handler before that `exit 1`. A, B and C hold at both revisions.

## K3f — the byte-identity, measured on a repaired runner

`K3d` shows no committed transcript was *edited*. It does not show that a
**repaired runner still produces the committed bytes**, which is what the whole
R1 class rests on. `code/face_geometry/run_all.sh` — the subject of claim C6 —
is therefore executed and its two transcripts compared: **exit 0, neither
transcript moved.** `> f` and `| tee f` write the same stream, demonstrated on
the real runner instead of deduced from the shell's semantics.

And the other direction, because *"no transcript moved"* is a weak claim if none
of them ever move: four transcripts in `code/face_geometry_audit_1c80/` do **not**
regenerate (`out_n6.txt`, `out_witness.txt`, `out_claims.txt`,
`out_mutations.txt`). That drift is **not this repair's** — it reproduces on a
pristine `git archive bee07a1` checkout with none of these edits present,
because those instruments read the live tree and the live history. It is the
same class the arc already records for mg-6653 and mg-7d5a, and it is named
here so that "no transcript moved" cannot be read as "nothing in the arc ever
moves".

## An edit outside the runners, and the one deliberately not made

`code/face_geometry/controls.py`'s `ArtifactTee` docstring stated that
`run_all.sh` builds `controls_output.txt` **as a `tee` pipeline**. After the
repair that sentence is false, so it was corrected — and the correction was then
checked the only way it can be: the runner was re-run and both transcripts came
back byte-identical.

`code/face_geometry_audit_e720/attack_artifact_check.py` prints the same stale
clause, and it was **left alone**. Its output is a *committed audit transcript*
whose byte identity that audit claims and defends; editing the source would
break a control in order to fix a comment. The arc's own convention for a frozen
audit — see the STATUS block in `code/face_geometry_audit_6653/run_all.sh` — is
to record the staleness in prose beside it, which is what §6 of
`docs/OneThird-RunnerExit-ArcWideSweep.md` does.

## K1 — the ticket's own numbers

Not predicted by this ticket (a census is a measurement), but the *ticket*
predicted them:

| | ticket | re-derived | |
|---|---|---|---|
| `run_all.sh` | 63 | **64** | DIFFERS — `code/hodge_leverage_repair_8eca/` landed in `bee07a1`, after the ticket |
| bare grep `\| *tee` | 23 | **23** | AGREES |
| `pipefail` | 1 | **1** | AGREES — but see below |

and the number the ticket did not separate: **17** runners contain a real
pipeline. The other six are header comments saying they do not.

**mg-7522 — the `pipefail` row was AGREES in this table and `DIFFERS` in the
instrument's own transcript.** `out_k1_census.txt` prints `ticket 1 /
re-derived 0 / DIFFERS`; this file, the README, the published document and
`k1_census.py`'s docstring all reported **1, "confirmed exactly"**. The ticket
was right and `libc2b3.PIPEFAIL_RE` was wrong — it matched only the spelling
`set -o pipefail`, and `code/state_restructure_34bf/run_all.sh` writes
`set -euo pipefail`. The regex is repaired and the row above now holds for a
reason rather than by coincidence. The transcript is left as the record of the
run that produced this commit; the corrected reading is in
`code/runner_exit_repair_7522/out_s3_figure.txt`.

**mg-7522 — the population of every number in this section.** All of them are
over files *named* `run_all.sh`. Two runners called `run_audit.sh` carried eight
`| tee` pipelines and were unrepaired at `HEAD` after this sweep, and three more
throw a status away without using `| tee`. Over every tracked `*.sh` the census
is **19 files / 42 `| tee` pipelines** at `bee07a1`.
