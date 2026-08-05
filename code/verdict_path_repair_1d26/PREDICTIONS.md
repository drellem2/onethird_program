# mg-1d26 — PREDICTIONS, written and committed BEFORE ANY SCRIPT OF THIS REPAIR EXISTS

This file is the whole content of its commit. The tree of that commit contains
this file and nothing else of this instrument: no kernel, no probe, no runner,
no transcript. Everything else in `code/verdict_path_repair_1d26/` arrives in a
later commit and is scored against what is written here, unedited.

**A refuted prediction is a RESULT.** Nothing below is revised because the
measurement disagreed. `OUTCOMES.md` scores every line of this file against the
transcripts and keeps the misses as written.

---

## What this ticket is

mg-d53d, auditing the mg-4adb deletion-population repair, reported that the
verdict path is 806 lines and that mg-4adb's certificate covers 255 of them —
and that **six deletions outside the certified 255 turn a red gate green, four
of them silently.** The most valuable of the six is `e2_crosssection.py:52`,
`FILES += _f`: delete it and the checker **reads no document, says nothing and
returns 0.**

**Every figure in that paragraph is mg-d53d's.** I have run none of it. This
instrument re-derives each of them from the source before it uses any of them,
and where the re-derivation disagrees the disagreement is the finding.

---

## MEASUREMENTS ALREADY TAKEN, disclosed as measurements and not laundered into predictions

These four were made **before this file was written**, by reading files and by
running `e2_crosssection.py` once at `a8eaf2a`. They are disclosed here so that
a reader can see they were not predicted. They are scored in `OUTCOMES.md` as
DISCLOSED, never as hits.

* **D1.** `wc -l` at `a8eaf2a` over the five files mg-d53d names: 83, 85, 87
  (the three runners, 255), `e2_crosssection.py` 299, `kernd633.py` 252.
  Total 806. mg-d53d's 806 and its 255 are arithmetically reproduced at the
  **line** grain, on the **file list mg-d53d chose**. Whether that list is the
  right one is P1's question and is **not** settled by this.
