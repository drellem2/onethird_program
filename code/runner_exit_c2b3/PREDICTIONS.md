# mg-c2b3 — predictions, written before the runs they score

Recorded so that a miss is a **finding** rather than a retune. Scored in
`OUTCOMES.md` against the committed transcripts.

## What is and is not predicted here, stated first

K1's census and K2's per-line classification are **measurements, not
hypotheses** — you cannot predict how many `run_all.sh` are in a tree, you
count them. They are not predicted and no credit is claimed for them. The
ticket's own three numbers (63 / 23 / 1) *are* predictions in this sense, made
by the ticket, and K1 scores them.

K3b's first two rows (`b0_repro.sh`, `selftest2060.py`) were already on screen
when this file was written. The remaining 32 are predicted below.

K4 had not been executed when this file was written.

---

## K3b — the exit status each pipeline discarded

**Q1.** All 34 tee'd targets exit **0** when run directly on the tree as it
stands. *Reasoning:* the arc's committed transcripts show clean verdicts, and
`git status` is clean between arcs, so a target exiting non-zero today would
mean an unnoticed regression — possible, and the reason the row exists.

**Q2.** `git status --porcelain` is **identical** before and after K3b.
*Reasoning:* three of the targets (`selftest6cb9.py`, `a6_mutations.py`,
`attack_artifact_check.py`) mutate a tree and restore it, and two of the three
say so in their headers. A miss here is the more interesting outcome.

**Q3.** **Zero** committed `out_*.txt` outside `code/runner_exit_c2b3/` change
as a result of this repair. *Reasoning:* `cmd | tee f` and `cmd > f` write the
same byte stream to `f`. If this misses, every byte-comparison claim in the arc
is in scope and the repair is wrong.

---

## K4 — the positive control

**Q4.** On the **pre-repair** text with a step forced to exit 1, the runner
reaches the same number of stubs as the baseline at **34 of 34** sites — i.e.
the failure never stops the run. *This is the defect, reproduced.*

**Q5.** On the **post-repair** text with the same step forced to exit 1, the
runner exits **non-zero** and reaches **fewer** stubs than baseline at **34 of
34** sites.

**Q6 — the interesting one.** On the pre-repair text the runner's exit code is
**0 at 31 of 34 sites and 1 at exactly 3**, and the three are

- `code/species_7d75/run_all.sh` (`selftest.py`)
- `code/species_audit_73df/run_all.sh` (`selftest73df.py`)
- `code/species_audit_a61f/run_all.sh` (`selftesta61f.py`)

*Reasoning:* those three end with a `grep -h "TOTAL BAD" out_*.txt` that has no
`|| true`. Under stubs the transcripts contain no `TOTAL BAD`, so the final
`grep` returns 1 and `set -e` exits 1 — **for a reason with nothing to do with
the failure**. This is why K4 scores the defect on REACH and not on the exit
code; if Q6 lands, an exit-code-only control would have called three broken
runners healthy.

**Q7.** The **baseline exit code is non-zero** for `species_repair_a4ef` and
`species_remainder_f8fa` as well, because their cross-section block ends in
`echo "$E2OUT" | grep -E ...` over a stub's output. Predicted so that a
non-zero baseline is not later read as a fault in the harness.

**Q8.** Baseline **reach is identical** pre- and post-repair for all 17
runners: with nothing failing, the repair changes nothing about what executes.

---

## The prediction most likely to be wrong, named

**Q6.** The count of three rests on reading the last line of seventeen runners
and reasoning about what a stubbed transcript contains. Both the count and the
membership are checkable, and either could be off by one. It is written as an
exact list rather than "some" precisely so that being off by one is visible.
