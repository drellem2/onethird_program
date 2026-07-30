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
| `run_all.sh` | all four sections |

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

## Safety

Sections 2, 3 and 4 of `run_all.sh` mutate tracked files in the working tree —
`docs/state-history/README.md`, `docs/state-history/attempt-mg-276d.md`, `STATE.md` and
`code/state_landing_control_2da3/delta_control.py` — and restore them under a `finally` plus
a sha256 check. Each refuses to run on a dirty tree, because a crash would then restore the
wrong bytes. `globalpos_bee1.py` mutates nothing: every mutation there is applied to a string
in memory.
