# mg-7522 — predictions

**This file states WHEN each row was written, because this repair is about
populations and provenance and a prediction with no timestamp is a claim about
the author's memory.** Three states:

| state | meaning |
|---|---|
| **PREDICTED** | written before the probe that measures it was run |
| **INHERITED** | a figure taken from mg-05eb's audit rather than predicted; re-derived here from a parser written from scratch, and the agreement (or not) is the row |
| **MEASURED FIRST** | this number was scanned exploratorily before the probe existed, so it is **not** a prediction and is not scored as one |

mg-05eb's own OUTCOMES records that its two prediction misses were *"the two
where I inherited the sweep's answer instead of measuring it"*. Inheriting is
not the defect; **inheriting silently** is. So every inherited row says so.

---

## S1 — the population

| | state | prediction |
|---|---|---|
| **Q1** | INHERITED | tracked `*.sh` at `bee07a1`: **72** |
| **Q2** | INHERITED | of which named `run_all.sh`: **64** |
| **Q3** | INHERITED | files with a real `\| tee` pipeline at `bee07a1`: **19**, pipelines **42** |
| **Q4** | INHERITED | of those, in a `run_all.sh`: **17** files, **34** pipelines |
| **Q5** | INHERITED | outside the name rule: **2** files, **8** pipelines |
| **Q6** | MEASURED FIRST | P2 (status consumed *and* discarded stage can fail) at `bee07a1`: **19** files, **26** lines |
| **Q7** | PREDICTED | the set missed by the NAME rule and the set missed by the SHAPE rule are **disjoint**, and **neither is empty** |
| **Q8** | PREDICTED | P2 at HEAD after this repair: **0** files, **0** lines |
| **Q9** | PREDICTED | tracked `*.sh` at HEAD is **more** than 72 — the arc has grown since the pin, which is the same fact that makes a pinned census stale |

## S2 — the status the pipelines discarded

| | state | prediction |
|---|---|---|
| **Q10** | PREDICTED | all **11** pipelines outside mg-c2b3's population exit **0** when their discarded stage is run directly |
| **Q11** | PREDICTED | PRE-repair positive control: **8 of 8** sites SWALLOW — runner exits 0 *and* every later step still runs |
| **Q12** | PREDICTED | REPAIRED positive control: **8 of 8** sites CAUGHT — runner exits non-zero *and* no later step runs |
| **Q13** | PREDICTED | **0** committed transcripts move: `> f` and `\| tee f` write the same bytes |
| **Q14** | PREDICTED | at **0** of the 8 sites does the pre-repair runner exit non-zero for an unrelated later reason (mg-c2b3 found 8 such in its own 34; these two runners have no `grep` steps, so the conjunction should be redundant here — and if it is, that is worth saying, because it means the exit-code column alone would have been enough *for this population and not for the sweep's*) |

## S3 — the figure

| | state | prediction |
|---|---|---|
| **Q15** | MEASURED FIRST | `pipefail` under mg-c2b3's regex over `run_all.sh` at `bee07a1`: **0** |
| **Q16** | MEASURED FIRST | under the repaired regex: **1**, and the ticket said **1** |
| **Q17** | MEASURED FIRST | `#!/bin/sh` on `run_all.sh` at `bee07a1`: **59 of 64**, so *"all 64 (measured)"* is false |
| **Q18** | PREDICTED | strength-marked numeric claims in mg-c2b3's reader-facing artifacts: **10 to 20** |
| **Q19** | PREDICTED | of those, **4** were wrong (two `pipefail` rows, the shebang sentence, the `k1_census.py` docstring) |

## S4 — the anchor

| | state | prediction |
|---|---|---|
| **Q20** | PREDICTED | `code/species_depth_audit_4700/` appears in **exactly one** cell of the anchor × rule 2×2, namely (HEAD, runtime-path) |
| **Q21** | PREDICTED | therefore **unpinning alone is not sufficient** — the ticket's remedy names one of two independent reasons |
| **Q22** | PREDICTED | the pinned byte-comparison sees **strictly more** than the HEAD-anchored one, which is why its pin stays |
| **Q23** | INHERITED | `code/species_depth_audit_4700/out_q2_wiring.txt` contains **2** `SWALLOWED` rows naming affected runners |

## S5 — this tree, checked for the defects it repairs

| | state | prediction |
|---|---|---|
| **Q24** | PREDICTED | this tree's own `run_all.sh` contains **0** pipelines of any kind, and every step redirects and guards |
| **Q25** | PREDICTED | **0** real `shell=True` / `os.system(` call sites |
| **Q26** | PREDICTED | **0** USES of a strength marker, and a non-zero number of MENTIONs — this tree's subject *is* those words |

---

## Misses, kept as written

Filled in after the run. See `OUTCOMES.md`.
