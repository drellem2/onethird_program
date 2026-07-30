# OUTCOMES — mg-d633

Scored against `PREDICTIONS.md`, which was written before any probe ran and has not been
edited since.

## Score: 1 of 21 predictions wrong, kept as written

| probe | predicted | measured | kept |
|---|---|---|---|
| P1–P10, P12–P21 | as written | as predicted | — |
| **P11** | **1** | **0** | **yes, and the reason is a finding** |

### P11, the miss, and what it actually measured

**Predicted:** X3 planted at the end of `code/species_repair_a4ef/run_all.sh` makes
`s1_extent.py` fire, because mg-d633 widened that checker to read every regular file in the
tree. **Measured: exit 0.**

**The extent is not what failed.** The file *is* read — `E1` measures that directly with an
instrumented `open`, and the count `s1_extent.py` prints for that tree (9) is the count it
read. What silenced the probe is the **exoneration rule**: `kerna4ef.py` clears any hit within
six lines of `mg-(6f61|f8fa|a61f|73df|a4ef)`, and line 18 of that `run_all.sh` says *"mg-73df's
MAJOR"* about something else entirely.

**So the probe was measuring the exoneration rule while claiming to measure the extent.** The
two are split rather than the probe retuned to pass: **P11** now plants in
`code/species_remainder_f8fa/run_all.sh`, whose only ticket id is twelve lines away, and
**P11b** keeps the original site as an explicit probe *of the rule*, predicted 0 and measured 0.

**This is the fourth recorded instance in this arc of a marker disarming a checker by
accident** — `w3_scope.py`'s bare *"REPAIRED"*, `c4_scope.py`'s *"is not the framework this
ticket is about"*, `s1_extent.py`'s own control (d), and now this. It is also exactly why
`e2_crosssection.py` does **not** use a ticket-id window: its control (c) measures that
mg-a4ef's ±6-line rule, applied to B1, is **disarmed by an unrelated `mg-6f61` five lines
below** — so the one occurrence in this repository that had to fire would not have.

## Three defects in this instrument, kept

Two of the three would have **inverted** a result — the shape mg-7dd3 recorded five of, one
audit earlier.

1. **E2's control (a) truncated the document instead of editing it.** The first version spliced
   §0's misquotation back in by writing `doc[:cut] + B1`, which **deleted §4's strike along with
   the rest of the file**. The control reported *"0 findings, expected 1"* — the detector was
   fine and the control had removed the strike it was testing for. A control that deletes its
   own subject reports a working detector as broken.

2. **E2's control (a), second version, restored the false belief *beside its correction*.** It
   inserted the misquotation into the paragraph that now says *"MISQUOTATION. The book's species
   is `Π*` in both slots"* — so the occurrence was exonerated, correctly, and the control still
   read 0. **Restoring a false belief next to its retraction does not restore the false belief**,
   which is the whole of B1 said backwards. The control now reverses the repair.

3. **The `open`-tracer subtracted reads it should have kept — twice.** First it dropped the
   checker's own path unconditionally, which hid the fact that `s1_extent.py` reads its own
   source **as a target** (its file sits in one of the four trees it scans) and made E1 report
   that checker's printed file count as **false**. A skip-once for *"runpy's own read"* was
   added — and `runpy` does not read through `builtins.open` at all, so the skip was never
   consumed by runpy and swallowed the genuine self-read instead. The self-test caught the
   second one (`the tracer records a SELF-read as a target`). The tracer now subtracts nothing.

   **This is the same defect as the ticket's own subject, in the instrument measuring it**: an
   exclusion applied by a rule that no printed sentence carried. mg-7dd3 recorded the identical
   near-miss — an `open`-tracer that counted `shutil.copytree`'s binary reads and would have
   hidden the `run_all.sh` hole. Binary reads are now counted and reported separately for that
   reason.

4. **A control that searched for its subject by fragment matched the wrong line.** E2's control
   (c) located the restated sentence by looking for `"is the algebra of"` and matched AM
   §10.10's *"`A/J` is the algebra of flats"* **78 lines earlier**, then reported the ±6-line
   ticket-id rule as *not* disarmed — the opposite of the truth. It now uses the line control
   (a) actually reported.

## What went right, and is worth keeping

* **Every one of the five checkers is now green in both directions**: inside the claimed extent
  the mutation fires, outside it the checker stays silent. Per checker, in `E3b`.
* **P9 and P14 are mg-7dd3's M12 and M16**, the two probes that exited **0** against the parent
  commit and are the whole of findings A1 and A2. Both now exit **1**.
* **P13 and P12 are the extent being true in the other direction**: a named exclusion and a
  declared-silent tree, both silent, both printed by the run.
* **E1 found no false extent line after the repairs** — 20 comparisons, every one measured
  against an instrumented `open` rather than read off the source.
