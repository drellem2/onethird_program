# `code/species_extent_audit_6cb9` — all four extents, both ways, and the cross-section check made to fire

**Work item:** mg-6cb9. **Audits:** mg-d633 (`e8fbd4f`), which repaired mg-7dd3 (`798afb7`)
against mg-a4ef (`106e121`).

```
sh code/species_extent_audit_6cb9/run_all.sh      # ~3 min, no network
```

> **This instrument mutates the worktree it runs in.** One edit at a time, applied on disk and
> undone, with `git status --porcelain` captured before every probe and compared after it. Any
> difference stops the run with exit 2. Run it on a clean tree.

## Why on disk and not in a sandbox

mg-d633's own E3 mutates a `shutil.copytree` sandbox, and that sandbox has no `.git`. So
`s1_extent.py`'s controls **(a)** at `ebecd89` and **(b)** at `83ac472` take their `git archive`
failure branch and print *"git unavailable — SKIPPED"* in **every one of E3's 28 probes**; since
`s1_extent.py` does `bad += ctl`, those two controls contribute nothing to any exit code E3
recorded, and E3's table does not carry that. Probing a checker with two of its four controls
silently disarmed is probing a different checker. A1f measures this both ways.

## The scripts

| file | what it does |
|---|---|
| `kern6cb9.py` | the probe: one edit, applied and undone, with the undo verified |
| `a1_bothways.py` | **all four extents, IN and OUT, at 29 sites of my own choosing** |
| `a2_crosssection.py` | **the cross-section check shown FIRING** (3 ways) and SILENT (4 ways) |
| `a3_differ_and_placement.py` | every *"the answer would differ under X"*, with X made; anchors; placement; thresholds |
| `selftest6cb9.py` | 33 assertions, over half of them that something does **not** happen |

`A1`, `A2` and `A3 TOTAL BAD` are **not zero and are not meant to be**: each counts the findings
this audit reports. Each is followed in the output by its own extent.

## What it found

| # | finding |
|---|---|
| 1 | *"EVERY REGULAR FILE in each tree is read"* is **true only because no species tree has a subdirectory.** Both repaired scans use a non-recursive `os.listdir` and skip directories **by a rule no sentence carries** — the exact shape mg-d633 removed one layer up. `e1_extents.py`, the file whose job is checking printed extents, has the same blind spot. Q10, Q17, Q17e |
| 2 | **The cross-section check is real and it fires** — 3 IN probes red, 4 OUT probes silent, in two documents. Not vacuous |
| 3 | …and it is reachable **by reading and not by running**: named in every artifact, called by **0 of 3** species-tree `run_all.sh`. The trees whose checkers were green while B1 stood still cannot run it. A2d |
| 4 | The committed `out_e2_crosssection.txt` says **100 markdown files**; the tree it ships in has **105**. The run was produced at `c7f9673`, **three commits before the commit that ships it** — confirmed independently by its Bratteli line numbers. The census is right, so the verdict survives; the **extent line** is false. A2c |
| 5 | `check_doc.py`'s C4 is a **presence test** over a document that writes **3 of its 5 anchors more than once** (19, 3 and 2 copies). Deleting the copy a reader reads leaves the run green. This is where my own prediction Q2 missed. A3b |
| 6 | `check_doc.py`'s repair was a **claim narrowing** and nothing guards it at its own site: making it read two more files changes nothing it prints or exits. A3a D4 |
| 7 | **The seam is `e2`'s `RUN_MIN`, and it is two tokens wide.** A 7-token strike in the document B1 lived in, restated **verbatim** in another section, is silent — measured. `e2`'s extent names two holes and not this one. A3d |
| 8 | mg-d633's `s2_seam.py` probes are all **exact** duplicates, so all three fire on the 90 % pass it added; the **45 % sweep is exercised by no probe in that instrument**. Q20 fires it, at 47.5 % over 423 characters |

## What did not break

Three widened the code, one narrowed the claim, **and all four say which** — in the run a reader
reads and in the source (A1g). Every deletion test moves the artifact (A3a D1–D3). Disarming
`e2`'s rule turns `e2` red through its own controls (D5). B1 is fixed at §0 and the correction is
in the paragraph that carried it. mg-d633's 37-point margin on the 90 % pass reproduces.

## What this does not cover, named

* **29 probes is not an extent verified at every point.** The sites are mine and are listed by
  name in the output so a successor can see which regions were never touched.
* **No probe plants two mutations at once**, and none tests a checker against a mutation of its
  own source.
* **Every `e2` probe restates VERBATIM**, because that is all `e2` matches. Paraphrase is
  untested here and is named as untested there.
* **A3a can only test flip conditions the code STATES.** An unstated one cannot be tested this
  way; its absence is reported instead.
* **Reachable is not read.** A3c measures whether a correction sits in the artifact carrying the
  false belief. Whether anyone reads it is not measurable here.

## Predictions

`PREDICTIONS.md` was written after reading `e8fbd4f`'s source and before executing a single
probe, and is not edited afterwards. **3 of 36 were wrong** and are kept as written; `OUTCOMES.md`
scores them and records the **three defects in this instrument itself, one of which inverted a
result**.
