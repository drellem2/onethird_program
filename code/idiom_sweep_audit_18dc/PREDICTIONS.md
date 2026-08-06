# mg-18dc — PREDICTIONS for the INDEPENDENT AUDIT of the runner-idiom sweep

**Committed before any script of this audit exists.** `code/idiom_sweep_audit_18dc`
holds this file and nothing else at the commit that carries it. My HEAD is
`7fccb4e`, the commit that carries mg-ec63's transcripts onto `main`.

The subject is mg-ec63, the arc-wide truncate-before-probe sweep, which has
merged; through it, mg-03d1's three inherited figures **109 / 86 / 43**.

---

## DISCLOSURES — measured before these predictions were written

The arc's convention: a figure I already know is a **measurement**, not a
prediction, and laundering it into one is the cheapest way to look right. Eight,
all obtained by reading the record and by `git ls-tree` / `git patch-id`, before
this file existed.

- **D1.** `git ls-tree` count of `code/*/run_all.sh`, by revision:
  `9f1ecaa` **108**, `d33970b` **109**, `eacc5e1` **112**, `3fc870a` **110**,
  `41972fb` **110**, `c1bb466` **116**, `7fccb4e` (my HEAD) **116**.
- **D2.** Four commit pairs in this lineage are **patch-id SAME / tree DIFF** —
  pre- and post-rebase twins: `9f1ecaa`↔`6fda370`, `d33970b`↔`eacc5e1`,
  `454f565`↔`f98ef34`, `41972fb`↔`7fccb4e`. Patch-id adjudicates the *diff*;
  the *base* differs, and every population figure is a fact about the base.
- **D3.** `code/grain_axis_audit_03d1` is **absent** at `3fc870a`/`41972fb` and
  **present** at `c1bb466`/`7fccb4e`.
- **D4.** `code/truncate_sweep_ec63/s1_population.py` has been touched by
  **exactly one** commit, `8313882`. Commit `2bf262f`, whose subject announces
  the S1a change, touched `README.md` and `out_s2_bite.txt.new` **only**.
- **D5.** The string `THE TOTALS AGREE AND THE POPULATIONS DO NOT` is present at
  `s1_population.py:40` and in the shipped `out_s1_population.txt`.
- **D6.** mg-ec63's `s3_sweep.classify()` defines `NEVER EXERCISED` as
  `b_broke and a_ok` — the **healthy** arm breaking while the **defect** arm
  works.
- **D7.** mg-ec63's 11 `SAME` and 14 `NDET` steps are named in
  `out_s3_sweep.txt` (S3d). I have the list.
- **D8.** mg-c2b3's `out_k1_census.txt` already re-derives the ticket's
  `1 runner sets pipefail` as **0** (`ticket 1 re-derived 0 DIFFERS`). The
  figure my own brief hands me is contradicted inside the tree it cites.

---

## PREDICTIONS

Each names its **population** and the **grain** of its unit, and each names what
would falsify it.

### P1 — THE ORDERING. The sweep ran before the fix.

