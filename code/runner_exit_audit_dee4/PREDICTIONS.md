# mg-dee4 — every count, with when it was written

Written before `run_all.sh` was first run end-to-end. Each row carries its
**provenance**, because a prediction with no timestamp is a claim about the
author's memory and not about the subject:

* **PREDICTED** — written down before the probe that measures it existed.
* **MEASURED FIRST** — found during reconnaissance, before the probe was
  written. Recorded as such rather than dressed up as a prediction. Reading
  a figure and then "predicting" it is the defect this arc keeps finding,
  one level up from the code.
* **INHERITED** — mg-7522's own figure, taken as the thing to be checked.

The misses are kept in `OUTCOMES.md` as written. One is already recorded
below (**P4**) and it went the wrong way for me: I predicted a hole and
measured none.

---

## A1 — the population, and what is outside it

| id | provenance | claim |
|---|---|---|
| **P1** | INHERITED | mg-7522's table at `bee07a1`: P0 **72**, P1 **23** files / **53** pipelines, P2 **19** / **26**, shape **19** / **42**, name **17** / **34** |
| **P2** | PREDICTED | every one of those five re-derives **identically** under a parser written from scratch |
| **P3** | MEASURED FIRST | tracked files that are shell scripts but do **not** end in `.sh`: **0**, so `ls_sh`'s extension rule loses nothing in this repository |
| **P4** | PREDICTED — **MISSED** | at least **1** P2 pipeline at the pin lies outside mg-7522's "corrected population of 45". Measured: **0**. The 45 covers P2 entirely. |
| **P5** | MEASURED FIRST | shell-executing call sites in all tracked `*.py`: **1** (`code/state_landing_audit_bd41/instrument_sensitivity.py:33`), carrying **0** pipelines |
| **P6** | MEASURED FIRST | pipelines at HEAD dropped from P2 by `guarded()`: **0** |
| **P7** | MEASURED FIRST | pipelines at HEAD dropped from P2 by **`has_set_e` alone**: **2**, both in `code/branching_audit_a218/c0_repro.sh` — a file that is not `run_all.sh`, has no `| tee`, and has no `set -e`, so **all three rules miss it** |
| **P8** | PREDICTED | of those 2, at least **1** has its pipeline's result consumed and reaching the script's own exit status |

## A2 — the statuses, read directly

| id | provenance | claim |
|---|---|---|
| **P9** | INHERITED | "the 11 discarded statuses read directly, **11 of 11** exit 0" |
| **P10** | MEASURED FIRST | the 3 `git diff` rows are a **hand-list** of 3 argv, while the 3 source lines sit in `for` loops and execute **8** discarded `git diff`s at run time |
| **P11** | MEASURED FIRST | the row labelled `state_delegation_audit_16eb/run_all.sh:39` runs a command that is **not on line 39** — line 39 carries the `':!*.md'` pathspec and the argv has none |
| **P12** | PREDICTED | all **8** runtime `git diff` executions exit **0**, so the clearance's substance survives at the finer grain |
| **P13** | PREDICTED | the 8 `\| tee` rows **are** direct: derived from `tee_pipelines` + `invocation`, not hand-listed |
| **P14** | PREDICTED | the "byte counts unchanged, **verified** against the pre-repair output (`0 / 0 / 0 / 0 / 2111 / 0`)" claim **holds** on both arms — and **no probe in mg-7522's tree prints it** |

## A3 — the anchor

| id | provenance | claim |
|---|---|---|
| **P15** | PREDICTED | `k2_consume.py`'s census is unpinned (`CALLER_REF = None`) **and** its classification and `s4_unpin.py`'s comparison keep `bee07a1`. The moving-baseline defect is **not** reintroduced. |
| **P16** | PREDICTED | old caller anchor (pin) finds strictly **fewer** sites than the new one (HEAD) over the same rule |
| **P17** | PREDICTED | the repaired target rule `(?:run_all\|run_audit)\.sh` is still a **name** rule; the property rule `\w+\.sh` finds at least **5** more sites at HEAD |
| **P18** | MEASURED FIRST | the published document's *"the byte-comparison sees **154 changed files**"* matches **no** anchor: `s4`'s own transcript prints **166**, and the same measurement on `main` today is **263** |

## A4 — the repair's own strongest wording

| id | provenance | claim |
|---|---|---|
| **P19** | INHERITED | "**0 uses**, 19 mentions" of a strength marker |
| **P20** | MEASURED FIRST | the D4 population is `MINE_PY + MINE_SH` — the tree's `README.md`, `OUTCOMES.md`, `PREDICTIONS.md` and the **published document** are outside it |
| **P21** | MEASURED FIRST | `lib7522._STRENGTH` has **3** alternatives; `s3_figure.MARK`, the rule applied to the *subject*, has **9**. **"verified"** is named in the D4 docstring, in the README and in the document, and is **absent from the rule that produces the 0** |
| **P22** | PREDICTED | running mg-7522's own `MARK` + `NUM` over mg-7522's own artifacts yields **> 0** strength-marked numeric claims, none of them dispositioned |
| **P23** | MEASURED FIRST | the repair's **commit message** says *"18 strength-marked numeric claims … FOUR WRONG"*; its own transcript says **20** and **5** |

## A5 — the floor: one thing no list in the ticket names

I chose **the instrument mg-7522 edited underneath mg-05eb's citations.**
mg-7522 changed `libc2b3.PIPEFAIL_RE`, `k1_census.py`, `k2_consume.py` and
`selftestc2b3.py`, and deliberately did **not** regenerate their transcripts.
Nothing in the ticket asks whether those probes still *run*.

| id | provenance | claim |
|---|---|---|
| **P24** | PREDICTED | `selftestc2b3.py` at HEAD exits **0** |
| **P25** | PREDICTED | `k1_census.py` at HEAD exits **0**, and its `pipefail` row now reads ticket **1** / re-derived **1** / **AGREES** where the committed transcript reads **DIFFERS** |
| **P26** | PREDICTED | `k2_consume.py` at HEAD exits **0** |
| **P27** | PREDICTED | both repaired runners, `code/face_geometry_audit_f1b2/run_audit.sh` and `code/face_geometry_audit_fcf1/run_audit.sh`, exit **0** at HEAD |

## Exit codes, predicted before the run

| probe | predicted | why |
|---|---|---|
| `selftestdee4.py` | **0** | both senses at every rule |
| `a1_outside.py` | **0** | P7/P8 are findings about mg-7522's predicate, reported, not counted BAD |
| `a2_direct.py` | **1** | P10/P11 are a grain error in a claim that says *directly* |
| `a3_anchor.py` | **1** | P18: a prose figure no anchor reproduces |
| `a4_superlatives.py` | **1** | P20/P21: the rule that produces `0 USES` is narrower than the definition it is printed under |
| `a5_floor.py` | **0** | I expect the edited instrument to still run |
