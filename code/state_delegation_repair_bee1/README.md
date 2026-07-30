# `state_delegation_repair_bee1` — mg-bee1's repair of mg-4acd against mg-218d's audit

The instrument being repaired is `code/state_landing_control_2da3/`; this directory is the
**evidence for the repair**, not a second control. Nothing here is imported by anything
there.

```
sh code/state_delegation_repair_bee1/run_all.sh      # ~2 min
```

**Headline.** mg-218d found that mg-4acd's certified property is **false as stated** — the
sentence is universally quantified over mutations and the mechanism is quantified over a
region's own section — and that a certified region's meaning is carried by a file **outside
the certified set**. Ten of sixteen mutations changed what a reader is shown and exited 0.

- **The statement is repaired first**, in every place it is published that can still be
  edited: `presentation.py`'s header, `COVERAGE.md`, `delta_control.py`'s header, and a new
  certified block in `docs/state-history/README.md` which is the correction of record for
  `e4426c9`'s commit message, which cannot be.
- **The delegation is repaired mechanically.** `delta_control.py` section 2c reads each
  certified region's own bytes, extracts every inline link, and digests the target sections
  a link cites **by name**. mg-218d's `T1`, `T2` and `T3` go from exit 0 to non-zero.
- **The document-global ordinal is measured and NOT taken.** It would close four of the
  silent rows, re-baseline on **83%** of the commits that have touched `STATE.md` and **4 of
  4** that have touched the state-history README, and **still** leave the unqualified
  property false — a retraction that *replaces* a paragraph elsewhere adds no block and is
  silent under it too.
- **L3, L4-within-section, L5, L6 and the 140/140 renderer agreement are untouched.** Not
  one line of `presentation.py`'s model changed, and not one line of
  `code/state_layer_audit_218d/` did either.

| file | what it is |
|---|---|
| `globalpos_bee1.py` | the document-global ordinal implemented as the smallest possible re-scoping of mg-4acd's record, then measured: what it closes, its re-baselining rate over the real git history of both certified files, and `P7`, the mutation it still misses |
| `battery_bee1.py` | 7 new mutations at the boundary of the new mechanism, each carrying **the exit code predicted before the run**. Three are predicted **silent**: they are the stated bound, tested |
| `out_globalpos.txt`, `out_battery_bee1.txt` | committed runs of the two |
| `out_layers_bee1.txt` | **mg-218d's 16-mutation battery, re-run UNMODIFIED** — the evidence, and the only rows here that were not written by the author of the repair |
| `out_battery_babf_bee1.txt`, `out_battery_2216_bee1.txt` | mg-babf's 15 and mg-2216's 14, re-run unmodified against the repaired instrument: **11 of 11 caught / 0 silent misses** and **10 caught / 0 missed / 2 tolerated / 2 noisy**, identical to what mg-4acd and mg-218d each measured |
| `out_coverage_bee1.txt` | mg-218d's `coverage218d.py`, re-run unmodified: **40 of 40** claims in `COVERAGE.md` still hold against the code, and **3 of 3** uncontrolled layers are now NAMED there — it measured 0 of 3 against `e4426c9` |
| `run_all.sh` | all five sections |

## What the re-run of mg-218d's battery shows

Re-run **unmodified** — not one line of `code/state_layer_audit_218d/` is touched by this
repair. Its silent rows go from **ten of sixteen to six of sixteen**:

| row | mg-218d measured | after mg-bee1 |
|---|---|---|
| `T1` a cited section deleted from the target | 0 | **1 (FAIL)** |
| `T2` the F1 repair inverted in the target | 0 | **2 (MOVED)** |
| `T3` the target emptied | 0 | **1 (FAIL)** |
| `I2` `norm()` widened to `.strip()` | 0 | **1 (FAIL)** |
| `P2` `P3` `P4` `P6` cross-section context | 0 | 0 — **stated, not closed** |
| `S1` a contradicting near-copy added | 0 | 0 — **open, and named** |
| `I1` an entry dropped from `CERTIFIED` | 0 | 0 — **open, and named** |
| `L3a`–`L3d`, `P1`, `P5` | fire | fire, unchanged |