Over every commit from `eacc5e1` (mg-03d1's carrier) to `7fccb4e` inclusive,
**zero** `code/*/run_all.sh` outside `code/truncate_sweep_ec63/` that already
existed at `eacc5e1` is **modified**.
*Population:* commits in that range. *Grain:* one modification of one
pre-existing `run_all.sh`. *Falsifier:* one or more.

### P2 — 109 is a fact about a base, and its counter was untracked.

**P2a.** The single tree in mg-03d1's 109 that `git ls-tree` at its own declared
HEAD `9f1ecaa` does **not** carry is `code/grain_axis_audit_03d1` — its own.
*Grain:* one tree. *Falsifier:* the difference is any other tree, or more than one.

**P2b.** At `d33970b` the set of 109 partitions exactly as mg-03d1 printed it:
86 truncating + 2 `.new`/`mv` + 21 neither = 109, with `runner_exit_repair_bf79`
and `grain_axis_audit_03d1` the two.
*Falsifier:* any cell differs.

### P3 — 86 is wrong in **both** directions, and I will show it by execution.

My rule is not a regex and not a shell parser: I run each `run_all.sh` in a
**disposable clone** with `python3` replaced by a stub that records its argv and
writes nothing, and I record which `out_*.txt` the **shell itself** truncates or
creates. That measures the redirection, not a sentence about it.

**P3a.** At tree state `d33970b` my execution count of truncating runners is
**strictly greater than 86**.
*Population:* the 109 runners at `d33970b`. *Grain:* one `run_all.sh`.
*Falsifier:* ≤ 86.

**P3b.** At least **one** runner mg-03d1 counted as truncating is shown by
execution to truncate **no** `out_*.txt` — a false positive of the regex.
*Falsifier:* zero.

**P3c.** At least **three** runners mg-03d1 counted as non-truncating do
truncate under execution — false negatives.
*Falsifier:* fewer than three.

### P4 — 43 does not reproduce either.

My execution-derived tree-grain count of runners where the shell empties an
`out_*.txt` that a probe of the **same run** then opens for reading is **not 43**
at `d33970b`.
*Population:* the truncating runners of P3a. *Grain:* one `run_all.sh`.
*Falsifier:* exactly 43.

### P5 — THE THIRD OUTCOME IS UNREACHABLE FROM mg-ec63'S RULE, AND IT IS NOT EMPTY.

The ticket's three outcomes are SAME / DIFFERENT / **cannot run at all against
real input**. mg-ec63 reports the third as **0**. Its `classify()` (D6) can only
reach that verdict when the **populated** arm breaks and the **emptied** arm
works. A probe that cannot run at all fails in *both* arms, is therefore
`A_text == B_text`, and lands in **SAME** — "the ordering bug cost nothing".

**P5a.** Of mg-ec63's 11 `SAME` steps, **at least one** raises a Python
traceback, or exits without executing its measurement, in **both** arms.
*Population:* the 11 named `SAME` steps. *Grain:* one step.
*Falsifier:* all 11 run clean in both arms.

**P5b.** Of the 11, **at least one** completes cleanly in both arms over an
**empty** population — a vacuous pass, the third outcome in its other reading.
*Falsifier:* none.

**P5c.** mg-ec63's reported `NEVER EXERCISED = 0` is a property of the rule and
not a measurement of the arc: I will construct a step that cannot run at all and
show mg-ec63's `classify()` calls it `SAME`.
*Falsifier:* `classify()` returns `NEVER EXERCISED` on it.

### P6 — THE SHAPE ELSEWHERE, and the two populations overlap.

At my HEAD, the set of runners using `| tee` without `pipefail` and the set
truncating a transcript a probe of the same run reads **overlap in at least 10**
runners.
*Population:* the 116 runners at `7fccb4e`. *Grain:* one `run_all.sh`.
*Falsifier:* fewer than 10.

### P7 — THE RESTORE IS SCOPED TO ONE DIRECTORY AND THE RUN IS NOT.

mg-03d1's A4d asserts its restore with `git status --porcelain -- <tree>`, one
directory. **At least one file outside that directory is modified** by the run it
restores from.
*Population:* the whole worktree. *Grain:* one file.
*Falsifier:* zero files outside.

### P8 — CONVERGENCE ON A TREE mg-03d1 DID NOT USE.

mg-03d1 verified 6-of-6 byte-identical on `runner_exit_repair_bf79`. On a
`.new`+`mv` tree it did **not** use, **at least one** transcript is **not**
byte-identical across two consecutive runs.
*Grain:* one transcript file. *Falsifier:* all identical.

### P9 — THIS INSTRUMENT WILL COMMIT THE DEFECT IT AUDITS.

I will record **at least three** defects of this instrument, **at least one** of
which is an instance of the audited class — a count over a population containing
the counter, or an artifact consumed by the run that produces it.
*Falsifier:* fewer than three, or zero self-instances.

---

## WHAT I AM NOT PREDICTING, AND WHY

- **Nothing about the 40 timed-out steps.** mg-ec63 says every count is a lower
  bound because of them. A prediction over an unmeasured set is a guess dressed
  as a hypothesis.
- **Nothing about the three `suspect` trees.** Turning suspect into wrong needs
  each probe run at its own publishing revision, which mg-ec63 did not do and
  which I do not expect to do either.
- **No prediction on the `>` vs `tee` *causal* question.** P6 is an overlap of
  two sets and nothing more.
