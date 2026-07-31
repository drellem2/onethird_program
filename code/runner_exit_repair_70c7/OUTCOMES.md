# mg-70c7 — outcomes

The six findings of `mg-dee4` against `1ee1f1b` (mg-7522), landed. Every figure
below is printed by a probe in this directory next to the predicate that
produced it; the transcripts are committed.

**The one-line verdict.** *All six are repaired at the predicate rather than at
the instance: the clearance is derived at the execution grain and reads 16 of
16, the moving figure is a pointer and the rule that moves it is now a census,
the marker rule is one object pointed in both directions over a population that
includes the prose, the claim window is one line either way, the caller scan
names a property, and the consumption clause is a named disjunction whose one
new member has had its failure direction measured rather than argued.*

---

## Predictions, scored

`PREDICTIONS.md` was committed at `93bd689`, before any probe in this directory
existed. **Two missed and are kept as written**, and both misses are of the same
kind: reasoning from the size of a gap without checking how much of it the new
rule could reach.

| id | prediction | outcome |
|---|---|---|
| **R1a** | the executions are derivable from the runners' bytes | **HIT** — the loop header expands, the body's `base=${pair%% *}` assignments are followed |
| **R1b** | 8 discarded `git diff` executions (6 + 2) | **HIT** — 8 |
| **R1c** | 4 of them never run by mg-7522, and the `':!*.md'` form never in any shape | **HIT** — 4, of which 3 carry the pathspec |
| **R1d** | all 8 exit 0 | **HIT** |
| **R1e** | 16 discarded statuses read at the execution grain | **HIT** — 8 `\| tee` + 8 `git diff` |
| **R1f** | 4 of 4 artifacts need the sentence changed | **HIT** — `s2_status.py`, `README.md`, `OUTCOMES.md`, the published document |
| **R2a** | no anchor reproduces 154; the live figure exceeds mg-dee4's 275 | **HIT** — 166 / 257 / 240 in prose because they cannot move, and the two that move are in `out_r2_anchor.txt` |
| **R2b** | `154` is no longer a figure in the document | **HIT** |
| **R2c** | between 2 and 8 unbacked figures in mg-7522's artifacts | **HIT** — 4: `154` in the document **and again** in `OUTCOMES.md:28`, `2111`, and a quotation of mg-c2b3's `63` |
| **R3a** | 9 alternatives against 3, `verified` in the nine only | **HIT** |
| **R3b** | at least 5 USEs appear under the widened rule over `*.py` + `*.sh` | **HIT** — 16 |
| **R3c** | 0 UNBACKED in `*.py` + `*.sh` | **HIT** |
| **R3d** | the `.md` widening adds 3 artifacts + the document, and finds ≥1 UNBACKED | **HIT** — and the one it found is `OUTCOMES.md:88`, the `verified` claim `mg-dee4`'s F4 is about |
| **R4a** | the one-line window takes mg-c2b3's artifacts from 20 to 24 | **HIT** |
| **R4b** | the 4 new claims include `code/runner_exit_c2b3/OUTCOMES.md:88` | **MISS — the wrong population.** Line 88 is in **mg-7522's** `OUTCOMES.md`, not mg-c2b3's. The four the window adds to mg-c2b3's population are `OUTCOMES.md:9`, `k1_census.py:20`, `libc2b3.py:141` and `selftestc2b3.py:108` |
| **R4c** | 0 of the 4 new claims is WRONG | **HIT** — all four disposition as NOT A CLAIM |
| **R5a** | 9 sites outside the two names, 4 consuming | **HIT** |
| **R5b** | 0 sites name `run_audit.sh` | **HIT** |
| **R5c** | the widening loses nothing | **HIT** — every site the two-name rule found is still found |
| **R6a** | the value arm pulls `c0_repro.sh:47` in | **HIT** |
| **R6b** | mg-7522's own three do not move | **HIT** — both arms are true of all three |
| **R6c** | widened P2 at `bee07a1` between 21/29 and 28/40 | **MISS — 20 / 27.** I reasoned from the gap between P1 (53 pipelines) and P2 (26) without asking how much of it the VALUE arm could reach. Almost all of that gap fails C3, not C1 |
| **R6d** | at least 2 files in the widened P2 at HEAD | **MISS — 1.** Same reasoning error, same direction |
| **R6e** | every discarded status of the new member, read directly, exits 0 | **MISS — it cannot be read directly at all.** Its discarded stages read `$WORK`, a `mktemp -d` created at run time; there is no argv until the script that builds it is running. R5c stands in its place and is stronger: it makes the stage fail and reads what the script DOES |
| **R7a** | this tree's runner is outside the widened P2 as well | **HIT** — 0 pipelines of any kind, 7 of 7 steps redirect and guard |
| **R7b** | my own first draft fails the grain check somewhere | **HIT, three times over** — see below |
| **R7c** | 0 undispositioned figures in my own artifacts | **HIT** |