Those four rows now read as *"predicted 0, got non-zero"* in `out_layers_bee1.txt`. **That
is the finding landing, not a regression in mg-218d's battery** — its predictions were
written against `e4426c9` and were correct against `e4426c9`. Its own frozen run stays at
`code/state_layer_audit_218d/out_layers.txt`, and this one is a separate file, so neither
overwrites the other's evidence.

## The predict-first discipline is mg-218d's and is kept

Every row in `battery_bee1.py` carries the exit code this repair predicted **before** it was
run, written into the file before it was executed. A battery whose expectations are written
after the run is a battery that cannot be wrong. Its harness is mg-218d's
`harness218d.py` — the auditor's, not one written by the author of the code under test.

## Which layer is uncontrolled after this repair

Assume the blind spot **moved** rather than closed; five generations running, it has.

| layer | after mg-bee1 |
|---|---|
| **L0 instrument** | **partly closed.** `norm()` is checked behaviourally against its published rule, so `I2` and `I3` fire. Deleting an entry from `CERTIFIED` (`I1`) still exits 0, and nothing inside the file can change that |
| **L1 what a region points at** | **closed for cited sections** (`T1` `T2` `T3` `D1` `D2` `D3`). The target's uncited sections and its own framing are not (`D4` `D5`) |
| **L2 region set** | **OPEN** (`S1`). No digest over a chosen set of regions can see a region that is not on the set, and the cheap fix would catch mg-218d's mutation rather than the layer |
| **L3 region location** | closed; all four of mg-218d's fire, each classified FAIL |
| **L4 presentation** | **section-local, and now SAID to be** (`P2` `P3` `P4` `P6` `P7` still exit 0) |
| **L5 / L6** | closed by mg-7870, probed by mg-babf, verified against two renderers by mg-218d |

**Read L2 and the L4 residual as the next auditor's targets.** They are stated here, in
`COVERAGE.md` and in `delta_control.py`'s header, so they are tested rather than discovered.

> **CORRECTION OF RECORD — the `L1` row above is FALSE AS STATED (mg-5644 B1, repaired by
> mg-0049).** The row is left verbatim; this note is appended rather than folded in, because
> a repair that rewrites its own superseded claim leaves no record that it made one.
>
> *"Closed for cited sections"* is quantified over **which sections are followed**. What this
> repair built was a content digest over their **bytes**, with **no presentation record and
> none of section 8's default-deny guards** — the two things every certified region in the
> two files this instrument *reads* has carried since mg-4acd. mg-5644 put mg-babf's own
> `B05`/`B06` to the surface this repair created: **one `<!--` line at the top of the target,
> never closed.** Every cited section byte-identical, every digest above matching, `marked`
> and `markdown-it` agreeing over 60 comparisons that **zero of the five cited sections are
> visible**, a reader following the certified cell's six links **shown a blank page** — and
> the control **exited 0**. It is the same defect as the one this repair was filed to fix:
> **a true sentence quantified over the wrong thing.**
>
> `code/state_delegation_repair_0049/` closes it, applying the same `presentation.py` to the
> delegated surface, and restates the bound in terms of **what a reader is shown**. Nothing
> else in this directory is changed: `battery_bee1.py` and `globalpos_bee1.py` are unedited
> and still reproduce byte-identically.

## Safety

Sections 2, 3 and 4 of `run_all.sh` mutate tracked files in the working tree —
`docs/state-history/README.md`, `docs/state-history/attempt-mg-276d.md`, `STATE.md` and
`code/state_landing_control_2da3/delta_control.py` — and restore them under a `finally` plus
a sha256 check. Each refuses to run on a dirty tree, because a crash would then restore the
wrong bytes. `globalpos_bee1.py` mutates nothing: every mutation there is applied to a string
in memory.
