# `state_delegation_audit_5644` — mg-5644's independent audit of mg-bee1

The object under audit is **mg-bee1**, commits `a2d5a81` + `2a29f30`, which repaired
`code/state_landing_control_2da3/` against mg-218d's audit. This is the **sixth** control in
this lineage.

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_delegation_audit_5644/run_all.sh    # ~6 min
```

## The question, and the answer

Each control so far was blind in a different place: a pinned revision (INPUT), author-chosen
substrings (MUTATION SET), a vacuous control group (POPULATION), a restatement labelled a
control (PROPOSITION), a real property bounded to a SECTION while stated universally. **Five
for five, the blind spot moved rather than closed.**

**It moved again, and it moved twice.**

| | finding | evidence |
|---|---|---|
| **B1** | mg-bee1 created a NEW REGION SET — five delegated sections of a file outside the two the instrument reads — gave it a **content digest and no presentation record**, and published it as *"closed for cited sections"*. **mg-babf's B05/B06 work verbatim on it.** One `<!--` line at the top of the target and a reader following the certified cell's six links is shown a **blank page** by both `marked` and `markdown-it`, while every delegated digest matches and the control **exits 0** | `out_delegated.txt` Q1 Q2, `out_render.txt` |
| **B2** | **BEYOND BRIEF.** The new L0 probes are published as *"they fire on a widened EDGE constant"* and *"raises ... from free to two edits"*. `str.strip()` removes 29 characters, the published rule admits 4, the probes name **2 of the 25** that matter. **23 of 25 widenings exit 0**, one edit each, probes left in place and passing. mg-bee1's own row `I3` widens `EDGE` with `U+00A0` — **the character probe 2 is built around** | `out_norm.txt`, exhaustive sweep of all 25 |
| **M1** | mg-bee1's README and `2a29f30`'s message say the document-global ordinal would re-baseline on **"4 of 4"** commits of the state-history README. Its own instrument prints **5 of 5 (100%)** | `out_globalpos.txt` line 68 |

B2 is the sharper one for the lineage's own record. Generation 2's defect was *author-chosen
substrings at the mutation set*. Generation 5's was *a universally quantified sentence over a
mechanism quantified on a chosen subset*. **Section 0 is both, in the same file, in the commit
that repaired generation 5** — and it is beyond-brief material, which is where roughly seven
consecutive generations of this arc have put their worst finding.

## What is NOT undone — verified, not assumed

Every figure below was re-measured in this worktree from an independent run, not read off
mg-bee1's committed outputs.

| claim | mg-bee1 reports | this audit measured |
|---|---|---|
| mg-218d's 16-mutation battery re-run **UNMODIFIED** | 10 silent → 6 | `git diff a4aeeb9..HEAD -- code/state_layer_audit_218d/` is **empty**; independent re-run is **byte-identical** to `out_layers_bee1.txt`; 10 → 6 confirmed, still silent: `I1 S1 P2 P3 P4 P6` |
| the two-renderer agreement | "140 of 140 stands" | **141 of 141** — the population grew by mg-bee1's own new block. Nothing retreated |
| mg-babf's 15 re-run unmodified | 11 of 11 caught, 0 silent misses | identical |
| mg-2216's 14 re-run unmodified | 10 caught, 0 missed, 2 tolerated, 2 noisy | identical |
| `coverage218d.py` re-run unmodified | 40 of 40 claims hold; 3 of 3 uncontrolled layers NAMED | identical — but see B1: there is now a **fourth**, and it is named nowhere |
| B2 (delegation): delete a cited section / invert it / empty the file | `T1` `T2` `T3` all fire | confirmed 1 / 2 / 1, and reproduced on this audit's own harness as `Q5` `Q6` |
| `battery_bee1.py`, `globalpos_bee1.py` | 7 of 7 predicted; the ordinal measured | both reproduce **byte-identically** |

**No over-correction.** L3, L5, L6 and the renderer agreement stand and were not weakened.
The statement repair is real and is in all three editable places plus a certified
correction-of-record block; the fourth occurrence of the unqualified sentence is inside
mg-218d's own audit document, where it is the thing being criticised, which is correct.

## Which layer is uncontrolled after mg-bee1 — verified, not inherited

mg-218d found L0, L1 and L2 firing on none of their six. That verdict was **re-measured
here** rather than carried forward, because an inherited layer verdict is the pinned-input
defect this lineage already suffered once.

| layer | after mg-bee1 | this audit |
|---|---|---|
| **L0** instrument | mg-bee1: "partly closed — `norm()` checked against its published rule" | **the specific divergence is closed; the RULE is not asserted.** `E8` (a bare `strip()`) fires, so mg-218d's `I2` is genuinely shut. 23 of 25 single-character widenings, and any interior rewrite outside the four fixtures, exit 0 |
| **L1** what a region points at | mg-bee1: "closed for cited sections" | **closed for their BYTES, open for their PRESENTATION.** `Q1` `Q2` |
| **L2** region set | mg-bee1: OPEN, and the fix declined as mutation-shaped | OPEN, agreed. The *reason given* is overstated — see `out_l2pop.txt` |
| **L3** region location | closed, 4 of 4 fire | confirmed |
| **L4** presentation | section-local, and now SAID to be | confirmed; `P2` `P3` `P4` `P6` `P7` still 0, correctly stated. **But L4 on the DELEGATED surface is a new hole and is stated nowhere** |
| **L5 / L6** | closed | confirmed, 141/141 |

**Read L4-on-the-delegated-surface as the next auditor's target**, and note that it did not
exist before `a2d5a81`: the repair created the surface it is on. The fix is available and
cheap — section 8's two default-deny guards already do exactly this job for the two files the
instrument reads, and neither is applied to a delegated target.

## The negatives, tested by construction rather than by argument

Three negatives fell in this arc on 2026-07-30, all refuted by construction and none by
argument. mg-bee1 publishes two more.

- **"a document-global ordinal still leaves the sentence false"** — **stands.** `P7` replaces
  a paragraph in place, so no ordinal and no block count moves under any scoping. Nothing was
  built that refutes it; `globalpos_bee1.py` reproduces byte-identically.
- **"closing L2 by counting blockquotes would catch mg-218d's mutation and not the layer …
  and there is not one here"** — **OVERSTATED, not false.** `l2pop5644.py` builds a
  population rule — every blockquote block in the README must be certified or explicitly
  declared, with the same two-way default-deny mg-bee1 wrote for the delegation surface — and
  **6 of 6** L2-shaped mutations fire, including three mg-218d never wrote and the removal
  direction. It is not mutation-shaped. **Its bound, and why this is an observation and not a
  BROKEN:** it closes L2 for blockquotes in one file; a near-copy as a plain paragraph, or in
  `STATE.md`, is outside its population. mg-bee1's substantive point survives; the specific
  reason it gives for declining does not.

## Files

| file | what it is |
|---|---|
| `harness5644.py` | this audit's own mutation harness — not mg-218d's, not mg-bee1's. Its own snapshot, restore discipline and exit-code reader. mg-218d's sixteen are ALSO re-run on mg-218d's own harness, unmodified, in section 5 |
| `delegated5644.py` | **B1.** Six mutations on the delegated surface, each with the exit code predicted before the run. `Q1` `Q2` are mg-babf's B06/B05 moved one file out; `Q3` `Q4` re-measure mg-bee1's stated bound rather than inherit it; `Q5` `Q6` are positive controls |
| `render5644.py` | **B1 measured, not argued.** The mutated target handed to `marked` and `markdown-it`; 60 comparisons, both renderers agreeing on every one |
| `norm5644.py` | **B2.** Eight predicted-first mutations plus an **exhaustive sweep of all 25 characters** — the population, not a sample |
| `l2pop5644.py` | the L2 negative, tested by building the object it forbids, with the construction's own cost measured to the same standard |
| `out_layers_5644.txt` | mg-218d's sixteen, re-run unmodified in this worktree — byte-identical to mg-bee1's committed re-run |

**Two defects in `l2pop5644.py` were found by running it and are recorded in its docstring**
rather than quietly fixed: it first compared region spans by LINE NUMBER and reported five
false hits the moment a mutation shifted a line, and it was then silent on a verbatim
duplicate because one marker matched two blocks. Both are failures this cluster's own
locator discipline already forbids, and finding them in this audit's own instrument is the
reason the instrument is committed and not just its conclusion.

## Safety

Sections 1, 2 and 5 mutate `docs/state-history/attempt-mg-276d.md` and
`code/state_landing_control_2da3/delta_control.py` in the working tree and restore them under
a `finally` plus a sha256 check; each refuses to run on a dirty tree. Sections 3 and 4 mutate
nothing — every mutation there is applied to a string in memory. Nothing in this directory is
imported by anything in `code/state_landing_control_2da3/`, and this audit changed no file it
audits.