* **D2.** **The tree is ALREADY RED at `a8eaf2a` and neither mg-4adb nor
  mg-d53d's clean-tree control is true today.** `python3
  code/species_extent_d633/e2_crosssection.py` at `a8eaf2a` exits **1** with
  `E2 TOTAL BAD: 1`, over one STANDING occurrence in
  `code/face_geometry_repair_e35b/README.md` — strike at line 39, restated live
  at line 36, planted by nobody. mg-4adb's V1b row (`3 of 3 runners are GREEN on
  a clean tree`) and mg-d53d's G1b row (`3 of 3 runners GREEN on a clean tree
  and e2 silent`) were both true when they were run and are **false of this
  tree**. This is not a defect of this ticket's subject and is **not repaired
  here** — it is a live cross-section finding doing exactly what e2 exists to do.
* **D3.** e2 at `a8eaf2a` examines **264 markdown files**, 18 of which carry at
  least one strike, 37 strikes measured. Population: `*.md` under `docs/` and
  `code/`, recursively. Grain: **file**, and **37 is the strike grain**, which
  is a different grain over the same population.
* **D4.** `kernd633.py` imports only `os`, `re`, `shutil`, `subprocess`, `sys`
  and `e2_crosssection.py` imports only those plus `kernd633`. Read from the
  source, not run.

---

## THE POPULATION, and why it is re-derived rather than inherited

The defect is that the certified population was **narrower than believed**. A
repair that re-uses the certification's own boundary reproduces the error. So
`p1_population.py` derives the verdict path by a **rule**, from the runner
outward:

> the verdict path is the runner file, plus the script its **last command**
> invokes, plus the transitive closure of that script's **repository-local
> imports**.

and prints the closure it walked, file by file, with the line count of each and
the grain of every number beside it.

* **P1a.** The rule above, applied at `a8eaf2a`, yields **exactly five files**
  and **806 lines** — the same five mg-d53d names. *(A reproduction. If it
  yields more, the hole is wider than mg-d53d's too, and that is the finding.)*
* **P1b.** The closure step adds **nothing** beyond `kernd633.py`: no
  repository-local import of `e2_crosssection.py` or of `kernd633.py` is
  unresolved, and `trace_open.py`, `e1_extents.py` and `e3_bothways.py` are
  **not** on the verdict path.
* **P1c.** mg-4adb's certified population, parsed out of its own committed
  `out_v1_population.txt`, is **255 rows over 3 files**, so **551 lines of the
  verdict path have no certificate**. Grain: **line**.
* **P1d.** The last command of all three runners is
  `python3 ../species_extent_d633/e2_crosssection.py`, asserted against the
  source and not against a comment.

---

## THE BEFORE-STATE, re-derived and not quoted

`p2_widened.py` sweeps **every line of `e2_crosssection.py` and `kernd633.py`**,
deleted one at a time, in a `git clone --shared` sandbox, with a strike planted
by this instrument, at the **pre-repair** content of those two files and again
at the repaired content.

The pre-repair content is carried in this directory as
`pre1d26_e2_crosssection.py` and `pre1d26_kernd633.py`, **byte-identical copies**
committed beside the probes — *not* a SHA. The refinery rebases, so a recorded
SHA is displaced on `main` and an ancestry check gives a false negative
(mg-c067, mg-a74f). Content cannot be displaced.

* **P2a.** Over the 551 pre-repair lines the sweep finds **exactly 6** deletions
  that leave e2 exiting 0 with the strike live, and they are the six mg-d53d
  names: `e2:52`, `e2:144`, `e2:299`, `kernd633:127`, `kernd633:196`,
  `kernd633:205`. *(A reproduction, by an instrument that does not read
  mg-d53d's transcripts for it.)*
* **P2b.** **4 of the 6 are silent** — the finding sentence `STANDING UN-STRUCK`
  is absent from the output — and they are `e2:52`, `kernd633:127`,
  `kernd633:196` and `kernd633:205`.
* **P2c.** The mechanism of `kernd633:127` is **directional**: `spans.append((prev,
  len(text)))` is the span AFTER the last strike, so deleting it makes every
  restatement that FOLLOWS its own strike invisible. E2b's five existing
  controls all restate **before** the strike, which is why all five stay green
  while the detector is half blind. *(A mechanism prediction. It is wrong if any
  of E2b's five controls fails when line 127 is deleted.)*
* **P2d.** `e2:52` deleted makes `len(FILES)` **0**, and the pre-repair e2 prints
  no row, no finding, and exits **0**.

## THE REPAIR

* **P3a.** After the repair, the sweep over the **whole widened population** —
  every line of both repaired files — finds **0** deletions that leave e2
  exiting 0 with the strike live.
* **P3b.** Each of the six lines, deleted at the repaired tree, is run through
  **all three species runners**: **18 of 18 exit non-zero.** A claim that the
  hole is closed with no per-case demonstration is what this arc's audits keep
  refuting, so every one of the eighteen is a printed row.
* **P3c.** The repaired e2 **cannot exit 0 over an empty population.** Run
  against a tree with no markdown at all it exits non-zero and prints a sentence
  that distinguishes *checked and found nothing wrong* from *found nothing to
  check*. The pre-repair e2, given the same tree, exits **0**.
* **P3d.** The repaired e2 prints its population size on **every** run,
  including the runs where it exits 0, so a vacuous pass is visible in the
  output rather than inferable only by reading the code.
* **P3e.** The repair grows the verdict path. I predict the post-repair path is
  **more than 806 and fewer than 950 lines**, and that P3a holds over all of it —
  including every line the repair itself adds.
* **P3f.** The repair adds **no exclusion list**. The post-repair sweep's
  population is every line of both files, as the pre-repair sweep's was.

## WHAT I EXPECT TO GET WRONG

* **P4a.** If P2a misses, it misses in the direction of **MORE than six** —
  because that is the direction all four of mg-d53d's own misses went, and
  because the tree has grown by many commits since mg-d53d ran.
* **P4b.** At least one of the six is **not** reproduced as mg-d53d classified
  it: I predict `kernd633:196` and `kernd633:205` are structurally suspect,
  because deleting a `for` header or an `else:` from an indented block is a
  candidate for `IndentationError`, which would exit **1** and be a *held* gate,
  not a lost one. If they reproduce as GATE LOST, my reading of them was wrong.
* **P4c.** The first post-repair sweep goes **red on its first run** — some line
  of the repair is itself a hole. I expect to find it by running the sweep and
  not by reading.

## WHAT THIS WILL NOT DO, stated in advance so it is not read as covered

1. **Deletions are one line at a time.** Two lines deleted together, and a line
   *edited* rather than removed, are outside every number this instrument prints.
2. The population is the **verdict path of the e2 cross-section gate**. The
   other checkers each runner calls — `s1_extent.py`, `w3_scope.py`,
   `r2_columns.py` and the rest — are outside it, and so is
   `code/species_7d75/run_all.sh`, which mg-d53d's G5 leaves open and this
   ticket does not name.
3. **D2's live finding is not repaired.** It is reported, and the fact that both
   parent instruments' clean-tree controls are false of this tree is reported
   with it.
4. mg-d53d's G2 sentinel item (`(cannot be told from the output)` counted as a
   member of the set of catcher names) is **mg-d53d's own instrument**, not the
   gate, and is not touched here.