---

## Three defects in this instrument, recorded rather than smoothed away

**1. A line number backed a measurement.** The figure census built its corpus by
matching every number in the transcript text. Under that rule `154` — the exact
figure `mg-dee4`'s F2 is about — came back **BACKED**, by the string
`s3_figure.py:154` in `out_s5_self.txt`. The census would have blessed the
figure it was written to catch. The corpus is built with the same `figures()`
rule the claim side uses now, line by line, and `on line 89` is not a figure
either.

**2. A check that would have been satisfied by deleting the evidence.** R1e's
first draft forbade the string `11 of 11` outright. Every artifact that had
correctly described what it repaired went red **for saying so** — and the
cheapest way to pass would have been to delete the record of the defect. QUOTED
and ASSERTED are counted separately now, by whether the line is also correcting
the figure. That is the mention-vs-use distinction this arc runs on, one more
level down.

**3. The marker rule scored a quoted phrase as a use.** `strength_lines` tested
the single character on each side of the marker, so `` `verified against the` ``
— a phrase quoted whole, with the marker at its start — was a USE. The first
thing it flagged was **this repair's own comment about mg-dee4's F4.** The rule
tests containment in a delimited span now, which is what the delimiters were
always standing for.

---

## What was regenerated, and what deliberately was not

| transcript | regenerated? | why |
|---|---|---|
| `runner_exit_repair_7522/out_s{1..5}*.txt`, `out_selftest_7522.txt` | **yes** | every one of those probes changed |
| `runner_exit_c2b3/out_selftest.txt`, `out_k2_consume.txt` | **yes** | the rules they exercise changed; a transcript of a rule that no longer exists is not a record of anything |
| `runner_exit_c2b3/out_k1_census.txt` | **NO** | it is the record of `ticket 1 / re-derived 0 / DIFFERS`, and `mg-05eb` cites it as that record. The regex is repaired, so a re-run would print `AGREES` and destroy the citation |
| `runner_exit_c2b3/out_k3_retro.txt`, `out_k4_control.txt` | **NO** | untouched rules |
| `runner_exit_audit_dee4/*` | **NO** | an audit's transcript is the record of what it found; this tree answers it, it does not edit it |

---

## What this repair did NOT check, named rather than folded into a total

* **Whether the value arm is the RIGHT widening.** F6 is a disagreement with a
  definition, not a measurement of one. `lib7522.consumed` is written out in
  full — both arms, with their reasons — so that disagreeing with it is
  possible.
* **mg-c2b3's own 34.** Cited, not re-measured, for the third ticket running.
  The covered set is *16 executions run here + 8 `| tee` sites mg-7522 derived +
  34 inherited from a transcript nobody in this chain has re-run.*
* **Whether a BACKED figure is backed by the RIGHT measurement.** The backing
  test asks whether a figure appears in a transcript, not whether it appears as
  the answer to the same question. Weak in one direction, stated where the rule
  lives, and every row prints the figure so the sense is checkable by eye.
* **Whether the grain WORD is the right one.** R6a establishes that a count over
  source carries a grain word within its window. A count labelled `executions`
  that is really sites would pass. What it prevents is a number with no grain
  attached at all — which cannot be argued with, because it does not say what it
  counts.
* **Every intermediate commit.** Read at `HEAD`, on one machine, inherited from
  mg-7522's own statement of the same limit.
